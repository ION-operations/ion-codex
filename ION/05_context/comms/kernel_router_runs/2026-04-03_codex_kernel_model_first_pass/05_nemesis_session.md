---
type: role_session
template: ROLE_SESSION
created: 2026-04-03T17:57:21-04:00
status: COMPLETE
workstream: implementation
role: nemesis
objective: implement the first lawful kernel model slice
source_task: ION/05_context/inbox/codex_kernel_model_first_pass_2026-04-03.task.md
updated: 2026-04-03T17:59:50-04:00
---

# Role Session: nemesis

## Role

nemesis

## Purpose

audit or verify when the slice becomes release-sensitive

## Source Task / Objective

- objective: implement the first lawful kernel model slice
- source_task: ION/05_context/inbox/codex_kernel_model_first_pass_2026-04-03.task.md

## Required Reads

- nemesis.boot: ION/03_registry/boots/NEMESIS.boot.md
- nemesis.private_mini: ION/agents/nemesis/MINI.md
- nemesis.private_capsule: ION/agents/nemesis/CAPSULE.md [optional]
- nemesis.directive.1: ION/01_doctrine/SOVEREIGN_KERNEL.md
- nemesis.signals: ION/05_context/signals
- nemesis.projection.MINI.md: ION/MINI.md [optional]
- nemesis.projection.STATUS.md: ION/STATUS.md [optional]
- nemesis.projection.CAPSULE.md: ION/CAPSULE.md [optional]

## Expected Output

- Produce the nemesis pass for the bounded `implementation` objective.
- Preserve provenance explicitly if any cross-role judgment is made.
- Update only the artifacts that the governing task or lane actually permits.

## Next Target

- next_role: none

## Notes

- This is a generated sequential-kernel session scaffold, not a claim that the role pass already happened.

## Status Update — 2026-04-03T17:59:50-04:00

- status: COMPLETE
- operator: Codex
- summary: Audited the first pass against the current spec floor and verified the combined sequential-kernel and model-layer test suite passes.
- artifacts:
  - ION/tests/test_sequential_kernel.py
  - ION/tests/test_kernel_model.py
- next_action: Retire the task and file the implementation witness note.
- note: Completed by Codex acting in sequential-kernel mode; this is not independent multi-chat role review.
