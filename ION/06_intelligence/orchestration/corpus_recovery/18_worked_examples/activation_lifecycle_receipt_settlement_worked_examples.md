# Activation/lifecycle receipt and settlement worked examples

## Purpose
Show the activation/lifecycle candidate operating through explicit receipt lineage and settlement classification without losing the boundary between:
- enactment permission,
- executor transition law,
- runtime/carrier witness surfaces,
- and settlement as history closure rather than retroactive authority.

## Common invariant sequence
Across all worked examples, the lawful sequence remains:

1. bounded work candidate exists
2. activation decision emits one explicit activation receipt or denial witness
3. lifecycle transitions emit bounded executor-state witnesses
4. runtime/carrier surfaces emit operational receipts about what actually happened
5. settlement reads those witnesses and classifies closure, deferment, escalation, or re-entry posture
6. future re-entry, if any, occurs only through explicit preserved-authority or fresh-activation paths

The key boundary is this:
**receipts witness; settlement classifies; neither one grants or rewrites enactment permission.**

---

## Example 1 — Successful enactment with accepted settlement

### Situation
A manual or supervised run is lawfully activated, enters enactment, completes its bounded task, and returns a clean result.

### Lawful reading
- Activation authority decides whether the task may cross into enactment.
- Lifecycle governs claim/readiness/entry and bounded return.
- Runtime or carrier receipts witness actual completion.
- Settlement closes the history by citing those receipts; it does not recreate the enactment decision.

### Example flow
1. `ActivationRequest` is presented for a bounded task.
2. Activation authority emits `ALLOW` and persists an activation receipt.
3. Lifecycle emits `CLAIM`, `READY`, and `ENTER`.
4. The carrier or runtime emits a completion receipt.
5. Lifecycle emits `RETURN` and `RELEASE` as appropriate.
6. Settlement reads the activation receipt, lifecycle chain, and completion receipt.
7. Settlement records `ACCEPTED_AS_IS`.
8. The task closes as durable history.

### Boundary proved
- completion receipt is a witness, not fresh authority
- settlement closes the record without restating activation/lifecycle from scratch
- accepted settlement does not erase the receipt chain that made closure intelligible

---

## Example 2 — Suspended work with deferred settlement and future re-entry

### Situation
A daemon-carried task begins lawfully, performs partial bounded work, then suspends because an upstream dependency or review gate remains unresolved.

### Lawful reading
- The task was lawfully activated and entered enactment.
- Partial progress does not mean final closure.
- Settlement may classify the state as deferred without pretending the work was never enacted.

### Example flow
1. Activation authority emits `ALLOW` and records an activation receipt.
2. Lifecycle emits `CLAIM`, `READY`, and `ENTER`.
3. Runtime emits a partial-progress or suspend-capable receipt.
4. Lifecycle emits `SUSPEND` and `RETURN` with preserved continuity state.
5. Settlement reads the activation receipt, lifecycle chain, and partial-progress receipt.
6. Settlement records `SETTLEMENT_DEFERRED` with one explicit future re-entry path.
7. No final closure is claimed yet.
8. Later work may resume only through the explicit preserved-authority or fresh-activation path that actually applies.

### Boundary proved
- deferred settlement preserves lawful lineage without false closure
- future re-entry is a stated next posture, not an implied right to continue forever
- settlement does not revoke the fact that enactment already happened lawfully

---

## Example 3 — Failed enactment with escalated settlement

### Situation
An external/API run is activated lawfully and enters enactment, but a carrier-side or side-effect failure occurs after entry.

### Lawful reading
- Lawful entry is still lawful even if post-entry failure occurs.
- Runtime failure receipts do not retroactively decide whether activation should have been granted.
- Settlement may escalate review because the failure matters, but that is not the same as rewriting history.

### Example flow
1. Activation authority emits `ALLOW` with an activation receipt.
2. Lifecycle emits `CLAIM`, `READY`, and `ENTER` for the external/API executor.
3. Runtime or carrier emits a failure receipt after entry.
4. Lifecycle emits `FAIL` and `RETURN`.
5. Settlement reads the activation receipt, lifecycle chain, and failure receipt.
6. Settlement records `ESCALATE_REVIEW` with cited failure evidence.
7. Follow-up may require fresh activation, remediation, or carrier review depending on the fault class.

### Boundary proved
- failure after entry does not retroactively void lawful activation
- settlement may escalate without becoming a hidden second activation center
- runtime/carrier receipts witness failure but do not own enactment meaning

---

## Example 4 — Cross-carrier resumed completion with final settlement

### Situation
A task begins in a manual carrier, suspends with preserved continuity, later resumes under a daemon or external carrier, and finally closes.

### Lawful reading
- Receipt lineage must remain explicit across carrier change.
- The later carrier does not mint a new hidden center of authority.
- Final settlement closes the whole chain by citing prior and later witnesses together.

### Example flow
1. Manual enactment begins under one activation receipt and lifecycle chain.
2. The task later `SUSPEND`s and returns preserved continuity state.
3. Settlement may record `SETTLED_WITH_FUTURE_REENTRY` or equivalent deferred closure posture for the first leg.
4. A later carrier becomes eligible.
5. The repo validates whether preserved authority remains sufficient or whether fresh activation is required.
6. Resumed lifecycle entry occurs only under the lawful path that actually applies.
7. Later runtime receipts witness successful completion in the new carrier.
8. Final settlement cites the earlier activation/lifecycle witnesses, the re-entry path, and the later completion receipts.
9. The chain closes as durable history without pretending the later carrier was the original source of authority.

### Boundary proved
- receipt lineage survives carrier change
- settlement closes the chain without inventing new authority
- final closure may cite multiple legs without flattening them into one vague success event

---

## Compressed findings

### 1. Receipt lineage now has first-form boundary evidence
The review set can now show that activation receipts, lifecycle witnesses, runtime receipts, and settlement outcomes can coexist without collapsing into one ambiguous history object.

### 2. Settlement is now better constrained
Settlement may:
- accept,
- defer,
- escalate,
- and reopen future posture lawfully.

Settlement may **not**:
- pretend it granted enactment,
- silently void prior lawful activation,
- or hide future re-entry behind informal continuation.

### 3. The hardest remaining edge is install-path clarity
The examples make the candidate easier to trust conceptually.
What remains is showing exactly where this review-set would live if later thaw review allowed active installation.

## Resulting judgment
The activation/lifecycle set is stronger after receipt/settlement demonstration.
The remaining major blocker before thaw-readiness reassessment is:
- install-path mapping into active architecture
