---
type: workflow_lifecycle
authority: A2_EXECUTOR
created: 2026-04-09T16:05:00-04:00
status: ACTIVE
purpose: Explain the end-to-end continuity lifecycle of one lawful ION step and how the loop resumes across time and carriers
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/02_architecture/HORIZON_TO_EXECUTION_WORKFLOW_REHEARSAL_PROTOCOL.md
  - ION/06_intelligence/orchestration/2026-04-09_post_l0_state_forward_path_and_codex_handoff.md
---

# ION Workflow and Continuity Lifecycle

## Purpose

This document explains how one lawful ION step moves from entry to continuation.

It is the practical lifecycle view of the canonical workflow.

## The lifecycle in one pass

### 1. Enter the current state

The executor reads the current bounded truth:
- doctrine,
- governing task or handoff,
- scope state,
- current operator posture,
- and relevant packets or receipts.

The goal is not to reconstruct the whole system.
The goal is to enter the current lawful window.

### 2. Compile bounded context

The executor or runtime compiles the minimum lawful context for the next step:
- target scope,
- allowed writes,
- exact requested action,
- dependencies,
- unresolved questions,
- and expected output family.

If the context is not bounded, the step is not ready.

### 3. Determine the next lawful route

The system decides what kind of step this is:
- direct execution,
- review,
- handoff,
- manual fallback,
- child-work issuance,
- horizon tightening,
- enactment,
- or schedule projection.

This is where workflow law matters more than convenience.

### 4. Choose the carrier

The same lawful step may be carried by:
- the current executor,
- the supervised runtime,
- an external worker,
- or later another bounded executor.

The chosen carrier must not change the workflow.

### 5. Execute one bounded step

The step must remain bounded enough that:
- the output is legible,
- the result can be reviewed,
- and a fresh executor can continue from the emitted artifacts.

Hidden multi-step jumps are disallowed because they destroy lawful continuation.

### 6. Return a proposal, not hidden truth

Execution returns one or more bounded outputs such as:
- packet,
- role session,
- handoff,
- receipt,
- commit delta,
- signal,
- or review artifact.

The result is not automatically truth just because it was produced.

### 7. Land, hold, or escalate

The system must decide whether to:
- land the result into kernel truth,
- hold it for later,
- or escalate for review.

This is where threshold, validation, and governed write matter.

### 8. Emit the next continuity surface

Every completed step should leave behind enough lawful evidence for continuation:
- what happened,
- what remains,
- what must be read next,
- what risk remains unresolved,
- and what the next executor is expected to do.

### 9. Resume after interruption

If the process is interrupted, recovery and replay must re-enter the same loop rather than inventing a different rescue workflow.

## What continuity means here

Continuity does not mean infinite context.

It means that the next lawful step can be continued from bounded artifacts with:
- enough truth,
- enough scope,
- enough traceability,
- and enough explicit next-step structure.

## Why this lifecycle matters

Without this lifecycle, the system collapses into:
- hidden memory dependence,
- ad hoc routing,
- non-repeatable handoff,
- and features that only work when the original operator is still present.

With this lifecycle, intelligence becomes governable across time and carriers.

## What is already proven

The current proof center already shows:
- horizon state can persist,
- the next lawful packet can be tightened and enacted,
- receipts can witness the transition,
- operator surfaces can rediscover that state,
- and a fresh executor can continue from canonical packet artifacts.

## Remaining proof work

The next lifecycle gaps are:
- principled executor capability law,
- stronger handoff normalization beyond the current bounded proof,
- manual and automation equivalence proof,
- and context-perfect continuation under stricter read limits.

## Practical operating question

For any proposed change, ask:

Can a fresh capable executor continue the next lawful step from the emitted artifacts alone?

If the answer is no, the lifecycle is being weakened.
