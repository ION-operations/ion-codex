
"""M9 schedule settlement and future re-entry surfaces."""

from __future__ import annotations

from datetime import datetime
import re

from .graph import KernelGraph
from .index import KernelIndex
from .model import ScheduleCompletionReleaseReceipt, ScheduleSettlementReceipt
from .schedule_completion_release import KernelScheduleCompletionReleaseManager, KernelScheduleCompletionReleaseError
from .schedule_controls import KernelScheduleControlManager
from .schedule_dispatch_reconciliation import KernelScheduleDispatchReconciliationManager
from .scheduler import KernelScheduler
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleSettlementError(Exception):
    """Raised when one schedule settlement / future re-entry operation cannot be completed."""


class KernelScheduleSettlementManager:
    def __init__(self) -> None:
        self._scheduler = KernelScheduler()
        self._controls = KernelScheduleControlManager()
        self._dispatch = KernelScheduleDispatchReconciliationManager()
        self._release = KernelScheduleCompletionReleaseManager()

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M9_SCHEDULE_SETTLEMENT_FUTURE_REENTRY_V1",
            "notes": (
                "M9 settles finished schedule lines into durable history rather than leaving superseded witness floating.",
                "Future re-entry remains bounded to the existing scheduler surface rather than inventing a second planner.",
                "Settlement may record a fresh next schedule receipt when completion lawfully opens a new candidate horizon.",
            ),
        }

    def settle_and_reenter(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        scope_type: str,
        scope_ref: str,
        generated_at: str | None = None,
    ) -> ScheduleSettlementReceipt:
        timestamp = generated_at or _iso_now()
        release_receipt = self._release.latest_receipt(index, scope_type, scope_ref)
        if release_receipt is None:
            raise KernelScheduleSettlementError(f"No schedule completion release receipt exists for {scope_type}:{scope_ref}")

        dispatch_receipt = self._dispatch.latest_receipt(index, scope_type, scope_ref)
        control_receipt = self._controls.latest_receipt(index, scope_type, scope_ref)
        warnings: list[str] = list(release_receipt.warnings)

        retired_schedule_receipt_ids = tuple(r.receipt_id for r in index.schedule_receipts_for_scope(scope_type, scope_ref))
        retired_schedule_control_receipt_ids = tuple(r.receipt_id for r in index.schedule_control_receipts_for_scope(scope_type, scope_ref))
        retired_schedule_dispatch_receipt_ids = tuple(r.receipt_id for r in index.schedule_dispatch_receipts_for_scope(scope_type, scope_ref))
        retired_schedule_completion_release_receipt_ids = tuple(r.receipt_id for r in index.schedule_completion_release_receipts_for_scope(scope_type, scope_ref))

        future_reentry_schedule = None
        future_reentry_reason = None
        action = "SETTLEMENT_DEFERRED"

        if release_receipt.release_action == "RELEASE_DEFERRED":
            warnings.append("Schedule completion release remains deferred; settlement cannot yet close the schedule line.")
        else:
            projection = self._scheduler.build_schedule_projection(
                index,
                graph,
                scope_type=scope_type,
                scope_ref=scope_ref,
                generated_at=timestamp,
            )
            candidate = projection.selected_candidate
            if candidate is not None:
                future_reentry_schedule = self._scheduler.persist_schedule_receipt(
                    store,
                    index,
                    candidate,
                    created_at=timestamp,
                    policy_id=projection.policy.policy_id,
                )
                future_reentry_reason = "NEXT_CANDIDATE_OPENED_AFTER_COMPLETION"
                action = "SETTLED_WITH_FUTURE_REENTRY"
            else:
                action = "SETTLED_NO_FUTURE_REENTRY"

        receipt = ScheduleSettlementReceipt(
            receipt_id=schedule_settlement_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_completion_release_receipt_id=release_receipt.receipt_id,
            source_schedule_dispatch_reconciliation_receipt_id=(None if dispatch_receipt is None else dispatch_receipt.receipt_id),
            source_schedule_control_receipt_id=(None if control_receipt is None else control_receipt.receipt_id),
            work_unit_id=release_receipt.work_unit_id,
            settlement_action=action,
            terminal_commit_delta_id=release_receipt.terminal_commit_delta_id,
            terminal_commit_delta_status=release_receipt.terminal_commit_delta_status,
            retired_schedule_receipt_ids=retired_schedule_receipt_ids,
            retired_schedule_control_receipt_ids=retired_schedule_control_receipt_ids,
            retired_schedule_dispatch_receipt_ids=retired_schedule_dispatch_receipt_ids,
            retired_schedule_completion_release_receipt_ids=retired_schedule_completion_release_receipt_ids,
            future_reentry_schedule_receipt_id=(None if future_reentry_schedule is None else future_reentry_schedule.receipt_id),
            future_reentry_candidate_id=(None if future_reentry_schedule is None else future_reentry_schedule.candidate_id),
            future_reentry_candidate_title=(None if future_reentry_schedule is None else future_reentry_schedule.candidate_title),
            future_reentry_scheduler_state=(None if future_reentry_schedule is None else future_reentry_schedule.scheduler_state),
            future_reentry_commitment=(None if future_reentry_schedule is None else future_reentry_schedule.commitment),
            future_reentry_reason=future_reentry_reason,
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_receipt(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleSettlementReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type("schedule_settlement_receipt") if isinstance(r, ScheduleSettlementReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_settlement_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleSettlementError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleSettlementReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_completion_release_receipt_id": receipt.source_schedule_completion_release_receipt_id,
            "source_schedule_dispatch_reconciliation_receipt_id": receipt.source_schedule_dispatch_reconciliation_receipt_id,
            "source_schedule_control_receipt_id": receipt.source_schedule_control_receipt_id,
            "work_unit_id": receipt.work_unit_id,
            "settlement_action": receipt.settlement_action,
            "terminal_commit_delta_id": receipt.terminal_commit_delta_id,
            "terminal_commit_delta_status": None if receipt.terminal_commit_delta_status is None else receipt.terminal_commit_delta_status.value,
            "retired_schedule_receipt_ids": list(receipt.retired_schedule_receipt_ids),
            "retired_schedule_control_receipt_ids": list(receipt.retired_schedule_control_receipt_ids),
            "retired_schedule_dispatch_receipt_ids": list(receipt.retired_schedule_dispatch_receipt_ids),
            "retired_schedule_completion_release_receipt_ids": list(receipt.retired_schedule_completion_release_receipt_ids),
            "future_reentry_schedule_receipt_id": receipt.future_reentry_schedule_receipt_id,
            "future_reentry_candidate_id": receipt.future_reentry_candidate_id,
            "future_reentry_candidate_title": receipt.future_reentry_candidate_title,
            "future_reentry_scheduler_state": None if receipt.future_reentry_scheduler_state is None else receipt.future_reentry_scheduler_state.value,
            "future_reentry_commitment": None if receipt.future_reentry_commitment is None else receipt.future_reentry_commitment.value,
            "future_reentry_reason": receipt.future_reentry_reason,
            "warnings": list(receipt.warnings),
        }


def schedule_settlement_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-settlement-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
