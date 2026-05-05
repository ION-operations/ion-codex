---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-09T01:35:00-04:00
status: ACTIVE
connections:
  - ION/02_architecture/HORIZON_STATE_AND_TIGHTENING_PROTOCOL.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/04_packages/kernel/horizon_state.py
  - ION/04_packages/kernel/operator_cli.py
---

# Horizon Packet Enactment Protocol

## Purpose

K4 makes a packet-ready tightened horizon candidate enactable without inventing a second packet workflow.

The enactment helper must return tightened horizon pressure back into the same canonical packet family already used elsewhere in ION.

## Enactment law

A horizon candidate may only be enacted when tightening already says it is packet-ready.

That means:
- the candidate exists,
- unresolved dependencies are absent,
- and the executor surface is explicit enough to hand off.

If those conditions are not satisfied, enactment must refuse explicitly.

## Allowed packet families

K4 may render only already-canonical packet families:
- `handoff`
- `role_session`
- `cursor_handoff`
- `manual_automation_fallback`

No new packet family is introduced by K4.

## Default operator surface

The enactment surface lives under the existing packet CLI family:

`python -m kernel packet enact-horizon <scope_type> <scope_ref> ...`

This keeps enactment discoverable inside the same operator entry surface that already governs status, validation, and supervised runtime control.

## Write law

Enactment must not silently materialize a packet on disk without explicit operator intent.

- If the operator requests an output path, the helper may write the rendered packet.
- If no output path is requested, the helper may return the rendered scaffold without writing it.

## Success condition

K4 is complete when a packet-ready tightened horizon candidate can be rendered into one lawful canonical packet scaffold through the existing CLI surface, and non-ready candidates are refused explicitly.
