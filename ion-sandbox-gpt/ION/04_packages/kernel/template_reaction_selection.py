"""Dry-run reaction selection for Template Completion Event witnesses.

This module implements Phase 2 of the Evented Template File Graph law. It reads
Phase 1 Template Completion Event witnesses, selects allowed downstream reaction
families from declared template/file metadata, and emits durable dry-run reaction
selection witnesses.

It intentionally does not mutate source files, graph state, registries,
schedules, indexes, or agent activation state. Phase 2 proves that reaction
routing can be selected lawfully before any graph writeback is permitted.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .contract_bound_event_runtime import gate_reaction_selection_by_contract
from .template_contract_registry import load_contracts_if_projection_exists


class KernelTemplateReactionSelectionError(Exception):
    """Raised when dry-run reaction selection cannot proceed."""


@dataclass(frozen=True)
class GraphReactionFamily:
    """A dry-run selectable downstream reaction family."""

    family_id: str
    reaction_class: str
    required_authority: str
    receipt_type: str
    dry_run_allowed: bool = True
    phase2_allowed_effects: tuple[str, ...] = ("dry_run_selection_witness",)


@dataclass(frozen=True)
class TemplateReactionSelection:
    """One dry-run selected reaction for a Template Completion Event."""

    event_id: str
    source_path: str
    requested_effect: str
    reaction_family: str
    reaction_class: str
    required_authority: str
    status: str
    dry_run_only: bool
    contract_bound: bool = False
    contract_blocked_reason: str = ""
    refusal_reason: str = ""


@dataclass(frozen=True)
class TemplateReactionSelectionWitness:
    """Durable witness for one event's dry-run reaction selection."""

    selection_id: str
    event_id: str
    event_type: str
    source_path: str
    emitted_at: str
    phase: str
    dry_run_only: bool
    source_event_witness_path: str
    selections: tuple[TemplateReactionSelection, ...]
    refused_effects: tuple[TemplateReactionSelection, ...]
    graph_mutation_blocked: bool
    scheduler_mutation_blocked: bool
    agent_activation_blocked: bool
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TemplateReactionSelectionScanReceipt:
    """Summary receipt for one dry-run reaction-selection pass."""

    receipt_id: str
    emitted_at: str
    scanned_root: str
    event_witness_count: int
    selection_witness_count: int
    selected_reaction_count: int
    refused_reaction_count: int
    selection_witness_paths: tuple[str, ...]


