---
type: research
from: Codex
created: 2026-04-03T18:27:00-04:00
status: COMPLETE
topic: First lawful kernel index slice
connections:
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_index.py
  - ION/05_context/inbox/completed/codex_kernel_index_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_index_first_pass/00_trace.md
  - SOS-OPUS/04_packages/ion_kernel/index.py
---

# Codex Kernel Index First Pass

## Why this exists

The kernel now had typed records and durable persistence, but later daemon or graph work
would still have to rescan the filesystem repeatedly. This pass adds the first bounded
in-memory index over the persisted record families.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_index.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/specs/T05_OpenQuestionSchema.spec.md`
- `SOS-OPUS/04_packages/ion_kernel/index.py`

## Findings

- `ION/04_packages/kernel/index.py` now provides a first-pass in-memory index for the
  active kernel record families:
  `WorkUnit`, `ContextPackage`, `CommitDelta`, and `OpenQuestion`.
- The index can rebuild from `KernelStore`, track incremental add/change/remove events,
  and answer bounded cross-record queries without reopening filesystem scans.
- The query floor now includes:
  record-family lookup, protocol/transition/context-version views, work-unit joins,
  scope views, work-unit status/role views, context-package role/work-unit views,
  commit-delta status/agent/authority/artifact views, and open-question
  status/priority/domain/requested-role views.
- `ION/04_packages/kernel/store.py` gained one small support hook:
  `supported_record_types()`, so later layers can enumerate persisted families without
  duplicating the store registry.
- `ION/04_packages/kernel/__init__.py` now exports `KernelIndex` and `IonIndex` as the
  first-pass compatibility alias.
- `ION/tests/test_kernel_index.py` proves full build-from-store behavior, cross-record
  joins, and incremental update/removal semantics. The combined suite is now at
  thirty-two passing tests across sequential-kernel, model, store, and index surfaces.

## Boundary

- This is not a graph engine.
- It does not infer bonds, precedence, or semantic relationships beyond the explicit
  indexed fields.
- It does not yet own daemon scheduling or commit validation.

## Implications

- The kernel now has a three-layer operational floor:
  typed records, durable store, and fast in-memory lookup.
- The next slice can build on a real query substrate instead of ad hoc scans.

## Recommended next moves

- Implement the first bounded graph slice, or a minimal compiler helper that consumes
  the stored-and-indexed record families directly.
- Keep the index scope narrow until the graph layer defines the stronger relationship
  semantics explicitly.
