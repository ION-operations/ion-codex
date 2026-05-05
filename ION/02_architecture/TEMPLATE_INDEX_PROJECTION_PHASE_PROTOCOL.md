---
title: Template Index Projection Phase Protocol
status: PROPOSED_RESTORATION_SURFACE
authority_class: A3_OPERATIONAL_PROPOSAL
phase: PHASE_3_PROJECTION_ONLY_INDEX_UPDATE
root_law: EVENTED_TEMPLATE_FILE_GRAPH
---

# Template Index Projection Phase Protocol

## Claim

Phase 3 of the Evented Template File Graph converts dry-run reaction-selection witnesses into a separate projection-only index surface. This phase makes evented template files visible to operator/index consumers without mutating source graph truth, source files, registries, schedules, or agent activation state.

## Boundary

A Phase 3 projection may:

- read `template_reaction_selection_witnesses`;
- materialize projection-safe `index_update` reactions as projection entries;
- defer non-projection reactions with explicit reasons;
- emit a projection surface and receipt.

A Phase 3 projection may not:

- write source context graph nodes;
- write source context graph edges;
- mutate registries;
- schedule follow-up work;
- activate agents or subagents;
- treat projection as kernel truth.

## Lifecycle

```text
Template Completion Event witness
→ Template Reaction Selection witness
→ projection-safe index entries
→ deferred non-projection reactions
→ Template Index Projection receipt
```

## Safety Law

Projection is visibility, not authority. A projection surface can tell ION what a completed template file appears to imply; it cannot by itself land graph mutations or downstream work.
