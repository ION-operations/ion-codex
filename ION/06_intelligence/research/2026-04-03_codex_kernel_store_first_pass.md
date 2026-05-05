---
type: research
from: Codex
created: 2026-04-03T18:14:00-04:00
status: COMPLETE
topic: First lawful kernel store slice
connections:
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_store.py
  - ION/05_context/inbox/completed/codex_kernel_store_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_store_first_pass/00_trace.md
  - SOS-OPUS/04_packages/ion_kernel/store.py
---

# Codex Kernel Store First Pass

## Why this exists

The kernel package had a typed record layer but still no durable persistence for those
records. This pass adds the minimum lawful store surface so work units, context
packages, commit deltas, and open questions can be written to disk and loaded back as
typed objects.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_store.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `SOS-OPUS/04_packages/ion_kernel/store.py`

## Findings

- `ION/04_packages/kernel/store.py` now provides a first-pass filesystem-backed store
  for the active machine-facing kernel records:
  `WorkUnit`, `ContextPackage`, `CommitDelta`, and `OpenQuestion`.
- The store writes deterministic JSON envelopes under per-record-family directories,
  reconstructs nested dataclasses and enums on read, and rejects path-escape style
  record IDs.
- The surface is intentionally bounded:
  `create`, `replace`, `read`, `delete`, `exists`, `list_ids`, `list_records`,
  `count`, and `summary`.
- `ION/04_packages/kernel/__init__.py` now exports `KernelStore`,
  `KernelStoreError`, and `IonStore` as a compatibility alias for the current first
  pass.
- `ION/tests/test_kernel_store.py` proves round-trip persistence, overwrite control,
  counting/listing, deletion, and ID sanitization against real temp directories.
- The combined suite is now at twenty-six passing tests across sequential-kernel,
  model, and store surfaces.

## Boundary

- This is not a port of the older markdown-ion document store.
- It does not yet choose a canonical runtime root for persisted kernel state.
- It does not yet implement indexing, graph bonds, gatekeeper logic, or context
  compilation.

## Implications

- The kernel now has both a typed object floor and a durable persistence floor.
- The next implementation step can build on stored kernel records rather than on
  in-memory-only objects.

## Recommended next moves

- Build the next concrete kernel surface on top of the persisted records, likely the
  first bounded index slice.
- Defer the daemon-facing default store root decision until the runtime layer is ready
  to own it explicitly.
