---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T08:07:00-04:00
status: ACTIVE
---

# T72 — Branch reschedule receipt

The kernel must persist one `branch_reschedule_receipt` when the parent schedule is reconsidered after explicit M4 synchronization.

Minimum witness:
- source sync receipt
- prior/new schedule receipt refs
- prior/new carrier binding
- prior/new executor/capability binding
- rebinding_required
- rebinding_fields
- reschedule_reason
