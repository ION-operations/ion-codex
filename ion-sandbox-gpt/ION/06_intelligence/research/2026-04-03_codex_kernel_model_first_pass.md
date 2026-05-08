---
type: research
from: Codex
created: 2026-04-03T17:59:56-04:00
status: COMPLETE
topic: First lawful kernel model slice
connections:
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_model.py
  - ION/05_context/inbox/completed/codex_kernel_model_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_model_first_pass/00_trace.md
---

# Codex Kernel Model First Pass

## Why this exists

The kernel package previously had only a scaffold placeholder for `model.py`.
This pass turns that placeholder into a real typed model layer so later store,
index, graph, and daemon work can build on concrete objects instead of prose alone.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_model.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/specs/T05_OpenQuestionSchema.spec.md`
- `ION/06_intelligence/specs/T06_AuthorityClassSchema.spec.md`

## Findings

- `ION/04_packages/kernel/model.py` now contains a first real set of kernel model
  enums and dataclasses for:
  authority classes, work units, context packages, commit deltas, open questions,
  and the supporting nested record types those schemas imply.
- The kernel package now exports those model types lazily through
  `ION/04_packages/kernel/__init__.py`.
- The model layer includes a few bounded helpers where the specs clearly justify them:
  checksum generation for produced artifacts, explicit stale-context comparison for
  context packages, readiness checks for work units, and blocking semantics for open
  questions.
- The proof set now includes `ION/tests/test_kernel_model.py`, and the combined test
  suite is at twenty passing tests.
- The first-pass boundary is explicit:
  this is the typed execution-contract layer only.
  It does not yet implement store persistence, graph bonds, or daemon scheduling.

## Implications

- The kernel package now has a real object-model floor rather than a placeholder.
- The next concrete implementation step should build on these types, not reopen the
  task-routing substrate.

## Recommended next moves

- Implement the next kernel surface directly on top of the model layer, likely store
  persistence or a minimal context-package compiler helper.
- Keep the model aligned to the active specs as those specs evolve.
