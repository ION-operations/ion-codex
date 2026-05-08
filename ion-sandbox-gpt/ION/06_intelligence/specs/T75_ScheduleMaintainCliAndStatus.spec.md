
---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T09:33:00-04:00
status: ACTIVE
---

# T75 — Schedule maintain CLI and status

The operator CLI must expose:
- `schedule maintain`

Status must expose:
- latest schedule-control receipt

The CLI response must include:
- stale detection
- control action
- retry/reassignment flags
- new schedule receipt id when a refresh occurred
