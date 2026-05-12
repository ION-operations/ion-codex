"""Local-only ION cockpit web app.

This app renders the live cockpit projection for the operator. It is a
visibility surface only: no state writes, no shell bridge, no production or live
execution authority.
"""

from __future__ import annotations

import argparse
import html
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from .ion_cockpit_view_model import build_cockpit_view_model
from .ion_cockpit_service_manager import RESTART_CONFIRMATION, build_service_console_model, restart_service
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
JOC_REACT_DIST = Path("ION/08_ui/joc_cockpit_shell/dist")
LEGACY_CSP = "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'"
REACT_CSP = "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; frame-ancestors 'none'"


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


def react_cockpit_dist_root(root: str | Path = ".") -> Path:
    return Path(root).expanduser().resolve() / JOC_REACT_DIST


def build_react_cockpit_html(root: str | Path = ".") -> str | None:
    index_path = react_cockpit_dist_root(root) / "index.html"
    if not index_path.exists() or not index_path.is_file():
        return None
    return index_path.read_text(encoding="utf-8")


def resolve_react_static_asset(root: str | Path, request_path: str) -> Path | None:
    prefix = "/joc-static/"
    if not request_path.startswith(prefix):
        return None
    rel = unquote(request_path[len(prefix):]).lstrip("/")
    if not rel or "\x00" in rel:
        return None
    dist_root = react_cockpit_dist_root(root).resolve()
    target = (dist_root / rel).resolve()
    try:
        target.relative_to(dist_root)
    except ValueError:
        return None
    if not target.exists() or not target.is_file():
        return None
    return target


