"""Governance reflection for triggered runtime-report artifacts.

This module does not create a new kernel truth family. It reflects already-emitted
runtime-report trigger receipts into bounded generated witness surfaces: a JSON ledger
for durable event traceability and an optional operator-facing markdown summary.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
import json
from pathlib import Path
import re
from typing import TYPE_CHECKING, Iterable

from .runtime_report_anchors import anchor_tag, governance_summary_anchor

if TYPE_CHECKING:
    from .runtime_report_triggers import RuntimeReportTriggerReceipt


class KernelRuntimeReportGovernanceError(Exception):
    """Raised when one runtime-report governance reflection cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportGovernanceBatchResult:
    event_id: str
    created_at: str
    ledger_path: str
    summary_path: str | None
    receipt_count: int


class KernelRuntimeReportGovernanceManager:
    """Reflect trigger receipts into bounded witness ledgers and summaries."""

    def reflect_receipts(
        self,
        receipts: Iterable["RuntimeReportTriggerReceipt"],
        *,
        workspace_root: str | Path,
        created_at: str | None = None,
        ledger_path: str | Path = "ION/05_context/history/runtime_report_trigger_ledger.json",
        summaries_dir: str | Path = "ION/05_context/runtime_reports/governance",
        write_summary: bool = True,
    ) -> tuple["RuntimeReportTriggerReceipt", ...]:
        realized = tuple(receipts)
        if not realized:
            return ()
        generated_at = created_at or _iso_now()
        root = Path(workspace_root).resolve()
        root.mkdir(parents=True, exist_ok=True)

        event_id = _event_id(realized[0], generated_at)
        ledger_relative = Path(ledger_path)
        ledger_resolved = _resolve_relative_file(root, ledger_relative)
        summary_relative: Path | None = None
        summary_resolved: Path | None = None
        if write_summary:
            summary_relative = Path(summaries_dir) / _summary_filename(realized[0], generated_at)
            summary_resolved = _resolve_relative_file(root, summary_relative)

        if summary_relative is not None and summary_resolved is not None:
            summary_resolved.parent.mkdir(parents=True, exist_ok=True)
            summary_resolved.write_text(
                _render_summary(
                    receipts=realized,
                    created_at=generated_at,
                    event_id=event_id,
                    ledger_path=str(ledger_relative),
                    summary_path=str(summary_relative),
                ),
                encoding="utf-8",
            )

        ledger_rows = _load_ledger_rows(ledger_resolved)
        ledger_start_index = len(ledger_rows) + 1
        for position, receipt in enumerate(realized, start=1):
            summary_anchor = (
                governance_summary_anchor(receipt.artifact_kind.value, receipt.source_ref, position)
                if summary_relative is not None
                else None
            )
            ledger_rows.append(
                {
                    "event_id": event_id,
                    "entry_index": ledger_start_index + position - 1,
                    "batch_entry_index": position,
                    "entry_type": "runtime_report_trigger_reflection",
                    "created_at": generated_at,
                    "trigger_event": receipt.event.value,
                    "artifact_kind": receipt.artifact_kind.value,
                    "source_ref": receipt.source_ref,
                    "reason": receipt.reason,
                    "artifact_relative_output_path": receipt.artifact_result.preparation.artifact.relative_output_path,
                    "artifact_generated_at": receipt.artifact_result.preparation.artifact.generated_at,
                    "artifact_authority_class": receipt.artifact_result.preparation.artifact.authority_class.value,
                    "runtime_refs": list(receipt.artifact_result.preparation.artifact.runtime_refs),
                    "summary_path": (str(summary_relative) if summary_relative is not None else None),
                    "summary_anchor": summary_anchor,
                }
            )
        ledger_resolved.parent.mkdir(parents=True, exist_ok=True)
        ledger_resolved.write_text(json.dumps(ledger_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        batch = RuntimeReportGovernanceBatchResult(
            event_id=event_id,
            created_at=generated_at,
            ledger_path=str(ledger_relative),
            summary_path=(str(summary_relative) if summary_relative is not None else None),
            receipt_count=len(realized),
        )
        return tuple(
            replace(
                receipt,
                governance_event_id=batch.event_id,
                governance_ledger_path=batch.ledger_path,
                governance_ledger_entry_index=ledger_start_index + position - 1,
                operator_summary_path=batch.summary_path,
                operator_summary_anchor=(
                    governance_summary_anchor(receipt.artifact_kind.value, receipt.source_ref, position)
                    if batch.summary_path is not None
                    else None
                ),
            )
            for position, receipt in enumerate(realized, start=1)
        )


IonRuntimeReportGovernanceManager = KernelRuntimeReportGovernanceManager


def _load_ledger_rows(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    existing = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(existing, list):
        raise KernelRuntimeReportGovernanceError("runtime_report_trigger_ledger.json must contain a JSON list.")
    return existing


def _render_summary(
    *,
    receipts: tuple["RuntimeReportTriggerReceipt", ...],
    created_at: str,
    event_id: str,
    ledger_path: str,
    summary_path: str,
) -> str:
    first = receipts[0]
    lines = [
        "---",
        "reflection_kind: RUNTIME_REPORT_TRIGGER_SUMMARY",
        "authority_class: GENERATED_STATE",
        f"generated_at: {created_at}",
        f"event_id: {event_id}",
        f"trigger_event: {first.event.value}",
        f"ledger_path: {ledger_path}",
        f"relative_output_path: {summary_path}",
        "---",
        "",
        f"# Runtime Report Trigger Summary — {first.event.value}",
        "",
        "## Event",
        "",
        f"- Event Id: {event_id}",
        f"- Trigger Event: {first.event.value}",
        f"- Created At: {created_at}",
        f"- Receipt Count: {len(receipts)}",
        "",
        "## Reflected Trigger Receipts",
        "",
    ]
    for position, receipt in enumerate(receipts, start=1):
        artifact = receipt.artifact_result.preparation.artifact
        lines.extend(
            [
                anchor_tag(governance_summary_anchor(receipt.artifact_kind.value, receipt.source_ref, position)),
                f"### {receipt.artifact_kind.value} — {receipt.source_ref}",
                "",
                f"- Reason: {receipt.reason}",
                f"- Artifact Path: {artifact.relative_output_path}",
                f"- Artifact Generated At: {artifact.generated_at}",
                f"- Artifact Authority Class: {artifact.authority_class.value}",
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
            "- These rows are witness reflections over already-emitted runtime artifacts.",
            "- They do not become kernel truth, doctrine, or runtime authority by being summarized here.",
            "",
        ]
    )
    return "\n".join(lines)


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportGovernanceError(f"Absolute output paths are not allowed: {relative_path}")
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportGovernanceError(f"Output path escapes workspace root: {relative_path}") from exc
    return resolved


def _summary_filename(receipt: "RuntimeReportTriggerReceipt", created_at: str) -> str:
    stamp = re.sub(r"[^0-9]", "", created_at)[:14]
    safe_event = _safe(receipt.event.value)
    safe_source = _safe(receipt.source_ref)
    return f"{safe_event}__{safe_source}__{stamp}.runtime_trigger_summary.md"


def _event_id(receipt: "RuntimeReportTriggerReceipt", created_at: str) -> str:
    stamp = re.sub(r"[^0-9]", "", created_at)[:14]
    return f"runtime-trigger-{_safe(receipt.event.value)}-{_safe(receipt.source_ref)}-{stamp}"


def _safe(value: str) -> str:
    safe = re.sub(r"[^0-9A-Za-z._-]+", "-", value).strip("-._")
    return safe or "runtime"


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
