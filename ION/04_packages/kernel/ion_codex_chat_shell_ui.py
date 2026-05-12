"""Outer shell renderer for the Codex Chat cockpit."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .ion_codex_chat_assets_ui import CODEX_CHAT_APP_CSS, CODEX_CHAT_APP_JS
from .ion_codex_chat_left_drawer_ui import render_left_drawer
from .ion_codex_chat_main_ui import render_main_chat
from .ion_codex_chat_memory_visualization_ui import render_memory_visualization_body
from .ion_codex_chat_right_inspector_ui import render_inspector
from .ion_codex_chat_ui_common import e, icon


def render_top_bar(top_bar: Mapping[str, Any], *, model_href: str, cockpit_href: str, joc_href: str, docs_packages_href: str) -> str:
    canonical_tabs = [
        {"id": "chat", "label": "Chat"},
        {"id": "joc", "label": "JOC"},
        {"id": "queue", "label": "Queue"},
        {"id": "codex", "label": "Codex"},
        {"id": "extension", "label": "Extension"},
        {"id": "docs", "label": "Docs"},
        {"id": "projects", "label": "Projects"},
        {"id": "wisdom", "label": "WisdomNET"},
        {"id": "gates", "label": "Gates"},
        {"id": "receipts", "label": "Receipts"},
        {"id": "settings", "label": "Settings"},
    ]
    page_tabs = []
    for tab in canonical_tabs:
        if isinstance(tab, Mapping):
            active = " is-active" if tab.get("id") == "chat" else ""
            page_tabs.append(
                f'<button class="top-page-tab{active}" type="button" data-page-target="{e(tab.get("id"))}">{e(tab.get("label"))}</button>'
            )
    chips = []
    for chip in top_bar.get("status_chips") or []:
        if isinstance(chip, Mapping):
            chips.append(f'<span class="capsule-chip {e(chip.get("tone") or "watch")}">{e(chip.get("label"))}: {e(chip.get("value"))}</span>')
    return (
        '<header class="capsule-topbar">'
        f'<div class="capsule-brand">{e(top_bar.get("title") or "ION Codex")} <small>{e(top_bar.get("subtitle") or "Chat")}</small></div>'
        f'<nav class="top-page-tabs" aria-label="Pages">{"".join(page_tabs)}</nav>'
        f'<a class="capsule-chip" href="{model_href}">model</a>'
        f'<a class="capsule-chip" href="{e(cockpit_href)}">cockpit</a>'
        '<span class="capsule-chip watch">UI route: JOC canon</span>'
        '<div class="capsule-top-spacer"></div>'
        f'{"".join(chips)}</header>'
    )


def render_left_rail(items: list[Mapping[str, Any]]) -> str:
    canonical_items = [
        {"id": "joc", "label": "JOC", "icon": "joc"},
        {"id": "queue", "label": "Queue", "icon": "runs"},
        {"id": "codex", "label": "Codex", "icon": "chat"},
        {"id": "extension", "label": "Extension", "icon": "agents"},
        {"id": "docs", "label": "Docs", "icon": "context"},
        {"id": "projects", "label": "Projects", "icon": "receipts"},
        {"id": "wisdom", "label": "WisdomNET", "icon": "context"},
        {"id": "gates", "label": "Gates", "icon": "settings"},
    ]
    existing_ids = {str(item.get("id") or "") for item in items if isinstance(item, Mapping)}
    items = [item for item in canonical_items if str(item.get("id") or "") not in existing_ids] + items
    links = []
    for item in items:
        if not isinstance(item, Mapping):
            continue
        active = " is-active" if item.get("id") == "composer" else ""
        icon_name = str(item.get("icon") or item.get("id") or "chat")
        links.append(
            f'<button class="capsule-rail-button{active}" type="button" data-left-drawer-target="{e(item.get("id"))}" title="{e(item.get("label"))}" aria-label="{e(item.get("label"))}">{icon(icon_name)}</button>'
        )
    return f'<nav class="capsule-left-rail" aria-label="Codex app rail">{"".join(links)}</nav>'


def render_right_rail(items: list[Mapping[str, Any]]) -> str:
    buttons = []
    for item in items:
        if not isinstance(item, Mapping):
            continue
        active = " is-active" if item.get("id") == "assistant" else ""
        icon_name = str(item.get("icon") or item.get("id") or "chat")
        buttons.append(
            f'<button class="right-rail-button{active}" type="button" data-inspector-target="{e(item.get("id"))}" title="{e(item.get("label"))}" aria-label="{e(item.get("label"))}">{icon(icon_name)}</button>'
        )
    return f'<nav class="capsule-right-rail" aria-label="Universal tools">{"".join(buttons)}</nav>'


def render_bottom_timeline(timeline: Mapping[str, Any], fallback_activity: list[Mapping[str, Any]]) -> str:
    lanes = [lane for lane in timeline.get("lanes", []) if isinstance(lane, Mapping)] if isinstance(timeline.get("lanes"), list) else []
    items = [item for item in timeline.get("items", []) if isinstance(item, Mapping)] if isinstance(timeline.get("items"), list) else fallback_activity
    filters = "".join(
        f'<button class="timeline-filter{" is-active" if lane.get("id") == "all" else ""}" type="button" data-timeline-filter="{e(lane.get("id"))}">{e(lane.get("label"))} <b>{e(lane.get("count"))}</b></button>'
        for lane in lanes
    )
    rows = "".join(
        f'<article class="activity-item" data-timeline-kind="{e(item.get("kind"))}"><span>{e(item.get("kind"))} / {e(item.get("status"))}</span><b>{e(item.get("label"))}</b><p>{e(item.get("detail"))}</p></article>'
        for item in items
        if isinstance(item, Mapping)
    )
    if not rows:
        rows = '<article class="activity-item"><span>idle</span><b>No recent activity</b><p>Waiting for chat or Codex queue movement.</p></article>'
    return f'<footer class="capsule-activity-strip" aria-label="Runtime timeline"><div class="timeline-filter-row">{filters}</div><div class="activity-row">{rows}</div></footer>'


def _page_metric(label: str, value: Any) -> str:
    return f'<div class="drawer-kpi"><span>{e(label)}</span><b>{e(value)}</b></div>'


def _page_card(title: str, summary: str, rows: list[tuple[str, Any]] | None = None) -> str:
    row_html = ""
    if rows:
        row_html = "<ul class=\"left-drawer-list\">" + "".join(
            f"<li><span>{e(label)}</span><code>{e(value)}</code></li>"
            for label, value in rows
        ) + "</ul>"
    return (
        '<article class="skill-card">'
        f"<div><b>{e(title)}</b></div>"
        f"<p>{e(summary)}</p>"
        f"{row_html}</article>"
    )


def _focused_page(title: str, summary: str, metrics: list[tuple[str, Any]], cards: list[str], *, footer_note: str | None = None) -> str:
    return (
        '<div class="page-surface page-surface-shell">'
        '<div class="page-scroll-body">'
        f"<h2>{e(title)}</h2>"
        f"<p>{e(summary)}</p>"
        f'<div class="drawer-kpis">{"".join(_page_metric(label, value) for label, value in metrics)}</div>'
        f'<div class="skill-list">{"".join(cards)}</div>'
        "</div>"
        '<footer class="page-anchor-bar">'
        f"<span><b>{e(title)}</b> / {e(footer_note or 'page body scrolls above; actions, inspector, and timeline stay anchored')}</span>"
        '<span class="page-anchor-actions"><span>LEFT DRAWER: tools</span><span>RIGHT INSPECTOR: proof</span><span>BOTTOM: events</span></span>'
        "</footer>"
        "</div>"
    )


def render_main_work_surface(
    conversation: Mapping[str, Any],
    composer: Mapping[str, Any],
    pages: Mapping[str, Any],
    drawers: Mapping[str, Any],
    *,
    base_path: str,
    token_input: str,
) -> str:
    context = drawers.get("context") if isinstance(drawers.get("context"), Mapping) else {}
    runs = drawers.get("runs") if isinstance(drawers.get("runs"), Mapping) else {}
    agents = drawers.get("agents") if isinstance(drawers.get("agents"), Mapping) else {}
    receipts = drawers.get("receipts") if isinstance(drawers.get("receipts"), Mapping) else {}
    settings = drawers.get("settings") if isinstance(drawers.get("settings"), Mapping) else {}
    memory_visualization = context.get("memory_visualization") if isinstance(context.get("memory_visualization"), Mapping) else {}
    runner = runs.get("runner") if isinstance(runs.get("runner"), Mapping) else {}
    skills = drawers.get("skills") if isinstance(drawers.get("skills"), Mapping) else {}
    current_skill = skills.get("current_activation") if isinstance(skills.get("current_activation"), Mapping) else {}
    chat_engine = drawers.get("chat_engine") if isinstance(drawers.get("chat_engine"), Mapping) else {}
    assistant_work_routes = drawers.get("assistant_work_routes") if isinstance(drawers.get("assistant_work_routes"), Mapping) else {}
    carrier = drawers.get("carrier") if isinstance(drawers.get("carrier"), Mapping) else {}
    timeline = drawers.get("timeline") if isinstance(drawers.get("timeline"), Mapping) else {}
    joc_page = _focused_page(
        "JOC Recovery Cockpit",
        "This is the active 8765 JOC surface. Recovery rule: pages and drawers first; failed 8788 panel inventory remains candidate-only until remapped into this shell.",
        [
            ("route", "ui-frontend-excellence"),
            ("status", "recovery"),
            ("accepted UI", False),
        ],
        [
            _page_card("Canon shell", "The active layout is top bar, left rail, left drawer, one main page, right inspector, right rail, and bottom timeline.", [("source", "UI_FRONTEND_EXCELLENCE_DOMAIN_PROTOCOL_V0_1.md")]),
            _page_card("Quarantine", "C-078 through C-085 are candidate inventory only, not accepted product UI.", [("receipt", "HELIXION_JOC_UI_ROUTE_RECOVERY_RECEIPT_20260511.json")]),
            _page_card("Next build law", "New panels cannot be added as a wall. Each surface must become a top page, left drawer tab, right inspector lens, or timeline event.", [("gate", "JOC_UI_CANON_STEWARD")]),
        ],
    )
    queue_page = _focused_page(
        "Queue Carrier",
        "Browser/GPT Actions queue state belongs here as one focused page. Details, approvals, and receipts stay in the right inspector and timeline.",
        [
            ("queued", runner.get("queued_request_count", 0)),
            ("active", runner.get("active_process_running", False)),
            ("returns", (runs.get("return_hydration") or {}).get("record_count") if isinstance(runs.get("return_hydration"), Mapping) else 0),
        ],
        [
            _page_card("Carrier rule", "Autoplay and packet execution require visible state, pause/kill controls, receipts, and no silent sensitive send.", [("authority", "bounded only")]),
            _page_card("Output detector", "Future browser-carrier work should expose waiting, active output, send availability, and blocked state as timeline events.", [("lane", "queue")]),
        ],
    )
    codex_page = _focused_page(
        "Codex / Capsule",
        "Codex chat context, skills, carrier runs, Capsule, Mini, and model route are visible through inspector lenses instead of scattered panels.",
        [
            ("lenses", chat_engine.get("lens_count", 0)),
            ("skills", skills.get("skill_count", 0)),
            ("current", current_skill.get("display_name") or "none"),
        ],
        [
            _page_card("Active skill", "Skill activation must select the correct workflow before implementation. UI work now routes to UI Frontend Excellence.", [("skill", current_skill.get("skill_id") or "none")]),
            _page_card("Carrier", "Respond-only chat and bounded work packets remain separated; no unrestricted local execution is granted.", [("enabled", carrier.get("enabled", False))]),
        ],
    )
    extension_page = _focused_page(
        "dAimon Extension",
        "The portable page companion needs its own page for DOM perception, element capture, anchors, drop zones, docs/packages drag/drop, and prompt queue visibility.",
        [
            ("dom", "planned"),
            ("drop zones", "planned"),
            ("silent control", False),
        ],
        [
            _page_card("DOM capture", "Element capture must show selected DOM evidence, geometry, anchor points, and user approval before persistent calibration.", [("surface", "right inspector")]),
            _page_card("Docs/package drop", "Folder zip/drop behavior belongs behind explicit progress, target, receipt, and cancel state.", [("lane", "bottom timeline")]),
        ],
    )
    docs_page = _focused_page(
        "Docs / Packages",
        "Docs, favorites, package thumbnails, folder trees, and context packages are a real page, not an external prototype link.",
        [
            ("context packages", "mounted"),
            ("zip/drop", "gated"),
            ("favorites", "drawer"),
        ],
        [
            _page_card("Favorites grid", "ION, dAimon, WisdomNET, project roots, and selected folders should render as page thumbnails with one-click and double-click actions.", [("drawer", "Favorites")]),
            _page_card("Tree selector", "Computer folder search/tree belongs in the left drawer; selected item detail and proof belongs in the right inspector.", [("drawer", "Folder Tree")]),
        ],
    )
    projects_page = _focused_page(
        "Projects",
        "ION assembled project context packages and latest version state belong here, with sync/receipt proof visible.",
        [
            ("package route", "context"),
            ("versions", "latest"),
            ("acceptance", "receipt required"),
        ],
        [
            _page_card("Project cards", "Each project card should show latest context package, version, health, and action buttons without becoming a general file browser.", [("source", "context package folder")]),
            _page_card("Sync gate", "Onboard/rescan state must show project name, version, and whether Codex/ION context is current.", [("gate", "context proof")]),
        ],
    )
    wisdom_page = _focused_page(
        "WisdomNET",
        "WisdomNET remains a dedicated work surface for knowledge graph, learning routes, lineage, and integration state.",
        [
            ("state", "planned"),
            ("lineage", "visible"),
            ("mutation", "gated"),
        ],
        [
            _page_card("Knowledge route", "Show what context, source, and lineage is selected for AI use without exposing hidden reasoning.", [("lens", "context")]),
            _page_card("Learning gate", "Any durable learning or integration must carry source proof and acceptance receipt.", [("gate", "receipt")]),
        ],
    )
    gates_page = _focused_page(
        "Gates / Recovery",
        "This page holds authority, visual proof, service health, blocked capabilities, and recovery state so issues are visible to both operator and AI chat.",
        [
            ("production", False),
            ("live browser", False),
            ("visual proof", "required"),
        ],
        [
            _page_card("UI gate", "No accepted UI state without JOC canon settlement and visual proof.", [("route", "VISUAL_PROOF_AUDITOR")]),
            _page_card("Route health", "Future JOC UI work must activate ui-frontend-excellence before implementation.", [("skill", "ui-frontend-excellence")]),
            _page_card("Timeline", "Async work, receipts, errors, and blocked actions must appear as bottom timeline events.", [("events", timeline.get("trace_count", 0))]),
        ],
    )
    return (
        '<section class="capsule-main-work-surface" aria-label="Main work surface">'
        f'<div class="main-page is-active" data-page-panel="chat">{render_main_chat(conversation, composer, base_path=base_path, token_input=token_input)}</div>'
        f'<div class="main-page" data-page-panel="joc" hidden>{joc_page}</div>'
        f'<div class="main-page" data-page-panel="queue" hidden>{queue_page}</div>'
        f'<div class="main-page" data-page-panel="codex" hidden>{codex_page}</div>'
        f'<div class="main-page" data-page-panel="extension" hidden>{extension_page}</div>'
        f'<div class="main-page" data-page-panel="docs" hidden>{docs_page}</div>'
        f'<div class="main-page" data-page-panel="projects" hidden>{projects_page}</div>'
        f'<div class="main-page" data-page-panel="wisdom" hidden>{wisdom_page}</div>'
        f'<div class="main-page" data-page-panel="gates" hidden>{gates_page}</div>'
        f'<div class="main-page" data-page-panel="context" hidden><div class="page-surface"><h2>{e((pages.get("context") or {}).get("title") if isinstance(pages.get("context"), Mapping) else "Context")}</h2><p>{e((pages.get("context") or {}).get("summary") if isinstance(pages.get("context"), Mapping) else "")}</p>{render_memory_visualization_body(memory_visualization)}</div></div>'
        f'<div class="main-page" data-page-panel="runs" hidden><div class="page-surface"><h2>Runs</h2><p>{e((pages.get("runs") or {}).get("summary") if isinstance(pages.get("runs"), Mapping) else "")}</p><div class="drawer-kpis"><div class="drawer-kpi"><span>Queued</span><b>{e(runner.get("queued_request_count", 0))}</b></div><div class="drawer-kpi"><span>Active</span><b>{e(runner.get("active_process_running", False))}</b></div><div class="drawer-kpi"><span>Returns</span><b>{e((runs.get("return_hydration") or {}).get("record_count") if isinstance(runs.get("return_hydration"), Mapping) else 0)}</b></div></div></div></div>'
        f'<div class="main-page" data-page-panel="agents" hidden><div class="page-surface"><h2>Agents</h2><p>{e((pages.get("agents") or {}).get("summary") if isinstance(pages.get("agents"), Mapping) else "")}</p><div class="drawer-kpis"><div class="drawer-kpi"><span>Available</span><b>{e(agents.get("agent_count", 0))}</b></div><div class="drawer-kpi"><span>Invocations</span><b>{e(agents.get("invocation_count", 0))}</b></div><div class="drawer-kpi"><span>Second system</span><b>{e(agents.get("creates_second_agent_system", False))}</b></div></div></div></div>'
        f'<div class="main-page" data-page-panel="receipts" hidden><div class="page-surface"><h2>Receipts</h2><p>{e((pages.get("receipts") or {}).get("summary") if isinstance(pages.get("receipts"), Mapping) else "")}</p><p>History: <code>{e(receipts.get("history_path"))}</code></p></div></div>'
        f'<div class="main-page" data-page-panel="settings" hidden><div class="page-surface"><h2>Settings</h2><p>{e((pages.get("settings") or {}).get("summary") if isinstance(pages.get("settings"), Mapping) else "")}</p><p>Memory: <code>{e(settings.get("memory_path"))}</code></p></div></div>'
        "</section>"
    )


def render_codex_chat_shell_html(model: Mapping[str, Any], *, base_path: str = "/chat", auth_token: str | None = None) -> str:
    ui = model.get("ui") if isinstance(model.get("ui"), Mapping) else {}
    top_bar = ui.get("top_bar") if isinstance(ui.get("top_bar"), Mapping) else {}
    composer = ui.get("composer") if isinstance(ui.get("composer"), Mapping) else {}
    conversation = ui.get("conversation") if isinstance(ui.get("conversation"), Mapping) else {}
    drawers = ui.get("drawers") if isinstance(ui.get("drawers"), Mapping) else {}
    left_rail = ui.get("left_rail") if isinstance(ui.get("left_rail"), list) else []
    left_drawer = ui.get("left_drawer") if isinstance(ui.get("left_drawer"), Mapping) else {}
    right_rail = ui.get("right_rail") if isinstance(ui.get("right_rail"), list) else []
    activity = ui.get("activity") if isinstance(ui.get("activity"), list) else []
    pages = ui.get("pages") if isinstance(ui.get("pages"), Mapping) else {}
    bottom_timeline = ui.get("bottom_timeline") if isinstance(ui.get("bottom_timeline"), Mapping) else {}
    token_input = f'<input type="hidden" name="public_token" value="{e(auth_token)}">' if auth_token else ""
    suffix = f"?token={e(auth_token)}" if auth_token else ""
    model_href = f"{e(base_path)}/model.json{suffix}"
    cockpit_href = f"/cockpit{suffix}"
    joc_href = "http://127.0.0.1:8788/helixion/development"
    docs_packages_href = "http://127.0.0.1:8788/helixion/development#docs-packages"

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>ION Codex Chat</title>
<style>{CODEX_CHAT_APP_CSS}</style>
</head>
<body>
<main class="capsule-app codex-chat-app" data-ui="ion-codex-chat-app" data-schema="{e(ui.get("schema_id"))}">
  {render_top_bar(top_bar, model_href=model_href, cockpit_href=cockpit_href, joc_href=joc_href, docs_packages_href=docs_packages_href)}
  {render_left_rail(left_rail)}
  {render_left_drawer(left_drawer)}
  {render_main_work_surface(conversation, composer, pages, drawers, base_path=base_path, token_input=token_input)}
  {render_inspector(drawers)}
  {render_right_rail(right_rail)}
  {render_bottom_timeline(bottom_timeline, activity)}
</main>
<script>{CODEX_CHAT_APP_JS}</script>
</body>
</html>"""
