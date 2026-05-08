---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-04T12:05:00-04:00
from: Sovereign
target: ION/04_packages/kernel/question_answers.py
depends_on: ION/04_packages/kernel/planner_gate.py
status: COMPLETE
updated: 2026-04-04T12:35:00-04:00
completed_by: Codex
---

# Mission: Persist answer and planner-manifest runtime state, then let the daemon consume ready planner manifests lawfully

## Goal

Take the two durability decisions that Codex MINI named next and land them as real runtime
state:

1. make explicit answer ingestion a first-class persisted record family
2. make planner/manifest linkage a first-class persisted record family beyond `CommitDelta.resolved_question_ids`

Then, because those families now exist, allow the daemon to issue child work through a
ready persisted planner manifest instead of only through raw accepted deltas.

## Source / Context

- `ION/03_registry/boots/CODEX.boot.md`
- `ION/agents/codex/MINI.md`
- `ION/agents/codex/CAPSULE.md`
- `ION/04_packages/kernel/question_answers.py`
- `ION/04_packages/kernel/planner_gate.py`
- `ION/04_packages/kernel/daemon.py`
- `ION/04_packages/kernel/daemon_actions.py`
- `ION/tests/test_kernel_question_answers.py`
- `ION/tests/test_kernel_planner_gate.py`
- `ION/tests/test_kernel_daemon.py`
- `ION/tests/test_kernel_daemon_actions.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the pass bounded and truthful.
2. Persist answer ingestion as its own runtime record family rather than only mutating `OpenQuestion` state.
3. Persist planner/manifest linkage as its own runtime record family rather than relying only on delta links.
4. Do not let signals create child work directly.
5. Only allow the daemon to issue child work through a planner manifest when that manifest is already `READY`.
6. Add focused tests covering the new durable families and the daemon manifest-consumption path.

## Deliverables

- widened kernel model/store/index/graph surfaces for answer + planner-manifest records
- widened `question_answers.py` and `planner_gate.py`
- widened daemon arbiter / actuator support for ready planner manifests
- focused tests plus one research note and one Codex signal

## Constraints

1. Do not claim a full reviewer queue, planner daemon, or retry compiler already exists.
2. Do not silently broaden signal-follow-up authority.
3. Keep planner-manifest issuance bounded to explicit child-spec deltas already on disk.
4. Preserve explicit provenance that this slice was completed by Codex under the active `CODE` binding.

## Completion Record — 2026-04-04T12:35:00-04:00

- status: COMPLETE
- operator: Codex
- summary: Added persisted `question_answer` and `planner_manifest` runtime families, widened answer ingestion and planner gate to use those families directly, then taught the daemon to prefer and execute `READY` planner manifests for child issuance while preserving the rule that signals remain pressure/evidence rather than direct child-work authority.
- artifacts:
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/graph.py
  - ION/04_packages/kernel/question_answers.py
  - ION/04_packages/kernel/planner_gate.py
  - ION/04_packages/kernel/daemon.py
  - ION/04_packages/kernel/daemon_actions.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_question_answers.py
  - ION/tests/test_kernel_planner_gate.py
  - ION/tests/test_kernel_daemon.py
  - ION/tests/test_kernel_daemon_actions.py
  - ION/06_intelligence/research/2026-04-04_codex_kernel_answer_record_and_planner_manifest_runtime_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_ANSWER_RECORD_AND_PLANNER_MANIFEST_RUNTIME_FIRST_PASS_20260404T1235.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-04_codex_kernel_answer_record_and_planner_manifest_runtime_first_pass/00_trace.md
- verification:
  - `PYTHONPATH=04_packages pytest -q tests/test_kernel_question_answers.py tests/test_kernel_planner_gate.py tests/test_kernel_store.py tests/test_kernel_index.py tests/test_kernel_graph.py tests/test_kernel_daemon.py tests/test_kernel_daemon_actions.py`
  - `PYTHONPATH=04_packages pytest -q`
- next_action: Decide whether question-answer records need reviewer-facing queue/projection surfaces beyond per-question lookup, then decide whether planner manifests need explicit cancellation/supersession plus daemon-side compilation from resolved follow-up pressure before any broader retry compiler lands.
- note: Completed by Codex under the explicit CODEX__CODE binding; this pass adds durable answer / manifest runtime state and a bounded daemon manifest-consumption path without claiming a general retry planner.
