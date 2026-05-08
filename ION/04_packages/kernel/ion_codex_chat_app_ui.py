"""Compatibility facade for the Codex Chat cockpit app shell.

The implementation is split across focused render modules so this file no
longer owns shell, chat, inspector, timeline, CSS, and JavaScript at once.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .ion_codex_chat_shell_ui import render_codex_chat_shell_html


def render_codex_chat_app_html(model: Mapping[str, Any], *, base_path: str = "/chat", auth_token: str | None = None) -> str:
    return render_codex_chat_shell_html(model, base_path=base_path, auth_token=auth_token)
