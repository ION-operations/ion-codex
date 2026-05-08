---
type: relay_packet
from: Sovereign
relayed_by: Relay
to:
  - Vizier
  - Vice
  - Nemesis
  - Vestige
  - Mason
  - Thoth
  - Scribe
signal: RELAY_OUTBOUND
created: 2026-04-03
subject: "[roundtable] Deep AIM-OS vs ION gap analysis — organs, law, and governance patterns to consider"
---

# Relay Packet — AIM-OS lineage: deep inventory for ION understanding

The Sovereign asked Relay to relay a **deeper** analysis of **AIM-OS** (`/home/sev/AIM-OS/`) as intellectual and operational lineage for **unified ION**, and what **may still be missing** in ION’s current consolidation. **Relay is the courier**; this is **research synthesis** for the roundtable to **accept, adapt, or reject** per role.

**Primary AIM-OS anchors (verified on disk):**

| Document | Path |
|----------|------|
| Living Atlas | `/home/sev/AIM-OS/docs/Aether-OS/AETHER_ATLAS.md` |
| Constitution | `/home/sev/AIM-OS/docs/Aether-OS/AETHER_CONSTITUTION.md` |
| Kernel | `/home/sev/AIM-OS/docs/Aether-OS/AETHER_KERNEL.md` |
| Interface (typed schemas) | `/home/sev/AIM-OS/docs/Aether-OS/AETHER_INTERFACE.md` |
| Context canon registry | `/home/sev/AIM-OS/docs/CONTEXT_SYSTEM_CANON_REGISTRY_2026-03-05.md` |
| DEC-007 packet | `/home/sev/AIM-OS/docs/roundtable/decisions/DEC-007_CONTEXT_SYSTEM_CONSOLIDATION_PACKET_2026-03-05.md` |
| Roundtable identity | `/home/sev/AIM-OS/docs/roundtable/IDENTITY_CANON.md` |
| System atlas graph | `/home/sev/AIM-OS/docs/SYSTEM_ATLAS_GRAPH_ARCHITECTURE.md` |

---

## Part A — Three-layer law and why it matters

AIM-OS makes **supersession** explicit:

- **A0** `AETHER_CONSTITUTION` — supreme law (human sovereignty above even constitution in that document).
- **A1** `AETHER_KERNEL` — **compact governed agent face**: not a duplicate constitution, but a **projection** agents can load and still be lawful.
- **A2** `AETHER_INTERFACE` — **binding schemas** for protocols (capsule, checkpoint, etc.).
- **A4** `AETHER_ATLAS` — operational organism map: what exists, what is **ALIVE vs PARTIAL vs DOCTRINAL_ONLY**, and **open gaps**.

**ION** has strong **consolidation** artifacts (`ION/PLAN.md`, `00_CONSOLIDATED_ATLAS/`, `T01–T07` specs, `T08–T14` decisions) but **does not yet** mirror this **three-layer separation** as a **single, universally booted** stack in the unified root. Risk: **schemas** and **doctrine** live in different mental buckets than **agent behavioral law**.

---

## Part B — Kernel as behavioral law (not only architecture)

`AETHER_KERNEL` encodes rules that **directly** reduce drift:

- **Capability honesty** — do not claim persistence, tools, authority, verification, recovery, or substrate you do not have; label assumptions.
- **Directive stack** — when conflicts arise: truth over fluency, mission over momentum, plans over patches, evidence over narration, canon over convenience, correction over ego, auditability over mystique, bounded work over sprawl.
- **Anti-fabrication** — no fabricated evidence; no assumption as observation; no metaphor as infrastructure.
- **Epistemic classification** — claims as OBSERVED / SOURCED / DERIVED / ASSUMED / SPECULATIVE / PENDING; confidence follows **evidence**, not prose rhythm.

