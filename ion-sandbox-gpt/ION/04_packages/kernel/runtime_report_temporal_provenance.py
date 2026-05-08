"""Read-only temporal provenance tracing over downstream runtime-report witness surfaces.

This module compares successive generations of the same runtime-report receipt family
across the downstream witness chain: artifact, governance reflection, governance
aggregation, visibility projection, navigation packets, browser bundles, and crosslink
packets. It remains explicitly read-only and does not promote any downstream surface
into kernel truth, doctrine, route authority, runtime authority, or temporal analysis
authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable

from .runtime_report_navigation import KernelRuntimeReportNavigator, RuntimeReportNavigationQuery
from .runtime_report_provenance import (
    KernelRuntimeReportProvenanceError,
    KernelRuntimeReportProvenanceTracer,
    RuntimeReportProvenanceSelector,
    RuntimeReportProvenanceTrace,
)


class KernelRuntimeReportTemporalProvenanceError(Exception):
    """Raised when one temporal provenance request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportTemporalSelector:
    source_ref: str | None = None
    source_ref_contains: str | None = None
    trigger_event: str | None = None
    artifact_kind: str | None = None
    source_family: str | None = None
    limit: int | None = None


@dataclass(frozen=True)
class RuntimeReportTemporalGeneration:
    generation_label: str
    generation_index: int
    entry_index: int
    packet_index_pointer: str | None
    created_at: str | None
    trigger_event: str
    artifact_kind: str
    source_ref: str
    source_family: str
    reason: str | None
    runtime_refs: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportTemporalLayerGeneration:
    generation_label: str
    generation_index: int
    entry_index: int
    created_at: str | None
    target_count: int
    target_kinds: tuple[str, ...]
    target_refs: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportTemporalLayerTransition:
    from_generation_label: str
    to_generation_label: str
    added_target_kinds: tuple[str, ...]
    removed_target_kinds: tuple[str, ...]
    changed: bool


@dataclass(frozen=True)
class RuntimeReportTemporalLayer:
    layer_name: str
    label: str
    stable_target_kinds: tuple[str, ...]
    emergent_target_kinds: tuple[str, ...]
    vanished_target_kinds: tuple[str, ...]
    generations: tuple[RuntimeReportTemporalLayerGeneration, ...]
    transitions: tuple[RuntimeReportTemporalLayerTransition, ...]


@dataclass(frozen=True)
class RuntimeReportTemporalTrace:
    generated_at: str
    read_only_mode: bool
    packet_index_path: str
    selector: RuntimeReportTemporalSelector
    generation_count: int
    generations: tuple[RuntimeReportTemporalGeneration, ...]
    layers: tuple[RuntimeReportTemporalLayer, ...]


@dataclass(frozen=True)
class RuntimeReportTemporalWriteResult:
    markdown_path: str
    json_path: str
    trace: RuntimeReportTemporalTrace


