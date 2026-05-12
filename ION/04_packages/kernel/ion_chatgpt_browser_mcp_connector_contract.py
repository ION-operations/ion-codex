"""V120 ChatGPT browser MCP connector contract.

This module defines the bounded tool contract for a future ChatGPT-facing ION
connector. It is dependency-free and does not expose arbitrary shell, arbitrary
file writes, deletion, git push, credentials, provider calls, or browser control.
"""
from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_carrier_onboarding_packet import build_carrier_onboarding_packet
from .ion_agent_invocation_broker import (
    agent_queue,
    agent_result,
    build_agent_broker_status,
    build_agent_spawn_plan,
    cancel_agent_invocation,
    invoke_agent,
    list_agents,
    swarm_step_once,
)
from .ion_codex_queue_runner import (
    DEFAULT_CODEX_TIMEOUT_SECONDS,
    MAX_CODEX_TIMEOUT_SECONDS,
    build_codex_queue_runner_status,
    process_codex_queue_once,
    reconcile_codex_queue_runner_state,
)
from .ion_cockpit_view_model import build_cockpit_view_model
from .ion_context_proof_gate import evaluate_context_proof_return
from .ion_receipt_hydration_mapper import build_receipt_hydration_view_model
from .ion_status import build_ion_status
from .ion_template_action_gate import evaluate_template_action_proof

VERSION_LINE = "V120_CHATGPT_BROWSER_MCP_CONNECTOR_AND_CORRECT_CARRIER_ONBOARDING"
SCHEMA_ID = "ion.chatgpt_browser_mcp_connector_contract.v1"
CONNECTOR_ID = "ION_CHATGPT_BROWSER_CONNECTOR"
OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_V120.json")
CONNECTOR_STATE_DIR = Path("ION/05_context/current/chatgpt_connector")
CODEX_WORK_QUEUE_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json")
ACTIVE_CARRIER_MESSAGE_QUEUE_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json")

PROTOCOL_RELATIVE_PATH = Path("ION/02_architecture/ION_CHATGPT_BROWSER_MCP_CONNECTOR_PROTOCOL.md")
POLICY_RELATIVE_PATH = Path("ION/03_registry/ion_chatgpt_browser_mcp_tool_policy.yaml")
SCHEMA_RELATIVE_PATH = Path("ION/03_registry/ion_chatgpt_browser_mcp_connector.schema.json")
FULL_CARRIER_PROTOCOL_RELATIVE_PATH = Path("ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md")
FULL_CARRIER_TOOL_REGISTRY_RELATIVE_PATH = Path("ION/03_registry/mcp_full_carrier_tool_registry.yaml")
FULL_CARRIER_CAPABILITY_REGISTRY_RELATIVE_PATH = Path("ION/03_registry/carrier_capability_registry.yaml")
INTEGRATION_DIR_RELATIVE_PATH = Path("ION/09_integrations/mcp/chatgpt_connector")
SETUP_RELATIVE_PATH = Path("ION/docs/setup/CHATGPT_BROWSER_MCP_CONNECTOR_SETUP_V120.md")
WRAPPER_RELATIVE_PATH = INTEGRATION_DIR_RELATIVE_PATH / "ion_chatgpt_browser_connector.py"
MANIFEST_RELATIVE_PATH = INTEGRATION_DIR_RELATIVE_PATH / "connector_manifest.json"
MAX_TEXT_PUT_BYTES = 512 * 1024
MAX_UPLOAD_CHUNK_BYTES = 512 * 1024
MAX_UPLOAD_BYTES = 4 * 1024 * 1024
MAX_READ_BYTES = 256 * 1024
MAX_SEARCH_FILE_BYTES = 128 * 1024
MAX_SEARCH_FILES = 500
MIN_COMPLEX_WORKLOAD_TIMEOUT_SECONDS = 900
BASE_RETURN_CONTRACT_SECTIONS = (
    "### CONTEXT PROOF",
    "### TEMPLATE ACTION PROOF",
    "### VALIDATION",
    "### RESULT",
)
WORKLOAD_DIFF_SECTION = "### WORKLOAD DIFF"
RETURN_TEMPLATE_REQUIRED_SECTIONS = (
    "### CONTEXT PROOF",
    "### TEMPLATE ACTION PROOF",
    "### VALIDATION",
    "### RESULT",
    "### WORKLOAD DIFF",
    "### BLOCKERS",
    "### RECOMMENDED NEXT PACKET",
)
WORKLOAD_POLICY_HINTS = (
    "agent",
    "cartograph",
    "probe",
    "proof",
    "design",
)
ARTIFACT_TARGET_ROOTS = (
    Path("ION/05_context/current/chatgpt_connector/artifacts"),
    Path("ION/05_context/inbox"),
    Path("ION/05_context/signals"),
)
DEFAULT_SEARCH_ROOTS = (
    Path("ION/02_architecture"),
    Path("ION/03_registry"),
    Path("ION/04_packages/kernel"),
    Path("ION/05_context/current"),
    Path("ION/07_templates"),
    Path("ION/09_integrations/mcp"),
    Path("ION/tests"),
)
FORBIDDEN_TRANSFER_PATH_PARTS = {
    ".env",
    "credentials",
    "credential",
    "secrets",
    "secret",
    "vault",
}
FORBIDDEN_READ_PATH_PARTS = FORBIDDEN_TRANSFER_PATH_PARTS | {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
}

STATUS_READ_TOOLS = {
    "ion_status",
    "ion_current_operating_packet",
    "ion_carrier_onboarding_packet",
    "ion_read_active_packet",
    "ion_context_plan",
    "ion_cockpit_view",
    "ion_artifact_manifest",
    "ion_receipt_search",
    "ion_git_status_summary",
    "ion_codex_work_queue",
    "ion_carrier_message_poll",
    "ion_file_read",
    "ion_file_search",
    "ion_tree_list",
    "ion_registry_read",
    "ion_template_read",
    "ion_context_compile",
    "ion_receipt_hydrate",
    "ion_tool_manifest",
    "ion_daemon_status",
    "ion_codex_queue_autorun_status",
    "ion_codex_worker_live_status",
    "ion_agent_list",
    "ion_agent_status",
    "ion_agent_result",
    "ion_agent_queue",
    "ion_agent_spawn_plan",
    "ion_swarm_status",
    "ion_codex_capsule_chat_status",
    "ion_codex_capsule_message_poll",
}

BOUNDED_QUEUE_RECEIPT_TOOLS = {
    "ion_queue_operator_message",
    "ion_request_codex_work_packet",
    "ion_submit_task_return",
    "ion_record_chatgpt_decision",
    "ion_create_containment_receipt",
    "ion_file_put_text",
    "ion_artifact_upload_init",
    "ion_artifact_upload_chunk",
    "ion_artifact_upload_commit",
    "ion_carrier_message_send",
    "ion_carrier_message_ack",
    "ion_codex_queue_process_once",
    "ion_agent_invoke",
    "ion_agent_cancel",
    "ion_swarm_step_once",
    "ion_codex_runner_reconcile",
    "ion_codex_capsule_message_send",
    "ion_codex_capsule_sync_to_queue",
}

FORBIDDEN_CAPABILITIES = {
    "arbitrary_shell",
    "arbitrary_file_write",
    "direct_delete",
    "git_push",
    "credential_access",
    "browser_computer_control",
    "provider_api_calls",
    "unbounded_local_filesystem_access",
    "production_deployment",
    "direct_accept_unproofed_worker_output",
}

