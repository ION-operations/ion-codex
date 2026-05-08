---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-09T00:36:30-04:00
status: ACTIVE
---

# T54 — Horizon Tightening and Operator Projection

ION must provide one bounded tightening helper that selects the closest lawful next window while preserving packet law.

If the candidate is not packet-ready, the helper must report that fact explicitly rather than pretending execution can begin.

The latest tightening posture should be visible through the existing operator status family.
