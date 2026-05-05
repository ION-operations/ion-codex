---
type: plan
authority: A3_OPERATIONAL
created: 2026-04-09T00:42:00-04:00
status: COMPLETE
owner: Codex working session
purpose: Define the next workload after K3 horizon state and tightening groundwork
connections:
  - ION/02_architecture/HORIZON_STATE_AND_TIGHTENING_PROTOCOL.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/04_packages/kernel/horizon_state.py
  - ION/tests/test_kernel_horizon_state.py
---

# K4 Next Workload Plan — Horizon packet enactment

## Governing judgment

K3 made horizon state honest and visible. The next move is to make tightened candidates easier to enact without creating a second packet law.

## Objective

Turn a packet-ready tightened horizon candidate into one operator-usable packet enactment helper within the existing CLI / packet family.

## K4 workstreams

### W1 — Enactment helper
Add one bounded helper that can render a normalized packet draft or packet skeleton from a packet-ready horizon candidate.

### W2 — CLI bridge
Expose enactment through the current `python -m kernel ...` operator surface rather than a new carrier.

### W3 — Proof
Add focused tests showing:
- non-ready candidates cannot be enacted,
- ready candidates can be rendered into normalized packet scaffolds,
- and enactment still returns into the same canonical packet family.

## Non-goals

- no autonomous planning engine
- no new packet families
- no multi-scope scheduler
- no hidden packet emission without explicit operator intent

## Acceptance

K4 is done when packet-ready horizon candidates can be turned into lawful packet scaffolds through the existing operator surface, and non-ready candidates are refused explicitly.

## Landing note

K4 landed on 2026-04-09 through `ION/04_packages/kernel/horizon_state.py`, `ION/04_packages/kernel/operator_cli.py`, and focused proof in `ION/tests/test_kernel_horizon_state.py` plus `ION/tests/test_kernel_operator_cli.py`.

The next completion packet is K5 horizon enactment receipts.
