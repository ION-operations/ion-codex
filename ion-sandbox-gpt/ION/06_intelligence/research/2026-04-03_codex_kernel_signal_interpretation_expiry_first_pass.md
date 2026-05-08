---
type: research
from: Codex
created: 2026-04-03T22:06:20-04:00
status: COMPLETE
topic: First bounded canonical signal interpretation and stale-signal expiry slice
connections:
  - ION/04_packages/kernel/signals.py
  - ION/04_packages/kernel/receipts.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_signals.py
  - ION/05_context/inbox/codex_kernel_signal_interpretation_expiry_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_signal_interpretation_expiry_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_signal_consumption_archive_first_pass.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_daemon_act_once_first_pass.md
---

# Codex Kernel Signal Interpretation Expiry First Pass

## Why this exists

The active kernel could already emit canonical JSON signals and later consume them
into archive, but it still lacked two truthful pieces:

- a bounded interpretation layer for what those emitted signal types actually mean
- an explicit stale-signal expiry path for active signals that outlive their useful window

This pass adds both without pretending the full signal router already exists.

## Sources or surfaces considered

- `ION/04_packages/kernel/signals.py`
- `ION/04_packages/kernel/receipts.py`
- `ION/04_packages/kernel/daemon.py`
- `ION/tests/test_kernel_signals.py`
- `ION/tests/test_kernel_receipts.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/signals.py` now covers three bounded responsibilities:
  - discovery / consumption of active canonical `.signal.json` artifacts
  - interpretation of the emitted canonical signal types
  - stale-signal expiry into explicit archived `EXPIRED` state
- The new interpretation surface is intentionally narrow:
  - `TASK_COMPLETE -> COMPLETION -> ACKNOWLEDGE_AND_ARCHIVE`
  - `TASK_FAILED -> FAILURE -> REPLAN_OR_RETRY`
  - `BLOCKED -> BLOCKER -> ESCALATE_REQUIRED_ROLE`
- This keeps the daemon honest. It now has explicit meaning for the signals the
  current receipt emitter actually emits, but it does not yet claim a full router.
- `ION/04_packages/kernel/receipts.py` now carries optional `expired_by` and
  `expired_at` lifecycle metadata on `EmittedSignal`, so stale expiry is durable
  rather than an implicit archive side effect.
- `expire_stale_signals(...)` now gives the active signal lane a lawful path from:
  `ACTIVE -> EXPIRED -> archived file`
  when a signal ages past a supplied threshold.
- `ION/tests/test_kernel_signals.py` now proves:
  - completion-signal interpretation
  - failure-signal interpretation
  - blocked-signal interpretation
  - stale-signal expiry with archived provenance
  - preservation of fresh non-stale signals
- The combined kernel suite is now at **101 passing tests**.

## Boundary

- This is not yet full signal execution inside `act_once`.
- It does not yet interpret arbitrary user-written signal surfaces.
- It does not yet decide recovery strategy beyond the bounded recommended action.
- It does not yet add stale-signal expiry to a repeating daemon loop automatically.

## Implications

- The daemon stack no longer sees active canonical signals as opaque payloads only.
- Signal ageing is now explicit, which removes one of the main ambiguities around
  what to do with orphaned active daemon pressure.
- The next runtime step is now narrower and cleaner: either teach `act_once` how
  to consume interpreted active signals, or move up one level and build the first
  repeat-until-blocked daemon loop on top of the current arbiter and executor.

## Recommended next moves

- Support `CONSUME_ACTIVE_SIGNAL` inside `act_once` using the new interpretation layer.
- Then decide whether the daemon should:
  - keep advancing one step at a time under explicit operator control, or
  - gain a higher-order loop that repeats arbitration and supported execution until
    only unsupported or idle pressure remains.
