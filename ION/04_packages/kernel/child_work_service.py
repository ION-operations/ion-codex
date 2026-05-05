"""Supervised child-work issuance service for the live ION kernel stack.

This module does not create an unattended multi-agent field. It turns the already-landed
planner-gated child issuance path into an explicit supervised service action with:
- policy binding,
- operator-control checks,
- review/approval gates,
- durable service receipts.
"""

from __future__ import annotations

from dataclasses import dataclass
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
from .children import ChildAgentBinding
from .graph import KernelGraph
from .index import KernelIndex
from .model import CommitDelta, PlannerManifest, StrEnum, TierOneDoctrine, WorkUnit
from .operator_control import (
    DaemonServiceControlMode,
    KernelOperatorControlManager,
    OperatorControlState,
)
from .planner_gate import (
    KernelPlannerChildIssuanceGate,
    KernelPlannerGateError,
    PlannerChildIssuancePreparation,
    PlannerChildIssuanceResult,
    PlannerManifestPreparation,
)
from .runtime_state_views import KernelRuntimeStateView
from .store import KernelStore
from .threshold import AutomationStage, CalibrationStatus, ContextMode, PromotionAction, RouteStage


class KernelChildWorkServiceError(Exception):
    """Raised when supervised child-work issuance cannot be completed lawfully."""


class ChildWorkSelectionMode(StrEnum):
    MANIFEST = "MANIFEST"
    QUESTION_DELTA = "QUESTION_DELTA"


class ChildWorkServiceStatus(StrEnum):
    ISSUED = "ISSUED"
    DRY_RUN = "DRY_RUN"
    CONTROL_BLOCKED = "CONTROL_BLOCKED"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"


@dataclass(frozen=True)
class ChildWorkServiceRequest:
    workspace_root: str | Path
    repo_root: str | Path
    doctrine: TierOneDoctrine
    selection_mode: ChildWorkSelectionMode = ChildWorkSelectionMode.MANIFEST
    manifest_id: str | None = None
    question_id: str | None = None
    work_unit_id: str | None = None
    delta_id: str | None = None
    agent_bindings: dict[str, ChildAgentBinding] | None = None
    context_mode: ContextMode = ContextMode.IDE_MANUAL
    automation_stage: AutomationStage = AutomationStage.ASSISTED
    route_stage: RouteStage = RouteStage.ACTIVE
    calibration_status: CalibrationStatus = CalibrationStatus.INSUFFICIENT_DATA
    threshold_action: PromotionAction | None = None
    review_required: bool | None = None
    manual_fallback_required: bool | None = None
    supervisor_present: bool = True
    explicit_approval: bool = False
    dry_run: bool = False
    created_by: str = "DAEMON"
    notes: str | None = None
    expires_at: str | None = None
    actor: str = "OPERATOR"
    action_timestamp: str | None = None


