"""Codex Chat Engine for Capsule-backed ION chat turns.

The engine owns turn interpretation: context mount, skill activation, native
lens selection, model move, response mode, and response contract. It does not
render UI and it does not call a provider directly.
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

from .ion_codex_model_moves import build_codex_model_move_plan, summarize_model_move
from .ion_assistant_work_route_compiler import (
    build_assistant_work_route_surface,
    compile_assistant_work_route,
)
from .ion_codex_solo_context import (
    CAPSULE_PATH,
    CONTEXT_PACKAGES_PATH,
    HOT_CONTEXT_PATH,
    LONG_HORIZON_PATH,
    MINI_PATH,
    ROUTE_PATH,
    WITNESS_POLICY,
    build_codex_solo_context_model,
)
from .ion_skill_activation import build_ion_skill_activation


SCHEMA_ID = "ion.codex_chat_engine_turn.v1"
SURFACE_SCHEMA_ID = "ion.codex_chat_engine_surface.v1"
REGISTRY_SCHEMA_ID = "ion.native_lens_registry.v1"
READY_VERDICT = "ION_CODEX_CHAT_ENGINE_READY"
BLOCKED_VERDICT = "ION_CODEX_CHAT_ENGINE_BLOCKED"

CHAT_ENGINE_PROTOCOL_PATH = Path("ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md")
NATIVE_LENS_REGISTRY_PATH = Path("ION/03_registry/ion_native_lens_registry.yaml")

QUEUE_EXECUTION_MODES = {"queue_for_codex", "queue_and_start"}

IMPLEMENTATION_TERMS = (
    "implement",
    "build",
    "fix",
    "change",
    "update",
    "wire",
    "connect",
    "add",
    "remove",
    "delete",
    "refactor",
    "test",
    "run",
)
PLAN_TERMS = ("plan", "orchestrate", "design", "architecture", "schema", "protocol", "roadmap")
RECOVERY_TERMS = ("recover", "drift", "wrong root", "broken", "failure", "forensic", "confusing", "lost")
VERIFY_TERMS = ("verify", "audit", "review", "regression", "proof", "receipt", "nemesis")
ION_HANDOFF_TERMS = ("full ion", "relay", "steward", "persona", "ion workflow", "handoff")
TEMPLATE_TERMS = ("skill", "template", "binding", "proof contract", "governance")
RESEARCH_TERMS = ("research", "look into", "explain", "why", "how does", "what is")
HIGH_RISK_TERMS = ("production", "deploy", "secret", "credential", "token", "cloudflare", "systemd", "delete", "public")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _resolve_root(root: str | Path | None = None) -> Path:
    return Path(root or ".").expanduser().resolve()


def _read_yaml(path: Path) -> dict[str, Any] | None:
    if not path.exists() or yaml is None:
        return None
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else None


def _as_list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _as_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _trim(value: Any, *, limit: int = 4000) -> str:
    return str(value or "").replace("\r\n", "\n").strip()[:limit]


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _safe_summary(value: Any, *, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text[:limit]


def load_native_lens_registry(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    protocol_path = shell_root / CHAT_ENGINE_PROTOCOL_PATH
    registry_path = shell_root / NATIVE_LENS_REGISTRY_PATH
    findings: list[str] = []
    if yaml is None:
        findings.append("pyyaml_unavailable")
    if not protocol_path.exists():
        findings.append(f"chat_engine_protocol_missing:{CHAT_ENGINE_PROTOCOL_PATH.as_posix()}")
    payload = _read_yaml(registry_path)
    if payload is None:
        findings.append(f"native_lens_registry_missing_or_invalid:{NATIVE_LENS_REGISTRY_PATH.as_posix()}")
        return {
            "schema_id": REGISTRY_SCHEMA_ID,
            "verdict": BLOCKED_VERDICT,
            "ok": False,
            "registry_path": NATIVE_LENS_REGISTRY_PATH.as_posix(),
            "protocol_path": CHAT_ENGINE_PROTOCOL_PATH.as_posix(),
            "findings": findings,
            "lenses": [],
            "lens_count": 0,
            "production_authority": False,
            "live_execution_authority": False,
            "secrets_authority": False,
        }
    for key in ("production_authority", "live_execution_authority", "secrets_authority"):
        if payload.get(key) is not False:
            findings.append(f"{key}_must_be_false")
    lenses: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in _as_list(payload.get("lenses")):
        if not isinstance(raw, Mapping):
            findings.append("lens_entry_not_object")
            continue
        lens = dict(raw)
        lens_id = str(lens.get("lens_id") or "").strip()
        if not lens_id:
            findings.append("lens_id_missing")
            continue
        if lens_id in seen:
            findings.append(f"lens_id_duplicate:{lens_id}")
            continue
        seen.add(lens_id)
        lenses.append(lens)
    ok = not findings
    return {
        **payload,
        "schema_id": REGISTRY_SCHEMA_ID,
        "verdict": READY_VERDICT if ok else BLOCKED_VERDICT,
        "ok": ok,
        "generated_at": _now(),
        "registry_path": NATIVE_LENS_REGISTRY_PATH.as_posix(),
        "protocol_path": CHAT_ENGINE_PROTOCOL_PATH.as_posix(),
        "findings": findings,
        "lenses": lenses,
        "lens_count": len(lenses),
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }


def classify_response_mode(*, lane_id: str, message: str, execution_mode: str | None = None) -> str:
    text = message.lower()
    if lane_id == "ion_system" or _contains_any(text, ION_HANDOFF_TERMS):
        return "ion_handoff"
    if _contains_any(text, RECOVERY_TERMS):
        return "recover"
    if execution_mode in QUEUE_EXECUTION_MODES:
        return "queue_work"
    if _contains_any(text, PLAN_TERMS) and not _contains_any(text, IMPLEMENTATION_TERMS):
        return "plan"
    if text.count("?") >= 3 and len(text) < 220:
        return "clarify"
    return "answer"


def _stage_for_mode(response_mode: str, skill_id: str | None) -> str:
    if response_mode == "queue_work" or skill_id == "codex-solo-work":
        return "mason_codex_work"
    if response_mode == "recover" or skill_id == "codex-recovery":
        return "steward_route"
    if response_mode == "plan":
        return "vizier_plan"
    if response_mode == "ion_handoff" or skill_id == "ion-full-workflow-handoff":
        return "relay_ingress"
    if skill_id == "template-curation":
        return "vizier_plan"
    return "persona_response"


def _lens_by_id(registry: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for raw in _as_list(registry.get("lenses")):
        if isinstance(raw, Mapping) and raw.get("lens_id"):
            result[str(raw["lens_id"])] = dict(raw)
    return result


def _select_lens_ids(*, response_mode: str, skill_id: str | None, message: str) -> list[str]:
    text = message.lower()
    selected = ["persona", "context_cartographer"]
    if response_mode == "ion_handoff":
        selected.extend(["relay", "steward"])
    if response_mode == "queue_work" or skill_id == "codex-solo-work" or _contains_any(text, IMPLEMENTATION_TERMS):
        selected.extend(["steward", "mason_codex", "scribe"])
    if response_mode == "recover" or skill_id == "codex-recovery":
        selected.extend(["steward", "nemesis", "vestige", "vice"])
    if response_mode == "plan" or _contains_any(text, PLAN_TERMS):
        selected.extend(["vizier", "steward"])
    if _contains_any(text, VERIFY_TERMS):
        selected.extend(["nemesis", "scribe"])
    if _contains_any(text, TEMPLATE_TERMS) or skill_id == "template-curation":
        selected.extend(["template_curator", "ionologist"])
    if _contains_any(text, RESEARCH_TERMS):
        selected.append("thoth")
    if _contains_any(text, HIGH_RISK_TERMS):
        selected.extend(["steward", "nemesis", "vice"])
    deduped: list[str] = []
    for lens_id in selected:
        if lens_id not in deduped:
            deduped.append(lens_id)
    return deduped


def _select_native_lenses(registry: Mapping[str, Any], *, response_mode: str, skill_id: str | None, message: str) -> list[dict[str, Any]]:
    indexed = _lens_by_id(registry)
    lenses: list[dict[str, Any]] = []
    for lens_id in _select_lens_ids(response_mode=response_mode, skill_id=skill_id, message=message):
        lens = indexed.get(lens_id)
        if not lens:
            continue
        lenses.append({
            "lens_id": lens.get("lens_id"),
            "display_name": lens.get("display_name"),
            "role_id": lens.get("role_id"),
            "purpose": lens.get("purpose"),
            "model_stage_id": lens.get("model_stage_id"),
            "template_refs": _as_list(lens.get("template_refs")),
        })
    return lenses


def _context_refs(codex_solo_context: Mapping[str, Any]) -> list[str]:
    refs = [
        CAPSULE_PATH.as_posix(),
        HOT_CONTEXT_PATH.as_posix(),
        MINI_PATH.as_posix(),
        LONG_HORIZON_PATH.as_posix(),
        CONTEXT_PACKAGES_PATH.as_posix(),
        ROUTE_PATH.as_posix(),
    ]
    route = codex_solo_context.get("route") if isinstance(codex_solo_context.get("route"), Mapping) else {}
    entries = route.get("entries") if isinstance(route.get("entries"), list) else []
    for entry in entries:
        if isinstance(entry, Mapping) and entry.get("path"):
            path = str(entry["path"])
            if path not in refs:
                refs.append(path)
    return refs


def _latest_capsule_summary(codex_solo_context: Mapping[str, Any]) -> str:
    capsule = codex_solo_context.get("capsule") if isinstance(codex_solo_context.get("capsule"), Mapping) else {}
    rows = capsule.get("recent_rows") if isinstance(capsule.get("recent_rows"), list) else []
    latest = rows[-1] if rows and isinstance(rows[-1], Mapping) else {}
    return str(latest.get("summary") or "No capsule receipt rows yet.")


def _carrier_strategy(response_mode: str) -> dict[str, Any]:
    if response_mode == "queue_work":
        mode = "existing_codex_work_queue"
        request_kind = "codex_work"
    elif response_mode == "ion_handoff":
        mode = "existing_ion_relay_steward_projection"
        request_kind = "ion_handoff"
    else:
        mode = "gpt_5_5_codex_chat_response_contract"
        request_kind = "codex_chat_response"
    return {
        "mode": mode,
        "request_kind": request_kind,
        "uses_existing_queue": response_mode == "queue_work",
        "direct_provider_api": False,
        "raw_hidden_reasoning_exposed": False,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _compose_local_response(
    *,
    message: str,
    response_mode: str,
    skill_activation: Mapping[str, Any],
    native_lenses: list[Mapping[str, Any]],
    codex_solo_context: Mapping[str, Any],
    model_move: Mapping[str, Any],
) -> str:
    skill_name = skill_activation.get("display_name") or "Codex Chat"
    lens_names = ", ".join(str(lens.get("display_name")) for lens in native_lenses[:4] if lens.get("display_name"))
    latest = _latest_capsule_summary(codex_solo_context)
    model = model_move.get("selected_model") or "gpt-5.5"
    effort = model_move.get("selected_reasoning_effort") or "medium"
    if response_mode == "queue_work":
        return "\n".join([
            "I’ll treat this as bounded Codex work.",
            "",
            f"The active route is {skill_name}, with {lens_names or 'ION native lenses'} behind it. The work should go through the existing Codex queue, return with context proof and template action proof, and only then be treated as admissible.",
            "",
            f"Current Capsule basis: {latest}",
            f"Model move: {model} / {effort}.",
        ])
    if response_mode == "recover":
        return "\n".join([
            "I’ll handle this as recovery first.",
            "",
            "That means I should verify root, context, recent receipts, and the failed assumption before changing anything. The Recovery skill should use Steward/Nemesis/Vestige pressure instead of moving directly into implementation.",
            "",
            f"Current Capsule basis: {latest}",
        ])
    if response_mode == "plan":
        return "\n".join([
            "I’ll plan this before implementation.",
            "",
            f"I’m routing through {skill_name} with {lens_names or 'Vizier/Steward context'} and keeping the output as an executable plan until you ask for work to run.",
            "",
            f"Current Capsule basis: {latest}",
        ])
    if response_mode == "ion_handoff":
        return "\n".join([
            "I’ll route this toward the full ION workflow rather than treating it as standalone Codex chat.",
            "",
            "Relay and Steward should normalize the request, check authority, and decide which native roles are useful. This chat remains a front door and evidence surface, not a second ION queue.",
        ])
    if response_mode == "clarify":
        return "I can do that, but I need one concrete target or success condition before I route it into ION/Codex work."
    return "\n".join([
        "I’m mounted on the Codex Capsule context and can answer from this lane.",
        "",
        f"Nearest state: {latest}",
        f"Active route: {skill_name}; native lenses: {lens_names or 'Persona and Context Cartographer'}.",
        "",
        "For a full model-quality answer, this turn should be carried by the GPT-5.5 Codex chat response contract. For implementation, use Run task so the same message goes through the proof-gated Codex queue.",
    ])


def _response_contract(response_mode: str) -> dict[str, Any]:
    sections = ["answer"]
    if response_mode in {"plan", "queue_work", "recover", "ion_handoff"}:
        sections = ["answer", "reasoned_route", "next_action"]
    return {
        "schema_id": "ion.codex_chat_response_contract.v1",
        "quality_target": "chatgpt_browser_level_or_better",
        "response_mode": response_mode,
        "required_user_visible_sections": sections,
        "must_be_conversational": True,
        "must_not_expose_raw_hidden_reasoning": True,
        "must_not_make_unproved_state_claims": True,
        "must_use_context_refs_when_claiming_project_state": True,
        "template_proof_required_for_mutation": True,
        "receipt_required_for_material_work": True,
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_codex_chat_engine_turn(
    root: str | Path | None = None,
    *,
    lane_id: str,
    message: str,
    execution_mode: str | None = None,
    codex_solo_context: Mapping[str, Any] | None = None,
    codex_status: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    text = _trim(message)
    codex_solo = dict(codex_solo_context) if isinstance(codex_solo_context, Mapping) else build_codex_solo_context_model(shell_root, write=True)
    response_mode = classify_response_mode(lane_id=lane_id, message=text, execution_mode=execution_mode)
    initial_skill = build_ion_skill_activation(
        shell_root,
        lane_id=lane_id,
        objective=text,
        execution_mode=execution_mode,
        codex_solo_context=codex_solo,
    )
    stage_id = _stage_for_mode(response_mode, str(initial_skill.get("skill_id") or ""))
    model_move = build_codex_model_move_plan(shell_root, lane_id=lane_id, stage_id=stage_id, objective=text)
    skill_activation = build_ion_skill_activation(
        shell_root,
        lane_id=lane_id,
        objective=text,
        execution_mode=execution_mode,
        codex_solo_context=codex_solo,
        model_move=model_move,
    )
    registry = load_native_lens_registry(shell_root)
    native_lenses = _select_native_lenses(
        registry,
        response_mode=response_mode,
        skill_id=str(skill_activation.get("skill_id") or ""),
        message=text,
    )
    assistant_work_route = compile_assistant_work_route(
        shell_root,
        lane_id=lane_id,
        message=text,
        response_mode=response_mode,
        selected_skill_id=str(skill_activation.get("skill_id") or ""),
        execution_mode=execution_mode,
    )
    contract = _response_contract(response_mode)
    carrier = _carrier_strategy(response_mode)
    assistant_response = _compose_local_response(
        message=text,
        response_mode=response_mode,
        skill_activation=skill_activation,
        native_lenses=native_lenses,
        codex_solo_context=codex_solo,
        model_move=model_move,
    )
    context_refs = _context_refs(codex_solo)
    turn = {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT if registry.get("ok") and skill_activation.get("ok") and codex_solo.get("ok") else BLOCKED_VERDICT,
        "ok": bool(registry.get("ok")) and bool(skill_activation.get("ok")) and bool(codex_solo.get("ok")),
        "generated_at": _now(),
        "lane_id": lane_id,
        "operator_message_summary": _safe_summary(text),
        "response_mode": response_mode,
        "selected_skill": {
            "skill_id": skill_activation.get("skill_id"),
            "display_name": skill_activation.get("display_name"),
            "selection_reason": skill_activation.get("selection_reason"),
        },
        "skill_activation": skill_activation,
        "native_lenses": native_lenses,
        "assistant_work_route": assistant_work_route,
        "model_move": model_move,
        "model_move_summary": summarize_model_move(model_move),
        "context_mount": {
            "witness_policy": WITNESS_POLICY,
            "context_ok": codex_solo.get("ok"),
            "context_refs": context_refs,
            "minimum_context": CAPSULE_PATH.as_posix(),
            "hot_context": HOT_CONTEXT_PATH.as_posix(),
        },
        "carrier_strategy": carrier,
        "response_contract": contract,
        "assistant_response": assistant_response,
        "queue_recommendation": {
            "should_queue": response_mode == "queue_work",
            "request_kind": carrier.get("request_kind"),
            "existing_queue_only": True,
        },
        "codex_status": {
            "queued_request_count": (codex_status or {}).get("queued_request_count", 0) if isinstance(codex_status, Mapping) else 0,
            "active_process_running": (codex_status or {}).get("active_process_running", False) if isinstance(codex_status, Mapping) else False,
        },
        "authority": {
            "production_authority": False,
            "live_execution_authority": False,
            "secrets_authority": False,
            "state_acceptance_granted": False,
        },
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }
    return json.loads(json.dumps(turn))


def build_codex_chat_carrier_objective(engine_turn: Mapping[str, Any], operator_message: str) -> str:
    lenses = engine_turn.get("native_lenses") if isinstance(engine_turn.get("native_lenses"), list) else []
    lens_lines = "\n".join(
        f"- {lens.get('display_name')} ({lens.get('role_id')}): {lens.get('purpose')}"
        for lens in lenses[:8]
        if isinstance(lens, Mapping)
    ) or "- Persona + Context Cartographer"
    context = engine_turn.get("context_mount") if isinstance(engine_turn.get("context_mount"), Mapping) else {}
    refs = context.get("context_refs") if isinstance(context.get("context_refs"), list) else []
    ref_lines = "\n".join(f"- {ref}" for ref in refs[:16])
    assistant_work_route = engine_turn.get("assistant_work_route") if isinstance(engine_turn.get("assistant_work_route"), Mapping) else {}
    include = ((assistant_work_route.get("output_contract") or {}).get("include") if isinstance(assistant_work_route.get("output_contract"), Mapping) else []) or []
    forbid = ((assistant_work_route.get("output_contract") or {}).get("forbid") if isinstance(assistant_work_route.get("output_contract"), Mapping) else []) or []
    route_lines = "\n".join([
        f"- route_id: {assistant_work_route.get('route_id') or 'unavailable'}",
        f"- candidate_only: {assistant_work_route.get('candidate_only', True)}",
        f"- selected domains: {', '.join(str(item) for item in (assistant_work_route.get('candidate_domains') or [])[:6])}",
        f"- specialist agents: {', '.join(str(item) for item in (assistant_work_route.get('candidate_agents') or [])[:6])}",
        f"- include: {', '.join(str(item) for item in include[:6])}",
        f"- forbid: {', '.join(str(item) for item in forbid[:6])}",
    ])
    return "\n".join([
        "Codex chat response packet.",
        "",
        "Goal:",
        "Produce a high-quality user-facing assistant response for the operator message, using the mounted ION Codex Chat Engine contract.",
        "",
        f"Response mode: {engine_turn.get('response_mode')}",
        f"Selected skill: {((engine_turn.get('selected_skill') or {}).get('display_name') if isinstance(engine_turn.get('selected_skill'), Mapping) else None)}",
        f"Carrier strategy: {((engine_turn.get('carrier_strategy') or {}).get('mode') if isinstance(engine_turn.get('carrier_strategy'), Mapping) else None)}",
        "",
        "Native lenses:",
        lens_lines,
        "",
        "Candidate Assistant Work route:",
        route_lines,
        "",
        "Context policy:",
        f"- {WITNESS_POLICY}",
        f"- Minimum context: {CAPSULE_PATH.as_posix()}",
        f"- Mini is lookup/receipt index only: {MINI_PATH.as_posix()}",
        "",
        "Required context refs:",
        ref_lines,
        "",
        "Response rules:",
        "- Answer conversationally and directly.",
        "- Do not expose raw hidden reasoning.",
        "- Do not turn ION internals into user chores.",
        "- Do not claim production/live authority.",
        "- If state-changing work is needed, say it must go through proof-gated Codex work.",
        "- If you cite project state, ground it in loaded context refs.",
        "",
        "Operator message:",
        _trim(operator_message, limit=6000),
    ])


def build_codex_chat_engine_surface(root: str | Path | None = None) -> dict[str, Any]:
    registry = load_native_lens_registry(root)
    assistant_work_routes = build_assistant_work_route_surface(root)
    return {
        "schema_id": SURFACE_SCHEMA_ID,
        "verdict": registry.get("verdict"),
        "ok": registry.get("ok"),
        "protocol_path": registry.get("protocol_path"),
        "registry_path": registry.get("registry_path"),
        "lens_count": registry.get("lens_count", 0),
        "default_lenses": registry.get("default_lenses", []),
        "lenses": registry.get("lenses", []),
        "assistant_work_routes": assistant_work_routes,
        "response_modes": ["answer", "clarify", "plan", "queue_work", "recover", "ion_handoff"],
        "quality_target": "chatgpt_browser_level_or_better",
        "policy": "chat_engine_routes_context_skills_native_lenses_and_existing_codex_queue",
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }
