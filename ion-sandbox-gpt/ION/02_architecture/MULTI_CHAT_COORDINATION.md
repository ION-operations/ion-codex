---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-02T22:00:00-04:00
status: ACTIVE
connections:
  - ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md
  - ION-BUILD/context/13_cognitive/2026-03-28_concurrent_access_protocol.md
  - ION-BUILD/context/specs/inter_agent_signal_protocol.md
  - SOS-OPUS/07_templates/actions/SIGNAL.md
  - SOS-OPUS/07_templates/actions/HANDOFF.md
  - SOS-OPUS/07_templates/actions/CURSOR_HANDOFF.md
---

# MULTI-CHAT ION COORDINATION PROTOCOL

> The filesystem is the bus. Each Cursor chat tab is a persistent chassis.
> Agents coordinate through signals, tasks, and lane isolation — not conversation.
> This protocol adapts ION's D44 Concurrent Access Protocol and Inter-Agent Signal
> Protocol for parallel IDE chat sessions running different LLM models.

> Transitional note (2026-04-03):
> This file currently describes the broader multi-chat target model, not the safest default
> runtime for the active root after the continuity roundtable and today's spend spike.
> Treat `ION/02_architecture/CONTINUITY_ARCHITECTURE.md`, the roundtable continuity-law
> package, `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`, and
> `ION/06_intelligence/research/2026-04-03_codex_end_to_end_law_protocol_template_review_and_kernel_router_transition.md`
> as higher-priority current operating truth.
> Default runtime is now Steward-held low-burn sequential kernel routing, commonly
> carried through the Cursor chassis, unless there is a clear reason to activate
> a wider multi-chat field.

---

## 1. THE OPERATING MODEL

The model below is the fuller parallel target shape.
It should not be read as the default required staffing pattern for every active turn.

### Current default field (2026-04-03)

| Role | Current posture |
|------|-----------------|
| Steward | Current-phase orchestration truename and default sequential router |
| Cursor carrier compatibility witness | Historical Cursor-native carrier / chassis alias for Steward-held routing |
| Vizier | Architecture / plan / authority framing when explicitly mounted |
| Vice | Selective future-answerability and dissent pressure |
| Nemesis | Selective independent audit and release-risk review |
| Mason / Scribe / Relay / Vestige | Economical bounded support roles |
| Thoth / Atlas | Economical research and terrain support roles |

```
┌────────────────────────────────────────────────────────────────┐
│                    SOVEREIGN (Braden)                          │
│         Opens chat tabs, assigns roles, reviews work           │
└──────────┬──────────┬──────────┬──────────┬───────────────────┘
           │          │          │          │
     ┌─────▼───┐ ┌───▼────┐ ┌──▼────┐ ┌──▼─────┐
     │ VIZIER  │ │NEMESIS │ │MASON │ │ THOTH  │  ... more as needed
     │ Chat 1  │ │Chat 2  │ │Chat 3│ │ Chat 4 │
     │Opus 4.6 │ │GPT 5.4 │ │Sonnet│ │ Any    │
     │  COO    │ │Auditor │ │Coder │ │Research│
     └────┬────┘ └───┬────┘ └──┬───┘ └───┬────┘
          │          │         │          │
          └──────────┴─────────┴──────────┘
                         │
              ┌──────────▼──────────┐
              │   ION/ FILESYSTEM   │
              │  (shared state bus) │
              │                     │
              │ MINI.md    - routing│
              │ CAPSULE.md - log    │
              │ STATUS.md  - board  │
              │ 05_context/inbox/   │
              │ 05_context/signals/ │
              │ 06_intelligence/    │
              └─────────────────────┘
```

---

## 2. RECOMMENDED TEAM COMPOSITION

### Phase 0-2 (Kernel + Structure): 7-8 agents

