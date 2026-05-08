---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-04-09T23:55:00-04:00
status: ACTIVE
purpose: Define the M2 lawful fan-in / merge / review settlement embodiment on top of bounded branch allocation
connections:
  - ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md
  - ION/02_architecture/BOUNDED_MULTI_AGENT_ALLOCATOR_PROTOCOL.md
  - ION/06_intelligence/orchestration/2026-04-09_post_m2_state_forward_path_and_codex_handoff.md
---

# Fan-In / Merge / Review Settlement Protocol

## Principle

M2 does not permit silent rejoining of child branches.

When multiple bounded child returns come back under one parent scope, the parent must perform one explicit settlement act that says what happened, why, and what continuity artifact follows.

## What M2 embodies

M2 makes the following real:

- one bounded settlement projection over active branch claims,
- one explicit settlement outcome family,
- one explicit merge-proposal contract when conflict exists,
- one parent-scope settlement receipt,
- release of active branch claims once settlement is final,
- operator-facing settlement visibility through the canonical CLI/status surfaces.

## Minimum settlement outcomes

The canonical settlement outcomes remain:

- `ACCEPTED_AS_IS`
- `MERGE_PROPOSAL_REQUIRED`
- `ESCALATE_REVIEW`
- `DEFERRED`
- `ABANDONED`

## Outcome meaning

### ACCEPTED_AS_IS
All active branch returns are present, non-conflicting, and ready to rejoin the parent organism without additional merge work.

### MERGE_PROPOSAL_REQUIRED
Multiple child returns touch overlapping artifact paths or otherwise require one explicit merge contract before landing.

### ESCALATE_REVIEW
A child return itself requires review, falls outside claim boundaries, or otherwise crosses a trust boundary that must not be resolved silently.

### DEFERRED
At least one active claimed branch has not yet produced a return sufficient for settlement.

### ABANDONED
No viable active branch return remains for the current settlement act.

## Merge proposal law

A merge proposal is a contract, not an automatic merge.

It must preserve:

- parent scope,
- participating branch work-unit ids,
- considered delta ids,
- conflict paths,
- and the proposed next action.

A merge proposal does not imply landing. It preserves the shape of the conflict so later review or explicit synthesis can remain lawful.

## Claim-release law

Final settlement outcomes release active branch claims back to the parent scope.

Deferred settlement does not release claims, because the fan-in act is not complete yet.

## Operator surface

The canonical operator surface now includes:

- `python -m kernel allocator snapshot-settlement ...`
- `python -m kernel allocator settle-children ...`
- `python -m kernel status ...` latest settlement projection

## Non-goals

M2 still does **not** land:

- autonomous merge synthesis,
- branch budget / recursion / drift controls,
- parallel horizon synchronization,
- or unconstrained swarm behavior.

Those remain later M-phase work.
