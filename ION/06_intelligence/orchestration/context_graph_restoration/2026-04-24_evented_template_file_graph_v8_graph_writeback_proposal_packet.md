# Evented Template File Graph V8 — Governed Writeback Proposal Packet

## Summary

V8 adds the first proposal-only source graph writeback layer for the Evented
Template File Graph. The system can now transform Phase 3 projection entries
into inspectable proposed graph nodes and edges, without treating them as truth.

## Chain position

```text
Phase 1: Template Completion Event witness
Phase 2: Template Reaction Selection witness
Phase 3: Template Event Index Projection
Phase 4: Template Graph Writeback Proposal
```

## Boundary

V8 is still non-mutating. It only creates proposal records and receipts.

## Next phase

Phase 5 should add a governed LAND / HOLD / ESCALATE review path for accepting
or refusing graph writeback proposals.
