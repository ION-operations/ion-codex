---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T08:05:00-04:00
status: ACTIVE
purpose: Define the M5 law for explicit post-sync rescheduling and carrier/executor rebinding without hidden scheduler substitution
---

# M5 — Branch-aware rescheduling / carrier rebinding protocol

## Purpose

M4 returned bounded branch posture into parent future state.

M5 defines what happens next when the synchronized future must be re-evaluated.
The scheduler may reschedule or rebind, but it must do so explicitly and under witness.

## Core law

After branch future synchronization, any meaningful schedule reconsideration must remain inside the canonical scheduler surface.

If carrier, executor, or capability binding changes, that change must be persisted explicitly.

M5 must not create:
- a hidden rebinding layer,
- silent executor substitution,
- or a branch-only rescheduling subsystem.

## Required behavior

M5 must:
1. require explicit M4 synchronization witness,
2. rebuild the parent-scope schedule through the canonical scheduler,
3. persist a fresh schedule receipt when a candidate exists,
4. compare prior and new scheduling posture,
5. persist an explicit rescheduling / rebinding receipt,
6. expose the latest receipt through operator status and CLI.

## Explicit rebinding witness

The minimum M5 witness must preserve:
- source branch-horizon synchronization receipt id,
- prior schedule receipt id,
- new schedule receipt id,
- prior/new carrier,
- prior/new executor and capability ids,
- rebinding-required boolean,
- rebinding fields,
- reschedule reason.

## Operator surface

Canonical CLI route:
- `python -m kernel allocator reschedule-after-sync ...`

Status must expose:
- latest branch-reschedule receipt

## Non-goals

M5 does not:
- auto-dispatch work,
- auto-claim new branches,
- bypass packet law,
- or mutate carrier choice without witness.

## Acceptance standard

M5 is complete only when:
- post-sync schedule reconsideration is explicit,
- rebinding is witnessed rather than hidden,
- the operator surface can inspect the latest rebinding decision,
- and focused proof demonstrates visible carrier change after synchronized branch future change.
