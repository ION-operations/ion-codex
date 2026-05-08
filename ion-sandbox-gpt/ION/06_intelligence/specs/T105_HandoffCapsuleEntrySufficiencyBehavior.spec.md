---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T23:22:00-04:00
status: ACTIVE
---

# T105 — Handoff capsule entry sufficiency behavior

M16 must distinguish:
- a capsule that is directly sufficient for bounded entry rehearsal,
- a capsule missing required files,
- and a capsule missing required entry context.

A rehearsal-ready capsule must provide:
- capsule JSON
- capsule markdown
- capsule manifest
- activation summary ref
- continuation bundle root ref
- entry packet ref
- required reads
- next action / handoff content
