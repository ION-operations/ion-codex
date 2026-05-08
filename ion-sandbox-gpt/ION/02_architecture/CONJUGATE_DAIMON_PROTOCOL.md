---
type: spec
authority: A2_CONSTITUTIONAL
template: SYSTEM_EVOLUTION
created: 2026-04-03T09:30:00-04:00
status: ACTIVE
connections:
  - ION/02_architecture/MULTI_CHAT_COORDINATION.md
  - ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md
  - SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md (K6 Chassis, Art. 17 Decoupling)
  - ION/06_intelligence/research/multi_model_orchestration_inventory.md
  - ION/06_intelligence/audits/2026-04-03_vizier_tightening_pass_audit.md
evidence:
  - "Blind model-swap test: GPT 5.4 as Vizier produced drift 8/100 (PASS) where Opus 4.6 had been producing 19-71/100 (CONDITIONAL/FAIL)"
  - "APOE model_selector.py implements 'smart + execution' cross-model pairing"
  - "Victus k_gate.py implements phase-aware routing"
  - "Relay Orchestration Journal: 'Multi-model collaboration is a design feature'"
---

# CONJUGATE DAIMON PROTOCOL

> Greek δαίμων (daimōn): Socrates' guiding spirit that stopped him when he was
> about to make a mistake. It never told him what to do — only what not to do.
> The daimon sees from a basis the conscious mind cannot access.
>
> **Conjugate:** operating in the basis conjugate to the Primary's. The Primary's
> strength in one cognitive basis is structurally its blindness in the other.
> The Conjugate Daimon preserves future answerability in the basis the Primary
> is actively collapsing through present interrogation.
>
> Connection: this protocol instantiates the coupled dual-track controller
> hypothesis (H3) from the Conjugate-Basis Hidden Field research program.
> The Primary is h_t^(I) (intention track). The Daimon is h_t^(V) (contextual
> potential track). Empirical evidence: Vizier@Opus drift 19→8 when GPT Daimon
> took the precision pass — the split outperformed the monolithic controller.

> Transitional note (2026-04-03):
> The Daimon protocol remains valid, but continuous premium dual-staffing is no longer the
> safe default runtime for the active root. Under current budget constraints, Daimon use
> should be selective and load-bearing, not ambient.

---

## 1. CORE MODEL

| Concept | Definition |
|---------|-----------|
| **Role** | The stable identity (e.g. Vizier). Persists across sessions, models, and chats. |
| **Primary** | The foreground chassis currently carrying the role. Operates in basis A. Owns the drafting authority. |
| **Daimon** | The conjugate shadow. Operates in basis B — the cognitive basis the Primary structurally cannot see. Reviews, challenges, preserves future answerability. Does NOT own the role. |
| **Nemesis** | Independent of the Primary/Daimon pair. Audits the consolidated output. The release gate. |

### CBHF Mapping

| CBHF Concept | Daimon Protocol Instantiation |
|---|---|
| Hidden field Ψ_t | The problem space (consolidation decisions, schema designs, authority resolutions) |
| Basis A (intention-facing) | Primary's cognitive strength (e.g. Opus: architecture, synthesis, vision) |
| Basis B (context-facing) | Daimon's cognitive strength (e.g. GPT: precision, contracts, consistency) |
| Measurement in A degrades B | Strong architectural commitment degrades contract precision |
| Controller h_t^(I) | Primary track — what is being built now |
| Controller h_t^(V) | Daimon track — what must be preserved for future answerability |
| Coupled dual-track (H3) | Primary + Daimon with explicit communication (daimon lane, dissent signals) |
| Future answerability | The ability to resolve downstream tasks without re-doing upstream work |

Example for Vizier:
- **Broad architecture work:** Vizier@Opus (Primary, basis A) + Vizier@GPT (Daimon, basis B)
- **Contract tightening work:** Vizier@GPT (Primary, basis B) + Vizier@Opus (Daimon, basis A)

The role stays continuous. The conjugate counterforce stays alive. Future answerability is preserved.

---

## 2. DAIMON RULES

The daimon is a real cognitive participant, not a rubber stamp. But it has strict boundaries.

