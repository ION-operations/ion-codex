---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T16:32:00-04:00
status: ACTIVE
---

# T92 — Schedule resume projection receipt

The kernel must persist one `schedule_resume_projection_receipt` when replayed active-cycle state is projected into a bounded resume surface.

Minimum fields:
- source schedule-lineage replay receipt id
- active cycle stage
- projection action
- resume readiness
- packet path/checksum when materialized
- target executor
- required reads
- next action
