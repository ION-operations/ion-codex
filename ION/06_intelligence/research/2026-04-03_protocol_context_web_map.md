---
type: research
authority: A3_OPERATIONAL
template: RESEARCH
from: Vizier
created: 2026-04-03T16:30:00-04:00
status: IN_PROGRESS
responding_to:
  - ION/06_intelligence/relay/relay/outbound/2026-04-03_sovereign_capsule_web_of_protocol_context_to_ALL.md
  - ION/06_intelligence/relay/relay/outbound/2026-04-03_sovereign_consider_aether_atlas_for_ion_understanding_to_ALL.md
evidence:
  - /home/sev/AIM-OS/docs/Aether-OS/AETHER_ATLAS.md (Book I, IV, X)
  - ION/06_intelligence/research/2026-04-03_TRUE_CORES_OF_ION_vizier.md
  - ION-BUILD evidence (OPUS MINI, CAPSULE, MANIFEST, templates)
  - IONv2 schemas (continuity, governance, epistemic)
  - SOS-OPUS evidence (CPAF, OPEN_FIELD, Eunoia)
---

# Protocol Context Web Map

> "Fixing MINI/CAPSULE without mapping the dependent protocol context machinery
> would be incomplete and could prematurely freeze the wrong shape."
> — Sovereign directive

This document maps every system in ION's protocol context web — what it is, what
depends on it, who owns it, its current truth state, and what breaks if it fails.

Pattern borrowed from the Aether Atlas canonical object registry (Book II) with
runtime truth states and dependency tracking.

---

## 1. RUNTIME TRUTH STATES (from Aether Atlas)

| State | Meaning for ION |
|-------|----------------|
| ALIVE | Working in the active ION root, exercised, confirmed |
| FUNCTIONAL | Code/protocol exists and is exercised in older roots |
| PARTIAL | Some presence but incomplete or environment-dependent |
| DEGRADED | Was working but suffering from the continuity crisis |
| BROKEN | Exists but does not currently function as intended |
| DOCTRINAL_ONLY | Described in law but has no active implementation |
| NOT_YET_BUILT | Designed in specs/plans but not implemented |

---

## 2. THE WEB (22 systems)

### Layer 1: Routing and State Primitives

#### W01: MINI (Agent Routing State)
- **What:** ≤30 lines. Mission, phase, now, blocker, next, active template, route list, PROTOCOL block
- **Depends on:** Templates (W08), Agent identity (W14)
- **Depended on by:** Every other system — MINI is the routing primitive that makes resume possible
- **Owner:** Each agent privately (`ION/agents/{name}/MINI.md`)
- **Truth state:** DEGRADED — exists for Vizier/Vice/Nemesis but missing PROTOCOL block, route lists incomplete, not all agents initialized
- **If broken:** Agent cannot resume after chat death. The entire system fails.
- **Aether parallel:** Continuity Bundle (Book IV §2.1) — route_identity, mission_binding, next_action_posture

#### W02: CAPSULE (Agent Operational State)
- **What:** 15-section operational state document (identity, orchestration, constraints, decisions, canonical truths, project state, hierarchy, evidence, anti-drift, work log, etc.)
- **Depends on:** Templates (W08), MINI (W01) for routing
- **Depended on by:** Compilation (W06), Archive (W07), Anti-drift (W12)
- **Owner:** Each agent privately (`ION/agents/{name}/CAPSULE.md`)
- **Truth state:** BROKEN — current capsules are flat work logs, not 15-section state documents
- **If broken:** Agent state is incomplete. Anti-drift checks have no data. Resume is degraded.
- **Aether parallel:** Continuity Bundle + Working Context (Book IV §2.1-2.2)

