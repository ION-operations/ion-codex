---
type: clarification
authority: A3_OPERATIONAL
created: 2026-04-22T20:45:00-04:00
status: ACTIVE
purpose: Clarify current-phase continuity-home law for promoted lane-native support roles
connections:
  - ION/02_architecture/CONTINUITY_ARCHITECTURE.md
  - ION/03_registry/agent_roster_registry.yaml
  - ION/03_registry/boots/RELAY.boot.md
  - ION/03_registry/boots/VESTIGE.boot.md
  - ION/03_registry/semantic_identities/RELAY.semantic.yaml
  - ION/03_registry/semantic_identities/VESTIGE.semantic.yaml
  - ION/06_intelligence/orchestration/2026-04-22_current_phase_agent_roster_settlement_packet.md
---

# Promoted Lane-Native Support Role Continuity Normalization Note

## Purpose

Close the remaining continuity-home ambiguity for the promoted lane-native support roles:

- `Relay`
- `Vestige`

Both roles now have semantic identity, domain truth, and refined rank classes.
What remained insufficiently explicit was whether promotion should immediately move them
into `ION/agents/{role}/` source continuity.

## Current-phase judgment

For the active branch, promotion does **not** automatically move `Relay` or `Vestige`
into `ION/agents/{role}/`.

Their current source continuity remains:

- `Relay` → `ION/06_intelligence/relay/relay/`
- `Vestige` → `ION/06_intelligence/archaeology/vestige/`

This is not a temporary fiction.
It is current-phase source truth.

## Why this is the right current-phase rule

### 1. The live branch already treats those lanes as source continuity

Both boots already load from the lane-native continuity surfaces directly rather than
from an `ION/agents/{role}/MINI.md` and `CAPSULE.md` pair.

### 2. Parallel source homes would create split-brain risk

Creating `ION/agents/relay/` or `ION/agents/vestige/` now, without an explicit migration,
would create two bad outcomes:

- duplicate source continuity
- quiet uncertainty about which surface actually governs

That is worse than staying lane-native for the current phase.

### 3. The lanes are not only product lanes

For these two roles, the lane directories are already both:

- work-product lanes
- and role-private continuity homes

That is unusual relative to `Vizier`, `Codex`, `Mason`, or `Thoth`, but it is still lawful.

## Current-phase normalization rule

### Rule 1 — lane-native source continuity remains authoritative now

Until an explicit migration packet says otherwise:

- `Relay` source continuity is the relay lane
- `Vestige` source continuity is the archaeology lane

### Rule 2 — no parallel shadow agent-private home

Do **not** create `ION/agents/relay/` or `ION/agents/vestige/` as convenience mirrors,
scratch continuity, or secondary source homes.

If such directories ever appear later, they must not be treated as authoritative until
an explicit migration surface ratifies them.

### Rule 3 — future normalization is allowed, but only by explicit migration

A future normalization may still move a promoted lane-native role into
`ION/agents/{role}/`, but only if a bounded migration packet:

- names the target role
- names the old and new source homes
- states the cutover rule
- states whether the old lane remains a product lane, archive witness, or both
- updates boot, registry, and continuity law together

### Rule 4 — no dual-source phase

The branch should not tolerate an indefinite state where both:

- lane-native continuity
- and `ION/agents/{role}/`

claim to be simultaneous source continuity for the same promoted role.

One may be active source.
The other may be witness, product lane, or post-migration residue.
Not both.

## Operational consequence

For the current phase, the truthful continuity reading is:

- `Relay` is a semantically settled, domainized, ranked role whose source continuity is still lane-native
- `Vestige` is a semantically settled, domainized, ranked role whose source continuity is still lane-native

That is not a defect to hide.
It is the correct current-phase state.

## Final judgment

Promoted lane-native support roles do not need forced `ION/agents/{role}/` normalization right now.

The active branch should instead preserve the stronger rule:

- lane-native source continuity remains authoritative until explicit migration
- no shadow parallel source homes
- any later normalization must be explicit, one-way, and non-dual
