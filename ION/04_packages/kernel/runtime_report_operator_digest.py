"""Read-only operator digests over downstream runtime-report family summaries.

This module composes multiple G4 family summaries into one bounded operator-facing
higher-order digest. It stays explicitly read-only and downstream from artifacts,
reflections, aggregation witnesses, visibility projections, navigation packets,
browser bundles, crosslink packets, provenance traces, temporal traces, and family
summaries. It does not promote any downstream surface into kernel truth, doctrine,
route authority, runtime authority, or digest authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable, Sequence

from .runtime_report_family_summary import (
    KernelRuntimeReportFamilySummarizer,
    KernelRuntimeReportFamilySummaryError,
    RuntimeReportFamilySummary,
)
from .runtime_report_temporal_provenance import RuntimeReportTemporalSelector


class KernelRuntimeReportOperatorDigestError(Exception):
    """Raised when one operator-digest request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportOperatorDigestFamilyEntry:
    family_label: str
    selector: RuntimeReportTemporalSelector
    generation_count: int
    shared_trigger_event: str
    shared_artifact_kind: str
    shared_source_family: str
    first_generation_label: str
    first_source_ref: str
    last_generation_label: str
    last_source_ref: str
    runtime_ref_union: tuple[str, ...]
    ever_present_layers: tuple[str, ...]
    always_present_layers: tuple[str, ...]
    transient_layers: tuple[str, ...]
    emergent_layers: tuple[str, ...]
    vanished_layers: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportOperatorDigestLayerOverview:
    layer_name: str
    label: str
    family_presence_count: int
    always_present_family_count: int
    stable_target_kind_union: tuple[str, ...]
    transient_target_kind_union: tuple[str, ...]
    emergent_target_kind_union: tuple[str, ...]
    vanished_target_kind_union: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportOperatorDigest:
    generated_at: str
    read_only_mode: bool
    family_count: int
    total_generations: int
    packet_index_path: str
    shared_trigger_events: tuple[str, ...]
    shared_artifact_kinds: tuple[str, ...]
    shared_source_families: tuple[str, ...]
    runtime_ref_union: tuple[str, ...]
    families: tuple[RuntimeReportOperatorDigestFamilyEntry, ...]
    layers: tuple[RuntimeReportOperatorDigestLayerOverview, ...]


@dataclass(frozen=True)
class RuntimeReportOperatorDigestWriteResult:
    markdown_path: str
    json_path: str
    digest: RuntimeReportOperatorDigest


