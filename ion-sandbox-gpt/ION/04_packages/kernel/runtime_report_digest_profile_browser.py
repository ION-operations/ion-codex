"""Read-only browser surfaces over named runtime-report digest-profile catalog entries.

This module adds a bounded operator browsing layer on top of the H3 digest-profile
catalog/index surface. It loads lawful profile definitions through the existing H2/H3
pipeline, renders richer read-only browser packets, and remains explicitly downstream
from profile definitions and the digests rendered through them.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import html
import json
from pathlib import Path
import re
from typing import Sequence

from .runtime_report_digest_profile_catalog import (
    KernelRuntimeReportDigestProfileCatalog,
    RuntimeReportDigestProfileCatalog,
    RuntimeReportDigestProfileCatalogEntry,
    RuntimeReportDigestProfileCatalogQuery,
)
from .runtime_report_digest_profiles import (
    KernelRuntimeReportDigestProfiler,
    RuntimeReportDigestProfileSelector,
)


class KernelRuntimeReportDigestProfileBrowserError(Exception):
    """Raised when one digest-profile browser request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportDigestProfileBrowserSelectorView:
    label: str
    source_ref: str | None
    source_ref_contains: str | None
    trigger_event: str | None
    artifact_kind: str | None
    source_family: str | None
    limit: int | None


@dataclass(frozen=True)
class RuntimeReportDigestProfileBrowserEntry:
    profile_name: str
    description: str
    tags: tuple[str, ...]
    selector_count: int
    selector_labels: tuple[str, ...]
    markdown_path: str | None
    json_path: str
    selectors: tuple[RuntimeReportDigestProfileBrowserSelectorView, ...]


@dataclass(frozen=True)
class RuntimeReportDigestProfileBrowserFacetCounts:
    tags: tuple[tuple[str, int], ...]
    selector_labels: tuple[tuple[str, int], ...]
    artifact_kinds: tuple[tuple[str, int], ...]
    trigger_events: tuple[tuple[str, int], ...]
    source_families: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class RuntimeReportDigestProfileBrowserResult:
    catalog: RuntimeReportDigestProfileCatalog
    entries: tuple[RuntimeReportDigestProfileBrowserEntry, ...]
    facet_counts: RuntimeReportDigestProfileBrowserFacetCounts
    generated_at: str
    read_only_mode: bool = True


@dataclass(frozen=True)
class RuntimeReportDigestProfileBrowserWriteResult:
    markdown_path: str
    html_path: str
    json_path: str
    catalog_packet_path: str | None
    result: RuntimeReportDigestProfileBrowserResult


