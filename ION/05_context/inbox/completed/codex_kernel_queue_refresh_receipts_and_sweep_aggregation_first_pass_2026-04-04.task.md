---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-04T17:25:00-04:00
from: Sovereign
target: ION/04_packages/kernel/question_answers.py
depends_on: ION/04_packages/kernel/planner_gate.py
status: COMPLETE
updated: 2026-04-04T17:25:00-04:00
completed_by: Codex
---

# Mission: Persist reviewer-queue refresh receipts and aggregate retained planner sweeps

## Goal

Take the next generated-state witness questions left by Codex MINI and land the smallest
truthful kernel slices that answer them:

1. give stale reviewer-queue refresh its own durable receipt/topology lane rather than leaving it only in refreshed projections and loop telemetry
2. give retained planner-manifest sweep receipts a bounded aggregation helper so housekeeping witness can be summarized before any richer retry compiler is attempted

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
2. Do not claim a broader reviewer runtime or retry compiler already exists.
3. Persist queue-refresh witness as generated-state receipt/topology rather than only mutating queue projections.
4. Keep planner-sweep aggregation bounded to a retained receipt window; do not delete receipts.
5. Let the daemon surface/execute the new bounded witness-maintenance paths without jumping ahead into richer planning law.
6. Add focused tests for queue-refresh receipts, sweep aggregation, daemon arbitration, and daemon act-once execution.

## Deliverables

- widened `question_answers.py` with durable reviewer-queue refresh sweep receipts
- widened `model.py` / `store.py` / `index.py` / `graph.py` with `reviewer_queue_refresh` plus `planner_manifest_sweep_aggregate` witness families
- widened `planner_gate.py` with retained sweep-receipt aggregation helpers
- widened `daemon.py` / `daemon_actions.py` / `daemon_loop.py` to surface and witness queue-refresh sweeps plus sweep aggregation
- focused tests plus one research note and one Codex signal

## Constraints

1. Do not turn generated-state receipts into the authority surface.
2. Do not discard sweep receipts during aggregation.
3. Preserve the rule that child issuance still flows through explicit planner manifests.
4. Preserve explicit provenance that this slice was completed by Codex under the active `CODE` binding.

## Completion Record — 2026-04-04T17:25:00-04:00

- status: COMPLETE
- operator: Codex
- summary: Added durable reviewer-queue refresh receipts plus topology, added retained planner-sweep aggregation records and helpers, taught the daemon to surface/execute queue-refresh sweeps and sweep aggregation, widened loop telemetry to witness the new receipt families, and raised the combined kernel suite to 156 passing tests.
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
  - ION/06_intelligence/research/2026-04-04_codex_kernel_queue_refresh_receipts_and_sweep_aggregation_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_QUEUE_REFRESH_RECEIPTS_AND_SWEEP_AGGREGATION_FIRST_PASS_20260404T1725.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_queue_refresh_receipts_and_sweep_aggregation_first_pass/00_trace.md
- verification:
  - `PYTHONPATH=04_packages pytest -q tests/test_kernel_question_answers.py tests/test_kernel_planner_gate.py tests/test_kernel_daemon.py tests/test_kernel_daemon_actions.py`
  - `PYTHONPATH=04_packages pytest -q`
- next_action: Decide whether reviewer-queue refresh receipts need their own retained aggregation window, then decide whether planner-sweep aggregates should gain daemon-maintained refresh / retention policy before any richer retry-compiler work lands.
