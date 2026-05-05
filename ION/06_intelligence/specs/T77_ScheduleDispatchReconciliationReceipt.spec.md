---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T11:07:00-04:00
status: ACTIVE
---

# T77 — Schedule dispatch reconciliation receipt

The kernel must persist one `schedule_dispatch_reconciliation_receipt` when schedule witness is reconciled into assignment / dispatch reality.

Minimum fields:
- source schedule receipt id
- optional source schedule-control and branch-reschedule ids
- resolved work-unit id
- assignment action
- before/after work-unit status
- selected carrier / executor / capability
- capability assignment delta
- retired schedule and schedule-control receipt ids
