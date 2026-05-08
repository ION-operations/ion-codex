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


def render_top_bar(top_bar: Mapping[str, Any], *, model_href: str, cockpit_href: str) -> str:
    page_tabs = []
    for tab in top_bar.get("page_tabs") or []:
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
        '<div class="capsule-top-spacer"></div>'
        f'{"".join(chips)}</header>'
    )


def render_left_rail(items: list[Mapping[str, Any]]) -> str:
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
    return (
        '<section class="capsule-main-work-surface" aria-label="Main work surface">'
        f'<div class="main-page is-active" data-page-panel="chat">{render_main_chat(conversation, composer, base_path=base_path, token_input=token_input)}</div>'
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
  {render_top_bar(top_bar, model_href=model_href, cockpit_href=cockpit_href)}
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
