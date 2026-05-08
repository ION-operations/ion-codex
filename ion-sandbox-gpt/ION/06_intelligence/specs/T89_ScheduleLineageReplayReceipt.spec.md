---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T15:22:00-04:00
status: ACTIVE
---

# T89 — Schedule lineage replay receipt

The kernel must persist one `schedule_lineage_replay_receipt` when archived schedule lineage is replayed for one scope.

Minimum fields:
- source schedule-lineage archive receipt id
- active schedule receipt id when present
- matching dispatch/completion/settlement refs when present
- reconstructed active-cycle stage
- replay action
- replay summary
