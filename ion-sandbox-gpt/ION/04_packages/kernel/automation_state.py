"""Bounded automation-state persistence for the live ION kernel stack.

This module turns the B2 automation protocol into machine-readable kernel state without
claiming a general automation runner already exists. It makes posture, gates, fallback,
and promotion pressure durable and queryable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re

from .index import KernelIndex
from .model import AutomationGate, AutomationStateRecord
from .store import KernelStore
from .threshold import AutomationStage, ContextMode, ThresholdEvaluation


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")
_GATE_BLOCK_STATUSES = frozenset({"BLOCKED", "FAILED", "UNSATISFIED"})


class KernelAutomationStateError(Exception):
    """Raised when one bounded automation-state operation fails."""


@dataclass(frozen=True)
class AutomationStatePreparation:
    record: AutomationStateRecord
    replaced_existing: bool
    blocked_gate_ids: tuple[str, ...]


@dataclass(frozen=True)
class AutomationStateResult:
    preparation: AutomationStatePreparation
    persisted_record: AutomationStateRecord


class KernelAutomationStateManager:
    """Persist bounded automation-state records in the kernel store."""

    def prepare_record(
        self,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        current_stage: AutomationStage,
        governing_refs: tuple[str, ...] = (),
        active_gates: tuple[AutomationGate, ...] = (),
        blockers: tuple[str, ...] = (),
        promotion_criteria: tuple[str, ...] = (),
        fallback_mode: str = "MANUAL",
        last_transition_reason: str | None = None,
        operator_override: str | None = None,
        pending_actions: tuple[str, ...] = (),
        linked_manifest_id: str | None = None,
        context_mode: ContextMode = ContextMode.IDE_MANUAL,
        calibration_status: str | None = None,
        automation_state_id: str | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        notes: str | None = None,
    ) -> AutomationStatePreparation:
        scope_type = scope_type.strip().upper()
        scope_ref = scope_ref.strip()
        if not scope_type or not scope_ref:
            raise KernelAutomationStateError("scope_type and scope_ref are required")
        if context_mode is ContextMode.IDE_MANUAL and current_stage is AutomationStage.RUNTIME_ACTIVE:
            raise KernelAutomationStateError("RUNTIME_ACTIVE automation requires COMPILED_RUNTIME context mode")

        normalized_gates = tuple(active_gates)
        gate_ids = {gate.gate_id for gate in normalized_gates}
        if len(gate_ids) != len(normalized_gates):
            raise KernelAutomationStateError("gate ids must be unique within one automation-state record")
        blocked_gate_ids = tuple(
            gate.gate_id
            for gate in normalized_gates
            if (not gate.satisfied) or gate.status.upper() in _GATE_BLOCK_STATUSES
        )
        existing = index.get("automation_state", automation_state_id or automation_state_record_id(scope_type, scope_ref))
        timestamp = updated_at or _iso_now()
        record = AutomationStateRecord(
            automation_state_id=automation_state_id or automation_state_record_id(scope_type, scope_ref),
            created_at=created_at or getattr(existing, "created_at", timestamp),
            updated_at=timestamp,
            scope_type=scope_type,
            scope_ref=scope_ref,
            current_stage=current_stage.value,
            governing_refs=tuple(governing_refs),
            active_gates=normalized_gates,
            blockers=tuple(dict.fromkeys(tuple(blockers) + blocked_gate_ids)),
            promotion_criteria=tuple(promotion_criteria),
            fallback_mode=fallback_mode,
            last_transition_reason=last_transition_reason,
            operator_override=operator_override,
            pending_actions=tuple(pending_actions),
            linked_manifest_id=linked_manifest_id,
            context_mode=context_mode.value,
            calibration_status=calibration_status,
            notes=notes,
        )
        return AutomationStatePreparation(
            record=record,
            replaced_existing=existing is not None,
            blocked_gate_ids=blocked_gate_ids,
        )

    def upsert_record(self, store: KernelStore, index: KernelIndex, **kwargs: object) -> AutomationStateResult:
        preparation = self.prepare_record(index, **kwargs)
        if preparation.replaced_existing:
            store.replace(preparation.record)
            index.record_changed(preparation.record)
        else:
            store.create(preparation.record)
            index.record_added(preparation.record)
        return AutomationStateResult(preparation=preparation, persisted_record=preparation.record)

    def prepare_from_threshold_evaluation(
        self,
        index: KernelIndex,
        evaluation: ThresholdEvaluation,
        *,
        scope_type: str,
        scope_ref: str,
        governing_refs: tuple[str, ...] = (),
        linked_manifest_id: str | None = None,
        promotion_criteria: tuple[str, ...] = (),
        pending_actions: tuple[str, ...] = (),
        last_transition_reason: str | None = None,
        notes: str | None = None,
    ) -> AutomationStatePreparation:
        gates = tuple(
            AutomationGate(
                gate_id=f"gate-{_SAFE_ID_RE.sub('-', hit.condition.reason.lower()).strip('-') or 'threshold'}",
                gate_class=hit.condition.reason,
                status=("BLOCKED" if hit.triggered else "PASS"),
                satisfied=not hit.triggered,
                detail=hit.message,
                evidence_refs=tuple(str(item) for item in evaluation.snapshot.metadata.get("review_reasons", ())),
                required_for_promotion=True,
            )
            for hit in evaluation.hits
        )
        blockers = tuple(
            hit.condition.reason
            for hit in evaluation.triggered_hits
        )
        return self.prepare_record(
            index,
            scope_type=scope_type,
            scope_ref=scope_ref,
            current_stage=evaluation.snapshot.automation_stage,
            governing_refs=governing_refs,
            active_gates=gates,
            blockers=blockers,
            promotion_criteria=promotion_criteria,
            fallback_mode=("MANUAL" if evaluation.snapshot.manual_fallback_required else evaluation.snapshot.automation_stage.value),
            last_transition_reason=last_transition_reason or evaluation.recommended_action.value,
            pending_actions=pending_actions,
            linked_manifest_id=linked_manifest_id,
            context_mode=evaluation.snapshot.context_mode,
            calibration_status=evaluation.snapshot.calibration_status.value,
            notes=notes,
        )

    def upsert_from_threshold_evaluation(
        self,
        store: KernelStore,
        index: KernelIndex,
        evaluation: ThresholdEvaluation,
        **kwargs: object,
    ) -> AutomationStateResult:
        preparation = self.prepare_from_threshold_evaluation(index, evaluation, **kwargs)
        if preparation.replaced_existing:
            store.replace(preparation.record)
            index.record_changed(preparation.record)
        else:
            store.create(preparation.record)
            index.record_added(preparation.record)
        return AutomationStateResult(preparation=preparation, persisted_record=preparation.record)

    def render_report(self, record: AutomationStateRecord) -> str:
        lines = [
            f"# Automation State Report — {record.scope_type}:{record.scope_ref}",
            "",
            f"## Current Posture\nStage: {record.current_stage}",
            "",
            f"## Context and Route Binding\nContext Mode: {record.context_mode}\nRoute Surface: {record.linked_manifest_id or 'UNBOUND'}",
            "",
            "## Governing Sources",
        ]
        lines.extend(f"- {ref}" for ref in record.governing_refs)
        lines.extend(["", "## Active Gates"])
        if record.active_gates:
            lines.append("")
            for gate in record.active_gates:
                detail = f" — {gate.detail}" if gate.detail else ""
                lines.append(f"- {gate.gate_id}: {gate.status}{detail}")
        else:
            lines.extend(["", "- NONE"])
        lines.extend(["", "## Pending Actions or Queue State", ""])
        if record.pending_actions:
            lines.extend(f"- {item}" for item in record.pending_actions)
        else:
            lines.append("- EMPTY")
        lines.extend(["", "## Fallbacks and Blockers", ""])
        if record.blockers:
            lines.extend(f"- {item}" for item in record.blockers)
        else:
            lines.append("- NONE")
        lines.extend(["", "## Recommendation", "", record.last_transition_reason or "NO_CHANGE"])
        return "\n".join(lines) + "\n"


def automation_state_record_id(scope_type: str, scope_ref: str) -> str:
    clean_scope_type = _SAFE_ID_RE.sub("-", scope_type.lower()).strip("-") or "scope"
    clean_scope_ref = _SAFE_ID_RE.sub("-", scope_ref.lower()).strip("-") or "state"
    return f"automation-{clean_scope_type}-{clean_scope_ref}"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


IonAutomationStateManager = KernelAutomationStateManager
