---
type: scheduler_model
authority: A2_EXECUTOR
created: 2026-04-09T16:05:00-04:00
status: ACTIVE
purpose: Explain the lawful orchestration scheduler, progressive schedule compilation, and the current post-L4/M0 orchestration boundary
connections:
  - ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md
  - ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md
  - ION/02_architecture/HORIZON_STATE_AND_TIGHTENING_PROTOCOL.md
  - ION/04_packages/kernel/executor_registry.py
  - ION/04_packages/kernel/scheduler.py
  - ION/tests/test_kernel_executor_registry.py
  - ION/tests/test_kernel_scheduler.py
  - ION/06_intelligence/orchestration/2026-04-09_post_m0_state_forward_path_and_codex_handoff.md
---

# ION Scheduler and Orchestration Model

## Purpose

This document explains the scheduler as the orchestration intelligence of the kernel without confusing it for the kernel itself.

## Short thesis

ION does not need a normal scheduler.
It needs a lawful horizon-aware orchestration scheduler.

That scheduler must progressively compile future work rather than treating the future as either fixed queue or improvisation field.

## Progressive schedule compilation

The key idea is simple:
- future work exists before it is fixed,
- present execution changes what future work becomes,
- and schedule commitments should strengthen or relax as evidence changes.

This is why the schedule should be compiled progressively.

## Schedule dimensions

The scheduler reasons across at least two dimensions.

### Commitment posture

How fixed a candidate is becoming:
- speculative,
- emerging,
- likely,
- precommitted,
- committed,
- enacted,
- completed.

### Schedule state

What condition the candidate is currently in:
- ready,
- blocked,
- claimed,
- in flight,
- retry,
- stale,
- deferred,
- enacted but not landed,
- or future candidate.

These are not the same thing.
A candidate may be highly likely and still blocked.

## Scheduler inputs

The scheduler should reason over:
- current work units,
- horizon pressure,
- dependency satisfaction,
- review posture,
- operator intent,
- replay and recovery obligations,
- carrier availability,
- continuity cost of switching carriers,
- and explicit executor capability law.

## Scheduler outputs

The scheduler should produce:
- ranked next-step candidates,
- candidate posture,
- candidate-to-carrier proposals,
- refusal reasons where relevant,
- scheduling receipts,
- and operator-visible schedule projections.

It may recommend.
It must not silently bypass packet law.

## What L0 through L4 made explicit

L0 already landed:
- explicit schedule state classes,
- explicit commitment semantics,
- horizon-to-schedule projection,
- schedule receipts,
- minimal carrier-binding inference,
- operator CLI schedule snapshot and record surfaces,
- and workflow proof that enacted horizon pressure appears in schedule posture.

L1 now lands on top of that:
- explicit executor capability records,
- explicit registry-backed carrier binding,
- operator CLI capability snapshot and register surfaces,
- visible carrier-binding source on schedule candidates,
- and schedule receipts that preserve selected executor/capability ids.

L2 through L4 then made explicit:
- takeover normalization,
- manual/automation equivalence proof,
- and context-perfect continuation proof.

That is a real scheduler-to-continuation floor, not just architecture prose.

## What L0 through L4 intentionally did not claim

Even after L4, the root did not yet provide:
- bounded parallel claim law,
- settlement law,
- or branch-aware arbitration strong enough for wider multi-executor claims.

That is why M0 had to land before M1 rather than widening directly into allocator code.

## Why M0 was required

L0-L4 eliminated hidden scheduling and continuation intuition as the primary explanation for lawful next-step choice.

M0 now names:
- branch claim boundaries,
- fan-out law,
- settlement outcomes,
- merge and escalation boundaries,
- and future receipt families for later M1/M2 embodiment.

The next move is M4 branch-aware horizon / schedule synchronization (landed) on top of the now-real bounded branch fan-out / fan-in / control floor.

## Anti-patterns

Do not:
- reduce the scheduler to priority sorting,
- let it bypass packet law,
- create a separate schedule packet family,
- let heuristic fallback drift back into silent law,
- or widen into swarm claims before capability, continuation, and settlement law exist.

## One-line rule

The scheduler should make the future more legible and more lawful, not more magical.

## 2026-04-10 execution note

M2 settlement now gives the scheduler a lawful fan-in witness surface, but branch-budget / recursion / drift posture still remains later M-phase work.
