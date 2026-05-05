---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T22:01:29-04:00
from: Sovereign
target: ION/04_packages/kernel/signals.py
depends_on: ION/04_packages/kernel/receipts.py
status: COMPLETE
updated: 2026-04-03T22:10:41-04:00
completed_by: Codex
---

# Mission: Implement the first bounded kernel signal interpretation and expiry helper

## Goal

Extend the current canonical signal layer so the active kernel can interpret the
meaning of emitted daemon signals and expire stale active signals explicitly,
without pretending a full signal router or daemon reconciliation layer already exists.

## Source / Context

- `ION/04_packages/kernel/signals.py`
- `ION/04_packages/kernel/receipts.py`
- `ION/04_packages/kernel/daemon.py`
- `ION/tests/test_kernel_signals.py`
- `ION/tests/test_kernel_receipts.py`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Keep the first pass explicit and bounded.
2. Interpret only the canonical signal types the current receipt emitter actually emits.
3. Make stale-signal expiry explicit and durable.
4. Preserve archive safety and workspace-root path discipline.
5. Export the new interpretation / expiry surface from the kernel package.
6. Add focused tests for interpretation, expiry, and non-stale preservation.

## Deliverables

- patched `ION/04_packages/kernel/signals.py`
- patched `ION/04_packages/kernel/__init__.py`
- expanded `ION/tests/test_kernel_signals.py`
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim a full signal router exists.
2. Do not over-infer semantics beyond the receipt-emitted signal schema.
3. Preserve explicit provenance if the pass is completed by Codex under its own
   `CODE` binding rather than an independent support role.

## Completion Signal

Emit one Codex signal pointing to the signal interpretation / expiry first-pass result.

## Completion Record — 2026-04-03T22:10:41-04:00

- status: COMPLETE
- operator: Codex
- summary: Implemented the first bounded canonical signal interpretation and stale-signal expiry slice, giving the kernel explicit meaning for emitted completion/failure/blocker signals and a lawful path for aging active signals into archived EXPIRED state.
- artifacts:
  - ION/04_packages/kernel/signals.py
  - ION/04_packages/kernel/receipts.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_signals.py
  - ION/06_intelligence/research/2026-04-03_codex_kernel_signal_interpretation_expiry_first_pass.md
  - ION/05_context/signals/CODEX_KERNEL_SIGNAL_INTERPRETATION_EXPIRY_FIRST_PASS_20260403T2206.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_signal_interpretation_expiry_first_pass/00_trace.md
- next_action: Support signal consumption inside act_once or build a higher-order repeat-until-blocked daemon loop.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
