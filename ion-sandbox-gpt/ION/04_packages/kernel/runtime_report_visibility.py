"""Downstream visibility projection for aggregated runtime-report witness receipts.

This module does not create kernel truth. It projects selected E2-aggregated runtime-report
receipts into broader operator visibility surfaces such as packet indexes and dashboards,
while staying explicitly downstream from generated artifacts, governance reflections, and
aggregation witnesses.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
import json
from pathlib import Path
import re
from typing import TYPE_CHECKING, Iterable

from .runtime_report_anchors import (
    anchor_tag,
    dashboard_entry_anchor,
    packet_index_pointer,
)

if TYPE_CHECKING:
    from .runtime_report_triggers import RuntimeReportTriggerReceipt


class KernelRuntimeReportVisibilityError(Exception):
    """Raised when one runtime-report visibility projection cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportVisibilityBatchResult:
    visibility_event_id: str
    created_at: str
    packet_index_path: str | None
    operator_dashboard_path: str | None
    receipt_count: int


class KernelRuntimeReportVisibilityProjector:
    """Project E2-aggregated witness receipts into downstream operator visibility surfaces."""

    def project_receipts(
        self,
        receipts: Iterable["RuntimeReportTriggerReceipt"],
        *,
        workspace_root: str | Path,
        created_at: str | None = None,
        packet_index_path: str | Path = "ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json",
        operator_dashboard_path: str | Path = "ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md",
        append_packet_index: bool = True,
        write_operator_dashboard: bool = True,
    ) -> tuple["RuntimeReportTriggerReceipt", ...]:
        realized = tuple(receipts)
        if not realized:
            return ()
        if not append_packet_index and not write_operator_dashboard:
            return realized

        eligible = tuple(receipt for receipt in realized if _is_e2_eligible(receipt))
        if not eligible:
            return realized

        generated_at = created_at or _iso_now()
        root = Path(workspace_root).resolve()
        root.mkdir(parents=True, exist_ok=True)
        visibility_event_id = _visibility_event_id(eligible[0], generated_at)

        index_relative: Path | None = None
        index_resolved: Path | None = None
        packet_index_document: dict[str, object] | None = None
        if append_packet_index:
            index_relative = Path(packet_index_path)
            index_resolved = _resolve_relative_file(root, index_relative)
            packet_index_document = _load_packet_index(index_resolved)
            entries = list(packet_index_document["entries"])
            start_index = len(entries) + 1
            for offset, receipt in enumerate(eligible, start=0):
                entries.append(
                    _entry_for_receipt(
                        receipt,
                        created_at=generated_at,
                        visibility_event_id=visibility_event_id,
                        entry_index=start_index + offset,
                    )
                )
            packet_index_document["updated_at"] = generated_at
            packet_index_document["entry_count"] = len(entries)
            packet_index_document["entries"] = entries
            index_resolved.parent.mkdir(parents=True, exist_ok=True)
            index_resolved.write_text(json.dumps(packet_index_document, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        dashboard_relative: Path | None = None
        dashboard_resolved: Path | None = None
        if write_operator_dashboard:
            dashboard_relative = Path(operator_dashboard_path)
            dashboard_resolved = _resolve_relative_file(root, dashboard_relative)
            dashboard_resolved.parent.mkdir(parents=True, exist_ok=True)
            dashboard_resolved.write_text(
                _render_dashboard(
                    receipts=eligible,
                    created_at=generated_at,
                    visibility_event_id=visibility_event_id,
                    packet_index_path=(str(index_relative) if index_relative is not None else None),
                    packet_index_document=packet_index_document,
                    operator_dashboard_path=str(dashboard_relative),
                ),
                encoding="utf-8",
            )

        batch = RuntimeReportVisibilityBatchResult(
            visibility_event_id=visibility_event_id,
            created_at=generated_at,
            packet_index_path=(str(index_relative) if index_relative is not None else None),
            operator_dashboard_path=(str(dashboard_relative) if dashboard_relative is not None else None),
            receipt_count=len(eligible),
        )
        eligible_ids = {id(receipt) for receipt in eligible}
        eligible_position = {id(receipt): position for position, receipt in enumerate(eligible, start=1)}
        indexed_start = (len(packet_index_document["entries"]) - len(eligible) + 1) if packet_index_document is not None else 1
        return tuple(
            replace(
                receipt,
                visibility_event_id=batch.visibility_event_id,
                packet_index_path=batch.packet_index_path,
                packet_index_entry_index=(indexed_start + eligible_position[id(receipt)] - 1 if batch.packet_index_path is not None else None),
                packet_index_pointer=(
                    packet_index_pointer(indexed_start + eligible_position[id(receipt)] - 1)
                    if batch.packet_index_path is not None
                    else None
                ),
                operator_dashboard_path=batch.operator_dashboard_path,
                operator_dashboard_anchor=(
                    dashboard_entry_anchor(
                        receipt.event.value,
                        receipt.source_ref,
                        indexed_start + eligible_position[id(receipt)] - 1 if batch.packet_index_path is not None else eligible_position[id(receipt)],
                    )
                    if batch.operator_dashboard_path is not None
                    else None
                ),
            )
            if id(receipt) in eligible_ids
            else receipt
            for receipt in realized
        )


IonRuntimeReportVisibilityProjector = KernelRuntimeReportVisibilityProjector


def _entry_for_receipt(
    receipt: "RuntimeReportTriggerReceipt",
    *,
    created_at: str,
    visibility_event_id: str,
    entry_index: int,
) -> dict[str, object]:
    artifact = receipt.artifact_result.preparation.artifact
    dashboard_anchor = dashboard_entry_anchor(receipt.event.value, receipt.source_ref, entry_index)
    return {
        "visibility_event_id": visibility_event_id,
        "entry_index": entry_index,
        "entry_type": "runtime_report_visibility_projection",
        "created_at": created_at,
        "trigger_event": receipt.event.value,
        "artifact_kind": receipt.artifact_kind.value,
        "source_ref": receipt.source_ref,
        "source_family": _source_family(receipt.source_ref),
        "reason": receipt.reason,
        "artifact_relative_output_path": artifact.relative_output_path,
        "artifact_generated_at": artifact.generated_at,
        "artifact_authority_class": artifact.authority_class.value,
        "artifact_anchor": artifact.anchor_id,
        "runtime_refs": list(artifact.runtime_refs),
        "governance_event_id": receipt.governance_event_id,
        "governance_ledger_path": receipt.governance_ledger_path,
        "governance_ledger_entry_index": receipt.governance_ledger_entry_index,
        "operator_summary_path": receipt.operator_summary_path,
        "operator_summary_anchor": receipt.operator_summary_anchor,
        "aggregation_event_id": receipt.aggregation_event_id,
        "system_ledger_path": receipt.system_ledger_path,
        "system_ledger_entry_index": receipt.system_ledger_entry_index,
        "operator_rollup_path": receipt.operator_rollup_path,
        "operator_rollup_anchor": receipt.operator_rollup_anchor,
        "packet_index_pointer": packet_index_pointer(entry_index),
        "operator_dashboard_anchor": dashboard_anchor,
        "downstream_boundary": "Projected visibility over E2 witness outputs.",
    }


def _render_dashboard(
    *,
    receipts: tuple["RuntimeReportTriggerReceipt", ...],
    created_at: str,
    visibility_event_id: str,
    packet_index_path: str | None,
    packet_index_document: dict[str, object] | None,
    operator_dashboard_path: str,
) -> str:
    index_entries: list[dict[str, object]] = []
    if packet_index_document is not None:
        raw_entries = packet_index_document.get("entries", [])
        if isinstance(raw_entries, list):
            index_entries = [item for item in raw_entries if isinstance(item, dict)]
    active_entries = index_entries or [
        _entry_for_receipt(receipt, created_at=created_at, visibility_event_id=visibility_event_id, entry_index=position)
        for position, receipt in enumerate(receipts, start=1)
    ]

    trigger_counts = _count_by(active_entries, "trigger_event")
    artifact_counts = _count_by(active_entries, "artifact_kind")
    source_family_counts = _count_by(active_entries, "source_family")
    recent_entries = list(reversed(active_entries[-10:]))

    lines = [
        "---",
        "dashboard_kind: RUNTIME_REPORT_OPERATOR_DASHBOARD",
        "authority_class: GENERATED_STATE",
        f"generated_at: {created_at}",
        f"visibility_event_id: {visibility_event_id}",
        f"relative_output_path: {operator_dashboard_path}",
        "---",
        "",
        "# Runtime Report Operator Dashboard",
        "",
        "## Coverage",
        "",
        f"- Visibility Event Id: {visibility_event_id}",
        f"- Created At: {created_at}",
        f"- Current Batch Receipt Count: {len(receipts)}",
        f"- Indexed Entry Count: {len(active_entries)}",
    ]
    if packet_index_path is not None:
        lines.append(f"- Packet Index Path: {packet_index_path}")
    system_ledgers = _unique_nonempty(entry.get("system_ledger_path") for entry in active_entries)
    if system_ledgers:
        lines.append("- System Ledger Paths:")
        lines.extend(f"  - {value}" for value in system_ledgers)
    rollups = _unique_nonempty(entry.get("operator_rollup_path") for entry in active_entries)
    if rollups:
        lines.append("- Operator Rollup Paths:")
        lines.extend(f"  - {value}" for value in rollups)

    lines.extend(["", "## Trigger Event Counts", ""])
    for key, value in sorted(trigger_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Artifact Kind Counts", ""])
    for key, value in sorted(artifact_counts.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Source Family Counts", ""])
    for key, value in sorted(source_family_counts.items()):
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Recent Projected Packets", ""])
    for entry in recent_entries:
        entry_index = _as_int(entry.get("entry_index"))
        lines.extend(
            [
                anchor_tag(dashboard_entry_anchor(str(entry.get("trigger_event") or "UNKNOWN"), str(entry.get("source_ref") or "UNKNOWN"), entry_index)),
                f"### {entry['trigger_event']} — {entry['source_ref']}",
                "",
                f"- Artifact Kind: {entry['artifact_kind']}",
                f"- Artifact Path: {entry['artifact_relative_output_path']}",
                f"- Source Family: {entry['source_family']}",
                f"- Aggregation Event Id: {entry.get('aggregation_event_id') or 'NONE'}",
                f"- System Ledger Path: {entry.get('system_ledger_path') or 'NONE'}",
                f"- Operator Rollup Path: {entry.get('operator_rollup_path') or 'NONE'}",
            ]
        )
        runtime_refs = entry.get("runtime_refs")
        if isinstance(runtime_refs, list) and runtime_refs:
            lines.append("- Runtime Refs:")
            lines.extend(f"  - {ref}" for ref in runtime_refs)
        lines.append("")

    lines.extend(
        [
            "## Boundary",
            "",
            "- This dashboard is a downstream visibility projection over E2 witness outputs.",
            "- It does not become kernel truth, doctrine, route authority, or runtime authority.",
            "- Artifacts, reflections, and aggregation witnesses remain the governing upstream surfaces.",
            "",
        ]
    )
    return "\n".join(lines)


def _load_packet_index(path: Path) -> dict[str, object]:
    if not path.exists():
        return {
            "index_kind": "RUNTIME_REPORT_PACKET_INDEX",
            "authority_class": "GENERATED_STATE",
            "updated_at": None,
            "entry_count": 0,
            "entries": [],
        }
    existing = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(existing, dict):
        raise KernelRuntimeReportVisibilityError("runtime_report_packet_index.json must contain a JSON object.")
    entries = existing.get("entries")
    if not isinstance(entries, list):
        raise KernelRuntimeReportVisibilityError("runtime_report_packet_index.json entries must be a JSON list.")
    return existing


def _count_by(entries: list[dict[str, object]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        value = entry.get(key)
        if not isinstance(value, str) or not value:
            value = "UNKNOWN"
        counts[value] = counts.get(value, 0) + 1
    return counts


def _unique_nonempty(values: Iterable[object]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if isinstance(value, str) and value and value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def _source_family(source_ref: str) -> str:
    if ":" not in source_ref:
        return "UNKNOWN"
    prefix, _, _ = source_ref.partition(":")
    return prefix or "UNKNOWN"


def _is_e2_eligible(receipt: "RuntimeReportTriggerReceipt") -> bool:
    return any(
        bool(value)
        for value in (
            receipt.aggregation_event_id,
            receipt.system_ledger_path,
            receipt.operator_rollup_path,
        )
    )


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportVisibilityError(f"Absolute output paths are not allowed: {relative_path}")
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportVisibilityError(f"Output path escapes workspace root: {relative_path}") from exc
    return resolved


def _visibility_event_id(receipt: "RuntimeReportTriggerReceipt", created_at: str) -> str:
    stamp = re.sub(r"[^0-9]", "", created_at)[:14]
    return f"runtime-visibility-{_safe(receipt.event.value)}-{_safe(receipt.source_ref)}-{stamp}"


def _safe(value: str) -> str:
    safe = re.sub(r"[^0-9A-Za-z._-]+", "-", value).strip("-._")
    return safe or "runtime"


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def _as_int(value: object) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0
