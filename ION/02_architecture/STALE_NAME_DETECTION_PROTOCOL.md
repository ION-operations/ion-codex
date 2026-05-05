---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-23T18:34:00-04:00
status: ACTIVE_CURRENT_PHASE
connections:
  - ION/02_architecture/NAME_LINEAGE_REGISTRY_PROTOCOL.md
  - ION/03_registry/name_lineage_registry.yaml
  - ION/04_packages/kernel/name_lineage.py
---

# STALE NAME DETECTION PROTOCOL

## Purpose

Detect stale governed names in active surfaces before they silently steer runtime truth.

## Severity classes

### `INFO`

Historical or lineage-only usage in replay, witness, or registry-history surfaces.

### `ALERT`

A stale but auto-normalizable alias appears in an active surface.
The branch should patch the active surface to the current true name.

### `BLOCK`

A retired, ambiguous, or no-auto-route name appears in an active control surface.
The branch should not allow that token to remain a default steering surface.

## Active control surfaces in this first pass

- `ION/02_architecture/`
- `ION/04_packages/`
- `ION/07_templates/`
- startup/root summary surfaces explicitly named in the lineage registry

## Non-goal

This first pass is lexical and bounded.
It is meant to open cleanup missions truthfully, not to claim total semantic understanding
of every sentence in the repository.
