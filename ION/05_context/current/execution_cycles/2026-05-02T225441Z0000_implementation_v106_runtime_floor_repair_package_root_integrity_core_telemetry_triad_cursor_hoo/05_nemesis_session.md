---
type: role_session
template: ROLE_SESSION
created: 2026-05-02T18:54:41-04:00
status: PLANNED
workstream: implementation
role: nemesis
objective: V106 runtime floor repair: package root integrity, core telemetry triad, cursor hook state projection
---

# Role Session: nemesis

## Role

nemesis

## Purpose

audit or verify when the slice becomes release-sensitive

## Source Task / Objective

- objective: V106 runtime floor repair: package root integrity, core telemetry triad, cursor hook state projection

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
