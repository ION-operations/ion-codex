# T39 — Supervised Daemon Service

## Intent

Provide a truthful service harness over the existing bounded daemon loop.

## Required Behaviors

1. Load operator control state.
2. Evaluate automation policy before loop execution.
3. Refuse execution lawfully when control or policy blocks it.
4. Support bounded dry-run service evaluation.
5. Run the existing daemon loop only when allowed.
6. Emit machine-readable service receipts and ledger rows.

## Status Classes

- `EXECUTED`
- `DRY_RUN`
- `CONTROL_BLOCKED`
- `POLICY_BLOCKED`
- `APPROVAL_REQUIRED`

## Non-Goals

- unattended service mode
- background scheduler
- external execution bridge
