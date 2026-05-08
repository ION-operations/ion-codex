"""Main conversation and composer renderers for Codex Chat."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .ion_codex_chat_ui_common import CAPSULE_PATH, MINI_PATH, e, short


def _context_turn_display(turn: Mapping[str, Any]) -> str:
    if turn.get("kind") != "mini_auto_post":
        return str(turn.get("message") or "")
    lines = [
        "Context refreshed.",
        f"mini_ref: {turn.get('mini_ref') or MINI_PATH}",
        f"capsule_ref: {turn.get('capsule_ref') or CAPSULE_PATH}",
    ]
    if turn.get("mini_sha256"):
        lines.append(f"mini_sha256: {turn.get('mini_sha256')}")
    lines.append("Full Mini and Capsule history remain available through model/context evidence.")
    return "\n".join(lines)


def _bubble(turn: Mapping[str, Any], css_class: str, label: str) -> str:
    message = str(turn.get("message") or "")
    body = short(message)
    payload = ""
    turn_id = str(turn.get("turn_id") or "")
    memory_segment_id = f"turn:{turn_id}" if turn_id else ""
    turn_attrs = ""
    if turn_id:
        turn_attrs = (
            f' role="button" tabindex="0" data-chat-turn-id="{e(turn_id)}" '
            f'data-memory-segment-id="{e(memory_segment_id)}" '
            f'aria-label="Inspect chat turn {e(turn_id)}"'
        )
    if len(message) > len(body):
        payload = f"<details><summary>Full payload</summary><pre>{e(message)}</pre></details>"
    return (
        f'<article class="bubble {css_class}"{turn_attrs}>'
        f'<div class="bubble-head"><span>{e(label)}</span><time>{e(turn.get("created_at"))}</time></div>'
        f"<div>{e(body)}</div>{payload}</article>"
    )


def _return_card(record: Mapping[str, Any]) -> str:
    proof_status = str(record.get("proof_status") or "pending")
    label = {
        "accepted": "Proof accepted",
        "blocked": "Proof blocked",
        "returned": "Proof returned",
        "running": "Codex running",
        "pending": "Codex queued",
    }.get(proof_status, "Codex proof")
    lines = [f"status: {record.get('status') or 'unknown'}", f"request: {record.get('request_id') or 'none'}"]
    if record.get("latest_run_path"):
        lines.append(f"run: {record.get('latest_run_path')}")
    if record.get("latest_return_path"):
        lines.append(f"return: {record.get('latest_return_path')}")
    findings = [str(value) for value in (record.get("context_proof_findings") or [])]
    findings.extend(str(value) for value in (record.get("template_action_proof_findings") or []))
    if findings:
        lines.append(f"findings: {', '.join(findings)}")
    preview = str(record.get("task_output_preview") or "").strip()
    if preview:
        lines.extend(["", preview])
    touched_paths = record.get("touched_paths") if isinstance(record.get("touched_paths"), list) else []
    touched = ""
    if touched_paths:
        touched = "<details><summary>Touched paths</summary><pre>" + e("\n".join(str(path) for path in touched_paths)) + "</pre></details>"
    return (
        f'<article class="bubble proof {e(proof_status)}">'
        f'<div class="bubble-head"><span>{e(label)}</span><time>{e(record.get("request_path"))}</time></div>'
        f"<div>{e(chr(10).join(lines))}</div>{touched}</article>"
    )


def _trace_drawer(trace: Mapping[str, Any] | None) -> str:
    if not trace:
        return ""
    events = trace.get("events") if isinstance(trace.get("events"), list) else []
    if not events:
        return ""
    rows = []
    for event in events[:18]:
        if not isinstance(event, Mapping):
            continue
        refs = event.get("source_refs") if isinstance(event.get("source_refs"), list) else []
        detail = short(event.get("detail"), limit=260)
        rows.append(
            '<li class="trace-event">'
            f"<b>{e(event.get('label') or event.get('event_type'))}</b>"
            f"<span>{e(event.get('status'))}</span>"
            f"<code>{e(event.get('tool_name') or event.get('event_type'))}</code>"
            f"<span>{e(event.get('proof_status') or event.get('timestamp') or '')}</span>"
            f"<p>{e(detail)}</p><p>{e(', '.join(str(ref) for ref in refs[:3]))}</p>"
            "</li>"
        )
    policy = "Context, tool, queue, file, and proof events. Raw hidden reasoning is not exposed."
    return (
        f'<details class="turn-trace-drawer"><summary>Turn trace · {e(trace.get("event_count") or len(rows))} events</summary>'
        f"<ol>{''.join(rows)}</ol><p class=\"mini-text\">{e(policy)}</p></details>"
    )


def render_chat_groups(groups: list[Mapping[str, Any]]) -> str:
    if not groups:
        return '<div class="capsule-empty">Ask Codex.</div>'
    rendered = []
    for group in groups[-30:]:
        parts = []
        user_turn = group.get("user_turn") if isinstance(group.get("user_turn"), Mapping) else None
        group_turn_id = str((user_turn or {}).get("turn_id") or "")
        if user_turn:
            parts.append(_bubble(user_turn, "user", "You"))
        for turn in group.get("assistant_turns") or []:
            if isinstance(turn, Mapping):
                parts.append(_bubble(turn, "assistant", "Codex"))
        for turn in group.get("execution_turns") or []:
            if isinstance(turn, Mapping):
                parts.append(_bubble(turn, "execution", "Execution"))
        for record in group.get("return_records") or []:
            if isinstance(record, Mapping):
                parts.append(_return_card(record))
        trace = group.get("turn_trace") if isinstance(group.get("turn_trace"), Mapping) else None
        parts.append(_trace_drawer(trace))
        for turn in group.get("context_turns") or []:
            if isinstance(turn, Mapping):
                parts.append(_bubble({**dict(turn), "message": _context_turn_display(turn)}, "context", "Context update"))
        for turn in group.get("other_turns") or []:
            if isinstance(turn, Mapping):
                parts.append(_bubble(turn, "assistant", str(turn.get("author") or "system")))
        group_attr = f' data-turn-group-id="{e(group_turn_id)}"' if group_turn_id else ""
        rendered.append(f'<section class="turn-group"{group_attr}>{"".join(parts)}</section>')
    return "".join(rendered)


def render_composer(composer: Mapping[str, Any], *, base_path: str, token_input: str) -> str:
    primary_mode = e(composer.get("primary_mode") or "respond_only")
    run_mode = e(composer.get("run_mode") or "queue_for_codex")
    return f"""
    <form class="capsule-composer" method="post" action="{e(base_path)}/turn">
      {token_input}
      <input type="hidden" name="lane_id" value="{e(composer.get('lane_id') or 'codex_general')}">
      <input type="hidden" name="author" value="operator">
      <div class="composer-inner">
        <div class="composer-mode" role="radiogroup" aria-label="Message mode">
          <label><input type="radio" name="execution_mode" value="{primary_mode}" checked><span>Chat</span></label>
          <label><input type="radio" name="execution_mode" value="{run_mode}"><span>{e(composer.get('run_label') or 'Run task')}</span></label>
        </div>
        <textarea name="message" rows="3" placeholder="Ask Codex"></textarea>
        <button type="submit" data-ready-label="{e(composer.get('primary_label') or 'Send')}" data-busy-label="Sending...">{e(composer.get('primary_label') or 'Send')}</button>
      </div>
    </form>"""


def render_main_chat(conversation: Mapping[str, Any], composer: Mapping[str, Any], *, base_path: str, token_input: str) -> str:
    groups = conversation.get("turn_groups") if isinstance(conversation.get("turn_groups"), list) else []
    return (
        '<section class="capsule-main-chat" id="chat" aria-label="Codex Chat">'
        '<div class="capsule-message-scroll">'
        f'<div class="capsule-message-stack">{render_chat_groups(groups)}</div>'
        "</div>"
        f"{render_composer(composer, base_path=base_path, token_input=token_input)}"
        "</section>"
    )
