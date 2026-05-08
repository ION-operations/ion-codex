#!/usr/bin/env python3
"""Codex SessionStart hook for ION Codex Solo capsule context.

The hook is intentionally read-only. It injects a bounded HOT_CONTEXT-derived
developer context block when Codex starts in the active ION root.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ACTIVE_ROOT = Path("/home/sev/ION - Production/ION_CODEX FULL").resolve()
PACKAGE_ROOT = ACTIVE_ROOT / "ION" / "04_packages"


def _read_stdin() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root)
    except ValueError:
        return False
    return True


def _soft_context(message: str) -> dict[str, Any]:
    return {
        "continue": True,
        "systemMessage": message,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": (
                "ION Codex Solo capsule context was not loaded automatically. "
                f"{message}"
            ),
        },
    }


def main() -> int:
    payload = _read_stdin()
    cwd = Path(str(payload.get("cwd") or ".")).expanduser().resolve()
    if not _is_relative_to(cwd, ACTIVE_ROOT):
        print(json.dumps(_soft_context(f"cwd is outside active ION root: {cwd}")))
        return 0
    if not (ACTIVE_ROOT / "pyproject.toml").is_file() or not (ACTIVE_ROOT / "ION" / "REPO_AUTHORITY.md").is_file():
        print(json.dumps(_soft_context("active root proof files are missing.")))
        return 0

    sys.path.insert(0, str(PACKAGE_ROOT))
    try:
        from kernel.ion_codex_solo_context import build_codex_solo_boot_context

        boot = build_codex_solo_boot_context(ACTIVE_ROOT)
        context = str(boot.get("context") or "")
        if not context:
            print(json.dumps(_soft_context("boot context was empty.")))
            return 0
        print(json.dumps({
            "continue": True,
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            },
        }))
        return 0
    except Exception as exc:  # pragma: no cover - hook fail-soft boundary
        print(json.dumps(_soft_context(f"hook error: {exc}")))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
