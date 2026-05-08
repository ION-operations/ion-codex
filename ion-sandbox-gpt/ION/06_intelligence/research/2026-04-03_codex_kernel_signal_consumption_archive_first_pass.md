---
type: research
from: Codex
created: 2026-04-03T21:27:05-04:00
status: COMPLETE
topic: First bounded canonical signal-consumption / archive slice
connections:
  - ION/04_packages/kernel/signals.py
  - ION/04_packages/kernel/receipts.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_signals.py
  - ION/05_context/inbox/codex_kernel_signal_consumption_archive_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_signal_consumption_archive_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/specs/T07_SignalSchema.spec.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_validation_receipt_signal_first_pass.md
---

# Codex Kernel Signal Consumption / Archive First Pass

## Why this exists

The active kernel stack could now emit canonical JSON signals from live validation
outcomes, but those signals still had nowhere to go. They accumulated only as active
files, with no bounded runtime path for discovery, consumption, or archive movement.

This pass adds that first narrow signal-lifecycle bridge.

## Sources or surfaces considered

- `ION/04_packages/kernel/receipts.py`
- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_signals.py`
- `ION/06_intelligence/specs/T07_SignalSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/signals.py` now provides the first bounded canonical
  signal-consumption / archive helper for the active kernel stack.
- The helper introduces:
  `KernelSignalConsumer`, `IonSignalConsumer`, `KernelSignalConsumerError`,
  `SignalFileRef`, and `SignalConsumptionResult`.
- The signal lifecycle surface in `ION/04_packages/kernel/receipts.py` is now widened
  just enough to support real post-emission state:
  `ACTIVE`, `CONSUMED`, `ARCHIVED`, and `EXPIRED`, plus optional
  `consumed_by` / `consumed_at` provenance on emitted signals.
- This pass is intentionally narrow:
  it consumes only canonical `.signal.json` artifacts, not markdown `.signal.md`
  witness signals from the broader human field.
- Discovery is also intentionally narrow:
  only active signal JSON files in the configured live signal lane are considered, with
  target filtering defaulting to `DAEMON`.
- Consumption now performs the first truthful lifecycle mutation:
  - read active signal
  - record consumer provenance
  - mark it consumed
  - archive it under `ION/05_context/signals/archive/`
- Archive movement is explicit rather than silent deletion.
- `ION/tests/test_kernel_signals.py` proves:
  active daemon-signal discovery, consume-and-archive behavior, refusal of non-active
  signals, and refusal of non-canonical paths.
- The combined kernel suite is now at **81 passing tests**.

## Boundary

- This is not the full daemon signal router.
- It does not yet interpret signals into new work issuance.
- It does not yet consume markdown witness signals.
- It does not yet expire stale signals automatically.
- It does not yet branch behavior by signal type beyond discovery/consumption.

## Implications

- The active kernel now has the first real canonical signal lifecycle:
  `emit -> discover -> consume -> archive`
- The canonical JSON signal surface is no longer write-only.
- This makes the runtime more closed under its own artifacts and materially reduces one
  remaining place where state could accumulate without lawful progression.

## Recommended next moves

- Decide whether the next bounded runtime slice should be:
  - signal interpretation into child-work issuance
  - or direct child-work issuance from accepted follow-up intent without widening the
    signal layer yet
- If the goal is the narrower next step, child-work issuance is now the sharper move:
  the signal lifecycle itself has a truthful minimal loop.
