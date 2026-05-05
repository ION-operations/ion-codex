---
type: protocol_review_draft
authority: A0_UNRATIFIED_REVIEW
created: 2026-04-14T01:55:00-04:00
status: REVIEW_ONLY
future_target: ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md
source_packets:
  - ION/06_intelligence/orchestration/corpus_recovery/13_controlled_reintegration/lane_b_activation_authority_delta_packet.md
  - ION/06_intelligence/orchestration/corpus_recovery/14_surface_design/lane_b_activation_surface_design_packet.md
review_layer: ION/06_intelligence/orchestration/corpus_recovery/15_quarantined_active_law_review/
---

# Activation Authority Protocol — Review Draft

## Short thesis

ION needs an explicit activation-authority center.

This center governs the lawful boundary between:
- candidate work that may be scheduled, prepared, or packetized,
- and work that is actually authorized to cross into executable enactment.

Activation authority is therefore neither the scheduler nor the executor lifecycle.
It is the decision center that lawfully turns a candidate enactment request into an allowed, denied, deferred, or escalated activation outcome.

## Why this surface exists

The current line already preserves strong law for:
- canonical workflow,
- packet and handoff standardization,
- operator entry,
- capability registry,
- continuation and takeover,
- and orchestration scheduling.

What it still lacks as a first-class explicit center is the surface that answers:

**When is work merely present in the organism, and when is it lawfully authorized to begin execution?**

This protocol exists to answer that question without overloading scheduler law, runtime shells, or continuation artifacts.

## Activation authority is not

Activation authority is **not**:
- future-work planning,
- queue management,
- runtime session ontology,
- executor claim/release state transition law,
- autonomous swarm mythology,
- or a convenience wrapper around operator intent.

Those surfaces may supply inputs to activation authority, but they do not replace it.

## Governing formulation

Activation authority is the kernel-governed decision surface that evaluates whether a candidate enactment may cross into executable work under one-workflow law.

That decision should produce one of four outcomes:
- `ALLOW`
- `DENY`
- `DEFER`
- `ESCALATE`

Every outcome should be explicit, reviewable, and receiptable.

## Core relation map

### Relation to scheduler law
The scheduler compiles and ranks future work.
Activation authority does not decide the whole future schedule.
It decides whether a concrete enactment candidate is lawful to activate now.

### Relation to operator entry
Operator entry is an invocation surface.
Activation authority is not replaced by the fact that an operator asked for something.
Operator request may be a strong input, but the organism still owes an activation judgment.

### Relation to capability registry
Capability truth constrains activation decisions.
A candidate without a lawful eligible carrier/executor should not silently activate through optimism.

### Relation to continuation/takeover
Continuation and takeover provide lawful substrate for preserving work across sessions or carriers.
They do not, by themselves, grant activation.
A continuation bundle may be activation-ready or not ready; activation authority judges that boundary.

### Relation to executor lifecycle
Executor lifecycle governs claim, readiness, suspension, resume, release, and failure transitions after or around activation.
That remains a separate protocol surface.
This protocol may reference lifecycle prerequisites, but it must not absorb their full state machine.

## Canonical objects

### ActivationIntent
A declared intention that a bounded work packet or lawful step may need executable enactment.

### ActivationRequest
The concrete request presented to activation authority for judgment.
At minimum it should identify:
- work identity,
- packet or enactment target,
- requested carrier/executor class,
- capability requirements,
- scope and side-effect posture,
- prerequisite status,
- and continuity/handoff context if present.

### ActivationDecision
The formal decision object emitted by activation authority.
At minimum it should include:
- decision class,
- decision reason,
- approving or denying boundary,
- chosen or refused carrier/executor posture,
- any prerequisites still missing,
- and receipt reference.

### ActivationDenial
A structured denial object for cases where activation must not proceed.
Denial should be specific enough to support replay, repair, or escalation.

### ActivationReceipt
A witness artifact proving that activation judgment occurred and what its result was.

## Decision classes

### `ALLOW`
Use when:
- the candidate packet is enactment-ready,
- scope is lawful,
- required prerequisites are satisfied,
- an eligible carrier/executor exists,
- and activation would not violate continuity, settlement, or side-effect boundaries.

### `DENY`
Use when activation is currently unlawful.
Examples:
- missing capability fit,
- unresolved side-effect risk,
- absent required packet structure,
- broken continuity assumptions,
- or explicit law conflict.

### `DEFER`
Use when activation may become lawful later but should not cross now.
Examples:
- future-horizon candidate not yet packet-ready,
- blocked dependency,
- waiting on review,
- or awaiting a lower-cost carrier window.

### `ESCALATE`
Use when the activation question cannot be settled locally without a higher review or operator decision.
Examples:
- competing lawful interpretations,
- conflict between urgency and safety boundary,
- ambiguous carrier equivalence,
- or unresolved authority overlap.

## Minimum activation checks

A candidate activation should be judged against at least:
- packet readiness,
- scope/boundary fit,
- capability fit,
- side-effect posture,
- dependency satisfaction,
- continuity integrity,
- settlement obligations,
- operator constraint compatibility,
- and review/threshold pressure.

Failure on any critical check should not be hidden behind convenience or momentum.

## Carrier neutrality rule

Manual execution, IDE execution, daemon/service execution, API execution, and later bounded multi-carrier execution must all pass through the same activation law.

Different carriers may change:
- latency,
- convenience,
- observability,
- or continuity cost.

They must **not** change whether the work needs lawful activation judgment.

## Anti-theater rule

Activation authority must not be written as if ION already contains an unconstrained autonomous fleet or role mythology.

Activation may select among lawful bounded carriers or executors.
It may not invent self-justifying hierarchy, theatrical orchestration roles, or hidden agency beyond the workflow actually preserved.

## Denial classes

Candidate denial families include:
- `CAPABILITY_MISMATCH`
- `PACKET_NOT_READY`
- `SIDE_EFFECT_BOUNDARY_UNRESOLVED`
- `DEPENDENCY_UNSATISFIED`
- `CONTINUITY_INTEGRITY_FAILURE`
- `SETTLEMENT_BLOCK`
- `AUTHORITY_CONFLICT`
- `OPERATOR_CONSTRAINT_CONFLICT`

These are not necessarily final canon, but the denial surface should remain explicit rather than free-form.

## Activation boundary law

The activation boundary is crossed only when:
1. a bounded work candidate exists,
2. its enactment request is explicit,
3. activation authority produces a non-implicit decision,
4. any required prerequisites are satisfied or explicitly waived by lawful higher review,
5. and the decision is receipted or otherwise reviewable.

Without these conditions, the organism may be preparing, scheduling, or discussing work, but it is not yet lawfully activating it.

## What this protocol leaves open on purpose

This review draft does **not** fully define:
- executor claim/readiness/release transitions,
- runtime session queue semantics,
- daemon/API shell behavior,
- detailed receipt schemas,
- or final implementation object names.

Those belong partly to future lifecycle, runtime, and implementation surfaces.

## Minimal worked example

A packetized continuity repair task is ranked highly by the scheduler and an operator requests immediate execution.

Activation authority should still ask:
- is the packet enactment-ready,
- is the chosen carrier eligible,
- are side effects bounded,
- is continuity intact,
- and is settlement pressure acceptable?

Only after that judgment may the task cross into executable enactment.
Operator urgency alone is not activation law.
Scheduler ranking alone is not activation law.
A preserved continuation bundle alone is not activation law.

## Review boundary

This document is a review draft only.
It is not active law until explicitly approved and installed into `ION/02_architecture/` through the frozen control-kernel revision path.
