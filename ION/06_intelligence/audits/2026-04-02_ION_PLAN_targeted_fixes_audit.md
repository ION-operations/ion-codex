---
type: audit
authority: A3_OPERATIONAL
template: AUDIT
created: 2026-04-02T21:47:49-04:00
subject: ION/PLAN.md Rev 2 with targeted fixes
status: COMPLETE
---
# Audit: ION/PLAN.md Rev 2 with targeted fixes

**Date:** 2026-04-02T21:47:49-04:00 | **Agent:** Nemesis (GPT 5.4) | **Type:** Audit
**Scope:** Re-audit the current `ION/PLAN.md` after Vizier's targeted fixes, with deeper validation against live SOS authority surfaces and the atlas competition ledger.
**Status:** Complete
**Template:** AUDIT (D27)

## Sources Examined
| Source | Lines Read | Verified? |
|--------|-----------|-----------|
| `ION/PLAN.md` | 331 | YES |
| `SOS-OPUS/07_templates/_MASTER.md` | 127 | YES |
| `SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md` | 258 | YES |
| `SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md` | 197 | YES |
| `SOS/02_architecture/CONTEXT_PROTOCOL.md` | 128 | YES |
| `00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md` | 62 | YES |
| `SOS/04_packages/gatekeeper/src/Gatekeeper.ts` | 487 | YES |
| `SOS/04_packages/protocol_parser/src/index.ts` | 177 | YES |
| `SOS/04_packages/heartbeat/src/heartbeat.py` | 403 | YES |
| `SOS/04_packages/heartbeat/src/daemon.ts` | 412 | YES |
| `SOS/04_packages/spawner/src/spawn_agent.py` | 495 | YES |
| `SOS/04_packages/spawner/src/index.ts` | 311 | YES |
| `SOS/04_packages/cognitive/src/context_compiler.py` | 218 | YES |
| `SOS/04_packages/distiller/src/index.ts` | 480 | YES |
| `SOS/04_packages/ion_kernel/governed_write.py` | 444 | YES |
| `SOS/04_packages/spawner/src/code_extractor.py` | 53 | YES |

## Subject
The current plan is no longer structurally dangerous. The original catastrophic faults are resolved: premature canonicalization is gated, authority resolution is front-loaded, IDE/manual mode is correctly framed as a working assumption, and the missing dependency/approval sections have been restored.

The remaining issues are narrower. They do not justify another `FAIL`. They do, however, keep the full plan in `CONDITIONAL` territory until the final cleanup pass is made.

## Findings
| # | Finding | Evidence | Severity |
|---|---------|----------|----------|
| F1 | The original critical sequencing failures are now materially resolved. Phase `0A` exists, Phase 1 is provisional rather than ratified canon, Phase `2B` blocks later phases until audit + approval, and pre-approval work is limited to non-protected paths. | `ION/PLAN.md:L97-L117`; `ION/PLAN.md:L121-L135`; `ION/PLAN.md:L155-L162`; `ION/PLAN.md:L315-L321` | INFO |
| F2 | The targeted fixes now map the plan to real live SOS authority splits, not just abstract atlas labels. `T10-T12` explicitly absorb the exact competing surfaces that still exist on disk: `Gatekeeper.ts` vs `protocol_parser`, `heartbeat.py` vs `daemon.ts`, `spawn_agent.py` vs `index.ts`, and `context_compiler.py` vs `distiller/index.ts`. | `ION/PLAN.md:L107-L109`; `00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md:L26-L33`; `SOS/04_packages/gatekeeper/src/Gatekeeper.ts:L5-L14`; `SOS/04_packages/protocol_parser/src/index.ts:L4-L11`; `SOS/04_packages/heartbeat/src/heartbeat.py:L2-L20`; `SOS/04_packages/heartbeat/src/daemon.ts:L10-L22`; `SOS/04_packages/spawner/src/spawn_agent.py:L2-L23`; `SOS/04_packages/spawner/src/index.ts:L10-L18`; `SOS/04_packages/cognitive/src/context_compiler.py:L2-L18`; `SOS/04_packages/distiller/src/index.ts:L5-L22` | INFO |
| F3 | The earlier template-law problem is now reduced to doctrine-sync rather than operational invalidity. The active registry in `_MASTER` does register `SPEC`, `CONSOLIDATION`, `TEST`, and `APPROVAL`, and the plan now explicitly explains how they relate to the core FSM. The remaining mismatch is that Constitution/K4 still name only the smaller core node vocabulary until provisional doctrine is updated. | `ION/PLAN.md:L93-L93`; `SOS-OPUS/07_templates/_MASTER.md:L69-L108`; `SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md:L93-L112`; `SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md:L94-L118` | LOW |
| F4 | The plan now contains two separate `## APPROVAL GATE` sections with overlapping but non-identical criteria. This creates a stale self-contradiction and makes the document less machine-readable than intended. | `ION/PLAN.md:L276-L287`; `ION/PLAN.md:L303-L311` | MEDIUM |
| F5 | A small set of high-severity authority competitions remain unclassified as either `Phase 0A`, later-phase work, or explicit witness-only/open-question items: `truth precedence / currentness`, `registry authority` vs capsule narrative, `canonicalization status`, `canonical OS claim`, `code materialization boundary`, and `SOS write authority substrate`. These do not block starting Phase 0 and 0A, but they do keep full-plan approval conditional. | `00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md:L4-L4`; `00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md:L12-L16`; `00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md:L39-L39`; `00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md:L60-L60`; `ION/PLAN.md:L97-L111`; `SOS/04_packages/ion_kernel/governed_write.py:L1-L22`; `SOS/04_packages/spawner/src/code_extractor.py:L6-L52` | MEDIUM |
| F6 | The execution-mode issue is effectively closed. The plan now frames IDE/manual mode as a working assumption pending `T08`, which is constitutionally cleaner than the previous claim of already-settled law. If the Sovereign ratifies this assumption now, the remaining ambiguity disappears. | `ION/PLAN.md:L34-L44`; `SOS/02_architecture/CONTEXT_PROTOCOL.md:L15-L30`; `SOS/02_architecture/CONTEXT_PROTOCOL.md:L31-L77` | INFO |

