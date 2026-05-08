---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T12:00:00-04:00
status: ACTIVE
purpose: Define M8 law for completion-aware assignment release after schedule dispatch reconciliation
---

# M8 — Schedule completion / assignment release reconciliation

## Purpose

M8 closes the schedule-execution loop after M7 made assignment and dispatch witness explicit.

The problem is no longer whether the schedule can assign and dispatch lawfully.
The problem is whether active assignment counts and dispatch witness are released when execution actually reaches a terminal work-unit state.

## Core law

Assignment closure must not remain implicit in work-unit status.

Once execution reaches a terminal state for a schedule-bound work unit, the kernel must:
- reconcile that terminal state against the latest dispatch reconciliation witness,
- release active assignment count when assignment was previously claimed,
- preserve explicit release witness,
- and avoid leaving capabilities artificially occupied.

## Terminal states

M8 treats these work-unit states as releasable terminal posture:
- COMMITTED
- FAILED
- BLOCKED

Non-terminal states remain deferred.

## Required behavior

M8 must:
1. read the latest schedule-dispatch reconciliation receipt for scope,
2. resolve the associated work unit,
3. inspect latest commit-delta witness when present,
4. detect whether assignment was previously claimed,
5. decrement active assignment count lawfully,
6. persist one completion-release receipt,
7. expose the latest receipt through status and CLI.

## Non-goals

M8 does not:
- invent new execution states,
- apply commit deltas,
- bypass validation,
- or silently clear assignment without witness.
