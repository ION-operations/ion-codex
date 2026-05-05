---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T20:40:47-04:00
from: Sovereign
target: ION/04_packages/kernel/execution.py
depends_on: ION/04_packages/kernel/dispatch.py
status: COMPLETE
updated: 2026-04-03T20:45:15-04:00
completed_by: Codex
---

# Mission: Implement the first lawful kernel execution helper

## Goal

Build the bounded execution helper that accepts an explicit returned execution payload
for a dispatched work unit, materializes a `CommitDelta`, persists it, and advances the
work unit into `VALIDATING` without pretending the validation or commit phases already
exist.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/dispatch.py`
- `ION/06_intelligence/specs/T01_TransitionSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_dispatch_first_pass.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Accept an explicit returned execution submission rather than claiming to run the
   actor itself.
3. Require the work unit to be in a lawful post-dispatch execution state.
4. Materialize a real `CommitDelta` from the returned submission.
5. Persist that delta in the kernel store and index.
6. Advance the work unit into `VALIDATING`.
7. Export the execution surface from the kernel package.
8. Add focused tests for lawful binding, persisted delta creation, status transition,
   and rejection of non-dispatched work.

## Deliverables

- new `ION/04_packages/kernel/execution.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more execution tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim the full validator or committer exists.
2. Do not perform authority-aware acceptance or rejection in this pass.
3. Preserve explicit provenance if the pass is completed by Codex under its own `CODE`
   binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the execution first-pass result.

## Completion Record — 2026-04-03T20:45:15-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded kernel execution helper, exported it through the kernel package, verified explicit returned-submission to CommitDelta materialization plus VALIDATING transitions, and closed the pass under Codex's CODE binding.
- artifacts:
  - ION/04_packages/kernel/execution.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_execution.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_execution_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_EXECUTION_FIRST_PASS_20260403T2043.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_execution_first_pass/00_trace.md
- next_action: Build the first authority-aware validator / commit-gate helper, then make open-question routing operational.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
