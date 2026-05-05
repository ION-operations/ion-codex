---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-04-09T21:15:00-04:00
status: ACTIVE
purpose: Define lawful bounded parallelism, branch claims, and settlement boundaries before later multi-executor implementation
connections:
  - ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md
  - ION/02_architecture/HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md
  - ION/02_architecture/CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md
  - ION/06_intelligence/orchestration/2026-04-08_ion_completion_phase_architecture.md
  - ION/06_intelligence/orchestration/2026-04-09_post_m0_state_forward_path_and_codex_handoff.md
---

# Bounded Parallelism and Settlement Protocol

## Principle

Parallel work is not a second workflow.

It is one lawful parent scope temporarily partitioned into bounded branches that must:
- preserve the same packet, review, and landing law,
- remain explicit about authority and scope,
- return proposals rather than truth,
- and rejoin the organism through explicit settlement rather than informal synthesis.

M0 exists so later multi-executor implementation does not invent its own law under pressure.

## Why M0 exists now

L0 through L4 already made these floors explicit:
- schedule posture,
- executor capability law,
- takeover sufficiency,
- bounded manual/automation symmetry,
- and context-perfect continuation bundles.

What remains missing before wider parallel implementation is not more continuation doctrine.
It is explicit settlement law.

Without that law, any allocator, swarm, or merge behavior would depend on hidden operator intuition.

## Branch claim law

No parallel branch may exist without an explicit claim boundary.

Each bounded branch must preserve, at minimum:
- one parent scope type and scope ref,
- one branch identifier,
- one bounded objective,
- one packet family or continuation carrier,
- one selected executor or executor class when known,
- one explicit write/read boundary,
- one expected return family,
- and one named settlement target.

No branch may silently widen the parent assignment.

Overlapping write claims must remain illegal by default unless the branch is explicitly comparative, review-only, or otherwise governed by later ratified law.

## Fan-out law

Fan-out is lawful only when:
- the parent scope is already explicit,
- branch partitions are explicit,
- the expected settlement mode is explicit,
- concurrency/budget posture is explicit,
- and each branch remains takeover-capable under the same continuity law.

Fan-out should be treated as a special scheduling and routing posture within kernel law.
It must not become a hidden alternate planner.

## Return law

Every bounded branch returns:
- a proposal,
- one explicit branch identity,
- one parent scope reference,
- and the evidence needed for settlement.

Parallel return does not imply direct landing.

The branch may complete its bounded work, but the organism is not settled until the parent scope performs one lawful settlement act.

## Settlement law

Settlement is the parent-scope act that determines how multiple bounded returns rejoin the canonical loop.

The minimum settlement outcomes are:
- `ACCEPTED_AS_IS`
- `MERGE_PROPOSAL_REQUIRED`
- `ESCALATE_REVIEW`
- `DEFERRED`
- `ABANDONED`

Settlement must remain explicit about:
- which branch returns were considered,
- which conflicts or non-conflicts were observed,
- whether a merge proposal is sufficient,
- whether human/review escalation is required,
- and what next packet or horizon pressure results.

## Receipt law

M0 defines the following future kernel witness families:
- `branch_claim_receipt`
- `branch_settlement_receipt`

These names are now canonical as law surfaces.
M0 does not require their code embodiment yet.

When later implemented, those receipts should preserve:
- parent scope,
- branch identities,
- selected executors or capabilities when known,
- settlement outcome,
- conflict notes,
- and the next continuity artifact emitted from settlement.

## Merge boundary law

Merge is not an automatic text splice.
It is one lawful settlement mode.

If multiple branch returns cannot be accepted independently, the organism must either:
- synthesize one explicit merge proposal,
- escalate to review,
- or defer until the conflict boundary is clearer.

No branch return may silently overwrite another branch return under the cover of "helpful synthesis."

## Scheduler and capability relation

Scheduler law and capability law remain upstream inputs to later parallel execution.

The scheduler may later propose:
- when fan-out is lawful,
- how many branches are lawful,
- and which executors are eligible.

Capability law constrains:
- who may claim a branch,
- what carriers are suitable,
- and what fallback posture remains lawful.

M0 does not replace scheduler law.
It constrains how later M1 and M2 work may embody it.

## Continuation relation

Every branch must preserve:
- takeover sufficiency,
- explicit required reads,
- and context-perfect continuation expectations when applicable.

Parallelism does not weaken continuity law.
It increases the need for explicit continuity discipline.

## Boundaries

M0 does not yet claim:
- an implemented allocator,
- implemented branch claim records,
- implemented settlement receipts,
- implemented merge engines,
- or swarm runtime behavior.

It is the definition pass that later M1 and M2 must obey.

## Success condition

M0 succeeds when the repository has one canonical settlement law that makes the next implementation order unambiguous:
- M1 may implement bounded multi-agent allocation,
- M2 may implement settlement and merge embodiment,
- and neither may invent new parallel process law ad hoc.

## Activation/lifecycle boundary clarification

Settlement records how bounded branches or enactment paths close, defer, escalate, merge, or abandon.
It must not rewrite whether activation was lawful when enactment crossed, nor whether lifecycle transitions were lawful while work was active.
Settlement therefore classifies closure truth after the fact; it is not a substitute authority center.

## Runtime/session clarification

Settlement may classify when a runtime path pauses, closes, escalates, or is
re-entered.
It does **not** create runtime session identity, own session-local queue law, or
replace API carrier-entry authority.
Those authority surfaces now remain explicitly governed by the emitted Lane C
runtime/session trio.
