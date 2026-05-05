# Activation/lifecycle bounded thaw adjacent-edit plan

## Purpose

This note records the exact adjacency-edit categories allowed by the Pass 48 bounded thaw packet.

These are **not** implementation edits.
They are the only adjacent review moves that may be considered if thaw review begins.

## Allowed amendment categories

### 1. Root startup visibility
Files:
- `ION/README.md`
- `ION/STATUS.md`
- `ION/SYSTEM_MAP.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`

Allowed changes:
- add read-order visibility for the new pair once and only if thaw review closes
- state the pair as coupled active-law surfaces
- point to the historical review packet chain as non-canonical support evidence

### 2. Scheduler boundary clarification
File:
- `ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`

Allowed changes:
- clarify that scheduling does not itself authorize enactment
- cross-reference activation authority as the enactment crossing surface

### 3. Capability boundary clarification
File:
- `ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md`

Allowed changes:
- clarify that capability sufficiency is an input to activation decision, not a substitute for it
- cross-reference lifecycle only for post-crossing executor constraints

### 4. Packet / handoff boundary clarification
Files:
- `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- `ION/02_architecture/HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md`

Allowed changes:
- clarify that packet and handoff legality do not themselves confer enactment authority
- cross-reference activation and lifecycle as separate from packet normalization

### 5. Continuation boundary clarification
File:
- `ION/02_architecture/CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md`

Allowed changes:
- clarify that continuation preserves lawful thread identity after crossing
- clarify that continuation may not retroactively stand in for a missing activation decision

### 6. Settlement boundary clarification
File:
- `ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md`

Allowed changes:
- clarify that settlement records closure/deferment/escalation outcomes
- clarify that settlement may not rewrite prior activation lawfulness

## Forbidden amendment categories

The Pass 48 thaw packet does **not** authorize:
- broad protocol rewrites
- concept renaming outside the pair
- widening into runtime/session/API law
- widening into meta-template restoration
- direct mutation of worked examples into active law
