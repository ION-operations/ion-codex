---
type: role_session
template: ROLE_SESSION
created: 2026-04-03T18:15:19-04:00
status: COMPLETE
workstream: implementation
role: nemesis
objective: Implement the first lawful kernel graph slice
source_task: ION/05_context/inbox/codex_kernel_graph_first_pass_2026-04-03.task.md
updated: 2026-04-03T18:19:20-04:00
---

# Role Session: nemesis

## Role

nemesis

## Purpose

audit or verify when the slice becomes release-sensitive

## Source Task / Objective

- objective: Implement the first lawful kernel graph slice
- source_task: ION/05_context/inbox/codex_kernel_graph_first_pass_2026-04-03.task.md

## Required Reads

- nemesis.boot: ION/03_registry/boots/NEMESIS.boot.md
- nemesis.private_mini: ION/agents/nemesis/MINI.md
- nemesis.private_capsule: ION/agents/nemesis/CAPSULE.md [optional]
- nemesis.directive.1: ION/05_context/inbox/codex_kernel_graph_first_pass_2026-04-03.task.md
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

## Status Update — 2026-04-03T18:19:20-04:00

- status: COMPLETE
- operator: Codex
- summary: Completed the first bounded kernel graph slice in sequential-kernel mode.
- artifacts:
  - ION/04_packages/kernel/graph.py
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_graph.py
- next_action: Build the next kernel surface on top of the typed/store/index/graph stack, likely a minimal compiler helper.
- note: Completed by Codex acting as the sequential kernel router, not by independent multi-chat role execution.
