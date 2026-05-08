---
type: audit
authority: A3_OPERATIONAL
template: AUDIT
created: 2026-04-02T22:20:23-04:00
subject: Vizier Phase 0 schema set (T01-T07)
status: COMPLETE
---
# Audit: Vizier Phase 0 schema set (T01-T07)

**Date:** 2026-04-02T22:20:23-04:00 | **Agent:** Nemesis (GPT 5.4) | **Type:** Audit
**Scope:** Audit the current Phase 0 outputs in `ION/06_intelligence/specs/` (`T01` through `T07`) for internal consistency, source fidelity, and implementation readiness before they are used as the basis for later kernel work.
**Status:** Complete
**Template:** AUDIT (D27)

## Sources Examined
| Source | Lines Read | Verified? |
|--------|-----------|-----------|
| `ION/MINI.md` | 25 | YES |
| `ION/PLAN.md` | 338 | YES |
| `ION/CAPSULE.md` | 29 | YES |
| `ION/05_context/signals/VIZIER_PHASE0_COMPLETE_20260403T0040.signal.md` | 34 | YES |
| `ION/05_context/signals/VIZIER_TASK_COMPLETE_T01_20260402T2345.signal.md` | 17 | YES |
| `ION/06_intelligence/specs/T01_TransitionSchema.yaml` | 455 | YES |
| `ION/06_intelligence/specs/T02_WorkUnitSchema.yaml` | 194 | YES |
| `ION/06_intelligence/specs/T03_ContextPackageSchema.yaml` | 174 | YES |
| `ION/06_intelligence/specs/T04_CommitDeltaSchema.yaml` | 123 | YES |
| `ION/06_intelligence/specs/T05_OpenQuestionSchema.yaml` | 75 | YES |
| `ION/06_intelligence/specs/T06_AuthorityClassSchema.yaml` | 123 | YES |
| `ION/06_intelligence/specs/T07_SignalSchema.yaml` | 184 | YES |
| `SOS/04_packages/heartbeat/src/heartbeat.py` | 403 | YES |
| `SOS/04_packages/heartbeat/src/daemon.ts` | 412 | YES |
| `SOS/04_packages/spawner/src/spawn_agent.py` | 495 | YES |
| `SOS/04_packages/spawner/src/index.ts` | 311 | YES |
| `SOS/04_packages/spawner/src/task_spawner.py` | 96 | YES |
| `SOS/04_packages/heartbeat/src/signal_router.py` | 182 | YES |
| `SOS/04_packages/cognitive/src/context_compiler.py` | 218 | YES |
| `SOS/04_packages/distiller/src/index.ts` | 480 | YES |
| `SOS/04_packages/gatekeeper/src/Gatekeeper.ts` | 487 | YES |
| `SOS/04_packages/protocol_parser/src/index.ts` | 177 | YES |
| `SOS/04_packages/ion_kernel/governed_write.py` | 444 | YES |

## Subject
Vizier's Phase 0 work is directionally strong and conceptually ambitious, but it is not yet safe to treat as an implementation-ready kernel contract. The main problem is not lack of thought. It is that the current outputs still mix three different layers without resolving them cleanly:

1. human-readable spec documents
2. machine-readable schemas
3. current SOS runtime behavior

That mix creates contradictions at exactly the boundaries later code generation would depend on.

