---
type: next_workload_plan
authority: A3_OPERATIONAL
created: 2026-04-10T14:12:00-04:00
status: ACTIVE
purpose: Define the next workload after M10 schedule lineage and supersession archival
---

# M11 next workload plan — schedule lineage replay and active-cycle reconstruction

## Why M11 is next

M10 compacts settled schedule history into one explicit archival witness.

The next trust gap is whether the system can reconstruct the current active cycle from lineage and replay history without scanning raw schedule receipts manually.

## Goal

Land one bounded M11 surface for:
- replaying schedule-line lineage for one scope,
- reconstructing the currently active cycle from archival + active-line witness,
- and rendering that reconstruction as an explicit operator-facing kernel receipt or projection.

## Non-goals

- rewriting archived history
- hidden schedule mutation during replay
- multi-scope historical analytics beyond one bounded scope