class KernelTemplateReactionSelector:
    """Dry-run reaction selector for Template Completion Event witnesses.

    Phase 2 contract:
    - May read Phase 1 event witnesses.
    - May select candidate reaction families from declared downstream effects.
    - May emit reaction-selection witnesses and receipts.
    - Must not mutate graph, scheduler, registry, index, or agent state.
    """

    DEFAULT_EFFECT_TO_REACTION_FAMILY: dict[str, str] = {
        "update_index": "index_update",
        "update_summary": "index_update",
        "refresh_context_package_source": "index_update",
        "mark_stale_summary": "index_update",
        "create_graph_node": "graph_node_create",
        "bind_source_node": "graph_node_create",
        "update_graph_edge": "graph_edge_update",
        "mark_dependency_edge": "graph_edge_update",
        "schedule_followup": "schedule_followup",
        "schedule_review": "schedule_followup",
        "create_work_unit_proposal": "schedule_followup",
        "spawn_agent": "agent_activation_request",
        "request_specialist": "agent_activation_request",
        "fan_out_packet": "agent_activation_request",
        "mark_contradiction": "contradiction_mark",
        "contest_claim": "contradiction_mark",
        "registry_update_proposal": "registry_update_proposal",
        "semantic_identity_delta": "registry_update_proposal",
    }

    DEFAULT_REACTION_FAMILIES: dict[str, GraphReactionFamily] = {
        "index_update": GraphReactionFamily(
            family_id="index_update",
            reaction_class="projection_reaction",
            required_authority="WITNESS_OR_PROJECTION_UPDATE",
            receipt_type="index_update_receipt",
        ),
        "graph_node_create": GraphReactionFamily(
            family_id="graph_node_create",
            reaction_class="source_graph_reaction",
            required_authority="GOVERNED_WRITE_OR_RATIFIED_SOURCE_UPDATE",
            receipt_type="graph_writeback_receipt",
        ),
        "graph_edge_update": GraphReactionFamily(
            family_id="graph_edge_update",
            reaction_class="source_graph_reaction",
            required_authority="GOVERNED_WRITE_OR_RATIFIED_SOURCE_UPDATE",
            receipt_type="graph_writeback_receipt",
        ),
        "schedule_followup": GraphReactionFamily(
            family_id="schedule_followup",
            reaction_class="scheduling_reaction",
            required_authority="SCHEDULER_GATE",
            receipt_type="schedule_reaction_receipt",
        ),
        "agent_activation_request": GraphReactionFamily(
            family_id="agent_activation_request",
            reaction_class="fanout_reaction",
            required_authority="ROLE_ACTIVATION_REVIEW",
            receipt_type="agent_activation_request_receipt",
        ),
        "contradiction_mark": GraphReactionFamily(
            family_id="contradiction_mark",
            reaction_class="review_reaction",
            required_authority="CONTRADICTION_PRESERVATION",
            receipt_type="contradiction_mark_receipt",
        ),
        "registry_update_proposal": GraphReactionFamily(
            family_id="registry_update_proposal",
            reaction_class="registry_reaction",
            required_authority="REGISTRY_DELTA_REVIEW",
            receipt_type="registry_update_proposal_receipt",
        ),
    }

    def select_from_workspace(
        self,
        workspace_root: Path,
        *,
        emitted_at: str | None = None,
        write_witnesses: bool = True,
        effect_map: dict[str, str] | None = None,
        reaction_families: dict[str, GraphReactionFamily] | None = None,
        template_contracts: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> TemplateReactionSelectionScanReceipt:
        root = Path(workspace_root)
        if not root.exists():
            raise KernelTemplateReactionSelectionError(f"workspace root does not exist: {root}")
        timestamp = emitted_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        runtime_contracts = template_contracts
        if runtime_contracts is None:
            runtime_contracts = load_contracts_if_projection_exists(root)
        event_paths = tuple(sorted((root / "ION/05_context/history/template_completion_event_witnesses").glob("*.json")))
        witnesses: list[TemplateReactionSelectionWitness] = []
        selected_count = 0
        refused_count = 0
        for event_path in event_paths:
            witness = self.select_for_event_witness(
                root,
                event_path,
                emitted_at=timestamp,
                effect_map=effect_map,
                reaction_families=reaction_families,
                template_contracts=runtime_contracts,
            )
            witnesses.append(witness)
            selected_count += len(witness.selections)
            refused_count += len(witness.refused_effects)
        written_paths: list[str] = []
        if write_witnesses:
            for witness in witnesses:
                path = self.write_selection_witness(root, witness)
                written_paths.append(path.relative_to(root).as_posix())
        receipt = TemplateReactionSelectionScanReceipt(
            receipt_id=self._stable_id("template-reaction-selection-scan", root.as_posix(), timestamp),
            emitted_at=timestamp,
            scanned_root=root.as_posix(),
            event_witness_count=len(event_paths),
            selection_witness_count=len(witnesses),
            selected_reaction_count=selected_count,
            refused_reaction_count=refused_count,
            selection_witness_paths=tuple(written_paths),
        )
        if write_witnesses:
            self.write_scan_receipt(root, receipt)
        return receipt

    def select_for_event_witness(
        self,
        workspace_root: Path,
        event_witness_path: Path,
        *,
        emitted_at: str,
        effect_map: dict[str, str] | None = None,
        reaction_families: dict[str, GraphReactionFamily] | None = None,
        template_contracts: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> TemplateReactionSelectionWitness:
        root = Path(workspace_root)
        path = Path(event_witness_path)
        event = json.loads(path.read_text(encoding="utf-8"))
        if event.get("event_type") != "TEMPLATE_COMPLETION_EVENT":
            raise KernelTemplateReactionSelectionError(f"not a template completion event witness: {path}")
        requested_effects = tuple(_extract_downstream_effects(event))
        template_id = _resolve_event_template_id(event)
        active_effect_map = effect_map or self.DEFAULT_EFFECT_TO_REACTION_FAMILY
        active_families = reaction_families or self.DEFAULT_REACTION_FAMILIES
        selected: list[TemplateReactionSelection] = []
        refused: list[TemplateReactionSelection] = []
        for effect in requested_effects:
            if template_contracts is not None:
                gate = gate_reaction_selection_by_contract(template_id, effect, template_contracts)
                if not gate.selected:
                    refused.append(
                        TemplateReactionSelection(
                            event_id=str(event["event_id"]),
                            source_path=str(event["source_path"]),
                            requested_effect=effect,
                            reaction_family="CONTRACT_BLOCKED",
                            reaction_class="CONTRACT_BLOCKED",
                            required_authority="TEMPLATE_METADATA_CONTRACT",
                            status="REFUSED",
                            dry_run_only=True,
                            contract_bound=True,
                            contract_blocked_reason=gate.blocked_reason,
                            refusal_reason=gate.blocked_reason or "TEMPLATE_METADATA_CONTRACT_BLOCKED_REACTION",
                        )
                    )
                    continue
            family_id = active_effect_map.get(effect)
            if not family_id:
                refused.append(
                    TemplateReactionSelection(
                        event_id=str(event["event_id"]),
                        source_path=str(event["source_path"]),
                        requested_effect=effect,
                        reaction_family="UNKNOWN",
                        reaction_class="UNKNOWN",
                        required_authority="UNKNOWN",
                        status="REFUSED",
                        dry_run_only=True,
                        contract_bound=template_contracts is not None,
                        refusal_reason="NO_REACTION_FAMILY_FOR_EFFECT",
                    )
                )
                continue
            family = active_families.get(family_id)
            if not family or not family.dry_run_allowed:
                refused.append(
                    TemplateReactionSelection(
                        event_id=str(event["event_id"]),
                        source_path=str(event["source_path"]),
                        requested_effect=effect,
                        reaction_family=family_id,
                        reaction_class="UNKNOWN" if not family else family.reaction_class,
                        required_authority="UNKNOWN" if not family else family.required_authority,
                        status="REFUSED",
                        dry_run_only=True,
                        contract_bound=template_contracts is not None,
                        refusal_reason="REACTION_FAMILY_NOT_DRY_RUN_ALLOWED",
                    )
                )
                continue
            selected.append(
                TemplateReactionSelection(
                    event_id=str(event["event_id"]),
                    source_path=str(event["source_path"]),
                    requested_effect=effect,
                    reaction_family=family.family_id,
                    reaction_class=family.reaction_class,
                    required_authority=family.required_authority,
                    status="DRY_RUN_SELECTED",
                    dry_run_only=True,
                    contract_bound=template_contracts is not None,
                )
            )
        rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix()
        selection_id = self._stable_id("template-reaction-selection", str(event["event_id"]), emitted_at)
        notes = [
            "Dry-run reaction selection only: no downstream mutation performed.",
            "Selected reactions remain proposals for later governed write/scheduler phases.",
        ]
        if template_contracts is not None:
            notes.append("Template metadata contract gate applied before reaction selection.")
        return TemplateReactionSelectionWitness(
            selection_id=selection_id,
            event_id=str(event["event_id"]),
            event_type="TEMPLATE_REACTION_SELECTION",
            source_path=str(event["source_path"]),
            emitted_at=emitted_at,
            phase="PHASE_2_DRY_RUN_REACTION_SELECTION_ONLY",
            dry_run_only=True,
            source_event_witness_path=rel,
            selections=tuple(selected),
            refused_effects=tuple(refused),
            graph_mutation_blocked=True,
            scheduler_mutation_blocked=True,
            agent_activation_blocked=True,
            notes=tuple(notes),
        )

    def write_selection_witness(self, workspace_root: Path, witness: TemplateReactionSelectionWitness) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/history/template_reaction_selection_witnesses"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{witness.selection_id}.template_reaction_selection_witness.json"
        if path.exists():
            return path
        path.write_text(json.dumps(_to_jsonable(witness), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def write_scan_receipt(self, workspace_root: Path, receipt: TemplateReactionSelectionScanReceipt) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/history/template_reaction_selection_scan_receipts"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{receipt.receipt_id}.template_reaction_selection_scan_receipt.json"
        if path.exists():
            return path
        path.write_text(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
        return f"{prefix}-{digest}"


IonTemplateReactionSelector = KernelTemplateReactionSelector
IonTemplateReactionSelectionError = KernelTemplateReactionSelectionError


def _resolve_event_template_id(event: dict[str, Any]) -> str:
    if event.get("template_id"):
        return str(event["template_id"])
    front_matter = event.get("front_matter") or {}
    for key in ("template_id", "type", "packet_type", "template_class"):
        value = front_matter.get(key)
        if value:
            return str(value)
    return str(event.get("template_class") or "UNKNOWN_TEMPLATE")


def _extract_downstream_effects(event: dict[str, Any]) -> tuple[str, ...]:
    front_matter = event.get("front_matter") or {}
    raw = front_matter.get("downstream_effects") or front_matter.get("allowed_reactions") or []
    if isinstance(raw, str):
        return (raw,)
    if isinstance(raw, list):
        normalized = []
        for item in raw:
            if isinstance(item, str):
                normalized.append(item.strip())
            elif isinstance(item, dict):
                effect = item.get("effect") or item.get("reaction") or item.get("type")
                if effect:
                    normalized.append(str(effect).strip())
        return tuple(effect for effect in normalized if effect)
    return ()


def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    return value
