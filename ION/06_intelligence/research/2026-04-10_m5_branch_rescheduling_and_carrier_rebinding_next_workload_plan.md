---
type: next_workload_plan
authority: A3_OPERATIONAL
created: 2026-04-10T06:26:00-04:00
status: ACTIVE
purpose: Define the next workload after M4 branch-aware horizon / schedule synchronization
---

# M5 next workload plan — branch-aware rescheduling / carrier rebinding

## Why M5 is next

M4 makes branch posture return into parent future state.

The next trust gap is whether the schedule can now adapt lawfully when synchronized branch futures shift:
- different branch outcomes may change the best carrier,
- active/deferred branch posture may require reassignment,
- and the parent future queue may need explicit rebinding without changing the underlying workflow.

## Goal

Land one bounded M5 surface for:
- rescheduling after branch-state change,
- lawful carrier / executor rebinding after synchronization,
- and explicit receipts for that rebinding decision.

## Required outcomes

- branch-aware scheduler reconsideration after M4 sync
- explicit rebinding / reassignment receipt or schedule witness
- no hidden carrier switching
- focused rehearsal proving synchronized branch futures can alter carrier choice lawfully

## Non-goals

- free-form autonomous swarm management
- unconstrained branch replanning
- hidden executor substitution outside explicit scheduler law
