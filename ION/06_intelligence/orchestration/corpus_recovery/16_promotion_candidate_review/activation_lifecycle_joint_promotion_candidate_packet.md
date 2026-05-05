# Activation/lifecycle joint promotion-candidate packet

## Question class
Promotion-candidate review for a coupled active-law set.

## Primary surfaces under review
- `15_quarantined_active_law_review/drafts/ACTIVATION_AUTHORITY_PROTOCOL.review_draft.md`
- `15_quarantined_active_law_review/drafts/EXECUTOR_LIFECYCLE_PROTOCOL.review_draft.md`
- `15_quarantined_active_law_review/drafts/ACTIVATION_LIFECYCLE_INTERFACE.review_note.md`

## Purpose
State what must be true before the activation/lifecycle set may enter thaw review together.

This packet does **not** ratify active law.
This packet does **not** authorize installation into `ION/02_architecture/`.
This packet does **not** treat one member of the set as independently promotable while the others remain semantically unstable.

## Why this set must be reviewed jointly
The activation center is not one file. It is a coupled boundary:

- activation authority decides whether bounded work may cross into enactment
- executor lifecycle governs what the chosen executor may do after that crossing
- the interface contract preserves the seam so lifecycle enforcement does not silently re-adjudicate activation, and activation does not quietly annex lifecycle state

Promoting one surface without the others would recreate the same ambiguity the controlled-reintegration work has been trying to remove.

## Promotion-candidate judgment
Current judgment: **candidate only — not yet thaw-ready**

Rationale:
- the semantic split is now legible in review space
- the failure modes are named
- the shared boundary contract exists
- but the set has not yet been exercised against explicit counterexamples, carrier-crossing examples, or concrete promotion/installation rules

## Promotion requirements
The set may become thaw-ready only when all of the following are true:

1. **Boundary closure**
   - activation authority, executor lifecycle, and interface contract have no unresolved overlap on enactment permission, lifecycle entry, denial semantics, or continuity-safe re-entry.

2. **Carrier symmetry**
   - the set reads coherently for manual, daemonized, bootstrap, and external/API carriers without changing the governing meaning of enactment permission.

3. **Continuity compatibility**
   - the set does not conflict with handoff, takeover, packet, continuation, or equivalence law.

4. **Scheduler non-annexation**
   - scheduler law remains upstream planning/gating law and does not expand into activation adjudication or lifecycle state control.

5. **Runtime non-annexation**
   - runtime/session shells remain carriers and witnesses, not the source of activation authority.

6. **Receipt legibility**
   - the set can state what receipt or ledger facts must exist at enactment entry, during execution, and at bounded settlement.

7. **Negative-case coverage**
   - the set has explicit handling for denial, stale activation, invalidated prerequisites, mid-flight pause/hold, timeout, and continuity-safe re-entry.

8. **Promotion mapping**
   - a concrete install path exists showing where each promoted surface would land in active architecture, what it would supersede or leave unchanged, and what would remain quarantined.

## What would still block promotion even after surface polish
- vivid prose without boundary discipline
- lifecycle logic that silently re-decides capability truth
- activation language that quietly assumes queue/session primitives not yet ratified
- carrier-specific shortcuts that change doctrine by implementation convenience
- promotion without an explicit coexistence plan for current scheduler, continuation, and packet law

## Recommended next bounded review
- produce explicit counterexample tests in prose for mistaken activation/lifecycle overlap
- produce one carrier-crossing worked example set
- produce one install-path note for eventual `02_architecture/` thaw review

## Landing boundary
Promotion-candidate review only.
No thaw authorization.
No active-law installation.
