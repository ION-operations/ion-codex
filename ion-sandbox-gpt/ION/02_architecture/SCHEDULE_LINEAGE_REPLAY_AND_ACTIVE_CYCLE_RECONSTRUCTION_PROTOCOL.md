---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T15:20:00-04:00
status: ACTIVE
purpose: Define the M11 law for replaying archived schedule lineage into one explicit active-cycle reconstruction witness without mutating authoritative history
---

# M11 — Schedule lineage replay and active-cycle reconstruction protocol

## Purpose

M10 compacted settled schedule history into one archival witness.

M11 closes the next trust gap:
- an operator should not need to scan raw schedule receipts manually to understand the currently active cycle,
- and replay should not mutate archived history to achieve that understanding.

M11 therefore defines one bounded replay surface that reads the latest schedule-lineage archive and reconstructs the active cycle from lawful witness.

## Core law

Replay is interpretive witness, not hidden mutation.

M11 must:
- read the latest schedule-lineage archive for one scope,
- recover the active schedule line when one exists,
- follow the witnessed schedule -> dispatch -> completion -> settlement chain when present,
- and persist one replay receipt describing the current active-cycle stage.

M11 must not:
- rewrite archived history,
- mutate schedule state,
- or invent a second schedule authority plane.

## Minimum stages

The bounded reconstruction must support at least:
- `NO_ACTIVE_CYCLE`
- `ACTIVE_SCHEDULED`
- `ACTIVE_DISPATCHED`
- `ACTIVE_COMPLETED_AWAITING_SETTLEMENT`
- `ACTIVE_CYCLE_ALREADY_SETTLED`

## Operator surface

Canonical CLI route:
- `python -m kernel schedule replay-lineage ...`

Status must expose:
- latest `schedule_lineage_replay_receipt`
