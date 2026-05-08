"""Read-only structural family summaries over downstream runtime-report witness material.

This module collapses one temporal provenance family into a bounded structural synopsis
for operators. It summarizes first/last generation span, shared family identity, and
per-layer stability / transience across artifact, governance reflection, aggregation,
visibility projection, navigation packets, browser bundles, and crosslink packets.
It remains explicitly read-only and does not promote any downstream surface into
kernel truth, doctrine, route authority, runtime authority, or summary authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable

from .runtime_report_temporal_provenance import (
    KernelRuntimeReportTemporalProvenanceError,
    KernelRuntimeReportTemporalProvenanceTracer,
    RuntimeReportTemporalSelector,
    RuntimeReportTemporalTrace,
)


class KernelRuntimeReportFamilySummaryError(Exception):
    """Raised when one family-summary request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportFamilyGenerationSpan:
    first_generation_label: str
    first_generation_index: int
    first_created_at: str | None
    first_source_ref: str
    last_generation_label: str
    last_generation_index: int
    last_created_at: str | None
    last_source_ref: str


@dataclass(frozen=True)
class RuntimeReportFamilyLayerSummary:
    layer_name: str
    label: str
    presence_count: int
    ever_present: bool
    always_present: bool
    max_target_count: int
    stable_target_kinds: tuple[str, ...]
    transient_target_kinds: tuple[str, ...]
    emergent_target_kinds: tuple[str, ...]
    vanished_target_kinds: tuple[str, ...]
    first_present_generation_label: str | None
    last_present_generation_label: str | None


@dataclass(frozen=True)
class RuntimeReportFamilySummary:
    generated_at: str
    read_only_mode: bool
    packet_index_path: str
    selector: RuntimeReportTemporalSelector
    generation_count: int
    generation_span: RuntimeReportFamilyGenerationSpan
    shared_trigger_event: str
    shared_artifact_kind: str
    shared_source_family: str
    runtime_ref_union: tuple[str, ...]
    layers: tuple[RuntimeReportFamilyLayerSummary, ...]


@dataclass(frozen=True)
class RuntimeReportFamilySummaryWriteResult:
    markdown_path: str
    json_path: str
    summary: RuntimeReportFamilySummary


