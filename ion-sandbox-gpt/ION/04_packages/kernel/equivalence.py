"""L3 manual/automation equivalence proof surfaces for the active ION kernel stack.

This module proves a bounded symmetry claim: the same packet-ready horizon candidate
can yield both an automation-targeted packet and a manual-fallback packet, and both
can carry the same lawful step under the same continuity witness discipline.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import re

from .horizon_state import KernelHorizonStateManager
from .index import KernelIndex
from .model import ManualAutomationEquivalenceReceipt
from .store import KernelStore
from .takeover import KernelTakeoverManager


class KernelManualAutomationEquivalenceError(Exception):
    """Raised when one bounded manual/automation equivalence rehearsal fails."""


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelManualAutomationEquivalenceManager:
    """Rehearse and persist bounded manual/automation equivalence proof."""

    def __init__(self) -> None:
        self._horizon_manager = KernelHorizonStateManager()
        self._takeover_manager = KernelTakeoverManager()

    def rehearse_horizon_equivalence(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        workspace_root: str | Path,
        automation_packet_type: str = "cursor_handoff",
        automation_output_path: str | Path | None = None,
        manual_output_path: str | Path | None = None,
        created_at: str | None = None,
        automation_sender: str = "HORIZON",
        automation_receiver: str = "Automation carrier",
        automation_target_surface: str = "Supervised runtime / automation carrier",
        manual_operator: str = "OPERATOR",
        manual_automation_surface: str = "supervised runtime",
        manual_reason: str = "manual/automation equivalence rehearsal",
    ) -> ManualAutomationEquivalenceReceipt:
        if automation_packet_type not in {"handoff", "cursor_handoff"}:
            raise KernelManualAutomationEquivalenceError(
                "automation_packet_type must be 'handoff' or 'cursor_handoff'."
            )

        workspace = Path(workspace_root).resolve()
        automation_created_at, manual_created_at, receipt_created_at = _timestamp_triplet(created_at)
        automation_relative_path, manual_relative_path = _output_paths(
            scope_type,
            scope_ref,
            automation_packet_type,
            automation_output_path,
            manual_output_path,
        )

        automation_result = self._horizon_manager.enact_packet_for_scope(
            index,
            scope_type,
            scope_ref,
            store=store,
            packet_type=automation_packet_type,
            workspace_root=workspace,
            output_path=automation_relative_path,
            created_at=automation_created_at,
            sender=automation_sender,
            receiver=automation_receiver,
            target_surface=automation_target_surface,
        )
        manual_result = self._horizon_manager.enact_packet_for_scope(
            index,
            scope_type,
            scope_ref,
            store=store,
            packet_type="manual_automation_fallback",
            workspace_root=workspace,
            output_path=manual_relative_path,
            created_at=manual_created_at,
            receiver=manual_operator,
            automation_surface=manual_automation_surface,
            reason=manual_reason,
        )

        if not automation_result.valid:
            raise KernelManualAutomationEquivalenceError(
                f"Automation enactment did not produce a valid packet: {automation_result.status}"
            )
        if not manual_result.valid:
            raise KernelManualAutomationEquivalenceError(
                f"Manual fallback enactment did not produce a valid packet: {manual_result.status}"
            )
        if automation_result.packet_path is None or manual_result.packet_path is None:
            raise KernelManualAutomationEquivalenceError("Equivalence rehearsal requires written packet artifacts.")

        automation_takeover = self._takeover_manager.record_packet_takeover(
            store,
            index,
            automation_result.packet_path,
            expected_type=automation_packet_type,
            workspace_root=workspace,
            created_at=automation_created_at,
        )
        manual_takeover = self._takeover_manager.record_packet_takeover(
            store,
            index,
            manual_result.packet_path,
            expected_type="manual_automation_fallback",
            workspace_root=workspace,
            created_at=manual_created_at,
        )

        mismatches = _equivalence_mismatches(
            automation_result=automation_result,
            manual_result=manual_result,
            automation_takeover=automation_takeover,
            manual_takeover=manual_takeover,
        )
        if mismatches:
            raise KernelManualAutomationEquivalenceError(
                "Manual/automation equivalence failed: " + "; ".join(mismatches)
            )

        candidate_item_id = automation_result.candidate_item_id
        candidate_title = automation_result.candidate_title
        if candidate_item_id is None or candidate_title is None:
            raise KernelManualAutomationEquivalenceError("Equivalence rehearsal requires one enacted horizon candidate.")

        receipt = ManualAutomationEquivalenceReceipt(
            receipt_id=manual_automation_equivalence_receipt_id(
                automation_result.scope_type,
                automation_result.scope_ref,
                automation_packet_type,
                candidate_item_id,
                receipt_created_at,
            ),
            created_at=receipt_created_at,
            scope_type=automation_result.scope_type,
            scope_ref=automation_result.scope_ref,
            source_horizon_ids=automation_result.source_horizon_ids,
            source_layer=automation_result.source_layer,
            candidate_item_id=candidate_item_id,
            candidate_title=candidate_title,
            automation_packet_type=automation_packet_type,
            automation_packet_path=automation_result.packet_path,
            automation_packet_relative_path=automation_result.packet_relative_path,
            automation_horizon_receipt_id=automation_result.receipt_id,
            automation_takeover_receipt_id=automation_takeover.receipt_id,
            manual_packet_path=manual_result.packet_path,
            manual_packet_relative_path=manual_result.packet_relative_path,
            manual_horizon_receipt_id=manual_result.receipt_id,
            manual_takeover_receipt_id=manual_takeover.receipt_id,
            shared_objective=automation_takeover.objective,
            shared_scope_binding=f"{automation_takeover.scope_type}:{automation_takeover.scope_ref}",
            shared_required_reads=automation_takeover.required_reads,
            compared_fields=(
                "candidate_item_id",
                "source_horizon_ids",
                "objective",
                "scope_binding",
                "required_reads",
                "canonical_packet_validation",
                "takeover_assessment",
            ),
            equivalent=True,
            warnings=tuple(
                dict.fromkeys(
                    list(automation_result.warnings)
                    + list(manual_result.warnings)
                    + list(automation_takeover.warnings)
                    + list(manual_takeover.warnings)
                )
            ),
        )
        if index.exists("manual_automation_equivalence_receipt", receipt.receipt_id):
            store.replace(receipt)
            index.record_changed(receipt)
        else:
            store.create(receipt)
            index.record_added(receipt)
        return receipt

    def latest_equivalence_receipt(
        self,
        index: KernelIndex,
        scope_type: str | None = None,
        scope_ref: str | None = None,
    ) -> ManualAutomationEquivalenceReceipt | None:
        normalized_scope = _normalize_scope_filter(scope_type, scope_ref)
        if normalized_scope is None:
            receipts = [
                record
                for record in index.records_by_type("manual_automation_equivalence_receipt")
                if isinstance(record, ManualAutomationEquivalenceReceipt)
            ]
        else:
            receipts = index.manual_automation_equivalence_receipts_for_scope(
                normalized_scope[0],
                normalized_scope[1],
            )
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_equivalence_receipt_projection(
        self,
        receipt: ManualAutomationEquivalenceReceipt | None,
    ) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_horizon_ids": list(receipt.source_horizon_ids),
            "source_layer": (None if receipt.source_layer is None else receipt.source_layer.value),
            "candidate_item_id": receipt.candidate_item_id,
            "candidate_title": receipt.candidate_title,
            "automation_packet_type": receipt.automation_packet_type,
            "automation_packet_path": receipt.automation_packet_path,
            "automation_packet_relative_path": receipt.automation_packet_relative_path,
            "automation_horizon_receipt_id": receipt.automation_horizon_receipt_id,
            "automation_takeover_receipt_id": receipt.automation_takeover_receipt_id,
            "manual_packet_type": receipt.manual_packet_type,
            "manual_packet_path": receipt.manual_packet_path,
            "manual_packet_relative_path": receipt.manual_packet_relative_path,
            "manual_horizon_receipt_id": receipt.manual_horizon_receipt_id,
            "manual_takeover_receipt_id": receipt.manual_takeover_receipt_id,
            "shared_objective": receipt.shared_objective,
            "shared_scope_binding": receipt.shared_scope_binding,
            "shared_required_reads": list(receipt.shared_required_reads),
            "compared_fields": list(receipt.compared_fields),
            "equivalent": receipt.equivalent,
            "warnings": list(receipt.warnings),
        }


def manual_automation_equivalence_receipt_id(
    scope_type: str,
    scope_ref: str,
    automation_packet_type: str,
    candidate_item_id: str,
    created_at: str,
) -> str:
    clean_scope_type = _SAFE_ID_RE.sub("-", scope_type.lower()).strip("-") or "scope"
    clean_scope_ref = _SAFE_ID_RE.sub("-", scope_ref.lower()).strip("-") or "state"
    clean_packet_type = _SAFE_ID_RE.sub("-", automation_packet_type.lower()).strip("-") or "automation"
    clean_candidate = _SAFE_ID_RE.sub("-", candidate_item_id.lower()).strip("-") or "candidate"
    clean_created_at = _SAFE_ID_RE.sub("-", created_at.lower()).strip("-") or "timestamp"
    return f"manual-automation-equivalence-{clean_scope_type}-{clean_scope_ref}-{clean_packet_type}-{clean_candidate}-{clean_created_at}"


def _equivalence_mismatches(
    *,
    automation_result,
    manual_result,
    automation_takeover,
    manual_takeover,
) -> list[str]:
    mismatches: list[str] = []
    if automation_result.candidate_item_id != manual_result.candidate_item_id:
        mismatches.append("candidate item diverged between automation and manual packets")
    if automation_result.source_horizon_ids != manual_result.source_horizon_ids:
        mismatches.append("source horizon ids diverged between automation and manual packets")
    if automation_takeover.objective != manual_takeover.objective:
        mismatches.append("takeover objective diverged between automation and manual packets")
    if (
        automation_takeover.scope_type != manual_takeover.scope_type
        or automation_takeover.scope_ref != manual_takeover.scope_ref
    ):
        mismatches.append("takeover scope binding diverged between automation and manual packets")
    if automation_takeover.required_reads != manual_takeover.required_reads:
        mismatches.append("required reads diverged between automation and manual packets")
    return mismatches


def _output_paths(
    scope_type: str,
    scope_ref: str,
    automation_packet_type: str,
    automation_output_path: str | Path | None,
    manual_output_path: str | Path | None,
) -> tuple[str, str]:
    slug = _slugify(f"{scope_type}_{scope_ref}")
    automation_default = (
        f"ION/05_context/history/manual_automation_equivalence/{slug}_automation_{automation_packet_type}.md"
    )
    manual_default = (
        f"ION/05_context/history/manual_automation_equivalence/{slug}_manual_fallback.md"
    )
    return (
        str(automation_output_path or automation_default),
        str(manual_output_path or manual_default),
    )


def _normalize_scope_filter(
    scope_type: str | None,
    scope_ref: str | None,
) -> tuple[str, str] | None:
    if scope_type is None and scope_ref is None:
        return None
    if not scope_type or not scope_ref:
        raise KernelManualAutomationEquivalenceError("scope_type and scope_ref must be provided together.")
    return scope_type.strip().upper(), scope_ref.strip()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "equivalence"


def _timestamp_triplet(created_at: str | None) -> tuple[str, str, str]:
    base = _parse_or_now(created_at)
    return (
        base.isoformat(timespec="seconds"),
        (base + timedelta(seconds=1)).isoformat(timespec="seconds"),
        (base + timedelta(seconds=2)).isoformat(timespec="seconds"),
    )


def _parse_or_now(created_at: str | None) -> datetime:
    if created_at is None:
        return datetime.now().astimezone().replace(microsecond=0)
    return datetime.fromisoformat(created_at)
