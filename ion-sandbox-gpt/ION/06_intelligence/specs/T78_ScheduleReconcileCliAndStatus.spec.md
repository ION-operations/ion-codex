---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T11:08:00-04:00
status: ACTIVE
---

# T78 — Schedule reconcile CLI and status

The operator CLI must expose one bounded M7 route:
- `schedule reconcile`

Status must expose:
- latest schedule-dispatch reconciliation receipt

The CLI response must include:
- assignment action
- before/after work-unit status
- capability assignment delta
- retired schedule receipt ids
