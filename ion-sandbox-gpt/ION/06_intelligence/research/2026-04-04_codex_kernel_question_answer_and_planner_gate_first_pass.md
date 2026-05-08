---
type: research
from: Codex
created: 2026-04-04T11:55:00-04:00
status: COMPLETE
topic: First bounded question-answer ingestion and planner-gated child-issuance slice
connections:
  - ION/04_packages/kernel/question_answers.py
  - ION/04_packages/kernel/planner_gate.py
  - ION/04_packages/kernel/questions.py
  - ION/04_packages/kernel/signal_followups.py
  - ION/04_packages/kernel/children.py
  - ION/tests/test_kernel_question_answers.py
  - ION/tests/test_kernel_planner_gate.py
  - ION/05_context/inbox/completed/codex_kernel_question_answer_and_planner_gate_first_pass_2026-04-04.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_question_answer_and_planner_gate_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/research/2026-04-04_codex_kernel_review_followup_resolution_first_pass.md
---

# Codex Kernel Question Answer + Planner Gate First Pass

## Why this exists

Codex MINI left the next runtime order explicit after review/follow-up resolution:

- make bounded reviewer/follow-up answer ingestion explicit
- then revisit planner-gated retry / child-work issuance through explicit child specs

This pass lands both in the smallest honest form the current stack can support.

## Sources or surfaces considered

- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/reviews.py`
- `ION/04_packages/kernel/signal_followups.py`
- `ION/04_packages/kernel/children.py`
- `ION/tests/test_kernel_question_answers.py`
- `ION/tests/test_kernel_planner_gate.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/question_answers.py` now introduces the first explicit
  answer-ingestion helper for the two bounded pressure domains the runtime already owns:
  - `validation_review`
  - `signal_followup`
- The helper is narrow on purpose:
  - it requires an existing persisted `OpenQuestion`
  - it supports only `OPEN` or `ASSIGNED` questions
  - it refuses unrelated domains instead of pretending to be a universal answer bus
  - it resolves the question through the existing `KernelQuestionRouter.resolve_question(...)`
    path rather than adding a second question-state mutation mechanism
- This means reviewer/follow-up answers are now explicit runtime inputs instead of only
  an implied external human act.
- `ION/04_packages/kernel/planner_gate.py` then adds the next narrower lawful child path:
  - the relevant review/follow-up pressure must already be `RESOLVED`
  - the later accepted delta must belong to the same parent work unit
  - the later accepted delta must carry explicit `proposed_child_work_units`
  - the later accepted delta must also explicitly link back to the acted-on question through `CommitDelta.resolved_question_ids`
  - the later delta must not predate the recorded answer
  - only then does the helper delegate to the already-existing child issuer
- This preserves the current build-facing rule:
  - signals do not issue child work directly
  - answers do not issue child work directly
  - explicit child work still enters through accepted `ChildSpec` intent
- The focused tests prove:
  - review questions can now be answered explicitly into durable question state
  - signal-follow-up questions can also be answered explicitly into durable question state
  - unsupported domains refuse answer ingestion
  - planner-gated child issuance succeeds only after explicit answer resolution and a later
    accepted child-bearing delta
  - unresolved pressure, pre-answer deltas, and child-less deltas all refuse the planner gate
- The combined kernel suite is now at **129 passing tests, 3 subtests passed**.

## Boundary

- This is not a full reviewer daemon.
- It is not a full planner/manifest runtime.
- It does not persist a dedicated answer-record family yet.
- It does not yet persist a dedicated answer-record family beyond question-resolution state.
- It does not let signals or answers silently create child work on their own.

## Implications

- Reviewer/follow-up answers are now explicit kernel inputs rather than invisible external state.
- The kernel now has a cleaner lawful bridge from resolved pressure into explicit child work,
  without smuggling planner authority into signal interpretation.
- The next durability pressure is clearer: answer provenance now lands on question state and the planner link now lands on `CommitDelta.resolved_question_ids`, but there is still no dedicated answer-record or manifest family beyond those existing surfaces.

## Recommended next moves

- Decide whether answer ingestion should become a first-class persisted runtime record family,
  or remain a bounded helper around `OpenQuestion` resolution plus `CommitDelta.resolved_question_ids`.
- Consider whether planner/manifest state needs a stronger dedicated family beyond the current delta link before any broader daemon-owned retry logic lands.
- Only after that, consider whether any daemon-owned ingestion path is honest enough to
  promote beyond direct helper use.
