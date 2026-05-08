---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-09T03:12:00-04:00
status: ACTIVE
connections:
  - ION/02_architecture/HORIZON_TO_EXECUTION_WORKFLOW_REHEARSAL_PROTOCOL.md
  - ION/04_packages/kernel/horizon_state.py
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_kernel_workflow_rehearsal.py
---

# T60 — Horizon Carrier-Symmetry Rehearsal

## Requirement

The same packet-ready horizon candidate must preserve packet law whether it is rendered directly through the kernel helper, written through the CLI, or surfaced later through operator status.

## Acceptance

This spec is satisfied when the rehearsal proves:
1. direct render and CLI write preserve the same packet family,
2. candidate identity is stable across carriers,
3. and status can rediscover the enacted packet through the persisted receipt.
