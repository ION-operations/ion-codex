
"""M6 schedule stale / retry / reassignment controls."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re

from .branch_rescheduling import KernelBranchRescheduler
from .graph import KernelGraph
from .index import KernelIndex
from .model import (
    BranchRescheduleReceipt,
    ExecutorAvailability,
    ExecutorCapability,
    ScheduleControlReceipt,
    ScheduleReceipt,
)
from .scheduler import KernelScheduler
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleControlError(Exception):
    """Raised when one schedule-control operation cannot be completed."""


@dataclass(frozen=True)
class ScheduleControlPolicySurface:
    policy_id: str
    notes: tuple[str, ...]


class KernelScheduleControlManager:
    def __init__(self) -> None:
        self._scheduler = KernelScheduler()
        self._branch_rescheduler = KernelBranchRescheduler()

    def policy_surface(self) -> ScheduleControlPolicySurface:
        return ScheduleControlPolicySurface(
            policy_id="M6_SCHEDULE_CONTROL_V1",
            notes=(
                "Schedule receipts do not remain valid forever; stale posture must be made explicit.",
                "Retry and reassignment must be distinguished so carrier drift does not hide inside generic refresh.",
                "M6 may record a fresh schedule receipt, but it does not dispatch or execute the work itself.",
            ),
        )

    def maintain_schedule(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        scope_type: str,
        scope_ref: str,
        stale_after_seconds: int = 1800,
        generated_at: str | None = None,
    ) -> ScheduleControlReceipt:
        timestamp = generated_at or _iso_now()
        prior = self._scheduler.latest_schedule_receipt(index, scope_type, scope_ref)
        if prior is None:
            raise KernelScheduleControlError(f"No schedule receipt exists for {scope_type}:{scope_ref}")

        source_branch_reschedule = self._latest_branch_reschedule(index, scope_type, scope_ref)
        schedule_age_seconds = _schedule_age_seconds(prior.created_at, timestamp)
        stale_reasons: list[str] = []
        warnings: list[str] = []

        if schedule_age_seconds is not None and schedule_age_seconds > stale_after_seconds:
            stale_reasons.append("AGE_EXCEEDED")

        if prior.selected_capability_id is not None:
            capability = index.get("executor_capability", prior.selected_capability_id)
            if not isinstance(capability, ExecutorCapability):
                stale_reasons.append("CAPABILITY_MISSING")
            else:
                if capability.availability is not ExecutorAvailability.AVAILABLE:
                    stale_reasons.append(f"CAPABILITY_UNAVAILABLE:{capability.availability.value}")
                if not capability.has_capacity():
                    stale_reasons.append("CAPACITY_EXHAUSTED")

        projection = self._scheduler.build_schedule_projection(
            index,
            graph,
            scope_type=scope_type,
            scope_ref=scope_ref,
            generated_at=timestamp,
        )
        candidate = projection.selected_candidate
        new_schedule = None
        rebinding_fields: tuple[str, ...] = ()
        retry_required = False
        reassignment_required = False
        action = "NO_CHANGE"

        if candidate is None:
            stale_reasons.append("NO_ACTIONABLE_CANDIDATE")
        else:
            if candidate.candidate_id != prior.candidate_id:
                stale_reasons.append("CANDIDATE_DRIFT")
            if candidate.selected_carrier is not prior.selected_carrier:
                stale_reasons.append("CARRIER_DRIFT")
            if candidate.selected_executor_id != prior.selected_executor_id:
                stale_reasons.append("EXECUTOR_DRIFT")
            if candidate.selected_capability_id != prior.selected_capability_id:
                stale_reasons.append("CAPABILITY_DRIFT")
            if candidate.scheduler_state is not prior.scheduler_state:
                stale_reasons.append("STATE_DRIFT")

        if stale_reasons:
            if candidate is None:
                action = "MARK_STALE"
                warnings.append("No replacement schedule candidate was available during maintenance.")
            else:
                new_schedule = self._scheduler.persist_schedule_receipt(
                    store,
                    index,
                    candidate,
                    created_at=timestamp,
                )
                rebinding_fields = _rebinding_fields(prior, new_schedule)
                reassignment_required = bool(rebinding_fields)
                retry_required = not reassignment_required
                action = "REASSIGN_SCHEDULE" if reassignment_required else "RETRY_SCHEDULE"

        receipt = ScheduleControlReceipt(
            receipt_id=schedule_control_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface().policy_id,
            scope_type=scope_type,
            scope_ref=scope_ref,
            prior_schedule_receipt_id=prior.receipt_id,
            source_branch_reschedule_receipt_id=(None if source_branch_reschedule is None else source_branch_reschedule.receipt_id),
            new_schedule_receipt_id=(None if new_schedule is None else new_schedule.receipt_id),
            schedule_age_seconds=schedule_age_seconds,
            stale_detected=bool(stale_reasons),
            stale_reasons=tuple(dict.fromkeys(stale_reasons)),
            control_action=action,
            retry_required=retry_required,
            reassignment_required=reassignment_required,
            prior_candidate_id=prior.candidate_id,
            new_candidate_id=(None if new_schedule is None else new_schedule.candidate_id),
            prior_selected_carrier=prior.selected_carrier,
            new_selected_carrier=(None if new_schedule is None else new_schedule.selected_carrier),
            prior_selected_executor_id=prior.selected_executor_id,
            new_selected_executor_id=(None if new_schedule is None else new_schedule.selected_executor_id),
            prior_selected_capability_id=prior.selected_capability_id,
            new_selected_capability_id=(None if new_schedule is None else new_schedule.selected_capability_id),
            prior_scheduler_state=prior.scheduler_state,
            new_scheduler_state=(None if new_schedule is None else new_schedule.scheduler_state),
            prior_commitment=prior.commitment,
            new_commitment=(None if new_schedule is None else new_schedule.commitment),
            rebinding_fields=rebinding_fields,
            warnings=tuple(dict.fromkeys(tuple(warnings) + prior.warnings + (() if candidate is None else candidate.warnings))),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_receipt(
        self,
        index: KernelIndex,
        scope_type: str | None = None,
        scope_ref: str | None = None,
    ) -> ScheduleControlReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type("schedule_control_receipt") if isinstance(r, ScheduleControlReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_control_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleControlError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleControlReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "prior_schedule_receipt_id": receipt.prior_schedule_receipt_id,
            "source_branch_reschedule_receipt_id": receipt.source_branch_reschedule_receipt_id,
            "new_schedule_receipt_id": receipt.new_schedule_receipt_id,
            "schedule_age_seconds": receipt.schedule_age_seconds,
            "stale_detected": receipt.stale_detected,
            "stale_reasons": list(receipt.stale_reasons),
            "control_action": receipt.control_action,
            "retry_required": receipt.retry_required,
            "reassignment_required": receipt.reassignment_required,
            "prior_candidate_id": receipt.prior_candidate_id,
            "new_candidate_id": receipt.new_candidate_id,
            "prior_selected_carrier": None if receipt.prior_selected_carrier is None else receipt.prior_selected_carrier.value,
            "new_selected_carrier": None if receipt.new_selected_carrier is None else receipt.new_selected_carrier.value,
            "prior_selected_executor_id": receipt.prior_selected_executor_id,
            "new_selected_executor_id": receipt.new_selected_executor_id,
            "prior_selected_capability_id": receipt.prior_selected_capability_id,
            "new_selected_capability_id": receipt.new_selected_capability_id,
            "prior_scheduler_state": None if receipt.prior_scheduler_state is None else receipt.prior_scheduler_state.value,
            "new_scheduler_state": None if receipt.new_scheduler_state is None else receipt.new_scheduler_state.value,
            "prior_commitment": None if receipt.prior_commitment is None else receipt.prior_commitment.value,
            "new_commitment": None if receipt.new_commitment is None else receipt.new_commitment.value,
            "rebinding_fields": list(receipt.rebinding_fields),
            "warnings": list(receipt.warnings),
        }

    def _latest_branch_reschedule(self, index: KernelIndex, scope_type: str, scope_ref: str) -> BranchRescheduleReceipt | None:
        if scope_type.strip().upper() != "WORK_UNIT":
            return None
        receipts = index.branch_reschedule_receipts_for_parent(scope_type.strip().upper(), scope_ref)
        typed = [r for r in receipts if isinstance(r, BranchRescheduleReceipt)]
        if not typed:
            return None
        typed.sort(key=lambda item: (item.created_at, item.receipt_id))
        return typed[-1]


def schedule_control_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-control-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _rebinding_fields(prior: ScheduleReceipt, new: ScheduleReceipt) -> tuple[str, ...]:
    fields: list[str] = []
    if prior.candidate_id != new.candidate_id:
        fields.append("candidate_id")
    if prior.selected_carrier is not new.selected_carrier:
        fields.append("selected_carrier")
    if prior.selected_executor_id != new.selected_executor_id:
        fields.append("selected_executor_id")
    if prior.selected_capability_id != new.selected_capability_id:
        fields.append("selected_capability_id")
    return tuple(fields)


def _schedule_age_seconds(prior_created_at: str, generated_at: str) -> int | None:
    try:
        prior_dt = datetime.fromisoformat(prior_created_at)
        current_dt = datetime.fromisoformat(generated_at)
    except ValueError:
        return None
    return max(0, int((current_dt - prior_dt).total_seconds()))


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
