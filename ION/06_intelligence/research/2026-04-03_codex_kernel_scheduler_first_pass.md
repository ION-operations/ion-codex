---
type: research
from: Codex
created: 2026-04-03T19:48:00-04:00
status: COMPLETE
topic: First lawful kernel scheduler slice
connections:
  - ION/04_packages/kernel/scheduler.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_scheduler.py
  - ION/05_context/inbox/completed/codex_kernel_scheduler_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_scheduler_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md
---

# Codex Kernel Scheduler First Pass

## Why this exists

The kernel stack now had typed records, durable persistence, a query index, a causal
graph, and a context compiler, but it still had no bounded answer to a core daemon-side
question: which work units are dispatchable next?

This pass adds that first scheduler helper without pretending the full daemon dispatcher
already exists.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/graph.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_scheduler.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/scheduler.py` now provides the first bounded scheduler helper
  for the active kernel stack.
- The helper introduces:
  `KernelScheduler`, `IonScheduler`, `KernelSchedulerError`, `ScheduleReason`, and
  `WorkUnitDispatchAssessment`.
- The scheduler uses existing kernel semantics rather than inventing a parallel queue
  model:
  `WorkUnit.status`, `WorkUnit.dependencies`, `OpenQuestion.blocking`, `KernelIndex`,
  and `KernelGraph`.
- Dispatchability is currently defined narrowly and explicitly:
  a work unit must be `PENDING`, all dependencies must be in ready statuses
  (first pass: `COMMITTED`), and no blocking open questions may remain in blocking
  statuses (first pass: `OPEN` or `ASSIGNED`).
- The helper provides:
  per-work-unit assessment, sorted all-work assessment, a stable dispatchable queue, and
  a `next_dispatchable()` convenience path.
- Queue ordering is deterministic:
  priority first, then `created_at`, then `work_unit_id`.
- `ION/04_packages/kernel/__init__.py` now exports the scheduler surface.
- `ION/tests/test_kernel_scheduler.py` proves readiness, dependency blocking, open
  question blocking, non-pending status gating, queue ordering, and next-item selection.
- The combined suite is now at **46 passing tests**.

## Boundary

- This is not the full daemon scheduler.
- It does not compile work units from task files.
- It does not mutate store state or advance status automatically.
- It does not perform dispatch, spawn, or gatekeeper validation.

## Implications

- The kernel stack now has its first truthful scheduling surface on top of the
  typed/store/index/graph/compiler floor.
- The next runtime helper can build on a real dispatchability model rather than ad hoc
  scans.
- This pass also served as the first real build use of the new `CODEX__CODE` binding:
  the task and result were explicitly bounded as Codex implementation work rather than
  smuggling broader authority through a code patch.

## Recommended next moves

- Build the first dispatch helper on top of the scheduler.
- Or route a real support-agent cycle around this new surface:
  Mason-bound implementation refinement, Thoth research on scheduling policy, or Nemesis
  audit of scheduler semantics.
