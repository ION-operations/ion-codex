# Trace — Codex Recursive Witness Drift Rollback

## Inputs

- last bounded checkpoint: `ION_updated_2026-04-04_queue_receipts_sweep_aggregation.zip`
- contaminated latest checkpoint: `ION_updated_2026-04-04_reviewer_retention_policy_planner_receipt_retention_aggregation.zip`

## Actions

1. diffed the bounded checkpoint against the contaminated later root
2. confirmed recursive meta-maintenance families in code, exports, daemon routing, tests, and Codex continuity
3. reconstructed the working root from the bounded checkpoint
4. added a regression guard against recursive witness-family naming
5. filed rollback/quarantine audit and updated Codex continuity

## Result

The working root is restored to the last bounded witness-lane checkpoint and guarded against the same recursion pattern.
