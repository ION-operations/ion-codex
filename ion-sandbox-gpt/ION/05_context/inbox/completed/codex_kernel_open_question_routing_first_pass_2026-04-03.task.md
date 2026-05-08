---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T21:09:12-04:00
from: Sovereign
target: ION/04_packages/kernel/questions.py
depends_on: ION/04_packages/kernel/commit.py
status: COMPLETE
updated: 2026-04-03T21:15:31-04:00
completed_by: Codex
---

# Mission: Implement the first bounded kernel open-question routing helper

## Goal

Build the first truthful open-question routing layer so accepted `CommitDelta`
proposals can become persisted `OpenQuestion` records, influence future work
scheduling through the current graph/scheduler stack, and later be resolved
without pretending the full daemon scheduler already exists.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/execution.py`
- `ION/04_packages/kernel/validation.py`
- `ION/04_packages/kernel/scheduler.py`
- `ION/04_packages/kernel/graph.py`
- `ION/04_packages/kernel/index.py`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/06_intelligence/specs/T05_OpenQuestionSchema.spec.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_commit_first_pass.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Require a bound `WorkUnit` in `COMMITTED`.
3. Require a `CommitDelta` already accepted by validation.
4. Materialize persisted `OpenQuestion` records from `proposed_open_questions`.
5. Make the routed questions affect future scheduler behavior through the existing
   graph/index path.
6. Add a bounded resolution helper so routed questions can later stop blocking
   work.
7. Export the routing surface from the kernel package.
8. Add focused tests for routed blocking behavior, resolution release, default
   parsing, and refusal of unaccepted deltas.

## Deliverables

- new `ION/04_packages/kernel/questions.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more open-question routing tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim the full child-work compiler or daemon scheduler exists.
2. Do not invent a second question system outside `OpenQuestion`.
3. Preserve explicit provenance if the pass is completed by Codex under its own
   `CODE` binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the open-question routing first-pass result.

## Completion Record — 2026-04-03T21:15:31-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded open-question routing helper, exported it through the kernel package, verified blocking and resolution behavior through the live scheduler path, and closed the pass under Codex's CODE binding.
- artifacts:
  - ION/04_packages/kernel/questions.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_questions.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_open_question_routing_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_OPEN_QUESTION_ROUTING_FIRST_PASS_20260403T2113.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_open_question_routing_first_pass/00_trace.md
- next_action: Build the first bounded validation-receipt / signal-emission layer, then decide the next question-side expansion.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
