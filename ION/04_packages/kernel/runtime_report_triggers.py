"""Explicit runtime-report trigger policy for the active ION kernel stack.

This module does not create a background reporter or hidden autonomous runtime. It lets
already-invoked kernel events emit selected generated artifacts automatically when the
caller supplies an explicit governed workspace root and trigger policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from .index import KernelIndex
from .runtime_report_artifacts import (
    KernelRuntimeReportArtifactEmitter,
    RuntimeReportArtifactKind,
    RuntimeReportArtifactResult,
)
from .runtime_report_governance import KernelRuntimeReportGovernanceManager
from .runtime_report_governance_aggregation import KernelRuntimeReportGovernanceAggregationManager
from .runtime_report_visibility import KernelRuntimeReportVisibilityProjector
from .runtime_state_views import KernelRuntimeStateView

if TYPE_CHECKING:
    from .runtime_state_sync import RuntimeStateSyncResult
from .model import StrEnum


class KernelRuntimeReportTriggerError(Exception):
    """Raised when one runtime-report trigger operation cannot be completed lawfully."""


class RuntimeReportTriggerEvent(StrEnum):
    PLANNER_MANIFEST_CREATED = "PLANNER_MANIFEST_CREATED"
    REVIEW_ESCALATED = "REVIEW_ESCALATED"
    GOVERNED_WRITE_SYNCED = "GOVERNED_WRITE_SYNCED"
    CAPSULE_SYNCED = "CAPSULE_SYNCED"


@dataclass(frozen=True)
class RuntimeReportTriggerRequest:
    workspace_root: str | Path
    generated_at: str | None = None
    emit_manifest_packet_on_create: bool = True
    emit_review_packet_on_escalation: bool = True
    emit_scope_status_on_governed_write_sync: bool = True
    emit_scope_status_on_capsule_sync: bool = False
    require_blocking_posture_for_scope_status: bool = True
    reflect_into_governance_ledger: bool = False
    emit_governance_summary: bool = False
    governance_ledger_path: str = "ION/05_context/history/runtime_report_trigger_ledger.json"
    governance_summaries_dir: str = "ION/05_context/runtime_reports/governance"
    promote_into_system_ledger: bool = False
    emit_operator_rollup: bool = False
    system_ledger_path: str = "ION/05_context/history/system_ledger.json"
    operator_rollups_dir: str = "ION/05_context/runtime_reports/governance/rollups"
    project_into_packet_index: bool = False
    emit_operator_dashboard: bool = False
    packet_index_path: str = "ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json"
    operator_dashboard_path: str = "ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md"


@dataclass(frozen=True)
class RuntimeReportTriggerReceipt:
    event: RuntimeReportTriggerEvent
    artifact_kind: RuntimeReportArtifactKind
    source_ref: str
    reason: str
    artifact_result: RuntimeReportArtifactResult
    governance_event_id: str | None = None
    governance_ledger_path: str | None = None
    governance_ledger_entry_index: int | None = None
    operator_summary_path: str | None = None
    operator_summary_anchor: str | None = None
    aggregation_event_id: str | None = None
    system_ledger_path: str | None = None
    system_ledger_entry_index: int | None = None
    operator_rollup_path: str | None = None
    operator_rollup_anchor: str | None = None
    visibility_event_id: str | None = None
    packet_index_path: str | None = None
    packet_index_entry_index: int | None = None
    packet_index_pointer: str | None = None
    operator_dashboard_path: str | None = None
    operator_dashboard_anchor: str | None = None


class KernelRuntimeReportTriggerManager:
    """Evaluate explicit D2 trigger policy against already-invoked runtime events."""

    def __init__(
        self,
        *,
        runtime_report_emitter: KernelRuntimeReportArtifactEmitter | None = None,
        runtime_state_view: KernelRuntimeStateView | None = None,
        runtime_report_governance_manager: KernelRuntimeReportGovernanceManager | None = None,
        runtime_report_governance_aggregation_manager: KernelRuntimeReportGovernanceAggregationManager | None = None,
        runtime_report_visibility_projector: KernelRuntimeReportVisibilityProjector | None = None,
    ) -> None:
        self._runtime_report_emitter = runtime_report_emitter or KernelRuntimeReportArtifactEmitter()
        self._runtime_state_view = runtime_state_view or KernelRuntimeStateView()
        self._runtime_report_governance_manager = runtime_report_governance_manager or KernelRuntimeReportGovernanceManager()
        self._runtime_report_governance_aggregation_manager = (
            runtime_report_governance_aggregation_manager or KernelRuntimeReportGovernanceAggregationManager()
        )
        self._runtime_report_visibility_projector = runtime_report_visibility_projector or KernelRuntimeReportVisibilityProjector()

    def emit_for_manifest_creation(
        self,
        index: KernelIndex,
        manifest_id: str,
        request: RuntimeReportTriggerRequest | None,
    ) -> tuple[RuntimeReportTriggerReceipt, ...]:
        if request is None or not request.emit_manifest_packet_on_create:
            return ()
        artifact_result = self._runtime_report_emitter.emit_planner_manifest_artifact(
            index,
            manifest_id,
            request.workspace_root,
            generated_at=request.generated_at,
        )
        return self._finalize_receipts(
            (
                RuntimeReportTriggerReceipt(
                    event=RuntimeReportTriggerEvent.PLANNER_MANIFEST_CREATED,
                    artifact_kind=RuntimeReportArtifactKind.PLANNER_MANIFEST,
                    source_ref=f"MANIFEST:{manifest_id}",
                    reason="MANIFEST_CREATED_TRIGGER_ENABLED",
                    artifact_result=artifact_result,
                ),
            ),
            request,
        )

    def emit_for_review_escalation(
        self,
        index: KernelIndex,
        question_id: str,
        request: RuntimeReportTriggerRequest | None,
    ) -> tuple[RuntimeReportTriggerReceipt, ...]:
        if request is None or not request.emit_review_packet_on_escalation:
            return ()
        artifact_result = self._runtime_report_emitter.emit_review_packet_artifact(
            index,
            question_id,
            request.workspace_root,
            generated_at=request.generated_at,
        )
        return self._finalize_receipts(
            (
                RuntimeReportTriggerReceipt(
                    event=RuntimeReportTriggerEvent.REVIEW_ESCALATED,
                    artifact_kind=RuntimeReportArtifactKind.REVIEW,
                    source_ref=f"QUESTION:{question_id}",
                    reason="REVIEW_ESCALATION_TRIGGER_ENABLED",
                    artifact_result=artifact_result,
                ),
            ),
            request,
        )

    def emit_for_runtime_state_sync(
        self,
        index: KernelIndex,
        sync_result: "RuntimeStateSyncResult",
        request: RuntimeReportTriggerRequest | None,
    ) -> tuple[RuntimeReportTriggerReceipt, ...]:
        if request is None:
            return ()
        event = _event_for_sync(sync_result.source_kind)
        if event is RuntimeReportTriggerEvent.GOVERNED_WRITE_SYNCED and not request.emit_scope_status_on_governed_write_sync:
            return ()
        if event is RuntimeReportTriggerEvent.CAPSULE_SYNCED and not request.emit_scope_status_on_capsule_sync:
            return ()

        scope_type, scope_ref = _scope_binding_for_sync(sync_result)
        if not scope_type or not scope_ref:
            return ()
        should_emit, reason = self._should_emit_scope_status(index, scope_type, scope_ref, request)
        if not should_emit:
            return ()
        artifact_result = self._runtime_report_emitter.emit_scope_status_artifact(
            index,
            scope_type,
            scope_ref,
            request.workspace_root,
            generated_at=request.generated_at,
            responding_to=f"{event.value}:{sync_result.source_ref}",
        )
        return self._finalize_receipts(
            (
                RuntimeReportTriggerReceipt(
                    event=event,
                    artifact_kind=RuntimeReportArtifactKind.SCOPE_STATUS,
                    source_ref=f"{scope_type}:{scope_ref}",
                    reason=reason,
                    artifact_result=artifact_result,
                ),
            ),
            request,
        )

    def _finalize_receipts(
        self,
        receipts: tuple[RuntimeReportTriggerReceipt, ...],
        request: RuntimeReportTriggerRequest | None,
    ) -> tuple[RuntimeReportTriggerReceipt, ...]:
        if request is None or not receipts:
            return receipts
        realized = receipts
        if request.reflect_into_governance_ledger or request.emit_governance_summary:
            realized = self._runtime_report_governance_manager.reflect_receipts(
                realized,
                workspace_root=request.workspace_root,
                created_at=request.generated_at,
                ledger_path=request.governance_ledger_path,
                summaries_dir=request.governance_summaries_dir,
                write_summary=request.emit_governance_summary,
            )
        if request.promote_into_system_ledger or request.emit_operator_rollup:
            realized = self._runtime_report_governance_aggregation_manager.aggregate_receipts(
                realized,
                workspace_root=request.workspace_root,
                created_at=request.generated_at,
                system_ledger_path=request.system_ledger_path,
                operator_rollups_dir=request.operator_rollups_dir,
                append_system_ledger=request.promote_into_system_ledger,
                write_operator_rollup=request.emit_operator_rollup,
            )
        if request.project_into_packet_index or request.emit_operator_dashboard:
            realized = self._runtime_report_visibility_projector.project_receipts(
                realized,
                workspace_root=request.workspace_root,
                created_at=request.generated_at,
                packet_index_path=request.packet_index_path,
                operator_dashboard_path=request.operator_dashboard_path,
                append_packet_index=request.project_into_packet_index,
                write_operator_dashboard=request.emit_operator_dashboard,
            )
        return realized

    def _should_emit_scope_status(
        self,
        index: KernelIndex,
        scope_type: str,
        scope_ref: str,
        request: RuntimeReportTriggerRequest,
    ) -> tuple[bool, str]:
        view = self._runtime_state_view.scope_view(index, scope_type, scope_ref)
        if not view.has_runtime_state:
            return False, "NO_RUNTIME_STATE_PRESENT"
        if scope_type == "WORK_UNIT":
            posture = self._runtime_state_view.dispatch_posture_for_work_unit(index, scope_ref)
            if posture.dispatch_permitted and request.require_blocking_posture_for_scope_status:
                return False, "DISPATCH_PERMITTED"
            if not posture.dispatch_permitted:
                return True, f"BLOCKING_RUNTIME_POSTURE::{posture.reason}"
            return True, "RUNTIME_SCOPE_STATUS_TRIGGERED"
        blockers = []
        if view.manifest is not None:
            blockers.extend(view.manifest.evidence_pressure.blocker_refs)
            blockers.extend(view.manifest.evidence_pressure.drift_flags)
        if view.automation is not None:
            blockers.extend(view.automation.blockers)
            if view.automation.current_stage in {"SUSPENDED", "DISABLED"}:
                blockers.append(f"AUTOMATION::{view.automation.current_stage}")
        normalized = tuple(dict.fromkeys(item for item in blockers if item))
        if normalized:
            return True, f"BLOCKING_SCOPE_POSTURE::{normalized[0]}"
        if request.require_blocking_posture_for_scope_status:
            return False, "NON_BLOCKING_SCOPE_POSTURE"
        return True, "RUNTIME_SCOPE_STATUS_TRIGGERED"


IonRuntimeReportTriggerManager = KernelRuntimeReportTriggerManager


def _event_for_sync(source_kind: str) -> RuntimeReportTriggerEvent:
    normalized = source_kind.strip().lower()
    if normalized == "governed_write":
        return RuntimeReportTriggerEvent.GOVERNED_WRITE_SYNCED
    if normalized == "capsule":
        return RuntimeReportTriggerEvent.CAPSULE_SYNCED
    raise KernelRuntimeReportTriggerError(f"Unsupported runtime-state sync trigger source: {source_kind}")


def _scope_binding_for_sync(sync_result: "RuntimeStateSyncResult") -> tuple[str | None, str | None]:
    manifest = sync_result.manifest_result.persisted_record
    scope_type = manifest.owner_scope.scope_type.strip().upper()
    scope_ref = manifest.owner_scope.scope_id.strip()
    if scope_type and scope_ref:
        return scope_type, scope_ref
    automation = sync_result.automation_result.persisted_record
    scope_type = automation.scope_type.strip().upper()
    scope_ref = automation.scope_ref.strip()
    if scope_type and scope_ref:
        return scope_type, scope_ref
    return None, None
