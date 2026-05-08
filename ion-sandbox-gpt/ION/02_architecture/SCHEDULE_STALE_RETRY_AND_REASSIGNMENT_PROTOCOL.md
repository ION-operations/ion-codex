
---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-10T09:30:00-04:00
status: ACTIVE
purpose: Define the M6 law for explicit stale schedule detection, retry posture, and lawful reassignment without hidden churn
---

# M6 — Schedule stale / retry / reassignment protocol

## Purpose

M6 closes the gap after M5 made rebinding explicit.

The remaining problem is temporal and operational:
- schedule receipts should not remain valid forever,
- stale posture must be made explicit,
- retry and reassignment must not collapse into hidden scheduler churn.

## Core law

A schedule receipt is a witness of then-current future posture, not an eternal lease.

When later reality materially differs from that posture, the kernel must:
- classify the stale condition explicitly,
- distinguish retry from reassignment,
- optionally record one new schedule receipt through the canonical scheduler,
- and persist one schedule-control receipt describing why.

## Required behavior

M6 must be able to detect at least:
- age-exceeded stale posture,
- missing or unavailable bound capability,
- capacity exhaustion,
- candidate drift,
- carrier drift,
- executor drift,
- state drift,
- no-actionable-candidate posture.

## Control outcomes

- `NO_CHANGE`
- `MARK_STALE`
- `RETRY_SCHEDULE`
- `REASSIGN_SCHEDULE`

Retry means the same basic candidate remains lawful and the scheduler is refreshed.
Reassignment means carrier / executor / capability drift is explicit and a fresh schedule receipt is recorded.

## Non-goals

M6 does not:
- dispatch or execute work,
- mutate active assignment state,
- silently rebind carriers,
- or invent a second scheduler.

## Operator surfaces

Canonical CLI route:
- `python -m kernel schedule maintain ...`

Status must expose:
- latest schedule-control receipt
