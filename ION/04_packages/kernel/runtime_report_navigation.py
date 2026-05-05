"""Bounded navigation/query helpers over downstream runtime-report visibility surfaces.

This module consumes the E3 packet index and dashboard for human navigation. It remains
explicitly downstream from generated artifacts, governance reflections, aggregation
witnesses, and visibility projections, and it does not promote those surfaces into
kernel truth or runtime authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re


class KernelRuntimeReportNavigationError(Exception):
    """Raised when one runtime-report navigation request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportNavigationQuery:
    artifact_kind: str | None = None
    trigger_event: str | None = None
    source_family: str | None = None
    source_ref_contains: str | None = None
    runtime_ref_contains: str | None = None
    reason_contains: str | None = None
    limit: int = 20


@dataclass(frozen=True)
class RuntimeReportNavigationEntry:
    entry_index: int
    created_at: str | None
    trigger_event: str
    artifact_kind: str
    source_ref: str
    source_family: str
    reason: str | None
    artifact_relative_output_path: str
    runtime_refs: tuple[str, ...] = ()
    artifact_anchor: str | None = None
    governance_ledger_path: str | None = None
    governance_ledger_entry_index: int | None = None
    operator_summary_path: str | None = None
    operator_summary_anchor: str | None = None
    aggregation_event_id: str | None = None
    system_ledger_path: str | None = None
    system_ledger_entry_index: int | None = None
    operator_rollup_path: str | None = None
    operator_rollup_anchor: str | None = None
    packet_index_pointer: str | None = None
    operator_dashboard_path: str | None = None
    operator_dashboard_anchor: str | None = None


@dataclass(frozen=True)
class RuntimeReportNavigationResult:
    packet_index_path: str
    operator_dashboard_path: str | None
    total_entries: int
    matched_count: int
    query: RuntimeReportNavigationQuery
    entries: tuple[RuntimeReportNavigationEntry, ...]


