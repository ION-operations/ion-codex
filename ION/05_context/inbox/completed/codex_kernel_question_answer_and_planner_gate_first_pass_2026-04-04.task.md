---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-04T11:20:00-04:00
from: Sovereign
target: ION/04_packages/kernel/question_answers.py
depends_on: ION/04_packages/kernel/planner_gate.py
status: COMPLETE
updated: 2026-04-04T11:55:00-04:00
completed_by: Codex
---

# Mission: Implement explicit answer ingestion and planner-gated child issuance

## Goal

Make reviewer/follow-up answer ingestion an explicit lawful runtime helper, then land the
next narrower child-work path by gating explicit child-spec issuance behind already-
resolved review/follow-up pressure instead of raw signal interpretation.

## Source / Context

- `ION/03_registry/boots/CODEX.boot.md`
- `ION/agents/codex/MINI.md`
- `ION/agents/codex/CAPSULE.md`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/reviews.py`
- `ION/04_packages/kernel/signal_followups.py`
- `ION/04_packages/kernel/children.py`
- `ION/tests/test_kernel_question_answers.py`
- `ION/tests/test_kernel_planner_gate.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the pass bounded and truthful.
2. Make explicit answer ingestion operate through the existing canonical question-resolution path.
3. Support only the review/follow-up domains the current runtime already owns directly.
4. Keep signal follow-up pressure-only for child work; do not let signals issue children directly.
5. Allow child issuance only when the relevant pressure is already resolved and a later accepted delta explicitly carries `ChildSpec` intent.
6. Add focused tests for the new answer-ingestion and planner-gate surfaces.

## Deliverables

- new `ION/04_packages/kernel/question_answers.py`
- new `ION/04_packages/kernel/planner_gate.py`
- widened kernel exports
- focused tests for answer ingestion and planner-gated child issuance
- one research note and one Codex signal announcing the slice

## Constraints

1. Do not claim a full reviewer daemon, answer queue, or planner/manifest runtime already exists.
2. Do not invent child work from answers or signals alone.
3. Keep child issuance dependent on explicit accepted child specs.
4. Preserve explicit provenance that this slice was completed by Codex under the active `CODE` binding.

## Completion Signal

Emit one Codex signal pointing to the answer-ingestion / planner-gate first-pass result.

## Completion Record — 2026-04-04T11:55:00-04:00

- status: COMPLETE
- operator: Codex
- summary: Added explicit answer ingestion for `validation_review` and `signal_followup` questions through the canonical resolution path, then landed a planner-gated child-issuance wrapper that only allows explicit child-spec issuance after that pressure is already resolved, the later accepted delta belongs to the same parent work unit, and the later delta explicitly links back to the resolved question through `resolved_question_ids`.
- artifacts:
  - ION/04_packages/kernel/question_answers.py
  - ION/04_packages/kernel/planner_gate.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_question_answers.py
  - ION/tests/test_kernel_planner_gate.py
  - ION/06_intelligence/research/2026-04-04_codex_kernel_question_answer_and_planner_gate_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_QUESTION_ANSWER_AND_PLANNER_GATE_FIRST_PASS_20260404T1155.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_question_answer_and_planner_gate_first_pass/00_trace.md
- verification:
  - `PYTHONPATH=04_packages pytest -q tests/test_kernel_question_answers.py tests/test_kernel_planner_gate.py`
  - `PYTHONPATH=04_packages pytest -q`
- next_action: Decide whether answer ingestion should become a first-class persisted runtime record family next, then consider whether planner/manifest state needs a dedicated family beyond `CommitDelta.resolved_question_ids` before any broader daemon-owned retry logic lands.
- note: Completed by Codex under the explicit CODEX__CODE binding; this pass adds bounded answer ingestion and a lawful planner gate without claiming a broader reviewer or planner daemon.
