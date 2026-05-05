---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-09T00:35:00-04:00
status: ACTIVE
connections:
  - ION/02_architecture/HORIZON_ORCHESTRATION_PROTOCOL.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/04_packages/kernel/horizon_state.py
---

# Horizon State and Tightening Protocol

## Purpose

K3 makes the horizon doctrine executable.

ION must maintain living immediate / near / far horizon state as bounded machine-readable records, then tighten that pressure toward one next window without bypassing packet law.

## State family

For each active scope, horizon state may exist at three lawful layers:

- `IMMEDIATE`
- `NEAR`
- `FAR`

Each layer is persisted as a horizon-state record bound to one scope.

## Record law

A horizon-state record must contain:

- one scope binding,
- one layer,
- one plain-language summary,
- zero or more ordered work items,
- and optional links to manifest / automation state.

A work item may carry executor hints, target refs, dependency refs, and packet-readiness.

## Tightening law

The tightening helper may select one next candidate from the closest available lawful layer.

The helper must prefer:
1. `IMMEDIATE`
2. `NEAR`
3. `FAR`

The helper may only mark a candidate packet-ready when:

- the chosen item is already packet-ready,
- unresolved dependencies are absent,
- and the executor surface is explicit enough to hand off.

## What tightening must not do

Tightening must not:

- invent packet-readiness where it does not exist,
- convert vague far-horizon pressure into execution without an explicit packet step,
- replace packet/handoff law,
- or become a parallel planning religion.

## Operator projection

The current operator status surface should expose the latest horizon tightening posture through the existing CLI/status family.

## Success condition

K3 is complete when horizon state exists as durable kernel state, tightening is bounded and honest, and the chosen next window still returns into the canonical packet loop.
