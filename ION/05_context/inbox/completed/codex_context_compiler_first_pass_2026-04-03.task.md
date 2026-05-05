---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T18:48:00-04:00
from: Sovereign
target: ION/04_packages/kernel/context_compiler.py
depends_on: ION/04_packages/kernel/graph.py
status: COMPLETE
updated: 2026-04-03T18:25:38-04:00
completed_by: Codex
---

# Mission: Implement the first lawful context compiler helper

## Goal

Build the bounded compiler helper that turns a `WorkUnit` plus explicit inputs into a
real `ContextPackage`, using the active typed/store/index/graph stack where it helps,
without pretending the full daemon compiler pipeline already exists.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/graph.py`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_graph_first_pass.md`
- `SOS-OPUS/04_packages/cognitive/src/context_compiler.py`

## Requirements

1. Keep this first pass explicit and bounded.
2. Compile a real `ContextPackage` with deterministic `context_version` and token
   budget handling.
3. Follow the spec's drop order: tier 5 first, then tier 4, then mission payload if
   still necessary, never doctrine or target.
4. Provide one convenience path that can use the current index/graph stack to resolve
   related open questions for a work unit.
5. Export the compiler surface from the kernel package.
6. Add tests proving compilation, dropping order, and stack-assisted resolution.

## Deliverables

- new `ION/04_packages/kernel/context_compiler.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more compiler tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim full daemon orchestration exists.
2. Do not read arbitrary filesystem state inside the helper.
3. Keep provenance explicit if conceptual role passes are completed by Codex in
   sequential-kernel mode.

## Completion Signal

Emit one Codex signal pointing to the compiler first-pass result.

## Completion Record — 2026-04-03T18:25:38-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded context compiler helper, verified drop-order and stack-assisted question resolution, and closed the live implementation bundle.
- artifacts:
  - ION/04_packages/kernel/context_compiler.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_context_compiler.py
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_context_compiler_first_pass/00_trace.md
- next_action: Build the next kernel/runtime helper on top of the typed/store/index/graph/compiler stack.
- note: Retired by Codex after full live implementation-loop completion; this does not imply independent multi-chat role review.
