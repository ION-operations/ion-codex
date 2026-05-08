# Agent Context Systems Index — V81

## Operating conclusion

V80 correctly introduced proof-gated Cursor Task prompts and the ION Context Authority Team, but ordinary agents still carried legacy `MINI.md` / `CAPSULE.md` private-state assumptions. V81 makes the next correction: every live ION role is treated as a governed context system with a system card, base sources, active-package strategy, templates, context balance rule, route-deeper affordances, and receipt expectations.

## Live rule

MINI/CAPSULE are witness inputs, not primary context authority. The active package is the operative context for this run.

## Current role map

| Role | Card | Current legacy witness state | V81 package strategy |
|---|---|---|---|
| STEWARD | `STEWARD.context_system.md` | `ION/agents/steward/MINI.md` + `CAPSULE.md` | orchestration/integration active package with cycle plan, carrier limits, spawn proof gates |
| VIZIER | `VIZIER.context_system.md` | `ION/agents/vizier/MINI.md` + `CAPSULE.md` | architecture/scope active package with dependencies, implications, review posture |
| MASON | `MASON.context_system.md` | `ION/agents/mason/MINI.md` + `CAPSULE.md` | bounded implementation active package with exact files/tests and no architecture expansion |
| NEMESIS | `NEMESIS.context_system.md` | `ION/agents/nemesis/MINI.md`; capsule absent in current extraction | audit active package with evidence ledger and independent review boundary |
| VICE | `VICE.context_system.md` | `ION/agents/vice/MINI.md` + `CAPSULE.md` | contradiction-pressure package with risk, future answerability, and dissent conditions |
| RELAY | `RELAY.context_system.md` | lane-native relay surfaces under `ION/06_intelligence/relay/relay/` | packetization and operator transmission package, not authority ownership |
| VESTIGE | `VESTIGE.context_system.md` | lane-native archaeology surfaces under `ION/06_intelligence/archaeology/vestige/` | provenance/recovery package with broad read, narrow write, stale-surface classification |
| THOTH | `THOTH.context_system.md` | `ION/agents/thoth/MINI.md` + `CAPSULE.md` | reasoning/research package with synthesis and non-mutating analysis boundary |
| SCRIBE | `SCRIBE.context_system.md` | `ION/agents/scribe/MINI.md` + `CAPSULE.md` | documentation/receipt package with report style and path discipline |
| PERSONA_INTERFACE | `PERSONA_INTERFACE.context_system.md` | `ION/agents/persona_interface/continuity.md` | user-facing discourse package based on accepted Relay/Steward output, not hidden authority |
| ATLAS | `ATLAS.context_system.md` | `ION/agents/atlas/MINI.md` + `CAPSULE.md` | external systems reference package with evidence tiers, not ION continuity authority |
| IONOLOGIST | `IONOLOGIST.context_system.md` | new context-specialist role | live ION definition and reconstructive encyclopedia package |
| CONTEXT_CARTOGRAPHER | `CONTEXT_CARTOGRAPHER.context_system.md` | new context-specialist role | context graph to package compiler package |
| RUNTIME_CARTOGRAPHER | `RUNTIME_CARTOGRAPHER.context_system.md` | new context-specialist role | kernel/scheduler/carrier run-map package |
| CANON_LIBRARIAN | `CANON_LIBRARIAN.context_system.md` | new context-specialist role | live/donor/stale authority classification package |
| TEMPLATE_CURATOR | `TEMPLATE_CURATOR.context_system.md` | new context-specialist role | template and receipt-shape package |

## Next automation target

The next kernel change should make `ion_cycle_runner.materialize_cursor_task_context_package(...)` consult `ION/03_registry/agent_context_system_registry.yaml` and emit package prompts from the role's context system card plus the mission packet, rather than relying only on sequential-kernel load targets.
