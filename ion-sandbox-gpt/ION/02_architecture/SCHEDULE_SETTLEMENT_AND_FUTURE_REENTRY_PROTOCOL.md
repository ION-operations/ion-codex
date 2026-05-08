---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T12:40:00-04:00
status: ACTIVE
purpose: Define the M9 law for settling completed schedule lines and reopening lawful future posture without inventing a second planner
---

# M9 — Schedule settlement and future re-entry protocol

## Purpose

M9 closes the gap after completion-aware assignment release became real.

The problem is no longer whether active assignment counts can be released.
The problem is whether a finished schedule line can:
- settle cleanly into durable history,
- retire superseded schedule witness coherently,
- and reopen future posture lawfully when completion makes the next candidate available.

## Core law

A finished schedule line must not remain suspended between execution closure and future orchestration.

M9 therefore defines one bounded settlement point that:
- reads latest completion-release witness,
- records retirement / supersession context for the finished line,
- and only when warranted records one fresh schedule receipt through the existing scheduler surface.

M9 must not:
- invent a second planner,
- enqueue hidden follow-up work,
- or silently overwrite settled schedule history.

## Required behavior

M9 must:
1. read the latest completion-release receipt for a scope,
2. classify whether the schedule line can settle now,
3. record superseded schedule/control/dispatch/completion witness ids,
4. persist one schedule-settlement receipt,
5. optionally persist one fresh schedule receipt when a lawful next candidate exists,
6. expose this through CLI and status.

## Outcome mapping

Minimum bounded mapping:
- terminal completion with no next candidate -> `SETTLED_NO_FUTURE_REENTRY`
- terminal completion with next candidate -> `SETTLED_WITH_FUTURE_REENTRY`
- deferred completion release -> `SETTLEMENT_DEFERRED`

## Persistence families

M9 uses:
- `schedule_completion_release_receipt`
- `schedule_settlement_receipt`
- optionally `schedule_receipt` for future re-entry

## Operator surface

Canonical CLI route:
- `python -m kernel schedule settle ...`

Status must expose:
- latest schedule-settlement receipt

## Acceptance standard

M9 is complete only when:
- settled schedule lines can be closed as durable history,
- superseded witness ids are explicit,
- future re-entry occurs only through the existing scheduler,
- and focused proof shows both settlement with and without re-entry.
