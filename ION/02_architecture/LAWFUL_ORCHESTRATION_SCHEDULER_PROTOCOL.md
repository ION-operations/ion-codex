---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-09T10:15:00-04:00
status: ACTIVE
purpose: Define the lawful orchestration scheduler as a kernel subsystem that progressively compiles future work under continuity law
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md
  - ION/02_architecture/HORIZON_STATE_AND_TIGHTENING_PROTOCOL.md
  - ION/02_architecture/HORIZON_PACKET_ENACTMENT_PROTOCOL.md
  - ION/02_architecture/HORIZON_ENACTMENT_RECEIPT_PROTOCOL.md
  - ION/02_architecture/HORIZON_TO_EXECUTION_WORKFLOW_REHEARSAL_PROTOCOL.md
  - ION/06_intelligence/orchestration/2026-04-09_post_l1_state_forward_path_and_codex_handoff.md
  - ION/04_packages/kernel/scheduler.py
  - ION/04_packages/kernel/executor_registry.py
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_kernel_executor_registry.py
  - ION/tests/test_kernel_scheduler.py
  - ION/tests/test_kernel_operator_cli.py
---

# Lawful Orchestration Scheduler Protocol

## Short thesis

ION needs an explicit orchestration scheduler, but this scheduler is not the kernel itself.

The kernel remains the total lawful substrate. It owns:
- authority,
- continuity,
- packet law,
- horizon law,
- enactment law,
- review and threshold law,
- recovery and replay law,
- and carrier constraints.

The scheduler is a kernel subsystem. It decides, inside that law:
- what should run now,
- what should wait,
- what should remain provisional,
- what becomes more fixed,
- which executor or carrier should carry it,
- and how future schedule structure changes as present work compiles.

The scheduler is therefore not a queue and not a second planner. It is the lawful orchestration intelligence of the organism.

## Governing formulation

The future schedule is neither fully precomputed nor fully improvised.

Instead, ION should treat future work as a living compiled artifact. Present execution, review outcomes, child returns, operator decisions, and executor conditions continuously tighten or relax future commitments.

The correct phrase for this is:

**progressive schedule compilation**

## Horizon structure

The scheduler should preserve different degrees of rigidity across time horizons.

### Immediate window
Mostly frozen.

Use this layer for:
- the next one or few lawful steps,
- packet-ready actions,
- explicit carrier choice,
- explicit required reads,
- explicit fallback.

This layer should only change for strong reasons:
- blocker,
- refusal,
- higher-priority lawful interruption,
- carrier loss,
- explicit operator override,
- stronger review finding.

### Near horizon
Structured but revisable.

Use this layer for:
- likely next branches,
- contingent continuation paths,
- prerequisites that would tighten a candidate,
- ranked alternative next steps,
- branch-specific readiness signals.

### Far horizon
Weakly frozen possibility field.

Use this layer for:
- later orchestration chains,
- emerging strategic direction,
- long-form future pressure,
- deferred but meaningful possibilities,
- branch structures that are not ready to collapse.

Far horizon is not vagueness. It is disciplined non-premature fixation.

## Commitment gradient

The scheduler should not think in binary terms such as “scheduled” versus “not scheduled”.

Each future work item should carry a commitment gradient such as:
- `SPECULATIVE`
- `EMERGING`
- `LIKELY`
- `PRECOMMITTED`
- `COMMITTED`
- `ENACTED`
- `COMPLETED`

This allows the organism to acknowledge future pressure honestly without pretending every candidate is ready for enactment.

## Scheduler state model

The scheduler should eventually maintain explicit state classes for:
- `READY`
- `BLOCKED`
- `CLAIMED`
- `IN_FLIGHT`
- `RETRY`
- `STALE`
- `DEFERRED`
- `ENACTED_UNLANDED`
- `FUTURE_CANDIDATE`

