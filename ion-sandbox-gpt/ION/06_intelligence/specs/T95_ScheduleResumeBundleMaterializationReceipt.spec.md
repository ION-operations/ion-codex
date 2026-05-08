---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T18:22:00-04:00
status: ACTIVE
---

# T95 — Schedule resume-bundle materialization receipt

The kernel must persist one `schedule_resume_bundle_materialization_receipt` when an M12 resume projection is evaluated for continuation-bundle materialization.

Minimum fields:
- scope binding
- source schedule resume projection ref
- source lineage replay/archive refs
- linked context-perfect continuation receipt ref when materialized
- materialization action
- packet path/checksum when present
- bundle root + manifest/role-session paths when present
- warnings