class KernelRuntimeReportDigestProfileBrowser:
    """Provide bounded read-only browsing over named runtime-report digest profiles."""

    def __init__(
        self,
        *,
        cataloger: KernelRuntimeReportDigestProfileCatalog | None = None,
        profiler: KernelRuntimeReportDigestProfiler | None = None,
    ) -> None:
        self._cataloger = cataloger or KernelRuntimeReportDigestProfileCatalog()
        self._profiler = profiler or KernelRuntimeReportDigestProfiler()

    def browse(
        self,
        workspace_root: str | Path,
        query: RuntimeReportDigestProfileCatalogQuery | None = None,
        *,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        created_at: str | None = None,
    ) -> RuntimeReportDigestProfileBrowserResult:
        root = Path(workspace_root).resolve()
        catalog = self._cataloger.query_catalog(
            root,
            query,
            profiles_dir=profiles_dir,
            created_at=created_at,
        )
        entries = tuple(self._load_entry(root, entry) for entry in catalog.entries)
        generated_at = created_at or _iso_now()
        return RuntimeReportDigestProfileBrowserResult(
            catalog=catalog,
            entries=entries,
            facet_counts=_facet_counts(entries),
            generated_at=generated_at,
            read_only_mode=True,
        )

    def render_browser_markdown(
        self,
        result: RuntimeReportDigestProfileBrowserResult,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        query = result.catalog.query
        lines = [
            '---',
            'browser_kind: RUNTIME_REPORT_DIGEST_PROFILE_BROWSER',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {result.generated_at}',
            f'profiles_dir: {result.catalog.profiles_dir}',
            f'total_profiles: {result.catalog.total_profiles}',
            f'matched_count: {result.catalog.matched_count}',
        ]
        if query.profile_name_contains is not None:
            lines.append(f'profile_name_contains: {query.profile_name_contains}')
        if query.tag is not None:
            lines.append(f'tag: {query.tag}')
        if query.selector_label_contains is not None:
            lines.append(f'selector_label_contains: {query.selector_label_contains}')
        if query.description_contains is not None:
            lines.append(f'description_contains: {query.description_contains}')
        if query.limit is not None:
            lines.append(f'browser_limit: {query.limit}')
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Digest Profile Browser',
            '',
            'This browser is a bounded read-only surface over named runtime-report digest profiles.',
            '',
            '## Query',
            '',
            f'- Profile Name Contains: {query.profile_name_contains or "ANY"}',
            f'- Tag: {query.tag or "ANY"}',
            f'- Selector Label Contains: {query.selector_label_contains or "ANY"}',
            f'- Description Contains: {query.description_contains or "ANY"}',
            f'- Limit: {query.limit if query.limit is not None else "ANY"}',
            '',
            '## Coverage',
            '',
            f'- Profiles Directory: {result.catalog.profiles_dir}',
            f'- Total Profiles: {result.catalog.total_profiles}',
            f'- Matched Profiles: {result.catalog.matched_count}',
            '',
            '## Matched Facets',
            '',
        ])
        lines.extend(_markdown_counts('Tags', result.facet_counts.tags))
        lines.extend(_markdown_counts('Selector Labels', result.facet_counts.selector_labels))
        lines.extend(_markdown_counts('Artifact Kinds', result.facet_counts.artifact_kinds))
        lines.extend(_markdown_counts('Trigger Events', result.facet_counts.trigger_events))
        lines.extend(_markdown_counts('Source Families', result.facet_counts.source_families))
        lines.extend(['', '## Matched Profiles', ''])
        if not result.entries:
            lines.extend([
                'No named digest profiles matched the read-only browser query.',
                '',
            ])
        for index, entry in enumerate(result.entries, start=1):
            lines.extend([
                f'### {index}. {entry.profile_name}',
                '',
                f'- Selector Count: {entry.selector_count}',
                f'- Tags: {", ".join(entry.tags) if entry.tags else "NONE"}',
                f'- Description: {entry.description or "NONE"}',
                f'- Definition Markdown Path: {entry.markdown_path or "NONE"}',
                f'- Definition JSON Path: {entry.json_path}',
            ])
            if entry.selectors:
                lines.append('- Selector Detail:')
                for selector in entry.selectors:
                    lines.extend([
                        f'  - Label: {selector.label}',
                        f'    - Source Ref: {selector.source_ref or "NONE"}',
                        f'    - Source Ref Contains: {selector.source_ref_contains or "NONE"}',
                        f'    - Trigger Event: {selector.trigger_event or "NONE"}',
                        f'    - Artifact Kind: {selector.artifact_kind or "NONE"}',
                        f'    - Source Family: {selector.source_family or "NONE"}',
                        f'    - Limit: {selector.limit if selector.limit is not None else "NONE"}',
                    ])
            else:
                lines.append('- Selector Detail: NONE')
            lines.append('')
        lines.extend([
            '## Boundary',
            '',
            '- This browser is a read-only surface over digest-profile catalog entries and lawful profile definitions.',
            '- It remains downstream from digest profiles and from the digests rendered through them.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, or browser authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_browser_html(
        self,
        result: RuntimeReportDigestProfileBrowserResult,
        *,
        title: str = 'Runtime Report Digest Profile Browser',
        output_relative_path: str | Path | None = None,
    ) -> str:
        query = result.catalog.query
        entry_sections = ''.join(
            _entry_html(entry, output_relative_path=output_relative_path)
            for entry in result.entries
        ) or '<p class="empty">No named digest profiles matched the read-only browser query.</p>'
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
    .selector {{ margin: 0.5rem 0 0.75rem; padding-left: 1rem; border-left: 3px solid #e5e7eb; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <div class=\"meta\">
    <div><strong>Authority Class:</strong> GENERATED_STATE</div>
    <div><strong>Interface Mode:</strong> READ_ONLY</div>
    <div><strong>Generated At:</strong> {html.escape(result.generated_at)}</div>
    <div><strong>Profiles Directory:</strong> <code>{html.escape(result.catalog.profiles_dir)}</code></div>
  </div>
  <div class=\"query\">
    <h2>Query</h2>
    <ul>
      <li><strong>Profile Name Contains:</strong> {html.escape(query.profile_name_contains or 'ANY')}</li>
      <li><strong>Tag:</strong> {html.escape(query.tag or 'ANY')}</li>
      <li><strong>Selector Label Contains:</strong> {html.escape(query.selector_label_contains or 'ANY')}</li>
      <li><strong>Description Contains:</strong> {html.escape(query.description_contains or 'ANY')}</li>
      <li><strong>Limit:</strong> {query.limit if query.limit is not None else 'ANY'}</li>
    </ul>
  </div>
  <div class=\"counts\">
    <h2>Coverage</h2>
    <ul>
      <li><strong>Total Profiles:</strong> {result.catalog.total_profiles}</li>
      <li><strong>Matched Profiles:</strong> {result.catalog.matched_count}</li>
    </ul>
    <h3>Tags</h3>
    {_counts_html(result.facet_counts.tags)}
    <h3>Selector Labels</h3>
    {_counts_html(result.facet_counts.selector_labels)}
    <h3>Artifact Kinds</h3>
    {_counts_html(result.facet_counts.artifact_kinds)}
    <h3>Trigger Events</h3>
    {_counts_html(result.facet_counts.trigger_events)}
    <h3>Source Families</h3>
    {_counts_html(result.facet_counts.source_families)}
  </div>
  <section>
    <h2>Matched Profiles</h2>
    {entry_sections}
  </section>
  <div class=\"boundary\">
    <h2>Boundary</h2>
    <ul>
      <li>This browser is a read-only surface over digest-profile catalog entries and lawful profile definitions.</li>
      <li>It remains downstream from digest profiles and from the digests rendered through them.</li>
      <li>It does not become kernel truth, doctrine, route authority, runtime authority, or browser authority.</li>
    </ul>
  </div>
</body>
</html>
"""

    def render_browser_json(self, result: RuntimeReportDigestProfileBrowserResult) -> str:
        payload = {
            'browser_kind': 'RUNTIME_REPORT_DIGEST_PROFILE_BROWSER',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': result.generated_at,
            'profiles_dir': result.catalog.profiles_dir,
            'total_profiles': result.catalog.total_profiles,
            'matched_count': result.catalog.matched_count,
            'query': {
                'profile_name_contains': result.catalog.query.profile_name_contains,
                'tag': result.catalog.query.tag,
                'selector_label_contains': result.catalog.query.selector_label_contains,
                'description_contains': result.catalog.query.description_contains,
                'limit': result.catalog.query.limit,
            },
            'facet_counts': {
                'tags': [[name, count] for name, count in result.facet_counts.tags],
                'selector_labels': [[name, count] for name, count in result.facet_counts.selector_labels],
                'artifact_kinds': [[name, count] for name, count in result.facet_counts.artifact_kinds],
                'trigger_events': [[name, count] for name, count in result.facet_counts.trigger_events],
                'source_families': [[name, count] for name, count in result.facet_counts.source_families],
            },
            'entries': [
                {
                    'profile_name': entry.profile_name,
                    'description': entry.description,
                    'tags': list(entry.tags),
                    'selector_count': entry.selector_count,
                    'selector_labels': list(entry.selector_labels),
                    'markdown_path': entry.markdown_path,
                    'json_path': entry.json_path,
                    'selectors': [
                        {
                            'label': selector.label,
                            'source_ref': selector.source_ref,
                            'source_ref_contains': selector.source_ref_contains,
                            'trigger_event': selector.trigger_event,
                            'artifact_kind': selector.artifact_kind,
                            'source_family': selector.source_family,
                            'limit': selector.limit,
                        }
                        for selector in entry.selectors
                    ],
                }
                for entry in result.entries
            ],
            'boundary': [
                'Read-only surface over digest-profile catalog entries and lawful profile definitions.',
                'Remains downstream from digest profiles and from the digests rendered through them.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, or browser authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_browser_bundle(
        self,
        workspace_root: str | Path,
        query: RuntimeReportDigestProfileCatalogQuery | None = None,
        *,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/browser',
        output_stem: str | None = None,
        created_at: str | None = None,
        write_catalog_packet: bool = False,
        catalogs_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/catalog',
    ) -> RuntimeReportDigestProfileBrowserWriteResult:
        root = Path(workspace_root).resolve()
        active_query = query or RuntimeReportDigestProfileCatalogQuery()
        result = self.browse(root, active_query, profiles_dir=profiles_dir, created_at=created_at)
        relative_dir = Path(browser_dir)
        resolved_dir = _resolve_relative_dir(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stamp = re.sub(r'[^0-9]', '', result.generated_at)[:14]
        stem = output_stem or f'runtime_report_digest_profile_browser_{stamp}'
        markdown_relative = relative_dir / f'{stem}.md'
        html_relative = relative_dir / f'{stem}.html'
        json_relative = relative_dir / f'{stem}.json'
        _resolve_relative_file(root, markdown_relative).write_text(
            self.render_browser_markdown(result, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        _resolve_relative_file(root, html_relative).write_text(
            self.render_browser_html(result, output_relative_path=html_relative),
            encoding='utf-8',
        )
        _resolve_relative_file(root, json_relative).write_text(
            self.render_browser_json(result),
            encoding='utf-8',
        )
        catalog_packet_path: str | None = None
        if write_catalog_packet:
            catalog_packet = self._cataloger.write_catalog_packet(
                root,
                active_query,
                profiles_dir=profiles_dir,
                catalogs_dir=catalogs_dir,
                output_stem=f'{stem}_catalog',
                created_at=result.generated_at,
            )
            catalog_packet_path = catalog_packet.markdown_path
        return RuntimeReportDigestProfileBrowserWriteResult(
            markdown_path=str(markdown_relative),
            html_path=str(html_relative),
            json_path=str(json_relative),
            catalog_packet_path=catalog_packet_path,
            result=result,
        )

    def _load_entry(
        self,
        workspace_root: Path,
        entry: RuntimeReportDigestProfileCatalogEntry,
    ) -> RuntimeReportDigestProfileBrowserEntry:
        profile = self._profiler.load_profile(workspace_root, profile_path=entry.json_path)
        selectors = tuple(_selector_view(item) for item in profile.selectors)
        return RuntimeReportDigestProfileBrowserEntry(
            profile_name=entry.profile_name,
            description=entry.description,
            tags=entry.tags,
            selector_count=entry.selector_count,
            selector_labels=entry.selector_labels,
            markdown_path=entry.markdown_path,
            json_path=entry.json_path,
            selectors=selectors,
        )


IonRuntimeReportDigestProfileBrowser = KernelRuntimeReportDigestProfileBrowser


def _selector_view(item: RuntimeReportDigestProfileSelector) -> RuntimeReportDigestProfileBrowserSelectorView:
    selector = item.selector
    return RuntimeReportDigestProfileBrowserSelectorView(
        label=item.label,
        source_ref=selector.source_ref,
        source_ref_contains=selector.source_ref_contains,
        trigger_event=selector.trigger_event,
        artifact_kind=selector.artifact_kind,
        source_family=selector.source_family,
        limit=selector.limit,
    )


def _facet_counts(entries: Sequence[RuntimeReportDigestProfileBrowserEntry]) -> RuntimeReportDigestProfileBrowserFacetCounts:
    return RuntimeReportDigestProfileBrowserFacetCounts(
        tags=_sorted_counts(tag for entry in entries for tag in entry.tags),
        selector_labels=_sorted_counts(label for entry in entries for label in entry.selector_labels),
        artifact_kinds=_sorted_counts(
            selector.artifact_kind for entry in entries for selector in entry.selectors if selector.artifact_kind
        ),
        trigger_events=_sorted_counts(
            selector.trigger_event for entry in entries for selector in entry.selectors if selector.trigger_event
        ),
        source_families=_sorted_counts(
            selector.source_family for entry in entries for selector in entry.selectors if selector.source_family
        ),
    )


def _sorted_counts(values: Sequence[str] | tuple[str, ...] | list[str] | object) -> tuple[tuple[str, int], ...]:
    counts: dict[str, int] = {}
    for value in values:  # type: ignore[assignment]
        counts[str(value)] = counts.get(str(value), 0) + 1
    return tuple(sorted(counts.items(), key=lambda item: (item[0], item[1])))


def _markdown_counts(title: str, counts: tuple[tuple[str, int], ...]) -> list[str]:
    lines = [f'### {title}', '']
    if not counts:
        lines.extend(['- NONE', ''])
        return lines
    lines.extend(f'- {name}: {count}' for name, count in counts)
    lines.append('')
    return lines


def _counts_html(counts: tuple[tuple[str, int], ...]) -> str:
    if not counts:
        return '<p class="muted">NONE</p>'
    return ''.join(
        f'<span class="pill">{html.escape(name)} ({count})</span>'
        for name, count in counts
    )


def _entry_html(
    entry: RuntimeReportDigestProfileBrowserEntry,
    *,
    output_relative_path: str | Path | None = None,
) -> str:
    selectors = ''.join(
        (
            '<div class="selector">'
            f'<div><strong>Label:</strong> {html.escape(selector.label)}</div>'
            f'<div><strong>Source Ref:</strong> <code>{html.escape(selector.source_ref or "NONE")}</code></div>'
            f'<div><strong>Source Ref Contains:</strong> <code>{html.escape(selector.source_ref_contains or "NONE")}</code></div>'
            f'<div><strong>Trigger Event:</strong> {html.escape(selector.trigger_event or "NONE")}</div>'
            f'<div><strong>Artifact Kind:</strong> {html.escape(selector.artifact_kind or "NONE")}</div>'
            f'<div><strong>Source Family:</strong> {html.escape(selector.source_family or "NONE")}</div>'
            f'<div><strong>Limit:</strong> {selector.limit if selector.limit is not None else "NONE"}</div>'
            '</div>'
        )
        for selector in entry.selectors
    ) or '<p class="muted">No selectors.</p>'
    output_line = ''
    if output_relative_path is not None:
        output_line = f'<div class="muted"><strong>Output Path:</strong> <code>{html.escape(str(output_relative_path))}</code></div>'
    tag_html = ''.join(f'<span class="pill">{html.escape(tag)}</span>' for tag in entry.tags) or '<span class="muted">NONE</span>'
    return (
        '<article class="entry">'
        f'<h3>{html.escape(entry.profile_name)}</h3>'
        f'<div><strong>Selector Count:</strong> {entry.selector_count}</div>'
        f'<div><strong>Description:</strong> {html.escape(entry.description or "NONE")}</div>'
        f'<div><strong>Definition Markdown Path:</strong> <code>{html.escape(entry.markdown_path or "NONE")}</code></div>'
        f'<div><strong>Definition JSON Path:</strong> <code>{html.escape(entry.json_path)}</code></div>'
        f'{output_line}'
        f'<div><strong>Tags:</strong> {tag_html}</div>'
        '<h4>Selectors</h4>'
        f'{selectors}'
        '</article>'
    )


def _resolve_relative_dir(root: Path, relative_path: Path) -> Path:
    return _resolve_relative_file(root, relative_path)


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportDigestProfileBrowserError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportDigestProfileBrowserError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec='seconds')
