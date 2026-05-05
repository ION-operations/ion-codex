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
created: 2026-04-04T16:05:00-04:00
payload:
  artifact: ION/06_intelligence/research/2026-04-04_codex_kernel_queue_refresh_and_planner_sweep_first_pass.md
  summary: "Added stale reviewer-queue discovery plus lawful daemon refresh, added durable planner-manifest sweep receipts/topology, widened daemon telemetry to witness both paths, and raised the full kernel suite to 150 passing tests."
  companion_artifacts:
    - ION/04_packages/kernel/model.py
    - ION/04_packages/kernel/store.py
    - ION/04_packages/kernel/index.py
    - ION/04_packages/kernel/graph.py
    - ION/04_packages/kernel/question_answers.py
    - ION/04_packages/kernel/planner_gate.py
    - ION/04_packages/kernel/daemon.py
    - ION/04_packages/kernel/daemon_actions.py
    - ION/04_packages/kernel/daemon_loop.py
    - ION/tests/test_kernel_question_answers.py
    - ION/tests/test_kernel_planner_gate.py
    - ION/tests/test_kernel_daemon.py
    - ION/tests/test_kernel_daemon_actions.py
    - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_queue_refresh_and_planner_sweep_first_pass/00_trace.md
---
The active kernel now refreshes stale reviewer-queue witness lawfully and emits durable sweep evidence when broader planner-manifest housekeeping is applied.
