---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T14:06:00-04:00
status: ACTIVE
---

# T86 — Schedule lineage archive receipt

The kernel must persist one `schedule_lineage_archive_receipt` for a scope when settled schedule lineage is compacted into archival witness.

Minimum fields:
- source settlement receipt id
- active schedule receipt id when present
- active candidate summary when present
- archived schedule/control/dispatch/completion/settlement receipt ids
- settled line count
- archived receipt count
- lineage action
