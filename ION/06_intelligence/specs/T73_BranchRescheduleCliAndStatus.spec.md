---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T08:08:00-04:00
status: ACTIVE
---

# T73 — Branch rescheduling CLI and status

The operator surface must expose:
- `allocator reschedule-after-sync`
- latest branch-reschedule receipt in `status`

The response must preserve:
- rebinding_required
- rebinding_fields
- reschedule_reason
- prior/new carrier and executor binding where present
