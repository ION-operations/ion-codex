"""Read-only profile-to-digest tracing over digest-profile browser and digest surfaces.

This module follows one lawful digest-profile selection into the H1 operator digest it
renders. Selection may be direct (profile name/path) or via an H4 browser entry, but
rendering always delegates through the existing H2 profile-digest pipeline rather than
bypassing profile definitions, family summaries, or operator digests.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Sequence

from .runtime_report_digest_profile_browser import (
    KernelRuntimeReportDigestProfileBrowser,
    KernelRuntimeReportDigestProfileBrowserError,
    RuntimeReportDigestProfileBrowserEntry,
)
from .runtime_report_digest_profile_catalog import RuntimeReportDigestProfileCatalogQuery
from .runtime_report_digest_profiles import (
    KernelRuntimeReportDigestProfileError,
    KernelRuntimeReportDigestProfiler,
    RuntimeReportOperatorDigestProfile,
)


class KernelRuntimeReportProfileDigestTraceError(Exception):
    """Raised when one profile-to-digest trace cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportProfileDigestTraceSelector:
    profile_name: str | None = None
    profile_path: str | None = None
    browser_query: RuntimeReportDigestProfileCatalogQuery | None = None
    browser_entry_index: int | None = None


@dataclass(frozen=True)
class RuntimeReportProfileDigestTraceSelectorView:
    label: str
    source_ref: str | None
    source_ref_contains: str | None
    trigger_event: str | None
    artifact_kind: str | None
    source_family: str | None
    limit: int | None


@dataclass(frozen=True)
class RuntimeReportProfileDigestTraceBrowserSelection:
    entry_index: int
    matched_count: int
    total_profiles: int
    query: RuntimeReportDigestProfileCatalogQuery
    profile_name: str
    description: str
    tags: tuple[str, ...]
    selector_labels: tuple[str, ...]
    markdown_path: str | None
    json_path: str


@dataclass(frozen=True)
class RuntimeReportProfileDigestTrace:
    generated_at: str
    read_only_mode: bool
    selection_mode: str
    profile_name: str
    description: str
    tags: tuple[str, ...]
    profile_markdown_path: str | None
    profile_json_path: str | None
    selectors: tuple[RuntimeReportProfileDigestTraceSelectorView, ...]
    browser_selection: RuntimeReportProfileDigestTraceBrowserSelection | None
    digest_markdown_path: str
    digest_json_path: str
    digest_generated_at: str
    digest_family_count: int
    digest_total_generations: int
    digest_shared_trigger_events: tuple[str, ...]
    digest_shared_artifact_kinds: tuple[str, ...]
    digest_shared_source_families: tuple[str, ...]
    digest_runtime_ref_union: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportProfileDigestTraceWriteResult:
    markdown_path: str
    json_path: str
    trace: RuntimeReportProfileDigestTrace


