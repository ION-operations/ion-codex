"""Read-only structural summaries over lawful profile↔digest bridge histories.

This module collapses one temporal profile↔digest bridge family into a bounded
structural synopsis for operators. It summarizes first/last generation span and
per-aspect stability / transience across the lawful I5 bridge-history surface.
It remains explicitly read-only and downstream witness material.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable

from .runtime_report_bidirectional_trace_temporal import (
    KernelRuntimeReportBidirectionalTemporalError,
    KernelRuntimeReportBidirectionalTemporalTracer,
    RuntimeReportBidirectionalTemporalAspect,
    RuntimeReportBidirectionalTemporalSelector,
    RuntimeReportBidirectionalTemporalTrace,
)


class KernelRuntimeReportBidirectionalFamilySummaryError(Exception):
    """Raised when one bridge-family summary cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportBidirectionalFamilyGenerationSpan:
    first_generation_label: str
    first_generation_index: int
    first_digest_generated_at: str
    first_digest_markdown_path: str
    first_digest_json_path: str
    last_generation_label: str
    last_generation_index: int
    last_digest_generated_at: str
    last_digest_markdown_path: str
    last_digest_json_path: str


@dataclass(frozen=True)
class RuntimeReportBidirectionalFamilyAspectSummary:
    aspect_name: str
    label: str
    presence_count: int
    ever_present: bool
    always_present: bool
    max_value_count: int
    stable_values: tuple[str, ...]
    transient_values: tuple[str, ...]
    emergent_values: tuple[str, ...]
    vanished_values: tuple[str, ...]
    first_present_generation_label: str | None
    last_present_generation_label: str | None


@dataclass(frozen=True)
class RuntimeReportBidirectionalFamilySummary:
    generated_at: str
    read_only_mode: bool
    selector_mode: str
    profile_name: str
    profile_markdown_path: str | None
    profile_json_path: str | None
    digests_dir: str
    generation_count: int
    generation_span: RuntimeReportBidirectionalFamilyGenerationSpan
    forward_source_kind_union: tuple[str, ...]
    reverse_source_kind_union: tuple[str, ...]
    reverse_profile_resolution_mode_union: tuple[str, ...]
    trigger_event_union: tuple[str, ...]
    artifact_kind_union: tuple[str, ...]
    source_family_union: tuple[str, ...]
    runtime_ref_union: tuple[str, ...]
    asymmetry_union: tuple[str, ...]
    aspects: tuple[RuntimeReportBidirectionalFamilyAspectSummary, ...]


@dataclass(frozen=True)
class RuntimeReportBidirectionalFamilySummaryWriteResult:
    markdown_path: str
    json_path: str
    summary: RuntimeReportBidirectionalFamilySummary