class KernelRuntimeReportTemporalProvenanceTracer:
    """Compare successive generations of one receipt family without promoting them into authority."""

    def __init__(
        self,
        *,
        navigator: KernelRuntimeReportNavigator | None = None,
        tracer: KernelRuntimeReportProvenanceTracer | None = None,
    ) -> None:
        self._navigator = navigator or KernelRuntimeReportNavigator()
        self._tracer = tracer or KernelRuntimeReportProvenanceTracer(navigator=self._navigator)

    def trace_family_generations(
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
    ) -> RuntimeReportTemporalTrace:
        root = Path(workspace_root).resolve()
        matched_entries = self._resolve_family_entries(
            root,
            selector,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
        )
        traces: list[RuntimeReportProvenanceTrace] = []
        for entry in matched_entries:
            try:
                trace = self._tracer.trace_receipt(
                    root,
                    RuntimeReportProvenanceSelector(entry_index=entry.entry_index),
                    packet_index_path=packet_index_path,
                    operator_dashboard_path=operator_dashboard_path,
                    navigation_dir=navigation_dir,
                    browser_dir=browser_dir,
                    crosslinks_dir=crosslinks_dir,
                    created_at=created_at,
                )
            except KernelRuntimeReportProvenanceError as exc:
                raise KernelRuntimeReportTemporalProvenanceError(str(exc)) from exc
            traces.append(trace)

        generations = tuple(
            RuntimeReportTemporalGeneration(
                generation_label=f'Generation {position}',
                generation_index=position,
                entry_index=trace.entry_index,
                packet_index_pointer=trace.packet_index_pointer,
                created_at=matched_entries[position - 1].created_at,
                trigger_event=trace.trigger_event,
                artifact_kind=trace.artifact_kind,
                source_ref=trace.source_ref,
                source_family=trace.source_family,
                reason=trace.reason,
                runtime_refs=trace.runtime_refs,
            )
            for position, trace in enumerate(traces, start=1)
        )

        return RuntimeReportTemporalTrace(
            generated_at=created_at or _iso_now(),
            read_only_mode=True,
            packet_index_path=str(packet_index_path),
            selector=selector,
            generation_count=len(generations),
            generations=generations,
            layers=self._compare_temporal_layers(generations, traces),
        )

    def render_markdown(
        self,
        trace: RuntimeReportTemporalTrace,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'comparison_kind: RUNTIME_REPORT_TEMPORAL_PROVENANCE_TRACE',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {trace.generated_at}',
            f'packet_index_path: {trace.packet_index_path}',
            f'generation_count: {trace.generation_count}',
        ]
        if trace.selector.source_ref is not None:
            lines.append(f'source_ref: {trace.selector.source_ref}')
        if trace.selector.source_ref_contains is not None:
            lines.append(f'source_ref_contains: {trace.selector.source_ref_contains}')
        if trace.selector.source_family is not None:
            lines.append(f'source_family: {trace.selector.source_family}')
        if trace.selector.trigger_event is not None:
            lines.append(f'trigger_event: {trace.selector.trigger_event}')
        if trace.selector.artifact_kind is not None:
            lines.append(f'artifact_kind: {trace.selector.artifact_kind}')
        if trace.selector.limit is not None:
            lines.append(f'selector_limit: {trace.selector.limit}')
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Temporal Provenance Trace',
            '',
            '## Generation Family',
            '',
            f'- Generation Count: {trace.generation_count}',
            f'- Source Ref Family: {_selector_family_value(trace.selector.source_ref, trace.selector.source_ref_contains)}',
            f'- Trigger Event: {trace.selector.trigger_event or _single_value_or_mixed(item.trigger_event for item in trace.generations)}',
            f'- Artifact Kind: {trace.selector.artifact_kind or _single_value_or_mixed(item.artifact_kind for item in trace.generations)}',
            f'- Source Family: {trace.selector.source_family or _single_value_or_mixed(item.source_family for item in trace.generations)}',
            '',
            '## Generations',
            '',
        ])
        for generation in trace.generations:
            lines.extend([
                f'### {generation.generation_label}',
                '',
                f'- Entry Index: {generation.entry_index}',
                f'- Packet Index Pointer: {generation.packet_index_pointer or "NONE"}',
                f'- Created At: {generation.created_at or "NONE"}',
                f'- Trigger Event: {generation.trigger_event}',
                f'- Artifact Kind: {generation.artifact_kind}',
                f'- Source Ref: {generation.source_ref}',
                f'- Source Family: {generation.source_family}',
                f'- Reason: {generation.reason or "NONE"}',
            ])
            if generation.runtime_refs:
                lines.append('- Runtime Refs:')
                lines.extend(f'  - {item}' for item in generation.runtime_refs)
            lines.append('')

        lines.extend([
            '## Layer-by-Layer Temporal Comparison',
            '',
        ])
        for layer in trace.layers:
            lines.extend([
                f'### {layer.label}',
                '',
                f'- Stable Target Kinds: {", ".join(layer.stable_target_kinds) if layer.stable_target_kinds else "NONE"}',
                f'- Emergent Target Kinds: {", ".join(layer.emergent_target_kinds) if layer.emergent_target_kinds else "NONE"}',
                f'- Vanished Target Kinds: {", ".join(layer.vanished_target_kinds) if layer.vanished_target_kinds else "NONE"}',
                '',
            ])
            for item in layer.generations:
                lines.extend([
                    f'#### {item.generation_label}',
                    '',
                    f'- Entry Index: {item.entry_index}',
                    f'- Created At: {item.created_at or "NONE"}',
                    f'- Target Count: {item.target_count}',
                    f'- Target Kinds: {", ".join(item.target_kinds) if item.target_kinds else "NONE"}',
                ])
                if item.target_refs:
                    lines.append('- Target Refs:')
                    lines.extend(f'  - {target_ref}' for target_ref in item.target_refs)
                lines.append('')
            if layer.transitions:
                lines.append('#### Temporal Transitions')
                lines.append('')
                for transition in layer.transitions:
                    lines.extend([
                        f'- {transition.from_generation_label} -> {transition.to_generation_label}: '
                        f'changed={"YES" if transition.changed else "NO"}; '
                        f'added={", ".join(transition.added_target_kinds) if transition.added_target_kinds else "NONE"}; '
                        f'removed={", ".join(transition.removed_target_kinds) if transition.removed_target_kinds else "NONE"}',
                    ])
                lines.append('')
        lines.extend([
            '## Boundary',
            '',
            '- This packet is a read-only temporal comparison over downstream runtime-report witness material.',
            '- It compares successive generations of one receipt family across artifact, reflection, aggregation, visibility, navigation, browser, and crosslink layers when those files exist.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, or temporal analysis authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, trace: RuntimeReportTemporalTrace) -> str:
        payload = {
            'comparison_kind': 'RUNTIME_REPORT_TEMPORAL_PROVENANCE_TRACE',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': trace.generated_at,
            'packet_index_path': trace.packet_index_path,
            'generation_count': trace.generation_count,
            'selector': {
                'source_ref': trace.selector.source_ref,
                'source_ref_contains': trace.selector.source_ref_contains,
                'trigger_event': trace.selector.trigger_event,
                'artifact_kind': trace.selector.artifact_kind,
                'source_family': trace.selector.source_family,
                'limit': trace.selector.limit,
            },
            'generations': [
                {
                    'generation_label': item.generation_label,
                    'generation_index': item.generation_index,
                    'entry_index': item.entry_index,
                    'packet_index_pointer': item.packet_index_pointer,
                    'created_at': item.created_at,
                    'trigger_event': item.trigger_event,
                    'artifact_kind': item.artifact_kind,
                    'source_ref': item.source_ref,
                    'source_family': item.source_family,
                    'reason': item.reason,
                    'runtime_refs': list(item.runtime_refs),
                }
                for item in trace.generations
            ],
            'layers': [
                {
                    'layer_name': layer.layer_name,
                    'label': layer.label,
                    'stable_target_kinds': list(layer.stable_target_kinds),
                    'emergent_target_kinds': list(layer.emergent_target_kinds),
                    'vanished_target_kinds': list(layer.vanished_target_kinds),
                    'generations': [
                        {
                            'generation_label': item.generation_label,
                            'generation_index': item.generation_index,
                            'entry_index': item.entry_index,
                            'created_at': item.created_at,
                            'target_count': item.target_count,
                            'target_kinds': list(item.target_kinds),
                            'target_refs': list(item.target_refs),
                        }
                        for item in layer.generations
                    ],
                    'transitions': [
                        {
                            'from_generation_label': transition.from_generation_label,
                            'to_generation_label': transition.to_generation_label,
                            'added_target_kinds': list(transition.added_target_kinds),
                            'removed_target_kinds': list(transition.removed_target_kinds),
                            'changed': transition.changed,
                        }
                        for transition in layer.transitions
                    ],
                }
                for layer in trace.layers
            ],
            'boundary': [
                'Read-only temporal comparison over downstream runtime-report witness material.',
                'Compares successive generations of one receipt family across artifact, reflection, aggregation, visibility, navigation, browser, and crosslink layers when available.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, or temporal analysis authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_temporal_packet(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportTemporalSelector,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        temporal_dir: str | Path = 'ION/05_context/runtime_reports/governance/provenance/temporal',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportTemporalWriteResult:
        root = Path(workspace_root).resolve()
        trace = self.trace_family_generations(
            root,
            selector,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            browser_dir=browser_dir,
            crosslinks_dir=crosslinks_dir,
            created_at=created_at,
        )
        relative_dir = Path(temporal_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stem = output_stem or _default_stem(trace, created_at or trace.generated_at)
        markdown_relative = relative_dir / f'{stem}.md'
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        markdown_resolved.write_text(
            self.render_markdown(trace, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        json_relative = relative_dir / f'{stem}.json'
        json_resolved = _resolve_relative_file(root, json_relative)
        json_resolved.write_text(self.render_json(trace), encoding='utf-8')
        return RuntimeReportTemporalWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            trace=trace,
        )

    def _resolve_family_entries(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportTemporalSelector,
        *,
        packet_index_path: str | Path,
        operator_dashboard_path: str | Path,
    ) -> tuple:
        if not any((
            selector.source_ref,
            selector.source_ref_contains,
            selector.trigger_event,
            selector.artifact_kind,
            selector.source_family,
        )):
            raise KernelRuntimeReportTemporalProvenanceError(
                'A temporal provenance selector must identify at least one receipt family field.'
            )
        query = RuntimeReportNavigationQuery(
            artifact_kind=selector.artifact_kind,
            trigger_event=selector.trigger_event,
            source_family=selector.source_family,
            source_ref_contains=selector.source_ref_contains or selector.source_ref,
            limit=10_000,
        )
        result = self._navigator.query_entries(
            workspace_root,
            query,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
        )
        matches = [entry for entry in result.entries if _matches_family(entry, selector)]
        matches.sort(key=lambda item: (_sortable_timestamp(item.created_at), item.entry_index))
        if selector.limit is not None and selector.limit >= 0:
            matches = matches[-selector.limit:] if selector.limit > 0 else []
        if len(matches) < 2:
            raise KernelRuntimeReportTemporalProvenanceError(
                'Temporal provenance requires at least two matching receipt generations.'
            )
        return tuple(matches)

    def _compare_temporal_layers(
        self,
        generations: tuple[RuntimeReportTemporalGeneration, ...],
        traces: list[RuntimeReportProvenanceTrace],
    ) -> tuple[RuntimeReportTemporalLayer, ...]:
        if not traces:
            return ()
        reference_layers = traces[0].layers
        compared: list[RuntimeReportTemporalLayer] = []
        for layer_index, reference in enumerate(reference_layers):
            layer_generations: list[RuntimeReportTemporalLayerGeneration] = []
            kind_sets: list[set[str]] = []
            transitions: list[RuntimeReportTemporalLayerTransition] = []
            previous_kinds: set[str] | None = None
            for generation, trace in zip(generations, traces, strict=True):
                layer = trace.layers[layer_index]
                target_kinds = tuple(target.target_kind for target in layer.targets)
                current_kinds = set(target_kinds)
                kind_sets.append(current_kinds)
                layer_generations.append(
                    RuntimeReportTemporalLayerGeneration(
                        generation_label=generation.generation_label,
                        generation_index=generation.generation_index,
                        entry_index=generation.entry_index,
                        created_at=generation.created_at,
                        target_count=len(layer.targets),
                        target_kinds=target_kinds,
                        target_refs=tuple(target.target_ref for target in layer.targets),
                    )
                )
                if previous_kinds is not None:
                    added = tuple(sorted(current_kinds - previous_kinds))
                    removed = tuple(sorted(previous_kinds - current_kinds))
                    transitions.append(
                        RuntimeReportTemporalLayerTransition(
                            from_generation_label=generations[generation.generation_index - 2].generation_label,
                            to_generation_label=generation.generation_label,
                            added_target_kinds=added,
                            removed_target_kinds=removed,
                            changed=bool(added or removed),
                        )
                    )
                previous_kinds = current_kinds
            stable = tuple(sorted(set.intersection(*kind_sets))) if kind_sets else ()
            emergent = tuple(sorted({kind for transition in transitions for kind in transition.added_target_kinds}))
            vanished = tuple(sorted({kind for transition in transitions for kind in transition.removed_target_kinds}))
            compared.append(
                RuntimeReportTemporalLayer(
                    layer_name=reference.layer_name,
                    label=reference.label,
                    stable_target_kinds=stable,
                    emergent_target_kinds=emergent,
                    vanished_target_kinds=vanished,
                    generations=tuple(layer_generations),
                    transitions=tuple(transitions),
                )
            )
        return tuple(compared)


IonRuntimeReportTemporalProvenanceTracer = KernelRuntimeReportTemporalProvenanceTracer


def _matches_family(entry, selector: RuntimeReportTemporalSelector) -> bool:
    if selector.source_ref is not None and entry.source_ref != selector.source_ref:
        return False
    if selector.source_ref_contains is not None and selector.source_ref_contains.casefold() not in entry.source_ref.casefold():
        return False
    if selector.trigger_event is not None and entry.trigger_event.casefold() != selector.trigger_event.casefold():
        return False
    if selector.artifact_kind is not None and entry.artifact_kind.casefold() != selector.artifact_kind.casefold():
        return False
    if selector.source_family is not None and entry.source_family.casefold() != selector.source_family.casefold():
        return False
    return True


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


def _sortable_timestamp(value: str | None) -> tuple[int, str]:
    if isinstance(value, str) and value:
        return (1, value)
    return (0, '')


def _default_stem(trace: RuntimeReportTemporalTrace, created_at: str) -> str:
    stamp = re.sub(r'[^0-9]', '', created_at)[:14]
    family = _safe(
        trace.selector.source_ref
        or trace.selector.source_ref_contains
        or trace.selector.artifact_kind
        or trace.selector.trigger_event
        or trace.selector.source_family
        or 'family'
    )
    return f'{family}__runtime_temporal_provenance_{stamp}'


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportTemporalProvenanceError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportTemporalProvenanceError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
