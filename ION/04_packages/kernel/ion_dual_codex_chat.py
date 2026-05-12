"""Capsule Codex chat state and projection for the local ION cockpit.

The historical module name remains for import compatibility, but the product
shape is no longer "two chats." The primary surface is one user-facing Codex
Capsule chat. A secondary ION comms adapter keeps visibility into the existing
full ION Relay/Steward/workflow path without creating a second queue, second
agent system, or manual lane chore for the operator.

This module does not call an LLM directly, does not expose arbitrary shell, and
does not grant production or live execution authority. Bounded Codex work still
uses the existing ChatGPT-browser connector work-packet path and proof gates.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ion_chatgpt_browser_mcp_connector_contract import call_chatgpt_connector_tool
from .ion_agent_invocation_broker import agent_queue, list_agents
from .ion_codex_queue_runner import build_codex_queue_runner_status, process_codex_queue_once
from .ion_codex_model_moves import (
    DEFAULT_ROUTING_POSTURE,
    build_codex_model_move_plan,
    build_stage_model_move_matrix,
    list_codex_model_profiles,
    summarize_model_move,
)
from .ion_codex_chat_app_ui import render_codex_chat_app_html
from .ion_cockpit_service_manager import build_service_console_model
from .ion_codex_chat_engine import (
    build_codex_chat_carrier_objective,
    build_codex_chat_engine_surface,
    build_codex_chat_engine_turn,
)
from .ion_codex_chat_memory_visualization import build_codex_chat_memory_visualization
from .ion_codex_chat_response_carrier import (
    RUNS_DIR as RESPONSE_RUNS_DIR,
    build_chat_response_carrier_status,
    run_codex_chat_response_carrier,
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
    record_codex_solo_post,
)
from .ion_skill_activation import build_ion_skill_activation, build_ion_skill_surface

SCHEMA_ID = "ion.codex_capsule_chat_model.v1"
STATE_SCHEMA_ID = "ion.codex_capsule_chat_state.v1"
READY_VERDICT = "ION_CODEX_CAPSULE_CHAT_READY"
WRITE_CONFIRMATION_TOKEN = "ION_BOUNDED_WRITE_CONFIRMED"

CURRENT = Path("ION/05_context/current")
STATE_DIR = CURRENT / "codex_capsule_chat"
STATE_PATH = STATE_DIR / "state.json"
MODEL_PATH = CURRENT / "ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json"
CODEX_WORK_QUEUE_INDEX = CURRENT / "ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json"
CODEX_WORK_REQUESTS_DIR = CURRENT / "chatgpt_connector/codex_work_requests"
CODEX_QUEUE_RUNS_DIR = CURRENT / "chatgpt_connector/codex_queue_runs"
CODEX_TASK_RETURNS_DIR = CURRENT / "chatgpt_connector/task_returns"
CODEX_MEMORY_ENV = "ION_DUAL_CHAT_CODEX_MEMORY_PATH"
DEFAULT_CODEX_MEMORY_PATH = Path("/home/sev/.codex/memories/ion_codex_capsule_chat_memory.md")
CHAT_EXECUTION_MODE_ENV = "ION_CODEX_CAPSULE_CHAT_DEFAULT_EXECUTION_MODE"
CHAT_RUNNER_START_ENV = "ION_CODEX_CAPSULE_CHAT_ALLOW_RUNNER_START"
CHAT_EXECUTION_MODES = ("respond_only", "queue_for_codex", "queue_and_start")
DEFAULT_CHAT_EXECUTION_MODE = "respond_only"
PLAYWRIGHT_COCKPIT_SMOKE_RE = re.compile(r"^playwright-pending-smoke-\d+: reply exactly playwright-ok$")
PLAYWRIGHT_COCKPIT_SMOKE_PERSIST_ENV = "ION_COCKPIT_PLAYWRIGHT_SMOKE_PERSIST"
PLAYWRIGHT_COCKPIT_SMOKE_RESPONSE = "playwright-ok"

LANES = {
    "ion_system": {
        "label": "ION Comms Adapter",
        "purpose": "Secondary bridge to the existing full ION Relay/Steward/workflow surfaces. It is not the primary chat product.",
        "memory_policy": "ION state, proof-gated returns, receipts, and explicit promoted memory only.",
    },
    "codex_general": {
        "label": "Codex Chat",
        "purpose": "Primary user-facing Codex chat using Capsule as minimum context, Mini as lookup index, explicit repo context, and bounded receipts.",
        "memory_policy": "Codex solo Capsule is the minimum working context; Mini indexes receipts; long-horizon epochs and package selector decide older context; no hidden memory claims.",
    },
}

ION_PIPELINE_STAGES = (
    ("relay_ingress", "Relay ingress", "Translate operator text into a bounded semantic packet."),
    ("steward_route", "Steward route", "Classify authority, risk, and work legitimacy."),
    ("vizier_plan", "Vizier plan", "Set architecture, dependencies, and review posture."),
    ("mason_codex_work", "Mason/Codex work", "Execute bounded implementation through Codex queue and proof return."),
    ("vice_risk", "Vice risk pass", "Apply future-answerability and contradiction pressure."),
    ("nemesis_verify", "Nemesis verification", "Audit proof, regressions, and release sensitivity."),
    ("relay_return", "Relay return", "Package accepted state and receipts back to the front stage."),
    ("persona_response", "Persona response", "Present the user-facing response without claiming sovereign authority."),
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str, *, max_length: int = 64) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:max_length] or "chat"


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _truthy_env(name: str) -> bool:
    return str(os.environ.get(name) or "").strip().lower() in {"1", "true", "yes", "on"}


def _is_ephemeral_playwright_smoke(
    text: str,
    *,
    lane_id: str,
    author: str,
    execution_mode: str,
) -> bool:
    if _truthy_env(PLAYWRIGHT_COCKPIT_SMOKE_PERSIST_ENV):
        return False
    return (
        lane_id == "codex_general"
        and author in {"operator", "user"}
        and execution_mode == "respond_only"
        and bool(PLAYWRIGHT_COCKPIT_SMOKE_RE.fullmatch(text))
    )


def _playwright_smoke_turn_result(
    root: str | Path | None,
    *,
    lane_id: str,
    message: str,
    author: str,
    execution_mode: str,
) -> dict[str, Any]:
    now = _now()
    turn = {
        "turn_id": f"smoke_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(message)}",
        "lane_id": lane_id,
        "author": author,
        "kind": "playwright_smoke_probe",
        "message": message,
        "message_sha256": _sha256_text(message),
        "created_at": now,
        "execution_mode": execution_mode,
        "persistence": "ephemeral_not_saved",
        "production_authority": False,
        "live_execution_authority": False,
    }
    assistant_turn = {
        "turn_id": f"smoke_assistant_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(message)}",
        "lane_id": lane_id,
        "author": "codex_chat_engine",
        "kind": "assistant_response",
        "message": PLAYWRIGHT_COCKPIT_SMOKE_RESPONSE,
        "message_sha256": _sha256_text(PLAYWRIGHT_COCKPIT_SMOKE_RESPONSE),
        "created_at": now,
        "context_refs": [],
        "execution_mode": execution_mode,
        "response_mode": "smoke_probe",
        "response_carrier": {"status": "BYPASSED_FOR_EPHEMERAL_PLAYWRIGHT_SMOKE"},
        "persistence": "ephemeral_not_saved",
        "production_authority": False,
        "live_execution_authority": False,
    }
    return {
        "ok": True,
        "turn": turn,
        "assistant_turn": assistant_turn,
        "execution_mode": execution_mode,
        "queue_result": None,
        "runner_result": None,
        "execution_status_turn": None,
        "pipeline_run": None,
        "smoke_probe": {
            "schema_id": "ion.codex_capsule_chat_playwright_smoke_probe.v1",
            "persistence": "ephemeral_not_saved",
            "production_state_mutated": False,
            "response_carrier_invoked": False,
            "persist_override_env": PLAYWRIGHT_COCKPIT_SMOKE_PERSIST_ENV,
        },
        "model": build_dual_codex_chat_model(root, write=False),
        "production_authority": False,
        "live_execution_authority": False,
    }


def _resolve_root(root: str | Path | None = None) -> Path:
    return Path(root or ".").expanduser().resolve()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _trim(value: Any, *, limit: int = 12000) -> str:
    text = str(value or "").replace("\r\n", "\n").strip()
    return text[:limit]


def _short_message(value: Any, *, limit: int = 1400) -> str:
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n..."


def _runner_start_enabled() -> bool:
    return str(os.environ.get(CHAT_RUNNER_START_ENV) or "").strip().lower() in {"1", "true", "yes", "on"}


def _resolve_chat_execution_mode(value: Any = None) -> str:
    requested = str(value or os.environ.get(CHAT_EXECUTION_MODE_ENV) or DEFAULT_CHAT_EXECUTION_MODE).strip()
    return requested if requested in CHAT_EXECUTION_MODES else DEFAULT_CHAT_EXECUTION_MODE


def _chat_execution_config(root: str | Path | None = None) -> dict[str, Any]:
    default_mode = _resolve_chat_execution_mode(None)
    runner_start_enabled = _runner_start_enabled()
    response_carrier = build_chat_response_carrier_status(root)
    allowed_modes = ["respond_only", "queue_for_codex"]
    if runner_start_enabled:
        allowed_modes.append("queue_and_start")
    return {
        "schema_id": "ion.codex_capsule_chat_execution_bridge.v1",
        "default_mode": default_mode,
        "allowed_modes": allowed_modes,
        "runner_start_enabled": runner_start_enabled,
        "runner_start_env": CHAT_RUNNER_START_ENV,
        "default_mode_env": CHAT_EXECUTION_MODE_ENV,
        "response_carrier_enabled": response_carrier.get("enabled"),
        "response_carrier_enabled_env": response_carrier.get("enabled_env"),
        "response_carrier_timeout_seconds": response_carrier.get("timeout_seconds"),
        "queue_owner": "ION/04_packages/kernel/ion_codex_queue_runner.py",
        "work_request_owner": "ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py",
        "global_codex_context_injection": False,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _state_path(root: Path) -> Path:
    return root / STATE_PATH


def _default_state() -> dict[str, Any]:
    now = _now()
    return {
        "schema_id": STATE_SCHEMA_ID,
        "created_at": now,
        "updated_at": now,
        "lanes": {
            lane_id: {
                "lane_id": lane_id,
                **config,
                "turns": [],
                "queue_links": [],
            }
            for lane_id, config in LANES.items()
        },
        "pipeline_runs": [],
        "memory": {
            "pins": [],
            "codex_memory_path": str(Path(os.environ.get(CODEX_MEMORY_ENV) or DEFAULT_CODEX_MEMORY_PATH)),
            "policy": "explicit_source_linked_repo_and_codex_memory",
        },
        "product_mode": {
            "primary_lane_id": "codex_general",
            "ion_comms_lane_id": "ion_system",
            "dual_chat_infrastructure": False,
            "global_codex_context_injection": False,
            "default_chat_execution_mode": _resolve_chat_execution_mode(None),
            "runner_start_enabled": _runner_start_enabled(),
            "policy": "one Capsule Codex chat with bounded ION comms adapter",
        },
        "mini_auto_post": {
            "enabled": True,
            "lane_id": "codex_general",
            "last_mini_sha256": None,
            "last_turn_id": None,
            "policy": "post_mini_to_chat_when_capsule_summary_changes",
        },
        "production_authority": False,
        "live_execution_authority": False,
    }


def load_dual_chat_state(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    state = _read_json(_state_path(shell_root)) or _default_state()
    state.setdefault("lanes", {})
    for lane_id, config in LANES.items():
        state["lanes"].setdefault(lane_id, {"lane_id": lane_id, **config, "turns": [], "queue_links": []})
        state["lanes"][lane_id].setdefault("turns", [])
        state["lanes"][lane_id].setdefault("queue_links", [])
    state.setdefault("pipeline_runs", [])
    state.setdefault("memory", {"pins": [], "codex_memory_path": str(DEFAULT_CODEX_MEMORY_PATH)})
    state["memory"].setdefault("pins", [])
    state.setdefault("product_mode", {})
    state["product_mode"].setdefault("primary_lane_id", "codex_general")
    state["product_mode"].setdefault("ion_comms_lane_id", "ion_system")
    state["product_mode"].setdefault("dual_chat_infrastructure", False)
    state["product_mode"].setdefault("global_codex_context_injection", False)
    state["product_mode"]["default_chat_execution_mode"] = _resolve_chat_execution_mode(None)
    state["product_mode"]["runner_start_enabled"] = _runner_start_enabled()
    state["product_mode"].setdefault("policy", "one Capsule Codex chat with bounded ION comms adapter")
    state.setdefault("mini_auto_post", {})
    state["mini_auto_post"].setdefault("enabled", True)
    state["mini_auto_post"].setdefault("lane_id", "codex_general")
    state["mini_auto_post"].setdefault("last_mini_sha256", None)
    state["mini_auto_post"].setdefault("last_turn_id", None)
    state["mini_auto_post"].setdefault("policy", "post_mini_to_chat_when_capsule_summary_changes")
    state.setdefault("production_authority", False)
    state.setdefault("live_execution_authority", False)
    return state


def save_dual_chat_state(root: str | Path | None, state: Mapping[str, Any]) -> None:
    shell_root = _resolve_root(root)
    payload = dict(state)
    payload["schema_id"] = STATE_SCHEMA_ID
    payload["updated_at"] = _now()
    payload["production_authority"] = False
    payload["live_execution_authority"] = False
    _write_json(_state_path(shell_root), payload)


def _latest_json_files(root: Path, rel: str, *, limit: int = 5) -> list[dict[str, Any]]:
    base = root / rel
    if not base.exists():
        return []
    files = sorted((path for path in base.rglob("*.json") if path.is_file()), key=lambda p: p.stat().st_mtime, reverse=True)
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "name": path.name,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
        }
        for path in files[:limit]
    ]


def _safe_read_repo_json(root: Path, rel_path: Any) -> dict[str, Any] | None:
    text = str(rel_path or "").strip()
    if not text:
        return None
    rel = Path(text)
    if rel.is_absolute() or ".." in rel.parts:
        return None
    target = (root / rel).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return None
    if not target.is_file():
        return None
    payload = _read_json(target)
    return payload if isinstance(payload, dict) else None


def _json_packet_records(root: Path, rel_dir: Path, *, pattern: str = "*.json", limit: int = 400) -> list[dict[str, Any]]:
    base = root / rel_dir
    if not base.exists():
        return []
    paths = sorted(
        (path for path in base.rglob(pattern) if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    records: list[dict[str, Any]] = []
    for path in paths[:limit]:
        payload = _read_json(path)
        if not isinstance(payload, dict):
            continue
        records.append({
            "path": path.relative_to(root).as_posix(),
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
            "packet": payload,
        })
    return records


def _index_records(records: list[dict[str, Any]], *field_names: str) -> dict[str, list[dict[str, Any]]]:
    index: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        payload = record.get("packet") if isinstance(record.get("packet"), Mapping) else {}
        for field in field_names:
            value = str(payload.get(field) or "").strip()
            if value:
                index.setdefault(value, []).append(record)
    return index


def _dedupe_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for record in records:
        path = str(record.get("path") or "")
        if not path or path in seen:
            continue
        seen.add(path)
        deduped.append(record)
    return deduped


def _records_for_request(
    root: Path,
    request: Mapping[str, Any],
    *,
    run_index: Mapping[str, list[dict[str, Any]]],
    return_index: Mapping[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    request_id = str(request.get("request_id") or "").strip()
    request_path = str(request.get("packet_path") or request.get("work_request_path") or "").strip()
    runs: list[dict[str, Any]] = []
    returns: list[dict[str, Any]] = []
    for key in (request_id, request_path):
        if key:
            runs.extend(run_index.get(key, []))
            returns.extend(return_index.get(key, []))
    for rel_path in request.get("codex_queue_runner_runs") or []:
        payload = _safe_read_repo_json(root, rel_path)
        if isinstance(payload, dict):
            runs.append({"path": str(rel_path), "packet": payload, "mtime": payload.get("updated_at") or payload.get("created_at")})
    for rel_path in request.get("return_packet_paths") or []:
        payload = _safe_read_repo_json(root, rel_path)
        if isinstance(payload, dict):
            returns.append({"path": str(rel_path), "packet": payload, "mtime": payload.get("created_at")})
    latest_return = str(request.get("latest_return_packet_path") or "").strip()
    if latest_return:
        payload = _safe_read_repo_json(root, latest_return)
        if isinstance(payload, dict):
            returns.append({"path": latest_return, "packet": payload, "mtime": payload.get("created_at")})
    return _dedupe_records(runs), _dedupe_records(returns)


def _proof_status(request: Mapping[str, Any], latest_return: Mapping[str, Any] | None) -> str:
    status = str(request.get("status") or "").upper()
    if latest_return:
        accepted = latest_return.get("accepted_for_carrier_intake")
        if accepted is True:
            return "accepted"
        if accepted is False:
            return "blocked"
    if request.get("latest_context_proof_accepted") is True and request.get("latest_template_action_proof_accepted") is True:
        return "accepted"
    if "BLOCKED" in status or "FAILED" in status or "REFUSED" in status:
        return "blocked"
    if "RETURN_RECORDED" in status:
        return "returned"
    if "RUNNING" in status or "CLAIMED" in status:
        return "running"
    return "pending"


def _trace_event(
    *,
    event_type: str,
    label: str,
    status: str,
    timestamp: Any = None,
    detail: Any = None,
    source_refs: list[str] | None = None,
    tool_name: str | None = None,
    model_move: Mapping[str, Any] | None = None,
    proof_status: str | None = None,
) -> dict[str, Any]:
    return {
        "event_type": event_type,
        "label": label,
        "status": status,
        "timestamp": timestamp,
        "detail": _short_message(detail, limit=420) if detail else "",
        "source_refs": [str(ref) for ref in source_refs or [] if ref],
        "tool_name": tool_name,
        "model_move": dict(model_move) if isinstance(model_move, Mapping) else None,
        "proof_status": proof_status,
        "raw_hidden_reasoning_exposed": False,
    }


def build_codex_capsule_turn_trace_model(
    state: Mapping[str, Any],
    *,
    codex_solo_context: Mapping[str, Any],
    codex_status: Mapping[str, Any],
    return_hydration: Mapping[str, Any],
) -> dict[str, Any]:
    lanes = state.get("lanes") if isinstance(state.get("lanes"), Mapping) else {}
    codex_lane = lanes.get("codex_general") if isinstance(lanes.get("codex_general"), Mapping) else {}
    turns = [turn for turn in codex_lane.get("turns", []) if isinstance(turn, Mapping)]
    return_records = [record for record in return_hydration.get("records", []) if isinstance(record, Mapping)]
    returns_by_source: dict[str, list[Mapping[str, Any]]] = {}
    for record in return_records:
        source_turn_id = str(record.get("source_turn_id") or "").strip()
        if source_turn_id:
            returns_by_source.setdefault(source_turn_id, []).append(record)
    capsule_refs = [
        CAPSULE_PATH.as_posix(),
        MINI_PATH.as_posix(),
        HOT_CONTEXT_PATH.as_posix(),
        LONG_HORIZON_PATH.as_posix(),
        CONTEXT_PACKAGES_PATH.as_posix(),
        ROUTE_PATH.as_posix(),
    ]
    trace_records: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw_turn in turns:
        turn = dict(raw_turn)
        kind = str(turn.get("kind") or "chat_turn")
        author = str(turn.get("author") or "")
        if kind == "chat_turn" and author in {"operator", "user"}:
            current = {
                "schema_id": "ion.codex_capsule_chat_turn_trace.v1",
                "turn_id": turn.get("turn_id"),
                "created_at": turn.get("created_at"),
                "execution_mode": turn.get("execution_mode"),
                "events": [
                    _trace_event(
                        event_type="operator_message",
                        label="Message received",
                        status="received",
                        timestamp=turn.get("created_at"),
                        detail=turn.get("message"),
                    ),
                    _trace_event(
                        event_type="context_mount",
                        label="Capsule context mounted",
                        status="ready" if codex_solo_context.get("ok") else "blocked",
                        timestamp=turn.get("created_at"),
                        detail=codex_solo_context.get("verdict"),
                        source_refs=capsule_refs,
                    ),
                ],
                "policy": "transparent_events_without_raw_hidden_reasoning",
                "raw_hidden_reasoning_exposed": False,
                "production_authority": False,
                "live_execution_authority": False,
            }
            trace_records.append(current)
            skill_activation = turn.get("skill_activation") if isinstance(turn.get("skill_activation"), Mapping) else None
            if skill_activation:
                current["events"].append(_trace_event(
                    event_type="skill_activation",
                    label="Skill activated",
                    status="ready" if skill_activation.get("ok") else "blocked",
                    timestamp=turn.get("created_at"),
                    detail=(
                        f"{skill_activation.get('display_name')} / {skill_activation.get('skill_id')}\n"
                        f"{skill_activation.get('selection_reason')}\n"
                        "Templates remain proof gates."
                    ),
                    source_refs=skill_activation.get("activates_templates") if isinstance(skill_activation.get("activates_templates"), list) else [],
                    model_move=skill_activation.get("model_route") if isinstance(skill_activation.get("model_route"), Mapping) else None,
                ))
            chat_engine = turn.get("chat_engine") if isinstance(turn.get("chat_engine"), Mapping) else None
            if chat_engine:
                native_lenses = chat_engine.get("native_lenses") if isinstance(chat_engine.get("native_lenses"), list) else []
                assistant_work_route = chat_engine.get("assistant_work_route") if isinstance(chat_engine.get("assistant_work_route"), Mapping) else {}
                current["events"].append(_trace_event(
                    event_type="chat_engine",
                    label="Chat engine route",
                    status=str(chat_engine.get("response_mode") or "answer"),
                    timestamp=turn.get("created_at"),
                    detail=(
                        f"mode: {chat_engine.get('response_mode')}\n"
                        f"strategy: {(chat_engine.get('carrier_strategy') or {}).get('mode') if isinstance(chat_engine.get('carrier_strategy'), Mapping) else 'unknown'}\n"
                        f"native_lenses: {', '.join(str(lens.get('display_name')) for lens in native_lenses[:6] if isinstance(lens, Mapping))}"
                    ),
                    source_refs=(chat_engine.get("context_mount") or {}).get("context_refs") if isinstance(chat_engine.get("context_mount"), Mapping) else [],
                    model_move=chat_engine.get("model_move") if isinstance(chat_engine.get("model_move"), Mapping) else None,
                ))
                if assistant_work_route:
                    current["events"].append(_trace_event(
                        event_type="assistant_work_route",
                        label="Assistant work route",
                        status=str(assistant_work_route.get("route_id") or assistant_work_route.get("verdict") or "candidate_unavailable"),
                        timestamp=turn.get("created_at"),
                        detail=(
                            f"route: {assistant_work_route.get('route_id') or 'unavailable'}\n"
                            f"basis: {assistant_work_route.get('selection_basis') or assistant_work_route.get('finding') or 'candidate'}\n"
                            f"domains: {', '.join(str(item) for item in (assistant_work_route.get('candidate_domains') or [])[:6])}\n"
                            f"agents: {', '.join(str(item) for item in (assistant_work_route.get('candidate_agents') or [])[:6])}"
                        ),
                        source_refs=[
                            "ION/05_context/current/ai_assistant_work/registries/AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml",
                            "ION/05_context/current/ai_assistant_work/route_compiler",
                        ],
                    ))
            continue
        if current is None:
            continue
        if kind == "assistant_response":
            response_carrier = turn.get("response_carrier") if isinstance(turn.get("response_carrier"), Mapping) else None
            if response_carrier:
                run = response_carrier.get("run") if isinstance(response_carrier.get("run"), Mapping) else {}
                refs = [
                    str(run.get("run_packet_path") or ""),
                    str(run.get("latest_return_path") or ""),
                    str(run.get("events_path") or ""),
                ]
                current["events"].append(_trace_event(
                    event_type="codex_chat_response_carrier",
                    label="Response carrier",
                    status=str(response_carrier.get("status") or response_carrier.get("finding") or "unknown"),
                    timestamp=turn.get("created_at"),
                    detail=response_carrier.get("finding") or response_carrier.get("response_text") or "No carrier response captured.",
                    source_refs=[ref for ref in refs if ref],
                    tool_name="codex exec",
                    model_move=turn.get("codex_model_move") if isinstance(turn.get("codex_model_move"), Mapping) else None,
                ))
            current["events"].append(_trace_event(
                event_type="assistant_response",
                label="Assistant response",
                status="visible",
                timestamp=turn.get("created_at"),
                detail=turn.get("message"),
                source_refs=turn.get("context_refs") if isinstance(turn.get("context_refs"), list) else [],
                model_move=turn.get("codex_model_move") if isinstance(turn.get("codex_model_move"), Mapping) else None,
            ))
        elif kind == "execution_status":
            packet_path = str(turn.get("packet_path") or "")
            request_id = str(turn.get("request_id") or "")
            current["events"].append(_trace_event(
                event_type="tool_call",
                label="Codex queue request",
                status=str(turn.get("queue_status") or "requested"),
                timestamp=turn.get("created_at"),
                detail=f"{request_id}\n{packet_path}".strip(),
                source_refs=[packet_path] if packet_path else [],
                tool_name="ion_request_codex_work_packet",
            ))
            runner_result = turn.get("runner_result") if isinstance(turn.get("runner_result"), Mapping) else None
            if runner_result:
                current["events"].append(_trace_event(
                    event_type="runner",
                    label="Runner start request",
                    status=str(runner_result.get("result") or runner_result.get("finding") or "not_started"),
                    timestamp=turn.get("created_at"),
                    detail=runner_result.get("finding") or runner_result.get("result"),
                    tool_name="ion_codex_queue_process_once",
                ))
    for trace in trace_records:
        source_turn_id = str(trace.get("turn_id") or "")
        linked_returns = returns_by_source.get(source_turn_id, [])
        if not any(event.get("event_type") == "tool_call" for event in trace.get("events", [])):
            trace["events"].append(_trace_event(
                event_type="execution_bridge",
                label="Codex execution bridge",
                status="not_requested",
                timestamp=trace.get("created_at"),
                detail="Normal chat response only.",
            ))
        for record in linked_returns:
            refs = [ref for ref in record.get("path_refs", []) if ref] if isinstance(record.get("path_refs"), list) else []
            trace["events"].append(_trace_event(
                event_type="proof_return",
                label="Task return proof",
                status=str(record.get("status") or "returned"),
                timestamp=record.get("latest_return_path") or record.get("latest_run_path"),
                detail=record.get("task_output_preview") or record.get("latest_return_path"),
                source_refs=refs,
                tool_name="ion_submit_task_return",
                proof_status=str(record.get("proof_status") or "pending"),
            ))
        trace["event_count"] = len(trace.get("events", []))
    return {
        "schema_id": "ion.codex_capsule_chat_turn_trace_index.v1",
        "trace_count": len(trace_records),
        "traces": trace_records,
        "runner_active": codex_status.get("active_process_running", False),
        "queued_request_count": codex_status.get("queued_request_count", 0),
        "policy": "show_context_tool_queue_file_proof_events_not_raw_chain_of_thought",
        "raw_hidden_reasoning_exposed": False,
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_codex_capsule_agent_surface(root: Path) -> dict[str, Any]:
    try:
        roster = list_agents(root)
        queue = agent_queue(root, limit=12)
        agents = roster.get("agents") if isinstance(roster.get("agents"), list) else []
        invocations = queue.get("invocations") if isinstance(queue.get("invocations"), list) else []
        return {
            "schema_id": "ion.codex_capsule_chat_agent_surface.v1",
            "verdict": "ION_CODEX_CAPSULE_AGENT_SURFACE_READY",
            "agent_count": roster.get("agent_count", len(agents)),
            "available_agents": agents[:24],
            "invocation_count": queue.get("invocation_count", len(invocations)),
            "recent_invocations": invocations,
            "broker_owner": "ION/04_packages/kernel/ion_agent_invocation_broker.py",
            "creates_second_agent_system": False,
            "creates_second_queue": False,
            "policy": "read_only_projection_of_existing_ion_agent_invocation_broker",
            "production_authority": False,
            "live_execution_authority": False,
        }
    except Exception as exc:  # pragma: no cover - defensive UI projection
        return {
            "schema_id": "ion.codex_capsule_chat_agent_surface.v1",
            "verdict": "ION_CODEX_CAPSULE_AGENT_SURFACE_BLOCKED",
            "finding": str(exc),
            "agent_count": 0,
            "available_agents": [],
            "invocation_count": 0,
            "recent_invocations": [],
            "creates_second_agent_system": False,
            "creates_second_queue": False,
            "production_authority": False,
            "live_execution_authority": False,
        }


def build_codex_return_hydration(root: Path, state: Mapping[str, Any]) -> dict[str, Any]:
    lanes = state.get("lanes") if isinstance(state.get("lanes"), Mapping) else {}
    codex_lane = lanes.get("codex_general") if isinstance(lanes.get("codex_general"), Mapping) else {}
    turns = [turn for turn in codex_lane.get("turns", []) if isinstance(turn, Mapping)]
    queue_links = [link for link in codex_lane.get("queue_links", []) if isinstance(link, Mapping)]
    request_records = _json_packet_records(root, CODEX_WORK_REQUESTS_DIR)
    run_records = _json_packet_records(root, CODEX_QUEUE_RUNS_DIR, pattern="run.json")
    return_records = _json_packet_records(root, CODEX_TASK_RETURNS_DIR)
    request_index = _index_records(request_records, "request_id", "packet_path")
    run_index = _index_records(run_records, "request_id", "request_path")
    return_index = _index_records(return_records, "work_request_id", "work_request_path")
    sources: list[dict[str, Any]] = []
    seen_sources: set[tuple[str, str | None]] = set()
    for turn in turns:
        if turn.get("kind") != "execution_status":
            continue
        request_id = str(turn.get("request_id") or "").strip()
        packet_path = str(turn.get("packet_path") or "").strip()
        if not request_id and not packet_path:
            continue
        key = (request_id or packet_path, str(turn.get("source_turn_id") or ""))
        if key in seen_sources:
            continue
        seen_sources.add(key)
        sources.append({
            "request_id": request_id,
            "request_path": packet_path,
            "source_turn_id": turn.get("source_turn_id"),
            "execution_turn_id": turn.get("turn_id"),
            "queued_at": turn.get("created_at"),
            "queue_status": turn.get("queue_status"),
        })
    for link in queue_links:
        request_id = str(link.get("request_id") or "").strip()
        packet_path = str(link.get("packet_path") or "").strip()
        if not request_id and not packet_path:
            continue
        key = (request_id or packet_path, str(link.get("source_turn_id") or ""))
        if key in seen_sources:
            continue
        seen_sources.add(key)
        sources.append({
            "request_id": request_id,
            "request_path": packet_path,
            "source_turn_id": link.get("source_turn_id"),
            "execution_turn_id": None,
            "queued_at": link.get("created_at"),
            "queue_status": link.get("status"),
        })
    records: list[dict[str, Any]] = []
    for source in sources:
        request_id = str(source.get("request_id") or "").strip()
        request_path = str(source.get("request_path") or "").strip()
        matches: list[dict[str, Any]] = []
        for key in (request_id, request_path):
            if key:
                matches.extend(request_index.get(key, []))
        if request_path and not matches:
            payload = _safe_read_repo_json(root, request_path)
            if isinstance(payload, dict):
                matches.append({"path": request_path, "packet": payload, "mtime": payload.get("updated_at") or payload.get("created_at")})
        request_record = _dedupe_records(matches)[0] if matches else {"path": request_path, "packet": {}, "mtime": None}
        request = request_record.get("packet") if isinstance(request_record.get("packet"), Mapping) else {}
        runs, returns = _records_for_request(root, request, run_index=run_index, return_index=return_index) if request else ([], [])
        latest_run_record = runs[0] if runs else None
        latest_return_record = returns[0] if returns else None
        latest_run = latest_run_record.get("packet") if isinstance(latest_run_record, Mapping) and isinstance(latest_run_record.get("packet"), Mapping) else None
        latest_return = latest_return_record.get("packet") if isinstance(latest_return_record, Mapping) and isinstance(latest_return_record.get("packet"), Mapping) else None
        proof = _proof_status(request, latest_return)
        status = (
            request.get("status")
            or (latest_run or {}).get("status")
            or source.get("queue_status")
            or "QUEUED_FOR_CODEX_CARRIER"
        )
        template_result = latest_return.get("template_action_proof_result") if isinstance(latest_return, Mapping) and isinstance(latest_return.get("template_action_proof_result"), Mapping) else {}
        context_result = latest_return.get("context_proof_result") if isinstance(latest_return, Mapping) and isinstance(latest_return.get("context_proof_result"), Mapping) else {}
        path_refs = [
            request_record.get("path"),
            latest_run_record.get("path") if latest_run_record else None,
            latest_return_record.get("path") if latest_return_record else None,
        ]
        records.append({
            "schema_id": "ion.codex_capsule_chat_return_hydration_record.v1",
            "source_turn_id": source.get("source_turn_id"),
            "execution_turn_id": source.get("execution_turn_id"),
            "request_id": request.get("request_id") or request_id or None,
            "request_path": request_record.get("path") or request_path or None,
            "status": status,
            "proof_status": proof,
            "context_proof_accepted": context_result.get("accepted") if context_result else request.get("latest_context_proof_accepted"),
            "template_action_proof_accepted": template_result.get("accepted") if template_result else request.get("latest_template_action_proof_accepted"),
            "context_proof_findings": context_result.get("findings") or [],
            "template_action_proof_findings": template_result.get("findings") or [],
            "touched_paths": template_result.get("touched_paths") or [],
            "task_output_preview": _short_message((latest_return or {}).get("task_output_preview"), limit=900) if latest_return else "",
            "latest_run_path": latest_run_record.get("path") if latest_run_record else None,
            "latest_run_status": (latest_run or {}).get("status"),
            "latest_return_path": latest_return_record.get("path") if latest_return_record else None,
            "accepted_for_carrier_intake": (latest_return or {}).get("accepted_for_carrier_intake") if latest_return else None,
            "path_refs": [path for path in path_refs if path],
            "production_authority": False,
            "live_execution_authority": False,
        })
    return {
        "schema_id": "ion.codex_capsule_chat_return_hydration.v1",
        "record_count": len(records),
        "accepted_count": sum(1 for record in records if record.get("proof_status") == "accepted"),
        "blocked_count": sum(1 for record in records if record.get("proof_status") == "blocked"),
        "records": records,
        "policy": "read_only_projection_from_existing_codex_queue_runs_and_task_returns",
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_codex_chat_response_run_surface(root: Path) -> dict[str, Any]:
    records = []
    for record in _json_packet_records(root, RESPONSE_RUNS_DIR, pattern="run.json", limit=24):
        packet = record.get("packet") if isinstance(record.get("packet"), Mapping) else {}
        unexpected = packet.get("unexpected_worktree_changes") if isinstance(packet.get("unexpected_worktree_changes"), list) else []
        records.append({
            "schema_id": "ion.codex_chat_response_run_record.v1",
            "path": record.get("path"),
            "mtime": record.get("mtime"),
            "run_id": packet.get("run_id"),
            "created_at": packet.get("created_at"),
            "updated_at": packet.get("updated_at"),
            "status": packet.get("status"),
            "ok": packet.get("ok"),
            "finding": packet.get("finding"),
            "selected_model": packet.get("selected_model"),
            "selected_reasoning_effort": packet.get("selected_reasoning_effort"),
            "prompt_path": packet.get("prompt_path"),
            "latest_return_path": packet.get("latest_return_path"),
            "events_path": packet.get("events_path"),
            "stdout_path": packet.get("stdout_path"),
            "stderr_path": packet.get("stderr_path"),
            "response_sha256": packet.get("response_sha256"),
            "operator_message_sha256": packet.get("operator_message_sha256"),
            "unexpected_worktree_change_count": len(unexpected),
            "production_authority": False,
            "live_execution_authority": False,
        })
    return {
        "schema_id": "ion.codex_chat_response_run_surface.v1",
        "run_root": RESPONSE_RUNS_DIR.as_posix(),
        "record_count": len(records),
        "latest_status": records[0].get("status") if records else "none",
        "records": records,
        "policy": "read_only_response_carrier_run_prompt_return_event_projection",
        "production_authority": False,
        "live_execution_authority": False,
    }


def _turn_digest(turns: list[dict[str, Any]], *, limit: int = 4) -> list[dict[str, Any]]:
    digest = []
    for turn in turns[-limit:]:
        digest.append({
            "turn_id": turn.get("turn_id"),
            "author": turn.get("author"),
            "created_at": turn.get("created_at"),
            "summary": str(turn.get("message") or "")[:240],
        })
    return digest


def _build_shared_digest(state: Mapping[str, Any], codex_status: Mapping[str, Any]) -> dict[str, Any]:
    lanes = state.get("lanes") if isinstance(state.get("lanes"), Mapping) else {}
    ion_turns = list((lanes.get("ion_system") or {}).get("turns") or []) if isinstance(lanes.get("ion_system"), Mapping) else []
    codex_turns = list((lanes.get("codex_general") or {}).get("turns") or []) if isinstance(lanes.get("codex_general"), Mapping) else []
    latest_run = None
    latest_runs = codex_status.get("latest_runs") if isinstance(codex_status.get("latest_runs"), list) else []
    if latest_runs:
        latest_run = latest_runs[0]
    return {
        "schema_id": "ion.codex_capsule_chat_comms_digest.v1",
        "policy": "bounded_digest_not_full_transcript_by_default",
        "ion_comms_visible_to_capsule_codex": _turn_digest(ion_turns),
        "capsule_codex_visible_to_ion_comms": _turn_digest(codex_turns),
        "memory_pin_count": len((state.get("memory") or {}).get("pins") or []) if isinstance(state.get("memory"), Mapping) else 0,
        "codex_queue": {
            "queued_request_count": codex_status.get("queued_request_count", 0),
            "active_process_running": codex_status.get("active_process_running", False),
            "latest_run": latest_run,
        },
    }


def _mini_text(codex_solo_context: Mapping[str, Any]) -> str:
    mini = codex_solo_context.get("mini") if isinstance(codex_solo_context.get("mini"), Mapping) else {}
    return str(mini.get("text") or "").strip()


def _mini_auto_post_message(codex_solo_context: Mapping[str, Any], mini_sha: str) -> str:
    mini = _mini_text(codex_solo_context)
    capsule = codex_solo_context.get("capsule") if isinstance(codex_solo_context.get("capsule"), Mapping) else {}
    capsule_tail = capsule.get("tail") if isinstance(capsule.get("tail"), list) else []
    capsule_ref = CAPSULE_PATH.as_posix()
    latest_capsule_row = str(capsule_tail[-1]) if capsule_tail else "none"
    return "\n".join([
        "ION Mini capsule brief",
        f"mini_ref: {MINI_PATH.as_posix()}",
        f"capsule_ref: {capsule_ref}",
        f"mini_sha256: {mini_sha}",
        f"latest_capsule_row: {latest_capsule_row}",
        "",
        mini or "Mini not initialized.",
    ])


def _sync_mini_auto_post(
    state: dict[str, Any],
    codex_solo_context: Mapping[str, Any],
    *,
    reason: str,
) -> dict[str, Any]:
    config = state.setdefault("mini_auto_post", {})
    if config.get("enabled") is False:
        return {"ok": True, "posted": False, "finding": "mini_auto_post_disabled"}
    lane_id = str(config.get("lane_id") or "codex_general")
    if lane_id not in LANES:
        return {"ok": False, "posted": False, "finding": "mini_auto_post_lane_unknown", "lane_id": lane_id}
    mini = _mini_text(codex_solo_context)
    if not mini:
        return {"ok": False, "posted": False, "finding": "mini_text_missing"}
    mini_sha = _sha256_text(mini)
    if config.get("last_mini_sha256") == mini_sha:
        return {"ok": True, "posted": False, "finding": "mini_unchanged", "mini_sha256": mini_sha}
    now = _now()
    turn_id = f"mini_{now.replace(':', '').replace('+', 'Z')}_{mini_sha[:12]}"
    turn = {
        "turn_id": turn_id,
        "lane_id": lane_id,
        "author": "ion_context",
        "kind": "mini_auto_post",
        "message": _mini_auto_post_message(codex_solo_context, mini_sha),
        "message_sha256": _sha256_text(_mini_auto_post_message(codex_solo_context, mini_sha)),
        "created_at": now,
        "reason": reason,
        "mini_ref": MINI_PATH.as_posix(),
        "capsule_ref": CAPSULE_PATH.as_posix(),
        "mini_sha256": mini_sha,
        "production_authority": False,
        "live_execution_authority": False,
    }
    state["lanes"][lane_id].setdefault("turns", []).append(turn)
    config["last_mini_sha256"] = mini_sha
    config["last_turn_id"] = turn_id
    config["last_posted_at"] = now
    config["last_reason"] = reason
    return {"ok": True, "posted": True, "turn": turn, "mini_sha256": mini_sha}


def build_dual_codex_chat_model(root: str | Path | None = None, *, write: bool = False) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    state = load_dual_chat_state(shell_root)
    codex_status = build_codex_queue_runner_status(shell_root, reconcile=False)
    codex_solo_context = build_codex_solo_context_model(shell_root, write=write)
    mini_auto_post = _sync_mini_auto_post(state, codex_solo_context, reason="codex_capsule_chat_model_refresh") if write else {
        "ok": True,
        "posted": False,
        "finding": "write_not_requested",
        "mini_sha256": _sha256_text(_mini_text(codex_solo_context)) if _mini_text(codex_solo_context) else None,
    }
    if write and mini_auto_post.get("posted"):
        save_dual_chat_state(shell_root, state)
    lanes = json.loads(json.dumps(state.get("lanes", {})))
    if isinstance(lanes.get("codex_general"), dict):
        lanes["codex_general"]["context_substrate"] = {
            "schema_id": codex_solo_context.get("schema_id"),
            "verdict": codex_solo_context.get("verdict"),
            "active_context": codex_solo_context.get("active_context"),
            "paths": codex_solo_context.get("paths"),
            "witness_policy": codex_solo_context.get("witness_policy"),
        }
        lanes["codex_general"]["mini_auto_post"] = state.get("mini_auto_post")
    stage_model_moves = build_stage_model_move_matrix(ION_PIPELINE_STAGES, routing_posture=DEFAULT_ROUTING_POSTURE)
    return_hydration = build_codex_return_hydration(shell_root, state)
    response_runs = build_codex_chat_response_run_surface(shell_root)
    turn_traces = build_codex_capsule_turn_trace_model(
        state,
        codex_solo_context=codex_solo_context,
        codex_status=codex_status,
        return_hydration=return_hydration,
    )
    agent_surface = build_codex_capsule_agent_surface(shell_root)
    skill_surface = build_ion_skill_surface(
        shell_root,
        lane_id="codex_general",
        objective="model refresh",
        execution_mode=DEFAULT_CHAT_EXECUTION_MODE,
        codex_solo_context=codex_solo_context,
    )
    chat_engine_surface = build_codex_chat_engine_surface(shell_root)
    chat_response_carrier = build_chat_response_carrier_status(shell_root)
    memory_visualization = build_codex_chat_memory_visualization(
        state=state,
        codex_solo_context=codex_solo_context,
        turn_traces=turn_traces,
        return_hydration=return_hydration,
        codex_status=codex_status,
    )
    model = {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT,
        "generated_at": _now(),
        "state_path": STATE_PATH.as_posix(),
        "model_path": MODEL_PATH.as_posix(),
        "product": {
            "name": "ION Codex Chat",
            "primary_lane_id": "codex_general",
            "ion_comms_lane_id": "ion_system",
            "dual_chat_infrastructure": False,
            "chat_first": True,
            "global_codex_context_injection": False,
            "acceptance_gate": "operator_message_produces_visible_assistant_response",
            "policy": "Build one Capsule-backed Codex chat and communicate with full ION through existing comms/receipts.",
        },
        "execution_bridge": _chat_execution_config(shell_root),
        "lanes": lanes,
        "pipeline_runs": list(state.get("pipeline_runs") or [])[-12:],
        "memory": state.get("memory", {}),
        "product_mode": state.get("product_mode", {}),
        "codex_solo_context": codex_solo_context,
        "mini_auto_post": {
            **(state.get("mini_auto_post") if isinstance(state.get("mini_auto_post"), Mapping) else {}),
            "sync_result": mini_auto_post,
        },
        "model_moves": {
            "schema_id": "ion.codex_capsule_chat_model_moves.v1",
            "routing_posture": DEFAULT_ROUTING_POSTURE,
            "usage_limits_authoritative": False,
            "stage_defaults": stage_model_moves,
            "profiles": list_codex_model_profiles(),
            "production_authority": False,
            "live_execution_authority": False,
        },
        "shared_digest": _build_shared_digest(state, codex_status),
        "ion_comms": {
            "schema_id": "ion.codex_capsule_chat_ion_comms_adapter.v1",
            "mode": "existing_ion_comms_adapter",
            "primary_chat_is": "codex_general",
            "ion_comms_lane_id": "ion_system",
            "uses_existing_ion_owners": True,
            "creates_second_queue": False,
            "creates_second_agent_system": False,
            "digest": _build_shared_digest(state, codex_status),
            "front_door_adapter": "ION/04_packages/kernel/front_door_chat_orchestration.py",
            "codex_queue_owner": "ION/04_packages/kernel/ion_codex_queue_runner.py",
            "production_authority": False,
            "live_execution_authority": False,
        },
        "codex_queue": {
            "runner": codex_status,
            "work_queue_path": CODEX_WORK_QUEUE_INDEX.as_posix(),
            "latest_work_requests": _latest_json_files(shell_root, "ION/05_context/current/chatgpt_connector/codex_work_requests", limit=5),
            "latest_task_returns": _latest_json_files(shell_root, "ION/05_context/current/chatgpt_connector/task_returns", limit=5),
            "return_hydration": return_hydration,
        },
        "response_runs": response_runs,
        "turn_traces": turn_traces,
        "memory_visualization": memory_visualization,
        "agents": agent_surface,
        "skills": skill_surface,
        "chat_engine": chat_engine_surface,
        "service_console": build_service_console_model(shell_root),
        "assistant_work_routes": chat_engine_surface.get("assistant_work_routes") if isinstance(chat_engine_surface.get("assistant_work_routes"), Mapping) else {},
        "chat_response_carrier": chat_response_carrier,
        "remote_access": {
            "public_cockpit_path": "https://ion.helixion.net/cockpit/chat",
            "requires_token_env": "ION_COCKPIT_PUBLIC_TOKEN",
            "enabled_by_model": bool(os.environ.get("ION_COCKPIT_PUBLIC_TOKEN")),
        },
        "authority": {
            "production_authority": False,
            "live_execution_authority": False,
            "arbitrary_shell": False,
            "git_push": False,
            "proof_gates_required": True,
        },
        "production_authority": False,
        "live_execution_authority": False,
    }
    model["ui"] = build_codex_capsule_chat_ui_model(model)
    if write:
        _write_json(shell_root / MODEL_PATH, model)
    return model


def _codex_solo_context_refs(solo_context: Mapping[str, Any]) -> list[str]:
    refs = [
        CAPSULE_PATH.as_posix(),
        HOT_CONTEXT_PATH.as_posix(),
        MINI_PATH.as_posix(),
        LONG_HORIZON_PATH.as_posix(),
        CONTEXT_PACKAGES_PATH.as_posix(),
        ROUTE_PATH.as_posix(),
    ]
    route = solo_context.get("route") if isinstance(solo_context.get("route"), Mapping) else {}
    entries = route.get("entries") if isinstance(route.get("entries"), list) else []
    for entry in entries:
        if isinstance(entry, Mapping) and entry.get("path"):
            ref = str(entry["path"])
            if ref not in refs:
                refs.append(ref)
    return refs


def _codex_general_queued_objective(
    objective: str,
    solo_context: Mapping[str, Any],
    model_move: Mapping[str, Any],
    skill_activation: Mapping[str, Any],
    chat_engine: Mapping[str, Any],
) -> str:
    refs = _codex_solo_context_refs(solo_context)
    ref_lines = "\n".join(f"- {ref}" for ref in refs[:16])
    template_lines = "\n".join(f"- {ref}" for ref in skill_activation.get("activates_templates", [])[:8]) if isinstance(skill_activation.get("activates_templates"), list) else "- none"
    native_lenses = chat_engine.get("native_lenses") if isinstance(chat_engine.get("native_lenses"), list) else []
    assistant_work_route = chat_engine.get("assistant_work_route") if isinstance(chat_engine.get("assistant_work_route"), Mapping) else {}
    output_contract = assistant_work_route.get("output_contract") if isinstance(assistant_work_route.get("output_contract"), Mapping) else {}
    lens_lines = "\n".join(
        f"- {lens.get('display_name')} ({lens.get('role_id')}): {lens.get('purpose')}"
        for lens in native_lenses[:8]
        if isinstance(lens, Mapping)
    ) or "- none"
    include_lines = ", ".join(str(item) for item in (output_contract.get("include") or [])[:6]) if isinstance(output_contract.get("include"), list) else ""
    forbid_lines = ", ".join(str(item) for item in (output_contract.get("forbid") or [])[:6]) if isinstance(output_contract.get("forbid"), list) else ""
    return "\n".join([
        "Codex solo chat work packet.",
        "",
        "Chat engine route:",
        f"- Response mode: {chat_engine.get('response_mode')}",
        f"- Carrier strategy: {(chat_engine.get('carrier_strategy') or {}).get('mode') if isinstance(chat_engine.get('carrier_strategy'), Mapping) else 'unknown'}",
        "- Native lenses:",
        lens_lines,
        "",
        "Candidate Assistant Work route:",
        f"- Route: {assistant_work_route.get('route_id') or 'unavailable'}",
        f"- Selection basis: {assistant_work_route.get('selection_basis') or assistant_work_route.get('finding') or 'candidate'}",
        f"- Candidate domains: {', '.join(str(item) for item in (assistant_work_route.get('candidate_domains') or [])[:8])}",
        f"- Candidate agents: {', '.join(str(item) for item in (assistant_work_route.get('candidate_agents') or [])[:8])}",
        f"- Include: {include_lines or 'none'}",
        f"- Forbid: {forbid_lines or 'none'}",
        "- Candidate route metadata does not promote assistant-work registries to ION law.",
        "",
        "Skill activation:",
        f"- Skill: {skill_activation.get('display_name')} ({skill_activation.get('skill_id')})",
        f"- Selection reason: {skill_activation.get('selection_reason')}",
        "- Skill activates workflow only; templates remain proof gates.",
        "Activated template refs:",
        template_lines,
        "",
        "Context policy:",
        f"- {WITNESS_POLICY}",
        f"- Minimum working context: load {CAPSULE_PATH.as_posix()} before doing the work.",
        f"- Mini role: {MINI_PATH.as_posix()} is lookup/receipt index only, not the main prompt surface.",
        f"- Long horizon: use {LONG_HORIZON_PATH.as_posix()} for older capsule epochs instead of stuffing all history into the prompt.",
        f"- Context package selector: use {CONTEXT_PACKAGES_PATH.as_posix()} to choose authority, mission, evidence, recovery, and route-depth packages.",
        "- Use the active ION_CODEX FULL root only.",
        "- Treat historical roots only as explicitly named witness material.",
        "- Do not claim production or live execution authority.",
        "",
        *_model_move_context_lines(model_move),
        "Required context refs:",
        ref_lines,
        "",
        "Operator objective:",
        objective,
    ])


def _model_move_context_lines(model_move: Mapping[str, Any]) -> list[str]:
    return [
        "Codex model move:",
        f"- Selected model: {model_move.get('selected_model')}",
        f"- Reasoning effort: {model_move.get('selected_reasoning_effort')}",
        f"- Work class: {model_move.get('work_class')}",
        f"- ION stage: {model_move.get('ion_stage_id') or 'codex_general_work'}",
        f"- Usage pool label: {model_move.get('usage_pool_id')} ({model_move.get('usage_pool_authority')})",
        "- Usage pool labels are operator-observed hints, not authoritative provider limits.",
        "",
    ]


def _codex_capsule_assistant_message(
    *,
    operator_text: str,
    execution_mode: str,
    codex_solo_context: Mapping[str, Any],
    codex_status: Mapping[str, Any],
    model_move: Mapping[str, Any],
    skill_activation: Mapping[str, Any],
) -> str:
    capsule = codex_solo_context.get("capsule") if isinstance(codex_solo_context.get("capsule"), Mapping) else {}
    recent_rows = capsule.get("recent_rows") if isinstance(capsule.get("recent_rows"), list) else []
    latest_row = recent_rows[-1] if recent_rows and isinstance(recent_rows[-1], Mapping) else {}
    latest_summary = latest_row.get("summary") or "No capsule receipt rows yet."
    queue_count = codex_status.get("queued_request_count", 0)
    active = codex_status.get("active_process_running", False)
    selected_model = model_move.get("selected_model") or "codex model move unavailable"
    effort = model_move.get("selected_reasoning_effort") or "unknown"
    skill_label = skill_activation.get("display_name") or "Skill unavailable"
    skill_id = skill_activation.get("skill_id") or "unknown"
    trimmed = _trim(operator_text, limit=360)
    return "\n".join([
        "Capsule context is mounted.",
        "",
        f"I received: {trimmed}",
        "",
        "Current working basis:",
        f"- minimum context: {CAPSULE_PATH.as_posix()}",
        f"- hot context: {HOT_CONTEXT_PATH.as_posix()}",
        f"- latest capsule receipt: {latest_summary}",
        f"- active skill: {skill_label} ({skill_id})",
        "- skill role: activates workflow; templates still gate proof and receipts",
        f"- Codex queue: {queue_count} queued, active={active}",
        f"- planned Codex move for work from this chat: {selected_model} / {effort}",
        f"- execution mode: {execution_mode}",
        "",
        "This chat is isolated to the Capsule Codex profile. It does not make every Codex CLI instance inherit Capsule context, and ION workflow communication stays behind the existing ION queue/receipt owners.",
    ])


def _create_codex_capsule_assistant_turn(
    root: str | Path | None,
    *,
    operator_text: str,
    created_at: str,
    execution_mode: str,
    chat_engine: Mapping[str, Any] | None = None,
    codex_solo_context: Mapping[str, Any] | None = None,
    prior_turns: list[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    engine_turn = dict(chat_engine) if isinstance(chat_engine, Mapping) else build_codex_chat_engine_turn(
        root,
        lane_id="codex_general",
        message=operator_text,
        execution_mode=execution_mode,
        codex_solo_context=codex_solo_context,
    )
    message = str(engine_turn.get("assistant_response") or "").strip() or "I’m mounted on the Codex Chat Engine, but this turn did not produce a response contract."
    response_carrier = None
    if execution_mode == "respond_only":
        try:
            response_carrier = run_codex_chat_response_carrier(
                root,
                operator_message=operator_text,
                chat_engine_turn=engine_turn,
                codex_solo_context=codex_solo_context,
                prior_turns=prior_turns,
            )
        except Exception as exc:  # keep chat usable if the carrier fails before returning a packet
            response_carrier = {
                "schema_id": "ion.codex_chat_response_carrier_run.v1",
                "ok": False,
                "status": "CARRIER_EXCEPTION",
                "finding": exc.__class__.__name__,
                "response_text": "",
                "production_authority": False,
                "live_execution_authority": False,
                "provider_api_dispatch_authorized": False,
                "state_acceptance_granted": False,
            }
        carrier_text = str(response_carrier.get("response_text") or "").strip() if isinstance(response_carrier, Mapping) else ""
        if response_carrier.get("ok") and carrier_text:
            message = carrier_text
    context_mount = engine_turn.get("context_mount") if isinstance(engine_turn.get("context_mount"), Mapping) else {}
    context_refs = context_mount.get("context_refs") if isinstance(context_mount.get("context_refs"), list) else [
        CAPSULE_PATH.as_posix(),
        HOT_CONTEXT_PATH.as_posix(),
        MINI_PATH.as_posix(),
        LONG_HORIZON_PATH.as_posix(),
        CONTEXT_PACKAGES_PATH.as_posix(),
        ROUTE_PATH.as_posix(),
    ]
    return {
        "turn_id": f"assistant_{created_at.replace(':', '').replace('+', 'Z')}_{_safe_slug(operator_text)}",
        "lane_id": "codex_general",
        "author": "codex_chat_engine",
        "kind": "assistant_response",
        "message": message,
        "message_sha256": _sha256_text(message),
        "created_at": _now(),
        "context_refs": [str(ref) for ref in context_refs],
        "execution_mode": execution_mode,
        "response_mode": engine_turn.get("response_mode"),
        "codex_model_move": engine_turn.get("model_move"),
        "skill_activation": engine_turn.get("skill_activation"),
        "native_lenses": engine_turn.get("native_lenses"),
        "response_contract": engine_turn.get("response_contract"),
        "chat_engine": engine_turn,
        "response_carrier": response_carrier,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _execution_status_message(
    *,
    execution_mode: str,
    queue_result: Mapping[str, Any] | None,
    runner_result: Mapping[str, Any] | None,
) -> str:
    if not queue_result:
        return "Codex execution bridge was not requested for this turn."
    queue_link = queue_result.get("queue_link") if isinstance(queue_result.get("queue_link"), Mapping) else {}
    lines = [
        "Codex execution bridge status.",
        "",
        f"- execution mode: {execution_mode}",
        f"- queue result: {'queued' if queue_result.get('ok') else 'blocked'}",
        f"- request id: {queue_link.get('request_id') or 'none'}",
        f"- packet path: {queue_link.get('packet_path') or 'none'}",
        f"- status: {queue_link.get('status') or queue_result.get('finding') or 'unknown'}",
    ]
    if runner_result is not None:
        lines.extend([
            f"- runner result: {'started' if runner_result.get('ok') else 'not started'}",
            f"- runner finding/result: {runner_result.get('result') or runner_result.get('finding') or 'none'}",
        ])
    else:
        lines.append("- runner result: not requested")
    lines.extend([
        "",
        "The bridge uses the existing ION Codex queue owner. It does not create a second queue, does not globally inject Capsule into other Codex CLI instances, and does not grant production/live authority.",
    ])
    return "\n".join(str(line) for line in lines)


def _append_codex_execution_status_turn(
    root: str | Path | None,
    *,
    source_turn_id: str,
    execution_mode: str,
    queue_result: Mapping[str, Any] | None,
    runner_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    state = load_dual_chat_state(root)
    now = _now()
    queue_link = queue_result.get("queue_link") if isinstance(queue_result, Mapping) and isinstance(queue_result.get("queue_link"), Mapping) else {}
    message = _execution_status_message(
        execution_mode=execution_mode,
        queue_result=queue_result,
        runner_result=runner_result,
    )
    turn = {
        "turn_id": f"exec_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(source_turn_id)}",
        "lane_id": "codex_general",
        "author": "codex_capsule",
        "kind": "execution_status",
        "message": message,
        "message_sha256": _sha256_text(message),
        "created_at": now,
        "source_turn_id": source_turn_id,
        "execution_mode": execution_mode,
        "request_id": queue_link.get("request_id"),
        "packet_path": queue_link.get("packet_path"),
        "queue_status": queue_link.get("status"),
        "runner_result": runner_result,
        "production_authority": False,
        "live_execution_authority": False,
    }
    state["lanes"]["codex_general"].setdefault("turns", []).append(turn)
    save_dual_chat_state(root, state)
    return turn


def record_chat_turn(
    root: str | Path | None,
    *,
    lane_id: str,
    message: str,
    author: str = "operator",
    execution_mode: str | None = None,
) -> dict[str, Any]:
    if lane_id not in LANES:
        return {"ok": False, "finding": "unknown_lane_id", "allowed_lanes": sorted(LANES)}
    text = _trim(message)
    if not text:
        return {"ok": False, "finding": "message_required"}
    resolved_execution_mode = _resolve_chat_execution_mode(execution_mode)
    normalized_author = _trim(author, limit=80) or "operator"
    if _is_ephemeral_playwright_smoke(
        text,
        lane_id=lane_id,
        author=normalized_author,
        execution_mode=resolved_execution_mode,
    ):
        return _playwright_smoke_turn_result(
            root,
            lane_id=lane_id,
            message=text,
            author=normalized_author,
            execution_mode=resolved_execution_mode,
        )
    state = load_dual_chat_state(root)
    prior_turns = list(state["lanes"].get(lane_id, {}).get("turns", [])) if isinstance(state.get("lanes"), Mapping) else []
    now = _now()
    turn_skill_context = build_codex_solo_context_model(root, write=True) if lane_id == "codex_general" else None
    turn_chat_engine = build_codex_chat_engine_turn(
        root,
        lane_id=lane_id,
        message=text,
        execution_mode=resolved_execution_mode if lane_id == "codex_general" else "ion_comms_projection",
        codex_solo_context=turn_skill_context,
    )
    turn_skill_activation = turn_chat_engine.get("skill_activation") if isinstance(turn_chat_engine.get("skill_activation"), Mapping) else build_ion_skill_activation(
        root,
        lane_id=lane_id,
        objective=text,
        execution_mode=resolved_execution_mode if lane_id == "codex_general" else "ion_comms_projection",
        codex_solo_context=turn_skill_context,
    )
    turn_id = f"turn_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(text)}"
    turn = {
        "turn_id": turn_id,
        "lane_id": lane_id,
        "author": normalized_author,
        "kind": "chat_turn",
        "message": text,
        "message_sha256": _sha256_text(text),
        "created_at": now,
        "execution_mode": resolved_execution_mode if lane_id == "codex_general" else "ion_comms_projection",
        "skill_activation": turn_skill_activation,
        "chat_engine": turn_chat_engine,
        "production_authority": False,
        "live_execution_authority": False,
    }
    state["lanes"][lane_id].setdefault("turns", []).append(turn)
    pipeline_run = None
    assistant_turn = None
    if lane_id == "ion_system":
        pipeline_run = _create_pipeline_run(turn)
        state.setdefault("pipeline_runs", []).append(pipeline_run)
    if lane_id == "codex_general" and turn["author"] in {"operator", "user"}:
        assistant_turn = _create_codex_capsule_assistant_turn(
            root,
            operator_text=text,
            created_at=now,
            execution_mode=resolved_execution_mode,
            chat_engine=turn_chat_engine,
            codex_solo_context=turn_skill_context,
            prior_turns=[turn for turn in prior_turns if isinstance(turn, Mapping)],
        )
        state["lanes"][lane_id].setdefault("turns", []).append(assistant_turn)
    save_dual_chat_state(root, state)
    queue_result = None
    runner_result = None
    execution_status_turn = None
    if lane_id == "codex_general" and turn["author"] in {"operator", "user"} and resolved_execution_mode in {"queue_for_codex", "queue_and_start"}:
        queue_result = queue_chat_codex_work_packet(
            root,
            lane_id="codex_general",
            objective=text,
            confirmation=WRITE_CONFIRMATION_TOKEN,
            source_turn_id=turn_id,
        )
        if resolved_execution_mode == "queue_and_start":
            if queue_result.get("ok") and _runner_start_enabled():
                runner_result = process_codex_queue_once(root, start=True, background=True)
            else:
                runner_result = {
                    "schema_id": "ion.codex_capsule_chat_runner_start_refusal.v1",
                    "ok": False,
                    "finding": "runner_start_not_enabled" if queue_result.get("ok") else "queue_not_ready",
                    "required_env": CHAT_RUNNER_START_ENV,
                    "production_authority": False,
                    "live_execution_authority": False,
                }
        execution_status_turn = _append_codex_execution_status_turn(
            root,
            source_turn_id=turn_id,
            execution_mode=resolved_execution_mode,
            queue_result=queue_result,
            runner_result=runner_result,
        )
    model = build_dual_codex_chat_model(root, write=True)
    return {
        "ok": True,
        "turn": turn,
        "assistant_turn": assistant_turn,
        "execution_mode": resolved_execution_mode,
        "queue_result": queue_result,
        "runner_result": runner_result,
        "execution_status_turn": execution_status_turn,
        "pipeline_run": pipeline_run,
        "model": model,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _create_pipeline_run(turn: Mapping[str, Any]) -> dict[str, Any]:
    run_id = f"ion_pipe_{str(turn.get('created_at')).replace(':', '').replace('+', 'Z')}_{_safe_slug(str(turn.get('turn_id') or 'turn'))}"
    stages = []
    for index, (stage_id, label, description) in enumerate(ION_PIPELINE_STAGES, start=1):
        model_move = build_codex_model_move_plan(
            lane_id="ion_system",
            stage_id=stage_id,
            objective=f"{label}: {description}",
        )
        stages.append({
            "index": index,
            "stage_id": stage_id,
            "label": label,
            "description": description,
            "status": "ready" if index == 1 else "pending",
            "model_move": model_move,
            "receipt_refs": [],
            "request_refs": [],
        })
    return {
        "schema_id": "ion.codex_capsule_chat_ion_comms_pipeline_projection.v1",
        "run_id": run_id,
        "source_turn_id": turn.get("turn_id"),
        "source_lane_id": turn.get("lane_id"),
        "status": "PIPELINE_PROJECTED_AWAITING_PROOF_GATED_WORK",
        "created_at": turn.get("created_at"),
        "stages": stages,
        "production_authority": False,
        "live_execution_authority": False,
    }


def queue_chat_codex_work_packet(
    root: str | Path | None,
    *,
    lane_id: str,
    objective: str,
    confirmation: str,
    source_turn_id: str | None = None,
) -> dict[str, Any]:
    if confirmation != WRITE_CONFIRMATION_TOKEN:
        return {"ok": False, "finding": "bounded_write_confirmation_required", "required_confirmation": WRITE_CONFIRMATION_TOKEN}
    if lane_id not in LANES:
        return {"ok": False, "finding": "unknown_lane_id", "allowed_lanes": sorted(LANES)}
    text = _trim(objective)
    if not text:
        return {"ok": False, "finding": "objective_required"}
    state = load_dual_chat_state(root)
    queued_text = text
    context_refs: list[str] = []
    codex_solo_context: dict[str, Any] | None = None
    stage_id = "mason_codex_work" if lane_id == "ion_system" else "codex_general_work"
    model_move = build_codex_model_move_plan(root, lane_id=lane_id, stage_id=stage_id, objective=text)
    skill_activation: dict[str, Any] | None = None
    if lane_id == "codex_general":
        codex_solo_context = build_codex_solo_context_model(root, write=True)
        context_refs = _codex_solo_context_refs(codex_solo_context)
        chat_engine_turn = build_codex_chat_engine_turn(
            root,
            lane_id=lane_id,
            message=text,
            execution_mode="queue_for_codex",
            codex_solo_context=codex_solo_context,
        )
        skill_activation = build_ion_skill_activation(
            root,
            lane_id=lane_id,
            objective=text,
            execution_mode="queue_for_codex",
            codex_solo_context=codex_solo_context,
            model_move=model_move,
        )
        if not codex_solo_context.get("ok"):
            model = build_dual_codex_chat_model(root, write=True)
            return {
                "ok": False,
                "finding": "codex_solo_context_not_ready",
                "codex_solo_context": codex_solo_context,
                "model": model,
                "production_authority": False,
                "live_execution_authority": False,
            }
        queued_text = _codex_general_queued_objective(text, codex_solo_context, model_move, skill_activation, chat_engine_turn)
    else:
        chat_engine_turn = build_codex_chat_engine_turn(
            root,
            lane_id=lane_id,
            message=text,
            execution_mode="ion_comms_projection",
        )
        skill_activation = build_ion_skill_activation(
            root,
            lane_id=lane_id,
            objective=text,
            execution_mode="ion_comms_projection",
            model_move=model_move,
        )
    result = call_chatgpt_connector_tool(
        root,
        "ion_request_codex_work_packet",
        {
            "objective": queued_text,
            "codex_model_move": model_move,
            "required_context_reads": [{"path": ref, "kind": "file", "required": True} for ref in context_refs],
            "ion_skill_activation": skill_activation,
            "ion_chat_engine_turn": chat_engine_turn,
            "request_kind": (chat_engine_turn.get("carrier_strategy") or {}).get("request_kind") if isinstance(chat_engine_turn.get("carrier_strategy"), Mapping) else "codex_work",
        },
    )
    data = result.get("data") if isinstance(result.get("data"), Mapping) else {}
    link = {
        "created_at": _now(),
        "lane_id": lane_id,
        "source_turn_id": source_turn_id,
        "objective": text,
        "queued_objective_sha256": _sha256_text(queued_text),
        "context_refs": context_refs,
        "codex_solo_context_verdict": (codex_solo_context or {}).get("verdict"),
        "skill_activation": skill_activation,
        "chat_engine": chat_engine_turn,
        "model_move": model_move,
        "model_move_summary": summarize_model_move(model_move),
        "request_id": data.get("request_id"),
        "packet_path": data.get("packet_path"),
        "status": "QUEUED_FOR_CODEX_CARRIER" if result.get("ok") else "QUEUE_REQUEST_BLOCKED",
        "result": result,
    }
    state["lanes"][lane_id].setdefault("queue_links", []).append(link)
    if lane_id == "ion_system" and state.get("pipeline_runs"):
        latest = state["pipeline_runs"][-1]
        if isinstance(latest, dict):
            for stage in latest.get("stages", []):
                if stage.get("stage_id") == "mason_codex_work":
                    stage["status"] = "queued_for_codex_carrier" if result.get("ok") else "queue_blocked"
                    stage["model_move"] = model_move
                    stage.setdefault("request_refs", []).append(data.get("packet_path"))
            latest["status"] = "CODEX_WORK_PACKET_QUEUED" if result.get("ok") else "CODEX_WORK_PACKET_BLOCKED"
    save_dual_chat_state(root, state)
    solo_post = None
    if lane_id == "codex_general":
        evidence = [ref for ref in context_refs if ref]
        if data.get("packet_path"):
            evidence.append(str(data.get("packet_path")))
        solo_post = record_codex_solo_post(
            root,
            summary=f"Queued Codex solo work packet: {text}",
            evidence_paths=evidence,
            status=link["status"],
            next_action="Wait for Codex task return, then verify proof and update capsule route.",
        )
    model = build_dual_codex_chat_model(root, write=True)
    return {
        "ok": bool(result.get("ok")),
        "queue_link": link,
        "codex_solo_post": solo_post,
        "connector_result": result,
        "model": model,
        "production_authority": False,
        "live_execution_authority": False,
    }


def pin_dual_chat_memory(
    root: str | Path | None,
    *,
    lane_id: str,
    text: str,
    confirmation: str,
    source_turn_id: str | None = None,
    write_codex_memory: bool = True,
) -> dict[str, Any]:
    if confirmation != WRITE_CONFIRMATION_TOKEN:
        return {"ok": False, "finding": "bounded_write_confirmation_required", "required_confirmation": WRITE_CONFIRMATION_TOKEN}
    if lane_id not in LANES:
        return {"ok": False, "finding": "unknown_lane_id", "allowed_lanes": sorted(LANES)}
    memory_text = _trim(text, limit=4000)
    if not memory_text:
        return {"ok": False, "finding": "memory_text_required"}
    state = load_dual_chat_state(root)
    now = _now()
    pin = {
        "pin_id": f"mem_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(memory_text)}",
        "lane_id": lane_id,
        "source_turn_id": source_turn_id,
        "text": memory_text,
        "text_sha256": _sha256_text(memory_text),
        "created_at": now,
        "status": "active",
        "memory_scope": "repo_and_codex_memory",
        "production_authority": False,
        "live_execution_authority": False,
    }
    state.setdefault("memory", {}).setdefault("pins", []).append(pin)
    codex_memory_path = Path(str(state["memory"].get("codex_memory_path") or DEFAULT_CODEX_MEMORY_PATH)).expanduser()
    if write_codex_memory:
        codex_memory_path.parent.mkdir(parents=True, exist_ok=True)
        existing = codex_memory_path.read_text(encoding="utf-8", errors="replace") if codex_memory_path.exists() else "# ION Codex Chat Memory\n\n"
        entry = "\n".join([
            f"## {pin['pin_id']}",
            f"- created_at: {now}",
            f"- lane_id: {lane_id}",
            f"- source_turn_id: {source_turn_id or 'none'}",
            f"- text_sha256: {pin['text_sha256']}",
            "",
            memory_text,
            "",
        ])
        codex_memory_path.write_text(existing.rstrip() + "\n\n" + entry, encoding="utf-8")
    state["memory"]["codex_memory_path"] = str(codex_memory_path)
    save_dual_chat_state(root, state)
    solo_post = None
    if lane_id == "codex_general":
        solo_post = record_codex_solo_post(
            root,
            summary=f"Pinned Codex solo memory: {memory_text}",
            evidence_paths=[str(codex_memory_path)],
            status="MEMORY_PINNED",
            next_action="Use pinned memory only as explicit witness context for later Codex work.",
        )
    model = build_dual_codex_chat_model(root, write=True)
    return {"ok": True, "pin": pin, "codex_memory_path": str(codex_memory_path), "codex_solo_post": solo_post, "model": model}


def _e(value: Any) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def _chat_turn_groups(
    turns: list[Mapping[str, Any]],
    *,
    return_records: list[Mapping[str, Any]] | None = None,
    turn_traces: list[Mapping[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    returns_by_source: dict[str, list[dict[str, Any]]] = {}
    for raw_record in return_records or []:
        if not isinstance(raw_record, Mapping):
            continue
        source_turn_id = str(raw_record.get("source_turn_id") or "").strip()
        if source_turn_id:
            returns_by_source.setdefault(source_turn_id, []).append(dict(raw_record))
    traces_by_turn = {
        str(trace.get("turn_id")): dict(trace)
        for trace in turn_traces or []
        if isinstance(trace, Mapping) and trace.get("turn_id")
    }
    groups: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw_turn in turns:
        turn = dict(raw_turn)
        kind = str(turn.get("kind") or "chat_turn")
        author = str(turn.get("author") or "")
        if kind == "chat_turn" and author in {"operator", "user"}:
            current = {
                "group_id": turn.get("turn_id"),
                "created_at": turn.get("created_at"),
                "user_turn": turn,
                "assistant_turns": [],
                "execution_turns": [],
                "return_records": returns_by_source.get(str(turn.get("turn_id") or ""), []),
                "turn_trace": traces_by_turn.get(str(turn.get("turn_id") or "")),
                "context_turns": [],
                "other_turns": [],
            }
            groups.append(current)
            continue
        if current is None:
            current = {
                "group_id": f"system_{len(groups) + 1}",
                "created_at": turn.get("created_at"),
                "user_turn": None,
                "assistant_turns": [],
                "execution_turns": [],
                "return_records": [],
                "turn_trace": None,
                "context_turns": [],
                "other_turns": [],
            }
            groups.append(current)
        if kind == "assistant_response":
            current["assistant_turns"].append(turn)
        elif kind == "execution_status":
            current["execution_turns"].append(turn)
        elif kind == "mini_auto_post":
            current["context_turns"].append(turn)
        else:
            current["other_turns"].append(turn)
    return groups


def build_codex_capsule_chat_ui_model(model: Mapping[str, Any]) -> dict[str, Any]:
    lanes = model.get("lanes") if isinstance(model.get("lanes"), Mapping) else {}
    codex_lane = lanes.get("codex_general") if isinstance(lanes.get("codex_general"), Mapping) else {}
    turns = [turn for turn in codex_lane.get("turns", []) if isinstance(turn, Mapping)]
    codex_solo = model.get("codex_solo_context") if isinstance(model.get("codex_solo_context"), Mapping) else {}
    capsule = codex_solo.get("capsule") if isinstance(codex_solo.get("capsule"), Mapping) else {}
    mini = codex_solo.get("mini") if isinstance(codex_solo.get("mini"), Mapping) else {}
    route = codex_solo.get("route") if isinstance(codex_solo.get("route"), Mapping) else {}
    long_horizon = codex_solo.get("long_horizon") if isinstance(codex_solo.get("long_horizon"), Mapping) else {}
    context_packages = codex_solo.get("context_packages") if isinstance(codex_solo.get("context_packages"), Mapping) else {}
    queue = model.get("codex_queue") if isinstance(model.get("codex_queue"), Mapping) else {}
    runner = queue.get("runner") if isinstance(queue.get("runner"), Mapping) else {}
    latest_work_requests = queue.get("latest_work_requests") if isinstance(queue.get("latest_work_requests"), list) else []
    latest_task_returns = queue.get("latest_task_returns") if isinstance(queue.get("latest_task_returns"), list) else []
    return_hydration = queue.get("return_hydration") if isinstance(queue.get("return_hydration"), Mapping) else {}
    hydrated_return_records = [
        record for record in return_hydration.get("records", []) if isinstance(record, Mapping)
    ]
    turn_trace_index = model.get("turn_traces") if isinstance(model.get("turn_traces"), Mapping) else {}
    turn_trace_records = [
        trace for trace in turn_trace_index.get("traces", []) if isinstance(trace, Mapping)
    ]
    agents = model.get("agents") if isinstance(model.get("agents"), Mapping) else {}
    skills = model.get("skills") if isinstance(model.get("skills"), Mapping) else {}
    chat_engine = model.get("chat_engine") if isinstance(model.get("chat_engine"), Mapping) else {}
    assistant_work_routes = model.get("assistant_work_routes") if isinstance(model.get("assistant_work_routes"), Mapping) else {}
    chat_response_carrier = model.get("chat_response_carrier") if isinstance(model.get("chat_response_carrier"), Mapping) else {}
    response_runs = model.get("response_runs") if isinstance(model.get("response_runs"), Mapping) else {}
    execution_bridge = model.get("execution_bridge") if isinstance(model.get("execution_bridge"), Mapping) else {}
    remote_access = model.get("remote_access") if isinstance(model.get("remote_access"), Mapping) else {}
    ion_comms = model.get("ion_comms") if isinstance(model.get("ion_comms"), Mapping) else {}
    memory = model.get("memory") if isinstance(model.get("memory"), Mapping) else {}
    route_entries = route.get("entries") if isinstance(route.get("entries"), list) else []
    missing_route = [
        entry.get("path")
        for entry in route_entries
        if isinstance(entry, Mapping) and not entry.get("exists")
    ]
    latest_capsule_rows = capsule.get("recent_rows") if isinstance(capsule.get("recent_rows"), list) else []
    latest_receipt = latest_capsule_rows[-1] if latest_capsule_rows else None
    current_skill = skills.get("current_activation") if isinstance(skills.get("current_activation"), Mapping) else {}
    conversation_summary = {
        "turn_count": len(turns),
        "user_turn_count": sum(1 for turn in turns if turn.get("kind", "chat_turn") == "chat_turn" and turn.get("author") in {"operator", "user"}),
        "assistant_turn_count": sum(1 for turn in turns if turn.get("kind") == "assistant_response"),
        "execution_status_count": sum(1 for turn in turns if turn.get("kind") == "execution_status"),
        "hydrated_return_count": len(hydrated_return_records),
        "turn_trace_count": len(turn_trace_records),
        "proof_accepted_count": sum(1 for record in hydrated_return_records if record.get("proof_status") == "accepted"),
        "proof_blocked_count": sum(1 for record in hydrated_return_records if record.get("proof_status") == "blocked"),
        "latest_receipt": latest_receipt,
    }
    activity = []
    if runner:
        activity.append({
            "kind": "runner",
            "status": "active" if runner.get("active_process_running") else "idle",
            "label": runner.get("verdict") or "Codex runner",
            "detail": runner.get("next_request_path") or "no queued request selected",
        })
    for item in latest_work_requests[:3]:
        if isinstance(item, Mapping):
            activity.append({
                "kind": "work_request",
                "status": "queued",
                "label": item.get("name") or "work request",
                "detail": item.get("path"),
            })
    for item in latest_task_returns[:3]:
        if isinstance(item, Mapping):
            activity.append({
                "kind": "task_return",
                "status": "returned",
                "label": item.get("name") or "task return",
                "detail": item.get("path"),
            })
    context_drawer = {
        "mini_text": mini.get("text") or "",
        "recent_rows": latest_capsule_rows,
        "route_ok": route.get("ok"),
        "missing_route": missing_route,
        "long_horizon": long_horizon,
        "selected_packages": context_packages.get("selected_by_default", []),
        "memory_visualization": model.get("memory_visualization") if isinstance(model.get("memory_visualization"), Mapping) else {},
    }
    return {
        "schema_id": "ion.codex_capsule_chat_ui_model.v1",
        "layout": {
            "mode": "joc_shell_chat_first",
            "zones": ["top_bar", "left_icon_rail", "left_drawer", "main_work_surface", "right_inspector", "right_icon_rail", "bottom_timeline"],
            "primary_surface": "main_chat",
            "default_page_id": "chat",
        },
        "top_bar": {
            "title": "ION Codex",
            "subtitle": "Chat",
            "page_tabs": [
                {"id": "chat", "label": "Chat"},
                {"id": "context", "label": "Context"},
                {"id": "runs", "label": "Runs"},
                {"id": "agents", "label": "Agents"},
                {"id": "receipts", "label": "Receipts"},
                {"id": "settings", "label": "Settings"},
            ],
            "status_chips": [
                {"label": "chat", "value": model.get("verdict"), "tone": "ready"},
                {"label": "context", "value": "Capsule" if codex_solo.get("ok") else codex_solo.get("verdict"), "tone": "ready" if codex_solo.get("ok") else "blocked"},
                {"label": "skill", "value": current_skill.get("display_name") or "none", "tone": "ready" if skills.get("ok") else "blocked"},
                {"label": "engine", "value": chat_engine.get("verdict") or "unknown", "tone": "ready" if chat_engine.get("ok") else "blocked"},
                {"label": "routes", "value": assistant_work_routes.get("route_count", 0), "tone": "ready" if assistant_work_routes.get("ok") else "watch"},
                {"label": "carrier", "value": "enabled" if chat_response_carrier.get("enabled") else "fallback", "tone": "ready" if chat_response_carrier.get("enabled") else "watch"},
                {"label": "queue", "value": runner.get("queued_request_count", 0), "tone": "watch"},
                {"label": "runner", "value": runner.get("active_process_running", False), "tone": "watch"},
                {"label": "public", "value": remote_access.get("enabled_by_model", False), "tone": "watch"},
            ],
        },
        "left_rail": [
            {"id": "composer", "label": "Composer", "icon": "chat"},
            {"id": "models", "label": "Models", "icon": "route"},
            {"id": "skills", "label": "Skills", "icon": "skills"},
            {"id": "context-lens", "label": "Context Lens", "icon": "graph"},
            {"id": "run-mode", "label": "Run Mode", "icon": "runs"},
        ],
        "left_drawer": {
            "active_panel_id": "composer",
            "panels": [
                {
                    "id": "composer",
                    "title": "Composer",
                    "summary": "Primary user-facing Codex chat composer.",
                    "items": [
                        {"label": "Default mode", "value": execution_bridge.get("default_mode")},
                        {"label": "Run mode", "value": "queue_for_codex"},
                        {"label": "Runner start", "value": execution_bridge.get("runner_start_enabled", False)},
                    ],
                },
                {
                    "id": "models",
                    "title": "Models",
                    "summary": "Current model move hints for this chat lane.",
                    "items": [
                        {"label": "Routing posture", "value": DEFAULT_ROUTING_POSTURE},
                        {"label": "Usage authority", "value": "operator_observed_hint"},
                        {"label": "Production", "value": False},
                    ],
                },
                {
                    "id": "skills",
                    "title": "Skills",
                    "summary": "Skills activate workflows; templates remain proof gates.",
                    "items": [
                        {"label": "Current", "value": current_skill.get("display_name") or "none"},
                        {"label": "Registered", "value": skills.get("skill_count", 0)},
                        {"label": "State gate", "value": current_skill.get("state_acceptance_granted", False)},
                    ],
                },
                {
                    "id": "context-lens",
                    "title": "Context Lens",
                    "summary": "Capsule is the minimum context; Mini is the lookup index.",
                    "items": [
                        {"label": "Route OK", "value": route.get("ok")},
                        {"label": "Packages", "value": context_packages.get("package_count", 0)},
                        {"label": "Missing routes", "value": len(missing_route)},
                    ],
                },
                {
                    "id": "run-mode",
                    "title": "Run Mode",
                    "summary": "State-changing work remains proof-gated through the existing Codex queue.",
                    "items": [
                        {"label": "Queued", "value": runner.get("queued_request_count", 0)},
                        {"label": "Runner active", "value": runner.get("active_process_running", False)},
                        {"label": "Live authority", "value": False},
                    ],
                },
            ],
        },
        "right_rail": [
            {"id": "assistant", "label": "Assistant", "icon": "chat"},
            {"id": "context", "label": "Context", "icon": "graph"},
            {"id": "evidence", "label": "Evidence", "icon": "receipts"},
            {"id": "system", "label": "System", "icon": "agents"},
            {"id": "settings", "label": "Settings", "icon": "settings"},
        ],
        "composer": {
            "action": "/chat/turn",
            "lane_id": "codex_general",
            "primary_mode": "respond_only",
            "primary_label": "Send",
            "run_mode": "queue_for_codex",
            "run_label": "Run task",
            "allowed_execution_modes": execution_bridge.get("allowed_modes", ["respond_only"]),
            "runner_start_enabled": execution_bridge.get("runner_start_enabled", False),
        },
        "conversation": {
            "summary": conversation_summary,
            "turn_groups": _chat_turn_groups(
                turns[-80:],
                return_records=hydrated_return_records,
                turn_traces=turn_trace_records,
            ),
            "empty_state": "Ask Codex.",
        },
        "pages": {
            "context": {
                "title": "Context",
                "summary": "Visual projection of Capsule, Mini, long-horizon, route, and carrier context.",
            },
            "runs": {
                "title": "Runs",
                "summary": "Read-only view of queue, response carrier, runner, and proof-return state.",
            },
            "agents": {
                "title": "Agents",
                "summary": "Read-only existing ION agent broker projection. No second agent system.",
            },
            "receipts": {
                "title": "Receipts",
                "summary": "Capsule, task-return, and proof evidence surfaces.",
            },
            "settings": {
                "title": "Settings",
                "summary": "Local execution, public access, and service posture.",
            },
        },
        "drawers": {
            "timeline": turn_trace_index,
            "skills": skills,
            "chat_engine": chat_engine,
            "assistant_work_routes": assistant_work_routes,
            "carrier": chat_response_carrier,
            "agents": agents,
            "context": context_drawer,
            "capsule": context_drawer,
            "runs": {
                "runner": runner,
                "latest_work_requests": latest_work_requests,
                "latest_task_returns": latest_task_returns,
                "return_hydration": return_hydration,
                "response_runs": response_runs,
            },
            "receipts": {
                "capsule_recent_rows": latest_capsule_rows,
                "history_path": "ION/05_context/current/codex_solo/history",
            },
            "ion": {
                "mode": ion_comms.get("mode"),
                "creates_second_queue": ion_comms.get("creates_second_queue"),
                "creates_second_agent_system": ion_comms.get("creates_second_agent_system"),
                "digest": ion_comms.get("digest"),
            },
            "settings": {
                "execution_bridge": execution_bridge,
                "response_carrier": chat_response_carrier,
                "memory_path": memory.get("codex_memory_path"),
                "remote_access": remote_access,
            },
        },
        "bottom_timeline": {
            "lanes": [
                {"id": "all", "label": "All", "count": len(activity)},
                {"id": "runner", "label": "Runner", "count": sum(1 for item in activity if item.get("kind") == "runner")},
                {"id": "work_request", "label": "Requests", "count": sum(1 for item in activity if item.get("kind") == "work_request")},
                {"id": "task_return", "label": "Returns", "count": sum(1 for item in activity if item.get("kind") == "task_return")},
            ],
            "items": activity[:8],
        },
        "activity": activity[:8],
        "production_authority": False,
        "live_execution_authority": False,
    }


def render_dual_codex_chat_html(model: Mapping[str, Any], *, base_path: str = "/chat", auth_token: str | None = None) -> str:
    return render_codex_chat_app_html(model, base_path=base_path, auth_token=auth_token)
