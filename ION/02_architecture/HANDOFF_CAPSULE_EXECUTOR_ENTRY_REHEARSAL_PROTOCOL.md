---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T23:20:00-04:00
status: ACTIVE
purpose: Define the M16 law for rehearsing direct fresh-executor entry from the compact handoff capsule
---

# M16 — Handoff-capsule executor-entry rehearsal protocol

## Purpose

M16 closes the gap after M15 handoff-capsule materialization.

The problem is no longer whether a compact handoff capsule exists.
The problem is whether a fresh executor can enter directly from that capsule without reopening the broader continuation chain manually.

M16 therefore defines one bounded rehearsal from:
- the latest lawful `schedule_activation_handoff_capsule_receipt`,
- the compact handoff capsule files,
- and the linked activation / continuation references

into:
- one explicit executor-entry rehearsal summary,
- one explicit rehearsal manifest,
- and one durable `schedule_handoff_entry_rehearsal_receipt`.

## Core law

The rehearsal is not a second continuation system.
It is a bounded proof that the compact handoff capsule contains enough lawful entry context for the next executor.

M16 must:
- remain subordinate to the existing activation, continuation bundle, and takeover witness chain,
- validate direct entry from the capsule itself,
- make failure explicit when entry context is insufficient,
- and persist durable rehearsal witness.

It must not:
- silently reopen broader context,
- invent new planner behavior,
- substitute executors invisibly,
- or bypass the continuation bundle / activation chain.

## Inputs

M16 reads:
- latest `schedule_activation_handoff_capsule_receipt`
- capsule JSON / markdown / manifest
- linked activation summary
- linked continuation bundle root
- linked entry packet ref
- required reads / next action / target executor posture

## Required behavior

M16 must:
1. confirm the handoff capsule is ready,
2. confirm the capsule files exist,
3. confirm the capsule manifest and capsule JSON carry bounded entry context,
4. materialize one direct executor-entry rehearsal summary,
5. materialize one rehearsal manifest,
6. persist one `schedule_handoff_entry_rehearsal_receipt`,
7. expose the latest rehearsal receipt through operator status and CLI.

## Outcome mapping

Minimum bounded outcomes:
- capsule ready and sufficient -> `REHEARSED_DIRECT_ENTRY`
- no ready capsule -> `NO_HANDOFF_CAPSULE_READY`
- missing files -> `HANDOFF_CAPSULE_MISSING_FILES`
- insufficient entry context -> `HANDOFF_CAPSULE_INSUFFICIENT_ENTRY_CONTEXT`

## Persistence families

M16 uses:
- `schedule_activation_handoff_capsule_receipt`
- `schedule_handoff_entry_rehearsal_receipt`

## Operator surface

Canonical CLI route:
- `python -m kernel schedule rehearse-handoff-entry ...`

Status must expose:
- latest schedule handoff entry rehearsal receipt

## Acceptance standard

M16 is complete only when:
- a lawful handoff capsule can be rehearsed as a direct executor-entry artifact,
- insufficiency is explicit when entry context is missing,
- the rehearsal can be rediscovered through status and CLI,
- and focused proof shows the rehearsal remains subordinate to the activation / continuation chain.
