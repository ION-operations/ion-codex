---
type: research
from: Codex
created: 2026-04-04T10:15:00-04:00
status: COMPLETE
topic: First bounded review/follow-up resolution slice
connections:
  - ION/04_packages/kernel/signal_followups.py
  - ION/04_packages/kernel/questions.py
  - ION/04_packages/kernel/reviews.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/daemon_loop.py
  - ION/tests/test_kernel_signal_followups.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/tests/test_kernel_daemon_loop.py
  - ION/05_context/inbox/completed/codex_kernel_review_followup_resolution_first_pass_2026-04-04.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_review_followup_resolution_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_signal_followup_automation_first_pass.md
  - ION/06_intelligence/research/2026-04-04_codex_kernel_loop_receipts_telemetry_first_pass.md
---

# Codex Kernel Review/Follow-Up Resolution First Pass

## Why this exists

Codex MINI left the next runtime slice explicit after loop receipts / telemetry:

- land bounded review/follow-up resolution
- then determine whether signal follow-up should ever issue child work directly

This pass lands both build-facing outcomes in the smallest honest way the current stack
can support.

The goal is narrow:

- when a later completion signal lawfully supersedes older `signal_followup` or
  `validation_review` pressure, resolve that pressure into durable question state
  instead of leaving it open forever
- keep signal follow-up pressure-only for child work until the planner/manifest
  layer is stronger than the current first-pass signal surface

## Sources or surfaces considered

- `ION/04_packages/kernel/signal_followups.py`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/reviews.py`
- `ION/04_packages/kernel/children.py`
- `ION/04_packages/kernel/daemon_actions.py`
- `ION/04_packages/kernel/daemon_loop.py`
- `ION/tests/test_kernel_signal_followups.py`
- `ION/tests/test_kernel_daemon_actions.py`
- `ION/tests/test_kernel_daemon_loop.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/signal_followups.py` now widens `KernelSignalFollowUpHandler`
  so `TASK_COMPLETE` is no longer a pure `NO_FOLLOW_UP_REQUIRED` branch.
- The helper now discovers open questions for the same `work_unit_id` in the two bounded
  pressure domains the current runtime already knows how to own:
  - `signal_followup`
  - `validation_review`
- The resolution guard is explicit and narrow:
  - the question must still be `OPEN` or `ASSIGNED`
  - the question must belong to one of the two bounded domains above
  - the question must predate the completion signal
  - the completion signal's `delta_id` must not be the same delta that created the pressure
- When those guards hold, the helper now resolves the question via the existing
  `KernelQuestionRouter.resolve_question(...)` path instead of inventing a second
  question-state mutation mechanism.
- `SignalFollowUpDisposition` now includes `RESOLVED_EXISTING_QUESTIONS`, and
  `SignalFollowUpResult` now exposes the actual `QuestionResolutionResult` records.
- `ION/04_packages/kernel/daemon_loop.py` telemetry now records `resolved_question_ids`
  when signal-follow-up resolution happens inside a daemon step.
- The focused tests now prove three new runtime truths directly:
  - a completion signal can resolve an earlier `signal_followup` question
  - a completion signal can resolve an earlier `validation_review` question when it is
    clearly newer pressure
  - completion does **not** auto-resolve pressure tied to the same delta that created it
- The daemon-action and daemon-loop tests now also prove the wider runtime boundary:
  - daemon signal consumption can resolve durable pressure in the same bounded step
  - loop telemetry preserves machine-readable witness of the resolution path
- The combined kernel suite is now at **120 passing tests, 3 subtests passed**.

## Boundary

- This is not a full reviewer runtime.
- It is not a retry planner.
- It does not convert failure signals directly into child work.
- It resolves only the narrow pressure classes the current stack can already represent
  lawfully as open questions.

## Build-facing determination on child work

The current build should keep **signal follow-up pressure-only for child work**.

Why:

- `ION/04_packages/kernel/children.py` lawfully issues child work from explicit
  `CommitDelta.proposed_child_work_units` plus the parent work unit, doctrine, repo root,
  and spawn-policy checks.
- A consumed signal does not currently carry the equivalent bounded child-spec surface.
- Letting signal follow-up jump straight to child issuance here would smuggle in planner
  authority the current signal layer does not actually own.

So the current determination is:

- failure or blocked signals may create or resolve durable pressure
- child work still enters lawfully through explicit planner/execution surfaces, not
  directly from signal follow-up

This is a build-facing constraint, not a permanent constitutional claim.

## Implications

- Review/follow-up pressure is no longer one-way accumulation only.
- The daemon can now consume a later completion signal and close bounded older pressure in
  the same step when the evidence is already on disk.
- The child-work frontier is now clearer rather than blurrier:
  - if direct signal-to-child issuance ever lands, it should arrive through a stronger
    planner/manifest contract, not through silent expansion of the signal layer.

## Recommended next moves

- Keep signal follow-up pressure-only for child work until planner/manifest state is
  stronger.
- Make the next runtime slice one of these:
  - bounded reviewer/follow-up answer ingestion into existing question state
  - or planner-gated retry / child-work issuance that enters through explicit child specs
    rather than raw signal interpretation
