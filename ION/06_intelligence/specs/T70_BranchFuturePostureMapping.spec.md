---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T06:19:00-04:00
status: ACTIVE
---

# T70 — Branch future posture mapping

M4 must map bounded branch outcomes into parent-scope future posture under explicit law.

Accepted outcomes:
- accepted fan-in -> IMMEDIATE resume-parent posture
- merge-required -> IMMEDIATE merge-resolution posture
- review escalation -> IMMEDIATE review posture
- deferred -> NEAR waiting posture
- abandoned -> FAR weak future posture
- active claims without settlement -> NEAR pending-branches posture
- stale returns -> IMMEDIATE review posture
