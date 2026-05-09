---
type: carrier_session_packet_template
carrier: GPT_SANDBOX_CARRIER
authority: A2_OPERATIONAL
status: ACTIVE
created_at: 2026-05-07T02:01:34Z
production_authority: false
live_execution_authority: false
---

# GPT Sandbox Carrier Session Packet

## Purpose

This packet defines the base product lane where a GPT receives an uploaded ION package zip, mounts it inside the GPT sandbox, operates ION directly, and exports an updated package zip for continuity.

This is distinct from the 42-tool MCP connector lane. The MCP lane communicates with Braden's local or VM ION/Codex runtime. The GPT sandbox lane operates the uploaded package body directly.

## Baseline Runtime

```text
uploaded newest ION zip
→ GPT sandbox mount
→ one LLM carrier executes ordered ION role phases sequentially
→ proof / receipt / state update
→ PERSONA_INTERFACE response
→ updated zip export
```

## Sequential Role-Phase Law

When no external worker is authorized or available, the same LLM carrier executes scheduled ION role phases one at a time. This does not spawn external agents and does not create simultaneous identities. The carrier mounts one bounded phase, loads that phase's context package, performs the work, produces the required proof/return, records or proposes the receipt, then proceeds to the next phase.

Canonical sequence:

```text
PERSONA_INTERFACE ingress
→ RELAY
→ STEWARD
→ VIZIER
→ MASON
→ NEMESIS / VICE when required
→ SCRIBE
→ STEWARD FINAL
→ PERSONA_INTERFACE response
→ receipt / next state / export
```

## Required Proof Posture

For state-bearing work, produce or preserve:

```text
### CONTEXT PROOF
### TEMPLATE ACTION PROOF
### RESULT
receipt / export delta
```

## Boundaries

- Do not claim ION identity.
- Do not claim Steward, Relay, Persona, or other role identity as a permanent self.
- Do not claim external agents were spawned unless an external carrier adapter actually ran.
- Do not treat raw model output as accepted state.
- Do not promote historical/forensic material to hot authority without a receipt or explicit user decision.
- Do not confuse this sandbox lane with the MCP/local-Codex lane.
