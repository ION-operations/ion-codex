---
type: law
authority: A1_KERNEL
template: SYSTEM_EVOLUTION
created: 2026-04-03T11:00:00-04:00
status: ACTIVE
supersedes:
  - ION/02_architecture/MULTI_CHAT_COORDINATION.md (shared-surface model — WRONG)
evidence:
  - ION-BUILD/agents/OPUS/MINI.md (per-agent private)
  - ION-BUILD/agents/OPUS/CAPSULE.md (per-agent private)
  - ION-BUILD/agents/STEWARD/MINI.md (per-agent private)
  - ION-BUILD/agents/SENTINEL/MINI.md (per-agent private)
  - ION-BUILD/context/MINI.compiled.md (compiled projection)
  - ION-BUILD/context/CAPSULE.compiled.md (compiled projection)
  - ION-BUILD/tools/capsule-compiler.js (compilation tool)
  - SOS/02_architecture/CONTEXT_PROTOCOL.md (dual-mode)
---

# ION CONTINUITY ARCHITECTURE — Corrected Law

> Agent continuity is PRIVATE. Always has been. Always will be.
> Each agent writes ONLY its own context. No agent writes another agent's context.
> Shared surfaces are COMPILED PROJECTIONS, not raw shared state.

> Transitional clarification (2026-04-03):
> The active root does **not** currently have a compiled `ION/context/` tree.
> Current shared projections are the root trio (`ION/MINI.md`, `ION/CAPSULE.md`, `ION/STATUS.md`)
> plus the signal bus. A minimal live `ION/07_templates/` layer now exists, and the safest
> default runtime is low-burn sequential routing rather than broad premium-parallel staffing.

---

## 1. THE LAW

### 1.1 Private Continuity

Every agent maintains its own private continuity:

```
ION/agents/{agent_name}/
├── MINI.md           — this agent's routing state
├── CAPSULE.md        — this agent's work log
├── history/          — this agent's capsule snapshots
└── context/          — this agent's working context (if needed)
```

**No agent writes to another agent's directory. Ever.**

### 1.2 Inter-Agent Communication

Agents communicate ONLY through:

| Channel | Path | Who Writes | Who Reads |
|---------|------|-----------|-----------|
| Inbox | `ION/05_context/inbox/{agent}_*.task.md` | Vizier (dispatch) | Target agent |
| Signals | `ION/05_context/signals/*.signal.md` | Any agent (own signals) | All agents |
| Intelligence | `ION/06_intelligence/` | Any agent (own lane) | All agents |
| Handoff packets | `ION/05_context/handoffs/` | Sending agent | Receiving agent |

### 1.3 Compiled or Curated Projections (NOT raw shared state)

Shared views of system state are COMPILED from private agent state.
They are projections — read-only summaries, not source of truth.

**Future compiled shape (not present in the active root today):**

```
ION/context/
├── MINI.compiled.md
├── CAPSULE.compiled.md
└── STATUS.compiled.md
```

**Current active shape (present today):**

- `ION/MINI.md`
- `ION/CAPSULE.md`
- `ION/STATUS.md`

These are manually curated projections. They are NOT the real continuity.
The real continuity lives in private role lanes.

### 1.4 What This Means for the Root Files

The current `ION/MINI.md`, `ION/CAPSULE.md`, `ION/STATUS.md` at the root
are **temporary manual projections**. They are NOT agent continuity systems.

- `ION/MINI.md` → Vizier's projection of current system routing. Vizier curates it.
- `ION/CAPSULE.md` → Vizier's projection of system-wide work log. Vizier curates it.
- `ION/STATUS.md` → temporary or optional coordination projection. It may later be replaced, reduced, or removed once compiled context exists.
- `ION/PLAN.md` → system plan. Vizier-owned governance document, not continuity.

The REAL Vizier continuity is at `ION/agents/vizier/MINI.md` and `ION/agents/vizier/CAPSULE.md`.

---

## 2. PER-AGENT CONTINUITY SETUP

| Agent / Role | Source Continuity Location | Continuity Class | Boot Doc |
|--------------|----------------------------|------------------|----------|
| Vizier | `ION/agents/vizier/` | agent-private | `ION/03_registry/boots/VIZIER.boot.md` |
| Vice | `ION/agents/vice/` | agent-private | `ION/03_registry/boots/VICE.boot.md` |
| Nemesis | `ION/agents/nemesis/` | agent-private | `ION/03_registry/boots/NEMESIS.boot.md` |
| Mason | `ION/agents/mason/` | agent-private | `ION/03_registry/boots/MASON.boot.md` |
| Scribe | `ION/agents/scribe/` | agent-private | `ION/03_registry/boots/SCRIBE.boot.md` |
| Thoth | `ION/agents/thoth/` | agent-private | `ION/03_registry/boots/THOTH.boot.md` |
| Atlas | `ION/agents/atlas/` | agent-private | `ION/03_registry/boots/ATLAS.boot.md` |
| Steward | `ION/agents/steward/` | agent-private | `ION/03_registry/boots/STEWARD.boot.md` |
| Relay | `ION/06_intelligence/relay/relay/` | lane-native | `ION/03_registry/boots/RELAY.boot.md` |
| Vestige | `ION/06_intelligence/archaeology/vestige/` | lane-native | `ION/03_registry/boots/VESTIGE.boot.md` |

