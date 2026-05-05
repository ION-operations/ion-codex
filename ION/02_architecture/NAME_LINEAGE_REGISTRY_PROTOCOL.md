---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-23T18:30:00-04:00
status: ACTIVE_CURRENT_PHASE
connections:
  - ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md
  - ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md
  - ION/03_registry/name_lineage_registry.yaml
  - ION/03_registry/semantic_identities/README.md
---

# NAME LINEAGE REGISTRY PROTOCOL

## Purpose

Define one current-phase registry surface for governed naming continuity so older names
remain legible without silently steering live execution.

## Core law

1. Old names remain visible as lineage evidence.
2. Old names do not remain active authority by default.
3. Live execution must resolve names through a governed registry rather than through
   ad hoc string cleanup.
4. Historical witness and active authority are different layers.

## Required record powers

Each identity record should be able to answer:

- what the current true name is,
- which older names remain valid as lineage,
- whether an older name is ingress-acceptable,
- whether an older name may auto-normalize to current truth,
- whether an older name requires explicit correction instead of silent routing,
- and what successor or candidate successors exist when direct auto-routing is not lawful.

## Minimum fields

- `entity_id`
- `entity_kind`
- `current_true_name`
- `aliases`
- `alias_status`
- `relation_type`
- `accepted_for_ingress`
- `historical_only`
- `live_decision`
- `warning_code`
- `successor_candidates`
- `governing_sources`

## Relation classes

This first pass recognizes a few bounded relation types:

- `SELF`
- `DISPLAY_ALIAS_TO_CURRENT_TRUE_NAME`
- `RETIRED_ROLE_AND_CARRIER_WITNESS`
- `HISTORICAL_ALIAS_NO_AUTO_ROUTE`

The branch may later add burden-transfer, split-successor, and merge-successor relations,
but those are not required for this first operational slice.

## Current-phase registry surface

The live name-lineage authority for the active root is:

- `ION/03_registry/name_lineage_registry.yaml`

This registry does not replace semantic identity records.
It adds alias lifecycle, ingress posture, and retirement posture that semantic identity
records alone do not yet model.
