"""V73 — Cursor carrier mount and context-law audit (read-only filesystem checks)."""

from __future__ import annotations

from pathlib import Path
from typing import Any


_LAW_RELATIVE_PATHS = (
    "ION/REPO_AUTHORITY.md",
    "ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md",
    ".cursor/rules/ion-carrier-mount.mdc",
    "ION/docs/cursor/CURSOR_AS_ION_CARRIER_GUIDE.md",
    "ION/docs/cursor/ION_WORK_PACKET_TEMPLATE.md",
    "ION/docs/cursor/CURSOR_SUBAGENT_ION_ROLE_SPAWN.md",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def audit_v73_cursor_carrier_mount(root: Path) -> dict[str, Any]:
    """Return structured audit facts for carrier/context law surfaces under ``root``."""

    root = root.resolve()
    missing_paths: list[str] = []
    for rel in _LAW_RELATIVE_PATHS:
        p = root / rel
        if not p.is_file():
            missing_paths.append(rel)

    corpus_lc = ""
    if not missing_paths:
        corpus_lc = "\n".join(_read(root / rel) for rel in _LAW_RELATIVE_PATHS).lower()

    markers: dict[str, bool] = {
        "cursor_carrier_chassis": ("chassis" in corpus_lc and "cursor" in corpus_lc)
        or ("carrier" in corpus_lc and "cursor" in corpus_lc),
        "explicit_steward_mount": ("steward" in corpus_lc and "mount" in corpus_lc)
        or "local steward" in corpus_lc
        or "local_steward_carrier" in corpus_lc.replace(" ", "_"),
        "subagent_carrier_slot_not_role": ("subagent" in corpus_lc and "carrier slot" in corpus_lc)
        or ("subagent" in corpus_lc and "not a role" in corpus_lc),
        "workpacket_or_contextpackage": ("context package" in corpus_lc)
        or ("work packet" in corpus_lc)
        or ("workpacket" in corpus_lc),
        "proposals_until_integrated": ("proposal" in corpus_lc and "integrat" in corpus_lc),
        "no_separate_cursor_agent_ontology": ("does not define a separate" in corpus_lc)
        or ("separate" in corpus_lc and "ontology" in corpus_lc and "not" in corpus_lc),
        "manual_template_bound": ("manual" in corpus_lc and "template" in corpus_lc),
        "mini_capsule_not_primary": ("mini" in corpus_lc and "capsule" in corpus_lc and "primary" in corpus_lc and "not" in corpus_lc)
        or ("mini/capsule" in corpus_lc and "not" in corpus_lc),
        "no_sibling_archive_authority": ("sibling" in corpus_lc and "archives" in corpus_lc)
        or ("sibling" in corpus_lc and "authority" in corpus_lc),
        "production_authority_false": ("production_authority" in corpus_lc and "false" in corpus_lc)
        or ("no production" in corpus_lc)
        or ("no production authority" in corpus_lc),
    }

    missing_markers = [name for name, ok in markers.items() if not ok]
    carrier_law_ok = not missing_paths and not missing_markers

    return {
        "audit_id": "v73_cursor_carrier_mount",
        "root": str(root),
        "carrier_law_ok": carrier_law_ok,
        "production_authority": False,
        "live_execution_authorized": False,
        "missing_paths": missing_paths,
        "missing_markers": missing_markers,
        "markers": markers,
    }
