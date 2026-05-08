"""L1 executor capability registry surfaces for the active ION kernel stack.

This module makes executor and carrier choice explicit and queryable. It does not
replace scheduler law; it gives the scheduler a first principled basis for selecting
an executor/carrier without hardening string heuristics into hidden policy.
"""

from __future__ import annotations

from dataclasses import dataclass

from .index import KernelIndex
from .model import (
    ExecutorAvailability,
    ExecutorCapability,
    ExecutorTrustClass,
    FallbackSuitability,
    ScheduleCarrier,
)
from .store import KernelStore


class KernelExecutorCapabilityError(Exception):
    """Raised when one executor-capability operation cannot be completed."""


@dataclass(frozen=True)
class ExecutorCapabilitySelection:
    selected_capability: ExecutorCapability | None
    registry_count: int
    eligible_count: int
    capability_basis: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutorCapabilitySnapshot:
    total_capabilities: int
    available_capabilities: int
    by_carrier: dict[str, int]
    by_availability: dict[str, int]
    by_trust_class: dict[str, int]
    capabilities: tuple[ExecutorCapability, ...]


_ACTIVE_AVAILABILITY = frozenset(
    {
        ExecutorAvailability.AVAILABLE,
        ExecutorAvailability.DEGRADED,
    }
)

_AVAILABILITY_ORDER = {
    ExecutorAvailability.AVAILABLE: 0,
    ExecutorAvailability.DEGRADED: 1,
    ExecutorAvailability.DRAINED: 2,
    ExecutorAvailability.UNAVAILABLE: 3,
}

_TRUST_ORDER = {
    ExecutorTrustClass.HUMAN_SUPERVISED: 0,
    ExecutorTrustClass.SUPERVISED_AUTOMATION: 1,
    ExecutorTrustClass.EXTERNAL_VERIFIED: 2,
    ExecutorTrustClass.EXPERIMENTAL: 3,
}

_FALLBACK_ORDER = {
    FallbackSuitability.PRIMARY: 0,
    FallbackSuitability.FALLBACK_ONLY: 1,
    FallbackSuitability.UNSUITABLE: 2,
}


