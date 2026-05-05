# TEMPLATE GRAPH WRITEBACK PROPOSAL PHASE PROTOCOL

## Status

`CURRENT_PHASE / PROPOSAL_ONLY / NOT_SOURCE_GRAPH_MUTATION`

This protocol defines Phase 4 of the Evented Template File Graph operationalization.

## Core law

A projection-only template event index entry may be translated into proposed graph
nodes and edges, but it must not become source graph truth until a later governed
write / landing pass accepts it.

## Phase 4 lifecycle

```text
Template Event Index Projection
→ Template Graph Writeback Proposal
→ Proposal Receipt
→ later LAND / HOLD / ESCALATE decision
```

## Allowed in Phase 4

- read Phase 3 projection-only index surfaces
- derive proposed context graph nodes
- derive proposed context graph edges
- preserve deferred reactions as blocked evidence
- emit proposal files
- emit proposal receipts

## Forbidden in Phase 4

- source graph mutation
- registry mutation
- schedule mutation
- source file mutation
- agent activation
- treating proposal records as truth

## Required invariant

Every proposed graph node and edge must carry `PROPOSED_NOT_MUTATED` posture.
Every non-proposal reaction must remain `DEFERRED_NOT_MUTATED`.
