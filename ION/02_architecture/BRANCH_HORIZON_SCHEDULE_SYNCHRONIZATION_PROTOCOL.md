---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T06:15:00-04:00
status: ACTIVE
purpose: Define the M4 law for returning bounded branch posture into parent-scope horizon and scheduler state without creating a shadow planner
---

# M4 — Branch-aware horizon / schedule synchronization protocol

## Purpose

M4 closes the gap after bounded fan-out, bounded fan-in, and bounded branch control became real.

The problem is no longer whether branching can be bounded locally.
The problem is whether branch posture returns coherently into the parent future field.

M4 therefore defines one bounded return path from:
- branch claims,
- branch control posture,
- and branch settlement outcomes

back into:
- parent-scope horizon state,
- parent-scope scheduler projection,
- and durable synchronization witness.

## Core law

Branch outcomes must not remain trapped inside branch-local receipts.

Once bounded branch posture materially changes what the parent should do next, that change must return into the same future law that governs non-branch work.

This return path must:
- remain subordinate to kernel law,
- write one authoritative parent-scope horizon posture,
- use the existing scheduler surface,
- and persist explicit synchronization witness.

It must not create:
- a second planner,
- a hidden branch scheduler,
- or branch-only future semantics detached from canonical horizon/schedule law.

## Inputs

M4 reads:
- active branch claim receipts,
- latest branch-control receipt when present,
- latest branch-settlement receipt when present,
- parent work-unit scope,
- existing parent-scope horizon state,
- and the current scheduler projection surface.

## Required behavior

M4 must:

1. derive the current parent future posture from bounded branch state,
2. translate that posture into one parent-scope horizon record,
3. keep only the synchronized layer authoritative for that parent scope,
4. project the synchronized future through the existing scheduler surface,
5. persist one schedule receipt when a candidate is selected,
6. persist one branch-horizon synchronization receipt,
7. expose the latest synchronization receipt through operator status and CLI.

## Outcome mapping

The minimum bounded mapping is:

- settlement accepted as-is
  - parent horizon becomes IMMEDIATE
  - packet-ready resume-parent step
- settlement merge proposal required
  - parent horizon becomes IMMEDIATE
  - packet-ready merge-resolution step
- settlement escalates review
  - parent horizon becomes IMMEDIATE
  - packet-ready review escalation step
- settlement deferred
  - parent horizon becomes NEAR
  - non-ready waiting step with dependencies
- settlement abandoned
  - parent horizon becomes FAR
  - weak future pressure only
- stale returns present
  - parent horizon becomes IMMEDIATE
  - explicit review-bearing step
- active branch claims without settlement
  - parent horizon becomes NEAR
  - structured future pressure only
- no active branch pressure
  - parent horizon becomes FAR
  - weak future posture only

## Persistence families

M4 uses:
- `horizon_state`
- `schedule_receipt`
- `branch_horizon_sync_receipt`

## Operator surface

Canonical CLI route:
- `python -m kernel allocator sync-future-posture ...`

Status must expose:
- latest branch-horizon synchronization receipt

## Non-goals

M4 does not:
- autonomously widen the branch tree,
- invent new packet families,
- invent a branch-only scheduler,
- bypass review / threshold law,
- or settle unresolved branch conflicts silently.

## Acceptance standard

M4 is complete only when:
- bounded branch posture can be synchronized into parent future state,
- the synchronized horizon is discoverable through status,
- the schedule surface reflects the synchronized parent posture,
- and focused rehearsal proves this happens without hidden planner behavior.
