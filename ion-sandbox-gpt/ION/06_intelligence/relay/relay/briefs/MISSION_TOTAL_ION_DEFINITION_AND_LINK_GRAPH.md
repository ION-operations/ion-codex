---
type: mission_brief
authority: RELAY_DRAFT
from: Relay
template: SYSTEM_EVOLUTION
created: 2026-04-03
revised: 2026-04-03
status: DRAFT — NOT SOVEREIGN-RATIFIED
subject: Total definition of ION — research, direction, cross-linked intelligence
ratification: Pending Sovereign approval. Team may replace, fork, or ignore.
---

# Mission: Total ION Definition, Research, and Cross-Linked Intelligence

## Disclaimer (read first)

- This document is **Relay’s general draft**: a **working scaffold** of links, charters, and reading order. It is **not** Braden’s approval of content or structure unless the Sovereign explicitly ratifies it later.
- **The team may produce its own** hubs, missions, or indices in lawful lanes (e.g. Vizier research, Nemesis synthesis). Treat this file as **optional infrastructure**, not command authority.

The paragraphs below were **drafted by Relay** to capture a **possible** mission shape. They do **not** carry A0 supremacy unless the Sovereign adopts them verbatim.

> **Draft mission shape (Relay — not Sovereign-approved):** The team might **deeply research** the ION ecosystem, **explain at length** what each system is and how it relates, **define strategic and technical directions** with honesty about uncertainty, and **discuss with each other through the filesystem** by producing **linked, clearly labeled** documents. Depth could be **unbounded by token budgets** in principle; **closure** would be a Sovereign decision.

This file **routes** readers into major lanes and names **suggested outputs** so work can stay parallel without overwriting. **Vizier / Nemesis / others own** substantive direction and audit.

---

## 1. Mission outcomes (what “done” means)

| Outcome | Description |
|--------|-------------|
| **O1 — Ontology** | A shared vocabulary of ION subsystems (fingerprints, domains, evidence classes) aligned with the Atlas and with live ION doctrine. |
| **O2 — Direction** | Explicit statements of **where unified ION is going** (horizons in `ION/PLAN.md`), **what is provisional**, and **what would falsify** each claim. |
| **O3 — Lineage** | Traceable story from older roots (ION-BUILD, IONv2, SOS, Victus, etc.) to the unified root, with **witness vs authority** discipline. |
| **O4 — Coupled law** | Articulation of continuity as **protocol field** (Sovereign relay packets + roundtable): not only compliance, but **wholeness and tension-balance** of governance. |
| **O5 — Cross-links** | Every major artifact **links outward** to related roles’ docs and **links inward** from a maintained index (this hub or a Vizier-maintained master index). |
| **O6 — Dissent preserved** | Vice/Nemesis surfaces where **compression would hide risk** must remain visible; no “consensus by deletion.” |

---

## 2. Discussion protocol (how agents “talk” without a chat room)

1. **Write in your lawful lane** (see §6). Never overwrite another role’s continuity directory.
2. **Every substantive doc** begins with YAML frontmatter where possible: `type`, `from`, `responding_to` (paths), `status`, `created`.
3. **Cross-reference block** at end of each long doc:
   - **Upstream reads** — what you read to produce this
   - **Downstream expects** — what should read this
   - **Open questions** — explicit, numbered
4. **Signals:** when a slice is ready for review, emit a signal in `ION/05_context/signals/` pointing at the artifact (do not paste the whole doc into the signal).
5. **Relay** may produce **digests** and **link bundles** but does not own global truth files.

---

## 3. Canonical source map — workspace roots

All paths below are rooted at:

`/home/sev/ION - Production/`

### 3.1 Unified ION intelligence (`ION/`)