class KernelRuntimeReportFamilySummarizer:
    """Collapse one temporal provenance family into a bounded read-only synopsis."""

    def __init__(
        self,
        *,
        temporal_tracer: KernelRuntimeReportTemporalProvenanceTracer | None = None,
    ) -> None:
        self._temporal_tracer = temporal_tracer or KernelRuntimeReportTemporalProvenanceTracer()

    def summarize_family(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportTemporalSelector,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        created_at: str | None = None,
    ) -> RuntimeReportFamilySummary:
        root = Path(workspace_root).resolve()
        try:
            trace = self._temporal_tracer.trace_family_generations(
                root,
                selector,
                packet_index_path=packet_index_path,
                operator_dashboard_path=operator_dashboard_path,
                navigation_dir=navigation_dir,
                browser_dir=browser_dir,
                crosslinks_dir=crosslinks_dir,
                created_at=created_at,
            )
        except KernelRuntimeReportTemporalProvenanceError as exc:
            raise KernelRuntimeReportFamilySummaryError(str(exc)) from exc
        return self._build_summary(trace)

    def render_markdown(
        self,
        summary: RuntimeReportFamilySummary,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'summary_kind: RUNTIME_REPORT_FAMILY_SUMMARY',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {summary.generated_at}',
            f'packet_index_path: {summary.packet_index_path}',
            f'generation_count: {summary.generation_count}',
            f'trigger_event: {summary.shared_trigger_event}',
            f'artifact_kind: {summary.shared_artifact_kind}',
            f'source_family: {summary.shared_source_family}',
        ]
        if summary.selector.source_ref is not None:
            lines.append(f'source_ref: {summary.selector.source_ref}')
        if summary.selector.source_ref_contains is not None:
            lines.append(f'source_ref_contains: {summary.selector.source_ref_contains}')
        if summary.selector.limit is not None:
            lines.append(f'selector_limit: {summary.selector.limit}')
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Family Summary',
            '',
            'This packet is a read-only structural synopsis over one runtime-report receipt family.',
            '',
            '## Family Span',
            '',
            f'- Generation Count: {summary.generation_count}',
            f'- Trigger Event: {summary.shared_trigger_event}',
            f'- Artifact Kind: {summary.shared_artifact_kind}',
            f'- Source Family: {summary.shared_source_family}',
            f'- Selector Family: {_selector_family_value(summary.selector.source_ref, summary.selector.source_ref_contains)}',
            f'- First Generation: {summary.generation_span.first_generation_label} ({summary.generation_span.first_created_at or "NONE"})',
            f'- First Source Ref: {summary.generation_span.first_source_ref}',
            f'- Last Generation: {summary.generation_span.last_generation_label} ({summary.generation_span.last_created_at or "NONE"})',
            f'- Last Source Ref: {summary.generation_span.last_source_ref}',
        ])
        if summary.runtime_ref_union:
            lines.append('- Runtime Ref Union:')
            lines.extend(f'  - {item}' for item in summary.runtime_ref_union)
        else:
            lines.append('- Runtime Ref Union: NONE')
        lines.extend([
            '',
            '## Layer Synopses',
            '',
        ])
        for layer in summary.layers:
            lines.extend([
                f'### {layer.label}',
                '',
                f'- Presence Count: {layer.presence_count}/{summary.generation_count}',
                f'- Ever Present: {"YES" if layer.ever_present else "NO"}',
                f'- Always Present: {"YES" if layer.always_present else "NO"}',
                f'- Max Target Count: {layer.max_target_count}',
                f'- First Present Generation: {layer.first_present_generation_label or "NONE"}',
                f'- Last Present Generation: {layer.last_present_generation_label or "NONE"}',
                f'- Stable Target Kinds: {", ".join(layer.stable_target_kinds) if layer.stable_target_kinds else "NONE"}',
                f'- Transient Target Kinds: {", ".join(layer.transient_target_kinds) if layer.transient_target_kinds else "NONE"}',
                f'- Emergent Target Kinds: {", ".join(layer.emergent_target_kinds) if layer.emergent_target_kinds else "NONE"}',
                f'- Vanished Target Kinds: {", ".join(layer.vanished_target_kinds) if layer.vanished_target_kinds else "NONE"}',
                '',
            ])
        lines.extend([
            '## Boundary',
            '',
            '- This packet is a read-only structural synopsis over downstream runtime-report witness material.',
            '- It compresses one temporal receipt family into first/last generation span and per-layer structural summaries.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, or summary authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, summary: RuntimeReportFamilySummary) -> str:
        payload = {
            'summary_kind': 'RUNTIME_REPORT_FAMILY_SUMMARY',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': summary.generated_at,
            'packet_index_path': summary.packet_index_path,
            'generation_count': summary.generation_count,
            'selector': {
                'source_ref': summary.selector.source_ref,
                'source_ref_contains': summary.selector.source_ref_contains,
                'trigger_event': summary.selector.trigger_event,
                'artifact_kind': summary.selector.artifact_kind,
                'source_family': summary.selector.source_family,
                'limit': summary.selector.limit,
            },
            'generation_span': {
                'first_generation_label': summary.generation_span.first_generation_label,
                'first_generation_index': summary.generation_span.first_generation_index,
                'first_created_at': summary.generation_span.first_created_at,
                'first_source_ref': summary.generation_span.first_source_ref,
                'last_generation_label': summary.generation_span.last_generation_label,
                'last_generation_index': summary.generation_span.last_generation_index,
                'last_created_at': summary.generation_span.last_created_at,
                'last_source_ref': summary.generation_span.last_source_ref,
            },
            'shared_trigger_event': summary.shared_trigger_event,
            'shared_artifact_kind': summary.shared_artifact_kind,
            'shared_source_family': summary.shared_source_family,
            'runtime_ref_union': list(summary.runtime_ref_union),
            'layers': [
                {
                    'layer_name': layer.layer_name,
                    'label': layer.label,
                    'presence_count': layer.presence_count,
                    'ever_present': layer.ever_present,
                    'always_present': layer.always_present,
                    'max_target_count': layer.max_target_count,
                    'stable_target_kinds': list(layer.stable_target_kinds),
                    'transient_target_kinds': list(layer.transient_target_kinds),
                    'emergent_target_kinds': list(layer.emergent_target_kinds),
                    'vanished_target_kinds': list(layer.vanished_target_kinds),
                    'first_present_generation_label': layer.first_present_generation_label,
                    'last_present_generation_label': layer.last_present_generation_label,
                }
                for layer in summary.layers
            ],
            'boundary': [
                'Read-only structural synopsis over downstream runtime-report witness material.',
                'Compresses one temporal receipt family into first/last generation span and per-layer structural summaries.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, or summary authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_family_summary_packet(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportTemporalSelector,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        families_dir: str | Path = 'ION/05_context/runtime_reports/governance/provenance/families',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportFamilySummaryWriteResult:
        root = Path(workspace_root).resolve()
        summary = self.summarize_family(
            root,
            selector,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            browser_dir=browser_dir,
            crosslinks_dir=crosslinks_dir,
            created_at=created_at,
        )
        relative_dir = Path(families_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stem = output_stem or _default_stem(summary, created_at or summary.generated_at)
        markdown_relative = relative_dir / f'{stem}.md'
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        markdown_resolved.write_text(
            self.render_markdown(summary, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        json_relative = relative_dir / f'{stem}.json'
        json_resolved = _resolve_relative_file(root, json_relative)
        json_resolved.write_text(self.render_json(summary), encoding='utf-8')
        return RuntimeReportFamilySummaryWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            summary=summary,
        )

    def _build_summary(self, trace: RuntimeReportTemporalTrace) -> RuntimeReportFamilySummary:
        first = trace.generations[0]
        last = trace.generations[-1]
        runtime_ref_union = tuple(sorted({ref for generation in trace.generations for ref in generation.runtime_refs}))
        layers = tuple(self._summarize_layer(layer, trace.generation_count) for layer in trace.layers)
        return RuntimeReportFamilySummary(
            generated_at=trace.generated_at,
            read_only_mode=True,
            packet_index_path=trace.packet_index_path,
            selector=trace.selector,
            generation_count=trace.generation_count,
            generation_span=RuntimeReportFamilyGenerationSpan(
                first_generation_label=first.generation_label,
                first_generation_index=first.generation_index,
                first_created_at=first.created_at,
                first_source_ref=first.source_ref,
                last_generation_label=last.generation_label,
                last_generation_index=last.generation_index,
                last_created_at=last.created_at,
                last_source_ref=last.source_ref,
            ),
            shared_trigger_event=trace.selector.trigger_event or _single_value_or_mixed(item.trigger_event for item in trace.generations),
            shared_artifact_kind=trace.selector.artifact_kind or _single_value_or_mixed(item.artifact_kind for item in trace.generations),
            shared_source_family=trace.selector.source_family or _single_value_or_mixed(item.source_family for item in trace.generations),
            runtime_ref_union=runtime_ref_union,
            layers=layers,
        )

    def _summarize_layer(self, layer, generation_count: int) -> RuntimeReportFamilyLayerSummary:
        present_generations = [item for item in layer.generations if item.target_count > 0]
        all_target_kinds = tuple(sorted({kind for item in layer.generations for kind in item.target_kinds}))
        transient_target_kinds = tuple(sorted(set(all_target_kinds) - set(layer.stable_target_kinds)))
        first_present = present_generations[0].generation_label if present_generations else None
        last_present = present_generations[-1].generation_label if present_generations else None
        return RuntimeReportFamilyLayerSummary(
            layer_name=layer.layer_name,
            label=layer.label,
            presence_count=len(present_generations),
            ever_present=bool(present_generations),
            always_present=(len(present_generations) == generation_count and generation_count > 0),
            max_target_count=max((item.target_count for item in layer.generations), default=0),
            stable_target_kinds=layer.stable_target_kinds,
            transient_target_kinds=transient_target_kinds,
            emergent_target_kinds=layer.emergent_target_kinds,
            vanished_target_kinds=layer.vanished_target_kinds,
            first_present_generation_label=first_present,
            last_present_generation_label=last_present,
        )


IonRuntimeReportFamilySummarizer = KernelRuntimeReportFamilySummarizer


def _single_value_or_none(values: Iterable[str | None]) -> str | None:
    items = {value for value in values}
    if len(items) == 1:
        return next(iter(items))
    return None


def _single_value_or_mixed(values: Iterable[str | None]) -> str:
    value = _single_value_or_none(values)
    return value if value is not None else 'MIXED'


def _selector_family_value(source_ref: str | None, source_ref_contains: str | None) -> str:
    if source_ref is not None:
        return source_ref
    if source_ref_contains is not None:
        return f'contains:{source_ref_contains}'
    return 'MIXED'


def _default_stem(summary: RuntimeReportFamilySummary, created_at: str) -> str:
    stamp = re.sub(r'[^0-9]', '', created_at)[:14]
    family = _safe(
        summary.selector.source_ref
        or summary.selector.source_ref_contains
        or summary.shared_artifact_kind
        or summary.shared_trigger_event
        or summary.shared_source_family
        or 'family'
    )
    return f'{family}__runtime_family_summary_{stamp}'


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportFamilySummaryError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportFamilySummaryError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
