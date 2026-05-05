---
type: specification
authority: A3_OPERATIONAL
created: 2026-04-09T23:16:00-04:00
status: ACTIVE
---

# T62 — Branch Claim Receipt Persistence and CLI Bridge

## Requirement

The kernel must be able to persist active branch-claim receipts for the selected branch set and expose that behavior through the canonical CLI.

## The embodiment must

- persist one active `BranchClaimReceipt` per selected branch,
- index those receipts by parent work-unit scope, capability, and child work unit,
- allow the latest active receipt to be projected,
- and make `allocator claim-children` return the selected/deferred projection that justified the persisted receipts.

## Acceptance proof

- `ION/tests/test_kernel_allocator.py`
- `ION/tests/test_kernel_operator_cli.py`
