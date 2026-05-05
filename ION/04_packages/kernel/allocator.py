"""M1 bounded multi-agent allocator surfaces for the active ION kernel stack.

This module implements one bounded allocation floor under M0 law:
- allocate already-issued child work units under one committed parent,
- bind them through the explicit capability registry,
- respect concurrency limits and write-conflict boundaries,
- and persist explicit branch-claim receipts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .branch_controls import KernelBranchControlManager
from .executor_registry import KernelExecutorCapabilityRegistry
from .graph import KernelGraph
from .id_compaction import compact_identifier
from .index import KernelIndex
from .model import (
    BranchClaimReceipt,
    BranchClaimStatus,
    CarrierBindingSource,
    ContextPackage,
    ExecutorCapability,
    ScheduleCarrier,
    WorkUnit,
    WorkUnitStatus,
)
from .scheduler import KernelScheduler
from .store import KernelStore


class KernelAllocatorError(Exception):
    """Raised when one bounded allocation operation cannot be completed lawfully."""


class BranchAllocationReason:
    SELECTED = "SELECTED"
    NOT_DISPATCHABLE = "NOT_DISPATCHABLE"
    MISSING_CAPABILITY = "MISSING_CAPABILITY"
    CAPACITY_EXHAUSTED = "CAPACITY_EXHAUSTED"
    WRITE_CONFLICT = "WRITE_CONFLICT"
    ALREADY_CLAIMED = "ALREADY_CLAIMED"
    MAX_BRANCHES_REACHED = "MAX_BRANCHES_REACHED"
    RECURSION_REFUSED = "RECURSION_REFUSED"


@dataclass(frozen=True)
class AllocationPolicySurface:
    policy_id: str
    notes: tuple[str, ...]


@dataclass(frozen=True)
class BranchAllocationCandidate:
    branch_id: str
    branch_work_unit_id: str
    context_package_id: str
    branch_scope_type: str
    branch_scope_ref: str
    branch_title: str
    branch_objective: str
    selected: bool
    reason: str
    priority: str
    selected_carrier: ScheduleCarrier
    carrier_binding_source: CarrierBindingSource
    selected_executor_id: str | None
    selected_capability_id: str | None
    allowed_writes: tuple[str, ...] = ()
    requested_reads: tuple[str, ...] = ()
    expected_output: str | None = None
    settlement_target: str | None = None
    capability_basis: tuple[str, ...] = ()
    blocking_refs: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class BranchAllocationProjection:
    allocation_id: str
    generated_at: str
    policy: AllocationPolicySurface
    parent_scope_type: str
    parent_scope_ref: str
    max_branches: int | None
    branch_budget_limit: int | None
    budget_remaining: int | None
    recursion_refused: bool = False
    stale_claim_receipt_ids: tuple[str, ...] = ()
    stale_return_delta_ids: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    selected_claims: tuple[BranchAllocationCandidate, ...] = ()
    deferred_claims: tuple[BranchAllocationCandidate, ...] = ()


class KernelAllocator:
    """Allocate bounded child branches under one committed parent work unit."""

    def __init__(self) -> None:
        self._scheduler = KernelScheduler()
        self._registry = KernelExecutorCapabilityRegistry()
        self._branch_controls = KernelBranchControlManager()

    def policy_surface(self) -> AllocationPolicySurface:
        return AllocationPolicySurface(
            policy_id="M1_ALLOCATOR_V1",
            notes=(
                "Only already-issued child work units under one committed parent may be allocated.",
                "Explicit capability matching outranks heuristic carrier choice where possible.",
                "Overlapping write claims remain illegal by default.",
                "Active branch claims consume effective executor capacity even before later settlement embodiment exists.",
            ),
        )

    def build_children_projection(
        self,
        index: KernelIndex,
        graph: KernelGraph,
        parent_work_unit_id: str,
        *,
        max_branches: int | None = None,
        generated_at: str | None = None,
    ) -> BranchAllocationProjection:
        parent = _resolve_parent(index, parent_work_unit_id)
        children = _child_work_units(index, parent_work_unit_id)
        if not children:
            raise KernelAllocatorError(
                f"No child work units are available under parent {parent_work_unit_id}"
            )

        timestamp = generated_at or _iso_now()
        posture = self._branch_controls.build_posture(
            index,
            parent_work_unit_id,
            generated_at=timestamp,
            max_branches=max_branches,
        )
        selected: list[BranchAllocationCandidate] = []
        deferred: list[BranchAllocationCandidate] = []
        claimed_writes: set[str] = set()
        active_claimed_branches = set(posture.active_branch_work_unit_ids)
        stale_claim_ids = set(posture.stale_claim_receipt_ids)
        effective_claims_by_capability: dict[str, int] = {}

        for child in _sorted_children(children):
            context_package = _resolve_context_package(index, child.context_package_id)
            branch_id = child.work_unit_id
            preferred_carrier = _infer_carrier(child.chassis, fallback=ScheduleCarrier.SWARM_CHILD)
            assessment = self._scheduler.assess_work_unit(index, graph, child.work_unit_id)
            blocking_refs = assessment.unresolved_dependencies + assessment.blocking_questions
            settlement_target = f"WORK_UNIT:{parent_work_unit_id}"
            requested_reads = (child.scope_ref,)
            default_reason = BranchAllocationReason.NOT_DISPATCHABLE
            selected_capability_id: str | None = None
            selected_executor_id: str | None = None
            capability_basis: tuple[str, ...] = ()
            warnings: tuple[str, ...] = ()
            binding_source = CarrierBindingSource.HEURISTIC_FALLBACK
            selected_carrier = preferred_carrier
            selected_flag = False
            reason = default_reason

            if child.work_unit_id in active_claimed_branches:
                reason = BranchAllocationReason.ALREADY_CLAIMED
            elif not assessment.dispatchable:
                reason = BranchAllocationReason.NOT_DISPATCHABLE
            else:
                selection = self._registry.select_capability(
                    index,
                    preferred_carrier=preferred_carrier,
                    scope_type=child.scope_type.value,
                    scope_ref=child.scope_ref,
                    domain=child.agent_domain,
                    executor_hint=child.agent_personal_name,
                )
                if selection.selected_capability is None:
                    reason = BranchAllocationReason.MISSING_CAPABILITY
                    warnings = selection.warnings
                    capability_basis = selection.capability_basis
                else:
                    capability = selection.selected_capability
                    capacity_remaining = self._capacity_remaining(
                        index,
                        capability,
                        effective_claims_by_capability,
                        ignored_claim_receipt_ids=stale_claim_ids,
                    )
                    if posture.recursion_refused:
                        reason = BranchAllocationReason.RECURSION_REFUSED
                    elif capacity_remaining <= 0:
                        reason = BranchAllocationReason.CAPACITY_EXHAUSTED
                    elif claimed_writes.intersection(child.allowed_writes):
                        reason = BranchAllocationReason.WRITE_CONFLICT
                    elif posture.branch_budget_limit is not None and len(selected) >= max(posture.budget_remaining or 0, 0):
                        reason = BranchAllocationReason.MAX_BRANCHES_REACHED
                    else:
                        selected_flag = True
                        reason = BranchAllocationReason.SELECTED
                        selected_capability_id = capability.capability_id
                        selected_executor_id = capability.executor_id
                        selected_carrier = capability.carrier
                        binding_source = CarrierBindingSource.EXECUTOR_CAPABILITY_REGISTRY
                        capability_basis = selection.capability_basis
                        warnings = selection.warnings
                        effective_claims_by_capability[capability.capability_id] = (
                            effective_claims_by_capability.get(capability.capability_id, 0) + 1
                        )
                        claimed_writes.update(child.allowed_writes)

            candidate = BranchAllocationCandidate(
                branch_id=branch_id,
                branch_work_unit_id=child.work_unit_id,
                context_package_id=child.context_package_id,
                branch_scope_type=child.scope_type.value,
                branch_scope_ref=child.scope_ref,
                branch_title=f"Allocate {child.scope_ref}",
                branch_objective=_context_objective(context_package),
                selected=selected_flag,
                reason=reason,
                priority=child.priority.value,
                selected_carrier=selected_carrier,
                carrier_binding_source=binding_source,
                selected_executor_id=selected_executor_id,
                selected_capability_id=selected_capability_id,
                allowed_writes=child.allowed_writes,
                requested_reads=requested_reads,
                expected_output=child.expected_output_schema,
                settlement_target=settlement_target,
                capability_basis=capability_basis,
                blocking_refs=blocking_refs,
                warnings=warnings,
            )
            if selected_flag:
                selected.append(candidate)
            else:
                deferred.append(candidate)

        allocation_id = branch_allocation_id(parent.scope_type.value, parent.work_unit_id, timestamp)
        return BranchAllocationProjection(
            allocation_id=allocation_id,
            generated_at=timestamp,
            policy=self.policy_surface(),
            parent_scope_type="WORK_UNIT",
            parent_scope_ref=parent.work_unit_id,
            max_branches=max_branches,
            branch_budget_limit=posture.branch_budget_limit,
            budget_remaining=posture.budget_remaining,
            recursion_refused=posture.recursion_refused,
            stale_claim_receipt_ids=posture.stale_claim_receipt_ids,
            stale_return_delta_ids=posture.stale_return_delta_ids,
            warnings=posture.warnings,
            selected_claims=tuple(selected),
            deferred_claims=tuple(deferred),
        )

    def render_projection(self, projection: BranchAllocationProjection) -> dict[str, object]:
        return {
            "allocation_id": projection.allocation_id,
            "generated_at": projection.generated_at,
            "policy_id": projection.policy.policy_id,
            "policy_notes": list(projection.policy.notes),
            "parent_scope_type": projection.parent_scope_type,
            "parent_scope_ref": projection.parent_scope_ref,
            "max_branches": projection.max_branches,
            "branch_budget_limit": projection.branch_budget_limit,
            "budget_remaining": projection.budget_remaining,
            "recursion_refused": projection.recursion_refused,
            "stale_claim_receipt_ids": list(projection.stale_claim_receipt_ids),
            "stale_return_delta_ids": list(projection.stale_return_delta_ids),
            "warnings": list(projection.warnings),
            "selected_claims": [_candidate_projection(item) for item in projection.selected_claims],
            "deferred_claims": [_candidate_projection(item) for item in projection.deferred_claims],
        }

    def persist_branch_claims(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        parent_work_unit_id: str,
        *,
        max_branches: int | None = None,
        created_at: str | None = None,
    ) -> tuple[BranchClaimReceipt, ...]:
        self._branch_controls.decay_stale_claims(
            store,
            index,
            parent_work_unit_id,
            generated_at=created_at,
        )
        projection = self.build_children_projection(
            index,
            graph,
            parent_work_unit_id,
            max_branches=max_branches,
            generated_at=created_at,
        )
        if not projection.selected_claims:
            raise KernelAllocatorError("No branch claims are available to persist.")

        receipts: list[BranchClaimReceipt] = []
        for claim in projection.selected_claims:
            if index.branch_claim_receipts_for_work_unit(claim.branch_work_unit_id):
                active = [
                    receipt
                    for receipt in index.branch_claim_receipts_for_work_unit(claim.branch_work_unit_id)
                    if receipt.claim_status is BranchClaimStatus.ACTIVE
                ]
                if active:
                    raise KernelAllocatorError(
                        f"Active branch claim already exists for {claim.branch_work_unit_id}"
                    )
            receipt = BranchClaimReceipt(
                receipt_id=branch_claim_receipt_id(
                    projection.parent_scope_type,
                    projection.parent_scope_ref,
                    claim.branch_id,
                    projection.generated_at,
                ),
                allocation_id=projection.allocation_id,
                created_at=projection.generated_at,
                claim_status=BranchClaimStatus.ACTIVE,
                parent_scope_type=projection.parent_scope_type,
                parent_scope_ref=projection.parent_scope_ref,
                branch_id=claim.branch_id,
                branch_work_unit_id=claim.branch_work_unit_id,
                context_package_id=claim.context_package_id,
                branch_scope_type=claim.branch_scope_type,
                branch_scope_ref=claim.branch_scope_ref,
                branch_title=claim.branch_title,
                branch_objective=claim.branch_objective,
                selected_carrier=claim.selected_carrier,
                carrier_binding_source=claim.carrier_binding_source,
                selected_executor_id=claim.selected_executor_id,
                selected_capability_id=claim.selected_capability_id,
                allowed_writes=claim.allowed_writes,
                requested_reads=claim.requested_reads,
                expected_output=claim.expected_output,
                settlement_target=claim.settlement_target,
                priority=claim.priority,
                capability_basis=claim.capability_basis,
                blocking_refs=claim.blocking_refs,
                warnings=claim.warnings,
            )
            store.create(receipt)
            index.record_added(receipt)
            receipts.append(receipt)
        return tuple(receipts)

    def latest_branch_claim_receipt(
        self,
        index: KernelIndex,
        parent_scope_type: str | None = None,
        parent_scope_ref: str | None = None,
    ) -> BranchClaimReceipt | None:
        normalized_scope = _normalize_scope_filter(parent_scope_type, parent_scope_ref)
        if normalized_scope is None:
            receipts = [
                record
                for record in index.records_by_type("branch_claim_receipt")
                if isinstance(record, BranchClaimReceipt)
            ]
        else:
            receipts = index.branch_claim_receipts_for_parent(normalized_scope[0], normalized_scope[1])
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_branch_claim_receipt_projection(
        self,
        receipt: BranchClaimReceipt | None,
    ) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "allocation_id": receipt.allocation_id,
            "created_at": receipt.created_at,
            "claim_status": receipt.claim_status.value,
            "parent_scope_type": receipt.parent_scope_type,
            "parent_scope_ref": receipt.parent_scope_ref,
            "branch_id": receipt.branch_id,
            "branch_work_unit_id": receipt.branch_work_unit_id,
            "context_package_id": receipt.context_package_id,
            "branch_scope_type": receipt.branch_scope_type,
            "branch_scope_ref": receipt.branch_scope_ref,
            "branch_title": receipt.branch_title,
            "branch_objective": receipt.branch_objective,
            "selected_carrier": receipt.selected_carrier.value,
            "carrier_binding_source": receipt.carrier_binding_source.value,
            "selected_executor_id": receipt.selected_executor_id,
            "selected_capability_id": receipt.selected_capability_id,
            "allowed_writes": list(receipt.allowed_writes),
            "requested_reads": list(receipt.requested_reads),
            "expected_output": receipt.expected_output,
            "settlement_target": receipt.settlement_target,
            "priority": receipt.priority,
            "capability_basis": list(receipt.capability_basis),
            "blocking_refs": list(receipt.blocking_refs),
            "warnings": list(receipt.warnings),
        }

    def _capacity_remaining(
        self,
        index: KernelIndex,
        capability: ExecutorCapability,
        effective_claims_by_capability: dict[str, int],
        *,
        ignored_claim_receipt_ids: set[str] | None = None,
    ) -> int:
        ignored_claim_receipt_ids = ignored_claim_receipt_ids or set()
        active_receipts = [
            receipt
            for receipt in index.branch_claim_receipts_for_capability(capability.capability_id)
            if receipt.claim_status is BranchClaimStatus.ACTIVE and receipt.receipt_id not in ignored_claim_receipt_ids
        ]
        consumed = capability.active_assignments + len(active_receipts) + effective_claims_by_capability.get(
            capability.capability_id,
            0,
        )
        return capability.max_concurrency - consumed


def branch_allocation_id(parent_scope_type: str, parent_scope_ref: str, created_at: str) -> str:
    return f"branch-allocation-{_slug(parent_scope_type)}-{_slug(parent_scope_ref)}-{_slug(created_at)}"


def branch_claim_receipt_id(parent_scope_type: str, parent_scope_ref: str, branch_id: str, created_at: str) -> str:
    return (
        f"branch-claim-{_slug(parent_scope_type)}-{_slug(parent_scope_ref)}-"
        f"{_slug(branch_id)}-{_slug(created_at)}"
    )


def _resolve_parent(index: KernelIndex, parent_work_unit_id: str) -> WorkUnit:
    record = index.get("work_unit", parent_work_unit_id)
    if not isinstance(record, WorkUnit):
        raise KernelAllocatorError(f"Unknown parent work unit: {parent_work_unit_id}")
    if record.status is not WorkUnitStatus.COMMITTED:
        raise KernelAllocatorError(
            f"Parent work unit must be COMMITTED for bounded allocation: {parent_work_unit_id}"
        )
    return record


def _child_work_units(index: KernelIndex, parent_work_unit_id: str) -> list[WorkUnit]:
    return index.child_work_units_for_parent(parent_work_unit_id)


def _sorted_children(children: list[WorkUnit]) -> list[WorkUnit]:
    return sorted(
        children,
        key=lambda item: (
            _priority_rank(item.priority.value),
            item.created_at,
            item.work_unit_id,
        ),
    )


def _resolve_context_package(index: KernelIndex, context_package_id: str) -> ContextPackage:
    record = index.get("context_package", context_package_id)
    if not isinstance(record, ContextPackage):
        raise KernelAllocatorError(f"Unknown child context package: {context_package_id}")
    return record


def _context_objective(context_package: ContextPackage) -> str:
    return context_package.tiers.tier_3_mission.objective


def _priority_rank(value: str) -> int:
    order = {
        "P0_CRITICAL": 0,
        "P1_HIGH": 1,
        "P2_NORMAL": 2,
        "P3_LOW": 3,
    }
    return order.get(value, 3)


def _infer_carrier(text: str | None, *, fallback: ScheduleCarrier) -> ScheduleCarrier:
    if text is None:
        return fallback
    lowered = text.lower()
    if any(token in lowered for token in ("daemon", "runtime", "service")):
        return ScheduleCarrier.SUPERVISED_RUNTIME
    if any(token in lowered for token in ("api", "external", "mcp")):
        return ScheduleCarrier.EXTERNAL_API
    if any(token in lowered for token in ("swarm", "child")):
        return ScheduleCarrier.SWARM_CHILD
    # Historical carrier compatibility: older Codex executor hints still map to IDE-manual routing.
    if any(token in lowered for token in ("ide", "cursor", "codex", "executor", "manual")):
        return ScheduleCarrier.IDE_MANUAL
    return fallback


def _candidate_projection(candidate: BranchAllocationCandidate) -> dict[str, object]:
    return {
        "branch_id": candidate.branch_id,
        "branch_work_unit_id": candidate.branch_work_unit_id,
        "context_package_id": candidate.context_package_id,
        "branch_scope_type": candidate.branch_scope_type,
        "branch_scope_ref": candidate.branch_scope_ref,
        "branch_title": candidate.branch_title,
        "branch_objective": candidate.branch_objective,
        "selected": candidate.selected,
        "reason": candidate.reason,
        "priority": candidate.priority,
        "selected_carrier": candidate.selected_carrier.value,
        "carrier_binding_source": candidate.carrier_binding_source.value,
        "selected_executor_id": candidate.selected_executor_id,
        "selected_capability_id": candidate.selected_capability_id,
        "allowed_writes": list(candidate.allowed_writes),
        "requested_reads": list(candidate.requested_reads),
        "expected_output": candidate.expected_output,
        "settlement_target": candidate.settlement_target,
        "capability_basis": list(candidate.capability_basis),
        "blocking_refs": list(candidate.blocking_refs),
        "warnings": list(candidate.warnings),
    }


def _normalize_scope_filter(scope_type: str | None, scope_ref: str | None) -> tuple[str, str] | None:
    if scope_type is None and scope_ref is None:
        return None
    if not scope_type or not scope_ref:
        raise KernelAllocatorError("parent_scope_type and parent_scope_ref must be provided together.")
    return scope_type.strip().upper(), scope_ref.strip()


def _slug(value: str) -> str:
    return compact_identifier(value, empty="value", max_length=40)


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
