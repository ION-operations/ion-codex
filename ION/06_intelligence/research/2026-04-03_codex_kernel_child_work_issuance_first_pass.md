---
type: research
from: Codex
created: 2026-04-03T21:39:05-04:00
status: COMPLETE
topic: First bounded child-work issuance slice
connections:
  - ION/04_packages/kernel/children.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_children.py
  - ION/05_context/inbox/codex_kernel_child_work_issuance_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_child_work_issuance_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md
  - ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_validation_receipt_signal_first_pass.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_signal_consumption_archive_first_pass.md
---

# Codex Kernel Child-Work Issuance First Pass

## Why this exists

The active kernel stack could now validate deltas, apply accepted artifacts, route
open questions, emit receipts/signals, and archive consumed signals, but it still did
not do anything with accepted `proposed_child_work_units`. Child intent existed in the
schema and in live `CommitDelta` objects, but no daemon-side helper turned that intent
into real schedulable state.

This pass adds that missing issuance bridge.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/context_compiler.py`
- `ION/04_packages/kernel/dispatch.py`
- `ION/04_packages/kernel/validation.py`
- `ION/04_packages/kernel/graph.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_children.py`
- `ION/06_intelligence/specs/T02_WorkUnitSchema.spec.md`
- `ION/06_intelligence/specs/T04_CommitDeltaSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/children.py` now provides the first bounded child-work
  issuance helper for the active kernel stack.
- The helper introduces:
  `KernelChildWorkIssuer`, `IonChildWorkIssuer`, `KernelChildWorkIssuanceError`,
  `ChildAgentBinding`, `PreparedChildWork`, `ChildWorkIssuancePreparation`, and
  `ChildWorkIssuanceResult`.
- The issuer intentionally operates only on parent deltas already in
  `ACCEPTED` or `ACCEPTED_AS_WITNESS`, and only when the parent work unit is already
  `COMMITTED`. That keeps the first pass on the truthful post-validation side of the
  loop rather than inventing speculative pre-commit branching.
- Spawn policy is now materially enforced in runtime behavior rather than remaining
  only as schema text:
  - `may_spawn=False` rejects child issuance
  - `spawn_requires_approval=True` rejects child issuance
  - `max_children` is enforced when set
  - `spawn_templates` are enforced when present
- Each accepted `ChildSpec` now becomes:
  - one real child `WorkUnit`
  - one real compiled child `ContextPackage`
- Child lineage is preserved explicitly:
  - `parent_work_unit_id` is set on the child work unit
  - the parent work unit is also recorded as a dependency, which is already resolved
    once the parent is committed
  - the rebuilt graph then exposes the lineage via `SPAWNS_CHILD`
- The child issuer does not bypass the existing runtime:
  - issued children enter the store/index/graph as normal `PENDING` work units
  - the live scheduler can then assess them with no new special case
  - dispatch remains unchanged and still requires a matching compiled context package
- The issuer compiles child context honestly rather than creating placeholder work:
  - target files are resolved from an explicit repo root
  - existing files are read directly
  - missing file targets with a file suffix are allowed as empty file targets
  - directory targets become a small directory-manifest target file
- `ION/tests/test_kernel_children.py` proves:
  - accepted child intent becomes persisted child work plus compiled context
  - spawned lineage appears in the graph
  - the live scheduler sees the new child work as dispatchable once issued
  - spawn-policy refusal and `max_children` refusal both work
- The combined kernel suite is now at **84 passing tests**.

## Boundary

- This is not the full daemon planner.
- It does not yet compute child transitions from a broader protocol registry.
- It does not yet interpret child intent from canonical JSON signals.
- It does not yet auto-dispatch newly issued children.
- It does not yet generate multi-child routing strategies from open-question state.
- It still assumes explicit doctrine input rather than a resolved doctrine registry.

## Implications

- The active kernel now has a truthful first bridge from accepted follow-up intent
  into new schedulable work.
- `ChildSpec` is no longer dead schema. It now changes runtime state.
- Spawn policy is now partially real in runtime behavior rather than only modeled in
  types and specs.
- The kernel loop is closer to the canonical transition form because accepted work can
  now lawfully issue bounded next work without falling back to ad hoc inbox writing.

## Recommended next moves

- Build the first bounded interpreter that turns canonical consumed signals into
  follow-up runtime actions where appropriate.
- Or, if staying closer to the core transition loop is more valuable, build the next
  bounded daemon decision helper that chooses between dispatching newly issued child
  work, resolving open questions, or escalating held validations.
