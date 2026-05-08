"""Living Context Graph ontology adapter.

This module is intentionally read-only in V13. It maps restored living-context
graph node/edge/region classes onto existing kernel records, evented graph state,
registries, templates, file surfaces, or future adapter requirements.

It does not mutate kernel graph truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


ENACTED_KERNEL_RECORD = "ENACTED_KERNEL_RECORD"
ENACTED_KERNEL_EDGE = "ENACTED_KERNEL_EDGE"
ENACTED_FILE_SURFACE = "ENACTED_FILE_SURFACE"
ENACTED_REGISTRY_SURFACE = "ENACTED_REGISTRY_SURFACE"
ENACTED_TEMPLATE_SURFACE = "ENACTED_TEMPLATE_SURFACE"
ENACTED_EVENTED_GRAPH_STATE = "ENACTED_EVENTED_GRAPH_STATE"
SEMANTIC_ONLY_CURRENTLY = "SEMANTIC_ONLY_CURRENTLY"
PROJECTION_ONLY = "PROJECTION_ONLY"
ADAPTER_REQUIRED = "ADAPTER_REQUIRED"
CONFLICT_REQUIRES_REVIEW = "CONFLICT_REQUIRES_REVIEW"
UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class OntologyMapping:
    item_id: str
    mapping_class: str
    enacted_by: tuple[str, ...] = ()
    notes: str = ""


NODE_CLASS_MAPPINGS: Dict[str, OntologyMapping] = {
    "node.work_unit": OntologyMapping("node.work_unit", ENACTED_KERNEL_RECORD, ("model.py",), "Kernel WorkUnit record family."),
    "node.context_package": OntologyMapping("node.context_package", ENACTED_KERNEL_RECORD, ("model.py",), "Kernel ContextPackage record family."),
    "node.receipt": OntologyMapping("node.receipt", ENACTED_KERNEL_RECORD, ("model.py", "05_context/history/"), "Receipt records and history receipts."),
    "node.horizon": OntologyMapping("node.horizon", ENACTED_KERNEL_RECORD, ("horizon_state.py",), "Kernel horizon state."),
    "node.packet": OntologyMapping("node.packet", ENACTED_FILE_SURFACE, ("05_context/inbox/", "07_templates/"), "Packet file surfaces."),
    "node.template": OntologyMapping("node.template", ENACTED_TEMPLATE_SURFACE, ("07_templates/",), "Template surfaces."),
    "node.registry_entry": OntologyMapping("node.registry_entry", ENACTED_REGISTRY_SURFACE, ("03_registry/",), "Registry entries."),
    "node.semantic_identity": OntologyMapping("node.semantic_identity", ENACTED_REGISTRY_SURFACE, ("03_registry/semantic_identities/",), "Semantic identity surfaces."),
    "node.template_completion_event": OntologyMapping("node.template_completion_event", ENACTED_EVENTED_GRAPH_STATE, ("template_completion_events.py",), "V10 event witness."),
    "node.graph_writeback_proposal": OntologyMapping("node.graph_writeback_proposal", ENACTED_EVENTED_GRAPH_STATE, ("template_graph_writeback_proposals.py",), "V10 graph writeback proposal."),
    "node.graph_commit": OntologyMapping("node.graph_commit", ENACTED_EVENTED_GRAPH_STATE, ("template_graph_commit.py",), "V10 bounded graph commit."),
    "node.approved_context_entry": OntologyMapping("node.approved_context_entry", ENACTED_REGISTRY_SURFACE, ("approved_context_index.yaml",), "V12 approved context entry."),
    "node.ion_file_record": OntologyMapping("node.ion_file_record", ENACTED_TEMPLATE_SURFACE, ("ION_FILE_RECORD.md", "ion_file_record_schema.yaml"), "V12 file-record schema/template."),
    "node.system_card": OntologyMapping("node.system_card", ENACTED_TEMPLATE_SURFACE, ("SYSTEM_CARD.md", "system_card_registry.yaml"), "V12 system card seed."),
    "node.agent.role": OntologyMapping("node.agent.role", ENACTED_REGISTRY_SURFACE, ("03_registry/", "agents/"), "Role surfaces exist; jurisdiction lattice needs hardening."),
    "node.archive_capsule": OntologyMapping("node.archive_capsule", ENACTED_FILE_SURFACE, ("*.zip",), "Archive capsule file artifacts."),
    "node.user_interaction": OntologyMapping("node.user_interaction", ADAPTER_REQUIRED, (), "Front-door runtime not yet implemented."),
}

EDGE_CLASS_MAPPINGS: Dict[str, OntologyMapping] = {
    "edge.emits": OntologyMapping("edge.emits", ENACTED_KERNEL_EDGE, ("EMITS_DELTA",), "Existing kernel emitted-delta edge semantics."),
    "edge.blocks": OntologyMapping("edge.blocks", ENACTED_KERNEL_EDGE, ("BLOCKS_WORK",), "Existing kernel blocking edge semantics."),
    "edge.answers": OntologyMapping("edge.answers", ENACTED_KERNEL_EDGE, ("ANSWERS_QUESTION",), "Existing kernel question-answer edge semantics."),
    "edge.instantiates": OntologyMapping("edge.instantiates", ADAPTER_REQUIRED, (), "Template/file instantiation needs explicit adapter edge."),
    "edge.proves": OntologyMapping("edge.proves", ADAPTER_REQUIRED, (), "Receipt proof relation needs explicit adapter edge."),
    "edge.mutates": OntologyMapping("edge.mutates", ADAPTER_REQUIRED, (), "Mutation relation needs adapter over governed writes and V10 commits."),
    "edge.routes_to": OntologyMapping("edge.routes_to", SEMANTIC_ONLY_CURRENTLY, (), "Routing exists in packet/protocol form, not unified graph edge yet."),
    "edge.triggers_candidate_event": OntologyMapping("edge.triggers_candidate_event", ENACTED_EVENTED_GRAPH_STATE, ("template_completion_events.py",), "V10 completion event path."),
    "edge.triggers_allowed_reaction": OntologyMapping("edge.triggers_allowed_reaction", ENACTED_EVENTED_GRAPH_STATE, ("template_reaction_selection.py",), "V10 reaction selection path."),
    "edge.approves_context": OntologyMapping("edge.approves_context", ENACTED_REGISTRY_SURFACE, ("approved_context_index.yaml",), "V12 approved context projection."),
    "edge.classifies_file": OntologyMapping("edge.classifies_file", ENACTED_TEMPLATE_SURFACE, ("ION_FILE_RECORD.md",), "V12 file record template."),
}

REGION_MAPPINGS: Dict[str, OntologyMapping] = {
    "region.kernel_runtime": OntologyMapping("region.kernel_runtime", ENACTED_KERNEL_RECORD, ("04_packages/kernel/",), "Kernel runtime region."),
    "region.evented_file_graph": OntologyMapping("region.evented_file_graph", ENACTED_EVENTED_GRAPH_STATE, ("template_*",), "V10 evented graph runtime region."),
    "region.self_documenting_context": OntologyMapping("region.self_documenting_context", ENACTED_REGISTRY_SURFACE, ("approved_context_index.yaml",), "V12 approved-context region."),
    "region.doctrine_evolution": OntologyMapping("region.doctrine_evolution", ENACTED_REGISTRY_SURFACE, ("doctrine_evolution_registry.yaml",), "V11 doctrine governance region."),
    "region.front_door": OntologyMapping("region.front_door", ADAPTER_REQUIRED, (), "Front-door runtime not yet implemented."),
    "region.semantic_identity": OntologyMapping("region.semantic_identity", ENACTED_REGISTRY_SURFACE, ("03_registry/semantic_identities/",), "Semantic identity region."),
    "region.template_law": OntologyMapping("region.template_law", ENACTED_TEMPLATE_SURFACE, ("07_templates/",), "Template law region."),
    "region.recovery_reconstitution": OntologyMapping("region.recovery_reconstitution", ENACTED_FILE_SURFACE, ("06_intelligence/orchestration/",), "Recovery/reconstitution surfaces."),
}


def classify_node_class(node_class: str) -> str:
    return NODE_CLASS_MAPPINGS.get(node_class, OntologyMapping(node_class, UNKNOWN)).mapping_class


def classify_edge_class(edge_class: str) -> str:
    return EDGE_CLASS_MAPPINGS.get(edge_class, OntologyMapping(edge_class, UNKNOWN)).mapping_class


def classify_region(region: str) -> str:
    return REGION_MAPPINGS.get(region, OntologyMapping(region, UNKNOWN)).mapping_class


def list_living_node_class_mappings() -> List[OntologyMapping]:
    return list(NODE_CLASS_MAPPINGS.values())


def list_living_edge_class_mappings() -> List[OntologyMapping]:
    return list(EDGE_CLASS_MAPPINGS.values())


def list_living_region_mappings() -> List[OntologyMapping]:
    return list(REGION_MAPPINGS.values())


def produce_comparison_report_data() -> dict:
    return {
        "node_classes": {key: value.mapping_class for key, value in NODE_CLASS_MAPPINGS.items()},
        "edge_classes": {key: value.mapping_class for key, value in EDGE_CLASS_MAPPINGS.items()},
        "regions": {key: value.mapping_class for key, value in REGION_MAPPINGS.items()},
        "mutation_allowed": False,
        "adapter_phase": "V13_READ_ONLY_MAPPING",
    }
