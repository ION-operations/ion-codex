---
type: correction_packet
authority: A3_OPERATIONAL
created: 2026-04-24T11:09:04-04:00
status: ACTIVE
purpose: Correct A4 so user discourse is persona-fronted while internal roles remain workflow-visible and auditable.
connections:
  - ION/02_architecture/SINGLE_CARRIER_FULL_SPECTRUM_CHAT_PROTOCOL.md
  - ION/02_architecture/SOVEREIGN_RELAY_PROTOCOL.md
  - ION/03_registry/boots/RELAY.boot.md
  - ION/06_intelligence/relay/relay/persona_state.md
  - ION/06_intelligence/orchestration/corpus_recovery/32_single_carrier_full_spectrum_protocol_landing/single_carrier_full_spectrum_protocol_landing_packet.md
  - ION/06_intelligence/orchestration/corpus_recovery/32_single_carrier_full_spectrum_protocol_landing/single_carrier_full_spectrum_protocol_landing_judgment.md
---

# Persona front-door correction packet

## Purpose

Correct the A4 protocol so it reflects the intended ION experience:

**The user discourses with Persona. Persona routes into Relay. Relay routes into
Steward. Steward commands or sequences the team. Team work returns through
Steward and Relay. Persona finishes the user-facing response.**

## Correction trigger

The Sovereign clarified that internal agents should not all converse directly
with the user by default.

The user may see the communications and work of the agents in the workflow, but
the final discourse surface should be Persona.

## Corrected model

Target route:

1. Sovereign -> Persona
2. Persona -> Relay
3. Relay -> Steward
4. Steward -> team roles
5. team roles -> Steward
6. Steward -> Relay
7. Relay -> Persona
8. Persona -> Sovereign

## Distinctions

Persona:

- owns direct user discourse and final presentation,
- may apply EUNOIA/persona voice calibration,
- does not gain command authority.

Relay:

- packages the Sovereign's intent faithfully,
- digests team outputs,
- preserves user relationship state in its lane,
- does not own orchestration.

Steward:

- owns current-phase sequencing and board state,
- commands or activates the lawful team workflow,
- does not replace Persona as the final user-facing discourse surface.

Internal roles:

- perform bounded work under their own law,
- may be visible through artifacts or workflow transcript,
- do not become default conversational peers.

## Current-root limitation

The active root has Relay and Relay persona-state surfaces, but no fully
recovered current-phase Persona agent surface.

Until that surface is recovered, Relay or the active carrier may carry a
persona-fronted delivery fallback. That fallback should be treated as temporary
and should not erase the target route.

## A5 implication

A5 should not merely test whether role labels are useful. It should test whether
the Persona-fronted route works in live chat and whether current-root Persona /
`PERSONA_VOICE` recovery is required.
