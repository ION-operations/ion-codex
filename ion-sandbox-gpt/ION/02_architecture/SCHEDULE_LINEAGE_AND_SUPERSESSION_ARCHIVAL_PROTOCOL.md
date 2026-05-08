---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T14:05:00-04:00
status: ACTIVE
purpose: Define the M10 law for compacting settled schedule lineage and supersession history without hiding authoritative records
---

# M10 — Schedule lineage and supersession archival protocol

## Purpose

M10 closes the next trust gap after schedule settlement and lawful future re-entry became real.

The system now has explicit schedule-cycle receipts, but settled cycles still accumulate as live surface noise.
M10 defines one bounded archival witness that:
- compacts settled schedule-cycle history,
- identifies the current active line when one exists,
- and preserves authoritative raw receipts without destructive deletion.

## Core law

Archival must not hide or delete authoritative schedule receipts.
It may only record which receipts are now superseded historical surface and which schedule line is currently active.

## Required behavior

M10 must:
1. read settled schedule history for one scope,
2. aggregate retired schedule/control/dispatch/completion receipts across settled lines,
3. record settlement receipts as lineage history,
4. identify the current active line from lawful future re-entry when one exists,
5. persist one schedule-lineage archive receipt,
6. expose that receipt through CLI and status.

## Outcomes

- `ARCHIVED_WITH_ACTIVE_LINE`
- `ARCHIVED_NO_ACTIVE_LINE`

## Canonical CLI route

- `python -m kernel schedule archive-lineage --scope-type ... --scope-ref ...`

## Non-goals

- deleting schedule history
- rewriting scheduler truth
- inferring hidden active lines outside the existing schedule receipt surface
