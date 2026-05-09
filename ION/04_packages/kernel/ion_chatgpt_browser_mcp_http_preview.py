"""V121 local HTTP MCP preview for the ChatGPT browser connector.

This is a local preview harness for the V120 ChatGPT-browser connector
contract. It handles a small JSON-RPC MCP subset over HTTP-shaped payloads, but
it is not a public hosted connector and does not claim deployment authority.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qs, urlencode, urlparse

from .ion_chatgpt_browser_mcp_connector_contract import (
    BOUNDED_QUEUE_RECEIPT_TOOLS,
    FORBIDDEN_CAPABILITIES,
    STATUS_READ_TOOLS,
    audit_chatgpt_browser_mcp_connector_contract,
    call_chatgpt_connector_tool,
)
from .ion_cockpit_view_model import build_cockpit_view_model
from .ion_dual_codex_chat import (
    WRITE_CONFIRMATION_TOKEN,
    build_dual_codex_chat_model,
    pin_dual_chat_memory,
    queue_chat_codex_work_packet,
    record_chat_turn,
    render_dual_codex_chat_html,
)
from .ion_local_cockpit_app import build_cockpit_html
from .ion_public_cockpit_auth import (
    ALLOWED_EMAILS_ENV,
    GOOGLE_CLIENT_ID_ENV,
    GOOGLE_CLIENT_SECRET_ENV,
    GOOGLE_REDIRECT_URI_ENV,
    INVITE_TOKENS_ENV,
    OAUTH_STATE_COOKIE,
    PUBLIC_COCKPIT_TOKEN_ENV,
    SESSION_COOKIE,
    SESSION_SECRET_ENV,
    auth_status,
    authorize_google_user,
    build_google_authorization_url,
    clear_cookie_header,
    cockpit_session_secret,
    exchange_google_code_for_userinfo,
    google_oauth_configured,
    make_oauth_state_cookie,
    make_session_cookie,
    safe_next_path,
    validate_oauth_state_cookie,
    validate_permission_token,
    validate_session_cookie,
)

SCHEMA_ID = "ion.chatgpt_browser_http_mcp_preview.v1"
VERSION_LINE = "V121_CHATGPT_BROWSER_HTTP_MCP_PREVIEW"
READY_VERDICT = "ION_CHATGPT_BROWSER_HTTP_MCP_PREVIEW_READY"
BLOCKED_VERDICT = "ION_CHATGPT_BROWSER_HTTP_MCP_PREVIEW_BLOCKED"
WRITE_CONFIRMATION_TOKEN = "ION_BOUNDED_WRITE_CONFIRMED"
DEFAULT_BIND_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/CHATGPT_BROWSER_HTTP_MCP_PREVIEW_V121.json")
APP_PATHS = {"/", "/app", "/ion"}


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True)


def _html_text(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _tool_schema(name: str) -> dict[str, Any]:
    if name == "ion_read_active_packet":
        return {
            "type": "object",
            "properties": {"packet": {"type": "string"}},
            "required": ["packet"],
            "additionalProperties": False,
        }
    if name == "ion_carrier_onboarding_packet":
        return {
            "type": "object",
            "properties": {
                "carrier": {"type": "string"},
                "carrier_profile": {"type": "string"},
            },
            "additionalProperties": False,
        }
    if name == "ion_receipt_search":
        return {
            "type": "object",
            "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 50}},
            "additionalProperties": False,
        }
    if name == "ion_codex_work_queue":
        return {
            "type": "object",
            "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 100}},
            "additionalProperties": False,
        }
    if name == "ion_file_read":
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "max_bytes": {"type": "integer", "minimum": 1, "maximum": 262144},
            },
            "required": ["path"],
            "additionalProperties": False,
        }
    if name == "ion_file_search":
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "roots": {"type": "array", "items": {"type": "string"}, "maxItems": 10},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100},
                "max_files": {"type": "integer", "minimum": 1, "maximum": 500},
            },
            "required": ["query"],
            "additionalProperties": False,
        }
    if name == "ion_tree_list":
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "max_depth": {"type": "integer", "minimum": 0, "maximum": 6},
                "limit": {"type": "integer", "minimum": 1, "maximum": 1000},
            },
            "additionalProperties": False,
        }
    if name in {"ion_registry_read", "ion_template_read"}:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "name": {"type": "string"},
                "max_bytes": {"type": "integer", "minimum": 1, "maximum": 262144},
            },
            "additionalProperties": False,
        }
    if name == "ion_context_compile":
        return {
            "type": "object",
            "properties": {
                "profile": {"type": "string"},
                "include_excerpts": {"type": "boolean"},
            },
            "additionalProperties": False,
        }
    if name == "ion_receipt_hydrate":
        return {
            "type": "object",
            "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 100}},
            "additionalProperties": False,
        }
    if name == "ion_tool_manifest":
        return {"type": "object", "properties": {}, "additionalProperties": False}
    if name in {"ion_daemon_status", "ion_codex_queue_autorun_status"}:
        return {"type": "object", "properties": {}, "additionalProperties": False}
    if name in {"ion_agent_list", "ion_agent_status", "ion_swarm_status"}:
        return {"type": "object", "properties": {}, "additionalProperties": False}
    if name == "ion_agent_queue":
        return {
            "type": "object",
            "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 100}},
            "additionalProperties": False,
        }
    if name == "ion_agent_result":
        return {
            "type": "object",
            "properties": {"invocation_id": {"type": "string"}},
            "additionalProperties": False,
        }
    if name == "ion_agent_spawn_plan":
        return {
            "type": "object",
            "properties": {"objective": {"type": "string"}},
            "additionalProperties": False,
        }
    if name == "ion_codex_queue_process_once":
        return {
            "type": "object",
            "properties": {
                "request_path": {"type": "string"},
                "start": {"type": "boolean"},
                "max_runtime_seconds": {"type": "integer", "minimum": 30, "maximum": 7200},
                "confirmation": {"type": "string"},
            },
            "required": ["confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_agent_invoke":
        return {
            "type": "object",
            "properties": {
                "agent": {"type": "string"},
                "objective": {"type": "string"},
                "mode": {"type": "string"},
                "queue": {"type": "boolean"},
                "start": {"type": "boolean"},
                "context_refs": {"type": "array", "items": {"type": "string"}},
                "requested_by_carrier_id": {"type": "string"},
                "requested_by_callsign": {"type": "string"},
                "max_runtime_seconds": {"type": "integer", "minimum": 30, "maximum": 7200},
                "confirmation": {"type": "string"},
            },
            "required": ["agent", "objective", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_agent_cancel":
        return {
            "type": "object",
            "properties": {
                "invocation_id": {"type": "string"},
                "confirmation": {"type": "string"},
            },
            "required": ["invocation_id", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_swarm_step_once":
        return {
            "type": "object",
            "properties": {
                "request_path": {"type": "string"},
                "start": {"type": "boolean"},
                "max_runtime_seconds": {"type": "integer", "minimum": 30, "maximum": 7200},
                "confirmation": {"type": "string"},
            },
            "required": ["confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_file_put_text":
        return {
            "type": "object",
            "properties": {
                "target_path": {"type": "string"},
                "text": {"type": "string"},
                "expected_sha256": {"type": "string"},
                "overwrite": {"type": "boolean"},
                "confirmation": {"type": "string"},
            },
            "required": ["target_path", "text", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_artifact_upload_init":
        return {
            "type": "object",
            "properties": {
                "artifact_name": {"type": "string"},
                "target_path": {"type": "string"},
                "expected_sha256": {"type": "string"},
                "total_bytes": {"type": "integer", "minimum": 0},
                "mime_type": {"type": "string"},
                "confirmation": {"type": "string"},
            },
            "required": ["artifact_name", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_artifact_upload_chunk":
        return {
            "type": "object",
            "properties": {
                "upload_id": {"type": "string"},
                "chunk_index": {"type": "integer", "minimum": 0},
                "data_base64": {"type": "string"},
                "chunk_sha256": {"type": "string"},
                "confirmation": {"type": "string"},
            },
            "required": ["upload_id", "chunk_index", "data_base64", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_artifact_upload_commit":
        return {
            "type": "object",
            "properties": {
                "upload_id": {"type": "string"},
                "confirmation": {"type": "string"},
            },
            "required": ["upload_id", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_carrier_message_send":
        return {
            "type": "object",
            "properties": {
                "sender_carrier_id": {"type": "string"},
                "recipient": {"type": "string"},
                "channel": {"type": "string"},
                "message_type": {"type": "string"},
                "body": {"type": "string"},
                "context_refs": {"type": "array", "items": {"type": "string"}},
                "receipt_refs": {"type": "array", "items": {"type": "string"}},
                "confirmation": {"type": "string"},
            },
            "required": ["sender_carrier_id", "recipient", "body", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_carrier_message_poll":
        return {
            "type": "object",
            "properties": {
                "recipient": {"type": "string"},
                "channel": {"type": "string"},
                "include_acked": {"type": "boolean"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100},
            },
            "additionalProperties": False,
        }
    if name == "ion_carrier_message_ack":
        return {
            "type": "object",
            "properties": {
                "message_id": {"type": "string"},
                "ack_by_carrier": {"type": "string"},
                "confirmation": {"type": "string"},
            },
            "required": ["message_id", "ack_by_carrier", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_queue_operator_message":
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "priority": {"type": "integer", "minimum": 0, "maximum": 100},
                "confirmation": {"type": "string"},
            },
            "required": ["message", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_request_codex_work_packet":
        return {
            "type": "object",
            "properties": {
                "objective": {"type": "string"},
                "confirmation": {"type": "string"},
                "codex_model_move": {
                    "type": "object",
                    "description": "Optional deterministic Codex CLI model-move plan created by ION.",
                    "additionalProperties": True,
                },
                "required_context_reads": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "kind": {"type": "string"},
                            "path": {"type": "string"},
                            "required": {"type": "boolean"},
                        },
                        "required": ["path"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["objective", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_submit_task_return":
        return {
            "type": "object",
            "properties": {
                "task_output_text": {"type": "string"},
                "context_receipt": {"type": "object"},
                "work_request_id": {"type": "string"},
                "work_request_path": {"type": "string"},
                "confirmation": {"type": "string"},
            },
            "required": ["task_output_text", "context_receipt", "confirmation"],
            "additionalProperties": True,
        }
    if name == "ion_record_chatgpt_decision":
        return {
            "type": "object",
            "properties": {
                "decision": {"type": "string"},
                "rationale": {"type": "string"},
                "confirmation": {"type": "string"},
            },
            "required": ["decision", "confirmation"],
            "additionalProperties": False,
        }
    if name == "ion_create_containment_receipt":
        return {
            "type": "object",
            "properties": {
                "target_path": {"type": "string"},
                "transition": {"type": "string"},
                "reason": {"type": "string"},
                "confirmation": {"type": "string"},
            },
            "required": ["target_path", "reason", "confirmation"],
            "additionalProperties": False,
        }
    return {"type": "object", "properties": {}, "additionalProperties": False}


def http_mcp_tool_list() -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    for name in sorted(STATUS_READ_TOOLS | BOUNDED_QUEUE_RECEIPT_TOOLS):
        write_tool = name in BOUNDED_QUEUE_RECEIPT_TOOLS
        tools.append({
            "name": name,
            "description": (
                "ION bounded queue/receipt tool; requires explicit ION write confirmation."
                if write_tool
                else "ION bounded status/read tool."
            ),
            "inputSchema": _tool_schema(name),
            "annotations": {
                "readOnlyHint": not write_tool,
                "destructiveHint": False,
                "idempotentHint": not write_tool,
                "openWorldHint": False,
            },
        })
    return tools


def _jsonrpc_result(msg_id: Any, result: Mapping[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "result": dict(result)}


def _jsonrpc_error(msg_id: Any, message: str, code: int = -32000) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def _tool_call_result(tool_name: str, result: Mapping[str, Any], *, is_error: bool) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": _json_text(result)}],
        "structuredContent": dict(result),
        "isError": is_error,
    }


def _requires_write_confirmation(tool_name: str, args: Mapping[str, Any]) -> bool:
    return tool_name in BOUNDED_QUEUE_RECEIPT_TOOLS and args.get("confirmation") != WRITE_CONFIRMATION_TOKEN


def handle_mcp_jsonrpc(root: str | Path, payload: Mapping[str, Any]) -> dict[str, Any] | None:
    method = payload.get("method")
    msg_id = payload.get("id")
    params = payload.get("params") or {}
    if method and str(method).startswith("notifications/"):
        return None

    if method == "initialize":
        return _jsonrpc_result(msg_id, {
            "protocolVersion": params.get("protocolVersion") or "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "ion-chatgpt-browser-preview", "version": VERSION_LINE},
        })
    if method == "tools/list":
        return _jsonrpc_result(msg_id, {"tools": http_mcp_tool_list()})
    if method == "tools/call":
        tool_name = str(params.get("name") or "")
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, Mapping):
            return _jsonrpc_error(msg_id, "Tool arguments must be an object")
        if tool_name in FORBIDDEN_CAPABILITIES:
            blocked = {
                "schema_id": "ion.chatgpt_browser_http_mcp_tool_result.v1",
                "tool": tool_name,
                "ok": False,
                "finding": "forbidden_capability",
                "production_authority": False,
                "live_execution_authority": False,
            }
            return _jsonrpc_result(msg_id, _tool_call_result(tool_name, blocked, is_error=True))
        if _requires_write_confirmation(tool_name, arguments):
            blocked = {
                "schema_id": "ion.chatgpt_browser_http_mcp_tool_result.v1",
                "tool": tool_name,
                "ok": False,
                "finding": "bounded_write_confirmation_required",
                "required_confirmation": WRITE_CONFIRMATION_TOKEN,
                "production_authority": False,
                "live_execution_authority": False,
            }
            return _jsonrpc_result(msg_id, _tool_call_result(tool_name, blocked, is_error=True))

        clean_args = dict(arguments)
        clean_args.pop("confirmation", None)
        result = call_chatgpt_connector_tool(root, tool_name, clean_args)
        return _jsonrpc_result(msg_id, _tool_call_result(tool_name, result, is_error=not bool(result.get("ok"))))
    if method == "ping":
        return _jsonrpc_result(msg_id, {})
    return _jsonrpc_error(msg_id, f"Unsupported MCP method: {method}")


def audit_http_mcp_preview(root: str | Path | None = None) -> dict[str, Any]:
    contract = audit_chatgpt_browser_mcp_connector_contract(root)
    findings: list[str] = []
    tool_names = {tool["name"] for tool in http_mcp_tool_list()}
    allowed = STATUS_READ_TOOLS | BOUNDED_QUEUE_RECEIPT_TOOLS
    if tool_names != allowed:
        findings.append("http_tool_list_does_not_match_v120_contract")
    if tool_names & FORBIDDEN_CAPABILITIES:
        findings.append("http_tool_list_exposes_forbidden_capability")
    for tool in http_mcp_tool_list():
        if tool["name"] in BOUNDED_QUEUE_RECEIPT_TOOLS and "confirmation" not in tool["inputSchema"].get("properties", {}):
            findings.append(f"write_tool_missing_confirmation_schema:{tool['name']}")
    if not contract.get("accepted"):
        findings.append("v120_connector_contract_not_ready")
    ready = not findings
    return {
        "schema_id": SCHEMA_ID,
        "version_line": VERSION_LINE,
        "verdict": READY_VERDICT if ready else BLOCKED_VERDICT,
        "accepted": ready,
        "connector_state": "LOCAL_HTTP_PREVIEW_NOT_PUBLIC_CONNECTOR" if ready else "BLOCKED",
        "endpoint_path": "/mcp",
        "public_cockpit_auth": auth_status(),
        "default_bind_host": DEFAULT_BIND_HOST,
        "default_port": DEFAULT_PORT,
        "write_confirmation_required": True,
        "write_confirmation_token": WRITE_CONFIRMATION_TOKEN,
        "allowed_tools": sorted(allowed),
        "forbidden_tools": sorted(FORBIDDEN_CAPABILITIES),
        "findings": findings,
        "production_authority": False,
        "live_execution_authority": False,
        "deployment_authority": False,
    }


def render_ion_connector_landing(root: str | Path, *, public_base_url: str | None = None) -> str:
    """Render a safe human-facing landing page for the tunnel root.

    The page intentionally exposes only connector posture and tool names. It does
    not expose secrets, local absolute paths, source excerpts, or shell controls.
    """

    audit = audit_http_mcp_preview(root)
    base = (public_base_url or "").rstrip("/")
    connector_hint = f"{base}/mcp" if base else "/mcp"
    health_hint = f"{base}/health" if base else "/health"
    status_class = "ready" if audit.get("accepted") else "blocked"
    allowed_tools = audit.get("allowed_tools") if isinstance(audit.get("allowed_tools"), list) else []
    forbidden_tools = audit.get("forbidden_tools") if isinstance(audit.get("forbidden_tools"), list) else []
    findings = audit.get("findings") if isinstance(audit.get("findings"), list) else []
    tool_items = "\n".join(f"<li><code>{_html_text(tool)}</code></li>" for tool in allowed_tools[:80])
    forbidden_items = "\n".join(f"<li><code>{_html_text(tool)}</code></li>" for tool in forbidden_tools[:80])
    finding_items = "\n".join(f"<li>{_html_text(item)}</li>" for item in findings) or "<li>none</li>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>ION Connector</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #101112;
      --panel: #181a1b;
      --line: #303336;
      --text: #f4f4f2;
      --muted: #a8a8a1;
      --ok: #20d88f;
      --warn: #ff9f43;
      --accent: #ff7a1a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.45;
    }}
    main {{
      max-width: 1040px;
      margin: 0 auto;
      padding: 48px 22px 56px;
    }}
    header {{
      border-bottom: 1px solid var(--line);
      padding-bottom: 22px;
      margin-bottom: 22px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(34px, 7vw, 68px);
      line-height: 0.94;
      letter-spacing: 0;
    }}
    h2 {{
      margin: 0 0 12px;
      font-size: 18px;
      letter-spacing: 0;
    }}
    p {{ color: var(--muted); max-width: 760px; }}
    code {{
      background: #0b0c0d;
      border: 1px solid #26292b;
      border-radius: 6px;
      color: #f5d0b4;
      padding: 2px 5px;
      overflow-wrap: anywhere;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }}
    .status {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 10px;
      border: 1px solid var(--line);
      border-radius: 999px;
      color: var(--muted);
      font-size: 13px;
    }}
    .dot {{
      width: 9px;
      height: 9px;
      border-radius: 999px;
      background: var(--warn);
      box-shadow: 0 0 14px rgba(255, 159, 67, 0.42);
    }}
    .status.ready .dot {{
      background: var(--ok);
      box-shadow: 0 0 14px rgba(32, 216, 143, 0.42);
    }}
    .status.blocked .dot {{
      background: #ff6565;
      box-shadow: 0 0 14px rgba(255, 101, 101, 0.42);
    }}
    .laws {{
      display: grid;
      gap: 8px;
      margin: 14px 0 0;
      padding: 0;
      list-style: none;
    }}
    .laws li {{
      border-left: 2px solid var(--accent);
      padding-left: 10px;
      color: var(--muted);
    }}
    .tools {{
      columns: 2;
      padding-left: 18px;
      color: var(--muted);
    }}
    @media (max-width: 760px) {{
      .grid {{ grid-template-columns: 1fr; }}
      .tools {{ columns: 1; }}
      main {{ padding-top: 28px; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div class="status {status_class}"><span class="dot"></span><span>{_html_text(audit.get("verdict"))}</span></div>
      <h1>ION Connector</h1>
      <p>A bounded browser-carrier surface for ION. This page is a status/UI landing surface; MCP tools remain on <code>{_html_text(connector_hint)}</code>.</p>
    </header>
    <section class="grid" aria-label="connector summary">
      <article class="card">
        <h2>Current Surface</h2>
        <p>Endpoint path: <code>{_html_text(audit.get("endpoint_path"))}</code></p>
        <p>Health JSON: <code>{_html_text(health_hint)}</code></p>
        <p>Write confirmation required: <code>{_html_text(audit.get("write_confirmation_required"))}</code></p>
      </article>
      <article class="card">
        <h2>Authority Boundary</h2>
        <ul class="laws">
          <li>Production authority: <code>{_html_text(audit.get("production_authority"))}</code></li>
          <li>Live execution authority: <code>{_html_text(audit.get("live_execution_authority"))}</code></li>
          <li>Deployment authority: <code>{_html_text(audit.get("deployment_authority"))}</code></li>
        </ul>
      </article>
      <article class="card">
        <h2>Allowed MCP Tools</h2>
        <ul class="tools">{tool_items}</ul>
      </article>
      <article class="card">
        <h2>Blocked Capabilities</h2>
        <ul class="tools">{forbidden_items}</ul>
        <h2>Findings</h2>
        <ul>{finding_items}</ul>
      </article>
    </section>
  </main>
</body>
</html>
"""


