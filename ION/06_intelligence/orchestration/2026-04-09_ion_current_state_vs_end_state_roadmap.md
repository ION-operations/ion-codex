---
type: roadmap
authority: A3_OPERATIONAL
created: 2026-04-09T16:05:00-04:00
status: SUPERSEDED
superseded_by:
  - ION/06_intelligence/orchestration/2026-04-12_current_generation_ratification_record.md
  - ION/06_intelligence/orchestration/2026-04-12_ion_acceptance_evidence_bundle_current_state.md
purpose: Compare what is currently real in the canonical root against the intended mature end-state and preserve the correct next execution order
connections:
  - ION/MASTER_ORCHESTRATION_INDEX.md
  - ION/06_intelligence/orchestration/2026-04-09_post_m0_state_forward_path_and_codex_handoff.md
  - ION/06_intelligence/orchestration/2026-04-09_ion_full_system_architecture_and_end_state_framework.md
  - ION/tests/test_kernel_continuation.py
  - ION/tests/test_kernel_manual_automation_equivalence.py
  - ION/tests/test_kernel_takeover.py
  - ION/tests/test_kernel_executor_registry.py
  - ION/tests/test_kernel_workflow_rehearsal.py
  - ION/tests/test_kernel_scheduler.py
---

# ION Current State vs End-State Roadmap

## Supersession note (2026-04-12)

This remains useful as a dated roadmap witness for the L4/M0 era and the
intermediate M-phase reasoning that followed, but it is no longer the active
current-state record for the branch.

Current live-state truth now lives in:
- `ION/06_intelligence/orchestration/2026-04-12_current_generation_ratification_record.md`
- `ION/06_intelligence/orchestration/2026-04-12_ion_acceptance_evidence_bundle_current_state.md`
- `ION/06_intelligence/orchestration/2026-04-12_post_phase1_template_governance_state_forward_path_and_codex_handoff.md`
- `ION/06_intelligence/orchestration/2026-04-11_post_m17_state_forward_path_and_codex_handoff.md`

References below to `292 passed`, manual `PYTHONPATH`, or M17 as the next
implementation center are preserved as point-in-time witness only.

## Purpose

This document tells the truth about where the repository stands relative to the larger end-state.

It exists to prevent two common failures:
- underestimating how much is already real,
- and over-claiming maturity where proof is still thin.

## Current verified state

As of 2026-04-09, the canonical working root has:
- K1 operator entry,
- K2 packet and handoff normalization,
- K3 horizon state and tightening,
- K4 horizon packet enactment,
- K5 enactment receipts,
- K6 horizon-to-execution workflow rehearsal,
- K7 blind continuation and takeover rehearsal,
- L0 lawful orchestration scheduler definition,
- L1 executor capability registry,
- L2 handoff/takeover normalization,
- L3 manual/automation equivalence proof,
- and L4 context-perfect continuation proof.

In explicit doctrine/orchestration law, the canonical root now also has:
- M0 bounded parallelism and settlement law definition.

Current proof floor includes:
- bounded packet continuity,
- bounded fresh-executor takeover,
- horizon state and enactment traceability,
- operator visibility of horizon and schedule posture,
- explicit schedule receipts,
- explicit executor capability binding with registry-visible fallback,
- explicit takeover-assessment receipts plus operator takeover surfaces,
- explicit manual/automation equivalence receipts plus operator equivalence surfaces,
- and explicit continuation bundles plus continuation-proof receipts.

Most recent verified suite result:
- `292 passed, 3 subtests passed`

Packaging caveat:
- local execution still depends on `PYTHONPATH=04_packages`

## What the mature end-state should include

The intended mature system should support:
- one lawful workflow across all carriers,
- principled executor capability law,
- stronger takeover sufficiency,
- manual and automation equivalence proof,
- context-perfect continuation,
- branch-aware and settlement-aware orchestration,
- bounded multi-executor coordination,
- durable receipts across major orchestration transitions,
- and outsider-grade operational packaging.

## What is already materially real

The repository already has:
- a real kernel,
- real operator entry,
- real packet law,
- real horizon state,
- real enactment and enactment receipts,
- real workflow rehearsal,
- real takeover proof,
- real first-pass scheduler law,
- and real first-pass executor capability law.

This project is not searching for its center anymore.
It is proving and deepening a center that already exists.

## What is still missing

The biggest remaining gaps are:
- M1 bounded multi-agent allocator, now embodied in kernel/operator surfaces,
- M2 settlement and merge embodiment,
- later bounded multi-executor orchestration,
- and stronger packaging and evaluation maturity.

## Correct next implementation order

1. M17 handoff-capsule executor-start packet materialization
2. M3 budget, anti-recursion, and anti-drift controls
3. Only then wider M-phase parallelism and settlement-heavy orchestration

## Parallel explanatory work

The articulation suite may continue growing in parallel.

That work is valuable because the repository is now large enough that explanation is part of implementation.
But explanatory work must not replace the actual execution order above.

## What should not be done early

Do not:
- widen into swarm behavior first,
- harden hidden carrier heuristics into law,
- confuse receipts with canonical truth,
- create a parallel scheduling religion,
- or let product vision outrun proof.

## End-state standard

ION should be considered mature only when a capable executor can:
- enter from canonical artifacts,
- understand the lawful next step,
- carry one bounded step through any approved carrier,
- hand off without hidden context,
- and do so while the system retains future structure honestly and traceably.

That is the finish line.

## 2026-04-10 update

M2 bounded fan-in / merge / review settlement is now embodied. The next bounded gap is M3 branch budget / recursion / drift control.