def build_cockpit_html(model: dict[str, Any]) -> str:
    runtime = model.get("runtime") if isinstance(model.get("runtime"), dict) else {}
    service_console = build_service_console_model(runtime.get("shell_root") or ".")
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
    service_console_cards = []
    for row in service_console.get("services", []):
        if not isinstance(row, dict):
            continue
        severity = _text(row.get("severity"), "watch")
        unit = _escape(row.get("unit"))
        service_console_cards.append(
            "<article class=\"service-console-card\">"
            f"<div><b>{_escape(row.get('label'))}</b><span class=\"pill {_status_class(severity)}\">{_escape(row.get('status'))}</span></div>"
            f"<p>{_escape(row.get('role'))}</p>"
            f"<small>{_escape(row.get('finding'))}</small>"
            "<form method=\"post\" action=\"/cockpit/services/restart\">"
            f"<input type=\"hidden\" name=\"unit\" value=\"{unit}\">"
            f"<input type=\"hidden\" name=\"confirmation\" value=\"{_escape(RESTART_CONFIRMATION)}\">"
            "<input type=\"hidden\" name=\"next\" value=\"/cockpit\">"
            f"<button type=\"submit\">{_escape(row.get('fix_label') or 'Restart')}</button>"
            "</form>"
            "</article>"
        )
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
.service-alert {{ border-color: rgba(225,95,95,0.45); background: linear-gradient(135deg, rgba(225,95,95,0.18), rgba(17,21,23,0.94)); }}
.service-alert.is-ready {{ border-color: rgba(87,199,133,0.35); background: linear-gradient(135deg, rgba(87,199,133,0.12), rgba(17,21,23,0.94)); }}
.service-console {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }}
.service-console-card {{ display: grid; gap: 8px; background: var(--panel-2); border: 1px solid var(--line); border-radius: 6px; padding: 10px; }}
.service-console-card div {{ display: flex; gap: 8px; align-items: center; justify-content: space-between; }}
.service-console-card p {{ margin: 0; color: var(--muted); font-size: 12px; line-height: 1.35; }}
.service-console-card form {{ margin: 0; }}
.service-console-card button {{ width: 100%; border: 1px solid rgba(255,255,255,0.18); border-radius: 5px; background: var(--blue); color: #041018; font-weight: 800; padding: 8px 10px; cursor: pointer; }}
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
    <article class="panel wide service-alert {'is-ready' if service_console.get('ok') else 'is-blocked'}">
      <h2>Console Alerts</h2>
      <h1>{_escape(service_console.get("headline"))}</h1>
      <div class="objective">{_escape(service_console.get("operator_message"))}</div>
      <div class="service-console">{''.join(service_console_cards)}</div>
    </article>
    <article class="panel wide">
      <h2>Helixion JOC Evolution</h2>
      <h1>{_escape((model.get("helixion_joc_rebuild") or {}).get("status", "not_documented"))}</h1>
      <div class="objective">{_escape((model.get("helixion_joc_rebuild") or {}).get("decision", "No Helixion rebuild plan loaded."))}</div>
      <div class="objective">Development URL: <a href="/joc/evolution">/joc/evolution</a> | <a href="/helixion/development">/helixion/development</a></div>
      {metric("Phase 1", "unlocked" if (model.get("helixion_joc_rebuild") or {}).get("ready_for_phase_1") else "blocked")}
      {metric("Plan", "present" if (model.get("helixion_joc_rebuild") or {}).get("master_plan_present") else "missing")}
      {metric("Registry", "present" if (model.get("helixion_joc_rebuild") or {}).get("registry_present") else "missing")}
      <pre>{_escape(json.dumps({
          "roles": (model.get("helixion_joc_rebuild") or {}).get("product_roles", {}),
          "surfaces": (model.get("helixion_joc_rebuild") or {}).get("required_surfaces", []),
          "next": (model.get("helixion_joc_rebuild") or {}).get("next_build_sequence", [])[:5],
          "forbidden_v1": (model.get("helixion_joc_rebuild") or {}).get("forbidden_v1_capabilities", []),
      }, indent=2, sort_keys=True))}</pre>
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
<style>
:root {{
  --dxl-bg: #050505;
  --dxl-bg-deep: #0a0a0a;
  --dxl-surface: #0e0e0e;
  --dxl-panel: #111111;
  --dxl-border: #1e1e1e;
  --dxl-border-hot: #444444;
  --dxl-text: #cccccc;
  --dxl-text-soft: #aaaaaa;
  --dxl-text-hint: #555555;
  --dxl-ok: #33cc66;
  --dxl-watch: #cc9900;
  --dxl-blocked: #cc3333;
  --dxl-font: "IBM Plex Mono", "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  background:
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px) 0 0 / 28px 28px,
    linear-gradient(0deg, rgba(255,255,255,0.018) 1px, transparent 1px) 0 0 / 28px 28px,
    var(--dxl-bg);
  color: var(--dxl-text);
  font-family: var(--dxl-font);
  letter-spacing: 0.04em;
}}
main {{
  min-height: 100vh;
  background: radial-gradient(circle at top right, rgba(255,255,255,0.055), transparent 32%), transparent;
}}
header, .topbar, .hero {{
  background: rgba(14,14,14,0.96) !important;
  border-bottom: 1px solid var(--dxl-border) !important;
  box-shadow: none !important;
}}
button, input, textarea, select {{
  font-family: var(--dxl-font);
}}
button {{
  border: 1px solid var(--dxl-border) !important;
  border-radius: 2px !important;
  background: #090909 !important;
  color: var(--dxl-text-soft) !important;
  font-size: 9px !important;
  font-weight: 700 !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
}}
button:hover {{
  border-color: var(--dxl-border-hot) !important;
  color: var(--dxl-text) !important;
}}
a {{
  color: var(--dxl-text) !important;
  text-decoration: none !important;
  border-bottom: 1px solid var(--dxl-border-hot) !important;
}}
a:hover {{
  color: var(--dxl-ok) !important;
}}
.panel {{
  border: 1px solid var(--dxl-border) !important;
  border-radius: 2px !important;
  background: linear-gradient(180deg, rgba(17,17,17,0.98), rgba(10,10,10,0.98)) !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.035) !important;
}}
.panel h2 {{
  margin: 0 0 8px !important;
  color: var(--dxl-text-hint) !important;
  font-size: 9px !important;
  font-weight: 700 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
}}
.panel h1 {{
  margin: 0 0 10px !important;
  color: var(--dxl-text) !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
}}
.objective, .path, td, th, pre, p {{
  color: var(--dxl-text-soft) !important;
  font-family: var(--dxl-font) !important;
  font-size: 9px !important;
  line-height: 1.45 !important;
}}
pre {{
  border: 1px solid var(--dxl-border) !important;
  border-radius: 2px !important;
  background: #070707 !important;
  padding: 8px !important;
}}
table {{
  border-collapse: collapse !important;
  width: 100% !important;
}}
th, td {{
  border-top: 1px solid var(--dxl-border) !important;
  padding: 6px 8px !important;
  text-align: left !important;
  vertical-align: top !important;
}}
th {{
  color: var(--dxl-text-hint) !important;
  font-size: 8px !important;
  text-transform: uppercase !important;
}}
.metric, .timeline article, .receipt-list article, .service-console article {{
  border: 1px solid var(--dxl-border) !important;
  border-radius: 2px !important;
  background: #090909 !important;
}}
.is-ready {{
  border-left: 2px solid var(--dxl-ok) !important;
}}
.is-warning {{
  border-left: 2px solid var(--dxl-watch) !important;
}}
.is-blocked {{
  border-left: 2px solid var(--dxl-blocked) !important;
}}
.rail {{
  border-left: 1px solid var(--dxl-border) !important;
  background: rgba(5,5,5,0.74) !important;
}}
</style>
</body>
</html>"""


def build_helixion_development_html(model: dict[str, Any]) -> str:
    rebuild = model.get("helixion_joc_rebuild") or {}
    roles = rebuild.get("product_roles") if isinstance(rebuild.get("product_roles"), dict) else {}
    surfaces = rebuild.get("required_surfaces") if isinstance(rebuild.get("required_surfaces"), list) else []
    phases = rebuild.get("next_build_sequence") if isinstance(rebuild.get("next_build_sequence"), list) else []
    allowed = rebuild.get("allowed_v1_capabilities") if isinstance(rebuild.get("allowed_v1_capabilities"), list) else []
    forbidden = rebuild.get("forbidden_v1_capabilities") if isinstance(rebuild.get("forbidden_v1_capabilities"), list) else []
    authorities = rebuild.get("source_authorities") if isinstance(rebuild.get("source_authorities"), list) else []

    def chips(values: list[Any]) -> str:
        return "".join(f"<span>{_escape(value)}</span>" for value in values) or "<span>none</span>"

    def role_rows() -> str:
        return "".join(
            f"<article><b>{_escape(name)}</b><p>{_escape(role)}</p></article>"
            for name, role in roles.items()
        ) or "<article><b>NO ROLES</b><p>No product role projection loaded.</p></article>"

    def phase_rows() -> str:
        return "".join(
            f"<article><b>{index:02d}</b><p>{_escape(phase)}</p></article>"
            for index, phase in enumerate(phases, start=1)
        ) or "<article><b>00</b><p>No build sequence loaded.</p></article>"

    ready = "UNLOCKED" if rebuild.get("ready_for_phase_1") else "BLOCKED"
    ready_class = "ok" if rebuild.get("ready_for_phase_1") else "blocked"
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Helixion JOC Development</title>
<style>
:root {{
  --bg: #050505;
  --surface: #0e0e0e;
  --panel: #111111;
  --border: #1e1e1e;
  --hot: #444444;
  --text: #cccccc;
  --soft: #aaaaaa;
  --hint: #555555;
  --ok: #33cc66;
  --watch: #cc9900;
  --blocked: #cc3333;
  --font: "IBM Plex Mono", "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  min-height: 100vh;
  background:
    linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px) 0 0 / 28px 28px,
    linear-gradient(0deg, rgba(255,255,255,0.018) 1px, transparent 1px) 0 0 / 28px 28px,
    radial-gradient(circle at 80% 0%, rgba(255,255,255,0.065), transparent 30%),
    var(--bg);
  color: var(--text);
  font-family: var(--font);
  letter-spacing: 0.045em;
}}
.shell {{
  display: grid;
  grid-template-rows: 42px 1fr 34px;
  min-height: 100vh;
}}
.top, .bottom {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1px solid var(--border);
  background: rgba(14,14,14,0.96);
  padding: 0 12px;
}}
.bottom {{
  border-top: 1px solid var(--border);
  border-bottom: 0;
  color: var(--hint);
  font-size: 8px;
  text-transform: uppercase;
}}
.brand {{
  color: var(--text);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.16em;
}}
.state {{
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--soft);
  font-size: 8px;
  font-weight: 700;
  text-transform: uppercase;
}}
.dot {{
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--ok);
  box-shadow: 0 0 12px rgba(51,204,102,0.45);
}}
.dot.blocked {{
  background: var(--blocked);
  box-shadow: 0 0 12px rgba(204,51,51,0.45);
}}
.grid {{
  display: grid;
  grid-template-columns: 52px minmax(0, 1fr) 360px;
  min-height: 0;
}}
.rail {{
  border-right: 1px solid var(--border);
  background: rgba(5,5,5,0.82);
  padding: 10px 6px;
}}
.rail span {{
  display: block;
  border: 1px solid var(--border);
  color: var(--hint);
  font-size: 8px;
  font-weight: 800;
  margin-bottom: 6px;
  padding: 7px 0;
  text-align: center;
}}
.main {{
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(0, 0.75fr);
  gap: 10px;
  padding: 10px;
  overflow: auto;
}}
.inspector {{
  border-left: 1px solid var(--border);
  padding: 10px;
  overflow: auto;
  background: rgba(5,5,5,0.62);
}}
.panel {{
  border: 1px solid var(--border);
  border-radius: 2px;
  background: linear-gradient(180deg, rgba(17,17,17,0.98), rgba(8,8,8,0.98));
  margin-bottom: 10px;
  padding: 10px;
}}
.panel h1, .panel h2, .panel h3 {{
  margin: 0;
  text-transform: uppercase;
}}
.panel h1 {{
  color: var(--text);
  font-size: 16px;
  line-height: 1.25;
  letter-spacing: 0.08em;
}}
.panel h2 {{
  color: var(--hint);
  font-size: 9px;
  letter-spacing: 0.16em;
  margin-bottom: 8px;
}}
.panel h3 {{
  color: var(--soft);
  font-size: 10px;
  letter-spacing: 0.12em;
  margin-bottom: 8px;
}}
p, code, pre {{
  color: var(--soft);
  font-family: var(--font);
  font-size: 9px;
  line-height: 1.5;
}}
pre {{
  border: 1px solid var(--border);
  background: #070707;
  overflow: auto;
  padding: 8px;
  white-space: pre-wrap;
}}
.verdict {{
  display: inline-block;
  border: 1px solid var(--hot);
  color: var(--ok);
  font-size: 9px;
  font-weight: 800;
  margin-bottom: 8px;
  padding: 5px 8px;
  text-transform: uppercase;
}}
.verdict.blocked {{
  color: var(--blocked);
}}
.cards {{
  display: grid;
  gap: 6px;
}}
.cards article {{
  border: 1px solid var(--border);
  background: #090909;
  padding: 8px;
}}
.cards b {{
  color: var(--text);
  display: block;
  font-size: 9px;
  margin-bottom: 4px;
  text-transform: uppercase;
}}
.chips {{
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}}
.chips span {{
  border: 1px solid var(--border);
  background: #090909;
  color: var(--soft);
  font-size: 8px;
  font-weight: 700;
  padding: 5px 6px;
  text-transform: uppercase;
}}
a {{
  color: var(--text);
  text-decoration: none;
  border-bottom: 1px solid var(--hot);
}}
a:hover {{ color: var(--ok); }}
</style>
</head>
<body>
<main class="shell">
  <header class="top">
    <div class="brand">HELIXION / JOC DEVELOPMENT</div>
    <div class="state"><span class="dot {ready_class}"></span><span>PHASE 1: {ready}</span><span>{_escape(rebuild.get("status", "not_documented"))}</span></div>
  </header>
  <section class="grid">
    <aside class="rail"><span>JOC</span><span>ION</span><span>dAI</span><span>CODEX</span><span>WNET</span></aside>
    <section class="main">
      <div>
        <article class="panel">
          <h2>MASTER REBUILD DECISION</h2>
          <div class="verdict {ready_class}">{_escape(rebuild.get("status", "not_documented"))}</div>
          <h1>{_escape(rebuild.get("decision", "No Helixion rebuild decision loaded."))}</h1>
          <p>This URL is a visibility cockpit for the Helixion/JOC rebuild. It does not grant new production, browser-control, credential, purchase, destructive, or silent-send authority.</p>
        </article>
        <article class="panel">
          <h2>PRODUCT ROLES</h2>
          <div class="cards">{role_rows()}</div>
        </article>
        <article class="panel">
          <h2>BUILD SEQUENCE</h2>
          <div class="cards">{phase_rows()}</div>
        </article>
      </div>
      <div>
        <article class="panel">
          <h2>REQUIRED SURFACES</h2>
          <div class="chips">{chips(surfaces)}</div>
        </article>
        <article class="panel">
          <h2>ALLOWED V1</h2>
          <div class="chips">{chips(allowed)}</div>
        </article>
        <article class="panel">
          <h2>FORBIDDEN V1</h2>
          <div class="chips">{chips(forbidden)}</div>
        </article>
      </div>
    </section>
    <aside class="inspector">
      <article class="panel">
        <h2>URLS</h2>
        <p><a href="/cockpit">/cockpit</a></p>
        <p><a href="/joc/evolution">/joc/evolution</a></p>
        <p><a href="/helixion/development">/helixion/development</a></p>
        <p><a href="/model.json">/model.json</a></p>
      </article>
      <article class="panel">
        <h2>SOURCE AUTHORITIES</h2>
        <pre>{_escape(json.dumps(authorities, indent=2, sort_keys=True))}</pre>
      </article>
      <article class="panel">
        <h2>PLAN PATHS</h2>
        <pre>{_escape(json.dumps({
            "master_plan": rebuild.get("master_plan_path"),
            "registry": rebuild.get("registry_path"),
            "current_plan": rebuild.get("current_plan_path"),
        }, indent=2, sort_keys=True))}</pre>
      </article>
    </aside>
  </section>
  <footer class="bottom"><span>LOCAL JOC VISIBILITY SURFACE</span><span>NO NEW RUNTIME AUTHORITY</span></footer>
</main>
</body>
</html>"""


