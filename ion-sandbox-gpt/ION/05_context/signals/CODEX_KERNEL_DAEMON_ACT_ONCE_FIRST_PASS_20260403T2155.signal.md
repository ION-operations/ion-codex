---
type: signal
from: Codex
to:
  - Sovereign
  - Vizier
  - Vice
  - Nemesis
  - Mason
signal: KERNEL_ROUTER_UPDATE
status: ACTIVE
created: 2026-04-03T21:55:34-04:00
payload:
  artifact: ION/06_intelligence/research/2026-04-03_codex_kernel_daemon_act_once_first_pass.md
  summary: "Implemented the first bounded non-signal daemon act_once helper, allowing the kernel to execute one arbiter-selected non-signal action across question routing, child-work issuance, dispatch, and idle while explicitly refusing unsupported signal and review actions, and raised the combined kernel suite to 96 passing tests."
  companion_artifacts:
    - ION/04_packages/kernel/daemon_actions.py
    - ION/tests/test_kernel_daemon_actions.py
    - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_daemon_act_once_first_pass/00_trace.md
---
The active kernel can now perform one bounded non-signal daemon step instead of only
deciding what that next step should be.
