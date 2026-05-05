---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T23:23:00-04:00
status: ACTIVE
---

# T106 — Schedule rehearse-handoff-entry CLI and status

The operator CLI must expose one bounded M16 route:

- `schedule rehearse-handoff-entry`

Status must expose:
- latest schedule handoff entry rehearsal receipt

The CLI response must include:
- entry rehearsal action
- entry rehearsal readiness
- target executor
- rehearsal summary / manifest refs when materialized
