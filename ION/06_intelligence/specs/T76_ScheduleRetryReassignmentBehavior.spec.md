
---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T09:34:00-04:00
status: ACTIVE
---

# T76 — Schedule retry / reassignment behavior

M6 must distinguish:
- stale receipt with same candidate -> retry schedule
- stale receipt with carrier/executor/capability drift -> reassign schedule
- stale receipt with no candidate -> mark stale only
