---
type: research
from: Codex
created: 2026-04-03T20:11:03-04:00
status: COMPLETE
topic: First lawful kernel dispatch slice
connections:
  - ION/04_packages/kernel/dispatch.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_dispatch.py
  - ION/05_context/inbox/codex_kernel_dispatch_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_dispatch_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md
  - ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md
  - ION/06_intelligence/specs/T07_SignalSchema.spec.md
---

# Codex Kernel Dispatch First Pass

## Why this exists

The kernel stack now had enough truthful structure to know which work units are
dispatchable, but it still had no lawful bridge from that scheduling answer into an
actual dispatch transition. The missing piece was small but important: require a
matching compiled context package, materialize a durable dispatch packet, and persist
the `PENDING -> DISPATCHED` state change without pretending the whole daemon loop
already exists.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/graph.py`
- `ION/04_packages/kernel/context_compiler.py`
- `ION/04_packages/kernel/scheduler.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_dispatch.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T07_SignalSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/dispatch.py` now provides the first bounded dispatch helper
  for the active kernel stack.
- The helper introduces:
  `KernelDispatcher`, `IonDispatcher`, `KernelDispatchError`, `DispatchPacket`,
  `DispatchPreparation`, `DispatchResult`, `render_dispatch_packet`, and
  `write_dispatch_packet`.
- The dispatch boundary is narrow and explicit:
  it reuses `KernelScheduler` rather than inventing a second readiness model, requires
  a matching compiled `ContextPackage`, emits a durable packet payload, and persists a
  `WorkUnit` transition from `PENDING` to `DISPATCHED`.
- Context-package validation is real rather than assumed. The helper rejects missing or
  mismatched package identity, protocol, transition, context version, personal name,
  role, and structural identity.
- Durable dispatch packets now include both:
  a machine-readable packet envelope and the compiled context package payload/text
  needed to understand what was dispatched.
- `ION/04_packages/kernel/__init__.py` now exports the dispatch surface through the
  lazy kernel package.
- `ION/tests/test_kernel_dispatch.py` proves:
  packet preparation, non-dispatchable rejection, missing-context rejection,
  context-version mismatch rejection, durable packet writing, persisted status
  transition, and `dispatch_next()` ordering over the scheduler surface.
- The combined kernel suite is now at **52 passing tests**.

## Boundary

- This is not the full daemon dispatcher.
- It does not compile work units from task files.
- It does not execute the dispatched work unit.
- It does not run validation, gatekeeping, or commit logic.
- It does not yet emit or consume canonical machine `Signal` records.

## Implications

- The kernel stack now has a truthful dispatch bridge on top of the
  typed/store/index/graph/compiler/scheduler floor.
- A later execution helper can now build on a real persisted `DISPATCHED` transition
  and a durable packet format instead of open-coded handoff assumptions.
- The first machine-facing runtime story is becoming continuous:
  typed work unit -> compiled context package -> scheduler assessment -> dispatch packet
  -> persisted dispatch state.

## Recommended next moves

- Build the first bounded execution helper on top of the new dispatch surface.
- Or wire the dispatch helper into one real support-role packet so Mason/Thoth/Nemesis
  can operate against explicit dispatch artifacts rather than only task markdown.
