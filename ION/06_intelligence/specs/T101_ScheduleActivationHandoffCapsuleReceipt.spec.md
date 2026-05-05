
---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T22:07:00-04:00
status: ACTIVE
---

# T101 — Schedule activation handoff capsule receipt

The kernel must persist one `schedule_activation_handoff_capsule_receipt` when validated activation state is compacted into a handoff capsule.

Minimum fields:
- parent scope binding
- source activation / bundle / replay refs
- capsule action
- capsule readiness
- capsule file paths
- selected executor / capability
- required reads
- next action
