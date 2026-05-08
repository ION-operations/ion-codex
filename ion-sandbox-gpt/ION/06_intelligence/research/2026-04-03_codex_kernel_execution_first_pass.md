---
type: research
from: Codex
created: 2026-04-03T20:43:33-04:00
status: COMPLETE
topic: First lawful kernel execution slice
connections:
  - ION/04_packages/kernel/execution.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_execution.py
  - ION/05_context/inbox/codex_kernel_execution_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_execution_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/specs/T01_TransitionSchema.spec.md
  - ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_dispatch_first_pass.md
---

# Codex Kernel Execution First Pass

## Why this exists

The active kernel stack had reached a truthful dispatch bridge, but it still had no
lawful way to accept a returned execution payload and turn it into a persisted
`CommitDelta`. That meant the runtime story stopped at `DISPATCHED`.

This pass adds the next bounded bridge: explicit returned submission in, proposed
delta persisted out, and the work unit advanced to `VALIDATING`.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/dispatch.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_execution.py`
- `ION/06_intelligence/specs/T01_TransitionSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/execution.py` now provides the first bounded execution helper
  for the active kernel stack.
- The helper introduces:
  `KernelExecutor`, `IonExecutor`, `KernelExecutionError`, `ExecutionSubmission`,
  `ExecutionPreparation`, and `ExecutionResult`.
- The execution boundary is narrow and explicit:
  it does not claim to run the actor. It accepts an explicit returned submission,
  binds it to a lawful post-dispatch work unit, materializes a `CommitDelta`, persists
  that delta, and advances the work unit to `VALIDATING`.
- The helper currently permits only:
  `DISPATCHED -> VALIDATING`
  or
  `EXECUTING -> VALIDATING`
  style return paths.
- Context-package binding remains explicit:
  the helper rejects missing or mismatched package identity, protocol, transition,
  personal name, role, and structural identity.
- The helper deliberately preserves a returned `context_version` when supplied, so a
  later validator can make stale-context decisions rather than having freshness faked
  early.
- `ION/04_packages/kernel/__init__.py` now exports the execution surface through the
  lazy kernel package.
- `ION/tests/test_kernel_execution.py` proves:
  lawful delta materialization, persisted commit-delta creation, work-unit transition
  to `VALIDATING`, rejection of non-dispatched work, and preservation of a returned
  stale context version for later validation.
- The combined kernel suite is now at **60 passing tests**.

## Boundary

- This is not the full actor runtime.
- It does not perform validation or commit decisions.
- It does not enforce authority-aware acceptance or rejection yet.
- It does not yet make open-question routing operational.

## Implications

- The active kernel loop now reaches `VALIDATING` truthfully:
  `WorkUnit -> ContextPackage -> dispatch -> returned submission -> CommitDelta -> VALIDATING`
- The next missing runtime hinge is now sharply defined:
  the validator / commit gate.
- That means the immediate next build priority should no longer be another generic
  orchestration note. It should be the first authority-aware validation surface.

## Recommended next moves

- Build the first bounded validator / commit-gate helper on top of the new execution
  surface.
- After that, make `OpenQuestion` scheduling operational so the loop can issue follow-up
  work from unresolved questions instead of only storing them.