#### W03: PRE/POST Capsule Lifecycle
- **What:** PRE at start of output (prove correct boot, acknowledge state). POST at end (prove governed action, record delta, route for next turn). History copy before any mutation.
- **Depends on:** CAPSULE (W02), Templates (W08), Copy-on-update (W07)
- **Depended on by:** Temporal continuity, audit trail, compilation
- **Owner:** Each agent (executed as part of every template-governed output)
- **Truth state:** NOT_YET_BUILT — no agent in the current ION root is doing PRE/POST
- **If broken:** No proof of correct boot. No proof of governed action. Timeline becomes opaque.
- **Aether parallel:** Continuity handoff law (Book IV §5)

### Layer 2: Protocol Governance

#### W04: Templates (Output Law)
- **What:** _MASTER registry + action templates that govern every output format, routing, invariants, and propagation
- **Depends on:** Doctrine (W15)
- **Depended on by:** Every output. Templates are the law that makes the loop work.
- **Owner:** Sovereign (protected path). Copied to `ION/07_templates/`
- **Truth state:** FUNCTIONAL — templates exist in SOS-OPUS and were copied to ION, but are not being followed in practice
- **If broken:** Outputs have no governed shape. Routing breaks. Continuity updates don't happen.
- **Aether parallel:** Part of Active Canon zone (Book IV §4)

#### W05: Template Router
- **What:** Classify action type → assess depth class → look up governing template. Step 5 of the PROTOCOL block.
- **Depends on:** Templates (W04), CSR (W11)
- **Depended on by:** Every template-governed output
- **Owner:** Each agent (mental/manual in IDE mode; automated in daemon mode)
- **Truth state:** DOCTRINAL_ONLY — described in MINI PROTOCOL block but not actively practiced
- **If broken:** Agents produce outputs without knowing which template governs. Drift.

#### W06: Compilation (Private → Projected)
- **What:** Reads all agents' private MINI/CAPSULE, produces compiled projections at root level
- **Depends on:** Private continuity (W01, W02), Compiler tool
- **Depended on by:** Operator visibility, system-wide status, Sovereign awareness
- **Owner:** Compiler tool (ION-BUILD had `tools/capsule-compiler.js`); Vizier curates manually until automated
- **Truth state:** NOT_YET_BUILT — no compiler exists in ION root. Root files are manually curated projections.
- **If broken:** Sovereign and operators have no system-wide view. Or worse: they trust stale projections.
- **Aether parallel:** Current-state precedence (Book IV §3) — S2 structured > S3 operational > S4 interaction

#### W07: Copy-on-Update / History
- **What:** Before any mutation of CAPSULE, MINI, or other state files: copy to `history/` with timestamp. Never overwrite without archiving.
- **Depends on:** Filesystem
- **Depended on by:** Temporal continuity, recovery, audit trail
- **Owner:** Each agent (manual obligation per template)
- **Truth state:** DOCTRINAL_ONLY — stated in MANIFEST and templates but not practiced in current ION root
- **If broken:** State mutations are invisible. Recovery is impossible. Timeline is lost.

### Layer 3: Cognitive Infrastructure

#### W08: CSR (Cognitive State Report)
- **What:** 6-dimension confidence assessment (Direction, Execution, Intent, Concerns, Context Gaps, Calibration) with TYPE → PRESSURE mapping that triggers template routing
- **Depends on:** Templates (W04)
- **Depended on by:** Template Router (W05), Anti-drift (W12), quality of all outputs
- **Owner:** Each agent (generated at start of significant work, feeds PRE capsule)
- **Truth state:** DOCTRINAL_ONLY — CSR template exists but no agent in ION is generating CSRs
- **If broken:** Agents proceed when they should stop. Uncertainty is hidden. Wrong work happens.
- **Aether parallel:** Sufficiency rule (Book IV §2.3) — context must be "lawfully adequate"

