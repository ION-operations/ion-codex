---
type: research
from: Codex
created: 2026-04-03T20:36:37-04:00
status: COMPLETE
topic: First-pass sequential runtime portability cut
connections:
  - ION/04_packages/kernel/sequential_kernel.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_sequential_kernel.py
  - ION/05_context/inbox/codex_sequential_runtime_portability_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_sequential_runtime_portability_first_pass/00_trace.md
  - ION/06_intelligence/research/2026-04-03_codex_response_to_external_canonicalization_memo.md
  - ION/07_templates/bindings/CODEX__CODE.md
---

# Codex Sequential Runtime Portability First Pass

## Why this exists

The external canonicalization review was correct that the current root still had live
production-root coupling inside the sequential runtime layer.

That coupling was not only conceptual. It was visible in:

- `ION/04_packages/kernel/sequential_kernel.py`
- `ION/tests/test_sequential_kernel.py`

So this pass removes the first explicit machine/path assumptions from the live runtime
shell without pretending the whole runtime/environment separation is finished.

## Sources or surfaces considered

- `ION/04_packages/kernel/sequential_kernel.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_sequential_kernel.py`
- `ION/06_intelligence/research/2026-04-03_codex_response_to_external_canonicalization_memo.md`
- `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/bindings/CODEX__CODE.md`

## Findings

- `ION/04_packages/kernel/sequential_kernel.py` now resolves the default repo root from
  discoverable local structure with `default_repo_root()` instead of a hardcoded
  `/home/sev/ION - Production` literal.
- The Atlas reference root in the runtime role map is now repo-relative
  (`ATLAS/README.md`) rather than a machine-specific absolute path.
- The CLI no longer hardcodes a production-root default. If `--repo-root` is omitted,
  it now discovers the local active root.
- `ION/04_packages/kernel/__init__.py` now exports `default_repo_root` through the lazy
  kernel package.
- `ION/tests/test_sequential_kernel.py` now derives `REPO_ROOT` from its own file
  location rather than a fixed machine path.
- The sequential-runtime tests now also prove:
  default repo-root discovery works and Atlas reference binding is repo-relative.
- There are now **no hardcoded `ION - Production` literals left in live kernel/test
  Python** under:
  `ION/04_packages/` and `ION/tests/`.
- The combined kernel suite is now at **55 passing tests**.

## Boundary

- This does not complete the full kernel/runtime/environment split.
- It does not remove production-shape assumptions from documentation or broader
  architecture notes.
- It does not change the active runtime law; it only removes the clearest machine-local
  assumptions from the live sequential shell and its tests.

## Implications

- One of the most concrete canonicalization blockers is now materially reduced.
- The sequential runtime shell is more honestly portable without changing its current
  active behavior.
- The next runtime work can now focus less on obvious environment coupling and more on
  completing the actual daemon-facing loop.

## Recommended next moves

- Build the bounded execution helper on top of the dispatch surface.
- After that, make authority-aware commit handling and open-question routing
  operational.
