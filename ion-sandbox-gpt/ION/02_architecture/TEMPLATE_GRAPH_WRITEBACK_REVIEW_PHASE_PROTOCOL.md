# Template Graph Writeback Review Phase Protocol

**Status:** Current-phase proposal protocol  
**Phase:** V9 / Phase 5 of the Evented Template File Graph restoration path  
**Authority posture:** Proposal-before-truth; subordinate to governed write, graph substrate law, and operator/Steward review authority

## Core law

A `TEMPLATE_GRAPH_WRITEBACK_PROPOSAL` is not graph truth. It is an inspectable proposal created from projection-only template-event evidence. Before any later source graph mutation can be considered, the proposal must receive a bounded `LAND`, `HOLD`, or `ESCALATE` review verdict.

The Phase 5 verdict is itself a witness surface. It does not mutate the source graph.

## Verdicts

### LAND

`LAND` accepts the proposal as eligible input for a later bounded graph-commit phase. It does not commit proposed nodes or edges by itself.

A `LAND` verdict requires at least one proposed node or proposed edge. Empty proposals cannot be landed.

### HOLD

`HOLD` preserves the proposal but blocks forward movement until the stated review condition is satisfied. HOLD is appropriate when evidence is insufficient, scope is unclear, or a responsible specialist must inspect the proposal first.

### ESCALATE

`ESCALATE` preserves the proposal as a defect/contradiction surface requiring higher review. ESCALATE is appropriate when the proposal may encode false canon, unsafe authority, stale lineage, or a graph relation that would corrupt downstream context.

## Invariants

1. Phase 5 does not mutate source graph state.
2. Phase 5 does not mutate registries.
3. Phase 5 does not schedule follow-up work directly.
4. Phase 5 does not activate agents.
5. Every verdict requires reviewer identity and reason.
6. LAND only authorizes later bounded graph-commit consideration.
7. HOLD and ESCALATE must preserve the proposal and its reason rather than deleting evidence.

## Runtime surface

Phase 5 is implemented by:

```text
ION/04_packages/kernel/template_graph_writeback_review.py
```

It reads:

```text
ION/05_context/history/template_graph_writeback_proposals/*.template_graph_writeback_proposal.json
```

It writes:

```text
ION/05_context/history/template_graph_writeback_reviews/*.template_graph_writeback_review.json
ION/05_context/history/template_graph_writeback_review_receipts/*.template_graph_writeback_review_receipt.json
```

## Pipeline position

```text
Phase 1: completed template file -> Template Completion Event witness
Phase 2: event witness -> dry-run Template Reaction Selection witness
Phase 3: selected index reaction -> projection-only Template Event Index Projection
Phase 4: projection entry -> proposal-only Template Graph Writeback Proposal
Phase 5: writeback proposal -> LAND/HOLD/ESCALATE Review Verdict
```

The next phase, if ratified, is a bounded graph-commit implementation that can consume only LANDed proposals and still must pass governed-write constraints.
