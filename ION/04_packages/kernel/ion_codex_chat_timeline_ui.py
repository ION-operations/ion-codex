"""Timeline and trace drawer renderers for Codex Chat."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .ion_codex_chat_ui_common import e, short, state_pill


def render_timeline_body(timeline: Mapping[str, Any]) -> str:
    traces = [trace for trace in timeline.get("traces", []) if isinstance(trace, Mapping)] if isinstance(timeline.get("traces"), list) else []
    event_type_counts: dict[str, int] = {}
    for trace in traces:
        for event in trace.get("events") or []:
            if isinstance(event, Mapping):
                key = str(event.get("event_type") or "event")
                event_type_counts[key] = event_type_counts.get(key, 0) + 1
    event_type_rows = "".join(
        f"<li><code>{e(kind)}</code>{e(count)}</li>"
        for kind, count in sorted(event_type_counts.items())
    ) or "<li><code>none</code>0</li>"
    trace_cards = []
    for trace in traces[-4:]:
        events = [event for event in trace.get("events", []) if isinstance(event, Mapping)] if isinstance(trace.get("events"), list) else []
        event_rows = "".join(
            "<li>"
            f"<b>{e(event.get('label') or event.get('event_type'))}</b>"
            f"{state_pill(event.get('proof_status') or event.get('status'))}"
            f"<code>{e(event.get('tool_name') or event.get('event_type'))}</code>"
            f"<p>{e(short(event.get('detail'), limit=160))}</p>"
            "</li>"
            for event in events[:8]
        ) or "<li><b>No events</b><span></span><code>none</code></li>"
        trace_cards.append(
            '<article class="trace-card">'
            f'<div class="trace-card-head"><code>{e(trace.get("turn_id"))}</code><b>{e(trace.get("event_count") or len(events))} events</b></div>'
            f"<ol class=\"event-flow\">{event_rows}</ol>"
            "</article>"
        )
    if not trace_cards:
        trace_cards.append('<p class="empty-note">No user turn traces yet.</p>')
    return (
        f"<p>Trace policy: <code>{e(timeline.get('policy'))}</code></p>"
        '<div class="drawer-kpis">'
        f'<div class="drawer-kpi"><span>Traces</span><b>{e(timeline.get("trace_count") or len(traces))}</b></div>'
        f'<div class="drawer-kpi"><span>Runner</span><b>{e(timeline.get("runner_active", False))}</b></div>'
        f'<div class="drawer-kpi"><span>Queued</span><b>{e(timeline.get("queued_request_count", 0))}</b></div>'
        '</div>'
        '<h3>Trace Event Flow</h3>'
        f'<ul class="count-list">{event_type_rows}</ul>'
        f'{"".join(trace_cards)}'
    )
