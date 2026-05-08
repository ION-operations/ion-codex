"""V121 local HTTP MCP preview for the ChatGPT browser connector.

This is a local preview harness for the V120 ChatGPT-browser connector
contract. It handles a small JSON-RPC MCP subset over HTTP-shaped payloads, but
it is not a public hosted connector and does not claim deployment authority.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping

from .ion_chatgpt_browser_mcp_connector_contract import (
    BOUNDED_QUEUE_RECEIPT_TOOLS,
    FORBIDDEN_CAPABILITIES,
    STATUS_READ_TOOLS,
    audit_chatgpt_browser_mcp_connector_contract,
    call_chatgpt_connector_tool,
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
            "properties": {"objective": {"type": "string"}, "confirmation": {"type": "string"}},
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
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status: int, body_text: str) -> None:
        body = body_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def _public_base_url(self) -> str:
        host = self.headers.get("host") or ""
        if not host:
            return ""
        proto = self.headers.get("x-forwarded-proto") or ("https" if host.endswith(".trycloudflare.com") else "http")
        return f"{proto}://{host}"

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler name
        path = self.path.split("?", 1)[0]
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
        if self.path != "/mcp":
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
