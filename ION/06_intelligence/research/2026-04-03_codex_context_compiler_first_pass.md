---
type: research
from: Codex
created: 2026-04-03T18:55:00-04:00
status: COMPLETE
topic: First lawful context compiler helper
connections:
  - ION/04_packages/kernel/context_compiler.py
  - ION/04_packages/kernel/model.py
  - ION/04_packages/kernel/store.py
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/graph.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_context_compiler.py
  - ION/05_context/inbox/completed/codex_context_compiler_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_context_compiler_first_pass/00_trace.md
  - SOS-OPUS/04_packages/cognitive/src/context_compiler.py
---

# Codex Context Compiler First Pass

## Why this exists

The kernel now had typed records, durable persistence, indexed lookup, and a causal
graph, but still no explicit helper that turns those bounded inputs into a real
`ContextPackage`. This pass adds that first compiler surface.

## Sources or surfaces considered

- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/graph.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_context_compiler.py`
- `SOS-OPUS/04_packages/cognitive/src/context_compiler.py`

## Findings

- `ION/04_packages/kernel/context_compiler.py` now provides a bounded, deterministic
  compiler helper for producing real `ContextPackage` objects from a `WorkUnit` plus
  explicit doctrine, target, mission, semantic, and dependency inputs.
- The helper implements the current spec's drop order:
  tier 5 dependencies first, then tier 4 semantic items, then mission payload, while
  preserving doctrine and target.
- The helper computes deterministic `context_version` hashes from the compiled package
  content rather than from `compiled_at`.
- The convenience entrypoint `compile_context_package_for_work_unit(...)` uses the
  current `KernelIndex` and `KernelGraph` to resolve related open-question texts for a
  work unit without reading arbitrary filesystem state.
- The helper is intentionally explicit:
  it does not claim that the full daemon compiler pipeline or automatic file loading
  already exists.
- The package exports now include:
  `ContextCompileRequest`, `ContextCompilerError`, `compile_context_package`,
  `compile_context_package_for_work_unit`, and `render_context_package_text`.
- `ION/tests/test_context_compiler.py` proves:
  deterministic compilation for the same request,
  spec-order dropping under budget pressure,
  and stack-assisted open-question resolution.
- The combined kernel suite is now at forty passing tests.

## Important boundary

- If doctrine plus target plus required binding metadata alone exceed the requested
  token budget, the compiler will still return a valid package whose `actual_tokens`
  remain above budget after all legal drops are exhausted. That is the correct first-pass
  behavior because doctrine and target are not droppable.

## Implications

- The kernel now has a five-layer floor:
  typed records, durable store, fast index, causal graph, and explicit context
  compilation.
- The next runtime-facing slice can build on actual compiled packages rather than on
  implied manual loading rules alone.

## Recommended next moves

- Implement the next narrow runtime helper that consumes compiled packages, likely a
  scheduler or dispatch-side helper rather than a full daemon at once.
- Keep the compiler explicit and input-driven until the daemon owns source loading
  lawfully.
