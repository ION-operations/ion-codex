"""Shared helpers for Codex Chat cockpit UI renderers."""
from __future__ import annotations

import html
from typing import Any

CAPSULE_PATH = "ION/05_context/current/codex_solo/CAPSULE.md"
MINI_PATH = "ION/05_context/current/codex_solo/MINI.md"


def e(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def short(value: Any, *, limit: int = 1400) -> str:
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n..."


def icon(name: str) -> str:
    paths = {
        "chat": '<path d="M5 6.5h14v8.5H9l-4 3v-11.5Z"/><path d="M8 9.5h8M8 12h5"/>',
        "context": '<path d="M5 12a7 7 0 1 1 14 0a7 7 0 0 1-14 0Z"/><path d="M12 5v14M5 12h14"/>',
        "timeline": '<path d="M6 5v14"/><path d="M6 7h10l2 2-2 2H6"/><path d="M6 14h8l2 2-2 2H6"/>',
        "skills": '<path d="M7 4h10l2 3l-7 13L5 7l2-3Z"/><path d="M7 4l5 16l5-16"/><path d="M5 7h14"/>',
        "agents": '<path d="M8 19v-2a4 4 0 0 1 8 0v2"/><path d="M12 11a3 3 0 1 0 0-6a3 3 0 0 0 0 6Z"/><path d="M18 10.5a2.5 2.5 0 0 1 1 4.8"/>',
        "runs": '<path d="M5 12h10"/><path d="m12 8 4 4-4 4"/><path d="M5 6h14M5 18h14"/>',
        "receipts": '<path d="M7 4h10v16l-2-1.2-2 1.2-2-1.2-2 1.2-2-1.2V4Z"/><path d="M9 8h6M9 12h6M9 16h4"/>',
        "ion": '<path d="M12 4v16"/><path d="M5 8h14"/><path d="M5 16h14"/><path d="m8 5-3 3 3 3"/><path d="m16 13 3 3-3 3"/>',
        "settings": '<path d="M12 8.5a3.5 3.5 0 1 0 0 7a3.5 3.5 0 0 0 0-7Z"/><path d="M4 12h2M18 12h2M12 4v2M12 18v2M6.4 6.4l1.4 1.4M16.2 16.2l1.4 1.4M17.6 6.4l-1.4 1.4M7.8 16.2l-1.4 1.4"/>',
    }
    paths["graph"] = paths["context"]
    paths["stream"] = paths["timeline"]
    paths["lens"] = paths["agents"]
    paths["route"] = paths["runs"]
    paths["receipt"] = paths["receipts"]
    body = paths.get(name, paths["chat"])
    return (
        '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'
        f"{body}</svg>"
    )


def state_pill(value: Any) -> str:
    text = str(value or "unknown")
    lowered = text.lower()
    tone = "watch"
    if lowered in {"true", "ready", "accepted", "visible", "ok"} or "ready" in lowered or "accepted" in lowered:
        tone = "ready"
    elif lowered in {"false", "blocked", "failed"} or "blocked" in lowered or "fail" in lowered or "missing" in lowered:
        tone = "blocked"
    return f'<span class="state-pill {tone}">{e(text)}</span>'


def display_summary(value: Any) -> str:
    text = str(value or "")
    replacements = {
        "Codex Capsule Chat": "Codex Chat",
        "Codex Capsule chat": "Codex chat using Capsule context",
        "Codex Capsule app": "Codex chat app",
        "Codex Capsule": "Codex plus Capsule context",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def mini_brief(raw_text: Any) -> str:
    text = str(raw_text or "").strip()
    if not text:
        return "Mini not initialized."
    prefixes = (
        "CODEX SOLO MINI INDEX",
        "ROLE:",
        "ACTIVE_CAPSULE:",
        "HOT_CONTEXT:",
        "LONG_HORIZON:",
        "PACKAGES:",
        "HISTORY:",
        "PHASE:",
        "ACTIVE_TEMPLATE:",
        "ROUTE_INDEX:",
        "POLICY:",
    )
    lines = [line for line in text.splitlines() if line.strip()]
    brief = [line for line in lines if line.startswith(prefixes)]
    lookup_count = sum(1 for line in lines if line.startswith("- C-"))
    if lookup_count:
        brief.append(f"CAPSULE_LOOKUP: {lookup_count} receipt rows available in history.")
    return "\n".join(brief[:16]) or "Mini context available in model evidence."


def drawer(drawer_id: str, title: str, metric: Any, body: str) -> str:
    return (
        f'<details class="inspector-card" id="{e(drawer_id)}">'
        f'<summary class="section-title">{e(title)} <b>{e(metric)}</b></summary>'
        f"{body}</details>"
    )
