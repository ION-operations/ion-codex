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
created: 2026-04-04T13:35:00-04:00
payload:
  artifact: ION/06_intelligence/research/2026-04-04_codex_kernel_reviewer_queue_and_planner_lifecycle_first_pass.md
  summary: "Added reviewer-facing answer queue/projection surfaces, widened planner manifests with cancellation/supersession/expiry behavior, and taught the daemon to compile planner manifests from resolved follow-up pressure before child issuance; full suite now passes at 142 tests."
  companion_artifacts:
    - ION/04_packages/kernel/question_answers.py
    - ION/04_packages/kernel/planner_gate.py
    - ION/04_packages/kernel/daemon.py
    - ION/04_packages/kernel/daemon_actions.py
    - ION/04_packages/kernel/daemon_loop.py
    - ION/tests/test_kernel_question_answers.py
    - ION/tests/test_kernel_planner_gate.py
    - ION/tests/test_kernel_daemon.py
    - ION/tests/test_kernel_daemon_actions.py
    - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_reviewer_queue_and_planner_lifecycle_first_pass/00_trace.md
---
The active kernel now exposes reviewer-facing answer projections and planner-manifest lifecycle/compile behavior while preserving the rule that signals themselves do not issue child work directly.