## Gaps Detected
| # | Gap | Impact | Template Coverage | Automation Coverage |
|---|-----|--------|-------------------|---------------------|
| G1 | Duplicate `APPROVAL GATE` sections remain in the same plan file | Human review and automation may read different gates as authoritative | partial | none |
| G2 | Residual high-severity `05A` rows are not yet classified as early, later, or explicit witness-only concerns | Future agents can still over-trust stale narrative authority surfaces during consolidation | partial | none |
| G3 | Constitution/K4 vs `_MASTER` template vocabulary is not yet synchronized | Template legality remains partly interpretive until T16 updates provisional doctrine | partial | none |

## Automation Layer Analysis
- `G1`: Add a plan validator that rejects duplicate top-level sections with the same heading, especially `Approval Gate`, `Dependency Graph`, and `Automation Integration`.
- `G2`: Add a coverage checker that compares high-severity rows in `00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md` against the plan and requires each row to be either assigned to a task or explicitly deferred.
- `G3`: Add a doctrine-sync lint that compares `_MASTER` template names against the constitutional/kernel FSM vocabulary and flags unsynchronized additions.

## Compliance Matrix
| Protocol | Source | Defined? | Enforced By AI? | Enforced By Automation? | Gap? |
|----------|--------|----------|-----------------|------------------------|------|
| Anti-premature canonicalization | `ION/PLAN.md`; `00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md` | YES | yes | no | NO |
| Early authority-resolution sequencing | `ION/PLAN.md`; `00_CONSOLIDATED_ATLAS/05A_AUTHORITY_COMPETITION_LEDGER.md` | YES | yes | no | NO |
| Execution-mode separation | `ION/PLAN.md`; `SOS/02_architecture/CONTEXT_PROTOCOL.md` | YES | yes | no | NO |
| PLAN completeness and machine readability | `ION/PLAN.md`; `SOS-OPUS/07_templates/actions/PLAN.md` | YES | partial | no | YES |
| Template legality and registry alignment | `SOS-OPUS/07_templates/_MASTER.md`; `SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md`; `SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md` | YES | partial | no | YES |
| Protected-path pre-approval gating | `ION/PLAN.md`; `SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md` | YES | yes | no | NO |

## Recommendations
| # | Action | Priority | Template Needed? | Automation Needed? |
|---|--------|----------|------------------|---------------------|
| R1 | Collapse the two `APPROVAL GATE` sections into one authoritative block and remove the stale duplicate. | P0 | PLAN revision | yes |
| R2 | Add one explicit note or appendix classifying the remaining unmapped high-severity `05A` rows as either later-phase tasks, explicit witness-only material, or open questions outside the Phase 0A gate. | P0 | PLAN revision | yes |
| R3 | If Sovereign agrees, ratify `IDE/manual` mode now as the temporary governing surface for consolidation. This removes the last practical execution-mode ambiguity. | P0 | APPROVAL | no |
| R4 | Approve only `Phase 0` and `Phase 0A` to begin immediately. Keep `Phase 1+` fully gated behind later approval exactly as the plan states. | P0 | APPROVAL | no |
| R5 | When `T10` runs, explicitly inspect `SOS/04_packages/ion_kernel/governed_write.py` and `SOS/04_packages/spawner/src/code_extractor.py` alongside the already-named write-boundary surfaces so write-authority resolution closes the remaining SOS duplicates cleanly. | P1 | CONSOLIDATION | no |

## Drift Score
**15 / 100 (Low Residual Drift)**

This is now a structurally sound plan with a few cleanup-level governance gaps rather than foundational contradictions.

## Verdict
**CONDITIONAL**

For the full plan, the correct verdict remains `CONDITIONAL`.

For the Sovereign's immediate decision, Nemesis recommends:
- **YES** — approve `Phase 0` + `Phase 0A` to begin now
- **YES** — ratify `IDE/manual` mode as the temporary governing surface for consolidation
- **NO major team change required** — current composition is adequate; optional helper research capacity can accelerate `T08-T14`, but is not required for safety

## CONTEXT UPDATES
- Filed this audit at `ION/06_intelligence/audits/2026-04-02_ION_PLAN_targeted_fixes_audit.md`
- This audit supersedes the prior `CONDITIONAL` re-audit for the current plan state
- Remaining work is now cleanup and scope-clarification, not structural rescue