ACTIVE_PACKET_ALLOWLIST = {
    "hook": "ION/05_context/current/ACTIVE_CURSOR_HOOK_STATE.json",
    "work": "ION/05_context/current/ACTIVE_WORK_PACKET.json",
    "spawn_plan": "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
    "carrier_turn": "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json",
    "task_return_ledger": "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
    "steward_queue": "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
    "operator_queue": "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
    "human_gates": "ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json",
    "cockpit": "ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json",
    "context_window": "ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json",
    "front_door": "ION/05_context/current/ACTIVE_FRONT_DOOR_TEAM_PLAN.json",
    "lane_timeline": "ION/05_context/current/ACTIVE_LANE_TIMELINE_VIEW_MODEL.json",
    "receipt_hydration": "ION/05_context/current/ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json",
    "runtime_debug": "ION/05_context/current/ACTIVE_RUNTIME_DEBUG_OVERLAY.json",
    "current_operating_packet": "ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md",
    "carrier_onboarding": "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json",
    "chatgpt_codex_work_queue": "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json",
    "carrier_messages": "ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json",
    "chatgpt_tunnel": "ION/05_context/current/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json",
    "chatgpt_http_preview": "ION/05_context/current/CHATGPT_BROWSER_HTTP_MCP_PREVIEW_V121.json",
    "chatgpt_connector_contract": "ION/05_context/current/CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_V120.json",
    "codex_queue_runner_state": "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json",
    "agent_invocation_broker_state": "ION/05_context/current/chatgpt_connector/runtime/agent_invocation_broker_state.json",
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_connector_root(root: str | Path | None = None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    return resolve_shell_root_from_ion_root(root)


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sanitize_required_context_reads(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    reads: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in value:
        if isinstance(item, Mapping):
            path = str(item.get("path") or "").strip()
            kind = str(item.get("kind") or "file").strip() or "file"
            required = bool(item.get("required", True))
        else:
            path = str(item or "").strip()
            kind = "file"
            required = True
        if not path or path in seen or path.startswith("/") or ".." in Path(path).parts:
            continue
        seen.add(path)
        reads.append({"kind": kind, "path": path, "required": required})
    return reads[:64]


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:80] or "chatgpt_packet"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_rel_path(root: Path, value: str) -> Path:
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("path must be repo-relative and may not escape the ION root")
    candidate = (root / rel).resolve()
    candidate.relative_to(root)
    return candidate


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _validate_transfer_target(root: Path, value: str) -> tuple[Path | None, str | None]:
    if not value.strip():
        return None, "target_path_required"
    try:
        target = _safe_rel_path(root, value)
    except (ValueError, RuntimeError):
        return None, "target_path_must_be_repo_relative_without_escape"
    rel_parts = [part.lower() for part in target.relative_to(root).parts]
    if ".git" in rel_parts or any(part in FORBIDDEN_TRANSFER_PATH_PARTS for part in rel_parts):
        return None, "target_path_forbidden_by_transfer_policy"
    allowed_roots = [(root / rel).resolve() for rel in ARTIFACT_TARGET_ROOTS]
    if not any(_is_under(target, allowed) for allowed in allowed_roots):
        return None, "target_path_not_in_artifact_transfer_roots"
    if target.name in {"", ".", ".."}:
        return None, "target_filename_required"
    return target, None


def _validate_read_path(
    root: Path,
    value: str,
    *,
    allowed_roots: tuple[Path, ...] | None = None,
) -> tuple[Path | None, str | None]:
    if not value.strip():
        return None, "path_required"
    try:
        target = _safe_rel_path(root, value)
    except (ValueError, RuntimeError):
        return None, "path_must_be_repo_relative_without_escape"
    rel_parts = [part.lower() for part in target.relative_to(root).parts]
    if any(part in FORBIDDEN_READ_PATH_PARTS for part in rel_parts):
        return None, "path_forbidden_by_read_policy"
    if allowed_roots:
        resolved_roots = [(root / rel).resolve() for rel in allowed_roots]
        if not any(_is_under(target, allowed) for allowed in resolved_roots):
            return None, "path_not_in_tool_read_roots"
    return target, None


def _connector_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _extract_yaml_list(text: str, key: str) -> list[str]:
    values: list[str] = []
    in_block = False
    prefix = f"{key}:"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == prefix:
            in_block = True
            continue
        if in_block:
            if stripped.startswith("- "):
                values.append(stripped[2:].strip().strip("\"'"))
                continue
            if stripped and not line.startswith(" ") and not line.startswith("\t"):
                break
    return values


def _read_policy(root: Path) -> dict[str, list[str]]:
    policy_path = root / POLICY_RELATIVE_PATH
    text = _read_text(policy_path) if policy_path.exists() else ""
    return {
        "allowed_status_read_tools": _extract_yaml_list(text, "allowed_status_read_tools"),
        "allowed_bounded_queue_receipt_tools": _extract_yaml_list(text, "allowed_bounded_queue_receipt_tools"),
        "forbidden_tools": _extract_yaml_list(text, "forbidden_tools"),
        "required_task_return_sections": _extract_yaml_list(text, "required_task_return_sections"),
        "bounded_write_roots": _extract_yaml_list(text, "bounded_write_roots"),
    }


def tool_descriptors() -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    for name in sorted(STATUS_READ_TOOLS):
        tools.append({
            "name": name,
            "family": "status_read",
            "mutates_active_state": False,
            "requires_context_proof": False,
            "requires_template_action_proof": False,
        })
    for name in sorted(BOUNDED_QUEUE_RECEIPT_TOOLS):
        tools.append({
            "name": name,
            "family": "bounded_queue_receipt",
            "mutates_active_state": True,
            "writes_bounded_packet_only": True,
            "requires_context_proof": name == "ion_submit_task_return",
            "requires_template_action_proof": name == "ion_submit_task_return",
        })
    return tools


def _ok(name: str, data: Any, *, mutates_active_state: bool = False) -> dict[str, Any]:
    return {
        "schema_id": "ion.chatgpt_browser_connector_tool_result.v1",
        "tool": name,
        "ok": True,
        "mutates_active_state": mutates_active_state,
        "data": data,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _blocked(name: str, finding: str, data: Any | None = None) -> dict[str, Any]:
    return {
        "schema_id": "ion.chatgpt_browser_connector_tool_result.v1",
        "tool": name,
        "ok": False,
        "finding": finding,
        "data": data,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _latest_matching(root: Path, pattern: str) -> Path | None:
    candidates = sorted((root / "ION/05_context/current").glob(pattern))
    return candidates[-1] if candidates else None


def _packet_read(
    root: Path,
    packet: str,
    *,
    max_bytes: int | None = None,
    tool_name: str = "ion_read_active_packet",
) -> dict[str, Any]:
    rel = ACTIVE_PACKET_ALLOWLIST.get(packet)
    if not rel:
        return _blocked(tool_name, "packet_not_allowlisted", {"allowed": sorted(ACTIVE_PACKET_ALLOWLIST)})
    path = root / rel
    if not path.exists():
        return _blocked(tool_name, "packet_missing", {"path": rel})
    if max_bytes is not None:
        bounded_max = min(max(int(max_bytes), 1), MAX_READ_BYTES)
        data = path.read_bytes()
        shown = data[:bounded_max].decode("utf-8", errors="replace")
        return _ok(
            tool_name,
            {
                "path": rel,
                "content_preview": shown,
                "content_truncated": len(data) > bounded_max,
                "content_bytes": len(data),
                "max_bytes": bounded_max,
            },
        )
    if path.suffix == ".json":
        data: Any = _read_json(path)
    else:
        data = {"text": _read_text(path)}
    return _ok(tool_name, {"path": rel, "content": data})


def _artifact_manifest(root: Path) -> dict[str, Any]:
    safe = _latest_matching(root, "SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json")
    trunk = _latest_matching(root, "TRUNK_PRESERVATION_REPORT_V*.json")
    safe_payload = _read_json(safe) if safe else None
    trunk_payload = _read_json(trunk) if trunk else None
    return {
        "safe_full_project_package_result_path": str(safe.relative_to(root)) if safe else None,
        "trunk_preservation_report_path": str(trunk.relative_to(root)) if trunk else None,
        "zip_path": safe_payload.get("zip_path") if safe_payload else None,
        "zip_sha256": safe_payload.get("zip_sha256") if safe_payload else None,
        "packaging_verdict": trunk_payload.get("packaging_verdict") if trunk_payload else None,
        "unexpected_removed_files": trunk_payload.get("unexpected_removed_files") if trunk_payload else None,
        "protected_removed_files": trunk_payload.get("protected_removed_files") if trunk_payload else None,
    }


def _receipt_search(root: Path, query: str, limit: int) -> dict[str, Any]:
    normalized = query.lower().strip()
    matches: list[dict[str, Any]] = []
    for path in sorted((root / "ION/05_context/current").rglob("*.json")):
        rel = path.relative_to(root).as_posix()
        if len(matches) >= limit:
            break
        if "receipt" not in rel.lower() and "return" not in rel.lower():
            continue
        text = _read_text(path)
        if normalized and normalized not in text.lower() and normalized not in rel.lower():
            continue
        matches.append({"path": rel, "sha256": _sha256_text(text), "bytes": len(text.encode("utf-8"))})
    return {"query": query, "matches": matches, "limit": limit}


def _git_status_summary(root: Path) -> dict[str, Any]:
    git = root / ".git"
    if not git.exists():
        return {"git_present": False, "working_tree_scan": "not_available_without_git_metadata"}
    head_path = git / "HEAD"
    head = _read_text(head_path).strip() if head_path.exists() else None
    ref = None
    commit = None
    if head and head.startswith("ref: "):
        ref = head[5:]
        ref_path = git / ref
        commit = _read_text(ref_path).strip() if ref_path.exists() else None
    elif head:
        commit = head
    return {
        "git_present": True,
        "head": head,
        "ref": ref,
        "commit": commit,
        "working_tree_scan": "not_performed_no_shell_or_git_subprocess",
    }


def _bounded_file_read(
    root: Path,
    args: Mapping[str, Any],
    *,
    tool_name: str = "ion_file_read",
    allowed_roots: tuple[Path, ...] | None = None,
) -> dict[str, Any]:
    rel_value = str(args.get("path") or args.get("target_path") or "").strip()
    target, finding = _validate_read_path(root, rel_value, allowed_roots=allowed_roots)
    if finding or target is None:
        return _blocked(tool_name, finding or "invalid_path")
    if not target.exists():
        return _blocked(tool_name, "path_missing", {"path": rel_value})
    if not target.is_file():
        return _blocked(tool_name, "path_not_file", {"path": _connector_rel(target, root)})
    max_bytes = min(max(int(args.get("max_bytes") or 64 * 1024), 1), MAX_READ_BYTES)
    data = target.read_bytes()
    shown = data[:max_bytes]
    text = shown.decode("utf-8", errors="replace")
    return _ok(tool_name, {
        "path": _connector_rel(target, root),
        "bytes": len(data),
        "sha256": _sha256_bytes(data),
        "text": text,
        "truncated": len(data) > len(shown),
        "max_bytes": max_bytes,
        "production_authority": False,
        "live_execution_authority": False,
    })


def _tree_list(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    rel_value = str(args.get("path") or ".").strip() or "."
    base, finding = _validate_read_path(root, rel_value)
    if finding or base is None:
        return _blocked("ion_tree_list", finding or "invalid_path")
    if not base.exists():
        return _blocked("ion_tree_list", "path_missing", {"path": rel_value})
    max_depth = min(max(int(args.get("max_depth") or 2), 0), 6)
    limit = min(max(int(args.get("limit") or 200), 1), 1000)
    entries: list[dict[str, Any]] = []
    start_depth = len(base.relative_to(root).parts)
    paths = [base] if base.is_file() else sorted(base.rglob("*"), key=lambda item: item.relative_to(root).as_posix())
    for path in paths:
        rel_parts = [part.lower() for part in path.relative_to(root).parts]
        if any(part in FORBIDDEN_READ_PATH_PARTS for part in rel_parts):
            continue
        depth = len(path.relative_to(root).parts) - start_depth
        if depth > max_depth:
            continue
        stat = path.stat()
        entries.append({
            "path": _connector_rel(path, root),
            "kind": "dir" if path.is_dir() else "file",
            "bytes": stat.st_size if path.is_file() else None,
        })
        if len(entries) >= limit:
            break
    return _ok("ion_tree_list", {
        "root": _connector_rel(base, root),
        "max_depth": max_depth,
        "limit": limit,
        "entry_count": len(entries),
        "entries": entries,
        "truncated": len(entries) >= limit,
    })


def _file_search(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    query = str(args.get("query") or "").strip()
    if not query:
        return _blocked("ion_file_search", "query_required")
    limit = min(max(int(args.get("limit") or 25), 1), 100)
    max_files = min(max(int(args.get("max_files") or MAX_SEARCH_FILES), 1), MAX_SEARCH_FILES)
    raw_roots = args.get("roots")
    if isinstance(raw_roots, list) and raw_roots:
        search_roots: list[Path] = []
        for value in raw_roots[:10]:
            path, finding = _validate_read_path(root, str(value))
            if finding or path is None:
                continue
            search_roots.append(path)
    else:
        search_roots = [(root / rel).resolve() for rel in DEFAULT_SEARCH_ROOTS if (root / rel).exists()]
    normalized = query.lower()
    matches: list[dict[str, Any]] = []
    scanned = 0
    seen: set[str] = set()
    for base in search_roots:
        candidates = [base] if base.is_file() else sorted(base.rglob("*"), key=lambda item: item.relative_to(root).as_posix())
        for path in candidates:
            if scanned >= max_files or len(matches) >= limit:
                break
            if not path.is_file():
                continue
            rel = _connector_rel(path, root)
            if rel in seen:
                continue
            seen.add(rel)
            rel_parts = [part.lower() for part in path.relative_to(root).parts]
            if any(part in FORBIDDEN_READ_PATH_PARTS for part in rel_parts):
                continue
            scanned += 1
            try:
                data = path.read_bytes()
            except OSError:
                continue
            name_hit = normalized in rel.lower()
            text_hit = False
            line_hits: list[dict[str, Any]] = []
            if len(data) <= MAX_SEARCH_FILE_BYTES:
                text = data.decode("utf-8", errors="ignore")
                for number, line in enumerate(text.splitlines(), start=1):
                    if normalized in line.lower():
                        text_hit = True
                        line_hits.append({"line": number, "text": line[:240]})
                        if len(line_hits) >= 3:
                            break
            if name_hit or text_hit:
                matches.append({
                    "path": rel,
                    "sha256": _sha256_bytes(data),
                    "bytes": len(data),
                    "name_hit": name_hit,
                    "line_hits": line_hits,
                })
    return _ok("ion_file_search", {
        "query": query,
        "matches": matches,
        "match_count": len(matches),
        "scanned_files": scanned,
        "limit": limit,
        "max_files": max_files,
    })


def _registry_read(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    raw = str(args.get("path") or args.get("name") or "").strip()
    if raw and "/" not in raw:
        raw = f"ION/03_registry/{raw}"
    return _bounded_file_read(root, {"path": raw, "max_bytes": args.get("max_bytes")}, tool_name="ion_registry_read", allowed_roots=(Path("ION/03_registry"),))


def _template_read(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    raw = str(args.get("path") or args.get("name") or "").strip()
    if raw and "/" not in raw:
        raw = f"ION/07_templates/{raw}"
    return _bounded_file_read(root, {"path": raw, "max_bytes": args.get("max_bytes")}, tool_name="ion_template_read", allowed_roots=(Path("ION/07_templates"),))


def _context_compile(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    profile = str(args.get("profile") or "full_carrier_mcp_parity").strip()
    include_excerpts = bool(args.get("include_excerpts"))
    surface_paths = [
        "ION/REPO_AUTHORITY.md",
        "ION/02_architecture/ION_MOUNT_CONTRACT.md",
        "ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md",
        "ION/02_architecture/ION_CARRIER_TO_CARRIER_COMMUNICATION_PROTOCOL.md",
        "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
        "ION/03_registry/carrier_capability_registry.yaml",
        "ION/03_registry/mcp_full_carrier_tool_registry.yaml",
        "ION/05_context/current/CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_V120.json",
        "ION/05_context/current/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json",
        "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json",
        "ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json",
    ]
    surfaces: list[dict[str, Any]] = []
    for rel in surface_paths:
        path, finding = _validate_read_path(root, rel)
        if finding or path is None or not path.exists() or not path.is_file():
            surfaces.append({"path": rel, "exists": False, "finding": finding or "path_missing"})
            continue
        data = path.read_bytes()
        item: dict[str, Any] = {
            "path": rel,
            "exists": True,
            "bytes": len(data),
            "sha256": _sha256_bytes(data),
        }
        if include_excerpts:
            item["excerpt"] = data[:2400].decode("utf-8", errors="replace")
            item["excerpt_truncated"] = len(data) > 2400
        surfaces.append(item)
    return _ok("ion_context_compile", {
        "schema_id": "ion.chatgpt_browser_connector_context_compile.v1",
        "profile": profile,
        "surface_count": len(surfaces),
        "surfaces": surfaces,
        "production_authority": False,
        "live_execution_authority": False,
    })


def _receipt_hydrate(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    model = build_receipt_hydration_view_model(root)
    limit = min(max(int(args.get("limit") or 25), 1), 100)
    records = list(model.get("records") or [])[:limit]
    return _ok("ion_receipt_hydrate", {
        "schema_id": model.get("schema_id"),
        "generated_at": model.get("generated_at"),
        "source_paths": model.get("source_paths"),
        "receipt_count": model.get("receipt_count"),
        "unresolved_count": model.get("unresolved_count"),
        "hydration_conflict_count": model.get("hydration_conflict_count"),
        "records": records,
        "limit": limit,
    })


def _tool_manifest(root: Path) -> dict[str, Any]:
    contract = audit_chatgpt_browser_mcp_connector_contract(root)
    return {
        "schema_id": "ion.chatgpt_browser_connector_tool_manifest.v1",
        "connector_id": CONNECTOR_ID,
        "tool_count": len(contract.get("allowed_tools") or []),
        "allowed_tools": contract.get("allowed_tools"),
        "status_read_tools": contract.get("status_read_tools"),
        "bounded_queue_receipt_tools": contract.get("bounded_queue_receipt_tools"),
        "tool_descriptors": contract.get("tool_descriptors"),
        "source_paths": contract.get("source_paths"),
        "forbidden_tools": contract.get("forbidden_tools"),
        "production_authority": False,
        "live_execution_authority": False,
    }


def _write_connector_packet(root: Path, subdir: str, prefix: str, payload: Mapping[str, Any]) -> Path:
    timestamp = _now()
    packet_id = f"{timestamp.replace(':', '').replace('+', 'Z')}_{_safe_slug(prefix)}"
    path = root / CONNECTOR_STATE_DIR / subdir / f"{packet_id}.json"
    counter = 1
    while path.exists():
        path = root / CONNECTOR_STATE_DIR / subdir / f"{packet_id}_{counter}.json"
        counter += 1
    value = dict(payload)
    value.setdefault("schema_id", f"ion.chatgpt_browser_connector_{subdir.rstrip('s')}.v1")
    value.setdefault("created_at", timestamp)
    value.setdefault("connector_id", CONNECTOR_ID)
    value.setdefault("production_authority", False)
    value.setdefault("live_execution_authority", False)
    _write_json(path, value)
    return path


def _artifact_receipt(root: Path, prefix: str, payload: Mapping[str, Any]) -> Path:
    return _write_connector_packet(root, "artifact_receipts", prefix, payload)


def _put_text_artifact(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    target_path = str(args.get("target_path") or "")
    target, finding = _validate_transfer_target(root, target_path)
    if finding or target is None:
        return _blocked("ion_file_put_text", finding or "invalid_target_path")
    text = str(args.get("text") or "")
    data = text.encode("utf-8")
    if len(data) > MAX_TEXT_PUT_BYTES:
        return _blocked("ion_file_put_text", "text_payload_exceeds_connector_limit")
    expected_sha = str(args.get("expected_sha256") or "").strip()
    actual_sha = _sha256_bytes(data)
    if expected_sha and expected_sha != actual_sha:
        return _blocked("ion_file_put_text", "sha256_mismatch", {"expected_sha256": expected_sha, "actual_sha256": actual_sha})
    if target.exists():
        receipt = _artifact_receipt(root, target.name, {
            "schema_id": "ion.chatgpt_browser_connector_artifact_receipt.v1",
            "action": "ion_file_put_text_blocked_existing_target",
            "target_path": _connector_rel(target, root),
            "target_sha256": _sha256_file(target) if target.is_file() else None,
            "overwrite_requested": bool(args.get("overwrite")),
            "status": "BLOCKED_NO_SILENT_LOSS_REQUIRES_LIFECYCLE_RECEIPT",
        })
        return _blocked("ion_file_put_text", "target_exists_requires_lifecycle_receipt", {"receipt_path": _connector_rel(receipt, root)})
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    receipt = _artifact_receipt(root, target.name, {
        "schema_id": "ion.chatgpt_browser_connector_artifact_receipt.v1",
        "action": "ion_file_put_text",
        "target_path": _connector_rel(target, root),
        "bytes": len(data),
        "sha256": actual_sha,
        "status": "ARTIFACT_WRITTEN",
    })
    return _ok("ion_file_put_text", {
        "target_path": _connector_rel(target, root),
        "bytes": len(data),
        "sha256": actual_sha,
        "receipt_path": _connector_rel(receipt, root),
    }, mutates_active_state=True)


def _upload_session_path(root: Path, upload_id: str) -> Path:
    if not re.fullmatch(r"upload_[0-9TZ-]+_[a-z0-9_]+", upload_id):
        raise ValueError("invalid_upload_id")
    return root / CONNECTOR_STATE_DIR / "artifact_uploads" / f"{upload_id}.json"


def _artifact_upload_init(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    artifact_name = str(args.get("artifact_name") or "").strip()
    if not artifact_name:
        return _blocked("ion_artifact_upload_init", "artifact_name_required")
    target_path = str(args.get("target_path") or (ARTIFACT_TARGET_ROOTS[0] / artifact_name).as_posix())
    target, finding = _validate_transfer_target(root, target_path)
    if finding or target is None:
        return _blocked("ion_artifact_upload_init", finding or "invalid_target_path")
    if target.exists():
        return _blocked("ion_artifact_upload_init", "target_exists_requires_lifecycle_receipt")
    total_bytes = args.get("total_bytes")
    if total_bytes is not None and int(total_bytes) > MAX_UPLOAD_BYTES:
        return _blocked("ion_artifact_upload_init", "declared_upload_exceeds_connector_limit")
    now = _now()
    upload_id = f"upload_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(artifact_name)}"
    session = {
        "schema_id": "ion.chatgpt_browser_connector_artifact_upload_session.v1",
        "upload_id": upload_id,
        "artifact_name": artifact_name,
        "target_path": _connector_rel(target, root),
        "expected_sha256": str(args.get("expected_sha256") or "").strip() or None,
        "total_bytes": total_bytes,
        "mime_type": str(args.get("mime_type") or "application/octet-stream"),
        "status": "OPEN",
        "created_at": now,
        "updated_at": now,
        "chunks": {},
        "production_authority": False,
        "live_execution_authority": False,
    }
    path = _upload_session_path(root, upload_id)
    _write_json(path, session)
    return _ok("ion_artifact_upload_init", {
        "upload_id": upload_id,
        "session_path": _connector_rel(path, root),
        "target_path": _connector_rel(target, root),
        "max_chunk_bytes": MAX_UPLOAD_CHUNK_BYTES,
        "max_upload_bytes": MAX_UPLOAD_BYTES,
    }, mutates_active_state=True)


def _load_upload_session(root: Path, upload_id: str) -> tuple[Path | None, dict[str, Any] | None, str | None]:
    try:
        path = _upload_session_path(root, upload_id)
    except ValueError:
        return None, None, "invalid_upload_id"
    if not path.exists():
        return None, None, "upload_session_missing"
    return path, _load_json_file(path), None


def _artifact_upload_chunk(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    upload_id = str(args.get("upload_id") or "").strip()
    path, session, finding = _load_upload_session(root, upload_id)
    if finding or path is None or session is None:
        return _blocked("ion_artifact_upload_chunk", finding or "upload_session_missing")
    if session.get("status") != "OPEN":
        return _blocked("ion_artifact_upload_chunk", "upload_session_not_open")
    chunk_index = int(args.get("chunk_index"))
    if chunk_index < 0:
        return _blocked("ion_artifact_upload_chunk", "chunk_index_must_be_non_negative")
    try:
        data = base64.b64decode(str(args.get("data_base64") or ""), validate=True)
    except (binascii.Error, ValueError):
        return _blocked("ion_artifact_upload_chunk", "invalid_base64_chunk")
    if len(data) > MAX_UPLOAD_CHUNK_BYTES:
        return _blocked("ion_artifact_upload_chunk", "chunk_exceeds_connector_limit")
    expected = str(args.get("chunk_sha256") or "").strip()
    actual = _sha256_bytes(data)
    if expected and expected != actual:
        return _blocked("ion_artifact_upload_chunk", "chunk_sha256_mismatch", {"expected_sha256": expected, "actual_sha256": actual})
    chunk_dir = root / CONNECTOR_STATE_DIR / "artifact_uploads" / "chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    chunk_path = chunk_dir / f"{upload_id}_{chunk_index:08d}.chunk"
    if chunk_path.exists():
        return _blocked("ion_artifact_upload_chunk", "chunk_index_already_received")
    chunk_path.write_bytes(data)
    chunks = dict(session.get("chunks") or {})
    chunks[str(chunk_index)] = {"path": _connector_rel(chunk_path, root), "bytes": len(data), "sha256": actual}
    session["chunks"] = chunks
    session["updated_at"] = _now()
    _write_json(path, session)
    return _ok("ion_artifact_upload_chunk", {
        "upload_id": upload_id,
        "chunk_index": chunk_index,
        "bytes": len(data),
        "sha256": actual,
    }, mutates_active_state=True)


def _artifact_upload_commit(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    upload_id = str(args.get("upload_id") or "").strip()
    path, session, finding = _load_upload_session(root, upload_id)
    if finding or path is None or session is None:
        return _blocked("ion_artifact_upload_commit", finding or "upload_session_missing")
    if session.get("status") != "OPEN":
        return _blocked("ion_artifact_upload_commit", "upload_session_not_open")
    target, target_finding = _validate_transfer_target(root, str(session.get("target_path") or ""))
    if target_finding or target is None:
        return _blocked("ion_artifact_upload_commit", target_finding or "invalid_target_path")
    if target.exists():
        receipt = _artifact_receipt(root, target.name, {
            "schema_id": "ion.chatgpt_browser_connector_artifact_receipt.v1",
            "action": "ion_artifact_upload_commit_blocked_existing_target",
            "upload_id": upload_id,
            "target_path": _connector_rel(target, root),
            "target_sha256": _sha256_file(target) if target.is_file() else None,
            "status": "BLOCKED_NO_SILENT_LOSS_REQUIRES_LIFECYCLE_RECEIPT",
        })
        return _blocked("ion_artifact_upload_commit", "target_exists_requires_lifecycle_receipt", {"receipt_path": _connector_rel(receipt, root)})
    chunks = session.get("chunks") or {}
    if not chunks:
        return _blocked("ion_artifact_upload_commit", "no_chunks_received")
    ordered_indices = sorted(int(index) for index in chunks)
    if ordered_indices != list(range(0, max(ordered_indices) + 1)):
        return _blocked("ion_artifact_upload_commit", "missing_chunk_index")
    assembled = bytearray()
    for index in ordered_indices:
        chunk_meta = chunks[str(index)]
        chunk_path = _safe_rel_path(root, str(chunk_meta.get("path") or ""))
        data = chunk_path.read_bytes()
        if _sha256_bytes(data) != chunk_meta.get("sha256"):
            return _blocked("ion_artifact_upload_commit", "stored_chunk_sha256_mismatch", {"chunk_index": index})
        assembled.extend(data)
        if len(assembled) > MAX_UPLOAD_BYTES:
            return _blocked("ion_artifact_upload_commit", "assembled_upload_exceeds_connector_limit")
    data = bytes(assembled)
    actual_sha = _sha256_bytes(data)
    expected_sha = str(session.get("expected_sha256") or "").strip()
    if expected_sha and expected_sha != actual_sha:
        return _blocked("ion_artifact_upload_commit", "sha256_mismatch", {"expected_sha256": expected_sha, "actual_sha256": actual_sha})
    declared_total = session.get("total_bytes")
    if declared_total is not None and int(declared_total) != len(data):
        return _blocked("ion_artifact_upload_commit", "declared_total_bytes_mismatch", {"declared": declared_total, "actual": len(data)})
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    session["status"] = "COMMITTED"
    session["committed_at"] = _now()
    session["target_sha256"] = actual_sha
    session["target_bytes"] = len(data)
    _write_json(path, session)
    receipt = _artifact_receipt(root, target.name, {
        "schema_id": "ion.chatgpt_browser_connector_artifact_receipt.v1",
        "action": "ion_artifact_upload_commit",
        "upload_id": upload_id,
        "target_path": _connector_rel(target, root),
        "bytes": len(data),
        "sha256": actual_sha,
        "chunk_count": len(ordered_indices),
        "status": "ARTIFACT_COMMITTED",
    })
    return _ok("ion_artifact_upload_commit", {
        "upload_id": upload_id,
        "target_path": _connector_rel(target, root),
        "bytes": len(data),
        "sha256": actual_sha,
        "receipt_path": _connector_rel(receipt, root),
    }, mutates_active_state=True)


def _carrier_message_queue(root: Path) -> dict[str, Any]:
    path = root / ACTIVE_CARRIER_MESSAGE_QUEUE_RELATIVE_PATH
    return _read_json(path) or {
        "schema_id": "ion.carrier_message_queue.v1",
        "created_at": _now(),
        "updated_at": _now(),
        "messages": [],
        "production_authority": False,
        "live_execution_authority": False,
    }


def _write_carrier_message_queue(root: Path, queue: Mapping[str, Any]) -> None:
    value = dict(queue)
    value["updated_at"] = _now()
    _write_json(root / ACTIVE_CARRIER_MESSAGE_QUEUE_RELATIVE_PATH, value)


def _carrier_message_send(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    sender = str(args.get("sender_carrier_id") or args.get("from_carrier") or "").strip()
    recipient = str(args.get("recipient") or args.get("to") or "").strip()
    body = str(args.get("body") or args.get("message") or "").strip()
    if not sender or not recipient or not body:
        return _blocked("ion_carrier_message_send", "sender_recipient_body_required")
    now = _now()
    message_id = f"carmsg_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(sender)}_to_{_safe_slug(recipient)}"
    message = {
        "schema_id": "ion.carrier_message.v1",
        "message_id": message_id,
        "created_at": now,
        "updated_at": now,
        "sender_carrier_id": sender,
        "recipient": recipient,
        "channel": str(args.get("channel") or "default"),
        "message_type": str(args.get("message_type") or "carrier_message"),
        "body": body,
        "context_refs": list(args.get("context_refs") or []),
        "receipt_refs": list(args.get("receipt_refs") or []),
        "status": "pending",
        "acked_by": [],
        "production_authority": False,
        "live_execution_authority": False,
    }
    packet_path = _write_connector_packet(root, "carrier_messages", message_id, message)
    message["packet_path"] = _connector_rel(packet_path, root)
    _write_json(packet_path, message)
    queue = _carrier_message_queue(root)
    queue.setdefault("messages", []).append(message)
    _write_carrier_message_queue(root, queue)
    return _ok("ion_carrier_message_send", {
        "message_id": message_id,
        "queue_path": ACTIVE_CARRIER_MESSAGE_QUEUE_RELATIVE_PATH.as_posix(),
        "packet_path": _connector_rel(packet_path, root),
    }, mutates_active_state=True)


def _carrier_message_poll(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    recipient = str(args.get("recipient") or "").strip()
    channel = str(args.get("channel") or "").strip()
    include_acked = bool(args.get("include_acked"))
    limit = int(args.get("limit") or 25)
    queue = _carrier_message_queue(root)
    messages = list(queue.get("messages") or [])
    filtered: list[dict[str, Any]] = []
    for item in messages:
        if recipient and item.get("recipient") not in {recipient, "*", "broadcast"}:
            continue
        if channel and item.get("channel") != channel:
            continue
        if not include_acked and item.get("status") == "acked":
            continue
        filtered.append(item)
        if len(filtered) >= limit:
            break
    return _ok("ion_carrier_message_poll", {
        "queue_path": ACTIVE_CARRIER_MESSAGE_QUEUE_RELATIVE_PATH.as_posix(),
        "message_count": len(filtered),
        "messages": filtered,
    })


def _carrier_message_ack(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    message_id = str(args.get("message_id") or "").strip()
    ack_by = str(args.get("ack_by_carrier") or args.get("ack_by") or "").strip()
    if not message_id or not ack_by:
        return _blocked("ion_carrier_message_ack", "message_id_and_ack_by_required")
    queue = _carrier_message_queue(root)
    messages = list(queue.get("messages") or [])
    for item in messages:
        if item.get("message_id") != message_id:
            continue
        ack = {"ack_by_carrier": ack_by, "acked_at": _now()}
        acked_by = list(item.get("acked_by") or [])
        acked_by.append(ack)
        item["acked_by"] = acked_by
        item["status"] = "acked"
        item["updated_at"] = _now()
        _write_carrier_message_queue(root, queue)
        packet_path = _write_connector_packet(root, "carrier_message_acks", message_id, {
            "schema_id": "ion.carrier_message_ack.v1",
            "message_id": message_id,
            "ack": ack,
            "queue_path": ACTIVE_CARRIER_MESSAGE_QUEUE_RELATIVE_PATH.as_posix(),
        })
        return _ok("ion_carrier_message_ack", {
            "message_id": message_id,
            "status": "acked",
            "ack_packet_path": _connector_rel(packet_path, root),
        }, mutates_active_state=True)
    return _blocked("ion_carrier_message_ack", "message_id_not_found")


def _preview_text(value: Any, *, limit: int = 280) -> str:
    text = str(value or "").replace("\r\n", "\n").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def _capsule_file_surface(
    root: Path,
    rel_path: str,
    *,
    include_preview: bool = False,
    max_preview_bytes: int = 512,
) -> dict[str, Any]:
    target, finding = _validate_read_path(
        root,
        rel_path,
        allowed_roots=(
            Path("ION/05_context/current/codex_solo"),
            Path("ION/05_context/current/codex_capsule_chat"),
        ),
    )
    if finding or target is None:
        return {"path": rel_path, "exists": False, "finding": finding or "invalid_path"}
    if not target.exists():
        return {"path": rel_path, "exists": False, "finding": "path_missing"}
    if not target.is_file():
        return {"path": rel_path, "exists": False, "finding": "path_not_file"}
    data = target.read_bytes()
    payload: dict[str, Any] = {
        "path": _connector_rel(target, root),
        "exists": True,
        "bytes": len(data),
        "sha256": _sha256_bytes(data),
    }
    if include_preview:
        bounded_max = min(max(int(max_preview_bytes), 1), 2048)
        preview = data[:bounded_max].decode("utf-8", errors="replace")
        payload["preview"] = preview
        payload["preview_truncated"] = len(data) > bounded_max
    return payload


def _codex_capsule_chat_status(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    include_preview = bool(args.get("include_preview"))
    max_preview_bytes = int(args.get("max_preview_bytes") or 512)
    state_rel = "ION/05_context/current/codex_capsule_chat/state.json"
    state_payload = _read_json(root / state_rel) or {}
    lanes = state_payload.get("lanes") if isinstance(state_payload.get("lanes"), Mapping) else {}
    lane_summaries: dict[str, Any] = {}
    for lane_id in ("codex_general", "ion_system"):
        lane = lanes.get(lane_id) if isinstance(lanes.get(lane_id), Mapping) else {}
        turns = lane.get("turns") if isinstance(lane.get("turns"), list) else []
        queue_links = lane.get("queue_links") if isinstance(lane.get("queue_links"), list) else []
        latest_turn = turns[-1] if turns and isinstance(turns[-1], Mapping) else {}
        lane_summaries[lane_id] = {
            "turn_count": len(turns),
            "queue_link_count": len(queue_links),
            "latest_turn_id": latest_turn.get("turn_id"),
            "latest_turn_kind": latest_turn.get("kind"),
            "latest_turn_created_at": latest_turn.get("created_at"),
        }
    return _ok("ion_codex_capsule_chat_status", {
        "schema_id": "ion.codex_capsule_chat_bridge_status.v1",
        "state_path": state_rel,
        "state_exists": (root / state_rel).exists(),
        "state_sha256": _sha256_file(root / state_rel) if (root / state_rel).exists() else None,
        "paths": {
            "capsule": _capsule_file_surface(
                root,
                "ION/05_context/current/codex_solo/CAPSULE.md",
                include_preview=include_preview,
                max_preview_bytes=max_preview_bytes,
            ),
            "mini": _capsule_file_surface(
                root,
                "ION/05_context/current/codex_solo/MINI.md",
                include_preview=include_preview,
                max_preview_bytes=max_preview_bytes,
            ),
            "hot_context": _capsule_file_surface(
                root,
                "ION/05_context/current/codex_solo/HOT_CONTEXT.md",
                include_preview=include_preview,
                max_preview_bytes=max_preview_bytes,
            ),
        },
        "lanes": lane_summaries,
        "production_authority": False,
        "live_execution_authority": False,
    })


def _codex_capsule_message_send(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    from .ion_dual_codex_chat import record_chat_turn

    lane_id = str(args.get("lane_id") or "codex_general").strip() or "codex_general"
    message = str(args.get("message") or args.get("body") or "").strip()
    author = str(args.get("author") or "user").strip() or "user"
    execution_mode = str(args.get("execution_mode") or "respond_only").strip() or "respond_only"
    if not message:
        return _blocked("ion_codex_capsule_message_send", "message_required")
    if execution_mode != "respond_only":
        return _blocked(
            "ion_codex_capsule_message_send",
            "execution_mode_must_be_respond_only_for_bounded_message_send",
            {"allowed_execution_modes": ["respond_only"]},
        )
    result = record_chat_turn(
        root,
        lane_id=lane_id,
        message=message,
        author=author,
        execution_mode="respond_only",
    )
    if not result.get("ok"):
        return _blocked("ion_codex_capsule_message_send", str(result.get("finding") or "capsule_message_send_blocked"), result)
    turn = result.get("turn") if isinstance(result.get("turn"), Mapping) else {}
    assistant_turn = result.get("assistant_turn") if isinstance(result.get("assistant_turn"), Mapping) else {}
    packet = {
        "schema_id": "ion.codex_capsule_chat_message_packet.v1",
        "lane_id": lane_id,
        "author": author,
        "execution_mode": "respond_only",
        "turn_id": turn.get("turn_id"),
        "assistant_turn_id": assistant_turn.get("turn_id"),
        "message_sha256": _sha256_text(message),
        "message_preview": _preview_text(message),
        "created_at": _now(),
        "status": "RECORDED_TO_CAPSULE_CHAT_STATE",
        "production_authority": False,
        "live_execution_authority": False,
    }
    packet_path = _write_connector_packet(root, "capsule_messages", f"{lane_id}_message", packet)
    return _ok("ion_codex_capsule_message_send", {
        "lane_id": lane_id,
        "turn_id": turn.get("turn_id"),
        "assistant_turn_id": assistant_turn.get("turn_id"),
        "state_path": "ION/05_context/current/codex_capsule_chat/state.json",
        "packet_path": _connector_rel(packet_path, root),
        "status": "RECORDED_TO_CAPSULE_CHAT_STATE",
    }, mutates_active_state=True)


def _codex_capsule_message_poll(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    from .ion_dual_codex_chat import load_dual_chat_state

    lane_id = str(args.get("lane_id") or "codex_general").strip() or "codex_general"
    limit = min(max(int(args.get("limit") or 25), 1), 100)
    include_assistant = bool(args.get("include_assistant", True))
    include_context_posts = bool(args.get("include_context_posts", False))
    since_turn_id = str(args.get("since_turn_id") or "").strip()
    state = load_dual_chat_state(root)
    lanes = state.get("lanes") if isinstance(state.get("lanes"), Mapping) else {}
    lane = lanes.get(lane_id) if isinstance(lanes.get(lane_id), Mapping) else None
    if lane is None:
        return _blocked("ion_codex_capsule_message_poll", "unknown_lane_id", {"allowed_lanes": sorted(lanes)})
    turns = lane.get("turns") if isinstance(lane.get("turns"), list) else []
    start_index = 0
    if since_turn_id:
        for idx, raw in enumerate(turns):
            if isinstance(raw, Mapping) and str(raw.get("turn_id") or "") == since_turn_id:
                start_index = idx + 1
                break
    records: list[dict[str, Any]] = []
    for raw in reversed(turns[start_index:]):
        if not isinstance(raw, Mapping):
            continue
        author = str(raw.get("author") or "")
        kind = str(raw.get("kind") or "")
        if not include_assistant and author not in {"operator", "user"}:
            continue
        if not include_context_posts and kind == "mini_auto_post":
            continue
        message = str(raw.get("message") or "")
        records.append({
            "turn_id": raw.get("turn_id"),
            "created_at": raw.get("created_at"),
            "author": author,
            "kind": kind,
            "execution_mode": raw.get("execution_mode"),
            "message_sha256": raw.get("message_sha256"),
            "message_preview": _preview_text(message, limit=420),
        })
        if len(records) >= limit:
            break
    return _ok("ion_codex_capsule_message_poll", {
        "lane_id": lane_id,
        "since_turn_id": since_turn_id or None,
        "message_count": len(records),
        "messages": records,
        "state_path": "ION/05_context/current/codex_capsule_chat/state.json",
    })


def _codex_capsule_sync_to_queue(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    from .ion_dual_codex_chat import WRITE_CONFIRMATION_TOKEN as CAPSULE_WRITE_CONFIRMATION_TOKEN
    from .ion_dual_codex_chat import queue_chat_codex_work_packet

    lane_id = str(args.get("lane_id") or "codex_general").strip() or "codex_general"
    objective = str(args.get("objective") or args.get("message") or "").strip()
    source_turn_id = str(args.get("source_turn_id") or "").strip() or None
    if not objective:
        return _blocked("ion_codex_capsule_sync_to_queue", "objective_required")
    result = queue_chat_codex_work_packet(
        root,
        lane_id=lane_id,
        objective=objective,
        confirmation=CAPSULE_WRITE_CONFIRMATION_TOKEN,
        source_turn_id=source_turn_id,
    )
    if not result.get("ok"):
        return _blocked("ion_codex_capsule_sync_to_queue", str(result.get("finding") or "capsule_sync_to_queue_blocked"), result)
    queue_link = result.get("queue_link") if isinstance(result.get("queue_link"), Mapping) else {}
    packet_path = _write_connector_packet(root, "capsule_queue_sync", f"{lane_id}_sync", {
        "schema_id": "ion.codex_capsule_chat_queue_sync_packet.v1",
        "lane_id": lane_id,
        "source_turn_id": source_turn_id,
        "objective_sha256": _sha256_text(objective),
        "objective_preview": _preview_text(objective, limit=420),
        "queue_link": queue_link,
        "created_at": _now(),
        "status": queue_link.get("status") or "QUEUED_FOR_CODEX_CARRIER",
        "production_authority": False,
        "live_execution_authority": False,
    })
    return _ok("ion_codex_capsule_sync_to_queue", {
        "queue_link": queue_link,
        "sync_packet_path": _connector_rel(packet_path, root),
    }, mutates_active_state=True)


def _bounded_connector_packet_path(root: Path, rel_value: str, *, subdir: str) -> Path:
    path = _safe_rel_path(root, rel_value)
    allowed_root = (root / CONNECTOR_STATE_DIR / subdir).resolve()
    path.relative_to(allowed_root)
    if path.suffix != ".json":
        raise ValueError("connector packet path must point to a JSON packet")
    return path


def _load_json_file(path: Path) -> dict[str, Any]:
    value = _read_json(path)
    return value if isinstance(value, dict) else {}


def _task_returns_for_request(root: Path, request_path: str | None, request_id: str | None) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    returns_root = root / CONNECTOR_STATE_DIR / "task_returns"
    if not returns_root.exists():
        return results
    for path in sorted(returns_root.glob("*.json")):
        payload = _load_json_file(path)
        if request_path and payload.get("work_request_path") == request_path:
            results.append({"path": path.relative_to(root).as_posix(), "packet": payload})
        elif request_id and payload.get("work_request_id") == request_id:
            results.append({"path": path.relative_to(root).as_posix(), "packet": payload})
    return results


def _codex_work_queue(root: Path, *, limit: int = 50) -> dict[str, Any]:
    requests_root = root / CONNECTOR_STATE_DIR / "codex_work_requests"
    requests: list[dict[str, Any]] = []
    if requests_root.exists():
        for path in sorted(requests_root.glob("*.json"), reverse=True):
            if len(requests) >= limit:
                break
            payload = _load_json_file(path)
            rel_path = path.relative_to(root).as_posix()
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
                "accepted_return_count": sum(
                    1 for item in returns if item["packet"].get("accepted_for_carrier_intake") is True
                ),
            })
    return {
        "schema_id": "ion.chatgpt_browser_connector_codex_work_queue.v1",
        "queue_path": CODEX_WORK_QUEUE_RELATIVE_PATH.as_posix(),
        "state_dir": (CONNECTOR_STATE_DIR / "codex_work_requests").as_posix(),
        "request_count": len(requests),
        "requests": requests,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _write_codex_work_queue_index(root: Path) -> dict[str, Any]:
    queue = _codex_work_queue(root)
    _write_json(root / CODEX_WORK_QUEUE_RELATIVE_PATH, queue)
    return queue


def _enqueue_connector_operator_message(root: Path, *, message: str, priority: int) -> dict[str, Any]:
    path = root / "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json"
    queue = _read_json(path) or {
        "schema_id": "ion.operator_message_queue.v1",
        "created_at": _now(),
        "items": [],
        "production_authority": False,
        "live_execution_authority": False,
    }
    now = _now()
    item = {
        "id": f"opmsg_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(message)}",
        "created_at": now,
        "updated_at": now,
        "source": "chatgpt_browser_connector",
        "status": "pending",
        "priority": int(priority),
        "message": message,
        "classification": "chatgpt_browser_connector_queued_work",
        "classification_record": {
            "schema_id": "ion.chatgpt_browser_connector_operator_message_classification.v1",
            "classification": "chatgpt_browser_connector_queued_work",
            "production_authority": False,
            "live_execution_authority": False,
        },
        "consumed_at": None,
        "completed_at": None,
    }
    queue.setdefault("items", []).append(item)
    queue["updated_at"] = now
    _write_json(path, queue)
    return {
        "schema_id": "ion.operator_message_queue_result.v1",
        "verdict": "ION_OPERATOR_MESSAGE_ENQUEUED",
        "queue_path": "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
        "item": item,
    }


def _coerce_timeout_seconds(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return DEFAULT_CODEX_TIMEOUT_SECONDS


def _load_timeout_policy_request(root: Path, request_path: str | None) -> dict[str, Any] | None:
    if not request_path:
        return None
    try:
        bounded = _bounded_connector_packet_path(root, request_path, subdir="codex_work_requests")
    except (ValueError, RuntimeError):
        return None
    if not bounded.exists():
        return None
    payload = _load_json_file(bounded)
    return payload if isinstance(payload, dict) else None


def _work_request_requires_workload_diff(payload: Mapping[str, Any]) -> bool:
    requested_by = str(payload.get("requested_by") or "").strip().lower()
    if requested_by == "ion_agent_invocation_broker":
        return True
    signal_text = " ".join([
        str(payload.get("request_kind") or ""),
        str(payload.get("objective") or ""),
        str(payload.get("agent_role") or ""),
        str(payload.get("agent_role_id") or ""),
        str(payload.get("agent_display_name") or ""),
    ]).lower()
    return any(hint in signal_text for hint in WORKLOAD_POLICY_HINTS)


def _return_contract_sections_for_work_request(payload: Mapping[str, Any]) -> list[str]:
    sections: list[str] = []
    configured = payload.get("return_contract_sections")
    if isinstance(configured, list):
        for item in configured:
            section = str(item or "").strip()
            if section.startswith("### ") and section not in sections:
                sections.append(section)
    if not sections:
        sections = list(BASE_RETURN_CONTRACT_SECTIONS)
    if _work_request_requires_workload_diff(payload) and WORKLOAD_DIFF_SECTION not in sections:
        sections.append(WORKLOAD_DIFF_SECTION)
    return sections


def _section_heading_present(text: str, heading: str) -> bool:
    normalized = heading.strip().lower()
    for line in text.splitlines():
        if line.strip().lower() == normalized:
            return True
    return False


def _return_template_lint(text: str, required_reads: list[str]) -> dict[str, Any]:
    findings: list[str] = []
    for heading in RETURN_TEMPLATE_REQUIRED_SECTIONS:
        if not _section_heading_present(text, heading):
            findings.append(f"missing_required_section:{heading}")
    lower_text = text.lower()
    for required_field in ("template_id:", "action_id:", "result:"):
        if required_field not in lower_text:
            findings.append(f"missing_required_field:{required_field.rstrip(':')}")
    if "touched_paths:" not in lower_text and "no_touched_paths:" not in lower_text:
        findings.append("missing_required_field:touched_paths_or_no_touched_paths")
    for path in required_reads:
        if path not in text:
            findings.append(f"missing_required_read_path:{path}")
            continue
        idx = text.find(path)
        window = text[idx: idx + 800].lower()
        if "sha256:" not in window:
            findings.append(f"missing_sha256_near_required_read:{path}")
        if "excerpt:" not in window:
            findings.append(f"missing_excerpt_near_required_read:{path}")
    return {
        "schema_id": "ion.return_template_lint_result.v1",
        "accepted": not findings,
        "findings": findings,
    }


def _requires_extended_timeout(tool_name: str, args: Mapping[str, Any], request_payload: Mapping[str, Any] | None) -> bool:
    if tool_name in {"ion_agent_invoke", "ion_swarm_step_once"}:
        return True
    if request_payload and _work_request_requires_workload_diff(request_payload):
        return True
    signal_text = " ".join([
        str(args.get("request_kind") or ""),
        str(args.get("objective") or ""),
        str(args.get("agent") or ""),
    ]).lower()
    return any(hint in signal_text for hint in WORKLOAD_POLICY_HINTS)


def _normalized_timeout_for_tool(root: Path, tool_name: str, args: Mapping[str, Any]) -> int:
    raw = args.get("max_runtime_seconds")
    if raw is None:
        raw = args.get("timeout_seconds")
    timeout = _coerce_timeout_seconds(raw)
    request_payload = _load_timeout_policy_request(root, str(args.get("request_path") or "").strip() or None)
    if _requires_extended_timeout(tool_name, args, request_payload):
        timeout = max(timeout, MIN_COMPLEX_WORKLOAD_TIMEOUT_SECONDS)
    timeout = min(timeout, MAX_CODEX_TIMEOUT_SECONDS)
    timeout = max(timeout, 30)
    return timeout


def _evaluate_task_return_packet(root: Path, args: Mapping[str, Any]) -> dict[str, Any]:
    text = str(args.get("task_output_text") or "")
    receipt = args.get("context_receipt")
    if not isinstance(receipt, Mapping):
        return _blocked("ion_submit_task_return", "context_receipt_object_required")
    work_request_path = str(args.get("work_request_path") or "").strip()
    work_request_id = str(args.get("work_request_id") or "").strip()
    request_payload: dict[str, Any] | None = None
    request_path: Path | None = None
    if work_request_path:
        try:
            request_path = _bounded_connector_packet_path(root, work_request_path, subdir="codex_work_requests")
        except (ValueError, RuntimeError):
            return _blocked("ion_submit_task_return", "work_request_path_not_bounded_to_codex_work_requests")
        if not request_path.exists():
            return _blocked("ion_submit_task_return", "work_request_path_missing")
        request_payload = _load_json_file(request_path)
        work_request_id = work_request_id or str(request_payload.get("request_id") or "")
    required_reads = []
    receipt_reads = receipt.get("required_context_reads")
    if isinstance(receipt_reads, list):
        for item in receipt_reads:
            if isinstance(item, Mapping) and item.get("required") is True and str(item.get("kind") or "") == "file":
                read_path = str(item.get("path") or "").strip()
                if read_path:
                    required_reads.append(read_path)
    lint_result = _return_template_lint(text, required_reads)
    return_template_valid = bool(lint_result.get("accepted"))
    context_result = evaluate_context_proof_return(receipt=receipt, task_output=text)
    template_result = evaluate_template_action_proof(worker_output=text)
    required_sections = _return_contract_sections_for_work_request(request_payload or {})
    workload_diff_required = WORKLOAD_DIFF_SECTION in required_sections
    workload_diff_present = _section_heading_present(text, WORKLOAD_DIFF_SECTION)
    workload_diff_accepted = (not workload_diff_required) or workload_diff_present
    accepted = return_template_valid and bool(context_result.get("accepted")) and bool(template_result.get("accepted")) and workload_diff_accepted
    workload_diff_findings: list[str] = []
    if workload_diff_required and not workload_diff_present:
        workload_diff_findings.append("missing_required_section:### WORKLOAD DIFF")
    lint_findings = list(lint_result.get("findings", []))
    result_status = "RECORDED_FOR_CARRIER_INTAKE" if accepted else ("RETURN_TEMPLATE_INVALID" if not return_template_valid else "BLOCKED_BY_PROOF_GATE")
    packet = {
        "schema_id": "ion.chatgpt_browser_connector_task_return_packet.v1",
        "accepted_for_carrier_intake": accepted,
        "return_template_valid": return_template_valid,
        "return_template_lint_result": lint_result,
        "blocked_but_preserved": not accepted,
        "salvage_route": "ION/05_context/current/chatgpt_connector/task_returns",
        "raw_latest_return_md_expected_from_run_packet": True,
        "work_request_id": work_request_id or None,
        "work_request_path": work_request_path or None,
        "context_proof_result": context_result,
        "template_action_proof_result": template_result,
        "workload_diff_required": workload_diff_required,
        "workload_diff_present": workload_diff_present,
        "workload_diff_accepted": workload_diff_accepted,
        "task_output_sha256": _sha256_text(text),
        "task_output_preview": text[:1200],
        "result": result_status,
    }
    packet_path = _write_connector_packet(root, "task_returns", "task_return", packet)
    rel_return_path = packet_path.relative_to(root).as_posix()
    work_request_updated = False
    if request_path and request_payload is not None:
        paths = list(request_payload.get("return_packet_paths") or [])
        if rel_return_path not in paths:
            paths.append(rel_return_path)
        request_payload["return_packet_paths"] = paths
        request_payload["latest_return_packet_path"] = rel_return_path
        request_payload["status"] = "RETURN_RECORDED_PROOF_ACCEPTED" if accepted else ("RETURN_TEMPLATE_INVALID" if not return_template_valid else "RETURN_RECORDED_PROOF_BLOCKED")
        request_payload["updated_at"] = _now()
        request_payload["latest_context_proof_accepted"] = context_result.get("accepted")
        request_payload["latest_template_action_proof_accepted"] = template_result.get("accepted")
        _write_json(request_path, request_payload)
        work_request_updated = True
    queue = _write_codex_work_queue_index(root)
    return _ok(
        "ion_submit_task_return",
        {
            "accepted_for_carrier_intake": accepted,
            "packet_path": rel_return_path,
            "work_request_id": work_request_id or None,
            "work_request_path": work_request_path or None,
            "work_request_updated": work_request_updated,
            "codex_work_queue_path": CODEX_WORK_QUEUE_RELATIVE_PATH.as_posix(),
            "codex_work_queue_request_count": queue["request_count"],
                "return_template_valid": return_template_valid,
                "context_proof_accepted": context_result.get("accepted"),
                "template_action_proof_accepted": template_result.get("accepted"),
                "workload_diff_required": workload_diff_required,
                "workload_diff_present": workload_diff_present,
                "workload_diff_accepted": workload_diff_accepted,
                "blocked_but_preserved": not accepted,
                "salvage_route": "ION/05_context/current/chatgpt_connector/task_returns",
                "findings": lint_findings + list(context_result.get("findings", [])) + list(template_result.get("findings", [])) + workload_diff_findings,
            },
            mutates_active_state=True,
        )


def call_chatgpt_connector_tool(
    root: str | Path | None,
    tool_name: str,
    arguments: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_connector_root(root)
    args = dict(arguments or {})
    if tool_name in FORBIDDEN_CAPABILITIES:
        return _blocked(tool_name, "forbidden_capability")
    if tool_name == "ion_status":
        return _ok(tool_name, build_ion_status(shell_root))
    if tool_name == "ion_current_operating_packet":
        return _packet_read(shell_root, "current_operating_packet")
    if tool_name == "ion_carrier_onboarding_packet":
        carrier = str(args.get("carrier") or "chatgpt_browser")
        profile = args.get("carrier_profile")
        profile_path = str(profile) if profile else None
        packet = build_carrier_onboarding_packet(shell_root, carrier_id=carrier, carrier_profile_path=profile_path)
        return _ok(tool_name, packet)
    if tool_name == "ion_read_active_packet":
        max_bytes = args.get("max_bytes")
        return _packet_read(
            shell_root,
            str(args.get("packet") or ""),
            max_bytes=int(max_bytes) if max_bytes is not None else None,
            tool_name=tool_name,
        )
    if tool_name == "ion_context_plan":
        return _packet_read(shell_root, "context_window", max_bytes=int(args.get("max_bytes") or 32 * 1024), tool_name=tool_name)
    if tool_name == "ion_cockpit_view":
        return _ok(tool_name, build_cockpit_view_model(shell_root))
    if tool_name == "ion_artifact_manifest":
        return _ok(tool_name, _artifact_manifest(shell_root))
    if tool_name == "ion_receipt_search":
        return _ok(tool_name, _receipt_search(shell_root, str(args.get("query") or ""), int(args.get("limit") or 10)))
    if tool_name == "ion_git_status_summary":
        return _ok(tool_name, _git_status_summary(shell_root))
    if tool_name == "ion_codex_work_queue":
        return _ok(tool_name, _codex_work_queue(shell_root, limit=int(args.get("limit") or 50)))
    if tool_name == "ion_carrier_message_poll":
        return _carrier_message_poll(shell_root, args)
    if tool_name == "ion_file_read":
        return _bounded_file_read(shell_root, args)
    if tool_name == "ion_file_search":
        return _file_search(shell_root, args)
    if tool_name == "ion_tree_list":
        return _tree_list(shell_root, args)
    if tool_name == "ion_registry_read":
        return _registry_read(shell_root, args)
    if tool_name == "ion_template_read":
        return _template_read(shell_root, args)
    if tool_name == "ion_context_compile":
        return _context_compile(shell_root, args)
    if tool_name == "ion_receipt_hydrate":
        return _receipt_hydrate(shell_root, args)
    if tool_name == "ion_tool_manifest":
        return _ok(tool_name, _tool_manifest(shell_root))
    if tool_name == "ion_codex_capsule_chat_status":
        return _codex_capsule_chat_status(shell_root, args)
    if tool_name == "ion_codex_capsule_message_poll":
        return _codex_capsule_message_poll(shell_root, args)
    if tool_name in {"ion_daemon_status", "ion_codex_queue_autorun_status"}:
        data = build_codex_queue_runner_status(shell_root, reconcile=False)
        reconciliation = data.get("reconciliation") if isinstance(data.get("reconciliation"), dict) else {}
        mutates = bool(
            data.get("stale_active_run_detected")
            or reconciliation.get("latest_run_failure_classification_updated")
        )
        return _ok(tool_name, data, mutates_active_state=mutates)
    if tool_name == "ion_codex_worker_live_status":
        include_preview = bool(args.get("include_preview"))
        preview_target = str(args.get("preview_target") or "").strip() or None
        preview_max_bytes = int(args.get("max_preview_bytes") or 512)
        data = build_codex_queue_runner_status(
            shell_root,
            reconcile=False,
            include_preview=include_preview,
            preview_target=preview_target,
            preview_max_bytes=preview_max_bytes,
        )
        reconciliation = data.get("reconciliation") if isinstance(data.get("reconciliation"), dict) else {}
        mutates = bool(
            data.get("stale_active_run_detected")
            or reconciliation.get("latest_run_failure_classification_updated")
        )
        return _ok(tool_name, data, mutates_active_state=mutates)
    if tool_name == "ion_codex_runner_reconcile":
        write = bool(args.get("write", True))
        reconciliation = reconcile_codex_queue_runner_state(shell_root, write=write)
        status = build_codex_queue_runner_status(shell_root, reconcile=False)
        action = str(reconciliation.get("action") or "")
        mutates = bool(
            write
            and action not in {"", "no_active_run", "active_run_still_running", "not_requested"}
        )
        return _ok(
            tool_name,
            {
                "schema_id": "ion.codex_queue_runner_reconcile_result.v1",
                "reconcile_write": write,
                "reconciliation": reconciliation,
                "status": status,
            },
            mutates_active_state=mutates,
        )
    if tool_name == "ion_agent_list":
        return _ok(tool_name, list_agents(shell_root))
    if tool_name == "ion_agent_status":
        return _ok(tool_name, build_agent_broker_status(shell_root))
    if tool_name == "ion_agent_queue":
        return _ok(tool_name, agent_queue(shell_root, limit=int(args.get("limit") or 25)))
    if tool_name == "ion_agent_result":
        return _ok(tool_name, agent_result(shell_root, invocation_id=str(args.get("invocation_id") or "").strip() or None))
    if tool_name == "ion_agent_spawn_plan":
        return _ok(tool_name, build_agent_spawn_plan(shell_root, objective=str(args.get("objective") or "").strip() or None))
    if tool_name == "ion_swarm_status":
        return _ok(tool_name, build_agent_broker_status(shell_root))
    if tool_name == "ion_queue_operator_message":
        message = str(args.get("message") or "").strip()
        if not message:
            return _blocked(tool_name, "message_required")
        result = _enqueue_connector_operator_message(shell_root, message=message, priority=int(args.get("priority") or 50))
        return _ok(tool_name, result, mutates_active_state=True)
    if tool_name == "ion_file_put_text":
        return _put_text_artifact(shell_root, args)
    if tool_name == "ion_artifact_upload_init":
        return _artifact_upload_init(shell_root, args)
    if tool_name == "ion_artifact_upload_chunk":
        return _artifact_upload_chunk(shell_root, args)
    if tool_name == "ion_artifact_upload_commit":
        return _artifact_upload_commit(shell_root, args)
    if tool_name == "ion_carrier_message_send":
        return _carrier_message_send(shell_root, args)
    if tool_name == "ion_carrier_message_ack":
        return _carrier_message_ack(shell_root, args)
    if tool_name == "ion_codex_capsule_message_send":
        return _codex_capsule_message_send(shell_root, args)
    if tool_name == "ion_codex_capsule_sync_to_queue":
        return _codex_capsule_sync_to_queue(shell_root, args)
    if tool_name == "ion_codex_queue_process_once":
        request_path = str(args.get("request_path") or "").strip() or None
        timeout = _normalized_timeout_for_tool(shell_root, tool_name, args)
        start = bool(args.get("start"))
        result = process_codex_queue_once(
            shell_root,
            request_path=request_path,
            start=start,
            background=True,
            timeout_seconds=timeout,
        )
        return _ok(tool_name, result, mutates_active_state=True) if result.get("ok") else _blocked(tool_name, str(result.get("finding") or result.get("result") or "codex_queue_process_once_blocked"), result)
    if tool_name == "ion_agent_invoke":
        result = invoke_agent(
            shell_root,
            agent=str(args.get("agent") or ""),
            objective=str(args.get("objective") or ""),
            mode=str(args.get("mode") or "prepare_only"),
            queue=bool(args.get("queue")),
            start=bool(args.get("start")),
            context_refs=list(args.get("context_refs") or []),
            requested_by_carrier_id=str(args.get("requested_by_carrier_id") or "CHATGPT_BROWSER_CARRIER"),
            requested_by_callsign=str(args.get("requested_by_callsign") or "Sev"),
            timeout_seconds=_normalized_timeout_for_tool(shell_root, tool_name, args),
        )
        return _ok(tool_name, result, mutates_active_state=True) if result.get("ok") else _blocked(tool_name, str(result.get("finding") or "agent_invoke_blocked"), result)
    if tool_name == "ion_agent_cancel":
        result = cancel_agent_invocation(shell_root, invocation_id=str(args.get("invocation_id") or ""))
        return _ok(tool_name, result, mutates_active_state=True) if result.get("ok") else _blocked(tool_name, str(result.get("finding") or "agent_cancel_blocked"), result)
    if tool_name == "ion_swarm_step_once":
        result = swarm_step_once(
            shell_root,
            request_path=str(args.get("request_path") or "").strip() or None,
            start=bool(args.get("start")),
            timeout_seconds=_normalized_timeout_for_tool(shell_root, tool_name, args),
        )
        return _ok(tool_name, result, mutates_active_state=True) if result.get("ok") else _blocked(tool_name, str(result.get("finding") or result.get("result") or "swarm_step_once_blocked"), result)
    if tool_name == "ion_request_codex_work_packet":
        objective = str(args.get("objective") or "").strip()
        if not objective:
            return _blocked(tool_name, "objective_required")
        now = _now()
        request_id = f"codex_req_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(objective)}"
        payload = {
            "schema_id": "ion.chatgpt_browser_connector_codex_work_request.v1",
            "request_id": request_id,
            "objective": objective,
            "requested_by": "chatgpt_browser_connector",
            "status": "QUEUED_FOR_CODEX_CARRIER",
            "created_at": now,
            "updated_at": now,
            "return_packet_paths": [],
            "latest_return_packet_path": None,
            "production_authority": False,
            "live_execution_authority": False,
        }
        if isinstance(args.get("codex_model_move"), Mapping):
            payload["codex_model_move"] = dict(args["codex_model_move"])
        request_kind = str(args.get("request_kind") or "").strip()
        if request_kind:
            payload["request_kind"] = request_kind
        payload["return_contract_sections"] = _return_contract_sections_for_work_request(payload)
        if isinstance(args.get("ion_skill_activation"), Mapping):
            payload["ion_skill_activation"] = dict(args["ion_skill_activation"])
        if isinstance(args.get("ion_chat_engine_turn"), Mapping):
            payload["ion_chat_engine_turn"] = dict(args["ion_chat_engine_turn"])
        required_context_reads = _sanitize_required_context_reads(args.get("required_context_reads"))
        if required_context_reads:
            payload["required_context_reads"] = required_context_reads
        packet_path = _write_connector_packet(shell_root, "codex_work_requests", objective, payload)
        payload["packet_path"] = packet_path.relative_to(shell_root).as_posix()
        _write_json(packet_path, payload)
        queue = _write_codex_work_queue_index(shell_root)
        return _ok(
            tool_name,
            {
                "request_id": request_id,
                "packet_path": packet_path.relative_to(shell_root).as_posix(),
                "codex_work_queue_path": CODEX_WORK_QUEUE_RELATIVE_PATH.as_posix(),
                "codex_work_queue_request_count": queue["request_count"],
            },
            mutates_active_state=True,
        )
    if tool_name == "ion_submit_task_return":
        return _evaluate_task_return_packet(shell_root, args)
    if tool_name == "ion_record_chatgpt_decision":
        decision = str(args.get("decision") or "").strip()
        if not decision:
            return _blocked(tool_name, "decision_required")
        packet_path = _write_connector_packet(shell_root, "decisions", decision, {
            "schema_id": "ion.chatgpt_browser_connector_decision.v1",
            "decision": decision,
            "rationale": str(args.get("rationale") or ""),
            "status": "RECORDED_NOT_AUTHORITY_BY_ITSELF",
        })
        return _ok(tool_name, {"packet_path": packet_path.relative_to(shell_root).as_posix()}, mutates_active_state=True)
    if tool_name == "ion_create_containment_receipt":
        target = str(args.get("target_path") or "").strip()
        transition = str(args.get("transition") or "MOVE_TO_CONTAINMENT").strip()
        reason = str(args.get("reason") or "").strip()
        if not target or not reason:
            return _blocked(tool_name, "target_path_and_reason_required")
        target_path = _safe_rel_path(shell_root, target)
        packet_path = _write_connector_packet(shell_root, "containment_receipts", target, {
            "schema_id": "ion.chatgpt_browser_connector_containment_receipt.v1",
            "target_path": target,
            "target_exists": target_path.exists(),
            "target_sha256": _sha256_file(target_path) if target_path.exists() and target_path.is_file() else None,
            "transition": transition,
            "reason": reason,
            "movement_performed": False,
            "status": "RECEIPT_ONLY_REQUIRES_SEPARATE_BOUNDED_MUTATION",
        })
        return _ok(tool_name, {"packet_path": packet_path.relative_to(shell_root).as_posix()}, mutates_active_state=True)
    return _blocked(tool_name, "tool_not_in_v120_contract", {"allowed": sorted(STATUS_READ_TOOLS | BOUNDED_QUEUE_RECEIPT_TOOLS)})


def audit_chatgpt_browser_mcp_connector_contract(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_connector_root(root)
    findings: list[str] = []
    required_paths = {
        "protocol": PROTOCOL_RELATIVE_PATH,
        "full_carrier_protocol": FULL_CARRIER_PROTOCOL_RELATIVE_PATH,
        "policy": POLICY_RELATIVE_PATH,
        "full_carrier_tool_registry": FULL_CARRIER_TOOL_REGISTRY_RELATIVE_PATH,
        "carrier_capability_registry": FULL_CARRIER_CAPABILITY_REGISTRY_RELATIVE_PATH,
        "schema": SCHEMA_RELATIVE_PATH,
        "integration_dir": INTEGRATION_DIR_RELATIVE_PATH,
        "wrapper": WRAPPER_RELATIVE_PATH,
        "manifest": MANIFEST_RELATIVE_PATH,
        "setup": SETUP_RELATIVE_PATH,
        "codex_queue_runner": Path("ION/04_packages/kernel/ion_codex_queue_runner.py"),
        "agent_invocation_broker": Path("ION/04_packages/kernel/ion_agent_invocation_broker.py"),
    }
    for label, rel in required_paths.items():
        if not (shell_root / rel).exists():
            findings.append(f"missing_{label}:{rel.as_posix()}")

    policy = _read_policy(shell_root) if (shell_root / POLICY_RELATIVE_PATH).exists() else {}
    policy_read = set(policy.get("allowed_status_read_tools", []))
    policy_write = set(policy.get("allowed_bounded_queue_receipt_tools", []))
    policy_forbidden = set(policy.get("forbidden_tools", []))
    allowed = STATUS_READ_TOOLS | BOUNDED_QUEUE_RECEIPT_TOOLS

    if policy_read != STATUS_READ_TOOLS:
        findings.append("policy_allowed_status_read_tools_do_not_match_contract")
    if policy_write != BOUNDED_QUEUE_RECEIPT_TOOLS:
        findings.append("policy_allowed_bounded_queue_receipt_tools_do_not_match_contract")
    missing_forbidden = sorted(FORBIDDEN_CAPABILITIES - policy_forbidden)
    if missing_forbidden:
        findings.append(f"policy_missing_forbidden_capabilities:{','.join(missing_forbidden)}")
    overlap = sorted(allowed & policy_forbidden)
    if overlap:
        findings.append(f"forbidden_tool_also_allowed:{','.join(overlap)}")
    unsafe_overlap = sorted(allowed & FORBIDDEN_CAPABILITIES)
    if unsafe_overlap:
        findings.append(f"unsafe_capability_exposed_as_tool:{','.join(unsafe_overlap)}")

    protocol_text = _read_text(shell_root / PROTOCOL_RELATIVE_PATH) if (shell_root / PROTOCOL_RELATIVE_PATH).exists() else ""
    for phrase in (
        "No carrier is ION identity.",
        "production authority",
        "live execution authority",
        "arbitrary shell",
        "### CONTEXT PROOF",
        "### TEMPLATE ACTION PROOF",
    ):
        if phrase not in protocol_text:
            findings.append(f"protocol_missing_phrase:{phrase}")

    ready = not findings
    return {
        "schema_id": SCHEMA_ID,
        "version_line": VERSION_LINE,
        "generated_at": _now(),
        "connector_id": CONNECTOR_ID,
        "connector_state": "CONTRACT_READY_NOT_DEPLOYED" if ready else "BLOCKED",
        "verdict": "ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY" if ready else "ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_BLOCKED",
        "accepted": ready,
        "allowed_tools": sorted(allowed),
        "status_read_tools": sorted(STATUS_READ_TOOLS),
        "bounded_queue_receipt_tools": sorted(BOUNDED_QUEUE_RECEIPT_TOOLS),
        "forbidden_tools": sorted(FORBIDDEN_CAPABILITIES),
        "tool_descriptors": tool_descriptors(),
        "source_paths": {label: rel.as_posix() for label, rel in required_paths.items()},
        "findings": findings,
        "must_not_claim_ion_identity": True,
        "must_not_claim_steward_relay_persona": True,
        "production_authority": False,
        "live_execution_authority": False,
        "deployment_authority": False,
    }


def write_chatgpt_browser_mcp_connector_contract(
    root: str | Path | None = None,
    *,
    output: str | Path | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_connector_root(root)
    result = audit_chatgpt_browser_mcp_connector_contract(shell_root)
    out = shell_root / (Path(output) if output else OUTPUT_RELATIVE_PATH)
    _write_json(out, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ION ChatGPT browser MCP connector contract.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--tool", default=None)
    parser.add_argument("--arguments-json", default="{}")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.tool:
        result = call_chatgpt_connector_tool(args.ion_root, args.tool, json.loads(args.arguments_json or "{}"))
        ok = bool(result.get("ok"))
    elif args.write:
        result = write_chatgpt_browser_mcp_connector_contract(args.ion_root, output=args.output)
        ok = bool(result.get("accepted"))
    else:
        result = audit_chatgpt_browser_mcp_connector_contract(args.ion_root)
        ok = bool(result.get("accepted"))

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result.get("verdict") or ("OK" if ok else "BLOCKED"))
        for finding in result.get("findings", []):
            print(f"- {finding}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
