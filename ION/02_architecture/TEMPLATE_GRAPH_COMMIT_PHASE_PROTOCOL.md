# Template Graph Commit Phase Protocol

**Authority status:** Current-phase implementation protocol, Phase 6 of the Evented Template File Graph restoration.

## Core claim

A LANDed `TEMPLATE_GRAPH_WRITEBACK_PROPOSAL` may become bounded graph truth only through an explicit graph commit phase. The commit phase writes accepted nodes and edges to a dedicated evented-template graph-state surface and emits receipts. It does not mutate source files, registries, schedules, or agent activation state.

## Pipeline position

1. Template Completion Event witness.
2. Template Reaction Selection witness.
3. Template Event Index Projection.
4. Template Graph Writeback Proposal.
5. LAND / HOLD / ESCALATE review verdict.
6. **Bounded Template Graph Commit.**

## Commit eligibility

A proposal is eligible only when:

- a Phase 5 review exists;
- the review verdict is `LAND`;
- `accepted_for_later_graph_commit` is true;
- the proposal ID in the review matches the proposal file;
- proposed nodes or edges are non-empty;
- source graph mutation remained blocked in prior phases.

## Write surface

Committed graph state is written only under:

```text
ION/05_context/graph/template_event_graph_state/
  nodes/
  edges/
```

Commit records and receipts are written under:

```text
ION/05_context/history/template_graph_commits/
ION/05_context/history/template_graph_commit_receipts/
```

## Non-mutation boundary

Phase 6 still does not:

- rewrite source documents;
- mutate live registries;
- mutate schedules;
- activate agents;
- collapse deferred reactions into completed work.

It commits only the accepted evented-template graph nodes and edges.
