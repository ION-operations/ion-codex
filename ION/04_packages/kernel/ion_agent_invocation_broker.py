"""ION agent invocation broker over the existing Codex queue runner.

The broker is not a separate agent system. It compiles role/context evidence
into bounded Codex work requests and leaves execution, proof gates, task
returns, and receipts with the existing ION connector owners.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_codex_queue_runner import (
    DEFAULT_CODEX_TIMEOUT_SECONDS,
    MAX_CODEX_TIMEOUT_SECONDS,
    build_codex_queue_runner_status,
    process_codex_queue_once,
)

SCHEMA_ID = "ion.agent_invocation_broker.v1"
READY_VERDICT = "ION_AGENT_INVOCATION_BROKER_READY"
BLOCKED_VERDICT = "ION_AGENT_INVOCATION_BROKER_BLOCKED"

CONNECTOR_STATE_DIR = Path("ION/05_context/current/chatgpt_connector")
AGENT_INVOCATIONS_DIR = CONNECTOR_STATE_DIR / "agent_invocations"
RUNTIME_DIR = CONNECTOR_STATE_DIR / "runtime"
BROKER_STATE_PATH = RUNTIME_DIR / "agent_invocation_broker_state.json"
AGENT_IDEMPOTENCY_LEDGER = RUNTIME_DIR / "agent_invocation_idempotency_ledger.json"
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
BASE_RETURN_CONTRACT_SECTIONS = (
    "### CONTEXT PROOF",
    "### TEMPLATE ACTION PROOF",
    "### VALIDATION",
    "### RESULT",
)
WORKLOAD_DIFF_SECTION = "### WORKLOAD DIFF"
MIN_AGENT_WORKLOAD_TIMEOUT_SECONDS = 900

CANCELLABLE_INVOCATION_STATUSES = {
    "PREPARED_NOT_QUEUED",
    "QUEUED_FOR_CODEX_CARRIER",
    "QUEUED",
    "WAITING_FOR_CHATGPT",
    "WAITING_FOR_OPERATOR",
    "PAUSED",
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

AGENT_STATE_MACHINE = (
    "QUEUED",
    "VALIDATING",
    "RUNNING",
    "WAITING_FOR_CHATGPT",
    "WAITING_FOR_OPERATOR",
    "BLOCKED",
    "TERMINAL_ACCEPTED",
    "TERMINAL_BLOCKED",
    "TERMINAL_FAILED",
    "CANCELLED",
)

HARD_GATES = (
    "access_credential",
    "broad_shell",
    "delete_file",
    "overwrite_protected_file",
    "production_deploy",
    "push_main",
)

PROTECTED_PATH_TOKENS = (
    ".env",
    "secret",
    "secrets",
    "credential",
    "credentials",
    "token",
    "tokens",
    "vault",
    ".git/",
)

SUPPORTED_BOUNDED_AGENT_ROLES: dict[str, dict[str, Any]] = {
    "role.context_cartographer": {
        "display_name": "CONTEXT_CARTOGRAPHER",
        "default_read_zones": ["ION/"],
        "write_posture": "none",
        "default_proof_obligations": ["context_receipt", "template_action_proof", "changed_files_summary", "tests_or_validation", "receipt"],
        "settlement_target": "chatgpt_browser",
    },
    "role.runtime_cartographer": {
        "display_name": "RUNTIME_CARTOGRAPHER",
        "default_read_zones": ["ION/"],
        "write_posture": "none",
        "default_proof_obligations": ["context_receipt", "template_action_proof", "tests_or_validation", "receipt"],
        "settlement_target": "chatgpt_browser",
    },
    "role.canon_librarian": {
        "display_name": "CANON_LIBRARIAN",
        "default_read_zones": ["ION/"],
        "write_posture": "none",
        "default_proof_obligations": ["context_receipt", "template_action_proof", "receipt"],
        "settlement_target": "chatgpt_browser",
    },
    "role.template_curator": {
        "display_name": "TEMPLATE_CURATOR",
        "default_read_zones": ["ION/"],
        "write_posture": "gated",
        "default_proof_obligations": ["context_receipt", "template_action_proof", "changed_files_summary", "tests_or_validation", "receipt"],
        "settlement_target": "chatgpt_browser",
    },
    "role.scribe": {
        "display_name": "SCRIBE",
        "default_read_zones": ["ION/"],
        "write_posture": "gated",
        "default_proof_obligations": ["context_receipt", "template_action_proof", "changed_files_summary", "receipt"],
        "settlement_target": "chatgpt_browser",
    },
    "role.nemesis_reviewer": {
        "display_name": "NEMESIS_REVIEWER",
        "default_read_zones": ["ION/"],
        "write_posture": "none",
        "default_proof_obligations": ["context_receipt", "template_action_proof", "tests_or_validation", "receipt"],
        "settlement_target": "chatgpt_browser",
    },
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


def _normalize_agent_timeout_seconds(raw_timeout: Any) -> int:
    try:
        timeout = int(raw_timeout)
    except (TypeError, ValueError):
        timeout = DEFAULT_CODEX_TIMEOUT_SECONDS
    timeout = max(timeout, MIN_AGENT_WORKLOAD_TIMEOUT_SECONDS)
    timeout = min(timeout, MAX_CODEX_TIMEOUT_SECONDS)
    return timeout


def _agent_return_contract_sections() -> list[str]:
    return [*BASE_RETURN_CONTRACT_SECTIONS, WORKLOAD_DIFF_SECTION]


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

    for role_id, defaults in SUPPORTED_BOUNDED_AGENT_ROLES.items():
        record = by_role.setdefault(role_id, {
            "agent_id": role_id,
            "role_id": role_id,
            "display_name": defaults["display_name"],
            "base_sources": [
                AGENT_CONTEXT_SYSTEM_REGISTRY.as_posix(),
                AGENT_ROSTER_REGISTRY.as_posix(),
            ],
            "package_strategy": "bounded capsule context package compiled for ChatGPT Browser carrier invocation",
            "default_active_package_class": "BOUNDED_AGENT_INVOCATION_CONTEXT_PACKAGE",
        })
        record.setdefault("display_name", defaults["display_name"])
        record.setdefault("default_authority_ceiling", {
            "production_authority": False,
            "live_execution_authority": False,
            "local_write_authority": defaults["write_posture"],
        })
        record.setdefault("default_proof_obligations", list(defaults["default_proof_obligations"]))
        record.setdefault("default_read_zones", list(defaults["default_read_zones"]))
        record.setdefault("write_posture", defaults["write_posture"])
        record.setdefault("relay_policy", {
            "allow_relay_to_chatgpt": True,
            "allow_relay_to_operator": True,
            "no_silent_authority_expansion": True,
        })
        record.setdefault("settlement_target", defaults["settlement_target"])

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


def _timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _load_agent_idempotency_ledger(root: Path) -> dict[str, Any]:
    return _read_json(root / AGENT_IDEMPOTENCY_LEDGER) or {
        "schema_id": "ion.agent_invocation_idempotency_ledger.v1",
        "entries": {},
        "production_authority": False,
        "live_execution_authority": False,
    }


def _record_agent_idempotency(root: Path, key: str, entry: Mapping[str, Any]) -> None:
    ledger = _load_agent_idempotency_ledger(root)
    entries = dict(ledger.get("entries") if isinstance(ledger.get("entries"), Mapping) else {})
    entries[key] = dict(entry)
    ledger["entries"] = entries
    ledger["updated_at"] = _now()
    _write_json(root / AGENT_IDEMPOTENCY_LEDGER, ledger)


def _agent_invocation_dir(root: Path, invocation_id: str) -> Path:
    return root / AGENT_INVOCATIONS_DIR / _safe_slug(invocation_id)


def _agent_receipts_dir(root: Path, invocation_id: str) -> Path:
    return _agent_invocation_dir(root, invocation_id) / "receipts"


def _write_agent_receipt(root: Path, *, invocation_id: str, event: str, status: str, payload: Mapping[str, Any] | None = None) -> str:
    receipt_id = f"agent_receipt_{_timestamp_slug()}_{_safe_slug(event)}_{_safe_slug(invocation_id)[:40]}"
    receipt = {
        "schema_id": "ion.agent_invocation_receipt.v1",
        "receipt_id": receipt_id,
        "invocation_id": invocation_id,
        "event": event,
        "status": status,
        "created_at": _now(),
        "payload": dict(payload or {}),
        "production_authority": False,
        "live_execution_authority": False,
    }
    base = _agent_receipts_dir(root, invocation_id)
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{receipt_id}.json"
    counter = 1
    while path.exists():
        path = base / f"{receipt_id}_{counter}.json"
        counter += 1
    _write_json(path, receipt)
    return _connector_rel(path, root)


def _safe_repo_path_value(value: str) -> str | None:
    if not value:
        return "empty_path"
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or normalized.startswith("../") or "/../" in normalized or normalized.endswith("/.."):
        return "path_escape"
    lowered = normalized.lower()
    if any(token in lowered for token in PROTECTED_PATH_TOKENS):
        return "protected_path_token"
    return None


def _json_text(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True).lower()
    except TypeError:
        return str(value).lower()


def _default_invocation_packet(packet: Mapping[str, Any], agent_record: Mapping[str, Any], now: str) -> dict[str, Any]:
    agent_role = str(packet.get("agent_role") or agent_record.get("role_id") or "")
    authority = dict(packet.get("authority") if isinstance(packet.get("authority"), Mapping) else {})
    execution = dict(packet.get("execution") if isinstance(packet.get("execution"), Mapping) else {})
    capsule_context = dict(packet.get("capsule_context") if isinstance(packet.get("capsule_context"), Mapping) else {})
    relay_policy = dict(packet.get("relay_policy") if isinstance(packet.get("relay_policy"), Mapping) else {})
    proof_required = dict(packet.get("proof_required") if isinstance(packet.get("proof_required"), Mapping) else {})
    settlement = dict(packet.get("settlement") if isinstance(packet.get("settlement"), Mapping) else {})
    objective = str(packet.get("objective") or "").strip()
    key = str(packet.get("idempotency_key") or "").strip()
    invocation_id = str(packet.get("invocation_id") or f"agent_inv_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(agent_role)}_{hashlib.sha256((key + objective).encode('utf-8')).hexdigest()[:12]}")
    authority.setdefault("production_authority", False)
    authority.setdefault("live_execution_authority", False)
    authority.setdefault("local_write_authority", "none")
    authority.setdefault("requires_operator_approval", False)
    authority.setdefault("operator_approval_evidence", None)
    authority.setdefault("allowed_paths", list(agent_record.get("default_read_zones") or ["ION/"]))
    authority.setdefault("forbidden_paths", [".env", "secrets", "credentials"])
    authority.setdefault("hard_gates", list(HARD_GATES))
    execution.setdefault("backend", "codex_cli")
    execution.setdefault("queue", True)
    execution.setdefault("max_runtime_seconds", 1800)
    execution.setdefault("max_steps", 8)
    execution.setdefault("stop_condition", "return proof packet, relay question, or blocker")
    execution["max_runtime_seconds"] = _normalize_agent_timeout_seconds(execution.get("max_runtime_seconds"))
    capsule_context.setdefault("mode", "refs_and_inline_summary")
    capsule_context.setdefault("context_refs", [])
    capsule_context.setdefault("inline_summary", "")
    capsule_context.setdefault("required_reads", [])
    capsule_context.setdefault("forbidden_reads", [])
    capsule_context.setdefault("source_posture", "candidate")
    for key_name in ("context_receipt", "template_action_proof", "changed_files_summary", "tests_or_validation", "receipt"):
        proof_required.setdefault(key_name, True)
    relay_policy.setdefault("allow_relay_to_chatgpt", True)
    relay_policy.setdefault("allow_relay_to_operator", True)
    relay_policy.setdefault("ask_operator_on_authority_gap", True)
    relay_policy.setdefault("no_silent_authority_expansion", True)
    settlement.setdefault("settlement_target", "chatgpt_browser")
    settlement.setdefault("terminal_states", ["accepted", "blocked", "deferred", "rejected", "failed"])
    return {
        "schema_id": "ion.agent_invocation_packet.v1",
        "invocation_id": invocation_id,
        "idempotency_key": str(packet.get("idempotency_key") or "").strip(),
        "created_at": str(packet.get("created_at") or now),
        "created_by": str(packet.get("created_by") or "chatgpt_browser"),
        "agent_role": agent_role,
        "agent_display_name": str(packet.get("agent_display_name") or agent_record.get("display_name") or _display_from_role_id(agent_role)),
        "objective": objective,
        "capsule_context": capsule_context,
        "authority": authority,
        "execution": execution,
        "proof_required": proof_required,
        "relay_policy": relay_policy,
        "settlement": settlement,
        "production_authority": False,
        "live_execution_authority": False,
    }


def validate_agent_invocation_packet(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    findings: list[str] = []
    refusal_class: str | None = None
    if not str(packet.get("idempotency_key") or "").strip():
        findings.append("idempotency_key_required")
        refusal_class = "IDEMPOTENCY_KEY_REQUIRED"
    objective = str(packet.get("objective") or "").strip()
    if not objective:
        findings.append("objective_required")
        refusal_class = refusal_class or "SCHEMA_INVALID"
    agent_role = str(packet.get("agent_role") or packet.get("agent") or "").strip()
    if not agent_role:
        findings.append("agent_role_required")
        refusal_class = refusal_class or "SCHEMA_INVALID"
        agent_record = None
    else:
        agent_record, finding = _resolve_agent(shell_root, agent_role)
        if finding or agent_record is None:
            findings.append(f"agent_role_not_supported:{agent_role}")
            refusal_class = refusal_class or "SCHEMA_INVALID"
    authority = packet.get("authority") if isinstance(packet.get("authority"), Mapping) else {}
    if packet.get("production_authority") is True or authority.get("production_authority") is not False:
        findings.append("production_authority_refused")
        refusal_class = refusal_class or "PRODUCTION_AUTHORITY_REFUSED"
    if packet.get("live_execution_authority") is True or authority.get("live_execution_authority") is not False:
        findings.append("live_execution_authority_refused")
        refusal_class = refusal_class or "LIVE_EXECUTION_AUTHORITY_REFUSED"
    if str(authority.get("local_write_authority") or "none") not in {"none", "gated", "bounded"}:
        findings.append("invalid_local_write_authority")
        refusal_class = refusal_class or "SCHEMA_INVALID"
    intent = str(packet.get("intent") or "").strip()
    if intent in HARD_GATES:
        findings.append(f"hard_gated_intent:{intent}")
        refusal_class = refusal_class or "INTENT_HARD_GATED"
    text = _json_text({"objective": objective, "requested_authority": packet.get("requested_authority"), "intent": intent})
    for gate in HARD_GATES:
        if gate in text and intent != "":
            findings.append(f"hard_gated_scope:{gate}")
            refusal_class = refusal_class or "INTENT_HARD_GATED"
            break
    for key in ("allowed_paths", "forbidden_paths"):
        values = authority.get(key)
        if values is None:
            continue
        if not isinstance(values, list):
            findings.append(f"{key}_must_be_list")
            refusal_class = refusal_class or "SCHEMA_INVALID"
            continue
        for value in values:
            problem = _safe_repo_path_value(str(value))
            if problem and key == "allowed_paths":
                findings.append(f"invalid_allowed_path:{value}:{problem}")
                refusal_class = refusal_class or "PATH_NOT_ALLOWED"
    return {
        "schema_id": "ion.agent_invocation_packet_validation.v1",
        "ok": not findings,
        "accepted": not findings,
        "findings": findings,
        "refusal_class": refusal_class,
        "agent_role": agent_role or None,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _build_capsule_context(invocation: Mapping[str, Any], agent_record: Mapping[str, Any], generated_at: str) -> dict[str, Any]:
    context = dict(invocation.get("capsule_context") if isinstance(invocation.get("capsule_context"), Mapping) else {})
    return {
        "schema_id": "ion.agent_invocation_capsule_context.v1",
        "invocation_id": invocation.get("invocation_id"),
        "agent_role": invocation.get("agent_role"),
        "agent_display_name": invocation.get("agent_display_name"),
        "objective": invocation.get("objective"),
        "mode": context.get("mode") or "refs_and_inline_summary",
        "context_refs": context.get("context_refs") if isinstance(context.get("context_refs"), list) else [],
        "inline_summary": context.get("inline_summary") or "",
        "required_reads": context.get("required_reads") if isinstance(context.get("required_reads"), list) else [],
        "forbidden_reads": context.get("forbidden_reads") if isinstance(context.get("forbidden_reads"), list) else [],
        "authority_posture": invocation.get("authority"),
        "source_posture": context.get("source_posture") or "candidate",
        "agent_context_paths": agent_record.get("context_paths", []),
        "generated_at": generated_at,
        "checksum": hashlib.sha256(json.dumps({
            "invocation_id": invocation.get("invocation_id"),
            "objective": invocation.get("objective"),
            "context_refs": context.get("context_refs") if isinstance(context.get("context_refs"), list) else [],
            "inline_summary": context.get("inline_summary") or "",
        }, sort_keys=True).encode("utf-8")).hexdigest(),
        "production_authority": False,
        "live_execution_authority": False,
    }


def _build_bounded_agent_objective(invocation: Mapping[str, Any], capsule_rel: str) -> str:
    return "\n".join([
        f"Bounded ION agent invocation: {invocation.get('agent_display_name')} ({invocation.get('agent_role')}).",
        "",
        f"Invocation id: {invocation.get('invocation_id')}",
        f"Capsule context: {capsule_rel}",
        f"Objective: {invocation.get('objective')}",
        "",
        "Authority ceiling:",
        json.dumps(invocation.get("authority") or {}, indent=2, sort_keys=True),
        "",
        "Relay policy:",
        json.dumps(invocation.get("relay_policy") or {}, indent=2, sort_keys=True),
        "",
        "Proof law:",
        "- AI output is not state.",
        "- Agent output is candidate until proof, settlement, and receipt.",
        "- No proof -> no landing.",
        "- No receipt -> no inheritance.",
        "- Return CONTEXT PROOF, TEMPLATE ACTION PROOF, VALIDATION, RESULT, BLOCKERS, and RECOMMENDED NEXT PACKET.",
        "- Stop with a relay question or blocker if context, route, knowledge, or authority is missing.",
    ])


def invoke_bounded_agent(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    validation = validate_agent_invocation_packet(shell_root, packet)
    if not validation["ok"]:
        findings = list(validation.get("findings") or [])
        errors: list[str] = []
        for finding in findings:
            if finding == "idempotency_key_required":
                errors.append("MISSING_IDEMPOTENCY_KEY")
            elif finding == "production_authority_refused":
                errors.append("PRODUCTION_AUTHORITY_FORBIDDEN")
            elif finding == "live_execution_authority_refused":
                errors.append("LIVE_EXECUTION_AUTHORITY_FORBIDDEN")
            elif finding.startswith("hard_gated_intent:"):
                errors.append("HARD_GATED_INTENT:" + finding.split(":", 1)[1])
            elif finding.startswith("hard_gated_scope:"):
                errors.append("HARD_GATED_SCOPE:" + finding.split(":", 1)[1])
            elif finding.startswith("invalid_allowed_path:"):
                errors.append("FORBIDDEN_ALLOWED_PATH:" + finding.split(":", 1)[1])
        errors.extend(finding for finding in findings if finding not in errors)
        return {
            "schema_id": "ion.agent_invocation_gateway_result.v1",
            "ok": False,
            "status": "REFUSED",
            "error": "AGENT_INVOCATION_VALIDATION_FAILED",
            "errors": errors,
            "refusal_class": validation.get("refusal_class") or "SCHEMA_INVALID",
            "finding": "agent_invocation_packet_refused",
            "validation": validation,
            "production_authority": False,
            "live_execution_authority": False,
        }
    key = str(packet.get("idempotency_key") or "").strip()
    ledger = _load_agent_idempotency_ledger(shell_root)
    existing = (ledger.get("entries") if isinstance(ledger.get("entries"), Mapping) else {}).get(key)
    if isinstance(existing, Mapping):
        return {
            "schema_id": "ion.agent_invocation_gateway_result.v1",
            "ok": True,
            "idempotent_replay": True,
            "result": "AGENT_INVOCATION_IDEMPOTENT_REPLAY",
            "existing": dict(existing),
            "invocation_id": existing.get("invocation_id"),
            "status": existing.get("status"),
            "invocation_path": existing.get("invocation_path"),
            "capsule_context_path": existing.get("capsule_context_path"),
            "codex_work_request_path": existing.get("codex_work_request_path"),
            "receipt_paths": existing.get("receipt_paths", []),
            "production_authority": False,
            "live_execution_authority": False,
        }
    agent_record, _finding = _resolve_agent(shell_root, str(packet.get("agent_role") or packet.get("agent") or ""))
    if agent_record is None:
        return _blocked("ion_agent_invoke", "agent_resolution_failed_after_validation")
    now = _now()
    invocation = _default_invocation_packet(packet, agent_record, now)
    invocation_id = str(invocation["invocation_id"])
    invocation_dir = _agent_invocation_dir(shell_root, invocation_id)
    invocation_path = invocation_dir / "invocation.json"
    capsule_path = invocation_dir / "capsule_context.json"
    if invocation_path.exists():
        return {
            "schema_id": "ion.agent_invocation_gateway_result.v1",
            "ok": False,
            "refusal_class": "IDEMPOTENCY_REPLAY_BLOCKED",
            "finding": "invocation_id_already_exists",
            "invocation_id": invocation_id,
            "production_authority": False,
            "live_execution_authority": False,
        }
    invocation["status"] = "VALIDATING"
    invocation["state_machine"] = list(AGENT_STATE_MACHINE)
    invocation["agent"] = agent_record
    invocation["updated_at"] = now
    invocation_dir.mkdir(parents=True, exist_ok=True)
    _write_json(invocation_path, invocation)
    validated_receipt = _write_agent_receipt(shell_root, invocation_id=invocation_id, event="agent_invocation_validated", status="validated", payload={"validation": validation})
    capsule = _build_capsule_context(invocation, agent_record, now)
    _write_json(capsule_path, capsule)
    capsule_rel = _connector_rel(capsule_path, shell_root)
    capsule_receipt = _write_agent_receipt(shell_root, invocation_id=invocation_id, event="capsule_context_created", status="created", payload={"capsule_context_path": capsule_rel})
    execution = invocation.get("execution") if isinstance(invocation.get("execution"), Mapping) else {}
    queued = execution.get("queue") is not False
    request_status = "QUEUED_FOR_CODEX_CARRIER" if queued else "PREPARED_FOR_CODEX_CARRIER_NOT_QUEUED"
    request_id = f"codex_req_agent_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(invocation_id)}"
    work_path = _unique_packet_path(shell_root, CODEX_WORK_REQUESTS_DIR, now, _safe_slug(f"agent_{invocation.get('agent_display_name')}_{invocation.get('objective')}"))
    work_rel = _connector_rel(work_path, shell_root)
    context_refs = capsule.get("context_refs") if isinstance(capsule.get("context_refs"), list) else []
    required_reads = capsule.get("required_reads") if isinstance(capsule.get("required_reads"), list) else []
    required_context_reads = [{"kind": "capsule_context", "path": capsule_rel, "required": True}]
    required_context_reads.extend({"kind": "context_ref", "path": str(path), "required": False} for path in context_refs)
    required_context_reads.extend({"kind": "required_read", "path": str(path), "required": True} for path in required_reads)
    work_packet = {
        "schema_id": "ion.chatgpt_browser_connector_codex_work_request.v1",
        "request_id": request_id,
        "objective": _build_bounded_agent_objective(invocation, capsule_rel),
        "requested_by": "ion_agent_invocation_broker",
        "requested_by_carrier_id": invocation.get("created_by"),
        "agent_invocation_id": invocation_id,
        "invocation_id": invocation_id,
        "agent_role": invocation.get("agent_role"),
        "agent_role_id": invocation.get("agent_role"),
        "agent_display_name": invocation.get("agent_display_name"),
        "capsule_context_path": capsule_rel,
        "relay_policy": invocation.get("relay_policy"),
        "authority_ceiling": invocation.get("authority"),
        "settlement_target": (invocation.get("settlement") or {}).get("settlement_target") if isinstance(invocation.get("settlement"), Mapping) else "chatgpt_browser",
        "required_context_reads": required_context_reads,
        "return_contract_sections": _agent_return_contract_sections(),
        "failure_classes": list(FAILURE_CLASSES),
        "status": request_status,
        "created_at": now,
        "updated_at": now,
        "return_packet_paths": [],
        "latest_return_packet_path": None,
        "production_authority": False,
        "live_execution_authority": False,
    }
    work_packet["packet_path"] = work_rel
    _write_json(work_path, work_packet)
    invocation["status"] = "QUEUED" if queued else "PREPARED_NOT_QUEUED"
    invocation["codex_work_request_id"] = request_id
    invocation["codex_work_request_path"] = work_rel
    invocation["capsule_context_path"] = capsule_rel
    invocation["receipt_paths"] = [validated_receipt, capsule_receipt]
    invocation["updated_at"] = _now()
    _write_json(invocation_path, invocation)
    queue_index = _write_codex_work_queue_index(shell_root)
    enqueued_receipt = _write_agent_receipt(shell_root, invocation_id=invocation_id, event="agent_invocation_enqueued", status="queued" if queued else "prepared", payload={"codex_work_request_path": work_rel, "queue_path": CODEX_WORK_QUEUE_INDEX.as_posix()})
    invocation.setdefault("receipt_paths", []).append(enqueued_receipt)
    _write_json(invocation_path, invocation)
    result = {
        "schema_id": "ion.agent_invocation_gateway_result.v1",
        "ok": True,
        "result": "AGENT_INVOCATION_QUEUED" if queued else "AGENT_INVOCATION_PREPARED",
        "invocation_id": invocation_id,
        "status": invocation["status"],
        "invocation_path": _connector_rel(invocation_path, shell_root),
        "capsule_context_path": capsule_rel,
        "codex_work_request_id": request_id,
        "codex_work_request_path": work_rel,
        "codex_work_queue_path": CODEX_WORK_QUEUE_INDEX.as_posix(),
        "codex_work_queue_request_count": queue_index["request_count"],
        "receipt_paths": invocation["receipt_paths"],
        "relay_status": "none",
        "proof_posture": invocation.get("proof_required"),
        "production_authority": False,
        "live_execution_authority": False,
    }
    _record_agent_idempotency(shell_root, key, {
        "recorded_at": _now(),
        "invocation_id": invocation_id,
        "status": invocation["status"],
        "invocation_path": result["invocation_path"],
        "capsule_context_path": capsule_rel,
        "codex_work_request_path": work_rel,
        "receipt_paths": invocation["receipt_paths"],
    })
    _write_broker_state(shell_root, {
        "latest_invocation_id": invocation_id,
        "latest_invocation_path": result["invocation_path"],
        "latest_codex_work_request_path": work_rel,
        "latest_requested_agent": invocation.get("agent_role"),
    })
    return result


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
        "return_contract_sections": _agent_return_contract_sections(),
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
        normalized_timeout = _normalize_agent_timeout_seconds(timeout_seconds)
        start_result = process_codex_queue_once(
            shell_root,
            request_path=work_rel,
            start=True,
            background=True,
            timeout_seconds=normalized_timeout,
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
    paths = [path for path in base.glob("*.json") if path.is_file()]
    paths.extend(path for path in base.glob("*/invocation.json") if path.is_file())
    return sorted(paths, key=lambda path: path.stat().st_mtime, reverse=True)


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


def _relays_for_invocation(root: Path, invocation_id: str, *, include_answered: bool = False) -> list[dict[str, Any]]:
    base = _agent_invocation_dir(root, invocation_id) / "relays"
    if not base.exists():
        return []
    rows: list[dict[str, Any]] = []
    for path in sorted(base.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        payload = _read_json(path) or {}
        if not include_answered and payload.get("status") not in {"WAITING", "ESCALATED"}:
            continue
        row = dict(payload)
        row["path"] = _connector_rel(path, root)
        rows.append(row)
    return rows


def _update_invocation_status(root: Path, invocation_id: str, status: str) -> None:
    path, invocation = _load_invocation(root, invocation_id)
    if path is None or invocation is None:
        return
    invocation["status"] = status
    invocation["updated_at"] = _now()
    _write_json(path, invocation)
    work_rel = str(invocation.get("codex_work_request_path") or "")
    if work_rel:
        try:
            work_path = _safe_rel_path(root, work_rel)
        except (ValueError, RuntimeError):
            return
        work = _read_json(work_path) or {}
        if work:
            work["agent_state"] = status
            if status in {"WAITING_FOR_CHATGPT", "WAITING_FOR_OPERATOR"}:
                work["status"] = status
            elif status == "QUEUED" and work.get("status") in {"WAITING_FOR_CHATGPT", "WAITING_FOR_OPERATOR", "PAUSED"}:
                work["status"] = "QUEUED_FOR_CODEX_CARRIER"
            elif status == "CANCELLED":
                work["status"] = "CANCELLED_BY_AGENT_INVOCATION_BROKER"
            work["updated_at"] = _now()
            _write_json(work_path, work)
            _write_codex_work_queue_index(root)


def build_bounded_agent_status(root: str | Path | None = None, *, invocation_id: str | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    broker = build_agent_broker_status(shell_root)
    rows = agent_queue(shell_root, limit=50)["invocations"]
    if invocation_id:
        path, invocation = _load_invocation(shell_root, invocation_id)
        if path is None or invocation is None:
            return _blocked("agent_status", "agent_invocation_not_found")
        work = _work_request_for_invocation(shell_root, invocation) or {}
        relays = _relays_for_invocation(shell_root, str(invocation.get("invocation_id") or ""), include_answered=True)
        return {
            "schema_id": "ion.agent_invocation_status.v1",
            "ok": True,
            "invocation_id": invocation.get("invocation_id"),
            "status": invocation.get("status"),
            "invocation": invocation,
            "phase": work.get("status") or invocation.get("status"),
            "invocation_path": _connector_rel(path, shell_root),
            "capsule_context_path": invocation.get("capsule_context_path"),
            "codex_work_request_path": invocation.get("codex_work_request_path"),
            "latest_return_packet_path": work.get("latest_return_packet_path"),
            "heartbeat": {
                "updated_at": invocation.get("updated_at"),
                "active_process_running": broker.get("codex_queue_runner", {}).get("active_process_running") if isinstance(broker.get("codex_queue_runner"), Mapping) else None,
            },
            "evidence_refs": [invocation.get("capsule_context_path"), invocation.get("codex_work_request_path")],
            "relay_status": {
                "pending_count": sum(1 for relay in relays if relay.get("status") in {"WAITING", "ESCALATED"}),
                "relays": relays,
            },
            "proof_posture": invocation.get("proof_required"),
            "receipt_paths": invocation.get("receipt_paths", []),
            "broker_status": broker,
            "production_authority": False,
            "live_execution_authority": False,
        }
    return {
        "schema_id": "ion.agent_invocation_status.v1",
        "ok": True,
        "active_or_recent_invocations": rows,
        "broker_status": broker,
        "pending_relays": pending_agent_relays(shell_root, include_answered=False)["relays"],
        "state_machine": list(AGENT_STATE_MACHINE),
        "production_authority": False,
        "live_execution_authority": False,
    }


def create_agent_relay_message(
    root: str | Path | None,
    relay_packet: Mapping[str, Any] | None = None,
    *,
    invocation_id: str | None = None,
    question: str | None = None,
    question_type: str = "context",
    to: str = "chatgpt_browser",
    run_id: str | None = None,
    options: list[str] | None = None,
    authority_needed: Mapping[str, Any] | None = None,
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    if relay_packet is not None:
        invocation_id = str(relay_packet.get("invocation_id") or invocation_id or "")
        question = str(relay_packet.get("question") or question or "")
        question_type = str(relay_packet.get("question_type") or question_type)
        to = str(relay_packet.get("to") or to)
        run_id = str(relay_packet.get("run_id") or run_id or "") or None
        if isinstance(relay_packet.get("options"), list):
            options = list(relay_packet.get("options") or [])
        if isinstance(relay_packet.get("authority_needed"), Mapping):
            authority_needed = relay_packet.get("authority_needed")  # type: ignore[assignment]
        if isinstance(relay_packet.get("evidence_refs"), list):
            evidence_refs = list(relay_packet.get("evidence_refs") or [])
    if not invocation_id:
        return _blocked("agent_relay_create", "invocation_id_required")
    if not question:
        return _blocked("agent_relay_create", "question_required")
    path, invocation = _load_invocation(shell_root, invocation_id)
    if path is None or invocation is None:
        return _blocked("agent_relay_create", "agent_invocation_not_found")
    authority = dict(authority_needed or {})
    requires_operator = bool(authority.get("requires_operator")) or to == "operator"
    requested_change = authority.get("requested_authority_change")
    if requested_change:
        requested_text = _json_text(requested_change)
        if any(gate in requested_text for gate in HARD_GATES) and not requires_operator:
            requires_operator = True
            to = "operator"
    relay_id = f"relay_{_timestamp_slug()}_{_safe_slug(invocation_id)[:40]}"
    relay = {
        "schema_id": "ion.agent_relay_message.v1",
        "relay_id": relay_id,
        "invocation_id": invocation_id,
        "run_id": run_id,
        "from_agent": invocation.get("agent_role"),
        "to": "operator" if requires_operator else to,
        "question_type": question_type,
        "question": question,
        "options": list(options or []),
        "authority_needed": {
            "requires_operator": requires_operator,
            "requested_authority_change": requested_change,
        },
        "evidence_refs": list(evidence_refs or []),
        "created_at": _now(),
        "status": "WAITING",
        "response": None,
        "production_authority": False,
        "live_execution_authority": False,
    }
    relay_dir = _agent_invocation_dir(shell_root, invocation_id) / "relays"
    relay_dir.mkdir(parents=True, exist_ok=True)
    relay_path = relay_dir / f"{relay_id}.json"
    _write_json(relay_path, relay)
    status = "WAITING_FOR_OPERATOR" if requires_operator else "WAITING_FOR_CHATGPT"
    _update_invocation_status(shell_root, invocation_id, status)
    receipt_path = _write_agent_receipt(shell_root, invocation_id=invocation_id, event="relay_created", status="waiting", payload={"relay_path": _connector_rel(relay_path, shell_root), "to": relay["to"]})
    relay["receipt_path"] = receipt_path
    _write_json(relay_path, relay)
    return {
        "schema_id": "ion.agent_relay_create_result.v1",
        "ok": True,
        "relay_id": relay_id,
        "relay_path": _connector_rel(relay_path, shell_root),
        "status": status,
        "receipt_path": receipt_path,
        "production_authority": False,
        "live_execution_authority": False,
    }


def pending_agent_relays(root: str | Path | None = None, *, invocation_id: str | None = None, include_answered: bool = False) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    relays: list[dict[str, Any]] = []
    if invocation_id:
        relays.extend(_relays_for_invocation(shell_root, invocation_id, include_answered=include_answered))
    else:
        for path in _invocation_paths(shell_root):
            payload = _read_json(path) or {}
            inv_id = str(payload.get("invocation_id") or "")
            if inv_id:
                relays.extend(_relays_for_invocation(shell_root, inv_id, include_answered=include_answered))
    return {
        "schema_id": "ion.agent_relay_pending.v1",
        "ok": True,
        "relay_count": len(relays),
        "count": len(relays),
        "relays": relays,
        "relay_messages": relays,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _find_relay(root: Path, relay_id: str) -> tuple[Path | None, dict[str, Any] | None]:
    base = root / AGENT_INVOCATIONS_DIR
    if not base.exists():
        return None, None
    for path in base.glob("*/relays/*.json"):
        payload = _read_json(path) or {}
        if relay_id in {path.name, str(payload.get("relay_id") or "")}:
            return path, payload
    return None, None


def respond_agent_relay(root: str | Path | None, response_packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    relay_id = str(response_packet.get("relay_id") or "").strip()
    if not relay_id:
        return _blocked("agent_relay_respond", "relay_id_required")
    path, relay = _find_relay(shell_root, relay_id)
    if path is None or relay is None:
        return _blocked("agent_relay_respond", "relay_not_found")
    answered_by = str(response_packet.get("answered_by") or "chatgpt_browser")
    authority_delta = response_packet.get("authority_delta")
    requires_operator = bool((relay.get("authority_needed") or {}).get("requires_operator")) if isinstance(relay.get("authority_needed"), Mapping) else False
    if (authority_delta is not None or requires_operator) and answered_by != "operator":
        relay["status"] = "ESCALATED"
        relay["updated_at"] = _now()
        _write_json(path, relay)
        _update_invocation_status(shell_root, str(relay.get("invocation_id") or ""), "WAITING_FOR_OPERATOR")
        receipt = _write_agent_receipt(shell_root, invocation_id=str(relay.get("invocation_id") or "unknown"), event="relay_escalated", status="waiting_for_operator", payload={"relay_id": relay_id, "answered_by": answered_by})
        return {
            "schema_id": "ion.agent_relay_response_result.v1",
            "ok": False,
            "refusal_class": "OPERATOR_APPROVAL_REQUIRED",
            "finding": "operator_required_for_authority_delta_or_operator_relay",
            "relay_id": relay_id,
            "receipt_path": receipt,
            "production_authority": False,
            "live_execution_authority": False,
        }
    response = {
        "schema_id": "ion.agent_relay_response.v1",
        "relay_id": relay_id,
        "invocation_id": relay.get("invocation_id"),
        "answered_by": answered_by,
        "response": str(response_packet.get("response") or "").strip(),
        "authority_delta": authority_delta,
        "continue": response_packet.get("continue") is not False,
        "created_at": _now(),
        "production_authority": False,
        "live_execution_authority": False,
    }
    if not response["response"]:
        return _blocked("agent_relay_respond", "response_required")
    response_dir = path.parent.parent / "relay_responses"
    response_dir.mkdir(parents=True, exist_ok=True)
    response_path = response_dir / f"{relay_id}_response_{_timestamp_slug()}.json"
    _write_json(response_path, response)
    relay["status"] = "ANSWERED"
    relay["response"] = response
    relay["updated_at"] = _now()
    _write_json(path, relay)
    invocation_id = str(relay.get("invocation_id") or "")
    if response["continue"]:
        _update_invocation_status(shell_root, invocation_id, "QUEUED")
    receipt = _write_agent_receipt(shell_root, invocation_id=invocation_id, event="relay_answered", status="answered", payload={"relay_id": relay_id, "response_path": _connector_rel(response_path, shell_root), "continue": response["continue"]})
    return {
        "schema_id": "ion.agent_relay_response_result.v1",
        "ok": True,
        "relay_id": relay_id,
        "invocation_id": invocation_id,
        "response_path": _connector_rel(response_path, shell_root),
        "receipt_path": receipt,
        "continue": response["continue"],
        "status": "QUEUED" if response["continue"] else "ANSWERED_NO_CONTINUE",
        "production_authority": False,
        "live_execution_authority": False,
    }



def settle_agent_invocation(root: str | Path | None, settlement_packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    invocation_id = str(settlement_packet.get("invocation_id") or "").strip()
    if not invocation_id:
        return _blocked("agent_settle", "invocation_id_required")
    path, invocation = _load_invocation(shell_root, invocation_id)
    if path is None or invocation is None:
        return _blocked("agent_settle", "agent_invocation_not_found")

    raw_state = str(settlement_packet.get("terminal_state") or settlement_packet.get("state") or "").strip().lower()
    allowed = {"accepted", "blocked", "deferred", "rejected", "failed"}
    if raw_state not in allowed:
        return _blocked("agent_settle", "terminal_state_must_be_accepted_blocked_deferred_rejected_or_failed")

    evidence_refs = settlement_packet.get("evidence_refs") if isinstance(settlement_packet.get("evidence_refs"), list) else []
    proof_packet_path = str(settlement_packet.get("proof_packet_path") or "").strip()
    task_return_path = str(settlement_packet.get("task_return_path") or "").strip()
    if raw_state == "accepted" and not evidence_refs and not proof_packet_path and not task_return_path:
        receipt = _write_agent_receipt(
            shell_root,
            invocation_id=invocation_id,
            event="blocked_or_refused",
            status="accepted_settlement_requires_evidence",
            payload={"reason": "No proof/evidence/task return ref supplied for accepted settlement."},
        )
        return {
            "schema_id": "ion.agent_settlement_result.v1",
            "ok": False,
            "refusal_class": "PROOF_REQUIRED",
            "finding": "accepted_settlement_requires_evidence_ref",
            "receipt_path": receipt,
            "production_authority": False,
            "live_execution_authority": False,
        }

    now = _now()
    status = f"TERMINAL_{raw_state.upper()}"
    settlement_dir = _agent_invocation_dir(shell_root, invocation_id) / "settlements"
    settlement_dir.mkdir(parents=True, exist_ok=True)
    settlement_path = settlement_dir / f"{_timestamp_slug()}_{raw_state}.json"
    settlement_block = invocation.get("settlement") if isinstance(invocation.get("settlement"), Mapping) else {}
    settlement = {
        "schema_id": "ion.agent_invocation_settlement.v1",
        "invocation_id": invocation_id,
        "terminal_state": raw_state,
        "status": status,
        "settled_by": str(settlement_packet.get("settled_by") or "chatgpt_browser"),
        "settlement_target": str(settlement_packet.get("settlement_target") or settlement_block.get("settlement_target") or "chatgpt_browser"),
        "summary": str(settlement_packet.get("summary") or ""),
        "proof_packet_path": proof_packet_path or None,
        "task_return_path": task_return_path or None,
        "evidence_refs": list(evidence_refs),
        "blockers": settlement_packet.get("blockers") if isinstance(settlement_packet.get("blockers"), list) else [],
        "created_at": now,
        "production_authority": False,
        "live_execution_authority": False,
    }
    _write_json(settlement_path, settlement)
    settlement_rel = _connector_rel(settlement_path, shell_root)
    invocation["status"] = status
    invocation["terminal_state"] = raw_state
    invocation["settlement_path"] = settlement_rel
    invocation["updated_at"] = now
    receipt = _write_agent_receipt(
        shell_root,
        invocation_id=invocation_id,
        event="settlement_recorded",
        status=status,
        payload={"settlement_path": settlement_rel, "terminal_state": raw_state},
    )
    invocation.setdefault("receipt_paths", [])
    if isinstance(invocation["receipt_paths"], list):
        invocation["receipt_paths"].append(receipt)
    _write_json(path, invocation)
    _update_invocation_status(shell_root, invocation_id, status)
    return {
        "schema_id": "ion.agent_settlement_result.v1",
        "ok": True,
        "invocation_id": invocation_id,
        "terminal_state": raw_state,
        "status": status,
        "settlement_path": settlement_rel,
        "receipt_path": receipt,
        "production_authority": False,
        "live_execution_authority": False,
    }


def control_agent_invocation(root: str | Path | None, request: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    operation = str(request.get("operation") or "").strip()
    invocation_id = str(request.get("invocation_id") or "").strip()
    if not invocation_id:
        return _blocked("agent_control", "invocation_id_required")
    path, invocation = _load_invocation(shell_root, invocation_id)
    if path is None or invocation is None:
        return _blocked("agent_control", "agent_invocation_not_found")
    if operation == "cancel":
        result = cancel_agent_invocation(shell_root, invocation_id=invocation_id)
        if result.get("ok"):
            _write_agent_receipt(shell_root, invocation_id=invocation_id, event="blocked_or_refused", status="cancelled", payload={"operation": operation})
        return result
    if operation == "pause":
        _update_invocation_status(shell_root, invocation_id, "PAUSED")
        receipt = _write_agent_receipt(shell_root, invocation_id=invocation_id, event="agent_control", status="paused", payload={"operation": operation})
        return {"schema_id": SCHEMA_ID, "ok": True, "result": "AGENT_INVOCATION_PAUSED", "invocation_id": invocation_id, "receipt_path": receipt, "production_authority": False, "live_execution_authority": False}
    if operation == "resume":
        _update_invocation_status(shell_root, invocation_id, "QUEUED")
        receipt = _write_agent_receipt(shell_root, invocation_id=invocation_id, event="agent_control", status="resumed", payload={"operation": operation})
        return {"schema_id": SCHEMA_ID, "ok": True, "result": "AGENT_INVOCATION_RESUMED", "invocation_id": invocation_id, "receipt_path": receipt, "production_authority": False, "live_execution_authority": False}
    return _blocked("agent_control", "unsupported_control_operation")


def recent_agent_invocation_receipts(root: str | Path | None = None, *, limit: int = 20) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    base = shell_root / AGENT_INVOCATIONS_DIR
    rows: list[dict[str, Any]] = []
    if base.exists():
        for path in sorted(base.glob("*/receipts/*.json"), key=lambda item: item.stat().st_mtime, reverse=True)[: max(1, min(int(limit or 20), 50))]:
            payload = _read_json(path) or {}
            rows.append({
                "path": _connector_rel(path, shell_root),
                "receipt_id": payload.get("receipt_id"),
                "invocation_id": payload.get("invocation_id"),
                "event": payload.get("event"),
                "status": payload.get("status"),
                "created_at": payload.get("created_at"),
            })
    return {
        "schema_id": "ion.agent_invocation_recent_receipts.v1",
        "ok": True,
        "receipt_count": len(rows),
        "receipts": rows,
        "production_authority": False,
        "live_execution_authority": False,
    }


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
    normalized_timeout = _normalize_agent_timeout_seconds(timeout_seconds)
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
        timeout_seconds=normalized_timeout,
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
