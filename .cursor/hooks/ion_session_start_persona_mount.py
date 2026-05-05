#!/usr/bin/env python3
"""sessionStart hook: carrier mount — ACTIVE_WORK_PACKET + ACTIVE_ROLE_SPAWN_PLAN (kernel CLI).

Injects procedural context only (no role-play). Aligns with ION-native mount
authority and .cursor/rules/ion-carrier-runtime-foundation.mdc.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

_SESSION_OBJECTIVE = (
    "session bootstrap — refresh ACTIVE_WORK_PACKET and ACTIVE_ROLE_SPAWN_PLAN; "
    "operator states bounded objective on first substantive turn"
)


def _shell_roots_from_hook_input(data: dict) -> list[Path]:
    roots: list[Path] = []
    for key in ("workspace_roots", "workspaceRoots", "roots", "folders"):
        val = data.get(key)
        if isinstance(val, list):
            for item in val:
                if isinstance(item, str) and item.strip():
                    roots.append(Path(item).resolve())
                elif isinstance(item, dict) and "path" in item:
                    roots.append(Path(str(item["path"])).resolve())
    here = Path(__file__).resolve()
    roots.append(here.parents[2])
    cwd = Path.cwd().resolve()
    if cwd not in roots:
        roots.append(cwd)
    return roots


def _resolve_ion_shell_root(candidates: list[Path]) -> Path | None:
    for base in candidates:
        for p in (base, *base.parents):
            if (p / "ION" / "REPO_AUTHORITY.md").is_file() and (p / "pyproject.toml").is_file():
                return p
    return None


def _run_json_module(
    shell_root: Path,
    module: str,
    args: list[str],
) -> tuple[str | None, dict | None]:
    env = {**os.environ, "PYTHONPATH": str(shell_root / "ION" / "04_packages")}
    cmd = [sys.executable, "-m", module, *args]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(shell_root),
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"(subprocess failed: {exc})", None
    raw = (proc.stdout or "").strip()
    if proc.returncode != 0 and not raw:
        return f"(exit {proc.returncode}: {(proc.stderr or '')[:800]!s})", None
    if not raw:
        return "(no stdout)", None
    try:
        return None, json.loads(raw)
    except json.JSONDecodeError:
        return raw[:12000], None


def _packet_slim(packet: dict) -> dict:
    rs = packet.get("route_source") if isinstance(packet.get("route_source"), dict) else {}
    return {
        "packet_type": packet.get("packet_type"),
        "schema_version": packet.get("schema_version"),
        "objective": packet.get("objective"),
        "mode": packet.get("mode"),
        "role_phase_sequence": packet.get("role_phase_sequence"),
        "route_source": {
            "kind": rs.get("kind"),
            "workstream": rs.get("workstream"),
            "required_surfaces_ok": rs.get("required_surfaces_ok"),
        },
        "active_template": packet.get("active_template"),
        "next_lawful_action": packet.get("next_lawful_action"),
        "production_authority": packet.get("production_authority"),
        "live_execution_authority": packet.get("live_execution_authority"),
    }


def _spawn_schedule_lines(plan: dict) -> list[str]:
    lines: list[str] = []
    roles = plan.get("role_spawn_plan")
    if not isinstance(roles, list):
        return ["(no role_spawn_plan in cycle payload)"]
    for item in roles:
        if not isinstance(item, dict):
            continue
        if not item.get("spawn"):
            continue
        idx = item.get("index")
        role = item.get("role")
        path = item.get("session_packet_path")
        lines.append(f"- **{idx}. {role}** (spawn=true) → `{path}`")
    if not lines:
        lines.append("(no spawn=true rows — check plan validity / spawn_policy)")
    return lines


def main() -> int:
    data = json.loads(sys.stdin.read() or "{}")
    session_blob = json.dumps(data, separators=(",", ":"), ensure_ascii=False)

    shell_root = _resolve_ion_shell_root(_shell_roots_from_hook_input(data))
    if shell_root is None:
        onboard_block = (
            "**ION shell root not found** from hook paths (need `pyproject.toml` + "
            "`ION/REPO_AUTHORITY.md`). Open this repo as the Cursor workspace root."
        )
        cycle_block = ""
        schedule_block = ""
    else:
        ion_arg = str(shell_root / "ION")
        err_o, onboard = _run_json_module(
            shell_root,
            "kernel.ion_carrier_onboard",
            [
                "--ion-root",
                ion_arg,
                "--carrier",
                "cursor",
                "--objective",
                _SESSION_OBJECTIVE,
                "--write-current",
                "--json",
            ],
        )
        if err_o is not None:
            onboard_block = f"Shell root: `{shell_root}`\n\n```text\n{err_o}\n```"
            cycle_block = "(skipped: onboard did not return JSON)"
            schedule_block = ""
        else:
            assert onboard is not None
            packet = onboard.get("packet") if isinstance(onboard.get("packet"), dict) else {}
            slim = _packet_slim(packet)
            onboard_block = (
                f"Shell root: `{shell_root}`\n\n"
                f"- **onboard valid**: `{onboard.get('valid')}`\n"
                f"- **ACTIVE_WORK_PACKET.json** updated.\n\n"
                f"```json\n{json.dumps(slim, indent=2, ensure_ascii=False)}\n```"
            )
            if onboard.get("findings"):
                onboard_block += (
                    "\n\nfindings:\n"
                    + "\n".join(f"- `{f}`" for f in onboard["findings"] if isinstance(f, str))
                )

            err_c, cycle = _run_json_module(
                shell_root,
                "kernel.ion_cycle_runner",
                [
                    "--ion-root",
                    ion_arg,
                    "--carrier",
                    "cursor",
                    "--workstream",
                    "implementation",
                    "--objective",
                    _SESSION_OBJECTIVE,
                    "--spawn-policy",
                    "required",
                    "--write-current",
                    "--json",
                ],
            )
            if err_c is not None:
                cycle_block = f"```text\n{err_c}\n```"
                schedule_block = ""
            elif cycle is not None:
                plan = cycle.get("plan") if isinstance(cycle.get("plan"), dict) else {}
                cycle_block = (
                    f"- **cycle valid**: `{cycle.get('valid')}`\n"
                    f"- **verdict**: `{cycle.get('verdict')}`\n"
                    f"- **ACTIVE_ROLE_SPAWN_PLAN.json** written.\n"
                    f"- **execution_bundle_root**: `{plan.get('execution_bundle_root')}`\n"
                )
                if cycle.get("findings"):
                    cycle_block += (
                        "\nfindings:\n"
                        + "\n".join(f"- `{f}`" for f in cycle["findings"] if isinstance(f, str))
                    )
                schedule_block = "\n".join(_spawn_schedule_lines(plan))
            else:
                cycle_block = ""
                schedule_block = ""

    ctx = f"""
