"""Read-only bidirectional tracing across lawful profile↔digest paths.

This module composes the existing forward profile-to-digest bridge (I1) and reverse
 digest-to-profile bridge (I2) into one bounded witness packet. It never bypasses the
 lawful H2→H1 render path or promotes any downstream packet into authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any

from .runtime_report_digest_profile_catalog import RuntimeReportDigestProfileCatalogQuery
from .runtime_report_digest_reverse_trace import (
    KernelRuntimeReportDigestReverseTraceError,
    KernelRuntimeReportDigestReverseTracer,
    RuntimeReportDigestReverseTrace,
    RuntimeReportDigestReverseTraceSelector,
)
from .runtime_report_profile_digest_trace import (
    KernelRuntimeReportProfileDigestTraceError,
    KernelRuntimeReportProfileDigestTracer,
    RuntimeReportProfileDigestTrace,
    RuntimeReportProfileDigestTraceSelector,
)


class KernelRuntimeReportBidirectionalTraceError(Exception):
    """Raised when a bidirectional profile↔digest trace cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportBidirectionalTraceSelector:
    profile_name: str | None = None
    profile_path: str | None = None
    browser_query: RuntimeReportDigestProfileCatalogQuery | None = None
    browser_entry_index: int | None = None
    digest_json_path: str | None = None
    digest_markdown_path: str | None = None


@dataclass(frozen=True)
class RuntimeReportBidirectionalForwardView:
    source_kind: str
    selection_mode: str
    profile_name: str
    description: str
    tags: tuple[str, ...]
    profile_markdown_path: str | None
    profile_json_path: str | None
    digest_markdown_path: str
    digest_json_path: str
    digest_generated_at: str
    digest_family_count: int
    digest_total_generations: int
    digest_shared_trigger_events: tuple[str, ...]
    digest_shared_artifact_kinds: tuple[str, ...]
    digest_shared_source_families: tuple[str, ...]
    digest_runtime_ref_union: tuple[str, ...]
    trace_markdown_path: str | None
    trace_json_path: str | None
    browser_markdown_path: str | None
    browser_json_path: str | None


@dataclass(frozen=True)
class RuntimeReportBidirectionalReverseView:
    source_kind: str
    selection_mode: str
    profile_resolution_mode: str
    profile_name: str
    description: str
    tags: tuple[str, ...]
    profile_markdown_path: str | None
    profile_json_path: str | None
    digest_markdown_path: str
    digest_json_path: str
    digest_generated_at: str
    digest_family_count: int
    digest_total_generations: int
    digest_shared_trigger_events: tuple[str, ...]
    digest_shared_artifact_kinds: tuple[str, ...]
    digest_shared_source_families: tuple[str, ...]
    digest_runtime_ref_union: tuple[str, ...]
    catalog_json_paths: tuple[str, ...]
    browser_json_paths: tuple[str, ...]
    forward_link_json_path: str | None
    forward_link_markdown_path: str | None


@dataclass(frozen=True)
class RuntimeReportBidirectionalTrace:
    generated_at: str
    read_only_mode: bool
    selection_mode: str
    forward: RuntimeReportBidirectionalForwardView
    reverse: RuntimeReportBidirectionalReverseView
    profile_name_match: bool
    digest_json_path_match: bool
    digest_markdown_path_match: bool
    asymmetries: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportBidirectionalTraceWriteResult:
    markdown_path: str
    json_path: str
    trace: RuntimeReportBidirectionalTrace


