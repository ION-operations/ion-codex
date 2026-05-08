"""Candidate AI Assistant Work route compiler.

This module reads the imported `ai_assistant_work` candidate lane and projects
route metadata for Codex Chat. It is intentionally candidate-gated: it does not
promote domains, agents, routes, or templates into accepted ION registry law.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:  # pragma: no cover - dependency availability is environment-specific
    import yaml
except Exception:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


SCHEMA_ID = "ion.assistant_work_route_compiler.v0_1"
SURFACE_SCHEMA_ID = "ion.assistant_work_route_surface.v0_1"
READY_VERDICT = "ION_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_READY"
UNAVAILABLE_VERDICT = "ION_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_UNAVAILABLE"

AIW_ROOT = Path("ION/05_context/current/ai_assistant_work")
ROUTE_REGISTRY_PATH = AIW_ROOT / "registries/AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml"
ROUTE_COMPILER_DIR = AIW_ROOT / "route_compiler"
LIFECYCLE_REGISTRY_PATH = AIW_ROOT / "candidate_lifecycle/CANDIDATE_DOMAIN_LIFECYCLE_REGISTRY_V0_1.yaml"

ROUTE_COMPILER_ENABLED_LIFECYCLE_STATES = frozenset(
    {
        "operational_candidate",
        "proof_gated_candidate",
        "promotion_candidate",
        "accepted_operational_domain",
        "canonical_domain_or_law",
    }
)
ROUTE_COMPILER_DISABLED_LIFECYCLE_STATES = frozenset(
    {
        "raw_observation",
        "candidate_draft",
        "deferred",
        "rejected",
        "archived",
    }
)

FALLBACK_ROUTE_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("route.ui_specialist_work", ("ui", "ux", "frontend", "interface", "screen", "component", "accessibility", "a11y", "drawer")),
    ("route.documentation_specialist_work", ("docs", "documentation", "readme", "changelog", "api docs", "technical writing")),
    ("route.assistant_work_dataset_build", ("dataset", "taxonomy", "failure mode", "assistant work", "work pattern")),
    ("route.ide_agent_work_map", ("codex", "ide", "workspace", "codebase", "terminal", "test", "debug", "refactor")),
    ("route.cross_domain_feature_delivery", ("build feature", "ship", "full stack", "release", "product")),
    ("route.assistant_identity_definition", ("what is an ai assistant", "assistant ontology", "host body", "embodiment")),
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _resolve_root(root: str | Path | None = None) -> Path:
    return Path(root or ".").expanduser().resolve()


def _read_yaml(path: Path) -> dict[str, Any] | None:
    if yaml is None or not path.exists():
        return None
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _as_list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _clean_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").lower()).strip()


def _latest_candidate_map(shell_root: Path) -> dict[str, Any] | None:
    base = shell_root / ROUTE_COMPILER_DIR
    if not base.exists():
        return None
    candidates = sorted(base.glob("AI_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_MAP_*.json"))
    if not candidates:
        return None
    payload = _read_json(candidates[-1])
    if not isinstance(payload, dict):
        return None
    payload["_source_path"] = candidates[-1].relative_to(shell_root).as_posix()
    return payload


def _route_map_by_id(candidate_map: Mapping[str, Any] | None) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not isinstance(candidate_map, Mapping):
        return result
    for raw in _as_list(candidate_map.get("route_mappings")):
        if isinstance(raw, Mapping) and raw.get("route_id"):
            result[str(raw["route_id"])] = dict(raw)
    return result


def _registry_routes(registry: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    routes: list[dict[str, Any]] = []
    if not isinstance(registry, Mapping):
        return routes
    for raw in _as_list(registry.get("routes")):
        if isinstance(raw, Mapping) and raw.get("route_id"):
            routes.append(dict(raw))
    return routes


def _candidate_lifecycle_records(lifecycle_registry: Mapping[str, Any] | None) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    if not isinstance(lifecycle_registry, Mapping):
        return records
    raw_records = _as_list(lifecycle_registry.get("lifecycle_records")) or _as_list(lifecycle_registry.get("candidates"))
    for raw in raw_records:
        if not isinstance(raw, Mapping):
            continue
        candidate_id = raw.get("candidate_id") or raw.get("id")
        if candidate_id:
            records[str(candidate_id)] = dict(raw)
    return records


def _lifecycle_state(record: Mapping[str, Any] | None) -> str:
    if not isinstance(record, Mapping):
        return "unrecorded_candidate"
    state = _clean_text(record.get("lifecycle_state"))
    return state or "candidate_draft"


def _route_lifecycle_enabled(record: Mapping[str, Any] | None) -> bool:
    if not isinstance(record, Mapping):
        return True
    state = _lifecycle_state(record)
    if state in ROUTE_COMPILER_DISABLED_LIFECYCLE_STATES:
        return False
    if state not in ROUTE_COMPILER_ENABLED_LIFECYCLE_STATES:
        return False
    return bool(record.get("route_compiler_enabled", True))


def _lifecycle_summary(candidate_id: str | None, record: Mapping[str, Any] | None) -> dict[str, Any]:
    if not candidate_id:
        return {
            "candidate_id": None,
            "lifecycle_state": "unselected",
            "route_compiler_enabled": False,
            "source": "no_candidate_selected",
        }
    if not isinstance(record, Mapping):
        return {
            "candidate_id": candidate_id,
            "lifecycle_state": "unrecorded_candidate",
            "route_compiler_enabled": True,
            "source": "missing_lifecycle_record_default_active",
        }
    return {
        "candidate_id": candidate_id,
        "candidate_type": record.get("candidate_type"),
        "lifecycle_state": _lifecycle_state(record),
        "route_compiler_enabled": _route_lifecycle_enabled(record),
        "scorecard_path": record.get("scorecard_path"),
        "source": "candidate_lifecycle_registry",
    }


def _filter_lifecycle_enabled_routes(
    routes: list[dict[str, Any]],
    lifecycle_records: Mapping[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    active: list[dict[str, Any]] = []
    inactive_ids: list[str] = []
    for route in routes:
        route_id = str(route.get("route_id") or "")
        if not route_id:
            continue
        record = lifecycle_records.get(route_id)
        if _route_lifecycle_enabled(record):
            active.append(route)
        else:
            inactive_ids.append(route_id)
    return active, inactive_ids


def _score_route(route: Mapping[str, Any], text: str) -> tuple[int, list[str]]:
    score = 0
    matched: list[str] = []
    for raw_pattern in _as_list(route.get("trigger_patterns")):
        pattern = _clean_text(raw_pattern)
        if not pattern:
            continue
        if pattern in text:
            score += 30 + min(len(pattern), 30)
            matched.append(pattern)
            continue
        tokens = [token for token in re.split(r"[^a-z0-9]+", pattern) if len(token) >= 4]
        token_hits = sum(1 for token in tokens if token in text)
        if tokens and token_hits >= max(1, min(2, len(tokens))):
            score += token_hits * 6
            matched.append(pattern)
    for route_id, terms in FALLBACK_ROUTE_KEYWORDS:
        if str(route.get("route_id")) != route_id:
            continue
        hits = [term for term in terms if term in text]
        if hits:
            score += 12 * len(hits)
            matched.extend(hits)
    return score, sorted(set(matched))


def _fallback_route_id(*, text: str, response_mode: str | None, selected_skill_id: str | None) -> str:
    if response_mode == "ion_handoff" or selected_skill_id == "ion-full-workflow-handoff":
        return "route.cross_domain_feature_delivery"
    if response_mode == "queue_work" or selected_skill_id == "codex-solo-work":
        if any(term in text for term in ("ui", "ux", "frontend", "interface", "screen", "component")):
            return "route.ui_specialist_work"
        if any(term in text for term in ("docs", "documentation", "readme", "api docs")):
            return "route.documentation_specialist_work"
        return "route.ide_agent_work_map"
    if selected_skill_id == "template-curation":
        return "route.assistant_work_dataset_build"
    return "route.assistant_identity_definition" if "assistant" in text and ("what" in text or "ontology" in text) else "route.ide_agent_work_map"


def _select_route(
    routes: list[dict[str, Any]],
    *,
    message: str,
    response_mode: str | None,
    selected_skill_id: str | None,
) -> tuple[dict[str, Any] | None, int, list[str], str]:
    text = _clean_text(message)
    best: dict[str, Any] | None = None
    best_score = -1
    best_matches: list[str] = []
    for route in routes:
        score, matched = _score_route(route, text)
        if score > best_score:
            best = route
            best_score = score
            best_matches = matched
    if best is not None and best_score > 0:
        return best, best_score, best_matches, "trigger_match"
    fallback_id = _fallback_route_id(text=text, response_mode=response_mode, selected_skill_id=selected_skill_id)
    for route in routes:
        if route.get("route_id") == fallback_id:
            return route, 1, [f"fallback:{fallback_id}"], "fallback"
    return best, max(best_score, 0), best_matches, "best_available"


def build_assistant_work_route_surface(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    findings: list[str] = []
    if yaml is None:
        findings.append("pyyaml_unavailable")
    registry = _read_yaml(shell_root / ROUTE_REGISTRY_PATH)
    if registry is None:
        findings.append(f"route_registry_missing_or_invalid:{ROUTE_REGISTRY_PATH.as_posix()}")
    candidate_map = _latest_candidate_map(shell_root)
    all_routes = _registry_routes(registry)
    lifecycle_registry = _read_yaml(shell_root / LIFECYCLE_REGISTRY_PATH)
    if lifecycle_registry is None:
        findings.append(f"lifecycle_registry_missing_or_invalid:{LIFECYCLE_REGISTRY_PATH.as_posix()}")
    lifecycle_records = _candidate_lifecycle_records(lifecycle_registry)
    routes, inactive_route_ids = _filter_lifecycle_enabled_routes(all_routes, lifecycle_records)
    if all_routes and not routes:
        findings.append("no_lifecycle_enabled_routes")
    route_map = _route_map_by_id(candidate_map)
    ok = bool(registry) and bool(routes) and yaml is not None
    return {
        "schema_id": SURFACE_SCHEMA_ID,
        "verdict": READY_VERDICT if ok else UNAVAILABLE_VERDICT,
        "ok": ok,
        "candidate_only": True,
        "generated_at": _now(),
        "root": AIW_ROOT.as_posix(),
        "route_registry_path": ROUTE_REGISTRY_PATH.as_posix(),
        "lifecycle_registry_path": LIFECYCLE_REGISTRY_PATH.as_posix(),
        "candidate_map_path": candidate_map.get("_source_path") if isinstance(candidate_map, Mapping) else None,
        "total_route_count": len(all_routes),
        "route_count": len(routes),
        "route_ids": [str(route.get("route_id")) for route in routes if route.get("route_id")],
        "inactive_route_count": len(inactive_route_ids),
        "inactive_route_ids": inactive_route_ids,
        "lifecycle_record_count": len(lifecycle_records),
        "mapped_route_count": len(route_map),
        "findings": findings,
        "policy": "candidate_route_metadata_only_no_registry_or_product_law_mutation",
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }


def compile_assistant_work_route(
    root: str | Path | None = None,
    *,
    message: str,
    lane_id: str,
    response_mode: str | None = None,
    selected_skill_id: str | None = None,
    execution_mode: str | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    surface = build_assistant_work_route_surface(shell_root)
    registry = _read_yaml(shell_root / ROUTE_REGISTRY_PATH)
    lifecycle_registry = _read_yaml(shell_root / LIFECYCLE_REGISTRY_PATH)
    lifecycle_records = _candidate_lifecycle_records(lifecycle_registry)
    routes, inactive_route_ids = _filter_lifecycle_enabled_routes(_registry_routes(registry), lifecycle_records)
    candidate_map = _latest_candidate_map(shell_root)
    mapped_routes = _route_map_by_id(candidate_map)
    if not surface.get("ok") or not routes:
        return {
            "schema_id": SCHEMA_ID,
            "verdict": UNAVAILABLE_VERDICT,
            "ok": False,
            "candidate_only": True,
            "generated_at": _now(),
            "lane_id": lane_id,
            "response_mode": response_mode,
            "selected_skill_id": selected_skill_id,
            "execution_mode": execution_mode,
            "route_id": None,
            "finding": "assistant_work_candidate_route_registry_unavailable",
            "surface": surface,
            "policy": "chat_continues_without_candidate_assistant_work_route",
            "production_authority": False,
            "live_execution_authority": False,
            "secrets_authority": False,
        }
    route, score, matches, selection_basis = _select_route(
        routes,
        message=message,
        response_mode=response_mode,
        selected_skill_id=selected_skill_id,
    )
    route_id = str(route.get("route_id")) if isinstance(route, Mapping) and route.get("route_id") else None
    lifecycle_record = lifecycle_records.get(route_id or "")
    mapped = mapped_routes.get(route_id or "", {})
    output_contract = route.get("output_contract") if isinstance(route, Mapping) and isinstance(route.get("output_contract"), Mapping) else {}
    return {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT,
        "ok": True,
        "candidate_only": True,
        "generated_at": _now(),
        "lane_id": lane_id,
        "response_mode": response_mode,
        "selected_skill_id": selected_skill_id,
        "execution_mode": execution_mode,
        "route_id": route_id,
        "selection_basis": selection_basis,
        "score": score,
        "matched_triggers": matches,
        "candidate_lifecycle": _lifecycle_summary(route_id, lifecycle_record),
        "candidate_domains": _as_list((route or {}).get("required_domains")) or _as_list(mapped.get("candidate_domains")),
        "candidate_agents": _as_list((route or {}).get("primary_agents")) or _as_list(mapped.get("candidate_agents")),
        "active_skill_candidates": _as_list(mapped.get("active_skill_candidates")),
        "active_lens_candidates": _as_list(mapped.get("active_lens_candidates")),
        "template_spec_candidates": _as_list(mapped.get("template_spec_candidates")),
        "output_contract": {
            "include": _as_list(output_contract.get("include")),
            "forbid": _as_list(output_contract.get("forbid")),
        },
        "active_behavior": mapped.get("active_behavior"),
        "promotion_target": mapped.get("promotion_target"),
        "surface": {
            "route_registry_path": surface.get("route_registry_path"),
            "lifecycle_registry_path": surface.get("lifecycle_registry_path"),
            "route_count": surface.get("route_count"),
            "total_route_count": surface.get("total_route_count"),
            "inactive_route_count": surface.get("inactive_route_count"),
            "inactive_route_ids": inactive_route_ids,
            "mapped_route_count": surface.get("mapped_route_count"),
        },
        "policy": "candidate_route_metadata_only_no_registry_or_product_law_mutation",
        "authority_boundary": {
            "candidate_only": True,
            "mutates_ION_03_registry": False,
            "mutates_product_front_door": False,
            "production_authority": False,
            "live_execution_authority": False,
        },
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }
