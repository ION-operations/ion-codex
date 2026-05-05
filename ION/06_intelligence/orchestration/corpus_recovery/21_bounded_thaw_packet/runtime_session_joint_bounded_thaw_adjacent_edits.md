# Runtime/session bounded thaw adjacent-edit plan

## Purpose

This note records the exact adjacency-edit categories allowed by the Pass 61
bounded thaw packet.

These are **not** implementation edits.
They are the only adjacent review moves that may be considered if thaw review
begins.

## Allowed amendment categories

### 1. Root startup visibility
Files:
- `ION/README.md`
- `ION/STATUS.md`
- `ION/SYSTEM_MAP.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`

Allowed changes:
- add read-order visibility for the runtime/session trio once and only if thaw
  review closes
- state the trio as a coupled active-law set
- point to the historical review packet chain as non-canonical support evidence

### 2. Scheduler boundary clarification
File:
- `ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`

Allowed changes:
- clarify that scheduling does not own session identity, queue ownership, or
  API entry law
- cross-reference the runtime/session trio as the bounded center beneath
  scheduling

### 3. Runtime-state witness boundary clarification
Files:
- `ION/02_architecture/RUNTIME_STATE_BINDING_PROTOCOL.md`
- `ION/02_architecture/RUNTIME_STATE_QUERY_PROTOCOL.md`
- `ION/02_architecture/RUNTIME_STATE_REPORTING_PROTOCOL.md`

Allowed changes:
- clarify that runtime-state witness and reporting surfaces do not replace
  runtime/session authority
- cross-reference the runtime/session trio as the center whose state they may
  witness

### 4. Shell boundary clarification
Files:
- `ION/02_architecture/SUPERVISED_DAEMON_SERVICE_PROTOCOL.md`
- `ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`
- `ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md`

Allowed changes:
- clarify that shells and entry surfaces operationalize carrier invocation
  without becoming the runtime/session center
- cross-reference API runtime entry only as bounded attachment law

### 5. Activation boundary clarification
File:
- `ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md`

Allowed changes:
- clarify that queue readiness and API entry do not silently answer activation
  law
- cross-reference activation as an adjacent authority rather than a runtime
  session substitute

### 6. Continuation and settlement boundary clarification
Files:
- `ION/02_architecture/CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md`
- `ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md`

Allowed changes:
- clarify that continuation may preserve lawful thread identity without
  replacing session persistence
- clarify that settlement may classify closure without rewriting session
  authority or queue history

## Forbidden amendment categories

The Pass 61 thaw packet does **not** authorize:
- broad protocol rewrites
- concept renaming outside the trio
- widening into daemon controller or transport-stack restoration
- widening into meta-template restoration
- direct mutation of review artifacts into active law
