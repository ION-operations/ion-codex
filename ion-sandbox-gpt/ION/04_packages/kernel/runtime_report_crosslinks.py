"""Read-only cross-linking over downstream runtime-report navigation outputs.

This module builds bounded cross-link views so browser and packet surfaces can move more
 directly among related generated artifacts, dashboards, ledgers, summaries, and rollups.
It remains explicitly downstream from artifacts, governance reflections, aggregation
witnesses, visibility projections, navigation packets, and browser views.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from os.path import relpath
from pathlib import Path
import re

from .runtime_report_anchors import join_relative_target, ledger_row_pointer
from .runtime_report_navigation import RuntimeReportNavigationEntry, RuntimeReportNavigationResult


class KernelRuntimeReportCrosslinkError(Exception):
    """Raised when one runtime-report cross-link view cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportCrosslinkTarget:
    target_kind: str
    label: str
    relative_path: str
    exists: bool
    anchor_kind: str | None = None
    anchor_fragment: str | None = None

    @property
    def target_ref(self) -> str:
        return join_relative_target(self.relative_path, self.anchor_fragment)


@dataclass(frozen=True)
class RuntimeReportCrosslinkedEntry:
    entry_index: int
    trigger_event: str
    artifact_kind: str
    source_ref: str
    crosslinks: tuple[RuntimeReportCrosslinkTarget, ...]


@dataclass(frozen=True)
class RuntimeReportCrosslinkView:
    packet_index_path: str
    operator_dashboard_path: str | None
    generated_at: str
    read_only_mode: bool
    entries: tuple[RuntimeReportCrosslinkedEntry, ...]


@dataclass(frozen=True)
class RuntimeReportCrosslinkWriteResult:
    markdown_path: str
    json_path: str
    view: RuntimeReportCrosslinkView


