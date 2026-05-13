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
from urllib import request as url_request
from urllib.error import HTTPError, URLError

try:
    from .ion_agent_invocation_broker import (
        build_bounded_agent_status,
        control_agent_invocation,
        invoke_bounded_agent,
        pending_agent_relays,
        recent_agent_invocation_receipts,
        respond_agent_relay,
        settle_agent_invocation,
    )
except ImportError:  # pragma: no cover - direct script execution fallback
    from ion_agent_invocation_broker import (
        build_bounded_agent_status,
        control_agent_invocation,
        invoke_bounded_agent,
        pending_agent_relays,
        recent_agent_invocation_receipts,
        respond_agent_relay,
        settle_agent_invocation,
    )

from typing import Any, Callable, Mapping
from urllib.parse import parse_qs, urlencode, urlparse

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
from .ion_supabase_event_mirror import (
    DEFAULT_SUPABASE_SCHEMA,
    SupabaseConfig,
    SupabaseMirrorError,
    mirror_event,
)

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
BROWSER_QUEUE_FILE = RUNTIME_DIR / "browser_queue.json"
MAX_BODY_BYTES_DEFAULT = 262144
BROWSER_QUEUE_MAX_LENGTH_DEFAULT = 25
BROWSER_QUEUE_MAX_AUTOPLAY_TURNS_DEFAULT = 10
BROWSER_QUEUE_DEFAULT_MAX_TURNS = 3
BROWSER_QUEUE_HARD_MAX_TURNS = 8
BROWSER_QUEUE_LEASE_SECONDS = 120
BROWSER_QUEUE_RESULT_TEXT_MAX = 60000
DAIMON_REPO_RELATIVE_PATH = Path("../dAimon")

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
    "QUEUE_FULL",
    "BROWSER_PACKET_BLOCKED",
    "LOCAL_DAEMON_UNAVAILABLE",
    "ION_OWNER_REFUSED",
    "STEWARD_GATE_REQUIRED",
    "SUPABASE_ENV_MISSING",
    "SUPABASE_SCHEMA_PERMISSION_BLOCKED",
    "SUPABASE_API_UNAVAILABLE",
)

SUPABASE_READ_ROUTES = {
    "/supabase/cockpit/overview": {
        "relation": "v_cockpit_overview",
        "select": "*",
        "limit": 1,
        "order": None,
        "schema_id": "ion.action_gateway.supabase_cockpit_overview.v1",
    },
    "/supabase/events/recent": {
        "relation": "v_recent_automation_events",
        "select": "*",
        "limit": 20,
        "max_limit": 100,
        "order": "created_at.desc",
        "schema_id": "ion.action_gateway.supabase_recent_events.v1",
    },
    "/supabase/service-health/latest": {
        "relation": "v_latest_service_health",
        "select": "*",
        "limit": 100,
        "order": None,
        "schema_id": "ion.action_gateway.supabase_latest_service_health.v1",
    },
    "/supabase/carrier-mounts/current": {
        "relation": "v_current_carrier_mounts",
        "select": "*",
        "limit": 100,
        "order": None,
        "schema_id": "ion.action_gateway.supabase_current_carrier_mounts.v1",
    },
}

