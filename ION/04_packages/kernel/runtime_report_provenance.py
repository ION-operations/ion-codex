"""Read-only provenance tracing over downstream runtime-report witness surfaces.

This module walks one projected runtime-report receipt across the downstream witness
chain: artifact, governance reflection, governance aggregation, visibility projection,
navigation packets, browser bundles, and crosslink packets. It remains explicitly
read-only and does not promote any downstream surface into kernel truth, doctrine,
route authority, or runtime authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable

from .runtime_report_anchors import join_relative_target
from .runtime_report_navigation import (
    KernelRuntimeReportNavigator,
    RuntimeReportNavigationEntry,
    RuntimeReportNavigationQuery,
)


class KernelRuntimeReportProvenanceError(Exception):
    """Raised when one provenance trace cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportProvenanceSelector:
    entry_index: int | None = None
    packet_index_pointer: str | None = None
    source_ref: str | None = None
    trigger_event: str | None = None
    artifact_kind: str | None = None


@dataclass(frozen=True)
class RuntimeReportProvenanceTarget:
    target_kind: str
    label: str
    relative_path: str
    exists: bool
    anchor_kind: str | None = None
    anchor_fragment: str | None = None

    @property
    def target_ref(self) -> str:
        return join_relative_target(self.relative_path, self.anchor_fragment)


@dataclass(frozen=True)
class RuntimeReportProvenanceLayer:
    layer_name: str
    label: str
    targets: tuple[RuntimeReportProvenanceTarget, ...]


@dataclass(frozen=True)
class RuntimeReportProvenanceTrace:
    generated_at: str
    read_only_mode: bool
    packet_index_path: str
    selector: RuntimeReportProvenanceSelector
    entry_index: int
    packet_index_pointer: str | None
    trigger_event: str
    artifact_kind: str
    source_ref: str
    source_family: str
    reason: str | None
    runtime_refs: tuple[str, ...]
    layers: tuple[RuntimeReportProvenanceLayer, ...]


@dataclass(frozen=True)
class RuntimeReportProvenanceWriteResult:
    markdown_path: str
    json_path: str
    trace: RuntimeReportProvenanceTrace


