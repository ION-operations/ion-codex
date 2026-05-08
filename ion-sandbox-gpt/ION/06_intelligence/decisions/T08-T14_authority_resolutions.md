---
type: consolidation
authority: A2_CONSTITUTIONAL
template: CONSOLIDATION
created: 2026-04-03T00:50:00-04:00
status: DRAFT
tasks: [T08, T09, T10, T11, T12, T13, T14]
goal: Resolve the 7 highest-severity authority competitions before Phase 1
evidence:
  - 00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md
  - Thoth constitutional diff (ION-session subagent)
  - Argus registry diff (ION-session subagent)
  - ION-016 Thoth SOS runtime transition extraction
---

# Phase 0A: Authority Resolution Decisions

These 7 decisions resolve the highest-severity authority competitions identified in the
consolidated atlas. Each decision states what the unified ION will implement, what is
preserved as WITNESS, and what evidence supports the choice.

**Governing principle:** The unified ION takes the BEST implementation of each capability.
No system is "killed" — capabilities are preserved or superseded by evidence-backed choices.

---

## T08: Constitutional Law

**Competition:** SOS base (Articles 1-22) vs SOS-OPUS (Articles 1-23)
**05A rows:** `constitutional law`, `registry / liaison authority`

### Evidence

Thoth constitutional diff confirms:
- Articles 1-22 are **character-for-character identical** between SOS and SOS-OPUS
- SOS-OPUS adds only **Article 23 — The IDE Liaison (Tier 1.5)**
- No other wording, structural, or semantic changes exist
- Both are v5.0.0 DRAFT

### Decision

**Unified ION adopts the SOS-OPUS constitution (Articles 1-23).**

Rationale:
- SOS-OPUS is a pure superset — it adds Article 23 without modifying anything else
- Article 23 defines the IDE Liaison role, which is how we are currently operating (this session IS Vizier under Article 23)
- The Sovereign ratified Vizier on 2026-04-01 per the registry
- There is no competing content to resolve — only an addition to accept or reject

Article 23 will be adapted during provisional doctrine assembly (T16) to:
- Remove hardcoded "Claude Opus 4.6" chassis reference (IDE Liaison may run on any model)
- Remove "Antigravity" specific references (generalize to any secondary IDE)
- Retain the core capabilities/constraints framework

**Authority class:** SOS-OPUS constitution → AUTHORITY (provisional until T32 ratification)
**Authority class:** SOS base constitution → WITNESS (superseded by superset)

---

## T09: Agent Registry

**Competition:** SOS base (11 agents) vs SOS-OPUS (12 agents, Vizier + extended templates)
**05A rows:** `registry / liaison authority`, `registry authority`

### Evidence

Argus registry diff confirms:
- All 11 SOS agents exist in SOS-OPUS unchanged (tier, domain, status all identical)
- SOS-OPUS adds Vizier (tier 1.5, persistent, 10 valid_templates)
- SOS-OPUS extends valid_templates for 4 agents: Argus (+RECONNAISSANCE, +EVIDENCE), Metis (+CONSOLIDATION), Thoth (+EVIDENCE), Scribe (+EVIDENCE)
- No agents removed, no tiers changed, no domains changed

### Decision

**Unified ION adopts the SOS-OPUS registry (12 agents, extended templates).**

Rationale:
- Pure superset — adds Vizier and extends templates without removing anything
- Extended templates (EVIDENCE, RECONNAISSANCE, CONSOLIDATION) are the forensic pipeline templates from Phase 0A — agents need them to do their work
- Vizier is the role currently coordinating this consolidation
- Registry-vs-capsule confusion (05A row `registry authority`) is resolved by T06 AuthorityClassSchema: registry = AUTHORITY, capsule narrative = GENERATED_STATE

**Authority class:** SOS-OPUS registry → AUTHORITY (provisional until T32)
**Authority class:** SOS base registry → WITNESS

---

## T10: Write Authority