| Area | Path | Role |
|------|------|------|
| Routing / log (projection — see continuity law) | `ION/MINI.md`, `ION/CAPSULE.md`, `ION/STATUS.md` | Vizier-curated until compiled |
| Master plan | `ION/PLAN.md` | Governance |
| Architecture | `ION/02_architecture/` | Cross-cutting law & coordination |
| Boots | `ION/03_registry/boots/` | Per-agent identity |
| Daimon matrix | `ION/03_registry/daimon_matrix.yaml` | Vice pairing |
| Signals bus | `ION/05_context/signals/` | All roles |
| Comms / roundtable | `ION/05_context/comms/` | Visible discussion |
| Intelligence | `ION/06_intelligence/` | Audits, research, specs, decisions |
| Per-agent private continuity | `ION/agents/*/` | **Source continuity** per `CONTINUITY_ARCHITECTURE.md` |

### 3.2 Architecture files (read in this order for “systems view”)

| Order | File |
|------|------|
| 1 | `ION/02_architecture/CONTINUITY_ARCHITECTURE.md` — **corrected continuity law** |
| 2 | `ION/02_architecture/MULTI_CHAT_COORDINATION.md` — multi-chat bus model |
| 3 | `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md` — Cursor spawning |
| 4 | `ION/02_architecture/CONJUGATE_DAIMON_PROTOCOL.md` — Vice / Daimon |
| 5 | `ION/02_architecture/SOVEREIGN_RELAY_PROTOCOL.md` — Relay |
| 6 | `ION/02_architecture/ARCHAEOLOGY_DAEMON_PROTOCOL.md` + `ARCHAEOLOGY_DAEMON_CONTRACT.md` — Vestige |

### 3.3 Consolidated Atlas (`00_CONSOLIDATED_ATLAS/`)

Use these as **evidence and lineage** backbone:

| File | Contents |
|------|----------|
| `00_INPUT_ROOTS.md` | Input roots declaration |
| `01_PROJECT_UNIVERSE.md` | Universe of projects |
| `02_EVIDENCE_CLASSES.md` | Evidence class definitions |
| `03A_FILE_EVIDENCE_LEDGER.md` | File evidence |
| `03B_SUBSYSTEM_FINGERPRINT_LEDGER.md` | **Subsystem fingerprints** |
| `04A_LINEAGE_EDGE_LEDGER.md` | Lineage edges |
| `05A_AUTHORITY_COMPETITION_LEDGER.md` | **Authority competitions** |
| `06_MASTER_INDEX.md` | **Master index** — fingerprints, roots |
| `07_MASTER_REPORT.md` | Master report |
| `08_BLOCKERS_AND_MISSING_ROOTS.md` | Blockers |
| `09_CANONICALIZATION_QUEUE.md` | Canonicalization queue |
| `10_DENSIFICATION_PLAN.md` | Densification |
| `11_FINGERPRINT_SPLIT_QUEUE.md` | Fingerprint splits |
| `12_LINEAGE_GAP_QUEUE.md` | Lineage gaps |
| `13_DOMAIN_LOSS_REGRESSION_LEDGER.md` | Domain loss |
| `14_ROOT_CONTRIBUTION_LEDGER.md` | Per-root contributions |
| `15_MISSING_IN_NEWER_BUILDS_LEDGER.md` | Missing in newer builds |
| `16_WITNESS_VS_AUTHORITY_LEDGER.md` | Witness vs authority |
| `17_SYSTEM_FUNCTION_MATRIX.md` | **System function matrix** |
| `18_PER_ROOT_SYSTEM_MAP.md` | Per-root maps |
| `19_PARTIAL_MIGRATION_LEDGER.md` | Partial migrations |
| `20_OLDER_TO_NEWER_COMPARISON_MATRIX.md` | Older vs newer |

### 3.4 Kernel specs & authority decisions (`ION/06_intelligence/`)

| Area | Path |
|------|------|
| Phase 0 schemas | `ION/06_intelligence/specs/T0*.schema.yaml` (+ companion `.spec.md` where present) |
| T08–T14 resolutions | `ION/06_intelligence/decisions/T08-T14_authority_resolutions.md` |
| Audits | `ION/06_intelligence/audits/` |
| Research | `ION/06_intelligence/research/` |
| Continuity roundtable | `ION/06_intelligence/roundtable/continuity_crisis/` |
| Vice lane | `ION/06_intelligence/daimon/vizier/` |
| Vestige lane | `ION/06_intelligence/archaeology/vestige/` |
| Relay lane | `ION/06_intelligence/relay/relay/` |

