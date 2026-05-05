---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-09T01:37:00-04:00
status: ACTIVE
connections:
  - ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md
  - ION/02_architecture/HORIZON_PACKET_ENACTMENT_PROTOCOL.md
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_kernel_operator_cli.py
---

# T56 — Horizon Packet Enactment CLI Bridge

## Requirement

The operator entry surface must expose horizon packet enactment through the existing `packet` command family.

## Acceptance

This spec is satisfied when:
1. `python -m kernel packet enact-horizon ...` can render or write one canonical packet scaffold for a packet-ready candidate,
2. the command returns a nonzero exit code for non-ready enactment attempts,
3. and the emitted payload preserves scope, source layer, candidate identity, packet type, and warnings.
