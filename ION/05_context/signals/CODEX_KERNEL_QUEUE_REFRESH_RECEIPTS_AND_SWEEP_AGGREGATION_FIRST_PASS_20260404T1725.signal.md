---
type: signal
signal: CODEX_KERNEL_QUEUE_REFRESH_RECEIPTS_AND_SWEEP_AGGREGATION_FIRST_PASS
from: Codex
to: Sovereign
created: 2026-04-04T17:25:00-04:00
priority: P1
status: ACTIVE
---

Codex completed the next generated-state witness slice:

- reviewer-queue refresh now emits durable `reviewer_queue_refresh` receipts with graph topology into refreshed queue projections
- retained planner-manifest sweep receipts now aggregate into durable `planner_manifest_sweep_aggregate` witness records
- daemon arbitration/act-once/loop now surface and witness both paths lawfully
- verification: `156 passed, 3 subtests passed`
