"""Read-only reverse tracing from rendered digests back to lawful profile origins.

This module follows one H2-backed/H1-rendered operator digest backward into the digest
profile definition that rendered it and, when present, the downstream catalog/browser
surfaces that exposed or selected that profile. It does not bypass the existing H2/H3/H4
path or promote any downstream witness packet into authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any, Iterable, Sequence

from .runtime_report_digest_profile_catalog import RuntimeReportDigestProfileCatalogQuery
from .runtime_report_digest_profiles import (
    KernelRuntimeReportDigestProfileError,
    KernelRuntimeReportDigestProfiler,
    RuntimeReportOperatorDigestProfile,
)
from .runtime_report_operator_digest import RuntimeReportOperatorDigest


class KernelRuntimeReportDigestReverseTraceError(Exception):
    """Raised when one reverse trace from digest to profile cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportDigestReverseTraceSelector:
    digest_json_path: str | None = None
    digest_markdown_path: str | None = None


@dataclass(frozen=True)
class RuntimeReportDigestReverseTraceSelectorView:
    label: str
    source_ref: str | None
    source_ref_contains: str | None
    trigger_event: str | None
    artifact_kind: str | None
    source_family: str | None
    limit: int | None


@dataclass(frozen=True)
class RuntimeReportDigestReverseTraceQueryView:
    profile_name_contains: str | None
    tag: str | None
    selector_label_contains: str | None
    description_contains: str | None
    limit: int | None


@dataclass(frozen=True)
class RuntimeReportDigestReverseTraceCatalogSurface:
    entry_index: int
    matched_count: int
    total_profiles: int
    query: RuntimeReportDigestReverseTraceQueryView
    markdown_path: str | None
    json_path: str


@dataclass(frozen=True)
class RuntimeReportDigestReverseTraceBrowserSurface:
    entry_index: int
    matched_count: int
    total_profiles: int
    query: RuntimeReportDigestReverseTraceQueryView
    markdown_path: str | None
    html_path: str | None
    json_path: str


@dataclass(frozen=True)
class RuntimeReportDigestReverseTraceForwardLink:
    selection_mode: str
    markdown_path: str | None
    json_path: str
    browser_json_path: str | None
    browser_markdown_path: str | None


@dataclass(frozen=True)
class RuntimeReportDigestReverseTrace:
    generated_at: str
    read_only_mode: bool
    selection_mode: str
    profile_resolution_mode: str
    digest_markdown_path: str
    digest_json_path: str
    digest_generated_at: str
    digest_family_count: int
    digest_total_generations: int
    digest_shared_trigger_events: tuple[str, ...]
    digest_shared_artifact_kinds: tuple[str, ...]
    digest_shared_source_families: tuple[str, ...]
    digest_runtime_ref_union: tuple[str, ...]
    profile_name: str
    description: str
    tags: tuple[str, ...]
    profile_markdown_path: str | None
    profile_json_path: str | None
    selectors: tuple[RuntimeReportDigestReverseTraceSelectorView, ...]
    forward_link: RuntimeReportDigestReverseTraceForwardLink | None
    catalog_surfaces: tuple[RuntimeReportDigestReverseTraceCatalogSurface, ...]
    browser_surfaces: tuple[RuntimeReportDigestReverseTraceBrowserSurface, ...]


@dataclass(frozen=True)
class RuntimeReportDigestReverseTraceWriteResult:
    markdown_path: str
    json_path: str
    trace: RuntimeReportDigestReverseTrace


