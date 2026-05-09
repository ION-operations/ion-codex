"""Local-only ION cockpit web app.

This app renders the live cockpit projection for the operator. It is a
visibility surface only: no state writes, no shell bridge, no production or live
execution authority.
"""

from __future__ import annotations

import argparse
import html
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .ion_cockpit_view_model import build_cockpit_view_model
from .ion_dual_codex_chat import (
    WRITE_CONFIRMATION_TOKEN,
    build_dual_codex_chat_model,
    pin_dual_chat_memory,
    queue_chat_codex_work_packet,
    record_chat_turn,
    render_dual_codex_chat_html,
)

SCHEMA_ID = "ion.local_cockpit_app.v1"
READY_VERDICT = "ION_LOCAL_COCKPIT_APP_READY"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8788


def _text(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    return str(value)


def _escape(value: Any) -> str:
    return html.escape(_text(value), quote=True)


def _status_class(value: Any) -> str:
    lowered = _text(value, "unknown").lower().replace("_", "-")
    if lowered in {"ready", "configured", "active"}:
        return "is-ready"
    if lowered in {"blocked", "degraded", "missing-template", "not-running"}:
        return "is-blocked"
    return "is-watch"


def build_cockpit_health(root: str | Path = ".") -> dict[str, Any]:
    shell_root = Path(root).expanduser().resolve()
    return {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT,
        "status": "ready",
        "shell_root": shell_root.as_posix(),
        "bind_host": DEFAULT_HOST,
        "default_port": DEFAULT_PORT,
        "visibility_only": True,
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_cockpit_html(model: dict[str, Any]) -> str:
    runtime = model.get("runtime") if isinstance(model.get("runtime"), dict) else {}
    top = model.get("top_bar") if isinstance(model.get("top_bar"), dict) else {}
    services = model.get("local_services") if isinstance(model.get("local_services"), dict) else {}
    service_rows = services.get("services") if isinstance(services.get("services"), list) else []
    mcp = model.get("chatgpt_browser_mcp") if isinstance(model.get("chatgpt_browser_mcp"), dict) else {}
    codex = mcp.get("codex_queue_runner") if isinstance(mcp.get("codex_queue_runner"), dict) else {}
    agent_broker = mcp.get("agent_invocation_broker") if isinstance(mcp.get("agent_invocation_broker"), dict) else {}
    queues = model.get("queues") if isinstance(model.get("queues"), dict) else {}
    timeline = model.get("timeline") if isinstance(model.get("timeline"), list) else []
    receipts = model.get("receipts") if isinstance(model.get("receipts"), list) else []

    def metric(label: str, value: Any) -> str:
        return f"<div class=\"metric\"><span>{_escape(label)}</span><b>{_escape(value)}</b></div>"

    def service_row(row: dict[str, Any]) -> str:
        status = _text(row.get("status"), "unknown")
        endpoint = row.get("public_url") or row.get("health_url") or row.get("local_url") or ""
        findings = ", ".join(str(item) for item in row.get("findings", []) if item)
        return (
            "<tr>"
            f"<td>{_escape(row.get('unit_name'))}</td>"
            f"<td><span class=\"pill {_status_class(status)}\">{_escape(status)}</span>"
            f"<small>{_escape(findings)}</small></td>"
            f"<td class=\"path\">{_escape(endpoint)}</td>"
            "</tr>"
        )

    def timeline_card(event: dict[str, Any]) -> str:
        status = _text(event.get("status"), "unknown")
        detail = event.get("detail") or event.get("path") or ""
        return (
            f"<article class=\"timeline-card {_status_class(status)}\">"
            f"<b>{_escape(event.get('source'))}</b>"
            f"<span>{_escape(event.get('event_type'))}</span>"
            f"<em>{_escape(status)}</em>"
            f"<p>{_escape(detail)}</p>"
            "</article>"
        )

    receipt_cards = []
    for receipt in receipts[:20]:
        if not isinstance(receipt, dict):
            continue
        receipt_cards.append(
            "<article class=\"receipt-card\">"
            f"<b>{_escape(receipt.get('name') or 'receipt')}</b>"
            f"<span>{_escape(receipt.get('authority_class') or 'RECEIPT')}</span>"
            f"<p class=\"path\">{_escape(receipt.get('path') or '')}</p>"
            "</article>"
        )

    timeline_cards = [timeline_card(event) for event in timeline[:40] if isinstance(event, dict)]
    service_table = "".join(service_row(row) for row in service_rows if isinstance(row, dict))
    human_gates = queues.get("human_gates") if isinstance(queues.get("human_gates"), list) else []
    steward_items = queues.get("steward_integration") if isinstance(queues.get("steward_integration"), list) else []

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="20">
<title>ION Local Cockpit</title>
<style>
:root {{
  color-scheme: dark;
  --bg: #090b0c;
  --panel: #111517;
  --panel-2: #151b1e;
  --line: #293237;
  --text: #e6ecef;
  --muted: #8d9aa0;
  --green: #57c785;
  --amber: #d3a847;
  --red: #e15f5f;
  --blue: #6aa9e9;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--text); }}
main {{ min-height: 100vh; display: grid; grid-template-rows: auto 1fr; }}
header {{ display: flex; align-items: center; gap: 18px; padding: 12px 16px; border-bottom: 1px solid var(--line); background: #0d1113; }}
.brand {{ font-weight: 800; letter-spacing: 0; }}
.root {{ color: var(--muted); font-size: 12px; overflow-wrap: anywhere; }}
.status {{ margin-left: auto; }}
.layout {{ display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 12px; padding: 12px; }}
.grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }}
.panel {{ background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 12px; min-width: 0; }}
.panel.wide {{ grid-column: 1 / -1; }}
h1, h2 {{ margin: 0; letter-spacing: 0; }}
h1 {{ font-size: 18px; }}
h2 {{ color: var(--muted); font-size: 11px; text-transform: uppercase; margin-bottom: 10px; }}
.objective {{ margin-top: 8px; color: var(--text); line-height: 1.4; }}
.metrics {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; margin-top: 12px; }}
.metric {{ background: var(--panel-2); border: 1px solid var(--line); border-radius: 4px; padding: 8px; min-height: 56px; }}
.metric span {{ display: block; color: var(--muted); font-size: 11px; }}
.metric b {{ display: block; margin-top: 6px; font-size: 14px; overflow-wrap: anywhere; }}
.pill {{ display: inline-flex; align-items: center; min-height: 24px; padding: 3px 8px; border-radius: 999px; border: 1px solid var(--line); font-size: 12px; }}
.is-ready {{ color: var(--green); }}
.is-watch {{ color: var(--amber); }}
.is-blocked {{ color: var(--red); }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
td, th {{ border-top: 1px solid var(--line); padding: 8px 6px; text-align: left; vertical-align: top; }}
th {{ color: var(--muted); font-size: 11px; text-transform: uppercase; }}
small {{ display: block; color: var(--muted); margin-top: 4px; }}
.path {{ color: var(--muted); overflow-wrap: anywhere; }}
.timeline {{ display: grid; gap: 8px; max-height: 540px; overflow: auto; }}
.timeline-card, .receipt-card {{ background: var(--panel-2); border: 1px solid var(--line); border-radius: 4px; padding: 9px; }}
.timeline-card b, .timeline-card span, .timeline-card em {{ display: inline-block; margin-right: 8px; font-size: 12px; }}
.timeline-card p, .receipt-card p {{ margin: 6px 0 0; }}
.rail {{ display: grid; gap: 12px; align-content: start; }}
.receipt-list {{ display: grid; gap: 8px; max-height: 420px; overflow: auto; }}
pre {{ white-space: pre-wrap; margin: 0; color: var(--muted); font-size: 12px; }}
@media (max-width: 980px) {{
  .layout {{ grid-template-columns: 1fr; }}
  .grid {{ grid-template-columns: 1fr; }}
  .metrics {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .status {{ margin-left: 0; }}
  header {{ flex-wrap: wrap; }}
}}
</style>
</head>
<body>
<main>
<header>
  <div class="brand">ION LOCAL COCKPIT</div>
  <div class="root">{_escape(runtime.get("shell_root"))}</div>
  <div class="status pill {_status_class(runtime.get("status"))}">{_escape(runtime.get("status"))}</div>
</header>
<section class="layout">
  <section class="grid">
    <article class="panel wide">
      <h1>{_escape(top.get("objective") or "No active objective")}</h1>
      <div class="objective">Visibility-only local cockpit. Codex output remains proposal until proof-gated and accepted.</div>
      <div class="metrics">
        {metric("Services", services.get("status", top.get("local_service_status", "unknown")))}
        {metric("Codex queue", codex.get("queued_request_count", 0))}
        {metric("Codex active", codex.get("active_process_running", False))}
        {metric("Agent broker", agent_broker.get("verdict", "unknown"))}
        {metric("MCP transport", mcp.get("transport_state", "unknown"))}
        {metric("Connector", mcp.get("active_connector_url", "none"))}
        {metric("Human gates", top.get("gate_count", 0))}
        {metric("Steward queue", top.get("steward_queue_count", 0))}
      </div>
    </article>
    <article class="panel wide">
      <h2>Local Services</h2>
      <table><thead><tr><th>Unit</th><th>Status</th><th>Endpoint</th></tr></thead><tbody>{service_table}</tbody></table>
    </article>
    <article class="panel">
      <h2>Codex Carrier</h2>
      {metric("Runner verdict", codex.get("verdict", "unknown"))}
      {metric("Reconciliation write", (codex.get("reconciliation") or {}).get("write", False))}
      {metric("Next request", codex.get("next_request_path", "none"))}
    </article>
    <article class="panel">
      <h2>Queues</h2>
      {metric("Human gates", len(human_gates))}
      {metric("Steward items", len(steward_items))}
      {metric("Operator pending", top.get("operator_queue_pending", 0))}
    </article>
    <article class="panel">
      <h2>Authority</h2>
      {metric("Production", model.get("production_authority", False))}
      {metric("Live execution", model.get("live_execution_authority", False))}
      {metric("Runtime blocked", runtime.get("blocked", False))}
    </article>
    <article class="panel wide">
      <h2>Runtime Timeline</h2>
      <div class="timeline">{''.join(timeline_cards) or '<p class="path">No timeline events found.</p>'}</div>
    </article>
  </section>
  <aside class="rail">
    <article class="panel">
      <h2>Recent Receipts</h2>
      <div class="receipt-list">{''.join(receipt_cards) or '<p class="path">No receipts found.</p>'}</div>
    </article>
    <article class="panel">
      <h2>Source Paths</h2>
      <pre>{_escape(json.dumps(model.get("source_paths", {}), indent=2, sort_keys=True))}</pre>
    </article>
  </aside>
</section>
</main>
</body>
</html>"""


def make_handler(root: Path) -> type[BaseHTTPRequestHandler]:
    class IonCockpitHandler(BaseHTTPRequestHandler):
        server_version = "IONLocalCockpit/0.1"

        def log_message(self, fmt: str, *args: Any) -> None:
            return

        def _send_bytes(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def _send_json(self, status: int, payload: dict[str, Any]) -> None:
            self._send_bytes(status, json.dumps(payload, indent=2, sort_keys=True).encode("utf-8"), "application/json")

        def _redirect(self, target: str) -> None:
            self.send_response(303)
            self.send_header("Location", target)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()

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

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path == "/health":
                self._send_json(200, build_cockpit_health(root))
                return
            if path == "/model.json":
                self._send_json(200, build_cockpit_view_model(root))
                return
            if path == "/chat/model.json":
                self._send_json(200, build_dual_codex_chat_model(root))
                return
            if path in {"/chat", "/chat/"}:
                model = build_dual_codex_chat_model(root, write=True)
                self._send_bytes(200, render_dual_codex_chat_html(model).encode("utf-8"), "text/html; charset=utf-8")
                return
            if path in {"/", "/app", "/cockpit"}:
                model = build_cockpit_view_model(root)
                self._send_bytes(200, build_cockpit_html(model).encode("utf-8"), "text/html; charset=utf-8")
                return
            self._send_json(404, {"ok": False, "finding": "not_found", "path": path})

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path not in {"/chat/turn", "/chat/queue", "/chat/memory"}:
                self._send_json(404, {"ok": False, "finding": "not_found", "path": path})
                return
            try:
                payload = self._read_payload()
                if path == "/chat/turn":
                    result = record_chat_turn(
                        root,
                        lane_id=str(payload.get("lane_id") or ""),
                        message=str(payload.get("message") or ""),
                        author=str(payload.get("author") or "operator"),
                        execution_mode=str(payload.get("execution_mode") or ""),
                    )
                elif path == "/chat/queue":
                    result = queue_chat_codex_work_packet(
                        root,
                        lane_id=str(payload.get("lane_id") or ""),
                        objective=str(payload.get("objective") or ""),
                        confirmation=str(payload.get("confirmation") or ""),
                    )
                else:
                    result = pin_dual_chat_memory(
                        root,
                        lane_id=str(payload.get("lane_id") or ""),
                        text=str(payload.get("text") or ""),
                        source_turn_id=str(payload.get("source_turn_id") or "") or None,
                        confirmation=str(payload.get("confirmation") or WRITE_CONFIRMATION_TOKEN),
                    )
            except Exception as exc:
                result = {"ok": False, "finding": "request_failed", "error": exc.__class__.__name__}
            if self._wants_json():
                self._send_json(200 if result.get("ok") else 400, result)
                return
            self._redirect("/chat")

    return IonCockpitHandler


def run_server(root: str | Path = ".", *, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    shell_root = Path(root).expanduser().resolve()
    server = ThreadingHTTPServer((host, port), make_handler(shell_root))
    print(f"ION local cockpit listening on http://{host}:{port}", flush=True)
    server.serve_forever()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve the local-only ION cockpit app.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--health", action="store_true")
    parser.add_argument("--html", action="store_true")
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.serve:
        run_server(args.ion_root, host=args.host, port=args.port)
        return 0
    if args.html:
        print(build_cockpit_html(build_cockpit_view_model(args.ion_root)))
        return 0
    result = build_cockpit_health(args.ion_root)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json or args.health else result["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