| Chat | Agent | Model | Role | Why This Model | Primary Lane |
|------|-------|-------|------|---------------|-------------|
| 1 | **Vizier** | Claude Opus 4.6 | Primary Chief Architect | Broad architecture, strategic synthesis, Sovereign-facing continuity | ION/PLAN.md, ION/MINI.md, ION/02_architecture/, coordination |
| 2 | **Vice** | GPT 5.4 (thinking) | Conjugate Daimon | Preserves future answerability, contract pressure, hidden-defect exposure | ION/06_intelligence/daimon/vizier/ |
| 3 | **Nemesis** | GPT 5.4 (thinking) | Inspector General | Deep reasoning catches contradictions and schema flaws | ION/06_intelligence/audits/, review of all agents' output |
| 4 | **Mason** | Composer 2 | Software Architect | Near-unlimited usage, fast, good at following specs | ION/04_packages/kernel/, ION/04_packages/governance/ |
| 5 | **Scribe** | Composer 2 | Archivist / Utility | Near-unlimited usage, fast for git ops, file moves, bulk work | ION/tests/, git operations, file restructuring |
| 6 | **Thoth** | Any capable model | Research Analyst | Deep file reading, schema extraction | ION/06_intelligence/evidence/ |
| 7 | **Vestige** | Composer 2 | Systems Archaeologist | Persistent, low-cost excavation of stale surfaces, open threads, and issue candidates | ION/06_intelligence/archaeology/vestige/ |
| 8 | **Relay** | Composer 2 | Relay | Persistent user-facing relay, packetization, and digesting without touching shared continuity | ION/06_intelligence/relay/relay/ |

### Phase 3-5 (Daemon + MCP + UI): expand to 8-10 agents

Add: **Praetor** (Operations/integration testing), **Weaver** (frontend/UI), **Galen** (debugging).
Multiple Composer 2 chats can run in parallel for bulk implementation work.

### Model Strength Map

| Model | Best For | Weak At | Usage Budget | ION Role Match |
|-------|---------|---------|-------------|---------------|
| Claude Opus 4.6 | Architecture, long context, careful reasoning, writing | Cost per token | Cursor Ultra (fair usage) | Vizier (COO) — reserve for strategic work |
| GPT 5.4 thinking | Deep logical reasoning, contradictions, contract tightening, auditing | May over-think simple tasks | Cursor Ultra (fair usage) | Nemesis (Auditor), Vice (Conjugate Daimon) — reserve for validation and precision passes |
| Composer 2 | Fast execution, following orders, mechanical tasks, code gen, persistent archaeology sweeps | Complex multi-step architecture | **Near-unlimited** | Mason, Scribe, Vestige, Argus, Weaver — **primary workhorse** |
| Claude Sonnet 4.5 | Fast code gen, moderate reasoning | Complex architecture | Cursor Ultra (fair usage) | Backup for Mason when Composer 2 insufficient |
| Gemini 2.5 Pro | Massive context window, large-file analysis | May hallucinate details | Cursor Ultra (fair usage) | Argus (Recon) for large codebases |
| Fast subagent models | RECONNAISSANCE, simple EVIDENCE | Anything requiring judgment | Via Vizier's subagent dispatch | Within-session parallel work |

### Budget Strategy

**Core principle:** Burn Composer 2 tokens freely. Conserve Opus/GPT 5.4/Sonnet for decisions that matter.

| Work Type | Use This Model | Rationale |
|-----------|---------------|-----------|
| Writing code from specs | Composer 2 | Near-unlimited, fast, obedient |
| File restructuring, moves, renames | Composer 2 | Mechanical, high volume |
| Running tests, fixing lint errors | Composer 2 | Iterative, many cycles |
| Git operations, archiving | Composer 2 | Mechanical |
| Schema design, architecture decisions | Opus 4.6 primary + Vice@GPT when required | Requires broad judgment plus conjugate pressure |
| Auditing schemas and code | GPT 5.4 | Requires adversarial depth |
| Planning, dependency analysis | Opus 4.6 or GPT 5.4 | Requires strategic reasoning |
| Deep file analysis, evidence extraction | Any capable model | Depends on file complexity |
| Persistent issue archaeology, open-thread excavation | Composer 2 | Cheap, always-on excavation without burning premium judgment budget |
| Reading large codebases (1000+ files) | Gemini 2.5 Pro | Context window advantage |
| User-facing relay, packetization, briefing | Composer 2 | Cheap, persistent, precise conversational courier |