def render_public_cockpit_login(
    *,
    next_path: str = "/cockpit/chat",
    finding: str | None = None,
    env: Mapping[str, str] | None = None,
) -> str:
    status = auth_status(env)
    google_enabled = bool(status.get("google_oauth_configured"))
    token_enabled = bool(status.get("permission_token_configured"))
    allowed_count = int(status.get("google_allowed_email_count") or 0)
    google_status = (
        f"Google OAuth is configured. Allowed Google emails: {allowed_count}."
        if google_enabled
        else f"Google OAuth still needs client ID and secret. Allowed Google emails already listed: {allowed_count}."
    )
    finding_messages = {
        "google_oauth_state_missing_or_invalid": "Google login is not enabled yet. Use the permission token for now.",
        "google_oauth_not_configured": "Google login is not enabled yet. Use the permission token for now.",
        "google_oauth_state_mismatch": "Google login expired. Start again from this page after Google setup is complete.",
        "permission_token_invalid": "Permission token did not match.",
        "permission_token_required": "Enter the permission token.",
    }
    finding_text = finding_messages.get(str(finding or ""), str(finding or ""))
    finding_html = f"<p class=\"error\">{_html_text(finding_text)}</p>" if finding_text else ""
    google_button = (
        "<button type=\"submit\">Continue with Google</button>"
        if google_enabled
        else "<button type=\"submit\" disabled>Google OAuth setup needed</button>"
    )
    token_button = (
        "<button type=\"submit\">Login with permission token</button>"
        if token_enabled
        else "<button type=\"submit\" disabled>Permission token not configured</button>"
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <title>ION Cockpit Login</title>
  <style>
    :root {{ color-scheme: dark; --bg:#090b0c; --panel:#121619; --line:#2b343a; --text:#edf2f4; --muted:#9aa7ad; --blue:#65a7e8; --red:#e15f5f; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; min-height:100vh; display:grid; place-items:center; background:var(--bg); color:var(--text); }}
    main {{ width:min(920px, calc(100vw - 32px)); display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
    header {{ grid-column:1 / -1; border-bottom:1px solid var(--line); padding-bottom:14px; }}
    h1,h2,p {{ margin:0; letter-spacing:0; }}
    h1 {{ font-size:32px; }}
    h2 {{ font-size:16px; margin-bottom:8px; }}
    p {{ color:var(--muted); line-height:1.4; }}
    section {{ background:var(--panel); border:1px solid var(--line); border-radius:7px; padding:14px; }}
    form {{ display:grid; gap:8px; margin-top:12px; }}
    label {{ color:var(--muted); font-size:13px; }}
    input {{ width:100%; border:1px solid var(--line); border-radius:5px; background:#0d1113; color:var(--text); padding:9px; font:inherit; }}
    button {{ justify-self:start; border:1px solid var(--line); background:#18242b; color:var(--text); border-radius:5px; padding:8px 11px; font-weight:700; cursor:pointer; }}
    button:disabled {{ opacity:.55; cursor:not-allowed; }}
    .error {{ grid-column:1 / -1; color:var(--red); }}
    code {{ color:#f5d0b4; overflow-wrap:anywhere; }}
    @media (max-width:760px) {{ main {{ grid-template-columns:1fr; }} }}
  </style>
</head>
<body>
<main>
  <header>
    <h1>ION Cockpit Login</h1>
    <p>Access is limited to signed cockpit sessions, permission tokens, or approved Google accounts. This login does not grant production authority.</p>
  </header>
  {finding_html}
  <section>
    <h2>Permission Token</h2>
    <p>Use the current ION cockpit permission token or an invited token.</p>
    <form method="post" action="/cockpit/auth/token">
      <input type="hidden" name="next" value="{_html_text(safe_next_path(next_path))}">
      <label for="permission_token">Token</label>
      <input id="permission_token" name="permission_token" type="password" autocomplete="current-password">
      {token_button}
    </form>
  </section>
  <section>
    <h2>Google Account</h2>
    <p>{_html_text(google_status)}</p>
    <p>Allowed emails are controlled by <code>{ALLOWED_EMAILS_ENV}</code>. An invite token can permit an additional Google account.</p>
    <form method="post" action="/cockpit/auth/google/start">
      <input type="hidden" name="next" value="{_html_text(safe_next_path(next_path))}">
      <label for="invite_token">Invite token, optional</label>
      <input id="invite_token" name="invite_token" type="password" autocomplete="one-time-code">
      {google_button}
    </form>
  </section>
</main>
</body>
</html>"""


def write_http_mcp_preview_audit(
    root: str | Path | None = None,
    *,
    output: str | Path | None = None,
) -> dict[str, Any]:
    shell_root = Path(root or ".").expanduser().resolve()
    result = audit_http_mcp_preview(shell_root)
    out = shell_root / (Path(output) if output else OUTPUT_RELATIVE_PATH)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


class IonChatGPTPreviewHandler(BaseHTTPRequestHandler):
    server_version = "IONChatGPTMCPPreview/0.1"

    def _send_json(self, status: int, payload: Mapping[str, Any]) -> None:
        body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status: int, body_text: str) -> None:
        body = body_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def _public_base_url(self) -> str:
        host = self.headers.get("host") or ""
        if not host:
            return ""
        local_host = host.startswith("127.0.0.1") or host.startswith("localhost")
        proto = self.headers.get("x-forwarded-proto") or ("http" if local_host else "https")
        return f"{proto}://{host}"

    def _secure_cookie(self) -> bool:
        return self._public_base_url().startswith("https://")

    def _request_token(self, payload: Mapping[str, Any] | None = None) -> str:
        auth = self.headers.get("authorization") or ""
        if auth.lower().startswith("bearer "):
            return auth.split(" ", 1)[1].strip()
        query = parse_qs(urlparse(self.path).query)
        if query.get("token"):
            return str(query["token"][-1])
        if payload and payload.get("public_token"):
            return str(payload.get("public_token") or "")
        return ""

    def _check_public_cockpit_access(self, payload: Mapping[str, Any] | None = None) -> tuple[bool, str | None, str | None]:
        secret = cockpit_session_secret()
        if secret:
            session = validate_session_cookie(self.headers.get("cookie"), secret=secret)
            if session.ok:
                return True, None, None
        supplied = self._request_token(payload)
        if supplied:
            token_result = validate_permission_token(supplied)
            if token_result.ok:
                return True, None, supplied
            return False, token_result.finding or "permission_token_invalid", None
        if not secret and not validate_permission_token(os.environ.get(PUBLIC_COCKPIT_TOKEN_ENV) or "").ok and not google_oauth_configured():
            return False, "public_cockpit_auth_not_configured", None
        return False, "public_cockpit_login_required", None

    def _login_path(self, next_path: str | None = None, finding: str | None = None) -> str:
        params: dict[str, str] = {"next": safe_next_path(next_path or self.path)}
        if finding:
            params["finding"] = finding
        return "/cockpit/login?" + urlencode(params)

    def _send_public_cockpit_blocked(self, finding: str, *, next_path: str | None = None) -> None:
        if not self._wants_json() and finding in {"public_cockpit_login_required", "permission_token_required", "permission_token_invalid"}:
            self._redirect(self._login_path(next_path or self.path, None if finding == "public_cockpit_login_required" else finding))
            return
        self._send_json(
            503 if finding == "public_cockpit_auth_not_configured" else 401,
            {
                "ok": False,
                "finding": finding,
                "login_path": self._login_path(next_path or self.path),
                "public_cockpit_path": "/cockpit/chat",
                "session_cookie": SESSION_COOKIE,
                "requires_env": [
                    PUBLIC_COCKPIT_TOKEN_ENV,
                    SESSION_SECRET_ENV,
                    INVITE_TOKENS_ENV,
                    GOOGLE_CLIENT_ID_ENV,
                    GOOGLE_CLIENT_SECRET_ENV,
                    GOOGLE_REDIRECT_URI_ENV,
                    ALLOWED_EMAILS_ENV,
                ],
                "production_authority": False,
                "live_execution_authority": False,
            },
        )

    def _send_login(self, *, status: int = 200, next_path: str = "/cockpit/chat", finding: str | None = None) -> None:
        self._send_html(status, render_public_cockpit_login(next_path=next_path, finding=finding))

    def _redirect_with_headers(self, target: str, headers: Mapping[str, str]) -> None:
        self.send_response(303)
        self.send_header("Location", target)
        self.send_header("Cache-Control", "no-store")
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()

    def _session_redirect(self, principal: Mapping[str, Any], next_path: str) -> None:
        secret = cockpit_session_secret()
        if not secret:
            self._send_login(status=503, next_path=next_path, finding="cockpit_session_secret_not_configured")
            return
        self._redirect_with_headers(
            safe_next_path(next_path),
            {"Set-Cookie": make_session_cookie(principal, secret=secret, secure=self._secure_cookie())},
        )

    def _read_payload(self) -> dict[str, Any]:
        length = int(self.headers.get("content-length") or "0")
        raw = self.rfile.read(length)
        content_type = (self.headers.get("content-type") or "").split(";", 1)[0].strip().lower()
        if content_type == "application/json":
            return json.loads(raw.decode("utf-8") or "{}")
        parsed = parse_qs(raw.decode("utf-8"), keep_blank_values=True)
        return {key: values[-1] if values else "" for key, values in parsed.items()}

    def _wants_json(self) -> bool:
        accept = self.headers.get("accept") or ""
        content_type = self.headers.get("content-type") or ""
        return "application/json" in accept or content_type.startswith("application/json")

    def _redirect(self, target: str) -> None:
        self.send_response(303)
        self.send_header("Location", target)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler name
        path = self.path.split("?", 1)[0]
        query = parse_qs(urlparse(self.path).query)
        if path in {"/cockpit/login", "/cockpit/login/"}:
            self._send_login(
                next_path=str(query.get("next", ["/cockpit/chat"])[-1]),
                finding=str(query.get("finding", [""])[-1]) or None,
            )
            return
        if path in {"/cockpit/logout", "/cockpit/logout/"}:
            self.send_response(303)
            self.send_header("Location", "/cockpit/login")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Set-Cookie", clear_cookie_header(SESSION_COOKIE, secure=self._secure_cookie()))
            self.send_header("Set-Cookie", clear_cookie_header(OAUTH_STATE_COOKIE, secure=self._secure_cookie()))
            self.end_headers()
            return
        if path == "/cockpit/auth/google/callback":
            if not google_oauth_configured():
                self._send_login(status=503, finding="google_oauth_not_configured")
                return
            secret = cockpit_session_secret()
            if not secret:
                self._send_login(status=503, finding="cockpit_session_secret_not_configured")
                return
            state_result = validate_oauth_state_cookie(
                self.headers.get("cookie"),
                secret=secret,
                state=str(query.get("state", [""])[-1]),
            )
            if not state_result.ok:
                self._send_login(status=401, finding=state_result.finding)
                return
            if query.get("error"):
                self._send_login(status=401, finding="google_oauth_" + str(query.get("error", ["error"])[-1]))
                return
            try:
                userinfo = exchange_google_code_for_userinfo(
                    code=str(query.get("code", [""])[-1]),
                    base_url=self._public_base_url(),
                )
                auth = authorize_google_user(userinfo, oauth_state=state_result.principal or {})
            except Exception as exc:
                self._send_login(status=401, finding=f"google_oauth_failed:{exc.__class__.__name__}")
                return
            if not auth.ok:
                self._send_login(status=401, finding=auth.finding)
                return
            self.send_response(303)
            self.send_header("Location", safe_next_path(str((state_result.principal or {}).get("next") or "/cockpit/chat")))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Set-Cookie", make_session_cookie(auth.principal or {}, secret=secret, secure=self._secure_cookie()))
            self.send_header("Set-Cookie", clear_cookie_header(OAUTH_STATE_COOKIE, secure=self._secure_cookie()))
            self.end_headers()
            return
        if path in {"/cockpit", "/cockpit/"}:
            ok, finding, token = self._check_public_cockpit_access()
            if not ok:
                self._send_public_cockpit_blocked(str(finding), next_path="/cockpit")
                return
            html_text = build_cockpit_html(build_cockpit_view_model(self.server.ion_root))  # type: ignore[attr-defined]
            replacement = f'href="/cockpit?token={_html_text(token)}"' if token else 'href="/cockpit"'
            self._send_html(200, html_text.replace('href="/cockpit"', replacement))
            return
        if path in {"/cockpit/chat", "/cockpit/chat/"}:
            ok, finding, token = self._check_public_cockpit_access()
            if not ok:
                self._send_public_cockpit_blocked(str(finding), next_path="/cockpit/chat")
                return
            model = build_dual_codex_chat_model(self.server.ion_root, write=True)  # type: ignore[attr-defined]
            self._send_html(200, render_dual_codex_chat_html(model, base_path="/cockpit/chat", auth_token=token))
            return
        if path == "/cockpit/model.json":
            ok, finding, _token = self._check_public_cockpit_access()
            if not ok:
                self._send_public_cockpit_blocked(str(finding), next_path="/cockpit/model.json")
                return
            self._send_json(200, build_cockpit_view_model(self.server.ion_root))  # type: ignore[attr-defined]
            return
        if path == "/cockpit/chat/model.json":
            ok, finding, _token = self._check_public_cockpit_access()
            if not ok:
                self._send_public_cockpit_blocked(str(finding), next_path="/cockpit/chat/model.json")
                return
            self._send_json(200, build_dual_codex_chat_model(self.server.ion_root))  # type: ignore[attr-defined]
            return
        if path in APP_PATHS:
            self._send_html(
                200,
                render_ion_connector_landing(self.server.ion_root, public_base_url=self._public_base_url()),  # type: ignore[attr-defined]
            )
            return
        if path == "/app/status.json":
            self._send_json(200, audit_http_mcp_preview(self.server.ion_root))  # type: ignore[attr-defined]
            return
        if path != "/health":
            self._send_json(404, {"ok": False, "error": "not_found"})
            return
        self._send_json(200, audit_http_mcp_preview(self.server.ion_root))  # type: ignore[attr-defined]

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler name
        path = self.path.split("?", 1)[0]
        if path == "/cockpit/auth/token":
            payload = self._read_payload()
            next_path = safe_next_path(str(payload.get("next") or "/cockpit/chat"))
            token_result = validate_permission_token(str(payload.get("permission_token") or ""))
            if not token_result.ok:
                self._send_login(status=401, next_path=next_path, finding=token_result.finding)
                return
            self._session_redirect(token_result.principal or {}, next_path)
            return
        if path == "/cockpit/auth/google/start":
            payload = self._read_payload()
            next_path = safe_next_path(str(payload.get("next") or "/cockpit/chat"))
            if not google_oauth_configured():
                self._send_login(status=503, next_path=next_path, finding="google_oauth_not_configured")
                return
            secret = cockpit_session_secret()
            if not secret:
                self._send_login(status=503, next_path=next_path, finding="cockpit_session_secret_not_configured")
                return
            nonce, state_cookie = make_oauth_state_cookie(
                secret=secret,
                next_path=next_path,
                invite_token=str(payload.get("invite_token") or ""),
                secure=self._secure_cookie(),
            )
            self._redirect_with_headers(
                build_google_authorization_url(base_url=self._public_base_url(), state=nonce),
                {"Set-Cookie": state_cookie},
            )
            return
        if path in {"/cockpit/chat/turn", "/cockpit/chat/queue", "/cockpit/chat/memory"}:
            try:
                payload = self._read_payload()
                ok, finding, token = self._check_public_cockpit_access(payload)
                if not ok:
                    self._send_public_cockpit_blocked(str(finding), next_path="/cockpit/chat")
                    return
                if path == "/cockpit/chat/turn":
                    result = record_chat_turn(
                        self.server.ion_root,  # type: ignore[attr-defined]
                        lane_id=str(payload.get("lane_id") or ""),
                        message=str(payload.get("message") or ""),
                        author=str(payload.get("author") or "operator"),
                        execution_mode=str(payload.get("execution_mode") or ""),
                    )
                elif path == "/cockpit/chat/queue":
                    result = queue_chat_codex_work_packet(
                        self.server.ion_root,  # type: ignore[attr-defined]
                        lane_id=str(payload.get("lane_id") or ""),
                        objective=str(payload.get("objective") or ""),
                        confirmation=str(payload.get("confirmation") or ""),
                    )
                else:
                    result = pin_dual_chat_memory(
                        self.server.ion_root,  # type: ignore[attr-defined]
                        lane_id=str(payload.get("lane_id") or ""),
                        text=str(payload.get("text") or ""),
                        source_turn_id=str(payload.get("source_turn_id") or "") or None,
                        confirmation=str(payload.get("confirmation") or WRITE_CONFIRMATION_TOKEN),
                    )
            except Exception as exc:
                result = {"ok": False, "finding": "request_failed", "error": exc.__class__.__name__}
                token = None
            if self._wants_json():
                self._send_json(200 if result.get("ok") else 400, result)
                return
            suffix = f"?token={token}" if token else ""
            self._redirect(f"/cockpit/chat{suffix}")
            return
        if path != "/mcp":
            self._send_json(404, {"ok": False, "error": "not_found"})
            return
        length = int(self.headers.get("content-length") or "0")
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
            response = handle_mcp_jsonrpc(self.server.ion_root, payload)  # type: ignore[attr-defined]
        except Exception as exc:
            self._send_json(400, {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}})
            return
        if response is None:
            self.send_response(204)
            self.end_headers()
            return
        self._send_json(200, response)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002 - stdlib signature
        return


def make_http_server(root: str | Path, host: str = DEFAULT_BIND_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), IonChatGPTPreviewHandler)
    server.ion_root = Path(root).resolve()  # type: ignore[attr-defined]
    return server


def documented_launch_requests_serve(argv: list[str]) -> bool:
    """Honor the V120 setup-guide launch shape without changing no-arg audit mode."""
    explicit_bind = any(arg in {"--host", "--port"} or arg.startswith("--host=") or arg.startswith("--port=") for arg in argv)
    explicit_audit = any(arg in {"--self-test", "--write", "--json"} for arg in argv)
    return explicit_bind and not explicit_audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ION ChatGPT browser HTTP MCP preview.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--host", default=DEFAULT_BIND_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--json", action="store_true")
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = parser.parse_args(argv)
    serve_requested = args.serve or documented_launch_requests_serve(raw_argv)

    if args.write:
        result = write_http_mcp_preview_audit(args.ion_root, output=args.output)
        print(json.dumps(result, indent=2, sort_keys=True) if args.json or args.self_test else result["verdict"])
        return 0 if result["accepted"] else 1

    if args.self_test or not serve_requested:
        result = audit_http_mcp_preview(args.ion_root)
        print(json.dumps(result, indent=2, sort_keys=True) if args.json or args.self_test else result["verdict"])
        return 0 if result["accepted"] else 1

    server = make_http_server(args.ion_root, args.host, args.port)
    print(f"ION ChatGPT HTTP MCP preview listening on http://{args.host}:{args.port}/mcp")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()


if __name__ == "__main__":
    raise SystemExit(main())
