---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-09T03:10:00-04:00
status: ACTIVE
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/02_architecture/HORIZON_STATE_AND_TIGHTENING_PROTOCOL.md
  - ION/02_architecture/HORIZON_PACKET_ENACTMENT_PROTOCOL.md
  - ION/02_architecture/HORIZON_ENACTMENT_RECEIPT_PROTOCOL.md
  - ION/tests/test_kernel_workflow_rehearsal.py
---

# Horizon-to-Execution Workflow Rehearsal Protocol

## Purpose

K6 turns the K1-K5 packet line into one living proof path.

The goal is not a new runtime family. The goal is one executable rehearsal showing that the same ION loop can:
- compile and carry bounded work,
- persist horizon state,
- tighten the next lawful window,
- enact one canonical packet,
- persist one enactment receipt,
- and surface that result back to the operator.

## Rehearsal law

The workflow rehearsal must prove all of the following in one bounded scenario:
1. horizon state is persisted in kernel truth,
2. tightening chooses the nearest lawful packet-ready candidate,
3. enactment remains inside canonical packet law,
4. successful enactment emits one bounded receipt,
5. and operator status can project both tightening posture and the latest enacted packet receipt.

## Carrier-symmetry law

The rehearsal must show that the same packet can be:
- rendered directly through the kernel helper,
- written through the operator CLI,
- and then rediscovered through the operator status surface,
without changing packet family or candidate identity.

The carrier may change.
The loop must not.

## Non-goals

- no new planner
- no queue or scheduler
- no second continuity carrier
- no hidden readiness mutation
- no swarm claim

## Success condition

K6 is complete when `ION/tests/test_kernel_workflow_rehearsal.py` proves horizon state → tightening → packet enactment → enactment receipt → status visibility as one lawful loop, and the surrounding orchestration surfaces narrate that same path without drift.