The rule: **Composer 2 does the volume. Premium models do the judgment.** This lets us move fast without burning through the Ultra subscription on mechanical work.

---

## 3. LANE ISOLATION (D44 Layer 1)

Each agent has exclusive write access to their lane. This is the primary conflict prevention mechanism.

| Agent | May Write | May Read | Must Not Write |
|-------|-----------|----------|---------------|
| **Historical Cursor carrier witness** | preserved compatibility lanes and older routed packet references only | Read only as needed for lineage or artifact interpretation | Live orchestration authority, doctrine, registry truth, and silent role revival |
| **Vizier** | `ION/MINI.md`, `ION/CAPSULE.md`, `ION/PLAN.md`, `ION/STATUS.md`, `ION/02_architecture/`, `ION/01_doctrine/`, `ION/03_registry/`, `ION/07_templates/`, `ION/05_context/inbox/` (task dispatch) | Everything | Others' intelligence output |
| **Vice** | `ION/06_intelligence/daimon/vizier/`, `ION/05_context/signals/`, `ION/CAPSULE.md`, `ION/STATUS.md` | Everything | PLAN, MINI, doctrine, templates, registry, source code, other intelligence lanes |
| **Nemesis** | `ION/06_intelligence/audits/`, `ION/05_context/signals/` | Everything | Source code, doctrine, templates, MINI, PLAN |
| **Mason** | `ION/04_packages/` (assigned subdirectory only), `ION/tests/` (assigned tests) | Everything in scope | Doctrine, templates, registry, other packages |
| **Thoth** | `ION/06_intelligence/evidence/`, `ION/06_intelligence/research/` | Everything | Source code, doctrine, any mutation |
| **Vestige** | `ION/06_intelligence/archaeology/vestige/`, `ION/05_context/signals/`, `ION/CAPSULE.md`, `ION/STATUS.md` | Everything | Source code, doctrine, templates, registry, PLAN, MINI, other agents' write lanes |
| **Relay** | `ION/06_intelligence/relay/relay/`, `ION/05_context/signals/` | Everything | MINI, CAPSULE, STATUS, doctrine, templates, registry, source code, other agents' continuity lanes |
| **Praetor** | `ION/05_context/inbox/`, `ION/05_context/signals/`, `ION/STATUS.md` (progress section) | Everything | Source code, doctrine, architecture |

### Shared Files (require lock protocol)

These files may be written by multiple agents with coordination:
- `ION/CAPSULE.md` — append-only, each agent adds their own row with timestamp
- `ION/STATUS.md` — each agent updates their own section only
- `ION/05_context/signals/` — any agent may emit signals

---

## 4. COORDINATION THROUGH FILESYSTEM

### 4.1 STATUS.md — The Dashboard

Every agent reads and updates `ION/STATUS.md`. Each agent owns ONE section.

```markdown
# ION Team Status Board
Last updated: {latest timestamp}

## Vizier (Chat 1 — Claude Opus 4.6)
- **Current:** Working on T01 TransitionSchema
- **Blocked:** No
- **Needs from others:** Nemesis review of schema when complete
- **Last update:** 2026-04-02T22:00

## Nemesis (Chat 2 — GPT 5.4)
- **Current:** Reviewing PLAN.md for logical gaps
- **Blocked:** No
- **Needs from others:** Nothing yet
- **Last update:** 2026-04-02T22:05

## Mason (Chat 3 — Sonnet)
- **Current:** Waiting for T01 schema spec
- **Blocked:** Yes — needs T01 from Vizier
- **Needs from others:** TransitionSchema spec
- **Last update:** 2026-04-02T22:00
```

