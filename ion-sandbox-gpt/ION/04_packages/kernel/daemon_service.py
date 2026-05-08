"""Supervised daemon service harness for the live ION kernel stack.

This module wraps the bounded daemon loop in explicit operator-control and policy
checks. It does not claim unattended autonomy.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path
import re

from .automation_policy import (
    AutomationActionClass,
    AutomationPolicyDecision,
    AutomationPolicyEvaluation,
    AutomationPolicyRequest,
    KernelAutomationPolicy,
)
from .daemon_loop import DaemonLoopResult, DaemonLoopStatus, KernelDaemonLoop
from .child_work_service import ChildWorkServiceReceipt, ChildWorkServiceRequest, KernelChildWorkService
from .external_execution_bridge import ExternalExecutionBridgeReceipt, ExternalExecutionBridgeRequest, KernelExternalExecutionBridge
from .graph import KernelGraph
from .index import KernelIndex
from .operator_control import (
    DaemonServiceControlMode,
    KernelOperatorControlManager,
    OperatorControlState,
)
from .store import KernelStore
from .threshold import AutomationStage, CalibrationStatus, ContextMode, PromotionAction, RouteStage


class KernelDaemonServiceError(Exception):
    """Raised when a supervised daemon-service request is not lawful."""


class DaemonServiceStatus(str):
    EXECUTED = "EXECUTED"
    DRY_RUN = "DRY_RUN"
    CONTROL_BLOCKED = "CONTROL_BLOCKED"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"


@dataclass(frozen=True)
class DaemonServiceRequest:
    workspace_root: str | Path
    max_steps: int = 25
    scope_type: str | None = None
    scope_ref: str | None = None
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
    packet_output_root: str | Path | None = None
    repo_root: str | Path | None = None
    actor: str = "OPERATOR"
    action_timestamp: str | None = None
    replay_of_service_receipt_path: str | None = None
    replay_reason: str | None = None


@dataclass(frozen=True)
class DaemonServiceRecoveryState:
    resumable: bool
    classification: str


@dataclass(frozen=True)
class DaemonServiceReceipt:
    status: str
    requested_at: str
    control_state: OperatorControlState
    policy_evaluation: AutomationPolicyEvaluation
    loop_result: DaemonLoopResult | None = None
    recovery_state: DaemonServiceRecoveryState | None = None
    service_receipt_path: str | None = None
    service_ledger_path: str | None = None
    notes: tuple[str, ...] = ()


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelDaemonService:
    """Invoke the bounded daemon loop only under explicit policy and control state."""

    def __init__(
        self,
        *,
        policy: KernelAutomationPolicy | None = None,
        operator_controls: KernelOperatorControlManager | None = None,
        loop: KernelDaemonLoop | None = None,
        child_work_service: KernelChildWorkService | None = None,
        external_execution_bridge: KernelExternalExecutionBridge | None = None,
    ) -> None:
        self._policy = policy or KernelAutomationPolicy()
        self._operator_controls = operator_controls or KernelOperatorControlManager()
        self._loop = loop or KernelDaemonLoop()
        self._child_work_service = child_work_service or KernelChildWorkService(
            policy=self._policy,
            operator_controls=self._operator_controls,
        )
        self._external_execution_bridge = external_execution_bridge or KernelExternalExecutionBridge(
            policy=self._policy,
            operator_controls=self._operator_controls,
        )

    def run(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        request: DaemonServiceRequest,
    ) -> DaemonServiceReceipt:
        workspace_root = Path(request.workspace_root).resolve()
        requested_at = request.action_timestamp or _iso_now()
        control_state = self._operator_controls.load_state(workspace_root)

        control_notes: list[str] = []
        if control_state.service_mode is DaemonServiceControlMode.STOPPED:
            control_notes.append("SERVICE_MODE_STOPPED")
        elif control_state.service_mode is DaemonServiceControlMode.DRAINING:
            control_notes.append("SERVICE_MODE_DRAINING")
        if request.scope_type and request.scope_ref and control_state.is_scope_held(request.scope_type, request.scope_ref):
            control_notes.append("SCOPE_HOLD_ACTIVE")
        if request.replay_of_service_receipt_path:
            control_notes.append("RECOVERY_REPLAY_REQUEST")

        policy_request = AutomationPolicyRequest(
            action_class=AutomationActionClass.START_DAEMON_SERVICE,
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
                or (request.scope_type is not None and request.scope_ref is not None and control_state.is_scope_held(request.scope_type, request.scope_ref))
            ),
            supervisor_present=request.supervisor_present,
            explicit_approval=request.explicit_approval,
            notes=tuple(control_notes),
        )
        evaluation = self._policy.evaluate(policy_request)

        if control_notes and evaluation.decision in {AutomationPolicyDecision.BLOCK, AutomationPolicyDecision.HOLD}:
            status = DaemonServiceStatus.CONTROL_BLOCKED
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=status,
                control_state=control_state,
                evaluation=evaluation,
                notes=tuple(control_notes),
            )

        if evaluation.decision is AutomationPolicyDecision.BLOCK:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=DaemonServiceStatus.POLICY_BLOCKED,
                control_state=control_state,
                evaluation=evaluation,
            )

        if evaluation.decision is AutomationPolicyDecision.HOLD:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=DaemonServiceStatus.CONTROL_BLOCKED,
                control_state=control_state,
                evaluation=evaluation,
            )

        if evaluation.decision is AutomationPolicyDecision.REQUIRE_APPROVAL:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=DaemonServiceStatus.APPROVAL_REQUIRED,
                control_state=control_state,
                evaluation=evaluation,
            )

        if request.dry_run:
            return self._finalize(
                workspace_root,
                request=request,
                requested_at=requested_at,
                status=DaemonServiceStatus.DRY_RUN,
                control_state=control_state,
                evaluation=evaluation,
            )

        loop_result = self._loop.run_until_blocked(
            store,
            index,
            graph,
            max_steps=request.max_steps,
            workspace_root=workspace_root,
            packet_output_root=request.packet_output_root,
            repo_root=request.repo_root,
            action_timestamp=request.action_timestamp,
        )
        return self._finalize(
            workspace_root,
            request=request,
            requested_at=requested_at,
            status=DaemonServiceStatus.EXECUTED,
            control_state=control_state,
            evaluation=evaluation,
            loop_result=loop_result,
            notes=(f"loop_status={loop_result.status}", f"steps={loop_result.step_count}"),
        )

    def issue_child_work(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        request: ChildWorkServiceRequest,
    ) -> ChildWorkServiceReceipt:
        """Run supervised child-work issuance through the daemon service control floor."""

        return self._child_work_service.issue_child_work(store, index, graph, request)

    def bridge_external_execution(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        request: ExternalExecutionBridgeRequest,
    ) -> ExternalExecutionBridgeReceipt:
        """Delegate supervised external execution bridging through the daemon service floor."""

        return self._external_execution_bridge.bridge(store, index, graph, request)

    def _finalize(
        self,
        workspace_root: Path,
        *,
        request: DaemonServiceRequest,
        requested_at: str,
        status: str,
        control_state: OperatorControlState,
        evaluation: AutomationPolicyEvaluation,
        loop_result: DaemonLoopResult | None = None,
        notes: tuple[str, ...] = (),
        service_receipts_dir: str = "ION/05_context/history/daemon_service_receipts",
        service_ledger_path: str = "ION/05_context/history/daemon_service_ledger.json",
    ) -> DaemonServiceReceipt:
        receipt_relative_path = Path(service_receipts_dir) / f"{_service_run_id(requested_at)}.daemon_service_receipt.json"
        ledger_relative_path = Path(service_ledger_path)
        receipt_path = _resolve_relative_file(workspace_root, receipt_relative_path)
        ledger_path = _resolve_relative_file(workspace_root, ledger_relative_path)
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        recovery_state = _classify_recovery(status, loop_result)

        payload = {
            "requested_at": requested_at,
            "status": status,
            "request": _request_payload(request),
            "control_state": _control_payload(control_state),
            "policy_evaluation": _policy_payload(evaluation),
            "notes": list(notes),
            "loop_result": (_loop_payload(loop_result) if loop_result is not None else None),
            "recovery": {
                "resumable": recovery_state.resumable,
                "classification": recovery_state.classification,
            },
            "replay": {
                "is_replay": bool(request.replay_of_service_receipt_path),
                "replay_of_service_receipt_path": request.replay_of_service_receipt_path,
                "replay_reason": request.replay_reason,
            },
        }
        receipt_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        ledger_rows: list[dict[str, object]] = []
        if ledger_path.exists():
            existing = json.loads(ledger_path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                raise KernelDaemonServiceError("daemon service ledger must contain a JSON list.")
            ledger_rows = existing
        ledger_rows.append(
            {
                "event_id": _service_run_id(requested_at),
                "created_at": requested_at,
                "status": status,
                "receipt_path": str(receipt_relative_path),
                "policy_decision": evaluation.decision.value,
                "service_mode": control_state.service_mode.value,
                "scope_type": request.scope_type,
                "scope_ref": request.scope_ref,
                "loop_receipt_path": (loop_result.receipt_path if loop_result is not None else None),
                "resumable": recovery_state.resumable,
                "recovery_classification": recovery_state.classification,
                "is_replay": bool(request.replay_of_service_receipt_path),
                "replay_of_service_receipt_path": request.replay_of_service_receipt_path,
            }
        )
        ledger_path.write_text(json.dumps(ledger_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        return DaemonServiceReceipt(
            status=status,
            requested_at=requested_at,
            control_state=control_state,
            policy_evaluation=evaluation,
            loop_result=loop_result,
            recovery_state=recovery_state,
            service_receipt_path=str(receipt_relative_path),
            service_ledger_path=str(ledger_relative_path),
            notes=notes,
        )


IonDaemonService = KernelDaemonService


def _request_payload(request: DaemonServiceRequest) -> dict[str, object]:
    payload = asdict(request)
    payload["workspace_root"] = str(payload["workspace_root"])
    if payload.get("packet_output_root") is not None:
        payload["packet_output_root"] = str(payload["packet_output_root"])
    if payload.get("repo_root") is not None:
        payload["repo_root"] = str(payload["repo_root"])
    payload["context_mode"] = request.context_mode.value
    payload["automation_stage"] = request.automation_stage.value
    payload["route_stage"] = request.route_stage.value
    payload["calibration_status"] = request.calibration_status.value
    payload["threshold_action"] = None if request.threshold_action is None else request.threshold_action.value
    return payload


def _control_payload(state: OperatorControlState) -> dict[str, object]:
    return {
        "updated_at": state.updated_at,
        "service_mode": state.service_mode.value,
        "scope_holds": [asdict(hold) for hold in state.scope_holds],
        "global_notes": list(state.global_notes),
    }


def _policy_payload(evaluation: AutomationPolicyEvaluation) -> dict[str, object]:
    return {
        "decision": evaluation.decision.value,
        "reasons": list(evaluation.reasons),
        "required_controls": list(evaluation.required_controls),
    }


def _loop_payload(loop_result: DaemonLoopResult) -> dict[str, object]:
    return {
        "status": loop_result.status.value,
        "step_count": loop_result.step_count,
        "run_id": loop_result.run_id,
        "started_at": loop_result.started_at,
        "completed_at": loop_result.completed_at,
        "receipt_path": loop_result.receipt_path,
        "ledger_path": loop_result.ledger_path,
    }


def _classify_recovery(status: str, loop_result: DaemonLoopResult | None) -> DaemonServiceRecoveryState:
    if status == DaemonServiceStatus.EXECUTED and loop_result is not None:
        if loop_result.status is DaemonLoopStatus.MAX_STEPS_REACHED:
            return DaemonServiceRecoveryState(resumable=True, classification="MAX_STEPS_REACHED")
        if loop_result.status is DaemonLoopStatus.BLOCKED_UNSUPPORTED:
            return DaemonServiceRecoveryState(resumable=True, classification="BLOCKED_UNSUPPORTED")
        return DaemonServiceRecoveryState(resumable=False, classification="IDLE_COMPLETE")
    if status == DaemonServiceStatus.DRY_RUN:
        return DaemonServiceRecoveryState(resumable=False, classification="DRY_RUN_ONLY")
    if status == DaemonServiceStatus.APPROVAL_REQUIRED:
        return DaemonServiceRecoveryState(resumable=False, classification="APPROVAL_REQUIRED")
    if status == DaemonServiceStatus.CONTROL_BLOCKED:
        return DaemonServiceRecoveryState(resumable=False, classification="CONTROL_BLOCKED")
    return DaemonServiceRecoveryState(resumable=False, classification="POLICY_BLOCKED")


def _service_run_id(requested_at: str) -> str:
    safe = _SAFE_ID_RE.sub("-", requested_at.lower()).strip("-") or "service"
    return f"daemon-service-{safe}"


def _resolve_relative_file(workspace_root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelDaemonServiceError("relative_path must be relative to workspace_root")
    return workspace_root / relative_path


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
