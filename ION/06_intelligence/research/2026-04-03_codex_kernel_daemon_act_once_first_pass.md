---
type: research
from: Codex
created: 2026-04-03T21:55:34-04:00
status: COMPLETE
topic: First bounded non-signal daemon act_once slice
connections:
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/05_context/inbox/codex_kernel_daemon_act_once_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_daemon_act_once_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_daemon_arbiter_first_pass.md
---

# Codex Kernel Daemon Act Once First Pass

## Why this exists

The active kernel now had a daemon arbiter that could choose the next highest-priority
lawful action, but it still could not actually perform even one step from that
decision surface.

This pass adds the first truthful action executor.

## Sources or surfaces considered

- `ION/04_packages/kernel/daemon.py`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/children.py`
- `ION/04_packages/kernel/dispatch.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_daemon_actions.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/daemon_actions.py` now provides the first bounded
  non-signal daemon executor for the active kernel stack.
- The helper introduces:
  `KernelDaemonActuator`, `IonDaemonActuator`, `DaemonActOnceStatus`,
  `DaemonActOnceResult`, and `KernelDaemonActionError`.
- The executor intentionally supports only the non-signal actions the stack already
  knows how to perform lawfully:
  - `ROUTE_OPEN_QUESTIONS`
  - `ISSUE_CHILD_WORK`
  - `DISPATCH_WORK`
  - `IDLE`
- The executor intentionally refuses the actions that still lack truthful runtime
  machinery:
  - `CONSUME_ACTIVE_SIGNAL`
  - `ESCALATE_REVIEW`
- This is a deliberate boundary, not a bug. The current stack can see those
  pressures, but it does not yet have honest execution semantics for them.
- `act_once(...)` now combines:
  - daemon arbitration
  - selection of the chosen action
  - one bounded execution step when the chosen action is already supported
- The executor reuses the existing kernel helpers directly rather than inventing
  a shadow path:
  - open-question routing uses `KernelQuestionRouter`
  - child-work issuance uses `KernelChildWorkIssuer`
  - dispatch uses `KernelDispatcher`
- `ION/tests/test_kernel_daemon_actions.py` proves:
  - dispatch execution works and can write a dispatch packet
  - routed open questions are persisted from an arbiter-selected action
  - child work is issued from an arbiter-selected action
  - idle state remains explicit and clean
  - active daemon signals are marked unsupported rather than faked
  - held-review escalation is marked unsupported rather than faked
- The combined kernel suite is now at **96 passing tests**.

## Boundary

- This is not the full daemon loop.
- It does not yet execute signal consumption or semantic signal routing.
- It does not yet perform review escalation.
- It does not yet iterate until quiescence.
- It performs one bounded step only.

## Implications

- The active kernel can now not only decide a lawful next non-signal action, but
  actually perform one.
- The daemon stack has crossed from passive decision support into bounded execution.
- The unsupported cases are now explicit, which sharply defines the next runtime
  build pressure instead of leaving it ambiguous.

## Recommended next moves

- Build the first bounded signal-type interpretation layer plus stale-signal expiry.
- Then either:
  - support `CONSUME_ACTIVE_SIGNAL` inside `act_once`, or
  - build a higher-order loop that repeatedly arbitrates and executes supported
    actions until only unsupported or idle pressure remains.