class KernelRuntimeReportBidirectionalTracer:
    """Render one bounded witness packet over the forward and reverse profile↔digest path."""

    def __init__(
        self,
        *,
        profile_tracer: KernelRuntimeReportProfileDigestTracer | None = None,
        reverse_tracer: KernelRuntimeReportDigestReverseTracer | None = None,
    ) -> None:
        self._profile_tracer = profile_tracer or KernelRuntimeReportProfileDigestTracer()
        self._reverse_tracer = reverse_tracer or KernelRuntimeReportDigestReverseTracer()

    def trace_bidirectional(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportBidirectionalTraceSelector,
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
        digests_dir: str | Path = 'ION/05_context/runtime_reports/governance/digests/profiles',
        digest_output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportBidirectionalTrace:
        root = Path(workspace_root).resolve()
        route = _selection_route(selector)
        timestamp = created_at or _iso_now()
        if route == 'FORWARD_SELECTION':
            try:
                forward_trace = self._profile_tracer.trace_profile_to_digest(
                    root,
                    RuntimeReportProfileDigestTraceSelector(
                        profile_name=selector.profile_name,
                        profile_path=selector.profile_path,
                        browser_query=selector.browser_query,
                        browser_entry_index=selector.browser_entry_index,
                    ),
                    profiles_dir=profiles_dir,
                    packet_index_path=packet_index_path,
                    operator_dashboard_path=operator_dashboard_path,
                    navigation_dir=navigation_dir,
                    browser_dir=runtime_browser_dir,
                    crosslinks_dir=crosslinks_dir,
                    digests_dir=digests_dir,
                    digest_output_stem=digest_output_stem,
                    created_at=timestamp,
                )
            except KernelRuntimeReportProfileDigestTraceError as exc:
                raise KernelRuntimeReportBidirectionalTraceError(str(exc)) from exc
            try:
                reverse_trace = self._reverse_tracer.trace_digest_origin(
                    root,
                    RuntimeReportDigestReverseTraceSelector(
                        digest_json_path=forward_trace.digest_json_path,
                    ),
                    profiles_dir=profiles_dir,
                    traces_dir=traces_dir,
                    catalogs_dir=catalogs_dir,
                    browser_dir=browser_dir,
                    packet_index_path=packet_index_path,
                    operator_dashboard_path=operator_dashboard_path,
                    navigation_dir=navigation_dir,
                    runtime_browser_dir=runtime_browser_dir,
                    crosslinks_dir=crosslinks_dir,
                    created_at=timestamp,
                )
            except KernelRuntimeReportDigestReverseTraceError as exc:
                raise KernelRuntimeReportBidirectionalTraceError(str(exc)) from exc
            forward_view = _forward_view_from_live_trace(forward_trace)
        else:
            try:
                reverse_trace = self._reverse_tracer.trace_digest_origin(
                    root,
                    RuntimeReportDigestReverseTraceSelector(
                        digest_json_path=selector.digest_json_path,
                        digest_markdown_path=selector.digest_markdown_path,
                    ),
                    profiles_dir=profiles_dir,
                    traces_dir=traces_dir,
                    catalogs_dir=catalogs_dir,
                    browser_dir=browser_dir,
                    packet_index_path=packet_index_path,
                    operator_dashboard_path=operator_dashboard_path,
                    navigation_dir=navigation_dir,
                    runtime_browser_dir=runtime_browser_dir,
                    crosslinks_dir=crosslinks_dir,
                    created_at=timestamp,
                )
            except KernelRuntimeReportDigestReverseTraceError as exc:
                raise KernelRuntimeReportBidirectionalTraceError(str(exc)) from exc
            if reverse_trace.forward_link is not None and reverse_trace.forward_link.json_path:
                forward_view = self._load_forward_view_from_packet(
                    root,
                    reverse_trace.forward_link.json_path,
                )
            else:
                forward_view = _forward_view_reconstructed_from_reverse(reverse_trace)
        reverse_view = _reverse_view_from_live_trace(reverse_trace)
        asymmetries = _collect_asymmetries(forward_view, reverse_view)
        return RuntimeReportBidirectionalTrace(
            generated_at=timestamp,
            read_only_mode=True,
            selection_mode=route,
            forward=forward_view,
            reverse=reverse_view,
            profile_name_match=forward_view.profile_name == reverse_view.profile_name,
            digest_json_path_match=forward_view.digest_json_path == reverse_view.digest_json_path,
            digest_markdown_path_match=forward_view.digest_markdown_path == reverse_view.digest_markdown_path,
            asymmetries=tuple(asymmetries),
        )

    def _load_forward_view_from_packet(
        self,
        root: Path,
        json_path: str,
    ) -> RuntimeReportBidirectionalForwardView:
        resolved = _resolve_relative_file(root, Path(json_path))
        if not resolved.exists():
            raise KernelRuntimeReportBidirectionalTraceError(
                f'Forward trace JSON not found: {json_path}'
            )
        try:
            payload = json.loads(resolved.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            raise KernelRuntimeReportBidirectionalTraceError(
                f'Forward trace JSON is invalid: {json_path}'
            ) from exc
        if payload.get('trace_kind') != 'RUNTIME_REPORT_PROFILE_DIGEST_TRACE':
            raise KernelRuntimeReportBidirectionalTraceError(
                f'Forward trace JSON is not a lawful profile-digest trace packet: {json_path}'
            )
        digest = payload.get('digest') or {}
        browser_selection = payload.get('browser_selection') or {}
        return RuntimeReportBidirectionalForwardView(
            source_kind='FORWARD_TRACE_PACKET',
            selection_mode=str(payload.get('selection_mode') or 'UNKNOWN'),
            profile_name=str(payload.get('profile_name') or 'UNKNOWN'),
            description=str(payload.get('description') or ''),
            tags=tuple(payload.get('tags') or ()),
            profile_markdown_path=payload.get('profile_markdown_path'),
            profile_json_path=payload.get('profile_json_path'),
            digest_markdown_path=str(digest.get('markdown_path') or ''),
            digest_json_path=str(digest.get('json_path') or ''),
            digest_generated_at=str(digest.get('generated_at') or ''),
            digest_family_count=int(digest.get('family_count') or 0),
            digest_total_generations=int(digest.get('total_generations') or 0),
            digest_shared_trigger_events=tuple(digest.get('shared_trigger_events') or ()),
            digest_shared_artifact_kinds=tuple(digest.get('shared_artifact_kinds') or ()),
            digest_shared_source_families=tuple(digest.get('shared_source_families') or ()),
            digest_runtime_ref_union=tuple(digest.get('runtime_ref_union') or ()),
            trace_markdown_path=str(Path(json_path).with_suffix('.md')) if Path(json_path).suffix == '.json' else None,
            trace_json_path=json_path,
            browser_markdown_path=browser_selection.get('markdown_path'),
            browser_json_path=browser_selection.get('json_path'),
        )

    def render_markdown(
        self,
        trace: RuntimeReportBidirectionalTrace,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'trace_kind: RUNTIME_REPORT_BIDIRECTIONAL_TRACE',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {trace.generated_at}',
            f'selection_mode: {trace.selection_mode}',
        ]
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Bidirectional Trace',
            '',
            'This packet is a bounded read-only witness over the lawful profile→digest and digest→profile bridge surfaces.',
            '',
            '## Consistency',
            '',
            f'- Profile Name Match: {"YES" if trace.profile_name_match else "NO"}',
            f'- Digest JSON Path Match: {"YES" if trace.digest_json_path_match else "NO"}',
            f'- Digest Markdown Path Match: {"YES" if trace.digest_markdown_path_match else "NO"}',
        ])
        if trace.asymmetries:
            lines.append('- Asymmetries:')
            lines.extend(f'  - {item}' for item in trace.asymmetries)
        else:
            lines.append('- Asymmetries: NONE')
        lines.extend([
            '',
            '## Forward Path',
            '',
            f'- Source Kind: {trace.forward.source_kind}',
            f'- Selection Mode: {trace.forward.selection_mode}',
            f'- Profile Name: {trace.forward.profile_name}',
            f'- Description: {trace.forward.description or "NONE"}',
            f'- Tags: {", ".join(trace.forward.tags) if trace.forward.tags else "NONE"}',
            f'- Profile Markdown Path: {trace.forward.profile_markdown_path or "NONE"}',
            f'- Profile JSON Path: {trace.forward.profile_json_path or "NONE"}',
            f'- Digest Markdown Path: {trace.forward.digest_markdown_path}',
            f'- Digest JSON Path: {trace.forward.digest_json_path}',
            f'- Digest Generated At: {trace.forward.digest_generated_at}',
            f'- Family Count: {trace.forward.digest_family_count}',
            f'- Total Generations: {trace.forward.digest_total_generations}',
            f'- Shared Trigger Events: {", ".join(trace.forward.digest_shared_trigger_events) if trace.forward.digest_shared_trigger_events else "NONE"}',
            f'- Shared Artifact Kinds: {", ".join(trace.forward.digest_shared_artifact_kinds) if trace.forward.digest_shared_artifact_kinds else "NONE"}',
            f'- Shared Source Families: {", ".join(trace.forward.digest_shared_source_families) if trace.forward.digest_shared_source_families else "NONE"}',
            f'- Forward Trace Markdown Path: {trace.forward.trace_markdown_path or "NONE"}',
            f'- Forward Trace JSON Path: {trace.forward.trace_json_path or "NONE"}',
            f'- Browser Markdown Path: {trace.forward.browser_markdown_path or "NONE"}',
            f'- Browser JSON Path: {trace.forward.browser_json_path or "NONE"}',
        ])
        if trace.forward.digest_runtime_ref_union:
            lines.append('- Runtime Ref Union:')
            lines.extend(f'  - {item}' for item in trace.forward.digest_runtime_ref_union)
        else:
            lines.append('- Runtime Ref Union: NONE')
        lines.extend([
            '',
            '## Reverse Path',
            '',
            f'- Source Kind: {trace.reverse.source_kind}',
            f'- Selection Mode: {trace.reverse.selection_mode}',
            f'- Profile Resolution Mode: {trace.reverse.profile_resolution_mode}',
            f'- Profile Name: {trace.reverse.profile_name}',
            f'- Description: {trace.reverse.description or "NONE"}',
            f'- Tags: {", ".join(trace.reverse.tags) if trace.reverse.tags else "NONE"}',
            f'- Profile Markdown Path: {trace.reverse.profile_markdown_path or "NONE"}',
            f'- Profile JSON Path: {trace.reverse.profile_json_path or "NONE"}',
            f'- Digest Markdown Path: {trace.reverse.digest_markdown_path}',
            f'- Digest JSON Path: {trace.reverse.digest_json_path}',
            f'- Digest Generated At: {trace.reverse.digest_generated_at}',
            f'- Family Count: {trace.reverse.digest_family_count}',
            f'- Total Generations: {trace.reverse.digest_total_generations}',
            f'- Shared Trigger Events: {", ".join(trace.reverse.digest_shared_trigger_events) if trace.reverse.digest_shared_trigger_events else "NONE"}',
            f'- Shared Artifact Kinds: {", ".join(trace.reverse.digest_shared_artifact_kinds) if trace.reverse.digest_shared_artifact_kinds else "NONE"}',
            f'- Shared Source Families: {", ".join(trace.reverse.digest_shared_source_families) if trace.reverse.digest_shared_source_families else "NONE"}',
            f'- Forward Link Markdown Path: {trace.reverse.forward_link_markdown_path or "NONE"}',
            f'- Forward Link JSON Path: {trace.reverse.forward_link_json_path or "NONE"}',
        ])
        if trace.reverse.digest_runtime_ref_union:
            lines.append('- Runtime Ref Union:')
            lines.extend(f'  - {item}' for item in trace.reverse.digest_runtime_ref_union)
        else:
            lines.append('- Runtime Ref Union: NONE')
        if trace.reverse.catalog_json_paths:
            lines.append('- Catalog JSON Paths:')
            lines.extend(f'  - {item}' for item in trace.reverse.catalog_json_paths)
        else:
            lines.append('- Catalog JSON Paths: NONE')
        if trace.reverse.browser_json_paths:
            lines.append('- Browser JSON Paths:')
            lines.extend(f'  - {item}' for item in trace.reverse.browser_json_paths)
        else:
            lines.append('- Browser JSON Paths: NONE')
        lines.extend([
            '',
            '## Boundary',
            '',
            '- This packet is a read-only witness over the lawful profile→digest and digest→profile path.',
            '- It remains downstream from digest profiles, operator digests, profile catalogs, profile browsers, profile-digest traces, and digest reverse traces.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, or bidirectional-trace authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, trace: RuntimeReportBidirectionalTrace) -> str:
        payload = {
            'trace_kind': 'RUNTIME_REPORT_BIDIRECTIONAL_TRACE',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': trace.generated_at,
            'selection_mode': trace.selection_mode,
            'profile_name_match': trace.profile_name_match,
            'digest_json_path_match': trace.digest_json_path_match,
            'digest_markdown_path_match': trace.digest_markdown_path_match,
            'asymmetries': list(trace.asymmetries),
            'forward': {
                'source_kind': trace.forward.source_kind,
                'selection_mode': trace.forward.selection_mode,
                'profile_name': trace.forward.profile_name,
                'description': trace.forward.description,
                'tags': list(trace.forward.tags),
                'profile_markdown_path': trace.forward.profile_markdown_path,
                'profile_json_path': trace.forward.profile_json_path,
                'digest_markdown_path': trace.forward.digest_markdown_path,
                'digest_json_path': trace.forward.digest_json_path,
                'digest_generated_at': trace.forward.digest_generated_at,
                'digest_family_count': trace.forward.digest_family_count,
                'digest_total_generations': trace.forward.digest_total_generations,
                'digest_shared_trigger_events': list(trace.forward.digest_shared_trigger_events),
                'digest_shared_artifact_kinds': list(trace.forward.digest_shared_artifact_kinds),
                'digest_shared_source_families': list(trace.forward.digest_shared_source_families),
                'digest_runtime_ref_union': list(trace.forward.digest_runtime_ref_union),
                'trace_markdown_path': trace.forward.trace_markdown_path,
                'trace_json_path': trace.forward.trace_json_path,
                'browser_markdown_path': trace.forward.browser_markdown_path,
                'browser_json_path': trace.forward.browser_json_path,
            },
            'reverse': {
                'source_kind': trace.reverse.source_kind,
                'selection_mode': trace.reverse.selection_mode,
                'profile_resolution_mode': trace.reverse.profile_resolution_mode,
                'profile_name': trace.reverse.profile_name,
                'description': trace.reverse.description,
                'tags': list(trace.reverse.tags),
                'profile_markdown_path': trace.reverse.profile_markdown_path,
                'profile_json_path': trace.reverse.profile_json_path,
                'digest_markdown_path': trace.reverse.digest_markdown_path,
                'digest_json_path': trace.reverse.digest_json_path,
                'digest_generated_at': trace.reverse.digest_generated_at,
                'digest_family_count': trace.reverse.digest_family_count,
                'digest_total_generations': trace.reverse.digest_total_generations,
                'digest_shared_trigger_events': list(trace.reverse.digest_shared_trigger_events),
                'digest_shared_artifact_kinds': list(trace.reverse.digest_shared_artifact_kinds),
                'digest_shared_source_families': list(trace.reverse.digest_shared_source_families),
                'digest_runtime_ref_union': list(trace.reverse.digest_runtime_ref_union),
                'catalog_json_paths': list(trace.reverse.catalog_json_paths),
                'browser_json_paths': list(trace.reverse.browser_json_paths),
                'forward_link_markdown_path': trace.reverse.forward_link_markdown_path,
                'forward_link_json_path': trace.reverse.forward_link_json_path,
            },
            'boundary': [
                'Read-only witness over the lawful profile→digest and digest→profile path.',
                'Remains downstream from digest profiles, operator digests, profile catalogs, profile browsers, profile-digest traces, and digest reverse traces.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, or bidirectional-trace authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_trace_packet(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportBidirectionalTraceSelector,
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
        digests_dir: str | Path = 'ION/05_context/runtime_reports/governance/digests/profiles',
        bidirectional_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces',
        output_stem: str | None = None,
        digest_output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportBidirectionalTraceWriteResult:
        root = Path(workspace_root).resolve()
        trace = self.trace_bidirectional(
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
            digests_dir=digests_dir,
            digest_output_stem=digest_output_stem,
            created_at=created_at,
        )
        relative_dir = Path(bidirectional_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stamp = re.sub(r'[^0-9]', '', trace.generated_at)[:14]
        stem_base = trace.forward.profile_name or trace.reverse.profile_name
        stem = output_stem or f'{_safe(stem_base)}__bidirectional_trace_{stamp}'
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
        return RuntimeReportBidirectionalTraceWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            trace=trace,
        )


IonRuntimeReportBidirectionalTracer = KernelRuntimeReportBidirectionalTracer


def _selection_route(selector: RuntimeReportBidirectionalTraceSelector) -> str:
    has_forward = any([
        selector.profile_name,
        selector.profile_path,
        selector.browser_entry_index is not None,
    ])
    has_reverse = any([
        selector.digest_json_path,
        selector.digest_markdown_path,
    ])
    if has_forward and has_reverse:
        raise KernelRuntimeReportBidirectionalTraceError(
            'Bidirectional trace selector must use either a forward profile selection or a reverse digest selection, not both.'
        )
    if not has_forward and not has_reverse:
        raise KernelRuntimeReportBidirectionalTraceError(
            'Bidirectional trace selector requires either a lawful profile selection or a lawful digest selection.'
        )
    if has_forward:
        if bool(selector.profile_name) + bool(selector.profile_path) + bool(selector.browser_entry_index is not None) != 1:
            raise KernelRuntimeReportBidirectionalTraceError(
                'Forward bidirectional selection requires exactly one of profile_name, profile_path, or browser_entry_index.'
            )
        return 'FORWARD_SELECTION'
    if bool(selector.digest_json_path) == bool(selector.digest_markdown_path):
        raise KernelRuntimeReportBidirectionalTraceError(
            'Reverse bidirectional selection requires exactly one of digest_json_path or digest_markdown_path.'
        )
    return 'REVERSE_SELECTION'


def _forward_view_from_live_trace(trace: RuntimeReportProfileDigestTrace) -> RuntimeReportBidirectionalForwardView:
    browser_markdown_path = None
    browser_json_path = None
    if trace.browser_selection is not None:
        browser_markdown_path = trace.browser_selection.markdown_path
        browser_json_path = trace.browser_selection.json_path
    return RuntimeReportBidirectionalForwardView(
        source_kind='FORWARD_TRACE_LIVE',
        selection_mode=trace.selection_mode,
        profile_name=trace.profile_name,
        description=trace.description,
        tags=trace.tags,
        profile_markdown_path=trace.profile_markdown_path,
        profile_json_path=trace.profile_json_path,
        digest_markdown_path=trace.digest_markdown_path,
        digest_json_path=trace.digest_json_path,
        digest_generated_at=trace.digest_generated_at,
        digest_family_count=trace.digest_family_count,
        digest_total_generations=trace.digest_total_generations,
        digest_shared_trigger_events=trace.digest_shared_trigger_events,
        digest_shared_artifact_kinds=trace.digest_shared_artifact_kinds,
        digest_shared_source_families=trace.digest_shared_source_families,
        digest_runtime_ref_union=trace.digest_runtime_ref_union,
        trace_markdown_path=None,
        trace_json_path=None,
        browser_markdown_path=browser_markdown_path,
        browser_json_path=browser_json_path,
    )


def _forward_view_reconstructed_from_reverse(trace: RuntimeReportDigestReverseTrace) -> RuntimeReportBidirectionalForwardView:
    return RuntimeReportBidirectionalForwardView(
        source_kind='FORWARD_RECONSTRUCTED_FROM_REVERSE',
        selection_mode='REVERSE_RECONSTRUCTED',
        profile_name=trace.profile_name,
        description=trace.description,
        tags=trace.tags,
        profile_markdown_path=trace.profile_markdown_path,
        profile_json_path=trace.profile_json_path,
        digest_markdown_path=trace.digest_markdown_path,
        digest_json_path=trace.digest_json_path,
        digest_generated_at=trace.digest_generated_at,
        digest_family_count=trace.digest_family_count,
        digest_total_generations=trace.digest_total_generations,
        digest_shared_trigger_events=trace.digest_shared_trigger_events,
        digest_shared_artifact_kinds=trace.digest_shared_artifact_kinds,
        digest_shared_source_families=trace.digest_shared_source_families,
        digest_runtime_ref_union=trace.digest_runtime_ref_union,
        trace_markdown_path=None,
        trace_json_path=None,
        browser_markdown_path=None,
        browser_json_path=None,
    )


def _reverse_view_from_live_trace(trace: RuntimeReportDigestReverseTrace) -> RuntimeReportBidirectionalReverseView:
    return RuntimeReportBidirectionalReverseView(
        source_kind='REVERSE_TRACE_LIVE',
        selection_mode=trace.selection_mode,
        profile_resolution_mode=trace.profile_resolution_mode,
        profile_name=trace.profile_name,
        description=trace.description,
        tags=trace.tags,
        profile_markdown_path=trace.profile_markdown_path,
        profile_json_path=trace.profile_json_path,
        digest_markdown_path=trace.digest_markdown_path,
        digest_json_path=trace.digest_json_path,
        digest_generated_at=trace.digest_generated_at,
        digest_family_count=trace.digest_family_count,
        digest_total_generations=trace.digest_total_generations,
        digest_shared_trigger_events=trace.digest_shared_trigger_events,
        digest_shared_artifact_kinds=trace.digest_shared_artifact_kinds,
        digest_shared_source_families=trace.digest_shared_source_families,
        digest_runtime_ref_union=trace.digest_runtime_ref_union,
        catalog_json_paths=tuple(item.json_path for item in trace.catalog_surfaces),
        browser_json_paths=tuple(item.json_path for item in trace.browser_surfaces),
        forward_link_json_path=None if trace.forward_link is None else trace.forward_link.json_path,
        forward_link_markdown_path=None if trace.forward_link is None else trace.forward_link.markdown_path,
    )


def _collect_asymmetries(
    forward: RuntimeReportBidirectionalForwardView,
    reverse: RuntimeReportBidirectionalReverseView,
) -> list[str]:
    asymmetries: list[str] = []
    if forward.profile_name != reverse.profile_name:
        asymmetries.append(
            f'PROFILE_NAME_MISMATCH: forward={forward.profile_name} reverse={reverse.profile_name}'
        )
    if forward.digest_json_path != reverse.digest_json_path:
        asymmetries.append(
            f'DIGEST_JSON_PATH_MISMATCH: forward={forward.digest_json_path} reverse={reverse.digest_json_path}'
        )
    if forward.digest_markdown_path != reverse.digest_markdown_path:
        asymmetries.append(
            f'DIGEST_MARKDOWN_PATH_MISMATCH: forward={forward.digest_markdown_path} reverse={reverse.digest_markdown_path}'
        )
    if forward.digest_family_count != reverse.digest_family_count:
        asymmetries.append(
            f'DIGEST_FAMILY_COUNT_MISMATCH: forward={forward.digest_family_count} reverse={reverse.digest_family_count}'
        )
    if forward.digest_total_generations != reverse.digest_total_generations:
        asymmetries.append(
            f'DIGEST_TOTAL_GENERATIONS_MISMATCH: forward={forward.digest_total_generations} reverse={reverse.digest_total_generations}'
        )
    if forward.digest_runtime_ref_union != reverse.digest_runtime_ref_union:
        asymmetries.append('DIGEST_RUNTIME_REF_UNION_MISMATCH')
    return asymmetries


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime-bidirectional-trace'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime-bidirectional-trace'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportBidirectionalTraceError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportBidirectionalTraceError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
