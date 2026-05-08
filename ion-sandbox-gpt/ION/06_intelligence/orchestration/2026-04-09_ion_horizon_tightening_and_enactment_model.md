---
type: horizon_model
authority: A2_EXECUTOR
created: 2026-04-09T16:05:00-04:00
status: ACTIVE
purpose: Explain how future work exists in ION, tightens honestly, and returns into the packet loop through enactment and receipts
connections:
  - ION/02_architecture/HORIZON_STATE_AND_TIGHTENING_PROTOCOL.md
  - ION/02_architecture/HORIZON_PACKET_ENACTMENT_PROTOCOL.md
  - ION/02_architecture/HORIZON_ENACTMENT_RECEIPT_PROTOCOL.md
  - ION/02_architecture/HORIZON_TO_EXECUTION_WORKFLOW_REHEARSAL_PROTOCOL.md
  - ION/tests/test_kernel_horizon_state.py
  - ION/tests/test_kernel_workflow_rehearsal.py
---

# ION Horizon, Tightening, and Enactment Model

## Purpose

This document explains how ION carries future work without collapsing into either static planning or vague intention.

## Why horizon state exists

ION needs a lawful way to retain future pressure.

If future work is held only in loose prose, continuity weakens.
If future work is forced too early into execution-ready packets, the system starts lying about readiness.

Horizon state exists to hold the middle ground honestly.

## Horizon layers

Future work is carried across three lawful layers:
- `IMMEDIATE`
- `NEAR`
- `FAR`

These are not three separate planners.
They are three distances from execution.

### Immediate

The closest lawful next window.
This should contain the most concrete and execution-relevant candidates.

### Near

Structured likely-next work that still depends on further compilation, review, or dependency satisfaction.

### Far

Strategic or longer-range pressure that matters but is not yet ready to collapse into execution.

## Tightening

Tightening is the move from looser future pressure toward one next lawful candidate.

Tightening must prefer the nearest available lawful layer:
1. `IMMEDIATE`
2. `NEAR`
3. `FAR`

It may only mark a candidate packet-ready when:
- the candidate is explicit enough,
- dependencies are satisfied,
- and the executor surface is clear enough to hand off.

## What tightening must not do

Tightening must not:
- invent readiness,
- smuggle vague far-horizon desire into execution,
- replace packet law,
- or become a shadow planner.

## Enactment

Enactment returns a packet-ready tightened candidate into the canonical packet loop.

This is critical:
- the future field becomes execution through the same packet law,
- not through a second queue,
- not through a second planner,
- and not through hidden state.

Allowed output families remain canonical packet families such as handoffs and role sessions.

## Enactment receipts

Once enactment succeeds, a receipt may be written.

The receipt is:
- durable traceability,
- evidence of what candidate was enacted,
- and a witness that the candidate returned to canonical packet law.

The receipt is not:
- a second packet family,
- a readiness mutator,
- or a second authority layer.

## What K3-K6 already prove

The current root already proves that:
- horizon state can persist,
- tightening can choose the nearest lawful packet-ready candidate,
- enactment can render one canonical packet,
- enactment can emit one bounded receipt,
- and operator surfaces can project that posture back to the current executor.

That turns horizon work from idea into executable continuity.

## Relation to scheduler law

The horizon system is not the full scheduler.

Horizon state holds future pressure.
The scheduler reasons over that pressure, along with work-unit state, carrier posture, and later capability law, to progressively compile the future schedule.

## Practical rule

Future work should become more explicit as evidence accumulates and less rigid when reality changes.
That is the center of the horizon model.
