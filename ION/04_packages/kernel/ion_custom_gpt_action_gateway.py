"""ION Custom GPT Action Gateway.

The gateway is a public-facing local membrane for Custom GPT Actions. It adds
auth, payload, idempotency, approval, refusal, and gateway receipt checks before
delegating action validation/submission to the existing ChatOps owners.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qs, urlparse

from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_chatops_bridge import (
    APPROVAL_TOKEN as CHATOPS_APPROVAL_TOKEN,
    HARD_GATED_INTENTS as CHATOPS_HARD_GATED_INTENTS,
    SUPPORTED_INTENTS as CHATOPS_SUPPORTED_INTENTS,
    build_chatops_agent_queue,
    build_chatops_agent_status,
    build_chatops_context_pack,
    build_chatops_policy,
    submit_chatops_action,
    validate_chatops_action,
)
from .ion_codex_queue_runner import build_codex_queue_runner_status
from .ion_assistant_work_route_compiler import compile_assistant_work_route

SCHEMA_ID = "ion.custom_gpt_action_gateway.v1"
READY_VERDICT = "ION_CUSTOM_GPT_ACTION_GATEWAY_READY"
BLOCKED_VERDICT = "ION_CUSTOM_GPT_ACTION_GATEWAY_BLOCKED"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8777
POLICY_RELATIVE_PATH = Path("ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml")
OPENAPI_RELATIVE_PATH = Path("ION/09_integrations/custom_gpt_action_gateway/openapi.yaml")
RECEIPTS_DIR = Path("ION/05_context/current/action_gateway/receipts")
RUNTIME_DIR = Path("ION/05_context/current/action_gateway/runtime")
IDEMPOTENCY_LEDGER = RUNTIME_DIR / "idempotency_ledger.json"
MAX_BODY_BYTES_DEFAULT = 262144

REFUSAL_CLASSES = (
    "AUTH_MISSING",
    "AUTH_INVALID",
    "IDEMPOTENCY_KEY_REQUIRED",
    "IDEMPOTENCY_REPLAY_BLOCKED",
    "PAYLOAD_TOO_LARGE",
    "ENDPOINT_NOT_ALLOWED",
    "INTENT_NOT_SUPPORTED",
    "INTENT_HARD_GATED",
    "PRODUCTION_AUTHORITY_REFUSED",
    "LIVE_EXECUTION_AUTHORITY_REFUSED",
    "OPERATOR_APPROVAL_REQUIRED",
    "APPROVAL_EVIDENCE_INVALID",
    "PATH_NOT_ALLOWED",
    "SCHEMA_INVALID",
    "LOCAL_DAEMON_UNAVAILABLE",
    "ION_OWNER_REFUSED",
    "STEWARD_GATE_REQUIRED",
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:96] or "gateway"


def _resolve_root(root: str | Path | None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    return resolve_shell_root_from_ion_root(root)


def _repo_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "null":
        return None
    if value.isdigit():
        return int(value)
    return value.strip("\"'")


def _parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse the small registry YAML subset used by this policy file."""

    result: dict[str, Any] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()
        if indent == 0:
            if stripped.endswith(":"):
                current_key = stripped[:-1]
                result[current_key] = {}
            elif ":" in stripped:
                key, value = stripped.split(":", 1)
                current_key = key.strip()
                result[current_key] = _parse_scalar(value)
            continue
        if current_key is None:
            continue
        if stripped.startswith("- "):
            if not isinstance(result.get(current_key), list):
                result[current_key] = []
            result[current_key].append(_parse_scalar(stripped[2:]))
            continue
        if ":" in stripped:
            if not isinstance(result.get(current_key), dict):
                result[current_key] = {}
            key, value = stripped.split(":", 1)
            result[current_key][key.strip()] = _parse_scalar(value)
    return result


