"""Read-only comparative provenance tracing over downstream runtime-report witness surfaces.

This module places two or more runtime-report receipts side by side across the same
bounded downstream witness chain: artifact, governance reflection, governance
aggregation, visibility projection, navigation packets, browser bundles, and
crosslink packets. It remains explicitly read-only and does not promote any
comparative packet into kernel truth, doctrine, route authority, or runtime authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable

from .runtime_report_provenance import (
    KernelRuntimeReportProvenanceError,
    KernelRuntimeReportProvenanceTracer,
    RuntimeReportProvenanceSelector,
    RuntimeReportProvenanceTrace,
)


class KernelRuntimeReportComparativeProvenanceError(Exception):
    """Raised when one comparative provenance request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportComparativeSelector:
    selector: RuntimeReportProvenanceSelector
    label: str | None = None


@dataclass(frozen=True)
class RuntimeReportComparativeReceipt:
    comparison_label: str
    entry_index: int
    packet_index_pointer: str | None
    trigger_event: str
    artifact_kind: str
    source_ref: str
    source_family: str
    reason: str | None
    runtime_refs: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportComparativeLayerReceipt:
    comparison_label: str
    source_ref: str
    target_count: int
    target_kinds: tuple[str, ...]
    target_refs: tuple[str, ...]


@dataclass(frozen=True)
class RuntimeReportComparativeLayer:
    layer_name: str
    label: str
    shared_presence: bool
    shared_target_kinds: tuple[str, ...]
    divergent_target_kinds: tuple[str, ...]
    receipts: tuple[RuntimeReportComparativeLayerReceipt, ...]


@dataclass(frozen=True)
class RuntimeReportComparativeTrace:
    generated_at: str
    read_only_mode: bool
    packet_index_path: str
    compared_count: int
    receipts: tuple[RuntimeReportComparativeReceipt, ...]
    layers: tuple[RuntimeReportComparativeLayer, ...]


@dataclass(frozen=True)
class RuntimeReportComparativeWriteResult:
    markdown_path: str
    json_path: str
    trace: RuntimeReportComparativeTrace


