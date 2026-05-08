---
type: research
from: Codex
created: 2026-04-03T22:51:03-04:00
status: COMPLETE
topic: First bounded held-review escalation helper
connections:
  - ION/04_packages/kernel/reviews.py
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/validation.py
  - ION/04_packages/kernel/daemon.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/daemon_loop.py
  - ION/tests/test_kernel_reviews.py
  - ION/tests/test_kernel_validation.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/tests/test_kernel_daemon_loop.py
  - ION/05_context/inbox/codex_kernel_review_escalation_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_review_escalation_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_daemon_loop_first_pass.md
---

# Codex Kernel Review Escalation First Pass

## Why this exists

The active kernel could already hold a delta in `REQUIRES_REVIEW`, but the
daemon still treated that pressure as a terminal unsupported branch.

This pass adds the smallest honest escalation layer the current stack can
support today: persist the reasons for held review, turn the held delta into a
durable review-shaped `OpenQuestion`, and let the daemon loop continue lawfully
instead of stalling at review pressure.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/validation.py`
- `ION/04_packages/kernel/reviews.py`
- `ION/04_packages/kernel/daemon.py`
- `ION/04_packages/kernel/daemon_actions.py`
- `ION/04_packages/kernel/daemon_loop.py`
- `ION/tests/test_kernel_reviews.py`
- `ION/tests/test_kernel_validation.py`
- `ION/tests/test_kernel_daemon_actions.py`
- `ION/tests/test_kernel_daemon_loop.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/model.py` now lets `CommitDelta` carry
  `review_reasons`, giving held-review escalation lawful kernel inputs instead
  of relying on implied validator state.
- `ION/04_packages/kernel/validation.py` now persists those `review_reasons`
  whenever a delta lands in `REQUIRES_REVIEW`.
- `ION/04_packages/kernel/reviews.py` now provides:
  - `KernelReviewEscalator`
  - `ReviewEscalationPreparation`
  - `ReviewEscalationResult`
  - `KernelReviewEscalationError`
  - `REVIEW_DOMAIN`
- The escalator turns one persisted `REQUIRES_REVIEW` delta into one durable
  review-shaped `OpenQuestion`:
  - domain: `validation_review`
  - question id: deterministic `review-<delta-id>`
  - routing: `Vizier` for normal review, `Nemesis` for stale-competitor review
- `ION/04_packages/kernel/daemon.py` now skips held-review deltas that already
  have a review escalation, preventing the arbiter from escalating the same
  held delta indefinitely.
- `ION/04_packages/kernel/daemon_actions.py` now executes `ESCALATE_REVIEW`
  instead of treating review pressure as unsupported.
- `ION/tests/test_kernel_reviews.py` now proves:
  - low-confidence review escalates to `Vizier`
  - stale-competitor review escalates to `Nemesis`
  - duplicate escalation is refused
- The daemon/loop tests now prove that review escalation is no longer a hard
  unsupported stop:
  - `act_once(...)` escalates held review into durable question state
  - `run_until_blocked(...)` can escalate held review and then reach `IDLE`
- The combined kernel suite is now at **108 passing tests**.

## Boundary

- This is not substantive review resolution.
- It does not yet automatically close the review question after a reviewer pass.
- It does not yet perform signal-triggered follow-up automation beyond the
  current bounded layers.
- Review routing is still first-pass and intentionally narrow.

## Implications

- Held review is now lawful kernel state instead of an unresolved daemon dead
  end.
- The daemon loop can continue through the review branch without pretending that
  a full reviewer runtime already exists.
- The remaining daemon/runtime gaps are now narrower and more explicit than the
  old generic unsupported-review stop.

## Recommended next moves

- Decide whether the next runtime slice should be:
  - signal-triggered follow-up automation
  - or richer loop receipts / step telemetry
- After that, consider whether review resolution itself should become a bounded
  follow-up path rather than only durable open-question pressure.