class KernelExecutorCapabilityRegistry:
    """Persist, query, and select explicit executor capability records."""

    def register(
        self,
        store: KernelStore,
        index: KernelIndex,
        capability: ExecutorCapability,
    ) -> ExecutorCapability:
        if index.exists("executor_capability", capability.capability_id):
            store.replace(capability)
            index.record_changed(capability)
        else:
            store.create(capability)
            index.record_added(capability)
        return capability

    def capabilities(
        self,
        index: KernelIndex,
        *,
        include_inactive: bool = True,
    ) -> list[ExecutorCapability]:
        records = [
            record
            for record in index.records_by_type("executor_capability")
            if isinstance(record, ExecutorCapability)
        ]
        if not include_inactive:
            records = [record for record in records if record.availability in _ACTIVE_AVAILABILITY]
        return sorted(records, key=self._capability_sort_key)

    def build_snapshot(
        self,
        index: KernelIndex,
        *,
        include_inactive: bool = True,
    ) -> ExecutorCapabilitySnapshot:
        capabilities = self.capabilities(index, include_inactive=include_inactive)
        by_carrier: dict[str, int] = {}
        by_availability: dict[str, int] = {}
        by_trust_class: dict[str, int] = {}
        available_capabilities = 0

        for capability in capabilities:
            by_carrier[capability.carrier.value] = by_carrier.get(capability.carrier.value, 0) + 1
            by_availability[capability.availability.value] = (
                by_availability.get(capability.availability.value, 0) + 1
            )
            by_trust_class[capability.trust_class.value] = (
                by_trust_class.get(capability.trust_class.value, 0) + 1
            )
            if capability.availability in _ACTIVE_AVAILABILITY and capability.has_capacity():
                available_capabilities += 1

        return ExecutorCapabilitySnapshot(
            total_capabilities=len(capabilities),
            available_capabilities=available_capabilities,
            by_carrier=by_carrier,
            by_availability=by_availability,
            by_trust_class=by_trust_class,
            capabilities=tuple(capabilities),
        )

    def render_snapshot(self, snapshot: ExecutorCapabilitySnapshot) -> dict[str, object]:
        return {
            "total_capabilities": snapshot.total_capabilities,
            "available_capabilities": snapshot.available_capabilities,
            "by_carrier": dict(sorted(snapshot.by_carrier.items())),
            "by_availability": dict(sorted(snapshot.by_availability.items())),
            "by_trust_class": dict(sorted(snapshot.by_trust_class.items())),
            "capabilities": [self.render_capability(item) for item in snapshot.capabilities],
        }

    def render_capability(self, capability: ExecutorCapability) -> dict[str, object]:
        return {
            "capability_id": capability.capability_id,
            "executor_id": capability.executor_id,
            "created_at": capability.created_at,
            "updated_at": capability.updated_at,
            "personal_name": capability.personal_name,
            "role": capability.role,
            "structural_identity": capability.structural_identity,
            "carrier": capability.carrier.value,
            "trust_class": capability.trust_class.value,
            "availability": capability.availability.value,
            "max_concurrency": capability.max_concurrency,
            "active_assignments": capability.active_assignments,
            "supported_scope_types": list(capability.supported_scope_types),
            "domain_fitness": list(capability.domain_fitness),
            "supported_packet_families": list(capability.supported_packet_families),
            "fallback_suitability": capability.fallback_suitability.value,
            "aliases": list(capability.aliases),
            "side_effect_constraints": list(capability.side_effect_constraints),
            "notes": capability.notes,
        }

    def select_capability(
        self,
        index: KernelIndex,
        *,
        preferred_carrier: ScheduleCarrier,
        scope_type: str,
        scope_ref: str,
        domain: str | None = None,
        executor_hint: str | None = None,
        packet_family: str | None = None,
    ) -> ExecutorCapabilitySelection:
        registry = self.capabilities(index)
        eligible = [
            capability
            for capability in registry
            if self._is_eligible(
                capability,
                scope_type=scope_type,
                packet_family=packet_family,
            )
        ]
        if not eligible:
            return ExecutorCapabilitySelection(
                selected_capability=None,
                registry_count=len(registry),
                eligible_count=0,
                warnings=self._no_match_warnings(registry),
            )

        selected = min(
            eligible,
            key=lambda capability: self._selection_key(
                capability,
                preferred_carrier=preferred_carrier,
                scope_ref=scope_ref,
                domain=domain,
                executor_hint=executor_hint,
            ),
        )
        return ExecutorCapabilitySelection(
            selected_capability=selected,
            registry_count=len(registry),
            eligible_count=len(eligible),
            capability_basis=self._selection_basis(
                selected,
                preferred_carrier=preferred_carrier,
                scope_ref=scope_ref,
                domain=domain,
                executor_hint=executor_hint,
            ),
            warnings=(
                ()
                if selected.side_effect_constraints
                else ()
            ),
        )

    def _is_eligible(
        self,
        capability: ExecutorCapability,
        *,
        scope_type: str,
        packet_family: str | None,
    ) -> bool:
        return (
            capability.availability in _ACTIVE_AVAILABILITY
            and capability.has_capacity()
            and capability.supports_scope_type(scope_type)
            and capability.supports_packet_family(packet_family)
        )

    def _selection_key(
        self,
        capability: ExecutorCapability,
        *,
        preferred_carrier: ScheduleCarrier,
        scope_ref: str,
        domain: str | None,
        executor_hint: str | None,
    ) -> tuple[int, int, int, int, int, int, str]:
        carrier_rank = 0 if capability.carrier is preferred_carrier else 1
        hint_rank = self._hint_rank(capability, executor_hint)
        domain_rank = self._domain_rank(capability, domain, scope_ref)
        availability_rank = _AVAILABILITY_ORDER[capability.availability]
        fallback_rank = 0 if capability.carrier is preferred_carrier else _FALLBACK_ORDER[capability.fallback_suitability]
        trust_rank = _TRUST_ORDER[capability.trust_class]
        return (
            carrier_rank,
            hint_rank,
            domain_rank,
            availability_rank,
            fallback_rank,
            capability.active_assignments,
            capability.executor_id,
        )

    def _selection_basis(
        self,
        capability: ExecutorCapability,
        *,
        preferred_carrier: ScheduleCarrier,
        scope_ref: str,
        domain: str | None,
        executor_hint: str | None,
    ) -> tuple[str, ...]:
        basis = [
            f"selected capability {capability.capability_id} for executor {capability.executor_id}",
            f"carrier {capability.carrier.value} is bound through the executor capability registry",
            f"availability {capability.availability.value} with concurrency {capability.active_assignments}/{capability.max_concurrency}",
            f"trust class {capability.trust_class.value}",
        ]
        if capability.carrier is preferred_carrier:
            basis.append(f"preferred carrier {preferred_carrier.value} matched directly")
        if self._hint_rank(capability, executor_hint) == 0:
            basis.append("executor hint matched the registered executor identity or alias")
        if self._domain_rank(capability, domain, scope_ref) == 0:
            basis.append("scope or domain fit matched the registered capability")
        if capability.side_effect_constraints:
            basis.append(
                "side-effect constraints: " + ", ".join(capability.side_effect_constraints)
            )
        return tuple(basis)

    def _hint_rank(self, capability: ExecutorCapability, executor_hint: str | None) -> int:
        if not executor_hint:
            return 1
        normalized_hint = executor_hint.strip().lower()
        aliases = {
            capability.executor_id.lower(),
            capability.personal_name.lower(),
            capability.role.lower(),
            capability.structural_identity.lower(),
            *{item.lower() for item in capability.aliases},
        }
        return 0 if any(alias and alias in normalized_hint for alias in aliases) else 1

    def _domain_rank(
        self,
        capability: ExecutorCapability,
        domain: str | None,
        scope_ref: str,
    ) -> int:
        if not capability.domain_fitness:
            return 1
        normalized_domain = (domain or "").strip().lower()
        normalized_scope_ref = scope_ref.strip().lower()
        for item in capability.domain_fitness:
            normalized_item = item.strip().lower()
            if normalized_item and (
                normalized_item == normalized_domain
                or normalized_item in normalized_scope_ref
            ):
                return 0
        return 2

    def _no_match_warnings(self, registry: list[ExecutorCapability]) -> tuple[str, ...]:
        if not registry:
            return ("No executor capability records are registered; carrier binding remains heuristic.",)
        return (
            "No eligible executor capability matched this candidate; carrier binding fell back to the prior heuristic.",
        )

    def _capability_sort_key(self, capability: ExecutorCapability) -> tuple[int, int, str, str]:
        return (
            _AVAILABILITY_ORDER[capability.availability],
            _TRUST_ORDER[capability.trust_class],
            capability.executor_id,
            capability.capability_id,
        )
