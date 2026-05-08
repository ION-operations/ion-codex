"""Audit Cursor hook bridge readiness for ION V87.

The hook bridge is the host-side guardrail that makes Cursor session start behave
as ION carrier-control instead of ordinary free chat.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FILES = {
    "protocol": "ION/02_architecture/ION_CURSOR_SDK_HOOK_BRIDGE_PROTOCOL.md",
    "hooks_json": ".cursor/hooks.json",
    "session_start_hook": ".cursor/hooks/ion_carrier_session_start.py",
    "skill": ".cursor/skills/ion-carrier-control/SKILL.md",
    "command_continue": ".cursor/commands/ion-continue.md",
    "sdk_readme": "ION/09_integrations/cursor_sdk/README.md",
    "sdk_package": "ION/09_integrations/cursor_sdk/package.json",
    "sdk_agent": "ION/09_integrations/cursor_sdk/src/ion_cursor_sdk_carrier.ts",
}

REQUIRED_HOOK_PHRASES = [
    "kernel.ion_carrier_continue",
    "kernel.ion_carrier_workflow_audit",
    "kernel.ion_cursor_workflow_topology_audit",
    "kernel.ion_cursor_hooks_audit",
    "ACTIVE_CURSOR_HOOK_STATE.json",
    "additional_context",
    "ION Cursor Carrier-Control Surface",
]


def _resolve_root(root: str | Path | None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    if (candidate / "ION" / "REPO_AUTHORITY.md").exists() and (candidate / "pyproject.toml").exists():
        return candidate
    if candidate.name == "ION" and (candidate / "REPO_AUTHORITY.md").exists() and (candidate.parent / "pyproject.toml").exists():
        return candidate.parent
    raise FileNotFoundError("Could not resolve ION shell root; expected pyproject.toml and ION/REPO_AUTHORITY.md")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def audit_cursor_hooks(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    findings: list[str] = []

    for label, rel in REQUIRED_FILES.items():
        if not (shell_root / rel).exists():
            findings.append(f"missing_{label}:{rel}")

    hooks_path = shell_root / REQUIRED_FILES["hooks_json"]
    if hooks_path.exists():
        try:
            hooks = json.loads(_read(hooks_path))
        except json.JSONDecodeError as exc:
            findings.append(f"hooks_json_invalid:{exc}")
            hooks = {}
        session_hooks = (((hooks.get("hooks") or {}).get("sessionStart")) if isinstance(hooks, dict) else None)
        if not isinstance(session_hooks, list):
            findings.append("hooks_json_missing_sessionStart_list")
        else:
            commands = [str(item.get("command", "")) for item in session_hooks if isinstance(item, dict)]
            if not any("ion_carrier_session_start.py" in command for command in commands):
                findings.append("sessionStart_missing_ion_carrier_session_start")
            if any("persona" in command.lower() for command in commands):
                findings.append("sessionStart_still_points_to_persona_named_hook")

    hook_path = shell_root / REQUIRED_FILES["session_start_hook"]
    if hook_path.exists():
        text = _read(hook_path)
        for phrase in REQUIRED_HOOK_PHRASES:
            if phrase not in text:
                findings.append(f"hook_missing_phrase:{phrase}")

    skill_path = shell_root / REQUIRED_FILES["skill"]
    if skill_path.exists():
        skill = _read(skill_path)
        for phrase in (".cursor/hooks.json", "sessionStart", "ACTIVE_CURSOR_HOOK_STATE.json"):
            if phrase not in skill:
                findings.append(f"skill_missing_hook_bridge_phrase:{phrase}")

    continue_path = shell_root / REQUIRED_FILES["command_continue"]
    if continue_path.exists():
        command = _read(continue_path)
        if "ACTIVE_CURSOR_HOOK_STATE.json" not in command:
            findings.append("ion_continue_command_missing_hook_state_reference")

    tasks_path = shell_root / ".vscode/tasks.json"
    if tasks_path.exists():
        try:
            tasks = json.loads(_read(tasks_path))
            labels = {str(task.get("label", "")) for task in tasks.get("tasks", []) if isinstance(task, dict)}
            if "ION: cursor hooks audit" not in labels:
                findings.append("missing_vscode_task_label:ION: cursor hooks audit")
        except json.JSONDecodeError as exc:
            findings.append(f"tasks_json_invalid:{exc}")
    else:
        findings.append("missing_vscode_tasks_json")

    return {
        "schema_id": "ion.cursor_hooks_audit.v1",
        "verdict": "ION_CURSOR_HOOK_BRIDGE_READY" if not findings else "ION_CURSOR_HOOK_BRIDGE_BLOCKED",
        "findings": findings,
        "checked_files": REQUIRED_FILES,
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Cursor hook bridge readiness for ION.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = audit_cursor_hooks(args.ion_root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["verdict"] == "ION_CURSOR_HOOK_BRIDGE_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
