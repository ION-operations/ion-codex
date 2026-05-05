---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T22:58:00-04:00
from: Sovereign
target: ION/04_packages/kernel/signal_followups.py
depends_on: ION/04_packages/kernel/signals.py
status: COMPLETE
updated: 2026-04-03T23:23:01-04:00
completed_by: Codex
---

# Mission: Implement the first bounded signal-triggered follow-up helper

## Goal

Extend the active daemon/runtime stack so consumed canonical signals can
materialize one lawful bounded follow-up when the current kernel already knows
what that follow-up should be, instead of only archiving the signal and
returning a recommendation string.

## Source / Context

- `ION/04_packages/kernel/signals.py`
- `ION/04_packages/kernel/reviews.py`
- `ION/04_packages/kernel/daemon_actions.py`
- `ION/04_packages/kernel/daemon_loop.py`
- `ION/04_packages/kernel/questions.py`
- `ION/tests/test_kernel_signals.py`
- `ION/tests/test_kernel_daemon_actions.py`
- `ION/tests/test_kernel_daemon_loop.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Do not claim a full replanner or recovery daemon already exists.
3. Materialize follow-up only where the current kernel can do so lawfully.
4. Avoid duplicating the existing review-escalation path.
5. Wire the helper into daemon act-once so signal follow-up can happen in the same bounded step.
6. Add focused tests for direct follow-up plus daemon and loop behavior.

## Deliverables

- new `ION/04_packages/kernel/signal_followups.py`
- patched daemon-action/kernel exports and any narrowly needed support surfaces
- one or more focused signal-follow-up tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not fake substantive recovery or retry execution.
2. Do not create duplicate review questions for the same held delta.
3. Preserve explicit provenance if the pass is completed by Codex under its own
   `CODE` binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the signal-follow-up first-pass result.

## Completion Record — 2026-04-03T23:23:01-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded signal-triggered follow-up slice, allowing failure signals to create durable replan pressure and blocked-review signals to reuse review escalation inside the same daemon step.
- artifacts:
  - ION/04_packages/kernel/signal_followups.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_signal_followups.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/tests/test_kernel_daemon_loop.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_signal_followup_automation_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_SIGNAL_FOLLOWUP_AUTOMATION_FIRST_PASS_20260403T2320.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_signal_followup_automation_first_pass/00_trace.md
- next_action: Decide whether richer loop receipts / step telemetry or bounded review/follow-up resolution should land next.
- note: Completed by Codex under the explicit CODEX__CODE binding; support-role passes remained sequential rather than independent.
