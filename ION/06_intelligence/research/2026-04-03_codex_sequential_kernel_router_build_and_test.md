---
type: research
from: Codex
created: 2026-04-03T17:34:38-04:00
status: COMPLETE
topic: Sequential kernel router build and test
connections:
  - ION/04_packages/kernel/sequential_kernel.py
  - ION/04_packages/kernel/__init__.py
  - ION/04_packages/kernel/__main__.py
  - ION/tests/test_sequential_kernel.py
  - ION/06_intelligence/research/2026-04-03_codex_sequential_kernel_governance_trace.md
  - ION/06_intelligence/research/2026-04-03_codex_sequential_kernel_implementation_trace.md
---

# Codex Sequential Kernel Router Build and Test

## Why this exists

The active root already declared a low-burn sequential kernel posture, but until now
that posture was mostly doctrine and manual practice. This note records the first
real package-level implementation and the current proof boundary.

## Sources or surfaces considered

- `ION/04_packages/kernel/sequential_kernel.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/04_packages/kernel/__main__.py`
- `ION/tests/test_sequential_kernel.py`
- `ION/03_registry/boots/CODEX.boot.md`
- `ION/01_doctrine/SOVEREIGN_CONSTITUTION.md`
- `ION/01_doctrine/SOVEREIGN_KERNEL.md`
- `ION/06_intelligence/research/2026-04-03_codex_sequential_kernel_governance_trace.md`
- `ION/06_intelligence/research/2026-04-03_codex_sequential_kernel_implementation_trace.md`

## Findings

- `SequentialKernelRouter` now models the active low-burn role field directly:
  `governance`, `implementation`, `research`, `archaeology`, and `relay`
  workstreams are defined with explicit ordered role passes and per-role load
  surfaces.
- The router encodes current continuity law instead of the older shared-surface
  assumption: private agent continuity loads before root projections, and the
  lane-native Relay/Vestige roles load lane continuity before root projections.
- The kernel package now has two clean entrypoints:
  `python -m kernel.sequential_kernel ...` and `python -m kernel ...`.
  The earlier `runpy` warning is removed by making the package exports lazy.
- The CLI can now externalize a rendered trace to disk with `--output`.
  Two concrete traces were generated:
  `2026-04-03_codex_sequential_kernel_governance_trace.md` and
  `2026-04-03_codex_sequential_kernel_implementation_trace.md`.
- The current automated proof is stronger than a smoke test but still bounded.
  Ten tests now verify:
  runtime-surface presence, source-before-projection load order, all five
  workstream sequences, directive propagation, clean module entry, package entry,
  and trace artifact writing.
- This is still a routing-and-inspection kernel, not a full role-execution kernel.
  It does not yet perform automatic per-pass prompt transformation, packet claim
  mutation, or writeback closure on its own.

## Implications

- ION now has a real, inspectable sequential-kernel substrate rather than only a
  doctrinal claim that Codex can route across roles under budget pressure.
- The current kernel is good enough to validate whether the active root has the
  minimum surfaces needed for a bounded multi-role pass before spending more work.
- The next threshold is no longer "can we describe the kernel?"
  It is "can one trace drive one real end-to-end packet cycle with visible
  pass-by-pass outputs?"

## Recommended next moves

- Build a trace executor that takes one trace and writes per-pass session notes or
  handoff packets to disk.
- Run one real inbox-scoped task through that executor instead of only rendering
  the role chain.
- Keep the low-burn default posture until that first trace-driven cycle proves
  stable enough to justify more automation or more parallel staffing.
