"""Discover canonical ION agent truenames from registry boots (Cursor spawn validation)."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _boot_index(root: Path) -> dict[str, str]:
    """Map normalized role key (uppercase, ``-`` → ``_``) to actual ``*.boot.md`` filename."""

    boots = root.resolve() / "ION" / "03_registry" / "boots"
    idx: dict[str, str] = {}
    if not boots.is_dir():
        return idx
    for path in boots.glob("*.boot.md"):
        if not path.is_file():
            continue
        stem = path.name.removesuffix(".boot.md")
        key = stem.upper().replace("-", "_")
        idx[key] = path.name
    return idx


def ion_boot_agent_names(root: Path) -> tuple[str, ...]:
    """Return sorted uppercase truenames for every ``*.boot.md`` under ``ION/03_registry/boots/``."""

    idx = _boot_index(root)
    return tuple(sorted(idx.keys()))


def validate_cursor_subagent_role_packet(
    *,
    root: Path,
    agent_name: str,
    boot_filename: str | None = None,
) -> dict[str, Any]:
    """Check ``agent_name`` against on-disk boots; optional ``boot_filename`` must match."""

    root = root.resolve()
    idx = _boot_index(root)
    normalized = agent_name.strip().upper().replace("-", "_")
    in_registry = normalized in idx
    expected_file = idx.get(normalized)
    resolved_boot = root / "ION" / "03_registry" / "boots" / expected_file if expected_file else None
    boot_exists = resolved_boot.is_file() if resolved_boot is not None else False
    boot_match_ok = True
    if boot_filename is not None and expected_file is not None:
        boot_match_ok = boot_filename.strip() == expected_file

    return {
        "agent_name": normalized,
        "allowed_roles": tuple(sorted(idx.keys())),
        "in_registry": in_registry,
        "expected_boot_file": expected_file,
        "expected_boot_path": str(resolved_boot.relative_to(root)) if boot_exists and resolved_boot else None,
        "boot_exists": boot_exists,
        "boot_filename_match": boot_match_ok,
        "packet_ok": in_registry and boot_exists and (boot_filename is None or boot_match_ok),
    }