## Findings
| # | Finding | Evidence | Severity |
|---|---------|----------|----------|
| F1 | The Phase 0 outputs are not actually machine-readable YAML schemas. The plan says Phase 0 produces YAML-first specs that later compile into code, but the files in `ION/06_intelligence/specs/` are markdown documents with frontmatter, headings, prose, and fenced YAML snippets saved under `.yaml` names. As written, they cannot be consumed directly by codegen or validation tooling. Phase 0 therefore cannot honestly be treated as complete in the machine-contract sense. | `ION/PLAN.md:L77-L91`; `ION/06_intelligence/specs/T01_TransitionSchema.yaml:L1-L21`; `ION/06_intelligence/specs/T01_TransitionSchema.yaml:L64-L67`; `ION/06_intelligence/specs/T02_WorkUnitSchema.yaml:L1-L19`; `ION/06_intelligence/specs/T02_WorkUnitSchema.yaml:L44-L47` | CRITICAL |
| F2 | The schema set still disagrees on the kernel's most important boundary: whether agents write artifacts directly or propose deltas that the daemon commits. `T01` models execution as producing an artifact at `{task_target_path}` before validation, while `T02` and `T04` say the agent executes a WorkUnit and returns a `CommitDelta`, and only the daemon commits. That is a foundational architecture contradiction. | `ION/06_intelligence/specs/T01_TransitionSchema.yaml:L232-L277`; `ION/06_intelligence/specs/T01_TransitionSchema.yaml:L278-L337`; `ION/06_intelligence/specs/T02_WorkUnitSchema.yaml:L23-L29`; `ION/06_intelligence/specs/T04_CommitDeltaSchema.yaml:L20-L25`; `ION/06_intelligence/specs/T04_CommitDeltaSchema.yaml:L33-L64` | CRITICAL |
| F3 | `T01` is internally inconsistent as a schema. `OutputSpec.output_type` does not include `CONTEXT_PACKAGE`, yet `compile_context` emits one. `State.template` is typed as required `string`, yet daemon states set it to `null`. The general `Transition` shape requires inputs/outputs/writes/authority, yet the `FSM.template_chain` transition instances omit those fields entirely. This means `T01` cannot currently act as a single coherent validation target. | `ION/06_intelligence/specs/T01_TransitionSchema.yaml:L88-L105`; `ION/06_intelligence/specs/T01_TransitionSchema.yaml:L117-L128`; `ION/06_intelligence/specs/T01_TransitionSchema.yaml:L169-L198`; `ION/06_intelligence/specs/T01_TransitionSchema.yaml:L223-L226`; `ION/06_intelligence/specs/T01_TransitionSchema.yaml:L389-L423` | HIGH |
| F4 | `T04` does not actually carry the structures that `T05` requires. `CommitDelta.proposed_open_questions` is only `list[string]`, while `T05` defines a rich `OpenQuestion` object with `origin_*`, `domain`, `scope_ref`, `needed_from`, `priority`, and `status`. `T04` also documents `REQUIRES_RECONCILIATION` as a valid commit outcome but omits it from `CommitDelta.status`. This makes first-class unresolved questions and reconciliation outcomes only partially representable. | `ION/06_intelligence/specs/T04_CommitDeltaSchema.yaml:L57-L64`; `ION/06_intelligence/specs/T04_CommitDeltaSchema.yaml:L99-L105`; `ION/06_intelligence/specs/T05_OpenQuestionSchema.yaml:L27-L57`; `ION/06_intelligence/specs/T05_OpenQuestionSchema.yaml:L71-L74` | HIGH |
| F5 | The plan's machine-readable progress is stale relative to Vizier's own latest work. `ION/PLAN.md` still says `completed_tasks: 0` and keeps `T01-T07` marked `TODO`, while `MINI.md`, the Phase 0 completion signal, and `CAPSULE.md` all say Phase 0 is complete. That breaks the plan's automation contract and makes the completion claim harder to trust. | `ION/PLAN.md:L1-L12`; `ION/PLAN.md:L81-L89`; `ION/MINI.md:L6-L10`; `ION/05_context/signals/VIZIER_PHASE0_COMPLETE_20260403T0040.signal.md:L11-L23`; `ION/CAPSULE.md:L21-L28` | MEDIUM |

