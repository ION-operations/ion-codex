---
type: reasoning_journal
authority: A3_OPERATIONAL
created: 2026-04-09T23:58:00-04:00
status: ACTIVE
purpose: Record the M2 embodiment decisions for bounded fan-in / merge / review settlement
---

# M2 reasoning journal

## Why this packet existed

M1 made fan-out and bounded claim allocation real.
The next trust gap was not allocation. It was lawful rejoining.

## What was implemented

- settlement manager
- settlement outcome family
- merge proposal contract
- branch-settlement receipt family
- claim release on final settlement
- CLI/status settlement visibility
- focused settlement proof

## Important design decisions

- merge remains a contract, not an automatic synthesis engine
- deferred settlement preserves active claims
- final settlement releases claims
- returns outside claim boundaries escalate review rather than being normalized away
