---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-12T11:26:36-04:00
status: ACTIVE_CURRENT_PHASE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
connections:
  - ION/AGENT_CONTRACT.md
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/07_templates/reports/AUDIT.md
  - ION/07_templates/reports/RESEARCH.md
  - ION/07_templates/reports/PROPOSAL.md
  - ION/07_templates/actions/HANDOFF.md
  - ION/07_templates/actions/SIGNAL.md
  - ION/07_templates/actions/DISAGREEMENT_ESCALATION.md
  - ION/06_intelligence/research/2026-04-12_disagreement_escalation_provenance_note.md
---

# Disagreement Escalation Protocol

## Purpose

Define the minimum current-phase law for what must happen when live carriers materially
disagree about a mount, packet, implementation, evidence interpretation, protocol
meaning, or landing decision.

## Core law

1. Material disagreement must become filesystem-visible.
2. Disagreement must preserve contradiction rather than flatten it away in chat.
3. Work may not silently land through a disputed surface without an explicit escalation
   packet and the required supporting artifacts.
4. Existing shared templates remain the machine language:
   `AUDIT`, `RESEARCH`, `PROPOSAL`, `HANDOFF`, and `SIGNAL`.
5. The `DISAGREEMENT_ESCALATION` packet is the control packet that binds those artifacts
   into one lawful current-phase flow.

## When this protocol is required

Use this protocol when disagreement could materially change:

- role or chassis mounting
- template interpretation
- evidence trust
- code or packet landing
- escalation to operator or governance roles

## Disagreement classes

- `ROLE_MOUNT`
- `EVIDENCE`
- `IMPLEMENTATION`
- `PROTOCOL`
- `LANDING`

## Required flow

### 1. Hold widening

Pause the disputed widening or landing step.

### 2. Emit one control packet

Create one `DISAGREEMENT_ESCALATION` packet naming:

- the disagreement class
- the relevant surfaces
- the blocked next step
- the required artifact set

### 3. Produce the artifact set

At minimum, the flow should call for one or more of:

- `AUDIT`
- `RESEARCH`
- `PROPOSAL`

plus:

- `HANDOFF` when another carrier must take the next bounded pass
- `SIGNAL` when the field needs to know the disagreement exists

### 4. Reconcile or preserve

The result must either:

- reconcile into one bounded next step, or
- preserve the unresolved contradiction and escalate explicitly

### 5. Land or hold

Only after the disagreement flow completes may the disputed packet, patch, or landing be
advanced.

## Current-phase severity rule

If the disagreement concerns authority, template law, cross-lane writes, or release-risk
review, the flow should prefer audit-weighted resolution rather than casual integrator
judgment.

## Non-goals

- no promise that every disagreement is resolved automatically
- no replacement of `AUDIT`, `RESEARCH`, or `PROPOSAL`
- no claim that one conversation thread counts as lawful contradiction handling
