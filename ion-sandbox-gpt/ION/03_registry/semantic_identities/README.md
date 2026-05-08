---
type: registry_index
authority: A3_OPERATIONAL
created: 2026-04-07T22:24:00-04:00
updated: 2026-04-22T19:40:00-04:00
status: ACTIVE_FIRST_PASS
topic: Current-phase semantic identity records for governed entities in the live ION root
---

# ION Semantic Identities

These files carry the first explicit semantic layer for governed names in the live `ION/` root.

## Purpose

- preserve stable identifiers
- record structural identity separately from display naming
- preserve historical naming truth where needed
- bind roles into the current active domain lattice
- prevent casual rename drift

The semantic identity layer does not by itself define ingress alias posture or stale-name
retirement. Those now live in:

- `ION/03_registry/name_lineage_registry.yaml`

## Current first-pass records

- `RELAY.semantic.yaml`
- `STEWARD.semantic.yaml`
- `VESTIGE.semantic.yaml`
- `VIZIER.semantic.yaml`
- `VICE.semantic.yaml`
- `NEMESIS.semantic.yaml`

## Historical witness records

- `CODEX.semantic.yaml`

## Current-phase clarification

`STEWARD.semantic.yaml` holds current-phase orchestration truename truth.
`CODEX.semantic.yaml` is now historical witness only and does not define a live current-phase role.
`RELAY.semantic.yaml` now stabilizes the front-door courier surface without expanding it into orchestration or command.
`VESTIGE.semantic.yaml` now stabilizes the archaeology daemon as a real standing role rather than generic support labor.

Current operational orchestration should therefore prefer Steward-facing law when naming
role truth, while describing chassis/carrier truth through mount law rather than through a revived Codex role.