**Competition:** Gatekeeper.ts (10-stage K-Gate) vs spawner inline validation vs protocol_parser boundary vs ion_kernel/governed_write.py reference
**05A rows:** `write authority`, `gatekeeper implementation status`, `mutation boundary enforcement`, `write-authority reference`, `SOS write authority substrate`

### Evidence

From 05A and Thoth's runtime extraction:
- `Gatekeeper.ts`: Full 10-stage K-Gate class, validates SSP envelopes + target paths. **Not invoked from spawn_agent.py** — the Python spawner bypasses it.
- `spawn_agent.py`: Has inline `validate_envelope()` (simplified 4-field check). This is what ACTUALLY runs.
- `protocol_parser/index.ts`: Strips/repairs envelopes, enforces protected paths, directly writes targets. Overlaps with both.
- `ion_kernel/governed_write.py`: Exact copy of ION-BUILD's rich-ion W1-W10 pipeline. Reference only — not wired to runtime.

### Decision

**Unified ION will implement ONE write authority in Python, combining the best of Gatekeeper.ts formal rigor with governed_write.py's rich object model.**

Specifically:
- Port Gatekeeper.ts's 10-stage validation into Python
- Wire it into the spawner pipeline so ALL writes pass through it (fixing the current bypass)
- Use governed_write.py's IonStore/IonLock integration for rich object writes
- Use Gatekeeper-style SSP envelope validation for agent output writes
- Protocol parser's envelope repair logic becomes a pre-processing step, not a separate write authority

This resolves 5 competition rows by creating a single unified write authority.

**Authority class:** New unified Python Gatekeeper → AUTHORITY (when built in T37)
**Authority class:** Gatekeeper.ts → WITNESS (design reference)
**Authority class:** governed_write.py (ION-BUILD) → WITNESS (object model reference)
**Authority class:** protocol_parser → WITNESS (envelope repair patterns)
**Authority class:** spawn_agent.py inline validation → STALE_COMPETITOR (the bypass that caused the problem)

---

## T11: Runtime Loop Ownership

**Competition:** heartbeat.py vs daemon.ts vs mission_controller.py vs reference_daemon.mjs; spawn_agent.py vs index.ts
**05A rows:** `task orchestration`, `runtime loop ownership`, `runtime daemon surface`, `spawner execution surface`, `daemon trigger ownership`, `root script entry wiring`

### Evidence

From Thoth's runtime extraction (ION-016):
- `heartbeat.py`: LIVE runtime. Scans inbox, routes signals, spawns tasks via subprocess, budget/circuit-breaker, 5-second loop. **This is what actually runs.**
- `daemon.ts`: Retained TS code. Watches inbox + signals + code changes via chokidar. Named by EXECUTION_PIPELINE.md doctrine. **Not evidenced as current runtime.**
- `spawn_agent.py`: LIVE spawner. 12-step pipeline (parse→resolve→model→prompt→API→envelope→validate→write→extract→chronicle→signal). **This is what actually runs.**
- `index.ts` (TS spawner): Retained. Mounts HOT_CONTEXT, shells to Gatekeeper.ts, emits .signal.md. **Not invoked by heartbeat.py.**
- `mission_controller.py` (Victus): Multi-engine routing (PIPELINE/DAG/MESH/CRUCIBLE). **Unique capability not in SOS.**
- `reference_daemon.mjs`: Older chokidar model with code-change-triggered distillation. **Stale.**

### Decision

**Unified ION adopts the Python runtime loop (heartbeat.py + spawn_agent.py) as the execution backbone, enhanced with Victus multi-engine routing.**

Specifically:
- heartbeat.py's inbox-driven loop is the daemon core
- spawn_agent.py's 12-step pipeline is the agent dispatch path
- Victus mission_controller.py's engine routing (PIPELINE/DAG/MESH/CRUCIBLE) is ported as a dispatch strategy layer within the spawner
- daemon.ts and index.ts remain live on disk and are therefore treated as STALE_COMPETITOR surfaces until they are physically archived after parity is proven
- reference_daemon.mjs is preserved as WITNESS material for trigger/watcher lineage, not as a current authority
- EXECUTION_PIPELINE.md doctrine will be updated (T17) to reflect Python runtime reality