### 4.2 Signal Files — Machine-Readable Events

Per ION's D44 signal protocol. Filed at `ION/05_context/signals/`.

```yaml
# ION/05_context/signals/VIZIER_TASK_COMPLETE_T01_20260402T2200.signal.md
---
type: signal
from: Vizier
to: [Nemesis, Mason]
signal: TASK_COMPLETE
status: ACTIVE
created: 2026-04-02T22:00:00-04:00
payload:
  task: T01
  output: ION/04_packages/kernel/schemas/transition.py
  needs_review: true
  next_task: T02
---
T01 TransitionSchema complete. Filed at kernel/schemas/transition.py.
Nemesis: please audit for logical consistency.
Mason: you may now begin T13 (port model.py) using this schema.
```

### 4.3 Task Files — Work Dispatch

Vizier dispatches work by creating task files in `ION/05_context/inbox/`.
Other agents check their inbox on each session start.

```yaml
# ION/05_context/inbox/mason_T13_port_kernel_model.task.md
---
type: task
agent: Mason
template: CODE
priority: P0
target: ION/04_packages/kernel/model.py
depends_on: T01
created: 2026-04-02T22:00:00-04:00
from: Vizier
---

# Mission: Port ION Kernel Model

Port the Ion dataclass and all supporting types from ION-BUILD/src/ion/kernel/model.py
into the unified ION root at ION/04_packages/kernel/model.py.

## Source
- /home/sev/ION - Production/ION-BUILD/src/ion/kernel/model.py (940 lines)

## Requirements
- Adapt to use the new TransitionSchema from T01
- Keep IONv2's L0-L4 layering discipline (model.py is L0 — no internal imports)
- Use IONv2's AuthorityClass (8 members, not ION-BUILD's 12)
- Add __init__.py files for proper package structure
- Full type hints, no implicit Any

## DO NOT
- Change the fundamental Ion dataclass structure
- Add dependencies on anything outside stdlib + dataclasses
- Write to any file outside ION/04_packages/kernel/
```

### 4.4 File Locks — Concurrent Write Protection

Per D44 Layer 2. Only needed for shared files.

```yaml
# ION/05_context/signals/MASON_FILE_LOCK_model_py_20260402T2210.signal.md
---
type: signal
from: Mason
signal: FILE_LOCK
target_file: ION/04_packages/kernel/model.py
reason: "Porting kernel model per T13"
expected_duration: "< 15 minutes"
created: 2026-04-02T22:10:00-04:00
---
```

---

## 5. AGENT BOOT PROTOCOL

When the Sovereign opens a new Cursor chat tab and assigns it an ION agent role, the agent must boot by reading specific files.

### Boot Sequence (every agent, every session)

```
1. Read ION/MINI.md                    — current mission and routing state
2. Read ION/STATUS.md                  — what other agents are doing
3. Read ION/CAPSULE.md                 — what work has been completed
4. Read ION/05_context/inbox/{me}_*    — any tasks assigned to me
5. Read ION/05_context/signals/*       — any signals directed to me
6. Update STATUS.md                    — my section with current state
7. Begin work per assigned template
```

### Boot Document Format

Each agent gets a boot document at `ION/03_registry/boots/{AGENT}.boot.md`.
The Sovereign pastes this (or references it) when initializing a new chat.

---

## 6. COMMUNICATION PATTERNS

### Vizier → Agent (task dispatch)
1. Vizier creates `ION/05_context/inbox/{agent}_{task}.task.md`
2. Vizier emits signal: `VIZIER_TASK_ASSIGNED_{agent}_{task}.signal.md`
3. Vizier updates STATUS.md
4. Sovereign tells the agent chat to check inbox (or agent checks on its own)