class KernelRuntimeReportCrosslinker:
    """Build bounded read-only cross-link views over downstream runtime-report packets."""

    def build_view(
        self,
        workspace_root: str | Path,
        navigation: RuntimeReportNavigationResult,
        *,
        created_at: str | None = None,
    ) -> RuntimeReportCrosslinkView:
        root = Path(workspace_root).resolve()
        return RuntimeReportCrosslinkView(
            packet_index_path=navigation.packet_index_path,
            operator_dashboard_path=navigation.operator_dashboard_path,
            generated_at=created_at or _iso_now(),
            read_only_mode=True,
            entries=tuple(self._crosslink_entry(root, navigation, entry) for entry in navigation.entries),
        )

    def render_markdown(
        self,
        view: RuntimeReportCrosslinkView,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'crosslink_kind: RUNTIME_REPORT_CROSSLINK_PACKET',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {view.generated_at}',
            f'packet_index_path: {view.packet_index_path}',
        ]
        if view.operator_dashboard_path is not None:
            lines.append(f'operator_dashboard_path: {view.operator_dashboard_path}')
        lines.extend([
            f'entry_count: {len(view.entries)}',
            '---',
            '',
            '# Runtime Report Crosslink Packet',
            '',
            '## Coverage',
            '',
            f'- Packet Index Path: {view.packet_index_path}',
            f'- Operator Dashboard Path: {view.operator_dashboard_path or "NONE"}',
            f'- Entry Count: {len(view.entries)}',
            '',
            '## Crosslinked Packets',
            '',
        ])
        if not view.entries:
            lines.append('- No crosslinked packets were found in the read-only browser scope.')
        else:
            for entry in view.entries:
                lines.extend([
                    f'### {entry.trigger_event} — {entry.source_ref}',
                    '',
                    f'- Artifact Kind: {entry.artifact_kind}',
                ])
                if not entry.crosslinks:
                    lines.append('- Crosslinks: NONE')
                    lines.append('')
                    continue
                lines.append('- Crosslinks:')
                for target in entry.crosslinks:
                    lines.append(f'  - {target.label}: {_markdown_link(target, output_relative_path)}')
                lines.append('')
        lines.extend([
            '## Boundary',
            '',
            '- This packet is a read-only cross-link view over downstream runtime-report witness outputs.',
            '- It remains downstream from artifacts, governance reflections, aggregation witnesses, visibility projections, navigation packets, and browser views.',
            '- It does not become kernel truth, doctrine, route authority, or runtime authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, view: RuntimeReportCrosslinkView) -> str:
        payload = {
            'crosslink_kind': 'RUNTIME_REPORT_CROSSLINK_PACKET',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': view.generated_at,
            'packet_index_path': view.packet_index_path,
            'operator_dashboard_path': view.operator_dashboard_path,
            'entry_count': len(view.entries),
            'entries': [
                {
                    'entry_index': entry.entry_index,
                    'trigger_event': entry.trigger_event,
                    'artifact_kind': entry.artifact_kind,
                    'source_ref': entry.source_ref,
                    'crosslinks': [
                        {
                            'target_kind': target.target_kind,
                            'label': target.label,
                            'relative_path': target.relative_path,
                            'anchor_kind': target.anchor_kind,
                            'anchor_fragment': target.anchor_fragment,
                            'target_ref': target.target_ref,
                            'exists': target.exists,
                        }
                        for target in entry.crosslinks
                    ],
                }
                for entry in view.entries
            ],
            'boundary': [
                'Read-only cross-link view over downstream runtime-report witness outputs.',
                'Remains downstream from artifacts, reflections, aggregation witnesses, visibility projections, navigation packets, and browser views.',
                'Does not become kernel truth, doctrine, route authority, or runtime authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_crosslink_packet(
        self,
        workspace_root: str | Path,
        navigation: RuntimeReportNavigationResult,
        *,
        output_stem: str | None = None,
        crosslinks_dir: str = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        created_at: str | None = None,
    ) -> RuntimeReportCrosslinkWriteResult:
        root = Path(workspace_root).resolve()
        view = self.build_view(root, navigation, created_at=created_at)
        relative_dir = Path(crosslinks_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stem = output_stem or _default_stem(navigation, view.generated_at)
        markdown_relative = relative_dir / f'{stem}.md'
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        markdown_resolved.write_text(
            self.render_markdown(view, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        json_relative = relative_dir / f'{stem}.json'
        json_resolved = _resolve_relative_file(root, json_relative)
        json_resolved.write_text(self.render_json(view), encoding='utf-8')
        return RuntimeReportCrosslinkWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            view=view,
        )

    def _crosslink_entry(
        self,
        root: Path,
        navigation: RuntimeReportNavigationResult,
        entry: RuntimeReportNavigationEntry,
    ) -> RuntimeReportCrosslinkedEntry:
        seen: set[tuple[str, str]] = set()
        targets: list[RuntimeReportCrosslinkTarget] = []
        for target in (
            _make_target(root, 'ARTIFACT_REPORT', 'Artifact Report', entry.artifact_relative_output_path, _fragment(entry.artifact_anchor)),
            _make_target(root, 'PACKET_INDEX', 'Packet Index', navigation.packet_index_path, entry.packet_index_pointer, anchor_kind='JSON_POINTER'),
            _make_target(
                root,
                'OPERATOR_DASHBOARD',
                'Operator Dashboard',
                entry.operator_dashboard_path or navigation.operator_dashboard_path,
                _fragment(entry.operator_dashboard_anchor),
            ),
            _make_target(
                root,
                'GOVERNANCE_LEDGER',
                'Governance Ledger',
                entry.governance_ledger_path,
                (ledger_row_pointer(entry.governance_ledger_entry_index) if entry.governance_ledger_entry_index is not None else None),
                anchor_kind='JSON_POINTER',
            ),
            _make_target(root, 'GOVERNANCE_SUMMARY', 'Governance Summary', entry.operator_summary_path, _fragment(entry.operator_summary_anchor)),
            _make_target(
                root,
                'SYSTEM_LEDGER',
                'System Ledger',
                entry.system_ledger_path,
                (ledger_row_pointer(entry.system_ledger_entry_index) if entry.system_ledger_entry_index is not None else None),
                anchor_kind='JSON_POINTER',
            ),
            _make_target(root, 'OPERATOR_ROLLUP', 'Operator Rollup', entry.operator_rollup_path, _fragment(entry.operator_rollup_anchor)),
        ):
            if target is None:
                continue
            key = (target.target_kind, target.target_ref)
            if key in seen:
                continue
            seen.add(key)
            targets.append(target)
        return RuntimeReportCrosslinkedEntry(
            entry_index=entry.entry_index,
            trigger_event=entry.trigger_event,
            artifact_kind=entry.artifact_kind,
            source_ref=entry.source_ref,
            crosslinks=tuple(targets),
        )


IonRuntimeReportCrosslinker = KernelRuntimeReportCrosslinker


def build_target_href(output_relative_path: str | Path, target_relative_path: str, anchor_fragment: str | None = None) -> str:
    origin_dir = Path(output_relative_path).parent
    base = Path(relpath(target_relative_path, start=origin_dir)).as_posix()
    return join_relative_target(base, anchor_fragment)


def _markdown_link(target: RuntimeReportCrosslinkTarget, output_relative_path: str | Path | None) -> str:
    suffix = '' if target.exists else ' (missing)'
    label = target.target_ref
    if output_relative_path is None:
        return f'{label}{suffix}'
    href = build_target_href(output_relative_path, target.relative_path, target.anchor_fragment)
    return f'[{label}]({href}){suffix}'


def _fragment(anchor_id: str | None) -> str | None:
    return f'#{anchor_id}' if anchor_id else None


def _make_target(
    root: Path,
    target_kind: str,
    label: str,
    relative_path: str | None,
    anchor_fragment: str | None,
    *,
    anchor_kind: str = 'MARKDOWN_ANCHOR',
) -> RuntimeReportCrosslinkTarget | None:
    if not relative_path:
        return None
    normalized = str(relative_path)
    return RuntimeReportCrosslinkTarget(
        target_kind=target_kind,
        label=label,
        relative_path=normalized,
        exists=_path_exists(root, normalized),
        anchor_kind=(anchor_kind if anchor_fragment else None),
        anchor_fragment=anchor_fragment,
    )


def _path_exists(root: Path, relative_path: str) -> bool:
    try:
        return _resolve_relative_file(root, Path(relative_path)).exists()
    except KernelRuntimeReportCrosslinkError:
        return False


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportCrosslinkError(f'Absolute output paths are not allowed: {relative_path}')
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportCrosslinkError(f'Output path escapes workspace root: {relative_path}') from exc
    return resolved


def _default_stem(navigation: RuntimeReportNavigationResult, created_at: str) -> str:
    stamp = re.sub(r'[^0-9]', '', created_at)[:14]
    query = navigation.query
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
    return f'{slug}__runtime_crosslinks_{stamp}'


def _safe(value: str) -> str:
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime'


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