class KernelRuntimeReportOperatorDigester:
    """Compose multiple family summaries into one bounded read-only operator digest."""

    def __init__(
        self,
        *,
        summarizer: KernelRuntimeReportFamilySummarizer | None = None,
    ) -> None:
        self._summarizer = summarizer or KernelRuntimeReportFamilySummarizer()

    def build_digest(
        self,
        workspace_root: str | Path,
        selectors: Sequence[RuntimeReportTemporalSelector],
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        created_at: str | None = None,
    ) -> RuntimeReportOperatorDigest:
        root = Path(workspace_root).resolve()
        normalized_selectors = tuple(selectors)
        if not normalized_selectors:
            raise KernelRuntimeReportOperatorDigestError(
                'Operator digest requires at least one temporal family selector.'
            )
        summaries: list[RuntimeReportFamilySummary] = []
        for selector in normalized_selectors:
            try:
                summary = self._summarizer.summarize_family(
                    root,
                    selector,
                    packet_index_path=packet_index_path,
                    operator_dashboard_path=operator_dashboard_path,
                    navigation_dir=navigation_dir,
                    browser_dir=browser_dir,
                    crosslinks_dir=crosslinks_dir,
                    created_at=created_at,
                )
            except KernelRuntimeReportFamilySummaryError as exc:
                raise KernelRuntimeReportOperatorDigestError(str(exc)) from exc
            summaries.append(summary)

        generated_at = created_at or _iso_now()
        families = tuple(_family_entry(summary) for summary in summaries)
        layer_order = tuple(summary.layers[i].layer_name for i in range(len(summaries[0].layers)))
        layers = tuple(_rollup_layer(layer_name, summaries) for layer_name in layer_order)
        return RuntimeReportOperatorDigest(
            generated_at=generated_at,
            read_only_mode=True,
            family_count=len(summaries),
            total_generations=sum(summary.generation_count for summary in summaries),
            packet_index_path=str(packet_index_path),
            shared_trigger_events=_sorted_unique(summary.shared_trigger_event for summary in summaries),
            shared_artifact_kinds=_sorted_unique(summary.shared_artifact_kind for summary in summaries),
            shared_source_families=_sorted_unique(summary.shared_source_family for summary in summaries),
            runtime_ref_union=_sorted_unique(ref for summary in summaries for ref in summary.runtime_ref_union),
            families=families,
            layers=layers,
        )

    def render_markdown(
        self,
        digest: RuntimeReportOperatorDigest,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'digest_kind: RUNTIME_REPORT_OPERATOR_DIGEST',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {digest.generated_at}',
            f'packet_index_path: {digest.packet_index_path}',
            f'family_count: {digest.family_count}',
            f'total_generations: {digest.total_generations}',
        ]
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Operator Digest',
            '',
            'This packet is a bounded read-only digest over selected runtime-report family summaries.',
            '',
            '## Digest Scope',
            '',
            f'- Family Count: {digest.family_count}',
            f'- Total Generations: {digest.total_generations}',
            f'- Trigger Events: {", ".join(digest.shared_trigger_events) if digest.shared_trigger_events else "NONE"}',
            f'- Artifact Kinds: {", ".join(digest.shared_artifact_kinds) if digest.shared_artifact_kinds else "NONE"}',
            f'- Source Families: {", ".join(digest.shared_source_families) if digest.shared_source_families else "NONE"}',
        ])
        if digest.runtime_ref_union:
            lines.append('- Runtime Ref Union:')
            lines.extend(f'  - {item}' for item in digest.runtime_ref_union)
        else:
            lines.append('- Runtime Ref Union: NONE')
        lines.extend([
            '',
            '## Family Rollup',
            '',
        ])
        for family in digest.families:
            lines.extend([
                f'### {family.family_label}',
                '',
                f'- Generation Count: {family.generation_count}',
                f'- Trigger Event: {family.shared_trigger_event}',
                f'- Artifact Kind: {family.shared_artifact_kind}',
                f'- Source Family: {family.shared_source_family}',
                f'- First Generation: {family.first_generation_label}',
                f'- First Source Ref: {family.first_source_ref}',
                f'- Last Generation: {family.last_generation_label}',
                f'- Last Source Ref: {family.last_source_ref}',
                f'- Ever Present Layers: {", ".join(family.ever_present_layers) if family.ever_present_layers else "NONE"}',
                f'- Always Present Layers: {", ".join(family.always_present_layers) if family.always_present_layers else "NONE"}',
                f'- Transient Layers: {", ".join(family.transient_layers) if family.transient_layers else "NONE"}',
                f'- Emergent Layers: {", ".join(family.emergent_layers) if family.emergent_layers else "NONE"}',
                f'- Vanished Layers: {", ".join(family.vanished_layers) if family.vanished_layers else "NONE"}',
            ])
            if family.runtime_ref_union:
                lines.append('- Runtime Refs:')
                lines.extend(f'  - {item}' for item in family.runtime_ref_union)
            else:
                lines.append('- Runtime Refs: NONE')
            lines.append('')

        lines.extend([
            '## Layer Rollup',
            '',
        ])
        for layer in digest.layers:
            lines.extend([
                f'### {layer.label}',
                '',
                f'- Family Presence Count: {layer.family_presence_count}/{digest.family_count}',
                f'- Always Present Family Count: {layer.always_present_family_count}/{digest.family_count}',
                f'- Stable Target Kind Union: {", ".join(layer.stable_target_kind_union) if layer.stable_target_kind_union else "NONE"}',
                f'- Transient Target Kind Union: {", ".join(layer.transient_target_kind_union) if layer.transient_target_kind_union else "NONE"}',
                f'- Emergent Target Kind Union: {", ".join(layer.emergent_target_kind_union) if layer.emergent_target_kind_union else "NONE"}',
                f'- Vanished Target Kind Union: {", ".join(layer.vanished_target_kind_union) if layer.vanished_target_kind_union else "NONE"}',
                '',
            ])

        lines.extend([
            '## Boundary',
            '',
            '- This digest is a read-only higher-order packet over selected runtime-report family summaries.',
            '- It remains downstream from artifacts, reflections, aggregation witnesses, visibility projections, navigation packets, browser bundles, crosslink packets, provenance traces, temporal traces, and family summaries.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, or digest authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, digest: RuntimeReportOperatorDigest) -> str:
        payload = {
            'digest_kind': 'RUNTIME_REPORT_OPERATOR_DIGEST',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': digest.generated_at,
            'packet_index_path': digest.packet_index_path,
            'family_count': digest.family_count,
            'total_generations': digest.total_generations,
            'shared_trigger_events': list(digest.shared_trigger_events),
            'shared_artifact_kinds': list(digest.shared_artifact_kinds),
            'shared_source_families': list(digest.shared_source_families),
            'runtime_ref_union': list(digest.runtime_ref_union),
            'families': [
                {
                    'family_label': family.family_label,
                    'selector': {
                        'source_ref': family.selector.source_ref,
                        'source_ref_contains': family.selector.source_ref_contains,
                        'trigger_event': family.selector.trigger_event,
                        'artifact_kind': family.selector.artifact_kind,
                        'source_family': family.selector.source_family,
                        'limit': family.selector.limit,
                    },
                    'generation_count': family.generation_count,
                    'shared_trigger_event': family.shared_trigger_event,
                    'shared_artifact_kind': family.shared_artifact_kind,
                    'shared_source_family': family.shared_source_family,
                    'first_generation_label': family.first_generation_label,
                    'first_source_ref': family.first_source_ref,
                    'last_generation_label': family.last_generation_label,
                    'last_source_ref': family.last_source_ref,
                    'runtime_ref_union': list(family.runtime_ref_union),
                    'ever_present_layers': list(family.ever_present_layers),
                    'always_present_layers': list(family.always_present_layers),
                    'transient_layers': list(family.transient_layers),
                    'emergent_layers': list(family.emergent_layers),
                    'vanished_layers': list(family.vanished_layers),
                }
                for family in digest.families
            ],
            'layers': [
                {
                    'layer_name': layer.layer_name,
                    'label': layer.label,
                    'family_presence_count': layer.family_presence_count,
                    'always_present_family_count': layer.always_present_family_count,
                    'stable_target_kind_union': list(layer.stable_target_kind_union),
                    'transient_target_kind_union': list(layer.transient_target_kind_union),
                    'emergent_target_kind_union': list(layer.emergent_target_kind_union),
                    'vanished_target_kind_union': list(layer.vanished_target_kind_union),
                }
                for layer in digest.layers
            ],
            'boundary': [
                'Read-only higher-order packet over selected runtime-report family summaries.',
                'Remains downstream from artifacts, reflections, aggregation witnesses, visibility projections, navigation packets, browser bundles, crosslink packets, provenance traces, temporal traces, and family summaries.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, or digest authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_operator_digest_packet(
        self,
        workspace_root: str | Path,
        selectors: Sequence[RuntimeReportTemporalSelector],
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        digests_dir: str | Path = 'ION/05_context/runtime_reports/governance/digests',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportOperatorDigestWriteResult:
        root = Path(workspace_root).resolve()
        digest = self.build_digest(
            root,
            selectors,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            browser_dir=browser_dir,
            crosslinks_dir=crosslinks_dir,
            created_at=created_at,
        )
        relative_dir = Path(digests_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stem = output_stem or _default_stem(digest, created_at or digest.generated_at)
        markdown_relative = relative_dir / f'{stem}.md'
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        markdown_resolved.write_text(
            self.render_markdown(digest, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        json_relative = relative_dir / f'{stem}.json'
        json_resolved = _resolve_relative_file(root, json_relative)
        json_resolved.write_text(self.render_json(digest), encoding='utf-8')
        return RuntimeReportOperatorDigestWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            digest=digest,
        )


IonRuntimeReportOperatorDigester = KernelRuntimeReportOperatorDigester


def _family_entry(summary: RuntimeReportFamilySummary) -> RuntimeReportOperatorDigestFamilyEntry:
    ever_present_layers = tuple(layer.layer_name for layer in summary.layers if layer.ever_present)
    always_present_layers = tuple(layer.layer_name for layer in summary.layers if layer.always_present)
    transient_layers = tuple(layer.layer_name for layer in summary.layers if layer.transient_target_kinds)
    emergent_layers = tuple(layer.layer_name for layer in summary.layers if layer.emergent_target_kinds)
    vanished_layers = tuple(layer.layer_name for layer in summary.layers if layer.vanished_target_kinds)
    return RuntimeReportOperatorDigestFamilyEntry(
        family_label=_family_label(summary),
        selector=summary.selector,
        generation_count=summary.generation_count,
        shared_trigger_event=summary.shared_trigger_event,
        shared_artifact_kind=summary.shared_artifact_kind,
        shared_source_family=summary.shared_source_family,
        first_generation_label=summary.generation_span.first_generation_label,
        first_source_ref=summary.generation_span.first_source_ref,
        last_generation_label=summary.generation_span.last_generation_label,
        last_source_ref=summary.generation_span.last_source_ref,
        runtime_ref_union=summary.runtime_ref_union,
        ever_present_layers=ever_present_layers,
        always_present_layers=always_present_layers,
        transient_layers=transient_layers,
        emergent_layers=emergent_layers,
        vanished_layers=vanished_layers,
    )


def _rollup_layer(layer_name: str, summaries: Sequence[RuntimeReportFamilySummary]) -> RuntimeReportOperatorDigestLayerOverview:
    selected_layers = []
    for summary in summaries:
        for layer in summary.layers:
            if layer.layer_name == layer_name:
                selected_layers.append(layer)
                break
    if not selected_layers:
        raise KernelRuntimeReportOperatorDigestError(f'Layer not found across summaries: {layer_name}')
    reference = selected_layers[0]
    return RuntimeReportOperatorDigestLayerOverview(
        layer_name=reference.layer_name,
        label=reference.label,
        family_presence_count=sum(1 for layer in selected_layers if layer.ever_present),
        always_present_family_count=sum(1 for layer in selected_layers if layer.always_present),
        stable_target_kind_union=_sorted_unique(kind for layer in selected_layers for kind in layer.stable_target_kinds),
        transient_target_kind_union=_sorted_unique(kind for layer in selected_layers for kind in layer.transient_target_kinds),
        emergent_target_kind_union=_sorted_unique(kind for layer in selected_layers for kind in layer.emergent_target_kinds),
        vanished_target_kind_union=_sorted_unique(kind for layer in selected_layers for kind in layer.vanished_target_kinds),
    )


def _family_label(summary: RuntimeReportFamilySummary) -> str:
    family = summary.selector.source_ref or summary.selector.source_ref_contains
    if family:
        return family
    return f'{summary.shared_trigger_event}/{summary.shared_artifact_kind}/{summary.shared_source_family}'


def _sorted_unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({value for value in values if value}))


def _default_stem(digest: RuntimeReportOperatorDigest, created_at: str) -> str:
    stamp = re.sub(r'[^0-9]', '', created_at)[:14]
    family = _safe(digest.families[0].family_label if digest.families else 'digest')
    return f'{family}__runtime_operator_digest_{stamp}'


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportOperatorDigestError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportOperatorDigestError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
