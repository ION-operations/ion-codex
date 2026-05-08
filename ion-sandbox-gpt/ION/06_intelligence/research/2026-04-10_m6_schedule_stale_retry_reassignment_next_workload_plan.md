---
type: next_workload_plan
authority: A3_OPERATIONAL
created: 2026-04-10T08:12:00-04:00
status: ACTIVE
purpose: Define the next workload after M5 branch-aware rescheduling / carrier rebinding
---

# M6 next workload plan — schedule stale / retry / reassignment controls

## Why M6 is next

M5 makes post-sync rebinding explicit.

The next trust gap is temporal and operational:
- when does a schedule receipt become stale,
- when should retry posture replace stale posture,
- and when is reassignment lawful rather than silent thrash.

## Goal

Land one bounded M6 surface for:
- stale schedule classification,
- retry / reassignment triggers,
- explicit receipts for stale or reassigned schedule posture,
- and visible operator projection of those state changes.

## Required outcomes

- explicit stale-schedule detection
- lawful retry / reassignment rules
- durable receipt witness for reassignment pressure
- no hidden churn between carriers or executors