def _default_policy() -> dict[str, Any]:
    return {
        "schema_id": "ion.custom_gpt_action_gateway_policy.v1",
        "status": "draft_non_production",
        "production_authority": False,
        "live_execution_authority": False,
        "listen_host": DEFAULT_HOST,
        "listen_port": DEFAULT_PORT,
        "public_transport": "cloudflare_tunnel",
        "auth": {
            "required": True,
            "scheme": "bearer",
            "token_env_var": "ION_ACTION_GATEWAY_TOKEN",
            "token_sha256_env_var": "ION_ACTION_GATEWAY_TOKEN_SHA256",
        },
        "limits": {
            "max_body_bytes": MAX_BODY_BYTES_DEFAULT,
            "require_idempotency_key_for_mutation": True,
        },
        "allowed_get_paths": ["/health", "/policy", "/context-pack", "/codex/queue", "/agent/status", "/receipts/recent"],
        "allowed_post_paths": ["/actions/validate", "/actions/submit"],
        "supported_mvp_intents": sorted(CHATOPS_SUPPORTED_INTENTS),
        "hard_gated_intents": sorted(CHATOPS_HARD_GATED_INTENTS),
        "refusal_classes": list(REFUSAL_CLASSES),
        "storage": {
            "receipts": RECEIPTS_DIR.as_posix() + "/",
            "runtime": RUNTIME_DIR.as_posix() + "/",
        },
    }


