"""Contract-bound event runtime gates.

V15 introduces conservative helpers that bind the first two evented-template-file
graph phases to template metadata contracts.

The module is read-only: it does not mutate graph state, registries, schedules,
source files, or agents. It returns classification dictionaries that existing
or future event runtime callers can persist as witnesses/receipts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .template_metadata_contracts import (
    TemplateContractValidationResult,
    contract_allows_reaction,
    contract_requires_review,
    validate_template_metadata_contract,
)


@dataclass(frozen=True)
class ContractBoundCompletionGate:
    template_id: str
    allowed: bool
    witness_class: str
    blocked_reason: str = ""
    contract_status: str = ""
    missing_fields: tuple[str, ...] = ()


@dataclass(frozen=True)
class ContractBoundReactionGate:
    template_id: str
    reaction: str
    selected: bool
    witness_class: str
    blocked_reason: str = ""
    requires_review: bool = True


def gate_template_completion_by_contract(
    template_id: str,
    contracts_by_template_id: Mapping[str, Mapping[str, Any]],
) -> ContractBoundCompletionGate:
    """Return whether a template may emit a completion-event witness.

    Missing or inactive contracts block eventing. A structurally invalid contract
    also blocks eventing and exposes missing fields.
    """

    contract = contracts_by_template_id.get(template_id)
    if contract is None:
        return ContractBoundCompletionGate(
            template_id=template_id,
            allowed=False,
            witness_class="CONTRACT_BLOCKED_TEMPLATE_COMPLETION_EVENT",
            blocked_reason="MISSING_TEMPLATE_METADATA_CONTRACT",
        )

    validation = validate_template_metadata_contract(contract)
    status = str(contract.get("contract_status", ""))
    if not validation.valid:
        return ContractBoundCompletionGate(
            template_id=template_id,
            allowed=False,
            witness_class="CONTRACT_BLOCKED_TEMPLATE_COMPLETION_EVENT",
            blocked_reason=validation.blocked_reason or "INVALID_TEMPLATE_METADATA_CONTRACT",
            contract_status=status,
            missing_fields=validation.missing_fields,
        )

    if not validation.allows_eventing:
        return ContractBoundCompletionGate(
            template_id=template_id,
            allowed=False,
            witness_class="CONTRACT_BLOCKED_TEMPLATE_COMPLETION_EVENT",
            blocked_reason=validation.blocked_reason or "CONTRACT_STATUS_BLOCKS_EVENTING",
            contract_status=status,
        )

    return ContractBoundCompletionGate(
        template_id=template_id,
        allowed=True,
        witness_class="CONTRACT_BOUND_TEMPLATE_COMPLETION_EVENT",
        contract_status=status,
    )


def gate_reaction_selection_by_contract(
    template_id: str,
    reaction: str,
    contracts_by_template_id: Mapping[str, Mapping[str, Any]],
) -> ContractBoundReactionGate:
    """Return whether a reaction may be selected for a template event.

    This only selects/defer-classifies reactions. It does not execute them.
    """

    completion_gate = gate_template_completion_by_contract(template_id, contracts_by_template_id)
    if not completion_gate.allowed:
        return ContractBoundReactionGate(
            template_id=template_id,
            reaction=reaction,
            selected=False,
            witness_class="CONTRACT_BLOCKED_REACTION_SELECTION",
            blocked_reason=completion_gate.blocked_reason,
            requires_review=True,
        )

    contract = contracts_by_template_id[template_id]
    if not contract_allows_reaction(contract, reaction):
        return ContractBoundReactionGate(
            template_id=template_id,
            reaction=reaction,
            selected=False,
            witness_class="CONTRACT_BLOCKED_REACTION_SELECTION",
            blocked_reason="REACTION_NOT_DECLARED_ALLOWED_OR_FORBIDDEN",
            requires_review=contract_requires_review(contract),
        )

    return ContractBoundReactionGate(
        template_id=template_id,
        reaction=reaction,
        selected=True,
        witness_class="CONTRACT_BOUND_REACTION_SELECTION",
        requires_review=contract_requires_review(contract),
    )


def build_contract_bound_event_witness(
    source_file: str,
    template_id: str,
    contracts_by_template_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Build a serializable Phase-1-style contract-bound witness."""

    gate = gate_template_completion_by_contract(template_id, contracts_by_template_id)
    return {
        "witness_class": gate.witness_class,
        "source_file": source_file,
        "template_id": template_id,
        "allowed": gate.allowed,
        "blocked_reason": gate.blocked_reason,
        "contract_status": gate.contract_status,
        "missing_fields": list(gate.missing_fields),
        "mutation_allowed": False,
    }


def build_contract_bound_reaction_witness(
    template_id: str,
    reaction: str,
    contracts_by_template_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Build a serializable Phase-2-style contract-bound reaction witness."""

    gate = gate_reaction_selection_by_contract(template_id, reaction, contracts_by_template_id)
    return {
        "witness_class": gate.witness_class,
        "template_id": template_id,
        "reaction": reaction,
        "selected": gate.selected,
        "blocked_reason": gate.blocked_reason,
        "requires_review": gate.requires_review,
        "mutation_allowed": False,
    }
