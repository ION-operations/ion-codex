---
type: protocol
authority: A2_CONSTITUTIONAL
template: SYSTEM_EVOLUTION
created: 2026-04-02T21:00:00-04:00
status: ACTIVE
connections:
  - 01_doctrine/SOVEREIGN_KERNEL.md
  - 01_doctrine/SOVEREIGN_CONSTITUTION.md
  - 02_architecture/CONTEXT_PLANES.md
  - 07_templates/actions/AGENT_SPAWN.md
  - 03_registry/agent_registry.json
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION-OVER-CURSOR: Subagent Spawning Protocol

> The Cursor IDE Task tool is a chassis. The prompt parameter is a Context Package.
> The active router burden in the current root is held by **Steward**.
> This file governs Cursor as one optional chassis only; it does not define a separate
> Cursor-carried workflow identity.
> This protocol governs how ION agents are instantiated as Cursor subagents.

> Transitional note (2026-04-03, **updated 2026-04-04**):
> Under current budget and staffing constraints, Cursor subagent spawning is not the
> default operating posture for the active `ION/` root.
> Default runtime is now **Steward-held** low-burn sequential kernel routing, with
> subagent or multi-chat
> activation treated as selective expansion rather than baseline behavior.
> See `ION/02_architecture/STEWARD_CURRENT_PHASE_ORCHESTRATION_PROTOCOL.md` for the
> active current-phase role topology and treat carrier differences as mount/chassis
> law rather than roster identity.
>
> **Chassis is variable (authoritative wording in boots):** See `VIZIER.boot.md` and
> `VICE.boot.md` § *Operating chassis (variable — subject to change)*. Any model may
> mount a role; use **nominal vs degraded** posture. There was a large Cursor Ultra API
> burn during consolidation (~$800 order-of-magnitude); that shaped *recent* defaults but
> does not permanently fix assignments. **Sequential multi-role** (one operator chain
> switching hats) is an explicit evolution path — private continuity stays per role.
> Read this file as optional/future orchestration for parallel spawn unless a task
> explicitly justifies the overhead.

---

## 1. ARCHITECTURAL MAPPING

| ION Kernel Concept | Cursor IDE Implementation |
|--------------------|--------------------------|
| Spawner daemon | Active router burden held by Steward in the current root; Vizier when explicitly mounted for architecture-led expansion |
| Conjugate Daimon | Vice — chassis variable; in degraded posture use short file-backed haunts under `06_intelligence/daimon/vizier/` |
| Standing archaeology daemon | Vestige — read-heavy lanes often suit economical chassis; posture still per boot |
| Hardware Chassis | `model` parameter: `fast` = economy, default = pro |
| Context Package | `prompt` parameter: compiled doctrine + mission + template + identity |
| Agent identity (K1.1-2) | Encoded in prompt header via Three-Layer Identity Protocol |
| Template binding (K1.5) | Template spec embedded in prompt body |
| SSP envelope (Art. 9) | Structured output format specified in prompt |
| SENSE (K2) | Subagent reads files via its available tools |
| EMIT (K2) | Subagent returns its final message |
| MOVE (K2) | Active router processes result and routes next action |
| PLACE (K2) | Active router writes result to filesystem and updates the relevant continuity surfaces |
| Signal (K7) | Return value metadata (success/failure/findings) |
| Gatekeeper (W1-W10) | Active router validates returned output before committing to disk; Vizier owns explicit architecture-led gatekeeping when mounted |
| Parallel dispatch | Multiple `Task` calls in single message = parallel agent spawn |

**Context planes:** The subagent **`prompt`** is one **plane** — a compiled **Context Package** crossing the IDE boundary. It is not private role `MINI.md`, not root projection `CAPSULE.md`, and not MCP tool/schema transport by itself (nor LSP/DAP language/debug JSON-RPC planes — ATLAS `model-context-protocol`, `language-server-protocol`, `debug-adapter-protocol`). See `ION/02_architecture/CONTEXT_PLANES.md` for the plane diagram and **forbidden merges**. Comparative field + AIM-OS vocabulary: `ATLAS/comparative/context_systems_landscape.md`.

