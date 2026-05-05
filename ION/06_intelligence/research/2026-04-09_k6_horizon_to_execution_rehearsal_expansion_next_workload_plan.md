---
type: plan
authority: A3_OPERATIONAL
created: 2026-04-09T02:11:00-04:00
status: COMPLETE
owner: Codex working session
purpose: Define the next workload after K5 horizon enactment receipts
connections:
  - ION/MASTER_ORCHESTRATION_INDEX.md
  - ION/02_architecture/HORIZON_ENACTMENT_RECEIPT_PROTOCOL.md
  - ION/04_packages/kernel/horizon_state.py
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_kernel_workflow_rehearsal.py
---

# K6 Next Workload Plan — Horizon-to-execution workflow rehearsal expansion

## Governing judgment

K1–K5 made operator entry, packet law, horizon state, enactment, and enactment visibility real. The next move is stronger proof, not a new abstraction family.

## Objective

Expand the workflow rehearsal center so one end-to-end scenario proves:
- horizon state can be persisted,
- a packet-ready candidate can be enacted lawfully,
- enactment emits one bounded receipt,
- and operator status can see that result.

## K6 workstreams

### W1 — Rehearsal path
Extend the current workflow rehearsal so horizon state and enactment receipts are part of the executable proof path rather than isolated helper tests.

### W2 — Carrier symmetry check
Prove that horizon-to-packet handoff remains the same loop whether the packet is simply rendered, written through the CLI, or surfaced back through status.

### W3 — Completion-surface reconciliation
Tighten orchestration text so the live K packet frontier and the master completion suite describe the same current state.

## Non-goals

- no new runtime family
- no parallel/swarm lane yet
- no new planning substrate

## Acceptance

K6 is done when the workflow rehearsal proves horizon state → enactment → receipt → status visibility as one lawful loop, and the orchestration surfaces narrate that same path without drift.

## Completion note

K6 is now complete. The workflow rehearsal proves horizon state persistence, lawful tightening, canonical packet enactment, enactment receipt persistence, packet validation, and status visibility as one lawful loop.
