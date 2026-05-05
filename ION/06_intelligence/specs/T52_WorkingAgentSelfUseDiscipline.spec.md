---
type: spec
authority: A2_EXECUTOR
created: 2026-04-09T00:01:00-04:00
status: ACTIVE
implements:
  - ION/02_architecture/WORKING_AGENT_SELF_USE_PROTOCOL.md
implemented_by:
  - ION/05_context/comms/kernel_router_runs/2026-04-08_k2_packet_handoff_standardization/
  - ION/06_intelligence/research/2026-04-08_k2_packet_handoff_standardization_reasoning_journal.md
---

# T52 — Working-Agent Self-Use Discipline

## Goal

Make the working agent obey the same bounded continuity law it expects the system to carry.

## Required properties

1. Significant passes leave a reasoning journal when appropriate.
2. Significant passes leave role-session and handoff artifacts.
3. Next-step language is bounded and explicit.
4. Root projections are not treated as source continuity.

## Acceptance

This spec is satisfied when a fresh executor can reconstruct the packet, the chosen bounded step, and the next lawful move from the working-agent artifacts alone.