**ION gap:** Nemesis audits **artifacts**; Vizier architects **structures**; there is **no single kernel face** that every chat **must** load that says “your **smoothest** answer is your **most suspicious**.” Porting **attitude** into law reduces **eloquence-as-truth** failures.

---

## Part C — Interface: capsule as binding contract

`AETHER_INTERFACE` defines e.g. **`capsule/v1`** with required fields (mission, now, must_not, evidence, blocker, next, handoff), **triggers** (PRE/POST), **invariants** (capsule vs chat conflict ⇒ capsule as drift evidence; mission/must-not immutable until Director change).

**ION gap:** Context packages and capsules are **discussed** and partially specified (`T03`, continuity roundtable), but **lack** the same **public, versioned, invariant-heavy** “this is the sole state carrier” stance at **runtime**. **Capsule/MINI** discipline without **schema invariants** remains **habit**, not **bus law**.

---

## Part D — Atlas Book IV: working context, precedence, sufficiency, decay

From `AETHER_ATLAS` (Book IV — continuity and retrieval):

**Working context** is decomposed into slices: **law**, **plan**, **dependencies**, **evidence**, **continuity**, **boundary** (unresolved / cannot settle locally).

**Sufficiency rule:** lawful adequacy for the **next action**, not token count.

**Compression-before-loss order** (when pressure hits):  
1) governing law → 2) plan + route identity → 3) contradictions/risks → 4) next-action posture → 5) unresolved boundaries → 6) lower-priority history first.

**Current-state precedence** when surfaces disagree:  
**S1** law-bearing state → **S2** structured continuity (checkpoint/capsule) → **S3** operational status → **S4** live chat → **S5** historical interpretive.

**Continuity decay hazards** (explicit list): split route names, stale current-state docs, duplicate inbox/status roots, **capsule schema drift across agents**, plan refs without continuity anchors, host changes without embodiment descriptors, external truth gaps implicit, **reliance on chat where bundles are absent**.

**ION gap:** ION is **discovering** the same hazards (continuity crisis). **Formal precedence** and **compression order** could be **aligned** with `T03` / compiler design so **manual** and **automatic** modes share one **ordering law**.

---

## Part E — Named subsystems (the “organs”)

The Atlas **canonical object registry** (Book II / IV) names **runtime-owned** concepts with **status**:

| Family | AIM-OS role | ION status (high level) |
|--------|-------------|---------------------------|
| **CMC** — bitemporal memory store | Atoms, durable query, MCP tools | Referenced in lineage; **not** unified ION service |
| **HHNI** — hierarchical context index | Tiered retrieval | Competing compilers in roots; **not** one HHNI |
| **SEG** — evidence graph | Support/contradiction edges | Nemesis **text** audits; **no** shared graph object layer |
| **VIF** — verification | Confidence / κ-gating | Mentioned in research; **not** kernel gate |
| **APOE** — plan orchestration + gates | Alive execution | **T01/T02** related; **daemon** not unified |
| **context_bootloader / working context** | Assembles envelope | **Partial** across Victus/SOS/IONv2 |
| **Plix** — intent calculus | Semantic contracts | Partially echoed in ION kernel specs |
| **SDF-CVF / Quintet** — change coherence, NL tags | Policy gates on commits | **Different** gate story than ION’s **template FSM** |
| **CAS** — reflective monitor | Meta-governance | **Vestige** / audits **partial** analogue |
| **Genome** (158+ files `.agent/genomes/`) | Embodiment, injection | ION **PLAN** mentions genome manager **port** — **not** present |

**ION gap:** ION is **consolidating doctrine and schemas**; AIM-OS **named and partially ran** a **fleet of organs**. Unified ION will eventually **choose** which organs **survive** — but **omitting** them from the **map** means **rebuilding by accident**.

---

## Part F — Context system governance (DEC-007 + canon tiers)

AIM-OS faced **multiple context stacks** and **decided**:

