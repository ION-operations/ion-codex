"""Named read-only digest profiles over downstream runtime-report family summaries.

This module defines bounded selection profiles for recurring H1 operator digests.
Profiles are named downstream selection sets, not authority surfaces. Rendering a
profile-backed digest delegates into the existing operator-digest pipeline rather
than bypassing family summaries or digest construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable, Sequence

from .runtime_report_operator_digest import (
    KernelRuntimeReportOperatorDigestError,
    KernelRuntimeReportOperatorDigester,
    RuntimeReportOperatorDigest,
    RuntimeReportOperatorDigestWriteResult,
)
from .runtime_report_temporal_provenance import RuntimeReportTemporalSelector


class KernelRuntimeReportDigestProfileError(Exception):
    """Raised when a digest-profile request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportDigestProfileSelector:
    label: str
    selector: RuntimeReportTemporalSelector


@dataclass(frozen=True)
class RuntimeReportOperatorDigestProfile:
    profile_name: str
    description: str
    tags: tuple[str, ...]
    selectors: tuple[RuntimeReportDigestProfileSelector, ...]
    read_only_mode: bool = True


@dataclass(frozen=True)
class RuntimeReportDigestProfileWriteResult:
    markdown_path: str
    json_path: str
    profile: RuntimeReportOperatorDigestProfile


@dataclass(frozen=True)
class RuntimeReportDigestProfileDigestWriteResult:
    profile_name: str
    digest_markdown_path: str
    digest_json_path: str
    digest: RuntimeReportOperatorDigest


