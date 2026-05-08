
---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T22:09:00-04:00
status: ACTIVE
---

# T103 — Schedule materialize-handoff-capsule CLI and status

The operator CLI must expose one bounded M15 route:
- `schedule materialize-handoff-capsule`

Status must expose:
- latest `schedule_activation_handoff_capsule_receipt`

The CLI response must include:
- capsule materialization action
- capsule readiness
- capsule json / markdown / manifest paths when materialized
