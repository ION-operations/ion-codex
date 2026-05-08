# Activation/lifecycle overlap counterexample review packet

## Question class
Counterexample review for a coupled promotion candidate.

## Primary candidate under stress
- `../16_promotion_candidate_review/activation_lifecycle_joint_promotion_candidate_packet.md`
- `../15_quarantined_active_law_review/drafts/ACTIVATION_AUTHORITY_PROTOCOL.review_draft.md`
- `../15_quarantined_active_law_review/drafts/EXECUTOR_LIFECYCLE_PROTOCOL.review_draft.md`
- `../15_quarantined_active_law_review/drafts/ACTIVATION_LIFECYCLE_INTERFACE.review_note.md`

## Purpose
Test whether the activation/lifecycle set remains semantically stable when read through explicit negative and overlap cases.

This packet does **not** thaw the candidate.
This packet does **not** install active law.
This packet does **not** replace carrier-crossing worked examples or install-path mapping.

## Why this review is necessary
The current candidate is already legible in positive form. The remaining risk is that the boundary still collapses under pressure, especially when a reader tries to let one surface silently annex the work of another.

The failure mode is not only bad prose. It is doctrinal drift through plausible reinterpretation.

## Counterexample classes

### 1. Scheduler masquerading as activation authority
A schedule slot, queue ranking, or planned run is mistaken for lawful permission to cross into enactment.

Expected outcome:
- scheduler may prepare or nominate work
- scheduler does not grant enactment authority
- activation remains the crossing decision

### 2. Lifecycle re-adjudicating activation
An executor entry check or lifecycle prerequisite failure is interpreted as a fresh activation ruling.

Expected outcome:
- lifecycle may refuse entry on missing prerequisites
- lifecycle does not become the source of capability or enactment authority
- denial provenance must remain legible

### 3. Stale activation surviving invalidation
A once-valid activation token or decision is assumed to remain valid after material context drift, packet invalidation, or revoked prerequisites.

Expected outcome:
- stale activation is explicitly invalidatable
- re-entry does not mint hidden second activation authority
- invalidation emits a legible review/receipt event

### 4. Continuation becoming new activation
Takeover, replay, or continuity-safe re-entry is treated as a brand new enactment grant rather than a bounded continuation of prior lawful work.

Expected outcome:
- continuity law may restore or continue bounded work
- continuation does not silently bypass activation semantics
- the interface contract must state when revalidation is required

### 5. Carrier-specific enactment drift
Manual, daemonized, bootstrap, or external/API carriers interpret enactment crossing differently.

Expected outcome:
- carrier shell changes invocation form, not the governing meaning of enactment entry
- the same activation/lifecycle boundary survives across carriers

### 6. Runtime/session shell annexation
Service harnesses, daemon wrappers, or session surfaces are treated as if they own enactment permission.

Expected outcome:
- runtime shells are carriers and witnesses
- they may expose entry points and receipts
- they do not own activation authority by convenience

### 7. Settlement rewriting history
Lifecycle completion, pause, timeout, or abort records are used to retroactively reinterpret whether enactment was lawful in the first place.

Expected outcome:
- settlement records execution outcome
- settlement does not rewrite whether crossing into enactment was lawfully granted
- receipt linkage remains chronological and auditable

## Current review judgment
Current judgment: **counterexample review opened — candidate strengthened, still not thaw-ready**

What this pass establishes:
- the main overlap and annexation risks are now named concretely
- the promotion candidate can be challenged through explicit adversarial cases
- the repo now has a clearer barrier between semantic elegance and thaw readiness

What still remains after this pass:
- carrier-crossing worked examples
- install-path mapping into active architecture
- explicit settlement/receipt examples that bind activation, lifecycle, and packet law together

## Landing boundary
Counterexample review only.
No thaw authorization.
No active-law installation.
