"""M10 schedule lineage and supersession archival surfaces."""

from __future__ import annotations

from datetime import datetime
import re

from .index import KernelIndex
from .model import ScheduleLineageArchiveReceipt, ScheduleSettlementReceipt
from .scheduler import KernelScheduler
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleLineageArchiveError(Exception):
    """Raised when schedule lineage archival cannot be completed."""


class KernelScheduleLineageArchiveManager:
    def __init__(self) -> None:
        self._scheduler = KernelScheduler()

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M10_SCHEDULE_LINEAGE_ARCHIVAL_V1",
            "notes": (
                "M10 compacts settled schedule-cycle history into one explicit lineage/archive witness.",
                "Archival never deletes authoritative receipts; it only records which receipts are now superseded historical surface.",
                "The current active line, when one exists, is retrieved from lawful future re-entry rather than inferred through hidden state.",
            ),
        }

    def archive_lineage(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        generated_at: str | None = None,
    ) -> ScheduleLineageArchiveReceipt:
        timestamp = generated_at or _iso_now()
        settlement = self.latest_settlement(index, scope_type, scope_ref)
        if settlement is None:
            raise KernelScheduleLineageArchiveError(f"No schedule settlement receipt exists for {scope_type}:{scope_ref}")

        settlements = sorted(
            index.schedule_settlement_receipts_for_scope(scope_type, scope_ref),
            key=lambda item: (item.created_at, item.receipt_id),
        )

        archived_schedule_receipt_ids = _stable_unique(
            receipt_id
            for item in settlements
            for receipt_id in item.retired_schedule_receipt_ids
        )
        archived_schedule_control_receipt_ids = _stable_unique(
            receipt_id
            for item in settlements
            for receipt_id in item.retired_schedule_control_receipt_ids
        )
        archived_schedule_dispatch_receipt_ids = _stable_unique(
            receipt_id
            for item in settlements
            for receipt_id in item.retired_schedule_dispatch_receipt_ids
        )
        archived_schedule_completion_release_receipt_ids = _stable_unique(
            receipt_id
            for item in settlements
            for receipt_id in item.retired_schedule_completion_release_receipt_ids
        )
        archived_schedule_settlement_receipt_ids = tuple(item.receipt_id for item in settlements)

        active_schedule = None
        if settlement.future_reentry_schedule_receipt_id is not None:
            candidate = index.get("schedule_receipt", settlement.future_reentry_schedule_receipt_id)
            if candidate is not None:
                active_schedule = candidate

        lineage_action = "ARCHIVED_WITH_ACTIVE_LINE" if active_schedule is not None else "ARCHIVED_NO_ACTIVE_LINE"
        if active_schedule is not None:
            lineage_summary = (
                f"Archived {len(archived_schedule_settlement_receipt_ids)} settled schedule line(s); "
                f"active line is {active_schedule.candidate_title}."
            )
        else:
            lineage_summary = f"Archived {len(archived_schedule_settlement_receipt_ids)} settled schedule line(s); no active line remains."

        archived_receipt_count = (
            len(archived_schedule_receipt_ids)
            + len(archived_schedule_control_receipt_ids)
            + len(archived_schedule_dispatch_receipt_ids)
            + len(archived_schedule_completion_release_receipt_ids)
            + len(archived_schedule_settlement_receipt_ids)
        )

        warnings = tuple(dict.fromkeys(settlement.warnings))
        receipt = ScheduleLineageArchiveReceipt(
            receipt_id=schedule_lineage_archive_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_settlement_receipt_id=settlement.receipt_id,
            active_schedule_receipt_id=(None if active_schedule is None else active_schedule.receipt_id),
            active_candidate_id=(None if active_schedule is None else active_schedule.candidate_id),
            active_candidate_title=(None if active_schedule is None else active_schedule.candidate_title),
            active_scheduler_state=(None if active_schedule is None else active_schedule.scheduler_state),
            active_commitment=(None if active_schedule is None else active_schedule.commitment),
            lineage_action=lineage_action,
            lineage_summary=lineage_summary,
            archived_schedule_receipt_ids=archived_schedule_receipt_ids,
            archived_schedule_control_receipt_ids=archived_schedule_control_receipt_ids,
            archived_schedule_dispatch_receipt_ids=archived_schedule_dispatch_receipt_ids,
            archived_schedule_completion_release_receipt_ids=archived_schedule_completion_release_receipt_ids,
            archived_schedule_settlement_receipt_ids=archived_schedule_settlement_receipt_ids,
            settled_line_count=len(archived_schedule_settlement_receipt_ids),
            archived_receipt_count=archived_receipt_count,
            warnings=warnings,
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_settlement(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleSettlementReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type("schedule_settlement_receipt") if isinstance(r, ScheduleSettlementReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_settlement_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleLineageArchiveError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def latest_receipt(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleLineageArchiveReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type("schedule_lineage_archive_receipt") if isinstance(r, ScheduleLineageArchiveReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_lineage_archive_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleLineageArchiveError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleLineageArchiveReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_settlement_receipt_id": receipt.source_schedule_settlement_receipt_id,
            "active_schedule_receipt_id": receipt.active_schedule_receipt_id,
            "active_candidate_id": receipt.active_candidate_id,
            "active_candidate_title": receipt.active_candidate_title,
            "active_scheduler_state": None if receipt.active_scheduler_state is None else receipt.active_scheduler_state.value,
            "active_commitment": None if receipt.active_commitment is None else receipt.active_commitment.value,
            "lineage_action": receipt.lineage_action,
            "lineage_summary": receipt.lineage_summary,
            "archived_schedule_receipt_ids": list(receipt.archived_schedule_receipt_ids),
            "archived_schedule_control_receipt_ids": list(receipt.archived_schedule_control_receipt_ids),
            "archived_schedule_dispatch_receipt_ids": list(receipt.archived_schedule_dispatch_receipt_ids),
            "archived_schedule_completion_release_receipt_ids": list(receipt.archived_schedule_completion_release_receipt_ids),
            "archived_schedule_settlement_receipt_ids": list(receipt.archived_schedule_settlement_receipt_ids),
            "settled_line_count": receipt.settled_line_count,
            "archived_receipt_count": receipt.archived_receipt_count,
            "warnings": list(receipt.warnings),
        }


def schedule_lineage_archive_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-lineage-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _stable_unique(values) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            ordered.append(value)
    return tuple(ordered)


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
