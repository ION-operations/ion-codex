"""Deterministic Codex CLI model-move planner for ION chat lanes.

The planner describes which Codex model and reasoning effort should be used for
one bounded CLI call. It does not call providers, inspect credentials, consume
quota, or claim that account-level limits are authoritative.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.codex_cli_model_move_plan.v1"
MODEL_PROFILE_SCHEMA_ID = "ion.codex_cli_model_profiles.v1"
VERSION = "V126_CODEX_CLI_MODEL_MOVES"
READY_VERDICT = "ION_CODEX_CLI_MODEL_MOVES_READY"
DEFAULT_ROUTING_POSTURE = "conserve_main_bank"
REASONING_EFFORTS = ("low", "medium", "high", "xhigh")

CODEX_MODEL_PROFILES: dict[str, dict[str, Any]] = {
    "gpt-5.3-codex-spark": {
        "codex_model_slug": "gpt-5.3-codex-spark",
        "display_name": "GPT-5.3-Codex-Spark",
        "role": "fast_codex_lane",
        "default_reasoning_effort": "high",
        "reasoning_efforts_supported": list(REASONING_EFFORTS),
        "usage_pool_id": "codex_spark_observed",
        "usage_pool_authority": "operator_observed_pending_verification",
        "limit_authority": "not_authoritative",
        "local_codex_cache_observed": True,
        "production_authority": False,
        "live_execution_authority": False,
    },
    "gpt-5.3-codex": {
        "codex_model_slug": "gpt-5.3-codex",
        "display_name": "GPT-5.3-Codex",
        "role": "primary_codex_engineering_lane",
        "default_reasoning_effort": "medium",
        "reasoning_efforts_supported": list(REASONING_EFFORTS),
        "usage_pool_id": "codex_primary_observed",
        "usage_pool_authority": "operator_observed_pending_verification",
        "limit_authority": "not_authoritative",
        "local_codex_cache_observed": True,
        "production_authority": False,
        "live_execution_authority": False,
    },
    "gpt-5.5": {
        "codex_model_slug": "gpt-5.5",
        "display_name": "GPT-5.5",
        "role": "frontier_authority_and_architecture_lane",
        "default_reasoning_effort": "medium",
        "reasoning_efforts_supported": list(REASONING_EFFORTS),
        "usage_pool_id": "frontier_main_observed",
        "usage_pool_authority": "operator_observed_pending_verification",
        "limit_authority": "not_authoritative",
        "local_codex_cache_observed": True,
        "production_authority": False,
        "live_execution_authority": False,
    },
    "gpt-5.4": {
        "codex_model_slug": "gpt-5.4",
        "display_name": "GPT-5.4",
        "role": "fallback_frontier_lane",
        "default_reasoning_effort": "medium",
        "reasoning_efforts_supported": list(REASONING_EFFORTS),
        "usage_pool_id": "frontier_main_observed",
        "usage_pool_authority": "operator_observed_pending_verification",
        "limit_authority": "not_authoritative",
        "local_codex_cache_observed": True,
        "production_authority": False,
        "live_execution_authority": False,
    },
    "gpt-5.4-mini": {
        "codex_model_slug": "gpt-5.4-mini",
        "display_name": "GPT-5.4-Mini",
        "role": "fallback_light_codex_lane",
        "default_reasoning_effort": "medium",
        "reasoning_efforts_supported": list(REASONING_EFFORTS),
        "usage_pool_id": "codex_light_observed",
        "usage_pool_authority": "operator_observed_pending_verification",
        "limit_authority": "not_authoritative",
        "local_codex_cache_observed": True,
        "production_authority": False,
        "live_execution_authority": False,
    },
}

STAGE_WORK_CLASS: dict[str, str] = {
    "relay_ingress": "front_stage_claim_classification",
    "steward_route": "claim_audit",
    "vizier_plan": "architecture_design",
    "mason_codex_work": "code_patch",
    "vice_risk": "adversarial_review",
    "nemesis_verify": "code_review",
    "relay_return": "user_facing_answer",
    "persona_response": "user_facing_answer",
    "codex_general_work": "code_patch",
}

HIGH_RISK_TERMS = (
    "credential",
    "secret",
    "token",
    "delete",
    "remove",
    "production",
    "deploy",
    "cloudflare",
    "systemd",
    "service",
    "git push",
    "privacy",
    "public url",
)
ARCHITECTURE_TERMS = ("architecture", "schema", "protocol", "registry", "router", "policy", "workflow")
REVIEW_TERMS = ("review", "audit", "verify", "regression", "risk", "nemesis")
STATUS_TERMS = ("status", "health", "read-only", "read only", "smoke", "summary")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]


def _trim(value: Any, *, limit: int = 4000) -> str:
    return str(value or "").replace("\r\n", "\n").strip()[:limit]


def _risk_rank(value: str) -> int:
    return {"low": 1, "medium": 2, "high": 3, "critical": 4}.get(value, 1)


def _normalize_risk(value: str | None, objective: str) -> str:
    if value in {"low", "medium", "high", "critical"}:
        return value
    text = objective.lower()
    if any(term in text for term in HIGH_RISK_TERMS):
        return "high"
    if any(term in text for term in ARCHITECTURE_TERMS + REVIEW_TERMS):
        return "medium"
    return "low"


def infer_codex_work_class(*, lane_id: str, stage_id: str | None = None, objective: str = "") -> str:
    if stage_id and stage_id in STAGE_WORK_CLASS:
        return STAGE_WORK_CLASS[stage_id]
    text = objective.lower()
    if any(term in text for term in REVIEW_TERMS):
        return "code_review"
    if any(term in text for term in ARCHITECTURE_TERMS):
        return "architecture_design"
    if lane_id == "ion_system":
        return "claim_audit"
    if any(term in text for term in STATUS_TERMS):
        return "cheap_classification"
    return "code_patch"


def _selected_model(work_class: str, stage_id: str | None, risk_level: str, context_need: str, posture: str) -> tuple[str, list[str]]:
    reasons = [f"routing_posture:{posture}", f"work_class:{work_class}", f"risk_level:{risk_level}"]
    if context_need in {"huge", "long_horizon"}:
        reasons.append("long_or_huge_context_requires_frontier_lane")
        return "gpt-5.5", reasons
    if _risk_rank(risk_level) >= 4:
        reasons.append("critical_risk_requires_frontier_lane")
        return "gpt-5.5", reasons
    if stage_id in {"steward_route", "vizier_plan", "vice_risk"}:
        reasons.append(f"ion_stage:{stage_id}_requires_authority_or_architecture_lane")
        return "gpt-5.5", reasons
    if stage_id == "nemesis_verify" and _risk_rank(risk_level) >= 3:
        reasons.append("high_risk_nemesis_verification_requires_frontier_lane")
        return "gpt-5.5", reasons
    if work_class in {"architecture_design", "claim_audit", "adversarial_review"}:
        reasons.append("work_class_requires_frontier_reasoning")
        return "gpt-5.5", reasons
    if work_class == "code_review" and _risk_rank(risk_level) >= 3:
        reasons.append("high_risk_code_review_escalates_to_frontier")
        return "gpt-5.5", reasons
    if work_class in {"code_patch", "code_review", "conversation_repair", "long_context_digest"}:
        reasons.append("primary_codex_engineering_lane_is_sufficient")
        return "gpt-5.3-codex", reasons
    if posture == DEFAULT_ROUTING_POSTURE and work_class in {"cheap_classification", "front_stage_claim_classification"}:
        reasons.append("low_risk_fast_work_conserves_frontier_usage")
        return "gpt-5.3-codex-spark", reasons
    if stage_id == "relay_ingress":
        reasons.append("relay_ingress_uses_fast_classification_lane")
        return "gpt-5.3-codex-spark", reasons
    if stage_id in {"relay_return", "persona_response"}:
        reasons.append("user_visible_synthesis_defaults_to_frontier_medium")
        return "gpt-5.5", reasons
    reasons.append("fallback_primary_codex_lane")
    return "gpt-5.3-codex", reasons


def _selected_effort(model: str, work_class: str, stage_id: str | None, risk_level: str, context_need: str) -> str:
    if _risk_rank(risk_level) >= 4 or context_need in {"huge", "long_horizon"}:
        return "xhigh"
    if stage_id in {"vizier_plan", "vice_risk"}:
        return "high"
    if stage_id == "steward_route":
        return "high"
    if work_class in {"architecture_design", "claim_audit", "adversarial_review", "code_review"}:
        return "high"
    if work_class == "code_patch":
        return "high" if _risk_rank(risk_level) >= 3 else "medium"
    if model == "gpt-5.3-codex-spark":
        return "low" if risk_level == "low" else "medium"
    return "medium"


def list_codex_model_profiles() -> dict[str, Any]:
    return {
        "schema_id": MODEL_PROFILE_SCHEMA_ID,
        "version": VERSION,
        "verdict": READY_VERDICT,
        "default_routing_posture": DEFAULT_ROUTING_POSTURE,
        "profiles": CODEX_MODEL_PROFILES,
        "usage_limits_authoritative": False,
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_codex_model_move_plan(
    root: str | Path | None = None,
    *,
    lane_id: str,
    stage_id: str | None = None,
    work_class: str | None = None,
    objective: str = "",
    risk_level: str | None = None,
    context_need: str = "medium",
    routing_posture: str = DEFAULT_ROUTING_POSTURE,
    emitted_at: str | None = None,
) -> dict[str, Any]:
    text = _trim(objective)
    resolved_work_class = work_class or infer_codex_work_class(lane_id=lane_id, stage_id=stage_id, objective=text)
    resolved_risk = _normalize_risk(risk_level, text)
    model, reasons = _selected_model(resolved_work_class, stage_id, resolved_risk, context_need, routing_posture)
    effort = _selected_effort(model, resolved_work_class, stage_id, resolved_risk, context_need)
    profile = dict(CODEX_MODEL_PROFILES.get(model) or CODEX_MODEL_PROFILES["gpt-5.3-codex"])
    ts = emitted_at or _now()
    root_text = Path(root).expanduser().resolve().as_posix() if root else None
    return {
        "schema_id": SCHEMA_ID,
        "version": VERSION,
        "verdict": READY_VERDICT,
        "model_move_id": "codex_model_move_" + _stable_id(lane_id, stage_id or "none", resolved_work_class, resolved_risk, text, ts),
        "emitted_at": ts,
        "workspace_root": root_text,
        "routing_posture": routing_posture,
        "lane_id": lane_id,
        "ion_stage_id": stage_id,
        "work_class": resolved_work_class,
        "risk_level": resolved_risk,
        "context_need": context_need,
        "selected_model": model,
        "selected_reasoning_effort": effort,
        "usage_pool_id": profile.get("usage_pool_id"),
        "usage_pool_authority": profile.get("usage_pool_authority"),
        "limit_authority": profile.get("limit_authority"),
        "usage_limits_authoritative": False,
        "selection_reason": reasons,
        "model_profile": profile,
        "config_overrides": {
            "model": model,
            "model_reasoning_effort": effort,
        },
        "codex_exec_args": codex_exec_args_from_model_move({"selected_model": model, "selected_reasoning_effort": effort}),
        "command_preview": ["codex", "exec", *codex_exec_args_from_model_move({"selected_model": model, "selected_reasoning_effort": effort})],
        "receipt_fields_required": [
            "ion_stage_id",
            "work_class",
            "selected_model",
            "selected_reasoning_effort",
            "usage_pool_id",
            "model_move_id",
            "prompt_path",
            "run_packet_path",
            "tests_run",
        ],
        "provider_api_dispatch_authorized": False,
        "production_authority": False,
        "live_execution_authority": False,
        "claim_boundary": [
            "Model move plans configure Codex CLI invocation only.",
            "Usage-pool labels are operator-observed hints until externally verified.",
            "This plan does not authorize production, provider API dispatch, credentials, shell expansion, or state acceptance.",
        ],
    }


def build_stage_model_move_matrix(stages: Sequence[Sequence[Any]], *, routing_posture: str = DEFAULT_ROUTING_POSTURE) -> list[dict[str, Any]]:
    matrix = []
    for stage in stages:
        stage_id = str(stage[0])
        label = str(stage[1]) if len(stage) > 1 else stage_id
        description = str(stage[2]) if len(stage) > 2 else ""
        plan = build_codex_model_move_plan(
            lane_id="ion_system",
            stage_id=stage_id,
            objective=f"{label}: {description}",
            routing_posture=routing_posture,
        )
        matrix.append(plan)
    return matrix


def codex_exec_args_from_model_move(model_move: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(model_move, Mapping):
        return []
    model = str(model_move.get("selected_model") or "").strip()
    effort = str(model_move.get("selected_reasoning_effort") or "").strip()
    args: list[str] = []
    if model:
        args.extend(["-m", model])
    if effort in REASONING_EFFORTS:
        args.extend(["-c", f"model_reasoning_effort={effort}"])
    return args


def summarize_model_move(model_move: Mapping[str, Any] | None) -> str:
    if not isinstance(model_move, Mapping):
        return "model move unavailable"
    return (
        f"{model_move.get('selected_model')} / {model_move.get('selected_reasoning_effort')} "
        f"for {model_move.get('work_class')} ({model_move.get('routing_posture')})"
    )


def _jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(val) for key, val in value.items()}
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic Codex CLI model-move plan.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--lane-id", default="codex_general")
    parser.add_argument("--stage-id", default=None)
    parser.add_argument("--work-class", default=None)
    parser.add_argument("--objective", default="")
    parser.add_argument("--risk-level", default=None)
    parser.add_argument("--context-need", default="medium")
    parser.add_argument("--profiles", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = list_codex_model_profiles() if args.profiles else build_codex_model_move_plan(
        args.ion_root,
        lane_id=args.lane_id,
        stage_id=args.stage_id,
        work_class=args.work_class,
        objective=args.objective,
        risk_level=args.risk_level,
        context_need=args.context_need,
    )
    if args.json or args.profiles:
        print(json.dumps(_jsonable(payload), indent=2, sort_keys=True))
    else:
        print(summarize_model_move(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
