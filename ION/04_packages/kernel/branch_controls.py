"""M3 branch budget / recursion / drift control surfaces for the active ION kernel stack.

This module keeps bounded branching lawful after M1/M2 made fan-out and fan-in real:
- surface explicit branch budget posture for one committed parent work unit,
- refuse recursive re-fan-out beyond the current bounded depth ceiling,
- identify and optionally decay stale active branch claims,
- detect stale child returns that no longer belong to an active claim set,
- and persist explicit branch-control receipts for operator visibility.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
import re

from .index import KernelIndex
from .model import BranchClaimReceipt, BranchClaimStatus, BranchControlReceipt, CommitDelta, WorkUnit
from .store import KernelStore


class KernelBranchControlError(Exception):
    """Raised when branch-control posture cannot be assessed lawfully."""


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


@dataclass(frozen=True)
class BranchControlPolicySurface:
    policy_id: str
    stale_claim_after_seconds: int
    max_branch_depth: int
    notes: tuple[str, ...]


@dataclass(frozen=True)
class BranchControlProjection:
    receipt_id: str
    generated_at: str
    policy: BranchControlPolicySurface
    parent_scope_type: str
    parent_scope_ref: str
    parent_depth: int
    branch_budget_limit: int | None
    budget_remaining: int | None
    active_claim_receipt_ids: tuple[str, ...]
    active_branch_work_unit_ids: tuple[str, ...]
    stale_claim_receipt_ids: tuple[str, ...]
    stale_return_delta_ids: tuple[str, ...]
    stale_return_branch_work_unit_ids: tuple[str, ...]
    recursion_refused: bool
    next_action: str
    warnings: tuple[str, ...] = ()
    decayed_claim_receipt_ids: tuple[str, ...] = ()


class KernelBranchControlManager:
    """Assess and persist bounded branch-control posture under M3 law."""

    def __init__(
        self,
        *,
        stale_claim_after_seconds: int = 3600,
        max_branch_depth: int = 1,
    ) -> None:
        self._stale_claim_after_seconds = stale_claim_after_seconds
        self._max_branch_depth = max_branch_depth

    def policy_surface(self) -> BranchControlPolicySurface:
        return BranchControlPolicySurface(
            policy_id="M3_BRANCH_CONTROL_V1",
            stale_claim_after_seconds=self._stale_claim_after_seconds,
            max_branch_depth=self._max_branch_depth,
            notes=(
                "Bounded branching is now governed by explicit budget posture rather than hidden parent intent.",
                "Recursive re-fan-out beyond the configured branch depth ceiling is refused.",
                "Active claims that age past the stale window without a return are decay candidates rather than permanent budget consumers.",
                "Child returns that no longer belong to an active claim set are treated as stale-return drift and must not be ignored silently.",
            ),
        )

    def build_posture(
        self,
        index: KernelIndex,
        parent_work_unit_id: str,
        *,
        generated_at: str | None = None,
        max_branches: int | None = None,
    ) -> BranchControlProjection:
        parent = _resolve_parent(index, parent_work_unit_id)
        timestamp = generated_at or _iso_now()
        active_claims = [
            receipt
            for receipt in index.branch_claim_receipts_for_parent("WORK_UNIT", parent_work_unit_id)
            if receipt.claim_status is BranchClaimStatus.ACTIVE
        ]
        stale_claims = [
            receipt
            for receipt in active_claims
            if _claim_is_stale(index, receipt, timestamp, self._stale_claim_after_seconds)
        ]
        effective_active_claims = [
            receipt
            for receipt in active_claims
            if receipt.receipt_id not in {item.receipt_id for item in stale_claims}
        ]
        active_branch_work_unit_ids = tuple(sorted({receipt.branch_work_unit_id for receipt in effective_active_claims}))

        parent_depth = _branch_depth(index, parent)
        recursion_refused = parent_depth >= self._max_branch_depth

        branch_budget_limit = _branch_budget_limit(parent, max_branches)
        budget_remaining = (
            None
            if branch_budget_limit is None
            else max(branch_budget_limit - len(effective_active_claims), 0)
        )

        stale_return_delta_ids, stale_return_branch_work_unit_ids = _stale_returns(
            index,
            parent_work_unit_id,
            active_branch_work_unit_ids,
        )

        warnings: list[str] = []
        if recursion_refused:
            warnings.append(f"RECURSION_REFUSED:DEPTH_{parent_depth}")
        if stale_claims:
            warnings.append("STALE_CLAIMS_PRESENT:" + ",".join(sorted(item.receipt_id for item in stale_claims)))
        if stale_return_delta_ids:
            warnings.append("STALE_RETURNS_PRESENT:" + ",".join(stale_return_delta_ids))
        if branch_budget_limit is not None and budget_remaining == 0:
            warnings.append(f"BRANCH_BUDGET_EXHAUSTED:{branch_budget_limit}")

        if recursion_refused:
            next_action = "REFUSE_RECURSION"
        elif stale_return_delta_ids:
            next_action = "ESCALATE_STALE_RETURN_REVIEW"
        elif stale_claims:
            next_action = "DECAY_STALE_CLAIMS"
        elif branch_budget_limit is not None and budget_remaining == 0:
            next_action = "BUDGET_EXHAUSTED"
        else:
            next_action = "CONTINUE"

        return BranchControlProjection(
            receipt_id=branch_control_receipt_id("WORK_UNIT", parent_work_unit_id, timestamp),
            generated_at=timestamp,
            policy=self.policy_surface(),
            parent_scope_type="WORK_UNIT",
            parent_scope_ref=parent_work_unit_id,
            parent_depth=parent_depth,
            branch_budget_limit=branch_budget_limit,
            budget_remaining=budget_remaining,
            active_claim_receipt_ids=tuple(sorted(receipt.receipt_id for receipt in effective_active_claims)),
            active_branch_work_unit_ids=active_branch_work_unit_ids,
            stale_claim_receipt_ids=tuple(sorted(item.receipt_id for item in stale_claims)),
            stale_return_delta_ids=stale_return_delta_ids,
            stale_return_branch_work_unit_ids=stale_return_branch_work_unit_ids,
            recursion_refused=recursion_refused,
            next_action=next_action,
            warnings=tuple(warnings),
        )

    def decay_stale_claims(
        self,
        store: KernelStore,
        index: KernelIndex,
        parent_work_unit_id: str,
        *,
        generated_at: str | None = None,
    ) -> tuple[BranchClaimReceipt, ...]:
        posture = self.build_posture(index, parent_work_unit_id, generated_at=generated_at)
        updated: list[BranchClaimReceipt] = []
        for receipt_id in posture.stale_claim_receipt_ids:
            current = index.get("branch_claim_receipt", receipt_id)
            if not isinstance(current, BranchClaimReceipt):
                continue
            if current.claim_status is not BranchClaimStatus.ACTIVE:
                continue
            replaced = replace(current, claim_status=BranchClaimStatus.SUPERSEDED)
            store.replace(replaced)
            index.record_changed(replaced)
            updated.append(replaced)
        return tuple(updated)

    def persist_posture(
        self,
        store: KernelStore,
        index: KernelIndex,
        parent_work_unit_id: str,
        *,
        generated_at: str | None = None,
        max_branches: int | None = None,
        apply_decay: bool = False,
    ) -> BranchControlReceipt:
        timestamp = generated_at or _iso_now()
        posture = self.build_posture(
            index,
            parent_work_unit_id,
            generated_at=timestamp,
            max_branches=max_branches,
        )
        decayed_claim_receipt_ids: tuple[str, ...] = ()
        if apply_decay and posture.stale_claim_receipt_ids:
            decayed = self.decay_stale_claims(
                store,
                index,
                parent_work_unit_id,
                generated_at=timestamp,
            )
            decayed_claim_receipt_ids = tuple(sorted(item.receipt_id for item in decayed))
            posture = BranchControlProjection(
                **{
                    **posture.__dict__,
                    "decayed_claim_receipt_ids": decayed_claim_receipt_ids,
                }
            )

        receipt = BranchControlReceipt(
            receipt_id=posture.receipt_id,
            created_at=posture.generated_at,
            policy_id=posture.policy.policy_id,
            parent_scope_type=posture.parent_scope_type,
            parent_scope_ref=posture.parent_scope_ref,
            parent_depth=posture.parent_depth,
            branch_budget_limit=posture.branch_budget_limit,
            budget_remaining=posture.budget_remaining,
            active_claim_receipt_ids=posture.active_claim_receipt_ids,
            active_branch_work_unit_ids=posture.active_branch_work_unit_ids,
            stale_claim_receipt_ids=posture.stale_claim_receipt_ids,
            decayed_claim_receipt_ids=decayed_claim_receipt_ids,
            stale_return_delta_ids=posture.stale_return_delta_ids,
            stale_return_branch_work_unit_ids=posture.stale_return_branch_work_unit_ids,
            recursion_refused=posture.recursion_refused,
            next_action=posture.next_action,
            warnings=posture.warnings,
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_branch_control_receipt(
        self,
        index: KernelIndex,
        parent_scope_type: str | None = None,
        parent_scope_ref: str | None = None,
    ) -> BranchControlReceipt | None:
        if parent_scope_type is None and parent_scope_ref is None:
            receipts = [
                record
                for record in index.records_by_type("branch_control_receipt")
                if isinstance(record, BranchControlReceipt)
            ]
        elif parent_scope_type is not None and parent_scope_ref is not None:
            receipts = index.branch_control_receipts_for_parent(parent_scope_type, parent_scope_ref)
        else:
            raise KernelBranchControlError(
                "parent_scope_type and parent_scope_ref must be provided together"
            )
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_projection(self, projection: BranchControlProjection) -> dict[str, object]:
        return {
            "receipt_id": projection.receipt_id,
            "generated_at": projection.generated_at,
            "policy_id": projection.policy.policy_id,
            "policy_notes": list(projection.policy.notes),
            "stale_claim_after_seconds": projection.policy.stale_claim_after_seconds,
            "max_branch_depth": projection.policy.max_branch_depth,
            "parent_scope_type": projection.parent_scope_type,
            "parent_scope_ref": projection.parent_scope_ref,
            "parent_depth": projection.parent_depth,
            "branch_budget_limit": projection.branch_budget_limit,
            "budget_remaining": projection.budget_remaining,
            "active_claim_receipt_ids": list(projection.active_claim_receipt_ids),
            "active_branch_work_unit_ids": list(projection.active_branch_work_unit_ids),
            "stale_claim_receipt_ids": list(projection.stale_claim_receipt_ids),
            "stale_return_delta_ids": list(projection.stale_return_delta_ids),
            "stale_return_branch_work_unit_ids": list(projection.stale_return_branch_work_unit_ids),
            "recursion_refused": projection.recursion_refused,
            "next_action": projection.next_action,
            "warnings": list(projection.warnings),
            "decayed_claim_receipt_ids": list(projection.decayed_claim_receipt_ids),
        }

    def render_receipt_projection(self, receipt: BranchControlReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "parent_scope_type": receipt.parent_scope_type,
            "parent_scope_ref": receipt.parent_scope_ref,
            "parent_depth": receipt.parent_depth,
            "branch_budget_limit": receipt.branch_budget_limit,
            "budget_remaining": receipt.budget_remaining,
            "active_claim_receipt_ids": list(receipt.active_claim_receipt_ids),
            "active_branch_work_unit_ids": list(receipt.active_branch_work_unit_ids),
            "stale_claim_receipt_ids": list(receipt.stale_claim_receipt_ids),
            "decayed_claim_receipt_ids": list(receipt.decayed_claim_receipt_ids),
            "stale_return_delta_ids": list(receipt.stale_return_delta_ids),
            "stale_return_branch_work_unit_ids": list(receipt.stale_return_branch_work_unit_ids),
            "recursion_refused": receipt.recursion_refused,
            "next_action": receipt.next_action,
            "warnings": list(receipt.warnings),
        }


def branch_control_receipt_id(parent_scope_type: str, parent_scope_ref: str, created_at: str) -> str:
    return f"branch-control-{_slug(parent_scope_type)}-{_slug(parent_scope_ref)}-{_slug(created_at)}"


def _resolve_parent(index: KernelIndex, parent_work_unit_id: str) -> WorkUnit:
    record = index.get("work_unit", parent_work_unit_id)
    if not isinstance(record, WorkUnit):
        raise KernelBranchControlError(f"Unknown parent work unit: {parent_work_unit_id}")
    return record


def _branch_budget_limit(parent: WorkUnit, max_branches: int | None) -> int | None:
    if max_branches is not None:
        return max_branches
    if not parent.spawn_policy.may_spawn:
        return 0
    if parent.spawn_policy.max_children > 0:
        return parent.spawn_policy.max_children
    return None


def _branch_depth(index: KernelIndex, parent: WorkUnit) -> int:
    depth = 0
    cursor = parent.parent_work_unit_id
    visited: set[str] = set()
    while cursor is not None and cursor not in visited:
        visited.add(cursor)
        record = index.get("work_unit", cursor)
        if not isinstance(record, WorkUnit):
            break
        depth += 1
        cursor = record.parent_work_unit_id
    return depth


def _claim_is_stale(
    index: KernelIndex,
    receipt: BranchClaimReceipt,
    generated_at: str,
    stale_claim_after_seconds: int,
) -> bool:
    try:
        age = (datetime.fromisoformat(generated_at) - datetime.fromisoformat(receipt.created_at)).total_seconds()
    except ValueError:
        return False
    if age < stale_claim_after_seconds:
        return False
    return _latest_commit_delta(index, receipt.branch_work_unit_id) is None


def _stale_returns(
    index: KernelIndex,
    parent_work_unit_id: str,
    active_branch_work_unit_ids: tuple[str, ...],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    stale_delta_ids: list[str] = []
    stale_work_unit_ids: list[str] = []
    active_ids = set(active_branch_work_unit_ids)
    for child in index.child_work_units_for_parent(parent_work_unit_id):
        if child.work_unit_id in active_ids:
            continue
        delta = _latest_commit_delta(index, child.work_unit_id)
        if delta is None:
            continue
        stale_work_unit_ids.append(child.work_unit_id)
        stale_delta_ids.append(delta.delta_id)
    return tuple(sorted(stale_delta_ids)), tuple(sorted(stale_work_unit_ids))


def _latest_commit_delta(index: KernelIndex, work_unit_id: str) -> CommitDelta | None:
    deltas = [
        record
        for record in index.records_for_work_unit(work_unit_id)
        if isinstance(record, CommitDelta)
    ]
    if not deltas:
        return None
    deltas.sort(key=lambda item: (item.created_at, item.delta_id))
    return deltas[-1]


def _slug(value: str) -> str:
    clean = _SAFE_ID_RE.sub("-", value.strip().lower())
    return clean.strip("-") or "x"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
