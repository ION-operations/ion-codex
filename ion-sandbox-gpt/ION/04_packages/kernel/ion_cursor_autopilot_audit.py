"""Audit Cursor /ion autopilot command, skill, subagents, and MCP bridge surfaces."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_FILES = [
    ".cursor/commands/ion.md",
    ".cursor/rules/ion-autopilot-command.mdc",
    ".cursor/skills/ion-autopilot/SKILL.md",
    ".cursor/mcp.json",
    "ION/04_packages/kernel/ion_cursor_autopilot_packet.py",
    "ION/02_architecture/ION_CURSOR_AUTOPILOT_COMMAND_AND_SUBAGENT_PROTOCOL.md",
]

REQUIRED_AGENTS = [
    ".cursor/agents/ion-steward.md",
    ".cursor/agents/ion-relay.md",
    ".cursor/agents/ion-persona-interface.md",
    ".cursor/agents/ion-mason.md",
    ".cursor/agents/ion-nemesis.md",
    ".cursor/agents/ion-context-cartographer.md",
    ".cursor/agents/ion-runtime-cartographer.md",
    ".cursor/agents/ion-scribe.md",
]

REQUIRED_PHRASES = {
    ".cursor/commands/ion.md": [
        "ION Cursor Carrier-Control Surface",
        "ion_cursor_autopilot_packet",
        "ion_carrier_continue",
        "ion_carrier_task_return",
    ],
    ".cursor/rules/ion-autopilot-command.mdc": [
        "CURSOR_CARRIER_CONTROL_SURFACE",
        "Do not ask the user which ION agent to spawn",
    ],
    ".cursor/skills/ion-autopilot/SKILL.md": [
        "ion-control",
        "Cursor subagents are carrier slots",
    ],
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def audit_cursor_autopilot(root: Path) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    for rel in REQUIRED_FILES + REQUIRED_AGENTS:
        if not (root / rel).exists():
            findings.append({"level": "error", "path": rel, "message": "required file missing"})
    for rel, phrases in REQUIRED_PHRASES.items():
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for phrase in phrases:
            if phrase not in text:
                findings.append({"level": "error", "path": rel, "message": f"missing phrase: {phrase}"})
    for rel in REQUIRED_AGENTS:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "### CONTEXT PROOF" not in text:
            findings.append({"level": "error", "path": rel, "message": "subagent lacks context proof contract"})
        if "generated" not in text.lower() or "context package" not in text.lower():
            findings.append({"level": "warning", "path": rel, "message": "subagent may not clearly require generated context package"})
    status = "ION_CURSOR_AUTOPILOT_READY" if not [f for f in findings if f["level"] == "error"] else "ION_CURSOR_AUTOPILOT_NOT_READY"
    return {
        "schema_id": "ion.cursor_autopilot_audit.v1",
        "generated_at": _now(),
        "status": status,
        "findings": findings,
        "required_files": REQUIRED_FILES,
        "required_agents": REQUIRED_AGENTS,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ION Cursor /ion autopilot surfaces")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = audit_cursor_autopilot(Path(args.ion_root).resolve())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
        for finding in result["findings"]:
            print(f"{finding['level']}: {finding['path']}: {finding['message']}")
    return 0 if result["status"] == "ION_CURSOR_AUTOPILOT_READY" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
