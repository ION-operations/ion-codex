---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T17:58:00-04:00
from: Sovereign
target: ION/04_packages/kernel/model.py
depends_on: none
status: COMPLETE
updated: 2026-04-03T17:59:50-04:00
completed_by: Codex
---

# Mission: Implement the first lawful kernel model slice

## Goal

Replace the `ION/04_packages/kernel/model.py` scaffold with a first real model layer
based on the current schema specs, giving the kernel package typed objects for
authority classification and the daemon-facing execution contract.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/specs/T05_OpenQuestionSchema.spec.md`
- `ION/06_intelligence/specs/T06_AuthorityClassSchema.spec.md`

## Requirements

1. Keep this first pass bounded and legible.
2. Implement the core enums and dataclasses needed to represent:
   authority classes, work units, context packages, commit deltas, and open questions.
3. Export the model layer from the kernel package.
4. Add tests proving importability and basic model behavior.

## Deliverables

- patched `ION/04_packages/kernel/model.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more tests for the model layer
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not pretend the full store/index/graph stack exists yet.
2. Do not invent daemon behavior beyond what the current specs already support.
3. Keep the provenance trail explicit if conceptual role passes are completed by Codex
   in sequential-kernel mode.

## Completion Signal

Emit one Codex signal pointing to the first-pass kernel model result.

## Completion Record — 2026-04-03T17:59:50-04:00

- status: COMPLETE
- operator: Codex
- summary: Completed the first lawful kernel model slice and verified it through the live implementation bundle and model test suite.
- artifacts:
  - ION/04_packages/kernel/model.py
  - ION/tests/test_kernel_model.py
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_model_first_pass/00_trace.md
- next_action: Build the next concrete kernel surface on top of these types rather than extending task plumbing again.
- note: Retired by Codex after full live implementation-loop completion; this does not imply independent multi-chat role review.
