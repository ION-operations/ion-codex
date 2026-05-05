---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T03:05:00-04:00
status: ACTIVE
---

# T66 — BranchControlReceipt and budget posture

M3 requires one explicit witness family for bounded branch posture.

Required fields:
- receipt id / created at
- parent scope type / ref
- policy id
- parent depth
- branch budget limit / budget remaining
- active claim receipt ids
- active branch work-unit ids
- stale-claim receipt ids
- decayed claim receipt ids
- stale-return delta ids
- stale-return work-unit ids
- recursion-refused boolean
- next action
- warnings

Minimum behaviors:
- receipts persist under kernel store / index
- latest receipt is status-visible
- budget posture derives from parent spawn policy unless bounded override is lower
