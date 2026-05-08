
"""M8 schedule completion / assignment release reconciliation surfaces."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
import re

from .index import KernelIndex
from .model import (
    CommitDelta,
    ScheduleCompletionReleaseReceipt,
    ScheduleDispatchReconciliationReceipt,
    WorkUnit,
    WorkUnitStatus,
    ExecutorCapability,
)
from .schedule_controls import KernelScheduleControlManager
from .schedule_dispatch_reconciliation import KernelScheduleDispatchReconciliationManager
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleCompletionReleaseError(Exception):
    """Raised when one completion-release reconciliation cannot be completed."""


class KernelScheduleCompletionReleaseManager:
    def __init__(self) -> None:
        self._dispatch_reconciliation = KernelScheduleDispatchReconciliationManager()
        self._controls = KernelScheduleControlManager()

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M8_SCHEDULE_COMPLETION_RELEASE_V1",
            "notes": (
                "M8 closes the assignment lifecycle after execution reaches a terminal work-unit state.",
                "Active assignment release must be explicit and receipted rather than implicit in work-unit status alone.",
                "M8 does not invent new execution state; it reconciles release against existing validation/commit outcomes.",
            ),
        }

    def reconcile_release(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        generated_at: str | None = None,
    ) -> ScheduleCompletionReleaseReceipt:
        timestamp = generated_at or _iso_now()
        dispatch_receipt = self._dispatch_reconciliation.latest_receipt(index, scope_type, scope_ref)
        if dispatch_receipt is None:
            raise KernelScheduleCompletionReleaseError(f"No schedule dispatch reconciliation receipt exists for {scope_type}:{scope_ref}")

        source_control = self._controls.latest_receipt(index, scope_type, scope_ref)
        work_unit = self._resolve_work_unit(index, dispatch_receipt)
        commit_delta = self._latest_commit_delta(index, dispatch_receipt.work_unit_id)
        warnings: list[str] = []
        release_action = "NO_ASSIGNABLE_WORK_UNIT"
        release_reason = None
        retired_dispatch_ids: tuple[str, ...] = ()
        capability_delta = 0
        capability_before = None
        capability_after = None
        status_before = None if work_unit is None else work_unit.status
        status_after = status_before

        if work_unit is None:
            warnings.append("Dispatch reconciliation receipt did not resolve to a work unit.")
        elif work_unit.status in (WorkUnitStatus.COMMITTED, WorkUnitStatus.FAILED, WorkUnitStatus.BLOCKED):
            capability_before, capability_after, capability_delta, cap_warn = self._release_assignment_if_needed(
                store,
                index,
                dispatch_receipt,
                timestamp,
            )
            warnings.extend(cap_warn)
            status_after = work_unit.status
            release_reason = work_unit.status.value
            if capability_delta < 0:
                if work_unit.status is WorkUnitStatus.COMMITTED:
                    release_action = "RELEASED_ON_COMPLETION"
                elif work_unit.status is WorkUnitStatus.FAILED:
                    release_action = "RELEASED_ON_FAILURE"
                else:
                    release_action = "RELEASED_ON_BLOCK"
            else:
                release_action = "NO_ACTIVE_ASSIGNMENT_TO_RELEASE"
            retired_dispatch_ids = tuple(r.receipt_id for r in index.schedule_dispatch_receipts_for_scope(scope_type, scope_ref))
        else:
            release_action = "RELEASE_DEFERRED"
            warnings.append(f"Work unit status {work_unit.status.value} is not terminal for assignment release.")

        receipt = ScheduleCompletionReleaseReceipt(
            receipt_id=schedule_completion_release_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_dispatch_reconciliation_receipt_id=dispatch_receipt.receipt_id,
            source_schedule_control_receipt_id=(None if source_control is None else source_control.receipt_id),
            work_unit_id=(None if work_unit is None else work_unit.work_unit_id),
            terminal_commit_delta_id=(None if commit_delta is None else commit_delta.delta_id),
            terminal_commit_delta_status=(None if commit_delta is None else commit_delta.status),
            release_action=release_action,
            work_unit_status_before=status_before,
            work_unit_status_after=status_after,
            selected_capability_id=dispatch_receipt.selected_capability_id,
            capability_release_delta=capability_delta,
            capability_assignments_before=capability_before,
            capability_assignments_after=capability_after,
            retired_schedule_dispatch_receipt_ids=retired_dispatch_ids,
            release_reason=release_reason,
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_receipt(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleCompletionReleaseReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type("schedule_completion_release_receipt") if isinstance(r, ScheduleCompletionReleaseReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_completion_release_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleCompletionReleaseError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleCompletionReleaseReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_dispatch_reconciliation_receipt_id": receipt.source_schedule_dispatch_reconciliation_receipt_id,
            "source_schedule_control_receipt_id": receipt.source_schedule_control_receipt_id,
            "work_unit_id": receipt.work_unit_id,
            "terminal_commit_delta_id": receipt.terminal_commit_delta_id,
            "terminal_commit_delta_status": (None if receipt.terminal_commit_delta_status is None else receipt.terminal_commit_delta_status.value),
            "release_action": receipt.release_action,
            "work_unit_status_before": (None if receipt.work_unit_status_before is None else receipt.work_unit_status_before.value),
            "work_unit_status_after": (None if receipt.work_unit_status_after is None else receipt.work_unit_status_after.value),
            "selected_capability_id": receipt.selected_capability_id,
            "capability_release_delta": receipt.capability_release_delta,
            "capability_assignments_before": receipt.capability_assignments_before,
            "capability_assignments_after": receipt.capability_assignments_after,
            "retired_schedule_dispatch_receipt_ids": list(receipt.retired_schedule_dispatch_receipt_ids),
            "release_reason": receipt.release_reason,
            "warnings": list(receipt.warnings),
        }

    def _resolve_work_unit(self, index: KernelIndex, dispatch_receipt: ScheduleDispatchReconciliationReceipt) -> WorkUnit | None:
        if dispatch_receipt.work_unit_id is None:
            return None
        record = index.get("work_unit", dispatch_receipt.work_unit_id)
        return record if isinstance(record, WorkUnit) else None

    def _latest_commit_delta(self, index: KernelIndex, work_unit_id: str | None) -> CommitDelta | None:
        if not work_unit_id:
            return None
        deltas = [r for r in index.records_for_work_unit(work_unit_id) if isinstance(r, CommitDelta)]
        if not deltas:
            return None
        deltas.sort(key=lambda item: (item.created_at, item.delta_id))
        return deltas[-1]

    def _release_assignment_if_needed(self, store: KernelStore, index: KernelIndex, dispatch_receipt: ScheduleDispatchReconciliationReceipt, timestamp: str):
        if not dispatch_receipt.selected_capability_id or dispatch_receipt.capability_assignment_delta <= 0:
            return None, None, 0, ()
        record = index.get("executor_capability", dispatch_receipt.selected_capability_id)
        if not isinstance(record, ExecutorCapability):
            return None, None, 0, ("Selected capability record was missing during completion release.",)
        if record.active_assignments <= 0:
            return record.active_assignments, record.active_assignments, 0, ("Capability already had zero active assignments during release.",)
        updated = replace(record, active_assignments=record.active_assignments - 1, updated_at=timestamp)
        store.replace(updated)
        index.record_changed(updated)
        return record.active_assignments, updated.active_assignments, -1, ()


def schedule_completion_release_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-completion-release-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