class KernelRuntimeReportProfileDigestTracer:
    """Trace one lawful digest-profile selection into a rendered H1 operator digest."""

    def __init__(
        self,
        *,
        profiler: KernelRuntimeReportDigestProfiler | None = None,
        browser: KernelRuntimeReportDigestProfileBrowser | None = None,
    ) -> None:
        self._profiler = profiler or KernelRuntimeReportDigestProfiler()
        self._browser = browser or KernelRuntimeReportDigestProfileBrowser(profiler=self._profiler)

    def trace_profile_to_digest(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportProfileDigestTraceSelector,
        *,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        digests_dir: str | Path = 'ION/05_context/runtime_reports/governance/digests/profiles',
        digest_output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportProfileDigestTrace:
        root = Path(workspace_root).resolve()
        selection_mode, profile, browser_selection = self._resolve_profile_selection(
            root,
            selector,
            profiles_dir=profiles_dir,
            created_at=created_at,
        )
        try:
            digest_result = self._profiler.write_profile_digest_packet(
                root,
                profile=profile,
                packet_index_path=packet_index_path,
                operator_dashboard_path=operator_dashboard_path,
                navigation_dir=navigation_dir,
                browser_dir=browser_dir,
                crosslinks_dir=crosslinks_dir,
                digests_dir=digests_dir,
                output_stem=digest_output_stem,
                created_at=created_at,
            )
        except KernelRuntimeReportDigestProfileError as exc:
            raise KernelRuntimeReportProfileDigestTraceError(str(exc)) from exc

        return RuntimeReportProfileDigestTrace(
            generated_at=created_at or _iso_now(),
            read_only_mode=True,
            selection_mode=selection_mode,
            profile_name=profile.profile_name,
            description=profile.description,
            tags=profile.tags,
            profile_markdown_path=browser_selection.markdown_path if browser_selection else _profile_markdown_path(root, profile.profile_name, profiles_dir),
            profile_json_path=browser_selection.json_path if browser_selection else _profile_json_path(root, profile.profile_name, profiles_dir),
            selectors=tuple(_selector_view(item.label, item.selector) for item in profile.selectors),
            browser_selection=browser_selection,
            digest_markdown_path=digest_result.digest_markdown_path,
            digest_json_path=digest_result.digest_json_path,
            digest_generated_at=digest_result.digest.generated_at,
            digest_family_count=digest_result.digest.family_count,
            digest_total_generations=digest_result.digest.total_generations,
            digest_shared_trigger_events=digest_result.digest.shared_trigger_events,
            digest_shared_artifact_kinds=digest_result.digest.shared_artifact_kinds,
            digest_shared_source_families=digest_result.digest.shared_source_families,
            digest_runtime_ref_union=digest_result.digest.runtime_ref_union,
        )

    def render_markdown(
        self,
        trace: RuntimeReportProfileDigestTrace,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'trace_kind: RUNTIME_REPORT_PROFILE_DIGEST_TRACE',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {trace.generated_at}',
            f'selection_mode: {trace.selection_mode}',
            f'profile_name: {trace.profile_name}',
            f'digest_markdown_path: {trace.digest_markdown_path}',
            f'digest_json_path: {trace.digest_json_path}',
        ]
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Profile Digest Trace',
            '',
            'This packet is a bounded read-only bridge from one lawful digest-profile selection into the H1 operator digest it renders.',
            '',
            '## Trace Scope',
            '',
            f'- Selection Mode: {trace.selection_mode}',
            f'- Profile Name: {trace.profile_name}',
            f'- Tags: {", ".join(trace.tags) if trace.tags else "NONE"}',
            f'- Selector Count: {len(trace.selectors)}',
            '',
            '## Profile Definition',
            '',
            f'- Description: {trace.description or "NONE"}',
            f'- Definition Markdown Path: {trace.profile_markdown_path or "NONE"}',
            f'- Definition JSON Path: {trace.profile_json_path or "NONE"}',
            '',
        ])
        if trace.browser_selection is not None:
            browser = trace.browser_selection
            lines.extend([
                '## Browser Selection',
                '',
                f'- Entry Index: {browser.entry_index}',
                f'- Matched Profiles: {browser.matched_count}/{browser.total_profiles}',
                f'- Query Profile Name Contains: {browser.query.profile_name_contains or "ANY"}',
                f'- Query Tag: {browser.query.tag or "ANY"}',
                f'- Query Selector Label Contains: {browser.query.selector_label_contains or "ANY"}',
                f'- Query Description Contains: {browser.query.description_contains or "ANY"}',
                f'- Query Limit: {browser.query.limit if browser.query.limit is not None else "ANY"}',
                f'- Browser Markdown Path: {browser.markdown_path or "NONE"}',
                f'- Browser JSON Path: {browser.json_path}',
                '',
            ])
        lines.extend([
            '## Delegated Digest Render',
            '',
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
            '## Profile Selectors',
            '',
        ])
        for index, selector in enumerate(trace.selectors, start=1):
            lines.extend([
                f'### {index}. {selector.label}',
                '',
                f'- Source Ref: {selector.source_ref or "NONE"}',
                f'- Source Ref Contains: {selector.source_ref_contains or "NONE"}',
                f'- Trigger Event: {selector.trigger_event or "NONE"}',
                f'- Artifact Kind: {selector.artifact_kind or "NONE"}',
                f'- Source Family: {selector.source_family or "NONE"}',
                f'- Limit: {selector.limit if selector.limit is not None else "NONE"}',
                '',
            ])
        lines.extend([
            '## Boundary',
            '',
            '- This packet is a read-only bridge over a lawful profile selection and the downstream operator digest rendered from it.',
            '- It remains downstream from digest profiles, family summaries, operator digests, and profile-browser/catalog surfaces.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, digest authority, or trace authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, trace: RuntimeReportProfileDigestTrace) -> str:
        payload = {
            'trace_kind': 'RUNTIME_REPORT_PROFILE_DIGEST_TRACE',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': trace.generated_at,
            'selection_mode': trace.selection_mode,
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
            'browser_selection': None if trace.browser_selection is None else {
                'entry_index': trace.browser_selection.entry_index,
                'matched_count': trace.browser_selection.matched_count,
                'total_profiles': trace.browser_selection.total_profiles,
                'query': {
                    'profile_name_contains': trace.browser_selection.query.profile_name_contains,
                    'tag': trace.browser_selection.query.tag,
                    'selector_label_contains': trace.browser_selection.query.selector_label_contains,
                    'description_contains': trace.browser_selection.query.description_contains,
                    'limit': trace.browser_selection.query.limit,
                },
                'profile_name': trace.browser_selection.profile_name,
                'description': trace.browser_selection.description,
                'tags': list(trace.browser_selection.tags),
                'selector_labels': list(trace.browser_selection.selector_labels),
                'markdown_path': trace.browser_selection.markdown_path,
                'json_path': trace.browser_selection.json_path,
            },
            'delegation_chain': [
                trace.selection_mode,
                'RUNTIME_REPORT_OPERATOR_DIGEST_PROFILE',
                'RUNTIME_REPORT_OPERATOR_DIGEST',
            ],
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
            'boundary': [
                'Read-only bridge over a lawful profile selection and the downstream operator digest rendered from it.',
                'Remains downstream from digest profiles, family summaries, operator digests, and profile-browser/catalog surfaces.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, digest authority, or trace authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_trace_packet(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportProfileDigestTraceSelector,
        *,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        digests_dir: str | Path = 'ION/05_context/runtime_reports/governance/digests/profiles',
        traces_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/traces',
        output_stem: str | None = None,
        digest_output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportProfileDigestTraceWriteResult:
        root = Path(workspace_root).resolve()
        trace = self.trace_profile_to_digest(
            root,
            selector,
            profiles_dir=profiles_dir,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            browser_dir=browser_dir,
            crosslinks_dir=crosslinks_dir,
            digests_dir=digests_dir,
            digest_output_stem=digest_output_stem,
            created_at=created_at,
        )
        relative_dir = Path(traces_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stamp = re.sub(r'[^0-9]', '', trace.generated_at)[:14]
        stem = output_stem or f'{_safe(trace.profile_name)}__profile_digest_trace_{stamp}'
        markdown_relative = relative_dir / f'{stem}.md'
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        markdown_resolved.write_text(
            self.render_markdown(trace, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        json_relative = relative_dir / f'{stem}.json'
        json_resolved = _resolve_relative_file(root, json_relative)
        json_resolved.write_text(self.render_json(trace), encoding='utf-8')
        return RuntimeReportProfileDigestTraceWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            trace=trace,
        )

    def _resolve_profile_selection(
        self,
        root: Path,
        selector: RuntimeReportProfileDigestTraceSelector,
        *,
        profiles_dir: str | Path,
        created_at: str | None,
    ) -> tuple[str, RuntimeReportOperatorDigestProfile, RuntimeReportProfileDigestTraceBrowserSelection | None]:
        has_direct = bool(selector.profile_name) or bool(selector.profile_path)
        has_browser = selector.browser_entry_index is not None or selector.browser_query is not None
        if has_direct and has_browser:
            raise KernelRuntimeReportProfileDigestTraceError(
                'Profile digest trace selector must use either direct profile selection or browser-entry selection, not both.'
            )
        if not has_direct and not has_browser:
            raise KernelRuntimeReportProfileDigestTraceError(
                'Profile digest trace selector requires either profile_name/profile_path or browser_entry_index with optional browser_query.'
            )
        if has_direct:
            if bool(selector.profile_name) == bool(selector.profile_path):
                raise KernelRuntimeReportProfileDigestTraceError(
                    'Direct profile trace requires exactly one of profile_name or profile_path.'
                )
            try:
                profile = self._profiler.load_profile(
                    root,
                    profile_name=selector.profile_name,
                    profile_path=selector.profile_path,
                    profiles_dir=profiles_dir,
                )
            except KernelRuntimeReportDigestProfileError as exc:
                raise KernelRuntimeReportProfileDigestTraceError(str(exc)) from exc
            mode = 'PROFILE_NAME' if selector.profile_name else 'PROFILE_PATH'
            return mode, profile, None

        if selector.browser_entry_index is None or selector.browser_entry_index <= 0:
            raise KernelRuntimeReportProfileDigestTraceError(
                'Browser-entry profile trace requires a positive browser_entry_index.'
            )
        query = selector.browser_query or RuntimeReportDigestProfileCatalogQuery(limit=selector.browser_entry_index)
        try:
            browser_result = self._browser.browse(
                root,
                query,
                profiles_dir=profiles_dir,
                created_at=created_at,
            )
        except (KernelRuntimeReportDigestProfileBrowserError, KernelRuntimeReportDigestProfileError) as exc:
            raise KernelRuntimeReportProfileDigestTraceError(str(exc)) from exc
        if selector.browser_entry_index > len(browser_result.entries):
            raise KernelRuntimeReportProfileDigestTraceError(
                f'Browser entry index {selector.browser_entry_index} exceeds matched profile count {len(browser_result.entries)}.'
            )
        entry = browser_result.entries[selector.browser_entry_index - 1]
        try:
            profile = self._profiler.load_profile(
                root,
                profile_name=entry.profile_name,
                profiles_dir=profiles_dir,
            )
        except KernelRuntimeReportDigestProfileError as exc:
            raise KernelRuntimeReportProfileDigestTraceError(str(exc)) from exc
        return (
            'BROWSER_ENTRY',
            profile,
            RuntimeReportProfileDigestTraceBrowserSelection(
                entry_index=selector.browser_entry_index,
                matched_count=browser_result.catalog.matched_count,
                total_profiles=browser_result.catalog.total_profiles,
                query=browser_result.catalog.query,
                profile_name=entry.profile_name,
                description=entry.description,
                tags=entry.tags,
                selector_labels=entry.selector_labels,
                markdown_path=entry.markdown_path,
                json_path=entry.json_path,
            ),
        )


IonRuntimeReportProfileDigestTracer = KernelRuntimeReportProfileDigestTracer


def _selector_view(label: str, selector: object) -> RuntimeReportProfileDigestTraceSelectorView:
    return RuntimeReportProfileDigestTraceSelectorView(
        label=label,
        source_ref=getattr(selector, 'source_ref', None),
        source_ref_contains=getattr(selector, 'source_ref_contains', None),
        trigger_event=getattr(selector, 'trigger_event', None),
        artifact_kind=getattr(selector, 'artifact_kind', None),
        source_family=getattr(selector, 'source_family', None),
        limit=getattr(selector, 'limit', None),
    )


def _profile_markdown_path(root: Path, profile_name: str, profiles_dir: str | Path) -> str | None:
    relative = Path(profiles_dir) / f'{_safe(profile_name)}.md'
    resolved = _resolve_relative_file(root, relative)
    return str(relative) if resolved.exists() else None


def _profile_json_path(root: Path, profile_name: str, profiles_dir: str | Path) -> str | None:
    relative = Path(profiles_dir) / f'{_safe(profile_name)}.json'
    resolved = _resolve_relative_file(root, relative)
    return str(relative) if resolved.exists() else None


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime-profile'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime-profile'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportProfileDigestTraceError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportProfileDigestTraceError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
