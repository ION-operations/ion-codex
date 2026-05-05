---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-23T18:36:00-04:00
status: ACTIVE_CURRENT_PHASE
connections:
  - ION/02_architecture/STALE_NAME_DETECTION_PROTOCOL.md
  - ION/02_architecture/TEMPLATE_SURFACE_EVOLUTION_PROTOCOL.md
  - ION/07_templates/actions/TASK.md
  - ION/07_templates/actions/ROLE_SESSION.md
---

# ACTIVE SURFACE RETIREMENT PROTOCOL

## Purpose

Retire stale names from live control surfaces without erasing lineage.

## Retirement meaning

Retirement means removal from:

- active defaults,
- active packet templates,
- operator-facing defaults,
- live roster/controller summaries,
- and runtime entry surfaces.

Retirement does **not** mean deletion from:

- lineage registries,
- replay traces,
- witness packets,
- migration notes,
- or historical semantic records.

## Bounded workflow

1. detect stale-name usage in active surfaces,
2. classify whether the name is auto-normalizable or requires explicit correction,
3. patch active defaults first,
4. patch template and protocol surfaces second,
5. leave lineage and historical witness surfaces intact,
6. emit one visible witness of what was retired from control.

## Current-phase clarification

`Codex` is the clearest first-pass retirement case:

- preserve it as lineage and historical carrier witness,
- do not leave it as an active default authority name,
- and do not silently reconstitute it as a live specialist role.
