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
        "chatgpt_browser_mcp": _chatgpt_browser_mcp_summary(root),
        "chatgpt_sandbox_returns": sandbox_returns,
        "local_services": local_services,
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
