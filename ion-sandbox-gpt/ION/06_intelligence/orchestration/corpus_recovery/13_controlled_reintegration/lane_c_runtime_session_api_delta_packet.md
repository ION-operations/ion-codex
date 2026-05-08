# Lane C — Runtime / session / API delta packet

## Purpose

Open the third lawful Era 2 reintegration packet by making the restoration delta between the historical runtime/session/API center and the current branch runtime-state + supervised-service center explicit.

This packet is a **compare/recover/reintegration** surface.
It does **not** authorize active implementation rewrite.

## Control declaration

- Question class: runtime/session/API
- Primary historical center: `ION - Production/ION-BUILD/src/ion/entry/api.py`
- Historical runtime/session support: `ION - Production/ION-BUILD/tools/ion-cli/runtime_sessions.py` and `ION - Production/ION-BUILD/tests/test_runtime_sessions.py`
- Historical scheduler/runtime witnesses: `ION - Production/ION-BUILD/context/13_cognitive/benchmarks/2026-03-28_223748_phase8c_session_queue_smoke_v1.md`, `ION - Production/ION-BUILD/context/13_cognitive/benchmarks/2026-03-28_225217_phase8c_scheduler_tick_smoke_v1.md`, and `ION - Production/ION-BUILD/tools/ion-cli/test_api_swarm.py`
- Primary current centers: `ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`, `ION/02_architecture/RUNTIME_STATE_BINDING_PROTOCOL.md`, `ION/02_architecture/RUNTIME_STATE_QUERY_PROTOCOL.md`, `ION/02_architecture/RUNTIME_STATE_REPORTING_PROTOCOL.md`, and `ION/02_architecture/SUPERVISED_DAEMON_SERVICE_PROTOCOL.md`
- Current runtime-chain supports: `ION/02_architecture/SCHEDULE_DISPATCH_AND_ASSIGNMENT_RECONCILIATION_PROTOCOL.md`, `ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`, `ION/04_packages/kernel/scheduler.py`, `ION/04_packages/kernel/runtime_state_sync.py`, `ION/04_packages/kernel/runtime_state_views.py`, and `ION/04_packages/kernel/operator_cli.py`
- Default posture: compare centers, recover first, keep active law stable
- Answer / output class: reintegration delta packet
- Landing boundary: atlas/evidence only

## Why Lane C follows Lane B

Lane B restored the distinction between activation authority and scheduler / entry / handoff law.
Lane C now restores the distinction between a **truthful runtime-state witness/query layer** and a first-class **runtime/session/API center**.

The recovery program already judged that `ION-BUILD` preserved the strongest runtime/session/API center, while the current branch is stronger on governed kernel truth, bounded service surfaces, runtime-state honesty, and explicit report/provenance discipline.
That means the next lawful move is not to port the old HTTP runtime shell wholesale.
It is to make the split explicit so the current line stops implying that scheduler + runtime-state views + supervised daemon surfaces already equal a full session runtime organism.

## Horizon framing

### Completion for this packet
This packet is complete when the repo contains:
- an explicit runtime/session/API delta matrix,
- a candidate transition map for future current-line restoration,
- and an explicit statement of what must **not** change yet.

### Widening condition
Widen only after operator review of whether the current line truly needs a first-class runtime/session/API center, rather than only stronger wording around state binding, service harnesses, or scheduler surfaces.

### Return condition
Return to recovery-only posture if deeper evidence shows that the historical `ION-BUILD` runtime center was too chassis-bound or too API-first to restore lawfully into the current one-workflow kernel without major distortion.

## Recovered comparison

### 1. What the historical center governs
The historical center governs **runtime sessions as persistent executable service objects**.
It explicitly owns session creation, queue persistence, runnable-vs-blocked inspection, timed/sequential drain behavior, scheduler ticks over queued work, and API entry for external clients.

### 2. What the current center governs
The current branch governs **truthful bounded runtime posture inside the kernel**.
It is strongest on machine-readable route / automation-state binding, bounded runtime-state queries, runtime-report generation, future-work scheduling, supervised daemon/service invocation, and governed dispatch / return paths.

### 3. What the historical center adds that the current branch does not yet carry fully
The historical center carries:
- explicit persisted session identity,
- per-session queue state and prompt artifacts,
- timed / sequential queue semantics,
- session-local dispatch and inspection behavior,
- runtime tick execution over queued work,
- and a direct API-facing runtime surface.

### 4. What the current branch adds that should not be discarded
The current branch adds:
- stronger separation between kernel truth and service artifacts,
- explicit runtime-state honesty for route and automation posture,
- governed dispatch / execution return boundaries,
- capability-aware carrier and scheduler reasoning,
- stronger runtime reporting and provenance surfaces,
- and clearer anti-autonomy safeguards around daemon and external execution service layers.

## Delta judgment

The restoration target is **not** a rollback to the historical HTTP/runtime shell alone.
The restoration target is a current-line runtime/session center that regains historical session/runtime seriousness **while preserving** the current branch's truth-separation, bounded-service, and kernel-authority discipline.

That yields the following governing judgment:

1. `LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md` should remain the future-work compilation center, not silently absorb per-session queue runtime control.
2. `RUNTIME_STATE_BINDING_PROTOCOL.md`, `RUNTIME_STATE_QUERY_PROTOCOL.md`, and `RUNTIME_STATE_REPORTING_PROTOCOL.md` should remain machine-readable witness/query/reporting surfaces, not the whole explanation of a runtime/session organism.
3. `SUPERVISED_DAEMON_SERVICE_PROTOCOL.md` should remain a truthful service harness, not the whole explanation of API/runtime authority.
4. A future current-line restoration should introduce a first-class runtime/session authority surface, a session queue / dispatch surface, and an API runtime-entry surface.
5. This pass does not create or ratify those active-law surfaces yet.

## Lawful restoration target

The current line likely needs **three distinct layers** instead of one diffused implication chain:

### Layer A — Runtime session authority
A current-line surface that states what a runtime session is, what state persists, and how session identity relates to kernel truth, continuation, and carrier-specific service shells.

### Layer B — Session queue and dispatch lifecycle
A current-line surface that states how session-local queued work becomes runnable, blocked, drained, retried, cancelled, or completed under lawful dispatch boundaries.

### Layer C — API runtime entry and supervised service surface
A current-line surface that states how external/API clients lawfully create, inspect, and drive runtime sessions without collapsing kernel truth into a web-service facade.

This split preserves the best of both centers.

## Non-lawful moves for this packet

Do **not** do any of the following in this pass:
- import `ION-BUILD` runtime session or API code wholesale into active current law,
- treat scheduler-tick or session-queue witnesses as proof that the current branch already has a restored runtime/session center,
- mutate the current scheduler or runtime-state protocols so they rhetorically absorb session-runtime responsibilities,
- or claim that supervised daemon / external execution service wrappers already solve the runtime/session/API center.

## Candidate follow-up surfaces

See:
- `lane_c_runtime_session_api_delta_matrix.csv`
- `lane_c_runtime_session_api_transition_candidates.md`

## Pass result

Lane C is now opened as an explicit controlled-reintegration packet rather than an implicit runtime aspiration.
