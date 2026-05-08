
---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T09:32:00-04:00
status: ACTIVE
---

# T74 — Schedule control receipt

The kernel must persist one `schedule_control_receipt` when stale / retry / reassignment posture is evaluated.

Minimum fields:
- scope binding
- prior schedule receipt id
- optional new schedule receipt id
- stale flag and stale reasons
- control action
- retry / reassignment flags
- rebinding fields
