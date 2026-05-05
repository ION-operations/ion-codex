---
type: proposal
from: Codex
created: 2026-04-22T18:10:00-04:00
status: ACTIVE
topic: Current-phase agent roster settlement packet for the active ION root
responding_to:
  - ION/06_intelligence/research/2026-04-22_codex_canonical_agent_roster_and_evolution_dynamics_proposal.md
  - ION/06_intelligence/orchestration/2026-04-13_staffing_and_semantic_identity_steward_consolidation_proposal.md
  - ION/03_registry/semantic_identities/README.md
  - ION/03_registry/daimon_matrix.yaml
  - ION/06_intelligence/orchestration/2026-04-22_codex_current_phase_role_and_boot_retirement_note.md
  - ION/02_architecture/STEWARD_CURRENT_PHASE_ORCHESTRATION_PROTOCOL.md
  - ION/02_architecture/CONTINUITY_ARCHITECTURE.md
  - ION/03_registry/current_phase_template_surface_registry.yaml
---

# Proposed Current-Phase Agent Roster Settlement Packet

## Purpose

Convert the broader roster proposal into one current-phase settlement surface that is easier to operationalize.

This packet does **not** claim final canon closure.
It does claim that the active root now has enough evidence to state:

- the settled current-phase core,
- the live support field,
- the immediate promotion candidates,
- and the explicit exclusions that should not be counted as live roster closure.

## Proposal

### Settlement rule

Read the current-phase roster in three bands:

1. **Settled core**
2. **Live support field**
3. **Promotion candidates / unresolved positions**

These bands are not all the same kind of truth.
Band 1 is semantically settled current-phase truth.
Band 2 is lawful live operation.
Band 3 is explicit next-hardening pressure.

### Band 1 — Settled core

| Role | Standing | True-name status | Rank / tier posture | Default carrier posture | Continuity home | Write relation | Audit relation |
|---|---|---|---|---|---|---|---|
| `Steward` | current-phase orchestration core | `SETTLED_CURRENT_PHASE` | `BOUNDED_ORCHESTRATION_STEWARD` | carrier-agnostic variable execution chassis | semantic/governing truth anchored in `STEWARD.semantic.yaml`; operational carriage through current-phase orchestration surfaces | may coordinate and activate support roles; must not silently mutate template law or constitutional truth | auditable by Nemesis; not self-ratifying |
| `Vizier` | architectural continuity core | `SETTLED_CURRENT_PHASE` | `BURDEN_BEARER_ARCHITECTURAL`, Tier 1.5 | variable high-judgment chassis | `ION/agents/vizier/` | architecture, plan, inbox dispatch, continuity/governance artifacts; no silent doctrine mutation without authorization | primary constructive line, still auditable by Nemesis and pressure-bound by Vice |
| `Vice` | contradiction-pressure core | `SETTLED_CURRENT_PHASE` | `INTERNAL_CONTRADICTION_PRESSURE`, Tier 1.5 | conjugate / selective high-judgment chassis | `ION/agents/vice/` | dissent notes, contradiction pressure, future-answerability witness; does not rewrite primary artifacts directly | internal counterforce; unanswered serious dissent blocks clean release posture |
| `Nemesis` | independent audit core | `SETTLED_CURRENT_PHASE` | `INDEPENDENT_AUDIT_GATE`, Tier 2 | independent review chassis | `ION/agents/nemesis/` | audit artifacts only; no source landing, no silent implementation power | external audit/release gate for the consolidated artifact set |

### Band 2 — Live support field

| Role | Standing | Semantic posture | Tier posture | Default carrier posture | Continuity home | Write relation | Audit relation |
|---|---|---|---|---|---|---|---|
| `Relay` | live persistent support role | semantically settled current-phase support role | Tier 4 | persistent low-cost user-facing relay chassis | lane-native: `ION/06_intelligence/relay/relay/` | relay lane only; no doctrine, registry, source code, or root-projection ownership | no audit authority; may package artifacts for Sovereign-facing review |
| `Vestige` | live persistent support role | semantically settled current-phase support role | Tier 4 | persistent low-cost archaeology chassis | lane-native: `ION/06_intelligence/archaeology/vestige/` | archaeology lane only; broad read, narrow write | no audit authority; may surface evidence used by Vice or Nemesis |
| `Mason` | live bounded execution specialist | boot-plus-mount | Tier 5 | economical implementation chassis | `ION/agents/mason/` | bounded implementation and tests only when explicitly tasked | no independent audit or release authority |
| `Scribe` | live bounded execution specialist | boot-plus-mount | Tier 5 | economical utility chassis | `ION/agents/scribe/` | archive, git hygiene, bulk file work, mechanical system surgery | no independent audit authority |
| `Thoth` | live bounded research specialist | boot-plus-mount | Tier 5 | economical or read-heavy research chassis | `ION/agents/thoth/` | research/evidence lanes only unless explicitly tasked otherwise | no independent audit authority; may supply evidence surfaces |
| `Atlas` | live bounded comparative specialist | boot-plus-mount | Tier 5 | economical or read-heavy comparative chassis | `ION/agents/atlas/` | comparative/reference production and atlas maintenance | no independent audit authority; evidence-tier-gated reference producer only |