class KernelRuntimeReportDigestReverseTracer:
    """Trace one rendered digest back to its lawful digest-profile origin surfaces."""

    def __init__(
        self,
        *,
        profiler: KernelRuntimeReportDigestProfiler | None = None,
    ) -> None:
        self._profiler = profiler or KernelRuntimeReportDigestProfiler()

    def trace_digest_origin(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportDigestReverseTraceSelector,
        *,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        traces_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/traces',
        catalogs_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/catalog',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/browser',
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        runtime_browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        created_at: str | None = None,
    ) -> RuntimeReportDigestReverseTrace:
        root = Path(workspace_root).resolve()
        selection_mode, digest_markdown_path, digest_json_path, digest_payload = self._resolve_digest_selection(
            root,
            selector,
        )
        forward_link, trace_payload = self._find_forward_trace(
            root,
            digest_markdown_path=digest_markdown_path,
            digest_json_path=digest_json_path,
            traces_dir=traces_dir,
        )
        profile_resolution_mode, profile = self._resolve_profile(
            root,
            digest_payload=digest_payload,
            digest_json_path=digest_json_path,
            trace_payload=trace_payload,
            profiles_dir=profiles_dir,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            browser_dir=runtime_browser_dir,
            crosslinks_dir=crosslinks_dir,
        )
        catalog_surfaces = self._find_catalog_surfaces(
            root,
            profile_name=profile.profile_name,
            catalogs_dir=catalogs_dir,
        )
        browser_surfaces = self._find_browser_surfaces(
            root,
            profile_name=profile.profile_name,
            browser_dir=browser_dir,
            forward_link=forward_link,
        )
        return RuntimeReportDigestReverseTrace(
            generated_at=created_at or _iso_now(),
            read_only_mode=True,
            selection_mode=selection_mode,
            profile_resolution_mode=profile_resolution_mode,
            digest_markdown_path=digest_markdown_path,
            digest_json_path=digest_json_path,
            digest_generated_at=str(digest_payload.get('generated_at') or created_at or _iso_now()),
            digest_family_count=int(digest_payload.get('family_count') or 0),
            digest_total_generations=int(digest_payload.get('total_generations') or 0),
            digest_shared_trigger_events=tuple(digest_payload.get('shared_trigger_events') or ()),
            digest_shared_artifact_kinds=tuple(digest_payload.get('shared_artifact_kinds') or ()),
            digest_shared_source_families=tuple(digest_payload.get('shared_source_families') or ()),
            digest_runtime_ref_union=tuple(digest_payload.get('runtime_ref_union') or ()),
            profile_name=profile.profile_name,
            description=profile.description,
            tags=profile.tags,
            profile_markdown_path=_profile_markdown_path(root, profile.profile_name, profiles_dir),
            profile_json_path=_profile_json_path(root, profile.profile_name, profiles_dir),
            selectors=tuple(_selector_view(item.label, item.selector) for item in profile.selectors),
            forward_link=forward_link,
            catalog_surfaces=catalog_surfaces,
            browser_surfaces=browser_surfaces,
        )

    def render_markdown(
        self,
        trace: RuntimeReportDigestReverseTrace,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'trace_kind: RUNTIME_REPORT_DIGEST_REVERSE_TRACE',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {trace.generated_at}',
            f'selection_mode: {trace.selection_mode}',
            f'profile_resolution_mode: {trace.profile_resolution_mode}',
            f'digest_markdown_path: {trace.digest_markdown_path}',
            f'digest_json_path: {trace.digest_json_path}',
            f'profile_name: {trace.profile_name}',
        ]
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Digest Reverse Trace',
            '',
            'This packet is a bounded read-only reverse bridge from one rendered operator digest back to the lawful digest-profile definition and related browser/catalog witness surfaces when present.',
            '',
            '## Digest Selection',
            '',
            f'- Selection Mode: {trace.selection_mode}',
            f'- Digest Markdown Path: {trace.digest_markdown_path}',
            f'- Digest JSON Path: {trace.digest_json_path}',
            f'- Digest Generated At: {trace.digest_generated_at}',
            f'- Family Count: {trace.digest_family_count}',
            f'- Total Generations: {trace.digest_total_generations}',
            f'- Shared Trigger Events: {", ".join(trace.digest_shared_trigger_events) if trace.digest_shared_trigger_events else "NONE"}',
            f'- Shared Artifact Kinds: {", ".join(trace.digest_shared_artifact_kinds) if trace.digest_shared_artifact_kinds else "NONE"}',
            f'- Shared Source Families: {", ".join(trace.digest_shared_source_families) if trace.digest_shared_source_families else "NONE"}',
        ])
        if trace.digest_runtime_ref_union:
            lines.append('- Runtime Ref Union:')
            lines.extend(f'  - {item}' for item in trace.digest_runtime_ref_union)
        else:
            lines.append('- Runtime Ref Union: NONE')
        lines.extend([
            '',
            '## Resolved Profile',
            '',
            f'- Profile Resolution Mode: {trace.profile_resolution_mode}',
            f'- Profile Name: {trace.profile_name}',
            f'- Description: {trace.description or "NONE"}',
            f'- Tags: {", ".join(trace.tags) if trace.tags else "NONE"}',
            f'- Definition Markdown Path: {trace.profile_markdown_path or "NONE"}',
            f'- Definition JSON Path: {trace.profile_json_path or "NONE"}',
            '',
            '## Selectors',
            '',
        ])
        if not trace.selectors:
            lines.extend(['- NONE', ''])
        else:
            for index, item in enumerate(trace.selectors, start=1):
                lines.extend([
                    f'### {index}. {item.label}',
                    '',
                    f'- Source Ref: {item.source_ref or "NONE"}',
                    f'- Source Ref Contains: {item.source_ref_contains or "NONE"}',
                    f'- Trigger Event: {item.trigger_event or "NONE"}',
                    f'- Artifact Kind: {item.artifact_kind or "NONE"}',
                    f'- Source Family: {item.source_family or "NONE"}',
                    f'- Limit: {item.limit if item.limit is not None else "NONE"}',
                    '',
                ])
        lines.extend(['## Forward Link', ''])
        if trace.forward_link is None:
            lines.extend(['- NONE', ''])
        else:
            lines.extend([
                f'- Selection Mode: {trace.forward_link.selection_mode}',
                f'- Trace Markdown Path: {trace.forward_link.markdown_path or "NONE"}',
                f'- Trace JSON Path: {trace.forward_link.json_path}',
                f'- Browser Markdown Path: {trace.forward_link.browser_markdown_path or "NONE"}',
                f'- Browser JSON Path: {trace.forward_link.browser_json_path or "NONE"}',
                '',
            ])
        lines.extend(['## Browser Surfaces', ''])
        if not trace.browser_surfaces:
            lines.extend(['- NONE', ''])
        else:
            for index, item in enumerate(trace.browser_surfaces, start=1):
                lines.extend([
                    f'### {index}. Browser Entry {item.entry_index}',
                    '',
                    f'- Matched Profiles: {item.matched_count}/{item.total_profiles}',
                    f'- Query Profile Name Contains: {item.query.profile_name_contains or "ANY"}',
                    f'- Query Tag: {item.query.tag or "ANY"}',
                    f'- Query Selector Label Contains: {item.query.selector_label_contains or "ANY"}',
                    f'- Query Description Contains: {item.query.description_contains or "ANY"}',
                    f'- Query Limit: {item.query.limit if item.query.limit is not None else "ANY"}',
                    f'- Browser Markdown Path: {item.markdown_path or "NONE"}',
                    f'- Browser HTML Path: {item.html_path or "NONE"}',
                    f'- Browser JSON Path: {item.json_path}',
                    '',
                ])
        lines.extend(['## Catalog Surfaces', ''])
        if not trace.catalog_surfaces:
            lines.extend(['- NONE', ''])
        else:
            for index, item in enumerate(trace.catalog_surfaces, start=1):
                lines.extend([
                    f'### {index}. Catalog Entry {item.entry_index}',
                    '',
                    f'- Matched Profiles: {item.matched_count}/{item.total_profiles}',
                    f'- Query Profile Name Contains: {item.query.profile_name_contains or "ANY"}',
                    f'- Query Tag: {item.query.tag or "ANY"}',
                    f'- Query Selector Label Contains: {item.query.selector_label_contains or "ANY"}',
                    f'- Query Description Contains: {item.query.description_contains or "ANY"}',
                    f'- Query Limit: {item.query.limit if item.query.limit is not None else "ANY"}',
                    f'- Catalog Markdown Path: {item.markdown_path or "NONE"}',
                    f'- Catalog JSON Path: {item.json_path}',
                    '',
                ])
        lines.extend([
            '## Boundary',
            '',
            '- This reverse trace is a read-only bridge from one rendered digest back to its lawful digest-profile origin surfaces.',
            '- It remains downstream from digest profiles, operator digests, profile catalogs, profile browsers, and profile-digest traces.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, or reverse-trace authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, trace: RuntimeReportDigestReverseTrace) -> str:
        payload = {
            'trace_kind': 'RUNTIME_REPORT_DIGEST_REVERSE_TRACE',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': trace.generated_at,
            'selection_mode': trace.selection_mode,
            'profile_resolution_mode': trace.profile_resolution_mode,
            'profile_name': trace.profile_name,
            'description': trace.description,
            'tags': list(trace.tags),
            'profile_markdown_path': trace.profile_markdown_path,
            'profile_json_path': trace.profile_json_path,
            'selectors': [
                {
                    'label': item.label,
                    'source_ref': item.source_ref,
                    'source_ref_contains': item.source_ref_contains,
                    'trigger_event': item.trigger_event,
                    'artifact_kind': item.artifact_kind,
                    'source_family': item.source_family,
                    'limit': item.limit,
                }
                for item in trace.selectors
            ],
            'forward_link': None if trace.forward_link is None else {
                'selection_mode': trace.forward_link.selection_mode,
                'markdown_path': trace.forward_link.markdown_path,
                'json_path': trace.forward_link.json_path,
                'browser_markdown_path': trace.forward_link.browser_markdown_path,
                'browser_json_path': trace.forward_link.browser_json_path,
            },
            'digest': {
                'markdown_path': trace.digest_markdown_path,
                'json_path': trace.digest_json_path,
                'generated_at': trace.digest_generated_at,
                'family_count': trace.digest_family_count,
                'total_generations': trace.digest_total_generations,
                'shared_trigger_events': list(trace.digest_shared_trigger_events),
                'shared_artifact_kinds': list(trace.digest_shared_artifact_kinds),
                'shared_source_families': list(trace.digest_shared_source_families),
                'runtime_ref_union': list(trace.digest_runtime_ref_union),
            },
            'browser_surfaces': [
                {
                    'entry_index': item.entry_index,
                    'matched_count': item.matched_count,
                    'total_profiles': item.total_profiles,
                    'query': {
                        'profile_name_contains': item.query.profile_name_contains,
                        'tag': item.query.tag,
                        'selector_label_contains': item.query.selector_label_contains,
                        'description_contains': item.query.description_contains,
                        'limit': item.query.limit,
                    },
                    'markdown_path': item.markdown_path,
                    'html_path': item.html_path,
                    'json_path': item.json_path,
                }
                for item in trace.browser_surfaces
            ],
            'catalog_surfaces': [
                {
                    'entry_index': item.entry_index,
                    'matched_count': item.matched_count,
                    'total_profiles': item.total_profiles,
                    'query': {
                        'profile_name_contains': item.query.profile_name_contains,
                        'tag': item.query.tag,
                        'selector_label_contains': item.query.selector_label_contains,
                        'description_contains': item.query.description_contains,
                        'limit': item.query.limit,
                    },
                    'markdown_path': item.markdown_path,
                    'json_path': item.json_path,
                }
                for item in trace.catalog_surfaces
            ],
            'boundary': [
                'Read-only bridge from one rendered digest back to its lawful digest-profile origin surfaces.',
                'Remains downstream from digest profiles, operator digests, profile catalogs, profile browsers, and profile-digest traces.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, or reverse-trace authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_trace_packet(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportDigestReverseTraceSelector,
        *,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        traces_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/traces',
        catalogs_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/catalog',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/browser',
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        runtime_browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        reverse_traces_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/reverse_traces',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportDigestReverseTraceWriteResult:
        root = Path(workspace_root).resolve()
        trace = self.trace_digest_origin(
            root,
            selector,
            profiles_dir=profiles_dir,
            traces_dir=traces_dir,
            catalogs_dir=catalogs_dir,
            browser_dir=browser_dir,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            runtime_browser_dir=runtime_browser_dir,
            crosslinks_dir=crosslinks_dir,
            created_at=created_at,
        )
        relative_dir = Path(reverse_traces_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stamp = re.sub(r'[^0-9]', '', trace.generated_at)[:14]
        stem = output_stem or f'{_safe(trace.profile_name)}__digest_reverse_trace_{stamp}'
        markdown_relative = relative_dir / f'{stem}.md'
        json_relative = relative_dir / f'{stem}.json'
        _resolve_relative_file(root, markdown_relative).write_text(
            self.render_markdown(trace, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        _resolve_relative_file(root, json_relative).write_text(
            self.render_json(trace),
            encoding='utf-8',
        )
        return RuntimeReportDigestReverseTraceWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            trace=trace,
        )

    def _resolve_digest_selection(
        self,
        root: Path,
        selector: RuntimeReportDigestReverseTraceSelector,
    ) -> tuple[str, str, str, dict[str, Any]]:
        has_json = bool(selector.digest_json_path)
        has_markdown = bool(selector.digest_markdown_path)
        if has_json == has_markdown:
            raise KernelRuntimeReportDigestReverseTraceError(
                'Digest reverse trace requires exactly one of digest_json_path or digest_markdown_path.'
            )
        if has_json:
            json_relative = Path(selector.digest_json_path or '')
            selection_mode = 'DIGEST_JSON_PATH'
            markdown_relative = json_relative.with_suffix('.md')
        else:
            markdown_relative = Path(selector.digest_markdown_path or '')
            selection_mode = 'DIGEST_MARKDOWN_PATH'
            json_relative = markdown_relative.with_suffix('.json')
        json_resolved = _resolve_relative_file(root, json_relative)
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        if not json_resolved.exists():
            raise KernelRuntimeReportDigestReverseTraceError(f'Digest JSON not found: {json_relative}')
        if not markdown_resolved.exists():
            raise KernelRuntimeReportDigestReverseTraceError(f'Digest markdown not found: {markdown_relative}')
        try:
            payload = json.loads(json_resolved.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            raise KernelRuntimeReportDigestReverseTraceError(
                f'Digest JSON is invalid: {json_relative}'
            ) from exc
        if payload.get('digest_kind') != 'RUNTIME_REPORT_OPERATOR_DIGEST':
            raise KernelRuntimeReportDigestReverseTraceError(
                f'Digest JSON is not a lawful operator digest packet: {json_relative}'
            )
        return selection_mode, str(markdown_relative), str(json_relative), payload

    def _find_forward_trace(
        self,
        root: Path,
        *,
        digest_markdown_path: str,
        digest_json_path: str,
        traces_dir: str | Path,
    ) -> tuple[RuntimeReportDigestReverseTraceForwardLink | None, dict[str, Any] | None]:
        relative_dir = Path(traces_dir)
        resolved_dir = _resolve_relative_dir(root, relative_dir)
        if not resolved_dir.exists():
            return None, None
        matches: list[tuple[dict[str, Any], str]] = []
        for candidate in sorted(resolved_dir.glob('*.json')):
            payload = _load_json(candidate)
            if payload.get('trace_kind') != 'RUNTIME_REPORT_PROFILE_DIGEST_TRACE':
                continue
            digest = payload.get('digest') or {}
            if digest.get('json_path') == digest_json_path or digest.get('markdown_path') == digest_markdown_path:
                matches.append((payload, str(candidate.relative_to(root))))
        if not matches:
            return None, None
        payload, json_path = sorted(matches, key=lambda item: str(item[0].get('generated_at') or ''))[-1]
        markdown_path = str(Path(json_path).with_suffix('.md'))
        browser_selection = payload.get('browser_selection') or {}
        return RuntimeReportDigestReverseTraceForwardLink(
            selection_mode=str(payload.get('selection_mode') or 'PROFILE_NAME'),
            markdown_path=markdown_path if _resolve_relative_file(root, Path(markdown_path)).exists() else None,
            json_path=json_path,
            browser_json_path=browser_selection.get('json_path'),
            browser_markdown_path=browser_selection.get('markdown_path'),
        ), payload

    def _resolve_profile(
        self,
        root: Path,
        *,
        digest_payload: dict[str, Any],
        digest_json_path: str,
        trace_payload: dict[str, Any] | None,
        profiles_dir: str | Path,
        packet_index_path: str | Path,
        operator_dashboard_path: str | Path,
        navigation_dir: str | Path,
        browser_dir: str | Path,
        crosslinks_dir: str | Path,
    ) -> tuple[str, RuntimeReportOperatorDigestProfile]:
        if trace_payload is not None:
            profile_json_path = trace_payload.get('profile_json_path')
            profile_name = trace_payload.get('profile_name')
            try:
                profile = self._profiler.load_profile(
                    root,
                    profile_name=profile_name if profile_json_path is None else None,
                    profile_path=profile_json_path,
                    profiles_dir=profiles_dir,
                )
            except KernelRuntimeReportDigestProfileError as exc:
                raise KernelRuntimeReportDigestReverseTraceError(str(exc)) from exc
            return 'FORWARD_TRACE', profile
        stem_candidates = self._profile_candidates_from_digest_stem(root, digest_json_path, profiles_dir)
        if len(stem_candidates) == 1:
            return 'DIGEST_STEM', stem_candidates[0]
        matches = self._profile_candidates_from_digest_match(
            root,
            digest_payload=digest_payload,
            profiles_dir=profiles_dir,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            browser_dir=browser_dir,
            crosslinks_dir=crosslinks_dir,
        )
        if len(matches) == 1:
            return 'DIGEST_MATCH', matches[0]
        if not matches and not stem_candidates:
            raise KernelRuntimeReportDigestReverseTraceError(
                'Digest reverse trace could not resolve a lawful digest profile for the selected digest.'
            )
        candidates = stem_candidates or matches
        raise KernelRuntimeReportDigestReverseTraceError(
            'Digest reverse trace resolved multiple candidate profiles: ' + ', '.join(profile.profile_name for profile in candidates)
        )

    def _profile_candidates_from_digest_stem(
        self,
        root: Path,
        digest_json_path: str,
        profiles_dir: str | Path,
    ) -> list[RuntimeReportOperatorDigestProfile]:
        stem = Path(digest_json_path).stem
        prefix = stem.split('__runtime_operator_digest_', 1)[0]
        if prefix == stem:
            return []
        candidates: list[RuntimeReportOperatorDigestProfile] = []
        for profile in _iter_profiles(self._profiler, root, profiles_dir):
            if _safe(profile.profile_name) == prefix:
                candidates.append(profile)
        return candidates

    def _profile_candidates_from_digest_match(
        self,
        root: Path,
        *,
        digest_payload: dict[str, Any],
        profiles_dir: str | Path,
        packet_index_path: str | Path,
        operator_dashboard_path: str | Path,
        navigation_dir: str | Path,
        browser_dir: str | Path,
        crosslinks_dir: str | Path,
    ) -> list[RuntimeReportOperatorDigestProfile]:
        target_signature = _digest_signature_from_payload(digest_payload)
        matches: list[RuntimeReportOperatorDigestProfile] = []
        for profile in _iter_profiles(self._profiler, root, profiles_dir):
            try:
                rendered = self._profiler.build_digest_from_profile(
                    root,
                    profile,
                    packet_index_path=packet_index_path,
                    operator_dashboard_path=operator_dashboard_path,
                    navigation_dir=navigation_dir,
                    browser_dir=browser_dir,
                    crosslinks_dir=crosslinks_dir,
                    created_at=str(digest_payload.get('generated_at') or _iso_now()),
                )
            except KernelRuntimeReportDigestProfileError:
                continue
            if _digest_signature_from_digest(rendered) == target_signature:
                matches.append(profile)
        return matches

    def _find_browser_surfaces(
        self,
        root: Path,
        *,
        profile_name: str,
        browser_dir: str | Path,
        forward_link: RuntimeReportDigestReverseTraceForwardLink | None,
    ) -> tuple[RuntimeReportDigestReverseTraceBrowserSurface, ...]:
        relative_dir = Path(browser_dir)
        resolved_dir = _resolve_relative_dir(root, relative_dir)
        seen: set[str] = set()
        surfaces: list[RuntimeReportDigestReverseTraceBrowserSurface] = []
        preferred_json = forward_link.browser_json_path if forward_link is not None else None
        if resolved_dir.exists():
            candidates = sorted(resolved_dir.glob('*.json'))
            if preferred_json:
                preferred_path = _resolve_relative_file(root, Path(preferred_json))
                candidates = sorted(candidates, key=lambda path: (0 if path == preferred_path else 1, str(path)))
            for candidate in candidates:
                payload = _load_json(candidate)
                if payload.get('browser_kind') != 'RUNTIME_REPORT_DIGEST_PROFILE_BROWSER':
                    continue
                entry_index = _profile_entry_index(payload.get('entries') or (), profile_name)
                if entry_index is None:
                    continue
                json_path = str(candidate.relative_to(root))
                if json_path in seen:
                    continue
                seen.add(json_path)
                stem = candidate.with_suffix('')
                markdown_path = str(stem.with_suffix('.md').relative_to(root)) if stem.with_suffix('.md').exists() else None
                html_path = str(stem.with_suffix('.html').relative_to(root)) if stem.with_suffix('.html').exists() else None
                surfaces.append(
                    RuntimeReportDigestReverseTraceBrowserSurface(
                        entry_index=entry_index,
                        matched_count=int(payload.get('matched_count') or 0),
                        total_profiles=int(payload.get('total_profiles') or 0),
                        query=_query_view(payload.get('query') or {}),
                        markdown_path=markdown_path,
                        html_path=html_path,
                        json_path=json_path,
                    )
                )
        return tuple(surfaces)

    def _find_catalog_surfaces(
        self,
        root: Path,
        *,
        profile_name: str,
        catalogs_dir: str | Path,
    ) -> tuple[RuntimeReportDigestReverseTraceCatalogSurface, ...]:
        relative_dir = Path(catalogs_dir)
        resolved_dir = _resolve_relative_dir(root, relative_dir)
        surfaces: list[RuntimeReportDigestReverseTraceCatalogSurface] = []
        if not resolved_dir.exists():
            return ()
        for candidate in sorted(resolved_dir.glob('*.json')):
            payload = _load_json(candidate)
            if payload.get('catalog_kind') != 'RUNTIME_REPORT_DIGEST_PROFILE_CATALOG':
                continue
            entry_index = _profile_entry_index(payload.get('entries') or (), profile_name)
            if entry_index is None:
                continue
            stem = candidate.with_suffix('')
            markdown_path = str(stem.with_suffix('.md').relative_to(root)) if stem.with_suffix('.md').exists() else None
            surfaces.append(
                RuntimeReportDigestReverseTraceCatalogSurface(
                    entry_index=entry_index,
                    matched_count=int(payload.get('matched_count') or 0),
                    total_profiles=int(payload.get('total_profiles') or 0),
                    query=_query_view(payload.get('query') or {}),
                    markdown_path=markdown_path,
                    json_path=str(candidate.relative_to(root)),
                )
            )
        return tuple(surfaces)


IonRuntimeReportDigestReverseTracer = KernelRuntimeReportDigestReverseTracer


def _iter_profiles(
    profiler: KernelRuntimeReportDigestProfiler,
    root: Path,
    profiles_dir: str | Path,
) -> Sequence[RuntimeReportOperatorDigestProfile]:
    relative_dir = Path(profiles_dir)
    resolved_dir = _resolve_relative_dir(root, relative_dir)
    if not resolved_dir.exists():
        return ()
    profiles: list[RuntimeReportOperatorDigestProfile] = []
    for candidate in sorted(resolved_dir.glob('*.json')):
        try:
            payload = _load_json(candidate)
        except KernelRuntimeReportDigestReverseTraceError:
            continue
        if payload.get('profile_kind') != 'RUNTIME_REPORT_OPERATOR_DIGEST_PROFILE':
            continue
        try:
            profiles.append(profiler.load_profile(root, profile_path=str(candidate.relative_to(root))))
        except KernelRuntimeReportDigestProfileError:
            continue
    return tuple(profiles)


def _selector_view(label: str, selector: Any) -> RuntimeReportDigestReverseTraceSelectorView:
    return RuntimeReportDigestReverseTraceSelectorView(
        label=label,
        source_ref=selector.source_ref,
        source_ref_contains=selector.source_ref_contains,
        trigger_event=selector.trigger_event,
        artifact_kind=selector.artifact_kind,
        source_family=selector.source_family,
        limit=selector.limit,
    )


def _query_view(payload: dict[str, Any]) -> RuntimeReportDigestReverseTraceQueryView:
    return RuntimeReportDigestReverseTraceQueryView(
        profile_name_contains=payload.get('profile_name_contains'),
        tag=payload.get('tag'),
        selector_label_contains=payload.get('selector_label_contains'),
        description_contains=payload.get('description_contains'),
        limit=payload.get('limit'),
    )


def _profile_entry_index(entries: Sequence[dict[str, Any]], profile_name: str) -> int | None:
    for index, entry in enumerate(entries, start=1):
        if str(entry.get('profile_name') or '') == profile_name:
            return index
    return None


def _profile_markdown_path(root: Path, profile_name: str, profiles_dir: str | Path) -> str | None:
    relative = Path(profiles_dir) / f'{_safe(profile_name)}.md'
    return str(relative) if _resolve_relative_file(root, relative).exists() else None


def _profile_json_path(root: Path, profile_name: str, profiles_dir: str | Path) -> str | None:
    relative = Path(profiles_dir) / f'{_safe(profile_name)}.json'
    return str(relative) if _resolve_relative_file(root, relative).exists() else None


def _digest_signature_from_payload(payload: dict[str, Any]) -> tuple[Any, ...]:
    families = tuple(
        (
            family.get('family_label'),
            (family.get('selector') or {}).get('source_ref'),
            (family.get('selector') or {}).get('source_ref_contains'),
            (family.get('selector') or {}).get('trigger_event'),
            (family.get('selector') or {}).get('artifact_kind'),
            (family.get('selector') or {}).get('source_family'),
            (family.get('selector') or {}).get('limit'),
            family.get('generation_count'),
            family.get('shared_trigger_event'),
            family.get('shared_artifact_kind'),
            family.get('shared_source_family'),
            tuple(family.get('runtime_ref_union') or ()),
        )
        for family in payload.get('families') or ()
    )
    return (
        payload.get('family_count'),
        payload.get('total_generations'),
        tuple(payload.get('shared_trigger_events') or ()),
        tuple(payload.get('shared_artifact_kinds') or ()),
        tuple(payload.get('shared_source_families') or ()),
        tuple(payload.get('runtime_ref_union') or ()),
        families,
    )


def _digest_signature_from_digest(digest: RuntimeReportOperatorDigest) -> tuple[Any, ...]:
    families = tuple(
        (
            family.family_label,
            family.selector.source_ref,
            family.selector.source_ref_contains,
            family.selector.trigger_event,
            family.selector.artifact_kind,
            family.selector.source_family,
            family.selector.limit,
            family.generation_count,
            family.shared_trigger_event,
            family.shared_artifact_kind,
            family.shared_source_family,
            tuple(family.runtime_ref_union),
        )
        for family in digest.families
    )
    return (
        digest.family_count,
        digest.total_generations,
        tuple(digest.shared_trigger_events),
        tuple(digest.shared_artifact_kinds),
        tuple(digest.shared_source_families),
        tuple(digest.runtime_ref_union),
        families,
    )


def _load_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        raise KernelRuntimeReportDigestReverseTraceError(f'Invalid JSON packet: {path}') from exc
    if not isinstance(payload, dict):
        raise KernelRuntimeReportDigestReverseTraceError(f'JSON packet is not an object: {path}')
    return payload


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime-profile'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime-profile'


def _resolve_relative_dir(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportDigestReverseTraceError(
            f'Absolute paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportDigestReverseTraceError(
            f'Path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportDigestReverseTraceError(
            f'Absolute paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportDigestReverseTraceError(
            f'Path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
