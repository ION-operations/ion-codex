---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-08T23:12:00-04:00
status: ACTIVE
owner: Codex working session
purpose: Define lifecycle state and receipt schema for supervised runtime hardening
connections:
  - ION/02_architecture/OPERATIONAL_HARDENING_PROTOCOL.md
  - ION/04_packages/kernel/operational_hardening.py
---

# T45 — Operational Hardening Lifecycle

## Required objects

### SupervisedRuntimeStartupRequest
Fields:
- workspace_root
- context_mode
- automation_stage
- route_stage
- calibration_status
- threshold_action
- review_required
- manual_fallback_required
- supervisor_present
- explicit_approval
- actor
- reason
- action_timestamp

### SupervisedRuntimeShutdownRequest
Fields:
- workspace_root
- actor
- reason
- drain
- action_timestamp

### SupervisedRuntimeLifecycleReceipt
Fields:
- status
- requested_at
- control_state
- preferred_mode_active
- runtime_state_path
- lifecycle_receipt_path
- lifecycle_ledger_path
- policy_evaluation
- notes

## Required files

- `ION/05_context/history/supervised_runtime/supervised_runtime_state.json`
- `ION/05_context/history/supervised_runtime/receipts/*.supervised_runtime_receipt.json`
- `ION/05_context/history/supervised_runtime/supervised_runtime_ledger.json`

## Status values

- `STARTED`
- `ALREADY_ENABLED`
- `APPROVAL_REQUIRED`
- `POLICY_BLOCKED`
- `CONTROL_BLOCKED`
- `DRAINING`
- `STOPPED`

## Exit contract

A J5-compliant runtime may describe itself as the preferred active automation mode only if:
- preferred runtime state is persisted,
- lifecycle receipts are on disk,
- operator control state is resolvable.
