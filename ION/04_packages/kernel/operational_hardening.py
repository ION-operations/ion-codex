"""Operational hardening for the supervised ION runtime surface.

This module packages the now-landed supervised automation stack into a truthful
operator-facing runtime mode. It does not add unattended autonomy.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any

from .automation_policy import (
    AutomationActionClass,
    AutomationPolicyDecision,
    AutomationPolicyEvaluation,
    AutomationPolicyRequest,
    KernelAutomationPolicy,
)
from .operator_control import (
    DaemonServiceControlMode,
    KernelOperatorControlManager,
    OperatorControlState,
)
from .threshold import AutomationStage, CalibrationStatus, ContextMode, PromotionAction, RouteStage
from .model import StrEnum


class KernelOperationalHardeningError(Exception):
    """Raised when supervised runtime hardening artifacts cannot be loaded or written."""


class SupervisedRuntimeLifecycleStatus(StrEnum):
    STARTED = "STARTED"
    ALREADY_ENABLED = "ALREADY_ENABLED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    CONTROL_BLOCKED = "CONTROL_BLOCKED"
    DRAINING = "DRAINING"
    STOPPED = "STOPPED"


@dataclass(frozen=True)
class SupervisedRuntimeStartupRequest:
    workspace_root: str | Path
    context_mode: ContextMode = ContextMode.IDE_MANUAL
    automation_stage: AutomationStage = AutomationStage.MANUAL
    route_stage: RouteStage = RouteStage.ACTIVE
    calibration_status: CalibrationStatus = CalibrationStatus.INSUFFICIENT_DATA
    threshold_action: PromotionAction | None = None
    review_required: bool = False
    manual_fallback_required: bool = False
    supervisor_present: bool = True
    explicit_approval: bool = False
    actor: str = "OPERATOR"
    reason: str = "Enable supervised runtime"
    action_timestamp: str | None = None


@dataclass(frozen=True)
class SupervisedRuntimeShutdownRequest:
    workspace_root: str | Path
    actor: str = "OPERATOR"
    reason: str = "Disable supervised runtime"
    drain: bool = True
    action_timestamp: str | None = None


@dataclass(frozen=True)
class SupervisedRuntimeLifecycleReceipt:
    status: SupervisedRuntimeLifecycleStatus
    requested_at: str
    control_state: OperatorControlState
    preferred_mode_active: bool
    runtime_state_path: str
    lifecycle_receipt_path: str
    lifecycle_ledger_path: str
    policy_evaluation: AutomationPolicyEvaluation | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class OperationalAcceptanceCriterion:
    criterion_id: str
    satisfied: bool
    summary: str
    evidence_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class SupervisedRuntimeStatusSnapshot:
    generated_at: str
    preferred_active_mode: bool
    runtime_state_path: str
    operator_control_state: OperatorControlState
    latest_daemon_service_status: str | None
    latest_daemon_service_receipt_path: str | None
    child_work_service_events: int
    recovery_replay_events: int
    external_execution_events: int
    acceptance_criteria: tuple[OperationalAcceptanceCriterion, ...]


@dataclass(frozen=True)
class OperationalRunbookReceipt:
    generated_at: str
    status_snapshot: SupervisedRuntimeStatusSnapshot
    markdown_path: str
    json_path: str


@dataclass(frozen=True)
class OperationalAcceptanceChecklistReceipt:
    generated_at: str
    status_snapshot: SupervisedRuntimeStatusSnapshot
    markdown_path: str
    json_path: str


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")
_RUNTIME_STATE_PATH = Path("ION/05_context/history/supervised_runtime/supervised_runtime_state.json")
_LIFECYCLE_RECEIPTS_DIR = Path("ION/05_context/history/supervised_runtime/receipts")
_LIFECYCLE_LEDGER_PATH = Path("ION/05_context/history/supervised_runtime/supervised_runtime_ledger.json")
_RUNBOOK_DIR = Path("ION/05_context/runtime_reports/operations/runbooks")
_ACCEPTANCE_DIR = Path("ION/05_context/runtime_reports/operations/acceptance")


class KernelOperationalHardeningManager:
    """Package and harden the supervised runtime surface for operators."""

    def __init__(
        self,
        *,
        policy: KernelAutomationPolicy | None = None,
        operator_controls: KernelOperatorControlManager | None = None,
    ) -> None:
        self._policy = policy or KernelAutomationPolicy()
        self._operator_controls = operator_controls or KernelOperatorControlManager()

    def start_supervised_runtime(
        self,
        request: SupervisedRuntimeStartupRequest,
    ) -> SupervisedRuntimeLifecycleReceipt:
        workspace_root = Path(request.workspace_root).resolve()
        requested_at = request.action_timestamp or _iso_now()
        control_state = self._operator_controls.load_state(workspace_root)

        notes: list[str] = []
        if control_state.service_mode is DaemonServiceControlMode.DRAINING:
            notes.append("RESUME_FROM_DRAINING")
        if control_state.service_mode is DaemonServiceControlMode.STOPPED:
            notes.append("RESUME_FROM_STOPPED")

        policy_request = AutomationPolicyRequest(
            action_class=AutomationActionClass.START_DAEMON_SERVICE,
            context_mode=request.context_mode,
            automation_stage=request.automation_stage,
            route_stage=request.route_stage,
            calibration_status=request.calibration_status,
            threshold_action=request.threshold_action,
            review_required=request.review_required,
            manual_fallback_required=request.manual_fallback_required,
            operator_stop=False,
            operator_hold=False,
            supervisor_present=request.supervisor_present,
            explicit_approval=request.explicit_approval,
            notes=tuple(notes),
        )
        evaluation = self._policy.evaluate(policy_request)
        if evaluation.decision is AutomationPolicyDecision.BLOCK:
            return self._persist_lifecycle(
                workspace_root,
                requested_at=requested_at,
                status=SupervisedRuntimeLifecycleStatus.POLICY_BLOCKED,
                control_state=control_state,
                preferred_mode_active=self._load_runtime_state(workspace_root)["preferred_active_mode"],
                policy_evaluation=evaluation,
                actor=request.actor,
                reason=request.reason,
                notes=tuple(evaluation.reasons),
            )
        if evaluation.decision is AutomationPolicyDecision.HOLD:
            return self._persist_lifecycle(
                workspace_root,
                requested_at=requested_at,
                status=SupervisedRuntimeLifecycleStatus.CONTROL_BLOCKED,
                control_state=control_state,
                preferred_mode_active=self._load_runtime_state(workspace_root)["preferred_active_mode"],
                policy_evaluation=evaluation,
                actor=request.actor,
                reason=request.reason,
                notes=tuple(evaluation.reasons),
            )
        if evaluation.decision is AutomationPolicyDecision.REQUIRE_APPROVAL:
            return self._persist_lifecycle(
                workspace_root,
                requested_at=requested_at,
                status=SupervisedRuntimeLifecycleStatus.APPROVAL_REQUIRED,
                control_state=control_state,
                preferred_mode_active=self._load_runtime_state(workspace_root)["preferred_active_mode"],
                policy_evaluation=evaluation,
                actor=request.actor,
                reason=request.reason,
                notes=tuple(evaluation.reasons),
            )

        if control_state.service_mode is DaemonServiceControlMode.ENABLED:
            status = SupervisedRuntimeLifecycleStatus.ALREADY_ENABLED
            updated_state = control_state
        else:
            mutation = self._operator_controls.set_service_mode(
                workspace_root,
                mode=DaemonServiceControlMode.ENABLED,
                reason=request.reason,
                actor=request.actor,
                created_at=requested_at,
            )
            updated_state = mutation.state
            status = SupervisedRuntimeLifecycleStatus.STARTED

        return self._persist_lifecycle(
            workspace_root,
            requested_at=requested_at,
            status=status,
            control_state=updated_state,
            preferred_mode_active=True,
            policy_evaluation=evaluation,
            actor=request.actor,
            reason=request.reason,
            notes=("PREFERRED_ACTIVE_AUTOMATION_MODE=SUPERVISED_RUNTIME",),
        )

    def shutdown_supervised_runtime(
        self,
        request: SupervisedRuntimeShutdownRequest,
    ) -> SupervisedRuntimeLifecycleReceipt:
        workspace_root = Path(request.workspace_root).resolve()
        requested_at = request.action_timestamp or _iso_now()
        target_mode = DaemonServiceControlMode.DRAINING if request.drain else DaemonServiceControlMode.STOPPED
        mutation = self._operator_controls.set_service_mode(
            workspace_root,
            mode=target_mode,
            reason=request.reason,
            actor=request.actor,
            created_at=requested_at,
        )
        status = (
            SupervisedRuntimeLifecycleStatus.DRAINING
            if request.drain
            else SupervisedRuntimeLifecycleStatus.STOPPED
        )
        return self._persist_lifecycle(
            workspace_root,
            requested_at=requested_at,
            status=status,
            control_state=mutation.state,
            preferred_mode_active=True,
            policy_evaluation=None,
            actor=request.actor,
            reason=request.reason,
            notes=(("SERVICE_DRAIN_REQUESTED",) if request.drain else ("SERVICE_STOP_REQUESTED",)),
        )

    def build_status_snapshot(self, workspace_root: str | Path) -> SupervisedRuntimeStatusSnapshot:
        root = Path(workspace_root).resolve()
        generated_at = _iso_now()
        runtime_state = self._load_runtime_state(root)
        control_state = self._operator_controls.load_state(root)
        daemon_rows = self._load_json_list(root, Path("ION/05_context/history/daemon_service_ledger.json"))
        child_rows = self._load_json_list(root, Path("ION/05_context/history/child_work_service_ledger.json"))
        replay_rows = self._load_json_list(root, Path("ION/05_context/history/recovery_replay_ledger.json"))
        bridge_rows = self._load_json_list(root, Path("ION/05_context/history/external_execution_bridge_ledger.json"))
        latest_daemon = daemon_rows[-1] if daemon_rows else None
        criteria = self._build_acceptance_criteria(
            root,
            runtime_state_path=str(_RUNTIME_STATE_PATH),
            control_state=control_state,
            latest_daemon=latest_daemon,
            child_rows=child_rows,
            replay_rows=replay_rows,
            bridge_rows=bridge_rows,
        )
        return SupervisedRuntimeStatusSnapshot(
            generated_at=generated_at,
            preferred_active_mode=bool(runtime_state["preferred_active_mode"]),
            runtime_state_path=str(_RUNTIME_STATE_PATH),
            operator_control_state=control_state,
            latest_daemon_service_status=(None if latest_daemon is None else str(latest_daemon.get("status"))),
            latest_daemon_service_receipt_path=(None if latest_daemon is None else _opt_str(latest_daemon.get("receipt_path"))),
            child_work_service_events=len(child_rows),
            recovery_replay_events=len(replay_rows),
            external_execution_events=len(bridge_rows),
            acceptance_criteria=criteria,
        )

    def write_operational_runbook(self, workspace_root: str | Path) -> OperationalRunbookReceipt:
        root = Path(workspace_root).resolve()
        snapshot = self.build_status_snapshot(root)
        generated_at = snapshot.generated_at
        stem = f"{_safe_id(generated_at)}-supervised-runtime-runbook"
        markdown_path = _resolve_relative_file(root, _RUNBOOK_DIR / f"{stem}.md")
        json_path = _resolve_relative_file(root, _RUNBOOK_DIR / f"{stem}.json")
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        md = self._render_runbook_markdown(snapshot)
        markdown_path.write_text(md, encoding="utf-8")
        json_path.write_text(json.dumps(_snapshot_payload(snapshot), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return OperationalRunbookReceipt(
            generated_at=generated_at,
            status_snapshot=snapshot,
            markdown_path=str(_RUNBOOK_DIR / markdown_path.name),
            json_path=str(_RUNBOOK_DIR / json_path.name),
        )

    def write_acceptance_checklist(self, workspace_root: str | Path) -> OperationalAcceptanceChecklistReceipt:
        root = Path(workspace_root).resolve()
        snapshot = self.build_status_snapshot(root)
        generated_at = snapshot.generated_at
        stem = f"{_safe_id(generated_at)}-operational-acceptance"
        markdown_path = _resolve_relative_file(root, _ACCEPTANCE_DIR / f"{stem}.md")
        json_path = _resolve_relative_file(root, _ACCEPTANCE_DIR / f"{stem}.json")
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(self._render_acceptance_markdown(snapshot), encoding="utf-8")
        json_path.write_text(json.dumps(_snapshot_payload(snapshot), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return OperationalAcceptanceChecklistReceipt(
            generated_at=generated_at,
            status_snapshot=snapshot,
            markdown_path=str(_ACCEPTANCE_DIR / markdown_path.name),
            json_path=str(_ACCEPTANCE_DIR / json_path.name),
        )

    def _persist_lifecycle(
        self,
        workspace_root: Path,
        *,
        requested_at: str,
        status: SupervisedRuntimeLifecycleStatus,
        control_state: OperatorControlState,
        preferred_mode_active: bool,
        policy_evaluation: AutomationPolicyEvaluation | None,
        actor: str,
        reason: str,
        notes: tuple[str, ...],
    ) -> SupervisedRuntimeLifecycleReceipt:
        runtime_state = self._load_runtime_state(workspace_root)
        lifecycle_count = int(runtime_state.get("lifecycle_events", 0)) + 1
        runtime_state_payload = {
            "updated_at": requested_at,
            "preferred_active_mode": preferred_mode_active,
            "preferred_runtime_surface": "SUPERVISED_DAEMON_SERVICE",
            "service_mode": control_state.service_mode.value,
            "lifecycle_events": lifecycle_count,
            "latest_status": status.value,
            "last_runtime_receipt_path": str(_LIFECYCLE_RECEIPTS_DIR / f"{_safe_id(requested_at)}.supervised_runtime_receipt.json"),
        }
        runtime_state_path = _resolve_relative_file(workspace_root, _RUNTIME_STATE_PATH)
        runtime_state_path.parent.mkdir(parents=True, exist_ok=True)
        runtime_state_path.write_text(json.dumps(runtime_state_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        receipt_relative_path = _LIFECYCLE_RECEIPTS_DIR / f"{_safe_id(requested_at)}.supervised_runtime_receipt.json"
        receipt_path = _resolve_relative_file(workspace_root, receipt_relative_path)
        ledger_path = _resolve_relative_file(workspace_root, _LIFECYCLE_LEDGER_PATH)
        receipt_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        receipt_payload = {
            "requested_at": requested_at,
            "status": status.value,
            "actor": actor,
            "reason": reason,
            "preferred_active_mode": preferred_mode_active,
            "control_state": _control_payload(control_state),
            "runtime_state_path": str(_RUNTIME_STATE_PATH),
            "policy_evaluation": (None if policy_evaluation is None else _policy_payload(policy_evaluation)),
            "notes": list(notes),
        }
        receipt_path.write_text(json.dumps(receipt_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        ledger_rows = self._load_json_list(workspace_root, _LIFECYCLE_LEDGER_PATH)
        ledger_rows.append(
            {
                "event_id": f"supervised-runtime-{_safe_id(requested_at)}",
                "created_at": requested_at,
                "status": status.value,
                "actor": actor,
                "reason": reason,
                "service_mode": control_state.service_mode.value,
                "preferred_active_mode": preferred_mode_active,
                "receipt_path": str(receipt_relative_path),
                "policy_decision": None if policy_evaluation is None else policy_evaluation.decision.value,
            }
        )
        ledger_path.write_text(json.dumps(ledger_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return SupervisedRuntimeLifecycleReceipt(
            status=status,
            requested_at=requested_at,
            control_state=control_state,
            preferred_mode_active=preferred_mode_active,
            runtime_state_path=str(_RUNTIME_STATE_PATH),
            lifecycle_receipt_path=str(receipt_relative_path),
            lifecycle_ledger_path=str(_LIFECYCLE_LEDGER_PATH),
            policy_evaluation=policy_evaluation,
            notes=notes,
        )

    def _load_runtime_state(self, workspace_root: Path) -> dict[str, Any]:
        path = _resolve_relative_file(workspace_root, _RUNTIME_STATE_PATH)
        if not path.exists():
            return {
                "updated_at": _iso_now(),
                "preferred_active_mode": False,
                "preferred_runtime_surface": "SUPERVISED_DAEMON_SERVICE",
                "service_mode": DaemonServiceControlMode.ENABLED.value,
                "lifecycle_events": 0,
                "latest_status": None,
                "last_runtime_receipt_path": None,
            }
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise KernelOperationalHardeningError("supervised runtime state must contain a JSON object")
        return payload

    def _load_json_list(self, workspace_root: Path, relative_path: Path) -> list[dict[str, Any]]:
        path = _resolve_relative_file(workspace_root, relative_path)
        if not path.exists():
            return []
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise KernelOperationalHardeningError(f"{relative_path} must contain a JSON list")
        return [item for item in payload if isinstance(item, dict)]

    def _build_acceptance_criteria(
        self,
        workspace_root: Path,
        *,
        runtime_state_path: str,
        control_state: OperatorControlState,
        latest_daemon: dict[str, Any] | None,
        child_rows: list[dict[str, Any]],
        replay_rows: list[dict[str, Any]],
        bridge_rows: list[dict[str, Any]],
    ) -> tuple[OperationalAcceptanceCriterion, ...]:
        criteria: list[OperationalAcceptanceCriterion] = []
        criteria.append(
            OperationalAcceptanceCriterion(
                criterion_id="A1",
                satisfied=True,
                summary=f"Operator control state is machine-readable (service_mode={control_state.service_mode.value}).",
                evidence_paths=(
                    "ION/04_packages/kernel/operator_control.py",
                    "ION/05_context/history/operator_controls/operator_control_state.json",
                ),
            )
        )
        criteria.append(
            OperationalAcceptanceCriterion(
                criterion_id="A2",
                satisfied=latest_daemon is not None,
                summary=(
                    "Daemon service has executed or been invoked through the supervised service path."
                    if latest_daemon is not None
                    else "Daemon service ledger evidence has not yet been written."
                ),
                evidence_paths=(
                    "ION/04_packages/kernel/daemon_service.py",
                    "ION/05_context/history/daemon_service_ledger.json",
                ),
            )
        )
        criteria.append(
            OperationalAcceptanceCriterion(
                criterion_id="A3",
                satisfied=Path(workspace_root, "ION/04_packages/kernel/automation_policy.py").exists(),
                summary="Automation actions can be refused lawfully through the policy floor.",
                evidence_paths=(
                    "ION/04_packages/kernel/automation_policy.py",
                    runtime_state_path,
                ),
            )
        )
        criteria.append(
            OperationalAcceptanceCriterion(
                criterion_id="A4",
                satisfied=bool(child_rows) or Path(workspace_root, "ION/04_packages/kernel/child_work_service.py").exists(),
                summary="Child-work issuance has an approval-aware supervised service path.",
                evidence_paths=(
                    "ION/04_packages/kernel/child_work_service.py",
                    "ION/05_context/history/child_work_service_ledger.json",
                ),
            )
        )
        criteria.append(
            OperationalAcceptanceCriterion(
                criterion_id="A5",
                satisfied=bool(replay_rows) or Path(workspace_root, "ION/04_packages/kernel/recovery_replay.py").exists(),
                summary="Recovery and replay are available before stronger autonomy claims.",
                evidence_paths=(
                    "ION/04_packages/kernel/recovery_replay.py",
                    "ION/05_context/history/recovery_replay_ledger.json",
                ),
            )
        )
        criteria.append(
            OperationalAcceptanceCriterion(
                criterion_id="A6",
                satisfied=Path(workspace_root, "ION/06_intelligence/research/2026-04-08_ion_operationalization_master_plan.md").exists(),
                summary="Witness/report surfaces remain subordinate to the operational kernel by plan and protocol.",
                evidence_paths=(
                    "ION/06_intelligence/research/2026-04-08_ion_operationalization_master_plan.md",
                    "ION/05_context/comms/migration_ledgers/automation_operationalization_ledger.md",
                    "ION/05_context/history/external_execution_bridge_ledger.json",
                ) if bridge_rows else (
                    "ION/06_intelligence/research/2026-04-08_ion_operationalization_master_plan.md",
                    "ION/05_context/comms/migration_ledgers/automation_operationalization_ledger.md",
                ),
            )
        )
        return tuple(criteria)

    def _render_runbook_markdown(self, snapshot: SupervisedRuntimeStatusSnapshot) -> str:
        criteria_lines = "\n".join(
            f"- [{ 'x' if criterion.satisfied else ' '}] {criterion.criterion_id}: {criterion.summary}"
            for criterion in snapshot.acceptance_criteria
        )
        return f"""---
