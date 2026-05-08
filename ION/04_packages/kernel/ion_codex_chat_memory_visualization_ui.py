"""Renderer for the Codex Chat smart memory visualization projection."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from typing import Any

from .ion_codex_chat_ui_common import e, short, state_pill


WINDOW_LABELS = {
    "LIVE_INPUT": "Live Input",
    "ACTIVE_CRUCIBLE": "Active Crucible",
    "ACTIVE_CONTEXT": "Active Context",
    "HOT_CONTEXT": "Hot Context",
    "X_RAY_DAG": "X-Ray DAG",
    "MINI_LOOKUP": "Mini Lookup",
    "LONG_HORIZON": "Long Horizon",
    "COLD_EVIDENCE": "Cold Evidence",
    "OMITTED_OR_BLOCKED": "Omitted / Blocked",
}


def _items(value: Any) -> list[Mapping[str, Any]]:
    return [item for item in value if isinstance(item, Mapping)] if isinstance(value, list) else []


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _segment_index(segments: list[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(segment.get("segment_id")): segment for segment in segments if segment.get("segment_id")}


def _tag_list(values: Any) -> str:
    tags = [str(value) for value in values if value] if isinstance(values, list) else []
    if not tags:
        return '<span class="memory-tag muted">untagged</span>'
    return "".join(f'<span class="memory-tag">{e(tag)}</span>' for tag in tags[:5])


SOURCE_GROUP_LABELS = {
    "protocol": "Protocol",
    "kernel": "Kernel",
    "tests": "Tests",
    "capsule": "Capsule",
    "active_state": "Active State",
    "runtime": "Runtime",
    "omitted": "Omitted",
    "external": "External",
    "other": "Other",
}


def _source_group(ref: Any, *, kind: str = "source_ref") -> str:
    ref_text = str(ref or "")
    if kind in {"omitted_ref", "blocked_route"}:
        return "omitted"
    if ref_text.startswith(("ION/REPO_AUTHORITY.md", "ION/02_architecture/", "ION/03_registry/", "ION/docs/setup/")):
        return "protocol"
    if ref_text.startswith("ION/04_packages/"):
        return "kernel"
    if ref_text.startswith("ION/tests/"):
        return "tests"
    if ref_text.startswith(("ION/05_context/current/codex_solo/", "ION/05_context/current/codex_cli/")):
        return "capsule"
    if ref_text.startswith("ION/05_context/current/"):
        return "active_state"
    if "runtime" in ref_text or "service" in ref_text:
        return "runtime"
    if "://" in ref_text:
        return "external"
    return "other"


def _source_ref_button(ref: Any, *, kind: str = "source_ref", label: str | None = None, summary: Any = None) -> str:
    ref_text = str(ref or "")
    if not ref_text:
        return ""
    button_label = label or ref_text
    preview = str(summary or ref_text)
    group = _source_group(ref_text, kind=kind)
    return (
        f'<button class="source-ref-button" type="button" '
        f'data-source-ref="{e(ref_text)}" '
        f'data-source-kind="{e(kind)}" '
        f'data-source-group="{e(group)}" '
        f'data-source-preview="{e(preview)}" '
        f'title="{e(ref_text)}">'
        f'<code>{e(button_label)}</code>'
        '</button>'
    )


def _segment_card(segment: Mapping[str, Any], *, compact: bool = False) -> str:
    window_class = str(segment.get("window_class") or "UNKNOWN")
    preview = short(segment.get("text_preview"), limit=180 if compact else 320)
    refs = list(segment.get("receipt_refs") if isinstance(segment.get("receipt_refs"), list) else [])
    refs.extend(list(segment.get("route_refs") if isinstance(segment.get("route_refs"), list) else []))
    ref_line = ", ".join(str(ref) for ref in refs[:3])
    ref_html = f'<p class="memory-ref-line">{e(ref_line)}</p>' if ref_line and not compact else ""
    segment_id = str(segment.get("segment_id") or "")
    return (
        f'<article class="memory-segment-card memory-{e(window_class.lower())}" role="button" tabindex="0" '
        f'aria-label="Inspect memory segment {e(segment_id)}" '
        f'data-memory-segment-id="{e(segment_id)}" '
        f'data-memory-window="{e(window_class)}" '
        f'data-memory-turn-id="{e(segment.get("turn_id"))}" '
        f'data-memory-kind="{e(segment.get("source_kind"))}" '
        f'data-memory-prompt-state="{e(segment.get("prompt_inclusion_state"))}" '
        f'data-memory-lifecycle="{e(segment.get("lifecycle_class"))}" '
        f'data-memory-compaction="{e(segment.get("compaction_state"))}" '
        f'data-memory-token-estimate="{e(segment.get("token_estimate") or 0)}" '
        f'data-memory-confidence="{e(segment.get("confidence"))}" '
        f'data-memory-preview="{e(preview)}" '
        f'data-memory-refs="{e(ref_line)}">'
        '<div class="memory-segment-head">'
        f'<b>{e(segment.get("source_kind") or segment.get("segment_id"))}</b>'
        f'{state_pill(segment.get("prompt_inclusion_state"))}'
        '</div>'
        f'<p>{e(preview)}</p>'
        '<div class="memory-tag-row">'
        f'{_tag_list(segment.get("selection_signals"))}'
        f'<span class="memory-tag tone">{e(segment.get("compaction_state"))}</span>'
        f'<span class="memory-tag tone">{e(segment.get("lifecycle_class"))}</span>'
        '</div>'
        '<div class="memory-meta-row">'
        f'<code>{e(segment.get("segment_id"))}</code>'
        f'<span>{e(segment.get("token_estimate") or 0)} tok</span>'
        f'<span>{e(segment.get("confidence"))}</span>'
        '</div>'
        f"{ref_html}"
        "</article>"
    )


def _selection_panel(selected_segment: Mapping[str, Any] | None) -> str:
    segment = selected_segment or {}
    segment_id = str(segment.get("segment_id") or "none")
    refs = list(segment.get("receipt_refs") if isinstance(segment.get("receipt_refs"), list) else [])
    refs.extend(list(segment.get("route_refs") if isinstance(segment.get("route_refs"), list) else []))
    ref_line = ", ".join(str(ref) for ref in refs[:4])
    return (
        '<section class="memory-panel memory-selection-panel" data-memory-selection-panel>'
        '<div class="memory-panel-title"><h3>Selected Context Node</h3><span>click a turn, segment, or route edge</span></div>'
        '<div class="memory-selection-grid">'
        f'<p><span>ID</span><code data-memory-selection-field="id">{e(segment_id)}</code></p>'
        f'<p><span>Turn</span><code data-memory-selection-field="turn">{e(segment.get("turn_id") or "none")}</code></p>'
        f'<p><span>Window</span><code data-memory-selection-field="window">{e(segment.get("window_class") or "none")}</code></p>'
        f'<p><span>Kind</span><code data-memory-selection-field="kind">{e(segment.get("source_kind") or "none")}</code></p>'
        f'<p><span>Prompt State</span><code data-memory-selection-field="prompt">{e(segment.get("prompt_inclusion_state") or "none")}</code></p>'
        f'<p><span>Lifecycle</span><code data-memory-selection-field="lifecycle">{e(segment.get("lifecycle_class") or "none")}</code></p>'
        f'<p><span>Compaction</span><code data-memory-selection-field="compaction">{e(segment.get("compaction_state") or "none")}</code></p>'
        f'<p><span>Tokens</span><code data-memory-selection-field="tokens">{e(segment.get("token_estimate") or 0)}</code></p>'
        f'<p><span>Confidence</span><code data-memory-selection-field="confidence">{e(segment.get("confidence") or "none")}</code></p>'
        '</div>'
        f'<p class="memory-selection-preview" data-memory-selection-field="preview">{e(short(segment.get("text_preview"), limit=420) if segment else "No context node selected.")}</p>'
        f'<p class="memory-ref-line" data-memory-selection-field="refs">{e(ref_line)}</p>'
        '<p class="memory-ref-line">Route edge: <code data-memory-selection-field="edge">none</code></p>'
        '</section>'
    )


def _budget_strip(
    *,
    manifest: Mapping[str, Any],
    token_budget: Mapping[str, Any],
    visualization: Mapping[str, Any],
) -> str:
    return (
        '<section class="memory-panel memory-budget-panel">'
        '<div class="memory-panel-title"><h3>Context Budget</h3><span>estimated, not provider-authoritative</span></div>'
        '<div class="memory-budget-strip" aria-label="Context budget">'
        '<div class="drawer-kpi"><span>Segments</span>'
        f'<b>{e(token_budget.get("segment_count") or len(visualization.get("memory_segments") or []))}</b></div>'
        '<div class="drawer-kpi"><span>Edges</span>'
        f'<b>{e(token_budget.get("edge_count") or len(visualization.get("context_route_edges") or []))}</b></div>'
        '<div class="drawer-kpi"><span>Tokens</span>'
        f'<b>{e(token_budget.get("estimated_total_tokens") or 0)}</b></div>'
        '<div class="drawer-kpi"><span>Mode</span>'
        f'<b>{e(manifest.get("c1_c2_c3_mode") or "unknown")}</b></div>'
        '<div class="drawer-kpi"><span>Gate</span>'
        f'<b>{e(manifest.get("selected_gate") or "context_proof_required")}</b></div>'
        '<div class="drawer-kpi"><span>Hidden Reasoning</span><b>false</b></div>'
        "</div></section>"
    )


def _selected_turn_panel(
    *,
    selected: Mapping[str, Any],
    segments_by_id: dict[str, Mapping[str, Any]],
) -> str:
    active_ids = [str(value) for value in selected.get("active_prompt_segment_ids", []) if value] if isinstance(selected.get("active_prompt_segment_ids"), list) else []
    related_ids = [str(value) for value in selected.get("directly_related_segment_ids", []) if value] if isinstance(selected.get("directly_related_segment_ids"), list) else []
    lookup_ids = [str(value) for value in selected.get("lookup_available_segment_ids", []) if value] if isinstance(selected.get("lookup_available_segment_ids"), list) else []
    omitted_ids = [str(value) for value in selected.get("omitted_or_blocked_segment_ids", []) if value] if isinstance(selected.get("omitted_or_blocked_segment_ids"), list) else []

    def rows(ids: list[str]) -> str:
        rendered = []
        for segment_id in ids[:7]:
            segment = segments_by_id.get(segment_id)
            if segment:
                rendered.append(_segment_card(segment, compact=True))
            else:
                rendered.append(f'<code>{e(segment_id)}</code>')
        return "".join(rendered) or '<p class="empty-note">No segments in this set.</p>'

    return (
        '<section class="memory-panel selected-turn-context">'
        '<div class="memory-panel-title"><h3>Selected Turn Context</h3>'
        f'<code>{e(selected.get("selected_turn_id") or "none")}</code></div>'
        '<div class="memory-lane-grid compact">'
        f'<div><h4>Prompt Visible</h4>{rows(active_ids)}</div>'
        f'<div><h4>Directly Retrieved</h4>{rows(related_ids)}</div>'
        f'<div><h4>Lookup / Route Available</h4>{rows(lookup_ids)}</div>'
        f'<div><h4>Omitted / Blocked</h4>{rows(omitted_ids)}</div>'
        '</div>'
        f'<p class="memory-policy-note">{e(selected.get("policy") or "Raw hidden reasoning is not exposed.")}</p>'
        '</section>'
    )


def _strata_panel(
    *,
    windows: list[Mapping[str, Any]],
    segments: list[Mapping[str, Any]],
) -> str:
    segments_by_class: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for segment in segments:
        segments_by_class[str(segment.get("window_class") or "UNKNOWN")].append(segment)
    rows = []
    for item in windows:
        window_class = str(item.get("window_class") or "UNKNOWN")
        cards = "".join(_segment_card(segment, compact=True) for segment in segments_by_class.get(window_class, [])[:4])
        rows.append(
            f'<section class="memory-window memory-{e(window_class.lower())}" data-memory-window-class="{e(window_class)}">'
            '<div class="memory-window-head">'
            f'<b>{e(WINDOW_LABELS.get(window_class, window_class))}</b>'
            f'<span>{e(item.get("segment_count"))} segments / {e(item.get("token_estimate"))} tok</span>'
            '</div>'
            f'{cards or "<p class=\"empty-note\">No visible segments.</p>"}'
            '</section>'
        )
    if not rows:
        rows.append('<section class="memory-window"><div class="memory-window-head"><b>No Memory Windows</b><span>0</span></div></section>')
    return (
        '<section class="memory-panel">'
        '<div class="memory-panel-title"><h3>Memory Strata</h3><span>Memory Windows / backend window classes</span></div>'
        f'<div class="memory-window-grid">{"".join(rows)}</div>'
        '</section>'
    )


def _matryoshka_panel(
    *,
    layers: list[Mapping[str, Any]],
    segments_by_id: dict[str, Mapping[str, Any]],
) -> str:
    cards = []
    for layer in layers:
        segment_ids = [str(value) for value in layer.get("segment_ids", []) if value] if isinstance(layer.get("segment_ids"), list) else []
        preview_cards = "".join(
            _segment_card(segments_by_id[segment_id], compact=True)
            for segment_id in segment_ids[:3]
            if segment_id in segments_by_id
        )
        cards.append(
            f'<article class="matryoshka-layer" data-matryoshka-layer="{e(layer.get("layer_id"))}">'
            '<div class="memory-segment-head">'
            f'<b>{e(layer.get("label"))}</b>'
            f'<span>{e(layer.get("segment_count") or 0)} segments / {e(layer.get("token_estimate") or 0)} tok</span>'
            '</div>'
            f'<p>{e(layer.get("summary"))}</p>'
            f'<div class="memory-tag-row">{_tag_list(layer.get("window_classes"))}</div>'
            f'{preview_cards}'
            '</article>'
        )
    return (
        '<section class="memory-panel">'
        '<div class="memory-panel-title"><h3>Contextual Matryoshka</h3><span>rolling context layers</span></div>'
        f'<div class="matryoshka-grid">{"".join(cards)}</div>'
        '</section>'
    )


def _route_graph_panel(
    *,
    edges: list[Mapping[str, Any]],
    segments_by_id: dict[str, Mapping[str, Any]],
) -> str:
    edge_counts: dict[str, int] = {}
    for edge in edges:
        edge_type = str(edge.get("edge_type") or "unknown")
        edge_counts[edge_type] = edge_counts.get(edge_type, 0) + 1
    filter_buttons = [
        f'<button class="route-edge-filter is-active" type="button" data-route-edge-filter="all">All <b>{e(len(edges))}</b></button>'
    ]
    for edge_type, count in sorted(edge_counts.items()):
        filter_buttons.append(
            f'<button class="route-edge-filter" type="button" data-route-edge-filter="{e(edge_type)}">{e(edge_type)} <b>{e(count)}</b></button>'
        )
    summary_cards = "".join(
        '<article class="route-summary-card">'
        f'<span>{e(edge_type)}</span>'
        f'<b>{e(count)}</b>'
        '</article>'
        for edge_type, count in sorted(edge_counts.items())
    )
    rows = []
    for edge in edges[:18]:
        source = segments_by_id.get(str(edge.get("from_segment_id")))
        target = segments_by_id.get(str(edge.get("to_segment_id")))
        rows.append(
            f'<li class="route-edge-row" role="button" tabindex="0" '
            f'aria-label="Inspect route edge {e(edge.get("edge_id"))}" '
            f'data-route-edge-id="{e(edge.get("edge_id"))}" '
            f'data-route-from="{e(edge.get("from_segment_id"))}" '
            f'data-route-to="{e(edge.get("to_segment_id"))}" '
            f'data-route-type="{e(edge.get("edge_type"))}" '
            f'data-route-edge-type="{e(edge.get("edge_type"))}">'
            '<div>'
            f'<b>{e(edge.get("edge_type"))}</b>'
            f'<span>{e(edge.get("source_system"))}</span>'
            '</div>'
            f'<code>{e(edge.get("from_segment_id"))}</code>'
            '<span class="route-arrow">-></span>'
            f'<code>{e(edge.get("to_segment_id"))}</code>'
            f'<p>{e((source or {}).get("source_kind"))} to {e((target or {}).get("source_kind"))} · {e(edge.get("display_style"))} · confidence {e(edge.get("confidence"))}</p>'
            '</li>'
        )
    return (
        '<section class="memory-panel">'
        '<div class="memory-panel-title"><h3>Context Route Graph</h3><span>retrieval and compaction edges</span></div>'
        f'<div class="route-summary-grid">{summary_cards or "<article class=\"route-summary-card\"><span>none</span><b>0</b></article>"}</div>'
        f'<div class="route-edge-filter-row">{"".join(filter_buttons)}</div>'
        f'<ol class="route-edge-list">{"".join(rows) or "<li class=\"route-edge-row\"><b>No route edges</b></li>"}</ol>'
        '</section>'
    )


def _compaction_panel(events: list[Mapping[str, Any]]) -> str:
    rows = []
    for event in events[:12]:
        rows.append(
            '<li class="compaction-event">'
            f'<b>{e(event.get("event_type"))}</b>'
            f'{state_pill(event.get("target_window_class"))}'
            f'<p>{e(event.get("summary") or "")}</p>'
            f'<code>{e(event.get("source_path"))}</code>'
            f'<span>{e(event.get("epoch_id") or "")} {e(event.get("row_start") or "")} {e(event.get("row_end") or "")}</span>'
            '</li>'
        )
    return (
        '<section class="memory-panel">'
        '<div class="memory-panel-title"><h3>Compaction Timeline</h3><span>Capsule to Mini to long horizon</span></div>'
        f'<ol class="compaction-list">{"".join(rows) or "<li class=\"compaction-event\"><b>No compaction events</b></li>"}</ol>'
        '</section>'
    )


def _manifest_panel(manifest: Mapping[str, Any], omitted_refs: list[Mapping[str, Any]], source_refs: list[Any]) -> str:
    next_refs = [str(ref) for ref in manifest.get("next_files_or_sources", []) if ref] if isinstance(manifest.get("next_files_or_sources"), list) else []
    blocked = [str(ref) for ref in manifest.get("blocked_routes", []) if ref] if isinstance(manifest.get("blocked_routes"), list) else []
    omitted_rows = "".join(
        '<li>'
        f'{_source_ref_button(item.get("ref"), kind="omitted_ref", summary=item.get("reason"))}'
        f'{state_pill(item.get("authority_state"))}'
        f'<span>{e(item.get("reason"))}</span>'
        '</li>'
        for item in omitted_refs[:8]
    )
    source_rows = "".join(f'<li>{_source_ref_button(ref)}</li>' for ref in source_refs[:10])
    next_rows = "".join(f'<li>{_source_ref_button(ref, kind="next_source")}</li>' for ref in next_refs[:10])
    blocked_rows = "".join(f'<li>{_source_ref_button(ref, kind="blocked_route")}</li>' for ref in blocked[:8])
    return (
        '<section class="memory-panel">'
        '<div class="memory-panel-title"><h3>Protocol Manifest</h3><span>safe route metadata</span></div>'
        '<div class="memory-manifest-grid">'
        f'<p>Branch <code>{e(manifest.get("current_branch_id") or "model_refresh")}</code></p>'
        f'<p>Mode <code>{e(manifest.get("c1_c2_c3_mode") or "unknown")}</code></p>'
        f'<p>Gate <code>{e(manifest.get("selected_gate") or "context_proof_required")}</code></p>'
        f'<p>Human acceptance <code>{e(manifest.get("required_human_acceptance", False))}</code></p>'
        '</div>'
        '<h4>Next Files / Sources</h4>'
        f'<ul class="source-ref-list">{next_rows or "<li>No source refs.</li>"}</ul>'
        '<h4>Blocked Routes</h4>'
        f'<ul class="source-ref-list">{blocked_rows or "<li>No blocked route refs.</li>"}</ul>'
        '<h4>Forbidden / Omitted</h4>'
        f'<ul class="omitted-ref-list">{omitted_rows or "<li>No omitted refs.</li>"}</ul>'
        '<h4>Source Refs</h4>'
        f'<ul class="source-ref-list">{source_rows or "<li>No source refs.</li>"}</ul>'
        '</section>'
    )


def _source_ref_panel(source_refs: list[Any], omitted_refs: list[Mapping[str, Any]]) -> str:
    grouped_refs: dict[str, list[str]] = defaultdict(list)
    for ref in source_refs[:28]:
        group = _source_group(ref)
        grouped_refs[group].append(_source_ref_button(ref))
    for item in omitted_refs[:10]:
        group = "omitted"
        grouped_refs[group].append(_source_ref_button(item.get("ref"), kind="omitted_ref", summary=item.get("reason")))
    filter_buttons = [
        f'<button class="source-group-filter is-active" type="button" data-source-group-filter="all">All <b>{e(sum(len(items) for items in grouped_refs.values()))}</b></button>'
    ]
    for group, items in sorted(grouped_refs.items()):
        filter_buttons.append(
            f'<button class="source-group-filter" type="button" data-source-group-filter="{e(group)}">{e(SOURCE_GROUP_LABELS.get(group, group))} <b>{e(len(items))}</b></button>'
        )
    lanes = "".join(
        '<section class="source-ref-lane" data-source-ref-lane="{}">'.format(e(group))
        + f'<h4>{e(SOURCE_GROUP_LABELS.get(group, group))}</h4>'
        + f'<div class="source-ref-grid">{"".join(items)}</div>'
        + '</section>'
        for group, items in sorted(grouped_refs.items())
    )
    return (
        '<section class="memory-panel source-ref-drilldown">'
        '<div class="memory-panel-title"><h3>Source Ref Drilldown</h3><span>click a path/ref to inspect visible linkage</span></div>'
        f'<div class="source-group-filter-row">{"".join(filter_buttons)}</div>'
        f'{lanes or "<p class=\"empty-note\">No source refs.</p>"}'
        '</section>'
    )


def _phase_events_panel(events: list[Mapping[str, Any]]) -> str:
    rows = "".join(
        '<li class="trace-link-row" role="button" tabindex="0" '
        f'aria-label="Inspect trace event {e(item.get("event_id"))}" '
        f'data-trace-event-id="{e(item.get("event_id"))}" '
        f'data-trace-turn-id="{e(item.get("source_turn_id"))}" '
        f'data-trace-type="{e(item.get("event_type"))}" '
        f'data-trace-phase="{e(item.get("phase"))}" '
        f'data-trace-status="{e(item.get("proof_status") or item.get("status"))}" '
        f'data-trace-label="{e(item.get("label") or item.get("event_type"))}" '
        f'data-trace-refs="{e(", ".join(str(ref) for ref in (item.get("source_refs") if isinstance(item.get("source_refs"), list) else [])[:5]))}">'
        f"<b>{e(item.get('label') or item.get('event_type'))}</b>"
        f"{state_pill(item.get('proof_status') or item.get('status'))}"
        f"<code>{e(item.get('phase'))}</code>"
        f"<p>{e(', '.join(str(ref) for ref in (item.get('source_refs') if isinstance(item.get('source_refs'), list) else [])[:3]))}</p>"
        "</li>"
        for item in events[:8]
    ) or "<li><b>No phase events</b><span></span><code>none</code></li>"
    return (
        '<section class="memory-panel">'
        '<div class="memory-panel-title"><h3>Carrier Phase Events</h3><span>visible runtime trace</span></div>'
        f'<ol class="event-flow">{rows}</ol>'
        '</section>'
    )


def render_memory_visualization_body(visualization: Mapping[str, Any]) -> str:
    if not visualization:
        return '<p class="empty-note">Memory visualization projection unavailable.</p>'
    windows = _items(visualization.get("visible_windows"))
    segments = _items(visualization.get("memory_segments"))
    edges = _items(visualization.get("context_route_edges"))
    layers = _items(visualization.get("context_matryoshka_layers"))
    manifest = _mapping(visualization.get("protocol_manifest_summary"))
    token_budget = _mapping(visualization.get("token_budget_summary"))
    selected = _mapping(visualization.get("selected_turn_context"))
    events = _items(visualization.get("carrier_phase_events"))
    compaction_events = _items(visualization.get("compaction_events"))
    omitted_refs = _items(visualization.get("forbidden_or_omitted_refs"))
    source_refs = list(visualization.get("source_refs")) if isinstance(visualization.get("source_refs"), list) else []
    segments_by_id = _segment_index(segments)
    selected_segment_id = str(selected.get("selected_segment_id") or "")
    selected_segment = segments_by_id.get(selected_segment_id) or (segments[0] if segments else None)

    return (
        '<div class="memory-visualization-surface">'
        f"{_budget_strip(manifest=manifest, token_budget=token_budget, visualization=visualization)}"
        f"{_selection_panel(selected_segment)}"
        f"{_selected_turn_panel(selected=selected, segments_by_id=segments_by_id)}"
        f"{_strata_panel(windows=windows, segments=segments)}"
        f"{_matryoshka_panel(layers=layers, segments_by_id=segments_by_id)}"
        f"{_route_graph_panel(edges=edges, segments_by_id=segments_by_id)}"
        f"{_compaction_panel(compaction_events)}"
        f"{_manifest_panel(manifest, omitted_refs, source_refs)}"
        f"{_source_ref_panel(source_refs, omitted_refs)}"
        f"{_phase_events_panel(events)}"
        "</div>"
    )
