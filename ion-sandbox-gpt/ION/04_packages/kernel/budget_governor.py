"""V58 deterministic budget governor for model-economics routing.

The budget governor is a separate organ from the router and rate governor. It
never calls providers, loads credentials, dispatches scheduler work, or claims
production authority. It classifies whether a dry-run route candidate is
economically allowed under supplied or registry budget policy.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

SCHEMA_ID = "ion.budget_governor_decision.v1"
VERSION = "V58_BUDGET_AND_API_RATE_GOVERNORS"
AUTHORITY_SCOPE = "A3_STEWARD_BUDGET_GOVERNOR_CANDIDATE"
DEFAULT_REPORT_DIR = "ION/05_context/history/model_economics_budget_decisions"

DECISION_ALLOW = "allow"
DECISION_DOWNGRADE = "downgrade_model"
DECISION_BATCH = "batch_route"
DECISION_REQUIRE_APPROVAL = "require_approval"
DECISION_BLOCK = "block"

@dataclass(frozen=True)
class BudgetDecision:
    schema_id: str
    version: str
    decision_id: str
    emitted_at: str
    workspace_root: str
    authority_scope: str
    workflow_id: str
    work_class: str
    route_decision_id: str | None
    selected_provider: str | None
    selected_model: str | None
    routing_mode: str | None
    decision: str
    estimated_cost_usd: float | None
    budget_remaining_usd: float | None
    preferred_cost_usd: float | None
    maximum_cost_usd: float | None
    margin_status: str
    reason: tuple[str, ...]
    premium_escalation_required: bool
    premium_escalation_allowed: bool
    batch_allowed: bool
    consensus_allowed: bool
    live_provider_calls_authorized: bool
    provider_credentials_authorized: bool
    scheduler_direct_provider_calls_authorized: bool
    production_authority: bool
    claim_boundary: tuple[str, ...]
    next_recommended_branch: str = "V59_MODEL_CALL_RECEIPT_DRY_RUN_SURFACE"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:24]


def _load_yaml(path: Path) -> Mapping[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        raise ValueError(f"{path} did not parse to a mapping")
    return data


def _load_budget_policy(workspace_root: str | Path) -> Mapping[str, Any]:
    path = Path(workspace_root) / "ION/03_registry/budget_policy.yaml"
    return _load_yaml(path)


def _as_float(value: Any) -> float | None:
    if value is None or value == "unknown":
        return None
    try:
        return float(value)
    except Exception:
        return None


def _route_field(route: Any, name: str, default: Any = None) -> Any:
    if isinstance(route, Mapping):
        return route.get(name, default)
    return getattr(route, name, default)


def decide_budget(
    workspace_root: str | Path,
    route_decision: Any,
    *,
    workflow_budget: Mapping[str, Any] | None = None,
    budget_remaining_usd: float | None = None,
    emitted_at: str | None = None,
) -> BudgetDecision:
    root = Path(workspace_root).resolve()
    policy = _load_budget_policy(root)
    default_budget = dict(policy.get("default_workflow_budget", {})) if isinstance(policy.get("default_workflow_budget"), Mapping) else {}
    budget = {**default_budget, **dict(workflow_budget or {})}
    ts = emitted_at or _utc_now()

    workflow_id = str(_route_field(route_decision, "workflow_id", budget.get("workflow_id", "default")))
    work_class = str(_route_field(route_decision, "work_class", "unknown"))
    route_decision_id = _route_field(route_decision, "decision_id", None)
    selected_provider = _route_field(route_decision, "selected_provider", None)
    selected_model = _route_field(route_decision, "selected_model", None)
    routing_mode = _route_field(route_decision, "routing_mode", None)
    route_status = str(_route_field(route_decision, "decision_status", "UNKNOWN"))
    estimated_cost = _as_float(_route_field(route_decision, "estimated_cost_usd", None))

    maximum_cost = _as_float(budget.get("maximum_cost_usd"))
    preferred_cost = _as_float(budget.get("preferred_cost_usd"))
    abort_threshold = _as_float(budget.get("abort_if_projected_cost_exceeds"))
    premium_allowed = bool(budget.get("premium_escalation_allowed", False))
    batch_allowed = bool(budget.get("batch_allowed", True))
    consensus_allowed = bool(budget.get("consensus_allowed", False))

    reasons: list[str] = []
    decision = DECISION_ALLOW
    margin_status = "within_margin"
    premium_escalation_required = routing_mode == "highest_quality" or str(budget.get("cost_posture", "")).lower() in {"premium", "approval_required"}

    if route_status != "ROUTE_SELECTED":
        decision = DECISION_BLOCK
        margin_status = "blocked"
        reasons.append("route_not_selected")
    elif estimated_cost is None:
        decision = DECISION_REQUIRE_APPROVAL if premium_escalation_required else DECISION_ALLOW
        margin_status = "unknown_cost_non_authoritative"
        reasons.append("estimated_cost_unknown")
    elif abort_threshold is not None and estimated_cost > abort_threshold:
        decision = DECISION_BLOCK
        margin_status = "blocked"
        reasons.append("projected_cost_exceeds_abort_threshold")
    elif maximum_cost is not None and estimated_cost > maximum_cost:
        decision = DECISION_REQUIRE_APPROVAL if premium_allowed else DECISION_BLOCK
        margin_status = "exceeds_max"
        reasons.append("projected_cost_exceeds_maximum")
    elif budget_remaining_usd is not None and estimated_cost > budget_remaining_usd:
        decision = DECISION_BATCH if batch_allowed else DECISION_REQUIRE_APPROVAL
        margin_status = "no_remaining_budget"
        reasons.append("projected_cost_exceeds_remaining_budget")
    elif preferred_cost is not None and estimated_cost > preferred_cost:
        margin_status = "above_preferred"
        if premium_escalation_required and not premium_allowed:
            decision = DECISION_REQUIRE_APPROVAL
            reasons.append("premium_escalation_not_preapproved")
        elif batch_allowed and routing_mode in {"batch_preferred", "best_margin"}:
            decision = DECISION_BATCH
            reasons.append("above_preferred_cost_batch_route_available")
        else:
            decision = DECISION_ALLOW
            reasons.append("exceeds_preferred_cost_but_within_max")
    elif premium_escalation_required and not premium_allowed:
        decision = DECISION_REQUIRE_APPROVAL
        margin_status = "approval_required"
        reasons.append("premium_escalation_requires_explicit_approval")
    else:
        decision = DECISION_ALLOW
        reasons.append("within_budget")

    return BudgetDecision(
        schema_id=SCHEMA_ID,
        version=VERSION,
        decision_id=_stable_id("budget", route_decision_id or workflow_id, decision, ts),
        emitted_at=ts,
        workspace_root=root.as_posix(),
        authority_scope=AUTHORITY_SCOPE,
        workflow_id=workflow_id,
        work_class=work_class,
        route_decision_id=route_decision_id,
        selected_provider=selected_provider,
        selected_model=selected_model,
        routing_mode=routing_mode,
        decision=decision,
        estimated_cost_usd=estimated_cost,
        budget_remaining_usd=budget_remaining_usd,
        preferred_cost_usd=preferred_cost,
        maximum_cost_usd=maximum_cost,
        margin_status=margin_status,
        reason=tuple(reasons),
        premium_escalation_required=premium_escalation_required,
        premium_escalation_allowed=premium_allowed,
        batch_allowed=batch_allowed,
        consensus_allowed=consensus_allowed,
        live_provider_calls_authorized=False,
        provider_credentials_authorized=False,
        scheduler_direct_provider_calls_authorized=False,
        production_authority=False,
        claim_boundary=(
            "This budget decision is deterministic and non-production-authoritative.",
            "It does not call providers, enforce real billing, or prove model output truth.",
        ),
    )


def _jsonable(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, tuple):
        return [_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    return obj


def write_budget_decision(workspace_root: str | Path, decision: BudgetDecision, *, output_dir: str | Path = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root)
    out = root / output_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"V58_BUDGET_DECISION_{decision.decision_id}.json"
    path.write_text(json.dumps(_jsonable(decision), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Create a deterministic V58 budget-governor decision.")
    p.add_argument("--workspace-root", default=".")
    p.add_argument("--route-json", default=None, help="Path to a V57 route-decision JSON. If omitted, build a route from --work-class.")
    p.add_argument("--work-class", default="cheap_classification")
    p.add_argument("--estimated-input-tokens", type=int, default=1000)
    p.add_argument("--estimated-output-tokens", type=int, default=200)
    p.add_argument("--maximum-cost-usd", type=float, default=None)
    p.add_argument("--preferred-cost-usd", type=float, default=None)
    p.add_argument("--budget-remaining-usd", type=float, default=None)
    p.add_argument("--premium-escalation-allowed", action="store_true")
    p.add_argument("--write", action="store_true")
    p.add_argument("--json", action="store_true")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if args.route_json:
        route = json.loads(Path(args.route_json).read_text(encoding="utf-8"))
    else:
        from .model_router import build_call_intent_from_work_class, decide_route
        intent = build_call_intent_from_work_class(
            args.workspace_root,
            args.work_class,
            estimated_input_tokens=args.estimated_input_tokens,
            estimated_output_tokens=args.estimated_output_tokens,
        )
        route = decide_route(args.workspace_root, intent)
    budget = {
        "maximum_cost_usd": args.maximum_cost_usd,
        "preferred_cost_usd": args.preferred_cost_usd,
        "premium_escalation_allowed": args.premium_escalation_allowed,
    }
    decision = decide_budget(args.workspace_root, route, workflow_budget=budget, budget_remaining_usd=args.budget_remaining_usd)
    if args.write:
        write_budget_decision(args.workspace_root, decision)
    if args.json:
        print(json.dumps(_jsonable(decision), indent=2, sort_keys=True))
    else:
        print(f"decision: {decision.decision}")
        print(f"margin_status: {decision.margin_status}")
        print(f"estimated_cost_usd: {decision.estimated_cost_usd}")
        print(f"reason: {','.join(decision.reason)}")
        print(f"next: {decision.next_recommended_branch}")
    return 0 if decision.decision == DECISION_ALLOW else (3 if decision.decision == DECISION_BLOCK else 2)

if __name__ == "__main__":
    raise SystemExit(main())

