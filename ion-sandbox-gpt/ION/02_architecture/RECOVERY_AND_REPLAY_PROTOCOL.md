# RECOVERY AND REPLAY PROTOCOL

## Purpose

Define the truthful recovery/replay floor for supervised daemon-service runs.

## Core law

1. Recovery is subordinate to kernel truth and operator control.
2. Replay is explicit; no hidden auto-resume or unattended restart loop exists.
3. Replay re-enters the live daemon-service policy gate rather than bypassing it.
4. Replay must remain distinguishable from fresh daemon-service invocation.
5. Stale resumable runs require explicit operator approval unless an equivalent override is explicitly supplied.

## Required behaviors

### 1. Daemon-service recovery classification

Every daemon-service receipt must expose machine-readable recovery state:
- `resumable`
- `classification`
- replay metadata when the run was itself a replay

Minimum classifications:
- `MAX_STEPS_REACHED`
- `BLOCKED_UNSUPPORTED`
- `IDLE_COMPLETE`
- `DRY_RUN_ONLY`
- `APPROVAL_REQUIRED`
- `CONTROL_BLOCKED`
- `POLICY_BLOCKED`

### 2. Replay selection

Recovery/replay may select a source by:
- explicit daemon-service receipt path
- latest resumable daemon-service receipt from the service ledger

### 3. Stale-state detection

A resumable candidate may become stale by age threshold.
Stale resumable candidates must not replay silently.

### 4. Controlled resumption

Replay must:
- preserve the original daemon-service request shape unless explicitly overridden
- carry replay metadata into the new daemon-service request
- write its own replay receipt and replay ledger row
- map the resulting daemon-service status back into explicit replay status

### 5. Non-goals

- no hidden auto-restart
- no unattended replay loop
- no promotion of replay receipts into kernel truth
- no authority bypass around supervised daemon-service policy