class KernelRuntimeReportBidirectionalFamilySummarizer:
    """Collapse one temporal bridge family into a bounded read-only synopsis."""

    def __init__(
        self,
        *,
        temporal_tracer: KernelRuntimeReportBidirectionalTemporalTracer | None = None,
    ) -> None:
        self._temporal_tracer = temporal_tracer or KernelRuntimeReportBidirectionalTemporalTracer()

    def summarize_family(
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
    ) -> RuntimeReportBidirectionalFamilySummary:
        root = Path(workspace_root).resolve()
        try:
            trace = self._temporal_tracer.trace_bridge_family(
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
        except KernelRuntimeReportBidirectionalTemporalError as exc:
            raise KernelRuntimeReportBidirectionalFamilySummaryError(str(exc)) from exc
        return _build_summary(trace)

    def render_markdown(
        self,
        summary: RuntimeReportBidirectionalFamilySummary,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'summary_kind: RUNTIME_REPORT_BIDIRECTIONAL_FAMILY_SUMMARY',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {summary.generated_at}',
            f'selector_mode: {summary.selector_mode}',
            f'profile_name: {summary.profile_name}',
            f'digests_dir: {summary.digests_dir}',
            f'generation_count: {summary.generation_count}',
        ]
        if summary.profile_markdown_path is not None:
            lines.append(f'profile_markdown_path: {summary.profile_markdown_path}')
        if summary.profile_json_path is not None:
            lines.append(f'profile_json_path: {summary.profile_json_path}')
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Bidirectional Family Summary',
            '',
            'This packet is a read-only structural synopsis over one lawful profile↔digest bridge family.',
            '',
            '## Family Span',
            '',
            f'- Selector Mode: {summary.selector_mode}',
            f'- Profile Name: {summary.profile_name}',
            f'- Profile Markdown Path: {summary.profile_markdown_path or "NONE"}',
            f'- Profile JSON Path: {summary.profile_json_path or "NONE"}',
            f'- Digests Directory: {summary.digests_dir}',
            f'- Generation Count: {summary.generation_count}',
            f'- First Generation: {summary.generation_span.first_generation_label} ({summary.generation_span.first_digest_generated_at})',
            f'- First Digest Markdown Path: {summary.generation_span.first_digest_markdown_path}',
            f'- First Digest JSON Path: {summary.generation_span.first_digest_json_path}',
            f'- Last Generation: {summary.generation_span.last_generation_label} ({summary.generation_span.last_digest_generated_at})',
            f'- Last Digest Markdown Path: {summary.generation_span.last_digest_markdown_path}',
            f'- Last Digest JSON Path: {summary.generation_span.last_digest_json_path}',
            f'- Forward Source Kind Union: {", ".join(summary.forward_source_kind_union) if summary.forward_source_kind_union else "NONE"}',
            f'- Reverse Source Kind Union: {", ".join(summary.reverse_source_kind_union) if summary.reverse_source_kind_union else "NONE"}',
            f'- Reverse Profile Resolution Mode Union: {", ".join(summary.reverse_profile_resolution_mode_union) if summary.reverse_profile_resolution_mode_union else "NONE"}',
            f'- Trigger Event Union: {", ".join(summary.trigger_event_union) if summary.trigger_event_union else "NONE"}',
            f'- Artifact Kind Union: {", ".join(summary.artifact_kind_union) if summary.artifact_kind_union else "NONE"}',
            f'- Source Family Union: {", ".join(summary.source_family_union) if summary.source_family_union else "NONE"}',
        ])
        if summary.runtime_ref_union:
            lines.append('- Runtime Ref Union:')
            lines.extend(f'  - {item}' for item in summary.runtime_ref_union)
        else:
            lines.append('- Runtime Ref Union: NONE')
        if summary.asymmetry_union:
            lines.append('- Asymmetry Union:')
            lines.extend(f'  - {item}' for item in summary.asymmetry_union)
        else:
            lines.append('- Asymmetry Union: NONE')
        lines.extend([
            '',
            '## Aspect Synopses',
            '',
        ])
        for aspect in summary.aspects:
            lines.extend([
                f'### {aspect.label}',
                '',
                f'- Presence Count: {aspect.presence_count}/{summary.generation_count}',
                f'- Ever Present: {"YES" if aspect.ever_present else "NO"}',
                f'- Always Present: {"YES" if aspect.always_present else "NO"}',
                f'- Max Value Count: {aspect.max_value_count}',
                f'- First Present Generation: {aspect.first_present_generation_label or "NONE"}',
                f'- Last Present Generation: {aspect.last_present_generation_label or "NONE"}',
                f'- Stable Values: {", ".join(aspect.stable_values) if aspect.stable_values else "NONE"}',
                f'- Transient Values: {", ".join(aspect.transient_values) if aspect.transient_values else "NONE"}',
                f'- Emergent Values: {", ".join(aspect.emergent_values) if aspect.emergent_values else "NONE"}',
                f'- Vanished Values: {", ".join(aspect.vanished_values) if aspect.vanished_values else "NONE"}',
                '',
            ])
        lines.extend([
            '## Boundary',
            '',
            '- This packet is a read-only structural synopsis over one lawful profile↔digest bridge family.',
            '- It compresses the I5 bridge-history surface into first/last generation span and per-aspect structural summaries.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, bidirectional-trace authority, temporal authority, summary authority, or bridge-history authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, summary: RuntimeReportBidirectionalFamilySummary) -> str:
        payload = {
            'summary_kind': 'RUNTIME_REPORT_BIDIRECTIONAL_FAMILY_SUMMARY',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': summary.generated_at,
            'selector_mode': summary.selector_mode,
            'profile_name': summary.profile_name,
            'profile_markdown_path': summary.profile_markdown_path,
            'profile_json_path': summary.profile_json_path,
            'digests_dir': summary.digests_dir,
            'generation_count': summary.generation_count,
            'generation_span': {
                'first_generation_label': summary.generation_span.first_generation_label,
                'first_generation_index': summary.generation_span.first_generation_index,
                'first_digest_generated_at': summary.generation_span.first_digest_generated_at,
                'first_digest_markdown_path': summary.generation_span.first_digest_markdown_path,
                'first_digest_json_path': summary.generation_span.first_digest_json_path,
                'last_generation_label': summary.generation_span.last_generation_label,
                'last_generation_index': summary.generation_span.last_generation_index,
                'last_digest_generated_at': summary.generation_span.last_digest_generated_at,
                'last_digest_markdown_path': summary.generation_span.last_digest_markdown_path,
                'last_digest_json_path': summary.generation_span.last_digest_json_path,
            },
            'forward_source_kind_union': list(summary.forward_source_kind_union),
            'reverse_source_kind_union': list(summary.reverse_source_kind_union),
            'reverse_profile_resolution_mode_union': list(summary.reverse_profile_resolution_mode_union),
            'trigger_event_union': list(summary.trigger_event_union),
            'artifact_kind_union': list(summary.artifact_kind_union),
            'source_family_union': list(summary.source_family_union),
            'runtime_ref_union': list(summary.runtime_ref_union),
            'asymmetry_union': list(summary.asymmetry_union),
            'aspects': [
                {
                    'aspect_name': aspect.aspect_name,
                    'label': aspect.label,
                    'presence_count': aspect.presence_count,
                    'ever_present': aspect.ever_present,
                    'always_present': aspect.always_present,
                    'max_value_count': aspect.max_value_count,
                    'stable_values': list(aspect.stable_values),
                    'transient_values': list(aspect.transient_values),
                    'emergent_values': list(aspect.emergent_values),
                    'vanished_values': list(aspect.vanished_values),
                    'first_present_generation_label': aspect.first_present_generation_label,
                    'last_present_generation_label': aspect.last_present_generation_label,
                }
                for aspect in summary.aspects
            ],
            'boundary': [
                'Read-only structural synopsis over one lawful profile↔digest bridge family.',
                'Compresses the I5 bridge-history surface into first/last generation span and per-aspect structural summaries.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, bidirectional-trace authority, temporal authority, summary authority, or bridge-history authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_summary_packet(
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
        families_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/families',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportBidirectionalFamilySummaryWriteResult:
        root = Path(workspace_root).resolve()
        summary = self.summarize_family(
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
        relative_dir = Path(families_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stamp = re.sub(r'[^0-9]', '', summary.generated_at)[:14]
        stem = output_stem or f'{_safe(summary.profile_name)}__bidirectional_family_summary_{stamp}'
        markdown_relative = relative_dir / f'{stem}.md'
        json_relative = relative_dir / f'{stem}.json'
        _resolve_relative_file(root, markdown_relative).write_text(
            self.render_markdown(summary, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        _resolve_relative_file(root, json_relative).write_text(
            self.render_json(summary),
            encoding='utf-8',
        )
        return RuntimeReportBidirectionalFamilySummaryWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            summary=summary,
        )


IonRuntimeReportBidirectionalFamilySummarizer = KernelRuntimeReportBidirectionalFamilySummarizer


def _build_summary(trace: RuntimeReportBidirectionalTemporalTrace) -> RuntimeReportBidirectionalFamilySummary:
    first = trace.generations[0]
    last = trace.generations[-1]
    aspect_summaries = tuple(_summarize_aspect(aspect) for aspect in trace.aspects)
    return RuntimeReportBidirectionalFamilySummary(
        generated_at=trace.generated_at,
        read_only_mode=True,
        selector_mode=trace.selector_mode,
        profile_name=trace.profile_name,
        profile_markdown_path=trace.profile_markdown_path,
        profile_json_path=trace.profile_json_path,
        digests_dir=trace.digests_dir,
        generation_count=trace.generation_count,
        generation_span=RuntimeReportBidirectionalFamilyGenerationSpan(
            first_generation_label=first.generation_label,
            first_generation_index=first.generation_index,
            first_digest_generated_at=first.digest_generated_at,
            first_digest_markdown_path=first.digest_markdown_path,
            first_digest_json_path=first.digest_json_path,
            last_generation_label=last.generation_label,
            last_generation_index=last.generation_index,
            last_digest_generated_at=last.digest_generated_at,
            last_digest_markdown_path=last.digest_markdown_path,
            last_digest_json_path=last.digest_json_path,
        ),
        forward_source_kind_union=_sorted_unique(item.forward_source_kind for item in trace.generations),
        reverse_source_kind_union=_sorted_unique(item.reverse_source_kind for item in trace.generations),
        reverse_profile_resolution_mode_union=_sorted_unique(item.reverse_profile_resolution_mode for item in trace.generations),
        trigger_event_union=_sorted_unique(value for item in trace.generations for value in item.trigger_events),
        artifact_kind_union=_sorted_unique(value for item in trace.generations for value in item.artifact_kinds),
        source_family_union=_sorted_unique(value for item in trace.generations for value in item.source_families),
        runtime_ref_union=_sorted_unique(value for item in trace.generations for value in item.runtime_refs),
        asymmetry_union=_sorted_unique(value for item in trace.generations for value in item.asymmetries),
        aspects=aspect_summaries,
    )


def _summarize_aspect(aspect: RuntimeReportBidirectionalTemporalAspect) -> RuntimeReportBidirectionalFamilyAspectSummary:
    value_sets = [set(item.values) for item in aspect.generations]
    present_indexes = [index for index, item in enumerate(aspect.generations) if item.values]
    first_present = aspect.generations[present_indexes[0]].generation_label if present_indexes else None
    last_present = aspect.generations[present_indexes[-1]].generation_label if present_indexes else None
    union_values = set().union(*value_sets) if value_sets else set()
    transient = tuple(sorted(union_values - set(aspect.stable_values)))
    return RuntimeReportBidirectionalFamilyAspectSummary(
        aspect_name=aspect.aspect_name,
        label=aspect.label,
        presence_count=len(present_indexes),
        ever_present=bool(present_indexes),
        always_present=len(present_indexes) == len(aspect.generations),
        max_value_count=max((len(item.values) for item in aspect.generations), default=0),
        stable_values=tuple(aspect.stable_values),
        transient_values=transient,
        emergent_values=tuple(aspect.emergent_values),
        vanished_values=tuple(aspect.vanished_values),
        first_present_generation_label=first_present,
        last_present_generation_label=last_present,
    )


def _sorted_unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({value for value in values if value}))


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportBidirectionalFamilySummaryError(
            f'Absolute paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportBidirectionalFamilySummaryError(
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
