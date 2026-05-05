---
type: research
from: Codex
created: 2026-04-04T16:05:00-04:00
status: COMPLETE
topic: Daemon-maintained reviewer-queue refresh plus planner-manifest sweep receipts/topology
connections:
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/graph.py
  - ION/04_packages/kernel/question_answers.py
  - ION/04_packages/kernel/planner_gate.py
  - ION/04_packages/kernel/daemon.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/daemon_loop.py
  - ION/tests/test_kernel_question_answers.py
  - ION/tests/test_kernel_planner_gate.py
  - ION/tests/test_kernel_daemon.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/05_context/inbox/completed/codex_kernel_queue_refresh_and_planner_sweep_first_pass_2026-04-04.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_queue_refresh_and_planner_sweep_first_pass/00_trace.md
  - ION/06_intelligence/research/2026-04-04_codex_kernel_queue_projection_and_planner_housekeeping_first_pass.md
---

# Codex Kernel Queue Refresh + Planner Sweep First Pass

## Why this exists

Codex MINI left two explicit generated-state/runtime questions next:

- should durable reviewer-queue projections gain bounded refresh helpers or daemon-maintained refresh scheduling?
- should planner-manifest housekeeping emit broader sweep receipts/topology once the one-manifest maintenance path proved out?

This pass answers both in the affirmative and lands the smallest honest kernel slices that
follow from those decisions.

## Findings

- `ION/04_packages/kernel/question_answers.py` now discovers stale reviewer-queue projections by comparing persisted generated-state witness against the current pending-question / recent-answer surface.
- The same module now supports bounded single-projection refresh plus batch refresh across all stale reviewer queues without claiming a broader reviewer runtime already exists.
- `ION/04_packages/kernel/daemon.py` now surfaces `REFRESH_REVIEWER_QUEUE` as its own lawful generated-state maintenance action and does so only when a persisted queue projection has actually gone stale.
- `ION/04_packages/kernel/daemon_actions.py` now executes that refresh path and returns explicit refresh provenance instead of silently replacing queue witness state.
- `ION/04_packages/kernel/model.py`, `store.py`, `index.py`, and `graph.py` now carry a first-class `planner_manifest_sweep` receipt family so broader manifest housekeeping can be persisted and traversed topologically.
- `ION/04_packages/kernel/planner_gate.py` now supports one bounded maintenance sweep over the currently due planner manifests and persists a receipt witnessing which manifests were maintained and why.
- `ION/04_packages/kernel/daemon.py` now surfaces `SWEEP_PLANNER_MANIFESTS` when more than one manifest needs maintenance at once, while preserving the existing one-manifest maintenance path for singleton cases.
- `ION/04_packages/kernel/daemon_loop.py` now witnesses queue-refresh and planner-sweep activity in loop telemetry.

## Boundary

- This is not a full reviewer daemon or broad reviewer scheduling runtime.
- It is not a rich retry compiler.
- Queue refresh remains generated-state maintenance over existing projection records.
- Planner sweeps remain bounded housekeeping over already-discovered manifest lifecycle pressure.
- The daemon still does not synthesize new child work directly from signals.

## Implications

- persisted reviewer-facing queue witness can now stay in sync with the underlying question/answer state without external manual regeneration every time
- broader planner housekeeping now leaves durable sweep evidence instead of only step-local manifest mutation
- generated-state runtime witness is now more explicit across queue projections, planner manifests, sweep receipts, and daemon-loop receipts/telemetry

## Verification

- focused queue/planner/daemon tests pass
- full kernel suite result: **150 passed, 3 subtests passed**

## Recommended next moves

- decide whether reviewer-queue refresh should emit its own durable refresh receipts/topology or remain projection-only until a broader reviewer runtime exists
- decide whether planner-manifest sweep receipts need retention/aggregation helpers before richer retry compilation is attempted
- only after that, consider broader reviewer-runtime scheduling or retry compiler work