def make_handler(root: Path) -> type[BaseHTTPRequestHandler]:
    class IonCockpitHandler(BaseHTTPRequestHandler):
        server_version = "IONLocalCockpit/0.1"

        def log_message(self, fmt: str, *args: Any) -> None:
            return

        def _send_bytes(self, status: int, body: bytes, content_type: str, *, csp: str | None = None) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", csp or LEGACY_CSP)
            self.end_headers()
            self.wfile.write(body)

        def _send_react_static(self, request_path: str) -> None:
            target = resolve_react_static_asset(root, request_path)
            if target is None:
                self._send_json(404, {"ok": False, "finding": "react_static_not_found", "path": request_path})
                return
            content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
            self._send_bytes(200, target.read_bytes(), content_type, csp=REACT_CSP)

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
            if path.startswith("/joc-static/"):
                self._send_react_static(path)
                return
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
            if path == "/cockpit/legacy":
                model = build_cockpit_view_model(root)
                self._send_bytes(200, build_cockpit_html(model).encode("utf-8"), "text/html; charset=utf-8")
                return
            if path in {"/", "/app", "/cockpit", "/joc/evolution", "/helixion/development", "/development"}:
                react_html = build_react_cockpit_html(root)
                if react_html:
                    self._send_bytes(200, react_html.encode("utf-8"), "text/html; charset=utf-8", csp=REACT_CSP)
                    return
                model = build_cockpit_view_model(root)
                self._send_bytes(200, build_cockpit_html(model).encode("utf-8"), "text/html; charset=utf-8")
                return
            self._send_json(404, {"ok": False, "finding": "not_found", "path": path})

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path in {"/services/restart", "/cockpit/services/restart"}:
                result = restart_service(root, self._read_payload())
                if self._wants_json():
                    self._send_json(200 if result.get("ok") else 409, result)
                    return
                self._redirect("/cockpit")
                return
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