class KernelRuntimeReportNavigator:
    """Query and render bounded human-facing navigation over E3 packet indexes."""

    def load_packet_index(
        self,
        workspace_root: str | Path,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
    ) -> dict[str, object]:
        root = Path(workspace_root).resolve()
        resolved = _resolve_relative_file(root, Path(packet_index_path))
        if not resolved.exists():
            return {
                'index_kind': 'RUNTIME_REPORT_PACKET_INDEX',
                'authority_class': 'GENERATED_STATE',
                'updated_at': None,
                'entry_count': 0,
                'entries': [],
            }
        loaded = json.loads(resolved.read_text(encoding='utf-8'))
        if not isinstance(loaded, dict):
            raise KernelRuntimeReportNavigationError('runtime_report_packet_index.json must contain a JSON object.')
        entries = loaded.get('entries')
        if not isinstance(entries, list):
            raise KernelRuntimeReportNavigationError('runtime_report_packet_index.json entries must be a JSON list.')
        return loaded

    def query_entries(
        self,
        workspace_root: str | Path,
        query: RuntimeReportNavigationQuery | None = None,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
    ) -> RuntimeReportNavigationResult:
        realized_query = query or RuntimeReportNavigationQuery()
        document = self.load_packet_index(workspace_root, packet_index_path=packet_index_path)
        raw_entries = document.get('entries', [])
        typed_entries = [item for item in raw_entries if isinstance(item, dict)]
        filtered = [entry for entry in typed_entries if _matches_query(entry, realized_query)]
        filtered.sort(key=lambda item: _sortable_timestamp(item.get('created_at')), reverse=True)
        limited = filtered[: max(0, realized_query.limit)] if realized_query.limit >= 0 else filtered

        dashboard_relative = Path(operator_dashboard_path)
        root = Path(workspace_root).resolve()
        dashboard_resolved = _resolve_relative_file(root, dashboard_relative)
        return RuntimeReportNavigationResult(
            packet_index_path=str(packet_index_path),
            operator_dashboard_path=(str(operator_dashboard_path) if dashboard_resolved.exists() else None),
            total_entries=len(typed_entries),
            matched_count=len(filtered),
            query=realized_query,
            entries=tuple(_coerce_entry(entry, operator_dashboard_path=str(operator_dashboard_path)) for entry in limited),
        )

    def render_navigation_packet(
        self,
        result: RuntimeReportNavigationResult,
        *,
        created_at: str | None = None,
    ) -> str:
        generated_at = created_at or _iso_now()
        lines = [
            '---',
            'navigation_kind: RUNTIME_REPORT_NAVIGATION_PACKET',
            'authority_class: GENERATED_STATE',
            f'generated_at: {generated_at}',
            f'packet_index_path: {result.packet_index_path}',
        ]
        if result.operator_dashboard_path is not None:
            lines.append(f'operator_dashboard_path: {result.operator_dashboard_path}')
        lines.extend([
            f'total_entries: {result.total_entries}',
            f'matched_count: {result.matched_count}',
            '---',
            '',
            '# Runtime Report Navigation Packet',
            '',
            '## Query',
            '',
        ])
        query_rows = [
            ('Artifact Kind', result.query.artifact_kind),
            ('Trigger Event', result.query.trigger_event),
            ('Source Family', result.query.source_family),
            ('Source Ref Contains', result.query.source_ref_contains),
            ('Runtime Ref Contains', result.query.runtime_ref_contains),
            ('Reason Contains', result.query.reason_contains),
            ('Limit', str(result.query.limit)),
        ]
        for label, value in query_rows:
            lines.append(f'- {label}: {value if value else "ANY"}')

        lines.extend([
            '',
            '## Coverage',
            '',
            f'- Packet Index Path: {result.packet_index_path}',
            f'- Operator Dashboard Path: {result.operator_dashboard_path or "NONE"}',
            f'- Total Indexed Entries: {result.total_entries}',
            f'- Matched Entries: {result.matched_count}',
        ])

        lines.extend(['', '## Matched Packets', ''])
        if not result.entries:
            lines.append('- No matching packets were found in the downstream visibility index.')
        else:
            for entry in result.entries:
                lines.extend([
                    f"### {entry.trigger_event} — {entry.source_ref}",
                    '',
                    f'- Artifact Kind: {entry.artifact_kind}',
                    f'- Source Family: {entry.source_family}',
                    f'- Reason: {entry.reason or "NONE"}',
                    f'- Artifact Path: {entry.artifact_relative_output_path}',
                    f'- Artifact Anchor: {entry.artifact_anchor or "NONE"}',
                    f'- Packet Index Pointer: {entry.packet_index_pointer or "NONE"}',
                    f'- Governance Ledger Path: {entry.governance_ledger_path or "NONE"}',
                    f'- Governance Ledger Entry Index: {entry.governance_ledger_entry_index if entry.governance_ledger_entry_index is not None else "NONE"}',
                    f'- Governance Summary Path: {entry.operator_summary_path or "NONE"}',
                    f'- Governance Summary Anchor: {entry.operator_summary_anchor or "NONE"}',
                    f'- Aggregation Event Id: {entry.aggregation_event_id or "NONE"}',
                    f'- System Ledger Path: {entry.system_ledger_path or "NONE"}',
                    f'- System Ledger Entry Index: {entry.system_ledger_entry_index if entry.system_ledger_entry_index is not None else "NONE"}',
                    f'- Operator Rollup Path: {entry.operator_rollup_path or "NONE"}',
                    f'- Operator Rollup Anchor: {entry.operator_rollup_anchor or "NONE"}',
                    f'- Operator Dashboard Anchor: {entry.operator_dashboard_anchor or "NONE"}',
                ])
                if entry.runtime_refs:
                    lines.append('- Runtime Refs:')
                    lines.extend(f'  - {item}' for item in entry.runtime_refs)
                lines.append('')

        lines.extend([
            '## Boundary',
            '',
            '- This packet is a bounded navigation view over the E3 packet index and optional dashboard.',
            '- It remains downstream from artifacts, governance reflections, aggregation witnesses, and visibility projections.',
            '- It does not become kernel truth, doctrine, route authority, or runtime authority.',
            '',
        ])
        return '\n'.join(lines)

    def write_navigation_packet(
        self,
        workspace_root: str | Path,
        query: RuntimeReportNavigationQuery | None = None,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        output_path: str | Path | None = None,
        navigation_dir: str = 'ION/05_context/runtime_reports/governance/navigation',
        created_at: str | None = None,
    ) -> Path:
        result = self.query_entries(
            workspace_root,
            query,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
        )
        root = Path(workspace_root).resolve()
        relative = Path(output_path) if output_path is not None else Path(navigation_dir) / _default_filename(result.query, created_at)
        resolved = _resolve_relative_file(root, relative)
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(self.render_navigation_packet(result, created_at=created_at), encoding='utf-8')
        return resolved


