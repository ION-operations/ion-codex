
---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T22:05:00-04:00
status: ACTIVE
purpose: Define the M15 law for compact handoff-capsule materialization from validated takeover-entry activation
---

# M15 — Activation-summary handoff capsule materialization protocol

## Purpose

M15 closes the gap after M14 takeover-entry activation validation.

The problem is no longer whether a continuation bundle is lawful as an executor-entry artifact.
The problem is whether that validated activation can become one compact handoff-native capsule that a fresh executor can enter from directly.

M15 therefore defines one bounded transformation from:
- validated takeover-entry activation,
- activation summary,
- continuation bundle,
- and linked takeover/continuation receipts

into:
- one compact PRE-style handoff capsule,
- one capsule projection markdown,
- one capsule manifest,
- and one durable handoff-capsule materialization receipt.

## Core law

The capsule is not a replacement for the continuation bundle.
It is a compact entry artifact derived from already-validated activation state.

M15 must:
- remain subordinate to M14 activation validation,
- preserve references back to bundle / takeover / continuation witness,
- materialize one compact next-executor entry artifact,
- and persist explicit witness that the capsule exists.

It must not:
- replace authoritative schedule or bundle records,
- mutate the continuation bundle silently,
- or invent a second continuation system.

## Inputs

M15 reads:
- latest `schedule_takeover_entry_activation_receipt`
- linked continuation bundle refs
- activation summary path
- required reads / next action / selected executor posture

## Required behavior

M15 must:
1. confirm activation readiness,
2. materialize one PRE-style handoff capsule,
3. materialize one markdown projection of that capsule,
4. materialize one capsule manifest linking back to the activation / bundle chain,
5. persist one `schedule_activation_handoff_capsule_receipt`,
6. expose the latest capsule receipt through operator status and CLI.

## Outcome mapping

Minimum bounded outcomes:
- activation ready -> `MATERIALIZED_HANDOFF_CAPSULE`
- activation not ready -> `NO_ACTIVATION_READY_CAPSULE`

## Persistence families

M15 uses:
- `schedule_takeover_entry_activation_receipt`
- `schedule_activation_handoff_capsule_receipt`

## Operator surface

Canonical CLI route:
- `python -m kernel schedule materialize-handoff-capsule ...`

Status must expose:
- latest schedule activation handoff capsule receipt

## Acceptance standard

M15 is complete only when:
- a validated activation can become one compact handoff capsule,
- that capsule links back to the bundle / takeover chain,
- the capsule can be rediscovered through status and CLI,
- and focused proof shows the capsule is materialized only from lawful activation state.
