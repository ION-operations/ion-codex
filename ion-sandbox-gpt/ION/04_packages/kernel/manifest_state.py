"""Bounded manifest / route-state persistence for the live ION kernel stack.

This module does not claim a full autonomous route planner already exists. It lands the
next truthful runtime layer after B3: machine-readable manifest / route-state records that
can be persisted, reviewed, and recovered without collapsing into continuity prose or
automation-stage narration.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re

from .index import KernelIndex
from .model import (
    ManifestModeBinding,
    ManifestRouteStateRecord,
    EvidencePressure,
    RouteBranch,
    RouteFrame,
    RouteOwnerScope,
    RoutingAssessment,
)
from .store import KernelStore
from .threshold import AutomationStage, ContextMode, RouteStage


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")
_ALLOWED_BRANCH_STATUSES = frozenset(stage.value for stage in RouteStage)
_ALLOWED_LOOP_POSITIONS = frozenset({
    "CONTEXTUALIZE",
    "REFLECT",
    "PLAN",
    "GATE",
    "EXECUTE",
    "AUDIT",
    "DELIVER",
})


class KernelManifestRouteStateError(Exception):
    """Raised when one bounded manifest / route-state operation fails."""


@dataclass(frozen=True)
class ManifestRouteStatePreparation:
    record: ManifestRouteStateRecord
    replaced_existing: bool


@dataclass(frozen=True)
class ManifestRouteStateResult:
    preparation: ManifestRouteStatePreparation
    persisted_record: ManifestRouteStateRecord


class KernelManifestRouteStateManager:
    """Persist bounded manifest / route-state records in the kernel store."""

    def prepare_record(
        self,
        index: KernelIndex,
        *,
        owner_scope_type: str,
        owner_scope_id: str,
        steward: str,
        mission: str,
        governing_refs: tuple[str, ...] = (),
        loop_position: str = "CONTEXTUALIZE",
        branches: tuple[RouteBranch, ...] = (),
        context_mode: ContextMode = ContextMode.IDE_MANUAL,
        automation_stage: AutomationStage = AutomationStage.MANUAL,
        recent_evidence_refs: tuple[str, ...] = (),
        unresolved_issue_refs: tuple[str, ...] = (),
        blocker_refs: tuple[str, ...] = (),
        drift_flags: tuple[str, ...] = (),
        route_confidence: str = "MEDIUM",
        branching_stability: str = "STABLE",
        recommended_action: str = "CONTINUE",
        reasons: tuple[str, ...] = (),
        active_branch_id: str | None = None,
        handoff_summary: str | None = None,
        next_route_proposal: str | None = None,
        linked_automation_state_id: str | None = None,
        manifest_id: str | None = None,
        manifest_version: str = "1.0",
        created_at: str | None = None,
        updated_at: str | None = None,
        notes: str | None = None,
    ) -> ManifestRouteStatePreparation:
        owner_scope_type = owner_scope_type.strip().upper()
        owner_scope_id = owner_scope_id.strip()
        steward = steward.strip()
        mission = mission.strip()
        loop_position = loop_position.strip().upper()
        if not owner_scope_type or not owner_scope_id or not steward:
            raise KernelManifestRouteStateError("owner scope type, owner scope id, and steward are required")
        if not mission:
            raise KernelManifestRouteStateError("mission is required")
        if loop_position not in _ALLOWED_LOOP_POSITIONS:
            raise KernelManifestRouteStateError(f"Unsupported loop_position: {loop_position}")
        if context_mode is ContextMode.IDE_MANUAL and automation_stage is AutomationStage.RUNTIME_ACTIVE:
            raise KernelManifestRouteStateError("RUNTIME_ACTIVE manifest posture requires COMPILED_RUNTIME context mode")

        normalized_branches = tuple(branches)
        branch_ids = {branch.branch_id for branch in normalized_branches}
        if len(branch_ids) != len(normalized_branches):
            raise KernelManifestRouteStateError("branch ids must be unique within one manifest record")
        active_count = 0
        for branch in normalized_branches:
            if branch.status not in _ALLOWED_BRANCH_STATUSES:
                raise KernelManifestRouteStateError(
                    f"Unsupported branch status for {branch.branch_id}: {branch.status}"
                )
            if branch.status == RouteStage.ACTIVE.value:
                active_count += 1
            if branch.status == RouteStage.ABANDONED.value and not (branch.abandonment_reason or "").strip():
                raise KernelManifestRouteStateError(
                    f"ABANDONED branch requires abandonment_reason: {branch.branch_id}"
                )
        if active_branch_id is not None:
            if active_branch_id not in branch_ids:
                raise KernelManifestRouteStateError("active_branch_id must reference a known branch")
            if active_count != 1:
                raise KernelManifestRouteStateError("active_branch_id requires exactly one ACTIVE branch")
        elif active_count > 1:
            raise KernelManifestRouteStateError("only one ACTIVE branch is allowed per manifest record")

        manifest_id = manifest_id or manifest_route_state_id(owner_scope_type, owner_scope_id)
        existing = index.get("manifest_route_state", manifest_id)
        timestamp = updated_at or _iso_now()
        record = ManifestRouteStateRecord(
            manifest_id=manifest_id,
            manifest_version=manifest_version,
            created_at=created_at or getattr(existing, "created_at", timestamp),
            updated_at=timestamp,
            owner_scope=RouteOwnerScope(
                scope_type=owner_scope_type,
                scope_id=owner_scope_id,
                steward=steward,
            ),
            mode_binding=ManifestModeBinding(
                context_mode=context_mode.value,
                automation_stage=automation_stage.value,
            ),
            route_frame=RouteFrame(
                mission=mission,
                governing_refs=tuple(governing_refs),
                loop_position=loop_position,
                active_branch_id=active_branch_id,
                handoff_summary=handoff_summary,
                next_route_proposal=next_route_proposal,
            ),
            branches=normalized_branches,
            evidence_pressure=EvidencePressure(
                recent_evidence_refs=tuple(recent_evidence_refs),
                unresolved_issue_refs=tuple(unresolved_issue_refs),
                blocker_refs=tuple(blocker_refs),
                drift_flags=tuple(drift_flags),
            ),
            routing_assessment=RoutingAssessment(
                route_confidence=route_confidence,
                branching_stability=branching_stability,
                recommended_action=recommended_action,
                reasons=tuple(reasons),
            ),
            linked_automation_state_id=linked_automation_state_id,
            notes=notes,
        )
        return ManifestRouteStatePreparation(record=record, replaced_existing=existing is not None)

    def upsert_record(self, store: KernelStore, index: KernelIndex, **kwargs: object) -> ManifestRouteStateResult:
        preparation = self.prepare_record(index, **kwargs)
        if preparation.replaced_existing:
            store.replace(preparation.record)
            index.record_changed(preparation.record)
        else:
            store.create(preparation.record)
            index.record_added(preparation.record)
        return ManifestRouteStateResult(preparation=preparation, persisted_record=preparation.record)

    def render_report(self, record: ManifestRouteStateRecord) -> str:
        lines = [
            f"# Manifest Route State — {record.manifest_id}",
            "",
            f"- Scope: {record.owner_scope.scope_type}:{record.owner_scope.scope_id}",
            f"- Steward: {record.owner_scope.steward}",
            f"- Mission: {record.route_frame.mission}",
            f"- Loop Position: {record.route_frame.loop_position}",
            f"- Context Mode: {record.mode_binding.context_mode}",
            f"- Automation Stage: {record.mode_binding.automation_stage}",
            f"- Recommended Action: {record.routing_assessment.recommended_action}",
        ]
        if record.route_frame.handoff_summary:
            lines.append(f"- Handoff: {record.route_frame.handoff_summary}")
        if record.route_frame.next_route_proposal:
            lines.append(f"- Next Route Proposal: {record.route_frame.next_route_proposal}")
        if record.branches:
            lines.extend(["", "## Branches", ""])
            for branch in record.branches:
                lines.append(
                    f"- {branch.branch_id} :: {branch.label} [{branch.status}] priority={branch.priority} gate={branch.gate_class}"
                )
        if record.evidence_pressure.recent_evidence_refs:
            lines.extend(["", "## Evidence Pressure", ""])
            for ref in record.evidence_pressure.recent_evidence_refs:
                lines.append(f"- {ref}")
        if record.routing_assessment.reasons:
            lines.extend(["", "## Routing Reasons", ""])
            for reason in record.routing_assessment.reasons:
                lines.append(f"- {reason}")
        return "\n".join(lines) + "\n"


def manifest_route_state_id(owner_scope_type: str, owner_scope_id: str) -> str:
    scope_type = _SAFE_ID_RE.sub("-", owner_scope_type.lower()).strip("-") or "scope"
    scope_id = _SAFE_ID_RE.sub("-", owner_scope_id.lower()).strip("-") or "state"
    return f"manifest-{scope_type}-{scope_id}"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


IonManifestRouteStateManager = KernelManifestRouteStateManager
