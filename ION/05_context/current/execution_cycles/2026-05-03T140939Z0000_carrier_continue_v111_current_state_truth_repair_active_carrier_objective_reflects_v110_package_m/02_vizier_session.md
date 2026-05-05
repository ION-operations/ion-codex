---
type: role_session
template: ROLE_SESSION
created: 2026-05-03T10:09:39-04:00
status: PLANNED
workstream: implementation
role: vizier
objective: V111 current-state truth repair: active carrier objective reflects V110 package mountability, no-silent-deletion preservation, V72 MCP donor reconciliation, and no live or production authority.
source_task: carrier_continue:v111 current-state truth repair: active carrier objective reflects v110 package mountability, no-silent-deletion preservation, v72 mcp donor reconciliation, and no live or production authority.
next_role: mason
---

# Role Session: vizier

## Role

vizier

## Purpose

define scope, dependencies, and required review posture

## Source Task / Objective

- objective: V111 current-state truth repair: active carrier objective reflects V110 package mountability, no-silent-deletion preservation, V72 MCP donor reconciliation, and no live or production authority.
- source_task: carrier_continue:v111 current-state truth repair: active carrier objective reflects v110 package mountability, no-silent-deletion preservation, v72 mcp donor reconciliation, and no live or production authority.

## Required Reads

- vizier.boot: ION/03_registry/boots/VIZIER.boot.md
- vizier.private_mini: ION/agents/vizier/MINI.md [optional]
- vizier.private_capsule: ION/agents/vizier/CAPSULE.md [optional]
- vizier.inbox: ION/05_context/inbox/vizier* [optional]
- vizier.signals: ION/05_context/signals
- vizier.projection.MINI.md: ION/MINI.md [optional]
- vizier.projection.STATUS.md: ION/STATUS.md [optional]
- vizier.projection.CAPSULE.md: ION/CAPSULE.md [optional]

## Expected Output

- Produce the vizier pass for the bounded `implementation` objective.
- Preserve provenance explicitly if any cross-role judgment is made.
- Update only the artifacts that the governing task or lane actually permits.

## Next Target

- next_role: mason

## Notes

- This is a generated sequential-kernel session scaffold, not a claim that the role pass already happened.
