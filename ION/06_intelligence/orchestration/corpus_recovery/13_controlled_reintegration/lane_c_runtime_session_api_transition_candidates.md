# Lane C — Runtime / session / API transition candidates

## Purpose

Name the smallest future current-line surfaces that would restore the historical runtime/session/API center without discarding the current branch truth-separation, governed-dispatch, and supervised-service protections.

This is a candidate map only.
It is **not** an implementation pass.

## Candidate surface set

### 1. `ION/02_architecture/RUNTIME_SESSION_AUTHORITY_PROTOCOL.md`
Role:
- define runtime session identity as a first-class current-line function,
- state what session state persists and how it differs from kernel doctrine/truth,
- and clarify the relation between session continuity, work-unit continuity, and carrier/service shells.

### 2. `ION/02_architecture/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md`
Role:
- define lawful per-session queue semantics,
- restore runnable / blocked / timed / dependency-aware drain behavior,
- and bind session queue execution to the existing governed dispatch and return path.

### 3. `ION/02_architecture/API_RUNTIME_ENTRY_PROTOCOL.md`
Role:
- define the supervised API-facing runtime surface,
- clarify how external clients create, inspect, and drive sessions without becoming kernel authority,
- and bind any future HTTP/service shell to the same one-workflow and supervision law as CLI and daemon carriers.

### 4. Keep `ION/02_architecture/RUNTIME_STATE_BINDING_PROTOCOL.md`, `ION/02_architecture/RUNTIME_STATE_QUERY_PROTOCOL.md`, and `ION/02_architecture/RUNTIME_STATE_REPORTING_PROTOCOL.md`
Role:
- preserve machine-readable runtime posture as bounded witness/query/reporting substrate,
- prevent session restoration from collapsing route-state and automation-state into vague runtime prose.

### 5. Keep `ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`, `ION/02_architecture/SUPERVISED_DAEMON_SERVICE_PROTOCOL.md`, and `ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`
Role:
- preserve the distinction between project scheduling, supervised service harnesses, and external execution boundaries,
- ensure a restored runtime/session center remains adjacent to these surfaces rather than replacing them.

## Intended future relation

The future current line should likely read as:

1. `RUNTIME_SESSION_AUTHORITY_PROTOCOL.md` answers **what a runtime session is** and what state persists.
2. `SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md` answers **how session-local queued work becomes runnable, blocked, drained, or retired**.
3. `API_RUNTIME_ENTRY_PROTOCOL.md` answers **how external/API clients lawfully create and interact with runtime sessions**.
4. The runtime-state protocols answer **how kernel posture becomes machine-readable bounded runtime state**.
5. `LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md` answers **how project work is compiled and ordered**, not how session queues are serviced.
6. `SUPERVISED_DAEMON_SERVICE_PROTOCOL.md` and `EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md` answer **how carrier-specific service shells stay supervised**.

## Why this split is safer

It prevents two opposite mistakes:
- mistaking current runtime-state honesty and service harnesses for full runtime/session restoration,
- and mistaking historical session-runtime vividness for sufficient lawful current integration.

## Lawful next step after review

If this candidate map is accepted, the next bounded move should be a **surface-design packet** for `RUNTIME_SESSION_AUTHORITY_PROTOCOL.md`, `SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md`, and `API_RUNTIME_ENTRY_PROTOCOL.md`, still landing in draft / proposal space before active-law adoption.
