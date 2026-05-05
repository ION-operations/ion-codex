"""Bounded runtime-state query helpers for the active ION kernel stack.

This module turns persisted manifest/route-state and automation-state records into
small queryable views that other kernel services can consume directly without
pretending a larger autonomous runtime already exists.
"""

from __future__ import annotations

from dataclasses import dataclass

from .index import KernelIndex
from .model import AutomationStateRecord, CommitDelta, ManifestRouteStateRecord, WorkUnit
from .threshold import AutomationStage


_REVIEW_ACTIONS = frozenset({"REQUEST_REVIEW", "REQUIRE_REVIEW"})
_HOLD_ACTIONS = frozenset({"REQUEST_REVIEW", "HOLD", "ROLL_BACK"})
_BLOCKING_AUTOMATION_STAGES = frozenset({AutomationStage.SUSPENDED.value, AutomationStage.DISABLED.value})


@dataclass(frozen=True)
class RuntimeStateScopeView:
    scope_type: str
    scope_ref: str
    manifest: ManifestRouteStateRecord | None = None
    automation: AutomationStateRecord | None = None
    work_unit: WorkUnit | None = None

    @property
    def has_runtime_state(self) -> bool:
        return self.manifest is not None or self.automation is not None

    @property
    def state_refs(self) -> tuple[str, ...]:
        refs = []
        if self.manifest is not None:
            refs.append(self.manifest.manifest_id)
        if self.automation is not None:
            refs.append(self.automation.automation_state_id)
        return tuple(refs)

    @property
    def latest_timestamp(self) -> str | None:
        timestamps = [
            timestamp
            for timestamp in (
                getattr(self.manifest, "updated_at", None),
                getattr(self.automation, "updated_at", None),
                getattr(self.work_unit, "created_at", None),
            )
            if timestamp
        ]
        return max(timestamps) if timestamps else None

    def compact_summary(self) -> str:
        parts: list[str] = []
        if self.manifest is not None:
            parts.append(
                f"manifest={self.manifest.manifest_id} action={self.manifest.routing_assessment.recommended_action} loop={self.manifest.route_frame.loop_position}"
            )
        if self.automation is not None:
            parts.append(
                f"automation={self.automation.automation_state_id} stage={self.automation.current_stage}"
            )
        return "; ".join(parts) or "no-runtime-state"


@dataclass(frozen=True)
class RuntimeReviewPressure:
    scope_view: RuntimeStateScopeView
    requires_review: bool
    reason: str
    source_created_at: str | None
    detail_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuntimeDispatchPosture:
    scope_view: RuntimeStateScopeView
    dispatch_permitted: bool
    reason: str
    blockers: tuple[str, ...] = ()
    source_created_at: str | None = None


