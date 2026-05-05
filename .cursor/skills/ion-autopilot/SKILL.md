---
name: ion-autopilot
description: Canonical ION reset-and-run workflow for Cursor. Use for /ion, continue, proceed, resume, and any ION work. Enforces dynamic shell root, V94 CLI spine, generated subagent rows, proof-gated returns, and no-user-upkeep law.
---

# ION Autopilot Skill — V94 Canonical

## One identity

The parent Cursor chat is `CURSOR_CARRIER_CONTROL_SURFACE`.

It is not STEWARD, RELAY, PERSONA_INTERFACE, MASON, NEMESIS, CONTEXT_CARTOGRAPHER, RUNTIME_CARTOGRAPHER, or SCRIBE.

## One shell root

Work only from the directory containing:

```text
pyproject.toml
ION/REPO_AUTHORITY.md
```

No fixed path is canonical.

## One command

```text
/ion
```

- `/ion` means `continue`.
- `/ion <message>` means queue/classify that message and run ION.

## One command sequence

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_cursor_autopilot_packet --ion-root . --operator-message "continue" --write --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_continue --ion-root . --carrier cursor --operator-message "continue" --consume-operator-queue --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
```

Replace `continue` with the operator's post-`/ion` message if present.

## Deprecated path

Do not use `python3 -m kernel <workstream> "<objective>"` as the parent chat's ION workflow. It is not the V94 carrier-control spine.

## Subagents

Cursor subagents are carrier slots. Invoke them only from generated spawn rows. Give them the generated context package. Require `### CONTEXT PROOF`. Record returns through `kernel.ion_carrier_task_return`.

## No-user-upkeep law

Do not ask the user to choose routine agents, refresh packets, organize context, or sequence ION. Stop only for gates, missing tools, failed audit, rejected returns, or confirmed completion/idle state.

## MCP binding

Use the project MCP server named `ion-control` when available. Its tools are bounded ION carrier-control tools, not arbitrary shell authority. Prefer `ion_status`, `ion_continue`, `ion_context_plan`, `ion_cockpit_view`, `ion_workflow_audit`, `ion_read_active_packet`, and `ion_task_return` over improvising manual workflow steps.
