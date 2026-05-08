"""Read-only browser surfaces over downstream runtime-report navigation outputs.

This module adds a bounded operator browsing layer on top of the E3 packet index and the
F1 navigation/query surface. It remains explicitly downstream from artifacts,
reflections, aggregation witnesses, visibility projections, and navigation packets.
It does not promote any of those surfaces into kernel truth or runtime authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import html
import json
from pathlib import Path
import re

from .runtime_report_crosslinks import (
    KernelRuntimeReportCrosslinker,
    RuntimeReportCrosslinkTarget,
    RuntimeReportCrosslinkView,
    RuntimeReportCrosslinkWriteResult,
    build_target_href,
)
from .runtime_report_navigation import (
    KernelRuntimeReportNavigationError,
    KernelRuntimeReportNavigator,
    RuntimeReportNavigationEntry,
    RuntimeReportNavigationQuery,
    RuntimeReportNavigationResult,
)


class KernelRuntimeReportBrowserError(Exception):
    """Raised when one read-only runtime-report browser request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportBrowserFacetCounts:
    artifact_kinds: tuple[tuple[str, int], ...]
    trigger_events: tuple[tuple[str, int], ...]
    source_families: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class RuntimeReportBrowserResult:
    navigation: RuntimeReportNavigationResult
    facet_counts: RuntimeReportBrowserFacetCounts
    generated_at: str
    read_only_mode: bool = True
    crosslink_view: RuntimeReportCrosslinkView | None = None


@dataclass(frozen=True)
class RuntimeReportBrowserWriteResult:
    markdown_path: str | None
    html_path: str
    json_path: str
    navigation_packet_path: str | None
    crosslink_markdown_path: str | None
    crosslink_json_path: str | None
    result: RuntimeReportBrowserResult


