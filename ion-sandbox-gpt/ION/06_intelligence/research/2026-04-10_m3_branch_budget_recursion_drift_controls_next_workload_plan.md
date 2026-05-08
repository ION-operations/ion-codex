---
type: next_workload_plan
authority: A3_OPERATIONAL
created: 2026-04-10T00:00:00-04:00
status: ACTIVE
purpose: Define the next workload after M2 bounded fan-in / merge / review settlement embodiment
---

# M3 next workload plan — branch budget / recursion / drift controls

## Why M3 is next

M2 makes bounded fan-in real.
The next trust gap is no longer whether branches can rejoin.
It is whether branching itself remains bounded over time.

## Goal

Embodied control over:
- branch budgets,
- recursion ceilings,
- stale-claim decay,
- and anti-drift branch posture.

## Required outcomes

- explicit branch-budget record or policy surface
- recursion / re-fan-out refusal rules
- stale-claim and stale-return handling
- allocator + settlement awareness of branch budget posture
- focused M3 rehearsal proof

## Non-goals

- autonomous swarm expansion
- unconstrained branch trees
- horizon-wide speculative parallelism
