---
name: ion-carrier-control
description: ION Cursor carrier-control hook and command workflow. Use when Cursor session starts, /ion or /ion-continue runs, or hook state is degraded.
---

# ION Carrier Control Skill

The parent Cursor chat is the ION Cursor Carrier-Control Surface, not STEWARD, RELAY, PERSONA_INTERFACE, MASON, or any other ION role.

## Hook bridge

The session hook is configured in `.cursor/hooks.json` with `sessionStart` pointing to `.cursor/hooks/ion_carrier_session_start.py`.

The hook writes or refreshes `ION/05_context/current/ACTIVE_CURSOR_HOOK_STATE.json` and should run the carrier-control preparation path.

## Required behavior

1. Resolve shell root as the directory containing `pyproject.toml` and `ION/REPO_AUTHORITY.md`.
2. Run `/ion` or `/ion-continue` through the carrier-control command path.
3. Use active packets, not chat memory.
4. Use generated spawn rows and context bundles.
5. Require `### CONTEXT PROOF` on Task returns.
6. Route returns through `kernel.ion_carrier_task_return`.

If the hook state is missing, stale, or degraded, report it through status/audit and continue through the explicit command path when safe.
