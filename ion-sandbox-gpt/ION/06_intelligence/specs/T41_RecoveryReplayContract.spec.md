# T41 — Recovery Replay Contract

## Scope

Machine-readable contract for supervised daemon-service recovery and replay.

## Required surfaces

- `kernel/recovery_replay.py`
- daemon-service receipt recovery classification
- replay receipt + replay ledger

## Inputs

### RecoveryReplayRequest

Required:
- `workspace_root`
- `selection_mode`

Optional:
- `service_receipt_path`
- `stale_after_seconds`
- `current_timestamp`
- `explicit_approval`
- `supervisor_present`
- `allow_stale_replay`
- `dry_run`
- `max_steps_override`
- `packet_output_root`
- `repo_root`
- `actor`
- `notes`

## Selection modes

- `EXPLICIT_SERVICE_RECEIPT`
- `LATEST_RESUMABLE`

## Outputs

### ServiceRecoveryClassification

Must include:
- source receipt path
- daemon-service status
- loop status when present
- resumable boolean
- recovery classification
- stale boolean
- age seconds when parseable
- replay ancestry markers

### RecoveryReplayReceipt

Must include:
- replay status
- requested time
- selection mode
- optional classification
- source service receipt path
- replayed service receipt path when replay executed
- replayed service status when replay executed
- replay receipt path
- replay ledger path

## Replay statuses

- `REPLAYED`
- `DRY_RUN`
- `NO_RESUMABLE_CANDIDATE`
- `NON_RESUMABLE`
- `STALE_REQUIRES_APPROVAL`
- `CONTROL_BLOCKED`
- `POLICY_BLOCKED`
- `APPROVAL_REQUIRED`

## Lawful behavior

1. Replay must use the live daemon-service path.
2. Replay must not bypass operator control or automation policy.
3. Replay must remain distinguishable from a fresh daemon-service run.
4. Stale resumable candidates must require explicit approval unless explicitly overridden.