### 3.5 External / multi-root codebases (named in `ION/PLAN.md`)

Research must **cite actual paths** when the workspace contains these roots. Typical names:

| Root | Contribution (summary from PLAN) |
|------|-----------------------------------|
| `SOS/` | Daemon, signals, Gatekeeper, constitution, template FSM |
| `SOS-OPUS/` | Article 23, Vizier, forensic templates, handoffs |
| `SOS-Gemini/` | CPAF / ambiguity field |
| `ION-BUILD/` | Kernel object model, governed write, capsule tooling |
| `IONv2/` | Package discipline, tests, graph compiler, schemas |
| `operation-victus/` | Engines, mission router, breadth |
| `Project-Gemini/` | UI / services |
| `ProjectOpus/` | Audit / archaeology witness |

If a root is absent from disk, **state absence** and work from Atlas + ION intelligence only.

### 3.6 Sovereign & Relay packets (continuity as “protocol field”)

| Artifact |
|----------|
| `ION/06_intelligence/relay/relay/outbound/2026-04-03_sovereign_continuity_as_protocol_field_to_ALL.md` |
| `ION/05_context/signals/RELAY_OUTBOUND_20260403_CONTINUITY_PROTOCOL_FIELD.signal.md` |

### 3.7 CBHF / research adjacency (conceptual coupling)

| Path | Note |
|------|------|
| `conjugate-basis-hidden-field/paper/working_paper_2026-04-02.md` | Present vs future answerability; conjugate bases — **analogy** for governance, not literal physics claim for ION |

---

## 4. Workstreams — depth mandate

Each role **produces one or more long-form artifacts** that:

- Define **scope**, **assumptions**, **known unknowns**
- Link **at least 10** upstream canonical paths (from §3) unless the role is narrowly scoped
- Include **cross-links** to sibling roles’ documents once those exist

### 4.1 Vizier — Strategic architecture & unified direction

**Suggested primary output:**  
`ION/06_intelligence/research/2026-04-03_TOTAL_ION_DIRECTION_vizier.md`  
(or successor dated filename)

**Must address:** Five horizons; Phase map; Tier 0 vs Tier 2/3 (per recalibration); what unified ION **is** as protocol loop; relationship of `ION/PLAN.md` to per-agent continuity.

**Must link:** `ION/PLAN.md`, `CONTINUITY_ARCHITECTURE.md`, Atlas `06`, `07`, `17`, T08–T14 decisions, roundtable kickoff.

### 4.2 Vice — Future answerability, risk of false convergence

**Suggested primary output:**  
`ION/06_intelligence/daimon/vizier/notes/2026-04-03_TOTAL_ION_DIRECTION_vice_haunt.md`

**Must address:** What must **not** be optimized away; release/block posture; hidden defects if the team moves too fast; **responds to** Vizier direction doc.

### 4.3 Nemesis — Auditability, drift, minimum controls

**Suggested primary output:**  
`ION/06_intelligence/audits/2026-04-03_TOTAL_ION_DEFINITION_audit_framework.md`  
(synthesis audit or append to stabilization audit with explicit **definition-of-done** for “total map”)

**Must address:** What evidence would **prove** the ontology; drift vectors; sequencing for clone scaling / automation (linked to continuity audits).

### 4.4 Vestige — Lineage, stale surfaces, excavation priority

**Suggested primary output:**  
`ION/06_intelligence/archaeology/vestige/reports/2026-04-03_TOTAL_ION_LINEAGE_vestige.md`

**Must address:** Which older continuity systems **haunt** the tree; broken references; watchlist triage; **historical_capsule_inventory** cross-check.

### 4.5 Thoth — Evidence packages per subsystem cluster

**Suggested primary output:**  
`ION/06_intelligence/research/2026-04-03_TOTAL_ION_EVIDENCE_THOTH.md`

**Must address:** Fingerprint clusters → file citations; contradictions between roots; open questions for Vizier.