## ION — carrier session mount (hook; procedural)

**Do not** role-play STEWARD / RELAY / PERSONA to the human. Use plain technical language.

### Lawful carrier cycle (must follow)

1. **Onboard:** `kernel.ion_carrier_onboard` → `ION/05_context/current/ACTIVE_WORK_PACKET.json`
2. **Plan:** `kernel.ion_cycle_runner` → `ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json`
3. **Execute:** only `role_spawn_plan` rows with **`spawn: true`** (do not spawn roles from chat habit).
4. **Evidence:** proposals / test output; integration target in packet is **STEWARD**; visible report **RELAY** (labels, not voices).

Read **ION/REPO_AUTHORITY.md** and **ION/02_architecture/ION_MOUNT_CONTRACT.md**.

### This session — kernel refresh (objective: session bootstrap)

{onboard_block}

{cycle_block}

### Spawn schedule (execute in index order; spawn=true only)

{schedule_block or "(not available)"}

### Mandatory reads

- `ION/REPO_AUTHORITY.md`
- `ION/02_architecture/ION_MOUNT_CONTRACT.md`
- selected carrier profile under `ION/03_registry/`
- selected carrier execution packet template under `ION/07_templates/carriers/`
- active packet or spawn-row context package under `ION/05_context/current/`

### Session hook payload (informational)

{session_blob}
""".strip()

    sys.stdout.write(json.dumps({"continue": True, "additional_context": ctx}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
