---
type: role_session
template: ROLE_SESSION
created: 2026-05-02T18:54:41-04:00
status: PLANNED
workstream: implementation
role: mason
objective: V106 runtime floor repair: package root integrity, core telemetry triad, cursor hook state projection
next_role: vice
---

# Role Session: mason

## Role

mason

## Purpose

execute the bounded implementation slice

## Source Task / Objective

- objective: V106 runtime floor repair: package root integrity, core telemetry triad, cursor hook state projection

## Required Reads

- mason.boot: ION/03_registry/boots/MASON.boot.md
- mason.private_mini: ION/agents/mason/MINI.md [optional]
- mason.private_capsule: ION/agents/mason/CAPSULE.md [optional]
- mason.inbox: ION/05_context/inbox/mason_* [optional]
- mason.signals: ION/05_context/signals
- mason.projection.MINI.md: ION/MINI.md [optional]
- mason.projection.STATUS.md: ION/STATUS.md [optional]
- mason.projection.CAPSULE.md: ION/CAPSULE.md [optional]

## Expected Output

- Produce the mason pass for the bounded `implementation` objective.
- Preserve provenance explicitly if any cross-role judgment is made.
- Update only the artifacts that the governing task or lane actually permits.

## Next Target

- next_role: vice

## Notes

- This is a generated sequential-kernel session scaffold, not a claim that the role pass already happened.
