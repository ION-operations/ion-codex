---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-14T13:20:00-04:00
status: ACTIVE
purpose: Define the activation-authority center that governs whether bounded work may cross into executable enactment under one-workflow law
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md
  - ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/02_architecture/HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md
  - ION/02_architecture/CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_LIFECYCLE_PROTOCOL.md
  - ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md
  - ION/06_intelligence/orchestration/corpus_recovery/22_thaw_closure_review/activation_lifecycle_joint_thaw_closure_judgment.md
---

# Activation Authority Protocol

## Short thesis

ION needs an explicit activation-authority center.

This center governs the lawful boundary between:
- candidate work that may be scheduled, prepared, or packetized,
- and work that is actually authorized to cross into executable enactment.

Activation authority is therefore neither the scheduler nor the executor lifecycle.
It is the decision center that turns a candidate enactment request into an explicit `ALLOW`, `DENY`, `DEFER`, or `ESCALATE` outcome under one-workflow law.

## Why this surface exists

The current line already preserved strong law for:
- canonical workflow,
- packet and handoff standardization,
- operator entry,
- capability registry,
- continuation and takeover,
- and orchestration scheduling.

What it lacked as a first-class active center was the surface that answers:

**When is work merely present in the organism, and when is it lawfully authorized to begin execution?**

This protocol exists so that answer no longer has to be inferred from scheduler posture, carrier convenience, or continuation artifacts.

## Activation authority is not

Activation authority is **not**:
- future-work planning,
- queue management,
- runtime session ontology,
- executor lifecycle transition law,
- autonomous swarm mythology,
- or a convenience wrapper around operator intent.

Those surfaces may supply inputs to activation authority, but they do not replace it.

## Governing formulation

Activation authority is the kernel-governed decision surface that evaluates whether a candidate enactment may cross into executable work under one-workflow law.

Every activation judgment should produce one of four explicit outcomes:
- `ALLOW`
- `DENY`
- `DEFER`
- `ESCALATE`

Every outcome should be explicit, reviewable, and receiptable.

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
- and continuity or handoff context if present.

### ActivationDecision
The formal decision emitted by activation authority.
At minimum it should include:
- decision class,
- decision reason,
- governing boundary,
- chosen or refused carrier posture,
- any prerequisites still missing,
- and receipt reference.

### ActivationDenial
A structured denial object for cases where activation must not proceed.
Denial should remain specific enough to support replay, repair, or escalation.

### ActivationReceipt
A witness artifact proving that activation judgment occurred and what its result was.

## Decision classes

### `ALLOW`
Use when the candidate packet is enactment-ready, required prerequisites are satisfied, an eligible carrier or executor exists, and enactment would not violate continuity, settlement, or side-effect boundaries.

### `DENY`
Use when activation is currently unlawful.
Typical denial families include:
- `CAPABILITY_MISMATCH`
- `PACKET_NOT_READY`
- `SIDE_EFFECT_BOUNDARY_UNRESOLVED`
- `DEPENDENCY_UNSATISFIED`
- `CONTINUITY_INTEGRITY_FAILURE`
- `SETTLEMENT_BLOCK`
- `AUTHORITY_CONFLICT`
- `OPERATOR_CONSTRAINT_CONFLICT`

### `DEFER`
Use when activation may become lawful later but should not cross now.

### `ESCALATE`
Use when the activation question cannot be settled locally without higher review or explicit operator decision.

## Minimum activation checks

A candidate activation should be judged against at least:
- packet readiness,
- scope and boundary fit,
- capability fit,
- side-effect posture,
- dependency satisfaction,
- continuity integrity,
- settlement obligations,
- operator constraint compatibility,
- and review or threshold pressure.

Failure on any critical check should not be hidden behind convenience or momentum.

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
A candidate without a lawful eligible carrier or executor should not silently activate through optimism.
Capability sufficiency is a necessary input, not enactment authority by itself.

### Relation to packet and handoff law
Packet legality and handoff normalization may establish that a work object is bounded and continuation-safe.
They do not, by themselves, authorize enactment crossing.

### Relation to continuation and takeover
Continuation and takeover provide lawful substrate for preserving work across sessions or carriers.
They do not grant activation.
A continuation bundle may be activation-ready or not ready; activation authority judges that boundary.

### Relation to executor lifecycle
Executor lifecycle governs claim, readiness, entry, suspension, resume, return, release, failure, and retirement after or around activation.
This protocol may cite lifecycle prerequisites, but it must not absorb their full state machine.

### Relation to settlement law
Settlement classifies closure, deferment, escalation, or re-entry outcomes after enactment pressure has existed.
Settlement may not rewrite whether prior activation was lawful in the first place.

## Carrier neutrality rule

Manual execution, IDE execution, daemon or service execution, API execution, and later bounded multi-carrier execution must all pass through the same activation law.

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

## Activation boundary law

The activation boundary is crossed only when:
1. a bounded work candidate exists,
2. its enactment request is explicit,
3. activation authority produces a non-implicit decision,
4. any required prerequisites are satisfied or explicitly waived by lawful higher review,
5. and the decision is receipted or otherwise reviewable.

Without these conditions, the organism may be preparing, scheduling, or discussing work, but it is not yet lawfully activating it.

## What this protocol leaves open on purpose

This protocol does not define:
- the executor lifecycle state machine,
- runtime session ontology,
- queue compilation semantics,
- or broader activation receipt implementation details in code.

Those remain adjacent or later surfaces.

## Runtime/session boundary clarification

Queue readiness, dispatch nomination, or API carrier attachment may prepare a
runtime path, but none of them silently authorize enactment crossing.
A queue item marked `DISPATCH_READY` or an attached API carrier still owes an
explicit activation judgment before broader executable work may begin.

## Active emission note

This file was emitted into active architecture only after the coupled activation/lifecycle review chain completed bounded thaw review and thaw closure as one set. Review-space drafts, counterexamples, worked examples, install-path mapping, and thaw records remain preserved in the corpus recovery layers as support evidence rather than as active-law replacements.
