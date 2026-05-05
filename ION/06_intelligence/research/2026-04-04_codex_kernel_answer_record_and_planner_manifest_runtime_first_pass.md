---
type: research
from: Codex
created: 2026-04-04T12:35:00-04:00
status: COMPLETE
topic: First persisted answer-record and planner-manifest runtime families, plus daemon manifest consumption
connections:
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/graph.py
  - ION/04_packages/kernel/question_answers.py
  - ION/04_packages/kernel/planner_gate.py
  - ION/04_packages/kernel/daemon.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/tests/test_kernel_question_answers.py
  - ION/tests/test_kernel_planner_gate.py
  - ION/tests/test_kernel_daemon.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/05_context/inbox/completed/codex_kernel_answer_record_and_planner_manifest_runtime_first_pass_2026-04-04.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_answer_record_and_planner_manifest_runtime_first_pass/00_trace.md
  - ION/06_intelligence/research/2026-04-04_codex_kernel_question_answer_and_planner_gate_first_pass.md
---

# Codex Kernel Answer Record + Planner Manifest Runtime First Pass

## Why this exists

Codex MINI left two durability questions explicitly next:

- should answer ingestion become a first-class persisted runtime record family?
- does planner/manifest state need a dedicated family beyond `CommitDelta.resolved_question_ids` before broader daemon-owned retry logic lands?

This pass answers both in the affirmative and lands the smallest honest runtime slices that
follow from those decisions.

## Findings

- `ION/04_packages/kernel/model.py` now contains two new runtime families:
  - `QuestionAnswerRecord`
  - `PlannerManifest`
- `ION/04_packages/kernel/store.py`, `index.py`, and `graph.py` now persist, query, and
  link those families directly instead of treating answer/manifest state as only implied.
- `ION/04_packages/kernel/question_answers.py` now persists one explicit `question_answer`
  record before resolving the underlying `OpenQuestion`.
  - this makes answer provenance durable and queryable as runtime state
  - the current pass keeps the family narrow: one bounded explicit answer per question
- `ION/04_packages/kernel/planner_gate.py` now persists one dedicated `planner_manifest`
  record for the resolved-question + accepted-delta binding before child issuance.
  - the manifest stays `READY` until issuance
  - the manifest becomes `EXECUTED` with explicit child work ids after issuance
- `ION/04_packages/kernel/daemon.py` now prefers `READY` planner manifests when gathering
  child-work candidates.
- `ION/04_packages/kernel/daemon_actions.py` now consumes those ready manifests through the
  planner gate, producing `ISSUED_CHILD_WORK_FROM_PLANNER_MANIFEST` instead of bypassing the
  dedicated manifest state.

## Boundary

- This is not a full retry compiler.
- It is not a general planner daemon.
- It does not let failure signals or answers issue child work directly.
- It does not yet compile planner manifests automatically from resolved follow-up pressure;
  the manifest must already exist as runtime state.
- It does not yet define cancellation, supersession, or expiry behavior for planner manifests.

## Implications

- Answer provenance now survives as its own runtime record family instead of only living on
  `OpenQuestion` mutation fields.
- Planner linkage now survives as its own runtime family instead of only living on later
  deltas through `resolved_question_ids`.
- The daemon now has one truthful next-step bridge into that state: when a manifest is
  already `READY`, it can be consumed lawfully and marked `EXECUTED` after child issuance.
- This creates a cleaner substrate for any future retry compiler because answer evidence,
  manifest state, and execution outcomes are now separated.

## Verification

- focused state/runtime tests pass across answer, planner, store, index, graph, daemon,
  and daemon-action surfaces
- full kernel suite result: **133 passed, 3 subtests passed**

## Recommended next moves

- Decide whether `question_answer` records need reviewer-facing queue/projection surfaces
  beyond per-question lookup.
- Decide whether `planner_manifest` needs explicit lifecycle branches such as cancellation,
  supersession, or expiry when later evidence closes the branch.
- Only after that, consider whether resolved follow-up pressure should ever compile ready
  planner manifests automatically for bounded daemon-owned retry flow.
