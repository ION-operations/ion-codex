---
type: clarification
authority: A3_OPERATIONAL
created: 2026-04-22T20:25:00-04:00
status: ACTIVE
purpose: Refine rank classes for the promoted current-phase support roles Relay and Vestige
connections:
  - ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md
  - ION/03_registry/agent_roster_registry.yaml
  - ION/03_registry/semantic_identities/RELAY.semantic.yaml
  - ION/03_registry/semantic_identities/VESTIGE.semantic.yaml
  - ION/06_intelligence/orchestration/2026-04-22_current_phase_agent_roster_settlement_packet.md
  - ION/06_intelligence/orchestration/2026-04-22_relay_semantic_promotion_review_note.md
  - ION/06_intelligence/orchestration/2026-04-22_vestige_semantic_promotion_review_note.md
---

# Promoted Support-Role Rank Refinement Note

## Purpose

Close one remaining inconsistency in the current-phase roster settlement:

- `Relay` and `Vestige` now have semantic identities, domain truth, and explicit current-phase role law
- but both still carry the placeholder rank label `UNSETTLED_CURRENT_PHASE__SUPPORT_ROLE`

That placeholder was acceptable while the roles were still under promotion review.
It is no longer the clearest truthful label after promotion has already landed.

## Current judgment

The branch now has enough evidence to refine the promoted support-role rank classes as follows:

### `Relay` → `BOUNDED_INTENT_RELAY`

This class names:

- user-facing relay burden
- packet and digest courier work
- faithful preservation of sovereign/user intent
- explicit non-upgrade into orchestration, ratification, or command

Why this is better than the placeholder:

- it preserves the role’s boundedness
- it identifies Relay as a courier/interface burden rather than a generic helper
- it avoids collapsing Relay into `Steward` or treating it as hidden governance

### `Vestige` → `STANDING_ARCHAEOLOGY_DAEMON`

This class names:

- persistent excavation
- stale-authority and lineage-drift watch
- contradiction surfacing
- evidence-bound archaeology without adjudicative power

Why this is better than the placeholder:

- it reflects the branch’s actual protocol language
- it preserves the standing nature of the burden
- it distinguishes archaeology from generic research, audit, or architecture work

## Boundary conditions

This refinement does **not** mean:

- Relay gains orchestration truth or release authority
- Vestige gains audit verdict power or architectural authority
- every remaining boot-plus-mount specialist now needs a custom rank class

This is a narrow settlement for the already promoted persistent support roles only.

## Operational consequence

The active branch should now update:

- `ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md`
- `ION/03_registry/agent_roster_registry.yaml`
- `ION/03_registry/semantic_identities/RELAY.semantic.yaml`
- `ION/03_registry/semantic_identities/VESTIGE.semantic.yaml`

to use the refined classes:

- `BOUNDED_INTENT_RELAY`
- `STANDING_ARCHAEOLOGY_DAEMON`

## Final judgment

Promoted current-phase support roles should no longer be left under the generic label `UNSETTLED_CURRENT_PHASE__SUPPORT_ROLE`.

For the active branch, the truthful refined current-phase rank classes are:

- `Relay` → `BOUNDED_INTENT_RELAY`
- `Vestige` → `STANDING_ARCHAEOLOGY_DAEMON`
