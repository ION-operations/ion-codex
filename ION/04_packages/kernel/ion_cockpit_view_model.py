"""ION cockpit view-model projection.

This module is intentionally small and dependency-free. It reads the live ION
runtime packet layer and emits a normalized cockpit projection that the
Cursor/VS Code extension and JOC React shell can render without guessing from
chat memory.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .ion_agent_invocation_broker import build_agent_broker_status
from .ion_chatgpt_sandbox_return_intake import build_sandbox_return_queue_projection
from .ion_codex_queue_runner import build_codex_queue_runner_status
from .ion_cockpit_service_manager import build_service_console_model
from .ion_local_service_status import build_local_service_status

CURRENT = Path("ION/05_context/current")
SIGNALS = Path("ION/05_context/signals")
REPORTS = Path("ION/docs/consolidation")

ACTIVE_FILES = {
    "hook": CURRENT / "ACTIVE_CURSOR_HOOK_STATE.json",
    "work": CURRENT / "ACTIVE_WORK_PACKET.json",
    "spawn": CURRENT / "ACTIVE_ROLE_SPAWN_PLAN.json",
    "turn": CURRENT / "ACTIVE_CARRIER_TURN_PACKET.json",
    "ledger": CURRENT / "ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
    "steward": CURRENT / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
    "operator_queue": CURRENT / "ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
    "human_gates": CURRENT / "ACTIVE_HUMAN_GATE_QUEUE.json",
    "front_door_proof_trace": CURRENT / "ACTIVE_FRONT_DOOR_PROOF_TRACE.json",
    "lane_timeline": CURRENT / "ACTIVE_LANE_TIMELINE_VIEW_MODEL.json",
    "receipt_hydration": CURRENT / "ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json",
    "runtime_debug_overlay": CURRENT / "ACTIVE_RUNTIME_DEBUG_OVERLAY.json",
    "v72_mcp_donor_reconciliation": CURRENT / "V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json",
}
DEFAULT_SAFE_FULL_PROJECT_PACKAGE_RESULT = CURRENT / "SAFE_FULL_PROJECT_PACKAGE_RESULT_V110.json"
HELIXION_REBUILD_PLAN = Path("ION/02_architecture/HELIXION_JOC_DAIMON_WISDOMNET_MASTER_EVOLUTION_PLAN.md")
HELIXION_REBUILD_REGISTRY = Path("ION/03_registry/helixion_joc_evolution_registry.yaml")
HELIXION_REBUILD_CURRENT_PLAN = CURRENT / "helixion_joc_rebuild/HELIXION_JOC_REBUILD_CURRENT_PLAN.json"
CODEX_CAPSULE_CHAT_MODEL = CURRENT / "ACTIVE_CODEX_CAPSULE_CHAT_MODEL.json"
PORTABLE_COMPANION_PRODUCT_CONTEXT = CURRENT / "portable_ion_page_companion/PORTABLE_ION_PAGE_COMPANION_001_PRODUCT_CONTEXT.json"
DOM_PERCEPTION_TASK_RETURN = CURRENT / "browser_perception/DOM_PERCEPTION_001/TASK_RETURN_DOM_PERCEPTION_001.md"
DOM_PERCEPTION_DOMAIN_REGISTRY = Path("ION/03_registry/browser_perception_domain_registry_proposal.yaml")
BROWSER_EXTENSION_ROOT = Path("ION/09_integrations/browser_extension/ion_chatops_bridge")
BROWSER_EXTENSION_MANIFEST = BROWSER_EXTENSION_ROOT / "manifest.json"
BROWSER_EXTENSION_AGENT_CONTRACT = BROWSER_EXTENSION_ROOT / "AGENT_INVOCATION_LANE_CONTRACT.json"
BROWSER_EXTENSION_QUEUE_PACK_AUTHORING = BROWSER_EXTENSION_ROOT / "QUEUE_PACK_AUTHORING.md"
CODEX_CONTEXT_PACKAGES = CURRENT / "codex_solo/CONTEXT_PACKAGES.json"
CUSTOM_GPT_CAPSULE_SYSTEM_DIR = CURRENT / "custom_gpt_capsule_system"
CUSTOM_GPT_FACTORY_DIR = CURRENT / "custom_gpt_factory"
ARTIFACT_PACKAGES_DIR = Path("ION/06_artifacts/packages")

OUTPUT = CURRENT / "ACTIVE_COCKPIT_VIEW_MODEL.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    try:
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive projection, not authority
        return {"_read_error": str(exc), "_path": str(path)}


def latest_safe_package_result_rel(root: Path) -> Path:
    current = root / CURRENT
    candidates = sorted(current.glob("SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json"))
    if not candidates:
        return DEFAULT_SAFE_FULL_PROJECT_PACKAGE_RESULT
    return candidates[-1].relative_to(root)


def compact(value: Any, fallback: str = "unknown") -> str:
    if value is None:
        return fallback
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    return fallback


def listify(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def status_from_findings(findings: Iterable[Any], blocked: bool = False) -> str:
    if blocked:
        return "blocked"
    return "ready" if not list(findings) else "degraded"


def _spawn_rows(spawn: dict[str, Any], turn: dict[str, Any]) -> list[dict[str, Any]]:
    rows = listify(spawn.get("role_spawn_plan"))
    if rows:
        return rows
    for item in listify(turn.get("spawn_queue")):
        if isinstance(item, dict):
            rows.append(item)
    return rows


def _ledger_records(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    return [r for r in listify(ledger.get("records")) if isinstance(r, dict)]


def _steward_items(steward: dict[str, Any]) -> list[dict[str, Any]]:
    return [i for i in listify(steward.get("items")) if isinstance(i, dict)]


def _operator_items(queue: dict[str, Any]) -> list[dict[str, Any]]:
    return [i for i in listify(queue.get("items")) if isinstance(i, dict)]


def _gates(gates: dict[str, Any]) -> list[dict[str, Any]]:
    return [g for g in listify(gates.get("gates")) if isinstance(g, dict)]


def _spawn_count(rows: list[dict[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("spawn") is True or str(row.get("spawn", "")).lower() == "true")


def _deferred_spawn_count(rows: list[dict[str, Any]]) -> int:
    return sum(
        1
        for row in rows
        if row.get("spawn") is not True and (row.get("spawn_intent") is True or row.get("spawn_deferral_reason"))
    )


def _active_spawn_queue_count(turn: dict[str, Any], spawn_rows: list[dict[str, Any]]) -> int:
    if isinstance(turn.get("spawn_queue"), list):
        return len([row for row in turn.get("spawn_queue", []) if isinstance(row, dict)])
    return _spawn_count(spawn_rows)


def _return_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"accepted": 0, "rejected": 0, "pending": 0, "needs_human_review": 0}
    for record in records:
        if record.get("accepted") is True:
            counts["accepted"] += 1
            continue
        if record.get("accepted") is False:
            counts["rejected"] += 1
            continue
        decision = str(record.get("decision") or record.get("status") or "pending").lower()
        if "accept" in decision:
            counts["accepted"] += 1
        elif "human" in decision or "review" in decision:
            counts["needs_human_review"] += 1
        elif "reject" in decision or "fail" in decision:
            counts["rejected"] += 1
        else:
            counts["pending"] += 1
    return counts


def _authority_for_return(record: dict[str, Any]) -> str:
    if record.get("accepted") is True:
        return "ACCEPTED_TASK_RETURN"
    if record.get("accepted") is False:
        return "REJECTED_TASK_RETURN"
    decision = str(record.get("decision") or record.get("status") or "pending").lower()
    if "accept" in decision:
        return "ACCEPTED_TASK_RETURN"
    if "reject" in decision or "fail" in decision:
        return "REJECTED_TASK_RETURN"
    if "human" in decision or "review" in decision:
        return "HUMAN_GATE_REQUIRED"
    return "PENDING_TASK_RETURN"


def summarize_agents(spawn_rows: list[dict[str, Any]], records: list[dict[str, Any]]) -> dict[str, Any]:
    return_index = {}
    for record in records:
        key = (str(record.get("role", "")).upper(), str(record.get("index", record.get("spawn_index", ""))))
        return_index[key] = record

    rows = []
    context_packages = []
    for idx, row in enumerate(spawn_rows, start=1):
        role = compact(row.get("role") or row.get("display_name"), f"ROW_{idx}").upper()
        row_index = compact(row.get("index"), str(idx))
        record = return_index.get((role, row_index), {})
        ctx_path = row.get("context_package_path") or row.get("session_context_package_path") or row.get("context_package")
        receipt_path = row.get("context_load_receipt_path") or row.get("receipt_path")
        rows.append(
            {
                "index": row_index,
                "role": role,
                "spawn": bool(row.get("spawn", False)),
                "status": "return_captured" if record else ("spawn_pending" if row.get("spawn") else "not_spawned"),
                "context_package_path": ctx_path,
                "context_load_receipt_path": receipt_path,
                "authority_class": _authority_for_return(record) if record else "ACTIVE_RUNTIME_AUTHORITY",
                "return_recorded": bool(record),
            }
        )
        if ctx_path:
            context_packages.append(
                {
                    "role": role,
                    "index": row_index,
                    "path": ctx_path,
                    "receipt_path": receipt_path,
                    "authority_class": "ACTIVE_RUNTIME_AUTHORITY",
                }
            )
    return {
        "spawn_rows": rows,
        "context_packages": context_packages,
        "returns": [
            {
                "role": compact(record.get("role"), "unknown").upper(),
                "index": compact(record.get("index") or record.get("spawn_index"), "unknown"),
                "decision": compact(record.get("decision") or record.get("status"), "pending"),
                "path": record.get("task_output_path") or record.get("output_path"),
                "authority_class": _authority_for_return(record),
            }
            for record in records
        ],
    }


def synthesize_timeline(data: dict[str, dict[str, Any]], counts: dict[str, Any], active_files: dict[str, Path] | None = None) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    paths = active_files or ACTIVE_FILES

    def add(kind: str, label: str, status: str, path: Path, detail: str = "") -> None:
        payload = data.get(kind, {})
        stamp = payload.get("updated_at") or payload.get("created_at") or payload.get("installed_at") or utc_now()
        events.append(
            {
                "time": stamp,
                "source": kind,
                "event_type": label,
                "status": status,
                "path": str(path),
                "detail": detail,
            }
        )

    add("hook", "cursor hook state", compact(data.get("hook", {}).get("status"), "unknown"), paths["hook"])
    add("work", "work packet", "ready" if data.get("work") else "missing", paths["work"], compact(data.get("work", {}).get("objective"), "no objective"))
    add("turn", "carrier turn", "blocked" if data.get("turn", {}).get("blocked_by_findings") else "ready", paths["turn"])
    add("spawn", "spawn plan", "ready", paths["spawn"], f"spawn rows: {counts['spawn_rows']}")
    add("ledger", "task-return ledger", "ready", paths["ledger"], f"accepted: {counts['returns']['accepted']} rejected: {counts['returns']['rejected']}")
    add("steward", "steward queue", "ready", paths["steward"], f"items: {counts['steward_queue']}")
    add("operator_queue", "operator queue", "ready", paths["operator_queue"], f"pending: {counts['operator_queue_pending']}")
    add("human_gates", "human gate queue", "blocked" if counts["open_gates"] else "ready", paths["human_gates"], f"open: {counts['open_gates']}")
    safe_package = data.get("safe_full_project_package", {})
    safe_package_root = safe_package.get("zip_root_audit", {}) if isinstance(safe_package.get("zip_root_audit"), dict) else {}
    add(
        "safe_full_project_package",
        "safe full-project package",
        "ready" if safe_package.get("accepted") is True and safe_package_root.get("verdict") == "ZIP_ROOT_CONFIRMED" else "degraded",
        paths["safe_full_project_package"],
        compact(safe_package_root.get("archive_root_mode"), "no safe package result"),
    )
    donor = data.get("v72_mcp_donor_reconciliation", {})
    donor_verdict = compact(donor.get("reconciliation_verdict"), "no donor reconciliation audit")
    add(
        "v72_mcp_donor_reconciliation",
        "V72 MCP donor reconciliation",
        "ready" if donor_verdict == "V72_MCP_DONOR_RECONCILIATION_PASS" else "degraded",
        paths["v72_mcp_donor_reconciliation"],
        f"{donor_verdict}; restored: {compact(donor.get('restored_donor_surface_count'), '0')}; forbidden runtime: {compact(donor.get('forbidden_runtime_file_count'), '0')}",
    )
    front_door = data.get("front_door_proof_trace", {})
    add(
        "front_door_proof_trace",
        "front-door proof trace",
        "ready" if front_door.get("proof_complete") else "degraded",
        paths["front_door_proof_trace"],
        compact(front_door.get("verdict"), "no front-door proof trace"),
    )
    return events


def recent_receipts(root: Path, limit: int = 12) -> list[dict[str, Any]]:
    candidates: list[Path] = []
    for base in (root / SIGNALS, root / REPORTS):
        if base.exists():
            candidates.extend([p for p in base.iterdir() if p.is_file() and p.suffix.lower() in {".txt", ".md", ".json"}])
    candidates.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
    return [
        {
            "path": str(p.relative_to(root)),
            "name": p.name,
            "authority_class": "ACTIVE_RUNTIME_AUTHORITY" if "receipt" in p.name.lower() else "WITNESS_INPUT",
        }
        for p in candidates[:limit]
    ]


def _latest_files(root: Path, rel: str, *, limit: int = 5) -> list[dict[str, Any]]:
    base = root / rel
    if not base.exists():
        return []
    files = sorted([path for path in base.glob("*.json") if path.is_file()], key=lambda path: path.stat().st_mtime, reverse=True)
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "name": path.name,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
        }
        for path in files[:limit]
    ]


def _latest_paths(root: Path, rel: str, *, limit: int = 8, suffixes: set[str] | None = None, recursive: bool = False) -> list[dict[str, Any]]:
    base = root / rel
    if not base.exists():
        return []
    iterator = base.rglob("*") if recursive else base.glob("*")
    files = [path for path in iterator if path.is_file() and (suffixes is None or path.suffix.lower() in suffixes)]
    files.sort(key=lambda path: path.stat().st_mtime if path.exists() else 0, reverse=True)
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "name": path.name,
            "suffix": path.suffix.lower(),
            "bytes": path.stat().st_size if path.exists() else 0,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
        }
        for path in files[:limit]
    ]


def _read_text(path: Path) -> str:
    try:
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _profile_scalar(text: str, key: str) -> str | None:
    prefix = f"{key}:"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            value = stripped[len(prefix):].strip().strip("\"'")
            return value or None
    return None


def _chatgpt_browser_profile_summary(root: Path) -> dict[str, Any]:
    path = Path("ION/03_registry/chatgpt_browser_carrier_profile.yaml")
    text = _read_text(root / path)
    return {
        "profile_path": path.as_posix(),
        "carrier_id": _profile_scalar(text, "carrier_id"),
        "project_facing_callsign": _profile_scalar(text, "project_facing_callsign"),
        "callsign_authority": _profile_scalar(text, "callsign_authority"),
        "callsign_decision_receipt": _profile_scalar(text, "callsign_decision_receipt"),
    }


def _chatgpt_browser_mcp_summary(root: Path) -> dict[str, Any]:
    contract = read_json(root / CURRENT / "CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_V120.json")
    http_preview = read_json(root / CURRENT / "CHATGPT_BROWSER_HTTP_MCP_PREVIEW_V121.json")
    tunnel = read_json(root / CURRENT / "CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json")
    carrier_queue = read_json(root / CURRENT / "ACTIVE_CARRIER_MESSAGE_QUEUE.json")
    work_queue = read_json(root / CURRENT / "ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json")
    profile = _chatgpt_browser_profile_summary(root)
    uploads = _latest_files(root, "ION/05_context/current/chatgpt_connector/artifact_uploads")
    upload_payloads = [read_json(root / item["path"]) for item in uploads]
    upload_status_counts: dict[str, int] = {}
    for payload in upload_payloads:
        status = compact(payload.get("status"), "unknown")
        upload_status_counts[status] = upload_status_counts.get(status, 0) + 1
    tools = listify(contract.get("allowed_tools"))
    first_parity = [
        "ion_file_put_text",
        "ion_artifact_upload_init",
        "ion_artifact_upload_chunk",
        "ion_artifact_upload_commit",
        "ion_carrier_message_send",
        "ion_carrier_message_poll",
        "ion_carrier_message_ack",
    ]
    next_visibility = [
        "ion_file_read",
        "ion_file_search",
        "ion_tree_list",
        "ion_registry_read",
        "ion_template_read",
        "ion_context_compile",
        "ion_receipt_hydrate",
        "ion_tool_manifest",
    ]
    agent_tools = [
        "ion_agent_list",
        "ion_agent_status",
        "ion_agent_result",
        "ion_agent_queue",
        "ion_agent_spawn_plan",
        "ion_swarm_status",
        "ion_agent_invoke",
        "ion_agent_cancel",
        "ion_swarm_step_once",
    ]
    agent_broker = build_agent_broker_status(root)
    return {
        "schema_id": "ion.chatgpt_browser_mcp_cockpit_summary.v1",
        "connector_contract_verdict": contract.get("verdict"),
        "http_preview_verdict": http_preview.get("verdict"),
        "transport_state": tunnel.get("transport_state") or tunnel.get("connector_state"),
        "active_connector_url": tunnel.get("active_connector_url"),
        "carrier_id": profile.get("carrier_id"),
        "project_facing_callsign": profile.get("project_facing_callsign"),
        "callsign_authority": profile.get("callsign_authority"),
        "callsign_decision_receipt": profile.get("callsign_decision_receipt"),
        "tool_count": len(tools),
        "first_parity_tools_present": sorted(set(first_parity) & set(tools)),
        "visibility_tools_present": sorted(set(next_visibility) & set(tools)),
        "agent_invocation_tools_present": sorted(set(agent_tools) & set(tools)),
        "carrier_message_count": len(listify(carrier_queue.get("messages"))),
        "codex_work_request_count": work_queue.get("request_count"),
        "latest_carrier_messages": _latest_files(root, "ION/05_context/current/chatgpt_connector/carrier_messages"),
        "latest_task_returns": _latest_files(root, "ION/05_context/current/chatgpt_connector/task_returns"),
        "latest_agent_invocations": _latest_files(root, "ION/05_context/current/chatgpt_connector/agent_invocations"),
        "latest_artifact_receipts": _latest_files(root, "ION/05_context/current/chatgpt_connector/artifact_receipts"),
        "latest_decisions": _latest_files(root, "ION/05_context/current/chatgpt_connector/decisions"),
        "codex_queue_runner": build_codex_queue_runner_status(root, reconcile=False),
        "agent_invocation_broker": agent_broker,
        "artifact_upload_status_counts": upload_status_counts,
        "adapter_gap_not_core_failure": True,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _chatgpt_sandbox_returns_summary(root: Path) -> dict[str, Any]:
    projection = build_sandbox_return_queue_projection(root)
    returns = [row for row in listify(projection.get("returns")) if isinstance(row, dict)]
    status_counts: dict[str, int] = {}
    for row in returns:
        status = compact(row.get("status"), "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1
    return {
        "schema_id": "ion.chatgpt_sandbox_returns_cockpit_summary.v1",
        "queue_path": projection.get("queue_path"),
        "inbox_root": projection.get("inbox_root"),
        "return_count": projection.get("return_count"),
        "status_counts": status_counts,
        "latest_returns": returns[:10],
        "direct_apply_authority": False,
        "git_push_authority": False,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _safe_record_list(value: Any, limit: int = 5) -> list[dict[str, Any]]:
    return [item for item in listify(value) if isinstance(item, dict)][:limit]


def _compact_file_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "name": record.get("name") or Path(str(record.get("path", ""))).name,
            "path": record.get("path"),
            "mtime": record.get("mtime") or record.get("updated_at") or record.get("created_at"),
            "status": record.get("status"),
        }
        for record in records
    ]


def _codex_capsule_chat_summary(root: Path) -> dict[str, Any]:
    model = read_json(root / CODEX_CAPSULE_CHAT_MODEL)
    ui = model.get("ui", {}) if isinstance(model.get("ui"), dict) else {}
    conversation = ui.get("conversation", {}) if isinstance(ui.get("conversation"), dict) else {}
    conversation_summary = conversation.get("summary", {}) if isinstance(conversation.get("summary"), dict) else {}
    codex_context = model.get("codex_solo_context", {}) if isinstance(model.get("codex_solo_context"), dict) else {}
    capsule = codex_context.get("capsule", {}) if isinstance(codex_context.get("capsule"), dict) else {}
    mini = codex_context.get("mini", {}) if isinstance(codex_context.get("mini"), dict) else {}
    hot_context = codex_context.get("hot_context", {}) if isinstance(codex_context.get("hot_context"), dict) else {}
    codex_queue = model.get("codex_queue", {}) if isinstance(model.get("codex_queue"), dict) else {}
    response_runs = model.get("response_runs", {}) if isinstance(model.get("response_runs"), dict) else {}
    turn_traces = model.get("turn_traces", {}) if isinstance(model.get("turn_traces"), dict) else {}
    memory = model.get("memory_visualization", {}) if isinstance(model.get("memory_visualization"), dict) else {}
    skills = model.get("skills", {}) if isinstance(model.get("skills"), dict) else {}
    current_activation = skills.get("current_activation", {}) if isinstance(skills.get("current_activation"), dict) else {}
    chat_engine = model.get("chat_engine", {}) if isinstance(model.get("chat_engine"), dict) else {}
    response_carrier = model.get("chat_response_carrier", {}) if isinstance(model.get("chat_response_carrier"), dict) else {}
    execution_bridge = model.get("execution_bridge", {}) if isinstance(model.get("execution_bridge"), dict) else {}
    mini_text = compact(mini.get("text"), "")
    return {
        "schema_id": "ion.codex_capsule_chat_cockpit_summary.v1",
        "model_path": str(CODEX_CAPSULE_CHAT_MODEL),
        "model_present": bool(model),
        "verdict": compact(model.get("verdict"), "missing"),
        "generated_at": model.get("generated_at"),
        "product": model.get("product", {}),
        "product_mode": model.get("product_mode", {}),
        "authority": model.get("authority", {}),
        "conversation_summary": conversation_summary,
        "turn_trace_count": turn_traces.get("trace_count", 0),
        "queued_request_count": turn_traces.get("queued_request_count", 0),
        "runner_active": bool(turn_traces.get("runner_active")),
        "response_run_count": response_runs.get("record_count", 0),
        "latest_response_status": response_runs.get("latest_status"),
        "latest_response_runs": [
            {
                "run_id": record.get("run_id"),
                "status": record.get("status"),
                "selected_model": record.get("selected_model"),
                "selected_reasoning_effort": record.get("selected_reasoning_effort"),
                "created_at": record.get("created_at"),
                "latest_return_path": record.get("latest_return_path"),
                "path": record.get("path"),
            }
            for record in _safe_record_list(response_runs.get("records"), limit=5)
        ],
        "latest_work_requests": _compact_file_records(_safe_record_list(codex_queue.get("latest_work_requests"), limit=5)),
        "latest_task_returns": _compact_file_records(_safe_record_list(codex_queue.get("latest_task_returns"), limit=5)),
        "codex_queue_path": codex_queue.get("work_queue_path"),
        "capsule": {
            "ok": capsule.get("ok"),
            "path": capsule.get("path"),
            "entry_count": capsule.get("entry_count"),
            "context_line_limit": capsule.get("context_line_limit"),
            "recent_rows": _safe_record_list(capsule.get("recent_rows"), limit=5),
        },
        "mini": {
            "ok": mini.get("ok"),
            "role": mini.get("role"),
            "line_count": mini.get("line_count"),
            "max_lines": mini.get("max_lines"),
            "text_excerpt": "\n".join(mini_text.splitlines()[:16]),
        },
        "hot_context": hot_context,
        "memory_visualization": {
            "selected_turn_id": memory.get("selected_turn_id"),
            "active_process_running": memory.get("active_process_running"),
            "memory_segment_count": len(listify(memory.get("memory_segments"))),
            "context_layer_count": len(listify(memory.get("context_matryoshka_layers"))),
            "visible_window_count": len(listify(memory.get("visible_windows"))),
            "raw_hidden_reasoning_exposed": bool(memory.get("raw_hidden_reasoning_exposed")),
        },
        "chat_engine": {
            "verdict": chat_engine.get("verdict"),
            "quality_target": chat_engine.get("quality_target"),
            "lens_count": chat_engine.get("lens_count"),
            "response_modes": listify(chat_engine.get("response_modes")),
        },
        "skills": {
            "verdict": skills.get("verdict"),
            "skill_count": skills.get("skill_count"),
            "current_activation_verdict": current_activation.get("verdict"),
            "selection_reason": current_activation.get("selection_reason"),
            "findings": listify(skills.get("findings")) + listify(current_activation.get("findings")),
        },
        "response_carrier": {
            "enabled": response_carrier.get("enabled"),
            "verdict": response_carrier.get("verdict"),
            "uses_codex_cli": response_carrier.get("uses_codex_cli"),
            "provider_api_dispatch_authorized": response_carrier.get("provider_api_dispatch_authorized"),
            "state_acceptance_granted": response_carrier.get("state_acceptance_granted"),
        },
        "execution_bridge": {
            "default_mode": execution_bridge.get("default_mode"),
            "allowed_modes": listify(execution_bridge.get("allowed_modes")),
            "runner_start_enabled": execution_bridge.get("runner_start_enabled"),
            "response_carrier_enabled": execution_bridge.get("response_carrier_enabled"),
        },
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }


def _markdown_headings(text: str, limit: int = 10) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(stripped.lstrip("#").strip())
        if len(headings) >= limit:
            break
    return headings


def _yaml_domain_rows(text: str) -> list[dict[str, str]]:
    domains: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- domain_id:"):
            if current:
                domains.append(current)
            current = {"domain_id": stripped.split(":", 1)[1].strip().strip("\"'")}
            continue
        if current is None:
            continue
        for key in ("purpose", "safety_boundary"):
            prefix = f"{key}:"
            if stripped.startswith(prefix):
                current[key] = stripped[len(prefix):].strip().strip("\"'")
    if current:
        domains.append(current)
    return domains


def _extension_micro_shell_summary(root: Path) -> dict[str, Any]:
    companion = read_json(root / PORTABLE_COMPANION_PRODUCT_CONTEXT)
    manifest = read_json(root / BROWSER_EXTENSION_MANIFEST)
    agent_contract = read_json(root / BROWSER_EXTENSION_AGENT_CONTRACT)
    dom_registry_text = _read_text(root / DOM_PERCEPTION_DOMAIN_REGISTRY)
    task_return_text = _read_text(root / DOM_PERCEPTION_TASK_RETURN)
    queue_pack_text = _read_text(root / BROWSER_EXTENSION_QUEUE_PACK_AUTHORING)
    content_scripts = [item for item in listify(manifest.get("content_scripts")) if isinstance(item, dict)]
    background_messages = agent_contract.get("background_messages") if isinstance(agent_contract.get("background_messages"), dict) else {}
    authority = companion.get("current_v1_authority") if isinstance(companion.get("current_v1_authority"), dict) else {}
    joc_inheritance = companion.get("joc_inheritance_decision") if isinstance(companion.get("joc_inheritance_decision"), dict) else {}
    inherited_protocols = companion.get("inherited_protocols") if isinstance(companion.get("inherited_protocols"), dict) else {}
    domains = _yaml_domain_rows(dom_registry_text)
    return {
        "schema_id": "ion.extension_micro_shell_cockpit_summary.v1",
        "status": "visibility_projection_ready" if companion or manifest else "missing_source",
        "extension_root": str(BROWSER_EXTENSION_ROOT),
        "manifest": {
            "path": str(BROWSER_EXTENSION_MANIFEST),
            "present": bool(manifest),
            "name": manifest.get("name"),
            "version": manifest.get("version"),
            "description": manifest.get("description"),
            "permissions": listify(manifest.get("permissions")),
            "host_permissions": listify(manifest.get("host_permissions")),
            "content_script_count": len(content_scripts),
            "content_script_matches": [match for script in content_scripts for match in listify(script.get("matches"))],
        },
        "agent_lane_contract": {
            "path": str(BROWSER_EXTENSION_AGENT_CONTRACT),
            "present": bool(agent_contract),
            "status": agent_contract.get("status"),
            "purpose": agent_contract.get("purpose"),
            "panel_surfaces": listify(agent_contract.get("panel_surfaces")),
            "background_message_count": len(background_messages),
            "background_messages": sorted(background_messages.keys()),
            "safety_law": listify(agent_contract.get("safety_law")),
            "gateway_base_storage_key": agent_contract.get("gateway_base_storage_key"),
            "gateway_token_storage_key": agent_contract.get("gateway_token_storage_key"),
        },
        "portable_companion": {
            "path": str(PORTABLE_COMPANION_PRODUCT_CONTEXT),
            "present": bool(companion),
            "status": companion.get("status"),
            "context_id": companion.get("context_id"),
            "product_thesis": companion.get("product_thesis"),
            "joc_decision": joc_inheritance.get("decision"),
            "layout_zones": listify(joc_inheritance.get("layout_zones")),
            "visual_language": joc_inheritance.get("visual_language"),
            "inherited_protocol_count": len(inherited_protocols),
            "inherited_protocols": sorted(inherited_protocols.keys()),
            "shared_graph_model": companion.get("shared_graph_model", {}),
            "page_context_package_shape": companion.get("page_context_package_shape", {}),
        },
        "page_perception": {
            "domain_registry_path": str(DOM_PERCEPTION_DOMAIN_REGISTRY),
            "task_return_path": str(DOM_PERCEPTION_TASK_RETURN),
            "domain_registry_present": bool(dom_registry_text),
            "task_return_present": bool(task_return_text),
            "domain_count": len(domains),
            "domains": domains[:10],
            "task_return_headings": _markdown_headings(task_return_text, limit=8),
        },
        "queue_pack_authoring": {
            "path": str(BROWSER_EXTENSION_QUEUE_PACK_AUTHORING),
            "present": bool(queue_pack_text),
            "headings": _markdown_headings(queue_pack_text, limit=8),
        },
        "current_v1_authority": authority,
        "safety_law": listify(companion.get("safety_law")),
        "required_boundaries": listify(companion.get("required_boundaries")),
        "implementation_gates": listify(companion.get("implementation_gates")),
        "non_claim_boundaries": listify(companion.get("non_claim_boundaries")),
        "production_authority": False,
        "live_execution_authority": False,
        "unrestricted_browser_control": False,
        "silent_browser_send_authority": False,
    }


def _docs_projects_packages_summary(root: Path) -> dict[str, Any]:
    context_packages = read_json(root / CODEX_CONTEXT_PACKAGES)
    package_rows = [row for row in listify(context_packages.get("packages")) if isinstance(row, dict)]
    safe_package_rel = latest_safe_package_result_rel(root)
    safe_package = read_json(root / safe_package_rel)
    preservation = safe_package.get("preservation_report") if isinstance(safe_package.get("preservation_report"), dict) else {}
    zip_audit = safe_package.get("zip_root_audit") if isinstance(safe_package.get("zip_root_audit"), dict) else {}
    artifact_packages = _latest_paths(root, ARTIFACT_PACKAGES_DIR.as_posix(), suffixes={".zip"}, recursive=True, limit=12)
    custom_gpt_builds = _latest_paths(root, (CUSTOM_GPT_CAPSULE_SYSTEM_DIR / "build_drafts").as_posix(), suffixes={".md", ".json"}, recursive=False, limit=8)
    custom_gpt_factory = _latest_paths(root, CUSTOM_GPT_FACTORY_DIR.as_posix(), suffixes={".md", ".json", ".yaml", ".yml"}, recursive=True, limit=8)
    workspace_root = root.parent
    daimon_root = workspace_root / "dAimon"
    project_favorites = [
        {
            "project_id": "ion_codex_full",
            "label": "ION_CODEX FULL",
            "path": root.as_posix(),
            "exists": root.exists(),
            "kind": "ion_root",
            "context_authority": "active_repo_authority",
        },
        {
            "project_id": "daimon",
            "label": "dAimon",
            "path": daimon_root.as_posix(),
            "exists": daimon_root.exists(),
            "kind": "companion_project",
            "context_authority": "receipt_backed_external_project",
        },
        {
            "project_id": "helixion_joc_rebuild",
            "label": "Helixion JOC Rebuild",
            "path": (root / (CURRENT / "helixion_joc_rebuild")).as_posix(),
            "exists": (root / (CURRENT / "helixion_joc_rebuild")).exists(),
            "kind": "current_context_package",
            "context_authority": "active_rebuild_package",
        },
        {
            "project_id": "browser_extension",
            "label": "ION ChatOps Bridge",
            "path": (root / BROWSER_EXTENSION_ROOT).as_posix(),
            "exists": (root / BROWSER_EXTENSION_ROOT).exists(),
            "kind": "browser_extension",
            "context_authority": "bounded_extension_surface",
        },
        {
            "project_id": "custom_gpt_packages",
            "label": "Custom GPT Packages",
            "path": (root / (ARTIFACT_PACKAGES_DIR / "custom_gpt")).as_posix(),
            "exists": (root / (ARTIFACT_PACKAGES_DIR / "custom_gpt")).exists(),
            "kind": "artifact_package_lane",
            "context_authority": "candidate_package_artifacts",
        },
    ]
    package_types: dict[str, int] = {}
    for row in package_rows:
        kind = compact(row.get("context_type"), "unknown")
        package_types[kind] = package_types.get(kind, 0) + 1
    return {
        "schema_id": "ion.docs_projects_packages_cockpit_summary.v1",
        "status": "visibility_projection_ready",
        "context_packages": {
            "path": CODEX_CONTEXT_PACKAGES.as_posix(),
            "generated_at": context_packages.get("generated_at"),
            "package_count": context_packages.get("package_count", len(package_rows)),
            "selected_by_default": listify(context_packages.get("selected_by_default")),
            "package_types": package_types,
            "packages": package_rows[:10],
            "production_authority": False,
            "live_execution_authority": False,
        },
        "project_favorites": project_favorites,
        "artifact_packages": {
            "root": ARTIFACT_PACKAGES_DIR.as_posix(),
            "zip_count_visible": len(artifact_packages),
            "latest_zips": artifact_packages,
            "auto_zip_drop_authority": False,
            "drop_zone_execution_authority": False,
        },
        "safe_full_project_package": {
            "path": safe_package_rel.as_posix(),
            "present": bool(safe_package),
            "accepted": safe_package.get("accepted"),
            "zip_path": safe_package.get("zip_path"),
            "zip_sha256": safe_package.get("zip_sha256"),
            "packaging_verdict": preservation.get("packaging_verdict"),
            "files_before": preservation.get("files_before"),
            "files_after": preservation.get("files_after"),
            "zip_root_verdict": zip_audit.get("verdict"),
            "archive_root_mode": zip_audit.get("archive_root_mode"),
        },
        "custom_gpt_context": {
            "capsule_system_dir": CUSTOM_GPT_CAPSULE_SYSTEM_DIR.as_posix(),
            "factory_dir": CUSTOM_GPT_FACTORY_DIR.as_posix(),
            "latest_build_drafts": custom_gpt_builds,
            "latest_factory_files": custom_gpt_factory,
        },
        "operator_model": {
            "double_click_zip_drop": "planned_extension_runtime_capability_not_granted_here",
            "one_click_thumbnail": "planned_extension_runtime_capability_not_granted_here",
            "favorites_are_context_targets": True,
            "receipts_required_for_package_state": True,
        },
        "production_authority": False,
        "live_execution_authority": False,
        "unrestricted_filesystem_mutation": False,
    }


def _helixion_joc_rebuild_summary(root: Path) -> dict[str, Any]:
    current_plan = read_json(root / HELIXION_REBUILD_CURRENT_PLAN)
    phase_0_gate = current_plan.get("phase_0_exit_gate") if isinstance(current_plan.get("phase_0_exit_gate"), dict) else {}
    phase_1_package = current_plan.get("phase_1_orchestration_context_package") if isinstance(current_plan.get("phase_1_orchestration_context_package"), dict) else {}
    phase_2_shell = current_plan.get("phase_2_local_shell_seed") if isinstance(current_plan.get("phase_2_local_shell_seed"), dict) else {}
    react_bundle = phase_2_shell.get("react_bundle") if isinstance(phase_2_shell.get("react_bundle"), dict) else {}
    return {
        "schema_id": "ion.helixion_joc_rebuild_projection.v1",
        "status": compact(current_plan.get("status"), "not_documented"),
        "decision": compact(current_plan.get("decision"), "no rebuild decision recorded"),
        "master_plan_path": str(HELIXION_REBUILD_PLAN),
        "registry_path": str(HELIXION_REBUILD_REGISTRY),
        "current_plan_path": str(HELIXION_REBUILD_CURRENT_PLAN),
        "master_plan_present": (root / HELIXION_REBUILD_PLAN).exists(),
        "registry_present": (root / HELIXION_REBUILD_REGISTRY).exists(),
        "current_plan_present": (root / HELIXION_REBUILD_CURRENT_PLAN).exists(),
        "ready_for_phase_1": bool(phase_0_gate.get("ready_for_phase_1")),
        "phase_0_gate": phase_0_gate,
        "product_roles": current_plan.get("primary_product_roles", {}),
        "required_surfaces": listify(current_plan.get("required_surfaces")),
        "canonical_zones": listify(current_plan.get("canonical_zones")),
        "canonical_object_types": listify(current_plan.get("canonical_object_types")),
        "allowed_v1_capabilities": listify(current_plan.get("allowed_v1_capabilities")),
        "forbidden_v1_capabilities": listify(current_plan.get("forbidden_v1_capabilities")),
        "next_build_sequence": listify(current_plan.get("next_build_sequence")),
        "source_authorities": listify(current_plan.get("source_authorities")),
        "orchestration_context_package": phase_1_package,
        "local_shell": phase_2_shell,
        "react_bundle": react_bundle,
        "development_urls": listify(phase_2_shell.get("development_urls")),
        "latest_capsule_entry_id": phase_2_shell.get("capsule_entry_id") or phase_1_package.get("capsule_entry_id"),
        "latest_history_receipt": phase_2_shell.get("history_receipt") or phase_1_package.get("history_receipt"),
        "latest_codex_solo_checkpoint_id": phase_2_shell.get("codex_solo_checkpoint_id") or phase_1_package.get("codex_solo_checkpoint_id"),
        "authority_posture": current_plan.get("authority_posture", {}),
        "production_authority": False,
        "live_execution_authority": False,
        "unrestricted_browser_control": False,
    }


def build_cockpit_view_model(ion_root: str | Path = ".") -> dict[str, Any]:
    root = Path(ion_root).resolve()
    active_files = dict(ACTIVE_FILES)
    active_files["safe_full_project_package"] = latest_safe_package_result_rel(root)
    data = {name: read_json(root / rel) for name, rel in active_files.items()}
    spawn_rows = _spawn_rows(data["spawn"], data["turn"])
    records = _ledger_records(data["ledger"])
    steward_items = _steward_items(data["steward"])
    operator_items = _operator_items(data["operator_queue"])
    gates = _gates(data["human_gates"])
    open_gates = [g for g in gates if str(g.get("status", "open")).lower() not in {"resolved", "closed"}]
    pending_operator = [i for i in operator_items if str(i.get("status", "pending")).lower() in {"pending", "queued"}]
    findings = listify(data["turn"].get("findings")) if isinstance(data["turn"].get("findings"), list) else []
    if isinstance(data["turn"].get("findings"), dict):
        for value in data["turn"].get("findings", {}).values():
            findings.extend(listify(value))
    blocked = bool(open_gates) or bool(data["turn"].get("blocked_by_findings"))
    return_counts = _return_counts(records)
    active_spawn_count = _active_spawn_queue_count(data["turn"], spawn_rows)
    plan_spawn_count = _spawn_count(spawn_rows)
    deferred_spawn_count = _deferred_spawn_count(spawn_rows)
    sandbox_returns = _chatgpt_sandbox_returns_summary(root)
    local_services = build_local_service_status(root)
    service_console = build_service_console_model(root)
    helixion_rebuild = _helixion_joc_rebuild_summary(root)
    chatgpt_browser_mcp = _chatgpt_browser_mcp_summary(root)
    codex_capsule_chat = _codex_capsule_chat_summary(root)
    extension_micro_shell = _extension_micro_shell_summary(root)
    docs_projects_packages = _docs_projects_packages_summary(root)
    counts = {
        "spawn_rows": len(spawn_rows),
        "spawn_true": active_spawn_count,
        "plan_spawn_true": plan_spawn_count,
        "deferred_spawn": deferred_spawn_count,
        "returns": return_counts,
        "steward_queue": len(steward_items),
        "operator_queue_pending": len(pending_operator),
        "open_gates": len(open_gates),
    }
    runtime_status = status_from_findings(findings, blocked=blocked)

    view_model = {
        "schema_id": "ion.cockpit_view_model.v1",
        "generated_at": utc_now(),
        "runtime": {
            "status": runtime_status,
            "shell_root": str(root),
            "mode": compact(data["turn"].get("carrier") or data["work"].get("carrier"), "cursor"),
            "version": "V90_CURSOR_COCKPIT_LIVE_WEBVIEW_BINDING",
            "blocked": blocked,
            "audit_findings": findings,
        },
        "top_bar": {
            "objective": compact(data["turn"].get("objective") or data["work"].get("objective"), "no active objective"),
            "carrier_status": "blocked" if blocked else "ready",
            "hook_status": compact(data["hook"].get("status"), "unknown"),
            "gate_count": len(open_gates),
            "spawn_count": active_spawn_count,
            "plan_spawn_count": plan_spawn_count,
            "deferred_spawn_count": deferred_spawn_count,
            "spawn_rows_total": len(spawn_rows),
            "execution_bundle_materialized": data["spawn"].get("execution_bundle_materialized"),
            "return_counts": return_counts,
            "steward_queue_count": len(steward_items),
            "operator_queue_pending": len(pending_operator),
            "sandbox_return_count": sandbox_returns.get("return_count", 0),
            "local_service_status": local_services.get("status"),
            "local_service_count": local_services.get("service_count", 0),
            "local_service_missing_template_count": local_services.get("missing_template_count", 0),
            "helixion_rebuild_status": helixion_rebuild.get("status"),
            "helixion_rebuild_ready_for_phase_1": helixion_rebuild.get("ready_for_phase_1"),
            "browser_carrier_message_count": chatgpt_browser_mcp.get("carrier_message_count", 0),
            "codex_work_request_count": chatgpt_browser_mcp.get("codex_work_request_count", 0),
            "action_gateway_tool_count": chatgpt_browser_mcp.get("tool_count", 0),
            "action_gateway_transport_state": chatgpt_browser_mcp.get("transport_state"),
            "codex_capsule_chat_verdict": codex_capsule_chat.get("verdict"),
            "codex_capsule_chat_turn_count": codex_capsule_chat.get("conversation_summary", {}).get("turn_count", 0),
            "codex_capsule_chat_response_run_count": codex_capsule_chat.get("response_run_count", 0),
            "extension_version": extension_micro_shell.get("manifest", {}).get("version"),
            "extension_panel_count": len(extension_micro_shell.get("agent_lane_contract", {}).get("panel_surfaces", [])),
            "page_perception_domain_count": extension_micro_shell.get("page_perception", {}).get("domain_count", 0),
            "context_package_count": docs_projects_packages.get("context_packages", {}).get("package_count", 0),
            "artifact_package_count": docs_projects_packages.get("artifact_packages", {}).get("zip_count_visible", 0),
        },
        "queues": {
            "operator_messages": operator_items,
            "human_gates": gates,
            "steward_integration": steward_items,
        },
        "agents": summarize_agents(spawn_rows, records),
        "timeline": synthesize_timeline(data, counts, active_files),
        "front_door_proof_trace": data["front_door_proof_trace"],
        "lane_timeline": data["lane_timeline"],
        "receipt_hydration": data["receipt_hydration"],
        "runtime_debug_overlay": data["runtime_debug_overlay"],
        "safe_full_project_package": data["safe_full_project_package"],
        "v72_mcp_donor_reconciliation": data["v72_mcp_donor_reconciliation"],
        "chatgpt_browser_mcp": chatgpt_browser_mcp,
        "codex_capsule_chat": codex_capsule_chat,
        "extension_micro_shell": extension_micro_shell,
        "docs_projects_packages": docs_projects_packages,
        "chatgpt_sandbox_returns": sandbox_returns,
        "local_services": local_services,
        "service_console": service_console,
        "helixion_joc_rebuild": helixion_rebuild,
        "receipts": recent_receipts(root),
        "authority_classes": [
            "ACTIVE_RUNTIME_AUTHORITY",
            "ACCEPTED_TASK_RETURN",
            "PENDING_TASK_RETURN",
            "REJECTED_TASK_RETURN",
            "HUMAN_GATE_REQUIRED",
            "LEGACY_CONTEXT_WITNESS",
            "DONOR_REFERENCE",
            "FORBIDDEN_CAPABILITY",
            "JOC_REBUILD_PLAN",
            "PAGE_BRANCH_PROVISIONAL",
            "WISDOMNET_CANDIDATE",
        ],
        "source_paths": {name: str(rel) for name, rel in active_files.items()},
    }
    return view_model


def write_cockpit_view_model(ion_root: str | Path = ".", output: str | Path | None = None) -> dict[str, Any]:
    root = Path(ion_root).resolve()
    model = build_cockpit_view_model(root)
    out = root / (Path(output) if output else OUTPUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return model


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the ION/JOC cockpit runtime view model.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true", help="Write ACTIVE_COCKPIT_VIEW_MODEL.json")
    parser.add_argument("--output", default=None, help="Optional output path relative to ion-root")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    model = write_cockpit_view_model(args.ion_root, args.output) if args.write else build_cockpit_view_model(args.ion_root)
    result = {"status": "ION_COCKPIT_VIEW_MODEL_READY", "view_model": model}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
