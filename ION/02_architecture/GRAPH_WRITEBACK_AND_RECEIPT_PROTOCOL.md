# GRAPH WRITEBACK AND RECEIPT PROTOCOL

**Status:** Proposed restoration / operationalization protocol  
**Authority posture:** A2 production-governance candidate  
**Created:** 2026-04-24

## 1. Purpose

This protocol defines how event reactions write back into the context graph and how receipt evidence binds each mutation, refusal, warning, or schedule action.

## 2. Writeback classes

- `SOURCE_GRAPH_MUTATION` — creates or modifies source graph node/edge state.
- `PROJECTION_REFRESH` — updates an index, summary, status board, or membrane projection.
- `REACTION_RECEIPT_ONLY` — records refusal, blocked posture, or no-op idempotence.
- `SCHEDULE_OR_QUEUE_PROPOSAL` — emits a schedulable follow-up, not direct execution.
- `AGENT_OR_SUBAGENT_REQUEST` — emits a fan-out request, not automatic live activation.
- `REGISTRY_DELTA_PROPOSAL` — proposes registry change, not direct ratification.

## 3. Receipt requirements

Every writeback must include:

```yaml
receipt_id:
source_event_id:
source_file:
template_id:
reaction_id:
executor_family:
authority_basis:
inputs:
outputs:
writeback_class:
mutated_nodes:
mutated_edges:
projection_updates:
blocked_or_refused_reason:
content_hash_before:
content_hash_after:
created_at:
```

## 4. Mutation law

A graph mutation must cite:

- the source file;
- the template class;
- the Template Completion Event;
- the allowed reaction entry;
- the receipt proving the mutation;
- the authority posture under which the mutation occurred.

## 5. Refusal is first-class

A refused or blocked event is still graph information. It should create evidence that the system saw the event and chose not to act because of a specific lawful reason.

## 6. Projection boundary

A projection refresh may update summaries, indexes, or membranes. It may not declare source truth unless a source graph mutation receipt exists.