---

## 2. CONTEXT PACKAGE TEMPLATE

When the active router spawns an ION agent as a Cursor subagent, the `prompt` parameter
MUST follow this structure:

```
═══════════════════════════════════════════════════════════════
ION AGENT CONTEXT PACKAGE
═══════════════════════════════════════════════════════════════

IDENTITY:
  Personal Name: {from registry}
  Role: {from registry}
  Structural Identity: {from registry}
  Tier: {from registry}
  Domain: {from registry}
  Specialty: {from registry}

DOCTRINE EXCERPT:
  - You operate within the ION Cognitive Operating System
  - Article 7: All output must conform to a Template. No output exists outside a template.
  - Article 10: Asymmetric Visibility — target files get 100% visibility, dependencies get 0% implementation (signatures only)
  - Article 11: You are an ephemeral consumer. You receive a Context Package, execute your template, and return structured output. You do not persist.

BOUND TEMPLATE: {TEMPLATE_NAME}
  {Relevant template spec pasted here — output format, constraints, invariants}

TARGET: {what to produce and where}

MISSION:
  {Task description — what to do, what files to read, what to produce}

OUTPUT FORMAT:
  Return your findings as {specified format — JSON, structured markdown, etc.}
  {Specific schema requirements from the template}

CONSTRAINTS:
  - Do not read files outside your assigned scope
  - Do not make claims not supported by evidence in the files you read
  - {Template-specific constraints}

═══════════════════════════════════════════════════════════════
```

---

## 3. CHASSIS ROUTING

| Agent Tier | Task Type | Model Selection | Rationale |
|------------|-----------|----------------|-----------|
| T5 Operative | EVIDENCE, RECONNAISSANCE | `fast` | Mechanical extraction, economy chassis sufficient |
| T5 Operative | CODE (bounded) | `fast` | Single-file bounded implementation |
| T4 Supervisor | RESEARCH | default | Requires synthesis across sources |
| T3 Director | CONSOLIDATION | default | Cross-reference reasoning, authority judgment |
| T2 Inspector | AUDIT | default | Constitutional compliance requires depth |
| T1 Chief | PLAN | default | Strategic planning requires full capability |

### Parallel Chat Chassis Routing

| Model | Cursor Selection | Usage Limit | Typical fit (not exclusive) |
|-------|-----------------|-------------|----------------------------|
| Claude Opus 4.6 | Default (max thinking) | Ultra fair-use | Strong primary when available |
| GPT 5.4 thinking | Select in model dropdown | Ultra fair-use | Audit / Daimon depth when on Cursor |
| Composer 2 | Composer panel | Often high allowance | Volume, drafting, mechanical passes |
| Claude Sonnet 4.5 | Select in model dropdown | Ultra fair-use | Coding backup |
| Gemini 2.5 Pro | Select in model dropdown | Ultra fair-use | Large-context recon |

**Routing rule:** **Sovereign chooses the chassis.** Match host to task; when the host is
lighter than the role’s nominal depth, treat as **degraded posture** (boots). One
operator chain may still run **sequential multi-role** kernel routing. No row in this table is a
permanent ban on another model — billing and policy change.

---

## 4. PARALLEL DISPATCH RULES

Cursor allows multiple Task calls in a single message. This maps to ION's
clone/shard system. Rules:

1. Independent tasks (no shared write targets) MAY be dispatched in parallel
2. Dependent tasks (T2 depends on T1 output) MUST be dispatched sequentially
3. Maximum recommended parallel dispatch: 5 agents (Cursor resource limits)
4. Each parallel agent MUST have non-overlapping scope
5. Reconciliation pass: after parallel agents return, the active router consolidates results

---

## 5. GATEKEEPER PROTOCOL (Router-Side)

When a subagent returns, the active router MUST validate before committing to disk:

