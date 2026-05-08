"""V75 — Cursor full workflow mount surfaces (RELAY → STEWARD → spawn law)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

_PROTOCOL = Path("ION/02_architecture/ION_CURSOR_FULL_WORKFLOW_MOUNT_PROTOCOL.md")
_FW_GUIDE = Path("ION/docs/cursor/CURSOR_FULL_WORKFLOW_MOUNT_GUIDE.md")
_FW_RULE = Path(".cursor/rules/ion-full-workflow-mount.mdc")
_SPAWN_TEMPLATE = Path("ION/docs/cursor/ION_SUBAGENT_SPAWN_PACKET_TEMPLATE.md")
_SPAWN_READINESS = Path("ION/docs/cursor/ION_SUBAGENT_SPAWN_READINESS_GUIDE.md")
_LIVE = Path("ION/docs/cursor/ION_LIVE_WORKFLOW_STATUS_PACKET.md")


def _read(root: Path, rel: Path) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="replace")


def audit_v75_cursor_full_workflow_mount(root: Path) -> dict[str, Any]:
    """Verify full-workflow mount documentation set and spawn stack wording."""

    root = root.resolve()
    paths = (
        _PROTOCOL,
        _FW_GUIDE,
        _FW_RULE,
        _SPAWN_TEMPLATE,
        _SPAWN_READINESS,
        _LIVE,
    )
    missing = [str(p) for p in paths if not (root / p).is_file()]

    corpus = ""
    if (root / _PROTOCOL).is_file():
        corpus += _read(root, _PROTOCOL)
    if (root / _FW_GUIDE).is_file():
        corpus += _read(root, _FW_GUIDE)
    lc = corpus.lower()
    spawn_stack_ok = (
        "relay" in lc
        and "steward" in lc
        and "spawn" in lc
        and ("named ion role" in lc or "named role" in lc)
        and ("context package" in lc or "work packet" in lc)
        and "proposal" in lc
    )

    rule_ok = False
    if (root / _FW_RULE).is_file():
        rlc = _read(root, _FW_RULE).lower()
        rule_ok = "carrier slot" in rlc and "relay" in rlc and "steward" in rlc and (
            "named ion role" in rlc or "named role" in rlc
        )

    ok = not missing and spawn_stack_ok and rule_ok

    return {
        "audit_id": "v75_cursor_full_workflow_mount",
        "root": str(root),
        "full_workflow_surfaces_ok": ok,
        "missing_paths": missing,
        "spawn_stack_documented": spawn_stack_ok,
        "full_workflow_rule_ok": rule_ok,
        "production_authority": False,
        "live_execution_authorized": False,
    }
