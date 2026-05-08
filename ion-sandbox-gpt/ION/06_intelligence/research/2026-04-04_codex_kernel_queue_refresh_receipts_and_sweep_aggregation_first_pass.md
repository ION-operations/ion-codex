---
type: research
from: Codex
created: 2026-04-04T17:25:00-04:00
status: COMPLETE
topic: Reviewer-queue refresh receipts plus retained planner-sweep aggregation
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
  - ION/05_context/inbox/completed/codex_kernel_queue_refresh_receipts_and_sweep_aggregation_first_pass_2026-04-04.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_queue_refresh_receipts_and_sweep_aggregation_first_pass/00_trace.md
  - ION/06_intelligence/research/2026-04-04_codex_kernel_queue_refresh_and_planner_sweep_first_pass.md
---

# Codex Kernel Queue Refresh Receipts + Sweep Aggregation First Pass

## Why this exists

Codex MINI left two generated-state witness questions still open after the queue-refresh /
planner-sweep pass:

- should reviewer-queue refresh emit durable receipts/topology or remain projection-only?
- should retained planner-manifest sweep receipts gain bounded aggregation helpers before any richer retry compiler is attempted?

This pass answers both in the affirmative and lands the smallest truthful kernel slices that
follow from those decisions.

## Findings

- `ION/04_packages/kernel/question_answers.py` now emits a durable `reviewer_queue_refresh` receipt family when bounded stale queue sweeps are executed.
- `ION/04_packages/kernel/model.py`, `store.py`, `index.py`, and `graph.py` now carry first-class `reviewer_queue_refresh` and `planner_manifest_sweep_aggregate` witness families.
- The graph now witnesses queue-refresh receipts through explicit edges into refreshed reviewer-queue projections.
- `ION/04_packages/kernel/planner_gate.py` now keeps a bounded retained window of sweep receipts and can aggregate them into one durable summary record with status/reason counts plus retained receipt ids.
- `ION/04_packages/kernel/daemon.py` now surfaces `SWEEP_REVIEWER_QUEUES` when more than one stale reviewer queue exists and `AGGREGATE_PLANNER_SWEEP_RECEIPTS` when retained sweep receipts outpace their current aggregate witness.
- `ION/04_packages/kernel/daemon_actions.py` now executes both new witness-maintenance paths and returns explicit result provenance instead of burying them in step-local mutation.
- `ION/04_packages/kernel/daemon_loop.py` now records queue-refresh receipt ids and planner-sweep aggregate ids in per-step loop telemetry.

## Boundary

- This is not a broader reviewer runtime.
- It is not a retry compiler.
- Queue-refresh receipts remain generated-state witness over existing reviewer-queue projections.
- Sweep aggregation remains a bounded retained-window summary; it does not prune or replace the underlying sweep receipts.

## Implications

- reviewer-facing queue maintenance is now more inspectable because refresh sweeps leave durable receipt/topology witness
- planner housekeeping now has a retained aggregate surface that can summarize recent sweep pressure before richer retry compilation exists
- the generated-state runtime witness lane is now more explicit across loop receipts, queue-refresh receipts, reviewer queues, planner sweeps, and planner-sweep aggregates

## Verification

- focused queue/planner/daemon tests pass
- full kernel suite result: **156 passed, 3 subtests passed**

## Recommended next moves

- decide whether reviewer-queue refresh receipts need their own bounded retained aggregation window
- decide whether planner-sweep aggregates should gain daemon-maintained refresh / retention policy before richer retry-compiler work lands
- only after that, decide whether a broader retry-compiler/runtime can lawfully consume these witness families
