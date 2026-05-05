---
type: research_note
authority: A3_OPERATIONAL
created: 2026-04-10T14:10:00-04:00
status: ACTIVE
purpose: Record truthful verification of the callable daemon/runtime surfaces in the extracted ION root and define the next bootstrap work required for non-idle supervised runs.
---

# Daemon Surface Verification and Bootstrap Path

## Summary

A real bounded daemon/service surface is present and callable from the extracted working branch.
The currently available operator entry path is:

- `python -m kernel runtime ...`
- `python -m kernel control ...`
- `python -m kernel daemon ...`
- `python -m kernel replay ...`

using:

- working directory: repository root
- `PYTHONPATH=ION/04_packages`

The daemon is therefore not hypothetical.
It is a supervised bounded carrier that can be invoked truthfully from the current repo.

## Verified commands

From repository root:

```bash
PYTHONPATH=ION/04_packages python -m kernel --help
PYTHONPATH=ION/04_packages python -m kernel status --format json
PYTHONPATH=ION/04_packages python -m kernel runtime --format json start --approval
PYTHONPATH=ION/04_packages python -m kernel daemon --format json run --approval --dry-run
PYTHONPATH=ION/04_packages python -m kernel daemon --format json run --approval --max-steps 1
```

## What happened

### Status
The extracted root reported:
- operator control state present,
- supervised runtime state files present,
- daemon service ledger path present,
- kernel store currently empty,
- no existing lawful work candidates in this extracted environment.

### Runtime start
`runtime start --approval` succeeded and confirmed the preferred supervised runtime mode is available.
The runtime reported `ALREADY_ENABLED` in this environment and wrote lifecycle receipt paths under:

- `ION/05_context/history/supervised_runtime/`

### Daemon dry run
`daemon run --approval --dry-run` succeeded and wrote a daemon-service receipt path under:

- `ION/05_context/history/daemon_service_receipts/`

This proves the service gate, policy evaluation, and receipt path are live.

### Real bounded daemon run
`daemon run --approval --max-steps 1` executed successfully.
The run produced:

- daemon service receipt
- daemon loop receipt
- system ledger update

The truthful result was `IDLE` with reason `NO_ACTION_REQUIRED` and arbitration candidate `NO_LAWFUL_ACTIONS_AVAILABLE`.

This is a good sign, not a bad one.
It means the carrier is real, policy-gated, and bounded — but the extracted root has not yet been primed with lawful queued work for that carrier to act on.

## Why the daemon idled

The present extracted root has:
- empty kernel store,
- no queued work units,
- no planner manifests,
- no reviewer queue items,
- no signal consumption candidates visible to the daemon loop,
- no explicit bounded scope target passed in for active work.

So the daemon is callable, but the environment is not yet seeded for non-idle automation.

## What this means operationally

ION can already be used in a hybrid mode:

1. manual/route-driven work can create lawful artifacts,
2. bounded kernel CLI surfaces can validate, schedule, and emit receipts,
3. the daemon can be invoked as a supervised carrier for bounded runs,
4. replay/recovery surfaces exist for lawful interrupted runs.

What is *not* yet truthful to claim is a self-sustaining unattended automation loop in this current chat environment.
A persistent background service outside the current turn is not available here.

So the correct posture is:

- foreground bounded supervised runs,
- repo-native receipts and ledgers,
- manual or semi-automated seeding of lawful candidates,
- progressive embodiment of self-use automation.

## Immediate bootstrap gap

To make the daemon do real file automation in the extracted root, one of the following must become true:

### Path A — seed real kernel work objects
Create lawful `work_unit`, `context_package`, `planner_manifest`, or equivalent store-backed objects that the daemon loop already knows how to arbitrate.

### Path B — seed daemon-consumable signal traffic
Provide canonical signal files or other consumption candidates that the daemon loop/service can lawfully interpret and act on.

### Path C — add a bootstrap bridge from active inbox/task packets into kernel store candidates
Right now the repo clearly values inbox/task packets, but the live daemon loop in this extracted environment does not yet automatically convert those visible packets into arbitrable kernel work.
A bootstrap bridge here would materially increase native self-use power.

## Best next move

The highest-leverage next packet is:

**bootstrap lawful non-idle daemon input**

specifically:

1. identify the smallest daemon-consumable candidate type already supported,
2. create one canonical seed object/packet for it,
3. run the daemon again,
4. verify that it performs one non-idle bounded action,
5. record receipts and rollback/replay implications.

## Judgment

The daemon surface is real.
The automation posture is real.
The current limitation is not absence of automation code.
The limitation is that the extracted root still needs a lawful bootstrap path from visible project work into the daemon's arbitrable candidate space.

That is now a concrete build target rather than an abstraction.
