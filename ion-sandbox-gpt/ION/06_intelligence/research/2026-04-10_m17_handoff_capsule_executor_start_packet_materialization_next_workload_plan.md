---
type: next_workload_plan
authority: A3_OPERATIONAL
created: 2026-04-10T23:27:00-04:00
status: ACTIVE
purpose: Define the next workload after M16 handoff-capsule executor-entry rehearsal
---

# M17 next workload plan — handoff-capsule executor-start packet materialization

## Why M17 is next

M16 proves a fresh executor can enter directly from the compact handoff capsule.

The next trust gap is whether that successful rehearsal can become one explicit executor-start packet without manual reinterpretation.

## Goal

Land one bounded M17 surface for:
- materializing one executor-start packet from a successful M16 rehearsal,
- preserving linkage back to the capsule / activation / continuation chain,
- and persisting one executor-start materialization receipt.

## Required outcomes

- executor-start packet materialized only from successful rehearsal
- explicit success/failure witness
- no hidden continuation expansion beyond the rehearsed capsule entry path

## Non-goals

- new planner behavior
- autonomous dispatch widening
- shadow continuation systems
