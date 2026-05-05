---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-04-09T23:10:00-04:00
status: ACTIVE
purpose: Define the first bounded allocator embodiment under explicit M0 settlement law
connections:
  - ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md
  - ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md
  - ION/06_intelligence/orchestration/2026-04-09_post_m1_state_forward_path_and_codex_handoff.md
---

# Bounded Multi-Agent Allocator Protocol

## Purpose

M1 embodies the first lawful branch allocator under the already-explicit M0 settlement law.

This protocol defines how the kernel may allocate already-issued child work units under one committed parent without widening packet bounds, bypassing capability law, or pretending merge/settlement is already solved.

## Core claim

The allocator is allowed to:
- discover child work units by explicit `parent_work_unit_id` relation,
- assess whether each child is dispatchable under scheduler law,
- bind a lawful carrier/executor through the executor capability registry,
- enforce concurrency and write-conflict boundaries,
- and persist explicit active branch-claim receipts.

The allocator is **not** allowed to:
- invent new child work,
- silently widen packet bounds,
- auto-merge returns,
- or treat branch fan-out as autonomous execution.

## Eligibility floor

A candidate child may only be considered when:
- the parent work unit exists,
- the parent work unit is `COMMITTED`,
- the child exists as an already-issued work unit,
- the child is linked to the parent by `parent_work_unit_id`,
- the child is dispatchable under scheduler law,
- and the child does not already hold an active claim receipt.

## Allocation order

For each candidate child, the allocator must apply the following gates in order:
1. active-claim exclusion,
2. scheduler dispatchability,
3. executor-capability binding,
4. effective capacity check,
5. overlapping-write exclusion,
6. max-branches cap.

The selected claim set is the lawful bounded fan-out surface for that parent at that moment.

## Capability binding

Capability selection remains subordinate to L1 executor law.

The allocator may prefer a carrier heuristically from the work-unit chassis, but explicit executor capability records outrank hidden carrier intuition.

For child allocation, identity matching should favor the child executor identity itself rather than broad chassis aliases so that named child roles do not collapse into the first matching worker.

## Claim receipts

Successful selection must persist one `BranchClaimReceipt` per selected child.

Each receipt binds:
- parent work-unit scope,
- branch work-unit id,
- context package,
- selected carrier,
- selected executor and capability,
- allowed writes,
- requested reads,
- settlement target,
- priority,
- and any warnings or blocking refs.

These receipts are the continuity witness for bounded fan-out.

## Operator surface

The canonical operator entry points are:
- `python -m kernel allocator snapshot-children <parent_work_unit_id>`
- `python -m kernel allocator claim-children <parent_work_unit_id>`

`snapshot-children` renders the current bounded projection.

`claim-children` persists active claim receipts while returning the same selected/deferred projection that justified those receipts.

## Non-goals of M1

M1 does not implement:
- branch execution runtime,
- fan-in settlement,
- merge contracts,
- review settlement,
- stale-child controls,
- or horizon-aware parallel branch planning.

Those remain later M-phase work.

## Exit condition

M1 is complete when the kernel can lawfully produce and persist bounded branch claims for already-issued children under one committed parent, with explicit capacity and write-conflict controls, and expose that behavior through the canonical operator surface with green proof.
