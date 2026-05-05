"""Read-only temporal tracing over lawful profile↔digest bridge families.

This module extends the bidirectional profile↔digest bridge into a time-axis view.
It compares successive generations of the same lawful bridge family, resolved through
one digest profile selection route and traced through the existing I3 bidirectional
tracer. It remains explicitly downstream, read-only, and witness-only.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable, Sequence

from .runtime_report_bidirectional_trace import (
    KernelRuntimeReportBidirectionalTraceError,
    KernelRuntimeReportBidirectionalTracer,
    RuntimeReportBidirectionalTrace,
    RuntimeReportBidirectionalTraceSelector,
)
from .runtime_report_digest_profile_browser import (
    KernelRuntimeReportDigestProfileBrowser,
    KernelRuntimeReportDigestProfileBrowserError,
)
from .runtime_report_digest_profile_catalog import RuntimeReportDigestProfileCatalogQuery
from .runtime_report_digest_reverse_trace import (
    KernelRuntimeReportDigestReverseTraceError,
    KernelRuntimeReportDigestReverseTracer,
    RuntimeReportDigestReverseTraceSelector,
)
from .runtime_report_digest_profiles import (
    KernelRuntimeReportDigestProfileError,
    KernelRuntimeReportDigestProfiler,
)


class KernelRuntimeReportBidirectionalTemporalError(Exception):
    """Raised when one temporal bridge-family request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportBidirectionalTemporalSelector:
    profile_name: str | None = None
    profile_path: str | None = None
    browser_query: RuntimeReportDigestProfileCatalogQuery | None = None
    browser_entry_index: int | None = None
    limit: int | None = None


@dataclass(frozen=True)
class RuntimeReportBidirectionalTemporalGeneration:
    generation_label: str
    generation_index: int
    digest_generated_at: str
    digest_markdown_path: str
    digest_json_path: str
    profile_name: str
    selection_mode: str
    forward_source_kind: str
    reverse_source_kind: str
    reverse_profile_resolution_mode: str
    profile_name_match: bool
    digest_json_path_match: bool
    digest_markdown_path_match: bool
    asymmetries: tuple[str, ...]
    trigger_events: tuple[str, ...]
    artifact_kinds: tuple[str, ...]
    source_families: tuple[str, ...]
    runtime_refs: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportBidirectionalTemporalAspectGeneration:
    generation_label: str
    generation_index: int
    values: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportBidirectionalTemporalAspectTransition:
    from_generation_label: str
    to_generation_label: str
    added_values: tuple[str, ...]
    removed_values: tuple[str, ...]
    changed: bool


@dataclass(frozen=True)
class RuntimeReportBidirectionalTemporalAspect:
    aspect_name: str
    label: str
    stable_values: tuple[str, ...]
    emergent_values: tuple[str, ...]
    vanished_values: tuple[str, ...]
    generations: tuple[RuntimeReportBidirectionalTemporalAspectGeneration, ...]
    transitions: tuple[RuntimeReportBidirectionalTemporalAspectTransition, ...]


@dataclass(frozen=True)
class RuntimeReportBidirectionalTemporalTrace:
    generated_at: str
    read_only_mode: bool
    selector_mode: str
    profile_name: str
    profile_markdown_path: str | None
    profile_json_path: str | None
    digests_dir: str
    generation_count: int
    generations: tuple[RuntimeReportBidirectionalTemporalGeneration, ...]
    aspects: tuple[RuntimeReportBidirectionalTemporalAspect, ...]


@dataclass(frozen=True)
class RuntimeReportBidirectionalTemporalWriteResult:
    markdown_path: str
    json_path: str
    trace: RuntimeReportBidirectionalTemporalTrace


