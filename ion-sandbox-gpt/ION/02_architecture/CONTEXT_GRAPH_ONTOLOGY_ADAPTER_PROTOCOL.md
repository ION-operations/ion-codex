# CONTEXT GRAPH ONTOLOGY ADAPTER PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Workstream:** WS-03 — Context Graph Ontology Adapter  
**Purpose:** Define how the restored Living Context Graph ontology maps to the existing kernel `model.py`, `store.py`, `index.py`, and `graph.py` without falsely claiming that the existing kernel graph already exhausts the whole substrate.

---

## 1. Core distinction

```text
Living Context Graph = full substrate of meaning, memory, law, agents, templates, files, receipts, packets, registries, doctrine, runtime state, and recovery lineage.

Kernel graph.py = enacted runtime/causal projection over persisted kernel records.
```

The kernel graph is real and important. It is not the entire graph substrate.

---

## 2. Adapter rule

```text
Do not rewrite graph.py first.
Create an adapter/report layer mapping living-context-graph ontology to existing kernel records, existing graph edges, semantic-only surfaces, and future adapter requirements.
```

This prevents two failures:

1. **graph.py inflation** — pretending the current kernel graph already covers doctrine, templates, agents, donor lineage, approved context, and product surfaces.
2. **graph.py bypass** — inventing a parallel graph system that ignores the tested kernel store/index/graph machinery.

---

## 3. Mapping classes

Every proposed living-context node/edge/region must be assigned one mapping class.

```text
ENACTED_KERNEL_RECORD
ENACTED_KERNEL_EDGE
ENACTED_FILE_SURFACE
ENACTED_REGISTRY_SURFACE
ENACTED_TEMPLATE_SURFACE
ENACTED_EVENTED_GRAPH_STATE
SEMANTIC_ONLY_CURRENTLY
PROJECTION_ONLY
ADAPTER_REQUIRED
CONFLICT_REQUIRES_REVIEW
UNKNOWN
```

---

## 4. Node-class seed

The initial living-context node classes are:

```text
node.file.template_instantiated
node.template
node.agent.role
node.carrier
node.packet
node.work_unit
node.context_package
node.receipt
node.registry_entry
node.semantic_identity
node.contradiction
node.settlement
node.horizon
node.user_interaction
node.archive_capsule
node.graph_commit
node.graph_writeback_proposal
node.template_completion_event
node.approved_context_entry
node.ion_file_record
node.system_card
```

---

## 5. Edge-class seed

```text
edge.depends_on
edge.instantiates
edge.belongs_to_region
edge.owned_by_role
edge.operated_by
edge.emits
edge.proves
edge.mutates
edge.blocks
edge.routes_to
edge.derives_from
edge.contradicts
edge.supersedes
edge.preserved_as_lineage
edge.continues
edge.settles
edge.triggers_candidate_event
edge.triggers_allowed_reaction
edge.indexes
edge.packages
edge.approves_context
edge.classifies_file
```

---

## 6. Region seed

```text
region.front_door
region.semantic_identity
region.template_law
region.kernel_runtime
region.evented_file_graph
region.self_documenting_context
region.recovery_reconstitution
region.product_surface
region.project_build
region.doctrine_evolution
```

---

## 7. Comparison report requirement

Before promoting ontology claims, ION must maintain a comparison report:

```text
ION/06_intelligence/orchestration/context_graph_restoration/graph_py_comparison_report.md
```

The report must show:

```text
existing kernel record families
existing graph edge families
proposed node classes already enacted
proposed node classes semantic-only
proposed node classes requiring adapter work
edge classes already enacted
edge classes requiring adapter work
terminology conflicts
recommendations
```

---

## 8. Adapter implementation requirements

The first adapter implementation may be read-only.

Minimum functions:

```text
list_living_node_class_mappings()
list_living_edge_class_mappings()
list_living_region_mappings()
classify_node_class(node_class)
classify_edge_class(edge_class)
produce_comparison_report_data()
```

It must not mutate graph truth.

---

## 9. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. kernel `graph.py` to be renamed as the entire living context graph;
2. living-context graph doctrine to ignore enacted kernel records;
3. semantic-only node classes to be described as fully implemented;
4. adapter-required surfaces to be hidden;
5. parallel graph state to bypass kernel truth without review;
6. index projections to impersonate graph canon;
7. evented-template graph commits to mutate unrelated source surfaces silently.

---

## 10. Minimal test guards

```text
test_context_graph_adapter_protocol_exists
test_node_class_registry_exists
test_edge_class_registry_exists
test_region_registry_exists
test_adapter_classifies_work_unit_as_kernel_record
test_adapter_classifies_template_completion_event_as_evented_graph_surface
test_adapter_marks_user_interaction_adapter_required
test_comparison_report_exists
```
