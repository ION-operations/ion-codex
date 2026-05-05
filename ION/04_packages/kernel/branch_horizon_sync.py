
"""M4 branch-aware horizon / schedule synchronization surfaces.

This module returns bounded branch posture back into the parent-scope future field:
- inspect active branch claims, branch-control posture, and the latest settlement receipt,
- write one authoritative parent-scope horizon posture,
- project that posture through the existing scheduler surface,
- and persist an explicit synchronization receipt without creating a shadow planner.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re

from .branch_controls import KernelBranchControlManager
from .graph import KernelGraph
from .horizon_state import KernelHorizonStateManager
from .index import KernelIndex
from .model import (
    BranchClaimReceipt,
    BranchClaimStatus,
    BranchHorizonSyncReceipt,
    BranchSettlementOutcome,
    HorizonLayer,
    HorizonWorkItem,
    ScheduleReceipt,
    WorkUnit,
)
from .scheduler import KernelScheduler
from .settlement import KernelBranchSettlementManager
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelBranchHorizonSyncError(Exception):
    """Raised when branch posture cannot be synchronized back into future state."""


@dataclass(frozen=True)
class BranchHorizonSyncPolicySurface:
    policy_id: str
    notes: tuple[str, ...]


@dataclass(frozen=True)
class BranchHorizonSyncProjection:
    receipt_id: str
    generated_at: str
    policy: BranchHorizonSyncPolicySurface
    parent_scope_type: str
    parent_scope_ref: str
    synchronized_horizon_id: str
    synchronized_horizon_layer: HorizonLayer
    source_branch_control_receipt_id: str | None
    source_branch_settlement_receipt_id: str | None
    source_branch_claim_receipt_ids: tuple[str, ...]
    active_branch_work_unit_ids: tuple[str, ...]
    accepted_delta_ids: tuple[str, ...]
    deferred_branch_work_unit_ids: tuple[str, ...]
    review_reasons: tuple[str, ...]
    next_action: str | None
    synchronization_reason: str | None
    selected_schedule_candidate_id: str | None
    selected_schedule_state: str | None
    selected_schedule_commitment: str | None
    synchronized_schedule_receipt_id: str | None = None
    warnings: tuple[str, ...] = ()


class KernelBranchHorizonSynchronizer:
    def __init__(self) -> None:
        self._controls = KernelBranchControlManager()
        self._settlement = KernelBranchSettlementManager()
        self._horizon = KernelHorizonStateManager()
        self._scheduler = KernelScheduler()

    def policy_surface(self) -> BranchHorizonSyncPolicySurface:
        return BranchHorizonSyncPolicySurface(
            policy_id="M4_BRANCH_HORIZON_SYNC_V1",
            notes=(
                "Branch fan-out, fan-in, and control must return into parent-scope future state explicitly.",
                "Synchronization writes one authoritative parent-scope horizon layer rather than spawning a second planner.",
                "The existing scheduler surface remains the only lawful scheduling projection surface.",
            ),
        )

    def synchronize_parent_scope(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        parent_work_unit_id: str,
        *,
        generated_at: str | None = None,
        max_branches: int | None = None,
    ) -> BranchHorizonSyncReceipt:
        timestamp = generated_at or _iso_now()
        parent = _resolve_parent(index, parent_work_unit_id)
        source_claim_ids = tuple(
            sorted(
                receipt.receipt_id
                for receipt in index.branch_claim_receipts_for_parent("WORK_UNIT", parent_work_unit_id)
                if receipt.claim_status is BranchClaimStatus.ACTIVE
            )
        )
        posture = self._controls.build_posture(
            index,
            parent_work_unit_id,
            generated_at=timestamp,
            max_branches=max_branches,
        )
        latest_control = self._controls.latest_branch_control_receipt(index, "WORK_UNIT", parent_work_unit_id)
        latest_settlement = self._settlement.latest_settlement_receipt(index, "WORK_UNIT", parent_work_unit_id)

        layer, summary, work_item, synchronization_reason, next_action, accepted_delta_ids, deferred_branch_work_unit_ids, review_reasons, warnings = _derive_future_posture(
            parent,
            posture,
            latest_settlement,
        )

        _clear_other_horizon_layers(store, index, parent_work_unit_id, keep_layer=layer)
        horizon_result = self._horizon.upsert_record(
            store,
            index,
            scope_type="WORK_UNIT",
            scope_ref=parent_work_unit_id,
            horizon_layer=layer,
            summary=summary,
            work_items=(work_item,),
            governing_refs=tuple(
                dict.fromkeys(
                    tuple(filter(None, (
                        None if latest_control is None else latest_control.receipt_id,
                        None if latest_settlement is None else latest_settlement.receipt_id,
                    ))) + source_claim_ids
                )
            ),
            linked_automation_state_id=None,
            linked_manifest_id=None,
            notes="M4 branch-aware future synchronization",
        )

        schedule_projection = self._scheduler.build_schedule_projection(
            index,
            graph,
            scope_type="WORK_UNIT",
            scope_ref=parent_work_unit_id,
            generated_at=timestamp,
        )
        candidate = schedule_projection.selected_candidate or (schedule_projection.candidates[0] if schedule_projection.candidates else None)
        schedule_receipt = None
        if candidate is not None:
            schedule_receipt = self._scheduler.persist_schedule_receipt(
                store,
                index,
                candidate,
                created_at=timestamp,
            )

        receipt = BranchHorizonSyncReceipt(
            receipt_id=branch_horizon_sync_receipt_id("WORK_UNIT", parent_work_unit_id, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface().policy_id,
            parent_scope_type="WORK_UNIT",
            parent_scope_ref=parent_work_unit_id,
            synchronized_horizon_id=horizon_result.persisted_record.horizon_id,
            synchronized_horizon_layer=layer,
            synchronized_schedule_receipt_id=(None if schedule_receipt is None else schedule_receipt.receipt_id),
            selected_schedule_candidate_id=(None if candidate is None else candidate.candidate_id),
            selected_schedule_state=(None if candidate is None else candidate.scheduler_state),
            selected_schedule_commitment=(None if candidate is None else candidate.commitment),
            source_branch_control_receipt_id=(None if latest_control is None else latest_control.receipt_id),
            source_branch_settlement_receipt_id=(None if latest_settlement is None else latest_settlement.receipt_id),
            source_branch_claim_receipt_ids=source_claim_ids,
            active_branch_work_unit_ids=posture.active_branch_work_unit_ids,
            accepted_delta_ids=accepted_delta_ids,
            deferred_branch_work_unit_ids=deferred_branch_work_unit_ids,
            review_reasons=review_reasons,
            next_action=next_action,
            synchronization_reason=synchronization_reason,
            warnings=warnings,
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_receipt(
        self,
        index: KernelIndex,
        parent_scope_type: str | None = None,
        parent_scope_ref: str | None = None,
    ) -> BranchHorizonSyncReceipt | None:
        if parent_scope_type is None and parent_scope_ref is None:
            receipts = [
                record
                for record in index.records_by_type("branch_horizon_sync_receipt")
                if isinstance(record, BranchHorizonSyncReceipt)
            ]
        elif parent_scope_type is not None and parent_scope_ref is not None:
            receipts = index.branch_horizon_sync_receipts_for_parent(parent_scope_type, parent_scope_ref)
        else:
            raise KernelBranchHorizonSyncError("parent_scope_type and parent_scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: BranchHorizonSyncReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "parent_scope_type": receipt.parent_scope_type,
            "parent_scope_ref": receipt.parent_scope_ref,
            "synchronized_horizon_id": receipt.synchronized_horizon_id,
            "synchronized_horizon_layer": receipt.synchronized_horizon_layer.value,
            "synchronized_schedule_receipt_id": receipt.synchronized_schedule_receipt_id,
            "selected_schedule_candidate_id": receipt.selected_schedule_candidate_id,
            "selected_schedule_state": (None if receipt.selected_schedule_state is None else receipt.selected_schedule_state.value),
            "selected_schedule_commitment": (None if receipt.selected_schedule_commitment is None else receipt.selected_schedule_commitment.value),
            "source_branch_control_receipt_id": receipt.source_branch_control_receipt_id,
            "source_branch_settlement_receipt_id": receipt.source_branch_settlement_receipt_id,
            "source_branch_claim_receipt_ids": list(receipt.source_branch_claim_receipt_ids),
            "active_branch_work_unit_ids": list(receipt.active_branch_work_unit_ids),
            "accepted_delta_ids": list(receipt.accepted_delta_ids),
            "deferred_branch_work_unit_ids": list(receipt.deferred_branch_work_unit_ids),
            "review_reasons": list(receipt.review_reasons),
            "next_action": receipt.next_action,
            "synchronization_reason": receipt.synchronization_reason,
            "warnings": list(receipt.warnings),
        }


def branch_horizon_sync_receipt_id(parent_scope_type: str, parent_scope_ref: str, created_at: str) -> str:
    return f"sync-{_slug(parent_scope_type)}-{_slug(parent_scope_ref)}-{_slug(created_at)}"


def _derive_future_posture(parent, posture, settlement):
    base_target_refs = tuple(dict.fromkeys(parent.allowed_writes or (parent.scope_ref,)))
    warnings = list(posture.warnings)
    accepted_delta_ids = ()
    deferred_branch_work_unit_ids = ()
    review_reasons = ()
    if settlement is not None:
        accepted_delta_ids = settlement.accepted_delta_ids
        deferred_branch_work_unit_ids = settlement.deferred_branch_work_unit_ids
        review_reasons = settlement.review_reasons
        warnings.extend(settlement.warnings)
        if settlement.outcome is BranchSettlementOutcome.ACCEPTED_AS_IS:
            return (
                HorizonLayer.IMMEDIATE,
                "Accepted branch returns are ready to resume the parent execution loop.",
                HorizonWorkItem(
                    item_id=f"sync-accept-{parent.work_unit_id}",
                    title=f"Resume parent after accepted branches for {parent.scope_ref}",
                    summary="Bounded branch returns were accepted and should now continue in the parent loop.",
                    executor_hint=parent.agent_personal_name,
                    target_refs=base_target_refs,
                    packet_ready=True,
                    priority="P0_CRITICAL",
                    next_window_hint="IMMEDIATE",
                ),
                "SETTLEMENT_ACCEPTED",
                "RESUME_PARENT_LOOP",
                accepted_delta_ids,
                deferred_branch_work_unit_ids,
                review_reasons,
                tuple(dict.fromkeys(warnings)),
            )
        if settlement.outcome is BranchSettlementOutcome.MERGE_PROPOSAL_REQUIRED:
            conflict_refs = tuple(settlement.conflict_paths or base_target_refs)
            return (
                HorizonLayer.IMMEDIATE,
                "A bounded merge proposal is now the parent-scope next step.",
                HorizonWorkItem(
                    item_id=f"sync-merge-{parent.work_unit_id}",
                    title=f"Resolve merge proposal for {parent.scope_ref}",
                    summary="Branch settlement produced an explicit merge proposal that must be resolved before continuation.",
                    executor_hint=parent.agent_personal_name,
                    target_refs=conflict_refs,
                    packet_ready=True,
                    priority="P0_CRITICAL",
                    blocking_notes=settlement.conflict_paths,
                    next_window_hint="IMMEDIATE",
                ),
                "SETTLEMENT_REQUIRES_MERGE",
                "RESOLVE_MERGE_PROPOSAL",
                accepted_delta_ids,
                deferred_branch_work_unit_ids,
                review_reasons,
                tuple(dict.fromkeys(warnings)),
            )
        if settlement.outcome is BranchSettlementOutcome.ESCALATE_REVIEW:
            return (
                HorizonLayer.IMMEDIATE,
                "Branch settlement escalated review and should return as an immediate bounded review step.",
                HorizonWorkItem(
                    item_id=f"sync-review-{parent.work_unit_id}",
                    title=f"Escalate branch review for {parent.scope_ref}",
                    summary="Settlement reached explicit review pressure and must return as a bounded review packet.",
                    executor_hint=parent.agent_personal_name,
                    target_refs=base_target_refs,
                    packet_ready=True,
                    priority="P0_CRITICAL",
                    blocking_notes=settlement.review_reasons,
                    next_window_hint="IMMEDIATE",
                ),
                "SETTLEMENT_ESCALATED_REVIEW",
                "ESCALATE_BRANCH_REVIEW",
                accepted_delta_ids,
                deferred_branch_work_unit_ids,
                review_reasons,
                tuple(dict.fromkeys(warnings)),
            )
        if settlement.outcome is BranchSettlementOutcome.DEFERRED:
            return (
                HorizonLayer.NEAR,
                "Deferred branch settlement remains a near-horizon parent obligation.",
                HorizonWorkItem(
                    item_id=f"sync-deferred-{parent.work_unit_id}",
                    title=f"Await deferred branch prerequisites for {parent.scope_ref}",
                    summary="Settlement deferred parent continuation pending additional branch progress.",
                    executor_hint=parent.agent_personal_name,
                    target_refs=base_target_refs,
                    dependency_refs=tuple(settlement.deferred_branch_work_unit_ids),
                    packet_ready=False,
                    priority="P1_HIGH",
                    next_window_hint="NEAR",
                ),
                "SETTLEMENT_DEFERRED",
                "WAIT_FOR_DEFERRED_BRANCHES",
                accepted_delta_ids,
                deferred_branch_work_unit_ids,
                review_reasons,
                tuple(dict.fromkeys(warnings)),
            )
        if settlement.outcome is BranchSettlementOutcome.ABANDONED:
            return (
                HorizonLayer.FAR,
                "An abandoned branch line remains as weak future pressure rather than immediate work.",
                HorizonWorkItem(
                    item_id=f"sync-abandoned-{parent.work_unit_id}",
                    title=f"Reassess abandoned branch line for {parent.scope_ref}",
                    summary="The branch line was abandoned; preserve the future pressure without forcing immediate enactment.",
                    executor_hint=parent.agent_personal_name,
                    target_refs=base_target_refs,
                    packet_ready=False,
                    priority="P2_NORMAL",
                    next_window_hint="FAR",
                ),
                "SETTLEMENT_ABANDONED",
                "PRESERVE_ABANDONED_BRANCH_CONTEXT",
                accepted_delta_ids,
                deferred_branch_work_unit_ids,
                review_reasons,
                tuple(dict.fromkeys(warnings)),
            )

    if posture.stale_return_delta_ids:
        return (
            HorizonLayer.IMMEDIATE,
            "Stale branch returns require explicit immediate review.",
            HorizonWorkItem(
                item_id=f"sync-stale-return-{parent.work_unit_id}",
                title=f"Review stale branch returns for {parent.scope_ref}",
                summary="Returns exist outside the active claim set and must be reviewed explicitly.",
                executor_hint=parent.agent_personal_name,
                target_refs=base_target_refs,
                packet_ready=True,
                priority="P0_CRITICAL",
                blocking_notes=tuple(posture.stale_return_delta_ids),
                next_window_hint="IMMEDIATE",
            ),
            "STALE_RETURN_REVIEW",
            "ESCALATE_STALE_RETURN_REVIEW",
            accepted_delta_ids,
            deferred_branch_work_unit_ids,
            review_reasons,
            tuple(dict.fromkeys(warnings)),
        )

    if posture.active_branch_work_unit_ids:
        return (
            HorizonLayer.NEAR,
            "Active branches exist and should remain visible as structured near-horizon pressure.",
            HorizonWorkItem(
                item_id=f"sync-active-{parent.work_unit_id}",
                title=f"Await active branch returns for {parent.scope_ref}",
                summary="The parent future posture depends on currently active bounded child branches.",
                executor_hint=parent.agent_personal_name,
                target_refs=base_target_refs,
                dependency_refs=posture.active_branch_work_unit_ids,
                packet_ready=False,
                priority="P1_HIGH",
                next_window_hint="NEAR",
            ),
            "ACTIVE_BRANCHES_PENDING",
            "WAIT_FOR_ACTIVE_BRANCHES",
            accepted_delta_ids,
            deferred_branch_work_unit_ids,
            review_reasons,
            tuple(dict.fromkeys(warnings)),
        )

    if posture.stale_claim_receipt_ids:
        return (
            HorizonLayer.NEAR,
            "Stale branch claims still shape the parent near horizon until reconciled.",
            HorizonWorkItem(
                item_id=f"sync-stale-claims-{parent.work_unit_id}",
                title=f"Refresh stale branch claims for {parent.scope_ref}",
                summary="Stale claims should be decayed or refreshed before new branching pressure is added.",
                executor_hint=parent.agent_personal_name,
                target_refs=base_target_refs,
                dependency_refs=tuple(posture.stale_claim_receipt_ids),
                packet_ready=False,
                priority="P1_HIGH",
                next_window_hint="NEAR",
            ),
            "STALE_CLAIMS_PENDING",
            "DECAY_OR_REFRESH_STALE_CLAIMS",
            accepted_delta_ids,
            deferred_branch_work_unit_ids,
            review_reasons,
            tuple(dict.fromkeys(warnings)),
        )

    if posture.recursion_refused:
        return (
            HorizonLayer.NEAR,
            "Recursion refusal now constrains future branch widening.",
            HorizonWorkItem(
                item_id=f"sync-recursion-{parent.work_unit_id}",
                title=f"Respect branch ceiling for {parent.scope_ref}",
                summary="Branch recursion is currently refused; preserve that pressure without widening the branch tree.",
                executor_hint=parent.agent_personal_name,
                target_refs=base_target_refs,
                packet_ready=False,
                priority="P1_HIGH",
                next_window_hint="NEAR",
            ),
            "RECURSION_REFUSED",
            "PRESERVE_BRANCH_CEILING",
            accepted_delta_ids,
            deferred_branch_work_unit_ids,
            review_reasons,
            tuple(dict.fromkeys(warnings)),
        )

    return (
        HorizonLayer.FAR,
        "No active branch pressure exists; preserve a weak parent future posture only.",
        HorizonWorkItem(
            item_id=f"sync-idle-{parent.work_unit_id}",
            title=f"Maintain branch-aware future posture for {parent.scope_ref}",
            summary="No active branches are present; keep only weak future posture rather than forcing immediate work.",
            executor_hint=parent.agent_personal_name,
            target_refs=base_target_refs,
            packet_ready=False,
            priority="P2_NORMAL",
            next_window_hint="FAR",
        ),
        "NO_ACTIVE_BRANCH_PRESSURE",
        "MAINTAIN_WEAK_BRANCH_POSTURE",
        accepted_delta_ids,
        deferred_branch_work_unit_ids,
        review_reasons,
        tuple(dict.fromkeys(warnings)),
    )


def _clear_other_horizon_layers(store: KernelStore, index: KernelIndex, parent_work_unit_id: str, *, keep_layer: HorizonLayer) -> None:
    for record in list(index.horizon_states_for_scope("WORK_UNIT", parent_work_unit_id)):
        if record.horizon_layer is keep_layer:
            continue
        store.delete("horizon_state", record.horizon_id)
        index.record_removed("horizon_state", record.horizon_id)


def _resolve_parent(index: KernelIndex, parent_work_unit_id: str) -> WorkUnit:
    parent = index.get("work_unit", parent_work_unit_id)
    if not isinstance(parent, WorkUnit):
        raise KernelBranchHorizonSyncError(f"Unknown parent work unit: {parent_work_unit_id}")
    return parent


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
