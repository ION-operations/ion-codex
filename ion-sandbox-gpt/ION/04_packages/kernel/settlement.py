"""M2 fan-in / merge / review settlement surfaces for the active ION kernel stack.

This module implements one bounded settlement floor on top of M0/M1 law:
- inspect active branch claims under one committed parent scope,
- gather the latest explicit branch returns,
- classify the fan-in posture as accepted, deferred, merge-required, review escalation, or abandoned,
- persist bounded settlement receipts,
- and preserve merge proposals as explicit contracts rather than silent synthesis.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
import re

from .branch_controls import KernelBranchControlManager
from .index import KernelIndex
from .model import (
    BranchClaimReceipt,
    BranchClaimStatus,
    BranchMergeProposal,
    BranchSettlementOutcome,
    BranchSettlementReceipt,
    CommitDelta,
    CommitDeltaStatus,
)
from .store import KernelStore


class KernelBranchSettlementError(Exception):
    """Raised when one bounded settlement operation cannot be completed lawfully."""


@dataclass(frozen=True)
class SettlementPolicySurface:
    policy_id: str
    notes: tuple[str, ...]


@dataclass(frozen=True)
class BranchReturnCandidate:
    claim_receipt_id: str
    branch_work_unit_id: str
    branch_scope_type: str
    branch_scope_ref: str
    selected_executor_id: str | None
    selected_capability_id: str | None
    delta_id: str | None
    delta_status: str | None
    artifact_paths: tuple[str, ...]
    ready_for_settlement: bool
    reason: str
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class MergeProposalDraft:
    proposal_id: str
    created_at: str
    parent_scope_type: str
    parent_scope_ref: str
    branch_work_unit_ids: tuple[str, ...]
    delta_ids: tuple[str, ...]
    conflict_paths: tuple[str, ...]
    proposed_strategy: str
    notes: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class BranchSettlementProjection:
    settlement_id: str
    generated_at: str
    policy: SettlementPolicySurface
    parent_scope_type: str
    parent_scope_ref: str
    outcome: BranchSettlementOutcome
    considered_claim_receipt_ids: tuple[str, ...]
    branches: tuple[BranchReturnCandidate, ...]
    considered_delta_ids: tuple[str, ...]
    accepted_delta_ids: tuple[str, ...]
    deferred_branch_work_unit_ids: tuple[str, ...]
    conflict_paths: tuple[str, ...]
    review_reasons: tuple[str, ...]
    next_action: str
    merge_proposal: MergeProposalDraft | None = None
    warnings: tuple[str, ...] = ()


class KernelBranchSettlementManager:
    """Settle bounded child returns back into one parent scope under M2 law."""

    def __init__(self) -> None:
        self._branch_controls = KernelBranchControlManager()

    def policy_surface(self) -> SettlementPolicySurface:
        return SettlementPolicySurface(
            policy_id="M2_SETTLEMENT_V1",
            notes=(
                "Settlement never lands multiple child returns silently.",
                "Conflicting branch returns become explicit merge proposals or review escalation, not implicit synthesis.",
                "Deferred branches preserve active claims until later settlement can occur.",
                "Final settlement releases active branch claims back to the parent scope.",
            ),
        )

    def build_settlement_projection(
        self,
        index: KernelIndex,
        parent_work_unit_id: str,
        *,
        generated_at: str | None = None,
    ) -> BranchSettlementProjection:
        posture = self._branch_controls.build_posture(
            index,
            parent_work_unit_id,
            generated_at=generated_at,
        )
        stale_claim_ids = set(posture.stale_claim_receipt_ids)
        active_claims = [
            receipt
            for receipt in index.branch_claim_receipts_for_parent("WORK_UNIT", parent_work_unit_id)
            if receipt.claim_status is BranchClaimStatus.ACTIVE and receipt.receipt_id not in stale_claim_ids
        ]
        if not active_claims:
            raise KernelBranchSettlementError(
                f"No active branch claims exist under parent {parent_work_unit_id}"
            )

        timestamp = generated_at or _iso_now()
        branches: list[BranchReturnCandidate] = []
        considered_delta_ids: list[str] = []
        deferred_branch_ids: list[str] = []
        review_reasons: list[str] = []
        warnings: list[str] = list(posture.warnings)
        accepted_delta_ids: list[str] = []
        artifact_claims: dict[str, list[tuple[str, str]]] = {}
        rejected_delta_ids: list[str] = []

        for claim in _sorted_claims(active_claims):
            delta = _latest_commit_delta(index, claim.branch_work_unit_id)
            if delta is None:
                branches.append(
                    BranchReturnCandidate(
                        claim_receipt_id=claim.receipt_id,
                        branch_work_unit_id=claim.branch_work_unit_id,
                        branch_scope_type=claim.branch_scope_type,
                        branch_scope_ref=claim.branch_scope_ref,
                        selected_executor_id=claim.selected_executor_id,
                        selected_capability_id=claim.selected_capability_id,
                        delta_id=None,
                        delta_status=None,
                        artifact_paths=(),
                        ready_for_settlement=False,
                        reason="MISSING_BRANCH_RETURN",
                    )
                )
                deferred_branch_ids.append(claim.branch_work_unit_id)
                continue

            artifact_paths = tuple(artifact.path for artifact in delta.produced_artifacts)
            candidate_warnings: list[str] = []
            unexpected_paths = sorted(set(artifact_paths) - set(claim.allowed_writes))
            if unexpected_paths:
                candidate_warnings.append(
                    "RETURN_OUTSIDE_CLAIM:" + ",".join(unexpected_paths)
                )
                review_reasons.append(
                    f"{claim.branch_work_unit_id}:RETURN_OUTSIDE_CLAIM:{','.join(unexpected_paths)}"
                )
            if delta.status in {CommitDeltaStatus.REQUIRES_REVIEW, CommitDeltaStatus.REQUIRES_RECONCILIATION}:
                review_reasons.append(f"{claim.branch_work_unit_id}:{delta.status.value}")
            if delta.status is CommitDeltaStatus.REJECTED:
                rejected_delta_ids.append(delta.delta_id)
                review_reasons.append(f"{claim.branch_work_unit_id}:REJECTED")

            for artifact in delta.produced_artifacts:
                artifact_claims.setdefault(artifact.path, []).append((claim.branch_work_unit_id, delta.delta_id))

            considered_delta_ids.append(delta.delta_id)
            branches.append(
                BranchReturnCandidate(
                    claim_receipt_id=claim.receipt_id,
                    branch_work_unit_id=claim.branch_work_unit_id,
                    branch_scope_type=claim.branch_scope_type,
                    branch_scope_ref=claim.branch_scope_ref,
                    selected_executor_id=claim.selected_executor_id,
                    selected_capability_id=claim.selected_capability_id,
                    delta_id=delta.delta_id,
                    delta_status=delta.status.value,
                    artifact_paths=artifact_paths,
                    ready_for_settlement=delta.status not in {
                        CommitDeltaStatus.REQUIRES_REVIEW,
                        CommitDeltaStatus.REQUIRES_RECONCILIATION,
                        CommitDeltaStatus.REJECTED,
                    },
                    reason=_delta_reason(delta.status),
                    warnings=tuple(candidate_warnings),
                )
            )

        conflict_paths = tuple(
            sorted(path for path, claims in artifact_claims.items() if len(claims) > 1)
        )
        if posture.stale_return_delta_ids:
            for delta_id in posture.stale_return_delta_ids:
                review_reasons.append(f"STALE_RETURN:{delta_id}")

        merge_proposal: MergeProposalDraft | None = None
        outcome: BranchSettlementOutcome
        next_action: str

        if considered_delta_ids and len(rejected_delta_ids) == len(considered_delta_ids):
            outcome = BranchSettlementOutcome.ABANDONED
            next_action = "ABANDON_BRANCH_SET"
        elif review_reasons:
            outcome = BranchSettlementOutcome.ESCALATE_REVIEW
            next_action = "ESCALATE_REVIEW"
        elif deferred_branch_ids:
            outcome = BranchSettlementOutcome.DEFERRED
            next_action = "WAIT_FOR_BRANCH_RETURNS"
        elif conflict_paths:
            outcome = BranchSettlementOutcome.MERGE_PROPOSAL_REQUIRED
            next_action = "REVIEW_MERGE_PROPOSAL"
            merge_proposal = MergeProposalDraft(
                proposal_id=branch_merge_proposal_id("WORK_UNIT", parent_work_unit_id, timestamp),
                created_at=timestamp,
                parent_scope_type="WORK_UNIT",
                parent_scope_ref=parent_work_unit_id,
                branch_work_unit_ids=tuple(branch.branch_work_unit_id for branch in branches),
                delta_ids=tuple(considered_delta_ids),
                conflict_paths=conflict_paths,
                proposed_strategy="EXPLICIT_PARENT_REVIEW_REQUIRED",
                notes=(
                    "Multiple child returns touched overlapping artifact paths.",
                    "Parent-scope review or an explicit merge packet is required before landing.",
                ),
            )
        else:
            outcome = BranchSettlementOutcome.ACCEPTED_AS_IS
            next_action = "LAND_PARENT"
            accepted_delta_ids = list(considered_delta_ids)

        return BranchSettlementProjection(
            settlement_id=branch_settlement_receipt_id("WORK_UNIT", parent_work_unit_id, timestamp),
            generated_at=timestamp,
            policy=self.policy_surface(),
            parent_scope_type="WORK_UNIT",
            parent_scope_ref=parent_work_unit_id,
            outcome=outcome,
            considered_claim_receipt_ids=tuple(claim.receipt_id for claim in _sorted_claims(active_claims)),
            branches=tuple(branches),
            considered_delta_ids=tuple(considered_delta_ids),
            accepted_delta_ids=tuple(accepted_delta_ids),
            deferred_branch_work_unit_ids=tuple(sorted(deferred_branch_ids)),
            conflict_paths=conflict_paths,
            review_reasons=tuple(review_reasons),
            next_action=next_action,
            merge_proposal=merge_proposal,
            warnings=tuple(warnings),
        )

    def persist_settlement(
        self,
        store: KernelStore,
        index: KernelIndex,
        parent_work_unit_id: str,
        *,
        created_at: str | None = None,
    ) -> tuple[BranchSettlementReceipt, BranchMergeProposal | None]:
        projection = self.build_settlement_projection(
            index,
            parent_work_unit_id,
            generated_at=created_at,
        )

        merge_proposal = None
        if projection.merge_proposal is not None:
            merge_proposal = BranchMergeProposal(
                proposal_id=projection.merge_proposal.proposal_id,
                created_at=projection.merge_proposal.created_at,
                parent_scope_type=projection.merge_proposal.parent_scope_type,
                parent_scope_ref=projection.merge_proposal.parent_scope_ref,
                branch_work_unit_ids=projection.merge_proposal.branch_work_unit_ids,
                delta_ids=projection.merge_proposal.delta_ids,
                conflict_paths=projection.merge_proposal.conflict_paths,
                proposed_strategy=projection.merge_proposal.proposed_strategy,
                notes=projection.merge_proposal.notes,
                warnings=projection.merge_proposal.warnings,
            )
            store.create(merge_proposal)
            index.record_added(merge_proposal)

        released_claim_ids: list[str] = []
        if projection.outcome is not BranchSettlementOutcome.DEFERRED:
            for claim_receipt_id in projection.considered_claim_receipt_ids:
                current = index.get("branch_claim_receipt", claim_receipt_id)
                if not isinstance(current, BranchClaimReceipt):
                    continue
                if current.claim_status is not BranchClaimStatus.ACTIVE:
                    continue
                updated = replace(current, claim_status=BranchClaimStatus.RELEASED)
                store.replace(updated)
                index.record_changed(updated)
                released_claim_ids.append(updated.receipt_id)

        receipt = BranchSettlementReceipt(
            receipt_id=projection.settlement_id,
            created_at=projection.generated_at,
            parent_scope_type=projection.parent_scope_type,
            parent_scope_ref=projection.parent_scope_ref,
            outcome=projection.outcome,
            considered_claim_receipt_ids=projection.considered_claim_receipt_ids,
            branch_work_unit_ids=tuple(branch.branch_work_unit_id for branch in projection.branches),
            considered_delta_ids=projection.considered_delta_ids,
            accepted_delta_ids=projection.accepted_delta_ids,
            deferred_branch_work_unit_ids=projection.deferred_branch_work_unit_ids,
            released_claim_receipt_ids=tuple(released_claim_ids),
            merge_proposal_id=(merge_proposal.proposal_id if merge_proposal is not None else None),
            conflict_paths=projection.conflict_paths,
            review_reasons=projection.review_reasons,
            next_action=projection.next_action,
            warnings=projection.warnings,
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt, merge_proposal

    def latest_settlement_receipt(
        self,
        index: KernelIndex,
        parent_scope_type: str | None = None,
        parent_scope_ref: str | None = None,
    ) -> BranchSettlementReceipt | None:
        normalized_scope = _normalize_scope_filter(parent_scope_type, parent_scope_ref)
        if normalized_scope is None:
            receipts = [
                record
                for record in index.records_by_type("branch_settlement_receipt")
                if isinstance(record, BranchSettlementReceipt)
            ]
        else:
            receipts = index.branch_settlement_receipts_for_parent(normalized_scope[0], normalized_scope[1])
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_projection(self, projection: BranchSettlementProjection) -> dict[str, object]:
        return {
            "settlement_id": projection.settlement_id,
            "generated_at": projection.generated_at,
            "policy_id": projection.policy.policy_id,
            "policy_notes": list(projection.policy.notes),
            "parent_scope_type": projection.parent_scope_type,
            "parent_scope_ref": projection.parent_scope_ref,
            "outcome": projection.outcome.value,
            "considered_claim_receipt_ids": list(projection.considered_claim_receipt_ids),
            "branches": [_branch_projection(item) for item in projection.branches],
            "considered_delta_ids": list(projection.considered_delta_ids),
            "accepted_delta_ids": list(projection.accepted_delta_ids),
            "deferred_branch_work_unit_ids": list(projection.deferred_branch_work_unit_ids),
            "conflict_paths": list(projection.conflict_paths),
            "review_reasons": list(projection.review_reasons),
            "next_action": projection.next_action,
            "merge_proposal": (_merge_projection(projection.merge_proposal) if projection.merge_proposal else None),
            "warnings": list(projection.warnings),
        }

    def render_receipt_projection(
        self,
        receipt: BranchSettlementReceipt | None,
    ) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "parent_scope_type": receipt.parent_scope_type,
            "parent_scope_ref": receipt.parent_scope_ref,
            "outcome": receipt.outcome.value,
            "considered_claim_receipt_ids": list(receipt.considered_claim_receipt_ids),
            "branch_work_unit_ids": list(receipt.branch_work_unit_ids),
            "considered_delta_ids": list(receipt.considered_delta_ids),
            "accepted_delta_ids": list(receipt.accepted_delta_ids),
            "deferred_branch_work_unit_ids": list(receipt.deferred_branch_work_unit_ids),
            "released_claim_receipt_ids": list(receipt.released_claim_receipt_ids),
            "merge_proposal_id": receipt.merge_proposal_id,
            "conflict_paths": list(receipt.conflict_paths),
            "review_reasons": list(receipt.review_reasons),
            "next_action": receipt.next_action,
            "warnings": list(receipt.warnings),
        }


def branch_settlement_receipt_id(parent_scope_type: str, parent_scope_ref: str, created_at: str) -> str:
    return f"branch-settlement-{_slug(parent_scope_type)}-{_slug(parent_scope_ref)}-{_slug(created_at)}"


def branch_merge_proposal_id(parent_scope_type: str, parent_scope_ref: str, created_at: str) -> str:
    return f"branch-merge-proposal-{_slug(parent_scope_type)}-{_slug(parent_scope_ref)}-{_slug(created_at)}"


def _latest_commit_delta(index: KernelIndex, work_unit_id: str) -> CommitDelta | None:
    deltas = [record for record in index.records_for_work_unit(work_unit_id) if isinstance(record, CommitDelta)]
    if not deltas:
        return None
    deltas.sort(key=lambda item: (item.created_at, item.delta_id))
    return deltas[-1]


def _sorted_claims(claims: list[BranchClaimReceipt]) -> list[BranchClaimReceipt]:
    return sorted(claims, key=lambda item: (item.created_at, item.branch_work_unit_id, item.receipt_id))


def _branch_projection(candidate: BranchReturnCandidate) -> dict[str, object]:
    return {
        "claim_receipt_id": candidate.claim_receipt_id,
        "branch_work_unit_id": candidate.branch_work_unit_id,
        "branch_scope_type": candidate.branch_scope_type,
        "branch_scope_ref": candidate.branch_scope_ref,
        "selected_executor_id": candidate.selected_executor_id,
        "selected_capability_id": candidate.selected_capability_id,
        "delta_id": candidate.delta_id,
        "delta_status": candidate.delta_status,
        "artifact_paths": list(candidate.artifact_paths),
        "ready_for_settlement": candidate.ready_for_settlement,
        "reason": candidate.reason,
        "warnings": list(candidate.warnings),
    }


def _merge_projection(draft: MergeProposalDraft) -> dict[str, object]:
    return {
        "proposal_id": draft.proposal_id,
        "created_at": draft.created_at,
        "parent_scope_type": draft.parent_scope_type,
        "parent_scope_ref": draft.parent_scope_ref,
        "branch_work_unit_ids": list(draft.branch_work_unit_ids),
        "delta_ids": list(draft.delta_ids),
        "conflict_paths": list(draft.conflict_paths),
        "proposed_strategy": draft.proposed_strategy,
        "notes": list(draft.notes),
        "warnings": list(draft.warnings),
    }


def _delta_reason(status: CommitDeltaStatus) -> str:
    if status is CommitDeltaStatus.ACCEPTED:
        return "RETURN_READY"
    if status is CommitDeltaStatus.PROPOSED:
        return "RETURN_READY"
    if status is CommitDeltaStatus.ACCEPTED_AS_WITNESS:
        return "RETURN_READY"
    return status.value


def _normalize_scope_filter(
    scope_type: str | None,
    scope_ref: str | None,
) -> tuple[str, str] | None:
    if scope_type is None and scope_ref is None:
        return None
    if scope_type is None or scope_ref is None:
        raise KernelBranchSettlementError("scope_type and scope_ref must be provided together")
    return scope_type, scope_ref


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


def _slug(value: str) -> str:
    normalized = _SAFE_ID_RE.sub("-", value.lower()).strip("-")
    return normalized or "x"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
