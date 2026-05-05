"""Bind fleet lifecycle witness into executor capability registry (Target 2 / Slice 2).

This is a *bridge* module: it does not import swarm behavior or mission control.
It takes factual fleet membership state and materializes explicit ExecutorCapability
records so scheduler surfaces can select executors without hidden heuristics.

Key boundary:
- fleet lifecycle describes *member existence and member state*
- capability registry describes *what an executor can do and whether it is selectable*
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid

from .executor_registry import KernelExecutorCapabilityRegistry
from .index import KernelIndex
from .model import (
    ExecutorAvailability,
    ExecutorCapability,
    ExecutorTrustClass,
    FallbackSuitability,
    ScheduleCarrier,
)
from .store import KernelStore
from .fleet_lifecycle_store import FleetLifecycleStore, FleetMemberState


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class FleetCapabilityBindingError(Exception):
    """Raised when one fleet-to-capability binding operation fails."""


@dataclass(frozen=True)
class FleetCapabilitySyncReceipt:
    receipt_id: str
    fleet_id: str
    generated_at: str
    total_members: int
    active_members: int
    added_count: int
    updated_count: int
    updated_capability_ids: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


_STATE_TO_AVAILABILITY = {
    FleetMemberState.BOOTING: ExecutorAvailability.DEGRADED,
    FleetMemberState.ACTIVE: ExecutorAvailability.AVAILABLE,
    FleetMemberState.SUSPENDED: ExecutorAvailability.DRAINED,
    FleetMemberState.TERMINATED: ExecutorAvailability.UNAVAILABLE,
}


class FleetExecutorCapabilityBinder:
    """Materialize ExecutorCapability records from fleet membership witness."""

    def __init__(self, *, registry: KernelExecutorCapabilityRegistry | None = None) -> None:
        self.registry = registry or KernelExecutorCapabilityRegistry()

    def sync_fleet(
        self,
        *,
        fleet_store: FleetLifecycleStore,
        kernel_store: KernelStore,
        kernel_index: KernelIndex,
        fleet_id: str,
        carrier: ScheduleCarrier = ScheduleCarrier.SUPERVISED_RUNTIME,
        trust_class: ExecutorTrustClass = ExecutorTrustClass.SUPERVISED_AUTOMATION,
        max_concurrency: int = 1,
        supported_scope_types: tuple[str, ...] = (),
        domain_fitness: tuple[str, ...] = (),
        supported_packet_families: tuple[str, ...] = (),
        fallback_suitability: FallbackSuitability = FallbackSuitability.PRIMARY,
        notes: str | None = None,
    ) -> FleetCapabilitySyncReceipt:
        # Validate fleet exists.
        fleet_store.read_fleet(fleet_id)

        members = fleet_store.list_members(fleet_id=fleet_id)
        total = len(members)
        active = sum(1 for m in members if m.state == FleetMemberState.ACTIVE)

        added = 0
        updated = 0
        updated_ids: list[str] = []
        warnings: list[str] = []
        now = _utc_now()

        for member in members:
            capability_id = f"cap-{member.member_id}"
            availability = _STATE_TO_AVAILABILITY.get(member.state, ExecutorAvailability.UNAVAILABLE)
            existing = (
                kernel_index.get("executor_capability", capability_id)
                if kernel_index.exists("executor_capability", capability_id)
                else None
            )
            created_at = existing.created_at if isinstance(existing, ExecutorCapability) else now

            structural_identity = member.authority_class or "FLEET_MEMBER"
            role = "EXECUTOR"
            personal_name = member.callsign

            capability = ExecutorCapability(
                capability_id=capability_id,
                executor_id=member.member_id,
                created_at=created_at,
                updated_at=now,
                personal_name=personal_name,
                role=role,
                structural_identity=structural_identity,
                carrier=carrier,
                trust_class=trust_class,
                availability=availability,
                max_concurrency=max_concurrency,
                active_assignments=0,
                supported_scope_types=supported_scope_types,
                domain_fitness=domain_fitness,
                supported_packet_families=supported_packet_families,
                fallback_suitability=fallback_suitability,
                aliases=(),
                side_effect_constraints=(),
                notes=notes,
            )

            # Register via capability registry to keep index/store consistent.
            prior_exists = kernel_index.exists("executor_capability", capability.capability_id)
            self.registry.register(kernel_store, kernel_index, capability)
            if prior_exists:
                updated += 1
            else:
                added += 1
            updated_ids.append(capability.capability_id)

        if total == 0:
            warnings.append("No fleet members found to bind into capability registry.")

        return FleetCapabilitySyncReceipt(
            receipt_id=f"fcs-{uuid.uuid4().hex[:12]}",
            fleet_id=fleet_id,
            generated_at=now,
            total_members=total,
            active_members=active,
            added_count=added,
            updated_count=updated,
            updated_capability_ids=tuple(updated_ids),
            warnings=tuple(warnings),
        )
