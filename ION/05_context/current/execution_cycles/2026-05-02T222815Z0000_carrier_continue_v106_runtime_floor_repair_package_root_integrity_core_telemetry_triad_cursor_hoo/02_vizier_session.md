---
type: role_session
template: ROLE_SESSION
created: 2026-05-02T18:28:15-04:00
status: PLANNED
workstream: implementation
role: vizier
objective: V106 runtime floor repair: package root integrity, core telemetry triad, cursor hook state projection
source_task: carrier_continue:v106 runtime floor repair: package root integrity, core telemetry triad, cursor hook state projection
next_role: mason
---

# Role Session: vizier

## Role

vizier

## Purpose

define scope, dependencies, and required review posture

## Source Task / Objective

- objective: V106 runtime floor repair: package root integrity, core telemetry triad, cursor hook state projection
- source_task: carrier_continue:v106 runtime floor repair: package root integrity, core telemetry triad, cursor hook state projection

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