**Authority class:** heartbeat.py + spawn_agent.py → AUTHORITY (when ported)
**Authority class:** mission_controller.py → WITNESS (engine routing patterns to port)
**Authority class:** daemon.ts, index.ts → STALE_COMPETITOR
**Authority class:** reference_daemon.mjs → WITNESS

---

## T12: Compiled Context

**Competition:** SOS context_compiler.py vs IONv2 context_compiler.py vs Victus context_assembler.py vs SOS distiller/index.ts
**05A rows:** `compiled context`, `compiled context / renamed fork`, `compiled context implementation`, `compiled context lineage`, `distiller identity`

### Evidence

From 05A and Metis IONv2 extraction (ION-007):
- `SOS context_compiler.py`: Asymmetric visibility, doctrine-aware, dependency signatures, overlays, roster, signals. **Live SOS authority.**
- `IONv2 context_compiler.py`: Graph-native compilation from IonStore/IonIndex/IonGraph. Cleaner code. compile_for_query + compile_summary. **Different model — store-backed, not file-backed.**
- `Victus context_assembler.py`: 4-layer Matryoshka (active chat, compressed history, capsules, swarm). Depends on absent AIM-OS-GIT. **Stale external dependency.**
- `SOS distiller/index.ts`: Compiles HOT_CONTEXT.md, writes active_routes.json, system_ledger.json. V4 path defaults. **Side effects not in Python compiler.**

### Decision

**Unified ION merges the SOS asymmetric model with IONv2's store-backed compilation.**

Specifically:
- T03 ContextPackageSchema defines the output format (5-tier compilation)
- The compiler reads from IonStore/IonIndex/IonGraph (IONv2 pattern) for structured data
- It applies SOS's asymmetric visibility (target 100%, deps signatures-only)
- It loads doctrine excerpts relevant to agent domain (SOS pattern)
- HOT_CONTEXT.md, active_routes.json, system_ledger.json side effects become daemon responsibilities (not compiler responsibilities) per K2 MOVE/PLACE separation
- Victus Matryoshka's conversation compression concept is preserved for the overseer/memory layer, not the context compiler

**Authority class:** New unified Python compiler → AUTHORITY (when built in T34)
**Authority class:** SOS context_compiler.py → WITNESS (asymmetric patterns)
**Authority class:** IONv2 context_compiler.py → WITNESS (store-backed patterns)
**Authority class:** distiller/index.ts → WITNESS (side-effect patterns for daemon)
**Authority class:** Victus context_assembler.py → STALE_COMPETITOR

---

## T13: Signal Dependency Authority

**Competition:** signal_router.py vs signal_protocol.py + signal naming inconsistency
**05A rows:** `signal dependency authority`, `signal file format authority`

### Evidence

From Thoth's runtime extraction (ION-016):
- `signal_router.py`: Gates task creation on `TaskCompleteSignal` parent IDs. Creates inbox .task.md from `TaskRequestSignal` JSON files. **Consumed by heartbeat.py at start of each cycle.**
- `signal_protocol.py`: Independently resolves dependency readiness with same parent-ID logic. Also writes signal JSON files from spawner output. **Overlapping logic.**
- **Naming bug:** spawn_agent.py emits `"type": "SPAWN_COMPLETE"` but signal_router checks for `"signal_type": "TaskCompleteSignal"`. These don't match — dependency checking may silently fail.

### Decision

**Unified ION merges signal logic into a single `signals` package with T07 SignalSchema as the canonical contract.**

Specifically:
- One Python module handles signal emission, dependency checking, and task routing
- All signal types use the standardized names from T07 (TASK_COMPLETE, TASK_REQUEST, etc.)
- The SPAWN_COMPLETE vs TaskCompleteSignal naming bug is eliminated
- JSON format is canonical (resolving .signal.md vs .signal.json inconsistency)
- signal_router's task-creation-from-signals stays (it's the chaining mechanism)
- signal_protocol's emission logic merges into the same module

