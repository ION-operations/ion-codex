---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T21:45:12-04:00
from: Sovereign
target: ION/04_packages/kernel/daemon.py
depends_on: ION/04_packages/kernel/children.py
status: COMPLETE
updated: 2026-04-03T21:52:04-04:00
completed_by: Codex
---

# Mission: Implement the first bounded kernel daemon arbitration helper

## Goal

Build the first truthful daemon decision layer so the active kernel can inspect
current persisted state and choose the next highest-priority lawful action among
signal pressure, held-review escalation, open-question routing, child-work
issuance, and dispatchable work without pretending the full autonomous daemon
loop already exists.

## Source / Context

- `ION/04_packages/kernel/scheduler.py`
- `ION/04_packages/kernel/signals.py`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/children.py`
- `ION/04_packages/kernel/validation.py`
- `ION/06_intelligence/specs/T01_TransitionSchema.spec.md`
- `ION/06_intelligence/specs/T07_SignalSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Return structured next-action decisions rather than claiming a full daemon loop.
3. Consider at least these pressures:
   - active daemon-targeted signals
   - review-held validation state
   - accepted deltas still carrying unrouted open questions
   - accepted deltas still carrying unissued child work
   - dispatchable pending work
4. Make the action priority order explicit in code and tests.
5. Export the arbiter surface from the kernel package.
6. Add focused tests for decision ordering and representative candidate kinds.

## Deliverables

- new `ION/04_packages/kernel/daemon.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more daemon-arbiter tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim automatic action execution exists if this pass only decides.
2. Do not require broad signal-type interpretation yet.
3. Preserve explicit provenance if the pass is completed by Codex under its own
   `CODE` binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the daemon-arbiter first-pass result.

## Completion Record — 2026-04-03T21:52:04-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded daemon arbitration helper, giving the active kernel one explicit next-action decision surface across active daemon signals, held reviews, unrouted questions, unissued child work, and dispatchable work.
- artifacts:
  - ION/04_packages/kernel/daemon.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_daemon.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_daemon_arbiter_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_DAEMON_ARBITER_FIRST_PASS_20260403T2149.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_daemon_arbiter_first_pass/00_trace.md
- next_action: Build the first bounded act_once helper for non-signal daemon actions, or, if signal pressure becomes dominant, build type-specific signal interpretation and stale-signal expiry first.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