## Gaps Detected
| # | Gap | Impact | Template Coverage | Automation Coverage |
|---|-----|--------|-------------------|---------------------|
| G1 | No separate machine-readable artifact exists for the schemas | Mason cannot safely generate code or validators from the Phase 0 outputs | partial | none |
| G2 | No explicit reconciliation between current SOS direct-write runtime and future CommitDelta-based kernel | Implementers can code the wrong boundary and bake in drift early | partial | none |
| G3 | No shared cross-schema enum/shape layer for open questions, signal types, and transition outputs | Later schemas reference each other conceptually but not structurally | partial | none |
| G4 | No automatic sync between plan frontmatter/task statuses and capsule/signal state | Dashboard/progress automation can report false plan status | partial | none |

## Automation Layer Analysis
- `G1`: Add a schema build step that extracts or generates raw YAML/JSON schema artifacts from the human-readable spec documents, and fail if the result is not parseable.
- `G2`: Add a reconciliation matrix validator that forces each schema to declare whether it models current SOS behavior, future unified ION behavior, or both.
- `G3`: Generate shared enums/types for signal kinds, question proposals, artifact outputs, and transition I/O from one canonical definition instead of duplicating freeform strings.
- `G4`: Add a plan progress synchronizer that updates `completed_tasks` and per-task statuses when `TASK_COMPLETE` signals or capsule rows are filed.

## Protocol Compliance Matrix
| Protocol | Source | Defined? | Enforced By AI? | Enforced By Automation? | Gap? |
|----------|--------|----------|-----------------|------------------------|------|
| YAML-first schema contract | `ION/PLAN.md` | YES | partial | no | YES |
| Transition/work-unit/context/delta coherence | `T01`-`T04` | YES | partial | no | YES |
| Open question first-class state | `T04`; `T05` | YES | partial | no | YES |
| Signal naming and routing standardization | `T01`; `T07`; `signal_router.py`; `spawn_agent.py` | YES | partial | no | NO |
| Plan machine-readability and status tracking | `ION/PLAN.md`; `SOS-OPUS/07_templates/actions/PLAN.md` | YES | partial | no | YES |

## Recommendations
| # | Action | Priority | Template Needed? | Automation Needed? |
|---|--------|----------|------------------|---------------------|
| R1 | Split each Phase 0 schema into two artifacts: a human-readable `SPEC` document and a raw machine-readable schema artifact. Do not call Phase 0 complete until the raw artifacts exist and parse. | P0 | SPEC revision | yes |
| R2 | Resolve the kernel boundary explicitly: either revise `T01` so agents emit `CommitDelta` objects and the daemon commits artifacts, or revise `T02/T04` to match a direct-write model. The set cannot keep both stories. | P0 | SPEC revision | yes |
| R3 | Replace `proposed_open_questions: list[string]` with a structured proposal shape that can normalize into `T05`, and add `REQUIRES_RECONCILIATION` to `T04` status handling or move it to a daemon-side validation result type. | P0 | SPEC revision | yes |
| R4 | Update `ION/PLAN.md` now: increment `completed_tasks`, mark `T01-T07` complete, and keep the machine-readable plan state aligned with `MINI.md`, signals, and `CAPSULE.md`. | P1 | PLAN revision | yes |
| R5 | Before Mason uses these schemas for codegen, add one explicit source-mapping appendix stating which parts mirror current SOS runtime and which parts are intentional unified-ION departures. | P1 | SPEC or PLAN addendum | no |

## Drift Score
**53 / 100 (Moderate-High Drift)**

The Phase 0 schema work is conceptually valuable, but the current outputs still drift too far from a clean, unified machine contract to be treated as complete.

## Verdict
**FAIL**

Vizier's latest Phase 0 work should not yet be treated as implementation-ready or as truly complete. The right next move is revision, not code generation.

## CONTEXT UPDATES
- Filed this audit at `ION/06_intelligence/audits/2026-04-02_phase0_schema_set_audit.md`
- This audit applies to the Phase 0 schema set (`T01-T07`), not to the earlier plan audit cycle
- The most urgent follow-up is to repair the schema boundary and emit real machine-readable artifacts
