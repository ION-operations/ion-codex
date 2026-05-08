---
type: research
from: Codex
created: 2026-04-03T21:13:46-04:00
status: COMPLETE
topic: First bounded open-question routing slice
connections:
  - ION/04_packages/kernel/questions.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_questions.py
  - ION/05_context/inbox/codex_kernel_open_question_routing_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_open_question_routing_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md
  - ION/06_intelligence/specs/T05_OpenQuestionSchema.spec.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_commit_first_pass.md
---

# Codex Kernel Open-Question Routing First Pass

## Why this exists

The active kernel stack could already carry question text inside
`CommitDelta.proposed_open_questions`, and the scheduler already knew how to block on
persisted `OpenQuestion` records. What was missing was the bridge between those two
surfaces. Unresolved questions could be proposed, but not yet routed into live kernel
state.

This pass adds that bridge.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/execution.py`
- `ION/04_packages/kernel/validation.py`
- `ION/04_packages/kernel/scheduler.py`
- `ION/04_packages/kernel/graph.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_questions.py`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/specs/T05_OpenQuestionSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/questions.py` now provides the first bounded open-question
  routing helper for the active kernel stack.
- The helper introduces:
  `KernelQuestionRouter`, `IonQuestionRouter`, `KernelQuestionRoutingError`,
  `ParsedQuestionDirective`, `QuestionRoutingPreparation`,
  `QuestionRoutingResult`, and `QuestionResolutionResult`.
- The router only proceeds when:
  - the bound `WorkUnit` is already `COMMITTED`
  - the `CommitDelta` is already `ACCEPTED` or `ACCEPTED_AS_WITNESS`
  - work-unit / delta binding is still coherent
- `CommitDelta.proposed_open_questions` now becomes real kernel state:
  accepted question proposals are materialized into persisted `OpenQuestion` records,
  indexed, and graphed.
- The first-pass question syntax is intentionally bounded:
  plain strings remain legal,
  and optional bracketed directives can now refine routing:
  - `[needed_from=...]`
  - `[priority=...]`
  - `[blocking=wu-a,wu-b]`
  - `[domain=...]`
  - `[scope=...]`
  - `[context=...]`
  - `[parent=...]`
- Plain question strings route with conservative defaults:
  - `needed_from=UNSPECIFIED`
  - `priority=P2_NORMAL`
  - `domain=work_unit.agent_domain`
  - `scope_ref=work_unit.scope_ref`
- Resolution is now a real kernel action:
  routed questions can later be marked `RESOLVED` with `resolved_by`,
  `resolved_at`, `resolution`, and `resolution_evidence`.
- Because the graph and scheduler already knew about blocking questions, this routing
  layer immediately makes scheduler behavior more real:
  a routed blocking question will stop a pending work unit from being dispatchable,
  and resolving that same question releases the work unit again.
- `ION/tests/test_kernel_questions.py` proves:
  routed blocking behavior, resolution release, plain-question defaults, and refusal of
  malformed or non-routable question paths.
- The combined kernel suite is now at **74 passing tests**.

## Boundary

- This is not yet the full child-work compiler.
- It does not yet create follow-up `WorkUnit` records automatically from routed
  questions.
- It does not yet add receipt/signal emission around question routing.
- It does not yet reconcile competing answers from parallel question-resolution paths.

## Implications

- The active kernel now has a truthful unresolved-question loop:
  `CommitDelta.proposed_open_questions -> persisted OpenQuestion -> scheduler blocking -> question resolution -> scheduler release`
- Open questions are no longer only latent metadata. They now influence runtime
  dispatchability through the current index/graph/scheduler stack.
- This materially advances the kernel toward the proving workflow previously called
  for, even though child-work issuance and commit receipts still remain ahead.

## Recommended next moves

- Build the first bounded validation-receipt / signal-emission layer so accepted or
  failed runtime transitions produce explicit post-validation artifacts beyond the
  current filesystem hooks.
- After that, decide whether the next question step should be automatic child-work
  issuance or richer question assignment semantics.