class KernelRuntimeReportProvenanceTracer:
    """Resolve one runtime-report receipt into a bounded read-only lineage packet."""

    def __init__(self, *, navigator: KernelRuntimeReportNavigator | None = None) -> None:
        self._navigator = navigator or KernelRuntimeReportNavigator()

    def trace_receipt(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportProvenanceSelector,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        created_at: str | None = None,
    ) -> RuntimeReportProvenanceTrace:
        root = Path(workspace_root).resolve()
        entry = self._resolve_entry(
            root,
            selector,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
        )
        return RuntimeReportProvenanceTrace(
            generated_at=created_at or _iso_now(),
            read_only_mode=True,
            packet_index_path=str(packet_index_path),
            selector=selector,
            entry_index=entry.entry_index,
            packet_index_pointer=entry.packet_index_pointer,
            trigger_event=entry.trigger_event,
            artifact_kind=entry.artifact_kind,
            source_ref=entry.source_ref,
            source_family=entry.source_family,
            reason=entry.reason,
            runtime_refs=entry.runtime_refs,
            layers=(
                RuntimeReportProvenanceLayer(
                    layer_name='ARTIFACT',
                    label='Generated Artifact',
                    targets=tuple(
                        item for item in (
                            _make_target(
                                root,
                                'ARTIFACT_REPORT',
                                'Artifact Report',
                                entry.artifact_relative_output_path,
                                anchor_kind=('MARKDOWN_ANCHOR' if entry.artifact_anchor else None),
                                anchor_fragment=(f'#{entry.artifact_anchor}' if entry.artifact_anchor else None),
                            ),
                        ) if item is not None
                    ),
                ),
                RuntimeReportProvenanceLayer(
                    layer_name='GOVERNANCE_REFLECTION',
                    label='Governance Reflection',
                    targets=tuple(
                        item for item in (
                            _make_target(
                                root,
                                'GOVERNANCE_LEDGER',
                                'Governance Ledger',
                                entry.governance_ledger_path,
                                anchor_kind=('JSON_POINTER' if entry.governance_ledger_entry_index is not None else None),
                                anchor_fragment=(f'#/{entry.governance_ledger_entry_index - 1}' if entry.governance_ledger_entry_index is not None else None),
                            ),
                            _make_target(
                                root,
                                'GOVERNANCE_SUMMARY',
                                'Governance Summary',
                                entry.operator_summary_path,
                                anchor_kind=('MARKDOWN_ANCHOR' if entry.operator_summary_anchor else None),
                                anchor_fragment=(f'#{entry.operator_summary_anchor}' if entry.operator_summary_anchor else None),
                            ),
                        ) if item is not None
                    ),
                ),
                RuntimeReportProvenanceLayer(
                    layer_name='GOVERNANCE_AGGREGATION',
                    label='Governance Aggregation',
                    targets=tuple(
                        item for item in (
                            _make_target(
                                root,
                                'SYSTEM_LEDGER',
                                'System Ledger',
                                entry.system_ledger_path,
                                anchor_kind=('JSON_POINTER' if entry.system_ledger_entry_index is not None else None),
                                anchor_fragment=(f'#/{entry.system_ledger_entry_index - 1}' if entry.system_ledger_entry_index is not None else None),
                            ),
                            _make_target(
                                root,
                                'OPERATOR_ROLLUP',
                                'Operator Rollup',
                                entry.operator_rollup_path,
                                anchor_kind=('MARKDOWN_ANCHOR' if entry.operator_rollup_anchor else None),
                                anchor_fragment=(f'#{entry.operator_rollup_anchor}' if entry.operator_rollup_anchor else None),
                            ),
                        ) if item is not None
                    ),
                ),
                RuntimeReportProvenanceLayer(
                    layer_name='VISIBILITY_PROJECTION',
                    label='Visibility Projection',
                    targets=tuple(
                        item for item in (
                            _make_target(
                                root,
                                'PACKET_INDEX',
                                'Packet Index',
                                str(packet_index_path),
                                anchor_kind=('JSON_POINTER' if entry.packet_index_pointer else None),
                                anchor_fragment=entry.packet_index_pointer,
                            ),
                            _make_target(
                                root,
                                'OPERATOR_DASHBOARD',
                                'Operator Dashboard',
                                entry.operator_dashboard_path,
                                anchor_kind=('MARKDOWN_ANCHOR' if entry.operator_dashboard_anchor else None),
                                anchor_fragment=(f'#{entry.operator_dashboard_anchor}' if entry.operator_dashboard_anchor else None),
                            ),
                        ) if item is not None
                    ),
                ),
                RuntimeReportProvenanceLayer(
                    layer_name='NAVIGATION_PACKETS',
                    label='Navigation Packets',
                    targets=self._find_navigation_packets(root, entry, navigation_dir=navigation_dir),
                ),
                RuntimeReportProvenanceLayer(
                    layer_name='BROWSER_BUNDLES',
                    label='Browser Bundles',
                    targets=self._find_browser_bundles(root, entry, browser_dir=browser_dir),
                ),
                RuntimeReportProvenanceLayer(
                    layer_name='CROSSLINK_PACKETS',
                    label='Crosslink Packets',
                    targets=self._find_crosslink_packets(root, entry, crosslinks_dir=crosslinks_dir),
                ),
            ),
        )

    def render_markdown(
        self,
        trace: RuntimeReportProvenanceTrace,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'provenance_kind: RUNTIME_REPORT_PROVENANCE_TRACE',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {trace.generated_at}',
            f'packet_index_path: {trace.packet_index_path}',
            f'entry_index: {trace.entry_index}',
            f'trigger_event: {trace.trigger_event}',
            f'artifact_kind: {trace.artifact_kind}',
            f'source_ref: {trace.source_ref}',
        ]
        if output_relative_path is not None:
            lines.append(f'relative_output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Provenance Trace',
            '',
            '## Receipt',
            '',
            f'- Entry Index: {trace.entry_index}',
            f'- Packet Index Pointer: {trace.packet_index_pointer or "NONE"}',
            f'- Trigger Event: {trace.trigger_event}',
            f'- Artifact Kind: {trace.artifact_kind}',
            f'- Source Ref: {trace.source_ref}',
            f'- Source Family: {trace.source_family}',
            f'- Reason: {trace.reason or "NONE"}',
        ])
        if trace.runtime_refs:
            lines.append('- Runtime Refs:')
            lines.extend(f'  - {item}' for item in trace.runtime_refs)
        lines.extend(['', '## Provenance Layers', ''])
        for layer in trace.layers:
            lines.extend([
                f'### {layer.label}',
                '',
            ])
            if not layer.targets:
                lines.append('- No downstream witness targets were found for this layer.')
                lines.append('')
                continue
            for target in layer.targets:
                lines.extend([
                    f'- {target.label}: {target.target_ref}',
                    f'  - Target Kind: {target.target_kind}',
                    f'  - Relative Path: {target.relative_path}',
                    f'  - Exists: {"YES" if target.exists else "NO"}',
                    f'  - Anchor Kind: {target.anchor_kind or "NONE"}',
                    f'  - Anchor Fragment: {target.anchor_fragment or "NONE"}',
                ])
            lines.append('')
        lines.extend([
            '## Boundary',
            '',
            '- This packet is a read-only lineage trace over downstream runtime-report witness material.',
            '- It can follow one receipt across artifact, reflection, aggregation, visibility, navigation, browser, and crosslink surfaces when those files exist.',
            '- It does not become kernel truth, doctrine, route authority, or runtime authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_json(self, trace: RuntimeReportProvenanceTrace) -> str:
        payload = {
            'provenance_kind': 'RUNTIME_REPORT_PROVENANCE_TRACE',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': trace.generated_at,
            'packet_index_path': trace.packet_index_path,
            'selector': {
                'entry_index': trace.selector.entry_index,
                'packet_index_pointer': trace.selector.packet_index_pointer,
                'source_ref': trace.selector.source_ref,
                'trigger_event': trace.selector.trigger_event,
                'artifact_kind': trace.selector.artifact_kind,
            },
            'receipt': {
                'entry_index': trace.entry_index,
                'packet_index_pointer': trace.packet_index_pointer,
                'trigger_event': trace.trigger_event,
                'artifact_kind': trace.artifact_kind,
                'source_ref': trace.source_ref,
                'source_family': trace.source_family,
                'reason': trace.reason,
                'runtime_refs': list(trace.runtime_refs),
            },
            'layers': [
                {
                    'layer_name': layer.layer_name,
                    'label': layer.label,
                    'targets': [
                        {
                            'target_kind': target.target_kind,
                            'label': target.label,
                            'relative_path': target.relative_path,
                            'target_ref': target.target_ref,
                            'exists': target.exists,
                            'anchor_kind': target.anchor_kind,
                            'anchor_fragment': target.anchor_fragment,
                        }
                        for target in layer.targets
                    ],
                }
                for layer in trace.layers
            ],
            'boundary': [
                'Read-only lineage trace over downstream runtime-report witness material.',
                'Follows artifact, reflection, aggregation, visibility, navigation, browser, and crosslink surfaces when available.',
                'Does not become kernel truth, doctrine, route authority, or runtime authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_trace_packet(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportProvenanceSelector,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        provenance_dir: str | Path = 'ION/05_context/runtime_reports/governance/provenance',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportProvenanceWriteResult:
        root = Path(workspace_root).resolve()
        trace = self.trace_receipt(
            root,
            selector,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
            navigation_dir=navigation_dir,
            browser_dir=browser_dir,
            crosslinks_dir=crosslinks_dir,
            created_at=created_at,
        )
        relative_dir = Path(provenance_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stem = output_stem or _default_stem(trace, trace.generated_at)
        markdown_relative = relative_dir / f'{stem}.md'
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        markdown_resolved.write_text(
            self.render_markdown(trace, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        json_relative = relative_dir / f'{stem}.json'
        json_resolved = _resolve_relative_file(root, json_relative)
        json_resolved.write_text(self.render_json(trace), encoding='utf-8')
        return RuntimeReportProvenanceWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            trace=trace,
        )

    def _resolve_entry(
        self,
        workspace_root: str | Path,
        selector: RuntimeReportProvenanceSelector,
        *,
        packet_index_path: str | Path,
        operator_dashboard_path: str | Path,
    ) -> RuntimeReportNavigationEntry:
        entry_index = selector.entry_index
        if selector.packet_index_pointer:
            entry_index = _entry_index_from_pointer(selector.packet_index_pointer)
        if entry_index is None and not selector.source_ref and not selector.trigger_event and not selector.artifact_kind:
            raise KernelRuntimeReportProvenanceError('A provenance selector must identify at least one receipt.')

        query = RuntimeReportNavigationQuery(
            artifact_kind=selector.artifact_kind,
            trigger_event=selector.trigger_event,
            source_ref_contains=selector.source_ref,
            limit=10_000,
        )
        result = self._navigator.query_entries(
            workspace_root,
            query,
            packet_index_path=packet_index_path,
            operator_dashboard_path=operator_dashboard_path,
        )
        matches = [
            entry
            for entry in result.entries
            if _entry_matches(
                entry,
                entry_index=entry_index,
                source_ref=selector.source_ref,
                trigger_event=selector.trigger_event,
                artifact_kind=selector.artifact_kind,
            )
        ]
        if not matches:
            raise KernelRuntimeReportProvenanceError('No runtime-report receipt matched the provided provenance selector.')
        if len(matches) > 1:
            raise KernelRuntimeReportProvenanceError('The provenance selector matched multiple runtime-report receipts.')
        return matches[0]

    def _find_navigation_packets(
        self,
        root: Path,
        entry: RuntimeReportNavigationEntry,
        *,
        navigation_dir: str | Path,
    ) -> tuple[RuntimeReportProvenanceTarget, ...]:
        relative_dir = Path(navigation_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        if not resolved_dir.exists():
            return ()
        heading = f'### {entry.trigger_event} — {entry.source_ref}'
        targets: list[RuntimeReportProvenanceTarget] = []
        for path in sorted(resolved_dir.glob('*.md')):
            text = path.read_text(encoding='utf-8')
            if 'navigation_kind: RUNTIME_REPORT_NAVIGATION_PACKET' not in text:
                continue
            if heading not in text:
                continue
            targets.append(
                RuntimeReportProvenanceTarget(
                    target_kind='NAVIGATION_PACKET',
                    label=f'Navigation Packet ({path.name})',
                    relative_path=str(path.relative_to(root)),
                    exists=True,
                )
            )
        return tuple(targets)

    def _find_browser_bundles(
        self,
        root: Path,
        entry: RuntimeReportNavigationEntry,
        *,
        browser_dir: str | Path,
    ) -> tuple[RuntimeReportProvenanceTarget, ...]:
        relative_dir = Path(browser_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        if not resolved_dir.exists():
            return ()
        targets: list[RuntimeReportProvenanceTarget] = []
        seen: set[str] = set()
        for json_path in sorted(resolved_dir.glob('*.json')):
            payload = _load_json_object(json_path)
            if payload.get('browser_kind') != 'RUNTIME_REPORT_READ_ONLY_BROWSER':
                continue
            entries = payload.get('entries')
            if not isinstance(entries, list):
                continue
            if not any(_mapping_matches(item, entry) for item in entries if isinstance(item, dict)):
                continue
            stem = json_path.with_suffix('')
            for suffix, kind, label in (
                ('.md', 'BROWSER_MARKDOWN', 'Browser Markdown'),
                ('.html', 'BROWSER_HTML', 'Browser HTML'),
                ('.json', 'BROWSER_JSON', 'Browser JSON'),
            ):
                candidate = stem.with_suffix(suffix)
                if not candidate.exists():
                    continue
                relative_path = str(candidate.relative_to(root))
                if relative_path in seen:
                    continue
                seen.add(relative_path)
                targets.append(
                    RuntimeReportProvenanceTarget(
                        target_kind=kind,
                        label=f'{label} ({candidate.name})',
                        relative_path=relative_path,
                        exists=True,
                    )
                )
        return tuple(targets)

    def _find_crosslink_packets(
        self,
        root: Path,
        entry: RuntimeReportNavigationEntry,
        *,
        crosslinks_dir: str | Path,
    ) -> tuple[RuntimeReportProvenanceTarget, ...]:
        relative_dir = Path(crosslinks_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        if not resolved_dir.exists():
            return ()
        targets: list[RuntimeReportProvenanceTarget] = []
        seen: set[str] = set()
        for json_path in sorted(resolved_dir.glob('*.json')):
            payload = _load_json_object(json_path)
            if payload.get('crosslink_kind') != 'RUNTIME_REPORT_CROSSLINK_PACKET':
                continue
            entries = payload.get('entries')
            if not isinstance(entries, list):
                continue
            if not any(_mapping_matches(item, entry) for item in entries if isinstance(item, dict)):
                continue
            stem = json_path.with_suffix('')
            for suffix, kind, label in (
                ('.md', 'CROSSLINK_MARKDOWN', 'Crosslink Markdown'),
                ('.json', 'CROSSLINK_JSON', 'Crosslink JSON'),
            ):
                candidate = stem.with_suffix(suffix)
                if not candidate.exists():
                    continue
                relative_path = str(candidate.relative_to(root))
                if relative_path in seen:
                    continue
                seen.add(relative_path)
                targets.append(
                    RuntimeReportProvenanceTarget(
                        target_kind=kind,
                        label=f'{label} ({candidate.name})',
                        relative_path=relative_path,
                        exists=True,
                    )
                )
        return tuple(targets)


IonRuntimeReportProvenanceTracer = KernelRuntimeReportProvenanceTracer


def _make_target(
    root: Path,
    target_kind: str,
    label: str,
    relative_path: str | None,
    *,
    anchor_kind: str | None = None,
    anchor_fragment: str | None = None,
) -> RuntimeReportProvenanceTarget | None:
    if not relative_path:
        return None
    resolved = _resolve_relative_file(root, Path(relative_path))
    return RuntimeReportProvenanceTarget(
        target_kind=target_kind,
        label=label,
        relative_path=relative_path,
        exists=resolved.exists(),
        anchor_kind=anchor_kind,
        anchor_fragment=anchor_fragment,
    )


def _mapping_matches(item: dict[str, object], entry: RuntimeReportNavigationEntry) -> bool:
    entry_index = item.get('entry_index')
    if isinstance(entry_index, int) and entry_index == entry.entry_index:
        return True
    return (
        item.get('trigger_event') == entry.trigger_event
        and item.get('artifact_kind') == entry.artifact_kind
        and item.get('source_ref') == entry.source_ref
    )


def _entry_matches(
    entry: RuntimeReportNavigationEntry,
    *,
    entry_index: int | None,
    source_ref: str | None,
    trigger_event: str | None,
    artifact_kind: str | None,
) -> bool:
    if entry_index is not None and entry.entry_index != entry_index:
        return False
    if source_ref is not None and entry.source_ref != source_ref:
        return False
    if trigger_event is not None and entry.trigger_event != trigger_event:
        return False
    if artifact_kind is not None and entry.artifact_kind != artifact_kind:
        return False
    return True


def _entry_index_from_pointer(pointer: str) -> int:
    match = re.fullmatch(r'#/entries/(\d+)', pointer.strip())
    if match is None:
        raise KernelRuntimeReportProvenanceError(f'Unsupported packet-index pointer: {pointer}')
    return int(match.group(1)) + 1


def _load_json_object(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        raise KernelRuntimeReportProvenanceError(f'Expected JSON object in {path}')
    return payload


def _default_stem(trace: RuntimeReportProvenanceTrace, created_at: str) -> str:
    stamp = re.sub(r'[^0-9]', '', created_at)[:14]
    safe_event = _safe(trace.trigger_event)
    safe_source = _safe(trace.source_ref)
    return f'{safe_event}__{safe_source}__runtime_provenance_{stamp}'


def _safe(value: str) -> str:
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportProvenanceError(f'Absolute output paths are not allowed: {relative_path}')
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportProvenanceError(f'Output path escapes workspace root: {relative_path}') from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