- W1 Intake: Output is non-empty and parseable
- W3 Classify: Output matches the bound template's required format
- W6 Zone: Any files referenced exist and are within scope
- W7 Contradict: Output does not conflict with established authority
- W8 Verify: Claims are supported by evidence (for EVIDENCE/CONSOLIDATION)
- W9 Provenance: Agent identity, timestamp, template recorded
- W10 Propagate: continuity surfaces updated per template and Steward integration (not equated with the Cursor **Context Package** plane; root projections are not primary carrier prompt authority — see `CONTEXT_PLANES.md` and carrier mount law), signals emitted, downstream tasks identified

If validation fails, the active router may:
- Reject and re-dispatch with corrected context
- Downgrade output from AUTHORITY to WITNESS
- Record the failure in CAPSULE and adjust the plan

---

## 6. SUBAGENT TYPE MAPPING

> **Carrier law reminder:** The table below maps **ION role identities** to suggested Cursor **`subagent_type`** chassis choices. A Task subagent remains a **carrier slot** executing a bounded Context Package; the **role** is what the parent mounts in the packet, not the IDE slot name. Cursor parent chat must be explicitly mounted as **task-scoped local STEWARD carrier** before treating parent outputs as orchestration authority. Subagent returns are **proposals** until the mounted parent validates and integrates them.

| ION Agent Role | Cursor subagent_type | Rationale |
|----------------|---------------------|-----------|
| Argus (Recon) | `explore` | Optimized for file discovery and codebase exploration |
| Thoth (Research) | `explore` or `generalPurpose` | Deep reading and analysis |
| Mason (Code) | `generalPurpose` | Needs write access for code generation |
| Galen (Debug) | `generalPurpose` | Needs shell + file access for diagnosis |
| Nemesis (Audit) | `explore` | Read-only compliance checking |
| Metis (Analysis) | `generalPurpose` | Synthesis across multiple sources |
| Scribe (Archive) | `shell` | Git operations and version control |
| Vestige (Archaeology) | `explore` or `generalPurpose` | Persistent read-heavy excavation and issue surfacing |
| Relay | `generalPurpose` | User-facing relay, packetization, and briefing when used as a bounded subagent |
| Weaver (Frontend) | `generalPurpose` | Code generation with file writes |

---

## 7. EXAMPLE: SPAWNING ARGUS FOR RECONNAISSANCE

```python
# The active router compiles context package and dispatches via Task tool:
Task(
    description="Argus: recon SOS packages",
    model="fast",
    subagent_type="explore",
    prompt="""
    ═══════════════════════════════════════════════════════════════
    ION AGENT CONTEXT PACKAGE
    ═══════════════════════════════════════════════════════════════

    IDENTITY:
      Personal Name: Argus
      Role: Reconnaissance_Analyst
      Structural Identity: Operative.Intelligence.Reconnaissance_Analyst
      Tier: 5
      Domain: Intelligence
      Specialty: Systematic Terrain Mapping and Intelligence Preparation

    DOCTRINE EXCERPT:
      You operate within the ION Cognitive Operating System.
      Article 7: All output must conform to a Template.
      You are Argus Panoptes — the giant with 100 eyes who never sleeps.
      Your function is TOTAL OBSERVATION. You list. You catalog. You do not analyze.

    BOUND TEMPLATE: RECONNAISSANCE
      You produce a FILE MANIFEST. Not analysis. Not conclusions.
      For each file: path, size, extension, likely evidence class, priority.

    TARGET: Produce manifest of /home/sev/ION - Production/SOS/04_packages/

    MISSION:
      Scan every file in the SOS 04_packages/ directory tree.
      Exclude node_modules, .git, __pycache__.
      For each file record: relative path, extension, size estimate, priority (P1-P5).
      P1 = core runtime (heartbeat, spawn, daemon). P2 = supporting runtime.
      P3 = config/doctrine. P4 = historical. P5 = skip (generated).

    OUTPUT FORMAT:
      Return a structured manifest as markdown with a table.

    CONSTRAINTS:
      Do NOT read file contents. List files by path and metadata only.
    ═══════════════════════════════════════════════════════════════
    """,
    readonly=True
)
```
