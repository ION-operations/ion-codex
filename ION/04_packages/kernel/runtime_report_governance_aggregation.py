"""Second-order aggregation for runtime-report governance reflections.

This module does not mint new kernel truth. It promotes selected E1 witness outputs into
broader operator/system visibility surfaces only when a caller explicitly opts in.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
import json
from pathlib import Path
import re
from typing import TYPE_CHECKING, Iterable

from .runtime_report_anchors import anchor_tag, operator_rollup_anchor

if TYPE_CHECKING:
    from .runtime_report_triggers import RuntimeReportTriggerReceipt


class KernelRuntimeReportGovernanceAggregationError(Exception):
    """Raised when one governance aggregation step cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportGovernanceAggregationBatchResult:
    aggregation_event_id: str
    created_at: str
    system_ledger_path: str | None
    operator_rollup_path: str | None
    receipt_count: int


class KernelRuntimeReportGovernanceAggregationManager:
    """Aggregate E1 governance reflections into broader witness/system surfaces."""

    def aggregate_receipts(
        self,
        receipts: Iterable["RuntimeReportTriggerReceipt"],
        *,
        workspace_root: str | Path,
        created_at: str | None = None,
        system_ledger_path: str | Path = "ION/05_context/history/system_ledger.json",
        operator_rollups_dir: str | Path = "ION/05_context/runtime_reports/governance/rollups",
        append_system_ledger: bool = True,
        write_operator_rollup: bool = True,
    ) -> tuple["RuntimeReportTriggerReceipt", ...]:
        realized = tuple(receipts)
        if not realized:
            return ()
        if not append_system_ledger and not write_operator_rollup:
            return realized

        generated_at = created_at or _iso_now()
        root = Path(workspace_root).resolve()
        root.mkdir(parents=True, exist_ok=True)
        aggregation_event_id = _aggregation_event_id(realized[0], generated_at)

        ledger_relative: Path | None = None
        ledger_resolved: Path | None = None
        if append_system_ledger:
            ledger_relative = Path(system_ledger_path)
            ledger_resolved = _resolve_relative_file(root, ledger_relative)

        rollup_relative: Path | None = None
        rollup_resolved: Path | None = None
        if write_operator_rollup:
            rollup_relative = Path(operator_rollups_dir) / _rollup_filename(realized[0], generated_at)
            rollup_resolved = _resolve_relative_file(root, rollup_relative)
            rollup_resolved.parent.mkdir(parents=True, exist_ok=True)
            rollup_resolved.write_text(
                _render_rollup(
                    receipts=realized,
                    created_at=generated_at,
                    aggregation_event_id=aggregation_event_id,
                    system_ledger_path=(str(ledger_relative) if ledger_relative is not None else None),
                    operator_rollup_path=str(rollup_relative),
                ),
                encoding="utf-8",
            )

        ledger_entry_index: int | None = None
        if ledger_relative is not None and ledger_resolved is not None:
            ledger_rows = _load_system_ledger_rows(ledger_resolved)
            ledger_entry_index = len(ledger_rows) + 1
            ledger_rows.append(
                {
                    "event_id": aggregation_event_id,
                    "entry_index": ledger_entry_index,
                    "event_type": "runtime_report_governance_aggregation",
                    "created_at": generated_at,
                    "receipt_count": len(realized),
                    "trigger_events": sorted({receipt.event.value for receipt in realized}),
                    "artifact_kinds": sorted({receipt.artifact_kind.value for receipt in realized}),
                    "source_refs": [receipt.source_ref for receipt in realized],
                    "governance_event_ids": [
                        value
                        for value in dict.fromkeys(
                            receipt.governance_event_id for receipt in realized if receipt.governance_event_id
                        )
                    ],
                    "governance_ledger_paths": [
                        value
                        for value in dict.fromkeys(
                            receipt.governance_ledger_path for receipt in realized if receipt.governance_ledger_path
                        )
                    ],
                    "governance_summary_paths": [
                        value
                        for value in dict.fromkeys(
                            receipt.operator_summary_path for receipt in realized if receipt.operator_summary_path
                        )
                    ],
                    "operator_rollup_path": (str(rollup_relative) if rollup_relative is not None else None),
                    "authority_class": "GENERATED_STATE",
                    "boundary": "Second-order witness over runtime-report governance reflections.",
                }
            )
            ledger_resolved.parent.mkdir(parents=True, exist_ok=True)
            ledger_resolved.write_text(json.dumps(ledger_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        batch = RuntimeReportGovernanceAggregationBatchResult(
            aggregation_event_id=aggregation_event_id,
            created_at=generated_at,
            system_ledger_path=(str(ledger_relative) if ledger_relative is not None else None),
            operator_rollup_path=(str(rollup_relative) if rollup_relative is not None else None),
            receipt_count=len(realized),
        )
        return tuple(
            replace(
                receipt,
                aggregation_event_id=batch.aggregation_event_id,
                system_ledger_path=batch.system_ledger_path,
                system_ledger_entry_index=ledger_entry_index,
                operator_rollup_path=batch.operator_rollup_path,
                operator_rollup_anchor=(
                    operator_rollup_anchor(receipt.event.value, receipt.source_ref, position)
                    if batch.operator_rollup_path is not None
                    else None
                ),
            )
            for position, receipt in enumerate(realized, start=1)
        )


IonRuntimeReportGovernanceAggregationManager = KernelRuntimeReportGovernanceAggregationManager


def _load_system_ledger_rows(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    existing = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(existing, list):
        raise KernelRuntimeReportGovernanceAggregationError("system_ledger.json must contain a JSON list.")
    return existing


def _render_rollup(
    *,
    receipts: tuple["RuntimeReportTriggerReceipt", ...],
    created_at: str,
    aggregation_event_id: str,
    system_ledger_path: str | None,
    operator_rollup_path: str,
) -> str:
    trigger_counts: dict[str, int] = {}
    artifact_counts: dict[str, int] = {}
    for receipt in receipts:
        trigger_counts[receipt.event.value] = trigger_counts.get(receipt.event.value, 0) + 1
        artifact_counts[receipt.artifact_kind.value] = artifact_counts.get(receipt.artifact_kind.value, 0) + 1

    lines = [
        "---",
        "rollup_kind: RUNTIME_REPORT_GOVERNANCE_ROLLUP",
        "authority_class: GENERATED_STATE",
        f"generated_at: {created_at}",
        f"aggregation_event_id: {aggregation_event_id}",
        f"relative_output_path: {operator_rollup_path}",
        "---",
        "",
        "# Runtime Report Governance Rollup",
        "",
        "## Coverage",
        "",
        f"- Aggregation Event Id: {aggregation_event_id}",
        f"- Created At: {created_at}",
        f"- Receipt Count: {len(receipts)}",
    ]
    if system_ledger_path is not None:
        lines.append(f"- System Ledger Path: {system_ledger_path}")
    governance_ids = [value for value in dict.fromkeys(receipt.governance_event_id for receipt in receipts if receipt.governance_event_id)]
    if governance_ids:
        lines.append("- Governance Event Ids:")
        lines.extend(f"  - {value}" for value in governance_ids)

    lines.extend(["", "## Trigger Event Counts", ""])
    for event, count in sorted(trigger_counts.items()):
        lines.append(f"- {event}: {count}")
    lines.extend(["", "## Artifact Kind Counts", ""])
    for artifact_kind, count in sorted(artifact_counts.items()):
        lines.append(f"- {artifact_kind}: {count}")

    lines.extend(["", "## Receipts", ""])
    for position, receipt in enumerate(receipts, start=1):
        artifact = receipt.artifact_result.preparation.artifact
        lines.extend(
            [
                anchor_tag(operator_rollup_anchor(receipt.event.value, receipt.source_ref, position)),
                f"### {receipt.event.value} — {receipt.source_ref}",
                "",
                f"- Artifact Kind: {receipt.artifact_kind.value}",
                f"- Reason: {receipt.reason}",
                f"- Artifact Path: {artifact.relative_output_path}",
                f"- Governance Event Id: {receipt.governance_event_id or 'NONE'}",
                f"- Governance Ledger Path: {receipt.governance_ledger_path or 'NONE'}",
                f"- Governance Summary Path: {receipt.operator_summary_path or 'NONE'}",
            ]
        )
        if artifact.runtime_refs:
            lines.append("- Runtime Refs:")
            lines.extend(f"  - {ref}" for ref in artifact.runtime_refs)
        lines.append("")

    lines.extend(
        [
            "## Boundary",
            "",
            "- This rollup is a second-order witness over E1 governance reflections.",
            "- It does not become kernel truth, doctrine, route authority, or runtime authority.",
            "- It exists to improve operator visibility across already-emitted runtime report events.",
            "",
        ]
    )
    return "\n".join(lines)


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportGovernanceAggregationError(f"Absolute output paths are not allowed: {relative_path}")
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportGovernanceAggregationError(f"Output path escapes workspace root: {relative_path}") from exc
    return resolved


def _rollup_filename(receipt: "RuntimeReportTriggerReceipt", created_at: str) -> str:
    stamp = re.sub(r"[^0-9]", "", created_at)[:14]
    safe_event = _safe(receipt.event.value)
    safe_source = _safe(receipt.source_ref)
    return f"{safe_event}__{safe_source}__{stamp}.runtime_governance_rollup.md"


def _aggregation_event_id(receipt: "RuntimeReportTriggerReceipt", created_at: str) -> str:
    stamp = re.sub(r"[^0-9]", "", created_at)[:14]
    return f"runtime-governance-aggregation-{_safe(receipt.event.value)}-{_safe(receipt.source_ref)}-{stamp}"


def _safe(value: str) -> str:
    safe = re.sub(r"[^0-9A-Za-z._-]+", "-", value).strip("-._")
    return safe or "runtime"


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
