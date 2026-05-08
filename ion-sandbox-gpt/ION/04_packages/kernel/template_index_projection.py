"""Projection-only index updates for Evented Template File Graph reactions.

This module implements Phase 3 of the Evented Template File Graph law. It reads
Phase 2 Template Reaction Selection witnesses and materializes a separate,
projection-only index surface for reactions that are safe to represent as
index/projection updates.

It intentionally does not mutate source graph state, source files, registries,
schedules, or agent activation state. Projection files are witness/projection
surfaces, not kernel truth and not source graph truth.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


class KernelTemplateIndexProjectionError(Exception):
    """Raised when template reaction projection cannot proceed."""


@dataclass(frozen=True)
class TemplateIndexProjectionEntry:
    """One projection-safe index entry derived from a reaction selection witness."""

    event_id: str
    selection_id: str
    source_path: str
    requested_effect: str
    reaction_family: str
    reaction_class: str
    projection_status: str
    projection_kind: str
    required_authority: str
    source_selection_witness_path: str


@dataclass(frozen=True)
class TemplateIndexProjectionDeferral:
    """One non-projection reaction deliberately deferred by Phase 3."""

    event_id: str
    selection_id: str
    source_path: str
    requested_effect: str
    reaction_family: str
    reaction_class: str
    deferral_reason: str
    source_selection_witness_path: str


@dataclass(frozen=True)
class TemplateIndexProjectionSurface:
    """Durable projection-only index surface for template event reactions."""

    projection_id: str
    projection_type: str
    emitted_at: str
    phase: str
    projection_only: bool
    source_graph_mutation_blocked: bool
    registry_mutation_blocked: bool
    schedule_mutation_blocked: bool
    agent_activation_blocked: bool
    entries: tuple[TemplateIndexProjectionEntry, ...]
    deferred_reactions: tuple[TemplateIndexProjectionDeferral, ...]
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TemplateIndexProjectionReceipt:
    """Receipt for one Phase 3 projection-index update pass."""

    receipt_id: str
    emitted_at: str
    scanned_root: str
    selection_witness_count: int
    projected_entry_count: int
    deferred_reaction_count: int
    projection_path: str
    projection_only: bool


class KernelTemplateIndexProjector:
    """Projection-only index updater for Template Reaction Selection witnesses.

    Phase 3 contract:
    - May read Phase 2 reaction-selection witnesses.
    - May materialize a separate projection index and receipt.
    - May include only projection-safe reactions as index entries.
    - Must defer graph, registry, schedule, and agent-activation reactions.
    - Must not mutate source graph, registries, schedules, or source files.
    """

    PROJECTION_SAFE_FAMILIES: tuple[str, ...] = ("index_update",)

    def project_from_workspace(
        self,
        workspace_root: Path,
        *,
        emitted_at: str | None = None,
        write_projection: bool = True,
    ) -> TemplateIndexProjectionReceipt:
        root = Path(workspace_root)
        if not root.exists():
            raise KernelTemplateIndexProjectionError(f"workspace root does not exist: {root}")
        timestamp = emitted_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        selection_paths = tuple(
            sorted((root / "ION/05_context/history/template_reaction_selection_witnesses").glob("*.json"))
        )
        surface = self.build_projection_surface(root, selection_paths, emitted_at=timestamp)
        projection_path = ""
        if write_projection:
            projection_path = self.write_projection_surface(root, surface).relative_to(root).as_posix()
            self.write_projection_receipt(
                root,
                TemplateIndexProjectionReceipt(
                    receipt_id=self._stable_id("template-index-projection", surface.projection_id, timestamp),
                    emitted_at=timestamp,
                    scanned_root=root.as_posix(),
                    selection_witness_count=len(selection_paths),
                    projected_entry_count=len(surface.entries),
                    deferred_reaction_count=len(surface.deferred_reactions),
                    projection_path=projection_path,
                    projection_only=True,
                ),
            )
        return TemplateIndexProjectionReceipt(
            receipt_id=self._stable_id("template-index-projection", surface.projection_id, timestamp),
            emitted_at=timestamp,
            scanned_root=root.as_posix(),
            selection_witness_count=len(selection_paths),
            projected_entry_count=len(surface.entries),
            deferred_reaction_count=len(surface.deferred_reactions),
            projection_path=projection_path,
            projection_only=True,
        )

    def build_projection_surface(
        self,
        workspace_root: Path,
        selection_witness_paths: tuple[Path, ...],
        *,
        emitted_at: str,
    ) -> TemplateIndexProjectionSurface:
        root = Path(workspace_root)
        entries: list[TemplateIndexProjectionEntry] = []
        deferred: list[TemplateIndexProjectionDeferral] = []
        for path in selection_witness_paths:
            witness = json.loads(Path(path).read_text(encoding="utf-8"))
            if witness.get("event_type") != "TEMPLATE_REACTION_SELECTION":
                raise KernelTemplateIndexProjectionError(f"not a template reaction selection witness: {path}")
            rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix()
            for selected in witness.get("selections", []):
                family = str(selected.get("reaction_family", ""))
                if family in self.PROJECTION_SAFE_FAMILIES:
                    entries.append(
                        TemplateIndexProjectionEntry(
                            event_id=str(witness["event_id"]),
                            selection_id=str(witness["selection_id"]),
                            source_path=str(witness["source_path"]),
                            requested_effect=str(selected.get("requested_effect", "")),
                            reaction_family=family,
                            reaction_class=str(selected.get("reaction_class", "")),
                            projection_status="PROJECTED_ONLY",
                            projection_kind="template_event_index_projection",
                            required_authority=str(selected.get("required_authority", "")),
                            source_selection_witness_path=rel,
                        )
                    )
                else:
                    deferred.append(
                        TemplateIndexProjectionDeferral(
                            event_id=str(witness["event_id"]),
                            selection_id=str(witness["selection_id"]),
                            source_path=str(witness["source_path"]),
                            requested_effect=str(selected.get("requested_effect", "")),
                            reaction_family=family,
                            reaction_class=str(selected.get("reaction_class", "")),
                            deferral_reason="NOT_PROJECTION_SAFE_IN_PHASE_3",
                            source_selection_witness_path=rel,
                        )
                    )
            for refused in witness.get("refused_effects", []):
                deferred.append(
                    TemplateIndexProjectionDeferral(
                        event_id=str(witness["event_id"]),
                        selection_id=str(witness["selection_id"]),
                        source_path=str(witness["source_path"]),
                        requested_effect=str(refused.get("requested_effect", "")),
                        reaction_family=str(refused.get("reaction_family", "UNKNOWN")),
                        reaction_class=str(refused.get("reaction_class", "UNKNOWN")),
                        deferral_reason=str(refused.get("refusal_reason", "REFUSED_IN_PHASE_2")),
                        source_selection_witness_path=rel,
                    )
                )
        projection_id = self._stable_id(
            "template-event-index-projection",
            emitted_at,
            *(entry.event_id + entry.requested_effect for entry in entries),
            *(item.event_id + item.requested_effect + item.deferral_reason for item in deferred),
        )
        return TemplateIndexProjectionSurface(
            projection_id=projection_id,
            projection_type="TEMPLATE_EVENT_INDEX_PROJECTION",
            emitted_at=emitted_at,
            phase="PHASE_3_PROJECTION_ONLY_INDEX_UPDATE",
            projection_only=True,
            source_graph_mutation_blocked=True,
            registry_mutation_blocked=True,
            schedule_mutation_blocked=True,
            agent_activation_blocked=True,
            entries=tuple(entries),
            deferred_reactions=tuple(deferred),
            notes=(
                "Projection-only index surface: not source graph truth.",
                "Only projection-safe index_update reactions are materialized as entries in Phase 3.",
                "All graph, schedule, registry, and agent activation reactions remain deferred.",
            ),
        )

    def write_projection_surface(self, workspace_root: Path, surface: TemplateIndexProjectionSurface) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/projections/template_event_index_projection"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{surface.projection_id}.template_event_index_projection.json"
        if path.exists():
            return path
        path.write_text(json.dumps(_to_jsonable(surface), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def write_projection_receipt(self, workspace_root: Path, receipt: TemplateIndexProjectionReceipt) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/history/template_index_projection_receipts"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{receipt.receipt_id}.template_index_projection_receipt.json"
        if path.exists():
            return path
        path.write_text(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
        return f"{prefix}-{digest}"


IonTemplateIndexProjector = KernelTemplateIndexProjector
IonTemplateIndexProjectionError = KernelTemplateIndexProjectionError


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
