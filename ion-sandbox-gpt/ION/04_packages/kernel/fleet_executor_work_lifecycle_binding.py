"""Bounded fleet-member -> executor-work lifecycle bridge.

Target 2 / Slice 3:

- bridge one active fleet member and one matching executor capability into one explicit
  executor-entry receipt for one already-dispatched work unit;
- keep this subordinate to activation authority, schedule/dispatch witness, and executor
  lifecycle law;
- avoid importing mission-control, swarm cycles, or any broader orchestrator shell.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
import uuid

from .fleet_lifecycle_store import FleetLifecycleStore, FleetLifecycleStoreError, FleetMemberState
from .index import KernelIndex
from .model import (
    ExecutorAvailability,
    ExecutorCapability,
    ExecutorWorkLifecycleBindingReceipt,
    ScheduleDispatchReconciliationReceipt,
    WorkUnit,
    WorkUnitStatus,
)
from .store import KernelStore


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class FleetExecutorWorkLifecycleBindingError(Exception):
    """Raised when one fleet/executor/work entry binding cannot complete lawfully."""


@dataclass(frozen=True)
class FleetExecutorWorkEntryResult:
    receipt: ExecutorWorkLifecycleBindingReceipt
    work_unit_before: WorkUnit
    work_unit_after: WorkUnit


class FleetExecutorWorkLifecycleBinder:
    """Advance a dispatched work unit into explicit executor-entry using fleet witness."""

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "T2_EXECUTOR_WORK_LIFECYCLE_BINDING_V1",
            "notes": (
                "This bridge never invents activation authority; it only proves executor-entry alignment.",
                "A fleet member must already be active and materially bound into executor capability truth.",
                "The bridge requires an existing schedule/dispatch witness and moves work from DISPATCHED to EXECUTING only.",
            ),
        }

    def enter_execution(
        self,
        *,
        fleet_store: FleetLifecycleStore,
        kernel_store: KernelStore,
        kernel_index: KernelIndex,
        fleet_id: str,
        member_id: str,
        work_unit_id: str,
        generated_at: str | None = None,
    ) -> FleetExecutorWorkEntryResult:
        timestamp = generated_at or _utc_now()
        member = fleet_store.read_member(member_id)
        if member.fleet_id != fleet_id:
            raise FleetExecutorWorkLifecycleBindingError(
                f"Fleet member {member_id} does not belong to fleet {fleet_id}"
            )
        if member.state is not FleetMemberState.ACTIVE:
            raise FleetExecutorWorkLifecycleBindingError(
                f"Fleet member is not ACTIVE: {member_id} ({member.state.value})"
            )

        capability_id = f"cap-{member_id}"
        capability = kernel_index.get("executor_capability", capability_id)
        if not isinstance(capability, ExecutorCapability):
            raise FleetExecutorWorkLifecycleBindingError(
                f"Missing executor capability for fleet member {member_id}: {capability_id}"
            )
        if capability.executor_id != member_id:
            raise FleetExecutorWorkLifecycleBindingError(
                f"Executor capability mismatch for fleet member {member_id}: {capability.executor_id}"
            )
        if capability.availability not in (ExecutorAvailability.AVAILABLE, ExecutorAvailability.DEGRADED):
            raise FleetExecutorWorkLifecycleBindingError(
                f"Executor capability is not execution-eligible: {capability_id} ({capability.availability.value})"
            )

        work_unit = kernel_index.get("work_unit", work_unit_id)
        if not isinstance(work_unit, WorkUnit):
            raise FleetExecutorWorkLifecycleBindingError(f"Unknown work unit: {work_unit_id}")
        if work_unit.status is not WorkUnitStatus.DISPATCHED:
            raise FleetExecutorWorkLifecycleBindingError(
                f"Work unit must be DISPATCHED before executor entry: {work_unit_id} ({work_unit.status.value})"
            )

        dispatch_receipt = self._matching_dispatch_receipt(
            kernel_index,
            scope_type=str(work_unit.scope_type.value),
            scope_ref=work_unit.scope_ref,
            work_unit_id=work_unit_id,
        )
        if dispatch_receipt is None:
            raise FleetExecutorWorkLifecycleBindingError(
                f"No schedule dispatch reconciliation receipt exists for work unit {work_unit_id}"
            )
        warnings: list[str] = []
        if dispatch_receipt.selected_executor_id and dispatch_receipt.selected_executor_id != member_id:
            raise FleetExecutorWorkLifecycleBindingError(
                f"Selected executor mismatch: dispatch={dispatch_receipt.selected_executor_id} member={member_id}"
            )
        if dispatch_receipt.selected_capability_id and dispatch_receipt.selected_capability_id != capability_id:
            raise FleetExecutorWorkLifecycleBindingError(
                f"Selected capability mismatch: dispatch={dispatch_receipt.selected_capability_id} capability={capability_id}"
            )
        if not dispatch_receipt.selected_executor_id:
            warnings.append("DISPATCH_RECEIPT_MISSING_SELECTED_EXECUTOR_ID")
        if not dispatch_receipt.selected_capability_id:
            warnings.append("DISPATCH_RECEIPT_MISSING_SELECTED_CAPABILITY_ID")

        work_unit_after = replace(work_unit, status=WorkUnitStatus.EXECUTING)
        kernel_store.replace(work_unit_after)
        kernel_index.record_changed(work_unit_after)

        receipt = ExecutorWorkLifecycleBindingReceipt(
            receipt_id=f"ewlb-{uuid.uuid4().hex[:12]}",
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=str(work_unit.scope_type.value),
            scope_ref=work_unit.scope_ref,
            fleet_id=fleet_id,
            member_id=member_id,
            executor_id=member_id,
            capability_id=capability_id,
            source_schedule_dispatch_reconciliation_receipt_id=dispatch_receipt.receipt_id,
            work_unit_id=work_unit_id,
            lifecycle_action="ENTER_EXECUTION",
            work_unit_status_before=work_unit.status,
            work_unit_status_after=work_unit_after.status,
            selected_carrier=dispatch_receipt.selected_carrier,
            selected_executor_id=(dispatch_receipt.selected_executor_id or member_id),
            selected_capability_id=(dispatch_receipt.selected_capability_id or capability_id),
            dispatch_packet_path=dispatch_receipt.dispatch_packet_path,
            warnings=tuple(dict.fromkeys(warnings)),
        )
        kernel_store.create(receipt)
        kernel_index.record_added(receipt)
        return FleetExecutorWorkEntryResult(
            receipt=receipt,
            work_unit_before=work_unit,
            work_unit_after=work_unit_after,
        )

    def latest_receipt(
        self,
        index: KernelIndex,
        *,
        work_unit_id: str | None = None,
        scope_type: str | None = None,
        scope_ref: str | None = None,
    ) -> ExecutorWorkLifecycleBindingReceipt | None:
        receipts = [
            r
            for r in index.records_by_type("executor_work_lifecycle_binding_receipt")
            if isinstance(r, ExecutorWorkLifecycleBindingReceipt)
        ]
        if work_unit_id is not None:
            receipts = [r for r in receipts if r.work_unit_id == work_unit_id]
        if scope_type is not None or scope_ref is not None:
            if not (scope_type and scope_ref):
                raise FleetExecutorWorkLifecycleBindingError("scope_type and scope_ref must be provided together")
            receipts = [r for r in receipts if r.scope_type == scope_type and r.scope_ref == scope_ref]
        if not receipts:
            return None
        receipts.sort(key=lambda r: (r.created_at, r.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ExecutorWorkLifecycleBindingReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "fleet_id": receipt.fleet_id,
            "member_id": receipt.member_id,
            "executor_id": receipt.executor_id,
            "capability_id": receipt.capability_id,
            "source_schedule_dispatch_reconciliation_receipt_id": receipt.source_schedule_dispatch_reconciliation_receipt_id,
            "work_unit_id": receipt.work_unit_id,
            "lifecycle_action": receipt.lifecycle_action,
            "work_unit_status_before": None if receipt.work_unit_status_before is None else receipt.work_unit_status_before.value,
            "work_unit_status_after": None if receipt.work_unit_status_after is None else receipt.work_unit_status_after.value,
            "selected_carrier": None if receipt.selected_carrier is None else receipt.selected_carrier.value,
            "selected_executor_id": receipt.selected_executor_id,
            "selected_capability_id": receipt.selected_capability_id,
            "dispatch_packet_path": receipt.dispatch_packet_path,
            "warnings": list(receipt.warnings),
        }

    def _matching_dispatch_receipt(self, index: KernelIndex, *, scope_type: str, scope_ref: str, work_unit_id: str) -> ScheduleDispatchReconciliationReceipt | None:
        receipts = [
            r
            for r in index.schedule_dispatch_receipts_for_scope(scope_type, scope_ref)
            if isinstance(r, ScheduleDispatchReconciliationReceipt) and r.work_unit_id == work_unit_id
        ]
        if not receipts:
            return None
        receipts.sort(key=lambda r: (r.created_at, r.receipt_id))
        return receipts[-1]
