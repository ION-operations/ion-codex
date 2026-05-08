---
type: kernel_runtime_model
authority: A2_EXECUTOR
created: 2026-04-09T16:05:00-04:00
status: ACTIVE
purpose: Explain the lawful substrate, runtime organs, and authority boundaries of the current ION kernel
connections:
  - ION/06_intelligence/orchestration/2026-04-09_ion_full_system_architecture_and_end_state_framework.md
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/SYSTEM_MAP.md
  - ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md
  - ION/02_architecture/MANUAL_AUTOMATION_FALLBACK_PROTOCOL.md
---

# ION Kernel Law and Runtime Model

## Purpose

This document explains the distinction between kernel law, scheduler law, runtime embodiment, and witness surfaces.

It is meant to keep builders from flattening the organism into whichever module family they touched most recently.

## Kernel law

The kernel is the lawful substrate.

It owns:
- continuity,
- authority,
- packet law,
- horizon law,
- enactment law,
- threshold and review law,
- recovery and replay law,
- and carrier constraints.

If a surface changes one of those laws, it is touching the kernel whether it admits it or not.

## Scheduler inside kernel law

The scheduler is not the kernel.
It is a subsystem inside kernel law.

Its job is to determine:
- what should run now,
- what remains provisional,
- what should tighten,
- which candidate is more committed than another,
- and which carrier or executor is the best current fit.

After L0 and L1, schedule state, commitment posture, projection, schedule receipts, and executor capability binding are explicit.
What remains incomplete is broader continuation normalization and settlement depth rather than a total absence of capability law.

## Runtime embodiment

The runtime is the live operational field where kernel law is enacted.

In the current root, that includes:
- operator entry through `python -m kernel ...`,
- supervised daemon-service surfaces,
- child-work issuance,
- recovery and replay,
- external execution bridge surfaces,
- sequential low-burn manual routing,
- schedule snapshot and record surfaces,
- capability snapshot and register surfaces,
- and status projection for horizon and schedule posture.

## Runtime organs by role

### Truth organs

These persist and query lawful state:
- `model.py`
- `store.py`
- `index.py`
- `graph.py`

### Context and packet organs

These compile bounded continuity and continuity artifacts:
- `context_compiler.py`
- `capsule_manager.py`
- `manifest_state.py`
- `packet_validation.py`
- `sequential_kernel.py`

### Execution and landing organs

These choose, validate, execute, and land bounded work:
- `scheduler.py`
- `executor_registry.py`
- `dispatch.py`
- `execution.py`
- `validation.py`
- `commit.py`
- `threshold.py`
- `governed_write.py`

### Runtime-carriage organs

These carry the same workflow more explicitly:
- `daemon.py`
- `daemon_loop.py`
- `daemon_service.py`
- `automation_policy.py`
- `operator_control.py`
- `recovery_replay.py`
- `external_execution_bridge.py`

## Authority versus witness

This distinction is non-optional.

Canonical authority lives primarily in:
- doctrine,
- protocol law,
- kernel truth,
- bounded canonical packets,
- and lawful operator/runtime surfaces that land back into kernel truth.

Witness surfaces remain subordinate:
- runtime reports,
- receipts,
- summaries,
- research notes,
- and projection files.

Receipts and reports matter, but they do not outrank the thing they witness.

## Carrier neutrality

Carrier changes must not create process changes.

Manual, IDE, daemon-assisted, external, and later bounded multi-executor carriage are all valid only if they:
- read bounded lawful inputs,
- perform one bounded step,
- return a proposal rather than hidden truth,
- and emit the next lawful continuity artifact.

That is why manual fallback is part of kernel legitimacy rather than a convenience patch.

## Current maturity

The kernel is already real enough to support:
- bounded operator entry,
- packet law,
- horizon state,
- enactment,
- enactment receipts,
- blind continuation and takeover proof,
- context-perfect continuation proof,
- explicit first-pass scheduler law,
- and explicit first-pass executor capability law.

What remains incomplete is not the existence of a kernel.
What remains incomplete is the embodiment of bounded branch allocation, settlement execution, and wider bounded parallel coordination beyond the now-explicit proof and law floor.

## Practical rule

If a builder cannot say whether a surface is kernel truth, scheduler law, runtime embodiment, or witness only, they should stop before editing it.
