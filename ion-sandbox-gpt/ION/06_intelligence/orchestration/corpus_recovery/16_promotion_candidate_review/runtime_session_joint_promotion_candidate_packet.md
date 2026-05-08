# Runtime/session joint promotion-candidate packet

## Question class
Promotion-candidate review for a coupled runtime/session/API review set.

## Primary surfaces under review
- `../14_quarantined_runtime_review/RUNTIME_SESSION_AUTHORITY_PROTOCOL.review_draft.md`
- `../14_quarantined_runtime_review/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.review_draft.md`
- `../14_quarantined_runtime_review/API_RUNTIME_ENTRY_PROTOCOL.review_draft.md`
- `../15_runtime_seam_pressure/runtime_session_seam_findings.md`
- `../16_runtime_worked_examples/runtime_session_worked_examples.md`

## Purpose
State what must be true before the Lane C runtime/session trio may enter thaw
readiness review together.

This packet does **not** ratify active law.
This packet does **not** authorize installation into `ION/02_architecture/`.
This packet does **not** treat one member of the trio as independently
promotable while the others remain semantically unstable.

## Why this set must be reviewed jointly

The runtime/session center is not one file. It is a coupled boundary:

- session authority governs the runtime center itself
- queue/dispatch governs bounded movement inside that center
- API runtime entry governs external attachment into that center

Promoting one surface without the others would recreate the same ambiguity Lane
C was opened to remove:

- session authority would become too abstract to govern real movement
- queue/dispatch would drift upward into scheduler or activation territory
- API entry would drift sideways into fake runtime authority or shell-first
  convenience

## Promotion-candidate judgment
Current judgment: **candidate only — not yet thaw-ready**

Rationale:
- the three-surface split is legible in review space
- first adversarial seam pressure has already been applied
- first worked examples already survive without collapsing the split
- install-path ambiguity is now resolved
- first bounded receipt linkage is now explicit
- first bounded negative-case coverage is now explicit
- first bounded pause/re-entry/closure handling is now explicit
- the set is therefore ready to enter bounded thaw-readiness reassessment, not
  direct installation

## Promotion requirements
The set may become thaw-ready only when all of the following are true:

1. **Boundary closure**
   - session authority, queue/dispatch, and API entry have no unresolved
     overlap on center identity, queue ownership, carrier attachment, denial,
     or closure posture.

2. **Adjacent-law non-annexation**
   - scheduler law, runtime-state witness/reporting, supervised daemon/service
     shells, continuation law, settlement law, and activation law remain
     bounded neighbors rather than substitute centers.

3. **Carrier symmetry**
   - the trio reads coherently across internal/manual, supervised daemon, and
     external/API carriers without changing the governing meaning of the center.

4. **Continuity compatibility**
   - the set stays compatible with packet, handoff, takeover, continuation, and
     equivalence law without inventing a second runtime identity center.

5. **Receipt legibility**
   - session creation/re-entry, queue mutation/dispatch, API entry/denial, and
     closure/settlement witnesses can be named clearly without receipt overlap.

6. **Negative-case coverage**
   - the trio has explicit handling for invalid session identity, blocked queue
     prerequisites, API refusal, stale carrier binding, cancellation, runtime
     pause, and lawful re-entry.

7. **Worked-example survival**
   - the trio continues to survive concrete runtime flow narration without
     queue/dispatch becoming scheduler law, API entry becoming the center, or
     continuation/settlement becoming fake authority.

8. **Promotion mapping**
   - the repo can name where each promoted surface already lands or would land
     in `ION/02_architecture/`, what active-law surfaces it complements, and
     what current surfaces it explicitly does not replace.

## What would still block promotion even after prose polish
- vivid runtime prose without discipline on which surface owns the center
- queue/dispatch language that quietly re-answers activation or scheduler law
- API-facing convenience that rewrites the center from the transport side
- receipt names that sound complete but still leave denial or re-entry
  ambiguous
- promotion without an explicit coexistence map for runtime-state witness,
  supervised service shells, continuation, and settlement surfaces

## Recommended next bounded review
- produce one bounded thaw packet covering the exact active touch set,
  adjacent-file edits, and explicit review-only residue

## Landing boundary
Promotion-candidate review only.
No thaw authorization.
No active-law installation.