class KernelRuntimeReportBrowser:
    """Provide bounded read-only browsing over downstream runtime-report packet visibility."""

    def __init__(
        self,
        *,
        navigator: KernelRuntimeReportNavigator | None = None,
        crosslinker: KernelRuntimeReportCrosslinker | None = None,
    ) -> None:
        self._navigator = navigator or KernelRuntimeReportNavigator()
        self._crosslinker = crosslinker or KernelRuntimeReportCrosslinker()

    def browse(
        self,
        workspace_root: str | Path,
        query: RuntimeReportNavigationQuery | None = None,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        created_at: str | None = None,
    ) -> RuntimeReportBrowserResult:
        navigation = self._navigator.query_entries(
            workspace_root,
            query,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
        )
        generated_at = created_at or _iso_now()
        return RuntimeReportBrowserResult(
            navigation=navigation,
            facet_counts=_facet_counts(navigation.entries),
            generated_at=generated_at,
            read_only_mode=True,
            crosslink_view=self._crosslinker.build_view(workspace_root, navigation, created_at=generated_at),
        )

    def render_browser_markdown(
        self,
        result: RuntimeReportBrowserResult,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'browser_kind: RUNTIME_REPORT_READ_ONLY_BROWSER',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {result.generated_at}',
            f'packet_index_path: {result.navigation.packet_index_path}',
        ]
        if result.navigation.operator_dashboard_path is not None:
            lines.append(f'operator_dashboard_path: {result.navigation.operator_dashboard_path}')
        lines.extend([
            f'total_entries: {result.navigation.total_entries}',
            f'matched_count: {result.navigation.matched_count}',
            '---',
            '',
            '# Runtime Report Read-Only Browser',
            '',
            '## Query',
            '',
        ])
        query = result.navigation.query
        query_rows = [
            ('Artifact Kind', query.artifact_kind),
            ('Trigger Event', query.trigger_event),
            ('Source Family', query.source_family),
            ('Source Ref Contains', query.source_ref_contains),
            ('Runtime Ref Contains', query.runtime_ref_contains),
            ('Reason Contains', query.reason_contains),
            ('Limit', str(query.limit)),
        ]
        for label, value in query_rows:
            lines.append(f'- {label}: {value if value else "ANY"}')

        lines.extend([
            '',
            '## Coverage',
            '',
            f'- Packet Index Path: {result.navigation.packet_index_path}',
            f'- Operator Dashboard Path: {result.navigation.operator_dashboard_path or "NONE"}',
            f'- Total Indexed Entries: {result.navigation.total_entries}',
            f'- Matched Entries: {result.navigation.matched_count}',
            '',
            '## Matched Facets',
            '',
        ])
        lines.extend(_markdown_counts('Artifact Kinds', result.facet_counts.artifact_kinds))
        lines.extend(_markdown_counts('Trigger Events', result.facet_counts.trigger_events))
        lines.extend(_markdown_counts('Source Families', result.facet_counts.source_families))
        lines.extend(['', '## Matched Packets', ''])
        if not result.navigation.entries:
            lines.append('- No matching packets were found in the read-only browser view.')
        else:
            crosslinks = _crosslink_map(result.crosslink_view)
            for entry in result.navigation.entries:
                lines.extend(_entry_markdown(entry, crosslinks.get(entry.entry_index, ()), output_relative_path=output_relative_path))

        lines.extend([
            '## Boundary',
            '',
            '- This browser is a read-only surface over the downstream packet index and navigation layer.',
            '- It remains downstream from artifacts, reflections, aggregation witnesses, visibility projections, and navigation packets.',
            '- It does not become kernel truth, doctrine, route authority, or runtime authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_browser_html(
        self,
        result: RuntimeReportBrowserResult,
        *,
        title: str = 'Runtime Report Read-Only Browser',
        output_relative_path: str | Path | None = None,
    ) -> str:
        query = result.navigation.query
        facets = result.facet_counts
        crosslinks = _crosslink_map(result.crosslink_view)
        entry_sections = ''.join(
            _entry_html(entry, crosslinks.get(entry.entry_index, ()), output_relative_path=output_relative_path)
            for entry in result.navigation.entries
        ) or ('<p class="empty">No matching packets were found in the read-only browser view.</p>')
        return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.5; }}
    .meta, .boundary, .counts, .query {{ background: #f7f7f8; border: 1px solid #e5e7eb; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }}
    .entry {{ border: 1px solid #e5e7eb; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }}
    .pill {{ display: inline-block; padding: 0.15rem 0.5rem; border-radius: 999px; background: #eef2ff; margin-right: 0.4rem; margin-bottom: 0.3rem; }}
    .muted {{ color: #4b5563; }}
    code {{ background: #f3f4f6; padding: 0.1rem 0.25rem; border-radius: 6px; }}
    ul {{ margin-top: 0.5rem; }}
    h1, h2, h3 {{ margin-bottom: 0.5rem; }}
    .empty {{ padding: 1rem; border: 1px dashed #d1d5db; border-radius: 12px; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <div class=\"meta\">
    <div><strong>Authority Class:</strong> GENERATED_STATE</div>
    <div><strong>Interface Mode:</strong> READ_ONLY</div>
    <div><strong>Generated At:</strong> {html.escape(result.generated_at)}</div>
    <div><strong>Packet Index Path:</strong> <code>{html.escape(result.navigation.packet_index_path)}</code></div>
    <div><strong>Operator Dashboard Path:</strong> <code>{html.escape(result.navigation.operator_dashboard_path or 'NONE')}</code></div>
  </div>
  <div class=\"query\">
    <h2>Query</h2>
    <ul>
      <li><strong>Artifact Kind:</strong> {html.escape(query.artifact_kind or 'ANY')}</li>
      <li><strong>Trigger Event:</strong> {html.escape(query.trigger_event or 'ANY')}</li>
      <li><strong>Source Family:</strong> {html.escape(query.source_family or 'ANY')}</li>
      <li><strong>Source Ref Contains:</strong> {html.escape(query.source_ref_contains or 'ANY')}</li>
      <li><strong>Runtime Ref Contains:</strong> {html.escape(query.runtime_ref_contains or 'ANY')}</li>
      <li><strong>Reason Contains:</strong> {html.escape(query.reason_contains or 'ANY')}</li>
      <li><strong>Limit:</strong> {query.limit}</li>
    </ul>
  </div>
  <div class=\"counts\">
    <h2>Coverage</h2>
    <ul>
      <li><strong>Total Indexed Entries:</strong> {result.navigation.total_entries}</li>
      <li><strong>Matched Entries:</strong> {result.navigation.matched_count}</li>
    </ul>
    <h3>Matched Artifact Kinds</h3>
    {_counts_html(facets.artifact_kinds)}
    <h3>Matched Trigger Events</h3>
    {_counts_html(facets.trigger_events)}
    <h3>Matched Source Families</h3>
    {_counts_html(facets.source_families)}
  </div>
  <section>
    <h2>Matched Packets</h2>
    {entry_sections}
  </section>
  <div class=\"boundary\">
    <h2>Boundary</h2>
    <ul>
      <li>This browser is a read-only surface over the downstream packet index and navigation layer.</li>
      <li>It remains downstream from artifacts, reflections, aggregation witnesses, visibility projections, and navigation packets.</li>
      <li>It does not become kernel truth, doctrine, route authority, or runtime authority.</li>
    </ul>
  </div>
</body>
</html>
"""

    def render_browser_json(self, result: RuntimeReportBrowserResult) -> str:
        crosslinks = _crosslink_map(result.crosslink_view)
        payload = {
            'browser_kind': 'RUNTIME_REPORT_READ_ONLY_BROWSER',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': result.generated_at,
            'packet_index_path': result.navigation.packet_index_path,
            'operator_dashboard_path': result.navigation.operator_dashboard_path,
            'total_entries': result.navigation.total_entries,
            'matched_count': result.navigation.matched_count,
            'query': {
                'artifact_kind': result.navigation.query.artifact_kind,
                'trigger_event': result.navigation.query.trigger_event,
                'source_family': result.navigation.query.source_family,
                'source_ref_contains': result.navigation.query.source_ref_contains,
                'runtime_ref_contains': result.navigation.query.runtime_ref_contains,
                'reason_contains': result.navigation.query.reason_contains,
                'limit': result.navigation.query.limit,
            },
            'facet_counts': {
                'artifact_kinds': list(result.facet_counts.artifact_kinds),
                'trigger_events': list(result.facet_counts.trigger_events),
                'source_families': list(result.facet_counts.source_families),
            },
            'entries': [
                {
                    'entry_index': entry.entry_index,
                    'created_at': entry.created_at,
                    'trigger_event': entry.trigger_event,
                    'artifact_kind': entry.artifact_kind,
                    'source_ref': entry.source_ref,
                    'source_family': entry.source_family,
                    'reason': entry.reason,
                    'artifact_relative_output_path': entry.artifact_relative_output_path,
                    'runtime_refs': list(entry.runtime_refs),
                    'governance_ledger_path': entry.governance_ledger_path,
                    'operator_summary_path': entry.operator_summary_path,
                    'aggregation_event_id': entry.aggregation_event_id,
                    'system_ledger_path': entry.system_ledger_path,
                    'operator_rollup_path': entry.operator_rollup_path,
                    'operator_dashboard_path': entry.operator_dashboard_path,
                    'crosslinks': [
                        {
                            'target_kind': target.target_kind,
                            'label': target.label,
                            'relative_path': target.relative_path,
                            'exists': target.exists,
                        }
                        for target in crosslinks.get(entry.entry_index, ())
                    ],
                }
                for entry in result.navigation.entries
            ],
            'boundary': [
                'Read-only surface over downstream packet index and navigation layer.',
                'Remains downstream from artifacts, reflections, aggregation witnesses, visibility projections, and navigation packets.',
                'Does not become kernel truth, doctrine, route authority, or runtime authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_browser_bundle(
        self,
        workspace_root: str | Path,
        query: RuntimeReportNavigationQuery | None = None,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        browser_dir: str = 'ION/05_context/runtime_reports/governance/browser',
        output_stem: str | None = None,
        created_at: str | None = None,
        write_navigation_packet: bool = False,
        write_crosslink_packet: bool = False,
    ) -> RuntimeReportBrowserWriteResult:
        generated_at = created_at or _iso_now()
        root = Path(workspace_root).resolve()
        result = self.browse(
            root,
            query,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            created_at=generated_at,
        )
        browser_relative_dir = Path(browser_dir)
        browser_resolved_dir = _resolve_relative_file(root, browser_relative_dir)
        browser_resolved_dir.mkdir(parents=True, exist_ok=True)
        stem = output_stem or _default_stem(result.navigation.query, generated_at)

        markdown_relative = browser_relative_dir / f'{stem}.md'
        markdown_path = _resolve_relative_file(root, markdown_relative)
        markdown_path.write_text(
            self.render_browser_markdown(result, output_relative_path=markdown_relative),
            encoding='utf-8',
        )

        html_relative = browser_relative_dir / f'{stem}.html'
        html_path = _resolve_relative_file(root, html_relative)
        html_path.write_text(
            self.render_browser_html(result, output_relative_path=html_relative),
            encoding='utf-8',
        )

        json_relative = browser_relative_dir / f'{stem}.json'
        json_path = _resolve_relative_file(root, json_relative)
        json_path.write_text(self.render_browser_json(result), encoding='utf-8')

        navigation_packet_relative: str | None = None
        if write_navigation_packet:
            navigation_path = self._navigator.write_navigation_packet(
                root,
                query,
                packet_index_path=packet_index_path,
                operator_dashboard_path=operator_dashboard_path,
                created_at=generated_at,
            )
            navigation_packet_relative = str(navigation_path.relative_to(root))

        crosslink_write: RuntimeReportCrosslinkWriteResult | None = None
        if write_crosslink_packet:
            crosslink_write = self._crosslinker.write_crosslink_packet(
                root,
                result.navigation,
                output_stem=stem,
                created_at=generated_at,
            )

        return RuntimeReportBrowserWriteResult(
            markdown_path=str(markdown_relative),
            html_path=str(html_relative),
            json_path=str(json_relative),
            navigation_packet_path=navigation_packet_relative,
            crosslink_markdown_path=(crosslink_write.markdown_path if crosslink_write is not None else None),
            crosslink_json_path=(crosslink_write.json_path if crosslink_write is not None else None),
            result=result,
        )


IonRuntimeReportBrowser = KernelRuntimeReportBrowser


def _crosslink_map(view: RuntimeReportCrosslinkView | None) -> dict[int, tuple[RuntimeReportCrosslinkTarget, ...]]:
    if view is None:
        return {}
    return {entry.entry_index: entry.crosslinks for entry in view.entries}


def _facet_counts(entries: tuple[RuntimeReportNavigationEntry, ...]) -> RuntimeReportBrowserFacetCounts:
    return RuntimeReportBrowserFacetCounts(
        artifact_kinds=_count_tuples(entry.artifact_kind for entry in entries),
        trigger_events=_count_tuples(entry.trigger_event for entry in entries),
        source_families=_count_tuples(entry.source_family for entry in entries),
    )


def _count_tuples(values) -> tuple[tuple[str, int], ...]:
    counts: dict[str, int] = {}
    for value in values:
        if isinstance(value, str) and value:
            counts[value] = counts.get(value, 0) + 1
    return tuple(sorted(counts.items()))


def _markdown_counts(label: str, counts: tuple[tuple[str, int], ...]) -> list[str]:
    lines = [f'### {label}', '']
    if not counts:
        lines.append('- NONE')
        lines.append('')
        return lines
    for key, value in counts:
        lines.append(f'- {key}: {value}')
    lines.append('')
    return lines


def _entry_markdown(
    entry: RuntimeReportNavigationEntry,
    crosslinks: tuple[RuntimeReportCrosslinkTarget, ...],
    *,
    output_relative_path: str | Path | None = None,
) -> list[str]:
    lines = [
        f'### {entry.trigger_event} — {entry.source_ref}',
        '',
        f'- Artifact Kind: {entry.artifact_kind}',
        f'- Source Family: {entry.source_family}',
        f'- Reason: {entry.reason or "NONE"}',
        f'- Artifact Path: {entry.artifact_relative_output_path}',
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
    ]
    if entry.runtime_refs:
        lines.append('- Runtime Refs:')
        lines.extend(f'  - {item}' for item in entry.runtime_refs)
    if crosslinks:
        lines.append('- Crosslinks:')
        for target in crosslinks:
            lines.append(f'  - {target.label}: {_markdown_target(target, output_relative_path)}')
    lines.append('')
    return lines


def _entry_html(
    entry: RuntimeReportNavigationEntry,
    crosslinks: tuple[RuntimeReportCrosslinkTarget, ...],
    *,
    output_relative_path: str | Path | None = None,
) -> str:
    runtime_refs = ''.join(f'<li><code>{html.escape(item)}</code></li>' for item in entry.runtime_refs)
    runtime_block = f'<div><strong>Runtime Refs</strong><ul>{runtime_refs}</ul></div>' if runtime_refs else ''
    crosslink_block = ''
    if crosslinks:
        items = ''.join(
            f'<li><strong>{html.escape(target.label)}:</strong> {_html_target(target, output_relative_path)}</li>'
            for target in crosslinks
        )
        crosslink_block = f'<div><strong>Crosslinks</strong><ul>{items}</ul></div>'
    return f"""
    <article class=\"entry\">
      <h3>{html.escape(entry.trigger_event)} — {html.escape(entry.source_ref)}</h3>
      <div class=\"muted\">Created: {html.escape(entry.created_at or 'UNKNOWN')}</div>
      <p>
        <span class=\"pill\">Artifact Kind: {html.escape(entry.artifact_kind)}</span>
        <span class=\"pill\">Source Family: {html.escape(entry.source_family)}</span>
      </p>
      <ul>
        <li><strong>Reason:</strong> {html.escape(entry.reason or 'NONE')}</li>
        <li><strong>Artifact Path:</strong> <code>{html.escape(entry.artifact_relative_output_path)}</code></li>
        <li><strong>Packet Index Pointer:</strong> <code>{html.escape(entry.packet_index_pointer or 'NONE')}</code></li>
        <li><strong>Governance Ledger Path:</strong> <code>{html.escape(entry.governance_ledger_path or 'NONE')}</code></li>
        <li><strong>Governance Ledger Entry Index:</strong> {html.escape(str(entry.governance_ledger_entry_index) if entry.governance_ledger_entry_index is not None else 'NONE')}</li>
        <li><strong>Governance Summary Path:</strong> <code>{html.escape(entry.operator_summary_path or 'NONE')}</code></li>
        <li><strong>Governance Summary Anchor:</strong> <code>{html.escape(entry.operator_summary_anchor or 'NONE')}</code></li>
        <li><strong>Aggregation Event Id:</strong> {html.escape(entry.aggregation_event_id or 'NONE')}</li>
        <li><strong>System Ledger Path:</strong> <code>{html.escape(entry.system_ledger_path or 'NONE')}</code></li>
        <li><strong>System Ledger Entry Index:</strong> {html.escape(str(entry.system_ledger_entry_index) if entry.system_ledger_entry_index is not None else 'NONE')}</li>
        <li><strong>Operator Rollup Path:</strong> <code>{html.escape(entry.operator_rollup_path or 'NONE')}</code></li>
        <li><strong>Operator Rollup Anchor:</strong> <code>{html.escape(entry.operator_rollup_anchor or 'NONE')}</code></li>
        <li><strong>Operator Dashboard Anchor:</strong> <code>{html.escape(entry.operator_dashboard_anchor or 'NONE')}</code></li>
      </ul>
      {runtime_block}
      {crosslink_block}
    </article>
    """


def _markdown_target(target: RuntimeReportCrosslinkTarget, output_relative_path: str | Path | None) -> str:
    suffix = '' if target.exists else ' (missing)'
    if output_relative_path is None:
        return f'{target.target_ref}{suffix}'
    href = build_target_href(output_relative_path, target.relative_path, target.anchor_fragment)
    return f'[{target.target_ref}]({href}){suffix}'


def _html_target(target: RuntimeReportCrosslinkTarget, output_relative_path: str | Path | None) -> str:
    suffix = '' if target.exists else ' <span class="muted">(missing)</span>'
    label = html.escape(target.target_ref)
    if output_relative_path is None:
        return f'<code>{label}</code>{suffix}'
    href = html.escape(build_target_href(output_relative_path, target.relative_path, target.anchor_fragment))
    return f'<a href="{href}"><code>{label}</code></a>{suffix}'


def _counts_html(counts: tuple[tuple[str, int], ...]) -> str:
    if not counts:
        return '<p class="empty">NONE</p>'
    return '<p>' + ''.join(
        f'<span class="pill">{html.escape(key)}: {value}</span>'
        for key, value in counts
    ) + '</p>'


def _default_stem(query: RuntimeReportNavigationQuery, created_at: str) -> str:
    stamp = re.sub(r'[^0-9]', '', created_at)[:14]
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
    return f'{slug}__runtime_browser_{stamp}'


def _safe(value: str) -> str:
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportBrowserError(f'Absolute output paths are not allowed: {relative_path}')
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportBrowserError(f'Output path escapes workspace root: {relative_path}') from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
