---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-09T16:45:00-04:00
status: ACTIVE
purpose: Define the L1 executor capability registry so carrier binding becomes explicit kernel law rather than hidden heuristic intuition
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md
  - ION/04_packages/kernel/executor_registry.py
  - ION/04_packages/kernel/scheduler.py
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_kernel_executor_registry.py
  - ION/tests/test_kernel_scheduler.py
  - ION/tests/test_kernel_operator_cli.py
---

# Executor Capability Registry Protocol

## Purpose

L1 makes executor and carrier choice explicit.

Before L1, the scheduler could project carrier posture, but carrier binding still depended mainly on bounded string heuristics from chassis or executor hints.

After L1, the active root has one explicit executor capability registry that the scheduler may consult before falling back to those heuristics.

## Short thesis

Carrier choice is part of lawful orchestration.

It should not live only in code intuition.

The executor capability registry exists so the kernel can say, explicitly:
- who an executor is,
- what carrier class it belongs to,
- what trust posture it has,
- whether it is currently available,
- what concurrency it can support,
- what kinds of scope it can lawfully carry,
- and whether it should be treated as primary or fallback only.

## Registry law

The registry is a kernel record family.

Each capability record must bind, at minimum:
- executor identity,
- carrier class,
- trust class,
- availability,
- max concurrency and active assignments,
- supported scope types,
- domain fitness,
- fallback suitability,
- and any side-effect constraints worth preserving.

Optional aliases may exist so current bounded executor hints can resolve into explicit capability records without inventing a second identity system.

## Selection law

When the scheduler chooses a carrier binding, it should:
1. inspect eligible capability records,
2. prefer records whose carrier matches the current preferred carrier posture,
3. prefer records whose identity or alias matches the current executor hint where one exists,
4. prefer records whose domain fitness matches the current scope or domain,
5. reject unavailable or saturated records,
6. and only then fall back to heuristic inference if no eligible record exists.

This makes carrier choice explicit without freezing the system into a brittle exact-match-only model.

## Fallback law

Heuristic carrier inference is still allowed as a degraded path.

But after L1 it must remain visibly degraded:
- heuristic fallback should be explicit in the schedule candidate,
- explicit in the scheduling receipt,
- and visible through operator status.

Hidden heuristic carrier law is no longer acceptable as the primary explanation for why a carrier was chosen.

## Receipt law

Scheduling receipts should now preserve not only the selected carrier but also:
- whether the binding came from the executor capability registry or heuristic fallback,
- which executor id was selected when present,
- which capability record justified that choice when present,
- and the capability basis explaining why that match was chosen.

Receipts remain witness, not authority.
They exist to make carrier binding traceable.

## Operator surface

The operator should be able to:
- register or replace executor capability records,
- inspect the current registry snapshot,
- view capability-aware schedule projections,
- and view scheduling receipts that preserve the binding source and selected executor/capability ids.

This keeps capability law visible at the same surface where schedule posture is already visible.

## Non-goals

L1 does not yet provide:
- full settlement law,
- perfect takeover normalization,
- manual and automation equivalence proof,
- or branch-aware reassignment policy.

L1 only establishes the first explicit capability floor the scheduler can stand on.

## Success condition

L1 is complete when:
- executor capability exists as a real persisted kernel record family,
- the scheduler prefers explicit eligible capability matches over heuristics,
- schedule projections and receipts preserve the capability basis for the chosen carrier,
- the operator can inspect and mutate the registry through the CLI,
- and the proof center demonstrates that carrier binding is now explicit rather than hidden.

## Activation/lifecycle boundary clarification

Capability sufficiency is a necessary input to activation authority and lifecycle integrity.
It is not, by itself, enactment authority.
A carrier or executor may look eligible in the registry and still require explicit activation allowance before work may cross into execution.
After that crossing, lifecycle law constrains how the chosen executor may claim, enter, suspend, resume, return, release, fail, or retire.
