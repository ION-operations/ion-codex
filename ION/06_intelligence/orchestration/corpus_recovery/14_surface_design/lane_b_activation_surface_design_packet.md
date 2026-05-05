# Pass 37 — Lane B activation surface-design packet

## Purpose

Translate the Lane B activation-authority delta into the next **proposal-space** design packet for future current-line restoration.

This packet does **not** ratify active law.
It defines the narrowest candidate protocol split that could eventually be reviewed through the frozen project control kernel and later revision/thaw paths.

## Control declaration

- Source lane: `corpus_recovery/13_controlled_reintegration/lane_b_activation_authority_delta_packet.md`
- Question class: activation/orchestration surface design
- Default posture: proposal-space only
- Output class: protocol-shape packet
- Landing boundary: design / atlas only
- Active-law mutation: forbidden in this pass

## Why this packet exists now

Lane B already established that the current branch does **not** yet carry a first-class activation-authority center, and that the missing center should not be faked by stretching scheduler, operator entry, allocator, or handoff surfaces past what they actually govern.

The next lawful move is therefore not a fourth reintegration delta.
It is a bounded design packet that states what the missing current-line activation surfaces would need to own.

## Governing split

The current line likely needs **two** future protocol surfaces:

1. `ACTIVATION_AUTHORITY_PROTOCOL.md`
2. `EXECUTOR_LIFECYCLE_PROTOCOL.md`

The split matters because each surface answers a different architectural question.

### 1. Activation authority
This is the constitutional surface for what activation authority **is**.
It should govern:
- activation jurisdiction,
- lawful relation to scheduler, allocator, operator entry, and continuation,
- activation request classes,
- approval / denial / escalation semantics,
- and the boundary between candidate work and executable enactment.

It should **not** become a scheduler document, role-theater manifesto, or fleet-runtime shell.

### 2. Executor lifecycle
This is the enactment surface for how an executor is lawfully claimed and used.
It should govern:
- executor claim and binding,
- readiness and entry,
- suspension and resume,
- release and retirement,
- failure and settlement relation,
- and lifecycle receipts under one-workflow law.

It should **not** redefine activation jurisdiction, future-work scheduling, or continuation ontology.

## Draft design judgment

The safest current-line restoration path is:

- keep `LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md` as future-work compilation law,
- keep `OPERATOR_ENTRY_SURFACE_PROTOCOL.md` as operator-facing invocation law,
- keep the M14-M16 activation/handoff chain as validated continuation-entry substrate,
- and introduce the two missing activation surfaces as a separate authority stack.

That produces a five-layer activation stack:

1. one-workflow doctrine and capability truth
2. activation authority
3. executor lifecycle and bounded enactment
4. continuation / takeover / handoff activation substrate
5. operator-entry and service-shell invocation surfaces

## Candidate canonical objects

### Activation authority objects
- `ActivationIntent`
- `ActivationRequest`
- `ActivationDecision`
- `ActivationDenial`
- `ActivationAuthorityBoundary`
- `ActivationReceipt`

### Executor lifecycle objects
- `ExecutorIdentity`
- `ExecutorCapabilityBinding`
- `ExecutorClaim`
- `ExecutorLifecycleState`
- `ExecutorLifecycleTransition`
- `ExecutorLifecycleReceipt`

## Ratification prerequisites

No active protocol should be drafted into `ION/02_architecture/` unless all of the following are true:

1. the two-surface split still survives operator review,
2. ownership boundaries are clear enough that scheduler, allocator, entry, and handoff law are not overloaded,
3. the future revision path is classified correctly under the frozen project control kernel,
4. the proposed surfaces remain compatible with one-workflow doctrine, manual/automation equivalence, and anti-theater safeguards,
5. and a worked example proves that activation can be described without inventing hidden autonomous fleet behavior.

## Non-lawful moves for this packet

Do **not** do any of the following in this pass:
- draft active `02_architecture/` activation protocols as if they were ratified,
- rewrite scheduler law into activation ontology,
- rewrite handoff/continuation surfaces into a full lifecycle center,
- or treat named swarm roles as proof of lawful current architecture.

## Follow-up artifacts

See:
- `lane_b_activation_surface_design_matrix.csv`
- `lane_b_activation_surface_design_outlines.md`

## Pass result

The repo now contains the second proposal-space design packet for the missing Lane B activation surfaces, while keeping active-law mutation out of scope.
