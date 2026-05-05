"""V57 deterministic model router and cost-quality route decision surface.

This module intentionally performs pure routing over V56/V57 registries only.
It does not call providers, load credentials, dispatch work, enforce runtime rate
limits, or claim production model-routing authority.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

SCHEMA_ID = "ion.model_route_decision.v1"
VERSION = "V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING"
AUTHORITY_SCOPE = "A3_STEWARD_MODEL_ROUTING_CANDIDATE"
DEFAULT_REPORT_DIR = "ION/05_context/history/model_route_decisions"

REGISTRY_PATHS = {
    "provider_registry": "ION/03_registry/provider_registry.yaml",
    "model_capability_registry": "ION/03_registry/model_capability_registry.yaml",
    "model_pricing_registry": "ION/03_registry/model_pricing_registry.yaml",
    "model_rate_limit_registry": "ION/03_registry/model_rate_limit_registry.yaml",
    "model_routing_policy": "ION/03_registry/model_routing_policy.yaml",
    "model_eval_score_registry": "ION/03_registry/model_eval_score_registry.yaml",
    "model_data_handling_registry": "ION/03_registry/model_data_handling_registry.yaml",
    "budget_policy": "ION/03_registry/budget_policy.yaml",
    "work_class_model_policy": "ION/03_registry/work_class_model_policy.yaml",
}

QUALITY_ORDER = {"low": 1, "medium": 2, "high": 3, "supreme": 4}
CONTEXT_ORDER = {"small": 1, "medium": 2, "long": 3, "huge": 4}
LATENCY_SCORE = {"realtime": 1.0, "interactive": 0.85, "checked": 0.65, "background": 0.45, "batch": 0.25}
DECISION_SELECTED = "ROUTE_SELECTED"
DECISION_NO_ELIGIBLE = "ROUTE_BLOCKED_NO_ELIGIBLE_MODEL"
DECISION_PRIVACY = "ROUTE_BLOCKED_BY_PRIVACY"
DECISION_CAPABILITY = "ROUTE_BLOCKED_BY_CAPABILITY"
DECISION_BUDGET = "ROUTE_BLOCKED_BY_BUDGET_CEILING"

@dataclass(frozen=True)
class CallIntent:
    intent_id: str
    workflow_id: str
    parent_packet: str
    work_class: str
    quality_requirement: str | None = None
    latency_requirement: str = "interactive"
    cost_posture: str = "balanced"
    risk_level: str = "low"
    context_requirement: str = "medium"
    estimated_input_tokens: int | None = None
    estimated_output_tokens: int | None = None
    parallelism_allowed: bool = False
    consensus_required: bool | None = None
    privacy_requirement: str | None = None
    max_estimated_cost_usd: float | None = None
    max_latency_ms: int | None = None
    required_capabilities: tuple[str, ...] = ()
    forbidden_providers: tuple[str, ...] = ()
    preferred_providers: tuple[str, ...] = ()
    fallback_allowed: bool = True
    escalation_allowed: bool = True

@dataclass(frozen=True)
class AlternativeConsidered:
    provider: str
    model: str
    rejected_reason: str
    score: float | None = None
    estimated_cost_usd: float | None = None

@dataclass(frozen=True)
class RouteDecision:
    schema_id: str
    version: str
    decision_id: str
    emitted_at: str
    workspace_root: str
    authority_scope: str
    intent_id: str
    workflow_id: str
    parent_packet: str
    work_class: str
    decision_status: str
    selected_provider: str | None
    selected_model: str | None
    selected_lane: str | None
    routing_mode: str
    selection_reason: tuple[str, ...]
    alternatives_considered: tuple[AlternativeConsidered, ...]
    requires_rate_governor_check: bool
    requires_budget_governor_check: bool
    requires_front_stage_receipt_if_user_facing: bool
    estimated_cost_usd: float | None
    score: float | None
    consensus_required: bool
    fallback_allowed: bool
    live_provider_calls_authorized: bool
    provider_credentials_authorized: bool
    scheduler_direct_provider_calls_authorized: bool
    production_authority: bool
    claim_boundary: tuple[str, ...]
    next_recommended_branch: str = "V58_BUDGET_AND_API_RATE_GOVERNORS"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]


def load_yaml(path: Path) -> Mapping[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        raise ValueError(f"{path} did not parse to a mapping")
    return data


def load_registries(workspace_root: str | Path) -> dict[str, Mapping[str, Any]]:
    root = Path(workspace_root)
    loaded: dict[str, Mapping[str, Any]] = {}
    for key, rel in REGISTRY_PATHS.items():
        path = root / rel
        if not path.exists():
            loaded[key] = {"__missing__": True}
        else:
            loaded[key] = load_yaml(path)
    return loaded


def _as_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(str(x) for x in value)
    return (str(value),)


def build_call_intent_from_work_class(workspace_root: str | Path, work_class: str, **overrides: Any) -> CallIntent:
    registries = load_registries(workspace_root)
    classes = registries.get("work_class_model_policy", {}).get("work_classes", {})
    if work_class not in classes:
        raise ValueError(f"unknown work_class: {work_class}")
    contract = classes[work_class]
    if not isinstance(contract, Mapping):
        raise ValueError(f"work_class contract not mapping: {work_class}")
    payload: dict[str, Any] = {
        "intent_id": overrides.pop("intent_id", f"call-intent-{_stable_id(work_class, _utc_now())}"),
        "workflow_id": overrides.pop("workflow_id", "default"),
        "parent_packet": overrides.pop("parent_packet", "manual-v57-routing-check"),
        "work_class": work_class,
        "quality_requirement": overrides.pop("quality_requirement", contract.get("minimum_quality")),
        "latency_requirement": overrides.pop("latency_requirement", "interactive"),
        "cost_posture": overrides.pop("cost_posture", "balanced"),
        "risk_level": overrides.pop("risk_level", "low"),
        "context_requirement": overrides.pop("context_requirement", "medium"),
        "estimated_input_tokens": overrides.pop("estimated_input_tokens", None),
        "estimated_output_tokens": overrides.pop("estimated_output_tokens", None),
        "parallelism_allowed": overrides.pop("parallelism_allowed", False),
        "consensus_required": overrides.pop("consensus_required", contract.get("consensus_required_by_default", False)),
        "privacy_requirement": overrides.pop("privacy_requirement", contract.get("privacy_floor")),
        "max_estimated_cost_usd": overrides.pop("max_estimated_cost_usd", None),
        "max_latency_ms": overrides.pop("max_latency_ms", None),
        "required_capabilities": tuple(overrides.pop("required_capabilities", contract.get("required_capabilities", ()))),
        "forbidden_providers": tuple(overrides.pop("forbidden_providers", ())),
        "preferred_providers": tuple(overrides.pop("preferred_providers", ())),
        "fallback_allowed": overrides.pop("fallback_allowed", True),
        "escalation_allowed": overrides.pop("escalation_allowed", True),
    }
    if overrides:
        raise ValueError(f"unknown overrides: {sorted(overrides)}")
    return CallIntent(**payload)


def _quality_meets(model_quality: str, required: str) -> bool:
    return QUALITY_ORDER.get(model_quality, 0) >= QUALITY_ORDER.get(required, 0)


def _context_meets(model_context: str, required: str) -> bool:
    return CONTEXT_ORDER.get(model_context, 0) >= CONTEXT_ORDER.get(required, 0)


def _privacy_allowed(registries: Mapping[str, Mapping[str, Any]], provider: str, model_privacy: str | None, requirement: str) -> bool:
    handling = registries.get("model_data_handling_registry", {})
    req_profile = handling.get("profiles", {}).get(requirement, {}) if isinstance(handling.get("profiles"), Mapping) else {}
    allowed_profiles = set(_as_tuple(req_profile.get("allowed_provider_profiles"))) if isinstance(req_profile, Mapping) else {requirement}
    provider_profile = handling.get("provider_profiles", {}).get(provider) if isinstance(handling.get("provider_profiles"), Mapping) else None
    profile = model_privacy or provider_profile or "normal"
    return profile in allowed_profiles


def _estimate_cost(registries: Mapping[str, Mapping[str, Any]], model_key: str, intent: CallIntent) -> float | None:
    pricing = registries.get("model_pricing_registry", {}).get("pricing", {})
    if not isinstance(pricing, Mapping):
        return None
    row = pricing.get(model_key, {})
    if not isinstance(row, Mapping):
        return None
    in_price = row.get("input_per_million_tokens")
    out_price = row.get("output_per_million_tokens")
    if in_price is None or out_price is None:
        return None
    try:
        input_tokens = intent.estimated_input_tokens or 0
        output_tokens = intent.estimated_output_tokens or 0
        return round((float(in_price) * input_tokens + float(out_price) * output_tokens) / 1_000_000, 8)
    except Exception:
        return None


def _availability_score(registries: Mapping[str, Mapping[str, Any]], model_key: str) -> float:
    states = registries.get("model_rate_limit_registry", {}).get("capacity_states", {})
    row = states.get(model_key, {}) if isinstance(states, Mapping) else {}
    if not isinstance(row, Mapping):
        return 0.5
    if row.get("backoff_state") in {"blocked", "throttled"}:
        return 0.0
    max_par = row.get("safe_parallelism_max")
    try:
        return min(1.0, max(0.25, float(max_par) / 4.0))
    except Exception:
        return 0.5


def _cost_score(cost: float | None) -> float:
    if cost is None:
        return 0.35  # placeholder external prices are deliberately penalized until verified
    if cost <= 0:
        return 1.0
    return max(0.05, min(1.0, 1.0 / (1.0 + cost)))


def _score_candidate(registries: Mapping[str, Mapping[str, Any]], model_key: str, model: Mapping[str, Any], intent: CallIntent, routing_mode: str) -> float:
    quality = QUALITY_ORDER.get(str(model.get("capability_tier")), 0) / max(QUALITY_ORDER.values())
    context = CONTEXT_ORDER.get(str(model.get("context_class")), 0) / max(CONTEXT_ORDER.values())
    latency = LATENCY_SCORE.get(str(model.get("latency_class")), 0.5)
    availability = _availability_score(registries, model_key)
    cost = _cost_score(_estimate_cost(registries, model_key, intent))
    privacy = 1.0 if _privacy_allowed(registries, str(model.get("provider")), str(model.get("privacy_floor_supported", "normal")), intent.privacy_requirement or "normal") else 0.0
    preferred = 0.05 if model.get("provider") in set(intent.preferred_providers) else 0.0
    if routing_mode == "highest_quality":
        return 0.68 * quality + 0.10 * context + 0.08 * latency + 0.07 * availability + 0.04 * privacy + 0.03 * cost + preferred
    if routing_mode == "cheapest_good_enough":
        return 0.52 * cost + 0.18 * quality + 0.10 * latency + 0.08 * context + 0.07 * availability + 0.05 * privacy + preferred
    if routing_mode == "fastest_safe":
        return 0.48 * latency + 0.22 * quality + 0.12 * availability + 0.08 * context + 0.05 * cost + 0.05 * privacy + preferred
    if routing_mode == "batch_preferred":
        return 0.33 * cost + 0.27 * quality + 0.18 * context + 0.12 * availability + 0.05 * latency + 0.05 * privacy + preferred
    if routing_mode == "best_margin":
        return 0.40 * quality + 0.30 * cost + 0.12 * availability + 0.10 * context + 0.04 * latency + 0.04 * privacy + preferred
    # balanced and consensus_required use balanced primary scoring; consensus emits a flag later.
    return 0.35 * quality + 0.20 * cost + 0.15 * latency + 0.10 * context + 0.10 * availability + 0.10 * privacy + preferred


def _candidate_lane(contract: Mapping[str, Any], routing_mode: str) -> str | None:
    lanes = list(contract.get("allowed_lanes", []))
    if routing_mode == "batch_preferred":
        for lane in ("batch", "background", "local", "checked", "interactive"):
            if lane in lanes: return lane
    if routing_mode == "fastest_safe":
        for lane in ("realtime", "interactive", "checked", "local", "background", "batch"):
            if lane in lanes: return lane
    for lane in ("checked", "interactive", "background", "batch", "local", "human_ide_carrier", "realtime"):
        if lane in lanes: return lane
    return lanes[0] if lanes else None


def decide_route(workspace_root: str | Path, intent: CallIntent | Mapping[str, Any], *, emitted_at: str | None = None) -> RouteDecision:
    root = Path(workspace_root).resolve()
    if isinstance(intent, Mapping):
        intent = CallIntent(**{**intent, "required_capabilities": tuple(intent.get("required_capabilities", ())), "forbidden_providers": tuple(intent.get("forbidden_providers", ())), "preferred_providers": tuple(intent.get("preferred_providers", ()))})
    registries = load_registries(root)
    classes = registries.get("work_class_model_policy", {}).get("work_classes", {})
    contract = classes.get(intent.work_class, {}) if isinstance(classes, Mapping) else {}
    if not isinstance(contract, Mapping):
        contract = {}
    routing_mode = str(contract.get("default_routing_mode", "balanced"))
    if routing_mode == "balanced":
        routing_mode = "balanced"
    required_quality = intent.quality_requirement or str(contract.get("minimum_quality", "medium"))
    required_caps = set(intent.required_capabilities or _as_tuple(contract.get("required_capabilities")))
    privacy_req = intent.privacy_requirement or str(contract.get("privacy_floor", "normal"))
    selected: tuple[str, Mapping[str, Any], float, float | None] | None = None
    alternatives: list[AlternativeConsidered] = []
    models = registries.get("model_capability_registry", {}).get("models", {})
    providers = registries.get("provider_registry", {}).get("providers", {})
    if not isinstance(models, Mapping): models = {}
    if not isinstance(providers, Mapping): providers = {}
    any_privacy_block = False
    any_capability_block = False
    any_budget_block = False
    for model_key, model in models.items():
        if not isinstance(model, Mapping):
            continue
        provider = str(model.get("provider"))
        model_id = str(model.get("model_id"))
        cost = _estimate_cost(registries, model_key, intent)
        reasons: list[str] = []
        if provider in set(intent.forbidden_providers):
            reasons.append("provider_forbidden")
        if provider not in providers:
            reasons.append("provider_not_registered")
        elif providers[provider].get("credential_source_allowed") or providers[provider].get("enabled_for_live_calls"):
            reasons.append("unexpected_live_provider_authority")
        caps = set(_as_tuple(model.get("capabilities")))
        if not required_caps.issubset(caps):
            missing = sorted(required_caps - caps)
            reasons.append("insufficient_capability:" + ",".join(missing))
            any_capability_block = True
        if not _quality_meets(str(model.get("capability_tier")), required_quality):
            reasons.append("insufficient_quality")
            any_capability_block = True
        if not _context_meets(str(model.get("context_class")), intent.context_requirement):
            reasons.append("insufficient_context")
            any_capability_block = True
        if not _privacy_allowed(registries, provider, str(model.get("privacy_floor_supported", "normal")), privacy_req):
            reasons.append("privacy_mismatch")
            any_privacy_block = True
        if cost is not None and intent.max_estimated_cost_usd is not None and cost > intent.max_estimated_cost_usd:
            reasons.append("hard_budget_ceiling_exceeded")
            any_budget_block = True
        score = None if reasons else round(_score_candidate(registries, model_key, model, intent, routing_mode), 6)
        if reasons:
            alternatives.append(AlternativeConsidered(provider=provider, model=model_id, rejected_reason=";".join(reasons), score=score, estimated_cost_usd=cost))
            continue
        alternatives.append(AlternativeConsidered(provider=provider, model=model_id, rejected_reason="eligible", score=score, estimated_cost_usd=cost))
        if selected is None or (score or 0.0) > selected[2] or ((score or 0.0) == selected[2] and model_key < selected[0]):
            selected = (model_key, model, score or 0.0, cost)
    ts = emitted_at or _utc_now()
    if selected is None:
        if any_budget_block:
            status = DECISION_BUDGET
        elif any_privacy_block and not any_capability_block:
            status = DECISION_PRIVACY
        elif any_capability_block:
            status = DECISION_CAPABILITY
        else:
            status = DECISION_NO_ELIGIBLE
        return RouteDecision(
            schema_id=SCHEMA_ID, version=VERSION, decision_id=_stable_id("route", intent.intent_id, status, ts), emitted_at=ts,
            workspace_root=root.as_posix(), authority_scope=AUTHORITY_SCOPE, intent_id=intent.intent_id, workflow_id=intent.workflow_id,
            parent_packet=intent.parent_packet, work_class=intent.work_class, decision_status=status, selected_provider=None, selected_model=None,
            selected_lane=None, routing_mode=routing_mode, selection_reason=("no eligible candidate after filters",), alternatives_considered=tuple(alternatives),
            requires_rate_governor_check=False, requires_budget_governor_check=False, requires_front_stage_receipt_if_user_facing=intent.work_class in {"user_facing_answer", "front_stage_claim_classification", "conversation_repair"},
            estimated_cost_usd=None, score=None, consensus_required=bool(intent.consensus_required or contract.get("consensus_required_by_default") or routing_mode == "consensus_required"),
            fallback_allowed=intent.fallback_allowed, live_provider_calls_authorized=False, provider_credentials_authorized=False,
            scheduler_direct_provider_calls_authorized=False, production_authority=False,
            claim_boundary=("This route decision proves deterministic registry selection only, not provider availability, output truth, or production routing authority.",),
        )
    model_key, model, score, cost = selected
    provider = str(model.get("provider"))
    model_id = str(model.get("model_id"))
    return RouteDecision(
        schema_id=SCHEMA_ID, version=VERSION, decision_id=_stable_id("route", intent.intent_id, provider, model_id, ts), emitted_at=ts,
        workspace_root=root.as_posix(), authority_scope=AUTHORITY_SCOPE, intent_id=intent.intent_id, workflow_id=intent.workflow_id,
        parent_packet=intent.parent_packet, work_class=intent.work_class, decision_status=DECISION_SELECTED, selected_provider=provider,
        selected_model=model_id, selected_lane=_candidate_lane(contract, routing_mode), routing_mode=routing_mode,
        selection_reason=("sufficient_capability", "context_fit", "privacy_requirement_satisfied", "within_placeholder_budget", "dry_run_provider_registered"),
        alternatives_considered=tuple(alternatives), requires_rate_governor_check=True, requires_budget_governor_check=True,
        requires_front_stage_receipt_if_user_facing=intent.work_class in {"user_facing_answer", "front_stage_claim_classification", "conversation_repair"},
        estimated_cost_usd=cost, score=round(score, 6), consensus_required=bool(intent.consensus_required or contract.get("consensus_required_by_default") or routing_mode == "consensus_required"),
        fallback_allowed=intent.fallback_allowed, live_provider_calls_authorized=False, provider_credentials_authorized=False,
        scheduler_direct_provider_calls_authorized=False, production_authority=False,
        claim_boundary=("This route decision is a dry-run routing candidate only.", "It does not call providers, load credentials, bypass budget/rate governors, or make model output user-facing truth."),
    )


def _jsonable(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, tuple):
        return [_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    return obj


def write_route_decision(workspace_root: str | Path, decision: RouteDecision, *, output_dir: str | Path = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root)
    out = root / output_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"V57_MODEL_ROUTE_DECISION_{decision.decision_id}.json"
    path.write_text(json.dumps(_jsonable(decision), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Create a deterministic dry-run V57 model route decision.")
    p.add_argument("--workspace-root", default=".")
    p.add_argument("--work-class", default="cheap_classification")
    p.add_argument("--quality-requirement", default=None)
    p.add_argument("--privacy-requirement", default=None)
    p.add_argument("--context-requirement", default="medium")
    p.add_argument("--estimated-input-tokens", type=int, default=None)
    p.add_argument("--estimated-output-tokens", type=int, default=None)
    p.add_argument("--max-estimated-cost-usd", type=float, default=None)
    p.add_argument("--forbidden-provider", action="append", default=[])
    p.add_argument("--write", action="store_true")
    p.add_argument("--json", action="store_true")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    intent = build_call_intent_from_work_class(
        args.workspace_root,
        args.work_class,
        quality_requirement=args.quality_requirement,
        privacy_requirement=args.privacy_requirement,
        context_requirement=args.context_requirement,
        estimated_input_tokens=args.estimated_input_tokens,
        estimated_output_tokens=args.estimated_output_tokens,
        max_estimated_cost_usd=args.max_estimated_cost_usd,
        forbidden_providers=tuple(args.forbidden_provider),
    )
    decision = decide_route(args.workspace_root, intent)
    if args.write:
        write_route_decision(args.workspace_root, decision)
    if args.json:
        print(json.dumps(_jsonable(decision), indent=2, sort_keys=True))
    else:
        print(f"decision_status: {decision.decision_status}")
        print(f"work_class: {decision.work_class}")
        print(f"routing_mode: {decision.routing_mode}")
        print(f"selected_provider: {decision.selected_provider}")
        print(f"selected_model: {decision.selected_model}")
        print(f"score: {decision.score}")
        print(f"alternatives_considered: {len(decision.alternatives_considered)}")
        print(f"next: {decision.next_recommended_branch}")
    return 0 if decision.decision_status == DECISION_SELECTED else 2

if __name__ == "__main__":
    raise SystemExit(main())

