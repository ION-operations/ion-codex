---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T19:25:30-04:00
from: Sovereign
target: ION/04_packages/kernel/scheduler.py
depends_on: ION/04_packages/kernel/graph.py
status: COMPLETE
updated: 2026-04-03T19:48:00-04:00
completed_by: Codex
---

# Mission: Implement the first lawful kernel scheduler helper

## Goal

Build the bounded scheduler helper that can inspect persisted/indexed/graphed kernel
state and determine which work units are dispatchable next, without pretending the full
daemon dispatcher already exists.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/graph.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_graph_first_pass.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Use the current `WorkUnit`, `OpenQuestion`, `KernelIndex`, and `KernelGraph` surfaces
   rather than inventing a separate queue model.
3. Determine dispatchable work units from existing status, dependency, priority, and
   blocking-question semantics.
4. Provide a stable ordering for ready work units.
5. Export the scheduler surface from the kernel package.
6. Add tests proving readiness, dependency blocking, question blocking, status gating,
   and queue ordering.

## Deliverables

- new `ION/04_packages/kernel/scheduler.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more scheduler tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim the full daemon scheduler/dispatcher exists.
2. Do not mutate store state from inside the helper.
3. Keep provenance explicit if the pass is completed by Codex under its own `CODE`
   binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the scheduler first-pass result.

## Completion Record — 2026-04-03T19:48:00-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded kernel scheduler helper, exported it through the kernel package, verified dispatchability semantics and queue ordering, and completed the pass under Codex's `CODE` binding.
- artifacts:
  - ION/04_packages/kernel/scheduler.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_scheduler.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_scheduler_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_SCHEDULER_FIRST_PASS_20260403T1948.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_scheduler_first_pass/00_trace.md
- next_action: Build the dispatch helper on top of the new scheduler or route a real support-agent cycle against scheduler semantics.
- note: Completed by Codex under the explicit `CODEX__CODE` binding; this does not imply independent support-role review.
