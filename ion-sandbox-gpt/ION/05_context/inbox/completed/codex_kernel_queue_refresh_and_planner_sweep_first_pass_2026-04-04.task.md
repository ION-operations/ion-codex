---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-04T15:40:00-04:00
from: Sovereign
target: ION/04_packages/kernel/question_answers.py
depends_on: ION/04_packages/kernel/planner_gate.py
status: COMPLETE
updated: 2026-04-04T16:05:00-04:00
completed_by: Codex
---

# Mission: Add daemon-maintained queue refresh and planner-manifest sweep receipts

## Goal

Take the next two Codex MINI generated-state/runtime questions and land them as truthful
bounded kernel surfaces:

1. give durable reviewer-facing answer queues bounded refresh helpers plus a lawful daemon-maintained refresh path when projections go stale
2. give planner-manifest housekeeping a broader sweep receipt/topology path once the one-manifest maintenance step has proven out

## Source / Context

- `ION/03_registry/boots/CODEX.boot.md`
- `ION/agents/codex/MINI.md`
- `ION/agents/codex/CAPSULE.md`
- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/graph.py`
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
2. Do not claim a full reviewer daemon or retry compiler already exists.
3. Refresh reviewer-queue projections only when current runtime state proves they are stale.
4. Keep planner-manifest sweeps as bounded housekeeping over current maintenance candidates.
5. Persist sweep evidence as durable generated-state witness rather than burying it only in step-local telemetry.
6. Preserve the rule that child issuance still flows through explicit planner manifests rather than direct signal authority.
7. Add focused tests for queue refresh plus planner sweep behavior.

## Deliverables

- widened `question_answers.py` with stale-projection discovery plus single/batch refresh helpers
- widened daemon arbitration/action support for stale reviewer-queue refresh
- widened model/store/index/graph support for durable `planner_manifest_sweep` receipts
- widened `planner_gate.py` with bounded sweep execution
- widened daemon telemetry for queue refresh and planner sweeps
- focused tests plus one research note and one Codex signal

## Constraints

1. Do not turn reviewer-queue projections into the authority surface.
2. Do not let sweep maintenance silently discard manifest evidence.
3. Keep sweep behavior bounded to already-discovered candidates.
4. Preserve explicit provenance that this slice was completed by Codex under the active `CODE` binding.

## Completion Record — 2026-04-04T16:05:00-04:00

- status: COMPLETE
- operator: Codex
- summary: Added stale reviewer-queue discovery plus bounded refresh helpers, taught the daemon to surface and execute stale queue refresh, persisted planner-manifest sweep receipts as generated-state witness with graph/index/store support, widened planner housekeeping into a bounded sweep path, and widened loop telemetry to record refresh/sweep steps.
- artifacts:
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/graph.py
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
  - ION/06_intelligence/research/2026-04-04_codex_kernel_queue_refresh_and_planner_sweep_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_QUEUE_REFRESH_AND_PLANNER_SWEEP_FIRST_PASS_20260404T1605.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_queue_refresh_and_planner_sweep_first_pass/00_trace.md
- verification:
  - `PYTHONPATH=04_packages pytest -q tests/test_kernel_question_answers.py tests/test_kernel_planner_gate.py tests/test_kernel_daemon.py tests/test_kernel_daemon_actions.py`
  - `PYTHONPATH=04_packages pytest -q`
- next_action: Decide whether reviewer-queue refresh should emit durable refresh receipts/topology or remain projection-only until a broader reviewer runtime exists, then decide whether planner-manifest sweep receipts need retention/aggregation helpers before richer retry-compiler work lands.
