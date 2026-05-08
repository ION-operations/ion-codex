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
created: 2026-04-04T14:45:00-04:00
payload:
  artifact: ION/06_intelligence/research/2026-04-04_codex_kernel_queue_projection_and_planner_housekeeping_first_pass.md
  summary: "Persisted reviewer-facing answer queues as durable generated-state projection records, added daemon-maintained planner-manifest housekeeping for due expiry/cancellation, and widened loop telemetry to witness maintenance steps; full suite now passes at 143 tests."
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
    - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_queue_projection_and_planner_housekeeping_first_pass/00_trace.md
---
The active kernel now persists reviewer-facing answer queues as generated-state witness and can maintain due/stale planner manifests lawfully before child issuance.
