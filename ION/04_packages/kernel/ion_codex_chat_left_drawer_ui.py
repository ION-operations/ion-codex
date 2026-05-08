"""Left page-local drawer renderer for Codex Chat."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .ion_codex_chat_ui_common import e, state_pill


def render_left_drawer(drawer_model: Mapping[str, Any]) -> str:
    panels = [panel for panel in drawer_model.get("panels", []) if isinstance(panel, Mapping)] if isinstance(drawer_model.get("panels"), list) else []
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