**Authority class:** New unified signals package → AUTHORITY (when built in T36)
**Authority class:** signal_router.py → WITNESS (routing patterns)
**Authority class:** signal_protocol.py → WITNESS (emission patterns)

---

## T14: Manifest / Context Governance and Continuity

**Competition:** ION-BUILD dual manifests vs SOS CONTEXT_PROTOCOL.md vs IONv2 capsule_manager.py
**05A rows:** `manifest / context governance`, `capsule continuity`, `runtime manifest authority`

### Evidence

- `ION-BUILD/.ion-context/MANIFEST.md` + `ION-BUILD/context/ION_MANIFEST.md`: Duplicated manifest governance within same root. Template routing + capsule protocol.
- `SOS CONTEXT_PROTOCOL.md`: Dual-mode continuity — Mode A (IDE: MINI/CAPSULE) vs Mode B (swarm: compiled HOT_CONTEXT). **Most architecturally mature.**
- `IONv2 capsule_manager.py`: Code-enforced JSON PRE/POST capsules, `recover()`, `check_drift()`. **Cleanest implementation.**
- `ION-BUILD manifest.py`: Executable manifest manager with branches, evidence trail, handoff. **Richest feature set.**

### Decision

**Unified ION adopts the SOS dual-mode architecture with IONv2's capsule implementation.**

Specifically:
- Mode A (IDE/manual): MINI.md (routing state) + CAPSULE.md (work log) — this is our current operating mode
- Mode B (daemon/autonomous): Compiled ContextPackage (T03) + daemon-managed state (system_ledger.json, active_routes.json)
- Capsule persistence uses IONv2's CapsuleManager pattern (JSON PRE/POST with drift checking)
- ION-BUILD's manifest manager features (branches, evidence trail) are preserved for the navigator/cognitive loop layer, not the base continuity layer
- The dual-manifest duplication within ION-BUILD is NOT carried forward — one manifest authority

**Authority class:** SOS CONTEXT_PROTOCOL.md → AUTHORITY (dual-mode architecture)
**Authority class:** IONv2 capsule_manager.py → AUTHORITY (implementation pattern)
**Authority class:** ION-BUILD manifest.py → WITNESS (advanced features for later)
**Authority class:** ION-BUILD dual manifests → STALE_COMPETITOR

---

## SUMMARY TABLE

| Task | Domain | Decision | Key Sources Preserved | Deprecated To |
|------|--------|----------|----------------------|--------------|
| T08 | Constitutional law | SOS-OPUS (Art. 1-23) | SOS-OPUS constitution | SOS base → WITNESS |
| T09 | Agent registry | SOS-OPUS (12 agents) | SOS-OPUS registry | SOS base → WITNESS |
| T10 | Write authority | New unified Python Gatekeeper | Gatekeeper.ts + governed_write.py patterns | Gatekeeper.ts → WITNESS, governed_write.py → WITNESS, protocol_parser → WITNESS, inline validation → STALE_COMPETITOR |
| T11 | Runtime loop | Python heartbeat + spawner + Victus engine routing | heartbeat.py + spawn_agent.py + mission_controller.py patterns | daemon.ts/index.ts → STALE_COMPETITOR, reference_daemon.mjs → WITNESS |
| T12 | Compiled context | Merged SOS asymmetric + IONv2 store-backed | SOS compiler + IONv2 compiler patterns | TS distiller → WITNESS, Victus assembler → STALE_COMPETITOR |
| T13 | Signal authority | Single unified signals package per T07 schema | signal_router.py + signal_protocol.py patterns | Both originals → WITNESS |
| T14 | Continuity | SOS dual-mode + IONv2 capsule implementation | CONTEXT_PROTOCOL + CapsuleManager | ION-BUILD dual manifests → STALE_COMPETITOR |

All 7 resolutions cite specific 05A competition rows and subagent evidence. No system is declared "dead" — capabilities are either adopted into the unified ION or preserved as WITNESS/ARCHIVE material.
