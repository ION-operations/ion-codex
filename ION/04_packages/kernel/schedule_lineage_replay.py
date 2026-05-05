
"""M11 schedule lineage replay and active-cycle reconstruction surfaces."""

from __future__ import annotations

from datetime import datetime
import re

from .index import KernelIndex
from .model import (
    ScheduleCompletionReleaseReceipt,
    ScheduleDispatchReconciliationReceipt,
    ScheduleLineageArchiveReceipt,
    ScheduleLineageReplayReceipt,
    ScheduleSettlementReceipt,
)
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleLineageReplayError(Exception):
    """Raised when schedule lineage replay cannot be completed."""


class KernelScheduleLineageReplayManager:
    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M11_SCHEDULE_LINEAGE_REPLAY_V1",
            "notes": (
                "M11 replays archived schedule lineage into one explicit active-cycle reconstruction witness.",
                "Replay does not rewrite archived history or mutate schedule state.",
                "The current active cycle is reconstructed from lineage + witnessed schedule/dispatch/completion/settlement chain.",
            ),
        }

    def replay_lineage(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        generated_at: str | None = None,
    ) -> ScheduleLineageReplayReceipt:
        timestamp = generated_at or _iso_now()
        lineage = self.latest_archive(index, scope_type, scope_ref)
        if lineage is None:
            raise KernelScheduleLineageReplayError(f"No schedule lineage archive receipt exists for {scope_type}:{scope_ref}")

        active_schedule = None
        if lineage.active_schedule_receipt_id is not None:
            candidate = index.get('schedule_receipt', lineage.active_schedule_receipt_id)
            if candidate is not None:
                active_schedule = candidate

        dispatch = self._matching_dispatch(index, scope_type, scope_ref, lineage.active_schedule_receipt_id)
        completion = self._matching_completion(index, scope_type, scope_ref, None if dispatch is None else dispatch.receipt_id)
        settlement = self._matching_settlement(index, scope_type, scope_ref, None if completion is None else completion.receipt_id)

        if active_schedule is None:
            stage = 'NO_ACTIVE_CYCLE'
            action = 'REPLAYED_NO_ACTIVE_CYCLE'
            summary = f"Replayed {lineage.settled_line_count} settled schedule line(s); no active cycle remains."
        elif dispatch is None:
            stage = 'ACTIVE_SCHEDULED'
            action = 'RECONSTRUCTED_ACTIVE_CYCLE'
            summary = f"Active cycle reconstructed at scheduled stage for {active_schedule.candidate_title}."
        elif completion is None:
            stage = 'ACTIVE_DISPATCHED'
            action = 'RECONSTRUCTED_ACTIVE_CYCLE'
            summary = f"Active cycle reconstructed at dispatch stage for {active_schedule.candidate_title}."
        elif settlement is None:
            stage = 'ACTIVE_COMPLETED_AWAITING_SETTLEMENT'
            action = 'RECONSTRUCTED_ACTIVE_CYCLE'
            summary = f"Active cycle reconstructed at completion-awaiting-settlement stage for {active_schedule.candidate_title}."
        else:
            stage = 'ACTIVE_CYCLE_ALREADY_SETTLED'
            action = 'REPLAYED_SUPERSEDED_ACTIVE_CYCLE'
            summary = f"Archived active line for {active_schedule.candidate_title} has already been settled."

        warnings: tuple[str, ...] = ()
        receipt = ScheduleLineageReplayReceipt(
            receipt_id=schedule_lineage_replay_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()['policy_id'],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_lineage_archive_receipt_id=lineage.receipt_id,
            source_schedule_receipt_id=(None if active_schedule is None else active_schedule.receipt_id),
            source_schedule_dispatch_reconciliation_receipt_id=(None if dispatch is None else dispatch.receipt_id),
            source_schedule_completion_release_receipt_id=(None if completion is None else completion.receipt_id),
            source_schedule_settlement_receipt_id=(None if settlement is None else settlement.receipt_id),
            active_candidate_id=(None if active_schedule is None else active_schedule.candidate_id),
            active_candidate_title=(None if active_schedule is None else active_schedule.candidate_title),
            active_scheduler_state=(None if active_schedule is None else active_schedule.scheduler_state),
            active_commitment=(None if active_schedule is None else active_schedule.commitment),
            active_cycle_stage=stage,
            replay_action=action,
            replay_summary=summary,
            settled_line_count=lineage.settled_line_count,
            archived_receipt_count=lineage.archived_receipt_count,
            warnings=warnings,
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_archive(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleLineageArchiveReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type('schedule_lineage_archive_receipt') if isinstance(r, ScheduleLineageArchiveReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_lineage_archive_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleLineageReplayError('scope_type and scope_ref must be provided together')
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def latest_receipt(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleLineageReplayReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type('schedule_lineage_replay_receipt') if isinstance(r, ScheduleLineageReplayReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_lineage_replay_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleLineageReplayError('scope_type and scope_ref must be provided together')
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleLineageReplayReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            'receipt_id': receipt.receipt_id,
            'created_at': receipt.created_at,
            'policy_id': receipt.policy_id,
            'scope_type': receipt.scope_type,
            'scope_ref': receipt.scope_ref,
            'source_schedule_lineage_archive_receipt_id': receipt.source_schedule_lineage_archive_receipt_id,
            'source_schedule_receipt_id': receipt.source_schedule_receipt_id,
            'source_schedule_dispatch_reconciliation_receipt_id': receipt.source_schedule_dispatch_reconciliation_receipt_id,
            'source_schedule_completion_release_receipt_id': receipt.source_schedule_completion_release_receipt_id,
            'source_schedule_settlement_receipt_id': receipt.source_schedule_settlement_receipt_id,
            'active_candidate_id': receipt.active_candidate_id,
            'active_candidate_title': receipt.active_candidate_title,
            'active_scheduler_state': None if receipt.active_scheduler_state is None else receipt.active_scheduler_state.value,
            'active_commitment': None if receipt.active_commitment is None else receipt.active_commitment.value,
            'active_cycle_stage': receipt.active_cycle_stage,
            'replay_action': receipt.replay_action,
            'replay_summary': receipt.replay_summary,
            'settled_line_count': receipt.settled_line_count,
            'archived_receipt_count': receipt.archived_receipt_count,
            'warnings': list(receipt.warnings),
        }

    def _matching_dispatch(self, index: KernelIndex, scope_type: str, scope_ref: str, schedule_receipt_id: str | None) -> ScheduleDispatchReconciliationReceipt | None:
        if schedule_receipt_id is None:
            return None
        receipts = [
            r for r in index.schedule_dispatch_receipts_for_scope(scope_type, scope_ref)
            if r.source_schedule_receipt_id == schedule_receipt_id
        ]
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def _matching_completion(self, index: KernelIndex, scope_type: str, scope_ref: str, dispatch_receipt_id: str | None) -> ScheduleCompletionReleaseReceipt | None:
        if dispatch_receipt_id is None:
            return None
        receipts = [
            r for r in index.schedule_completion_release_receipts_for_scope(scope_type, scope_ref)
            if r.source_schedule_dispatch_reconciliation_receipt_id == dispatch_receipt_id
        ]
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def _matching_settlement(self, index: KernelIndex, scope_type: str, scope_ref: str, completion_receipt_id: str | None) -> ScheduleSettlementReceipt | None:
        if completion_receipt_id is None:
            return None
        receipts = [
            r for r in index.schedule_settlement_receipts_for_scope(scope_type, scope_ref)
            if r.source_schedule_completion_release_receipt_id == completion_receipt_id
        ]
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]


def schedule_lineage_replay_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-lineage-replay-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub('-', value.lower()).strip('-') or 'value'


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec='seconds')
