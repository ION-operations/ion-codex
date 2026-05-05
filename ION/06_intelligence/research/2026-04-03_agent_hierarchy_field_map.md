---
type: research
authority: A3_OPERATIONAL
template: SYSTEM_EVOLUTION
from: Vizier
created: 2026-04-03T19:30:00-04:00
status: DRAFT
responding_to:
  - ION/06_intelligence/relay/relay/outbound/2026-04-03_sovereign_agent_hierarchy_realms_specialists_to_ALL.md
evidence:
  - SOS-OPUS/03_registry/agent_registry.json (12 agents, v2.0.0)
  - ION/03_registry/boots/*.boot.md (current boot set)
  - ION/03_registry/daimon_matrix.yaml (Vice pairing)
  - SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md (Art. 2 tiers, Art. 3 domains, Art. 6 identity)
---

# ION Agent Hierarchy and Field Map

## 1. HIERARCHY LEVELS

The hierarchy governs authority, precedence, and veto. Higher tiers have broader scope
but not necessarily more volume of work. Lower tiers have bounded scope but high throughput.

| Tier | Level | Function | Precedence |
|------|-------|----------|-----------|
| **T0** | Sovereign | Human authority. Final. Non-delegable. | Overrides all. |
| **T1** | Chief of Staff | Strategic synthesis. System-wide operational coordination. | Below Sovereign only. |
| **T1.5** | Chief Architect / IDE Liaison | Persistent strategic architecture. Cross-domain orchestration. Institutional memory. | Below T1, above T2. |
| **T1.5d** | Conjugate Daimon | Persistent counterforce to T1.5. Less initiative, more veto. Preserves future answerability. | Advisory to T1.5. Veto power on releases. |
| **T2** | Inspector General | Independent cross-cutting audit. Release gate. | Cross-cutting. Cannot be overridden except by Sovereign. |
| **T3** | Director | Domain ownership. Synthesis within domain. | Owns one domain completely. |
| **T4** | Supervisor | Quality coordination. Translation between systems. Relay. | Coordinates within a domain or cross-domain communication. |
| **T5** | Operative | Bounded execution. Single task. | Executes what higher tiers assign. |

## 2. REALMS (Domains)

Each agent operates in exactly one domain (Constitution Art. 3). Domain boundaries are
constitutional — crossing them is a violation.

| Realm | Territory | What Lives Here |
|-------|-----------|----------------|
| **Governance** | Constitutional law, compliance, naming | Doctrine, templates, audit, True Names |
| **Intelligence** | Research, analysis, evidence, synthesis | Reports, findings, consolidation, archaeology |
| **Source** | Executable codebase | Python, TypeScript, tests, build systems |
| **Context** | Cognitive state machine | Context packages, semantic overlays, compilation |
| **Communications** | Inter-agent routing | Signals, tasks, handoffs, dispatch, relay |
| **Interface** | Human-system boundary | IDE liaison, strategic architecture, continuity |
| **System** | Infrastructure substrate | Git, files, processes, deployment, archiving |
| **Interfaces** | User-facing surfaces | UI, CLI, extensions, dashboards |
| **Knowledge** | Comparative reference | External system analysis, OS patterns, ATLAS |

## 3. THE CURRENT FIELD (17 roles)

### Leadership Tier (T0–T1.5d)

| Name | Role | Tier | Realm | Chassis | Persistent | Valid Templates |
|------|------|------|-------|---------|-----------|----------------|
| *Sovereign* | Human Authority | T0 | All | Human | Yes | All (ratification) |
| **Praetor** | Operations_Officer | T1 | Communications | Any premium | No | PLAN, SIGNAL, SPAWN |
| **Vizier** | Continuity_Architect | T1.5 | Interface | Opus 4.6 (default) | Yes | PLAN, RESEARCH, REFLECTION, AUDIT, SYSTEM_EVOLUTION, CURSOR_HANDOFF, SIGNAL, EVIDENCE, CONSOLIDATION, RECONNAISSANCE |
| **Vice** | Conjugate_Daimon | T1.5d | Interface | GPT 5.4 (default) | Yes | HAUNT, MIRROR, COUNTERFACTUAL (daimon modes) |

### Audit and Governance Tier (T2–T3)

| Name | Role | Tier | Realm | Valid Templates |
|------|------|------|-------|----------------|
| **Nemesis** | Inspector_General | T2 | Governance | AUDIT, SIGNAL |
| **Metis** | All_Source_Analyst | T3 | Intelligence | RESEARCH, SIGNAL, CONSOLIDATION |

### Supervisor Tier (T4)

| Name | Role | Tier | Realm | Valid Templates |
|------|------|------|-------|----------------|
| **Dragoman** | Cryptologic_Linguist | T4 | Context | RESEARCH, CODE, SIGNAL |
| **Relay** | Sovereign_Relay | T4 | Communications | RELAY modes (outbound, inbound, digest, clarification) |

### Operative Tier (T5)

| Name | Role | Tier | Realm | Valid Templates |
|------|------|------|-------|----------------|
| **Argus** | Reconnaissance_Analyst | T5 | Intelligence | RESEARCH, SIGNAL, RECONNAISSANCE, EVIDENCE |
| **Thoth** | Research_Analyst | T5 | Intelligence | RESEARCH, SIGNAL, EVIDENCE |
| **Mason** | Software_Architect | T5 | Source | CODE, SIGNAL |
| **Galen** | Diagnostician | T5 | Source | DEBUG, SIGNAL |
| **Scribe** | Archivist | T5 | System | RESEARCH, CODE, SIGNAL, EVIDENCE |
| **Weaver** | Frontend_Engineer | T5 | Interfaces | RESEARCH, CODE, SIGNAL |
| **Ren** | Nomenclator | T5 | Governance | RESEARCH, SIGNAL |

### Standing Watch (special — persistent, self-guiding)

| Name | Role | Tier | Realm | Function |
|------|------|------|-------|----------|
| **Vestige** | Archaeology_Daemon | T5 | Intelligence | Self-guiding excavation, stale-surface detection, issue surfacing |
| **Atlas** | Systems_Cartographer | T5 | Knowledge | Comparative OS/platform/agent reference corpus |

## 4. PRECEDENCE AND VETO RULES

| Situation | Who Decides | Who Can Veto |
|-----------|------------|-------------|
| Architecture decision | Vizier | Vice (dissent blocks release), Nemesis (audit blocks release), Sovereign (overrides all) |
| Code quality | Mason produces, Nemesis audits | Nemesis rejects → Mason reworks |
| Release of phase/artifact set | Vizier proposes | Vice + Nemesis must both clear. Sovereign ratifies. |
| Doctrine change | Sovereign directs, Vizier drafts | Nemesis audits. Vice pressure-tests. |
| Agent spawn / new role | Sovereign or Vizier proposes | Nemesis verifies identity law compliance |
| Template creation | Vizier or domain Director | Nemesis audits, Sovereign ratifies |
| Continuity model change | Roundtable proposes | Sovereign ratifies. Nemesis + Vice must clear. |

## 5. EXPANSION HOOKS (how new specialists attach)

### Adding a new T5 Operative

1. Apply the Weight-Exploitation Algorithm (Art. 5) to find the True Name
2. Assign to exactly one Realm
3. Define valid_templates (what this operative may do)
4. Register in agent_registry.json (Sovereign approval)
5. Create boot doc following VIZIER.boot.md pattern (private continuity, lane permissions)
6. Initialize private MINI + CAPSULE in `ION/agents/{name}/`
7. Nemesis audits the identity for compliance

### Adding a new T3 Director

Same as above, plus:
- Must define domain ownership scope explicitly
- Must not overlap with existing Director domains
- Requires Sovereign ratification

### Adding a new Conjugate Daimon pairing

Per CONJUGATE_DAIMON_PROTOCOL.md:
- The new daimon is always T(n)d relative to its Primary at T(n)
- Must have its own private state objects (shadow continuity, dissent ledger, etc.)
- Must follow the Haunt/Mirror/Counterfactual mode structure

### Specialist examples that could be added

| Potential Name | Role | Tier | Realm | When Needed |
|---------------|------|------|-------|-------------|
| *Censor* | Security_Auditor | T5 | Governance | When security review is needed beyond general audit |
| *Cartwright* | Build_Engineer | T5 | System | When CI/CD pipeline complexity grows |
| *Herald* | Documentation_Writer | T5 | Communications | When user-facing docs need dedicated attention |
| *Crucible* | Test_Engineer | T5 | Source | When test suite management needs dedicated ownership |
| *Sentinel* | Runtime_Monitor | T5 | System | When the daemon needs a dedicated health-monitoring agent |

These are NOT approved — they are expansion examples showing how the framework accommodates growth.

## 6. RELATIONSHIP TO PRIOR REGISTRY SYSTEMS

The SOS-OPUS agent_registry.json (v2.0.0) is the current canonical source for the 12 original
agents. The new roles (Vice, Relay, Vestige, Atlas) emerged during the consolidation roundtable
and need to be formally registered.

**What the prior registry got right:**
- Three-Layer Identity Protocol (personal name + role + structural identity)
- Weight-Exploitation Algorithm for naming
- Tier/domain assignment
- valid_templates as permission boundary
- Protected registry (Sovereign-only writes)

**What the current field adds:**
- Conjugate Daimon pairing (Vice) as a new structural pattern
- Lane-native continuity for supervisor/special roles (Relay, Vestige)
- Standing-watch agents (Vestige, Atlas) as persistent self-guiding roles
- Explicit precedence/veto rules
- Expansion hooks

## 7. OPEN QUESTIONS FOR THE ROUNDTABLE

1. Should Praetor (T1, Chief of Staff) be activated for this consolidation, or does Vizier cover operational coordination for now?
2. Should Vice have a formal registry entry, or does the daimon_matrix serve that function?
3. Should Relay and Vestige be registered in agent_registry.json, or are their boot docs + lane definitions sufficient?
4. Does the current realm taxonomy need refinement? "Interface" vs "Interfaces" is awkward.
5. Should the registry version bump to 3.0.0 to reflect the expanded field?

---

## Upstream Reads
- SOS-OPUS/03_registry/agent_registry.json
- SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md (Art. 2, 3, 5, 6)
- ION/03_registry/daimon_matrix.yaml
- ION/03_registry/boots/*.boot.md
- ION/06_intelligence/relay/relay/outbound/2026-04-03_sovereign_agent_hierarchy_realms_specialists_to_ALL.md

## Downstream Expects
- Vice haunt (hidden defects in hierarchy design)
- Nemesis audit (constitutional compliance of new roles)
- Sovereign review and ratification
- Potential registry update to v3.0.0