def load_gateway_policy(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    policy_path = shell_root / POLICY_RELATIVE_PATH
    policy = _default_policy()
    if policy_path.exists():
        parsed = _parse_simple_yaml(policy_path.read_text(encoding="utf-8"))
        for key, value in parsed.items():
            if isinstance(value, dict) and isinstance(policy.get(key), dict):
                merged = dict(policy[key])
                merged.update(value)
                policy[key] = merged
            else:
                policy[key] = value
    policy["policy_path"] = POLICY_RELATIVE_PATH.as_posix()
    return policy


def build_gateway_health(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    policy = load_gateway_policy(shell_root)
    return {
        "schema_id": "ion.custom_gpt_action_gateway_health.v1",
        "ok": True,
        "verdict": READY_VERDICT,
        "status": policy.get("status"),
        "gateway": "ion_custom_gpt_action_gateway",
        "policy_path": POLICY_RELATIVE_PATH.as_posix(),
        "listen_host": policy.get("listen_host"),
        "listen_port": policy.get("listen_port"),
        "public_transport": policy.get("public_transport"),
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_gateway_policy_surface(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    policy = load_gateway_policy(shell_root)
    chatops_policy = build_chatops_policy(shell_root)
    auth = policy.get("auth") if isinstance(policy.get("auth"), Mapping) else {}
    safe_auth = {
        "required": bool(auth.get("required", True)),
        "scheme": auth.get("scheme") or "bearer",
        "token_env_var": auth.get("token_env_var") or "ION_ACTION_GATEWAY_TOKEN",
        "token_sha256_env_var": auth.get("token_sha256_env_var") or "ION_ACTION_GATEWAY_TOKEN_SHA256",
        "token_configured": bool(os.environ.get(str(auth.get("token_env_var") or "ION_ACTION_GATEWAY_TOKEN"))),
        "token_sha256_configured": bool(os.environ.get(str(auth.get("token_sha256_env_var") or "ION_ACTION_GATEWAY_TOKEN_SHA256"))),
    }
    return {
        "schema_id": "ion.custom_gpt_action_gateway_policy_surface.v1",
        "verdict": READY_VERDICT,
        "policy_path": POLICY_RELATIVE_PATH.as_posix(),
        "status": policy.get("status"),
        "auth": safe_auth,
        "limits": policy.get("limits"),
        "allowed_get_paths": policy.get("allowed_get_paths"),
        "allowed_post_paths": policy.get("allowed_post_paths"),
        "supported_mvp_intents": policy.get("supported_mvp_intents"),
        "hard_gated_intents": policy.get("hard_gated_intents"),
        "imported_chatops_hard_gated_intents": chatops_policy.get("hard_gated_intents"),
        "imported_chatops_supported_mvp_intents": chatops_policy.get("supported_mvp_intents"),
        "chatops_owner_verdict": chatops_policy.get("verdict"),
        "owner_paths": {
            "gateway_policy": {"path": POLICY_RELATIVE_PATH.as_posix(), "exists": (shell_root / POLICY_RELATIVE_PATH).exists()},
            "gateway_module": {"path": "ION/04_packages/kernel/ion_custom_gpt_action_gateway.py", "exists": True},
            "chatops_bridge": {"path": "ION/04_packages/kernel/ion_chatops_bridge.py", "exists": (shell_root / "ION/04_packages/kernel/ion_chatops_bridge.py").exists()},
            "codex_queue_runner": {"path": "ION/04_packages/kernel/ion_codex_queue_runner.py", "exists": (shell_root / "ION/04_packages/kernel/ion_codex_queue_runner.py").exists()},
            "agent_invocation_broker": {"path": "ION/04_packages/kernel/ion_agent_invocation_broker.py", "exists": (shell_root / "ION/04_packages/kernel/ion_agent_invocation_broker.py").exists()},
        },
        "refusal_classes": list(REFUSAL_CLASSES),
        "production_authority": False,
        "live_execution_authority": False,
    }


def _headers_get(headers: Mapping[str, Any], name: str) -> str:
    target = name.lower()
    for key, value in headers.items():
        if str(key).lower() == target:
            return str(value or "")
    return ""


def validate_gateway_auth(headers: Mapping[str, Any], policy: Mapping[str, Any]) -> dict[str, Any]:
    auth = policy.get("auth") if isinstance(policy.get("auth"), Mapping) else {}
    if auth.get("required") is False:
        return {"ok": True, "refusal_class": None, "finding": None}

    raw_header = _headers_get(headers, "authorization").strip()
    if not raw_header:
        return {"ok": False, "refusal_class": "AUTH_MISSING", "finding": "authorization_header_required"}
    prefix = "Bearer "
    if not raw_header.startswith(prefix):
        return {"ok": False, "refusal_class": "AUTH_INVALID", "finding": "bearer_authorization_required"}
    supplied = raw_header[len(prefix):].strip()
    token_env_var = str(auth.get("token_env_var") or "ION_ACTION_GATEWAY_TOKEN")
    token_sha_env_var = str(auth.get("token_sha256_env_var") or "ION_ACTION_GATEWAY_TOKEN_SHA256")
    expected_token = os.environ.get(token_env_var)
    expected_sha = os.environ.get(token_sha_env_var)
    if expected_token:
        ok = hmac.compare_digest(supplied, expected_token)
    elif expected_sha:
        ok = hmac.compare_digest(hashlib.sha256(supplied.encode("utf-8")).hexdigest(), expected_sha)
    else:
        return {"ok": False, "refusal_class": "AUTH_MISSING", "finding": "gateway_token_not_configured"}
    if not ok:
        return {"ok": False, "refusal_class": "AUTH_INVALID", "finding": "gateway_token_invalid"}
    return {"ok": True, "refusal_class": None, "finding": None}


def _normalize_packet_for_chatops(packet: Mapping[str, Any]) -> dict[str, Any]:
    normalized = dict(packet)
    if "ion_action" not in normalized and isinstance(normalized.get("action"), Mapping):
        action = normalized["action"]
        normalized["ion_action"] = action.get("ion_action") if isinstance(action.get("ion_action"), Mapping) else action
    approval = normalized.get("approval")
    evidence = normalized.get("operator_approval_evidence")
    if not isinstance(approval, Mapping) and isinstance(evidence, Mapping):
        normalized["approval"] = dict(evidence)
    return normalized


def _action_mapping(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    normalized = _normalize_packet_for_chatops(packet)
    action = normalized.get("ion_action")
    if isinstance(action, Mapping):
        return action
    nested = normalized.get("action")
    if isinstance(nested, Mapping):
        nested_action = nested.get("ion_action")
        return nested_action if isinstance(nested_action, Mapping) else nested
    return {}


def _intent(packet: Mapping[str, Any]) -> str:
    return str(_action_mapping(packet).get("intent") or "").strip()


def _authority(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    action = _action_mapping(packet)
    authority = action.get("authority")
    if isinstance(authority, Mapping):
        return authority
    return action


def _route_preview_text(packet: Mapping[str, Any]) -> str:
    action = _action_mapping(packet)
    refs = action.get("artifact_refs") if isinstance(action.get("artifact_refs"), list) else []
    ref_paths = [
        str(ref.get("path") or ref.get("uri") or "")
        for ref in refs
        if isinstance(ref, Mapping)
    ]
    context_refs = action.get("context_refs") if isinstance(action.get("context_refs"), list) else []
    return "\n".join(
        part
        for part in [
            f"intent: {_intent(packet)}",
            f"action_id: {action.get('action_id') or packet.get('action_id') or ''}",
            str(action.get("objective") or action.get("summary") or action.get("description") or packet.get("objective") or packet.get("message") or ""),
            "artifact_refs: " + ", ".join(path for path in ref_paths if path),
            "context_refs: " + ", ".join(str(ref) for ref in context_refs if ref),
        ]
        if part.strip()
    )


def _gateway_route_preview(root: Path, packet: Mapping[str, Any], *, validated: bool) -> dict[str, Any]:
    intent = _intent(packet)
    response_mode = "queue_work" if intent in {"write_file_draft", "create_codex_work_packet", "create_github_issue_draft"} else "answer"
    selected_skill = "codex-solo-work" if response_mode == "queue_work" else "codex-chat-answer"
    route = compile_assistant_work_route(
        root,
        lane_id="custom_gpt_action_gateway",
        message=_route_preview_text(packet),
        response_mode=response_mode,
        selected_skill_id=selected_skill,
        execution_mode="validate_only",
    )
    route["gateway_validation_only"] = True
    route["gateway_packet_validated"] = validated
    route["policy"] = "candidate_route_metadata_only_no_registry_or_product_law_mutation"
    return route


def validate_gateway_request_envelope(packet: Mapping[str, Any], *, mutation: bool) -> dict[str, Any]:
    findings: list[str] = []
    refusal_class: str | None = None
    authority = _authority(packet)
    if packet.get("production_authority") is True or authority.get("production_authority") is not False:
        findings.append("production_authority_refused")
        refusal_class = "PRODUCTION_AUTHORITY_REFUSED"
    if packet.get("live_execution_authority") is True or authority.get("live_execution_authority") is not False:
        findings.append("live_execution_authority_refused")
        refusal_class = refusal_class or "LIVE_EXECUTION_AUTHORITY_REFUSED"
    if mutation and not str(packet.get("idempotency_key") or "").strip():
        findings.append("idempotency_key_required")
        refusal_class = refusal_class or "IDEMPOTENCY_KEY_REQUIRED"
    action = _action_mapping(packet)
    if not action:
        findings.append("ion_action_required")
        refusal_class = refusal_class or "SCHEMA_INVALID"
    return {
        "schema_id": "ion.custom_gpt_action_gateway_envelope_validation.v1",
        "accepted": not findings,
        "findings": findings,
        "refusal_class": refusal_class,
        "mutation": mutation,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _map_chatops_validation_refusal(validation: Mapping[str, Any], packet: Mapping[str, Any]) -> str | None:
    findings = [str(item) for item in validation.get("findings", []) if item]
    intent = _intent(packet)
    if intent in CHATOPS_HARD_GATED_INTENTS or any(item.startswith("hard_gated_intent:") for item in findings):
        return "INTENT_HARD_GATED"
    if any(item.startswith("unsupported_intent:") for item in findings):
        return "INTENT_NOT_SUPPORTED"
    if "production_authority_must_be_false" in findings:
        return "PRODUCTION_AUTHORITY_REFUSED"
    if "live_execution_authority_must_be_false" in findings:
        return "LIVE_EXECUTION_AUTHORITY_REFUSED"
    if any("path" in item for item in findings):
        return "PATH_NOT_ALLOWED"
    if findings:
        return "SCHEMA_INVALID"
    return None


def validate_gateway_action_packet(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    envelope = validate_gateway_request_envelope(packet, mutation=False)
    chatops_packet = _normalize_packet_for_chatops(packet)
    chatops_validation = validate_chatops_action(chatops_packet, require_approval=False) if envelope["accepted"] else None
    refusal = envelope.get("refusal_class")
    if chatops_validation and not chatops_validation.get("accepted"):
        refusal = _map_chatops_validation_refusal(chatops_validation, chatops_packet)
    accepted = bool(envelope["accepted"] and chatops_validation and chatops_validation.get("accepted"))
    assistant_work_route = _gateway_route_preview(shell_root, chatops_packet, validated=accepted)
    return {
        "schema_id": "ion.custom_gpt_action_gateway_validation.v1",
        "ok": accepted,
        "verdict": READY_VERDICT if accepted else BLOCKED_VERDICT,
        "action_id": chatops_validation.get("action_id") if isinstance(chatops_validation, Mapping) else None,
        "intent": chatops_validation.get("intent") if isinstance(chatops_validation, Mapping) else _intent(chatops_packet),
        "gateway_envelope": envelope,
        "chatops_validation": chatops_validation,
        "assistant_work_route": assistant_work_route,
        "refusal_class": None if accepted else (refusal or "SCHEMA_INVALID"),
        "owner": "ION/04_packages/kernel/ion_chatops_bridge.py",
        "validated_without_mutation": True,
        "root": shell_root.as_posix(),
        "production_authority": False,
        "live_execution_authority": False,
    }


def _approval_evidence(packet: Mapping[str, Any]) -> Mapping[str, Any]:
    approval = packet.get("approval")
    if isinstance(approval, Mapping):
        return approval
    evidence = packet.get("operator_approval_evidence")
    return evidence if isinstance(evidence, Mapping) else {}


def _validate_operator_approval(packet: Mapping[str, Any]) -> dict[str, Any]:
    evidence = _approval_evidence(packet)
    findings: list[str] = []
    if not evidence:
        findings.append("operator_approval_evidence_required")
        refusal = "OPERATOR_APPROVAL_REQUIRED"
    else:
        refusal = "APPROVAL_EVIDENCE_INVALID"
        if evidence.get("approved") is not True:
            findings.append("approval_must_be_true")
        if evidence.get("approved_by") != "Braden":
            findings.append("approval_must_be_by_Braden")
        if evidence.get("approval_token") != CHATOPS_APPROVAL_TOKEN:
            findings.append("approval_token_invalid")
    return {
        "schema_id": "ion.custom_gpt_action_gateway_approval_validation.v1",
        "accepted": not findings,
        "findings": findings,
        "refusal_class": None if not findings else refusal,
        "approved_by": evidence.get("approved_by") if evidence else None,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _receipt_path(root: Path, receipt_id: str) -> Path:
    return root / RECEIPTS_DIR / f"{_safe_slug(receipt_id)}.json"


def _unique_receipt_path(root: Path, receipt_id: str) -> Path:
    path = _receipt_path(root, receipt_id)
    counter = 1
    while path.exists():
        path = _receipt_path(root, f"{receipt_id}_{counter}")
        counter += 1
    return path


def _write_gateway_receipt(
    root: Path,
    *,
    operation: str,
    status: str,
    packet: Mapping[str, Any] | None,
    result: Mapping[str, Any],
    refusal_class: str | None = None,
) -> str:
    action = _action_mapping(packet or {})
    action_id = str(action.get("action_id") or "unknown")
    receipt_id = f"action_gateway_receipt_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{_safe_slug(operation)}_{_safe_slug(action_id)}"
    receipt = {
        "schema_id": "ion.custom_gpt_action_gateway_receipt.v1",
        "receipt_id": receipt_id,
        "created_at": _now(),
        "operation": operation,
        "status": status,
        "action_id": action_id,
        "intent": action.get("intent"),
        "idempotency_key": (packet or {}).get("idempotency_key"),
        "refusal_class": refusal_class,
        "result": dict(result),
        "production_authority": False,
        "live_execution_authority": False,
    }
    path = _unique_receipt_path(root, receipt_id)
    _write_json(path, receipt)
    return _repo_rel(path, root)


def _load_idempotency_ledger(root: Path) -> dict[str, Any]:
    return _read_json(root / IDEMPOTENCY_LEDGER) or {
        "schema_id": "ion.custom_gpt_action_gateway_idempotency_ledger.v1",
        "entries": {},
        "production_authority": False,
        "live_execution_authority": False,
    }


def _idempotency_entry(root: Path, key: str) -> Mapping[str, Any] | None:
    ledger = _load_idempotency_ledger(root)
    entries = ledger.get("entries") if isinstance(ledger.get("entries"), Mapping) else {}
    entry = entries.get(key)
    return entry if isinstance(entry, Mapping) else None


def _record_idempotency(root: Path, key: str, *, receipt_path: str, result: Mapping[str, Any]) -> None:
    ledger = _load_idempotency_ledger(root)
    entries = dict(ledger.get("entries") if isinstance(ledger.get("entries"), Mapping) else {})
    entries[key] = {
        "recorded_at": _now(),
        "receipt_path": receipt_path,
        "ok": bool(result.get("ok")),
        "action_id": result.get("action_id"),
        "intent": result.get("intent"),
    }
    ledger["entries"] = entries
    ledger["updated_at"] = _now()
    _write_json(root / IDEMPOTENCY_LEDGER, ledger)


def submit_gateway_action_packet(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    envelope = validate_gateway_request_envelope(packet, mutation=True)
    if not envelope["accepted"]:
        receipt_path = _write_gateway_receipt(
            shell_root,
            operation="actions_submit",
            status="rejected",
            packet=packet,
            result=envelope,
            refusal_class=str(envelope.get("refusal_class") or "SCHEMA_INVALID"),
        )
        return {
            "schema_id": "ion.custom_gpt_action_gateway_submit.v1",
            "ok": False,
            "verdict": BLOCKED_VERDICT,
            "finding": "gateway_envelope_refused",
            "refusal_class": envelope.get("refusal_class"),
            "gateway_receipt_path": receipt_path,
            "gateway_envelope": envelope,
            "production_authority": False,
            "live_execution_authority": False,
        }

    key = str(packet.get("idempotency_key") or "").strip()
    existing = _idempotency_entry(shell_root, key)
    if existing:
        result = {
            "schema_id": "ion.custom_gpt_action_gateway_replay_refusal.v1",
            "ok": False,
            "finding": "idempotency_key_replayed",
            "existing": dict(existing),
            "production_authority": False,
            "live_execution_authority": False,
        }
        receipt_path = _write_gateway_receipt(
            shell_root,
            operation="actions_submit",
            status="rejected",
            packet=packet,
            result=result,
            refusal_class="IDEMPOTENCY_REPLAY_BLOCKED",
        )
        return {
            "schema_id": "ion.custom_gpt_action_gateway_submit.v1",
            "ok": False,
            "verdict": BLOCKED_VERDICT,
            "finding": "idempotency_replay_blocked",
            "refusal_class": "IDEMPOTENCY_REPLAY_BLOCKED",
            "gateway_receipt_path": receipt_path,
            "existing": dict(existing),
            "production_authority": False,
            "live_execution_authority": False,
        }

    validation = validate_gateway_action_packet(shell_root, packet)
    if not validation["ok"]:
        receipt_path = _write_gateway_receipt(
            shell_root,
            operation="actions_submit",
            status="rejected",
            packet=packet,
            result=validation,
            refusal_class=str(validation.get("refusal_class") or "SCHEMA_INVALID"),
        )
        return {
            "schema_id": "ion.custom_gpt_action_gateway_submit.v1",
            "ok": False,
            "verdict": BLOCKED_VERDICT,
            "finding": "gateway_validation_refused",
            "refusal_class": validation.get("refusal_class"),
            "gateway_receipt_path": receipt_path,
            "validation": validation,
            "production_authority": False,
            "live_execution_authority": False,
        }

    approval = _validate_operator_approval(packet)
    if not approval["accepted"]:
        receipt_path = _write_gateway_receipt(
            shell_root,
            operation="actions_submit",
            status="rejected",
            packet=packet,
            result=approval,
            refusal_class=str(approval.get("refusal_class") or "OPERATOR_APPROVAL_REQUIRED"),
        )
        return {
            "schema_id": "ion.custom_gpt_action_gateway_submit.v1",
            "ok": False,
            "verdict": BLOCKED_VERDICT,
            "finding": "operator_approval_refused",
            "refusal_class": approval.get("refusal_class"),
            "gateway_receipt_path": receipt_path,
            "approval": approval,
            "production_authority": False,
            "live_execution_authority": False,
        }

    chatops_packet = _normalize_packet_for_chatops(packet)
    owner_result = submit_chatops_action(shell_root, chatops_packet)
    refusal = None if owner_result.get("ok") else "ION_OWNER_REFUSED"
    receipt_path = _write_gateway_receipt(
        shell_root,
        operation="actions_submit",
        status="completed" if owner_result.get("ok") else "rejected",
        packet=packet,
        result=owner_result,
        refusal_class=refusal,
    )
    result = {
        "schema_id": "ion.custom_gpt_action_gateway_submit.v1",
        "ok": bool(owner_result.get("ok")),
        "verdict": READY_VERDICT if owner_result.get("ok") else BLOCKED_VERDICT,
        "action_id": owner_result.get("action_id"),
        "intent": owner_result.get("intent"),
        "gateway_receipt_path": receipt_path,
        "owner": "ION/04_packages/kernel/ion_chatops_bridge.py",
        "owner_result": owner_result,
        "refusal_class": refusal,
        "steward_gate": "result_is_evidence_not_steward_integration",
        "production_authority": False,
        "live_execution_authority": False,
    }
    _record_idempotency(shell_root, key, receipt_path=receipt_path, result=result)
    return result


def _latest_json_files(root: Path, rel: Path, *, limit: int) -> list[dict[str, Any]]:
    base = root / rel
    if not base.exists():
        return []
    rows: list[dict[str, Any]] = []
    for path in sorted((item for item in base.glob("*.json") if item.is_file()), key=lambda item: item.stat().st_mtime, reverse=True)[:limit]:
        rows.append({
            "path": _repo_rel(path, root),
            "name": path.name,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
        })
    return rows


def build_recent_gateway_receipts(root: str | Path | None, limit: int = 20) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    bounded_limit = max(1, min(int(limit or 20), 50))
    return {
        "schema_id": "ion.custom_gpt_action_gateway_recent_receipts.v1",
        "ok": True,
        "gateway_receipts": _latest_json_files(shell_root, RECEIPTS_DIR, limit=bounded_limit),
        "chatops_receipts": _latest_json_files(shell_root, Path("ION/05_context/current/chatops_bridge/receipts"), limit=bounded_limit),
        "production_authority": False,
        "live_execution_authority": False,
    }


def _openapi_surface(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    path = shell_root / OPENAPI_RELATIVE_PATH
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    operation_ids = re.findall(r"operationId:\s*([A-Za-z0-9_]+)", text)
    return {
        "schema_id": "ion.custom_gpt_action_gateway_openapi_surface.v1",
        "ok": path.exists(),
        "openapi_path": OPENAPI_RELATIVE_PATH.as_posix(),
        "operation_ids": operation_ids,
        "raw_yaml": text,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _response_status(payload: Mapping[str, Any]) -> int:
    if payload.get("ok") is not False:
        return 200
    refusal = payload.get("refusal_class")
    if refusal in {"AUTH_MISSING", "AUTH_INVALID"}:
        return 401
    if refusal == "PAYLOAD_TOO_LARGE":
        return 413
    if refusal == "ENDPOINT_NOT_ALLOWED":
        return 404
    return 409


def _http_response(handler: BaseHTTPRequestHandler, status: int, payload: Mapping[str, Any]) -> None:
    body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "https://chatgpt.com")
    handler.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.end_headers()
    handler.wfile.write(body)


def make_handler(root: Path) -> type[BaseHTTPRequestHandler]:
    class GatewayHandler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - stdlib signature
            return

        def _policy(self) -> dict[str, Any]:
            return load_gateway_policy(root)

        def _auth(self) -> dict[str, Any]:
            return validate_gateway_auth(self.headers, self._policy())

        def _protected_or_respond(self) -> bool:
            auth = self._auth()
            if auth["ok"]:
                return True
            _http_response(self, _response_status(auth), auth)
            return False

        def do_OPTIONS(self) -> None:  # noqa: N802
            _http_response(self, 200, {"ok": True})

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path
            if path == "/health":
                _http_response(self, 200, build_gateway_health(root))
                return
            if not self._protected_or_respond():
                return
            if path == "/policy":
                _http_response(self, 200, build_gateway_policy_surface(root))
                return
            if path == "/context-pack":
                _http_response(self, 200, build_chatops_context_pack(root))
                return
            if path == "/codex/queue":
                payload = build_chatops_agent_queue(root)
                payload["runner_status"] = build_codex_queue_runner_status(root, reconcile=False)
                _http_response(self, 200, payload)
                return
            if path == "/agent/status":
                payload = build_chatops_agent_status(root)
                _http_response(self, 200, payload)
                return
            if path == "/receipts/recent":
                params = parse_qs(parsed.query)
                limit = int(params.get("limit", ["20"])[0])
                _http_response(self, 200, build_recent_gateway_receipts(root, limit=limit))
                return
            _http_response(self, 404, {"ok": False, "refusal_class": "ENDPOINT_NOT_ALLOWED", "finding": "endpoint_not_allowed"})

        def do_POST(self) -> None:  # noqa: N802
            if not self._protected_or_respond():
                return
            policy = self._policy()
            limits = policy.get("limits") if isinstance(policy.get("limits"), Mapping) else {}
            max_body = int(limits.get("max_body_bytes") or MAX_BODY_BYTES_DEFAULT)
            length = int(self.headers.get("Content-Length") or "0")
            if length > max_body:
                payload = {"ok": False, "refusal_class": "PAYLOAD_TOO_LARGE", "finding": "payload_too_large", "max_body_bytes": max_body}
                _http_response(self, 413, payload)
                return
            try:
                raw = self.rfile.read(length).decode("utf-8", errors="replace")
                packet = json.loads(raw or "{}")
            except Exception as exc:
                _http_response(self, 400, {"ok": False, "refusal_class": "SCHEMA_INVALID", "finding": "invalid_json", "error": str(exc)})
                return
            if not isinstance(packet, Mapping):
                _http_response(self, 400, {"ok": False, "refusal_class": "SCHEMA_INVALID", "finding": "json_object_required"})
                return
            path = urlparse(self.path).path
            if path == "/actions/validate":
                payload = validate_gateway_action_packet(root, packet)
                _http_response(self, 200 if payload.get("ok") else 409, payload)
                return
            if path == "/actions/submit":
                payload = submit_gateway_action_packet(root, packet)
                _http_response(self, _response_status(payload), payload)
                return
            _http_response(self, 404, {"ok": False, "refusal_class": "ENDPOINT_NOT_ALLOWED", "finding": "endpoint_not_allowed"})

    return GatewayHandler


def run_server(root: str | Path | None = None, *, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    shell_root = _resolve_root(root)
    server = ThreadingHTTPServer((host, port), make_handler(shell_root))
    print(f"ION Custom GPT Action Gateway listening on http://{host}:{port}")
    try:
        server.serve_forever()
    finally:
        server.server_close()


def _load_json_arg(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON input must be an object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ION Custom GPT Action Gateway.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--policy", action="store_true")
    parser.add_argument("--health", action="store_true")
    parser.add_argument("--openapi", action="store_true")
    parser.add_argument("--validate-json", default=None)
    parser.add_argument("--submit-json", default=None)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.serve:
        run_server(args.ion_root, host=args.host, port=args.port)
        return 0
    if args.policy:
        result = build_gateway_policy_surface(args.ion_root)
    elif args.health:
        result = build_gateway_health(args.ion_root)
    elif args.openapi:
        result = _openapi_surface(args.ion_root)
    elif args.validate_json:
        result = validate_gateway_action_packet(args.ion_root, _load_json_arg(args.validate_json))
    elif args.submit_json:
        result = submit_gateway_action_packet(args.ion_root, _load_json_arg(args.submit_json))
    else:
        result = build_gateway_health(args.ion_root)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif args.openapi and result.get("raw_yaml"):
        print(result["raw_yaml"])
    else:
        print(result.get("verdict") or ("OK" if result.get("ok") else "BLOCKED"))
    return 0 if result.get("ok") is not False else 1


if __name__ == "__main__":
    raise SystemExit(main())
