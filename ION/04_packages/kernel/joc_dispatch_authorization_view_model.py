"""V61 JOC dispatch authorization governor verdict view model.

This module is deliberately projection-only. It does not dispatch missions,
call providers, mutate browser sessions, access credentials, or spend budget.
It binds a V59-style mission route preview to budget/API/capability governor
verdicts and emits an operator-visible authorization view model.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Iterable, List, Literal

VERSION = "V61_DISPATCH_AUTHORIZATION_GOVERNOR_VERDICT_VIEW_MODEL"
AUTHORITY_SCOPE = "DISPATCH_AUTHORIZATION_VIEW_MODEL_RECEIPT_ONLY"

AuthorizationVerdict = Literal[
    "AUTHORIZATION_PREVIEW_READY",
    "NEEDS_SUPERVISED_APPROVAL",
    "BLOCKED_BY_BUDGET",
    "BLOCKED_BY_API_RATE_LIMIT",
    "BLOCKED_BY_FORBIDDEN_CAPABILITY",
    "BLOCKED_BY_MISSING_GOVERNOR_EVIDENCE",
    "BLOCKED_BY_CLAIM_REVIEW",
    "BLOCKED_BY_PRODUCTION_BOUNDARY",
]

ApprovalMode = Literal[
    "AUTO_FORBIDDEN",
    "SUPERVISED_REQUIRED",
    "MANUAL_ONLY",
    "VIEW_ONLY_BLOCKED",
]

BLOCKING_BUDGET_VERDICTS = {
    "BUDGET_BLOCKED",
    "MONTHLY_BUDGET_EXCEEDED",
    "MISSION_BUDGET_EXCEEDED",
}

BLOCKING_API_RATE_VERDICTS = {
    "RATE_LIMIT_BLOCKED",
    "PROVIDER_QUOTA_EXHAUSTED",
    "PARALLELISM_LIMIT_EXCEEDED",
}

BLOCKING_CAPABILITY_VERDICTS = {
    "FORBIDDEN_CAPABILITY",
    "CREDENTIAL_REQUIRED",
    "DESTRUCTIVE_ACTION",
    "PAID_CLOUD_REQUIRES_MANUAL_APPROVAL",
}

AUTO_FORBIDDEN_CAPABILITIES = {
    "credential_vault",
    "settings_mutation",
    "destructive_browser_action",
    "paid_cloud_launch",
    "source_summary_rewrite",
    "canonical_graph_write",
    "unrestricted_agent_activation",
}


@dataclass(frozen=True)
class DispatchAuthorizationInput:
    mission_id: str
    route_preview_id: str
    selected_target: str
    compute_ring: str
    access_method: str
    task_class: str
    claim_lane: str
    estimated_cost_usd: float
    estimated_latency_band: str
    quality_band: str
    budget_governor_verdict: str
    api_rate_governor_verdict: str
    capability_policy_verdict: str
    evidence_refs: List[str]
    blocked_capabilities: List[str] = field(default_factory=list)
    route_factors: List[str] = field(default_factory=list)
    production_boundary: bool = False


@dataclass(frozen=True)
class DispatchAuthorizationViewModel:
    version: str
    mission_id: str
    route_preview_id: str
    selected_target: str
    compute_ring: str
    access_method: str
    task_class: str
    claim_lane: str
    authorization_verdict: AuthorizationVerdict
    authority_scope: str
    approval_mode: ApprovalMode
    budget_governor_verdict: str
    api_rate_governor_verdict: str
    capability_policy_verdict: str
    estimated_cost_usd: float
    estimated_latency_band: str
    quality_band: str
    blocked_capabilities: List[str]
    route_factors: List[str]
    evidence_refs: List[str]
    operator_reason: str
    next_required_action: str
    dispatch_receipt_preview: Dict[str, Any]
    production_authority: bool = False
    live_dispatch_claim: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _missing_required(value: Any) -> bool:
    return value is None or value == "" or value == []


def _has_auto_forbidden_capability(blocked_capabilities: Iterable[str]) -> bool:
    return bool(AUTO_FORBIDDEN_CAPABILITIES.intersection(set(blocked_capabilities)))


def build_dispatch_authorization_view_model(
    data: DispatchAuthorizationInput | Dict[str, Any]
) -> DispatchAuthorizationViewModel:
    """Build a projection-only dispatch authorization view model.

    The function accepts a dataclass or dict to make it easy for UI tests,
    CLI harnesses, and future kernel callers to bind route/governor evidence.
    """

    if isinstance(data, dict):
        data = DispatchAuthorizationInput(**data)

    missing = [
        name
        for name in (
            "mission_id",
            "route_preview_id",
            "selected_target",
            "compute_ring",
            "access_method",
            "task_class",
            "claim_lane",
            "budget_governor_verdict",
            "api_rate_governor_verdict",
            "capability_policy_verdict",
            "evidence_refs",
        )
        if _missing_required(getattr(data, name))
    ]

    if missing:
        verdict: AuthorizationVerdict = "BLOCKED_BY_MISSING_GOVERNOR_EVIDENCE"
        approval: ApprovalMode = "VIEW_ONLY_BLOCKED"
        reason = f"Missing required governor evidence: {', '.join(missing)}."
        next_action = "Attach missing route/governor evidence before requesting approval."
    elif data.production_boundary:
        verdict = "BLOCKED_BY_PRODUCTION_BOUNDARY"
        approval = "VIEW_ONLY_BLOCKED"
        reason = "Route would cross a production boundary that V61 is not authorized to execute."
        next_action = "Escalate to production-gate review; do not dispatch from this view model."
    elif data.budget_governor_verdict in BLOCKING_BUDGET_VERDICTS:
        verdict = "BLOCKED_BY_BUDGET"
        approval = "VIEW_ONLY_BLOCKED"
        reason = f"Budget governor blocked route with verdict {data.budget_governor_verdict}."
        next_action = "Reduce scope, choose cheaper target, or request budget override through a separate authority path."
    elif data.api_rate_governor_verdict in BLOCKING_API_RATE_VERDICTS:
        verdict = "BLOCKED_BY_API_RATE_LIMIT"
        approval = "VIEW_ONLY_BLOCKED"
        reason = f"API/rate governor blocked route with verdict {data.api_rate_governor_verdict}."
        next_action = "Wait for rate reset, reduce parallelism, or choose a fallback target."
    elif data.capability_policy_verdict in BLOCKING_CAPABILITY_VERDICTS or _has_auto_forbidden_capability(data.blocked_capabilities):
        verdict = "BLOCKED_BY_FORBIDDEN_CAPABILITY"
        approval = "VIEW_ONLY_BLOCKED"
        reason = "Capability policy found forbidden or manual-only capability requirements."
        next_action = "Remove forbidden capability, switch to manual lane, or request explicit supervised authority."
    elif data.claim_lane in {"C4", "C5", "FORBIDDEN", "UNVERIFIED_RELAY_CONTENT"}:
        verdict = "BLOCKED_BY_CLAIM_REVIEW"
        approval = "VIEW_ONLY_BLOCKED"
        reason = f"Claim lane {data.claim_lane} is not eligible for dispatch approval."
        next_action = "Run claim review and grounding before presenting dispatch for approval."
    else:
        verdict = "NEEDS_SUPERVISED_APPROVAL"
        approval = "SUPERVISED_REQUIRED"
        reason = "Governors allow route preview to request supervised approval; no live dispatch authority is granted."
        next_action = "Present to operator with budget/rate/capability evidence and require explicit approval before execution."

    receipt_preview = {
        "version": VERSION,
        "mission_id": data.mission_id,
        "route_preview_id": data.route_preview_id,
        "selected_target": data.selected_target,
        "verdict": verdict,
        "approval_mode": approval,
        "authority_scope": AUTHORITY_SCOPE,
        "production_authority": False,
        "live_dispatch_claim": False,
    }

    return DispatchAuthorizationViewModel(
        version=VERSION,
        mission_id=data.mission_id,
        route_preview_id=data.route_preview_id,
        selected_target=data.selected_target,
        compute_ring=data.compute_ring,
        access_method=data.access_method,
        task_class=data.task_class,
        claim_lane=data.claim_lane,
        authorization_verdict=verdict,
        authority_scope=AUTHORITY_SCOPE,
        approval_mode=approval,
        budget_governor_verdict=data.budget_governor_verdict,
        api_rate_governor_verdict=data.api_rate_governor_verdict,
        capability_policy_verdict=data.capability_policy_verdict,
        estimated_cost_usd=float(data.estimated_cost_usd),
        estimated_latency_band=data.estimated_latency_band,
        quality_band=data.quality_band,
        blocked_capabilities=list(data.blocked_capabilities),
        route_factors=list(data.route_factors),
        evidence_refs=list(data.evidence_refs),
        operator_reason=reason,
        next_required_action=next_action,
        dispatch_receipt_preview=receipt_preview,
    )


def build_fixture_authorization_input(**overrides: Any) -> DispatchAuthorizationInput:
    base = DispatchAuthorizationInput(
        mission_id="M-061",
        route_preview_id="route-preview-v59-001",
        selected_target="gemini-cli",
        compute_ring="RING_2_API_CLI_LOCAL",
        access_method="cli",
        task_class="context_route_analysis",
        claim_lane="C2",
        estimated_cost_usd=0.02,
        estimated_latency_band="interactive_seconds",
        quality_band="high",
        budget_governor_verdict="BUDGET_WITHIN_LIMITS",
        api_rate_governor_verdict="API_RATE_WITHIN_LIMITS",
        capability_policy_verdict="CAPABILITY_ALLOWED_WITH_SUPERVISION",
        evidence_refs=[
            "ION/03_registry/model_budget_policy.yaml",
            "ION/03_registry/api_rate_governor_policy.yaml",
            "ION/04_packages/kernel/joc_mission_dispatch_route_view_model.py",
        ],
        blocked_capabilities=[],
        route_factors=["cost", "latency", "quality", "context_window"],
    )
    values = asdict(base)
    values.update(overrides)
    return DispatchAuthorizationInput(**values)


def validate_dispatch_authorization_view_model(model: DispatchAuthorizationViewModel) -> Dict[str, Any]:
    findings: List[str] = []
    if model.version != VERSION:
        findings.append("invalid_version")
    if model.authority_scope != AUTHORITY_SCOPE:
        findings.append("invalid_authority_scope")
    if model.production_authority:
        findings.append("production_authority_must_be_false")
    if model.live_dispatch_claim:
        findings.append("live_dispatch_claim_must_be_false")
    if not model.evidence_refs:
        findings.append("missing_evidence_refs")
    if model.authorization_verdict.startswith("BLOCKED") and model.approval_mode != "VIEW_ONLY_BLOCKED":
        findings.append("blocked_verdict_requires_view_only_blocked")

    return {
        "version": VERSION,
        "validation_verdict": "VALID_DISPATCH_AUTHORIZATION_VIEW_MODEL" if not findings else "INVALID_DISPATCH_AUTHORIZATION_VIEW_MODEL",
        "authority_scope": AUTHORITY_SCOPE,
        "findings": findings,
        "production_authority": False,
        "live_dispatch_claim": False,
    }


if __name__ == "__main__":
    model = build_dispatch_authorization_view_model(build_fixture_authorization_input())
    print(model.to_dict())
    print(validate_dispatch_authorization_view_model(model))
