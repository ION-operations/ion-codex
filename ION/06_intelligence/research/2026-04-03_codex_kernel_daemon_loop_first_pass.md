---
type: research
from: Codex
created: 2026-04-03T22:21:03-04:00
status: COMPLETE
topic: First bounded higher-order daemon loop
connections:
  - ION/04_packages/kernel/daemon_loop.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_daemon_loop.py
  - ION/05_context/inbox/codex_kernel_daemon_loop_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_daemon_loop_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_daemon_signal_consumption_first_pass.md
---

# Codex Kernel Daemon Loop First Pass

## Why this exists

The active kernel could already arbitrate the next daemon action and execute one
bounded supported step, but it still had no truthful higher-order loop.

This pass adds the smallest honest loop the current stack can support today:
repeat arbitration plus supported execution until the runtime reaches idle,
encounters unsupported pressure, or hits an explicit safety cap.

## Sources or surfaces considered

- `ION/04_packages/kernel/daemon.py`
- `ION/04_packages/kernel/daemon_actions.py`
- `ION/04_packages/kernel/signals.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_daemon_loop.py`
- `ION/tests/test_kernel_daemon_actions.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/daemon_loop.py` now provides:
  - `DaemonLoopStatus`
  - `DaemonLoopResult`
  - `KernelDaemonLoop`
  - `IonDaemonLoop`
  - `KernelDaemonLoopError`
- `run_until_blocked(...)` now repeats `act_once(...)` and stops only on:
  - `IDLE`
  - `BLOCKED_UNSUPPORTED`
  - `MAX_STEPS_REACHED`
- The loop deliberately reuses the current daemon stack rather than creating a
  shadow runtime path:
  - arbitration still comes from `KernelDaemonArbiter`
  - one-step execution still comes from `KernelDaemonActuator`
- This means the loop inherits the current truthful boundaries automatically:
  - signal consumption works
  - question routing works
  - child-work issuance works
  - dispatch works
  - review escalation is still unsupported
- `ION/tests/test_kernel_daemon_loop.py` now proves:
  - the loop can consume a signal, dispatch work, and then reach idle
  - the loop stops explicitly when review escalation becomes the top unsupported pressure
  - the loop respects a max-step cap instead of overclaiming autonomy
- The combined kernel suite is now at **105 passing tests**.

## Boundary

- This is not full daemon sovereignty.
- It does not yet execute unsupported review escalation.
- It does not yet automatically perform the recommended follow-up after signal consumption.
- It is still a bounded in-process loop, not a long-running service.

## Implications

- The daemon stack now has its first honest repeat-until-blocked surface.
- The kernel can now advance through multiple lawful runtime pressures in one visible run.
- The remaining unsupported gaps are cleaner than before because they now appear
  as explicit loop termination conditions rather than ambient incompleteness.

## Recommended next moves

- Decide whether the next unsupported branch to land should be:
  - held-review escalation
  - or signal-triggered follow-up automation beyond acknowledgement
- After that, consider whether the loop should gain:
  - durable loop receipts
  - or explicit per-step runtime telemetry beyond the current bundle/provenance surfaces
