---
type: research
from: Codex
created: 2026-04-03T21:20:48-04:00
status: COMPLETE
topic: First bounded validation-receipt / signal-emission slice
connections:
  - ION/04_packages/kernel/receipts.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_receipts.py
  - ION/05_context/inbox/codex_kernel_validation_receipt_signal_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_validation_receipt_signal_first_pass/00_trace.md
  - ION/07_templates/bindings/CODEX__CODE.md
  - ION/06_intelligence/specs/T01_TransitionSchema.spec.md
  - ION/06_intelligence/specs/T07_SignalSchema.spec.md
  - ION/06_intelligence/research/2026-04-03_codex_kernel_open_question_routing_first_pass.md
---

# Codex Kernel Validation Receipt / Signal First Pass

## Why this exists

The active kernel stack could now validate deltas, apply accepted artifacts, and route
open questions, but it still lacked the first durable post-validation explanation layer.
Validation reasons existed only in the live `ValidationDecision`, and no canonical
machine-readable signal was yet emitted from those outcomes.

This pass adds that bounded reporting layer.

## Sources or surfaces considered

- `ION/04_packages/kernel/validation.py`
- `ION/04_packages/kernel/questions.py`
- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_receipts.py`
- `ION/06_intelligence/specs/T01_TransitionSchema.spec.md`
- `ION/06_intelligence/specs/T07_SignalSchema.spec.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/receipts.py` now provides the first bounded
  validation-receipt / signal-emission helper for the active kernel stack.
- The helper introduces:
  `KernelReceiptEmitter`, `IonReceiptEmitter`, `KernelReceiptError`,
  `ValidationReceipt`, `EmittedSignal`, `ReceiptPreparation`, and
  `ReceiptEmissionResult`.
- The helper intentionally binds to the live `ValidationDecision` object rather than
  trying to reconstruct reasons from persisted state later. That is the truthful first
  pass because validation reasons are not yet stored anywhere else.
- Each emission now produces:
  - one durable validation receipt JSON artifact
  - one canonical signal JSON artifact
- The signal side is deliberately narrow and canonicalized by outcome:
  - `ACCEPTED` / `ACCEPTED_AS_WITNESS` -> `TASK_COMPLETE`
  - `REJECTED` -> `TASK_FAILED`
  - `REQUIRES_REVIEW` -> `BLOCKED`
- Receipts preserve the key validation provenance now available in the live decision:
  work unit, delta, protocol, transition, resulting statuses, confidence, reasons,
  artifact paths, artifact authority classes, and proposed signal types.
- Signals are emitted in JSON form, aligned with the active draft signal schema rather
  than the root’s human-authored markdown signals.
- `ION/tests/test_kernel_receipts.py` proves:
  accepted receipt plus completion signal, rejected receipt plus failure signal, and
  review-held receipt plus blocked signal.
- The combined kernel suite is now at **77 passing tests**.

## Boundary

- This is not the full signal router.
- It does not yet consume or archive emitted signals.
- It does not yet append ledger rows.
- It does not yet persist validation reasons independently of the receipt artifact.
- It does not yet emit multiple signals from one decision, even if the delta proposed
  extra signals.

## Implications

- The active kernel now has a truthful post-validation explanation layer:
  `ValidationDecision -> validation receipt -> canonical signal`
- Validation results are no longer only in-memory control flow. They can now be
  externalized as machine-readable evidence and coordination artifacts.
- This materially improves the kernel’s portability and inspectability, even though
  signal routing, archiving, and ledger integration still remain ahead.

## Recommended next moves

- Decide whether the next runtime slice should be signal consumption / archiving or the
  first bounded child-work issuance path.
- If signal routing is next, keep it narrow: consume the canonical JSON signals this
  pass now emits before widening into the broader historical signal forest.
