---
type: audit
template: AUDIT
created: 2026-04-08T19:10:00-04:00
status: ACTIVE
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/SYSTEM_MAP.md
  - ION/tests/test_kernel_workflow_rehearsal.py
---

# Audit: workflow-to-module alignment

## Judgment

The repository has a real canonical workflow substrate, but its authority presentation was too flat. The main repair needed was not to discard the recent automation work, but to remap it explicitly to the canonical loop.

## Classification

### Core workflow
- `model.py`, `store.py`, `index.py`, `graph.py`
- `context_compiler.py`, `capsule_manager.py`, `manifest_state.py`, `automation_state.py`
- `scheduler.py`, `dispatch.py`, `execution.py`, `validation.py`, `commit.py`, `governed_write.py`, `threshold.py`
- `questions.py`, `question_answers.py`, `reviews.py`, `signal_followups.py`
- `children.py`, `planner_gate.py`, `child_work_service.py`
- `recovery_replay.py`
- `external_execution_bridge.py`

### Automation carriers
- `automation_policy.py`
- `operator_control.py`
- `daemon.py`, `daemon_actions.py`, `daemon_loop.py`, `daemon_service.py`
- `operational_hardening.py`
- `sequential_kernel.py` (manual/sequential carrier rather than automatic carrier)

### Support / witness
- `runtime_reporting.py`
- every `runtime_report_*` module family
- generated ledgers, dashboards, browsers, digests, and provenance packets

## Main clarification

The automation-carrier modules are not outside the workflow. They are the workflow becoming executable under supervised runtime. The support/witness family is what should remain visibly subordinate.

## Remaining repo risks

1. Top-level planning/history files still carry too many addenda.
2. The canonical workflow was not previously visible enough at the root.
3. End-to-end proof existed in pieces, but not as one named rehearsal.
4. Agent self-use of continuity and reasoning surfaces was weaker than the workflow itself expects.

## Repair applied in this pass

1. Added a canonical workflow doctrine.
2. Added an executor contract.
3. Added a workflow-to-module system map.
4. Added a lead-dev reasoning journal.
5. Added a new workflow rehearsal integration test.
6. Generated a new sequential router run for this exact repair pass.
