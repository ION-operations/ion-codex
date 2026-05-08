---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T16:30:00-04:00
status: ACTIVE
purpose: Define the M12 law for turning replayed active-cycle state into a bounded handoff / resume projection without mutating schedule state
---

# M12 — Schedule resume projection protocol

## Purpose

M12 turns replayed active-cycle state into one bounded continuation surface.

It exists to answer one operator question cleanly:
- given the replayed active cycle for one scope,
- what is the minimal lawful resume packet for the next executor?

## Core law

Replay is not enough by itself.
Another executor should not need to manually interpret lineage, schedule, dispatch, and completion receipts just to continue the current active cycle.

M12 therefore projects replayed active-cycle state into:
- one bounded resume/handoff view,
- and, when lawful, one minimal canonical packet.

This projection must:
- remain subordinate to packet law,
- avoid schedule mutation,
- avoid lineage rewriting,
- and stay scoped to one active cycle only.

## Required behavior

M12 must:
1. read the latest schedule-lineage replay receipt for a scope,
2. determine whether an active cycle is resumable,
3. when resumable, render one minimal `role_session` packet,
4. persist one `schedule_resume_projection_receipt`,
5. expose that receipt through CLI and status.

## Outcome mapping

- `ACTIVE_SCHEDULED` -> resumable role_session packet
- `ACTIVE_DISPATCHED` -> resumable role_session packet
- `ACTIVE_COMPLETED_AWAITING_SETTLEMENT` -> resumable role_session packet
- `NO_ACTIVE_CYCLE` -> no packet, explicit no-active-resume receipt
- `ACTIVE_CYCLE_ALREADY_SETTLED` -> no packet, explicit no-active-resume receipt

## Non-goals

M12 does not:
- dispatch work,
- reassign carriers,
- rewrite archival history,
- or replace context-perfect continuation proof.
