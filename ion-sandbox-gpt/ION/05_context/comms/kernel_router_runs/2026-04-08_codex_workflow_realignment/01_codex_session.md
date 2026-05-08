---
type: role_session
template: ROLE_SESSION
created: 2026-04-08T23:50:35+00:00
status: COMPLETE
workstream: implementation
role: codex
objective: restore canonical workflow clarity and add end-to-end rehearsal proof
source_task: ION/06_intelligence/research/2026-04-08_end_to_end_workflow_rehearsal.md
next_role: vizier
updated: 2026-04-08T23:50:35+00:00
---

# Role Session: codex

## Role

codex

## Purpose

classify the task and prepare the scoped implementation route

## Source Task / Objective

- objective: restore canonical workflow clarity and add end-to-end rehearsal proof
- source_task: ION/06_intelligence/research/2026-04-08_end_to_end_workflow_rehearsal.md

## Required Reads

- codex.boot: ION/03_registry/boots/CODEX.boot.md
- codex.private_mini: ION/agents/codex/MINI.md
- codex.private_capsule: ION/agents/codex/CAPSULE.md
- codex.directive.1: ION/01_doctrine/CANONICAL_WORKFLOW.md
- codex.directive.2: ION/AGENT_CONTRACT.md
- codex.directive.3: ION/SYSTEM_MAP.md
- codex.inbox: ION/05_context/inbox/codex_* [optional]
- codex.signals: ION/05_context/signals
- codex.projection.MINI.md: ION/MINI.md [optional]
- codex.projection.STATUS.md: ION/STATUS.md [optional]
- codex.projection.CAPSULE.md: ION/CAPSULE.md [optional]

## Expected Output

- Produce the codex pass for the bounded `implementation` objective.
- Preserve provenance explicitly if any cross-role judgment is made.
- Update only the artifacts that the governing task or lane actually permits.

## Next Target

- next_role: vizier

## Notes

- This is a generated sequential-kernel session scaffold, not a claim that the role pass already happened.

## Status Update — 2026-04-08T23:50:35+00:00

- status: COMPLETE
- operator: Codex
- summary: Restored the canonical workflow doctrine, executor contract, system map, and workflow rehearsal center.
- artifacts:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/SYSTEM_MAP.md
  - ION/06_intelligence/audits/2026-04-08_workflow_module_alignment_audit.md
  - ION/06_intelligence/research/2026-04-08_codex_workflow_realignment_reasoning_journal.md
  - ION/tests/test_kernel_workflow_rehearsal.py
- next_action: Have Vizier/Mason/Nemesis read the new workflow doctrine and judge remaining ambiguity by exact module mapping.
- note: This bundle exists to prove self-use of the router/session/handoff surfaces during the repair pass.
