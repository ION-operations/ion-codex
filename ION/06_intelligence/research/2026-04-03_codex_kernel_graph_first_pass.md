---
type: research
from: Codex
created: 2026-04-03T18:40:00-04:00
status: COMPLETE
topic: First lawful kernel graph slice
connections:
  - ION/04_packages/kernel/graph.py
  - ION/04_packages/kernel/index.py
  - ION/04_packages/kernel/__init__.py
  - ION/tests/test_kernel_graph.py
  - ION/05_context/inbox/completed/codex_kernel_graph_first_pass_2026-04-03.task.md
  - ION/05_context/comms/kernel_router_runs/2026-04-03_codex_kernel_graph_first_pass/00_trace.md
  - SOS-OPUS/04_packages/ion_kernel/graph.py
---

# Codex Kernel Graph First Pass

## Why this exists

The kernel now had typed records, durable persistence, and indexed lookup, but not yet
an explicit traversal layer for the causal relationships already present in those
records. This pass adds the first bounded graph over that stack.

## Sources or surfaces considered

- `ION/04_packages/kernel/model.py`
- `ION/04_packages/kernel/store.py`
- `ION/04_packages/kernel/index.py`
- `ION/04_packages/kernel/__init__.py`
- `ION/tests/test_kernel_graph.py`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_store_first_pass.md`
- `ION/06_intelligence/research/2026-04-03_codex_kernel_index_first_pass.md`
- `SOS-OPUS/04_packages/ion_kernel/graph.py`

## Findings

- `ION/04_packages/kernel/graph.py` now provides a first-pass causal graph for the
  active kernel records rather than the older broad semantic bond system.
- The graph currently models the explicit relations already present in the first-pass
  record stack:
  `CONTEXT_FOR`, `ENABLES_WORK`, `SPAWNS_CHILD`, `EMITS_DELTA`,
  `CONTEXT_FOR_DELTA`, `RAISES_QUESTION`, `PARENT_QUESTION_FOR`, and
  `BLOCKS_WORK`.
- The graph builds from `KernelIndex`, keeps forward and reverse adjacency,
  supports shortest-path traversal, reachability, topological sort, cycle check, and
  connected-component analysis.
- Public predecessor and neighbor views are node-unique even when multiple edge types
  connect the same pair.
- `ION/04_packages/kernel/__init__.py` now exports `KernelGraph`, `GraphEdge`,
  `GraphEdgeType`, and `IonGraph` as the first-pass compatibility alias.
- `ION/tests/test_kernel_graph.py` proves graph build, causal path resolution,
  dependency/blocking visibility, topological ordering, and component analysis. The
  combined kernel suite is now at thirty-seven passing tests.

## Boundary

- This is not the full legacy semantic bond graph.
- It only encodes explicit causal/runtime relations derivable from the current record
  families.
- It does not yet model broader artifact-to-artifact ontology, policy edges, or daemon
  execution semantics beyond those explicit links.

## Implications

- The kernel now has a four-layer floor:
  typed records, durable store, fast index, and causal graph.
- The next slice can consume an actual traversable runtime topology instead of ad hoc
  joins.

## Recommended next moves

- Build a minimal compiler helper on top of the typed/store/index/graph stack.
- Delay any broader semantic bond resurrection until doctrine and runtime need it
  explicitly.
