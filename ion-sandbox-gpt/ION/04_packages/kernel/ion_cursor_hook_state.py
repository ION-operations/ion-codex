"""Project Cursor hook state into the active ION runtime surface.

The real Cursor sessionStart hook writes ``ACTIVE_CURSOR_HOOK_STATE.json`` when
Cursor invokes it. This module gives shell/CI carriers a deterministic way to
publish the same status surface without pretending a live Cursor hook fired.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_cursor_hooks_audit import REQUIRED_FILES, audit_cursor_hooks


ACTIVE_CURSOR_HOOK_STATE_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CURSOR_HOOK_STATE.json")


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_cursor_hook_state(
    root: str | Path | None = None,
    *,
    live_hook_event_seen: bool = False,
    source: str = "kernel.ion_cursor_hook_state",
) -> dict[str, Any]:
    """Build a truthful Cursor hook-state projection.

    ``live_hook_event_seen`` should only be true when called from the actual
    Cursor hook path. Normal shell projection keeps it false even when the hook
    bridge files audit as ready.
    """

    shell_root = resolve_shell_root_from_ion_root(root)
    audit = audit_cursor_hooks(shell_root)
    bridge_ready = audit.get("verdict") == "ION_CURSOR_HOOK_BRIDGE_READY"
    status = (
        "live_session_start_observed"
        if live_hook_event_seen and bridge_ready
        else ("projected_not_connected" if bridge_ready else "blocked")
    )
    return {
        "schema_id": "ion.cursor_hook_state.v1",
        "created_at": _iso_now(),
        "status": status,
        "state_source": source,
        "hook": "sessionStart",
        "hook_script": REQUIRED_FILES["session_start_hook"],
        "shell_root": str(shell_root),
        "cursor_hook_bridge_verdict": audit.get("verdict"),
        "cursor_hook_bridge_ready": bridge_ready,
        "cursor_hook_bridge_findings": audit.get("findings", []),
        "checked_files": audit.get("checked_files", REQUIRED_FILES),
        "host_connection_state": "LIVE_HOOK_EVENT_OBSERVED" if live_hook_event_seen else "NOT_CONNECTED_OR_NOT_OBSERVED",
        "live_hook_event_seen": live_hook_event_seen,
        "continue_exit_code": None,
        "continue_verdict": None,
        "active_turn_packet_path": None,
        "active_spawn_plan_path": None,
        "task_return_ledger_path": None,
        "steward_integration_queue_path": None,
        "spawn_queue_count": None,
        "audits": [
            {
                "label": "cursor_hooks",
                "exit_code": 0 if bridge_ready else 1,
                "status": audit.get("verdict"),
                "findings": audit.get("findings", []),
            }
        ],
        "production_authority": False,
        "live_execution_authority": False,
    }


def write_cursor_hook_state(
    root: str | Path | None = None,
    *,
    output: str | Path | None = None,
    live_hook_event_seen: bool = False,
    source: str = "kernel.ion_cursor_hook_state",
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    state = build_cursor_hook_state(shell_root, live_hook_event_seen=live_hook_event_seen, source=source)
    out = shell_root / (Path(output) if output else ACTIVE_CURSOR_HOOK_STATE_RELATIVE_PATH)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project ION Cursor hook state.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--live-hook-event-seen", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    state = (
        write_cursor_hook_state(
            args.ion_root,
            output=args.output,
            live_hook_event_seen=args.live_hook_event_seen,
        )
        if args.write
        else build_cursor_hook_state(args.ion_root, live_hook_event_seen=args.live_hook_event_seen)
    )
    if args.json:
        print(json.dumps(state, indent=2, sort_keys=True))
    else:
        print(f"ION_CURSOR_HOOK_STATE_{state['status'].upper()}")
    return 0 if state["cursor_hook_bridge_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