@dataclass(frozen=True)
class ChildWorkServiceReceipt:
    status: ChildWorkServiceStatus
    requested_at: str
    control_state: OperatorControlState
    policy_evaluation: AutomationPolicyEvaluation
    selection_mode: ChildWorkSelectionMode
    parent_work_unit_id: str
    manifest_id: str | None = None
    question_id: str | None = None
    delta_id: str | None = None
    issued_child_work_unit_ids: tuple[str, ...] = ()
    issued_context_package_ids: tuple[str, ...] = ()
    child_count: int = 0
    planner_child_issuance_result: PlannerChildIssuanceResult | None = None
    service_receipt_path: str | None = None
    service_ledger_path: str | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class _ResolvedChildRequest:
    selection_mode: ChildWorkSelectionMode
    parent_work_unit: WorkUnit
    planner_commit_delta: CommitDelta
    manifest_id: str | None
    question_id: str | None
    review_required: bool
    manual_fallback_required: bool
    context_mode: ContextMode
    automation_stage: AutomationStage
    route_stage: RouteStage
    calibration_status: CalibrationStatus
    notes: tuple[str, ...]


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelChildWorkService:
    """Run planner-gated child issuance only through supervised service controls."""

    def __init__(
        self,
        *,
        planner_gate: KernelPlannerChildIssuanceGate | None = None,
        policy: KernelAutomationPolicy | None = None,
        operator_controls: KernelOperatorControlManager | None = None,
        runtime_state_view: KernelRuntimeStateView | None = None,
    ) -> None:
        self._planner_gate = planner_gate or KernelPlannerChildIssuanceGate()
        self._policy = policy or KernelAutomationPolicy()
        self._operator_controls = operator_controls or KernelOperatorControlManager()
        self._runtime_state_view = runtime_state_view or KernelRuntimeStateView()

    def issue_child_work(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        request: ChildWorkServiceRequest,
    ) -> ChildWorkServiceReceipt:
        workspace_root = Path(request.workspace_root).resolve()
        requested_at = request.action_timestamp or _iso_now()
        control_state = self._operator_controls.load_state(workspace_root)
        resolved = self._resolve_request(index, request)

        control_notes: list[str] = []
        if control_state.service_mode is DaemonServiceControlMode.STOPPED:
            control_notes.append("SERVICE_MODE_STOPPED")
        elif control_state.service_mode is DaemonServiceControlMode.DRAINING:
            control_notes.append("SERVICE_MODE_DRAINING")
        if control_state.is_scope_held("WORK_UNIT", resolved.parent_work_unit.work_unit_id):
            control_notes.append("PARENT_WORK_UNIT_HOLD_ACTIVE")
        if resolved.manifest_id and control_state.is_scope_held("MANIFEST", resolved.manifest_id):
            control_notes.append("MANIFEST_HOLD_ACTIVE")

        policy_request = AutomationPolicyRequest(
            action_class=AutomationActionClass.ISSUE_CHILD_WORK,
            context_mode=resolved.context_mode,
            automation_stage=resolved.automation_stage,
            route_stage=resolved.route_stage,
            calibration_status=resolved.calibration_status,
            threshold_action=request.threshold_action,
            review_required=resolved.review_required,
            manual_fallback_required=resolved.manual_fallback_required,
            operator_stop=(control_state.service_mode is DaemonServiceControlMode.STOPPED),
            operator_hold=(
                control_state.service_mode is DaemonServiceControlMode.DRAINING
                or control_state.is_scope_held("WORK_UNIT", resolved.parent_work_unit.work_unit_id)
                or (resolved.manifest_id is not None and control_state.is_scope_held("MANIFEST", resolved.manifest_id))
            ),
            supervisor_present=request.supervisor_present,
            explicit_approval=request.explicit_approval,
            notes=tuple(control_notes + list(resolved.notes)),
        )
        evaluation = self._policy.evaluate(policy_request)

        status: ChildWorkServiceStatus
        issuance_result: PlannerChildIssuanceResult | None = None
        if control_notes and evaluation.decision in {AutomationPolicyDecision.BLOCK, AutomationPolicyDecision.HOLD}:
            status = ChildWorkServiceStatus.CONTROL_BLOCKED
        elif evaluation.decision is AutomationPolicyDecision.BLOCK:
            status = ChildWorkServiceStatus.POLICY_BLOCKED
        elif evaluation.decision is AutomationPolicyDecision.HOLD:
            status = ChildWorkServiceStatus.CONTROL_BLOCKED
        elif evaluation.decision is AutomationPolicyDecision.REQUIRE_APPROVAL:
            status = ChildWorkServiceStatus.APPROVAL_REQUIRED
        elif request.dry_run:
            status = ChildWorkServiceStatus.DRY_RUN
        else:
            issuance_result = self._execute_request(
                store,
                index,
                graph,
                request,
                resolved,
            )
            status = ChildWorkServiceStatus.ISSUED

        issued_work_ids: tuple[str, ...] = ()
        issued_context_ids: tuple[str, ...] = ()
        manifest_id = resolved.manifest_id
        if issuance_result is not None:
            issued_work_ids = tuple(
                item.work_unit_id for item in issuance_result.child_work_result.created_work_units
            )
            issued_context_ids = tuple(
                item.context_package_id for item in issuance_result.child_work_result.created_context_packages
            )
            manifest_id = issuance_result.updated_manifest.manifest_id

        return self._finalize(
            workspace_root,
            request=request,
            requested_at=requested_at,
            status=status,
            control_state=control_state,
            evaluation=evaluation,
            resolved=resolved,
            issuance_result=issuance_result,
            manifest_id=manifest_id,
            issued_work_ids=issued_work_ids,
            issued_context_ids=issued_context_ids,
            notes=tuple(dict.fromkeys(tuple(control_notes) + resolved.notes)),
        )

    def _resolve_request(
        self,
        index: KernelIndex,
        request: ChildWorkServiceRequest,
    ) -> _ResolvedChildRequest:
        if request.selection_mode is ChildWorkSelectionMode.MANIFEST:
            manifest_id = _require_identifier(request.manifest_id, "manifest_id")
            preparation = self._planner_gate.prepare_issuance_from_manifest(index, manifest_id)
            return self._resolved_from_preparation(index, request, preparation, manifest_id=manifest_id)

        question_id = _require_identifier(request.question_id, "question_id")
        work_unit_id = _require_identifier(request.work_unit_id, "work_unit_id")
        delta_id = _require_identifier(request.delta_id, "delta_id")
        manifest_prep = self._planner_gate.prepare_manifest(
            index,
            question_id,
            work_unit_id,
            delta_id,
            created_by=request.created_by,
            notes=request.notes,
            expires_at=request.expires_at,
        )
        preparation = PlannerChildIssuancePreparation(
            planner_manifest=manifest_prep.planner_manifest,
            resolved_question=manifest_prep.resolved_question,
            parent_work_unit=manifest_prep.parent_work_unit,
            planner_commit_delta=manifest_prep.planner_commit_delta,
        )
        return self._resolved_from_preparation(index, request, preparation, manifest_id=None)

    def _resolved_from_preparation(
        self,
        index: KernelIndex,
        request: ChildWorkServiceRequest,
        preparation: PlannerChildIssuancePreparation,
        *,
        manifest_id: str | None,
    ) -> _ResolvedChildRequest:
        parent = preparation.parent_work_unit
        delta = preparation.planner_commit_delta
        dispatch_posture = self._runtime_state_view.dispatch_posture_for_work_unit(index, parent.work_unit_id)
        review_pressure = self._runtime_state_view.review_pressure_for_delta(index, delta)
        scope_view = dispatch_posture.scope_view

        context_mode = request.context_mode
        automation_stage = request.automation_stage
        route_stage = request.route_stage
        calibration_status = request.calibration_status
        derived_notes: list[str] = []

        if scope_view.automation is not None:
            try:
                context_mode = ContextMode(scope_view.automation.context_mode)
            except ValueError:
                derived_notes.append(f"UNKNOWN_CONTEXT_MODE::{scope_view.automation.context_mode}")
            try:
                automation_stage = AutomationStage(scope_view.automation.current_stage)
            except ValueError:
                derived_notes.append(f"UNKNOWN_AUTOMATION_STAGE::{scope_view.automation.current_stage}")
            calibration_text = scope_view.automation.calibration_status
            if calibration_text:
                try:
                    calibration_status = CalibrationStatus(calibration_text)
                except ValueError:
                    derived_notes.append(f"UNKNOWN_CALIBRATION_STATUS::{calibration_text}")

        if not dispatch_posture.dispatch_permitted:
            route_stage = RouteStage.BLOCKED
            derived_notes.extend(tuple(f"DISPATCH_BLOCKER::{item}" for item in dispatch_posture.blockers))

        review_required = (
            request.review_required
            if request.review_required is not None
            else (review_pressure.requires_review or parent.spawn_policy.spawn_requires_approval)
        )
        if parent.spawn_policy.spawn_requires_approval:
            derived_notes.append("SPAWN_POLICY_REQUIRES_APPROVAL")
        if review_pressure.requires_review:
            derived_notes.append(f"REVIEW_PRESSURE::{review_pressure.reason}")

        manual_fallback_required = (
            request.manual_fallback_required
            if request.manual_fallback_required is not None
            else (not dispatch_posture.dispatch_permitted)
        )

        return _ResolvedChildRequest(
            selection_mode=request.selection_mode,
            parent_work_unit=parent,
            planner_commit_delta=delta,
            manifest_id=manifest_id,
            question_id=preparation.resolved_question.question_id,
            review_required=review_required,
            manual_fallback_required=manual_fallback_required,
            context_mode=context_mode,
            automation_stage=automation_stage,
            route_stage=route_stage,
            calibration_status=calibration_status,
            notes=tuple(dict.fromkeys(derived_notes)),
        )

    def _execute_request(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        request: ChildWorkServiceRequest,
        resolved: _ResolvedChildRequest,
    ) -> PlannerChildIssuanceResult:
        if resolved.selection_mode is ChildWorkSelectionMode.MANIFEST:
            if resolved.manifest_id is None:
                raise KernelChildWorkServiceError("Manifest selection requires a manifest_id.")
            return self._planner_gate.issue_child_work_from_manifest(
                store,
                index,
                graph,
                resolved.manifest_id,
                repo_root=request.repo_root,
                doctrine=request.doctrine,
                agent_bindings=request.agent_bindings,
                created_at=request.action_timestamp,
            )
        return self._planner_gate.issue_child_work(
            store,
            index,
            graph,
            resolved.question_id or _require_identifier(request.question_id, "question_id"),
            resolved.parent_work_unit.work_unit_id,
            resolved.planner_commit_delta.delta_id,
            repo_root=request.repo_root,
            doctrine=request.doctrine,
            agent_bindings=request.agent_bindings,
            created_at=request.action_timestamp,
            created_by=request.created_by,
            notes=request.notes,
            expires_at=request.expires_at,
        )

    def _finalize(
        self,
        workspace_root: Path,
        *,
        request: ChildWorkServiceRequest,
        requested_at: str,
        status: ChildWorkServiceStatus,
        control_state: OperatorControlState,
        evaluation: AutomationPolicyEvaluation,
        resolved: _ResolvedChildRequest,
        issuance_result: PlannerChildIssuanceResult | None,
        manifest_id: str | None,
        issued_work_ids: tuple[str, ...],
        issued_context_ids: tuple[str, ...],
        notes: tuple[str, ...],
        receipts_dir: str = "ION/05_context/history/child_work_service_receipts",
        ledger_path: str = "ION/05_context/history/child_work_service_ledger.json",
    ) -> ChildWorkServiceReceipt:
        event_id = _child_service_run_id(requested_at, resolved.parent_work_unit.work_unit_id)
        receipt_relative_path = Path(receipts_dir) / f"{event_id}.child_work_service_receipt.json"
        ledger_relative_path = Path(ledger_path)
        resolved_receipt_path = _resolve_relative_file(workspace_root, receipt_relative_path)
        resolved_ledger_path = _resolve_relative_file(workspace_root, ledger_relative_path)
        resolved_receipt_path.parent.mkdir(parents=True, exist_ok=True)
        resolved_ledger_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "requested_at": requested_at,
            "status": status.value,
            "selection": {
                "selection_mode": resolved.selection_mode.value,
                "manifest_id": manifest_id,
                "question_id": resolved.question_id,
                "parent_work_unit_id": resolved.parent_work_unit.work_unit_id,
                "delta_id": resolved.planner_commit_delta.delta_id,
            },
            "request": _request_payload(request),
            "control_state": _control_payload(control_state),
            "policy_evaluation": _policy_payload(evaluation),
            "notes": list(notes),
            "issued_child_work_unit_ids": list(issued_work_ids),
            "issued_context_package_ids": list(issued_context_ids),
            "child_count": len(issued_work_ids),
        }
        if issuance_result is not None:
            payload["planner_manifest_status"] = issuance_result.updated_manifest.status.value
            payload["executed_at"] = issuance_result.updated_manifest.executed_at
        resolved_receipt_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        rows: list[dict[str, object]] = []
        if resolved_ledger_path.exists():
            existing = json.loads(resolved_ledger_path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                raise KernelChildWorkServiceError("child work service ledger must contain a JSON list.")
            rows = existing
        rows.append(
            {
                "event_id": event_id,
                "created_at": requested_at,
                "status": status.value,
                "selection_mode": resolved.selection_mode.value,
                "manifest_id": manifest_id,
                "question_id": resolved.question_id,
                "parent_work_unit_id": resolved.parent_work_unit.work_unit_id,
                "delta_id": resolved.planner_commit_delta.delta_id,
                "child_count": len(issued_work_ids),
                "issued_child_work_unit_ids": list(issued_work_ids),
                "policy_decision": evaluation.decision.value,
                "service_mode": control_state.service_mode.value,
                "receipt_path": str(receipt_relative_path),
            }
        )
        resolved_ledger_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        return ChildWorkServiceReceipt(
            status=status,
            requested_at=requested_at,
            control_state=control_state,
            policy_evaluation=evaluation,
            selection_mode=resolved.selection_mode,
            parent_work_unit_id=resolved.parent_work_unit.work_unit_id,
            manifest_id=manifest_id,
            question_id=resolved.question_id,
            delta_id=resolved.planner_commit_delta.delta_id,
            issued_child_work_unit_ids=issued_work_ids,
            issued_context_package_ids=issued_context_ids,
            child_count=len(issued_work_ids),
            planner_child_issuance_result=issuance_result,
            service_receipt_path=str(receipt_relative_path),
            service_ledger_path=str(ledger_relative_path),
            notes=notes,
        )


IonChildWorkService = KernelChildWorkService


def _request_payload(request: ChildWorkServiceRequest) -> dict[str, object]:
    return {
        "selection_mode": request.selection_mode.value,
        "manifest_id": request.manifest_id,
        "question_id": request.question_id,
        "work_unit_id": request.work_unit_id,
        "delta_id": request.delta_id,
        "repo_root": str(request.repo_root),
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
        "created_by": request.created_by,
        "notes": request.notes,
        "expires_at": request.expires_at,
        "actor": request.actor,
        "agent_bindings": sorted((request.agent_bindings or {}).keys()),
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


def _require_identifier(value: str | None, field_name: str) -> str:
    if value is None or not value.strip():
        raise KernelChildWorkServiceError(f"{field_name} is required.")
    return value.strip()


def _resolve_relative_file(workspace_root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelChildWorkServiceError("relative path must stay relative to the workspace root")
    return workspace_root / relative_path


def _child_service_run_id(requested_at: str, work_unit_id: str) -> str:
    safe_time = _SAFE_ID_RE.sub("-", requested_at.lower()).strip("-") or "run"
    safe_work = _SAFE_ID_RE.sub("-", work_unit_id.lower()).strip("-") or "work"
    return f"child-work-service-{safe_work}-{safe_time}"


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
