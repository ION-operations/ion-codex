---
type: research
from: Codex
created: 2026-04-03T20:52:53-04:00
status: COMPLETE
topic: First authority-aware kernel validator / commit-gate slice
connections:
  - ION/04_packages/kernel/validation.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_validation.py
  - ION/05_context/inbox/codex_kernel_validation_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_validation_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md
  - ION/06_intelligence/specs/T06_AuthorityClassSchema.spec.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_execution_first_pass.md
---

# Codex Kernel Validation First Pass

## Why this exists

The active kernel loop had reached `VALIDATING`, but authority class was still mostly a
typed concept rather than a runtime decision surface. The loop still lacked a truthful
gate that could reject illegal writes, require review, or downgrade stale authority to
witness.

This pass adds that first bounded gate.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/execution.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_validation.py`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/specs/T06_AuthorityClassSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/validation.py` now provides the first bounded authority-aware
  validator / commit-gate helper for the active kernel stack.
- The helper introduces:
  `KernelValidator`, `IonValidator`, `KernelValidationError`, and `ValidationDecision`.
- The validator currently performs four real runtime decisions:
  - reject produced artifacts outside `allowed_writes`
  - reject produced artifacts that match `must_not`
  - require review for low-confidence deltas
  - downgrade stale authority-bearing artifacts to `WITNESS`
- The validator persists both:
  an updated `CommitDelta.status`
  and
  the resulting `WorkUnit.status`.
- Current work-unit outcomes are now truthful and explicit:
  - `ACCEPTED` -> `COMMITTED`
  - `ACCEPTED_AS_WITNESS` -> `COMMITTED`
  - `REJECTED` -> `FAILED`
  - `REQUIRES_REVIEW` -> remains `VALIDATING`
- `ION/tests/test_kernel_validation.py` proves:
  fresh acceptance, stale authority downgrade to witness, outside-scope rejection,
  low-confidence review hold, and rejection of non-validating work units.
- The combined kernel suite is now at **65 passing tests**.

## Boundary

- This is not the full artifact-apply committer.
- It does not yet write accepted artifacts or state mutations to the filesystem.
- It does not yet emit validation receipts or completion signals automatically.
- It does not yet perform reconciliation routing.
- It does not yet operationalize open-question scheduling.

## Implications

- The active kernel now makes its first real authority-aware runtime decision.
- The runtime loop now reaches truthful status outcomes beyond `VALIDATING`:
  `WorkUnit -> ContextPackage -> dispatch -> execution submission -> CommitDelta -> validation decision -> COMMITTED/FAILED/held`
- Authority class is no longer only metadata. It now affects runtime outcome.

## Recommended next moves

- Build the first bounded artifact-apply / commit-applier helper so accepted deltas can
  write their produced artifacts and state mutations lawfully.
- After that, make open-question routing operational so accepted or reviewed deltas can
  issue real follow-up work from unresolved questions.