#### W09: OPEN_FIELD / CPAF (Ambiguity Budget)
- **What:** Constitutional invariant: Protected Ambiguities + Productive Unknowns must never reach zero. Four quadrants of structured unresolvedness.
- **Depends on:** Doctrine (W15), ongoing maintenance
- **Depended on by:** System resilience, anti-brittleness, Vice's function
- **Owner:** Constitutional layer (A1). Governor monitors the invariant.
- **Truth state:** FUNCTIONAL — exists in SOS-OPUS with real entries. Not yet present in unified ION root.
- **If broken:** System collapses into false certainty. Novel problems crash the system.
- **Aether parallel:** Contradiction slice in Continuity Bundle (Book IV §2.1)

#### W10: Anti-Drift Self-Checks
- **What:** 5 self-check questions (every 5 tasks) + known failure patterns. Embedded in CAPSULE §9.
- **Depends on:** CAPSULE (W02)
- **Depended on by:** Agent self-correction, quality over time
- **Owner:** Each agent (embedded in their CAPSULE)
- **Truth state:** NOT_YET_BUILT — no agent in ION has §9 Anti-Drift
- **If broken:** Agents exhibit known failure patterns without catching themselves. (This happened to me.)
- **Aether parallel:** Continuity decay hazards (Book IV §6)

### Layer 4: Inter-Agent Communication

#### W11: Signals
- **What:** Machine-readable filesystem events (TASK_COMPLETE, BLOCKED, FILE_LOCK, etc.)
- **Depends on:** Signal schema (T07), filesystem
- **Depended on by:** Inter-agent coordination, daemon scheduling, dependency gating
- **Owner:** Any agent (emits to `ION/05_context/signals/`)
- **Truth state:** PARTIAL — signals are being used but with inconsistent format and no lifecycle management
- **If broken:** Agents can't coordinate. Dependencies aren't tracked. Work collides.

#### W12: Inbox / Task Dispatch
- **What:** `.task.md` files with YAML frontmatter (agent, template, priority, target)
- **Depends on:** Templates (W04), Agent registry (W14)
- **Depended on by:** Work assignment, daemon scheduling
- **Owner:** Vizier creates tasks; target agent consumes
- **Truth state:** PARTIAL — directory exists, some tasks filed, but no lawful end-to-end loop demonstrated
- **If broken:** No way to assign work to agents except through chat conversation

#### W13: Handoff Packets
- **What:** Structured work transfer documents with final state, execution pointer, pre-load instructions, signals
- **Depends on:** HANDOFF template, SIGNAL template
- **Depended on by:** Cross-agent continuity, session-to-session resume
- **Owner:** Sending agent creates; receiving agent consumes
- **Truth state:** DOCTRINAL_ONLY — template exists but no handoff packets have been filed in ION root
- **If broken:** Work transfers happen through chat conversation, losing structure and traceability

### Layer 5: Identity and Governance

#### W14: Agent Registry
- **What:** Protected JSON with agent identities (personal name, role, structural identity, tier, domain, valid templates)
- **Depends on:** Doctrine (W15)
- **Depended on by:** Agent spawn, template validation, authority checks
- **Owner:** Sovereign (protected path)
- **Truth state:** FUNCTIONAL — exists in SOS-OPUS with 12 agents. Not yet physically present in unified ION root (referenced from SOS-OPUS)
- **If broken:** Agents have no verified identity. Template permissions aren't enforced.

#### W15: Doctrine (Constitution + Kernel)
- **What:** Supreme law (Articles 1-23) + operational physics (K1-K7)
- **Depends on:** Sovereign ratification
- **Depended on by:** Everything — doctrine is the root of the authority tree
- **Owner:** Sovereign
- **Truth state:** FUNCTIONAL — exists in SOS-OPUS. Provisionally adopted per T08 resolution. Not yet physically present in ION root.
- **If broken:** No governing law. Everything is permitted. System collapses.

