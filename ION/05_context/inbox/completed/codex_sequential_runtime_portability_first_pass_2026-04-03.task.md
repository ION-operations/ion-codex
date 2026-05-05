---
type: task
agent: Codex
template: CODE
priority: P1
created: 2026-04-03T20:35:14-04:00
from: Sovereign
target: ION/04_packages/kernel/sequential_kernel.py
depends_on: ION/06_intelligence/research/2026-04-03_codex_response_to_external_canonicalization_memo.md
status: COMPLETE
updated: 2026-04-03T20:38:10-04:00
completed_by: Codex
---

# Mission: Remove first-pass sequential runtime path coupling

## Goal

Remove the live production-root hardcoding from the sequential runtime shell and its
tests without changing the current lawful behavior of the active runtime.

## Source / Context

- `ION/04_packages/kernel/sequential_kernel.py`
- `ION/tests/test_sequential_kernel.py`
- `ION/06_intelligence/research/2026-04-03_codex_response_to_external_canonicalization_memo.md`
- `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Requirements

1. Remove hardcoded `/home/sev/ION - Production` assumptions from the live sequential
   runtime shell and its direct tests.
2. Preserve current runtime behavior for the active root.
3. Resolve the default repo root from discoverable local structure rather than a fixed
   machine path.
4. Remove the hardcoded Atlas absolute reference path from role config.
5. Add or update tests proving the runtime still resolves correctly after the change.

## Deliverables

- patched `ION/04_packages/kernel/sequential_kernel.py`
- patched `ION/tests/test_sequential_kernel.py`
- any required package export changes
- one runtime-hardening note
- one live implementation bundle under `ION/05_context/comms/kernel_router_runs/`

## Constraints

1. Do not claim the full runtime/environment split is complete after this pass.
2. Keep the change bounded to live portability blockers already visible in kernel/test
   code.
3. Preserve explicit provenance if the pass is completed by Codex under its own `CODE`
   binding.

## Completion Signal

Emit one Codex signal pointing to the sequential-runtime portability result.

## Completion Record — 2026-04-03T20:38:10-04:00

- status: COMPLETE
- operator: Codex
- summary: Removed the first live production-root hardcoding from the sequential runtime shell and its tests by adding discoverable repo-root resolution and repo-relative Atlas binding, while preserving active runtime behavior.
- artifacts:
  - ION/04_packages/kernel/sequential_kernel.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_sequential_kernel.py
  - ION/06_intelligence/research/2026-04-03_codex_sequential_runtime_portability_first_pass.md
  - ION/05_context/signals/CODEX_SEQUENTIAL_RUNTIME_PORTABILITY_FIRST_PASS_20260403T2036.signal.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_sequential_runtime_portability_first_pass/00_trace.md
- next_action: Build the bounded execution helper on top of the dispatch surface, then make authority handling and open-question routing operational.
- note: Completed by Codex under the explicit CODEX__CODE binding; this does not imply independent support-role review.
