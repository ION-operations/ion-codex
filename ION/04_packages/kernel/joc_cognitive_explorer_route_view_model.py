"""V58 ION/JOC Cognitive Explorer and Infinite Context route view-model verifier.

This module validates a UI-facing view model for the ION/JOC Cognitive Explorer:
query -> deterministic route -> selected graph nodes -> structural blueprint ->
dependency web -> context injection preview.

It is deliberately non-executing. It does not dispatch prompts, call external
models, read credentials, mutate browser sessions, rewrite source summaries,
or grant production authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.joc_cognitive_explorer_route_view_model.v1"
VERSION = "V58_COGNITIVE_EXPLORER_AND_CONTEXT_ROUTE_VIEW_MODEL"
AUTHORITY_SCOPE = "COGNITIVE_EXPLORER_ROUTE_VIEW_MODEL_RECEIPT_ONLY"
DEFAULT_REPORT_DIR = "ION/05_context/history/joc_cognitive_explorer_route_view_model_receipts"

REQUIRED_VIEW_SURFACES = (
    "COGNITIVE_EXPLORER",
    "INFINITE_CONTEXT_COMMAND_PALETTE",
    "SELECTED_CONTEXT_LENS",
    "STRUCTURAL_BLUEPRINT_VIEW",
    "DEPENDENCY_WEB_VIEW",
    "SOURCE_LINE_CITATION_RAIL",
    "ROUTE_REASONING_PANEL",
)

REQUIRED_ROUTE_CLASSES = (
    "EXACT_SYMBOL",
    "FILE_PATH",
    "DEPENDENCY_EDGE",
    "RECEIPT_FAMILY",
    "FALLBACK_BOUNDARY",
)

ALLOWED_NODE_CLASSES = (
    "FILE",
    "CLASS",
    "FUNCTION",
    "PROTOCOL",
    "REGISTRY",
    "RECEIPT",
    "TEST",
    "UI_COMPONENT",
)

ALLOWED_ROUTE_VERDICTS = (
    "VALID_CONTEXT_ROUTE_VIEW_MODEL",
    "BLOCKED_EMPTY_QUERY",
    "BLOCKED_NO_SELECTED_NODES",
    "BLOCKED_MISSING_SURFACE",
    "BLOCKED_MISSING_ROUTE_CLASS",
    "BLOCKED_UNCITED_CONTEXT",
    "BLOCKED_FORBIDDEN_CAPABILITY",
)

FORBIDDEN_CAPABILITIES = {
    "production_authority": False,
    "external_model_dispatch": False,
    "browser_session_mutation": False,
    "credential_access": False,
    "source_summary_rewrite": False,
    "canonical_graph_write": False,
    "unrestricted_agent_activation": False,
    "live_ui_claim": False,
}


@dataclass(frozen=True)
class ExplorerNode:
    node_id: str
    label: str
    node_class: str
    path: str
    symbol: str = ""
    line_range: str = ""
    confidence: str = "SOURCE_INDEXED"


@dataclass(frozen=True)
class DependencyEdge:
    source: str
    target: str
    edge_class: str
    evidence_ref: str


@dataclass(frozen=True)
class ContextRouteCandidate:
    query: str
    route_classes: tuple[str, ...]
    selected_nodes: tuple[ExplorerNode, ...]
    dependency_edges: tuple[DependencyEdge, ...]
    view_surfaces: tuple[str, ...]
    source_citations: tuple[str, ...]
    route_reasoning: str
    injection_preview: str
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_CAPABILITIES.copy())


@dataclass(frozen=True)
class CognitiveExplorerReceipt:
    version: str
    schema_id: str
    receipt_id: str
    generated_at: str
    authority_scope: str
    route_verdict: str
    query: str
    selected_node_count: int
    dependency_edge_count: int
    route_class_count: int
    view_surface_count: int
    citation_count: int
    selected_nodes: tuple[Mapping[str, Any], ...]
    dependency_edges: tuple[Mapping[str, Any], ...]
    route_classes: tuple[str, ...]
    view_surfaces: tuple[str, ...]
    source_citations: tuple[str, ...]
    route_reasoning: str
    injection_preview: str
    findings: tuple[str, ...]
    forbidden_capabilities: Mapping[str, bool]
    production_authority: bool = False
    live_ui_claim: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _hash_payload(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:24]


def _validate_forbidden(candidate: ContextRouteCandidate) -> tuple[str, ...]:
    findings: list[str] = []
    for key, expected in FORBIDDEN_CAPABILITIES.items():
        actual = candidate.blocked_capabilities.get(key)
        if actual is not expected:
            findings.append(f"forbidden capability {key!r} expected {expected!r} got {actual!r}")
    for key, value in candidate.blocked_capabilities.items():
        if value is not False:
            findings.append(f"capability {key!r} is not blocked")
    return tuple(findings)


def validate_cognitive_explorer_route(candidate: ContextRouteCandidate) -> CognitiveExplorerReceipt:
    findings: list[str] = []
    route_verdict = "VALID_CONTEXT_ROUTE_VIEW_MODEL"

    if not candidate.query.strip():
        findings.append("query is empty")
        route_verdict = "BLOCKED_EMPTY_QUERY"

    if not candidate.selected_nodes:
        findings.append("no selected graph nodes are present")
        route_verdict = "BLOCKED_NO_SELECTED_NODES"

    missing_surfaces = [surface for surface in REQUIRED_VIEW_SURFACES if surface not in candidate.view_surfaces]
    if missing_surfaces:
        findings.append("missing required view surfaces: " + ", ".join(missing_surfaces))
        route_verdict = "BLOCKED_MISSING_SURFACE"

    missing_route_classes = [route_class for route_class in REQUIRED_ROUTE_CLASSES if route_class not in candidate.route_classes]
    if missing_route_classes:
        findings.append("missing required route classes: " + ", ".join(missing_route_classes))
        route_verdict = "BLOCKED_MISSING_ROUTE_CLASS"

    for node in candidate.selected_nodes:
        if node.node_class not in ALLOWED_NODE_CLASSES:
            findings.append(f"node {node.node_id!r} has invalid node class {node.node_class!r}")
        if not node.path:
            findings.append(f"node {node.node_id!r} has no path")
        if not node.line_range:
            findings.append(f"node {node.node_id!r} has no line_range")

    cited_paths = set()
    for citation in candidate.source_citations:
        if ":" in citation:
            cited_paths.add(citation.split(":", 1)[0])
    uncited = [node.path for node in candidate.selected_nodes if node.path not in cited_paths]
    if uncited:
        findings.append("selected nodes missing source citations: " + ", ".join(sorted(set(uncited))))
        route_verdict = "BLOCKED_UNCITED_CONTEXT"

    if candidate.dependency_edges and not any(route_class == "DEPENDENCY_EDGE" for route_class in candidate.route_classes):
        findings.append("dependency edges exist without DEPENDENCY_EDGE route class")
        route_verdict = "BLOCKED_MISSING_ROUTE_CLASS"

    forbidden_findings = _validate_forbidden(candidate)
    if forbidden_findings:
        findings.extend(forbidden_findings)
        route_verdict = "BLOCKED_FORBIDDEN_CAPABILITY"

    if not candidate.route_reasoning.strip():
        findings.append("route reasoning is empty")
    if not candidate.injection_preview.strip():
        findings.append("injection preview is empty")

    payload_for_id = {
        "query": candidate.query,
        "route_classes": list(candidate.route_classes),
        "selected_nodes": [asdict(node) for node in candidate.selected_nodes],
        "dependency_edges": [asdict(edge) for edge in candidate.dependency_edges],
        "view_surfaces": list(candidate.view_surfaces),
        "source_citations": list(candidate.source_citations),
        "findings": findings,
    }

    return CognitiveExplorerReceipt(
        version=VERSION,
        schema_id=SCHEMA_ID,
        receipt_id=_hash_payload(payload_for_id),
        generated_at=datetime.now(timezone.utc).isoformat(),
        authority_scope=AUTHORITY_SCOPE,
        route_verdict=route_verdict,
        query=candidate.query,
        selected_node_count=len(candidate.selected_nodes),
        dependency_edge_count=len(candidate.dependency_edges),
        route_class_count=len(set(candidate.route_classes)),
        view_surface_count=len(set(candidate.view_surfaces)),
        citation_count=len(candidate.source_citations),
        selected_nodes=tuple(asdict(node) for node in candidate.selected_nodes),
        dependency_edges=tuple(asdict(edge) for edge in candidate.dependency_edges),
        route_classes=tuple(candidate.route_classes),
        view_surfaces=tuple(candidate.view_surfaces),
        source_citations=tuple(candidate.source_citations),
        route_reasoning=candidate.route_reasoning,
        injection_preview=candidate.injection_preview,
        findings=tuple(findings),
        forbidden_capabilities=dict(candidate.blocked_capabilities),
        production_authority=False,
        live_ui_claim=False,
    )


def build_demo_candidate() -> ContextRouteCandidate:
    nodes = (
        ExplorerNode(
            node_id="node.kernel.joc_reactive_os_stream_view_model",
            label="Reactive OS Stream verifier",
            node_class="FUNCTION",
            path="ION/04_packages/kernel/joc_reactive_os_stream_view_model.py",
            symbol="validate_reactive_os_stream_view_model",
            line_range="L1-L220",
        ),
        ExplorerNode(
            node_id="node.ui.ReactiveOsStreamPanel",
            label="Reactive OS Stream panel",
            node_class="UI_COMPONENT",
            path="ION/08_ui/joc_cockpit_shell/ReactiveOsStreamPanel.tsx",
            symbol="ReactiveOsStreamPanel",
            line_range="L1-L80",
        ),
        ExplorerNode(
            node_id="node.ui.AutomationOverlayPanel",
            label="Browser automation overlay panel",
            node_class="UI_COMPONENT",
            path="ION/08_ui/joc_cockpit_shell/AutomationOverlayPanel.tsx",
            symbol="AutomationOverlayPanel",
            line_range="L1-L90",
        ),
        ExplorerNode(
            node_id="node.protocol.reactive_os_stream",
            label="Reactive OS stream protocol",
            node_class="PROTOCOL",
            path="ION/02_architecture/ION_JOC_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL_PROTOCOL.md",
            symbol="V57 protocol",
            line_range="L1-L140",
        ),
    )
    edges = (
        DependencyEdge(
            source="node.kernel.joc_reactive_os_stream_view_model",
            target="node.ui.ReactiveOsStreamPanel",
            edge_class="projects_to",
            evidence_ref="V57 stream fixture",
        ),
        DependencyEdge(
            source="node.ui.AutomationOverlayPanel",
            target="node.protocol.reactive_os_stream",
            edge_class="conforms_to",
            evidence_ref="V57 protocol required surfaces",
        ),
    )
    return ContextRouteCandidate(
        query="Explain the reactive OS stream and automation overlay path.",
        route_classes=REQUIRED_ROUTE_CLASSES,
        selected_nodes=nodes,
        dependency_edges=edges,
        view_surfaces=REQUIRED_VIEW_SURFACES,
        source_citations=tuple(f"{node.path}:{node.line_range}" for node in nodes),
        route_reasoning=(
            "Exact indexed symbols for the V57 stream verifier and cockpit panels satisfy the query before any "
            "semantic fallback. Dependency edges show how kernel receipts project into UI components."
        ),
        injection_preview=(
            "Context route preview: include V57 stream verifier, ReactiveOsStreamPanel, AutomationOverlayPanel, "
            "and protocol lines. Dispatch is not executed in V58."
        ),
    )


def write_receipt(receipt: CognitiveExplorerReceipt, workspace_root: Path | str = ".") -> Path:
    root = Path(workspace_root)
    report_dir = root / DEFAULT_REPORT_DIR
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{receipt.receipt_id}.joc_cognitive_explorer_route_view_model_receipt.json"
    path.write_text(json.dumps(receipt.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate V58 ION/JOC Cognitive Explorer route view model.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    receipt = validate_cognitive_explorer_route(build_demo_candidate())
    print(json.dumps(receipt.to_dict(), indent=2, sort_keys=True))
    if args.write:
        path = write_receipt(receipt, args.workspace_root)
        print(f"receipt_written={path}")
    return 0 if receipt.route_verdict == "VALID_CONTEXT_ROUTE_VIEW_MODEL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