### Band 3 — Promotion candidates / unresolved positions

This band may overlap with Band 2.
It exists because the live root needs a clean promotion policy, not just more names.

With the current pass, `Relay` and `Vestige` are no longer only abstract candidates.
They now have emitted promotion reviews and landed semantic identity records.
The remaining pressure is follow-on hardening rather than basic candidacy.

| Role | Current status | Why it matters | Recommended action |
|---|---|---|---|
| `Relay` | semantic record and communications-domain truth landed; front-door support role now stabilized | clearest front-door support role; reduces ambiguity between orchestration and user-facing packaging | next hardening should focus on continuity-home normalization and optional packet-family refinement, not re-arguing role existence |
| `Vestige` | semantic record, archaeology domain, and first archaeology binding landed; role now stabilized | carries durable drift, lineage, and stale-surface burden | next hardening should focus on continuity-home normalization and optional packet-family refinement rather than basic role closure |
| `Weaver` | protocol-mentioned, not boot-realized in current root | UI/presentation role should not remain folklore if truly needed | either instantiate with boot + continuity + binding, or remove from active prose until real |

### Explicit exclusions from current roster count

Do **not** count the following as live roster closure:

- `role.codex`
- `ION/03_registry/boots/CODEX.boot.md`
- `ION/03_registry/semantic_identities/CODEX.semantic.yaml`
- `VIZIER_DAIMON_GPT.boot.md`
- `VIZIER_DAIMON_OPUS.boot.md`

These are excluded from current live roster closure.
`Codex` is preserved only as historical carrier witness, not as a live current-phase role.

Do **not** count browser ChatGPT or other external surfaces as mounted internal roles by default.
Current truthful default remains bounded external carriage unless explicit mount law says otherwise.

## What changes operationally

If this packet is accepted as the working settlement surface, the active root should now behave as though:

1. the core roster is explicitly `Steward`, `Vizier`, `Vice`, and `Nemesis`
2. the live support field is explicitly `Relay`, `Vestige`, `Mason`, `Scribe`, `Thoth`, and `Atlas`
3. `Weaver` is treated as unresolved rather than silently assumed
4. the canonical front door is read as `Steward + Relay`
5. support-role promotion is governed by persistence, continuity burden, and drift risk rather than naming appetite
6. no one should speak as though carrier differences require a separate live roster entity
7. no one should speak as though the specialist layer is missing; the truer statement is that it exists but is not yet normalized

### Suggested next concrete artifacts

1. explicit packet-family enumeration per promoted support role if the branch wants stronger registry-level packet law than binding references alone
2. explicit `Weaver` instantiation packet only if UI/presentation burden becomes real
3. optional later generalization of support-role rank law if the branch wants these current refined classes abstracted into a wider family
4. only later, if truly needed, a bounded one-way migration packet for any promoted lane-native role that should move into `ION/agents/{role}/`

## Risks / edge cases

### Risk 1 — over-closing the support field

This packet should not be misread as a demand to semanticize every support role now.
That would contradict the current branch’s own staffing/semantic-identity settlement logic.

### Risk 2 — reactivating chassis-as-roster confusion

Older Codex-named surfaces remain in the tree as historical witness.
If they are casually re-read as live roster law, the branch will drift back into chassis-as-truename confusion.

### Risk 3 — treating lane-native continuity as permanent final form

`Relay` and `Vestige` are lawful today.
That does not mean their current continuity-home pattern is the final ideal shape.

### Risk 4 — counting protocol folklore as roster reality

`Weaver` is the main current case.
If a role is only named in orchestration prose but lacks a live boot, continuity home, and actual packet/binding reality, it should not be treated as equally settled.

## Open questions

1. Should the roster registry include explicit expected packet families per role, or should that remain in template bindings only?
2. Does `Weaver` deserve real current-phase instantiation, or is UI/presentation work too intermittent to justify a live role?
3. Should these current refined support-role rank classes remain role-specific, or later be generalized into a broader support-rank family?
4. Under what concrete trigger would a lane-native promoted role ever warrant explicit migration into `ION/agents/{role}/` rather than staying lane-native?