class KernelRuntimeStateView:
    """Read bounded manifest/automation runtime posture from the current index."""

    def scope_view(self, index: KernelIndex, scope_type: str, scope_ref: str) -> RuntimeStateScopeView:
        normalized_scope_type = scope_type.strip().upper()
        normalized_scope_ref = scope_ref.strip()
        manifests = sorted(
            index.manifest_route_states_for_owner(normalized_scope_type, normalized_scope_ref),
            key=lambda record: (record.updated_at, record.manifest_id),
        )
        automations = sorted(
            index.automation_states_for_scope(normalized_scope_type, normalized_scope_ref),
            key=lambda record: (record.updated_at, record.automation_state_id),
        )
        work_unit = None
        if normalized_scope_type == "WORK_UNIT":
            candidate = index.get("work_unit", normalized_scope_ref)
            if isinstance(candidate, WorkUnit):
                work_unit = candidate
        return RuntimeStateScopeView(
            scope_type=normalized_scope_type,
            scope_ref=normalized_scope_ref,
            manifest=(manifests[-1] if manifests else None),
            automation=(automations[-1] if automations else None),
            work_unit=work_unit,
        )

    def work_unit_view(self, index: KernelIndex, work_unit_id: str) -> RuntimeStateScopeView:
        return self.scope_view(index, "WORK_UNIT", work_unit_id)

    def review_pressure_for_delta(self, index: KernelIndex, delta: CommitDelta) -> RuntimeReviewPressure:
        view = self.work_unit_view(index, delta.work_unit_id)
        detail_refs: list[str] = []
        for reason in delta.review_reasons:
            if reason not in detail_refs:
                detail_refs.append(reason)

        if view.manifest is not None:
            detail_refs.append(view.manifest.manifest_id)
            manifest_action = view.manifest.routing_assessment.recommended_action.upper()
            manifest_reasons = tuple(reason.upper() for reason in view.manifest.routing_assessment.reasons)
            if manifest_action in _REVIEW_ACTIONS or any("REVIEW" in reason for reason in manifest_reasons):
                return RuntimeReviewPressure(
                    scope_view=view,
                    requires_review=True,
                    reason="MANIFEST_REQUESTS_REVIEW",
                    source_created_at=view.manifest.updated_at,
                    detail_refs=tuple(dict.fromkeys(detail_refs)),
                )

        if view.automation is not None:
            detail_refs.append(view.automation.automation_state_id)
            transition_reason = (view.automation.last_transition_reason or "").upper()
            pending_actions = tuple(item.upper() for item in view.automation.pending_actions)
            blockers = tuple(item.upper() for item in view.automation.blockers)
            gate_classes = tuple(gate.gate_class.upper() for gate in view.automation.active_gates)
            if "REVIEW" in transition_reason or any("REVIEW" in item for item in pending_actions):
                return RuntimeReviewPressure(
                    scope_view=view,
                    requires_review=True,
                    reason="AUTOMATION_PENDING_REVIEW",
                    source_created_at=view.automation.updated_at,
                    detail_refs=tuple(dict.fromkeys(detail_refs)),
                )
            if any("REVIEW" in item for item in blockers) or any("REVIEW" in item for item in gate_classes):
                return RuntimeReviewPressure(
                    scope_view=view,
                    requires_review=True,
                    reason="AUTOMATION_GATE_REVIEW",
                    source_created_at=view.automation.updated_at,
                    detail_refs=tuple(dict.fromkeys(detail_refs)),
                )

        if delta.review_reasons:
            return RuntimeReviewPressure(
                scope_view=view,
                requires_review=True,
                reason="DELTA_REVIEW_REASONS_PRESENT",
                source_created_at=view.latest_timestamp or delta.created_at,
                detail_refs=tuple(dict.fromkeys(detail_refs)),
            )
        return RuntimeReviewPressure(
            scope_view=view,
            requires_review=False,
            reason="NO_RUNTIME_REVIEW_PRESSURE",
            source_created_at=view.latest_timestamp or delta.created_at,
            detail_refs=tuple(dict.fromkeys(detail_refs)),
        )

    def dispatch_posture_for_work_unit(self, index: KernelIndex, work_unit_id: str) -> RuntimeDispatchPosture:
        view = self.work_unit_view(index, work_unit_id)
        blockers: list[str] = []
        if view.manifest is not None:
            action = view.manifest.routing_assessment.recommended_action.upper()
            blockers.extend(view.manifest.evidence_pressure.blocker_refs)
            blockers.extend(view.manifest.evidence_pressure.drift_flags)
            if action in _HOLD_ACTIONS:
                blockers.append(f"MANIFEST::{action}")
        if view.automation is not None:
            blockers.extend(view.automation.blockers)
            if view.automation.current_stage in _BLOCKING_AUTOMATION_STAGES:
                blockers.append(f"AUTOMATION::{view.automation.current_stage}")
        normalized = tuple(dict.fromkeys(item for item in blockers if item))
        if normalized:
            return RuntimeDispatchPosture(
                scope_view=view,
                dispatch_permitted=False,
                reason=normalized[0],
                blockers=normalized,
                source_created_at=view.latest_timestamp,
            )
        return RuntimeDispatchPosture(
            scope_view=view,
            dispatch_permitted=True,
            reason="DISPATCH_PERMITTED",
            blockers=(),
            source_created_at=view.latest_timestamp,
        )


IonRuntimeStateView = KernelRuntimeStateView
