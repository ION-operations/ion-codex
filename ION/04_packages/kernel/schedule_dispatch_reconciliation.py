
"""M7 schedule dispatch / assignment reconciliation surfaces."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from pathlib import Path
import re

from .branch_rescheduling import KernelBranchRescheduler
from .dispatch import KernelDispatcher
from .graph import KernelGraph
from .index import KernelIndex
from .model import (
    ExecutorCapability,
    ScheduleDispatchReconciliationReceipt,
    ScheduleReceipt,
    ScheduleSourceKind,
    WorkUnit,
    WorkUnitStatus,
)
from .schedule_controls import KernelScheduleControlManager
from .scheduler import KernelScheduler
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleDispatchReconciliationError(Exception):
    """Raised when one dispatch reconciliation operation cannot be completed."""


class KernelScheduleDispatchReconciliationManager:
    def __init__(self) -> None:
        self._scheduler = KernelScheduler()
        self._controls = KernelScheduleControlManager()
        self._branch_rescheduler = KernelBranchRescheduler()
        self._dispatcher = KernelDispatcher(scheduler=self._scheduler)

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M7_SCHEDULE_DISPATCH_RECONCILIATION_V1",
            "notes": (
                "Schedule witness must reconcile with assignment and dispatch reality explicitly.",
                "Execution authority retires future-only schedule witness without deleting the witness itself.",
                "M7 may increment active assignments for a selected capability, but it does not close the assignment lifecycle.",
            ),
        }

    def reconcile(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        scope_type: str,
        scope_ref: str,
        generated_at: str | None = None,
        packet_output_root: str | Path | None = None,
    ) -> ScheduleDispatchReconciliationReceipt:
        timestamp = generated_at or _iso_now()
        schedule = self._scheduler.latest_schedule_receipt(index, scope_type, scope_ref)
        if schedule is None:
            raise KernelScheduleDispatchReconciliationError(f"No schedule receipt exists for {scope_type}:{scope_ref}")

        source_control = self._controls.latest_receipt(index, scope_type, scope_ref)
        source_branch_reschedule = self._latest_branch_reschedule(index, scope_type, scope_ref)
        work_unit = self._resolve_work_unit(index, schedule)

        warnings: list[str] = list(schedule.warnings)
        retired_schedule_receipt_ids: tuple[str, ...] = ()
        retired_schedule_control_receipt_ids: tuple[str, ...] = ()
        dispatch_packet_path: str | None = None
        capability_delta = 0
        capability_before = None
        capability_after = None
        status_before = None if work_unit is None else work_unit.status
        status_after = status_before
        action = "NO_ASSIGNABLE_WORK_UNIT"

        if work_unit is None:
            warnings.append("Schedule receipt did not resolve to an assignable work unit.")
        elif work_unit.status is WorkUnitStatus.PENDING:
            capability_before, capability_after, capability_delta, cap_warn = self._apply_assignment_if_needed(
                store,
                index,
                schedule,
                timestamp,
            )
            warnings.extend(cap_warn)
            packet_path = None
            if packet_output_root is not None:
                packet_path = Path(packet_output_root).resolve() / f"{work_unit.work_unit_id}.dispatch.packet.json"
            result = self._dispatcher.dispatch_work_unit(
                store,
                index,
                graph,
                work_unit.work_unit_id,
                dispatched_at=timestamp,
                packet_output_path=packet_path,
            )
            dispatch_packet_path = None if result.packet_path is None else str(result.packet_path)
            status_after = result.work_unit_after.status
            action = "DISPATCHED_AND_ASSIGNED" if capability_delta else "DISPATCHED"
            retired_schedule_receipt_ids = tuple(r.receipt_id for r in index.schedule_receipts_for_scope(scope_type, scope_ref))
            retired_schedule_control_receipt_ids = tuple(r.receipt_id for r in index.schedule_control_receipts_for_scope(scope_type, scope_ref))
        elif work_unit.status in (WorkUnitStatus.DISPATCHED, WorkUnitStatus.EXECUTING, WorkUnitStatus.VALIDATING):
            action = "EXECUTION_ALREADY_AUTHORITATIVE"
            status_after = work_unit.status
            retired_schedule_receipt_ids = tuple(r.receipt_id for r in index.schedule_receipts_for_scope(scope_type, scope_ref))
            retired_schedule_control_receipt_ids = tuple(r.receipt_id for r in index.schedule_control_receipts_for_scope(scope_type, scope_ref))
        else:
            action = "ASSIGNMENT_DEFERRED"
            warnings.append(f"Work unit status {work_unit.status.value} is not ready for dispatch reconciliation.")
            status_after = work_unit.status

        receipt = ScheduleDispatchReconciliationReceipt(
            receipt_id=schedule_dispatch_reconciliation_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_receipt_id=schedule.receipt_id,
            source_schedule_control_receipt_id=(None if source_control is None else source_control.receipt_id),
            source_branch_reschedule_receipt_id=(None if source_branch_reschedule is None else source_branch_reschedule.receipt_id),
            work_unit_id=(None if work_unit is None else work_unit.work_unit_id),
            schedule_source_kind=schedule.source_kind,
            assignment_action=action,
            work_unit_status_before=status_before,
            work_unit_status_after=status_after,
            dispatch_packet_path=dispatch_packet_path,
            selected_carrier=schedule.selected_carrier,
            selected_executor_id=schedule.selected_executor_id,
            selected_capability_id=schedule.selected_capability_id,
            capability_assignment_delta=capability_delta,
            capability_assignments_before=capability_before,
            capability_assignments_after=capability_after,
            retired_schedule_receipt_ids=retired_schedule_receipt_ids,
            retired_schedule_control_receipt_ids=retired_schedule_control_receipt_ids,
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_receipt(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleDispatchReconciliationReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type("schedule_dispatch_reconciliation_receipt") if isinstance(r, ScheduleDispatchReconciliationReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_dispatch_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleDispatchReconciliationError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleDispatchReconciliationReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_receipt_id": receipt.source_schedule_receipt_id,
            "source_schedule_control_receipt_id": receipt.source_schedule_control_receipt_id,
            "source_branch_reschedule_receipt_id": receipt.source_branch_reschedule_receipt_id,
            "work_unit_id": receipt.work_unit_id,
            "schedule_source_kind": (None if receipt.schedule_source_kind is None else receipt.schedule_source_kind.value),
            "assignment_action": receipt.assignment_action,
            "work_unit_status_before": (None if receipt.work_unit_status_before is None else receipt.work_unit_status_before.value),
            "work_unit_status_after": (None if receipt.work_unit_status_after is None else receipt.work_unit_status_after.value),
            "dispatch_packet_path": receipt.dispatch_packet_path,
            "selected_carrier": (None if receipt.selected_carrier is None else receipt.selected_carrier.value),
            "selected_executor_id": receipt.selected_executor_id,
            "selected_capability_id": receipt.selected_capability_id,
            "capability_assignment_delta": receipt.capability_assignment_delta,
            "capability_assignments_before": receipt.capability_assignments_before,
            "capability_assignments_after": receipt.capability_assignments_after,
            "retired_schedule_receipt_ids": list(receipt.retired_schedule_receipt_ids),
            "retired_schedule_control_receipt_ids": list(receipt.retired_schedule_control_receipt_ids),
            "warnings": list(receipt.warnings),
        }

    def _resolve_work_unit(self, index: KernelIndex, schedule: ScheduleReceipt) -> WorkUnit | None:
        if schedule.source_kind is not ScheduleSourceKind.WORK_UNIT:
            return None
        record = index.get("work_unit", schedule.source_record_id)
        return record if isinstance(record, WorkUnit) else None

    def _latest_branch_reschedule(self, index: KernelIndex, scope_type: str, scope_ref: str):
        if scope_type.strip().upper() == "WORK_UNIT":
            return self._branch_rescheduler.latest_receipt(index, "WORK_UNIT", scope_ref)
        return None

    def _apply_assignment_if_needed(self, store: KernelStore, index: KernelIndex, schedule: ScheduleReceipt, timestamp: str):
        if not schedule.selected_capability_id:
            return None, None, 0, ()
        record = index.get("executor_capability", schedule.selected_capability_id)
        if not isinstance(record, ExecutorCapability):
            return None, None, 0, ("Selected capability record was missing during dispatch reconciliation.",)
        updated = replace(record, active_assignments=record.active_assignments + 1, updated_at=timestamp)
        store.replace(updated)
        index.record_changed(updated)
        return record.active_assignments, updated.active_assignments, 1, ()


def schedule_dispatch_reconciliation_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-dispatch-reconciliation-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
