"""M5 branch-aware rescheduling / carrier rebinding surfaces.

This module keeps M5 subordinate to the existing scheduler. It does not invent a
second arbitration system. Instead it:

- requires explicit M4 synchronization witness,
- re-evaluates the parent-scope schedule after synchronization,
- persists one new schedule receipt when a candidate exists,
- and records whether carrier / executor / capability rebinding occurred.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re

from .branch_horizon_sync import KernelBranchHorizonSynchronizer
from .graph import KernelGraph
from .index import KernelIndex
from .model import (
    BranchHorizonSyncReceipt,
    BranchRescheduleReceipt,
    CarrierBindingSource,
    ScheduleCarrier,
    ScheduleCommitment,
    ScheduleReceipt,
    ScheduleState,
)
from .scheduler import KernelScheduler
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelBranchReschedulingError(Exception):
    """Raised when one M5 branch-aware rescheduling operation cannot be completed."""


@dataclass(frozen=True)
class BranchReschedulingPolicySurface:
    policy_id: str
    notes: tuple[str, ...]


class KernelBranchRescheduler:
    def __init__(self) -> None:
        self._scheduler = KernelScheduler()
        self._branch_sync = KernelBranchHorizonSynchronizer()

    def policy_surface(self) -> BranchReschedulingPolicySurface:
        return BranchReschedulingPolicySurface(
            policy_id="M5_BRANCH_RESCHEDULING_V1",
            notes=(
                "M5 must remain subordinate to the canonical scheduler rather than inventing a branch-only arbiter.",
                "Rescheduling after branch synchronization must preserve explicit witness for any carrier or executor rebinding.",
                "Hidden executor switching is disallowed; rebinding must be persisted as an explicit receipt.",
            ),
        )

    def reschedule_after_sync(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        parent_work_unit_id: str,
        *,
        generated_at: str | None = None,
    ) -> BranchRescheduleReceipt:
        timestamp = generated_at or _iso_now()
        sync_receipt = self._branch_sync.latest_receipt(index, "WORK_UNIT", parent_work_unit_id)
        if sync_receipt is None:
            raise KernelBranchReschedulingError(
                f"No branch-horizon synchronization receipt exists for parent {parent_work_unit_id}"
            )

        prior_schedule = self._resolve_prior_schedule(index, sync_receipt)
        projection = self._scheduler.build_schedule_projection(
            index,
            graph,
            scope_type=sync_receipt.parent_scope_type,
            scope_ref=sync_receipt.parent_scope_ref,
            generated_at=timestamp,
        )
        candidate = projection.selected_candidate
        new_schedule = None
        warnings: list[str] = []
        if candidate is None:
            warnings.append("No actionable schedule candidate exists after branch synchronization.")
        else:
            new_schedule = self._scheduler.persist_schedule_receipt(
                store,
                index,
                candidate,
                created_at=timestamp,
            )

        rebinding_fields = _rebinding_fields(prior_schedule, new_schedule)
        receipt = BranchRescheduleReceipt(
            receipt_id=branch_reschedule_receipt_id("WORK_UNIT", parent_work_unit_id, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface().policy_id,
            parent_scope_type="WORK_UNIT",
            parent_scope_ref=parent_work_unit_id,
            source_branch_horizon_sync_receipt_id=sync_receipt.receipt_id,
            prior_schedule_receipt_id=(None if prior_schedule is None else prior_schedule.receipt_id),
            new_schedule_receipt_id=(None if new_schedule is None else new_schedule.receipt_id),
            prior_candidate_id=(None if prior_schedule is None else prior_schedule.candidate_id),
            new_candidate_id=(None if new_schedule is None else new_schedule.candidate_id),
            prior_selected_carrier=(None if prior_schedule is None else prior_schedule.selected_carrier),
            new_selected_carrier=(None if new_schedule is None else new_schedule.selected_carrier),
            prior_selected_executor_id=(None if prior_schedule is None else prior_schedule.selected_executor_id),
            new_selected_executor_id=(None if new_schedule is None else new_schedule.selected_executor_id),
            prior_selected_capability_id=(None if prior_schedule is None else prior_schedule.selected_capability_id),
            new_selected_capability_id=(None if new_schedule is None else new_schedule.selected_capability_id),
            prior_scheduler_state=(None if prior_schedule is None else prior_schedule.scheduler_state),
            new_scheduler_state=(None if new_schedule is None else new_schedule.scheduler_state),
            prior_commitment=(None if prior_schedule is None else prior_schedule.commitment),
            new_commitment=(None if new_schedule is None else new_schedule.commitment),
            rebinding_required=bool(rebinding_fields),
            rebinding_fields=rebinding_fields,
            reschedule_reason=_reschedule_reason(prior_schedule, new_schedule, rebinding_fields),
            warnings=tuple(dict.fromkeys(tuple(warnings) + tuple(candidate.warnings if candidate is not None else ()))),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_receipt(
        self,
        index: KernelIndex,
        parent_scope_type: str | None = None,
        parent_scope_ref: str | None = None,
    ) -> BranchRescheduleReceipt | None:
        if parent_scope_type is None and parent_scope_ref is None:
            receipts = [
                record
                for record in index.records_by_type("branch_reschedule_receipt")
                if isinstance(record, BranchRescheduleReceipt)
            ]
        elif parent_scope_type is not None and parent_scope_ref is not None:
            receipts = index.branch_reschedule_receipts_for_parent(parent_scope_type, parent_scope_ref)
        else:
            raise KernelBranchReschedulingError(
                "parent_scope_type and parent_scope_ref must be provided together"
            )
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: BranchRescheduleReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "parent_scope_type": receipt.parent_scope_type,
            "parent_scope_ref": receipt.parent_scope_ref,
            "source_branch_horizon_sync_receipt_id": receipt.source_branch_horizon_sync_receipt_id,
            "prior_schedule_receipt_id": receipt.prior_schedule_receipt_id,
            "new_schedule_receipt_id": receipt.new_schedule_receipt_id,
            "prior_candidate_id": receipt.prior_candidate_id,
            "new_candidate_id": receipt.new_candidate_id,
            "prior_selected_carrier": (None if receipt.prior_selected_carrier is None else receipt.prior_selected_carrier.value),
            "new_selected_carrier": (None if receipt.new_selected_carrier is None else receipt.new_selected_carrier.value),
            "prior_selected_executor_id": receipt.prior_selected_executor_id,
            "new_selected_executor_id": receipt.new_selected_executor_id,
            "prior_selected_capability_id": receipt.prior_selected_capability_id,
            "new_selected_capability_id": receipt.new_selected_capability_id,
            "prior_scheduler_state": (None if receipt.prior_scheduler_state is None else receipt.prior_scheduler_state.value),
            "new_scheduler_state": (None if receipt.new_scheduler_state is None else receipt.new_scheduler_state.value),
            "prior_commitment": (None if receipt.prior_commitment is None else receipt.prior_commitment.value),
            "new_commitment": (None if receipt.new_commitment is None else receipt.new_commitment.value),
            "rebinding_required": receipt.rebinding_required,
            "rebinding_fields": list(receipt.rebinding_fields),
            "reschedule_reason": receipt.reschedule_reason,
            "warnings": list(receipt.warnings),
        }

    def _resolve_prior_schedule(
        self,
        index: KernelIndex,
        sync_receipt: BranchHorizonSyncReceipt,
    ) -> ScheduleReceipt | None:
        if sync_receipt.synchronized_schedule_receipt_id:
            record = index.get("schedule_receipt", sync_receipt.synchronized_schedule_receipt_id)
            if isinstance(record, ScheduleReceipt):
                return record
        receipts = index.schedule_receipts_for_scope(sync_receipt.parent_scope_type, sync_receipt.parent_scope_ref)
        typed = [record for record in receipts if isinstance(record, ScheduleReceipt)]
        if not typed:
            return None
        typed.sort(key=lambda item: (item.created_at, item.receipt_id))
        return typed[-1]


def branch_reschedule_receipt_id(parent_scope_type: str, parent_scope_ref: str, created_at: str) -> str:
    return f"reschedule-{_slug(parent_scope_type)}-{_slug(parent_scope_ref)}-{_slug(created_at)}"


def _rebinding_fields(prior: ScheduleReceipt | None, new: ScheduleReceipt | None) -> tuple[str, ...]:
    if prior is None or new is None:
        return ()
    fields: list[str] = []
    if prior.selected_carrier is not new.selected_carrier:
        fields.append("selected_carrier")
    if prior.selected_executor_id != new.selected_executor_id:
        fields.append("selected_executor_id")
    if prior.selected_capability_id != new.selected_capability_id:
        fields.append("selected_capability_id")
    return tuple(fields)


def _reschedule_reason(
    prior: ScheduleReceipt | None,
    new: ScheduleReceipt | None,
    rebinding_fields: tuple[str, ...],
) -> str:
    if new is None:
        return "NO_ACTIONABLE_CANDIDATE"
    if prior is None:
        return "INITIAL_SCHEDULE_AFTER_SYNC"
    if rebinding_fields:
        return "REBOUND_AFTER_SYNC"
    if prior.candidate_id != new.candidate_id or prior.scheduler_state is not new.scheduler_state or prior.commitment is not new.commitment:
        return "RESCHEDULED_AFTER_SYNC"
    return "NO_REBINDING_REQUIRED"


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