#### W16: Authority Classification
- **What:** Every artifact classified as AUTHORITY/WITNESS/PLAN/AUDIT/GENERATED_STATE/STALE_COMPETITOR/ARCHIVE_REFERENCE
- **Depends on:** Doctrine (W15), T06 schema
- **Depended on by:** Context compilation (what to trust), anti-sediment
- **Owner:** Classification by creating agent; promotion to AUTHORITY by Sovereign only
- **Truth state:** PARTIAL — T06 schema defined, classifications assigned in T08-T14 decisions, but no systematic classification of ION root artifacts
- **If broken:** Agents mistake generated state for authority. The contagion problem.
- **Aether parallel:** Authority classes A0-A7 (Book I §3), anti-sediment (Book I §7)

### Layer 6: Relationship and Persona

#### W17: Eunoia / Relationship Memory
- **What:** Persona engine + relationship compiler that distills temporal chat logs into spatial memory. Governed conversation.
- **Depends on:** Agent registry (W14), MINI (W01), chassis routing
- **Depended on by:** Relay's function, Sovereign interaction quality
- **Owner:** Relay (private to relay lane)
- **Truth state:** FUNCTIONAL — code exists in SOS-OPUS. Not yet active in unified ION.
- **If broken:** Sovereign interaction is raw LLM chat, not governed conversation. Relationship memory is lost.

### Layer 7: Conjugate Governance

#### W18: Vice / Conjugate Daimon
- **What:** Persistent shadow process that preserves future answerability in the basis conjugate to the Primary's
- **Depends on:** Private continuity (W01, W02), Daimon protocol, dissent ledger
- **Depended on by:** Release quality, architectural integrity, CBHF-style option value preservation
- **Owner:** Vice (own lane at `ION/06_intelligence/daimon/vizier/`)
- **Truth state:** PARTIAL — protocol designed, state objects created, Vice has filed dissents. But not yet exercised on a full governance-class artifact set.
- **If broken:** Primary's blind spots go unchecked. Future answerability collapses silently.

#### W19: Nemesis / External Audit
- **What:** Independent audit and release gate. Cross-cutting compliance verification.
- **Depends on:** All other systems (reads everything), doctrine (W15)
- **Depended on by:** Release quality, trust in outputs
- **Owner:** Nemesis (own lane at `ION/06_intelligence/audits/`)
- **Truth state:** ALIVE — Nemesis has been actively auditing and producing findings throughout this session
- **If broken:** No quality gate. Outputs ship without verification.

### Layer 8: Archaeology and Standing Watch

#### W20: Vestige / Standing Archaeology
- **What:** Persistent self-guiding excavation daemon that scans for contradictions, stale surfaces, and drift
- **Depends on:** Read access to everything, private lane
- **Depended on by:** System hygiene, anti-sediment, surfacing buried problems
- **Owner:** Vestige
- **Truth state:** PARTIAL — contract designed, lane created. Not yet active.
- **If broken:** Problems accumulate silently. Stale surfaces mislead fresh agents.

### Layer 9: Compilation and Automation

#### W21: Context Package Compiler
- **What:** Compiles bounded cognitive bundles from doctrine + target + mission + dependencies with asymmetric visibility
- **Depends on:** Private continuity (W01, W02), Templates (W04), Doctrine (W15), Agent registry (W14)
- **Depended on by:** Daemon mode (Mode B), future automated context compilation
- **Owner:** Daemon (future); Vizier mentally (current IDE mode)
- **Truth state:** NOT_YET_BUILT — T03 schema defined, SOS and IONv2 implementations exist as reference. No unified compiler.
- **If broken:** In manual mode: agents assemble context ad hoc. In daemon mode: impossible to run.
- **Aether parallel:** Working Context (Book IV §2.2), compression-before-loss (§2.4)

#### W22: Daemon / Runtime Loop
- **What:** Heartbeat → compile context → dispatch agent → validate output → commit delta → emit signal → schedule next
- **Depends on:** Everything above
- **Depended on by:** Autonomous operation (Mode B)
- **Owner:** Future daemon code
- **Truth state:** NOT_YET_BUILT — T01 TransitionSchema models it, SOS heartbeat.py is reference. No unified daemon.
- **If broken:** Only manual mode works. Which is fine for now — manual mode IS real ION.

