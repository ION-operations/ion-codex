# Pass 36 — Lane C runtime/session surface-design packet

## Purpose

Translate the Lane C runtime/session/API delta into the first **proposal-space** design packet for future current-line restoration.

This packet does **not** ratify active law.
It defines the narrowest candidate protocol split that could eventually be reviewed through the frozen project control kernel and later revision/thaw paths.

## Control declaration

- Source lane: `corpus_recovery/13_controlled_reintegration/lane_c_runtime_session_api_delta_packet.md`
- Question class: runtime/session/API surface design
- Default posture: proposal-space only
- Output class: protocol-shape packet
- Landing boundary: design / atlas only
- Active-law mutation: forbidden in this pass

## Why this packet exists now

Lane C already established that the current branch does **not** yet carry a first-class runtime/session/API center, and that the missing center should not be faked by stretching scheduler, runtime-state witness surfaces, or daemon-service wrappers.

The next lawful move is therefore not a fourth recovery widening pass.
It is a bounded design packet that states what the missing current-line surfaces would need to own.

## Governing split

The current line likely needs **three** future protocol surfaces:

1. `RUNTIME_SESSION_AUTHORITY_PROTOCOL.md`
2. `SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md`
3. `API_RUNTIME_ENTRY_PROTOCOL.md`

The split matters because each surface answers a different architectural question.

### 1. Runtime session authority
This is the constitutional surface for what a runtime session **is**.
It should govern:
- session identity,
- persistence boundary,
- session lifecycle posture,
- relation to kernel truth,
- relation to continuation/handoff,
- and relation to carrier/service shells.

It should **not** become a queue algorithm document, scheduler document, or web entry wrapper.

### 2. Session queue and dispatch
This is the operational surface for how session-bound work moves.
It should govern:
- session-local queue admission,
- runnable vs blocked classification,
- dispatch attempts,
- retries and cancellation,
- settlement / return semantics,
- and lawful relation to scheduler and execution receipts.

It should **not** redefine session identity or external API law.

### 3. API runtime entry
This is the boundary surface for how outside callers interact with runtime sessions.
It should govern:
- creation / inspect / enqueue / drive / cancel requests,
- request validation and operator control gates,
- service-shell translation rules,
- receipt surfaces,
- and the law that prevents kernel truth from collapsing into transport-layer fiction.

It should **not** redefine core session ontology or queue-state semantics.

## Draft design judgment

The safest current-line restoration path is:

- keep `RUNTIME_STATE_BINDING_PROTOCOL.md`, `RUNTIME_STATE_QUERY_PROTOCOL.md`, and `RUNTIME_STATE_REPORTING_PROTOCOL.md` as witness/query/reporting law,
- keep `SUPERVISED_DAEMON_SERVICE_PROTOCOL.md` as bounded service-shell law,
- and introduce the three missing runtime/session surfaces as a separate authority stack.

That produces a five-layer runtime stack:

1. kernel truth and continuation substrate
2. runtime session authority
3. session queue / dispatch lifecycle
4. runtime-state witness / query / reporting
5. supervised service / API entry shells

## Candidate canonical objects

### Runtime session authority objects
- `RuntimeSession`
- `RuntimeSessionIdentity`
- `RuntimeSessionScope`
- `RuntimeSessionCarrierBinding`
- `RuntimeSessionPosture`
- `RuntimeSessionTruthBoundary`

### Session queue / dispatch objects
- `SessionQueueItem`
- `SessionQueueAdmissionDecision`
- `SessionQueueState`
- `SessionDispatchAttempt`
- `SessionDispatchOutcome`
- `SessionSettlementReceipt`

### API runtime entry objects
- `RuntimeEntryRequest`
- `RuntimeEntryValidationResult`
- `RuntimeEntryReceipt`
- `RuntimeEntryClientBinding`
- `RuntimeEntryServicePosture`

## Ratification prerequisites

No active protocol should be drafted into `ION/02_architecture/` unless all of the following are true:

1. the three-surface split still survives operator review,
2. ownership boundaries are clear enough that scheduler, runtime-state, and service-shell law are not overloaded,
3. the future revision path is classified correctly under the frozen project control kernel,
4. the proposed surfaces remain compatible with one-workflow doctrine and current anti-autonomy law,
5. and a worked example proves that a runtime session can be described without silently inventing background autonomy.

## Non-lawful moves for this packet

Do **not** do any of the following in this pass:
- draft active `02_architecture/` protocol files as if they were ratified,
- rewrite `SUPERVISED_DAEMON_SERVICE_PROTOCOL.md` into a runtime ontology surface,
- rewrite `RUNTIME_STATE_*` surfaces into session-authority surfaces,
- or claim that API/client convenience determines runtime truth.

## Follow-up artifacts

See:
- `lane_c_runtime_session_surface_design_matrix.csv`
- `lane_c_runtime_session_surface_design_outlines.md`

## Pass result

The repo now contains the first proposal-space design packet for the missing Lane C runtime/session surfaces, while keeping active-law mutation out of scope.
