---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-04T14:20:00-04:00
from: Sovereign
target: ION/04_packages/kernel/question_answers.py
depends_on: ION/04_packages/kernel/planner_gate.py
status: COMPLETE
updated: 2026-04-04T14:45:00-04:00
completed_by: Codex
---

# Mission: Persist reviewer-queue projections and add daemon-maintained planner-manifest housekeeping

## Goal

Take the next two Codex MINI runtime questions and land them as truthful bounded kernel
surfaces:

1. turn reviewer-facing answer queues into durable generated-state projection records rather than index-only views
2. give planner-manifest expiry/cancellation a daemon-maintained housekeeping path before any broader retry compiler lands

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
2. Do not claim a full reviewer daemon, broad retry compiler, or rich planner topology already exists.
3. Persist reviewer-facing queue views as generated-state witness records without making them the authority surface.
4. Keep planner-manifest maintenance bounded to explicit expiry/cancellation housekeeping.
5. Let the daemon surface manifest-housekeeping work before child issuance when that maintenance is lawfully due.
6. Preserve the rule that signals remain pressure/evidence rather than direct child-work authority.
7. Add focused tests for persisted queue projections plus daemon-maintained manifest housekeeping.

## Deliverables

- widened model/store/index/graph support for durable reviewer-queue projection records
- widened `question_answers.py` with projection persistence helpers
- widened `planner_gate.py` with manifest-maintenance discovery/execution helpers
- widened daemon arbitration/action/telemetry for planner-manifest housekeeping
- focused tests plus one research note and one Codex signal

## Constraints

1. Do not collapse source continuity into generated-state projections.
2. Do not let due-expiry or cancellation silently delete planner-manifest evidence.
3. Keep maintenance one bounded manifest at a time.
4. Preserve explicit provenance that this slice was completed by Codex under the active `CODE` binding.

## Completion Record — 2026-04-04T14:45:00-04:00

- status: COMPLETE
- operator: Codex
- summary: Persisted reviewer-facing answer queues as durable generated-state projection records, widened the graph/index/store stack to witness those projections, added daemon-maintained planner-manifest housekeeping for due expiry/cancellation, and widened daemon telemetry so housekeeping steps are visible before child issuance.
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
  - ION/06_intelligence/research/2026-04-04_codex_kernel_queue_projection_and_planner_housekeeping_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_QUEUE_PROJECTION_AND_PLANNER_HOUSEKEEPING_FIRST_PASS_20260404T1445.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_queue_projection_and_planner_housekeeping_first_pass/00_trace.md
- verification:
  - `PYTHONPATH=04_packages pytest -q tests/test_kernel_question_answers.py tests/test_kernel_planner_gate.py tests/test_kernel_daemon.py tests/test_kernel_daemon_actions.py`
  - `PYTHONPATH=04_packages pytest -q`
- next_action: Decide whether durable reviewer-queue projections should gain batch refresh helpers or daemon-maintained refresh scheduling, then decide whether planner-manifest housekeeping should gain broader sweep receipts/topology only after the current one-manifest maintenance path proves out.
