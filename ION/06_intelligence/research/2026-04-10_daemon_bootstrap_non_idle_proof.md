# 2026-04-10 daemon bootstrap non-idle proof

## Summary

ION's supervised daemon already has enough truthful surface to perform one lawful bounded action in an otherwise empty extracted root.

The smallest currently working bootstrap path is:

1. place one canonical `TASK_FAILED` `.signal.json` artifact in `ION/05_context/signals/`
2. run `python -m kernel daemon --workspace-root . --format json run --approval --max-steps 1`
3. allow the daemon to consume/archive the signal and materialize one durable `signal_followup` open question in the kernel store

This does **not** fake autonomy. It uses the current bounded supervised carrier exactly as implemented.

## Live proof performed in this working branch

Seed artifact placed:

- `ION/05_context/signals/archive/ION_TASK_FAILED_bootstrap_non_idle_daemon_20260410T1835.signal.json`

Daemon outcome:

- service status: `EXECUTED`
- loop status: `MAX_STEPS_REACHED`
- final action: `CONSUME_ACTIVE_SIGNAL`
- final reason: `CONSUMED_ACTIVE_SIGNAL:REPLAN_OR_RETRY:CREATED_OPEN_QUESTION`

Primary persisted evidence:

- `ION/05_context/history/daemon_service_ledger.json`
- `ION/05_context/history/daemon_service_receipts/daemon-service-2026-04-10t18-15-04-00-00.daemon_service_receipt.json`
- `ION/05_context/history/kernel_store/open_questions/signal-followup-sig-ion-self-use-bootstrap-20260410t183500z.json`

## Why this matters

This proves the daemon can already be non-idle under current law without inventing a future runtime.
It also proves there is a truthful self-use bootstrap path even when the kernel store begins empty.

The daemon did not need hidden context. It only needed one lawful machine-readable pressure artifact.

## Immediate interpretation

The current missing piece is not "daemon existence".
The missing piece is **repeatable lawful seed pressure**.

That can likely be supplied by one or more future bridges such as:

- inbox/task packet -> canonical signal
- inbox/task packet -> kernel work unit + context package
- operator/bootstrap packet -> open question / signal / work seed

## Next bounded step

Define and land one explicit bootstrap bridge so fresh extracted roots do not require manual signal authoring to produce the first lawful daemon action.
