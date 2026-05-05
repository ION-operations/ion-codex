---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T21:56:20-04:00
from: Sovereign
target: ION/04_packages/kernel/daemon_actions.py
depends_on: ION/04_packages/kernel/daemon.py
status: COMPLETE
updated: 2026-04-03T21:58:04-04:00
completed_by: Codex
---

# Mission: Implement the first bounded kernel daemon act_once helper

## Goal

Build the first truthful daemon action executor so the active kernel can perform
exactly one arbiter-selected non-signal action when the underlying runtime helper
already exists, while refusing unsupported signal and review actions explicitly.

## Source / Context

- `ION/04_packages/kernel/daemon.py`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/children.py`
- `ION/04_packages/kernel/dispatch.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Combine arbitration plus one execution step.
3. Support only actions the current stack can already perform lawfully.
4. Make unsupported top-priority actions explicit rather than faking them.
5. Export the actuator surface from the kernel package.
6. Add focused tests for dispatch, question routing, child issuance, idle, and
   unsupported signal/review actions.

## Deliverables

- new `ION/04_packages/kernel/daemon_actions.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more daemon-action tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim a full daemon loop exists.
2. Do not fake signal semantics or review escalation.
3. Preserve explicit provenance if the pass is completed by Codex under its own
   `CODE` binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the daemon act_once first-pass result.

## Completion Record — 2026-04-03T21:58:04-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded non-signal daemon act_once helper, allowing the kernel to execute one arbiter-selected non-signal action across question routing, child-work issuance, dispatch, and idle while explicitly refusing unsupported signal and review actions.
- artifacts:
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_daemon_act_once_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_DAEMON_ACT_ONCE_FIRST_PASS_20260403T2155.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_daemon_act_once_first_pass/00_trace.md
- next_action: Build signal-type interpretation plus stale-signal expiry, then either support signal consumption inside act_once or add a higher-order repeat-until-blocked loop.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
