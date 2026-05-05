---
type: role_session
template: ROLE_SESSION
created: 2026-04-03T17:57:21-04:00
status: COMPLETE
workstream: implementation
role: vizier
objective: implement the first lawful kernel model slice
source_task: ION/05_context/inbox/codex_kernel_model_first_pass_2026-04-03.task.md
next_role: mason
updated: 2026-04-03T17:59:50-04:00
---

# Role Session: vizier

## Role

vizier

## Purpose

define scope, dependencies, and required review posture

## Source Task / Objective

- objective: implement the first lawful kernel model slice
- source_task: ION/05_context/inbox/codex_kernel_model_first_pass_2026-04-03.task.md

## Required Reads

- vizier.boot: ION/03_registry/boots/VIZIER.boot.md
- vizier.private_mini: ION/agents/vizier/MINI.md
- vizier.private_capsule: ION/agents/vizier/CAPSULE.md
- vizier.directive.1: ION/01_doctrine/SOVEREIGN_KERNEL.md
- vizier.inbox: ION/05_context/inbox/vizier* [optional]
- vizier.signals: ION/05_context/signals
- vizier.projection.MINI.md: ION/MINI.md [optional]
- vizier.projection.STATUS.md: ION/STATUS.md [optional]
- vizier.projection.CAPSULE.md: ION/CAPSULE.md [optional]

## Expected Output

- Produce the vizier pass for the bounded `implementation` objective.
- Preserve provenance explicitly if any cross-role judgment is made.
- Update only the artifacts that the governing task or lane actually permits.

## Next Target

- next_role: mason

## Notes

- This is a generated sequential-kernel session scaffold, not a claim that the role pass already happened.

## Status Update — 2026-04-03T17:59:50-04:00

- status: COMPLETE
- operator: Codex
- summary: Scoped the first pass to typed execution-contract objects only, explicitly leaving store/index/graph work for later phases.
- artifacts:
  - ION/04_packages/kernel/model.py
  - ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md
  - ION/06_intelligence/specs/T06_AuthorityClassSchema.spec.md
- next_action: Proceed to the Mason implementation pass.
- note: Completed by Codex acting in sequential-kernel mode; this is not independent multi-chat role review.
