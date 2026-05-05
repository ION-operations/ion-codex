---
type: research
from: Codex
created: 2026-04-04T13:35:00-04:00
status: COMPLETE
topic: Reviewer-facing answer queues, planner-manifest lifecycle, and daemon-side manifest compilation
connections:
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/question_answers.py
  - ION/04_packages/kernel/planner_gate.py
  - ION/04_packages/kernel/daemon.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/daemon_loop.py
  - ION/tests/test_kernel_question_answers.py
  - ION/tests/test_kernel_planner_gate.py
  - ION/tests/test_kernel_daemon.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/05_context/inbox/completed/codex_kernel_reviewer_queue_and_planner_lifecycle_first_pass_2026-04-04.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_reviewer_queue_and_planner_lifecycle_first_pass/00_trace.md
  - ION/06_intelligence/research/2026-04-04_codex_kernel_answer_record_and_planner_manifest_runtime_first_pass.md
---

# Codex Kernel Reviewer Queue + Planner Lifecycle First Pass

## Why this exists

Codex MINI left two runtime questions explicitly next:

- should persisted `question_answer` records gain reviewer-facing queue/projection surfaces beyond per-question lookup?
- should `planner_manifest` gain explicit cancellation / supersession / expiry behavior plus daemon-side compilation from resolved follow-up pressure before any broader retry compiler lands?

This pass answers both in the affirmative and lands the smallest honest kernel slices that
follow from those decisions.

## Findings

- `ION/04_packages/kernel/question_answers.py` now includes a narrow projection builder:
  - recent answer projections join one persisted `question_answer` record back to its linked `OpenQuestion` and parent `WorkUnit`
  - reviewer-facing queues now expose both pending review/follow-up pressure and recent answer history without pretending those queues are the authority surface
- `ION/04_packages/kernel/model.py` and `ION/04_packages/kernel/planner_gate.py` now widen planner manifests with explicit lifecycle behavior:
  - `CANCELLED`
  - `SUPERSEDED`
  - `EXPIRED`
  - explicit status reason / change timestamps
  - optional expiry deadlines
- `ION/04_packages/kernel/planner_gate.py` now discovers compilable resolved follow-up/review pressure and can compile `READY` planner manifests directly from that pressure without yet claiming a general retry compiler.
- `ION/04_packages/kernel/daemon.py` now surfaces `COMPILE_PLANNER_MANIFEST` as its own bounded daemon action.
- `ION/04_packages/kernel/daemon_actions.py` now executes that compile step, and `ION/04_packages/kernel/daemon_loop.py` now witnesses compiled manifest ids in loop telemetry.
- direct child issuance from raw pressure-linked deltas is now skipped when a planner-manifest compile step is required, so resolved pressure must pass through manifest state before child issuance.

## Boundary

- This is not a full reviewer runtime.
- It is not a broad retry compiler.
- Answer queues are index-backed projections, not durable rendered artifacts yet.
- Planner-manifest expiry is explicit/opt-in rather than inferred from doctrine or host time.
- The daemon can compile manifests from resolved pressure, but it does not yet run a general manifest-maintenance sweep or richer retry topology compiler.

## Implications

- reviewer-facing answer history now has a truthful browse surface without collapsing the answer record family back into question mutation only
- planner manifests now have explicit lifecycle state instead of behaving like one-shot ready/executed markers only
- the daemon’s workflow is now cleaner:
  - resolved pressure
  - compile planner manifest
  - consume ready planner manifest
  - issue child work
- signal authority remains bounded: signals still create or resolve pressure; they do not issue child work themselves

## Verification

- focused reviewer/planner/daemon tests pass
- full kernel suite result: **142 passed, 3 subtests passed**

## Recommended next moves

- decide whether reviewer-facing answer queues should become durable generated-state projections on disk rather than only index-backed views
- decide whether due-expiry and stale-cancellation for planner manifests should become daemon-maintained housekeeping before any broader retry compiler lands
- only after that, consider richer manifest topology or broader retry compilation
