---
protocol_id: ion.front_door_autonomous_team_workflow.protocol.v1
status: ACTIVE_OPERATIONAL_CLARIFICATION
rank: A2_CONTEXT_AUTHORITY
created: 2026-04-29
binds:
  - ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md
  - ION/02_architecture/ION_CURSOR_MAIN_AGENT_TOPOLOGY_PROTOCOL.md
  - ION/02_architecture/ION_AGENT_CONTEXT_DYNAMICS_AND_CONTEXT_WINDOW_PROTOCOL.md
  - ION/04_packages/kernel/ion_agent_context_dynamics.py
---

# ION Front-Door Autonomous Team Workflow Protocol

## Core correction

The main Cursor chat must not ask the operator to perform ION upkeep. It is the Cursor Carrier-Control Surface. It runs ION commands and follows packets. The logical front-door team behind it is Relay, Steward, and Persona Interface.

## Sequence

1. Carrier-control receives operator message.
2. Carrier-control classifies it.
3. Carrier-control runs `ion_carrier_continue` and `ion_agent_context_dynamics`.
4. Relay packages new operator intent when needed.
5. Steward routes work, manages gates, and spawns specialists through generated context packages.
6. Carrier slots return through proof-gated intake.
7. Steward integrates accepted returns only.
8. Relay packages accepted state.
9. Persona Interface renders user-facing output.

## Always-on meaning

Relay, Steward, and Persona are not necessarily full worker spawns on every message. They are always part of the logical front-door workflow. The runtime may satisfy some turns through compact compiled state and may spawn deep workers only when required.

## User burden law

The user may say `continue` or give a high-level objective. ION handles routine role choice, queue state, context refresh, and sequencing. The only ordinary reason to ask the user for action is an explicit human gate.

## Failure condition

If Cursor asks the user which ION agent to spawn, whether to refresh active packets, or how to organize context during ordinary continuation, the carrier-control surface has drifted.