### 2.1 Current-phase rule for promoted lane-native roles

For the active branch, `Relay` and `Vestige` remain lawful lane-native source
continuity roles even after semantic promotion and domain settlement.

That means:

- their listed lane-native paths above remain source continuity now
- the branch should not create parallel `ION/agents/relay/` or `ION/agents/vestige/`
  source homes by convenience
- any future move into `ION/agents/{role}/` must happen through an explicit migration
  packet and a single cutover rule, not by gradual dual-writing

See:

- `ION/06_intelligence/orchestration/2026-04-22_promoted_lane_native_support_role_continuity_normalization_note.md`

### Boot Sequence (corrected)

```
1. Read own boot doc: ION/03_registry/boots/{AGENT}.boot.md
2. If continuity class is `agent-private`, read `ION/agents/{agent}/MINI.md` and `ION/agents/{agent}/CAPSULE.md`
3. If continuity class is `lane-native`, read the role's explicit lane-native continuity surfaces from its boot
4. Read ION/05_context/inbox/{agent}_* — tasks assigned to you
5. Read ION/05_context/signals/* — signals directed to you
6. Optionally read shared projections (`ION/MINI.md`, `ION/CAPSULE.md`, `ION/STATUS.md`) as projections only; if a compiled context path exists later, treat it the same way
7. Begin work per your template
8. On completion: update your authoritative source continuity surfaces and emit signals to `ION/05_context/signals/`
```

### What NEVER Happens

- Agent A writes to `ION/agents/B/MINI.md` — **NEVER**
- Agent A appends to a shared CAPSULE.md as if it were their own — **WRONG MODEL**
- Agent A updates "their section" of a shared STATUS.md — **WRONG MODEL**
- Any agent treats root-level MINI/CAPSULE/STATUS as their continuity — **WRONG MODEL**

---

## 3. HOW THIS CHANGES EXISTING DOCUMENTS

### Documents Still Requiring Careful Reading or Further Correction

| Document | What's Wrong | Correction |
|----------|-------------|-----------|
| `PLAN.md` | Older revisions taught root trio as source continuity and assumed a broader premium-parallel runtime | Teach private source continuity, projection status, and low-burn default runtime |
| `MULTI_CHAT_COORDINATION.md` | Still contains the larger target-shape parallel model even though transitional notes were added | Keep demoted behind the continuity law until fully rewritten |
| `ION_OVER_CURSOR_PROTOCOL.md` | Still describes subagent spawning as if it were normal baseline behavior | Treat as optional/future orchestration protocol unless explicitly invoked |
| `RELAY.boot.md` | Lane-native role with private relay continuity and projection-aware load order | Keep lane-native continuity as source truth until an explicit normalization migration exists |
| `VESTIGE.boot.md` | Lane-native archaeology role with projection-aware load order | Keep lane-native continuity as source truth until an explicit normalization migration exists |
| This file (`CONTINUITY_ARCHITECTURE.md`) | Previously overstated future compiled-path shape as if it already existed | Keep present-vs-future distinction explicit |

---

## 4. THE COMPILATION MODEL (future)

When a compiler exists, it may:
1. Read all `ION/agents/*/MINI.md` files
2. Read all `ION/agents/*/CAPSULE.md` files
3. Produce compiled projections at `ION/context/*.compiled.md` or an equivalent compiled path
4. These projections are READ-ONLY for all agents
5. Agents read projections for system awareness, write only to their own state

Until the compiler exists, the root-level files are manually curated
operator-facing projections. They are convenience views, not source authority.

---

## 5. TEMPORARY MANUAL RECOVERY MODE

During the consolidation phase (before automation exists):
- Each agent maintains private MINI/CAPSULE in `ION/agents/{name}/`
- Root `ION/MINI.md` and `ION/CAPSULE.md` are curated projections
- `ION/STATUS.md` is deprecated — agents report state in their own MINI.md
- Default runtime is low-burn sequential routing unless wider staffing is explicitly justified
- The minimal local template floor lives at `ION/07_templates/`
- Inter-agent coordination through inbox + signals only
- No agent assumes compiled context exists — everything is manual

---

## 6. SEE ALSO

- **`ION/02_architecture/CONTEXT_PLANES.md`** — diagram and **forbidden merges** for “context” (private vs projection vs tools vs ATLAS); complements this law without replacing it.
