---
type: proposal
from: Codex
created: 2026-04-12T13:18:30-04:00
status: ROUTED
topic: Current branch posture on bridge packet family status and validator coverage
responding_to:
  - ION/06_intelligence/archaeology/vestige/reports/2026-04-12_bridge_packet_family_archaeology.md
  - ION/06_intelligence/research/2026-04-12_thoth_bridge_packet_status_evidence.md
  - ION/06_intelligence/research/2026-04-12_bridge_packet_family_status_and_validation_next_workload_plan.md
---

# Proposed Bridge Packet Status Posture

## Purpose

Set the current branch proposal on whether `ROLE_CHASSIS_MOUNT`,
`DISAGREEMENT_ESCALATION`, and `EXTERNAL_RETURN` should widen the canonical packet
family now, and decide whether Mason should start.

## Proposal

For the current branch, do **not** widen canonical packet taxonomy or packet-validator
coverage yet.

Instead:

- keep canonical packet law at the current five-family floor
- keep `ROLE_CHASSIS_MOUNT`, `DISAGREEMENT_ESCALATION`, and `EXTERNAL_RETURN` as
  governed bridge packets outside that floor
- keep their current `PROVISIONAL_BRIDGE` / `NOT_FINAL_CANON` posture explicit
- treat any future widening as a separate later law decision rather than as something
  already implied by Phase 1 proof usage

## What changes operationally

- `Vestige` and `Thoth` have completed the right pre-implementation passes
- `Mason` should remain held for now because no code/test widening is justified yet
- browser ChatGPT should remain held for this workload because no bounded external
  compare pass is currently needed
- the next Codex-local step should be one small explicit support note clarifying the
  non-canonical bridge-packet posture, rather than a validator change

## Risks / edge cases

- sessions may still overread `UNSUPPORTED_TYPE` as “illegal” instead of “outside the
  narrow canonical validator floor”
- if bridge packets continue spreading without support clarification, confusion will
  recur
- widening may still become the right choice later if these packets stabilize beyond
  current-phase bridge use

## Open questions

- should the branch add a separate explicit bridge-packet support protocol or note next
- if widening is proposed later, should it happen by extending the canonical packet law
  or by adding a second validator tier for bridge packets
- how should the branch name the relationship between bridge packets and older Aether
  schema packet meanings so “handoff” and related terms do not collapse across estates
