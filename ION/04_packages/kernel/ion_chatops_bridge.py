"""ION ChatOps Browser Carrier Runtime local bridge.

This module is a localhost-oriented adapter for approved Sev/ChatGPT Browser
YAML actions. It is not an authority layer. It validates action packets, writes
bounded action/receipt records, and delegates Codex work packet creation to the
existing ChatGPT connector queue owner.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_carrier_onboarding_packet import build_carrier_onboarding_packet
from .ion_chatgpt_browser_mcp_connector_contract import call_chatgpt_connector_tool
from .ion_codex_queue_runner import (
    build_codex_queue_runner_status,
    prepare_codex_queue_run,
    process_codex_queue_once,
)
from .ion_lifecycle_packager import create_lifecycle_package_zip, lifecycle_package_manifest_to_dict
from .ion_safe_full_project_packager import create_safe_full_project_package, safe_full_project_package_result_to_dict
from .ion_status import build_ion_status

SCHEMA_ID = "ion.chatops_bridge.v1"
ACTION_SCHEMA = "ion.chatops.action.v1"
RECEIPT_SCHEMA = "ion.chatops.receipt.v1"
READY_VERDICT = "ION_CHATOPS_BRIDGE_READY"
BLOCKED_VERDICT = "ION_CHATOPS_BRIDGE_BLOCKED"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8767
APPROVAL_TOKEN = "ION_CHATOPS_APPROVED"

BASE_DIR = Path("ION/05_context/current/chatops_bridge")
ACTIONS_DIR = BASE_DIR / "actions"
RECEIPTS_DIR = BASE_DIR / "receipts"
RUNTIME_DIR = BASE_DIR / "runtime"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
EXPORTS_DIR = BASE_DIR / "exports"

POLICY_PATHS = {
    "runtime_protocol": "ION/02_architecture/ION_BROWSER_CARRIER_RUNTIME_PROTOCOL.md",
    "yaml_protocol": "ION/02_architecture/ION_CHATOPS_YAML_ACTION_PROTOCOL.md",
    "action_schema": "ION/03_registry/ion_chatops_action.schema.yaml",
    "extension_policy": "ION/03_registry/ion_chatops_extension_policy.yaml",
    "daemon_policy": "ION/03_registry/ion_chatops_local_daemon_policy.yaml",
    "github_data_plane_registry": "ION/03_registry/ion_github_data_plane_registry.yaml",
    "connector_contract": "ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py",
    "codex_queue_runner": "ION/04_packages/kernel/ion_codex_queue_runner.py",
    "lifecycle_packager": "ION/04_packages/kernel/ion_lifecycle_packager.py",
    "safe_full_project_packager": "ION/04_packages/kernel/ion_safe_full_project_packager.py",
}

SUPPORTED_INTENTS = {
    "register_artifact",
    "write_file_draft",
    "create_codex_work_packet",
    "create_github_issue_draft",
}

INTENT_ALIASES = {
    "create_github_issue": "create_github_issue_draft",
}

HARD_GATED_INTENTS = {
    "delete_file",
    "overwrite_protected_file",
    "push_main",
    "access_credential",
    "production_deploy",
    "broad_shell",
}

ALLOWED_WRITE_PREFIXES = (
    "ION/02_architecture/",
    "ION/03_registry/",
    "ION/05_context/current/chatops_bridge/",
    "ION/05_context/inbox/",
)

PROTECTED_PATH_TOKENS = (
    "/.git/",
    ".env",
    "secret",
    "token",
    "credential",
    "vault",
)

FAILURE_CLASSES = (
    "CHATOPS_SCHEMA_FAILURE",
    "AGENT_INVOCATION_FAILURE",
    "USER_APPROVAL_REJECTED",
    "LOCAL_DAEMON_FAILURE",
    "GITHUB_DATA_PLANE_FAILURE",
    "ION_PACKET_WRITE_FAILURE",
    "CODEX_BACKEND_FAILURE",
    "BACKEND_CODEX_FAILURE",
    "CARRIER_ADAPTER_FAILURE",
    "DAEMON_FAILURE",
    "ION_CORE_FAILURE",
    "POLICY_BLOCK_WORKING_AS_DESIGNED",
)

PLACEHOLDER_ACTION_ID_TOKENS = (
    "YYYY",
    "MMDD",
    "HHMMSS",
    "short-slug",
)

PLACEHOLDER_OBJECTIVES = (
    "State the exact bounded work for local Codex/ION to perform.",
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:96] or "chatops"


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _resolve_root(root: str | Path | None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    return resolve_shell_root_from_ion_root(root)


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _repo_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _normalize_action(packet: Mapping[str, Any]) -> dict[str, Any]:
    value = packet.get("ion_action") if "ion_action" in packet else packet
    if not isinstance(value, Mapping):
        return {}
    action = dict(value)
    if not isinstance(action.get("actor"), Mapping):
        callsign = action.get("callsign")
        carrier = action.get("carrier")
        if callsign or carrier:
            action["actor"] = {
                "callsign": callsign,
                "carrier": carrier,
            }
    if not isinstance(action.get("authority"), Mapping):
        authority_keys = (
            "human_sovereign",
            "requires_approval",
            "production_authority",
            "live_execution_authority",
        )
        if any(key in action for key in authority_keys):
            action["authority"] = {
                key: action.get(key)
                for key in authority_keys
                if key in action
            }
    if not isinstance(action.get("receipts"), Mapping):
        intent = _normalize_intent(action.get("intent"))
        default_receipts = {
            "write_file_draft": ["file_write_receipt", "sha256_receipt"],
            "create_codex_work_packet": ["codex_work_packet_receipt", "action_receipt"],
            "create_github_issue_draft": ["github_issue_draft_receipt", "action_receipt"],
            "register_artifact": ["artifact_registration_receipt", "action_receipt"],
        }
        action["receipts"] = {"requested": default_receipts.get(intent, ["action_receipt"])}
    return action


def _normalize_intent(intent: Any) -> str:
    raw = str(intent or "").strip()
    return INTENT_ALIASES.get(raw, raw)


def _intent_requires_daemon_approval(intent: str, risk_class: str) -> bool:
    """Derive submit approval requirement from daemon policy.

    The browser/user supplied ``authority.requires_approval`` field is a claim,
    not an authority source. Mutating submission gates are therefore decided by
    server-side policy and then checked against Braden approval evidence.
    """

    return bool(
        intent in SUPPORTED_INTENTS
        or risk_class in {
            "approval_required_mutation",
            "hard_gated",
            "bounded",
            "receipt_only",
        }
    )


def _approval_from_packet(packet: Mapping[str, Any], action: Mapping[str, Any]) -> dict[str, Any]:
    approval = packet.get("approval")
    if isinstance(approval, Mapping):
        return dict(approval)
    embedded = action.get("approval")
    return dict(embedded) if isinstance(embedded, Mapping) else {}


def _target_path_from_action(action: Mapping[str, Any]) -> str:
    target = action.get("target")
    if isinstance(target, Mapping):
        return str(target.get("path") or "").strip()
    return ""


def _content_text_from_action(action: Mapping[str, Any]) -> str:
    content = action.get("content")
    if isinstance(content, Mapping):
        return str(content.get("text") or "")
    return ""


def _validate_repo_relative_path(root: Path, rel_value: str) -> tuple[Path | None, str | None]:
    rel = rel_value.replace("\\", "/").strip()
    if not rel:
        return None, "path_required"
    if rel.startswith("/") or rel.startswith("../") or "/../" in rel or rel.endswith("/.."):
        return None, "path_escape"
    lowered = f"/{rel.lower()}"
    if any(token in lowered for token in PROTECTED_PATH_TOKENS):
        return None, "protected_path_token"
    if not any(rel.startswith(prefix) for prefix in ALLOWED_WRITE_PREFIXES):
        return None, "path_prefix_not_allowed"
    target = (root / rel).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        return None, "path_escape"
    return target, None


def validate_chatops_action(packet: Mapping[str, Any], *, require_approval: bool = False) -> dict[str, Any]:
    action = _normalize_action(packet)
    findings: list[str] = []
    warnings: list[str] = []

    if not action:
        findings.append("missing_ion_action_object")

    schema = action.get("schema")
    action_id = str(action.get("action_id") or "").strip()
    intent = _normalize_intent(action.get("intent"))
    actor = action.get("actor") if isinstance(action.get("actor"), Mapping) else {}
    authority = action.get("authority") if isinstance(action.get("authority"), Mapping) else {}
    receipts = action.get("receipts") if isinstance(action.get("receipts"), Mapping) else {}

    if schema != ACTION_SCHEMA:
        findings.append("schema_must_be_ion_chatops_action_v1")
    if not action_id:
        findings.append("action_id_required")
    if any(token.lower() in action_id.lower() for token in PLACEHOLDER_ACTION_ID_TOKENS):
        findings.append("action_id_must_not_be_template_placeholder")
    if not intent:
        findings.append("intent_required")
    if actor.get("callsign") != "Sev":
        findings.append("actor_callsign_must_be_Sev")
    if actor.get("carrier") != "chatgpt_browser":
        findings.append("actor_carrier_must_be_chatgpt_browser")
    if authority.get("human_sovereign") != "Braden":
        findings.append("human_sovereign_must_be_Braden")
    if authority.get("production_authority") is not False:
        findings.append("production_authority_must_be_false")
    if authority.get("live_execution_authority") is not False:
        findings.append("live_execution_authority_must_be_false")
    if not isinstance(receipts.get("requested"), list):
        findings.append("receipts_requested_list_required")
    if intent in HARD_GATED_INTENTS:
        findings.append(f"hard_gated_intent:{intent}")
    elif intent and intent not in SUPPORTED_INTENTS:
        findings.append(f"unsupported_intent:{intent}")

    risk_class = classify_chatops_action(action)["risk_class"] if action else "unknown"
    requires_approval = bool(authority.get("requires_approval"))
    approval_required_by_policy = _intent_requires_daemon_approval(intent, risk_class)
    approval = _approval_from_packet(packet, action)
    if require_approval and approval_required_by_policy:
        if approval.get("approved") is not True:
            findings.append("approval_required")
        if approval.get("approved_by") != "Braden":
            findings.append("approval_must_be_by_Braden")
        if approval.get("approval_token") != APPROVAL_TOKEN:
            findings.append("approval_token_invalid")
    if risk_class == "approval_required_mutation" and not requires_approval:
        findings.append("requires_approval_must_be_true_for_mutating_intent")
    elif not requires_approval:
        warnings.append("action_does_not_require_approval")

    if intent == "write_file_draft":
        if not _target_path_from_action(action):
            findings.append("target_path_required")
        if not _content_text_from_action(action):
            findings.append("content_text_required")

    if intent == "create_codex_work_packet":
        objective = str(action.get("objective") or "").strip()
        if not objective:
            findings.append("objective_required")
        if objective in PLACEHOLDER_OBJECTIVES:
            findings.append("objective_must_be_concrete_not_template_placeholder")

    if intent == "create_github_issue_draft":
        github = action.get("github") if isinstance(action.get("github"), Mapping) else {}
        for key in ("owner", "repo", "title", "body"):
            if not str(github.get(key) or "").strip():
                findings.append(f"github_{key}_required")

    accepted = not findings
    return {
        "schema_id": "ion.chatops.action_validation.v1",
        "accepted": accepted,
        "action_id": action_id or None,
        "intent": intent or None,
        "risk_class": risk_class,
        "findings": findings,
        "warnings": warnings,
        "requires_approval": requires_approval,
        "approval_checked": require_approval,
        "production_authority": False,
        "live_execution_authority": False,
    }


def classify_chatops_action(action: Mapping[str, Any]) -> dict[str, Any]:
    intent = _normalize_intent(action.get("intent"))
    if intent in HARD_GATED_INTENTS:
        risk = "hard_gated"
    elif intent in {"write_file_draft", "create_codex_work_packet", "create_github_issue_draft"}:
        risk = "approval_required_mutation"
    elif intent == "register_artifact":
        risk = "receipt_only"
    elif intent in SUPPORTED_INTENTS:
        risk = "bounded"
    else:
        risk = "unsupported"
    return {
        "schema_id": "ion.chatops.action_classification.v1",
        "intent": intent,
        "risk_class": risk,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _action_path(root: Path, action_id: str) -> Path:
    return root / ACTIONS_DIR / f"{_safe_slug(action_id)}.json"


def _receipt_path(root: Path, receipt_id: str) -> Path:
    return root / RECEIPTS_DIR / f"{_safe_slug(receipt_id)}.json"


def _base_receipt(
    *,
    action: Mapping[str, Any],
    status: str,
    approved_by: str | None,
    failure_classification: str | None = None,
) -> dict[str, Any]:
    action_id = str(action.get("action_id") or "unknown")
    receipt_id = f"chatops_receipt_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{_safe_slug(action_id)}"
    return {
        "schema_id": RECEIPT_SCHEMA,
        "receipt_id": receipt_id,
        "action_id": action_id,
        "created_at": _now(),
        "actor": {
            "callsign": "Sev",
            "carrier": "chatgpt_browser",
        },
        "approved_by": approved_by,
        "intent": _normalize_intent(action.get("intent")),
        "status": status,
        "target_refs": [],
        "files_touched": [],
        "github_refs": [],
        "sha256": {},
        "validation": {},
        "failure_classification": failure_classification,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _write_action_packet(root: Path, packet: Mapping[str, Any], action: Mapping[str, Any]) -> str:
    action_path = _action_path(root, str(action.get("action_id") or "unknown"))
    stored = {
        "schema_id": "ion.chatops.action_packet.v1",
        "created_at": _now(),
        "ion_action": dict(action),
        "source": "ion_chatops_bridge",
        "production_authority": False,
        "live_execution_authority": False,
    }
    approval = _approval_from_packet(packet, action)
    if approval:
        stored["approval"] = approval
    _write_json(action_path, stored)
    return _repo_rel(action_path, root)


def _complete_receipt(root: Path, receipt: dict[str, Any]) -> str:
    receipt_path = _receipt_path(root, str(receipt["receipt_id"]))
    _write_json(receipt_path, receipt)
    return _repo_rel(receipt_path, root)


def _handle_write_file_draft(root: Path, action: Mapping[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    target_path, finding = _validate_repo_relative_path(root, _target_path_from_action(action))
    if finding or target_path is None:
        receipt["status"] = "failed"
        receipt["failure_classification"] = "POLICY_BLOCK_WORKING_AS_DESIGNED"
        receipt["validation"]["finding"] = finding
        return {"ok": False, "finding": finding}

    target = action.get("target") if isinstance(action.get("target"), Mapping) else {}
    overwrite = bool(target.get("overwrite"))
    if target_path.exists() and not overwrite:
        receipt["status"] = "failed"
        receipt["failure_classification"] = "POLICY_BLOCK_WORKING_AS_DESIGNED"
        receipt["validation"]["finding"] = "target_exists_overwrite_false"
        return {"ok": False, "finding": "target_exists_overwrite_false"}
    if target_path.exists() and overwrite:
        receipt["status"] = "failed"
        receipt["failure_classification"] = "POLICY_BLOCK_WORKING_AS_DESIGNED"
        receipt["validation"]["finding"] = "overwrite_not_supported_in_mvp"
        return {"ok": False, "finding": "overwrite_not_supported_in_mvp"}

    text = _content_text_from_action(action)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    content = action.get("content") if isinstance(action.get("content"), Mapping) else {}
    target_path.write_text(text, encoding=str(content.get("encoding") or "utf-8"))
    rel = _repo_rel(target_path, root)
    receipt["status"] = "completed"
    receipt["files_touched"].append(rel)
    receipt["target_refs"].append({"provider": "local_ion", "path": rel})
    receipt["sha256"][rel] = _sha256_file(target_path)
    receipt["validation"]["after_write"] = ["sha256"]
    return {"ok": True, "path": rel, "sha256": receipt["sha256"][rel]}


def _handle_create_codex_work_packet(root: Path, action: Mapping[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    objective = str(action.get("objective") or "").strip()
    result = call_chatgpt_connector_tool(
        root,
        "ion_request_codex_work_packet",
        {
            "objective": objective,
            "confirmation": "ION_BOUNDED_WRITE_CONFIRMED",
        },
    )
    if not result.get("ok"):
        receipt["status"] = "failed"
        receipt["failure_classification"] = "ION_PACKET_WRITE_FAILURE"
        receipt["validation"]["connector_result"] = result
        return {"ok": False, "finding": result.get("finding") or "codex_work_packet_failed", "connector_result": result}
    data = result.get("data") if isinstance(result.get("data"), Mapping) else {}
    packet_path = str(data.get("packet_path") or "")
    receipt["status"] = "completed"
    receipt["target_refs"].append({"provider": "local_ion", "path": packet_path, "role": "codex_work_request"})
    receipt["files_touched"].append(packet_path)
    receipt["validation"]["connector_result"] = {
        "request_id": data.get("request_id"),
        "packet_path": packet_path,
        "codex_work_queue_path": data.get("codex_work_queue_path"),
    }
    return {"ok": True, "request_id": data.get("request_id"), "packet_path": packet_path}


def _handle_create_github_issue_draft(root: Path, action: Mapping[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    github = action.get("github") if isinstance(action.get("github"), Mapping) else {}
    action_id = str(action.get("action_id") or "github_issue")
    draft_path = root / ARTIFACTS_DIR / "github_issue_drafts" / f"{_safe_slug(action_id)}.json"
    draft = {
        "schema_id": "ion.chatops.github_issue_draft.v1",
        "created_at": _now(),
        "github": dict(github),
        "source_action_id": action_id,
        "status": "draft_not_submitted",
        "production_authority": False,
        "live_execution_authority": False,
    }
    _write_json(draft_path, draft)
    rel = _repo_rel(draft_path, root)
    receipt["status"] = "completed"
    receipt["target_refs"].append({"provider": "github", "owner": github.get("owner"), "repo": github.get("repo"), "draft_path": rel})
    receipt["github_refs"].append({"owner": github.get("owner"), "repo": github.get("repo"), "title": github.get("title"), "status": "draft_not_submitted"})
    receipt["files_touched"].append(rel)
    receipt["sha256"][rel] = _sha256_file(draft_path)
    return {"ok": True, "draft_path": rel}


def _handle_register_artifact(root: Path, action: Mapping[str, Any], receipt: dict[str, Any]) -> dict[str, Any]:
    action_id = str(action.get("action_id") or "artifact")
    record_path = root / ARTIFACTS_DIR / "registered" / f"{_safe_slug(action_id)}.json"
    record = {
        "schema_id": "ion.chatops.registered_artifact.v1",
        "created_at": _now(),
        "source_action_id": action_id,
        "artifact_refs": list(action.get("artifact_refs") or []),
        "context_refs": list(action.get("context_refs") or []),
        "production_authority": False,
        "live_execution_authority": False,
    }
    _write_json(record_path, record)
    rel = _repo_rel(record_path, root)
    receipt["status"] = "completed"
    receipt["target_refs"].extend(record["artifact_refs"])
    receipt["files_touched"].append(rel)
    receipt["sha256"][rel] = _sha256_file(record_path)
    return {"ok": True, "record_path": rel}


def submit_chatops_action(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    action = _normalize_action(packet)
    validation = validate_chatops_action(packet, require_approval=True)
    approval = _approval_from_packet(packet, action)
    approved_by = str(approval.get("approved_by") or "") or None

    if not validation["accepted"]:
        receipt = _base_receipt(
            action=action or {"action_id": "invalid", "intent": "unknown"},
            status="rejected",
            approved_by=approved_by,
            failure_classification=(
                "USER_APPROVAL_REJECTED"
                if any("approval" in finding for finding in validation["findings"])
                else "CHATOPS_SCHEMA_FAILURE"
            ),
        )
        receipt["validation"] = validation
        receipt_path = _complete_receipt(shell_root, receipt)
        return {
            "schema_id": "ion.chatops.submit_result.v1",
            "ok": False,
            "verdict": BLOCKED_VERDICT,
            "finding": "validation_failed",
            "validation": validation,
            "receipt_path": receipt_path,
            "production_authority": False,
            "live_execution_authority": False,
        }

    action_path = _write_action_packet(shell_root, packet, action)
    receipt = _base_receipt(action=action, status="accepted", approved_by=approved_by)
    receipt["validation"]["action_validation"] = validation
    receipt["files_touched"].append(action_path)

    intent = _normalize_intent(action.get("intent"))
    if intent == "write_file_draft":
        execution = _handle_write_file_draft(shell_root, action, receipt)
    elif intent == "create_codex_work_packet":
        execution = _handle_create_codex_work_packet(shell_root, action, receipt)
    elif intent == "create_github_issue_draft":
        execution = _handle_create_github_issue_draft(shell_root, action, receipt)
    elif intent == "register_artifact":
        execution = _handle_register_artifact(shell_root, action, receipt)
    else:
        receipt["status"] = "failed"
        receipt["failure_classification"] = "POLICY_BLOCK_WORKING_AS_DESIGNED"
        execution = {"ok": False, "finding": "unsupported_intent"}

    receipt["validation"]["execution"] = execution
    receipt_path = _complete_receipt(shell_root, receipt)
    return {
        "schema_id": "ion.chatops.submit_result.v1",
        "ok": bool(execution.get("ok")),
        "verdict": READY_VERDICT if execution.get("ok") else BLOCKED_VERDICT,
        "action_id": action.get("action_id"),
        "intent": intent,
        "action_path": action_path,
        "receipt_path": receipt_path,
        "execution": execution,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _bridge_approval_from_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    approval = packet.get("approval")
    return dict(approval) if isinstance(approval, Mapping) else {}


def _validate_bridge_operation_approval(packet: Mapping[str, Any]) -> dict[str, Any]:
    approval = _bridge_approval_from_packet(packet)
    findings: list[str] = []
    if approval.get("approved") is not True:
        findings.append("approval_required")
    if approval.get("approved_by") != "Braden":
        findings.append("approval_must_be_by_Braden")
    if approval.get("approval_token") != APPROVAL_TOKEN:
        findings.append("approval_token_invalid")
    return {
        "schema_id": "ion.chatops.bridge_operation_approval.v1",
        "accepted": not findings,
        "findings": findings,
        "approved_by": approval.get("approved_by"),
        "production_authority": False,
        "live_execution_authority": False,
    }


def _rel_if_inside_root(root: Path, value: str | Path | None) -> str | None:
    if value is None:
        return None
    candidate = Path(value).expanduser()
    path = candidate if candidate.is_absolute() else root / candidate
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _operation_receipt_path(root: Path, receipt_id: str) -> Path:
    return root / RECEIPTS_DIR / f"{_safe_slug(receipt_id)}.json"


def _write_operation_receipt(
    root: Path,
    *,
    operation: str,
    status: str,
    packet: Mapping[str, Any],
    result: Mapping[str, Any],
    files_touched: list[str] | None = None,
    target_refs: list[Mapping[str, Any]] | None = None,
    failure_classification: str | None = None,
) -> str:
    approval = _bridge_approval_from_packet(packet)
    receipt_id = f"chatops_bridge_operation_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{_safe_slug(operation)}"
    receipt = {
        "schema_id": "ion.chatops.bridge_operation_receipt.v1",
        "receipt_id": receipt_id,
        "created_at": _now(),
        "operation": operation,
        "actor": {
            "callsign": "Sev",
            "carrier": "chatgpt_browser",
        },
        "approved_by": approval.get("approved_by"),
        "status": status,
        "target_refs": list(target_refs or []),
        "files_touched": list(files_touched or []),
        "validation": {
            "result": dict(result),
        },
        "failure_classification": failure_classification,
        "production_authority": False,
        "live_execution_authority": False,
    }
    path = _operation_receipt_path(root, receipt_id)
    _write_json(path, receipt)
    return _repo_rel(path, root)


def build_chatops_agent_status(root: str | Path | None = None, *, reconcile: bool = False) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    status = build_codex_queue_runner_status(shell_root, reconcile=reconcile)
    return {
        "schema_id": "ion.chatops.agent_status_projection.v1",
        "ok": True,
        "verdict": status.get("verdict"),
        "backend": "codex_cli",
        "runner_owner": "ION/04_packages/kernel/ion_codex_queue_runner.py",
        "queued_request_count": status.get("queued_request_count"),
        "next_request_path": status.get("next_request_path"),
        "active_run": status.get("active_run"),
        "active_process_running": status.get("active_process_running"),
        "stale_active_run_detected": status.get("stale_active_run_detected"),
        "latest_runs": status.get("latest_runs"),
        "failure_classes": [
            "AGENT_INVOCATION_FAILURE",
            "BACKEND_CODEX_FAILURE",
            "CARRIER_ADAPTER_FAILURE",
            "DAEMON_FAILURE",
            "ION_CORE_FAILURE",
        ],
        "runner_status": status,
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_chatops_agent_queue(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    queue_path = shell_root / "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json"
    queue = _read_json(queue_path) or {
        "schema_id": "ion.chatops.empty_codex_queue_projection.v1",
        "request_count": 0,
        "requests": [],
    }
    requests = queue.get("requests") if isinstance(queue.get("requests"), list) else []
    compact_requests: list[dict[str, Any]] = []
    for item in requests[:20]:
        if not isinstance(item, Mapping):
            continue
        compact_requests.append({
            "request_id": item.get("request_id"),
            "status": item.get("status"),
            "packet_path": item.get("packet_path"),
            "objective": str(item.get("objective") or "")[:240],
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
        })
    return {
        "schema_id": "ion.chatops.agent_queue_projection.v1",
        "ok": True,
        "queue_path": _repo_rel(queue_path, shell_root),
        "request_count": queue.get("request_count", len(compact_requests)),
        "requests": compact_requests,
        "raw_queue_present": queue_path.exists(),
        "production_authority": False,
        "live_execution_authority": False,
    }


def prepare_chatops_agent_next(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    approval = _validate_bridge_operation_approval(packet)
    if not approval["accepted"]:
        receipt_path = _write_operation_receipt(
            shell_root,
            operation="agent_prepare_next",
            status="rejected",
            packet=packet,
            result=approval,
            failure_classification="USER_APPROVAL_REJECTED",
        )
        return {
            "schema_id": "ion.chatops.agent_prepare_result.v1",
            "ok": False,
            "finding": "approval_failed",
            "approval": approval,
            "receipt_path": receipt_path,
            "production_authority": False,
            "live_execution_authority": False,
        }
    request_path = str(packet.get("request_path") or "").strip() or None
    result = prepare_codex_queue_run(shell_root, request_path=request_path, claim=False)
    run = result.get("run") if isinstance(result.get("run"), Mapping) else {}
    files = [
        str(run.get(key))
        for key in ("run_packet_path", "prompt_path", "context_receipt_path")
        if run.get(key)
    ]
    receipt_path = _write_operation_receipt(
        shell_root,
        operation="agent_prepare_next",
        status="completed" if result.get("ok") else "failed",
        packet=packet,
        result=result,
        files_touched=files,
        target_refs=[{"provider": "local_ion", "path": path, "role": "codex_queue_run"} for path in files],
        failure_classification=None if result.get("ok") else "AGENT_INVOCATION_FAILURE",
    )
    return {
        "schema_id": "ion.chatops.agent_prepare_result.v1",
        "ok": bool(result.get("ok")),
        "operation": "agent_prepare_next",
        "receipt_path": receipt_path,
        "result": result,
        "production_authority": False,
        "live_execution_authority": False,
    }


def process_chatops_agent_once(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    approval = _validate_bridge_operation_approval(packet)
    if not approval["accepted"]:
        receipt_path = _write_operation_receipt(
            shell_root,
            operation="agent_process_one",
            status="rejected",
            packet=packet,
            result=approval,
            failure_classification="USER_APPROVAL_REJECTED",
        )
        return {
            "schema_id": "ion.chatops.agent_process_result.v1",
            "ok": False,
            "finding": "approval_failed",
            "approval": approval,
            "receipt_path": receipt_path,
            "production_authority": False,
            "live_execution_authority": False,
        }
    request_path = str(packet.get("request_path") or "").strip() or None
    start = bool(packet.get("start"))
    timeout_seconds = int(packet.get("timeout_seconds") or 1800)
    result = process_codex_queue_once(
        shell_root,
        request_path=request_path,
        start=start,
        background=True,
        timeout_seconds=timeout_seconds,
    )
    run = result.get("run") if isinstance(result.get("run"), Mapping) else {}
    files = [
        str(run.get(key))
        for key in ("run_packet_path", "prompt_path", "context_receipt_path", "stdout_path", "stderr_path", "last_message_path")
        if run.get(key)
    ]
    receipt_path = _write_operation_receipt(
        shell_root,
        operation="agent_process_one_start" if start else "agent_process_one_prepare_only",
        status="completed" if result.get("ok") else "failed",
        packet=packet,
        result=result,
        files_touched=files,
        target_refs=[{"provider": "local_ion", "path": path, "role": "codex_queue_run"} for path in files],
        failure_classification=None if result.get("ok") else "BACKEND_CODEX_FAILURE",
    )
    return {
        "schema_id": "ion.chatops.agent_process_result.v1",
        "ok": bool(result.get("ok")),
        "operation": "agent_process_one_start" if start else "agent_process_one_prepare_only",
        "receipt_path": receipt_path,
        "result": result,
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_chatops_context_pack(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    sev_context = build_sev_context_brief(shell_root)
    agent_status = build_chatops_agent_status(shell_root)
    agent_queue = build_chatops_agent_queue(shell_root)
    latest_receipts = _latest_chatops_files(shell_root, RECEIPTS_DIR, limit=8)
    pack = {
        "schema": "ion.chatops.context_pack.v1",
        "generated_at": _now(),
        "root": shell_root.as_posix(),
        "callsign": "Sev",
        "carrier": "chatgpt_browser",
        "human_sovereign": "Braden",
        "ion_status": sev_context.get("brief", {}).get("ion_status"),
        "agent_status": {
            "queued_request_count": agent_status.get("queued_request_count"),
            "next_request_path": agent_status.get("next_request_path"),
            "active_process_running": agent_status.get("active_process_running"),
            "latest_runs": agent_status.get("latest_runs"),
        },
        "agent_queue": {
            "queue_path": agent_queue.get("queue_path"),
            "request_count": agent_queue.get("request_count"),
            "requests": agent_queue.get("requests"),
        },
        "latest_chatops_receipts": latest_receipts,
        "bridge_tools": {
            "onboard": "GET /context/sev/onboarding",
            "agent_status": "GET /agent/status",
            "agent_queue": "GET /agent/queue",
            "agent_prepare_next": "POST /agent/prepare-next with Braden approval",
            "agent_start_one": "POST /agent/process-one with start=true and Braden approval",
            "compact_zip": "POST /exports/lifecycle-zip with package_class=COMPACT_RUNTIME and Braden approval",
        },
        "authority": {
            "production_authority": False,
            "live_execution_authority": False,
            "git_push_main_authority": False,
            "secrets_authority": False,
        },
    }
    prompt = "\n".join([
        "ION local context pack from the ChatOps bridge.",
        "",
        "Use this as current repo/runtime context. For implementation work, emit one concrete ion_action YAML block with intent create_codex_work_packet, or ask Braden to use the Agent tab to prepare/start the local Codex queue runner.",
        "",
        "```json",
        json.dumps(pack, indent=2, sort_keys=True),
        "```",
    ])
    return {
        "schema_id": "ion.chatops.context_pack_response.v1",
        "ok": True,
        "verdict": READY_VERDICT,
        "pack": pack,
        "prompt": prompt,
        "production_authority": False,
        "live_execution_authority": False,
    }


def create_chatops_lifecycle_zip(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    approval = _validate_bridge_operation_approval(packet)
    if not approval["accepted"]:
        receipt_path = _write_operation_receipt(
            shell_root,
            operation="export_lifecycle_zip",
            status="rejected",
            packet=packet,
            result=approval,
            failure_classification="USER_APPROVAL_REJECTED",
        )
        return {"schema_id": "ion.chatops.export_result.v1", "ok": False, "finding": "approval_failed", "receipt_path": receipt_path}
    package_class = str(packet.get("package_class") or "COMPACT_RUNTIME").strip() or "COMPACT_RUNTIME"
    try:
        manifest = create_lifecycle_package_zip(shell_root, package_class=package_class, write_manifest=True)
        result = lifecycle_package_manifest_to_dict(manifest)
        zip_rel = _rel_if_inside_root(shell_root, result.get("zip_path"))
        files = [path for path in [zip_rel, result.get("context_lifecycle_audit_path")] if path]
        if result.get("zip_creation_performed") and result.get("zip_path"):
            status = "completed"
            failure = None
            ok = True
        else:
            status = "failed"
            failure = "POLICY_BLOCK_WORKING_AS_DESIGNED"
            ok = False
        receipt_path = _write_operation_receipt(
            shell_root,
            operation=f"export_lifecycle_zip_{package_class.lower()}",
            status=status,
            packet=packet,
            result=result,
            files_touched=list(files),
            target_refs=[{"provider": "local_ion", "path": zip_rel, "role": "package_zip"}] if zip_rel else [],
            failure_classification=failure,
        )
        return {
            "schema_id": "ion.chatops.export_result.v1",
            "ok": ok,
            "operation": "export_lifecycle_zip",
            "package_class": package_class,
            "receipt_path": receipt_path,
            "zip_path": zip_rel,
            "zip_sha256": result.get("zip_sha256"),
            "manifest": result,
            "production_authority": False,
            "live_execution_authority": False,
        }
    except Exception as exc:
        result = {"ok": False, "error": str(exc), "package_class": package_class}
        receipt_path = _write_operation_receipt(
            shell_root,
            operation=f"export_lifecycle_zip_{package_class.lower()}",
            status="failed",
            packet=packet,
            result=result,
            failure_classification="LOCAL_DAEMON_FAILURE",
        )
        return {"schema_id": "ion.chatops.export_result.v1", "ok": False, "finding": "package_failed", "error": str(exc), "receipt_path": receipt_path}


def create_chatops_safe_full_zip(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    approval = _validate_bridge_operation_approval(packet)
    if not approval["accepted"]:
        receipt_path = _write_operation_receipt(
            shell_root,
            operation="export_safe_full_zip",
            status="rejected",
            packet=packet,
            result=approval,
            failure_classification="USER_APPROVAL_REJECTED",
        )
        return {"schema_id": "ion.chatops.export_result.v1", "ok": False, "finding": "approval_failed", "receipt_path": receipt_path}
    try:
        result_obj = create_safe_full_project_package(shell_root)
        result = safe_full_project_package_result_to_dict(result_obj)
        zip_rel = _rel_if_inside_root(shell_root, result.get("zip_path"))
        files = [
            path
            for path in [
                zip_rel,
                _rel_if_inside_root(shell_root, result.get("baseline_manifest_path")),
                _rel_if_inside_root(shell_root, result.get("post_manifest_path")),
                _rel_if_inside_root(shell_root, result.get("preservation_report_path")),
            ]
            if path
        ]
        receipt_path = _write_operation_receipt(
            shell_root,
            operation="export_safe_full_zip",
            status="completed" if result.get("accepted") else "failed",
            packet=packet,
            result=result,
            files_touched=list(files),
            target_refs=[{"provider": "local_ion", "path": zip_rel, "role": "safe_full_project_zip"}] if zip_rel else [],
            failure_classification=None if result.get("accepted") else "POLICY_BLOCK_WORKING_AS_DESIGNED",
        )
        return {
            "schema_id": "ion.chatops.export_result.v1",
            "ok": bool(result.get("accepted")),
            "operation": "export_safe_full_zip",
            "receipt_path": receipt_path,
            "zip_path": zip_rel,
            "zip_sha256": result.get("zip_sha256"),
            "result": result,
            "production_authority": False,
            "live_execution_authority": False,
        }
    except Exception as exc:
        result = {"ok": False, "error": str(exc)}
        receipt_path = _write_operation_receipt(
            shell_root,
            operation="export_safe_full_zip",
            status="failed",
            packet=packet,
            result=result,
            failure_classification="LOCAL_DAEMON_FAILURE",
        )
        return {"schema_id": "ion.chatops.export_result.v1", "ok": False, "finding": "package_failed", "error": str(exc), "receipt_path": receipt_path}


def build_chatops_policy(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    owner_paths = {
        label: {"path": rel, "exists": (shell_root / rel).exists()}
        for label, rel in POLICY_PATHS.items()
    }
    return {
        "schema_id": "ion.chatops.policy_projection.v1",
        "verdict": READY_VERDICT if all(item["exists"] for item in owner_paths.values()) else BLOCKED_VERDICT,
        "owner_paths": owner_paths,
        "supported_mvp_intents": sorted(SUPPORTED_INTENTS),
        "hard_gated_intents": sorted(HARD_GATED_INTENTS),
        "approval_token": APPROVAL_TOKEN,
        "listen_host": DEFAULT_HOST,
        "listen_port": DEFAULT_PORT,
        "storage": {
            "actions": ACTIONS_DIR.as_posix(),
            "receipts": RECEIPTS_DIR.as_posix(),
            "runtime": RUNTIME_DIR.as_posix(),
            "artifacts": ARTIFACTS_DIR.as_posix(),
            "exports": EXPORTS_DIR.as_posix(),
        },
        "agent_surface": {
            "status": "GET /agent/status",
            "queue": "GET /agent/queue",
            "prepare_next": "POST /agent/prepare-next",
            "process_one": "POST /agent/process-one",
            "backend_owner": "ION/04_packages/kernel/ion_codex_queue_runner.py",
        },
        "export_surface": {
            "context_pack": "GET /exports/context-pack",
            "compact_runtime_zip": "POST /exports/lifecycle-zip",
            "safe_full_project_zip": "POST /exports/safe-full-zip",
            "packager_owners": [
                "ION/04_packages/kernel/ion_lifecycle_packager.py",
                "ION/04_packages/kernel/ion_safe_full_project_packager.py",
            ],
        },
        "main_policy": {
            "main_auto_push_allowed": False,
            "scoped_branch_push_allowed": "policy_gated_later",
            "allowed_branch_prefixes": ["work/", "docs/", "agent/", "data-plane/", "sev/"],
        },
        "production_authority": False,
        "live_execution_authority": False,
    }


def _active_file_exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def _latest_chatops_files(root: Path, rel: Path, *, limit: int = 5) -> list[dict[str, Any]]:
    base = root / rel
    if not base.exists():
        return []
    paths = sorted((path for path in base.glob("*.json") if path.is_file()), key=lambda path: path.stat().st_mtime, reverse=True)
    return [
        {
            "path": _repo_rel(path, root),
            "name": path.name,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
        }
        for path in paths[:limit]
    ]


def _queue_item_count(value: Mapping[str, Any] | None) -> int:
    if not value:
        return 0
    for key in ("items", "requests", "messages", "records"):
        items = value.get(key)
        if isinstance(items, list):
            return len(items)
    for key in ("request_count", "count", "total"):
        count = value.get(key)
        if isinstance(count, int):
            return count
    return 0


def _brief_yaml_lines(value: Mapping[str, Any], *, indent: int = 0) -> list[str]:
    lines: list[str] = []
    prefix = " " * indent
    for key, item in value.items():
        if isinstance(item, Mapping):
            lines.append(f"{prefix}{key}:")
            lines.extend(_brief_yaml_lines(item, indent=indent + 2))
        elif isinstance(item, list):
            lines.append(f"{prefix}{key}:")
            for row in item:
                if isinstance(row, Mapping):
                    lines.append(f"{prefix}  -")
                    lines.extend(_brief_yaml_lines(row, indent=indent + 4))
                else:
                    lines.append(f"{prefix}  - {json.dumps(row)}")
        else:
            lines.append(f"{prefix}{key}: {json.dumps(item)}")
    return lines


def build_sev_context_brief(root: str | Path | None = None) -> dict[str, Any]:
    """Build a compact browser-carrier onboarding prompt for Sev.

    This is a read-only projection for the extension. It does not grant new
    authority and does not execute actions; it gives ChatGPT Browser enough ION
    state to ask for the next action through the normal YAML/approval path.
    """

    shell_root = _resolve_root(root)
    status = build_ion_status(shell_root)
    onboarding = build_carrier_onboarding_packet(shell_root, carrier_id="sev", include_excerpts=False)
    policy = build_chatops_policy(shell_root)
    codex_queue = _read_json(shell_root / "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json")
    carrier_messages = _read_json(shell_root / "ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json")

    active_paths = [
        "ION/05_context/current/ACTIVE_WORK_PACKET.json",
        "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.sev.json",
        "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
        "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json",
        "ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json",
        "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
        "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
    ]
    brief = {
        "schema": "ion.chatops.sev_context_brief.v1",
        "generated_at": _now(),
        "callsign": "Sev",
        "carrier": "chatgpt_browser",
        "human_sovereign": "Braden",
        "root": shell_root.as_posix(),
        "ion_status": {
            "verdict": status.get("verdict"),
            "objective": status.get("objective"),
            "next_lawful_action": status.get("next_lawful_action"),
            "spawn_queue_count": status.get("spawn_queue_count"),
            "plan_spawn_count": status.get("plan_spawn_count"),
            "deferred_spawn_count": status.get("deferred_spawn_count"),
            "operator_queue_counts": status.get("operator_queue_counts"),
        },
        "carrier_onboarding": {
            "verdict": onboarding.get("onboarding_verdict"),
            "profile_path": (onboarding.get("carrier_profile") or {}).get("path"),
            "project_facing_callsign": (onboarding.get("carrier_profile_metadata") or {}).get("project_facing_callsign"),
            "proof_flow": [row.get("step") for row in onboarding.get("proof_flow", []) if isinstance(row, Mapping)],
        },
        "queues": {
            "codex_work_request_count": _queue_item_count(codex_queue),
            "carrier_message_count": _queue_item_count(carrier_messages),
        },
        "active_paths": [
            {"path": rel, "exists": _active_file_exists(shell_root, rel)}
            for rel in active_paths
        ],
        "chatops": {
            "daemon": "http://127.0.0.1:8767",
            "supported_intents": policy.get("supported_mvp_intents"),
            "hard_gated_intents": policy.get("hard_gated_intents"),
            "normal_flow": "emit one YAML/code block whose first YAML key is ion_action; extension validates; Braden approves; daemon records/executes; ION writes receipt",
        },
        "authority": {
            "production_authority": False,
            "live_execution_authority": False,
            "git_push_main_authority": False,
            "secrets_authority": False,
        },
    }
    prompt = "\n".join(
        [
            "You are Sev, Braden's ION browser carrier.",
            "",
            "Do not rely on chat memory. The local ION ChatOps bridge supplied this current carrier context from the repo.",
            "Use it as onboarding context, then continue by emitting exactly one YAML/code block whenever ION should act.",
            "The first YAML key of a runnable action block must be ion_action. Literal triple-backtick characters are not required; ChatGPT may render the YAML as a styled code block.",
            "Do not describe an action block instead of rendering the YAML block.",
            "",
            "```yaml",
            "ion_reentry:",
            *_brief_yaml_lines(brief, indent=2),
            "```",
            "",
            "When you need implementation work, emit a fresh action block with a concrete action_id and objective.",
            "The following is a non-runnable schema reminder; do not copy placeholder values from it:",
            "",
            "```yaml",
            "ion_action_example:",
            "  schema: ion.chatops.action.v1",
            "  action_id: sev-20260505-123456-concrete-short-slug",
            "  intent: create_codex_work_packet",
            "  callsign: Sev",
            "  carrier: chatgpt_browser",
            "  human_sovereign: Braden",
            "  requires_approval: true",
            "  production_authority: false",
            "  live_execution_authority: false",
            "  objective: \"A concrete bounded task for local Codex/ION to perform.\"",
            "```",
        ]
    )
    return {
        "schema_id": "ion.chatops.sev_context_brief_response.v1",
        "ok": True,
        "verdict": READY_VERDICT,
        "brief": brief,
        "prompt": prompt,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _http_response(handler: BaseHTTPRequestHandler, status: int, payload: Mapping[str, Any]) -> None:
    body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "https://chatgpt.com")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.end_headers()
    handler.wfile.write(body)


def make_handler(root: Path) -> type[BaseHTTPRequestHandler]:
    class ChatOpsHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - stdlib signature
            return

        def do_OPTIONS(self) -> None:  # noqa: N802 - stdlib handler name
            _http_response(self, 200, {"ok": True})

        def do_GET(self) -> None:  # noqa: N802 - stdlib handler name
            path = self.path.split("?", 1)[0]
            if path == "/health":
                _http_response(self, 200, {"ok": True, "schema_id": SCHEMA_ID, "verdict": READY_VERDICT})
                return
            if path == "/policy":
                _http_response(self, 200, build_chatops_policy(root))
                return
            if path == "/context/sev/onboarding":
                _http_response(self, 200, build_sev_context_brief(root))
                return
            if path == "/agent/status":
                _http_response(self, 200, build_chatops_agent_status(root))
                return
            if path == "/agent/queue":
                _http_response(self, 200, build_chatops_agent_queue(root))
                return
            if path == "/exports/context-pack":
                _http_response(self, 200, build_chatops_context_pack(root))
                return
            if path.startswith("/actions/"):
                action_id = path.rsplit("/", 1)[-1]
                payload = _read_json(_action_path(root, action_id))
                _http_response(self, 200 if payload else 404, payload or {"ok": False, "finding": "action_not_found"})
                return
            if path.startswith("/receipts/"):
                receipt_id = path.rsplit("/", 1)[-1]
                payload = _read_json(_receipt_path(root, receipt_id))
                _http_response(self, 200 if payload else 404, payload or {"ok": False, "finding": "receipt_not_found"})
                return
            _http_response(self, 404, {"ok": False, "finding": "not_found"})

        def do_POST(self) -> None:  # noqa: N802 - stdlib handler name
            try:
                length = int(self.headers.get("Content-Length") or "0")
                raw = self.rfile.read(length).decode("utf-8", errors="replace")
                packet = json.loads(raw or "{}")
            except Exception as exc:
                _http_response(self, 400, {"ok": False, "finding": "invalid_json", "error": str(exc)})
                return
            if not isinstance(packet, Mapping):
                _http_response(self, 400, {"ok": False, "finding": "json_object_required"})
                return
            path = self.path.split("?", 1)[0]
            if path == "/actions/validate":
                _http_response(self, 200, validate_chatops_action(packet, require_approval=False))
                return
            if path == "/actions/submit":
                result = submit_chatops_action(root, packet)
                _http_response(self, 200 if result.get("ok") else 409, result)
                return
            if path == "/agent/prepare-next":
                result = prepare_chatops_agent_next(root, packet)
                _http_response(self, 200 if result.get("ok") else 409, result)
                return
            if path == "/agent/process-one":
                result = process_chatops_agent_once(root, packet)
                _http_response(self, 200 if result.get("ok") else 409, result)
                return
            if path == "/exports/lifecycle-zip":
                result = create_chatops_lifecycle_zip(root, packet)
                _http_response(self, 200 if result.get("ok") else 409, result)
                return
            if path == "/exports/safe-full-zip":
                result = create_chatops_safe_full_zip(root, packet)
                _http_response(self, 200 if result.get("ok") else 409, result)
                return
            _http_response(self, 404, {"ok": False, "finding": "not_found"})

    return ChatOpsHandler


def run_server(root: str | Path | None = None, *, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    shell_root = _resolve_root(root)
    server = ThreadingHTTPServer((host, port), make_handler(shell_root))
    server.serve_forever()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ION ChatOps localhost bridge.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--policy", action="store_true")
    parser.add_argument("--validate-json", default=None)
    parser.add_argument("--submit-json", default=None)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.policy:
        print(json.dumps(build_chatops_policy(args.ion_root), indent=2, sort_keys=True))
        return 0
    if args.validate_json:
        packet = json.loads(Path(args.validate_json).read_text(encoding="utf-8"))
        result = validate_chatops_action(packet, require_approval=False)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["accepted"] else 1
    if args.submit_json:
        packet = json.loads(Path(args.submit_json).read_text(encoding="utf-8"))
        result = submit_chatops_action(args.ion_root, packet)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["ok"] else 1
    if args.serve:
        run_server(args.ion_root, host=args.host, port=args.port)
        return 0
    result = build_chatops_policy(args.ion_root)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result["verdict"])
    return 0 if result["verdict"] == READY_VERDICT else 1


if __name__ == "__main__":
    raise SystemExit(main())
