# ION Agent Spawn Protocol

status: proposed_integration_overlay_v0_1
depends_on:
  - ION/04_agents/carriers/CARRIER_AGENT.boot.md
  - ION/04_agents/carriers/carrier_registry.json
  - ION/07_templates/agents/AGENT_SPAWN_REQUEST.md
  - ION/07_templates/agents/AGENT_RESULT_PACKET.md

## Purpose

ION agents do not freely spawn other agents. Core agents may request agents. The Kernel/Scheduler or approved spawn law decides.

## Spawn pathway

1. Requesting agent fills `AGENT_SPAWN_REQUEST.md`.
2. Request declares parent Carrier, carrier level, spawn reality, scope, outputs, forbidden actions, and return target.
3. Request enters existing scheduler/kernel/spawn plan path.
4. Scheduler approves, rejects, modifies, or defers.
5. If approved, execution occurs through one of:
   - manual_phase;
   - host_native_spawn;
   - ion_native_spawn;
   - api_runtime_call.
6. Result returns as `AGENT_RESULT_PACKET.md`.
7. Current Carrier receives result unless another return target is explicitly declared.
8. Carrier journals/drafts journal and updates report/checkpoint state.

## No pretend spawn rule

If no real worker was invoked, mark `spawn_reality: manual_phase`. Do not name it as a real subagent.
