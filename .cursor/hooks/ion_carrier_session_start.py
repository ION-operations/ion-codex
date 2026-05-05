#!/usr/bin/env python3
"""Cursor sessionStart hook for the ION carrier-control surface.

V87 replaces the stale persona-named session hook with a carrier-control hook.
The hook is intentionally procedural: it does not role-play STEWARD, RELAY, or
PERSONA. It refreshes the active carrier turn state with the unified V84/V85
entrypoint, runs workflow/topology/hook audits, writes an operator-visible hook
state file, and injects a short additional_context block into Cursor.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HOOK_STATE_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CURSOR_HOOK_STATE.json")


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json_stdin() -> dict[str, Any]:
    raw = sys.stdin.read() or "{}"
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else {"raw_hook_payload": raw}
    except json.JSONDecodeError:
        return {"raw_hook_payload": raw}


def _shell_roots_from_hook_input(data: dict[str, Any]) -> list[Path]:
    roots: list[Path] = []
    for key in ("workspace_roots", "workspaceRoots", "roots", "folders", "workspaceFolders"):
        val = data.get(key)
        if isinstance(val, list):
            for item in val:
                if isinstance(item, str) and item.strip():
                    roots.append(Path(item).expanduser().resolve())
                elif isinstance(item, dict) and item.get("path"):
                    roots.append(Path(str(item["path"])).expanduser().resolve())
    here = Path(__file__).resolve()
    roots.append(here.parents[2])
    roots.append(Path.cwd().resolve())
    deduped: list[Path] = []
    for root in roots:
        if root not in deduped:
            deduped.append(root)
    return deduped


def _resolve_shell_root(candidates: list[Path]) -> Path | None:
    for base in candidates:
        for p in (base, *base.parents):
            if (p / "pyproject.toml").is_file() and (p / "ION" / "REPO_AUTHORITY.md").is_file():
                return p
    return None


def _run_json_module(shell_root: Path, module: str, args: list[str], timeout: int = 120) -> tuple[int, dict[str, Any] | None, str]:
    env = {**os.environ, "PYTHONPATH": str(shell_root / "ION" / "04_packages")}
    cmd = [sys.executable, "-m", module, *args]
    try:
        proc = subprocess.run(cmd, cwd=str(shell_root), env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        return 124, None, f"timeout running {' '.join(cmd)}: {exc}"
    except OSError as exc:
        return 127, None, f"failed running {' '.join(cmd)}: {exc}"
    raw = (proc.stdout or "").strip()
    if raw:
        try:
            parsed = json.loads(raw)
            return proc.returncode, parsed if isinstance(parsed, dict) else {"value": parsed}, proc.stderr or ""
        except json.JSONDecodeError:
            return proc.returncode, None, raw[:12000] + (("\nstderr:\n" + proc.stderr[:4000]) if proc.stderr else "")
    return proc.returncode, None, proc.stderr or "(no stdout)"


def _spawn_lines(result: dict[str, Any] | None) -> list[str]:
    if not result:
        return ["- unavailable: carrier continuation did not return JSON"]
    rows = result.get("spawn_queue")
    if not isinstance(rows, list) or not rows:
        return ["- no spawn=true rows in ACTIVE_CARRIER_TURN_PACKET.json"]
    lines: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        lines.append(
            f"- {row.get('index')}. `{row.get('role')}` → `{row.get('context_package_path')}` "
            f"(receipt: `{row.get('context_load_receipt_path')}`)"
        )
    return lines or ["- no valid spawn rows"]


def _audit_summary(label: str, code: int, payload: dict[str, Any] | None, fallback: str) -> dict[str, Any]:
    if payload is None:
        return {"label": label, "exit_code": code, "status": "no_json", "summary": fallback[:1200]}
    return {
        "label": label,
        "exit_code": code,
        "status": payload.get("verdict") or payload.get("status") or ("ok" if code == 0 else "nonzero"),
        "findings": payload.get("findings", []),
    }


def main() -> int:
    hook_payload = _json_stdin()
    shell_root = _resolve_shell_root(_shell_roots_from_hook_input(hook_payload))
    if shell_root is None:
        ctx = (
            "## ION carrier hook could not resolve shell root\n\n"
            "Open the repository root that contains `pyproject.toml` and `ION/REPO_AUTHORITY.md`."
        )
        sys.stdout.write(json.dumps({"continue": True, "additional_context": ctx}, ensure_ascii=False))
        return 0

    code_continue, continue_result, continue_text = _run_json_module(
        shell_root,
        "kernel.ion_carrier_continue",
        ["--ion-root", ".", "--carrier", "cursor", "--operator-message", "continue", "--json"],
        timeout=180,
    )
    audits: list[dict[str, Any]] = []
    for label, module in (
        ("carrier_workflow", "kernel.ion_carrier_workflow_audit"),
        ("cursor_topology", "kernel.ion_cursor_workflow_topology_audit"),
        ("cursor_hooks", "kernel.ion_cursor_hooks_audit"),
    ):
        code, payload, text = _run_json_module(shell_root, module, ["--ion-root", ".", "--json"], timeout=90)
        audits.append(_audit_summary(label, code, payload, text))
    cursor_hooks_audit = next((audit for audit in audits if audit.get("label") == "cursor_hooks"), {})
    cursor_hook_bridge_ready = cursor_hooks_audit.get("status") == "ION_CURSOR_HOOK_BRIDGE_READY"

    state = {
        "schema_id": "ion.cursor_hook_state.v1",
        "created_at": _iso_now(),
        "status": "live_session_start_observed" if cursor_hook_bridge_ready else "blocked",
        "state_source": ".cursor/hooks/ion_carrier_session_start.py",
        "hook": "sessionStart",
        "hook_script": ".cursor/hooks/ion_carrier_session_start.py",
        "shell_root": str(shell_root),
        "cursor_hook_bridge_verdict": cursor_hooks_audit.get("status"),
        "cursor_hook_bridge_ready": cursor_hook_bridge_ready,
        "cursor_hook_bridge_findings": cursor_hooks_audit.get("findings", []),
        "host_connection_state": "LIVE_HOOK_EVENT_OBSERVED",
        "live_hook_event_seen": True,
        "continue_exit_code": code_continue,
        "continue_verdict": (continue_result or {}).get("verdict"),
        "active_turn_packet_path": (continue_result or {}).get("active_turn_packet_path"),
        "active_spawn_plan_path": (continue_result or {}).get("active_spawn_plan_path"),
        "task_return_ledger_path": (continue_result or {}).get("task_return_ledger_path"),
        "steward_integration_queue_path": (continue_result or {}).get("steward_integration_queue_path"),
        "spawn_queue_count": len((continue_result or {}).get("spawn_queue", [])) if isinstance((continue_result or {}).get("spawn_queue"), list) else 0,
        "audits": audits,
        "production_authority": False,
        "live_execution_authority": False,
    }
    state_path = shell_root / HOOK_STATE_RELATIVE_PATH
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit_lines: list[str] = []
    for audit in audits:
        findings = audit.get("findings")
        finding_count = len(findings) if isinstance(findings, list) else "?"
        audit_lines.append(f"- `{audit['label']}` → `{audit['status']}`; findings: `{finding_count}`")

    ctx = f"""
