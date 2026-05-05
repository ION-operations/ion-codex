---
type: template_surface_change
template: TEMPLATE_SURFACE_CHANGE
created: 2026-04-12T22:30:00-04:00
status: COMPLETE
target_surface: ION/07_templates/bindings/STEWARD__TASK.md
change_kind: CREATE
governing_packet: ION/05_context/comms/kernel_router_runs/2026-04-12_steward_truename_and_template_alignment/00_trace.md
---

# Template Surface Change: Steward orchestration bindings

## Purpose
Create direct current-phase orchestration bindings for the settled truename.

## Target Surface
`ION/07_templates/bindings/STEWARD__TASK.md` and companion Steward bindings.

## Change Kind
CREATE

## Governing Sources
- `ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md`
- `ION/02_architecture/TEMPLATE_SURFACE_EVOLUTION_PROTOCOL.md`
- `ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md`

## Historical Search / Provenance
The live branch already carried Codex orchestration bindings. This change restores a more correct current-phase role/truename expression without deleting compatibility/supporting carrier bindings.

## Downstream Affected Surfaces
- current-phase orchestration domain
- startup/status/read-order docs
- current-phase template surface registry

## Canon / Provisional Status
Current-phase, not final canon.

## Expected Review or Follow-up
Update orchestration maps and startup surfaces to prefer Steward when naming current-phase role truth.
