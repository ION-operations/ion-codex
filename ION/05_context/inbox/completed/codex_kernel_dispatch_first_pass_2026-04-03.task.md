---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T20:07:14-04:00
from: Sovereign
target: ION/04_packages/kernel/dispatch.py
depends_on: ION/04_packages/kernel/scheduler.py
status: COMPLETE
updated: 2026-04-03T20:12:57-04:00
completed_by: Codex
---

# Mission: Implement the first lawful kernel dispatch helper

## Goal

Build the bounded dispatch helper that can take a scheduler-approved work unit,
require a matching compiled context package, emit a durable dispatch packet, and
advance the work unit into `DISPATCHED` state without pretending execution,
validation, or full daemon routing already exist.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/graph.py`
- `ION/04_packages/kernel/context_compiler.py`
- `ION/04_packages/kernel/scheduler.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T07_SignalSchema.spec.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_scheduler_first_pass.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Require scheduler approval rather than inventing a second readiness model.
3. Require a matching `ContextPackage` before dispatch.
4. Advance the persisted `WorkUnit` from `PENDING` to `DISPATCHED`.
5. Emit a durable dispatch packet artifact surface from the helper.
6. Export the dispatch surface from the kernel package.
7. Add focused tests for packet preparation, missing or mismatched context, durable
   packet writing, and persisted status transition.

## Deliverables

- new `ION/04_packages/kernel/dispatch.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more dispatch tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim the full daemon dispatcher exists.
2. Do not automate execution, validation, or signal routing in this pass.
3. Keep provenance explicit if the pass is completed by Codex under its own `CODE`
   binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the dispatch first-pass result.

## Completion Record — 2026-04-03T20:12:57-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded kernel dispatch helper, exported it through the kernel package, verified durable dispatch packets plus persisted DISPATCHED transitions, and closed the pass under Codex's CODE binding.
- artifacts:
  - ION/04_packages/kernel/dispatch.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_dispatch.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_dispatch_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_DISPATCH_FIRST_PASS_20260403T2011.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_dispatch_first_pass/00_trace.md
- next_action: Build the bounded execution helper on top of the new dispatch surface or route one real support-agent cycle through dispatched work.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
