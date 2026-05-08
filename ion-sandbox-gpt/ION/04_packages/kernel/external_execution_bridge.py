"""Supervised external execution / MCP bridge for the live ION kernel stack.

This module does not claim that external tools become kernel truth. It exposes the
already-landed dispatch/execution path to supervised external surfaces by:
- exporting one lawful external execution packet for a dispatchable work unit,
- accepting one explicit returned execution payload back into the normal execution path,
- persisting explicit bridge receipts and ledger rows.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path

from .automation_policy import (
    AutomationActionClass,
    AutomationPolicyDecision,
    AutomationPolicyEvaluation,
    AutomationPolicyRequest,
    KernelAutomationPolicy,
)
from .dispatch import DispatchPreparation, DispatchResult, KernelDispatcher, render_dispatch_packet
from .execution import ExecutionResult, ExecutionSubmission, KernelExecutor
from .graph import KernelGraph
from .id_compaction import compact_identifier
from .index import KernelIndex
from .model import StrEnum, WorkUnit
from .operator_control import (
    DaemonServiceControlMode,
    KernelOperatorControlManager,
    OperatorControlState,
)
from .store import KernelStore
from .threshold import AutomationStage, CalibrationStatus, ContextMode, PromotionAction, RouteStage


class KernelExternalExecutionBridgeError(Exception):
    """Raised when supervised external execution bridging is not lawful."""


class ExternalExecutionActionMode(StrEnum):
    EXPORT_DISPATCH_PACKET = "EXPORT_DISPATCH_PACKET"
    ACCEPT_EXECUTION_RETURN = "ACCEPT_EXECUTION_RETURN"


class ExternalExecutionBridgeStatus(StrEnum):
    EXPORTED = "EXPORTED"
    RETURN_ACCEPTED = "RETURN_ACCEPTED"
    DRY_RUN = "DRY_RUN"
    CONTROL_BLOCKED = "CONTROL_BLOCKED"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"


@dataclass(frozen=True)
class MCPAutomationSurface:
    resource_kind: str
    resource_name: str
    transport: str
    tool_name: str
    request_schema: str
    response_schema: str


@dataclass(frozen=True)
class ExternalExecutionBridgeRequest:
    workspace_root: str | Path
    action_mode: ExternalExecutionActionMode
    work_unit_id: str
    submission: ExecutionSubmission | None = None
    context_mode: ContextMode = ContextMode.IDE_MANUAL
    automation_stage: AutomationStage = AutomationStage.ASSISTED
    route_stage: RouteStage = RouteStage.ACTIVE
    calibration_status: CalibrationStatus = CalibrationStatus.INSUFFICIENT_DATA
    threshold_action: PromotionAction | None = None
    review_required: bool = False
    manual_fallback_required: bool = False
    supervisor_present: bool = True
    explicit_approval: bool = False
    dry_run: bool = False
    actor: str = "OPERATOR"
    action_timestamp: str | None = None


@dataclass(frozen=True)
class ExternalExecutionBridgeReceipt:
    status: ExternalExecutionBridgeStatus
    requested_at: str
    action_mode: ExternalExecutionActionMode
    work_unit_id: str
    control_state: OperatorControlState
    policy_evaluation: AutomationPolicyEvaluation
    dispatch_result: DispatchResult | None = None
    execution_result: ExecutionResult | None = None
    export_packet_path: str | None = None
    mcp_surface: MCPAutomationSurface | None = None
    service_receipt_path: str | None = None
    service_ledger_path: str | None = None
    notes: tuple[str, ...] = ()


class KernelExternalExecutionBridge:
    """Expose dispatch/execution through a supervised external bridge."""

    def __init__(
        self,
        *,
        policy: KernelAutomationPolicy | None = None,
        operator_controls: KernelOperatorControlManager | None = None,
        dispatcher: KernelDispatcher | None = None,
        executor: KernelExecutor | None = None,
    ) -> None:
        self._policy = policy or KernelAutomationPolicy()
        self._operator_controls = operator_controls or KernelOperatorControlManager()
        self._dispatcher = dispatcher or KernelDispatcher()
        self._executor = executor or KernelExecutor()

    def bridge(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        request: ExternalExecutionBridgeRequest,
    ) -> ExternalExecutionBridgeReceipt:
        if request.action_mode is ExternalExecutionActionMode.EXPORT_DISPATCH_PACKET:
            return self.export_dispatch_packet(store, index, graph, request)
        return self.accept_execution_return(store, index, graph, request)

    def export_dispatch_packet(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        request: ExternalExecutionBridgeRequest,
    ) -> ExternalExecutionBridgeReceipt:
        workspace_root = Path(request.workspace_root).resolve()
        requested_at = request.action_timestamp or _iso_now()
        work_unit = _require_work_unit(index, request.work_unit_id)
        control_state = self._operator_controls.load_state(workspace_root)
        control_notes = _control_notes(control_state, work_unit)
        evaluation = self._policy.evaluate(
            AutomationPolicyRequest(
                action_class=AutomationActionClass.EXPORT_EXTERNAL_EXECUTION_PACKET,
                context_mode=request.context_mode,
                automation_stage=request.automation_stage,
                route_stage=request.route_stage,
                calibration_status=request.calibration_status,
                threshold_action=request.threshold_action,
                review_required=request.review_required,
                manual_fallback_required=request.manual_fallback_required,
                operator_stop=(control_state.service_mode is DaemonServiceControlMode.STOPPED),
                operator_hold=(
                    control_state.service_mode is DaemonServiceControlMode.DRAINING
                    or control_state.is_scope_held("WORK_UNIT", work_unit.work_unit_id)
                ),
                supervisor_present=request.supervisor_present,
                explicit_approval=request.explicit_approval,
                notes=tuple(control_notes),
            )
        )
        mcp_surface = _export_surface(work_unit.work_unit_id)
        packet_relative_path = _packet_relative_path(requested_at, work_unit.work_unit_id)

        if control_notes and evaluation.decision in {AutomationPolicyDecision.BLOCK, AutomationPolicyDecision.HOLD}:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.CONTROL_BLOCKED,
                control_state=control_state,
                evaluation=evaluation,
                export_packet_path=str(packet_relative_path),
                mcp_surface=mcp_surface,
                notes=tuple(control_notes),
            )
        if evaluation.decision is AutomationPolicyDecision.BLOCK:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.POLICY_BLOCKED,
                control_state=control_state,
                evaluation=evaluation,
                export_packet_path=str(packet_relative_path),
                mcp_surface=mcp_surface,
            )
        if evaluation.decision is AutomationPolicyDecision.HOLD:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.CONTROL_BLOCKED,
                control_state=control_state,
                evaluation=evaluation,
                export_packet_path=str(packet_relative_path),
                mcp_surface=mcp_surface,
            )
        if evaluation.decision is AutomationPolicyDecision.REQUIRE_APPROVAL:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.APPROVAL_REQUIRED,
                control_state=control_state,
                evaluation=evaluation,
                export_packet_path=str(packet_relative_path),
                mcp_surface=mcp_surface,
            )
        if request.dry_run:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.DRY_RUN,
                control_state=control_state,
                evaluation=evaluation,
                export_packet_path=str(packet_relative_path),
                mcp_surface=mcp_surface,
            )

        dispatch_result = self._dispatcher.dispatch_work_unit(
            store,
            index,
            graph,
            work_unit.work_unit_id,
            dispatched_at=requested_at,
            packet_output_path=None,
        )
        self._write_export_packet(
            workspace_root,
            packet_relative_path,
            dispatch_result.preparation,
            requested_at=requested_at,
            mcp_surface=mcp_surface,
        )
        return self._finalize(
            workspace_root,
            request=request,
            requested_at=requested_at,
            status=ExternalExecutionBridgeStatus.EXPORTED,
            control_state=control_state,
            evaluation=evaluation,
            dispatch_result=dispatch_result,
            export_packet_path=str(packet_relative_path),
            mcp_surface=mcp_surface,
            notes=(f"dispatch_status={dispatch_result.work_unit_after.status}",),
        )

    def accept_execution_return(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        request: ExternalExecutionBridgeRequest,
    ) -> ExternalExecutionBridgeReceipt:
        if request.submission is None:
            raise KernelExternalExecutionBridgeError(
                "Execution return acceptance requires an ExecutionSubmission."
            )
        workspace_root = Path(request.workspace_root).resolve()
        requested_at = request.action_timestamp or _iso_now()
        work_unit = _require_work_unit(index, request.work_unit_id)
        control_state = self._operator_controls.load_state(workspace_root)
        control_notes = _control_notes(control_state, work_unit)
        control_notes.append("EXTERNAL_RETURN_PATH")
        evaluation = self._policy.evaluate(
            AutomationPolicyRequest(
                action_class=AutomationActionClass.ACCEPT_EXTERNAL_EXECUTION_RETURN,
                context_mode=request.context_mode,
                automation_stage=request.automation_stage,
                route_stage=request.route_stage,
                calibration_status=request.calibration_status,
                threshold_action=request.threshold_action,
                review_required=request.review_required,
                manual_fallback_required=request.manual_fallback_required,
                operator_stop=(control_state.service_mode is DaemonServiceControlMode.STOPPED),
                operator_hold=(
                    control_state.service_mode is DaemonServiceControlMode.DRAINING
                    or control_state.is_scope_held("WORK_UNIT", work_unit.work_unit_id)
                ),
                supervisor_present=request.supervisor_present,
                explicit_approval=request.explicit_approval,
                notes=tuple(control_notes),
            )
        )
        mcp_surface = _return_surface(work_unit.work_unit_id)

        if control_notes and evaluation.decision in {AutomationPolicyDecision.BLOCK, AutomationPolicyDecision.HOLD}:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.CONTROL_BLOCKED,
                control_state=control_state,
                evaluation=evaluation,
                mcp_surface=mcp_surface,
                notes=tuple(control_notes),
            )
        if evaluation.decision is AutomationPolicyDecision.BLOCK:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.POLICY_BLOCKED,
                control_state=control_state,
                evaluation=evaluation,
                mcp_surface=mcp_surface,
            )
        if evaluation.decision is AutomationPolicyDecision.HOLD:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.CONTROL_BLOCKED,
                control_state=control_state,
                evaluation=evaluation,
                mcp_surface=mcp_surface,
            )
        if evaluation.decision is AutomationPolicyDecision.REQUIRE_APPROVAL:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.APPROVAL_REQUIRED,
                control_state=control_state,
                evaluation=evaluation,
                mcp_surface=mcp_surface,
            )
        if request.dry_run:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=ExternalExecutionBridgeStatus.DRY_RUN,
                control_state=control_state,
                evaluation=evaluation,
                mcp_surface=mcp_surface,
            )

        execution_result = self._executor.submit_execution(
            store,
            index,
            work_unit.work_unit_id,
            request.submission,
        )
        return self._finalize(
            workspace_root,
            request=request,
            requested_at=requested_at,
            status=ExternalExecutionBridgeStatus.RETURN_ACCEPTED,
            control_state=control_state,
            evaluation=evaluation,
            execution_result=execution_result,
            mcp_surface=mcp_surface,
            notes=(f"work_unit_status={execution_result.work_unit_after.status}",),
        )

    def _write_export_packet(
        self,
        workspace_root: Path,
        relative_path: Path,
        preparation: DispatchPreparation,
        *,
        requested_at: str,
        mcp_surface: MCPAutomationSurface,
    ) -> Path:
        packet_path = _resolve_relative_file(workspace_root, relative_path)
        packet_path.parent.mkdir(parents=True, exist_ok=True)
        base_payload = json.loads(render_dispatch_packet(preparation.packet, preparation.context_package))
        payload = {
            "bridge_kind": "EXTERNAL_EXECUTION_DISPATCH_PACKET",
            "generated_at": requested_at,
            "authority_class": "GENERATED_STATE",
            "work_unit_id": preparation.assessment.work_unit.work_unit_id,
            "dispatch": base_payload,
            "mcp_surface": asdict(mcp_surface),
            "boundaries": {
                "kernel_truth_is_not_external": True,
                "external_write_authority": "PROPOSED_COMMIT_DELTA_ONLY",
                "governed_write_required_for_commit_application": True,
                "allowed_writes": list(preparation.packet.allowed_writes),
                "allowed_next_actions": list(preparation.packet.allowed_next_actions),
            },
        }
        packet_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return packet_path

    def _finalize(
        self,
        workspace_root: Path,
        *,
        request: ExternalExecutionBridgeRequest,
        requested_at: str,
        status: ExternalExecutionBridgeStatus,
        control_state: OperatorControlState,
        evaluation: AutomationPolicyEvaluation,
        dispatch_result: DispatchResult | None = None,
        execution_result: ExecutionResult | None = None,
        export_packet_path: str | None = None,
        mcp_surface: MCPAutomationSurface | None = None,
        notes: tuple[str, ...] = (),
        receipts_dir: str = "ION/05_context/history/external_execution_bridge_receipts",
        ledger_path: str = "ION/05_context/history/external_execution_bridge_ledger.json",
    ) -> ExternalExecutionBridgeReceipt:
        event_id = _bridge_event_id(requested_at, request.action_mode, request.work_unit_id)
        receipt_relative_path = Path(receipts_dir) / f"{event_id}.external_execution_bridge_receipt.json"
        ledger_relative_path = Path(ledger_path)
        resolved_receipt_path = _resolve_relative_file(workspace_root, receipt_relative_path)
        resolved_ledger_path = _resolve_relative_file(workspace_root, ledger_relative_path)
        resolved_receipt_path.parent.mkdir(parents=True, exist_ok=True)
        resolved_ledger_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "requested_at": requested_at,
            "status": status.value,
            "request": _request_payload(request),
            "control_state": _control_payload(control_state),
            "policy_evaluation": _policy_payload(evaluation),
            "work_unit_id": request.work_unit_id,
            "notes": list(notes),
            "export_packet_path": export_packet_path,
            "mcp_surface": (asdict(mcp_surface) if mcp_surface is not None else None),
            "dispatch": (_dispatch_payload(dispatch_result) if dispatch_result is not None else None),
            "execution": (_execution_payload(execution_result) if execution_result is not None else None),
        }
        resolved_receipt_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        rows: list[dict[str, object]] = []
        if resolved_ledger_path.exists():
            existing = json.loads(resolved_ledger_path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                raise KernelExternalExecutionBridgeError(
                    "external execution bridge ledger must contain a JSON list."
                )
            rows = existing
        rows.append(
            {
                "event_id": event_id,
                "created_at": requested_at,
                "status": status.value,
                "action_mode": request.action_mode.value,
                "work_unit_id": request.work_unit_id,
                "policy_decision": evaluation.decision.value,
                "service_mode": control_state.service_mode.value,
                "receipt_path": str(receipt_relative_path),
                "export_packet_path": export_packet_path,
                "dispatch_packet_status": (
                    dispatch_result.work_unit_after.status.value if dispatch_result is not None else None
                ),
                "commit_delta_id": (
                    execution_result.preparation.commit_delta.delta_id if execution_result is not None else None
                ),
            }
        )
        resolved_ledger_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        return ExternalExecutionBridgeReceipt(
            status=status,
            requested_at=requested_at,
            action_mode=request.action_mode,
            work_unit_id=request.work_unit_id,
            control_state=control_state,
            policy_evaluation=evaluation,
            dispatch_result=dispatch_result,
            execution_result=execution_result,
            export_packet_path=export_packet_path,
            mcp_surface=mcp_surface,
            service_receipt_path=str(receipt_relative_path),
            service_ledger_path=str(ledger_relative_path),
            notes=notes,
        )


IonExternalExecutionBridge = KernelExternalExecutionBridge


def _request_payload(request: ExternalExecutionBridgeRequest) -> dict[str, object]:
    return {
        "workspace_root": str(request.workspace_root),
        "action_mode": request.action_mode.value,
        "work_unit_id": request.work_unit_id,
        "has_submission": request.submission is not None,
        "context_mode": request.context_mode.value,
        "automation_stage": request.automation_stage.value,
        "route_stage": request.route_stage.value,
        "calibration_status": request.calibration_status.value,
        "threshold_action": (None if request.threshold_action is None else request.threshold_action.value),
        "review_required": request.review_required,
        "manual_fallback_required": request.manual_fallback_required,
        "supervisor_present": request.supervisor_present,
        "explicit_approval": request.explicit_approval,
        "dry_run": request.dry_run,
        "actor": request.actor,
    }


def _control_payload(state: OperatorControlState) -> dict[str, object]:
    return {
        "updated_at": state.updated_at,
        "service_mode": state.service_mode.value,
        "scope_holds": [
            {
                "scope_type": hold.scope_type,
                "scope_ref": hold.scope_ref,
                "reason": hold.reason,
                "created_at": hold.created_at,
                "actor": hold.actor,
            }
            for hold in state.scope_holds
        ],
        "global_notes": list(state.global_notes),
    }


def _policy_payload(evaluation: AutomationPolicyEvaluation) -> dict[str, object]:
    return {
        "decision": evaluation.decision.value,
        "reasons": list(evaluation.reasons),
        "required_controls": list(evaluation.required_controls),
    }


def _dispatch_payload(result: DispatchResult) -> dict[str, object]:
    return {
        "work_unit_before_status": result.work_unit_before.status.value,
        "work_unit_after_status": result.work_unit_after.status.value,
        "dispatch_packet_work_unit_id": result.preparation.packet.work_unit_id,
        "context_package_id": result.preparation.context_package.context_package_id,
    }


def _execution_payload(result: ExecutionResult) -> dict[str, object]:
    return {
        "work_unit_before_status": result.work_unit_before.status.value,
        "work_unit_after_status": result.work_unit_after.status.value,
        "commit_delta_id": result.preparation.commit_delta.delta_id,
        "commit_delta_status": result.preparation.commit_delta.status.value,
        "context_version": result.preparation.commit_delta.context_version,
    }


def _export_surface(work_unit_id: str) -> MCPAutomationSurface:
    return MCPAutomationSurface(
        resource_kind="ION_EXTERNAL_EXECUTION_PACKET",
        resource_name=f"ion.external_execution.packet.{work_unit_id}",
        transport="MCP",
        tool_name="ion.submit_execution_return",
        request_schema="ExecutionSubmission",
        response_schema="ExternalExecutionBridgeReceipt",
    )


def _return_surface(work_unit_id: str) -> MCPAutomationSurface:
    return MCPAutomationSurface(
        resource_kind="ION_EXTERNAL_EXECUTION_RETURN",
        resource_name=f"ion.external_execution.return.{work_unit_id}",
        transport="MCP",
        tool_name="ion.submit_execution_return",
        request_schema="ExecutionSubmission",
        response_schema="ExternalExecutionBridgeReceipt",
    )


def _control_notes(control_state: OperatorControlState, work_unit: WorkUnit) -> list[str]:
    notes: list[str] = []
    if control_state.service_mode is DaemonServiceControlMode.STOPPED:
        notes.append("SERVICE_MODE_STOPPED")
    elif control_state.service_mode is DaemonServiceControlMode.DRAINING:
        notes.append("SERVICE_MODE_DRAINING")
    if control_state.is_scope_held("WORK_UNIT", work_unit.work_unit_id):
        notes.append("WORK_UNIT_HOLD_ACTIVE")
    return notes


def _require_work_unit(index: KernelIndex, work_unit_id: str) -> WorkUnit:
    record = index.get("work_unit", work_unit_id)
    if not isinstance(record, WorkUnit):
        raise KernelExternalExecutionBridgeError(f"Unknown work unit: {work_unit_id}")
    return record


def _packet_relative_path(requested_at: str, work_unit_id: str) -> Path:
    return Path("ION/05_context/history/external_execution_packets") / (
        f"{_bridge_event_id(requested_at, ExternalExecutionActionMode.EXPORT_DISPATCH_PACKET, work_unit_id)}.external_execution_packet.json"
    )


def _bridge_event_id(requested_at: str, action_mode: ExternalExecutionActionMode, work_unit_id: str) -> str:
    safe_time = compact_identifier(requested_at, empty="event", max_length=24)
    safe_work = compact_identifier(work_unit_id, empty="work-unit", max_length=56)
    return f"external-{action_mode.value.lower().replace('_', '-')}-{safe_work}-{safe_time}"


def _resolve_relative_file(workspace_root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelExternalExecutionBridgeError("relative_path must be relative to workspace_root")
    return workspace_root / relative_path


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