### Agent → Vizier (completion report)
1. Agent writes output to their designated lane
2. Agent emits signal: `{AGENT}_TASK_COMPLETE_{task}.signal.md`
3. Agent updates CAPSULE.md with their entry
4. Agent updates STATUS.md
5. Vizier reads signal and validates output (Gatekeeper role)

### Release Discipline (Vizier + Vice + Nemesis)
1. Vizier may draft or complete an artifact set, but that does **not** release it downstream by itself
2. For artifact classes covered by the Conjugate Daimon Protocol, Vice reviews the exact same artifact set before release
3. Nemesis audits the consolidated artifact set before any downstream dispatch, phase-complete claim, or codegen release
4. Only after architect, daimon, and auditor have reviewed the relevant files may Vizier:
   - mark a phase release-ready
   - dispatch Mason/Scribe on the next dependent phase
   - recommend Sovereign approval
5. If Vice raises unresolved `DAIMON_DISSENT`, or Nemesis finds unresolved HIGH or CRITICAL issues, release is blocked until Vizier revises and the relevant review cycle is complete

### Vestige (Standing Archaeology)
1. Vestige is a persistent Composer 2 archaeology chat with full read access and a bounded write lane
2. Vestige continuously excavates stale authority surfaces, open threads, contradictions, and issue candidates
3. Vestige does not release, dispatch, or adjudicate; it produces retrievable reports and alerts for Vizier, Vice, Nemesis, and future automations
4. Vestige's outputs live under `ION/06_intelligence/archaeology/vestige/`

### Relay
1. Relay is a persistent Composer 2 user-facing relay chat
2. Relay translates Sovereign intent into structured relay packets and digests team outputs back to the Sovereign
3. Relay does not own planning, auditing, or release authority
4. Relay writes only to `ION/06_intelligence/relay/relay/` and relay signals
5. Relay does not touch shared continuity files (`MINI`, `CAPSULE`, `STATUS`)

### Agent → Agent (mediated through Vizier)
1. Agents do NOT communicate directly
2. Agent A emits signal with `to: Vizier` describing what Agent B needs
3. Vizier reviews and dispatches to Agent B if appropriate
4. Exception: Nemesis (Auditor) may emit AUDIT signals to any agent

### Sovereign → All (broadcast)
1. Sovereign writes `ION/05_context/signals/SOVEREIGN_BROADCAST_{topic}.signal.md`
2. All agents read on next session start

---

## 7. CONFLICT RESOLUTION

| Conflict | Resolution |
|----------|-----------|
| Two agents write same file | D44 file lock protocol. Second agent blocks. |
| Agent exceeds lane boundary | Nemesis catches in audit. Vizier corrects. |
| Agents disagree on approach | Escalate to Vizier. If architectural, escalate to Sovereign. |
| Agent produces invalid output | Vizier (Gatekeeper) rejects. Agent re-executes or task re-assigned. |
| Agent crashes mid-task | Lock expires (30 min). Task file remains in inbox for retry. |
| Model hallucination | Nemesis audits all output. Cross-model validation catches model-specific errors. |

---

## 8. WHY MULTI-MODEL TEAMS MATTER

The single most dangerous failure mode in AI-assisted development is **model-specific blind spots**. Every LLM has systematic biases in how it reasons about code and systems.

Running GPT 5.4 as Nemesis (auditor) against Claude Opus 4.6 as Vizier (architect) creates **adversarial validation** — each model catches the other's characteristic failures:

- Claude may over-commit to elegant abstractions that don't serve the actual use case → GPT catches the gap between beauty and function
- GPT may over-engineer safety checks that add complexity without value → Claude catches the unnecessary bureaucracy
- Both may share the same training-data blind spot on a specific pattern → the ION evidence protocol (read the actual file, not your memory) catches it

This is not just "more agents." This is **epistemic diversity as a governance mechanism.**