1. **The Daimon does NOT own the role.** The Primary makes the final call.
2. **The Daimon does NOT release anything downstream.** Only the Primary (with Nemesis approval) releases.
3. **The Daimon does NOT dispatch workers.** No task files, no Mason/Scribe dispatch.
4. **The Daimon comments on the exact artifact set the Primary is producing.** Same inputs, bounded scope.
5. **The Daimon MAY challenge, concur, or propose alternate structure.**
6. **If the Daimon raises a serious dissent, the Primary MUST either incorporate it or explicitly answer it before release.** Unanswered dissents block release.
7. **Nemesis audits the consolidated set, not just the Primary draft.** Daimon notes are visible to Nemesis.

---

## 3. DAIMON MODES

Declared at task start by the Primary or Sovereign. Each mode defines how the Daimon engages.

### Mode 1: HAUNT
The Daimon reviews the Primary's draft and points out blind spots.

- Primary drafts first
- Daimon reads the draft and produces notes (blind spots, risks, alternatives)
- Primary incorporates or responds
- Lightest mode. Best for routine PLAN/SPEC work.

### Mode 2: MIRROR
The Daimon independently solves the same problem from the same artifact set. Both solutions are compared.

- Primary and Daimon both receive the same bounded input set
- Both produce independent drafts in their own lanes
- Primary consolidates the two drafts, noting which elements came from which
- Heaviest mode. Best for novel architecture or contested decisions.

### Mode 3: COUNTERFACTUAL
The Daimon does NOT rewrite the full artifact. It proposes a competing structure or alternate interpretation.

- Primary drafts the full artifact
- Daimon receives the draft and proposes a structural alternative ("what if X instead of Y?")
- Primary evaluates and either adopts, adapts, or records the counterfactual as a noted alternative
- Medium mode. Best for SPEC and CONSOLIDATION work.

---

## 4. WORKFLOW

```
1. Primary Vizier receives the task (from Sovereign or PLAN)
2. Sovereign opens Daimon chat with appropriate boot document
3. Daimon receives the same bounded artifact set as Primary
4. Primary drafts in their lane (ION/ working files)
5. Daimon responds in daimon lane (ION/06_intelligence/daimon/vizier/)
6. Primary reads daimon output and consolidates or records disagreement
7. Nemesis audits the consolidated set (including daimon notes)
8. Only after Nemesis clears may downstream release happen
```

---

## 5. WHEN TO INVOKE THE DAIMON

### Required (Daimon MUST be invoked)
- PLAN creation or major revision
- SPEC for kernel schemas or architecture
- CONSOLIDATION decisions on authority competition
- Doctrine changes (constitution, kernel)
- Release decisions (phase gates)
- Major architectural pivots

### Optional (Primary's judgment)
- Complex CODE review
- RESEARCH with high uncertainty
- Cross-project synthesis

### Not Required (Daimon adds noise, not value)
- Mechanical codegen from clear specs
- Lint fixes, test iteration
- File restructuring, git operations
- Low-risk worker task dispatch
- STATUS/CAPSULE updates

---

## 6. FILE LANES

### Daimon output directory
```
ION/06_intelligence/daimon/vizier/          # Vizier daimon lane
ION/06_intelligence/daimon/vizier/notes/    # HAUNT mode notes
ION/06_intelligence/daimon/vizier/mirrors/  # MIRROR mode independent drafts
ION/06_intelligence/daimon/vizier/counters/ # COUNTERFACTUAL proposals
```

### Daimon signal files
Filed in `ION/05_context/signals/` with the standard signal protocol:
```
DAIMON_{ROLE}_{SIGNAL_TYPE}_{timestamp}.signal.md
```

---

## 7. DAIMON SIGNAL VOCABULARY

| Signal | Meaning | Emitted By |
|--------|---------|-----------|
| `DAIMON_READY` | Daimon has loaded context and is ready to engage | Daimon |
| `DAIMON_NOTE` | Daimon has a review note, observation, or suggestion | Daimon |
| `DAIMON_CONCURRENCE` | Daimon agrees with Primary's approach — no changes needed | Daimon |
| `DAIMON_DISSENT` | Daimon disagrees with a specific structural choice. **Blocks release until Primary responds.** | Daimon |
| `DAIMON_COMPLETE` | Daimon has finished their review/mirror/counterfactual | Daimon |
| `DAIMON_INVOKED` | Primary is requesting Daimon engagement on a task | Primary |
| `DISSENT_ADDRESSED` | Primary has incorporated or explicitly answered a Daimon dissent | Primary |