These states are separate from commitment gradient. A work item may be highly likely yet still blocked, or fully enacted yet not landed.

## Scheduler inputs

Scheduler decisions should draw from:
- horizon records,
- current scope/manifests,
- packet readiness,
- dependency satisfaction,
- review and threshold posture,
- operator intent,
- replay/recovery obligations,
- executor capability and availability,
- stale work / retry history,
- continuity cost of a carrier switch,
- and branch settlement requirements.

## Scheduler outputs

The scheduler should eventually produce:
- ranked next-step candidates,
- candidate-to-carrier bindings,
- refusal reasons,
- tightened horizon updates,
- enactment recommendations,
- scheduling receipts,
- and takeover-ready continuity bundles.

The scheduler may recommend, but it must not silently bypass canonical packet law.

## Carrier neutrality

The scheduler must not treat a different carrier as a different process.

Manual, IDE, supervised runtime, external/API, and later bounded swarm carriers must all carry the same lawful step types. Carrier change may alter convenience, latency, or execution cost, but it must not alter workflow law.

## Executor capability model

The scheduler cannot become principled until the repo has an explicit executor capability registry.

That registry should describe, at minimum:
- executor identity,
- carrier class,
- trust class,
- supported packet families,
- scope/domain fitness,
- concurrency limits,
- availability,
- fallback suitability,
- and side-effect constraints.

This registry belongs after blind-takeover proof, not before it.

L1 now makes that registry real as a first-pass kernel record family plus operator surface.
Current carrier binding may therefore prefer explicit eligible capability matches over heuristics while still exposing heuristic fallback visibly when no eligible registry match exists.

## Arbitration policy surface

The scheduler will eventually need an explicit ranking/arbitration layer that balances:
- urgency,
- dependency satisfaction,
- review pressure,
- horizon pressure,
- executor fit,
- continuity cost,
- operator intent,
- fairness / starvation control,
- and retry/recovery obligations.

That ranking policy is part of law. It should not live only in code intuition.

## Branch-sensitive orchestration

The scheduler is not a linear queue. It must be able to represent:
- a current path,
- a near set of conditional continuations,
- and a far structured possibility field.

Later work may re-shape earlier assumptions when:
- returns are surprising,
- review escalates,
- a carrier fails,
- multiple child branches require settlement,
- or operator priorities change.

## Receipts and traceability

Every meaningful schedule transition should eventually be traceable.

This includes:
- tightening receipts,
- enactment receipts,
- carrier-binding receipts,
- reassignment receipts,
- and merge/settlement receipts.

Receipts must remain subordinate to kernel truth. They exist to make continuity legible, not to create a competing authority surface.

## Non-goals

The scheduler must not become:
- a hidden autonomous planner,
- an excuse for vague future claims,
- a parallel packet family,
- or a shadow authority system.

The scheduler serves the canonical loop. It does not replace it.

## Integration posture

Current K-phase work already provides early scheduler organs:
- horizon state,
- tightening,
- enactment,
- enactment receipts,
- operator status projection,
- and workflow rehearsal.

Current L-phase work now makes the scheduler materially more explicit in two steps:
- L0: schedule state, commitment posture, projection, and schedule receipts
- L1: executor capability registry, registry-aware carrier binding, operator capability surfaces, and carrier-binding witness in schedule receipts

The next architectural move is therefore L2 takeover normalization and then the remaining equivalence, arbitration, and branch semantics without breaking the one-loop law.

## Activation-boundary clarification

The scheduler may compile, rank, tighten, and project enactment candidates.
It does **not** itself authorize enactment crossing.
A projected or even committed candidate still owes an explicit activation judgment under `ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md` before executable work may begin.

## Runtime/session clarification

The scheduler may nominate work that later enters a runtime session.
It does **not** create runtime session identity, own session-local queues, or
legalize API carrier attachment.
Those surfaces now remain explicitly governed by the emitted Lane C trio rather
than by scheduler posture.
