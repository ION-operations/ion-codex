---
type: plan
authority: A3_OPERATIONAL
created: 2026-04-09T00:06:00-04:00
status: COMPLETE
owner: Codex working session
purpose: Define the immediate next workload after K2 packet and handoff standardization
connections:
  - ION/MASTER_ORCHESTRATION_INDEX.md
  - ION/02_architecture/HORIZON_ORCHESTRATION_PROTOCOL.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/02_architecture/WORKING_AGENT_SELF_USE_PROTOCOL.md
  - ION/06_intelligence/orchestration/2026-04-08_ion_completion_phase_architecture.md
  - ION/tests/test_kernel_workflow_rehearsal.py
---

# K3 Next Workload Plan — Horizon record and tightening groundwork

## Governing judgment

K2 should reduce ambiguity before K3 introduces more living state. With packet law normalized, the next honest move is to make horizon doctrine executable.

## Objective

Turn immediate / near / far horizon doctrine into a maintained kernel-adjacent state family that shapes the next execution window without becoming a second planning religion.

## K3 workstreams

### W1 — Horizon state family
Create one explicit horizon record family for:
- immediate bounded packet,
- near-horizon active queue,
- far-horizon deferred pressure.

### W2 — Tightening helper
Add a bounded helper that can compile or tighten horizon pressure from far/near into one immediate packet candidate or operator-facing next window.

### W3 — Operator projection
Expose the current horizon summary through one operator-readable surface, likely via the existing CLI/status family rather than a brand-new carrier.

### W4 — Proof
Add focused tests showing:
- horizon records can be created and updated lawfully,
- tightening does not bypass packet law,
- and the resulting immediate step can still be handed off through normalized packets.

## Non-goals

- no swarm allocator yet
- no multi-agent merge law yet
- no expansive roadmap database
- no new packet family unless strictly forced by proof

## Acceptance

K3 is done when the repo has living horizon state, a bounded tightening helper, at least one operator-readable projection, and proof that horizon shaping still returns into the same canonical packet loop.

## Landing note

K3 landed on 2026-04-09 through `ION/04_packages/kernel/horizon_state.py`, store/index integration, operator status projection, and focused proof tests.