type: operational_runbook
authority: A3_OPERATIONAL
generated_at: {snapshot.generated_at}
status: ACTIVE
preferred_active_mode: {str(snapshot.preferred_active_mode).lower()}
service_mode: {snapshot.operator_control_state.service_mode.value}
---

# Supervised Runtime Runbook

## Current status

- Preferred active automation mode: {'enabled' if snapshot.preferred_active_mode else 'not yet packaged'}
- Operator service mode: {snapshot.operator_control_state.service_mode.value}
- Latest daemon service status: {snapshot.latest_daemon_service_status or 'NONE'}
- Latest daemon service receipt: {snapshot.latest_daemon_service_receipt_path or 'NONE'}
- Child-work service events: {snapshot.child_work_service_events}
- Recovery/replay events: {snapshot.recovery_replay_events}
- External execution bridge events: {snapshot.external_execution_events}

## Startup sequence

1. Ensure operator control state is lawful and no scope hold blocks the intended run.
2. Start supervised runtime through `KernelOperationalHardeningManager.start_supervised_runtime(...)`.
3. Run bounded daemon service cycles through `KernelDaemonService.run(...)` with explicit policy and operator context.
4. Use child-work issuance, recovery/replay, and external execution bridge only through their supervised service paths.

## Shutdown sequence