class KernelRuntimeReportBidirectionalTemporalTracer:
    """Trace successive generations of one lawful profile↔digest bridge family."""

    def __init__(
        self,
        *,
        tracer: KernelRuntimeReportBidirectionalTracer | None = None,
        reverse_tracer: KernelRuntimeReportDigestReverseTracer | None = None,
        profiler: KernelRuntimeReportDigestProfiler | None = None,
        browser: KernelRuntimeReportDigestProfileBrowser | None = None,
    ) -> None:
        self._tracer = tracer or KernelRuntimeReportBidirectionalTracer()
        self._reverse_tracer = reverse_tracer or KernelRuntimeReportDigestReverseTracer()
        self._profiler = profiler or KernelRuntimeReportDigestProfiler()
        self._browser = browser or KernelRuntimeReportDigestProfileBrowser(profiler=self._profiler)

    def trace_bridge_family(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportBidirectionalTemporalSelector,
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
        created_at: str | None = None,
    ) -> RuntimeReportBidirectionalTemporalTrace:
        root = Path(workspace_root).resolve()
        selector_mode, profile_name, profile_markdown_path, profile_json_path = self._resolve_profile_selection(
            root,
            selector,
            profiles_dir=profiles_dir,
            created_at=created_at,
        )
        digest_paths = self._resolve_digest_family(
            root,
            profile_name=profile_name,
            traces_dir=traces_dir,
            catalogs_dir=catalogs_dir,
            browser_dir=browser_dir,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            runtime_browser_dir=runtime_browser_dir,
            crosslinks_dir=crosslinks_dir,
            digests_dir=digests_dir,
            limit=selector.limit,
            created_at=created_at,
        )
        if len(digest_paths) < 2:
            raise KernelRuntimeReportBidirectionalTemporalError(
                f'Bidirectional temporal tracing requires at least two digest generations for profile: {profile_name}'
            )

        traces: list[RuntimeReportBidirectionalTrace] = []
        for digest_json_path in digest_paths:
            try:
                trace = self._tracer.trace_bidirectional(
                    root,
                    RuntimeReportBidirectionalTraceSelector(digest_json_path=digest_json_path),
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
                    created_at=created_at,
                )
            except KernelRuntimeReportBidirectionalTraceError as exc:
                raise KernelRuntimeReportBidirectionalTemporalError(str(exc)) from exc
            traces.append(trace)

        generations = tuple(
            RuntimeReportBidirectionalTemporalGeneration(
                generation_label=f'Generation {index}',
                generation_index=index,
                digest_generated_at=trace.forward.digest_generated_at,
                digest_markdown_path=trace.forward.digest_markdown_path,
                digest_json_path=trace.forward.digest_json_path,
                profile_name=trace.forward.profile_name,
                selection_mode=trace.selection_mode,
                forward_source_kind=trace.forward.source_kind,
                reverse_source_kind=trace.reverse.source_kind,
                reverse_profile_resolution_mode=trace.reverse.profile_resolution_mode,
                profile_name_match=trace.profile_name_match,
                digest_json_path_match=trace.digest_json_path_match,
                digest_markdown_path_match=trace.digest_markdown_path_match,
                asymmetries=tuple(trace.asymmetries),
                trigger_events=_sorted_unique(trace.forward.digest_shared_trigger_events + trace.reverse.digest_shared_trigger_events),
                artifact_kinds=_sorted_unique(trace.forward.digest_shared_artifact_kinds + trace.reverse.digest_shared_artifact_kinds),
                source_families=_sorted_unique(trace.forward.digest_shared_source_families + trace.reverse.digest_shared_source_families),
                runtime_refs=_sorted_unique(trace.forward.digest_runtime_ref_union + trace.reverse.digest_runtime_ref_union),
            )
            for index, trace in enumerate(traces, start=1)
        )
        aspects = self._build_aspects(generations)
        return RuntimeReportBidirectionalTemporalTrace(
            generated_at=created_at or _iso_now(),
            read_only_mode=True,
            selector_mode=selector_mode,
            profile_name=profile_name,
            profile_markdown_path=profile_markdown_path,
            profile_json_path=profile_json_path,
            digests_dir=str(digests_dir),
            generation_count=len(generations),
            generations=generations,
            aspects=aspects,
        )

    def _resolve_profile_selection(
        self,
        root: Path,
        selector: RuntimeReportBidirectionalTemporalSelector,
        *,
        profiles_dir: str | Path,
        created_at: str | None,
    ) -> tuple[str, str, str | None, str | None]:
        profile_fields = [bool(selector.profile_name), bool(selector.profile_path), bool(selector.browser_query or selector.browser_entry_index is not None)]
        if sum(profile_fields) != 1:
            raise KernelRuntimeReportBidirectionalTemporalError(
                'Provide exactly one profile selection mode: profile_name, profile_path, or browser selection.'
            )
        if selector.profile_name or selector.profile_path:
            try:
                profile = self._profiler.load_profile(
                    root,
                    profile_name=selector.profile_name,
                    profile_path=selector.profile_path,
                    profiles_dir=profiles_dir,
                )
            except KernelRuntimeReportDigestProfileError as exc:
                raise KernelRuntimeReportBidirectionalTemporalError(str(exc)) from exc
            return (
                'PROFILE_NAME' if selector.profile_name else 'PROFILE_PATH',
                profile.profile_name,
                str(Path(profiles_dir) / f'{_safe(profile.profile_name)}.md'),
                str(Path(profiles_dir) / f'{_safe(profile.profile_name)}.json'),
            )
        if selector.browser_query is None or selector.browser_entry_index is None:
            raise KernelRuntimeReportBidirectionalTemporalError(
                'Browser selection requires both browser_query and browser_entry_index.'
            )
        try:
            result = self._browser.browse(
                root,
                selector.browser_query,
                profiles_dir=profiles_dir,
                created_at=created_at,
            )
        except KernelRuntimeReportDigestProfileBrowserError as exc:
            raise KernelRuntimeReportBidirectionalTemporalError(str(exc)) from exc
        if selector.browser_entry_index < 1 or selector.browser_entry_index > len(result.entries):
            raise KernelRuntimeReportBidirectionalTemporalError(
                f'Browser entry index out of range: {selector.browser_entry_index}'
            )
        entry = result.entries[selector.browser_entry_index - 1]
        return ('BROWSER_ENTRY', entry.profile_name, entry.markdown_path, entry.json_path)

    def _resolve_digest_family(
        self,
        root: Path,
        *,
        profile_name: str,
        traces_dir: str | Path,
        catalogs_dir: str | Path,
        browser_dir: str | Path,
        packet_index_path: str | Path,
        operator_dashboard_path: str | Path,
        navigation_dir: str | Path,
        runtime_browser_dir: str | Path,
        crosslinks_dir: str | Path,
        digests_dir: str | Path,
        limit: int | None,
        created_at: str | None,
    ) -> tuple[str, ...]:
        digests_root = _resolve_relative_file(root, Path(digests_dir))
        if not digests_root.exists():
            raise KernelRuntimeReportBidirectionalTemporalError(f'Digests directory not found: {digests_dir}')
        matches: list[tuple[str, Path]] = []
        for candidate in sorted(digests_root.glob('*.json')):
            try:
                reverse = self._reverse_tracer.trace_digest_origin(
                    root,
                    RuntimeReportDigestReverseTraceSelector(digest_json_path=str(Path(digests_dir) / candidate.name)),
                    profiles_dir='ION/05_context/runtime_reports/governance/digest_profiles',
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
            except KernelRuntimeReportDigestReverseTraceError:
                continue
            if reverse.profile_name != profile_name:
                continue
            matches.append((reverse.digest_generated_at, candidate))
        matches.sort(key=lambda item: (item[0], item[1].name))
        selected = matches[-limit:] if limit is not None else matches
        return tuple(str(Path(digests_dir) / item[1].name) for item in selected)

    def _build_aspects(
        self,
        generations: Sequence[RuntimeReportBidirectionalTemporalGeneration],
    ) -> tuple[RuntimeReportBidirectionalTemporalAspect, ...]:
        aspect_specs = (
            ('FORWARD_SOURCE_KIND', 'Forward Source Kind', lambda item: (item.forward_source_kind,)),
            ('REVERSE_SOURCE_KIND', 'Reverse Source Kind', lambda item: (item.reverse_source_kind,)),
            ('REVERSE_PROFILE_RESOLUTION_MODE', 'Reverse Profile Resolution Mode', lambda item: (item.reverse_profile_resolution_mode,)),
            (
                'CONSISTENCY_MARKERS',
                'Consistency Markers',
                lambda item: tuple(
                    marker
                    for marker, flag in (
                        ('PROFILE_NAME_MATCH', item.profile_name_match),
                        ('DIGEST_JSON_PATH_MATCH', item.digest_json_path_match),
                        ('DIGEST_MARKDOWN_PATH_MATCH', item.digest_markdown_path_match),
                    )
                    if flag
                ),
            ),
            ('ASYMMETRIES', 'Asymmetries', lambda item: item.asymmetries),
            ('TRIGGER_EVENTS', 'Trigger Events', lambda item: item.trigger_events),
            ('ARTIFACT_KINDS', 'Artifact Kinds', lambda item: item.artifact_kinds),
            ('SOURCE_FAMILIES', 'Source Families', lambda item: item.source_families),
            ('RUNTIME_REFS', 'Runtime Refs', lambda item: item.runtime_refs),
        )
        return tuple(
            _build_aspect(name, label, generations, extractor)
            for name, label, extractor in aspect_specs
        )

    def render_markdown(
        self,
        trace: RuntimeReportBidirectionalTemporalTrace,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'trace_kind: RUNTIME_REPORT_BIDIRECTIONAL_TEMPORAL_TRACE',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {trace.generated_at}',
            f'selector_mode: {trace.selector_mode}',
            f'profile_name: {trace.profile_name}',
            f'digests_dir: {trace.digests_dir}',
            f'generation_count: {trace.generation_count}',
        ]
        if trace.profile_markdown_path is not None:
            lines.append(f'profile_markdown_path: {trace.profile_markdown_path}')
        if trace.profile_json_path is not None:
            lines.append(f'profile_json_path: {trace.profile_json_path}')
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Bidirectional Temporal Trace',
            '',
            'This packet is a bounded read-only temporal trace over successive generations of one lawful profile↔digest bridge family.',
            '',
            '## Bridge Family',
            '',
            f'- Selector Mode: {trace.selector_mode}',
            f'- Profile Name: {trace.profile_name}',
            f'- Profile Markdown Path: {trace.profile_markdown_path or "NONE"}',
            f'- Profile JSON Path: {trace.profile_json_path or "NONE"}',
            f'- Digests Directory: {trace.digests_dir}',
            f'- Generation Count: {trace.generation_count}',
            '',
            '## Generations',
            '',
        ])
        for generation in trace.generations:
            lines.extend([
                f'### {generation.generation_label}',
                '',
                f'- Digest Generated At: {generation.digest_generated_at}',
                f'- Digest Markdown Path: {generation.digest_markdown_path}',
                f'- Digest JSON Path: {generation.digest_json_path}',
                f'- Selection Mode: {generation.selection_mode}',
                f'- Forward Source Kind: {generation.forward_source_kind}',
                f'- Reverse Source Kind: {generation.reverse_source_kind}',
                f'- Reverse Profile Resolution Mode: {generation.reverse_profile_resolution_mode or "NONE"}',
                f'- Profile Name Match: {"YES" if generation.profile_name_match else "NO"}',
                f'- Digest JSON Path Match: {"YES" if generation.digest_json_path_match else "NO"}',
                f'- Digest Markdown Path Match: {"YES" if generation.digest_markdown_path_match else "NO"}',
                f'- Trigger Events: {", ".join(generation.trigger_events) if generation.trigger_events else "NONE"}',
                f'- Artifact Kinds: {", ".join(generation.artifact_kinds) if generation.artifact_kinds else "NONE"}',
                f'- Source Families: {", ".join(generation.source_families) if generation.source_families else "NONE"}',
            ])
            if generation.runtime_refs:
                lines.append('- Runtime Refs:')
                lines.extend(f'  - {item}' for item in generation.runtime_refs)
            else:
                lines.append('- Runtime Refs: NONE')
            if generation.asymmetries:
                lines.append('- Asymmetries:')
                lines.extend(f'  - {item}' for item in generation.asymmetries)
            else:
                lines.append('- Asymmetries: NONE')
            lines.append('')
        lines.extend(['## Aspect-by-Aspect Temporal Comparison', ''])
        for aspect in trace.aspects:
            lines.extend([
                f'### {aspect.label}',
                '',
                f'- Stable Values: {", ".join(aspect.stable_values) if aspect.stable_values else "NONE"}',
                f'- Emergent Values: {", ".join(aspect.emergent_values) if aspect.emergent_values else "NONE"}',
                f'- Vanished Values: {", ".join(aspect.vanished_values) if aspect.vanished_values else "NONE"}',
                '',
            ])
            for item in aspect.generations:
                lines.extend([
                    f'#### {item.generation_label}',
                    '',
                    f'- Values: {", ".join(item.values) if item.values else "NONE"}',
                    '',
                ])
            if aspect.transitions:
                lines.append('#### Transitions')
                lines.append('')
                for transition in aspect.transitions:
                    lines.extend([
                        f'- {transition.from_generation_label} → {transition.to_generation_label}: {"CHANGED" if transition.changed else "UNCHANGED"}',
                        f'  - Added: {", ".join(transition.added_values) if transition.added_values else "NONE"}',
                        f'  - Removed: {", ".join(transition.removed_values) if transition.removed_values else "NONE"}',
                    ])
                lines.append('')
        lines.extend([
            '## Boundary',
            '',
            '- This packet is a read-only temporal trace over successive lawful profile↔digest bridge generations.',
            '- It remains downstream from bidirectional traces, profile-to-digest traces, digest reverse traces, digest profiles, digests, catalogs, and browsers.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, bidirectional-trace authority, temporal authority, or bridge-history authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, trace: RuntimeReportBidirectionalTemporalTrace) -> str:
        payload = {
            'trace_kind': 'RUNTIME_REPORT_BIDIRECTIONAL_TEMPORAL_TRACE',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': trace.generated_at,
            'selector_mode': trace.selector_mode,
            'profile_name': trace.profile_name,
            'profile_markdown_path': trace.profile_markdown_path,
            'profile_json_path': trace.profile_json_path,
            'digests_dir': trace.digests_dir,
            'generation_count': trace.generation_count,
            'generations': [
                {
                    'generation_label': item.generation_label,
                    'generation_index': item.generation_index,
                    'digest_generated_at': item.digest_generated_at,
                    'digest_markdown_path': item.digest_markdown_path,
                    'digest_json_path': item.digest_json_path,
                    'profile_name': item.profile_name,
                    'selection_mode': item.selection_mode,
                    'forward_source_kind': item.forward_source_kind,
                    'reverse_source_kind': item.reverse_source_kind,
                    'reverse_profile_resolution_mode': item.reverse_profile_resolution_mode,
                    'profile_name_match': item.profile_name_match,
                    'digest_json_path_match': item.digest_json_path_match,
                    'digest_markdown_path_match': item.digest_markdown_path_match,
                    'asymmetries': list(item.asymmetries),
                    'trigger_events': list(item.trigger_events),
                    'artifact_kinds': list(item.artifact_kinds),
                    'source_families': list(item.source_families),
                    'runtime_refs': list(item.runtime_refs),
                }
                for item in trace.generations
            ],
            'aspects': [
                {
                    'aspect_name': aspect.aspect_name,
                    'label': aspect.label,
                    'stable_values': list(aspect.stable_values),
                    'emergent_values': list(aspect.emergent_values),
                    'vanished_values': list(aspect.vanished_values),
                    'generations': [
                        {
                            'generation_label': item.generation_label,
                            'generation_index': item.generation_index,
                            'values': list(item.values),
                        }
                        for item in aspect.generations
                    ],
                    'transitions': [
                        {
                            'from_generation_label': item.from_generation_label,
                            'to_generation_label': item.to_generation_label,
                            'added_values': list(item.added_values),
                            'removed_values': list(item.removed_values),
                            'changed': item.changed,
                        }
                        for item in aspect.transitions
                    ],
                }
                for aspect in trace.aspects
            ],
            'boundary': [
                'Read-only temporal trace over successive lawful profile↔digest bridge generations.',
                'Remains downstream from bidirectional traces, profile-to-digest traces, digest reverse traces, digest profiles, digests, catalogs, and browsers.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, bidirectional-trace authority, temporal authority, or bridge-history authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_trace_packet(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportBidirectionalTemporalSelector,
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
        temporal_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/temporal',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportBidirectionalTemporalWriteResult:
        root = Path(workspace_root).resolve()
        trace = self.trace_bridge_family(
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
            created_at=created_at,
        )
        relative_dir = Path(temporal_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stamp = re.sub(r'[^0-9]', '', trace.generated_at)[:14]
        stem = output_stem or f'{_safe(trace.profile_name)}__bidirectional_temporal_{stamp}'
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
        return RuntimeReportBidirectionalTemporalWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            trace=trace,
        )


IonRuntimeReportBidirectionalTemporalTracer = KernelRuntimeReportBidirectionalTemporalTracer


def _build_aspect(
    aspect_name: str,
    label: str,
    generations: Sequence[RuntimeReportBidirectionalTemporalGeneration],
    extractor,
) -> RuntimeReportBidirectionalTemporalAspect:
    generation_views = tuple(
        RuntimeReportBidirectionalTemporalAspectGeneration(
            generation_label=item.generation_label,
            generation_index=item.generation_index,
            values=_sorted_unique(extractor(item)),
        )
        for item in generations
    )
    value_sets = [set(item.values) for item in generation_views]
    stable = tuple(sorted(set.intersection(*value_sets))) if value_sets else ()
    transitions: list[RuntimeReportBidirectionalTemporalAspectTransition] = []
    added_union: set[str] = set()
    removed_union: set[str] = set()
    for earlier, later in zip(generation_views, generation_views[1:]):
        earlier_set = set(earlier.values)
        later_set = set(later.values)
        added = tuple(sorted(later_set - earlier_set))
        removed = tuple(sorted(earlier_set - later_set))
        if added:
            added_union.update(added)
        if removed:
            removed_union.update(removed)
        transitions.append(
            RuntimeReportBidirectionalTemporalAspectTransition(
                from_generation_label=earlier.generation_label,
                to_generation_label=later.generation_label,
                added_values=added,
                removed_values=removed,
                changed=bool(added or removed),
            )
        )
    return RuntimeReportBidirectionalTemporalAspect(
        aspect_name=aspect_name,
        label=label,
        stable_values=stable,
        emergent_values=tuple(sorted(added_union)),
        vanished_values=tuple(sorted(removed_union)),
        generations=generation_views,
        transitions=tuple(transitions),
    )


def _sorted_unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({value for value in values if value}))


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportBidirectionalTemporalError(
            f'Absolute paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportBidirectionalTemporalError(
            f'Path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime-profile'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime-profile'


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