IonRuntimeReportNavigator = KernelRuntimeReportNavigator


def _coerce_entry(entry: dict[str, object], *, operator_dashboard_path: str) -> RuntimeReportNavigationEntry:
    runtime_refs = entry.get('runtime_refs')
    if not isinstance(runtime_refs, list):
        runtime_refs = []
    return RuntimeReportNavigationEntry(
        entry_index=_as_int(entry.get('entry_index')),
        created_at=_as_optional_str(entry.get('created_at')),
        trigger_event=_as_optional_str(entry.get('trigger_event')) or 'UNKNOWN',
        artifact_kind=_as_optional_str(entry.get('artifact_kind')) or 'UNKNOWN',
        source_ref=_as_optional_str(entry.get('source_ref')) or 'UNKNOWN',
        source_family=_as_optional_str(entry.get('source_family')) or 'UNKNOWN',
        reason=_as_optional_str(entry.get('reason')),
        artifact_relative_output_path=_as_optional_str(entry.get('artifact_relative_output_path')) or '',
        runtime_refs=tuple(item for item in runtime_refs if isinstance(item, str) and item),
        artifact_anchor=_as_optional_str(entry.get('artifact_anchor')),
        governance_ledger_path=_as_optional_str(entry.get('governance_ledger_path')),
        governance_ledger_entry_index=_as_optional_int(entry.get('governance_ledger_entry_index')),
        operator_summary_path=_as_optional_str(entry.get('operator_summary_path')),
        operator_summary_anchor=_as_optional_str(entry.get('operator_summary_anchor')),
        aggregation_event_id=_as_optional_str(entry.get('aggregation_event_id')),
        system_ledger_path=_as_optional_str(entry.get('system_ledger_path')),
        system_ledger_entry_index=_as_optional_int(entry.get('system_ledger_entry_index')),
        operator_rollup_path=_as_optional_str(entry.get('operator_rollup_path')),
        operator_rollup_anchor=_as_optional_str(entry.get('operator_rollup_anchor')),
        packet_index_pointer=_as_optional_str(entry.get('packet_index_pointer')),
        operator_dashboard_path=operator_dashboard_path,
        operator_dashboard_anchor=_as_optional_str(entry.get('operator_dashboard_anchor')),
    )


def _as_optional_int(value: object) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def _matches_query(entry: dict[str, object], query: RuntimeReportNavigationQuery) -> bool:
    if query.artifact_kind and not _equals(entry.get('artifact_kind'), query.artifact_kind):
        return False
    if query.trigger_event and not _equals(entry.get('trigger_event'), query.trigger_event):
        return False
    if query.source_family and not _equals(entry.get('source_family'), query.source_family):
        return False
    if query.source_ref_contains and not _contains(entry.get('source_ref'), query.source_ref_contains):
        return False
    if query.reason_contains and not _contains(entry.get('reason'), query.reason_contains):
        return False
    if query.runtime_ref_contains:
        runtime_refs = entry.get('runtime_refs')
        if not isinstance(runtime_refs, list):
            return False
        needle = query.runtime_ref_contains.casefold()
        if not any(isinstance(item, str) and needle in item.casefold() for item in runtime_refs):
            return False
    return True


def _equals(value: object, expected: str) -> bool:
    return isinstance(value, str) and value.casefold() == expected.casefold()


def _contains(value: object, needle: str) -> bool:
    return isinstance(value, str) and needle.casefold() in value.casefold()


def _as_optional_str(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _as_int(value: object) -> int:
    return value if isinstance(value, int) else 0


def _sortable_timestamp(value: object) -> tuple[int, str]:
    if isinstance(value, str) and value:
        return (1, value)
    return (0, '')


def _default_filename(query: RuntimeReportNavigationQuery, created_at: str | None) -> str:
    stamp = re.sub(r'[^0-9]', '', created_at or _iso_now())[:14]
    slug_parts = [
        query.source_family or None,
        query.artifact_kind or None,
        query.trigger_event or None,
        query.source_ref_contains or None,
        query.runtime_ref_contains or None,
    ]
    slug = '-'.join(_safe(part) for part in slug_parts if part)
    if not slug:
        slug = 'all-packets'
    return f'{slug}__runtime_navigation_{stamp}.md'


def _safe(value: str) -> str:
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportNavigationError(f'Absolute output paths are not allowed: {relative_path}')
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportNavigationError(f'Output path escapes workspace root: {relative_path}') from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
