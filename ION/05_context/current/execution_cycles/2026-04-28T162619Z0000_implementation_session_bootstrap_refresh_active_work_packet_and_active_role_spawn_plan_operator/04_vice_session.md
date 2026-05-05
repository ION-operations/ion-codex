---
type: role_session
template: ROLE_SESSION
created: 2026-04-28T12:26:19-04:00
status: PLANNED
workstream: implementation
role: vice
objective: session bootstrap — refresh ACTIVE_WORK_PACKET and ACTIVE_ROLE_SPAWN_PLAN; operator states bounded objective on first substantive turn
next_role: nemesis
---

# Role Session: vice

## Role

vice

## Purpose

apply risk pressure if the slice affects continuity or governance

## Source Task / Objective

- objective: session bootstrap — refresh ACTIVE_WORK_PACKET and ACTIVE_ROLE_SPAWN_PLAN; operator states bounded objective on first substantive turn

## Required Reads

- vice.boot: ION/03_registry/boots/VICE.boot.md
- vice.private_mini: ION/agents/vice/MINI.md
- vice.private_capsule: ION/agents/vice/CAPSULE.md
- vice.signals: ION/05_context/signals
- vice.projection.MINI.md: ION/MINI.md [optional]
- vice.projection.STATUS.md: ION/STATUS.md [optional]
- vice.projection.CAPSULE.md: ION/CAPSULE.md [optional]

## Expected Output

- Produce the vice pass for the bounded `implementation` objective.
- Preserve provenance explicitly if any cross-role judgment is made.
- Update only the artifacts that the governing task or lane actually permits.

## Next Target

- next_role: nemesis

## Notes

- This is a generated sequential-kernel session scaffold, not a claim that the role pass already happened.
