---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-04T13:10:00-04:00
from: Sovereign
target: ION/04_packages/kernel/question_answers.py
depends_on: ION/04_packages/kernel/planner_gate.py
status: COMPLETE
updated: 2026-04-04T13:35:00-04:00
completed_by: Codex
---

# Mission: Add reviewer-facing answer projections plus planner-manifest lifecycle and daemon-side manifest compilation

## Goal

Take the next two Codex MINI runtime questions and land them as truthful bounded kernel
surfaces:

1. give persisted `question_answer` records reviewer-facing queue/projection access beyond per-question lookup
2. give `planner_manifest` explicit lifecycle behavior (cancellation, supersession, expiry) plus a daemon-side manifest-compilation step from resolved follow-up pressure

## Source / Context

- `ION/03_registry/boots/CODEX.boot.md`
- `ION/agents/codex/MINI.md`
- `ION/agents/codex/CAPSULE.md`
- `ION/04_packages/kernel/question_answers.py`
- `ION/04_packages/kernel/planner_gate.py`
- `ION/04_packages/kernel/daemon.py`
- `ION/04_packages/kernel/daemon_actions.py`
- `ION/04_packages/kernel/daemon_loop.py`
- `ION/tests/test_kernel_question_answers.py`
- `ION/tests/test_kernel_planner_gate.py`
- `ION/tests/test_kernel_daemon.py`
- `ION/tests/test_kernel_daemon_actions.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the pass bounded and truthful.
2. Do not claim a full reviewer daemon, retry compiler, or rich manifest topology already exists.
3. Expose reviewer-facing queue/projection surfaces from persisted answer state without making them the sole authority surface.
4. Allow planner manifests to be cancelled, superseded, or explicitly expired without broadening signal authority.
5. Let the daemon compile planner manifests from resolved review/follow-up pressure before child issuance, rather than letting pressure-linked deltas issue child work directly.
6. Preserve the rule that signals remain pressure/evidence, not direct child-work authority.
7. Add focused tests for the new projection, lifecycle, and daemon-compilation behavior.

## Deliverables

- widened `question_answers.py` reviewer-facing queue/projection surface
- widened planner-manifest lifecycle and compile helpers in `planner_gate.py`
- widened daemon arbiter / actuator / loop telemetry for manifest compilation
- focused tests plus one research note and one Codex signal

## Constraints

1. Do not collapse manual authority and generated-state witness surfaces.
2. Do not let resolved pressure bypass planner manifests.
3. Keep planner-manifest expiry explicit and bounded.
4. Preserve explicit provenance that this slice was completed by Codex under the active `CODE` binding.

## Completion Record — 2026-04-04T13:35:00-04:00

- status: COMPLETE
- operator: Codex
- summary: Added reviewer-facing answer queue/projection surfaces over persisted `question_answer` records, widened planner manifests with explicit cancellation/supersession/expiry behavior, and taught the daemon to compile ready planner manifests from resolved review/follow-up pressure before child issuance while preserving the rule that signals themselves never issue child work directly.
- artifacts:
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/question_answers.py
  - ION/04_packages/kernel/planner_gate.py
  - ION/04_packages/kernel/daemon.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/daemon_loop.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_question_answers.py
  - ION/tests/test_kernel_planner_gate.py
  - ION/tests/test_kernel_daemon.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/06_intelligence/research/2026-04-04_codex_kernel_reviewer_queue_and_planner_lifecycle_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_REVIEWER_QUEUE_AND_PLANNER_LIFECYCLE_FIRST_PASS_20260404T1335.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_reviewer_queue_and_planner_lifecycle_first_pass/00_trace.md
- verification:
  - `PYTHONPATH=04_packages pytest -q tests/test_kernel_question_answers.py tests/test_kernel_planner_gate.py tests/test_kernel_daemon.py tests/test_kernel_daemon_actions.py`
  - `PYTHONPATH=04_packages pytest -q`
- next_action: Decide whether reviewer-facing answer queues should become durable generated-state projection artifacts and whether planner-manifest due-expiry/cancellation should gain daemon-actuated maintenance before any broader retry compiler lands.
- note: The prior zip-size discrepancy was traced to cache omission rather than missing source files; this pass is repackaged from the fuller tree.
