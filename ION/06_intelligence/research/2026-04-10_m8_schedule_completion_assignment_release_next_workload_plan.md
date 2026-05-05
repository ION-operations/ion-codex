---
type: next_workload_plan
authority: A3_OPERATIONAL
created: 2026-04-10T11:14:00-04:00
status: ACTIVE
purpose: Define the next workload after M7 schedule dispatch / assignment reconciliation
---

# M8 next workload plan — schedule completion / assignment release reconciliation

## Why M8 is next

M7 makes assignment and dispatch witness explicit.

The next trust gap is lifecycle closure:
- when execution completes,
- how active assignment counts are released,
- and how execution completion returns lawfully into scheduler / future posture without leaving assignments stuck.

## Goal

Land one bounded M8 surface for:
- completion-aware assignment release,
- capability active-assignment decrement under law,
- and durable completion / release witness for the schedule-execution loop.
