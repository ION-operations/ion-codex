"""V58 deterministic API rate governor for provider capacity decisions.

This module reads known/placeholder capacity state and classifies whether a dry-run
route candidate may dispatch now. It does not query provider APIs, consume rate
limits, load credentials, or authorize production dispatch.
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

SCHEMA_ID = "ion.api_rate_governor_decision.v1"
VERSION = "V58_BUDGET_AND_API_RATE_GOVERNORS"
AUTHORITY_SCOPE = "A3_STEWARD_API_RATE_GOVERNOR_CANDIDATE"
DEFAULT_REPORT_DIR = "ION/05_context/history/model_economics_rate_decisions"

DECISION_ALLOW = "allow"
DECISION_QUEUE = "queue"
DECISION_REROUTE = "reroute"
DECISION_BATCH = "batch"
DECISION_THROTTLE = "throttle"
DECISION_BLOCK = "block"

@dataclass(frozen=True)
class ApiRateGovernorDecision:
    schema_id: str
    version: str
    decision_id: str
    emitted_at: str
    workspace_root: str
    authority_scope: str
    route_decision_id: str | None
    provider: str | None
    model: str | None
    model_key: str | None
    selected_lane: str | None
    decision: str
    reason: tuple[str, ...]
    earliest_dispatch_at: str | None
    suggested_fallbacks: tuple[str, ...]
    safe_parallelism_current: int | None
    safe_parallelism_max: int | None
    in_flight_requests: int
    backoff_state: str
    retry_after_active: bool
    capacity_confidence: str
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


def _route_field(route: Any, name: str, default: Any = None) -> Any:
    if isinstance(route, Mapping):
        return route.get(name, default)
    return getattr(route, name, default)


def _to_int(value: Any, default: int | None = None) -> int | None:
    try:
        return int(value)
    except Exception:
        return default


def _model_key(provider: str | None, model: str | None) -> str | None:
    if not provider or not model:
        return None
    return f"{provider}/{model}"


def _load_capacity_state(workspace_root: str | Path, model_key: str | None) -> Mapping[str, Any]:
    path = Path(workspace_root) / "ION/03_registry/model_rate_limit_registry.yaml"
    reg = _load_yaml(path)
    states = reg.get("capacity_states", {})
    if not isinstance(states, Mapping) or model_key not in states:
        return {}
    row = states[model_key]
    return row if isinstance(row, Mapping) else {}


def decide_api_rate(
    workspace_root: str | Path,
    route_decision: Any,
    *,
    in_flight_requests: int | None = None,
    retry_after_active: bool = False,
    provider_degraded: bool = False,
    emitted_at: str | None = None,
) -> ApiRateGovernorDecision:
    root = Path(workspace_root).resolve()
    ts = emitted_at or _utc_now()
    route_status = str(_route_field(route_decision, "decision_status", "UNKNOWN"))
    route_decision_id = _route_field(route_decision, "decision_id", None)
    provider = _route_field(route_decision, "selected_provider", None)
    model = _route_field(route_decision, "selected_model", None)
    lane = _route_field(route_decision, "selected_lane", None)
    key = _model_key(provider, model)
    state = _load_capacity_state(root, key)
    backoff = str(state.get("backoff_state", "unknown"))
    safe_max = _to_int(state.get("safe_parallelism_max"), None)
    safe_current = _to_int(state.get("safe_parallelism_current"), safe_max)
    current = int(in_flight_requests if in_flight_requests is not None else state.get("in_flight_requests", 0) or 0)
    confidence = str(state.get("confidence", "low" if not state else "medium"))
    reasons: list[str] = []
    fallbacks: list[str] = []
    decision = DECISION_ALLOW
    earliest = None

    if route_status != "ROUTE_SELECTED" or not key:
        decision = DECISION_BLOCK
        reasons.append("route_not_selected")
    elif not state:
        decision = DECISION_QUEUE
        reasons.append("capacity_state_unknown")
        earliest = "after_capacity_state_refresh"
    elif provider_degraded:
        decision = DECISION_REROUTE
        reasons.append("provider_degraded")
        fallbacks.append("select_alternate_route")
    elif retry_after_active or state.get("retry_after_until"):
        decision = DECISION_QUEUE
        reasons.append("retry_after_active")
        earliest = str(state.get("retry_after_until") or "after_retry_after_window")
    elif backoff == "blocked":
        decision = DECISION_BLOCK
        reasons.append("provider_backoff_blocked")
    elif backoff == "throttled":
        decision = DECISION_THROTTLE
        reasons.append("provider_throttled")
        earliest = "after_backoff_cooldown"
    elif backoff == "cooling":
        decision = DECISION_QUEUE
        reasons.append("provider_cooling")
        earliest = "after_cooling_window"
    elif safe_max is not None and current >= safe_max:
        if lane in {"batch", "background"}:
            decision = DECISION_BATCH
            reasons.append("in_flight_at_or_above_safe_parallelism_batch_lane")
        else:
            decision = DECISION_QUEUE
            reasons.append("in_flight_at_or_above_safe_parallelism")
        earliest = "after_in_flight_settles"
    else:
        decision = DECISION_ALLOW
        reasons.extend(["capacity_state_present", "in_flight_below_safe_parallelism", "backoff_state_allows_dispatch"])

    return ApiRateGovernorDecision(
        schema_id=SCHEMA_ID,
        version=VERSION,
        decision_id=_stable_id("api-rate", route_decision_id or key or "none", decision, ts),
        emitted_at=ts,
        workspace_root=root.as_posix(),
        authority_scope=AUTHORITY_SCOPE,
        route_decision_id=route_decision_id,
        provider=provider,
        model=model,
        model_key=key,
        selected_lane=lane,
        decision=decision,
        reason=tuple(reasons),
        earliest_dispatch_at=earliest,
        suggested_fallbacks=tuple(fallbacks),
        safe_parallelism_current=safe_current,
        safe_parallelism_max=safe_max,
        in_flight_requests=current,
        backoff_state=backoff,
        retry_after_active=bool(retry_after_active or state.get("retry_after_until")),
        capacity_confidence=confidence,
        live_provider_calls_authorized=False,
        provider_credentials_authorized=False,
        scheduler_direct_provider_calls_authorized=False,
        production_authority=False,
        claim_boundary=(
            "This rate-governor decision is deterministic and non-production-authoritative.",
            "It does not query providers, consume quotas, execute calls, or authorize scheduler dispatch.",
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


def write_api_rate_decision(workspace_root: str | Path, decision: ApiRateGovernorDecision, *, output_dir: str | Path = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root)
    out = root / output_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"V58_API_RATE_DECISION_{decision.decision_id}.json"
    path.write_text(json.dumps(_jsonable(decision), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Create a deterministic V58 API-rate-governor decision.")
    p.add_argument("--workspace-root", default=".")
    p.add_argument("--route-json", default=None, help="Path to a V57 route-decision JSON. If omitted, build a route from --work-class.")
    p.add_argument("--work-class", default="cheap_classification")
    p.add_argument("--in-flight-requests", type=int, default=None)
    p.add_argument("--retry-after-active", action="store_true")
    p.add_argument("--provider-degraded", action="store_true")
    p.add_argument("--write", action="store_true")
    p.add_argument("--json", action="store_true")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if args.route_json:
        route = json.loads(Path(args.route_json).read_text(encoding="utf-8"))
    else:
        from .model_router import build_call_intent_from_work_class, decide_route
        intent = build_call_intent_from_work_class(args.workspace_root, args.work_class, context_requirement="small")
        route = decide_route(args.workspace_root, intent)
    decision = decide_api_rate(
        args.workspace_root,
        route,
        in_flight_requests=args.in_flight_requests,
        retry_after_active=args.retry_after_active,
        provider_degraded=args.provider_degraded,
    )
    if args.write:
        write_api_rate_decision(args.workspace_root, decision)
    if args.json:
        print(json.dumps(_jsonable(decision), indent=2, sort_keys=True))
    else:
        print(f"decision: {decision.decision}")
        print(f"provider: {decision.provider}")
        print(f"model: {decision.model}")
        print(f"reason: {','.join(decision.reason)}")
        print(f"next: {decision.next_recommended_branch}")
    return 0 if decision.decision == DECISION_ALLOW else (3 if decision.decision in {DECISION_BLOCK, DECISION_REROUTE, DECISION_THROTTLE} else 2)

if __name__ == "__main__":
    raise SystemExit(main())

