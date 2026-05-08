---
type: research
from: Codex
created: 2026-04-04T14:45:00-04:00
status: COMPLETE
topic: Durable reviewer-queue projections and daemon-maintained planner-manifest housekeeping
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
  - ION/05_context/inbox/completed/codex_kernel_queue_projection_and_planner_housekeeping_first_pass_2026-04-04.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_queue_projection_and_planner_housekeeping_first_pass/00_trace.md
  - ION/06_intelligence/research/2026-04-04_codex_kernel_reviewer_queue_and_planner_lifecycle_first_pass.md
---

# Codex Kernel Queue Projection + Planner Housekeeping First Pass

## Why this exists

Codex MINI left two explicit runtime questions next:

- should reviewer-facing answer queues become durable generated-state projections rather than remaining index-only views?
- should planner-manifest expiry/cancellation gain daemon-maintained housekeeping before any broader retry compiler lands?

This pass answers both in the affirmative and lands the smallest honest kernel slices that
follow from those decisions.

## Findings

- `ION/04_packages/kernel/model.py`, `store.py`, `index.py`, and `graph.py` now carry a first-class `reviewer_answer_queue` record family so reviewer-facing queue views can be persisted as generated-state runtime witness.
- `ION/04_packages/kernel/question_answers.py` now builds, persists, and reconstructs durable reviewer-queue projections without pretending those projections are the source authority surface.
- The graph now witnesses reviewer-queue projections through explicit edges to queued pending questions and projected recent answer records.
- `ION/04_packages/kernel/planner_gate.py` now discovers explicit planner-manifest maintenance candidates and can maintain one manifest at a time through bounded expiry/cancellation updates.
- `ION/04_packages/kernel/daemon.py` now surfaces `MAINTAIN_PLANNER_MANIFEST` as its own lawful action ahead of child issuance when due-expiry or stale-cancellation applies.
- `ION/04_packages/kernel/daemon_actions.py` now executes that maintenance step, and `ION/04_packages/kernel/daemon_loop.py` now witnesses maintained manifest ids/statuses in loop telemetry.

## Boundary

- This is not a full reviewer queue daemon.
- It is not a batch refresh scheduler yet.
- It is not a broad retry compiler or rich planner topology engine.
- Planner-manifest maintenance stays one bounded manifest at a time.
- Reviewer-queue projections remain generated-state witness, not governing continuity.

## Implications

- reviewer-facing queue views now have durable runtime witness records that can be inspected without recomputing the queue purely from the index every time
- generated-state witness is now more explicit across the active runtime lane: loop receipts, answer records, queue projections, and planner manifests all have durable surfaced state
- daemon workflow is now safer around manifest deadlines because expired/stale ready manifests can be maintained before the daemon tries to issue child work from them

## Verification

- focused queue/planner/daemon tests pass
- full kernel suite result: **143 passed, 3 subtests passed**

## Recommended next moves

- decide whether durable reviewer-queue projections should gain batch refresh helpers or daemon-maintained refresh scheduling
- decide whether planner-manifest housekeeping should emit its own sweep receipts or remain step-local until richer topology is warranted
- only after that, consider broader retry compilation or richer manifest topology
