---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T20:46:00-04:00
from: Sovereign
target: ION/04_packages/kernel/validation.py
depends_on: ION/04_packages/kernel/execution.py
status: COMPLETE
updated: 2026-04-03T20:55:15-04:00
completed_by: Codex
---

# Mission: Implement the first authority-aware kernel validator / commit-gate helper

## Goal

Build the bounded validator helper that can evaluate a proposed `CommitDelta` against
its bound work unit, make the first real runtime authority decision, persist the delta
outcome, and move the work unit toward `COMMITTED`, `FAILED`, or held review without
pretending the full artifact-apply committer already exists.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/execution.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/specs/T06_AuthorityClassSchema.spec.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_execution_first_pass.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Make a real runtime decision on delta outcome rather than treating authority class as
   passive metadata.
3. Reject produced artifacts outside `allowed_writes`.
4. Apply at least one authority-aware downgrade rule.
5. Persist both updated `CommitDelta.status` and resulting `WorkUnit.status`.
6. Export the validator surface from the kernel package.
7. Add focused tests for acceptance, witness downgrade, rejection, and review hold.

## Deliverables

- new `ION/04_packages/kernel/validation.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more validation tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim the full artifact-apply committer exists.
2. Do not yet implement reconciliation or open-question scheduling.
3. Preserve explicit provenance if the pass is completed by Codex under its own `CODE`
   binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the validation first-pass result.

## Completion Record — 2026-04-03T20:55:15-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first authority-aware kernel validator / commit-gate helper, exported it through the kernel package, verified witness downgrade and rejection behavior, and closed the pass under Codex's CODE binding.
- artifacts:
  - ION/04_packages/kernel/validation.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_validation.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_validation_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_VALIDATION_FIRST_PASS_20260403T2052.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_validation_first_pass/00_trace.md
- next_action: Build the first bounded artifact-apply / commit-applier helper, then make open-question routing operational.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
