---
type: template
template_name: TEMPLATE_SURFACE_CHANGE
created: 2026-04-12T22:15:00-04:00
status: ACTIVE_CURRENT_PHASE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
---

# TEMPLATE — TEMPLATE SURFACE CHANGE

Use this when creating, updating, restoring, superseding, demoting, or retiring a template surface or binding.

## Required frontmatter

```yaml
---
type: template_surface_change
template: TEMPLATE_SURFACE_CHANGE
created: <ISO timestamp>
status: <ACTIVE|COMPLETE|SUPERSEDED>
target_surface: <path>
change_kind: <CREATE|UPDATE|RESTORE|SUPERSEDE|DEMOTE|RETIRE>
governing_packet: <task, handoff, or route path>
---
```

## Required body sections

```markdown
# Template Surface Change: <title>

## Purpose

## Target Surface

## Change Kind

## Governing Sources

## Historical Search / Provenance

## Downstream Affected Surfaces

## Canon / Provisional Status

## Expected Review or Follow-up
```

## Invariants

1. The target surface must be named explicitly.
2. The change kind must be explicit.
3. Provenance must say whether the change is recovered, restated, or newly introduced.
4. Downstream affected surfaces must be named if role/truename/binding/context behavior changes.
5. Template mutation does not silently ratify final canon.