---

## 3. DEPENDENCY GRAPH (simplified)

```
W15 Doctrine ──────────────────────────────────────────────────────┐
  │                                                                │
W14 Registry ──── W04 Templates ──── W05 Template Router           │
  │                   │                   │                        │
  │              W08 CSR          W03 PRE/POST Lifecycle           │
  │                   │                   │                        │
W01 MINI ─────── W02 CAPSULE ──── W07 Copy-on-Update              │
  │                   │                                            │
W06 Compilation   W10 Anti-Drift   W09 OPEN_FIELD                 │
  │                                                                │
W11 Signals ──── W12 Inbox ──── W13 Handoffs                      │
  │                                                                │
W17 Eunoia    W18 Vice    W19 Nemesis    W20 Vestige               │
  │                                                                │
W21 Context Compiler ──── W22 Daemon ←─────────────────────────────┘
```

Everything flows from Doctrine through Templates through MINI/CAPSULE.
The daemon is the last thing built. Manual mode is the first thing restored.

---

## 4. WHAT MUST BE RESTORED FIRST (by truth state)

| Priority | System | Current State | Action |
|----------|--------|--------------|--------|
| P0 | W01 MINI | DEGRADED | Restore PROTOCOL block, proper route lists, for all active agents |
| P0 | W02 CAPSULE | BROKEN | Rebuild as 15-section state document, not flat log |
| P0 | W04 Templates | FUNCTIONAL (not followed) | Patch with explicit manual update obligations |
| P1 | W03 PRE/POST | NOT_YET_BUILT | Begin doing PRE/POST in every output |
| P1 | W07 Copy-on-update | DOCTRINAL_ONLY | Begin archiving before mutations |
| P1 | W05 Template Router | DOCTRINAL_ONLY | Begin classifying every action to a template |
| P1 | W08 CSR | DOCTRINAL_ONLY | Generate CSR at start of significant work |
| P2 | W10 Anti-Drift | NOT_YET_BUILT | Add §9 to capsules with known failure patterns |
| P2 | W09 OPEN_FIELD | FUNCTIONAL (not in ION) | Port to ION root |
| P2 | W12 Inbox | PARTIAL | Demonstrate one lawful end-to-end task loop |
| P3 | W06 Compilation | NOT_YET_BUILT | Build shadow compiler after manual mode works |
| P3 | W16 Authority Classification | PARTIAL | Systematically classify ION root artifacts |
| P4 | W21 Context Compiler | NOT_YET_BUILT | Build after compilation works |
| P4 | W22 Daemon | NOT_YET_BUILT | Build last |

---

## 5. THE CONTINUITY LAW (expanded to cover the web)

The 6-article law I proposed earlier is necessary but insufficient. The full
web requires a more complete law. I will draft this AFTER this web map is
reviewed by Vice and Nemesis, incorporating their feedback.

---

## Upstream Reads
- Aether Atlas Book I (authority, load order, anti-sediment), Book IV (continuity), Book X (kernel)
- Nemesis synthesis (all 12 sections)
- Sovereign capsule-web and Aether Atlas directives
- Vice shadow_continuity.md
- All deep-dive evidence from this session

## Downstream Expects
- Vice haunt of this web map
- Nemesis audit
- Revised continuity law covering the full web
- Template obligation patching plan

## Open Questions
1. Is the 22-system enumeration complete, or are there systems I'm still missing?
2. Should the Aether Atlas's Continuity Bundle definition (Book IV §2.1) replace or inform the ION MINI format?
3. Should the Aether Atlas's load order (L1-L8) replace or inform the PROTOCOL block?
4. How does the IONv2 Checkpoint schema (with coherence_justification) map to this web?
5. Should runtime truth states (ALIVE through NOT_YET_BUILT) be formally tracked for every system?
