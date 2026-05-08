---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T12:42:00-04:00
status: ACTIVE
---

# T83 — Schedule settlement receipt

The kernel must persist one `schedule_settlement_receipt` when a completed schedule line is settled.

Minimum fields:
- scope binding
- source completion-release receipt ref
- settlement action
- retired schedule/control/dispatch/completion receipt ids
- optional future-reentry schedule receipt ref
- warnings
