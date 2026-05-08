---
type: reasoning_journal
authority: A3_OPERATIONAL
created: 2026-04-10T03:15:00-04:00
status: ACTIVE
purpose: Record the M3 implementation reasoning for bounded branch-control posture, recursion refusal, stale-claim decay, and stale-return handling
---

# M3 reasoning journal

## Why M3 was necessary

M1 made bounded fan-out real.
M2 made bounded fan-in real.
That left one exposed trust gap: branch growth itself could still drift through stale claims, off-claim returns, or recursive re-fan-out.

## Design choices

- used parent spawn policy as the first explicit budget surface
- kept recursion law strict via a bounded depth ceiling rather than introducing provisional recursion optimism
- treated stale claims as explicit decay candidates, not silent garbage collection
- treated stale returns as review pressure, not invisible noise
- added one receipt family instead of creating another planner or control stack

## Most important implementation boundary

M3 does not widen swarm behavior.
It tightens the existing bounded branch loop.

## Result

The branch loop now has:
- lawful fan-out,
- lawful fan-in,
- and lawful control over branch growth itself.
