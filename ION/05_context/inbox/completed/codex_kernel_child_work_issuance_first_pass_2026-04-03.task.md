---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T21:31:23-04:00
from: Sovereign
target: ION/04_packages/kernel/children.py
depends_on: ION/04_packages/kernel/signals.py
status: COMPLETE
updated: 2026-04-03T21:42:36-04:00
completed_by: Codex
---

# Mission: Implement the first bounded kernel child-work issuance helper

## Goal

Build the first truthful post-validation child-work issuance layer so accepted
follow-up intent in a `CommitDelta` can become real persisted child `WorkUnit`
and `ContextPackage` records without pretending the full daemon scheduler or
multi-agent runtime already exists.

## Source / Context

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/context_compiler.py`
- `ION/04_packages/kernel/dispatch.py`
- `ION/04_packages/kernel/validation.py`
- `ION/04_packages/kernel/graph.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Operate only on accepted or accepted-as-witness parent deltas.
3. Materialize real child `WorkUnit` records, not placeholders.
4. Compile and persist matching child `ContextPackage` records for each child.
5. Preserve parent lineage through `parent_work_unit_id`.
6. Respect bounded spawn policy and reject unlawful child issuance.
7. Leave dispatch unchanged; children should enter the existing scheduler path as
   normal persisted work units.
8. Export the helper surface from the kernel package.
9. Add focused tests for accepted issuance, spawn-policy limits, and scheduler /
   graph integration.

## Deliverables

- new `ION/04_packages/kernel/children.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more child-work issuance tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not invent hidden agent execution or direct child dispatch in this pass.
2. Do not create child units without a real compiled context package.
3. Preserve explicit provenance if the pass is completed by Codex under its own
   `CODE` binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the child-work issuance first-pass result.

## Completion Record — 2026-04-03T21:42:36-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded child-work issuance helper, turning accepted ChildSpec follow-up intent into real child WorkUnit and ContextPackage records with enforced spawn policy and scheduler-visible lineage.
- artifacts:
  - ION/04_packages/kernel/children.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_children.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_child_work_issuance_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_CHILD_WORK_ISSUANCE_FIRST_PASS_20260403T2139.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_child_work_issuance_first_pass/00_trace.md
- next_action: Decide whether the next bounded daemon step should be signal-type interpretation, stale-signal expiry, or a higher-order arbitration helper.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
