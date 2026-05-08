"""Read-only comparison over multiple lawful bidirectional profile↔digest traces.

This module compares two or more bidirectional trace surfaces side by side. Inputs may
be live lawful selectors delegated into the existing I3 bidirectional tracer or
previously written bidirectional-trace JSON packets. The resulting packet remains a
bounded downstream witness and does not become a ranking, control, or authority layer.
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


class KernelRuntimeReportBidirectionalTraceComparisonError(Exception):
    """Raised when a bidirectional-trace comparison cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportBidirectionalTraceComparisonInput:
    selector: RuntimeReportBidirectionalTraceSelector | None = None
    trace_json_path: str | None = None
    label: str | None = None


@dataclass(frozen=True)
class RuntimeReportBidirectionalTraceComparisonEntry:
    comparison_label: str
    source_kind: str
    selection_mode: str
    profile_name: str
    digest_markdown_path: str
    digest_json_path: str
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
    trace_markdown_path: str | None
    trace_json_path: str | None
    has_browser_selection: bool
    catalog_count: int
    browser_count: int
    has_forward_link: bool


@dataclass(frozen=True)
class RuntimeReportBidirectionalTraceComparisonSummary:
    profile_name_union: tuple[str, ...]
    selection_mode_union: tuple[str, ...]
    forward_source_kind_union: tuple[str, ...]
    reverse_source_kind_union: tuple[str, ...]
    reverse_profile_resolution_mode_union: tuple[str, ...]
    shared_trigger_events: tuple[str, ...]
    trigger_event_union: tuple[str, ...]
    shared_artifact_kinds: tuple[str, ...]
    artifact_kind_union: tuple[str, ...]
    shared_source_families: tuple[str, ...]
    source_family_union: tuple[str, ...]
    shared_runtime_refs: tuple[str, ...]
    runtime_ref_union: tuple[str, ...]
    all_profile_name_match: bool
    all_digest_json_path_match: bool
    all_digest_markdown_path_match: bool
    asymmetry_labels: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportBidirectionalTraceComparison:
    generated_at: str
    read_only_mode: bool
    compared_count: int
    entries: tuple[RuntimeReportBidirectionalTraceComparisonEntry, ...]
    summary: RuntimeReportBidirectionalTraceComparisonSummary


@dataclass(frozen=True)
class RuntimeReportBidirectionalTraceComparisonWriteResult:
    markdown_path: str
    json_path: str
    comparison: RuntimeReportBidirectionalTraceComparison


