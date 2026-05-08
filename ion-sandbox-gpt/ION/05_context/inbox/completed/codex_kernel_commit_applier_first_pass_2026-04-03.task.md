---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T20:58:49-04:00
from: Sovereign
target: ION/04_packages/kernel/commit.py
depends_on: ION/04_packages/kernel/validation.py
status: COMPLETE
updated: 2026-04-03T21:06:41-04:00
completed_by: Codex
---

# Mission: Implement the first bounded kernel commit-applier helper

## Goal

Build the first truthful post-commit helper that can apply validated
`CommitDelta` outputs to a bounded workspace root. This pass should materialize
accepted produced artifacts and state mutations without pretending the full
receipt, signal, or reconciliation layer already exists.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/validation.py`
- `ION/04_packages/kernel/execution.py`
- `ION/04_packages/kernel/store.py`
- `ION/06_intelligence/specs/T01_TransitionSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_validation_first_pass.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Require a bound `WorkUnit` in `COMMITTED`.
3. Require a `CommitDelta` already accepted by validation.
4. Apply produced artifacts to an explicit workspace root with strict path
   safety.
5. Apply bounded state mutations in a truthful first-pass way.
6. Re-check write legality defensively before filesystem mutation.
7. Export the commit-applier surface from the kernel package.
8. Add focused tests for accepted apply, witness apply, state mutation apply,
   rejection of unaccepted deltas, and path escape refusal.

## Deliverables

- new `ION/04_packages/kernel/commit.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more commit-applier tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim the full signal-emission or reconciliation layer exists.
2. Do not invent a new runtime state beyond the current post-`COMMITTED` hook.
3. Preserve explicit provenance if the pass is completed by Codex under its own
   `CODE` binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the commit-applier first-pass result.

## Completion Record — 2026-04-03T21:06:41-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded post-commit artifact/state applier, exported it through the kernel package, verified accepted and witness-downgraded apply plus state-mutation safety, and closed the pass under Codex's CODE binding.
- artifacts:
  - ION/04_packages/kernel/commit.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_commit.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_commit_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_COMMIT_FIRST_PASS_20260403T2103.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_commit_applier_first_pass/00_trace.md
- next_action: Make open-question routing operational, then build the first bounded validation-receipt / signal-emission layer.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
