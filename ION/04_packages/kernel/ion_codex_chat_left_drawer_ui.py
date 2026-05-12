"""Left page-local drawer renderer for Codex Chat."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .ion_codex_chat_ui_common import e, state_pill


def render_left_drawer(drawer_model: Mapping[str, Any]) -> str:
    panels = [panel for panel in drawer_model.get("panels", []) if isinstance(panel, Mapping)] if isinstance(drawer_model.get("panels"), list) else []
    canonical_panels: list[Mapping[str, Any]] = [
        {
            "id": "joc",
            "title": "JOC Instruments",
            "summary": "Recovery surface controls. This drawer is for page-local tools, not global navigation.",
            "items": [
                {"label": "Shell zones", "value": "active"},
                {"label": "Monolith quarantine", "value": "on"},
                {"label": "Visual proof gate", "value": "required"},
            ],
        },
        {
            "id": "queue",
            "title": "Queue Instruments",
            "summary": "Controls and filters for packets, autoplay, output detector, approvals, and receipts.",
            "items": [
                {"label": "Autoplay", "value": "gated"},
                {"label": "Output stopped detector", "value": "required"},
                {"label": "Kill switch", "value": "required"},
            ],
        },
        {
            "id": "codex",
            "title": "Codex Instruments",
            "summary": "Capsule, Mini, skill activation, carrier runs, and model route controls.",
            "items": [
                {"label": "Capsule", "value": "minimum"},
                {"label": "Mini", "value": "lookup"},
                {"label": "Skill route", "value": "visible"},
            ],
        },
        {
            "id": "extension",
            "title": "Extension Instruments",
            "summary": "dAimon companion controls for DOM capture, anchors, drop zones, prompt queue, and page evidence.",
            "items": [
                {"label": "Inspector hover", "value": "page only"},
                {"label": "Anchor capture", "value": "planned"},
                {"label": "Drop calibration", "value": "planned"},
            ],
        },
        {
            "id": "docs",
            "title": "Docs Instruments",
            "summary": "Favorites, folder tree, thumbnail grid, zip progress, and drop target controls.",
            "items": [
                {"label": "Favorites", "value": "drawer"},
                {"label": "Folder tree", "value": "drawer"},
                {"label": "Zip/drop", "value": "timeline"},
            ],
        },
        {
            "id": "projects",
            "title": "Project Instruments",
            "summary": "ION context package roots, version sync, onboard state, and project receipts.",
            "items": [
                {"label": "Project versions", "value": "visible"},
                {"label": "Context package", "value": "required"},
                {"label": "Sync receipt", "value": "required"},
            ],
        },
        {
            "id": "wisdom",
            "title": "WisdomNET Instruments",
            "summary": "Knowledge route, source lineage, learning gates, and integration state.",
            "items": [
                {"label": "Lineage", "value": "visible"},
                {"label": "Learning", "value": "gated"},
                {"label": "Mutation", "value": "receipt"},
            ],
        },
        {
            "id": "gates",
            "title": "Gate Instruments",
            "summary": "Recovery, blocked authority, visual proof, service health, and operator approval surfaces.",
            "items": [
                {"label": "Production", "value": "false"},
                {"label": "Live browser", "value": "false"},
                {"label": "Accepted UI", "value": "false"},
            ],
        },
    ]
    existing_ids = {str(panel.get("id") or "") for panel in panels}
    panels = [panel for panel in canonical_panels if str(panel.get("id") or "") not in existing_ids] + panels
    active_id = str(drawer_model.get("active_panel_id") or (panels[0].get("id") if panels else "composer"))
    panel_html = []
    for panel in panels:
        panel_id = str(panel.get("id") or "")
        hidden = "" if panel_id == active_id else " hidden"
        items = panel.get("items") if isinstance(panel.get("items"), list) else []
        item_rows = "".join(
            f"<li><span>{e(item.get('label'))}</span>{state_pill(item.get('value'))}</li>"
            for item in items
            if isinstance(item, Mapping)
        ) or "<li><span>No page-local details.</span></li>"
        panel_html.append(
            f'<section class="left-drawer-panel" data-left-panel="{e(panel_id)}"{hidden}>'
            f'<div class="panel-header"><span>{e(panel.get("title") or panel_id)}</span></div>'
            f'<p>{e(panel.get("summary") or "")}</p>'
            f'<ul class="left-drawer-list">{item_rows}</ul>'
            "</section>"
        )
    if not panel_html:
        panel_html.append('<section class="left-drawer-panel"><p>No page-local drawers configured.</p></section>')
    return (
        '<aside class="capsule-left-drawer" aria-label="Page tools">'
        f'{"".join(panel_html)}'
        "</aside>"
    )