class KernelRuntimeReportBidirectionalTraceComparer:
    """Compare two or more lawful bidirectional traces without promoting them into authority."""

    def __init__(
        self,
        *,
        tracer: KernelRuntimeReportBidirectionalTracer | None = None,
    ) -> None:
        self._tracer = tracer or KernelRuntimeReportBidirectionalTracer()

    def compare_traces(
        self,
        workspace_root: str | Path,
        inputs: Iterable[RuntimeReportBidirectionalTraceComparisonInput],
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
    ) -> RuntimeReportBidirectionalTraceComparison:
        realized = tuple(inputs)
        if len(realized) < 2:
            raise KernelRuntimeReportBidirectionalTraceComparisonError(
                'Bidirectional trace comparison requires at least two inputs.'
            )
        root = Path(workspace_root).resolve()
        entries: list[RuntimeReportBidirectionalTraceComparisonEntry] = []
        timestamp = created_at or _iso_now()
        for index, item in enumerate(realized, start=1):
            label = item.label or f'Bridge {index}'
            entry = self._resolve_entry(
                root,
                item,
                label=label,
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
                created_at=timestamp,
            )
            entries.append(entry)
        entry_tuple = tuple(entries)
        return RuntimeReportBidirectionalTraceComparison(
            generated_at=timestamp,
            read_only_mode=True,
            compared_count=len(entry_tuple),
            entries=entry_tuple,
            summary=_build_summary(entry_tuple),
        )

    def _resolve_entry(
        self,
        root: Path,
        item: RuntimeReportBidirectionalTraceComparisonInput,
        *,
        label: str,
        profiles_dir: str | Path,
        traces_dir: str | Path,
        catalogs_dir: str | Path,
        browser_dir: str | Path,
        packet_index_path: str | Path,
        operator_dashboard_path: str | Path,
        navigation_dir: str | Path,
        runtime_browser_dir: str | Path,
        crosslinks_dir: str | Path,
        digests_dir: str | Path,
        created_at: str | None,
    ) -> RuntimeReportBidirectionalTraceComparisonEntry:
        has_selector = item.selector is not None
        has_packet = bool(item.trace_json_path)
        if has_selector == has_packet:
            raise KernelRuntimeReportBidirectionalTraceComparisonError(
                'Provide exactly one of selector or trace_json_path for each comparison input.'
            )
        if item.trace_json_path:
            return self._load_entry_from_packet(root, item.trace_json_path, label=label)
        try:
            trace = self._tracer.trace_bidirectional(
                root,
                item.selector,  # type: ignore[arg-type]
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
            raise KernelRuntimeReportBidirectionalTraceComparisonError(str(exc)) from exc
        return _entry_from_trace(label, 'LIVE_SELECTION', trace, trace_json_path=None)

    def _load_entry_from_packet(
        self,
        root: Path,
        trace_json_path: str | Path,
        *,
        label: str,
    ) -> RuntimeReportBidirectionalTraceComparisonEntry:
        candidate = Path(trace_json_path)
        resolved = _resolve_relative_file(root, candidate)
        if not resolved.exists():
            raise KernelRuntimeReportBidirectionalTraceComparisonError(
                f'Bidirectional trace packet not found: {candidate}'
            )
        try:
            payload = json.loads(resolved.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            raise KernelRuntimeReportBidirectionalTraceComparisonError(
                f'Bidirectional trace JSON is invalid: {candidate}'
            ) from exc
        if payload.get('trace_kind') != 'RUNTIME_REPORT_BIDIRECTIONAL_TRACE':
            raise KernelRuntimeReportBidirectionalTraceComparisonError(
                f'JSON packet is not a bidirectional trace: {candidate}'
            )
        forward = payload.get('forward') or {}
        reverse = payload.get('reverse') or {}
        return RuntimeReportBidirectionalTraceComparisonEntry(
            comparison_label=label,
            source_kind='TRACE_PACKET',
            selection_mode=str(payload.get('selection_mode') or ''),
            profile_name=str(forward.get('profile_name') or reverse.get('profile_name') or ''),
            digest_markdown_path=str(forward.get('digest_markdown_path') or reverse.get('digest_markdown_path') or ''),
            digest_json_path=str(forward.get('digest_json_path') or reverse.get('digest_json_path') or ''),
            forward_source_kind=str(forward.get('source_kind') or ''),
            reverse_source_kind=str(reverse.get('source_kind') or ''),
            reverse_profile_resolution_mode=str(reverse.get('profile_resolution_mode') or ''),
            profile_name_match=bool(payload.get('profile_name_match')),
            digest_json_path_match=bool(payload.get('digest_json_path_match')),
            digest_markdown_path_match=bool(payload.get('digest_markdown_path_match')),
            asymmetries=tuple(payload.get('asymmetries') or ()),
            trigger_events=_sorted_unique((forward.get('digest_shared_trigger_events') or ()) + (reverse.get('digest_shared_trigger_events') or ())),
            artifact_kinds=_sorted_unique((forward.get('digest_shared_artifact_kinds') or ()) + (reverse.get('digest_shared_artifact_kinds') or ())),
            source_families=_sorted_unique((forward.get('digest_shared_source_families') or ()) + (reverse.get('digest_shared_source_families') or ())),
            runtime_refs=_sorted_unique((forward.get('digest_runtime_ref_union') or ()) + (reverse.get('digest_runtime_ref_union') or ())),
            trace_markdown_path=str(Path(candidate).with_suffix('.md')) if candidate.suffix == '.json' else None,
            trace_json_path=str(candidate),
            has_browser_selection=bool(forward.get('browser_json_path')),
            catalog_count=len(tuple(reverse.get('catalog_json_paths') or ())),
            browser_count=len(tuple(reverse.get('browser_json_paths') or ())),
            has_forward_link=bool(reverse.get('forward_link_json_path')),
        )

    def render_markdown(
        self,
        comparison: RuntimeReportBidirectionalTraceComparison,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'comparison_kind: RUNTIME_REPORT_BIDIRECTIONAL_TRACE_COMPARISON',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {comparison.generated_at}',
            f'compared_count: {comparison.compared_count}',
        ]
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Bidirectional Trace Comparison',
            '',
            'This packet is a bounded read-only comparison over multiple lawful profile↔digest bridge traces.',
            '',
            '## Compared Bridges',
            '',
        ])
        for entry in comparison.entries:
            lines.extend([
                f'### {entry.comparison_label}',
                '',
                f'- Source Kind: {entry.source_kind}',
                f'- Selection Mode: {entry.selection_mode}',
                f'- Profile Name: {entry.profile_name}',
                f'- Digest Markdown Path: {entry.digest_markdown_path}',
                f'- Digest JSON Path: {entry.digest_json_path}',
                f'- Forward Source Kind: {entry.forward_source_kind}',
                f'- Reverse Source Kind: {entry.reverse_source_kind}',
                f'- Reverse Profile Resolution Mode: {entry.reverse_profile_resolution_mode or "NONE"}',
                f'- Profile Name Match: {"YES" if entry.profile_name_match else "NO"}',
                f'- Digest JSON Path Match: {"YES" if entry.digest_json_path_match else "NO"}',
                f'- Digest Markdown Path Match: {"YES" if entry.digest_markdown_path_match else "NO"}',
                f'- Browser Selection Present: {"YES" if entry.has_browser_selection else "NO"}',
                f'- Catalog Count: {entry.catalog_count}',
                f'- Browser Count: {entry.browser_count}',
                f'- Forward Link Present: {"YES" if entry.has_forward_link else "NO"}',
                f'- Trace Markdown Path: {entry.trace_markdown_path or "NONE"}',
                f'- Trace JSON Path: {entry.trace_json_path or "NONE"}',
                f'- Trigger Events: {", ".join(entry.trigger_events) if entry.trigger_events else "NONE"}',
                f'- Artifact Kinds: {", ".join(entry.artifact_kinds) if entry.artifact_kinds else "NONE"}',
                f'- Source Families: {", ".join(entry.source_families) if entry.source_families else "NONE"}',
            ])
            if entry.runtime_refs:
                lines.append('- Runtime Refs:')
                lines.extend(f'  - {item}' for item in entry.runtime_refs)
            else:
                lines.append('- Runtime Refs: NONE')
            if entry.asymmetries:
                lines.append('- Asymmetries:')
                lines.extend(f'  - {item}' for item in entry.asymmetries)
            else:
                lines.append('- Asymmetries: NONE')
            lines.append('')
        summary = comparison.summary
        lines.extend([
            '## Shared Structure',
            '',
            f'- Profile Names: {_one_or_mixed(summary.profile_name_union)}',
            f'- Selection Modes: {_one_or_mixed(summary.selection_mode_union)}',
            f'- Forward Source Kinds: {_one_or_mixed(summary.forward_source_kind_union)}',
            f'- Reverse Source Kinds: {_one_or_mixed(summary.reverse_source_kind_union)}',
            f'- Reverse Profile Resolution Modes: {_one_or_mixed(summary.reverse_profile_resolution_mode_union)}',
            f'- Shared Trigger Events: {", ".join(summary.shared_trigger_events) if summary.shared_trigger_events else "NONE"}',
            f'- Trigger Event Union: {", ".join(summary.trigger_event_union) if summary.trigger_event_union else "NONE"}',
            f'- Shared Artifact Kinds: {", ".join(summary.shared_artifact_kinds) if summary.shared_artifact_kinds else "NONE"}',
            f'- Artifact Kind Union: {", ".join(summary.artifact_kind_union) if summary.artifact_kind_union else "NONE"}',
            f'- Shared Source Families: {", ".join(summary.shared_source_families) if summary.shared_source_families else "NONE"}',
            f'- Source Family Union: {", ".join(summary.source_family_union) if summary.source_family_union else "NONE"}',
            f'- Shared Runtime Refs: {", ".join(summary.shared_runtime_refs) if summary.shared_runtime_refs else "NONE"}',
            f'- Runtime Ref Union: {", ".join(summary.runtime_ref_union) if summary.runtime_ref_union else "NONE"}',
            f'- All Profile Name Match Markers True: {"YES" if summary.all_profile_name_match else "NO"}',
            f'- All Digest JSON Path Match Markers True: {"YES" if summary.all_digest_json_path_match else "NO"}',
            f'- All Digest Markdown Path Match Markers True: {"YES" if summary.all_digest_markdown_path_match else "NO"}',
        ])
        if summary.asymmetry_labels:
            lines.append('- Bridges With Asymmetries:')
            lines.extend(f'  - {item}' for item in summary.asymmetry_labels)
        else:
            lines.append('- Bridges With Asymmetries: NONE')
        lines.extend([
            '',
            '## Boundary',
            '',
            '- This packet is a read-only structural comparison over multiple lawful profile↔digest bridge traces.',
            '- It remains downstream from bidirectional traces, profile-to-digest traces, digest reverse traces, digest profiles, digests, catalogs, and browsers.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, bidirectional-trace authority, or comparison authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, comparison: RuntimeReportBidirectionalTraceComparison) -> str:
        payload = {
            'comparison_kind': 'RUNTIME_REPORT_BIDIRECTIONAL_TRACE_COMPARISON',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': comparison.generated_at,
            'compared_count': comparison.compared_count,
            'entries': [
                {
                    'comparison_label': entry.comparison_label,
                    'source_kind': entry.source_kind,
                    'selection_mode': entry.selection_mode,
                    'profile_name': entry.profile_name,
                    'digest_markdown_path': entry.digest_markdown_path,
                    'digest_json_path': entry.digest_json_path,
                    'forward_source_kind': entry.forward_source_kind,
                    'reverse_source_kind': entry.reverse_source_kind,
                    'reverse_profile_resolution_mode': entry.reverse_profile_resolution_mode,
                    'profile_name_match': entry.profile_name_match,
                    'digest_json_path_match': entry.digest_json_path_match,
                    'digest_markdown_path_match': entry.digest_markdown_path_match,
                    'asymmetries': list(entry.asymmetries),
                    'trigger_events': list(entry.trigger_events),
                    'artifact_kinds': list(entry.artifact_kinds),
                    'source_families': list(entry.source_families),
                    'runtime_refs': list(entry.runtime_refs),
                    'trace_markdown_path': entry.trace_markdown_path,
                    'trace_json_path': entry.trace_json_path,
                    'has_browser_selection': entry.has_browser_selection,
                    'catalog_count': entry.catalog_count,
                    'browser_count': entry.browser_count,
                    'has_forward_link': entry.has_forward_link,
                }
                for entry in comparison.entries
            ],
            'summary': {
                'profile_name_union': list(comparison.summary.profile_name_union),
                'selection_mode_union': list(comparison.summary.selection_mode_union),
                'forward_source_kind_union': list(comparison.summary.forward_source_kind_union),
                'reverse_source_kind_union': list(comparison.summary.reverse_source_kind_union),
                'reverse_profile_resolution_mode_union': list(comparison.summary.reverse_profile_resolution_mode_union),
                'shared_trigger_events': list(comparison.summary.shared_trigger_events),
                'trigger_event_union': list(comparison.summary.trigger_event_union),
                'shared_artifact_kinds': list(comparison.summary.shared_artifact_kinds),
                'artifact_kind_union': list(comparison.summary.artifact_kind_union),
                'shared_source_families': list(comparison.summary.shared_source_families),
                'source_family_union': list(comparison.summary.source_family_union),
                'shared_runtime_refs': list(comparison.summary.shared_runtime_refs),
                'runtime_ref_union': list(comparison.summary.runtime_ref_union),
                'all_profile_name_match': comparison.summary.all_profile_name_match,
                'all_digest_json_path_match': comparison.summary.all_digest_json_path_match,
                'all_digest_markdown_path_match': comparison.summary.all_digest_markdown_path_match,
                'asymmetry_labels': list(comparison.summary.asymmetry_labels),
            },
            'boundary': [
                'Read-only structural comparison over multiple lawful profile↔digest bridge traces.',
                'Remains downstream from bidirectional traces, profile-to-digest traces, digest reverse traces, digest profiles, digests, catalogs, and browsers.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, bidirectional-trace authority, or comparison authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_comparison_packet(
        self,
        workspace_root: str | Path,
        inputs: Iterable[RuntimeReportBidirectionalTraceComparisonInput],
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
        comparisons_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/comparisons',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportBidirectionalTraceComparisonWriteResult:
        root = Path(workspace_root).resolve()
        comparison = self.compare_traces(
            root,
            inputs,
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
        relative_dir = Path(comparisons_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stamp = re.sub(r'[^0-9]', '', comparison.generated_at)[:14]
        stem = output_stem or f'runtime_report_bidirectional_trace_comparison_{stamp}'
        markdown_relative = relative_dir / f'{stem}.md'
        json_relative = relative_dir / f'{stem}.json'
        _resolve_relative_file(root, markdown_relative).write_text(
            self.render_markdown(comparison, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        _resolve_relative_file(root, json_relative).write_text(
            self.render_json(comparison),
            encoding='utf-8',
        )
        return RuntimeReportBidirectionalTraceComparisonWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            comparison=comparison,
        )


IonRuntimeReportBidirectionalTraceComparer = KernelRuntimeReportBidirectionalTraceComparer


def _entry_from_trace(
    label: str,
    source_kind: str,
    trace: RuntimeReportBidirectionalTrace,
    *,
    trace_json_path: str | None,
) -> RuntimeReportBidirectionalTraceComparisonEntry:
    return RuntimeReportBidirectionalTraceComparisonEntry(
        comparison_label=label,
        source_kind=source_kind,
        selection_mode=trace.selection_mode,
        profile_name=trace.forward.profile_name,
        digest_markdown_path=trace.forward.digest_markdown_path,
        digest_json_path=trace.forward.digest_json_path,
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
        trace_markdown_path=trace_json_path[:-5] + '.md' if trace_json_path and trace_json_path.endswith('.json') else None,
        trace_json_path=trace_json_path,
        has_browser_selection=trace.forward.browser_json_path is not None,
        catalog_count=len(trace.reverse.catalog_json_paths),
        browser_count=len(trace.reverse.browser_json_paths),
        has_forward_link=trace.reverse.forward_link_json_path is not None,
    )


def _build_summary(
    entries: Sequence[RuntimeReportBidirectionalTraceComparisonEntry],
) -> RuntimeReportBidirectionalTraceComparisonSummary:
    return RuntimeReportBidirectionalTraceComparisonSummary(
        profile_name_union=_sorted_unique(entry.profile_name for entry in entries),
        selection_mode_union=_sorted_unique(entry.selection_mode for entry in entries),
        forward_source_kind_union=_sorted_unique(entry.forward_source_kind for entry in entries),
        reverse_source_kind_union=_sorted_unique(entry.reverse_source_kind for entry in entries),
        reverse_profile_resolution_mode_union=_sorted_unique(
            entry.reverse_profile_resolution_mode for entry in entries
        ),
        shared_trigger_events=_shared(values.trigger_events for values in entries),
        trigger_event_union=_sorted_unique(item for entry in entries for item in entry.trigger_events),
        shared_artifact_kinds=_shared(values.artifact_kinds for values in entries),
        artifact_kind_union=_sorted_unique(item for entry in entries for item in entry.artifact_kinds),
        shared_source_families=_shared(values.source_families for values in entries),
        source_family_union=_sorted_unique(item for entry in entries for item in entry.source_families),
        shared_runtime_refs=_shared(values.runtime_refs for values in entries),
        runtime_ref_union=_sorted_unique(item for entry in entries for item in entry.runtime_refs),
        all_profile_name_match=all(entry.profile_name_match for entry in entries),
        all_digest_json_path_match=all(entry.digest_json_path_match for entry in entries),
        all_digest_markdown_path_match=all(entry.digest_markdown_path_match for entry in entries),
        asymmetry_labels=tuple(entry.comparison_label for entry in entries if entry.asymmetries),
    )


def _sorted_unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({value for value in values if value}))


def _shared(groups: Iterable[Sequence[str]]) -> tuple[str, ...]:
    iterator = iter(groups)
    try:
        first = set(next(iterator))
    except StopIteration:
        return ()
    shared = set(first)
    for group in iterator:
        shared &= set(group)
    return tuple(sorted(shared))


def _one_or_mixed(values: Sequence[str]) -> str:
    if not values:
        return 'NONE'
    if len(values) == 1:
        return values[0]
    return f'MIXED ({", ".join(values)})'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportBidirectionalTraceComparisonError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportBidirectionalTraceComparisonError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
