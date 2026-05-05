---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T11:05:00-04:00
status: ACTIVE
purpose: Define the M7 law for reconciling schedule witness into active assignment and dispatch reality
---

# M7 — Schedule dispatch / assignment reconciliation protocol

## Purpose

M7 closes the gap between future witness and execution authority.

After M6, the kernel can:
- record schedule witness,
- refresh stale schedule witness,
- and explicitly retry or reassign future posture.

The next question is whether that refreshed witness can become actual assignment / dispatch reality without hidden executor state.

M7 therefore defines one bounded enactment surface that:
- takes the latest schedule witness for a scope,
- resolves its assignable work-unit target,
- materializes explicit assignment witness,
- dispatches when lawful,
- and retires superseded schedule-only witness once execution becomes authoritative.

## Core law

Schedule witness and execution authority are different layers.

Schedule witness proposes future action.
Execution authority begins once assignment / dispatch state becomes real.

M7 must keep that boundary explicit:
- schedule receipts are not silently treated as dispatch,
- dispatch does not silently erase prior schedule witness,
- and retirement of superseded schedule/control receipts is recorded through explicit reconciliation witness.

## Required behavior

M7 must:
1. read the latest schedule receipt for one scope,
2. optionally read the latest schedule-control and branch-reschedule witness for that same scope,
3. resolve the assignable work unit when the schedule source is a work-unit candidate,
4. increment active assignments on the bound executor capability when assignment becomes real,
5. dispatch the work unit when it is lawfully pending,
6. record a durable schedule-dispatch reconciliation receipt,
7. and mark schedule witness as retired once dispatch / execution reality is authoritative.

## Outcome mapping

Minimum bounded actions:
- pending work unit + lawful selected capability -> `DISPATCHED_AND_ASSIGNED`
- pending work unit + no selected capability -> `DISPATCHED`
- already dispatched/executing/validating work unit -> `EXECUTION_ALREADY_AUTHORITATIVE`
- schedule source does not resolve to an assignable work unit -> `NO_ASSIGNABLE_WORK_UNIT`
- work unit exists but is not ready for dispatch -> `ASSIGNMENT_DEFERRED`

## Persistence family

M7 uses:
- `schedule_dispatch_reconciliation_receipt`

## Operator surface

Canonical CLI route:
- `python -m kernel schedule reconcile ...`

Status must expose:
- latest schedule-dispatch reconciliation receipt

## Non-goals

M7 does not:
- close the assignment lifecycle,
- release capability assignments on execution completion,
- infer completion from dispatch alone,
- or invent hidden execution state outside the work unit + receipt surfaces.

## Acceptance standard

M7 is complete only when:
- schedule witness can become explicit assignment / dispatch witness,
- a bound executor capability increments active assignments when used,
- dispatch authority retires superseded schedule-only witness explicitly,
- and focused proof shows this behavior through both unit and CLI/status paths.