1. Request draining shutdown when in-flight work should finish without admitting new service action.
2. Request stopped shutdown for an immediate operator-controlled stop.
3. Confirm the resulting operator service mode in the operator control state and supervised runtime lifecycle receipt.

## Acceptance overview

{criteria_lines}
"""

    def _render_acceptance_markdown(self, snapshot: SupervisedRuntimeStatusSnapshot) -> str:
        rows = "\n".join(
            f"- [{ 'x' if criterion.satisfied else ' '}] {criterion.criterion_id}: {criterion.summary}"
            for criterion in snapshot.acceptance_criteria
        )
        return f"""---
type: operational_acceptance_checklist
authority: A3_OPERATIONAL
generated_at: {snapshot.generated_at}
status: ACTIVE
preferred_active_mode: {str(snapshot.preferred_active_mode).lower()}
service_mode: {snapshot.operator_control_state.service_mode.value}
---

# Operational Acceptance Checklist

{rows}
"""


IonOperationalHardeningManager = KernelOperationalHardeningManager


def _snapshot_payload(snapshot: SupervisedRuntimeStatusSnapshot) -> dict[str, Any]:
    return {
        "generated_at": snapshot.generated_at,
        "preferred_active_mode": snapshot.preferred_active_mode,
        "runtime_state_path": snapshot.runtime_state_path,
        "operator_control_state": _control_payload(snapshot.operator_control_state),
        "latest_daemon_service_status": snapshot.latest_daemon_service_status,
        "latest_daemon_service_receipt_path": snapshot.latest_daemon_service_receipt_path,
        "child_work_service_events": snapshot.child_work_service_events,
        "recovery_replay_events": snapshot.recovery_replay_events,
        "external_execution_events": snapshot.external_execution_events,
        "acceptance_criteria": [
            {
                "criterion_id": criterion.criterion_id,
                "satisfied": criterion.satisfied,
                "summary": criterion.summary,
                "evidence_paths": list(criterion.evidence_paths),
            }
            for criterion in snapshot.acceptance_criteria
        ],
    }


def _policy_payload(evaluation: AutomationPolicyEvaluation) -> dict[str, object]:
    return {
        "decision": evaluation.decision.value,
        "reasons": list(evaluation.reasons),
        "required_controls": list(evaluation.required_controls),
    }


def _control_payload(state: OperatorControlState) -> dict[str, object]:
    return {
        "updated_at": state.updated_at,
        "service_mode": state.service_mode.value,
        "scope_holds": [asdict(hold) for hold in state.scope_holds],
        "global_notes": list(state.global_notes),
    }


def _resolve_relative_file(workspace_root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelOperationalHardeningError("relative paths must be relative to workspace_root")
    return workspace_root / relative_path


def _safe_id(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "runtime"


def _opt_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
