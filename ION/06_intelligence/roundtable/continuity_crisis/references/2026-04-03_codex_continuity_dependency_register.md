---
type: reference
authority: A3_OPERATIONAL
template: SYSTEM_EVOLUTION
from: Codex
created: 2026-04-03T12:28:54-04:00
status: IN_PROGRESS
ratification: NOT_RATIFIED
topic: Continuity dependency register
---

# Continuity Dependency Register

## Purpose

This register exists to make the “capsule protocol web” discussable as a set of
classified objects instead of a vague intuition.

Each row identifies:

- what the dependency is,
- what class of continuity object it is,
- where it appears in the active `ION/` root,
- where it appears as lineage witness,
- whether it appears required for Phase 0B,
- and what its current status looks like.

## Continuity Classes Used Here

- `SOURCE_CONTINUITY`
- `PROJECTION`
- `INTERCHANGE`
- `GOVERNING_LAW`
- `TEMPLATE_OBLIGATION`
- `ARCHIVE`
- `DEEP_CONTEXT`
- `VALIDATION`
- `IMMUNE_SYSTEM`
- `PRIVATE_MODULATION`
- `LINEAGE_WITNESS`

## Register

| Dependency | Class | Active Root Surface | Lineage Witness | Phase 0B Need | Current Status | Notes |
|------------|-------|---------------------|-----------------|---------------|----------------|-------|
| Per-role `MINI.md` | `SOURCE_CONTINUITY` | `ION/agents/vizier/MINI.md`, `ION/agents/vice/MINI.md`, `ION/agents/nemesis/MINI.md` | `ION-BUILD/agents/*/MINI.md` | Required | Partial | Source routing exists in part, not yet for all active roles. |
| Per-role `CAPSULE.md` | `SOURCE_CONTINUITY` | `ION/agents/vizier/CAPSULE.md` | `ION-BUILD/agents/*/CAPSULE.md` | Required | Partial | Source memory exists for Vizier; not yet uniformly restored across active roles. |
| Continuity law | `GOVERNING_LAW` | `ION/02_architecture/CONTINUITY_ARCHITECTURE.md`; proposed short law in `ION/05_context/comms/roundtable/vizier_synthesis_response.md` | `ION-BUILD/.ion-context/MANIFEST.md` | Required | Partial | Direction is converged, ratification still missing. |
| Boot/load order | `GOVERNING_LAW` | `ION/03_registry/boots/*.boot.md`; corrected sequence in `CONTINUITY_ARCHITECTURE.md` | `ION-BUILD/agents/OPUS/MINI.md`; `AIM-OS/docs/Aether-OS/AETHER_ATLAS.md` | Required | Incomplete | Boots exist, but private-first load order is not yet uniform. |
| Role write/read contract | `GOVERNING_LAW` | boots + architecture protocols | old lane structures across ION-BUILD / SOS-OPUS | Required | Incomplete | Still mixed by role; Relay especially reflects older root-centered start assumptions. |
| Output update obligations | `TEMPLATE_OBLIGATION` | no clearly landed active-root template layer found | `ION-BUILD/context/templates/actions/UPDATE_CAPSULE.md` | Required | Missing | Manual mode lacks a visibly active equivalent in new root. |
| Confidence routing / CSR | `IMMUNE_SYSTEM` | conceptually present in roundtable only | `ION-BUILD/context/templates/confidence/CSR.md` | Strongly recommended | Missing | Important if Phase 0B wants explicit anti-guessing behavior. |
| Anti-drift self-checks | `IMMUNE_SYSTEM` | conceptually present in roundtable and Vizier true-cores work | `ION-BUILD/.ion-context/MANIFEST.md` | Strongly recommended | Missing | Could be adopted as a light protocol before full templates return. |
| Ambiguity budget / OPEN_FIELD | `IMMUNE_SYSTEM` | present as concept in current research/synthesis | `SOS-OPUS/05_context/OPEN_FIELD.md` | Optional for first loop, likely kernel later | Partial | Probably too heavy to require fully for the first proof loop, but should stay visible. |
| Copy-on-update history | `ARCHIVE` | no per-role `history/` visible under `ION/agents/` | `ION-BUILD/context/history/*CAPSULE*`; `SOS-OPUS/05_context/history/*CAPSULE*` | Required | Missing | Without this, reconstructability remains weak. |
| PRE/POST temporal snapshots | `ARCHIVE` | not visibly active in root | historical capsule timelines in ION-BUILD / SOS-OPUS | Recommended | Missing | Strong witness that continuity was once richer than a flat work log. |
| Deep context-bank attachments | `DEEP_CONTEXT` | `ION/05_context/`, `ION/06_intelligence/`, role lanes | `ION-BUILD/.ion-context/MANIFEST.md` 15-section system | Required in reduced form | Partial | Present as scattered structure, not yet re-expressed as one governed attached web. |
| Signals bus | `INTERCHANGE` | `ION/05_context/signals/` | prior signal systems across older roots | Required | Active | Strongest currently working interchange surface. |
| Inbox task bus | `INTERCHANGE` | `ION/05_context/inbox/` | task/handoff lineage in earlier systems | Required | Partial | Directory exists, but no visible task files yet. |
| Public intelligence artifacts | `INTERCHANGE` | `ION/06_intelligence/` | same pattern across earlier roots | Required | Active | This is currently the main visible discussion and evidence bus. |
| Handoff/review packets | `INTERCHANGE` | named in law, not visibly normalized as active directory | handoff templates and earlier packet systems | Recommended | Partial | Useful but not yet a visibly landed standardized active surface. |
| Root `ION/MINI.md` | `PROJECTION` | `ION/MINI.md` | `ION-BUILD/context/MINI.compiled.md` | Required as operator convenience only if clearly marked | Partial | Exists, but still psychologically competes with source continuity. |
| Root `ION/CAPSULE.md` | `PROJECTION` | `ION/CAPSULE.md` | `ION-BUILD/context/CAPSULE.compiled.md` | Required as operator convenience only if clearly marked | Partial | Same issue as root MINI: present before its final law is embodied. |
| Root `ION/STATUS.md` | `PROJECTION` | `ION/STATUS.md` | compiled/operator status analogs | Optional for Phase 0B | Partial | Better treated as coordination view, not source. |
| Future compiled projection directory | `PROJECTION` | described as `ION/context/*.compiled.md` in `CONTINUITY_ARCHITECTURE.md` | `ION-BUILD/context/*.compiled.md` | Not required before proof loop if manual projections are explicit | Missing | Important future shape, not yet landed. |
| Projection compiler | `VALIDATION` | no visible new-root compiler | `ION-BUILD/tools/capsule-compiler.js` | Not required as primary before proof loop, but required later in shadow mode | Missing | Strong candidate for first post-loop automation. |
| Projection drift comparison procedure | `VALIDATION` | no explicit active procedure | dual-write / compilation-clean logic in witness templates | Required in minimal form | Missing | Even before code, the team likely needs a human comparison procedure. |
| Relay relationship/persona state | `PRIVATE_MODULATION` | `ION/06_intelligence/relay/relay/sovereign_profile.md`, `interaction_digest.md`, `persona_state.md` | Eunoia lineage | Not required globally, required locally for Relay | Partial | Attached to continuity web but must remain role-private, not global source continuity. |
| Role-private archaeology/daimon side state | `PRIVATE_MODULATION` | `ION/06_intelligence/daimon/vizier/`, `ION/06_intelligence/archaeology/vestige/` | older specialized lanes | Optional for first loop, important for full field | Active | These are attached role-specific continuities, not replacements for source pair. |
| Historical capsule inventory | `LINEAGE_WITNESS` | `ION/06_intelligence/roundtable/continuity_crisis/references/historical_capsule_inventory.md` | itself aggregates older roots | Required as witness, not runtime | Active | Useful guard against collapsing lineage into current convenience. |

## Immediate Reading of the Register

### What looks truly mandatory for a lawful first proof loop

1. per-role MINI/CAPSULE source continuity
2. ratified short continuity law
3. corrected boot/load order
4. one explicit update obligation protocol
5. signals bus
6. one live interchange path
7. projections clearly demoted to projection status
8. copy-on-update in at least a minimal form
9. one drift/uncertainty guard

### What looks important but can likely remain shadow or witness for the first loop

1. full projection compiler
2. full deep-branch restoration in historical richness
3. full OPEN_FIELD formalization
4. all specialized modulation systems

## Open Questions

1. Should copy-on-update history be mandatory before the very first proof loop,
   or can the first loop itself define the history discipline?
2. Is a lightweight manual update protocol enough for Phase 0B, or does the
   roundtable want a visibly restored template file before any proof loop?
3. Should the dependency register eventually split into:
   - kernel dependencies
   - attached private systems
   - witness-only lineage
4. Which active roles must have a full per-role pair before the table will call
   Stage B complete: Vizier only, leadership trio, or everyone participating?
