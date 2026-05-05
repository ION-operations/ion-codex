---
type: research
from: Codex
created: 2026-04-12T11:26:36-04:00
status: COMPLETE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
topic: Provenance note for the current-phase disagreement escalation bridge
connections:
  - ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md
  - ION/07_templates/actions/DISAGREEMENT_ESCALATION.md
  - ION/AGENT_CONTRACT.md
  - ION/07_templates/reports/AUDIT.md
  - ION/07_templates/reports/RESEARCH.md
  - ION/07_templates/reports/PROPOSAL.md
  - /home/sev/ION - Production/ION-BUILD/context/08_comms/replies/2026-03-29_090500_codex_audit_escalation_policy.md
  - /home/sev/ION - Production/AIM-ION/lucid_mcp_server.py
---

# Disagreement Escalation Provenance Note

## Why this exists

The live branch already had audit, research, proposal, signal, and handoff surfaces, but
it did not yet have one current-phase bridge packet binding them into a single explicit
disagreement flow.

## Historical and live sources searched

- `ION/AGENT_CONTRACT.md`
- `ION/01_doctrine/CANONICAL_WORKFLOW.md`
- `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- `ION/07_templates/reports/AUDIT.md`
- `ION/07_templates/reports/RESEARCH.md`
- `ION/07_templates/reports/PROPOSAL.md`
- `/home/sev/ION - Production/ION-BUILD/context/08_comms/replies/2026-03-29_090500_codex_audit_escalation_policy.md`
- `/home/sev/ION - Production/AIM-ION/lucid_mcp_server.py` (`signal_disagreement`, `request_escalation`)

## What was found

- The live branch already requires proposal-return rather than silent truth assertion.
- The packet spine already has the carrier artifacts needed for disagreement handling.
- Older estate surfaces already used explicit disagreement and escalation language.
- No exact active `DISAGREEMENT_ESCALATION` control packet existed in the current root.

## What is reused directly

- proposal law and bounded-step law from `AGENT_CONTRACT.md`
- packet-law assumptions from `PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- supporting artifact families from the existing `AUDIT`, `RESEARCH`, `PROPOSAL`,
  `HANDOFF`, and `SIGNAL` templates

## What is restated for current phase

- the explicit disagreement classes
- the mandatory control packet binding the artifact set together
- the rule that work is held while contradiction is being surfaced

## Why this remains provisional

- the branch still needs a real disagreement drill to prove the flow
- the bridge is current-phase operational law, not final constitutional contradiction law

## Non-claims

- This note does not claim all disagreement classes are now permanently settled.
- This note does not replace Nemesis, Thoth, or other role-specific discipline.
- This note does not claim chat-only disagreement counts as lawful escalation.
