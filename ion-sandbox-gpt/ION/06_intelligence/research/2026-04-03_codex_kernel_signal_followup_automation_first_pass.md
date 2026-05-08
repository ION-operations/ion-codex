---
type: research
from: Codex
created: 2026-04-03T23:20:40-04:00
status: COMPLETE
topic: First bounded signal-triggered follow-up helper
connections:
  - ION/04_packages/kernel/signal_followups.py
  - ION/04_packages/kernel/signals.py
  - ION/04_packages/kernel/reviews.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/daemon_loop.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_signal_followups.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/tests/test_kernel_daemon_loop.py
  - ION/05_context/inbox/codex_kernel_signal_followup_automation_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_signal_followup_automation_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_review_escalation_first_pass.md
---

# Codex Kernel Signal Follow-Up Automation First Pass

## Why this exists

The active daemon could already consume and interpret canonical signals, but it
still stopped short of materializing the bounded next step those signals often
already implied.

This pass adds the smallest honest follow-up layer the current stack can support
today: a consumed failure signal can create one durable replan/retry question,
and a consumed blocked-review signal can reuse the existing review-escalation
path in the same bounded daemon step.

## Sources or surfaces considered

- `ION/04_packages/kernel/signals.py`
- `ION/04_packages/kernel/reviews.py`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/daemon_actions.py`
- `ION/04_packages/kernel/daemon_loop.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_signal_followups.py`
- `ION/tests/test_kernel_daemon_actions.py`
- `ION/tests/test_kernel_daemon_loop.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/signal_followups.py` now provides:
  - `KernelSignalFollowUpHandler`
  - `SignalFollowUpDisposition`
  - `SignalFollowUpPreparation`
  - `SignalFollowUpResult`
  - `SIGNAL_FOLLOWUP_DOMAIN`
- The new helper keeps the first pass narrow:
  - `TASK_COMPLETE` signals now resolve to explicit `NO_FOLLOW_UP_REQUIRED`
  - `TASK_FAILED` signals now create one deterministic `signal_followup`
    `OpenQuestion` routed to `Vizier`
  - `BLOCKED` signals tied to a live `REQUIRES_REVIEW` delta now reuse
    `KernelReviewEscalator` instead of spawning a parallel generic blocker
    question
- `ION/04_packages/kernel/daemon_actions.py` now materializes signal follow-up
  in the same bounded `CONSUME_ACTIVE_SIGNAL` step rather than only returning a
  recommendation string.
- This improves the loop boundary materially:
  - a blocked-review signal can now be consumed and escalated inside the same
    daemon step
  - the following loop step can go straight to `IDLE` instead of needing a
    separate later `ESCALATE_REVIEW` action
- The first-pass dedupe rules are explicit:
  - deterministic signal-follow-up question ids prevent duplicate replan
    questions
  - existing review-escalation detection prevents duplicate held-review
    questions for the same delta
- `ION/tests/test_kernel_signal_followups.py` now proves the helper directly:
  - failure signal creates one `Vizier` follow-up question
  - blocked signal reuses review escalation
  - duplicate failure follow-up is refused as new pressure
- The daemon tests now prove:
  - `act_once(...)` creates durable follow-up for failure signals
  - `act_once(...)` reuses review escalation for blocked signals
  - `run_until_blocked(...)` can consume a blocked signal, escalate review, and
    then reach `IDLE` without a separate review branch
- The combined kernel suite is now at **113 passing tests**.

## Boundary

- This is not a full replanner or retry engine.
- It does not yet issue new work units directly from failure signals.
- It does not yet resolve the follow-up questions it creates.
- It keeps signal-triggered automation bounded to durable pressure creation and
  review-path reuse only.

## Implications

- Signal consumption is no longer a pure archive-and-return operation.
- The daemon can now collapse some signal pressure directly into lawful kernel
  state in the same bounded step.
- The remaining runtime frontier is narrower than before:
  - richer loop receipts / telemetry
  - or bounded review-resolution / follow-up execution beyond durable pressure

## Recommended next moves

- Decide whether the next runtime slice should be:
  - richer loop receipts and per-step telemetry
  - or bounded review/follow-up resolution
- After that, determine whether signal follow-up should ever issue child work
  directly or remain pressure-only until the planner layer is stronger.