class KernelRuntimeReportComparativeProvenanceTracer:
    """Compare two or more provenance traces without promoting them into authority."""

    def __init__(self, *, tracer: KernelRuntimeReportProvenanceTracer | None = None) -> None:
        self._tracer = tracer or KernelRuntimeReportProvenanceTracer()

    def compare_receipts(
        self,
        workspace_root: str | Path,
        selectors: Iterable[RuntimeReportComparativeSelector],
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        created_at: str | None = None,
    ) -> RuntimeReportComparativeTrace:
        realized = tuple(selectors)
        if len(realized) < 2:
            raise KernelRuntimeReportComparativeProvenanceError(
                'Comparative provenance requires at least two receipt selectors.'
            )
        root = Path(workspace_root).resolve()
        traces: list[tuple[str, RuntimeReportProvenanceTrace]] = []
        for index, item in enumerate(realized, start=1):
            try:
                trace = self._tracer.trace_receipt(
                    root,
                    item.selector,
                    packet_index_path=packet_index_path,
                    operator_dashboard_path=operator_dashboard_path,
                    navigation_dir=navigation_dir,
                    browser_dir=browser_dir,
                    crosslinks_dir=crosslinks_dir,
                    created_at=created_at,
                )
            except KernelRuntimeReportProvenanceError as exc:
                raise KernelRuntimeReportComparativeProvenanceError(str(exc)) from exc
            label = item.label or f'Receipt {index}'
            traces.append((label, trace))

        packet_index_values = {trace.packet_index_path for _, trace in traces}
        packet_index_value = next(iter(packet_index_values)) if packet_index_values else str(packet_index_path)
        return RuntimeReportComparativeTrace(
            generated_at=created_at or _iso_now(),
            read_only_mode=True,
            packet_index_path=packet_index_value,
            compared_count=len(traces),
            receipts=tuple(
                RuntimeReportComparativeReceipt(
                    comparison_label=label,
                    entry_index=trace.entry_index,
                    packet_index_pointer=trace.packet_index_pointer,
                    trigger_event=trace.trigger_event,
                    artifact_kind=trace.artifact_kind,
                    source_ref=trace.source_ref,
                    source_family=trace.source_family,
                    reason=trace.reason,
                    runtime_refs=trace.runtime_refs,
                )
                for label, trace in traces
            ),
            layers=self._compare_layers(traces),
        )

    def render_markdown(
        self,
        trace: RuntimeReportComparativeTrace,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'comparison_kind: RUNTIME_REPORT_COMPARATIVE_PROVENANCE_TRACE',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {trace.generated_at}',
            f'packet_index_path: {trace.packet_index_path}',
            f'compared_count: {trace.compared_count}',
        ]
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Comparative Provenance Trace',
            '',
            '## Compared Receipts',
            '',
        ])
        for receipt in trace.receipts:
            lines.extend([
                f'### {receipt.comparison_label}',
                '',
                f'- Entry Index: {receipt.entry_index}',
                f'- Packet Index Pointer: {receipt.packet_index_pointer or "NONE"}',
                f'- Trigger Event: {receipt.trigger_event}',
                f'- Artifact Kind: {receipt.artifact_kind}',
                f'- Source Ref: {receipt.source_ref}',
                f'- Source Family: {receipt.source_family}',
                f'- Reason: {receipt.reason or "NONE"}',
            ])
            if receipt.runtime_refs:
                lines.append('- Runtime Refs:')
                lines.extend(f'  - {item}' for item in receipt.runtime_refs)
            lines.append('')

        lines.extend([
            '## Shared Structure',
            '',
            f'- Shared Trigger Event: {_single_value_or_mixed(item.trigger_event for item in trace.receipts)}',
            f'- Shared Artifact Kind: {_single_value_or_mixed(item.artifact_kind for item in trace.receipts)}',
            f'- Shared Source Family: {_single_value_or_mixed(item.source_family for item in trace.receipts)}',
            '',
            '## Layer-by-Layer Comparison',
            '',
        ])
        for layer in trace.layers:
            lines.extend([
                f'### {layer.label}',
                '',
                f'- Shared Presence Across Compared Receipts: {"YES" if layer.shared_presence else "NO"}',
                f'- Shared Target Kinds: {", ".join(layer.shared_target_kinds) if layer.shared_target_kinds else "NONE"}',
                f'- Divergent Target Kinds: {", ".join(layer.divergent_target_kinds) if layer.divergent_target_kinds else "NONE"}',
                '',
            ])
            for receipt in layer.receipts:
                lines.extend([
                    f'#### {receipt.comparison_label}',
                    '',
                    f'- Source Ref: {receipt.source_ref}',
                    f'- Target Count: {receipt.target_count}',
                    f'- Target Kinds: {", ".join(receipt.target_kinds) if receipt.target_kinds else "NONE"}',
                ])
                if receipt.target_refs:
                    lines.append('- Target Refs:')
                    lines.extend(f'  - {item}' for item in receipt.target_refs)
                lines.append('')
        lines.extend([
            '## Boundary',
            '',
            '- This packet is a read-only structural comparison over downstream runtime-report witness material.',
            '- It can place two or more receipts side by side across artifact, reflection, aggregation, visibility, navigation, browser, and crosslink layers when those files exist.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, or comparative analysis authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, trace: RuntimeReportComparativeTrace) -> str:
        payload = {
            'comparison_kind': 'RUNTIME_REPORT_COMPARATIVE_PROVENANCE_TRACE',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': trace.generated_at,
            'packet_index_path': trace.packet_index_path,
            'compared_count': trace.compared_count,
            'receipt_summary': {
                'trigger_event': _single_value_or_none(item.trigger_event for item in trace.receipts),
                'artifact_kind': _single_value_or_none(item.artifact_kind for item in trace.receipts),
                'source_family': _single_value_or_none(item.source_family for item in trace.receipts),
            },
            'receipts': [
                {
                    'comparison_label': item.comparison_label,
                    'entry_index': item.entry_index,
                    'packet_index_pointer': item.packet_index_pointer,
                    'trigger_event': item.trigger_event,
                    'artifact_kind': item.artifact_kind,
                    'source_ref': item.source_ref,
                    'source_family': item.source_family,
                    'reason': item.reason,
                    'runtime_refs': list(item.runtime_refs),
                }
                for item in trace.receipts
            ],
            'layers': [
                {
                    'layer_name': layer.layer_name,
                    'label': layer.label,
                    'shared_presence': layer.shared_presence,
                    'shared_target_kinds': list(layer.shared_target_kinds),
                    'divergent_target_kinds': list(layer.divergent_target_kinds),
                    'receipts': [
                        {
                            'comparison_label': receipt.comparison_label,
                            'source_ref': receipt.source_ref,
                            'target_count': receipt.target_count,
                            'target_kinds': list(receipt.target_kinds),
                            'target_refs': list(receipt.target_refs),
                        }
                        for receipt in layer.receipts
                    ],
                }
                for layer in trace.layers
            ],
            'boundary': [
                'Read-only structural comparison over downstream runtime-report witness material.',
                'Places two or more receipts side by side across artifact, reflection, aggregation, visibility, navigation, browser, and crosslink layers when available.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, or comparative analysis authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_comparison_packet(
        self,
        workspace_root: str | Path,
        selectors: Iterable[RuntimeReportComparativeSelector],
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        comparisons_dir: str | Path = 'ION/05_context/runtime_reports/governance/provenance/comparisons',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportComparativeWriteResult:
        root = Path(workspace_root).resolve()
        realized = tuple(selectors)
        trace = self.compare_receipts(
            root,
            realized,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            browser_dir=browser_dir,
            crosslinks_dir=crosslinks_dir,
            created_at=created_at,
        )
        relative_dir = Path(comparisons_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stem = output_stem or _default_stem(trace, realized, trace.generated_at)
        markdown_relative = relative_dir / f'{stem}.md'
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        markdown_resolved.write_text(
            self.render_markdown(trace, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        json_relative = relative_dir / f'{stem}.json'
        json_resolved = _resolve_relative_file(root, json_relative)
        json_resolved.write_text(self.render_json(trace), encoding='utf-8')
        return RuntimeReportComparativeWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            trace=trace,
        )

    def _compare_layers(
        self,
        traces: Iterable[tuple[str, RuntimeReportProvenanceTrace]],
    ) -> tuple[RuntimeReportComparativeLayer, ...]:
        realized = tuple(traces)
        if not realized:
            return ()
        first_layers = realized[0][1].layers
        comparison_layers: list[RuntimeReportComparativeLayer] = []
        for layer_index, reference in enumerate(first_layers):
            receipt_views: list[RuntimeReportComparativeLayerReceipt] = []
            kind_sets: list[set[str]] = []
            for label, trace in realized:
                layer = trace.layers[layer_index]
                target_kinds = tuple(target.target_kind for target in layer.targets)
                kind_set = set(target_kinds)
                kind_sets.append(kind_set)
                receipt_views.append(
                    RuntimeReportComparativeLayerReceipt(
                        comparison_label=label,
                        source_ref=trace.source_ref,
                        target_count=len(layer.targets),
                        target_kinds=target_kinds,
                        target_refs=tuple(target.target_ref for target in layer.targets),
                    )
                )
            union_kinds = sorted(set().union(*kind_sets)) if kind_sets else []
            shared_kinds = sorted(set.intersection(*kind_sets)) if kind_sets else []
            comparison_layers.append(
                RuntimeReportComparativeLayer(
                    layer_name=reference.layer_name,
                    label=reference.label,
                    shared_presence=all(view.target_count > 0 for view in receipt_views),
                    shared_target_kinds=tuple(shared_kinds),
                    divergent_target_kinds=tuple(kind for kind in union_kinds if kind not in shared_kinds),
                    receipts=tuple(receipt_views),
                )
            )
        return tuple(comparison_layers)


IonRuntimeReportComparativeProvenanceTracer = KernelRuntimeReportComparativeProvenanceTracer


def _single_value_or_none(values: Iterable[str | None]) -> str | None:
    items = {value for value in values}
    if len(items) == 1:
        return next(iter(items))
    return None


def _single_value_or_mixed(values: Iterable[str | None]) -> str:
    value = _single_value_or_none(values)
    return value if value is not None else 'MIXED'


def _default_stem(
    trace: RuntimeReportComparativeTrace,
    selectors: tuple[RuntimeReportComparativeSelector, ...],
    created_at: str,
) -> str:
    stamp = re.sub(r'[^0-9]', '', created_at)[:14]
    labels = [
        _safe(item.label) for item in selectors if item.label
    ]
    if not labels:
        labels = [_safe(receipt.source_ref) for receipt in trace.receipts[:2]]
    joined = '__'.join(labels[:3]) or 'comparison'
    return f'{joined}__runtime_comparative_provenance_{stamp}'


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportComparativeProvenanceError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportComparativeProvenanceError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
