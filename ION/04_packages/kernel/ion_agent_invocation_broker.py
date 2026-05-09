"""ION agent invocation broker over the existing Codex queue runner.

The broker is not a separate agent system. It compiles role/context evidence
into bounded Codex work requests and leaves execution, proof gates, task
returns, and receipts with the existing ION connector owners.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_codex_queue_runner import build_codex_queue_runner_status, process_codex_queue_once

SCHEMA_ID = "ion.agent_invocation_broker.v1"
READY_VERDICT = "ION_AGENT_INVOCATION_BROKER_READY"
BLOCKED_VERDICT = "ION_AGENT_INVOCATION_BROKER_BLOCKED"

CONNECTOR_STATE_DIR = Path("ION/05_context/current/chatgpt_connector")
AGENT_INVOCATIONS_DIR = CONNECTOR_STATE_DIR / "agent_invocations"
RUNTIME_DIR = CONNECTOR_STATE_DIR / "runtime"
BROKER_STATE_PATH = RUNTIME_DIR / "agent_invocation_broker_state.json"
CODEX_WORK_REQUESTS_DIR = CONNECTOR_STATE_DIR / "codex_work_requests"
CODEX_WORK_QUEUE_INDEX = Path("ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json")
TASK_RETURNS_DIR = CONNECTOR_STATE_DIR / "task_returns"

AGENT_ROSTER_REGISTRY = Path("ION/03_registry/agent_roster_registry.yaml")
AGENT_CONTEXT_SYSTEM_REGISTRY = Path("ION/03_registry/agent_context_system_registry.yaml")
CODEX_CLI_CARRIER_PROFILE = Path("ION/03_registry/codex_cli_carrier_profile.yaml")
CODEX_CLI_EXECUTION_PACKET = Path("ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md")
FULL_CARRIER_PROTOCOL = Path("ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md")
CONNECTOR_CONTRACT = Path("ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py")
QUEUE_RUNNER_OWNER = Path("ION/04_packages/kernel/ion_codex_queue_runner.py")

BACKEND_CARRIER_ID = "CODEX_CLI_CARRIER"
REQUESTED_BY_CARRIER_ID = "CHATGPT_BROWSER_CARRIER"
REQUESTED_BY_CALLSIGN = "Sev"
HUMAN_SOVEREIGN_LABEL = "Braden"

FAILURE_CLASSES = (
    "AGENT_INVOCATION_FAILURE",
    "BACKEND_CODEX_FAILURE",
    "CARRIER_ADAPTER_FAILURE",
    "DAEMON_FAILURE",
    "ION_CORE_FAILURE",
)

CANCELLABLE_INVOCATION_STATUSES = {
    "PREPARED_NOT_QUEUED",
    "QUEUED_FOR_CODEX_CARRIER",
}

CANCELLABLE_WORK_REQUEST_STATUSES = {
    "PREPARED_FOR_CODEX_CARRIER_NOT_QUEUED",
    "QUEUED_FOR_CODEX_CARRIER",
}

ACTIVE_BACKEND_WORK_REQUEST_STATUSES = {
    "CLAIMED_BY_CODEX_QUEUE_RUNNER",
    "CODEX_QUEUE_RUNNER_WORKER_STARTED",
    "CODEX_CLI_RUNNING",
}

READ_TOOL_NAMES = (
    "ion_agent_list",
    "ion_agent_status",
    "ion_agent_result",
    "ion_agent_queue",
    "ion_agent_spawn_plan",
    "ion_swarm_status",
)

WRITE_TOOL_NAMES = (
    "ion_agent_invoke",
    "ion_agent_cancel",
    "ion_swarm_step_once",
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:80] or "agent_invocation"


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _resolve_root(root: str | Path | None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    if candidate.is_dir() and (candidate / "ION").exists():
        return candidate
    return resolve_shell_root_from_ion_root(root)


def _connector_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _safe_rel_path(root: Path, value: str) -> Path:
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("path must be repo-relative and may not escape the repo root")
    target = (root / rel).resolve()
    target.relative_to(root)
    return target


def _clean_yaml_scalar(value: str) -> str:
    value = value.strip()
    if value in {"[]", "{}", "null", "NULL", "~"}:
        return ""
    return value.strip("\"'")


def _parse_indented_role_blocks(path: Path, *, id_key: str) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    list_key: str | None = None
    section = ""
    for raw in _read_text(path).splitlines():
        stripped = raw.strip()
        indent = len(raw) - len(raw.lstrip(" "))
        if indent == 0 and stripped.endswith(":"):
            section = stripped[:-1]
        marker = f"- {id_key}:"
        if indent == 2 and stripped.startswith(marker):
            if current:
                records.append(current)
            current = {
                id_key: _clean_yaml_scalar(stripped[len(marker):]),
                "registry_section": section,
                "source_registry": path.as_posix(),
            }
            list_key = None
            continue
        if current is None:
            continue
        if indent == 4 and stripped.endswith(":"):
            list_key = stripped[:-1]
            current[list_key] = []
            continue
        if indent == 4 and ": " in stripped:
            key, value = stripped.split(": ", 1)
            if value.startswith(">-") or value.startswith("|"):
                list_key = None
                current[key] = ""
            else:
                current[key] = _clean_yaml_scalar(value)
                list_key = None
            continue
        if indent == 6 and stripped.startswith("- ") and list_key:
            current.setdefault(list_key, []).append(_clean_yaml_scalar(stripped[2:]))
    if current:
        records.append(current)
    return records


def _display_from_role_id(role_id: str) -> str:
    label = role_id.split(".", 1)[1] if role_id.startswith("role.") else role_id
    return label.upper()


def _normalized_alias(value: str) -> str:
    value = value.lower()
    if value.startswith("role."):
        value = value.split(".", 1)[1]
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


def _agent_aliases(record: Mapping[str, Any]) -> list[str]:
    role_id = str(record.get("role_id") or "")
    display = str(record.get("display_name") or _display_from_role_id(role_id))
    base = role_id.split(".", 1)[1] if role_id.startswith("role.") else role_id
    aliases = {
        role_id,
        base,
        display,
        display.lower(),
        _normalized_alias(role_id),
        _normalized_alias(display),
    }
    if base == "steward":
        aliases.update({"steward_review", "steward_proposal", "steward_review_proposal"})
    return sorted(alias for alias in aliases if alias)


def _merge_agent_records(root: Path) -> list[dict[str, Any]]:
    context_records = _parse_indented_role_blocks(root / AGENT_CONTEXT_SYSTEM_REGISTRY, id_key="role_id")
    roster_records = _parse_indented_role_blocks(root / AGENT_ROSTER_REGISTRY, id_key="entity_id")
    by_role: dict[str, dict[str, Any]] = {}

    for record in context_records:
        role_id = str(record.get("role_id") or "")
        if not role_id:
            continue
        by_role[role_id] = {
            "agent_id": role_id,
            "role_id": role_id,
            "display_name": str(record.get("display_name") or _display_from_role_id(role_id)),
            "context_system_card": record.get("context_system_card"),
            "base_sources": list(record.get("base_sources") or []),
            "primary_templates": list(record.get("primary_templates") or []),
            "package_strategy": record.get("package_strategy"),
            "default_active_package_class": record.get("default_active_package_class"),
            "context_registry_section": record.get("registry_section"),
            "context_registry_path": AGENT_CONTEXT_SYSTEM_REGISTRY.as_posix(),
        }

    for record in roster_records:
        role_id = str(record.get("entity_id") or "")
        if not role_id:
            continue
        merged = by_role.setdefault(role_id, {
            "agent_id": role_id,
            "role_id": role_id,
            "display_name": str(record.get("display_name") or _display_from_role_id(role_id)),
        })
        merged.setdefault("display_name", str(record.get("display_name") or _display_from_role_id(role_id)))
        merged["roster_registry_path"] = AGENT_ROSTER_REGISTRY.as_posix()
        for key in (
            "band",
            "standing_class",
            "live_status",
            "rank_class",
            "structural_identity",
            "activation_owner",
            "audit_relation",
            "write_scope_summary",
        ):
            if record.get(key):
                merged[key] = record[key]
        if record.get("template_bindings"):
            merged["template_bindings"] = list(record.get("template_bindings") or [])
        if record.get("source_refs"):
            merged["source_refs"] = list(record.get("source_refs") or [])

    agents: list[dict[str, Any]] = []
    for role_id, record in by_role.items():
        aliases = _agent_aliases(record)
        context_paths = _existing_agent_context_paths(root, record)
        missing_paths = _missing_declared_context_paths(root, record)
        agent = {
            **record,
            "aliases": aliases,
            "invocable": bool(context_paths),
            "backend_carrier_id": BACKEND_CARRIER_ID,
            "adapter_surface": "ChatGPT Browser MCP -> ION agent invocation broker -> Codex queue runner",
            "context_paths": context_paths,
            "missing_declared_context_paths": missing_paths,
            "production_authority": False,
            "live_execution_authority": False,
        }
        agents.append(agent)
    return sorted(agents, key=lambda item: str(item.get("role_id") or ""))


def _existing_agent_context_paths(root: Path, record: Mapping[str, Any]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    candidates: list[str] = []
    for key in ("context_system_card",):
        value = record.get(key)
        if value:
            candidates.append(str(value))
    for key in ("base_sources", "primary_templates", "template_bindings", "source_refs"):
        candidates.extend(str(value) for value in record.get(key) or [])
    for value in candidates:
        if not value or value in seen:
            continue
        path = root / value
        if path.exists() and path.is_file():
            ordered.append(value)
            seen.add(value)
    return ordered


def _missing_declared_context_paths(root: Path, record: Mapping[str, Any]) -> list[str]:
    missing: list[str] = []
    seen: set[str] = set()
    candidates: list[str] = []
    for key in ("context_system_card",):
        value = record.get(key)
        if value:
            candidates.append(str(value))
    for key in ("base_sources", "primary_templates", "template_bindings", "source_refs"):
        candidates.extend(str(value) for value in record.get(key) or [])
    for value in candidates:
        if not value or value in seen:
            continue
        path = root / value
        if not path.exists():
            missing.append(value)
            seen.add(value)
    return missing


def list_agents(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    agents = _merge_agent_records(shell_root)
    return {
        "schema_id": "ion.agent_invocation_broker_agent_list.v1",
        "verdict": READY_VERDICT,
        "agent_count": len(agents),
        "agents": agents,
        "source_paths": {
            "agent_roster_registry": AGENT_ROSTER_REGISTRY.as_posix(),
            "agent_context_system_registry": AGENT_CONTEXT_SYSTEM_REGISTRY.as_posix(),
            "codex_cli_carrier_profile": CODEX_CLI_CARRIER_PROFILE.as_posix(),
            "codex_cli_execution_packet": CODEX_CLI_EXECUTION_PACKET.as_posix(),
        },
        "failure_classes": list(FAILURE_CLASSES),
        "production_authority": False,
        "live_execution_authority": False,
    }


def _resolve_agent(root: Path, agent: str) -> tuple[dict[str, Any] | None, str | None]:
    requested = _normalized_alias(agent)
    if not requested:
        return None, "agent_required"
    agents = list_agents(root)["agents"]
    for record in agents:
        aliases = {_normalized_alias(alias) for alias in record.get("aliases") or []}
        if requested in aliases:
            return dict(record), None
    if requested.startswith("steward"):
        for record in agents:
            if record.get("role_id") == "role.steward":
                return dict(record), None
    return None, "agent_not_found_in_roster_or_context_system_registry"


def _required_context_reads(root: Path, agent: Mapping[str, Any], invocation_rel: str) -> tuple[list[str], list[str]]:
    candidates = [
        invocation_rel,
        AGENT_ROSTER_REGISTRY.as_posix(),
        AGENT_CONTEXT_SYSTEM_REGISTRY.as_posix(),
        CODEX_CLI_CARRIER_PROFILE.as_posix(),
        CODEX_CLI_EXECUTION_PACKET.as_posix(),
        FULL_CARRIER_PROTOCOL.as_posix(),
        QUEUE_RUNNER_OWNER.as_posix(),
        CONNECTOR_CONTRACT.as_posix(),
        *list(agent.get("context_paths") or []),
    ]
    ordered: list[str] = []
    missing: list[str] = []
    seen: set[str] = set()
    for rel in candidates:
        if not rel or rel in seen:
            continue
        seen.add(rel)
        path = root / rel
        if rel == invocation_rel or (path.exists() and path.is_file()):
            ordered.append(rel)
        else:
            missing.append(rel)
    return ordered, missing


def _task_returns_for_request(root: Path, request_path: str | None, request_id: str | None) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    returns_root = root / TASK_RETURNS_DIR
    if not returns_root.exists():
        return results
    for path in sorted(returns_root.glob("*.json")):
        payload = _read_json(path) or {}
        if request_path and payload.get("work_request_path") == request_path:
            results.append({"path": _connector_rel(path, root), "packet": payload})
        elif request_id and payload.get("work_request_id") == request_id:
            results.append({"path": _connector_rel(path, root), "packet": payload})
    return results


def _codex_work_queue(root: Path, *, limit: int = 100) -> dict[str, Any]:
    requests: list[dict[str, Any]] = []
    requests_root = root / CODEX_WORK_REQUESTS_DIR
    if requests_root.exists():
        for path in sorted(requests_root.glob("*.json"), reverse=True):
            if len(requests) >= limit:
                break
            payload = _read_json(path) or {}
            rel_path = _connector_rel(path, root)
            returns = _task_returns_for_request(root, rel_path, str(payload.get("request_id") or ""))
            requests.append({
                "request_id": payload.get("request_id"),
                "path": rel_path,
                "objective": payload.get("objective"),
                "status": payload.get("status"),
                "created_at": payload.get("created_at"),
                "updated_at": payload.get("updated_at"),
                "latest_return_packet_path": payload.get("latest_return_packet_path"),
                "return_packet_paths": payload.get("return_packet_paths", []),
                "linked_return_count": len(returns),
                "accepted_return_count": sum(1 for item in returns if item["packet"].get("accepted_for_carrier_intake") is True),
                "agent_invocation_id": payload.get("agent_invocation_id"),
            })
    return {
        "schema_id": "ion.chatgpt_browser_connector_codex_work_queue.v1",
        "queue_path": CODEX_WORK_QUEUE_INDEX.as_posix(),
        "state_dir": CODEX_WORK_REQUESTS_DIR.as_posix(),
        "request_count": len(requests),
        "requests": requests,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _write_codex_work_queue_index(root: Path) -> dict[str, Any]:
    queue = _codex_work_queue(root)
    _write_json(root / CODEX_WORK_QUEUE_INDEX, queue)
    return queue


def _unique_packet_path(root: Path, rel_dir: Path, timestamp: str, slug: str) -> Path:
    stem = f"{timestamp.replace(':', '').replace('+', 'Z')}_{slug}"
    path = root / rel_dir / f"{stem}.json"
    counter = 1
    while path.exists():
        path = root / rel_dir / f"{stem}_{counter}.json"
        counter += 1
    return path


def _build_agent_work_objective(agent: Mapping[str, Any], objective: str, invocation_rel: str, mode: str) -> str:
    return "\n".join([
        f"ION agent invocation for {agent.get('display_name')} ({agent.get('role_id')}) via Codex CLI backend.",
        "",
        "Invariant: ION has one core engine mounted by all carriers. ChatGPT Browser/Sev is a full ION carrier target, not an observer-only lane.",
        "Distinguish human sovereign Braden, Sev as delegated operator carrier/callsign, ION core engine, Steward integration membrane, and Codex-backed worker.",
        "This is a role/context packet compiled by the ION agent invocation broker; it is not a separate agent system.",
        "",
        f"Invocation packet: {invocation_rel}",
        f"Requested mode: {mode}",
        f"Original objective: {objective}",
        "",
        "Backend and proof rules:",
        "- Mount the requested role only through the supplied boot/context/template evidence.",
        "- Do not claim to be ION, sovereign authority, or production authority.",
        "- Do not let raw Codex output become ION state except through the existing task-return proof gates.",
        "- Return must include CONTEXT PROOF, TEMPLATE ACTION PROOF, VALIDATION, and RESULT sections.",
        "- Classify failures as AGENT_INVOCATION_FAILURE, BACKEND_CODEX_FAILURE, CARRIER_ADAPTER_FAILURE, DAEMON_FAILURE, or ION_CORE_FAILURE.",
    ])


def _write_broker_state(root: Path, payload: Mapping[str, Any]) -> None:
    value = dict(payload)
    value.setdefault("schema_id", "ion.agent_invocation_broker_state.v1")
    value["updated_at"] = _now()
    value.setdefault("production_authority", False)
    value.setdefault("live_execution_authority", False)
    _write_json(root / BROKER_STATE_PATH, value)


def invoke_agent(
    root: str | Path | None = None,
    *,
    agent: str,
    objective: str,
    mode: str = "prepare_only",
    queue: bool = False,
    start: bool = False,
    context_refs: list[str] | None = None,
    requested_by_carrier_id: str = REQUESTED_BY_CARRIER_ID,
    requested_by_callsign: str = REQUESTED_BY_CALLSIGN,
    timeout_seconds: int = 1800,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    objective = objective.strip()
    if not objective:
        return _blocked("ion_agent_invoke", "objective_required")
    agent_record, finding = _resolve_agent(shell_root, agent)
    if finding or agent_record is None:
        return _blocked("ion_agent_invoke", finding or "agent_resolution_failed", {"available_agents": list_agents(shell_root)["agents"]})

    now = _now()
    requested_slug = _safe_slug(f"{agent_record.get('display_name')}_{objective}")
    invocation_id = f"agent_inv_{now.replace(':', '').replace('+', 'Z')}_{requested_slug}"
    invocation_path = _unique_packet_path(shell_root, AGENT_INVOCATIONS_DIR, now, requested_slug)
    invocation_rel = _connector_rel(invocation_path, shell_root)
    required_paths, missing_core_paths = _required_context_reads(shell_root, agent_record, invocation_rel)
    queued = bool(queue or start)
    request_status = "QUEUED_FOR_CODEX_CARRIER" if queued else "PREPARED_FOR_CODEX_CARRIER_NOT_QUEUED"
    request_id = f"codex_req_agent_{now.replace(':', '').replace('+', 'Z')}_{requested_slug}"
    objective_text = _build_agent_work_objective(agent_record, objective, invocation_rel, mode)
    work_path = _unique_packet_path(shell_root, CODEX_WORK_REQUESTS_DIR, now, _safe_slug(f"agent_{agent_record.get('display_name')}_{objective}"))
    work_rel = _connector_rel(work_path, shell_root)
    work_packet = {
        "schema_id": "ion.chatgpt_browser_connector_codex_work_request.v1",
        "request_id": request_id,
        "objective": objective_text,
        "requested_by": "ion_agent_invocation_broker",
        "requested_by_carrier_id": requested_by_carrier_id,
        "requested_by_callsign": requested_by_callsign,
        "agent_invocation_id": invocation_id,
        "agent_invocation_path": invocation_rel,
        "agent_role_id": agent_record.get("role_id"),
        "agent_display_name": agent_record.get("display_name"),
        "backend_carrier_id": BACKEND_CARRIER_ID,
        "backend_runner_owner": QUEUE_RUNNER_OWNER.as_posix(),
        "required_context_reads": [{"kind": "file", "path": path, "required": True} for path in required_paths],
        "declared_but_missing_context_paths": sorted(set(agent_record.get("missing_declared_context_paths") or []) | set(missing_core_paths)),
        "return_contract_sections": ["### CONTEXT PROOF", "### TEMPLATE ACTION PROOF", "### VALIDATION", "### RESULT"],
        "failure_classes": list(FAILURE_CLASSES),
        "status": request_status,
        "created_at": now,
        "updated_at": now,
        "return_packet_paths": [],
        "latest_return_packet_path": None,
        "production_authority": False,
        "live_execution_authority": False,
    }
    invocation_packet: dict[str, Any] = {
        "schema_id": "ion.agent_invocation.v1",
        "invocation_id": invocation_id,
        "created_at": now,
        "updated_at": now,
        "status": "QUEUED_FOR_CODEX_CARRIER" if queued else "PREPARED_NOT_QUEUED",
        "requested_agent": agent,
        "mode": mode,
        "objective": objective,
        "context_refs": list(context_refs or []),
        "agent": agent_record,
        "human_sovereign": HUMAN_SOVEREIGN_LABEL,
        "delegated_operator_carrier": {
            "carrier_id": requested_by_carrier_id,
            "project_facing_callsign": requested_by_callsign,
        },
        "ion_core_engine": "ONE_CORE_ENGINE_MOUNTED_BY_ALL_CARRIERS",
        "steward_integration_membrane": "proof_gated_task_return_and_steward_review_surfaces",
        "backend_carrier_id": BACKEND_CARRIER_ID,
        "backend_runner_owner": QUEUE_RUNNER_OWNER.as_posix(),
        "codex_work_request_id": request_id,
        "codex_work_request_path": work_rel,
        "required_context_reads": work_packet["required_context_reads"],
        "declared_but_missing_context_paths": work_packet["declared_but_missing_context_paths"],
        "raw_backend_output_state_policy": "RAW_CODEX_OUTPUT_NOT_ACCEPTED_WITHOUT_TASK_RETURN_PROOF_GATES",
        "failure_classes": list(FAILURE_CLASSES),
        "production_authority": False,
        "live_execution_authority": False,
    }
    _write_json(invocation_path, invocation_packet)
    work_packet["packet_path"] = work_rel
    _write_json(work_path, work_packet)
    queue_index = _write_codex_work_queue_index(shell_root)

    start_result = None
    if start:
        start_result = process_codex_queue_once(
            shell_root,
            request_path=work_rel,
            start=True,
            background=True,
            timeout_seconds=timeout_seconds,
        )
        invocation_packet["backend_start_result"] = start_result
        invocation_packet["status"] = "BACKEND_CODEX_STARTED" if start_result.get("ok") else "BACKEND_CODEX_START_BLOCKED"
        invocation_packet["updated_at"] = _now()
        _write_json(invocation_path, invocation_packet)
        _write_codex_work_queue_index(shell_root)

    _write_broker_state(shell_root, {
        "latest_invocation_id": invocation_id,
        "latest_invocation_path": invocation_rel,
        "latest_codex_work_request_path": work_rel,
        "latest_requested_agent": agent_record.get("role_id"),
    })
    return {
        "schema_id": SCHEMA_ID,
        "ok": True,
        "result": invocation_packet["status"],
        "invocation": invocation_packet,
        "invocation_path": invocation_rel,
        "codex_work_request_path": work_rel,
        "codex_work_request_id": request_id,
        "codex_work_request_status": request_status,
        "queued_for_codex_carrier": queued,
        "start_result": start_result,
        "codex_work_queue_path": CODEX_WORK_QUEUE_INDEX.as_posix(),
        "codex_work_queue_request_count": queue_index["request_count"],
        "production_authority": False,
        "live_execution_authority": False,
    }


def _blocked(tool: str, finding: str, data: Any | None = None) -> dict[str, Any]:
    return {
        "schema_id": SCHEMA_ID,
        "ok": False,
        "tool": tool,
        "finding": finding,
        "failure_classification": "AGENT_INVOCATION_FAILURE",
        "data": data,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _invocation_paths(root: Path) -> list[Path]:
    base = root / AGENT_INVOCATIONS_DIR
    if not base.exists():
        return []
    return sorted((path for path in base.glob("*.json") if path.is_file()), key=lambda path: path.name, reverse=True)


def _load_invocation(root: Path, identifier: str | None = None) -> tuple[Path | None, dict[str, Any] | None]:
    paths = _invocation_paths(root)
    if not identifier:
        if not paths:
            return None, None
        path = paths[0]
        return path, _read_json(path) or {}
    for path in paths:
        payload = _read_json(path) or {}
        if identifier in {path.relative_to(root).as_posix(), path.name, str(payload.get("invocation_id") or "")}:
            return path, payload
    return None, None


def _work_request_for_invocation(root: Path, invocation: Mapping[str, Any]) -> dict[str, Any] | None:
    rel = str(invocation.get("codex_work_request_path") or "")
    if not rel:
        return None
    try:
        path = _safe_rel_path(root, rel)
    except (ValueError, RuntimeError):
        return None
    return _read_json(path)


def agent_queue(root: str | Path | None = None, *, limit: int = 25) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    invocations: list[dict[str, Any]] = []
    for path in _invocation_paths(shell_root)[: max(1, min(limit, 100))]:
        payload = _read_json(path) or {}
        work_request = _work_request_for_invocation(shell_root, payload) or {}
        invocations.append({
            "invocation_id": payload.get("invocation_id"),
            "path": _connector_rel(path, shell_root),
            "status": payload.get("status"),
            "agent_role_id": (payload.get("agent") or {}).get("role_id") if isinstance(payload.get("agent"), dict) else None,
            "agent_display_name": (payload.get("agent") or {}).get("display_name") if isinstance(payload.get("agent"), dict) else None,
            "codex_work_request_id": payload.get("codex_work_request_id"),
            "codex_work_request_path": payload.get("codex_work_request_path"),
            "codex_work_request_status": work_request.get("status"),
            "latest_return_packet_path": work_request.get("latest_return_packet_path"),
            "created_at": payload.get("created_at"),
            "updated_at": payload.get("updated_at"),
        })
    return {
        "schema_id": "ion.agent_invocation_queue.v1",
        "queue_root": AGENT_INVOCATIONS_DIR.as_posix(),
        "invocation_count": len(_invocation_paths(shell_root)),
        "invocations": invocations,
        "failure_classes": list(FAILURE_CLASSES),
        "production_authority": False,
        "live_execution_authority": False,
    }


def agent_result(root: str | Path | None = None, *, invocation_id: str | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    path, invocation = _load_invocation(shell_root, invocation_id)
    if path is None or invocation is None:
        return _blocked("ion_agent_result", "agent_invocation_not_found")
    work_request = _work_request_for_invocation(shell_root, invocation) or {}
    returns = _task_returns_for_request(
        shell_root,
        str(invocation.get("codex_work_request_path") or ""),
        str(invocation.get("codex_work_request_id") or ""),
    )
    latest_return = returns[-1] if returns else None
    return {
        "schema_id": "ion.agent_invocation_result.v1",
        "ok": True,
        "invocation_path": _connector_rel(path, shell_root),
        "invocation": invocation,
        "codex_work_request": work_request,
        "task_return_count": len(returns),
        "latest_task_return_path": latest_return["path"] if latest_return else None,
        "latest_task_return": latest_return["packet"] if latest_return else None,
        "accepted_return_count": sum(1 for item in returns if item["packet"].get("accepted_for_carrier_intake") is True),
        "raw_backend_output_state_policy": "RAW_CODEX_OUTPUT_NOT_ACCEPTED_WITHOUT_TASK_RETURN_PROOF_GATES",
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_agent_spawn_plan(root: str | Path | None = None, *, objective: str | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    agents = list_agents(shell_root)["agents"]
    preferred = [
        role for role in ("role.mason", "role.vizier", "role.nemesis", "role.steward", "role.template_curator", "role.context_cartographer")
        if any(agent.get("role_id") == role for agent in agents)
    ]
    return {
        "schema_id": "ion.agent_spawn_plan.v1",
        "objective": objective,
        "spawn_policy": "BROKER_PREPARES_OR_QUEUES_CODEX_WORK_REQUESTS_ONLY",
        "backend_carrier_id": BACKEND_CARRIER_ID,
        "preferred_roles": preferred,
        "available_agent_count": len(agents),
        "available_agents": agents,
        "proof_gate": "existing ion_submit_task_return context/template proof gates",
        "no_parallel_agent_system_created": True,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _agent_work_requests(root: Path, *, queued_only: bool = False) -> list[tuple[Path, dict[str, Any]]]:
    requests_root = root / CODEX_WORK_REQUESTS_DIR
    if not requests_root.exists():
        return []
    pairs: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(requests_root.glob("*.json")):
        payload = _read_json(path) or {}
        if not payload.get("agent_invocation_id"):
            continue
        if queued_only and payload.get("status") != "QUEUED_FOR_CODEX_CARRIER":
            continue
        pairs.append((path, payload))
    return pairs


def _load_agent_work_request_for_step(root: Path, request_path: str) -> tuple[Path | None, dict[str, Any] | None, str | None]:
    try:
        path = _safe_rel_path(root, request_path)
        path.relative_to((root / CODEX_WORK_REQUESTS_DIR).resolve())
    except (ValueError, RuntimeError):
        return None, None, "request_path_not_bounded_to_codex_work_requests"
    if not path.exists():
        return None, None, "request_path_missing"
    payload = _read_json(path) or {}
    if not payload.get("agent_invocation_id"):
        return path, payload, "request_path_is_not_agent_invocation_work"
    if payload.get("status") != "QUEUED_FOR_CODEX_CARRIER":
        return path, payload, "agent_invocation_work_request_not_queued"
    return path, payload, None


def swarm_step_once(
    root: str | Path | None = None,
    *,
    start: bool = False,
    request_path: str | None = None,
    timeout_seconds: int = 1800,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    selected: str | None = None
    if request_path:
        selected = request_path
    else:
        queued = _agent_work_requests(shell_root, queued_only=True)
        if queued:
            selected = _connector_rel(queued[0][0], shell_root)
    if not selected:
        return {
            "schema_id": SCHEMA_ID,
            "ok": True,
            "result": "NO_QUEUED_AGENT_INVOCATION",
            "swarm_status": build_agent_broker_status(shell_root),
            "production_authority": False,
            "live_execution_authority": False,
        }
    _path, _payload, finding = _load_agent_work_request_for_step(shell_root, selected)
    if finding:
        return {
            "schema_id": SCHEMA_ID,
            "ok": False,
            "result": "AGENT_SWARM_STEP_BLOCKED",
            "request_path": selected,
            "finding": finding,
            "failure_classification": "AGENT_INVOCATION_FAILURE",
            "production_authority": False,
            "live_execution_authority": False,
        }
    result = process_codex_queue_once(
        shell_root,
        request_path=selected,
        start=start,
        background=True,
        timeout_seconds=timeout_seconds,
    )
    return {
        "schema_id": SCHEMA_ID,
        "ok": bool(result.get("ok")),
        "result": result.get("result") or ("BACKEND_RUN_STARTED" if start else "BACKEND_RUN_PREPARED"),
        "request_path": selected,
        "start_requested": start,
        "backend_result": result,
        "failure_classification": None if result.get("ok") else "BACKEND_CODEX_FAILURE",
        "production_authority": False,
        "live_execution_authority": False,
    }


def cancel_agent_invocation(root: str | Path | None = None, *, invocation_id: str) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    path, invocation = _load_invocation(shell_root, invocation_id)
    if path is None or invocation is None:
        return _blocked("ion_agent_cancel", "agent_invocation_not_found")
    work_rel = str(invocation.get("codex_work_request_path") or "")
    work_payload = _work_request_for_invocation(shell_root, invocation) or {}
    if work_payload.get("status") in ACTIVE_BACKEND_WORK_REQUEST_STATUSES:
        return _blocked("ion_agent_cancel", "cannot_cancel_active_backend_run", {"codex_work_request_status": work_payload.get("status")})
    invocation_status = str(invocation.get("status") or "")
    work_status = str(work_payload.get("status") or "")
    if invocation_status not in CANCELLABLE_INVOCATION_STATUSES or work_status not in CANCELLABLE_WORK_REQUEST_STATUSES:
        return _blocked(
            "ion_agent_cancel",
            "can_cancel_only_prepared_or_queued_invocations",
            {
                "invocation_status": invocation_status or None,
                "codex_work_request_status": work_status or None,
            },
        )
    now = _now()
    invocation["status"] = "CANCELLED_BY_CARRIER_REQUEST"
    invocation["updated_at"] = now
    _write_json(path, invocation)
    if work_rel and work_payload:
        work_path = _safe_rel_path(shell_root, work_rel)
        work_payload["status"] = "CANCELLED_BY_AGENT_INVOCATION_BROKER"
        work_payload["updated_at"] = now
        _write_json(work_path, work_payload)
    queue = _write_codex_work_queue_index(shell_root)
    return {
        "schema_id": SCHEMA_ID,
        "ok": True,
        "result": "AGENT_INVOCATION_CANCELLED",
        "invocation_id": invocation.get("invocation_id"),
        "invocation_path": _connector_rel(path, shell_root),
        "codex_work_request_path": work_rel or None,
        "codex_work_queue_request_count": queue["request_count"],
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_agent_broker_status(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    owner_paths = {
        "agent_invocation_broker": "ION/04_packages/kernel/ion_agent_invocation_broker.py",
        "codex_queue_runner": QUEUE_RUNNER_OWNER.as_posix(),
        "codex_work_queue": CODEX_WORK_QUEUE_INDEX.as_posix(),
        "codex_work_requests": CODEX_WORK_REQUESTS_DIR.as_posix(),
        "task_returns": TASK_RETURNS_DIR.as_posix(),
        "agent_roster_registry": AGENT_ROSTER_REGISTRY.as_posix(),
        "agent_context_system_registry": AGENT_CONTEXT_SYSTEM_REGISTRY.as_posix(),
        "codex_cli_carrier_profile": CODEX_CLI_CARRIER_PROFILE.as_posix(),
        "codex_cli_execution_packet": CODEX_CLI_EXECUTION_PACKET.as_posix(),
    }
    findings = [f"missing_owner_surface:{label}:{rel}" for label, rel in owner_paths.items() if not (shell_root / rel).exists()]
    agent_work = _agent_work_requests(shell_root)
    queued_agent_work = [payload for _path, payload in agent_work if payload.get("status") == "QUEUED_FOR_CODEX_CARRIER"]
    state = _read_json(shell_root / BROKER_STATE_PATH) or {}
    ready = not findings
    return {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT if ready else BLOCKED_VERDICT,
        "accepted": ready,
        "owner_paths": {label: {"path": rel, "exists": (shell_root / rel).exists()} for label, rel in owner_paths.items()},
        "agent_count": list_agents(shell_root)["agent_count"],
        "agent_invocation_count": len(_invocation_paths(shell_root)),
        "agent_codex_work_request_count": len(agent_work),
        "queued_agent_codex_work_request_count": len(queued_agent_work),
        "next_agent_codex_work_request_path": _connector_rel(_agent_work_requests(shell_root, queued_only=True)[0][0], shell_root) if queued_agent_work else None,
        "latest_state": state,
        "codex_queue_runner": build_codex_queue_runner_status(shell_root, reconcile=False),
        "failure_classes": list(FAILURE_CLASSES),
        "tools": {"read": list(READ_TOOL_NAMES), "write": list(WRITE_TOOL_NAMES)},
        "no_parallel_agent_system_created": True,
        "raw_backend_output_state_policy": "RAW_CODEX_OUTPUT_NOT_ACCEPTED_WITHOUT_TASK_RETURN_PROOF_GATES",
        "findings": findings,
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ION agent invocation broker.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--queue", action="store_true")
    parser.add_argument("--result", default=None)
    parser.add_argument("--spawn-plan", action="store_true")
    parser.add_argument("--invoke", action="store_true")
    parser.add_argument("--agent", default="")
    parser.add_argument("--objective", default="")
    parser.add_argument("--enqueue", action="store_true")
    parser.add_argument("--start", action="store_true")
    parser.add_argument("--step-once", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.list:
        result = list_agents(args.ion_root)
        ok = True
    elif args.queue:
        result = agent_queue(args.ion_root)
        ok = True
    elif args.result is not None:
        result = agent_result(args.ion_root, invocation_id=args.result or None)
        ok = bool(result.get("ok"))
    elif args.spawn_plan:
        result = build_agent_spawn_plan(args.ion_root, objective=args.objective or None)
        ok = True
    elif args.invoke:
        result = invoke_agent(
            args.ion_root,
            agent=args.agent,
            objective=args.objective,
            queue=args.enqueue,
            start=args.start,
        )
        ok = bool(result.get("ok"))
    elif args.step_once:
        result = swarm_step_once(args.ion_root, start=args.start)
        ok = bool(result.get("ok"))
    else:
        result = build_agent_broker_status(args.ion_root)
        ok = bool(result.get("accepted", result.get("verdict") == READY_VERDICT))

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result.get("verdict") or result.get("result") or ("OK" if ok else "BLOCKED"))
        for finding in result.get("findings", []):
            print(f"- {finding}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
