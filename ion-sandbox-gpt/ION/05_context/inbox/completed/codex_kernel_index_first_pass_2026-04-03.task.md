---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T18:22:00-04:00
from: Sovereign
target: ION/04_packages/kernel/index.py
depends_on: ION/04_packages/kernel/store.py
status: COMPLETE
updated: 2026-04-03T18:12:49-04:00
completed_by: Codex
---

# Mission: Implement the first lawful kernel index slice

## Goal

Build the bounded in-memory index layer that sits on top of the persisted kernel
records so later graph, daemon, and compiler work can query active state without
filesystem rescans.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_store_first_pass.md`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/specs/T05_OpenQuestionSchema.spec.md`
- `SOS-OPUS/04_packages/ion_kernel/index.py`

## Requirements

1. Keep this first pass bounded and machine-facing.
2. Build from the persisted record families already present in the kernel store.
3. Provide the minimum fast query surfaces that later runtime work will obviously need.
4. Export the index surface from the kernel package.
5. Add tests proving both build-from-store and incremental update behavior.

## Deliverables

- new `ION/04_packages/kernel/index.py`
- patched `ION/04_packages/kernel/store.py` only if a small support hook is needed
- patched `ION/04_packages/kernel/__init__.py`
- one or more index tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not pretend the graph layer or gatekeeper layer already exists.
2. Do not turn this into a broad analytics subsystem.
3. Keep provenance explicit if conceptual role passes are completed by Codex in
   sequential-kernel mode.

## Completion Signal

Emit one Codex signal pointing to the kernel index first-pass result.

## Completion Record — 2026-04-03T18:12:49-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded kernel index slice, verified build and incremental updates, and closed the live implementation bundle.
- artifacts:
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_index.py
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_index_first_pass/00_trace.md
- next_action: Build the next kernel surface on top of the store and index floors, likely the first bounded graph slice.
- note: Retired by Codex after full live implementation-loop completion; this does not imply independent multi-chat role review.
