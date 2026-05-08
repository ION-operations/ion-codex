---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T18:10:00-04:00
from: Sovereign
target: ION/04_packages/kernel/store.py
depends_on: ION/04_packages/kernel/model.py
status: COMPLETE
updated: 2026-04-03T18:07:37-04:00
completed_by: Codex
---

# Mission: Implement the first lawful kernel store slice

## Goal

Create a bounded persistence layer for the active kernel objects so the new model
types can be stored on disk and reloaded without reopening the old full ion kernel.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_model_first_pass.md`
- `SOS-OPUS/04_packages/ion_kernel/store.py`

## Requirements

1. Keep this first pass machine-facing and bounded.
2. Persist the current kernel record types to disk with deterministic paths and
   round-trippable serialization.
3. Support the minimum CRUD/query surface needed for later index/compiler work.
4. Export the store surface from the kernel package.
5. Add tests proving the store works on real temp directories.

## Deliverables

- new `ION/04_packages/kernel/store.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more store tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not pretend the old full markdown-ion store has already been ported.
2. Do not couple this first pass to daemon scheduling or gatekeeper logic.
3. Keep provenance explicit if conceptual role passes are completed by Codex in
   sequential-kernel mode.

## Completion Signal

Emit one Codex signal pointing to the kernel store first-pass result.

## Completion Record — 2026-04-03T18:07:37-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded kernel store slice, verified round-trip persistence, and closed the live implementation bundle.
- artifacts:
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_store.py
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_store_first_pass/00_trace.md
- next_action: Build the next kernel surface on top of durable records, likely the index or a minimal compiler helper.
- note: Retired by Codex after full live implementation-loop completion; this does not imply independent multi-chat role review.
