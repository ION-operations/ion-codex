---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-08T23:15:00-04:00
status: ACTIVE
implements:
  - ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md
implemented_by:
  - ION/04_packages/kernel/operator_cli.py
---

# T49 — Operator Entry Surface

## Goal

Expose the preferred supervised runtime and the major workflow carriers through one discoverable CLI/operator surface.

## Required commands

- `status`
- `runtime start|drain|stop`
- `control service-mode|hold-scope|resume-scope`
- `daemon run`
- `replay latest|receipt`
- `child issue-manifest|issue-delta`
- `external export|accept-return`
- `bootstrap init|emit|activate`
- `route`

## Required properties

1. Legacy route invocations remain supported.
2. Workspace root is explicit or discoverable.
3. Store root is explicit or defaults lawfully.
4. JSON output is available for all commands.
5. Commands call the live service modules rather than re-implementing workflow law ad hoc.
6. No command bypasses policy or control gates.

## Acceptance

This spec is satisfied when:
- the operator surface can drive the supervised runtime without direct module imports,
- key commands are covered by focused CLI tests,
- and the root docs point operators to the new entry surface.
