---
type: architecture_note
authority: A3_OPERATIONAL
created: 2026-04-12T14:24:48-04:00
status: ACTIVE
canon_status: NOT_FINAL_CANON
purpose: Clarify the current-phase relationship between the canonical five-family packet floor and the governed bridge packet set now used in live branch proof flows
connections:
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md
  - ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md
  - ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md
  - ION/03_registry/current_phase_template_surface_registry.yaml
  - ION/07_templates/README.md
  - ION/07_templates/_MASTER.md
---

# Bridge Packet Status Clarification

## Current branch posture

The current branch keeps the canonical packet floor at the five families defined in
`PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`:

- `task`
- `role_session`
- `handoff`
- `cursor_handoff`
- `manual_automation_fallback`

That floor remains the only packet family set claimed as canonical and supported by the
current packet validator.

## Active current-phase bridge packet set

The live branch also uses these governed current-phase bridge packet types:

- `role_chassis_mount`
- `disagreement_escalation`
- `external_return`

Those three packet types are active and lawful when carried under their own current-phase
bridge surfaces:

- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`
- `ION/07_templates/actions/ROLE_CHASSIS_MOUNT.md`
- `ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md`
- `ION/07_templates/actions/DISAGREEMENT_ESCALATION.md`
- `ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md`
- `ION/07_templates/actions/EXTERNAL_RETURN.md`

They remain:

- `CURRENT_PHASE`
- `PROVISIONAL_BRIDGE`
- `NOT_FINAL_CANON`

They are therefore governed packet surfaces, but they are not yet canonical packet
families.

## Validator reading rule

`python -m kernel packet validate ...` currently checks only the canonical five-family
floor.

So for `role_chassis_mount`, `disagreement_escalation`, or `external_return`:

- `UNSUPPORTED_TYPE` means outside the narrow canonical validator floor
- it does **not** by itself mean the packet is unlawful
- it does **not** silently promote the packet to canonical status either

Bridge packets must instead be judged by their governing bridge protocol, template, and
provenance surfaces.

## Startup reading rule

Fresh sessions should read this boundary in the following order:

1. `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
2. `ION/02_architecture/BRIDGE_PACKET_STATUS_CLARIFICATION.md`
3. the specific bridge protocol/template/provenance triple for the packet type present

That keeps the branch from collapsing "validated canonical packet" and "lawful current-
phase bridge packet" into the same category.

## Future widening rule

If the branch later decides to widen canonical packet law or packet-validator coverage,
that must be a separate explicit law decision.

Phase 1 proof usage of bridge packets did not itself ratify packet-family widening.