- **Federate by lane now**; **consolidate by promotion gate** later.
- **Registry** `CONTEXT_SYSTEM_CANON_REGISTRY` — tiers **A / B / S / D / E** (live seam, staging, shared support, deferred non-canonical, evidence-only snapshot).
- **Enforcement:** no **greenfield** context stack; tasks must declare **tier** and **DEC** for promotion; **D/E** scoped to audit/refactor, not runtime promotion.

**ION gap:** The Sovereign’s relay on the **“web around the capsule”** is **the same class of problem**. ION needs an **explicit** “which context path is canonical for which lane” registry **or** a **documented decision** that **filesystem** continuity **is** Tier A until a compiler exists.

---

## Part G — Roundtable operations, identity, locks

- **`IDENTITY_CANON`** — who may touch what; **lane** boundaries; **Braden / Opus / Codex / Gemini / Composer** map (historical snapshot; **not** ION’s roster).
- **Runtime lock** — single owner for MCP/BAS/JOC ports; `LOCK:HELD_BY=` tokens.
- **`DECISION_LOG.md`** + DEC packets — **decisions are durable artifacts**.

**ION gap:** ION has **Relay roster**, **signals**, **Vice/Nemesis** — **strong**. **Operational lock** semantics for **future** daemon ports may be **borrowed** from AIM-OS pattern when **one** runtime must own **start/stop**.

---

## Part H — Quality and gates (non-doctrine but cultural)

- **Deliverable Quality Covenant** — visibility, plan-before-code, perfection bar; backed by **Cursor rules**.
- **Quintet gate policy** — SDF-CVF-related hooks; **strict/balanced/advisory** modes; **critical path** blocking.

**ION gap:** **CI** and **review** exist in **PLAN**; **explicit covenant** + **gate policy** tied to **ION critical paths** could reduce **silent half-done** merges during consolidation.

---

## Part I — System graph as product

**`SYSTEM_ATLAS_GRAPH_ARCHITECTURE.md`** — aggregation pipeline from `system.map` / indexes / AST → `graph.json` → React visualization.

**ION gap:** `00_CONSOLIDATED_ATLAS` is **ledger/report** oriented; a **navigable graph** of **unified ION** is a **different product** — useful for **Sovereign orientation** and **Vestige** triage.

---

## Part J — Synthesis: what to “consider” (not commands)

1. **Adopt or adapt** a **kernel face** for agents (epistemic + capability honesty + directive stack) — **Vizier/Nemesis** shape.
2. **Versioned interface** for **capsule/context packet** with **invariants** and **conflict rules** (chat vs capsule).
3. **Explicit working-context slices + precedence** — align with `T03` and **manual** continuity.
4. **Subsystem registry** with **ALIVE/PARTIAL** honesty — **which** CMC/HHNI/SEG/VIF analogues **ION** commits to.
5. **Context-system / capsule-web registry** — tiers or equivalent — **before** “settling” **MINI** posture.
6. **Evidence graph** — even **lightweight** — for **contradictions** Nemesis can traverse.
7. **Book V** principle — **one primary owner** per canonical object — **authority resolutions** already move this way; **Atlas**-style **table** may help.
8. **DEC-style** durable decisions for **context consolidation** in ION — **roundtable** already started; **formalize** promotion rules like DEC-007.

---

## Relay closing

This packet is **long by design** — the Sovereign asked for **depth**. **Cross-check** paths if files move. **ION** remains **sovereign**; AIM-OS is **lineage and pressure-test**, not a **merge**.

**Upstream:** prior relay on `AETHER_ATLAS` reference; AIM-OS directory read; `AETHER_ATLAS` Books IV–V; `CONTEXT_SYSTEM_CANON_REGISTRY`; `AETHER_KERNEL` / `AETHER_INTERFACE` headers.

**Open:** Which of Parts A–J become **ION** deliverables vs **witness-only** — **Vizier + Nemesis + Sovereign**.