## ION — Cursor carrier hook mounted

You are the **ION Cursor Carrier-Control Surface**. You are not STEWARD, RELAY, PERSONA, MASON, VIZIER, NEMESIS, or any other ION role.

The sessionStart hook already ran the unified carrier entrypoint:

```bash
PYTHONPATH=ION/04_packages python3 -m kernel.ion_carrier_continue --ion-root . --carrier cursor --operator-message "continue" --json
```

### Current carrier verdict

- verdict: `{(continue_result or {}).get('verdict', 'unavailable')}`
- objective: `{(continue_result or {}).get('objective', 'unavailable')}`
- active turn packet: `{(continue_result or {}).get('active_turn_packet_path', 'unavailable')}`
- active spawn plan: `{(continue_result or {}).get('active_spawn_plan_path', 'unavailable')}`
- hook state: `{HOOK_STATE_RELATIVE_PATH}`

### Spawn queue

{chr(10).join(_spawn_lines(continue_result))}

### Audits

{chr(10).join(audit_lines)}

### Mandatory carrier behavior

1. Open `ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json` before answering any continuation request.
2. Execute only `spawn=true` rows in index order, using each generated `context_package_path`.
3. Save each Cursor Task return and run `kernel.ion_carrier_task_return` before Steward integration.
4. Do not ask the operator which ION role to spawn when the turn packet already provides the queue.
5. Do not collapse the parent chat into STEWARD. STEWARD receives only proof-gated accepted returns.
""".strip()

    sys.stdout.write(json.dumps({"continue": True, "additional_context": ctx}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
