---
protocol_id: ion.agent_context_systems.protocol.v1
status: ACTIVE_OPERATIONAL_LAW
rank: A2_CONTEXT_AUTHORITY
created: 2026-04-28
owned_by:
  - role.context_cartographer
  - role.ionologist
  - role.template_curator
  - role.runtime_cartographer
  - role.canon_librarian
supersedes:
  - mini_capsule_as_primary_agent_context
  - path_list_onboarding_as_context_loading
  - one_boot_file_as_agent_identity
---

# ION Agent Context Systems Protocol

## 1. Core correction

ION agents are not loose role names plus a boot file. Each ION agent is a small governed context system: identity law, live ION definition, role boundary, standing memory, mission context, context graph routes, templates, receipts, and package-evolution rules.

The legacy `MINI.md` / `CAPSULE.md` pattern is preserved only as witness material and private historical continuity. It is not sufficient for live onboarding. Live onboarding requires a High-Detail Agent Context Package assembled for the role, mission, carrier, and authority ceiling.

## 2. Agent context system definition

An Agent Context System contains the following layers:

1. **Semantic identity layer** — true name, role class, authority ceiling, standing domain, and forbidden conflations.
2. **Durable base package** — durable role law, core ION definition relevant to the role, allowed writes, forbidden writes, required templates, and domain limits.
3. **Standing continuity layer** — current high-density summaries of prior work. Existing MINI/CAPSULE files may be mined here, but they are not primary authority.
4. **Mission package layer** — task-specific package containing the actual loaded context needed for the current objective.
5. **Route-and-depth layer** — what the agent may inspect next when it must route deeper than the active package.
6. **Template layer** — exactly which template the agent fills for the step it is performing.
7. **Receipt layer** — context-load proof, delta receipt, return packet, file changes, and Steward integration notes.
8. **Evolution layer** — package lineage and context deltas after ION evolves.

## 3. One-file-per-step operating law

ION context evolution should be template-first. For each bounded step, an agent fills one primary template file. That file must contain the role's active package, necessary index, loaded summaries, full details for that step, route-deeper instructions, authority limits, output contract, and receipt target. Automation may then project, refresh, or split related files from that completed template.

A step file is invalid when it merely says to read a chain of files. Paths are provenance anchors and route affordances; they do not replace loaded context.

## 4. Package classes

- **ROLE_BASE_SYSTEM_PACKAGE**: durable agent identity, domain law, allowed/forbidden writes, standing templates, and live ION definition for that role.
- **MISSION_ACTIVE_CONTEXT_PACKAGE**: task-specific loaded context for the current objective.
- **CONTEXT_DELTA_PACKAGE**: what changed since the prior package and which roles are affected.
- **RECOVERY_CONTEXT_PACKAGE**: branch/donor/historical reconstruction context.
- **CARRIER_CONTEXT_PACKAGE**: carrier-specific constraints and prompt shape for Cursor, ChatGPT, Codex, Claude, Gemini, MCP, shell, or local API.
- **SYSTEM_CARD_PACKAGE**: concise machine-readable summary of the agent's context system.

## 5. Management flow

1. **IONOLOGIST** decides whether the change alters what ION is or how it should be described.
2. **CANON_LIBRARIAN** classifies live, donor, archived, projection, receipt, stale, and false-primary surfaces.
3. **TEMPLATE_CURATOR** selects or updates the template to be filled.
4. **CONTEXT_CARTOGRAPHER** compiles the affected agent context system cards and active packages.
5. **RUNTIME_CARTOGRAPHER** verifies the carrier/kernel/scheduler can deliver those packages.
6. **STEWARD** accepts, rejects, or routes for more work.
7. **RELAY / PERSONA_INTERFACE** present only the accepted operator-facing result.

## 6. Relationship to MINI/CAPSULE

Existing role `MINI.md` and `CAPSULE.md` files are not deleted. They are demoted to **standing continuity witnesses**. The system may use them as source inputs when compiling a Role Base System Package or Mission Active Context Package. They may not be handed to a new worker as the complete context source.

Required wording for generated context packages:

> MINI/CAPSULE are witness inputs, not primary context authority. The active package is the operative context for this run.

## 7. Context size balance

ION must avoid both extremes:

- **Too small**: the agent receives a pointer file and pretends to understand ION.
- **Too large**: the agent receives undifferentiated history and loses the current task.

Every active package must be balanced around:

- role domain;
- mission objective;
- authority ceiling;
- carrier context limit;
- required proof depth;
- available automation;
- route-deeper affordances when judgement is needed.

## 8. Acceptance condition

This protocol is active only when:

- `ION/03_registry/agent_context_system_registry.yaml` exists;
- `ION/05_context/current/agent_context_systems/AGENT_CONTEXT_SYSTEMS_INDEX.md` exists;
- every current live agent has a context-system card;
- templates exist for system cards and one-file-per-step context builds;
- future carrier spawn plans prefer agent context systems and active packages over stale MINI/CAPSULE onboarding.