---

## 8. DAIMON MATRIX

Declares the default Primary/Daimon pairing for each leadership role.

```yaml
# ION/03_registry/daimon_matrix.yaml
daimon_matrix:
  schema_version: "1.0"
  
  vizier:
    role: Vizier
    description: "Chief Architect / COO — strategic coordination, architecture, planning"
    primary_default: "claude-opus-4.6"
    daimon_default: "gpt-5.4"
    swap_triggers:
      - "Contract tightening, schema precision, type alignment → swap to GPT primary"
      - "Novel architecture, broad synthesis, human communication → swap to Opus primary"
    daimon_modes_required: [PLAN, SPEC, CONSOLIDATION, DOCTRINE, RELEASE]
    daimon_modes_optional: [CODE_REVIEW, RESEARCH]
    
  # Future: add daimon pairs for other leadership roles as protocol proves itself
  # nemesis:
  #   role: Nemesis
  #   primary_default: "gpt-5.4"
  #   daimon_default: "claude-opus-4.6"
  #   daimon_modes_required: [AUDIT of DOCTRINE, AUDIT of RELEASE]
```

---

### Current approved assignment

- Primary Vizier chassis: **Claude Opus 4.6**
- Vice (Conjugate Daimon) chassis: **GPT 5.4**

This remains the validated high-capability pairing for load-bearing architecture and
governance work. It should not be read as a claim that this pairing must run continuously
on every turn of the active low-burn runtime.

## 9. CONSOLIDATION RULES

When Primary and Daimon produce distinct outputs, the Primary consolidates:

1. **If Daimon concurs:** Note the concurrence in the artifact. Proceed.
2. **If Daimon has notes (HAUNT):** Primary reviews each note. Incorporate or respond in-artifact.
3. **If Daimon produced independent draft (MIRROR):** Primary produces a unified artifact noting which elements came from which source. Nemesis reviews the merge.
4. **If Daimon dissents:** Primary MUST either:
   - Incorporate the dissent (change the artifact), OR
   - Write an explicit `DISSENT_ADDRESSED` response explaining why the Primary's approach is retained
   - Unanswered dissents are a Nemesis audit failure condition
5. **All daimon output is preserved** in `06_intelligence/daimon/vizier/`. It is WITNESS material, not discardable.

---

## 10. NEMESIS INTERACTION

Nemesis remains independent of the Primary/Daimon pair:

- Nemesis does NOT participate in the Daimon exchange
- Nemesis audits the FINAL consolidated artifact, with daimon notes visible
- Nemesis checks that dissents were addressed
- Nemesis may cite daimon notes as evidence in audit findings
- If Nemesis finds that a Daimon dissent was ignored without response, that is an automatic HIGH finding

---

## 11. BOOT DOCUMENTS

Two daimon-specific boots for the Vizier role:

- `ION/03_registry/boots/VIZIER_DAIMON_OPUS.boot.md` — when Opus is the Daimon
- `ION/03_registry/boots/VIZIER_DAIMON_GPT.boot.md` — when GPT is the Daimon

These are distinct from the Primary Vizier boot because the Daimon has different lane permissions and a different output format.

---

## 12. SCALING POLICY

**Start with Vizier only.** Do not assign a Daimon to every agent yet.

The Daimon protocol adds real cognitive overhead. It is valuable for architecture, planning, and governance — exactly the work where model-specific blind spots are dangerous. It is noise for mechanical codegen and file restructuring.

Under the current low-burn runtime:

- invoke the Daimon for ratification, doctrine, release, major architecture, and contested consolidation
- do not keep a premium Daimon continuously active just because the protocol allows it
- prefer sequential kernel routing unless the extra Daimon pass clearly buys needed safety

If the Vizier daimon proves valuable over the next phase of work, consider:
- Daimon for Nemesis on doctrine-level audits
- Daimon for Praetor on large-scale planning

Do NOT assign a Daimon to Mason, Scribe, Thoth, or other execution-tier agents. Their work is bounded and audited by Nemesis. That's sufficient quality governance.
