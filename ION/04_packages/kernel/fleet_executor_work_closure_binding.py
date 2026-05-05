"""Bounded executor-work closure witnesses on top of fleet/executor entry.

Target 2 / Slice 4:

- make executor return-for-validation explicit;
- make executor execution failure explicit;
- bind terminal work-unit state into schedule completion release with an explicit closure witness;
- avoid introducing mission-control, swarm loops, or hidden authority.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
import uuid

from .fleet_lifecycle_store import FleetLifecycleStore, FleetMemberState
from .fleet_executor_work_lifecycle_binding import (
    FleetExecutorWorkLifecycleBindingError,
    FleetExecutorWorkLifecycleBinder,
)
from .execution import ExecutionSubmission, KernelExecutor, KernelExecutionError
from .index import KernelIndex
from .model import (
    CommitDeltaStatus,
    ExecutorWorkLifecycleBindingReceipt,
    WorkUnit,
    WorkUnitStatus,
)
from .schedule_completion_release import (
    KernelScheduleCompletionReleaseError,
    KernelScheduleCompletionReleaseManager,
)
from .store import KernelStore


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class FleetExecutorWorkClosureBindingError(Exception):
    """Raised when one executor-work closure witness cannot be created lawfully."""


@dataclass(frozen=True)
class FleetExecutorWorkClosureResult:
    receipt: ExecutorWorkLifecycleBindingReceipt
    work_unit_before: WorkUnit
    work_unit_after: WorkUnit


class FleetExecutorWorkClosureBinder:
    """Emit explicit executor return/failure/release witnesses for one work unit."""

    def __init__(self) -> None:
        self._entry = FleetExecutorWorkLifecycleBinder()
        self._release = KernelScheduleCompletionReleaseManager()

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "T2_EXECUTOR_WORK_CLOSURE_BINDING_V1",
            "notes": (
                "Closure witnesses never invent activation authority; they only classify return, failure, and release after executor entry.",
                "Return-for-validation is distinct from terminal release and must preserve the validating stage explicitly.",
                "Release remains subordinate to existing schedule completion-release law rather than replacing it.",
            ),
        }

    def return_for_validation(
        self,
        *,
        fleet_store: FleetLifecycleStore,
        kernel_store: KernelStore,
        kernel_index: KernelIndex,
        fleet_id: str,
        member_id: str,
        work_unit_id: str,
        generated_at: str | None = None,
    ) -> FleetExecutorWorkClosureResult:
        timestamp = generated_at or _utc_now()
        entry_receipt, work_unit = self._require_entry_alignment(
            fleet_store=fleet_store,
            kernel_index=kernel_index,
            fleet_id=fleet_id,
            member_id=member_id,
            work_unit_id=work_unit_id,
            allowed_status=WorkUnitStatus.EXECUTING,
        )
        work_unit_after = replace(work_unit, status=WorkUnitStatus.VALIDATING)
        kernel_store.replace(work_unit_after)
        kernel_index.record_changed(work_unit_after)
        receipt = self._emit_closure_receipt(
            kernel_store=kernel_store,
            kernel_index=kernel_index,
            entry_receipt=entry_receipt,
            created_at=timestamp,
            lifecycle_action="RETURN_FOR_VALIDATION",
            work_unit_before=work_unit,
            work_unit_after=work_unit_after,
        )
        return FleetExecutorWorkClosureResult(receipt=receipt, work_unit_before=work_unit, work_unit_after=work_unit_after)


    def submit_execution_return(
        self,
        *,
        fleet_store: FleetLifecycleStore,
        kernel_store: KernelStore,
        kernel_index: KernelIndex,
        executor: KernelExecutor,
        fleet_id: str,
        member_id: str,
        work_unit_id: str,
        submission: ExecutionSubmission,
    ) -> FleetExecutorWorkClosureResult:
        entry_receipt, work_unit = self._require_entry_alignment(
            fleet_store=fleet_store,
            kernel_index=kernel_index,
            fleet_id=fleet_id,
            member_id=member_id,
            work_unit_id=work_unit_id,
            allowed_status=WorkUnitStatus.EXECUTING,
        )
        try:
            execution_result = executor.submit_execution(
                kernel_store,
                kernel_index,
                work_unit_id,
                submission,
            )
        except KernelExecutionError as exc:
            raise FleetExecutorWorkClosureBindingError(str(exc)) from exc
        receipt = self._emit_closure_receipt(
            kernel_store=kernel_store,
            kernel_index=kernel_index,
            entry_receipt=entry_receipt,
            created_at=(submission.created_at or _utc_now()),
            lifecycle_action="RETURN_FOR_VALIDATION",
            work_unit_before=execution_result.work_unit_before,
            work_unit_after=execution_result.work_unit_after,
        )
        return FleetExecutorWorkClosureResult(
            receipt=receipt,
            work_unit_before=execution_result.work_unit_before,
            work_unit_after=execution_result.work_unit_after,
        )

    def fail_execution(
        self,
        *,
        fleet_store: FleetLifecycleStore,
        kernel_store: KernelStore,
        kernel_index: KernelIndex,
        fleet_id: str,
        member_id: str,
        work_unit_id: str,
        failure_reason: str | None = None,
        generated_at: str | None = None,
    ) -> FleetExecutorWorkClosureResult:
        timestamp = generated_at or _utc_now()
        entry_receipt, work_unit = self._require_entry_alignment(
            fleet_store=fleet_store,
            kernel_index=kernel_index,
            fleet_id=fleet_id,
            member_id=member_id,
            work_unit_id=work_unit_id,
            allowed_status=WorkUnitStatus.EXECUTING,
        )
        work_unit_after = replace(work_unit, status=WorkUnitStatus.FAILED)
        kernel_store.replace(work_unit_after)
        kernel_index.record_changed(work_unit_after)
        receipt = self._emit_closure_receipt(
            kernel_store=kernel_store,
            kernel_index=kernel_index,
            entry_receipt=entry_receipt,
            created_at=timestamp,
            lifecycle_action="FAIL_EXECUTION",
            work_unit_before=work_unit,
            work_unit_after=work_unit_after,
            closure_reason=failure_reason,
        )
        return FleetExecutorWorkClosureResult(receipt=receipt, work_unit_before=work_unit, work_unit_after=work_unit_after)

    def release_terminal_work(
        self,
        *,
        fleet_store: FleetLifecycleStore,
        kernel_store: KernelStore,
        kernel_index: KernelIndex,
        fleet_id: str,
        member_id: str,
        work_unit_id: str,
        generated_at: str | None = None,
    ) -> FleetExecutorWorkClosureResult:
        timestamp = generated_at or _utc_now()
        entry_receipt, work_unit = self._require_entry_alignment(
            fleet_store=fleet_store,
            kernel_index=kernel_index,
            fleet_id=fleet_id,
            member_id=member_id,
            work_unit_id=work_unit_id,
            allowed_status=None,
        )
        if work_unit.status not in (WorkUnitStatus.COMMITTED, WorkUnitStatus.FAILED, WorkUnitStatus.BLOCKED):
            raise FleetExecutorWorkClosureBindingError(
                f"Work unit is not terminal for release: {work_unit_id} ({work_unit.status.value})"
            )
        try:
            release_receipt = self._release.reconcile_release(
                kernel_store,
                kernel_index,
                scope_type=str(work_unit.scope_type.value),
                scope_ref=work_unit.scope_ref,
                generated_at=timestamp,
            )
        except KernelScheduleCompletionReleaseError as exc:
            raise FleetExecutorWorkClosureBindingError(str(exc)) from exc
        action = {
            WorkUnitStatus.COMMITTED: "RELEASE_AFTER_COMPLETION",
            WorkUnitStatus.FAILED: "RELEASE_AFTER_FAILURE",
            WorkUnitStatus.BLOCKED: "RELEASE_AFTER_BLOCK",
        }[work_unit.status]
        latest_delta_id = release_receipt.terminal_commit_delta_id
        latest_delta_status = release_receipt.terminal_commit_delta_status
        receipt = self._emit_closure_receipt(
            kernel_store=kernel_store,
            kernel_index=kernel_index,
            entry_receipt=entry_receipt,
            created_at=timestamp,
            lifecycle_action=action,
            work_unit_before=work_unit,
            work_unit_after=work_unit,
            source_schedule_completion_release_receipt_id=release_receipt.receipt_id,
            terminal_commit_delta_id=latest_delta_id,
            terminal_commit_delta_status=latest_delta_status,
            closure_reason=release_receipt.release_reason,
            warnings=release_receipt.warnings,
        )
        return FleetExecutorWorkClosureResult(receipt=receipt, work_unit_before=work_unit, work_unit_after=work_unit)

    def latest_receipt(
        self,
        index: KernelIndex,
        *,
        work_unit_id: str | None = None,
        lifecycle_actions: tuple[str, ...] | None = None,
    ) -> ExecutorWorkLifecycleBindingReceipt | None:
        receipts = [
            r for r in index.records_by_type("executor_work_lifecycle_binding_receipt")
            if isinstance(r, ExecutorWorkLifecycleBindingReceipt)
        ]
        if work_unit_id is not None:
            receipts = [r for r in receipts if r.work_unit_id == work_unit_id]
        if lifecycle_actions is not None:
            allowed = set(lifecycle_actions)
            receipts = [r for r in receipts if r.lifecycle_action in allowed]
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def _require_entry_alignment(
        self,
        *,
        fleet_store: FleetLifecycleStore,
        kernel_index: KernelIndex,
        fleet_id: str,
        member_id: str,
        work_unit_id: str,
        allowed_status: WorkUnitStatus | None,
    ) -> tuple[ExecutorWorkLifecycleBindingReceipt, WorkUnit]:
        member = fleet_store.read_member(member_id)
        if member.fleet_id != fleet_id:
            raise FleetExecutorWorkClosureBindingError(
                f"Fleet member {member_id} does not belong to fleet {fleet_id}"
            )
        if member.state is FleetMemberState.TERMINATED:
            raise FleetExecutorWorkClosureBindingError(
                f"Fleet member has terminated and cannot close work: {member_id}"
            )
        entry_receipt = self.latest_receipt(
            kernel_index,
            work_unit_id=work_unit_id,
            lifecycle_actions=("ENTER_EXECUTION",),
        )
        if entry_receipt is None:
            raise FleetExecutorWorkClosureBindingError(
                f"No executor entry receipt exists for work unit {work_unit_id}"
            )
        if entry_receipt.member_id != member_id or entry_receipt.fleet_id != fleet_id:
            raise FleetExecutorWorkClosureBindingError(
                f"Executor entry receipt mismatch for work unit {work_unit_id}: fleet/member do not align"
            )
        work_unit = kernel_index.get("work_unit", work_unit_id)
        if not isinstance(work_unit, WorkUnit):
            raise FleetExecutorWorkClosureBindingError(f"Unknown work unit: {work_unit_id}")
        if allowed_status is not None and work_unit.status is not allowed_status:
            raise FleetExecutorWorkClosureBindingError(
                f"Work unit must be {allowed_status.value} for this closure action: {work_unit_id} ({work_unit.status.value})"
            )
        return entry_receipt, work_unit

    def _emit_closure_receipt(
        self,
        *,
        kernel_store: KernelStore,
        kernel_index: KernelIndex,
        entry_receipt: ExecutorWorkLifecycleBindingReceipt,
        created_at: str,
        lifecycle_action: str,
        work_unit_before: WorkUnit,
        work_unit_after: WorkUnit,
        source_schedule_completion_release_receipt_id: str | None = None,
        terminal_commit_delta_id: str | None = None,
        terminal_commit_delta_status: CommitDeltaStatus | None = None,
        closure_reason: str | None = None,
        warnings: tuple[str, ...] = (),
    ) -> ExecutorWorkLifecycleBindingReceipt:
        receipt = ExecutorWorkLifecycleBindingReceipt(
            receipt_id=f"ewlb-{uuid.uuid4().hex[:12]}",
            created_at=created_at,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=entry_receipt.scope_type,
            scope_ref=entry_receipt.scope_ref,
            fleet_id=entry_receipt.fleet_id,
            member_id=entry_receipt.member_id,
            executor_id=entry_receipt.executor_id,
            capability_id=entry_receipt.capability_id,
            source_schedule_dispatch_reconciliation_receipt_id=entry_receipt.source_schedule_dispatch_reconciliation_receipt_id,
            work_unit_id=entry_receipt.work_unit_id,
            lifecycle_action=lifecycle_action,
            source_executor_work_lifecycle_binding_receipt_id=entry_receipt.receipt_id,
            source_schedule_completion_release_receipt_id=source_schedule_completion_release_receipt_id,
            terminal_commit_delta_id=terminal_commit_delta_id,
            terminal_commit_delta_status=terminal_commit_delta_status,
            closure_reason=closure_reason,
            work_unit_status_before=work_unit_before.status,
            work_unit_status_after=work_unit_after.status,
            selected_carrier=entry_receipt.selected_carrier,
            selected_executor_id=entry_receipt.selected_executor_id,
            selected_capability_id=entry_receipt.selected_capability_id,
            dispatch_packet_path=entry_receipt.dispatch_packet_path,
            warnings=tuple(dict.fromkeys(warnings)),
        )
        kernel_store.create(receipt)
        kernel_index.record_added(receipt)
        return receipt
