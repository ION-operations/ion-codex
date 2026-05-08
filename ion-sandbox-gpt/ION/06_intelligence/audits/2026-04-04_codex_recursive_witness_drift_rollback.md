# Codex Recursive Witness Drift Rollback

## Verdict

The later 2026-04-04 witness-lane expansions crossed from bounded runtime deepening into recursive meta-maintenance drift.

The clean rollback boundary is the checkpoint `ION_updated_2026-04-04_queue_receipts_sweep_aggregation.zip`. Everything after that boundary is treated as contaminated until re-proposed explicitly.

## Why the later chain is invalid

- runtime family names began recursively composing `aggregate` and `maintenance` into self-similar layers
- daemon routing began surfacing actions whose value came only from maintaining prior maintenance witnesses
- Codex continuity began using those recursive names as if they were a legitimate next frontier
- passing tests stopped meaning architectural health because the tests were proving the same drift

## Repair applied

1. Reconstructed the working root from the last bounded checkpoint.
2. Quarantined the later witness-recursion chain instead of extending it.
3. Added an anti-recursion regression test over kernel/runtime surfaces and Codex continuity so recursive meta-families fail fast.
4. Reset Codex continuity to a safe frontier: hold witness depth here unless a new doctrine-backed reason justifies a fresh runtime family.

## Quarantined later chain

- `2026-04-04_codex_kernel_refresh_aggregate_and_planner_policy_first_pass`
- `2026-04-04_codex_kernel_reviewer_aggregate_policy_and_planner_housekeeping_receipts_first_pass`
- `2026-04-04_codex_kernel_reviewer_housekeeping_receipts_and_planner_maintenance_aggregation_first_pass`
- `2026-04-04_codex_kernel_reviewer_maintenance_aggregation_and_planner_aggregate_policy_first_pass`
- `2026-04-04_codex_kernel_reviewer_policy_receipts_and_planner_policy_aggregation_first_pass`
- `2026-04-04_codex_kernel_reviewer_retention_aggregation_and_planner_policy_receipts_first_pass`
- `2026-04-04_codex_kernel_reviewer_retention_policy_and_planner_receipt_retention_aggregation_first_pass`

## Safe next posture

- keep `reviewer_queue_refresh`, `planner_manifest_sweep`, and `planner_manifest_sweep_aggregate` as the current bounded witness lane
- do not add witness-of-witness families without an explicit architecture decision
- if deeper retention is required, design one canonical housekeeping family instead of recursively mirroring existing families