class KernelRuntimeReportDigestProfiler:
    """Manage named read-only digest profiles and render profile-backed digests."""

    def __init__(
        self,
        *,
        digester: KernelRuntimeReportOperatorDigester | None = None,
    ) -> None:
        self._digester = digester or KernelRuntimeReportOperatorDigester()

    def build_profile(
        self,
        profile_name: str,
        selectors: Sequence[RuntimeReportDigestProfileSelector],
        *,
        description: str = '',
        tags: Sequence[str] = (),
    ) -> RuntimeReportOperatorDigestProfile:
        normalized_name = (profile_name or '').strip()
        if not normalized_name:
            raise KernelRuntimeReportDigestProfileError('Digest profile requires a non-empty profile name.')
        normalized_selectors = tuple(selectors)
        if not normalized_selectors:
            raise KernelRuntimeReportDigestProfileError('Digest profile requires at least one selector.')
        for entry in normalized_selectors:
            if not entry.label.strip():
                raise KernelRuntimeReportDigestProfileError('Digest profile selector labels must be non-empty.')
        return RuntimeReportOperatorDigestProfile(
            profile_name=normalized_name,
            description=description.strip(),
            tags=_sorted_unique(tags),
            selectors=normalized_selectors,
            read_only_mode=True,
        )

    def render_profile_markdown(
        self,
        profile: RuntimeReportOperatorDigestProfile,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'profile_kind: RUNTIME_REPORT_OPERATOR_DIGEST_PROFILE',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'profile_name: {profile.profile_name}',
            f'selector_count: {len(profile.selectors)}',
        ]
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            f'# Runtime Report Digest Profile — {profile.profile_name}',
            '',
            'This profile is a bounded named selector-set for recurring operator digest rendering.',
            '',
        ])
        if profile.description:
            lines.extend([
                '## Description',
                '',
                profile.description,
                '',
            ])
        lines.extend([
            '## Profile Scope',
            '',
            f'- Selector Count: {len(profile.selectors)}',
            f'- Tags: {", ".join(profile.tags) if profile.tags else "NONE"}',
            '',
            '## Selectors',
            '',
        ])
        for index, entry in enumerate(profile.selectors, start=1):
            selector = entry.selector
            lines.extend([
                f'### {index}. {entry.label}',
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
            '- This profile is a read-only named selector-set for recurring digest rendering.',
            '- It remains downstream from runtime-report witness surfaces and from the digest packets rendered through it.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, or profile authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_profile_json(self, profile: RuntimeReportOperatorDigestProfile) -> str:
        payload = {
            'profile_kind': 'RUNTIME_REPORT_OPERATOR_DIGEST_PROFILE',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'profile_name': profile.profile_name,
            'description': profile.description,
            'tags': list(profile.tags),
            'selector_count': len(profile.selectors),
            'selectors': [
                {
                    'label': entry.label,
                    'selector': {
                        'source_ref': entry.selector.source_ref,
                        'source_ref_contains': entry.selector.source_ref_contains,
                        'trigger_event': entry.selector.trigger_event,
                        'artifact_kind': entry.selector.artifact_kind,
                        'source_family': entry.selector.source_family,
                        'limit': entry.selector.limit,
                    },
                }
                for entry in profile.selectors
            ],
            'boundary': [
                'Read-only named selector-set for recurring digest rendering.',
                'Remains downstream from runtime-report witness surfaces and from the digest packets rendered through it.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, or profile authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_profile_definition(
        self,
        workspace_root: str | Path,
        profile: RuntimeReportOperatorDigestProfile,
        *,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        output_stem: str | None = None,
    ) -> RuntimeReportDigestProfileWriteResult:
        root = Path(workspace_root).resolve()
        relative_dir = Path(profiles_dir)
        resolved_dir = _resolve_relative_file(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stem = output_stem or _safe(profile.profile_name)
        markdown_relative = relative_dir / f'{stem}.md'
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        markdown_resolved.write_text(
            self.render_profile_markdown(profile, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        json_relative = relative_dir / f'{stem}.json'
        json_resolved = _resolve_relative_file(root, json_relative)
        json_resolved.write_text(self.render_profile_json(profile), encoding='utf-8')
        return RuntimeReportDigestProfileWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            profile=profile,
        )

    def load_profile(
        self,
        workspace_root: str | Path,
        *,
        profile_name: str | None = None,
        profile_path: str | Path | None = None,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
    ) -> RuntimeReportOperatorDigestProfile:
        root = Path(workspace_root).resolve()
        if bool(profile_name) == bool(profile_path):
            raise KernelRuntimeReportDigestProfileError(
                'Provide exactly one of profile_name or profile_path when loading a digest profile.'
            )
        if profile_name:
            candidate = Path(profiles_dir) / f'{_safe(profile_name)}.json'
        else:
            candidate = Path(profile_path)  # type: ignore[arg-type]
        resolved = _resolve_relative_file(root, candidate)
        if not resolved.exists():
            raise KernelRuntimeReportDigestProfileError(f'Digest profile not found: {candidate}')
        try:
            payload = json.loads(resolved.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            raise KernelRuntimeReportDigestProfileError(
                f'Digest profile JSON is invalid: {candidate}'
            ) from exc
        selectors_payload = payload.get('selectors') or []
        selectors: list[RuntimeReportDigestProfileSelector] = []
        for item in selectors_payload:
            selector_payload = item.get('selector') or {}
            selectors.append(
                RuntimeReportDigestProfileSelector(
                    label=str(item.get('label') or '').strip(),
                    selector=RuntimeReportTemporalSelector(
                        source_ref=selector_payload.get('source_ref'),
                        source_ref_contains=selector_payload.get('source_ref_contains'),
                        trigger_event=selector_payload.get('trigger_event'),
                        artifact_kind=selector_payload.get('artifact_kind'),
                        source_family=selector_payload.get('source_family'),
                        limit=selector_payload.get('limit'),
                    ),
                )
            )
        return self.build_profile(
            str(payload.get('profile_name') or profile_name or Path(candidate).stem),
            selectors,
            description=str(payload.get('description') or ''),
            tags=tuple(payload.get('tags') or ()),
        )

    def build_digest_from_profile(
        self,
        workspace_root: str | Path,
        profile: RuntimeReportOperatorDigestProfile,
        *,
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        created_at: str | None = None,
    ) -> RuntimeReportOperatorDigest:
        selectors = [entry.selector for entry in profile.selectors]
        try:
            return self._digester.build_digest(
                workspace_root,
                selectors,
                packet_index_path=packet_index_path,
                operator_dashboard_path=operator_dashboard_path,
                navigation_dir=navigation_dir,
                browser_dir=browser_dir,
                crosslinks_dir=crosslinks_dir,
                created_at=created_at,
            )
        except KernelRuntimeReportOperatorDigestError as exc:
            raise KernelRuntimeReportDigestProfileError(str(exc)) from exc

    def write_profile_digest_packet(
        self,
        workspace_root: str | Path,
        *,
        profile: RuntimeReportOperatorDigestProfile | None = None,
        profile_name: str | None = None,
        profile_path: str | Path | None = None,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        packet_index_path: str | Path = 'ION/05_context/runtime_reports/governance/indexes/runtime_report_packet_index.json',
        operator_dashboard_path: str | Path = 'ION/05_context/runtime_reports/governance/dashboards/runtime_report_operator_dashboard.md',
        navigation_dir: str | Path = 'ION/05_context/runtime_reports/governance/navigation',
        browser_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser',
        crosslinks_dir: str | Path = 'ION/05_context/runtime_reports/governance/browser/crosslinks',
        digests_dir: str | Path = 'ION/05_context/runtime_reports/governance/digests/profiles',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportDigestProfileDigestWriteResult:
        active_profile = profile or self.load_profile(
            workspace_root,
            profile_name=profile_name,
            profile_path=profile_path,
            profiles_dir=profiles_dir,
        )
        stamp = re.sub(r'[^0-9]', '', created_at or _iso_now())[:14]
        stem = output_stem or f'{_safe(active_profile.profile_name)}__runtime_operator_digest_{stamp}'
        try:
            written: RuntimeReportOperatorDigestWriteResult = self._digester.write_operator_digest_packet(
                workspace_root,
                [entry.selector for entry in active_profile.selectors],
                packet_index_path=packet_index_path,
                operator_dashboard_path=operator_dashboard_path,
                navigation_dir=navigation_dir,
                browser_dir=browser_dir,
                crosslinks_dir=crosslinks_dir,
                digests_dir=digests_dir,
                output_stem=stem,
                created_at=created_at,
            )
        except KernelRuntimeReportOperatorDigestError as exc:
            raise KernelRuntimeReportDigestProfileError(str(exc)) from exc
        return RuntimeReportDigestProfileDigestWriteResult(
            profile_name=active_profile.profile_name,
            digest_markdown_path=written.markdown_path,
            digest_json_path=written.json_path,
            digest=written.digest,
        )


IonRuntimeReportDigestProfiler = KernelRuntimeReportDigestProfiler


def _sorted_unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({value for value in values if value}))


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime-profile'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime-profile'


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportDigestProfileError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportDigestProfileError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