### 4.6 Mason / Scribe — Implementation reality (when engaged)

**Suggested paths:**  
`ION/06_intelligence/research/` or package-local docs **+ signal**

**Must address:** What is buildable vs blocked; physical scaffolding for dispatch; CI/package boundaries — only when Sovereign releases downstream work.

### 4.7 Relay — Digests, bundles, link maintenance

**Outputs:**  
- This hub (`MISSION_TOTAL_ION_DEFINITION_AND_LINK_GRAPH.md`) — **maintain link rot checks** when asked  
- Optional digest: `ION/06_intelligence/relay/relay/briefs/2026-04-03_continuity_roundtable_brief.md` (roundtable-specific)  
- Inbound digests when Sovereign requests consolidation

---

## 5. Dependency graph (logical, not dispatch)

```
Atlas (evidence) ─────► Vizier direction doc ────┬──► Vice dissent / pressure
      │                                         │
      ├──► Thoth evidence digest                ├──► Nemesis audit criteria
      │                                         │
      └──► Vestige lineage report ──────────────┴──► Nemesis synthesis (later)
```

**Rule:** No role “finishes” the mission alone. **Convergence** is Nemesis + Sovereign + Vizier after visible artifacts exist.

---

## 6. Lane boundaries (non-negotiable)

| Write | Do not write |
|-------|----------------|
| Vizier: `ION/agents/vizier/`, research, architecture under authority | Others’ `agents/*` trees |
| Vice: `ION/06_intelligence/daimon/vizier/` | Vizier-owned plan ratification unilaterally |
| Nemesis: `ION/06_intelligence/audits/` | Code, doctrine merge without charter |
| Vestige: `ION/06_intelligence/archaeology/vestige/` | Production code |
| Relay: `ION/06_intelligence/relay/relay/*`, relay signals | `ION/MINI.md`, `ION/CAPSULE.md`, `ION/STATUS.md`, registry |
| Mason/Scribe: code lanes when released | Upstream doctrine |

---

## 7. First-wave reading order (single researcher bootstrap)

1. `ION/PLAN.md` — horizons and phases  
2. `00_CONSOLIDATED_ATLAS/06_MASTER_INDEX.md` + `07_MASTER_REPORT.md`  
3. `ION/02_architecture/CONTINUITY_ARCHITECTURE.md`  
4. `ION/06_intelligence/decisions/T08-T14_authority_resolutions.md`  
5. `ION/06_intelligence/audits/2026-04-03_continuity_stabilization_audit.md`  
6. `ION/06_intelligence/audits/2026-04-03_continuity_roundtable_kickoff.md`  
7. `ION/06_intelligence/research/2026-04-03_vizier_continuity_roundtable.md`  
8. `ION/05_context/comms/roundtable/vizier_response_recalibration.md`  
9. All `ION/06_intelligence/specs/T0*.schema.yaml` (skim + deep read T01–T04)  
10. `ION/06_intelligence/research/multi_model_orchestration_inventory.md`

---

## 8. Hub maintenance

| Action | Owner |
|--------|--------|
| Add new major doc to §3 tables | Vizier or Relay (Relay only for relay/briefs hub pointers) |
| Declare mission phase complete | Sovereign |
| Archive superseded hub | Vizier with `supersedes` frontmatter |

---

## 9. Upstream / downstream (for this file)

**Upstream reads:** Sovereign request via Relay; `ION/PLAN.md`; Atlas index; continuity roundtable INDEX; `RESPONSE_STATUS.md`; prior relay outbound on protocol field.

**Downstream expects:** All roles listed in §4; Nemesis eventual synthesis; Sovereign review.

**Open questions:**

1. Should a **single** “master TOC” live under `ION/06_intelligence/` vs only this hub?
2. When should Mason/Scribe be formally spawned for implementation sub-missions?
3. What is the ratification path for merging **Vizier direction** + **Nemesis audit criteria** into `ION/PLAN.md`?

---

*End of mission hub. Extend by appending new rows to §3 tables and new workstream rows to §4 — prefer additive edits with dated changelog footers.*
