---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T18:20:00-04:00
status: ACTIVE
purpose: Define the M13 law for materializing an M12 resume projection into one explicit continuation bundle under existing continuation/takeover proof law
---

# M13 — Schedule resume-bundle materialization protocol

## Purpose

M13 closes the gap between a lawful M12 resume projection and a fresh-executor continuation bundle.

The problem is no longer whether the active cycle can be replayed or projected.
The problem is whether that projection can become one bounded continuation bundle without hidden context loading.

## Core law

M13 must:
- remain subordinate to M12 resume projection,
- reuse existing context-perfect continuation law,
- materialize explicit required reads,
- and persist one linking receipt that ties schedule resume witness back to continuation/takeover proof.

M13 must not:
- mutate schedule state silently,
- invent hidden context loading,
- or introduce a parallel continuation system.

## Required behavior

1. read the latest lawful schedule resume projection for a scope,
2. if the projection is resume-ready but lacks a packet file, materialize the packet first,
3. prove that packet through the existing context-perfect continuation manager,
4. persist one schedule-resume bundle materialization receipt,
5. expose the latest receipt through CLI and status.

## Outcomes

- `MATERIALIZED_CONTINUATION_BUNDLE`
- `NO_RESUME_PACKET_AVAILABLE`

## Persistence families

M13 uses:
- `schedule_resume_projection_receipt`
- `context_perfect_continuation_receipt`
- `schedule_resume_bundle_materialization_receipt`

## Operator surface

Canonical CLI route:
- `python -m kernel schedule materialize-resume-bundle ...`

Status must expose:
- latest schedule-resume bundle materialization receipt