SUPABASE_WRITE_ROUTES = {
    "/supabase/events/record": "automation_event",
    "/supabase/service-health/record": "service_health_snapshot",
    "/supabase/carrier-mounts/record": "carrier_mount_receipt",
}


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
        "allowed_get_paths": [
            "/health",
            "/openapi.yaml",
            "/policy",
            "/context-pack",
            "/codex/queue",
            "/agent/status",
        "/agent/relay/pending",
        "/agent/receipts/recent",
            "/projects/daimon/visibility",
            "/supabase/cockpit/overview",
            "/supabase/events/recent",
            "/supabase/service-health/latest",
            "/supabase/carrier-mounts/current",
            "/browser-queue/status",
            "/browser-queue/receipts/recent",
            "/receipts/recent",
        ],
        "allowed_post_paths": [
            "/actions/validate",
            "/actions/submit",
            "/browser-queue/enqueue",
            "/browser-queue/claim",
            "/browser-queue/result",
            "/browser-queue/control",
            "/supabase/events/record",
            "/supabase/service-health/record",
            "/supabase/carrier-mounts/record",
        "/agent/invoke",
        "/agent/relay/respond",
        "/agent/control",
        "/agent/settle",
        ],
        "supported_mvp_intents": sorted(CHATOPS_SUPPORTED_INTENTS),
        "hard_gated_intents": sorted(CHATOPS_HARD_GATED_INTENTS),
        "refusal_classes": list(REFUSAL_CLASSES),
        "storage": {
            "receipts": RECEIPTS_DIR.as_posix() + "/",
            "runtime": RUNTIME_DIR.as_posix() + "/",
            "browser_queue": BROWSER_QUEUE_FILE.as_posix(),
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


def _safe_external_path(path: Path) -> str:
    return path.as_posix()


def _daimon_root(shell_root: Path) -> Path:
    configured = os.environ.get("DAIMON_REPO_PATH")
    if configured:
        return Path(configured).expanduser().resolve()
    return (shell_root / DAIMON_REPO_RELATIVE_PATH).resolve()


def _external_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return _safe_external_path(path)


def _load_external_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _artifact_state(root: Path, relative_path: str) -> dict[str, Any]:
    path = root / relative_path
    row: dict[str, Any] = {
        "path": relative_path,
        "exists": path.exists(),
    }
    if path.exists():
        row["mtime"] = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat()
    return row


def _sanitize_blocker(value: Any) -> str:
    text = str(value)
    if "gcloud auth login" in text or "Reauthentication failed" in text:
        return "gcloud reauthentication required before IAM/user-access queries can complete"
    return text


def _unique_strings(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _compact_claims(package: Mapping[str, Any]) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    raw_claims = package.get("claim_matrix", [])
    for claim in raw_claims if isinstance(raw_claims, list) else []:
        if not isinstance(claim, Mapping):
            continue
        blockers = [_sanitize_blocker(item) for item in claim.get("blockers", [])] if isinstance(claim.get("blockers"), list) else []
        claims.append({
            "claim_id": claim.get("claim_id"),
            "status": claim.get("status"),
            "non_claim": bool(claim.get("non_claim")),
            "evidence": claim.get("evidence", []),
            "blockers": _unique_strings(blockers),
        })
    return claims


def build_daimon_project_visibility(root: str | Path | None = None) -> dict[str, Any]:
    """Build a safe Custom GPT visibility packet for the dAimon project.

    This reads receipt artifacts only. It never reads `.env`, credentials, raw
    service account JSON, MongoDB URIs, or arbitrary project files.
    """

    shell_root = _resolve_root(root)
    daimon_root = _daimon_root(shell_root)
    outputs = daimon_root / "sample_outputs"
    demo_package = _load_external_json(outputs / "demo_evidence_package.json")
    cloud_run_health = _load_external_json(outputs / "cloud_run_live_health.json")
    cloud_run_deploy = _load_external_json(outputs / "cloud_run_deploy_summary.json")
    agent_validation = _load_external_json(outputs / "agent_builder_mcp_trace_validation.json")
    agent_deploy = _load_external_json(outputs / "agent_engine_deploy_summary.json")
    user_access = _load_external_json(outputs / "google_user_access_readiness.json")
    custom_gpt_smoke = _load_external_json(outputs / "custom_gpt_action_visibility_smoke.json")
    connector_expansion = _load_external_json(outputs / "connector_expansion_plan.json")
    live_summary = _load_external_json(outputs / "live_vertical_slice_summary.json")
    evidence = cloud_run_health.get("evidence") if isinstance(cloud_run_health.get("evidence"), Mapping) else {}
    mongodb = evidence.get("mongodb") if isinstance(evidence.get("mongodb"), Mapping) else {}
    user_runtime_identity = user_access.get("runtime_identity") if isinstance(user_access.get("runtime_identity"), Mapping) else {}
    live_mongodb = live_summary.get("mongo_database") or mongodb.get("database")
    live_collection = live_summary.get("mongo_collection")

    artifact_paths = [
        "sample_outputs/demo_evidence_package.json",
        "sample_outputs/dashboard_evidence_trace.json",
        "sample_outputs/demo_video_claims.json",
        "sample_outputs/cloud_run_live_health.json",
        "sample_outputs/cloud_run_deploy_summary.json",
        "sample_outputs/agent_builder_mcp_trace_validation.json",
        "sample_outputs/agent_builder_mcp_trace.json",
        "sample_outputs/google_user_access_readiness.json",
        "sample_outputs/custom_gpt_action_visibility_smoke.json",
        "sample_outputs/connector_expansion_plan.json",
        "sample_outputs/orchestration_validation.json",
        "README.md",
        "docs/google_user_access_readiness.md",
        "docs/custom_gpt_action_connection.md",
        "docs/gitlab_connection_readiness.md",
        "orchestration/connector_expansion_registry.json",
        "agent_builder/openapi_tools_contract.json",
        "agent_builder/system_prompt.md",
    ]
    blockers: list[str] = []
    for source in (user_access, cloud_run_health, agent_validation):
        for item in source.get("blockers", []) if isinstance(source.get("blockers"), list) else []:
            blockers.append(_sanitize_blocker(item))
    connector_rows = connector_expansion.get("connectors", []) if isinstance(connector_expansion.get("connectors"), list) else []
    recommended_next_actions: list[str] = []
    if user_access.get("ok") is not True:
        recommended_next_actions.extend([
            "Run gcloud auth login or select a refreshed authenticated account before IAM readiness checks.",
            "Run scripts/check_google_user_access_readiness.py with target tester principals.",
        ])
    if connector_expansion.get("ok") is True and connector_rows:
        first_next_gate = connector_rows[0].get("next_gate") if isinstance(connector_rows[0], Mapping) else None
        if first_next_gate:
            recommended_next_actions.append(str(first_next_gate))
        gitlab = next((row for row in connector_rows if isinstance(row, Mapping) and row.get("connector_id") == "gitlab"), None)
        if gitlab and gitlab.get("next_gate"):
            recommended_next_actions.append(str(gitlab["next_gate"]))
    else:
        recommended_next_actions.append("Run scripts/generate_connector_expansion_plan.py to refresh Custom GPT/GitLab connector readiness.")
    recommended_next_actions.append("Keep dAimon Custom GPT access to curated receipts unless the operator approves a bounded packet.")

    return {
        "schema_id": "ion.daimon_project_visibility.v1",
        "ok": daimon_root.exists(),
        "project": {
            "name": "dAimon",
            "public_line": "Gemini can generate useful work. dAimon decides what becomes trusted future context.",
            "repo_path": _safe_external_path(daimon_root),
            "repo_present": daimon_root.exists(),
            "read_scope": "curated_receipts_and_project_manifest_only",
        },
        "connector_surfaces": {
            "action_gateway": "https://ion-actions.helixion.net",
            "mcp_connector": "https://ion.helixion.net/mcp",
            "custom_gpt_endpoint": "/projects/daimon/visibility",
        },
        "live_surfaces": {
            "cloud_run_url": cloud_run_health.get("cloud_run_url") or cloud_run_deploy.get("cloud_run_url") or agent_deploy.get("cloud_run_url"),
            "cloud_run_ok": cloud_run_health.get("ok") is True,
            "cloud_run_auth_mode": cloud_run_health.get("auth_mode"),
            "google_project": cloud_run_deploy.get("project") or agent_deploy.get("project") or user_access.get("project"),
            "google_location": agent_deploy.get("location") or user_access.get("region") or cloud_run_deploy.get("region"),
            "agent_engine_resource": agent_deploy.get("remote_agent_name") or user_runtime_identity.get("agent_engine_resource"),
            "agent_service_account": agent_deploy.get("service_account") or user_runtime_identity.get("agent_service_account"),
            "mongodb_database": live_mongodb,
            "mongodb_collection": live_collection,
        },
        "claim_state": {
            "headline_status": demo_package.get("headline_status"),
            "metrics": demo_package.get("metrics", {}),
            "claims": _compact_claims(demo_package),
            "agent_builder_mcp": {
                "ok": agent_validation.get("ok"),
                "proof_status": agent_validation.get("proof_status"),
                "live_mcp_execution_proven": agent_validation.get("live_mcp_execution_proven"),
            },
            "google_user_access": {
                "ok": user_access.get("ok"),
                "proof_status": user_access.get("proof_status"),
                "target_principals_count": len(user_access.get("target_principals", [])) if isinstance(user_access.get("target_principals"), list) else 0,
            },
            "connector_expansion": {
                "ok": connector_expansion.get("ok"),
                "connector_count": connector_expansion.get("connector_count"),
                "connector_ids": connector_expansion.get("connector_ids", []),
                "next_priority_connector": connector_expansion.get("next_priority_connector"),
            },
            "custom_gpt_action_smoke": {
                "ok": custom_gpt_smoke.get("ok"),
                "proof_status": custom_gpt_smoke.get("proof_status"),
                "operation_id": custom_gpt_smoke.get("operation_id"),
                "recommended_default_action": custom_gpt_smoke.get("recommended_default_action"),
            },
        },
        "artifact_inventory": [_artifact_state(daimon_root, path) for path in artifact_paths],
        "current_blockers": sorted(_unique_strings(blockers)),
        "recommended_next_actions": _unique_strings(recommended_next_actions),
        "non_claims": [
            "This endpoint does not expose secrets, environment variables, MongoDB URIs, tokens, or raw service account JSON.",
            "This endpoint does not grant production authority, live execution authority, deploy authority, or accepted-state authority.",
            "Custom GPT visibility over dAimon receipts is not the same as permission to mutate dAimon, Google Cloud, MongoDB, or local files.",
        ],
        "source_receipts": {
            "demo_package": _external_rel(outputs / "demo_evidence_package.json", daimon_root),
            "cloud_run_health": _external_rel(outputs / "cloud_run_live_health.json", daimon_root),
            "agent_builder_validation": _external_rel(outputs / "agent_builder_mcp_trace_validation.json", daimon_root),
            "google_user_access": _external_rel(outputs / "google_user_access_readiness.json", daimon_root),
            "custom_gpt_action_smoke": _external_rel(outputs / "custom_gpt_action_visibility_smoke.json", daimon_root),
            "connector_expansion": _external_rel(outputs / "connector_expansion_plan.json", daimon_root),
        },
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


def _browser_queue_default_state() -> dict[str, Any]:
    return {
        "schema_id": "ion.browser_carrier_queue.v1",
        "created_at": _now(),
        "updated_at": _now(),
        "paused": False,
        "killed": False,
        "max_queue_length": BROWSER_QUEUE_MAX_LENGTH_DEFAULT,
        "max_autoplay_turns": BROWSER_QUEUE_MAX_AUTOPLAY_TURNS_DEFAULT,
        "auto_accept_actions": {
            "enabled": False,
            "until": None,
            "mode": "off",
            "scope": ["browser_queue_safe_packets"],
            "forbidden_classes": [
                "production_authority",
                "live_execution_authority",
                "credentials",
                "purchase",
                "destructive_action",
                "unrestricted_browser_control",
            ],
        },
        "packets": [],
        "production_authority": False,
        "live_execution_authority": False,
    }


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def _load_browser_queue_state(root: Path) -> dict[str, Any]:
    raw = _read_json(root / BROWSER_QUEUE_FILE)
    state = raw if isinstance(raw, dict) else _browser_queue_default_state()
    state.setdefault("schema_id", "ion.browser_carrier_queue.v1")
    state.setdefault("created_at", _now())
    state.setdefault("updated_at", _now())
    state.setdefault("paused", False)
    state.setdefault("killed", False)
    state.setdefault("max_queue_length", BROWSER_QUEUE_MAX_LENGTH_DEFAULT)
    state.setdefault("max_autoplay_turns", BROWSER_QUEUE_MAX_AUTOPLAY_TURNS_DEFAULT)
    auto_accept = state.get("auto_accept_actions")
    if not isinstance(auto_accept, dict):
        auto_accept = {}
    state["auto_accept_actions"] = {
        "enabled": bool(auto_accept.get("enabled")) and not _iso_expired(auto_accept.get("until")),
        "until": auto_accept.get("until"),
        "mode": str(auto_accept.get("mode") or "off"),
        "scope": auto_accept.get("scope") if isinstance(auto_accept.get("scope"), list) else ["browser_queue_safe_packets"],
        "forbidden_classes": auto_accept.get("forbidden_classes")
        if isinstance(auto_accept.get("forbidden_classes"), list)
        else [
            "production_authority",
            "live_execution_authority",
            "credentials",
            "purchase",
            "destructive_action",
            "unrestricted_browser_control",
        ],
    }
    packets = state.get("packets")
    state["packets"] = packets if isinstance(packets, list) else []
    state["production_authority"] = False
    state["live_execution_authority"] = False
    return state


def _save_browser_queue_state(root: Path, state: Mapping[str, Any]) -> None:
    payload = dict(state)
    payload["updated_at"] = _now()
    payload["production_authority"] = False
    payload["live_execution_authority"] = False
    _atomic_write_json(root / BROWSER_QUEUE_FILE, payload)


def _safe_int(value: Any, default: int, low: int, high: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default
    return max(low, min(high, number))


def _clip_text(value: Any, limit: int = BROWSER_QUEUE_RESULT_TEXT_MAX) -> str:
    text = str(value or "")
    return text if len(text) <= limit else text[:limit] + "\n[ION clipped oversized browser result]"


def _utc_after(seconds: int) -> str:
    return datetime.fromtimestamp(datetime.now(timezone.utc).timestamp() + seconds, timezone.utc).replace(microsecond=0).isoformat()


def _iso_expired(value: Any) -> bool:
    if not value:
        return True
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return True
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed <= datetime.now(timezone.utc)


def _browser_packet_receipt_envelope(packet: Mapping[str, Any], intent: str) -> dict[str, Any]:
    return {
        "idempotency_key": packet.get("idempotency_key"),
        "ion_action": {
            "action_id": packet.get("packet_id") or packet.get("action_id") or "browser_queue_packet",
            "intent": intent,
        },
    }


def _write_browser_queue_receipt(root: Path, *, operation: str, status: str, packet: Mapping[str, Any] | None, result: Mapping[str, Any], refusal_class: str | None = None) -> str:
    envelope = _browser_packet_receipt_envelope(packet or {}, operation)
    return _write_gateway_receipt(
        root,
        operation=operation,
        status=status,
        packet=envelope,
        result=result,
        refusal_class=refusal_class,
    )


def _browser_queue_pending_count(state: Mapping[str, Any]) -> int:
    return sum(1 for packet in state.get("packets", []) if isinstance(packet, Mapping) and packet.get("state") in {"queued", "claimed", "needs_operator"})


def _browser_queue_reconcile(state: dict[str, Any]) -> bool:
    changed = False
    for packet in state.get("packets", []):
        if not isinstance(packet, dict):
            continue
        if packet.get("state") == "claimed" and _iso_expired(packet.get("lease_expires_at")):
            packet["state"] = "queued"
            packet["updated_at"] = _now()
            packet["claim"] = {"expired_at": _now(), "previous_lease_id": packet.get("lease_id")}
            packet.pop("lease_id", None)
            packet.pop("lease_expires_at", None)
            changed = True
    return changed


def _packet_allowed_actions(packet: Mapping[str, Any]) -> list[str]:
    raw = packet.get("allowed_actions")
    if isinstance(raw, list):
        values = [str(item).strip() for item in raw if str(item).strip()]
    else:
        values = []
    return values or ["observe", "draft_report"]


def _packet_authority(packet: Mapping[str, Any]) -> Any:
    authority = packet.get("authority")
    if authority is None and isinstance(packet.get("ion_action"), Mapping):
        authority = packet["ion_action"].get("authority")
    return authority if authority is not None else "analysis_only"


def _authority_flag(authority: Any, key: str) -> Any:
    if isinstance(authority, Mapping):
        return authority.get(key)
    return None


def _browser_packet_mutation_requested(packet: Mapping[str, Any]) -> bool:
    authority = _packet_authority(packet)
    authority_text = json.dumps(authority, sort_keys=True).lower() if isinstance(authority, Mapping) else str(authority).lower()
    actions_text = " ".join(_packet_allowed_actions(packet)).lower()
    mutation_words = ("write", "mutate", "execute", "file", "git", "codex", "local", "queue_work")
    return any(word in authority_text or word in actions_text for word in mutation_words)


def _browser_queue_auto_accept_active(state: Mapping[str, Any]) -> bool:
    policy = state.get("auto_accept_actions")
    if not isinstance(policy, Mapping):
        return False
    return bool(policy.get("enabled")) and not _iso_expired(policy.get("until"))


def _browser_packet_auto_accept_allowed(packet: Mapping[str, Any]) -> dict[str, Any]:
    authority = _packet_authority(packet)
    text = " ".join(
        [
            json.dumps(authority, sort_keys=True) if isinstance(authority, Mapping) else str(authority),
            " ".join(_packet_allowed_actions(packet)),
            str(packet.get("objective") or packet.get("prompt") or ""),
        ]
    ).lower()
    forbidden_words = (
        "credential",
        "password",
        "secret",
        "token",
        "purchase",
        "payment",
        "delete",
        "destructive",
        "production",
        "deploy",
        "unrestricted",
        "arbitrary shell",
        "raw shell",
    )
    findings = [f"auto_accept_forbidden_word:{word}" for word in forbidden_words if word in text]
    if packet.get("production_authority") is True or (isinstance(authority, Mapping) and _authority_flag(authority, "production_authority") is not False):
        findings.append("auto_accept_production_authority_refused")
    if packet.get("live_execution_authority") is True or (isinstance(authority, Mapping) and _authority_flag(authority, "live_execution_authority") is not False):
        findings.append("auto_accept_live_execution_authority_refused")
    return {
        "schema_id": "ion.browser_queue_auto_accept_policy.v1",
        "accepted": not findings,
        "findings": findings,
        "production_authority": False,
        "live_execution_authority": False,
    }


def validate_browser_queue_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    findings: list[str] = []
    refusal_class: str | None = None
    authority = _packet_authority(packet)
    if packet.get("production_authority") is True or (isinstance(authority, Mapping) and _authority_flag(authority, "production_authority") is not False):
        findings.append("production_authority_refused")
        refusal_class = "PRODUCTION_AUTHORITY_REFUSED"
    if packet.get("live_execution_authority") is True or (isinstance(authority, Mapping) and _authority_flag(authority, "live_execution_authority") is not False):
        findings.append("live_execution_authority_refused")
        refusal_class = refusal_class or "LIVE_EXECUTION_AUTHORITY_REFUSED"
    if not str(packet.get("idempotency_key") or "").strip():
        findings.append("idempotency_key_required")
        refusal_class = refusal_class or "IDEMPOTENCY_KEY_REQUIRED"
    if not str(packet.get("prompt") or packet.get("objective") or "").strip():
        findings.append("prompt_or_objective_required")
        refusal_class = refusal_class or "SCHEMA_INVALID"
    return {
        "schema_id": "ion.browser_carrier_queue_packet_validation.v1",
        "ok": not findings,
        "accepted": not findings,
        "findings": findings,
        "refusal_class": refusal_class,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _normalize_browser_queue_packet(packet: Mapping[str, Any], *, approval_status: str, initial_state: str) -> dict[str, Any]:
    key = str(packet.get("idempotency_key") or "").strip()
    objective = str(packet.get("objective") or packet.get("prompt") or "").strip()
    prompt = str(packet.get("prompt") or objective).strip()
    packet_id = str(packet.get("packet_id") or packet.get("action_id") or f"BQ-{hashlib.sha256(key.encode('utf-8')).hexdigest()[:16]}")
    return {
        "schema_id": "ion.browser_carrier_queue_packet.v1",
        "packet_id": packet_id,
        "idempotency_key": key,
        "source": str(packet.get("source") or "custom_gpt_action"),
        "created_at": _now(),
        "updated_at": _now(),
        "objective": objective,
        "prompt": prompt,
        "allowed_actions": _packet_allowed_actions(packet),
        "authority": _packet_authority(packet),
        "requires_operator_approval": bool(packet.get("requires_operator_approval") or _browser_packet_mutation_requested(packet)),
        "approval_status": approval_status,
        "auto_run": packet.get("auto_run") is not False,
        "max_turns": _safe_int(packet.get("max_turns"), BROWSER_QUEUE_DEFAULT_MAX_TURNS, 1, BROWSER_QUEUE_HARD_MAX_TURNS),
        "stop_condition": str(packet.get("stop_condition") or "return receipt or blocker"),
        "context_refs": packet.get("context_refs") if isinstance(packet.get("context_refs"), list) else [],
        "state": initial_state,
        "attempts": 0,
        "claim": {},
        "results": [],
        "receipt_refs": [],
        "production_authority": False,
        "live_execution_authority": False,
    }


def _public_browser_packet(packet: Mapping[str, Any], *, include_prompt: bool = False) -> dict[str, Any]:
    row = {
        "packet_id": packet.get("packet_id"),
        "objective": packet.get("objective"),
        "prompt_preview": str(packet.get("prompt") or "")[:240],
        "allowed_actions": packet.get("allowed_actions", []),
        "authority": packet.get("authority"),
        "requires_operator_approval": packet.get("requires_operator_approval"),
        "approval_status": packet.get("approval_status"),
        "auto_run": packet.get("auto_run"),
        "max_turns": packet.get("max_turns"),
        "stop_condition": packet.get("stop_condition"),
        "state": packet.get("state"),
        "attempts": packet.get("attempts"),
        "created_at": packet.get("created_at"),
        "updated_at": packet.get("updated_at"),
        "lease_expires_at": packet.get("lease_expires_at"),
        "receipt_refs": packet.get("receipt_refs", []),
        "production_authority": False,
        "live_execution_authority": False,
    }
    if include_prompt:
        row["prompt"] = packet.get("prompt")
        row["context_refs"] = packet.get("context_refs", [])
        row["claim"] = packet.get("claim", {})
    return row


def build_browser_queue_status(root: str | Path | None, *, include_packets: bool = True) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    state = _load_browser_queue_state(shell_root)
    if _browser_queue_reconcile(state):
        _save_browser_queue_state(shell_root, state)
    packets = [packet for packet in state.get("packets", []) if isinstance(packet, Mapping)]
    counts = {
        "queued": sum(1 for packet in packets if packet.get("state") == "queued"),
        "claimed": sum(1 for packet in packets if packet.get("state") == "claimed"),
        "needs_operator": sum(1 for packet in packets if packet.get("state") == "needs_operator"),
        "completed": sum(1 for packet in packets if packet.get("state") == "completed"),
        "blocked": sum(1 for packet in packets if packet.get("state") == "blocked"),
        "failed": sum(1 for packet in packets if packet.get("state") == "failed"),
        "cancelled": sum(1 for packet in packets if packet.get("state") == "cancelled"),
    }
    payload: dict[str, Any] = {
        "schema_id": "ion.browser_carrier_queue_status.v1",
        "ok": True,
        "paused": bool(state.get("paused")),
        "killed": bool(state.get("killed")),
        "max_queue_length": state.get("max_queue_length"),
        "max_autoplay_turns": state.get("max_autoplay_turns"),
        "auto_accept_actions": state.get("auto_accept_actions"),
        "counts": counts,
        "pending_count": counts["queued"] + counts["claimed"] + counts["needs_operator"],
        "queue_path": BROWSER_QUEUE_FILE.as_posix(),
        "production_authority": False,
        "live_execution_authority": False,
    }
    if include_packets:
        payload["packets"] = [_public_browser_packet(packet) for packet in packets[-50:]]
    return payload


def enqueue_browser_queue_packet(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    validation = validate_browser_queue_packet(packet)
    if not validation["ok"]:
        receipt_path = _write_browser_queue_receipt(
            shell_root,
            operation="browser_queue_enqueue",
            status="rejected",
            packet=packet,
            result=validation,
            refusal_class=str(validation.get("refusal_class") or "SCHEMA_INVALID"),
        )
        validation["gateway_receipt_path"] = receipt_path
        return validation
    key = str(packet.get("idempotency_key") or "").strip()
    existing = _idempotency_entry(shell_root, key)
    if existing:
        result = {
            "schema_id": "ion.browser_carrier_queue_enqueue.v1",
            "ok": False,
            "finding": "idempotency_key_replayed",
            "refusal_class": "IDEMPOTENCY_REPLAY_BLOCKED",
            "existing": dict(existing),
            "production_authority": False,
            "live_execution_authority": False,
        }
        receipt_path = _write_browser_queue_receipt(shell_root, operation="browser_queue_enqueue", status="rejected", packet=packet, result=result, refusal_class="IDEMPOTENCY_REPLAY_BLOCKED")
        result["gateway_receipt_path"] = receipt_path
        return result
    state = _load_browser_queue_state(shell_root)
    if _browser_queue_reconcile(state):
        _save_browser_queue_state(shell_root, state)
    max_length = _safe_int(state.get("max_queue_length"), BROWSER_QUEUE_MAX_LENGTH_DEFAULT, 1, 200)
    if _browser_queue_pending_count(state) >= max_length:
        result = {
            "schema_id": "ion.browser_carrier_queue_enqueue.v1",
            "ok": False,
            "finding": "browser_queue_full",
            "refusal_class": "QUEUE_FULL",
            "max_queue_length": max_length,
            "production_authority": False,
            "live_execution_authority": False,
        }
        receipt_path = _write_browser_queue_receipt(shell_root, operation="browser_queue_enqueue", status="rejected", packet=packet, result=result, refusal_class="QUEUE_FULL")
        result["gateway_receipt_path"] = receipt_path
        return result
    approval_status = "not_required"
    initial_state = "queued"
    if bool(packet.get("requires_operator_approval") or _browser_packet_mutation_requested(packet)):
        approval = _validate_operator_approval(packet)
        if approval["accepted"]:
            approval_status = "approved"
        elif _browser_queue_auto_accept_active(state):
            auto_accept = _browser_packet_auto_accept_allowed(packet)
            if auto_accept["accepted"]:
                approval_status = "auto_approved"
            else:
                approval_status = "needed"
                initial_state = "needs_operator"
        else:
            approval_status = "needed"
            initial_state = "needs_operator"
    queued_packet = _normalize_browser_queue_packet(packet, approval_status=approval_status, initial_state=initial_state)
    state.setdefault("packets", []).append(queued_packet)
    result = {
        "schema_id": "ion.browser_carrier_queue_enqueue.v1",
        "ok": True,
        "verdict": READY_VERDICT,
        "packet_id": queued_packet["packet_id"],
        "state": queued_packet["state"],
        "approval_status": queued_packet["approval_status"],
        "auto_run": queued_packet["auto_run"],
        "production_authority": False,
        "live_execution_authority": False,
    }
    receipt_path = _write_browser_queue_receipt(shell_root, operation="browser_queue_enqueue", status="queued" if initial_state == "queued" else "needs_operator", packet=queued_packet, result=result)
    queued_packet.setdefault("receipt_refs", []).append(receipt_path)
    _save_browser_queue_state(shell_root, state)
    result["gateway_receipt_path"] = receipt_path
    _record_idempotency(shell_root, key, receipt_path=receipt_path, result=result)
    return result


def claim_browser_queue_packet(root: str | Path | None, request: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    state = _load_browser_queue_state(shell_root)
    changed = _browser_queue_reconcile(state)
    if state.get("killed") or state.get("paused"):
        if changed:
            _save_browser_queue_state(shell_root, state)
        return {
            "schema_id": "ion.browser_carrier_queue_claim.v1",
            "ok": True,
            "claimed": False,
            "finding": "queue_killed" if state.get("killed") else "queue_paused",
            "production_authority": False,
            "live_execution_authority": False,
        }
    carrier_id = str(request.get("carrier_id") or "ion-browser-carrier").strip()
    chat_url = str(request.get("chat_url") or "").strip()
    claimed: dict[str, Any] | None = None
    for packet in state.get("packets", []):
        if not isinstance(packet, dict) or packet.get("state") != "queued" or packet.get("auto_run") is False:
            continue
        attempts = int(packet.get("attempts") or 0)
        max_turns = _safe_int(packet.get("max_turns"), BROWSER_QUEUE_DEFAULT_MAX_TURNS, 1, BROWSER_QUEUE_HARD_MAX_TURNS)
        if attempts >= max_turns:
            packet["state"] = "blocked"
            packet["blocked_reason"] = "max_turns_reached"
            packet["updated_at"] = _now()
            changed = True
            continue
        lease_id = f"{packet.get('packet_id')}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{attempts + 1}"
        packet["state"] = "claimed"
        packet["attempts"] = attempts + 1
        packet["lease_id"] = lease_id
        packet["lease_expires_at"] = _utc_after(BROWSER_QUEUE_LEASE_SECONDS)
        packet["updated_at"] = _now()
        packet["claim"] = {
            "carrier_id": carrier_id,
            "chat_url": chat_url,
            "claimed_at": _now(),
            "lease_id": lease_id,
            "lease_expires_at": packet["lease_expires_at"],
            "turn_index": packet["attempts"],
        }
        claimed = packet
        changed = True
        break
    if changed:
        _save_browser_queue_state(shell_root, state)
    if not claimed:
        return {
            "schema_id": "ion.browser_carrier_queue_claim.v1",
            "ok": True,
            "claimed": False,
            "finding": "no_eligible_packet",
            "production_authority": False,
            "live_execution_authority": False,
        }
    result = {
        "schema_id": "ion.browser_carrier_queue_claim.v1",
        "ok": True,
        "claimed": True,
        "packet": _public_browser_packet(claimed, include_prompt=True),
        "lease_id": claimed.get("lease_id"),
        "lease_expires_at": claimed.get("lease_expires_at"),
        "production_authority": False,
        "live_execution_authority": False,
    }
    receipt_path = _write_browser_queue_receipt(shell_root, operation="browser_queue_claim", status="claimed", packet=claimed, result={k: v for k, v in result.items() if k != "packet"})
    claimed.setdefault("receipt_refs", []).append(receipt_path)
    _save_browser_queue_state(shell_root, state)
    result["gateway_receipt_path"] = receipt_path
    return result


def complete_browser_queue_packet(root: str | Path | None, request: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    packet_id = str(request.get("packet_id") or "").strip()
    lease_id = str(request.get("lease_id") or "").strip()
    state = _load_browser_queue_state(shell_root)
    target: dict[str, Any] | None = None
    for packet in state.get("packets", []):
        if isinstance(packet, dict) and str(packet.get("packet_id") or "") == packet_id:
            target = packet
            break
    if not target:
        return {"schema_id": "ion.browser_carrier_queue_result.v1", "ok": False, "refusal_class": "SCHEMA_INVALID", "finding": "packet_not_found", "production_authority": False, "live_execution_authority": False}
    if target.get("lease_id") and lease_id and target.get("lease_id") != lease_id:
        return {"schema_id": "ion.browser_carrier_queue_result.v1", "ok": False, "refusal_class": "SCHEMA_INVALID", "finding": "lease_id_mismatch", "production_authority": False, "live_execution_authority": False}
    status = str(request.get("status") or "completed").strip()
    final_state = "completed" if status == "completed" else "blocked" if status in {"blocked", "needs_operator"} else "failed"
    result_row = {
        "packet_id": packet_id,
        "lease_id": lease_id,
        "carrier_id": request.get("carrier_id"),
        "chat_url": request.get("chat_url"),
        "turn_index": target.get("attempts"),
        "status": status,
        "blocked_reason": request.get("blocked_reason"),
        "assistant_text": _clip_text(request.get("assistant_text")),
        "structured_blocks": request.get("structured_blocks") if isinstance(request.get("structured_blocks"), list) else [],
        "captured_at": request.get("captured_at") or _now(),
        "production_authority": False,
        "live_execution_authority": False,
    }
    target["state"] = final_state
    target["updated_at"] = _now()
    target.setdefault("results", []).append(result_row)
    target.pop("lease_id", None)
    target.pop("lease_expires_at", None)
    receipt_path = _write_browser_queue_receipt(shell_root, operation="browser_queue_result", status=final_state, packet=target, result=result_row, refusal_class=None if final_state == "completed" else "BROWSER_PACKET_BLOCKED")
    target.setdefault("receipt_refs", []).append(receipt_path)
    result_row["receipt_path"] = receipt_path
    _save_browser_queue_state(shell_root, state)
    return {
        "schema_id": "ion.browser_carrier_queue_result.v1",
        "ok": final_state == "completed",
        "packet_id": packet_id,
        "state": final_state,
        "gateway_receipt_path": receipt_path,
        "production_authority": False,
        "live_execution_authority": False,
    }


def control_browser_queue(root: str | Path | None, request: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    state = _load_browser_queue_state(shell_root)
    operation = str(request.get("operation") or "").strip()
    packet_id = str(request.get("packet_id") or "").strip()
    target: dict[str, Any] | None = None
    if packet_id:
        for packet in state.get("packets", []):
            if isinstance(packet, dict) and str(packet.get("packet_id") or "") == packet_id:
                target = packet
                break
    ok = True
    finding = "control_applied"
    if operation == "pause":
        state["paused"] = True
    elif operation == "resume":
        state["paused"] = False
        state["killed"] = False
    elif operation == "kill":
        state["killed"] = True
        state["paused"] = True
    elif operation == "auto_accept_on":
        ttl = _safe_int(request.get("ttl_seconds"), 900, 60, 3600)
        state["auto_accept_actions"] = {
            "enabled": True,
            "until": _utc_after(ttl),
            "mode": "operator_visible_ttl",
            "scope": ["browser_queue_safe_packets"],
            "forbidden_classes": [
                "production_authority",
                "live_execution_authority",
                "credentials",
                "purchase",
                "destructive_action",
                "unrestricted_browser_control",
            ],
        }
    elif operation == "auto_accept_off":
        state["auto_accept_actions"] = {
            "enabled": False,
            "until": None,
            "mode": "off",
            "scope": ["browser_queue_safe_packets"],
            "forbidden_classes": [
                "production_authority",
                "live_execution_authority",
                "credentials",
                "purchase",
                "destructive_action",
                "unrestricted_browser_control",
            ],
        }
    elif operation == "cancel" and target:
        target["state"] = "cancelled"
        target["updated_at"] = _now()
    elif operation == "retry" and target:
        target["state"] = "queued"
        target["updated_at"] = _now()
        target.pop("lease_id", None)
        target.pop("lease_expires_at", None)
    elif operation == "approve" and target:
        approval = _validate_operator_approval(request)
        if approval["accepted"]:
            target["state"] = "queued"
            target["approval_status"] = "approved"
            target["updated_at"] = _now()
        else:
            ok = False
            finding = "approval_refused"
    else:
        ok = False
        finding = "unsupported_control_operation_or_missing_packet"
    result = {
        "schema_id": "ion.browser_carrier_queue_control.v1",
        "ok": ok,
        "operation": operation,
        "packet_id": packet_id or None,
        "finding": finding,
        "auto_accept_actions": state.get("auto_accept_actions"),
        "production_authority": False,
        "live_execution_authority": False,
    }
    receipt_path = _write_browser_queue_receipt(shell_root, operation=f"browser_queue_control_{operation or 'unknown'}", status="completed" if ok else "rejected", packet=target or {"packet_id": packet_id or "queue"}, result=result, refusal_class=None if ok else "SCHEMA_INVALID")
    if target:
        target.setdefault("receipt_refs", []).append(receipt_path)
    _save_browser_queue_state(shell_root, state)
    result["gateway_receipt_path"] = receipt_path
    result["status"] = build_browser_queue_status(shell_root, include_packets=True)
    return result


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


def _supabase_error_payload(
    *,
    route: str,
    finding: str,
    refusal_class: str,
    error: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_id": "ion.action_gateway.supabase_error.v1",
        "ok": False,
        "route": route,
        "finding": finding,
        "refusal_class": refusal_class,
        "production_authority": False,
        "live_execution_authority": False,
        "accepted_state_claim": False,
    }
    if error:
        payload["error"] = error
    return payload


def _classify_supabase_error(error: str) -> tuple[str, str]:
    lowered = error.lower()
    if "supabase_url" in lowered or "supabase_service_role_key" in lowered or "supabase_secret_key" in lowered:
        return "supabase_env_missing", "SUPABASE_ENV_MISSING"
    if "invalid schema" in lowered or "permission denied for schema" in lowered or "pgrst106" in lowered:
        return "supabase_schema_permission_blocked", "SUPABASE_SCHEMA_PERMISSION_BLOCKED"
    return "supabase_api_unavailable", "SUPABASE_API_UNAVAILABLE"


def _supabase_config_or_error(
    route: str,
    environ: Mapping[str, str] | None = None,
) -> tuple[SupabaseConfig | None, dict[str, Any] | None]:
    try:
        return SupabaseConfig.from_env(dict(environ) if environ is not None else None), None
    except SupabaseMirrorError as exc:
        finding, refusal = _classify_supabase_error(str(exc))
        return None, _supabase_error_payload(route=route, finding=finding, refusal_class=refusal, error=str(exc))


def _http_get_json(url: str, headers: Mapping[str, str], timeout: float) -> Any:
    req = url_request.Request(url, headers=dict(headers), method="GET")
    try:
        with url_request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw or "null")
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise SupabaseMirrorError(f"Supabase REST HTTP {exc.code}: {raw}") from exc
    except URLError as exc:
        raise SupabaseMirrorError(f"Supabase REST connection failed: {exc}") from exc


def _bounded_query_limit(params: Mapping[str, list[str]], *, default: int, maximum: int) -> int:
    raw = params.get("limit", [str(default)])[0]
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = default
    return max(1, min(value, maximum))


def build_supabase_readmodel_response(
    root: str | Path | None,
    route: str,
    query: str = "",
    *,
    environ: Mapping[str, str] | None = None,
    http_get: Callable[[str, Mapping[str, str], float], Any] | None = None,
) -> dict[str, Any]:
    _resolve_root(root)
    spec = SUPABASE_READ_ROUTES.get(route)
    if not spec:
        return _supabase_error_payload(route=route, finding="endpoint_not_allowed", refusal_class="ENDPOINT_NOT_ALLOWED")
    config, error = _supabase_config_or_error(route, environ)
    if error:
        return error
    assert config is not None

    params = parse_qs(query)
    limit = int(spec.get("limit") or 20)
    if "max_limit" in spec:
        limit = _bounded_query_limit(params, default=limit, maximum=int(spec["max_limit"]))

    query_params: dict[str, Any] = {
        "select": spec.get("select") or "*",
        "limit": str(limit),
    }
    if spec.get("order"):
        query_params["order"] = str(spec["order"])
    url = f"{config.url}/rest/v1/{spec['relation']}?{urlencode(query_params)}"
    headers = {
        "apikey": config.key,
        "Authorization": f"Bearer {config.key}",
        "Accept": "application/json",
        "Accept-Profile": config.schema or DEFAULT_SUPABASE_SCHEMA,
    }
    try:
        rows = (http_get or _http_get_json)(url, headers, 20.0)
    except Exception as exc:
        finding, refusal = _classify_supabase_error(str(exc))
        return _supabase_error_payload(route=route, finding=finding, refusal_class=refusal, error=str(exc))
    return {
        "schema_id": spec["schema_id"],
        "ok": True,
        "route": route,
        "tool": route,
        "data": rows,
        "count": len(rows) if isinstance(rows, list) else None,
        "supabase_schema": config.schema,
        "production_authority": False,
        "live_execution_authority": False,
        "accepted_state_claim": False,
    }


def submit_supabase_record_event(
    root: str | Path | None,
    route: str,
    packet: Mapping[str, Any],
    *,
    environ: Mapping[str, str] | None = None,
    http_post: Callable[[str, dict[str, Any], dict[str, str], float], Any] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    kind = SUPABASE_WRITE_ROUTES.get(route)
    if not kind:
        return _supabase_error_payload(route=route, finding="endpoint_not_allowed", refusal_class="ENDPOINT_NOT_ALLOWED")
    data = dict(packet)
    data.setdefault("kind", kind)
    if data.get("client_request_id") and not data.get("idempotency_key"):
        data["idempotency_key"] = data["client_request_id"]
    try:
        result = mirror_event(
            data,
            ion_root=shell_root,
            dry_run=False,
            kind=kind,
            environ=dict(environ) if environ is not None else None,
            http_post=http_post,
        )
    except SupabaseMirrorError as exc:
        finding, refusal = _classify_supabase_error(str(exc))
        if "rejected " in str(exc).lower():
            finding, refusal = "supabase_payload_rejected", "SCHEMA_INVALID"
        return _supabase_error_payload(route=route, finding=finding, refusal_class=refusal, error=str(exc))
    except Exception as exc:
        return _supabase_error_payload(route=route, finding="supabase_api_unavailable", refusal_class="SUPABASE_API_UNAVAILABLE", error=str(exc))

    if not result.get("ok"):
        finding, refusal = _classify_supabase_error(str(result.get("error") or "supabase mirror failed"))
        result.update(
            {
                "route": route,
                "tool": route,
                "refusal_class": refusal,
                "finding": finding,
                "production_authority": False,
                "live_execution_authority": False,
                "accepted_state_claim": False,
            }
        )
        return result

    remote = result.get("remote_result")
    remote_row_id = None
    if isinstance(remote, Mapping):
        remote_row_id = remote.get("event_id") or remote.get("snapshot_id") or remote.get("mount_receipt_id")
    result.update(
        {
            "schema_id": "ion.action_gateway.supabase_record_result.v1",
            "route": route,
            "tool": route,
            "kind": kind,
            "remote_row_id": remote_row_id,
            "production_authority": False,
            "live_execution_authority": False,
            "accepted_state_claim": False,
        }
    )
    return result


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


def _http_text_response(handler: BaseHTTPRequestHandler, status: int, text: str, *, content_type: str) -> None:
    body = text.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
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
            if path == "/openapi.yaml":
                surface = _openapi_surface(root)
                if surface.get("ok") and isinstance(surface.get("raw_yaml"), str):
                    _http_text_response(self, 200, str(surface["raw_yaml"]), content_type="application/yaml; charset=utf-8")
                    return
                _http_response(self, 404, {"ok": False, "refusal_class": "ENDPOINT_NOT_ALLOWED", "finding": "openapi_schema_not_found"})
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
            if path == "/projects/daimon/visibility":
                payload = build_daimon_project_visibility(root)
                _http_response(self, 200 if payload.get("ok") else 404, payload)
                return
            if path in SUPABASE_READ_ROUTES:
                payload = build_supabase_readmodel_response(root, path, parsed.query)
                _http_response(self, _response_status(payload), payload)
                return
            if path == "/browser-queue/status":
                params = parse_qs(parsed.query)
                include_packets = params.get("include_packets", ["1"])[0] not in {"0", "false", "False"}
                _http_response(self, 200, build_browser_queue_status(root, include_packets=include_packets))
                return
            if path == "/browser-queue/receipts/recent":
                params = parse_qs(parsed.query)
                limit = int(params.get("limit", ["20"])[0])
                _http_response(self, 200, build_recent_gateway_receipts(root, limit=limit))
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
            if path in SUPABASE_WRITE_ROUTES:
                payload = submit_supabase_record_event(root, path, packet)
                _http_response(self, _response_status(payload), payload)
                return
            if path == "/actions/validate":
                payload = validate_gateway_action_packet(root, packet)
                _http_response(self, 200 if payload.get("ok") else 409, payload)
                return
            if path == "/actions/submit":
                payload = submit_gateway_action_packet(root, packet)
                _http_response(self, _response_status(payload), payload)
                return
            if path == "/browser-queue/enqueue":
                payload = enqueue_browser_queue_packet(root, packet)
                _http_response(self, _response_status(payload), payload)
                return
            if path == "/browser-queue/claim":
                payload = claim_browser_queue_packet(root, packet)
                _http_response(self, _response_status(payload), payload)
                return
            if path == "/browser-queue/result":
                payload = complete_browser_queue_packet(root, packet)
                _http_response(self, _response_status(payload), payload)
                return
            if path == "/browser-queue/control":
                payload = control_browser_queue(root, packet)
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
    parser.add_argument("--daimon-visibility", action="store_true")
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
    elif args.daimon_visibility:
        result = build_daimon_project_visibility(args.ion_root)
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



def build_gateway_agent_status(root: Path, invocation_id: str | None = None) -> dict[str, object]:
    """Return the bounded-agent status surface plus legacy ChatOps status witness."""
    payload = build_bounded_agent_status(root, invocation_id=invocation_id)
    try:
        payload["chatops_status"] = build_chatops_agent_status(root)
    except Exception as exc:  # pragma: no cover - defensive status enrichment only
        payload["chatops_status_error"] = str(exc)
    return payload


def submit_gateway_agent_invocation(root: Path, packet: dict[str, object]) -> dict[str, object]:
    return invoke_bounded_agent(root, packet)


def build_gateway_agent_pending_relays(
    root: Path,
    invocation_id: str | None = None,
    include_answered: bool = False,
) -> dict[str, object]:
    return pending_agent_relays(root, invocation_id=invocation_id, include_answered=include_answered)


def submit_gateway_agent_relay_response(root: Path, response_packet: dict[str, object]) -> dict[str, object]:
    return respond_agent_relay(root, response_packet)


def submit_gateway_agent_control(root: Path, control_packet: dict[str, object]) -> dict[str, object]:
    return control_agent_invocation(root, control_packet)


def submit_gateway_agent_settlement(root: Path, settlement_packet: dict[str, object]) -> dict[str, object]:
    return settle_agent_invocation(root, settlement_packet)


def build_gateway_agent_recent_receipts(root: Path, limit: int = 20) -> dict[str, object]:
    return recent_agent_invocation_receipts(root, limit=limit)


def _gateway_handler_repo_root(handler: object) -> Path:
    server = getattr(handler, "server", None)
    for owner in (handler, server):
        if owner is None:
            continue
        for attr in ("ion_root", "repo_root", "root", "directory"):
            value = getattr(owner, attr, None)
            if value:
                candidate = Path(value)
                if (candidate / "ION").exists():
                    return candidate
                if candidate.name == "ION_CODEX FULL":
                    return candidate
    cwd = Path.cwd()
    for candidate in (cwd, cwd / "ION_CODEX FULL", cwd.parent / "ION_CODEX FULL"):
        if (candidate / "ION" / "04_packages" / "kernel" / "ion_custom_gpt_action_gateway.py").exists():
            return candidate
    return cwd


def _gateway_query_params(raw_path: str) -> dict[str, str]:
    from urllib.parse import parse_qs, urlparse

    parsed = parse_qs(urlparse(raw_path).query, keep_blank_values=True)
    return {key: values[-1] if values else "" for key, values in parsed.items()}


def _gateway_read_json_body(handler: object) -> dict[str, object]:
    raw_length = getattr(handler, "headers", {}).get("Content-Length", "0")
    try:
        length = int(raw_length or "0")
    except ValueError:
        length = 0
    raw = handler.rfile.read(length) if length else b"{}"
    if not raw:
        return {}
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON body must be an object")
    return data


def _gateway_send_json_response(handler: object, payload: dict[str, object], status: int = 200) -> None:
    body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _handle_gateway_agent_get(handler: object, path: str) -> None:
    root = _gateway_handler_repo_root(handler)
    params = _gateway_query_params(handler.path)
    if path == "/agent/status":
        payload = build_gateway_agent_status(root, invocation_id=params.get("invocation_id"))
    elif path == "/agent/relay/pending":
        include_answered = params.get("include_answered", "").lower() in {"1", "true", "yes"}
        payload = build_gateway_agent_pending_relays(
            root,
            invocation_id=params.get("invocation_id"),
            include_answered=include_answered,
        )
    elif path == "/agent/receipts/recent":
        try:
            limit = int(params.get("limit", "20") or "20")
        except ValueError:
            limit = 20
        payload = build_gateway_agent_recent_receipts(root, limit=limit)
    else:  # pragma: no cover - guarded by route predicate
        payload = {"ok": False, "error": "UNKNOWN_AGENT_GET_PATH", "path": path}
    _gateway_send_json_response(handler, payload, status=200 if payload.get("ok", True) else 400)


def _handle_gateway_agent_post(handler: object, path: str) -> None:
    root = _gateway_handler_repo_root(handler)
    try:
        body = _gateway_read_json_body(handler)
        if path == "/agent/invoke":
            payload = submit_gateway_agent_invocation(root, body)
        elif path == "/agent/relay/respond":
            payload = submit_gateway_agent_relay_response(root, body)
        elif path == "/agent/control":
            payload = submit_gateway_agent_control(root, body)
        elif path == "/agent/settle":
            payload = submit_gateway_agent_settlement(root, body)
        else:  # pragma: no cover - guarded by route predicate
            payload = {"ok": False, "error": "UNKNOWN_AGENT_POST_PATH", "path": path}
    except Exception as exc:
        payload = {"ok": False, "error": "AGENT_ENDPOINT_EXCEPTION", "detail": str(exc)}
    _gateway_send_json_response(handler, payload, status=200 if payload.get("ok") else 400)

if __name__ == "__main__":
    raise SystemExit(main())
