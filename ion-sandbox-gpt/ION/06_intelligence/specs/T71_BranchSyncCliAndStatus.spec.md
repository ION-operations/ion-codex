---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T06:20:00-04:00
status: ACTIVE
---

# T71 — Branch synchronization CLI and status

The operator CLI must expose one bounded M4 route:

- `allocator sync-future-posture`

Status must expose:
- latest branch-horizon synchronization receipt

The CLI response must include:
- synchronized horizon layer
- synchronization reason
- selected schedule receipt id when present
