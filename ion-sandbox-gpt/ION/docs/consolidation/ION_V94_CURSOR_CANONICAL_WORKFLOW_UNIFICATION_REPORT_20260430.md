# ION V94 — Cursor Canonical Workflow Unification Report

## Summary

V94 repairs the exact Cursor failure exposed by the operator: multiple project surfaces were giving Cursor Auto mode different instructions for shell root, CLI entrypoint, parent-chat identity, and subagent rigor. This made it possible for Cursor to claim it was following ION while running a stale or incomplete workflow.

## Canonical result

The live Cursor workflow is now one story:

```text
/ion
→ dynamic shell root check
→ kernel.ion_cursor_autopilot_packet
→ kernel.ion_carrier_continue
→ ACTIVE_CURSOR_AUTOPILOT_PACKET
→ ACTIVE_CARRIER_TURN_PACKET
→ ACTIVE_ROLE_SPAWN_PLAN
→ generated subagent rows only
→ ### CONTEXT PROOF returns
→ kernel.ion_carrier_task_return
→ ACTIVE_STEWARD_INTEGRATION_QUEUE
```

## Files added or updated

```text
ION/02_architecture/ION_CURSOR_CANONICAL_WORKFLOW_UNIFICATION_PROTOCOL.md
ION/04_packages/kernel/ion_cursor_canonical_workflow_audit.py
ION/tests/test_kernel_ion_cursor_canonical_workflow_audit.py
.cursor/rules/ion-canonical-workflow-unification.mdc
.cursor/rules/ion-carrier-mount.mdc
.cursor/rules/ion-cursor-onboarding.mdc
.cursor/commands/ion.md
.cursor/commands/ion-continue.md
.cursor/commands/ion-health.md
.cursor/skills/ion-autopilot/SKILL.md
.cursor/agents/ion-spawn-row-slot.md
AGENTS.md
START_HERE_FOR_ANY_AGENT.md
ION/05_context/current/PRODUCTIZED_RUNTIME_MANIFEST_V94.json
ION/05_context/signals/v94_cursor_canonical_workflow_unification_receipt_20260430.txt
```

## What changed

### Shell root

Removed fixed workspace-root language as authority. The only canonical root is the directory containing both `pyproject.toml` and `ION/REPO_AUTHORITY.md`.

### CLI

Demoted `python3 -m kernel <workstream> "<objective>"` from parent-chat spine to internal/backward-compatible call only when generated packets explicitly request it.

### `/ion`

Promoted `/ion` as the primary reset-and-run command. `/ion-continue` remains alias-only.

### Parent chat

The Cursor parent chat is `CURSOR_CARRIER_CONTROL_SURFACE`, not Steward or a solo implementer.

### Subagents

Subagents are strict carrier slots. They must receive generated context package content and return `### CONTEXT PROOF`.

## Audit

New audit command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_cursor_canonical_workflow_audit --ion-root . --json
```

Expected status after applying V94:

```text
ION_CURSOR_CANONICAL_WORKFLOW_READY
```
