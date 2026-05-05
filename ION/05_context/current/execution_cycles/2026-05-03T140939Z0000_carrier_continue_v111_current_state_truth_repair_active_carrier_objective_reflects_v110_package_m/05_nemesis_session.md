---
type: role_session
template: ROLE_SESSION
created: 2026-05-03T10:09:39-04:00
status: PLANNED
workstream: implementation
role: nemesis
objective: V111 current-state truth repair: active carrier objective reflects V110 package mountability, no-silent-deletion preservation, V72 MCP donor reconciliation, and no live or production authority.
source_task: carrier_continue:v111 current-state truth repair: active carrier objective reflects v110 package mountability, no-silent-deletion preservation, v72 mcp donor reconciliation, and no live or production authority.
---

# Role Session: nemesis

## Role

nemesis

## Purpose

audit or verify when the slice becomes release-sensitive

## Source Task / Objective

- objective: V111 current-state truth repair: active carrier objective reflects V110 package mountability, no-silent-deletion preservation, V72 MCP donor reconciliation, and no live or production authority.
- source_task: carrier_continue:v111 current-state truth repair: active carrier objective reflects v110 package mountability, no-silent-deletion preservation, v72 mcp donor reconciliation, and no live or production authority.

## Required Reads

- nemesis.boot: ION/03_registry/boots/NEMESIS.boot.md
- nemesis.private_mini: ION/agents/nemesis/MINI.md [optional]
- nemesis.private_capsule: ION/agents/nemesis/CAPSULE.md [optional]
- nemesis.signals: ION/05_context/signals
- nemesis.projection.MINI.md: ION/MINI.md [optional]
- nemesis.projection.STATUS.md: ION/STATUS.md [optional]
- nemesis.projection.CAPSULE.md: ION/CAPSULE.md [optional]

## Expected Output

- Produce the nemesis pass for the bounded `implementation` objective.
- Preserve provenance explicitly if any cross-role judgment is made.
- Update only the artifacts that the governing task or lane actually permits.

## Next Target

- next_role: none

## Notes

- This is a generated sequential-kernel session scaffold, not a claim that the role pass already happened.
