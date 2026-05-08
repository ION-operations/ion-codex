---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T21:24:40-04:00
from: Sovereign
target: ION/04_packages/kernel/signals.py
depends_on: ION/04_packages/kernel/receipts.py
status: COMPLETE
updated: 2026-04-03T21:28:50-04:00
completed_by: Codex
---

# Mission: Implement the first bounded kernel signal-consumption / archive helper

## Goal

Build the first truthful signal-consumption layer so canonical JSON signals
emitted by the receipt helper can be discovered, consumed, and archived under an
explicit workspace root without pretending the full daemon signal router already
exists.

## Source / Context

- `ION/04_packages/kernel/receipts.py`
- `ION/04_packages/kernel/model.py`
- `ION/06_intelligence/specs/T07_SignalSchema.spec.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_validation_receipt_signal_first_pass.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Operate only on canonical `.signal.json` artifacts.
3. Discover active signals from an explicit workspace root.
4. Support target filtering, with `DAEMON` as the default consumer path.
5. Consume signals by recording consumer provenance and moving them to an archive
   lane.
6. Export the helper surface from the kernel package.
7. Add focused tests for discovery, consume/archive behavior, and refusal of
   non-active or malformed paths.

## Deliverables

- new `ION/04_packages/kernel/signals.py`
- patched `ION/04_packages/kernel/__init__.py`
- one or more signal-consumption tests
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim broader signal routing or child-work issuance exists.
2. Do not consume markdown `.signal.md` artifacts in this pass.
3. Preserve explicit provenance if the pass is completed by Codex under its own
   `CODE` binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the signal-consumption first-pass result.

## Completion Record — 2026-04-03T21:28:50-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded canonical signal-consumption / archive helper, verified discovery plus consume/archive behavior against real emitted signals, and closed the pass under Codex's CODE binding.
- artifacts:
  - ION/04_packages/kernel/signals.py
  - ION/04_packages/kernel/receipts.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_signals.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_signal_consumption_archive_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_SIGNAL_CONSUMPTION_ARCHIVE_FIRST_PASS_20260403T2127.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_signal_consumption_archive_first_pass/00_trace.md
- next_action: Build the first bounded child-work issuance path from accepted follow-up intent.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
