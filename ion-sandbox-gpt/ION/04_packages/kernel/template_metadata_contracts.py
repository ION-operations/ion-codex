"""Template Metadata Contract validation utilities.

V14 is a conservative, dependency-free validator for machine-readable template
metadata contracts. It is intentionally not a YAML parser; callers pass contract
dictionaries, while registry files remain readable seed surfaces.

The validator performs schema checks only. It does not mutate registries,
templates, graph state, or source files.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


ACTIVE_CONTRACT = "ACTIVE_CONTRACT"
PROVISIONAL_CONTRACT = "PROVISIONAL_CONTRACT"
DRAFT_CONTRACT = "DRAFT_CONTRACT"
NO_CONTRACT = "NO_CONTRACT"
RETIRED_CONTRACT = "RETIRED_CONTRACT"
QUARANTINED_CONTRACT = "QUARANTINED_CONTRACT"

EVENTING_ALLOWED_STATUSES = {ACTIVE_CONTRACT, PROVISIONAL_CONTRACT}

REQUIRED_CONTRACT_FIELDS = (
    "template_id",
    "canonical_name",
    "version",
    "contract_status",
    "file_class",
    "graph_node_type",
    "graph_region",
    "authority_class",
    "lifecycle",
    "required_fields",
    "completion_threshold",
    "downstream_effects",
    "reaction_hooks",
    "review",
    "receipts",
    "safety",
)

REQUIRED_LIFECYCLE_FIELDS = ("allowed_statuses", "complete_statuses")
REQUIRED_COMPLETION_FIELDS = ("mode", "required_fields")
REQUIRED_DOWNSTREAM_FIELDS = ("allowed", "forbidden")
REQUIRED_RECEIPT_FIELDS = ("receipt_required",)
REQUIRED_SAFETY_FIELDS = ("escalation_behavior",)


@dataclass(frozen=True)
class TemplateContractValidationResult:
    valid: bool
    allows_eventing: bool
    missing_fields: tuple[str, ...] = ()
    blocked_reason: str = ""


def _missing(mapping: Mapping[str, Any], fields: Sequence[str], prefix: str = "") -> list[str]:
    missing: list[str] = []
    for field in fields:
        if field not in mapping or mapping[field] in (None, ""):
            missing.append(f"{prefix}{field}")
    return missing


def validate_template_metadata_contract(contract: Mapping[str, Any]) -> TemplateContractValidationResult:
    """Validate a template metadata contract dictionary.

    This is a structural validator, not a ratifier. A valid contract may still
    require review before use.
    """

    missing = _missing(contract, REQUIRED_CONTRACT_FIELDS)

    lifecycle = contract.get("lifecycle")
    if isinstance(lifecycle, Mapping):
        missing.extend(_missing(lifecycle, REQUIRED_LIFECYCLE_FIELDS, "lifecycle."))
    else:
        missing.append("lifecycle")

    completion = contract.get("completion_threshold")
    if isinstance(completion, Mapping):
        missing.extend(_missing(completion, REQUIRED_COMPLETION_FIELDS, "completion_threshold."))
    else:
        missing.append("completion_threshold")

    downstream = contract.get("downstream_effects")
    if isinstance(downstream, Mapping):
        missing.extend(_missing(downstream, REQUIRED_DOWNSTREAM_FIELDS, "downstream_effects."))
    else:
        missing.append("downstream_effects")

    receipts = contract.get("receipts")
    if isinstance(receipts, Mapping):
        missing.extend(_missing(receipts, REQUIRED_RECEIPT_FIELDS, "receipts."))
    else:
        missing.append("receipts")

    safety = contract.get("safety")
    if isinstance(safety, Mapping):
        missing.extend(_missing(safety, REQUIRED_SAFETY_FIELDS, "safety."))
    else:
        missing.append("safety")

    if missing:
        return TemplateContractValidationResult(
            valid=False,
            allows_eventing=False,
            missing_fields=tuple(sorted(set(missing))),
            blocked_reason="MISSING_REQUIRED_FIELDS",
        )

    status = str(contract.get("contract_status"))
    allows_eventing = status in EVENTING_ALLOWED_STATUSES
    if not allows_eventing:
        return TemplateContractValidationResult(
            valid=True,
            allows_eventing=False,
            blocked_reason=f"CONTRACT_STATUS_BLOCKS_EVENTING:{status}",
        )

    return TemplateContractValidationResult(valid=True, allows_eventing=True)


def contract_allows_reaction(contract: Mapping[str, Any], reaction: str) -> bool:
    downstream = contract.get("downstream_effects", {})
    if not isinstance(downstream, Mapping):
        return False
    allowed = set(downstream.get("allowed", []) or [])
    forbidden = set(downstream.get("forbidden", []) or [])
    return reaction in allowed and reaction not in forbidden


def contract_requires_review(contract: Mapping[str, Any]) -> bool:
    review = contract.get("review", {})
    if not isinstance(review, Mapping):
        return True
    return bool(review.get("approval_required", True))
