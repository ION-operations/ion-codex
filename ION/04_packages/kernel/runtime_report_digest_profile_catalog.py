"""Read-only catalog and index views over named runtime-report digest profiles.

This module provides a bounded browse/list layer over H2 digest-profile definitions.
It loads previously written profile definitions, summarizes them into read-only catalog
entries, and can emit governed catalog packets. It remains explicitly downstream from
profile definitions and from the digest packets rendered through them.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Iterable, Sequence

from .runtime_report_digest_profiles import (
    KernelRuntimeReportDigestProfileError,
    KernelRuntimeReportDigestProfiler,
    RuntimeReportOperatorDigestProfile,
)


class KernelRuntimeReportDigestProfileCatalogError(Exception):
    """Raised when one digest-profile catalog request cannot be completed lawfully."""


@dataclass(frozen=True)
class RuntimeReportDigestProfileCatalogQuery:
    profile_name_contains: str | None = None
    tag: str | None = None
    selector_label_contains: str | None = None
    description_contains: str | None = None
    limit: int | None = None


@dataclass(frozen=True)
class RuntimeReportDigestProfileCatalogEntry:
    profile_name: str
    description: str
    tags: tuple[str, ...]
    selector_count: int
    selector_labels: tuple[str, ...]
    markdown_path: str | None
    json_path: str


@dataclass(frozen=True)
class RuntimeReportDigestProfileCatalog:
    generated_at: str
    read_only_mode: bool
    profiles_dir: str
    total_profiles: int
    matched_count: int
    query: RuntimeReportDigestProfileCatalogQuery
    entries: tuple[RuntimeReportDigestProfileCatalogEntry, ...]


@dataclass(frozen=True)
class RuntimeReportDigestProfileCatalogWriteResult:
    markdown_path: str
    json_path: str
    catalog: RuntimeReportDigestProfileCatalog


class KernelRuntimeReportDigestProfileCatalog:
    """List, summarize, and packetize named digest-profile definitions."""

    def __init__(
        self,
        *,
        profiler: KernelRuntimeReportDigestProfiler | None = None,
    ) -> None:
        self._profiler = profiler or KernelRuntimeReportDigestProfiler()

    def query_catalog(
        self,
        workspace_root: str | Path,
        query: RuntimeReportDigestProfileCatalogQuery | None = None,
        *,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        created_at: str | None = None,
    ) -> RuntimeReportDigestProfileCatalog:
        root = Path(workspace_root).resolve()
        relative_dir = Path(profiles_dir)
        resolved_dir = _resolve_relative_dir(root, relative_dir)
        entries = self._load_entries(root, relative_dir, resolved_dir)
        active_query = query or RuntimeReportDigestProfileCatalogQuery()
        matched = tuple(self._filter_entries(entries, active_query))
        if active_query.limit is not None:
            if active_query.limit <= 0:
                raise KernelRuntimeReportDigestProfileCatalogError('Catalog query limit must be positive when provided.')
            matched = matched[: active_query.limit]
        return RuntimeReportDigestProfileCatalog(
            generated_at=created_at or _iso_now(),
            read_only_mode=True,
            profiles_dir=str(relative_dir),
            total_profiles=len(entries),
            matched_count=len(matched),
            query=active_query,
            entries=matched,
        )

    def render_catalog_markdown(
        self,
        catalog: RuntimeReportDigestProfileCatalog,
        *,
        output_relative_path: str | Path | None = None,
    ) -> str:
        lines = [
            '---',
            'catalog_kind: RUNTIME_REPORT_DIGEST_PROFILE_CATALOG',
            'authority_class: GENERATED_STATE',
            'interface_mode: READ_ONLY',
            f'generated_at: {catalog.generated_at}',
            f'profiles_dir: {catalog.profiles_dir}',
            f'total_profiles: {catalog.total_profiles}',
            f'matched_count: {catalog.matched_count}',
        ]
        if catalog.query.profile_name_contains is not None:
            lines.append(f'profile_name_contains: {catalog.query.profile_name_contains}')
        if catalog.query.tag is not None:
            lines.append(f'tag: {catalog.query.tag}')
        if catalog.query.selector_label_contains is not None:
            lines.append(f'selector_label_contains: {catalog.query.selector_label_contains}')
        if catalog.query.description_contains is not None:
            lines.append(f'description_contains: {catalog.query.description_contains}')
        if catalog.query.limit is not None:
            lines.append(f'catalog_limit: {catalog.query.limit}')
        if output_relative_path is not None:
            lines.append(f'output_path: {output_relative_path}')
        lines.extend([
            '---',
            '',
            '# Runtime Report Digest Profile Catalog',
            '',
            'This packet is a bounded read-only catalog over named runtime-report digest profiles.',
            '',
            '## Catalog Scope',
            '',
            f'- Profiles Directory: {catalog.profiles_dir}',
            f'- Total Profiles: {catalog.total_profiles}',
            f'- Matched Profiles: {catalog.matched_count}',
            f'- Profile Name Contains: {catalog.query.profile_name_contains or "NONE"}',
            f'- Tag: {catalog.query.tag or "NONE"}',
            f'- Selector Label Contains: {catalog.query.selector_label_contains or "NONE"}',
            f'- Description Contains: {catalog.query.description_contains or "NONE"}',
            f'- Limit: {catalog.query.limit if catalog.query.limit is not None else "NONE"}',
            '',
            '## Catalog Entries',
            '',
        ])
        if not catalog.entries:
            lines.extend([
                'No named digest profiles matched the read-only catalog query.',
                '',
            ])
        for index, entry in enumerate(catalog.entries, start=1):
            lines.extend([
                f'### {index}. {entry.profile_name}',
                '',
                f'- Selector Count: {entry.selector_count}',
                f'- Tags: {", ".join(entry.tags) if entry.tags else "NONE"}',
                f'- Description: {entry.description or "NONE"}',
                f'- Definition Markdown Path: {entry.markdown_path or "NONE"}',
                f'- Definition JSON Path: {entry.json_path}',
            ])
            if entry.selector_labels:
                lines.append('- Selector Labels:')
                lines.extend(f'  - {label}' for label in entry.selector_labels)
            else:
                lines.append('- Selector Labels: NONE')
            lines.append('')
        lines.extend([
            '## Boundary',
            '',
            '- This packet is a read-only listing and summary surface over digest-profile definitions.',
            '- It remains downstream from digest profiles and from the digests rendered through them.',
            '- It does not become kernel truth, doctrine, route authority, runtime authority, or catalog authority.',
            '',
        ])
        return '\n'.join(lines)

    def render_catalog_json(self, catalog: RuntimeReportDigestProfileCatalog) -> str:
        payload = {
            'catalog_kind': 'RUNTIME_REPORT_DIGEST_PROFILE_CATALOG',
            'authority_class': 'GENERATED_STATE',
            'interface_mode': 'READ_ONLY',
            'generated_at': catalog.generated_at,
            'profiles_dir': catalog.profiles_dir,
            'total_profiles': catalog.total_profiles,
            'matched_count': catalog.matched_count,
            'query': {
                'profile_name_contains': catalog.query.profile_name_contains,
                'tag': catalog.query.tag,
                'selector_label_contains': catalog.query.selector_label_contains,
                'description_contains': catalog.query.description_contains,
                'limit': catalog.query.limit,
            },
            'entries': [
                {
                    'profile_name': entry.profile_name,
                    'description': entry.description,
                    'tags': list(entry.tags),
                    'selector_count': entry.selector_count,
                    'selector_labels': list(entry.selector_labels),
                    'markdown_path': entry.markdown_path,
                    'json_path': entry.json_path,
                }
                for entry in catalog.entries
            ],
            'boundary': [
                'Read-only listing and summary surface over digest-profile definitions.',
                'Remains downstream from digest profiles and from the digests rendered through them.',
                'Does not become kernel truth, doctrine, route authority, runtime authority, or catalog authority.',
            ],
        }
        return json.dumps(payload, indent=2, sort_keys=True) + '\n'

    def write_catalog_packet(
        self,
        workspace_root: str | Path,
        query: RuntimeReportDigestProfileCatalogQuery | None = None,
        *,
        profiles_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles',
        catalogs_dir: str | Path = 'ION/05_context/runtime_reports/governance/digest_profiles/catalog',
        output_stem: str | None = None,
        created_at: str | None = None,
    ) -> RuntimeReportDigestProfileCatalogWriteResult:
        root = Path(workspace_root).resolve()
        active_query = query or RuntimeReportDigestProfileCatalogQuery()
        catalog = self.query_catalog(
            root,
            active_query,
            profiles_dir=profiles_dir,
            created_at=created_at,
        )
        relative_dir = Path(catalogs_dir)
        resolved_dir = _resolve_relative_dir(root, relative_dir)
        resolved_dir.mkdir(parents=True, exist_ok=True)
        stamp = re.sub(r'[^0-9]', '', catalog.generated_at)[:14]
        stem = output_stem or f'runtime_report_digest_profile_catalog_{stamp}'
        markdown_relative = relative_dir / f'{stem}.md'
        markdown_resolved = _resolve_relative_file(root, markdown_relative)
        markdown_resolved.write_text(
            self.render_catalog_markdown(catalog, output_relative_path=markdown_relative),
            encoding='utf-8',
        )
        json_relative = relative_dir / f'{stem}.json'
        json_resolved = _resolve_relative_file(root, json_relative)
        json_resolved.write_text(self.render_catalog_json(catalog), encoding='utf-8')
        return RuntimeReportDigestProfileCatalogWriteResult(
            markdown_path=str(markdown_relative),
            json_path=str(json_relative),
            catalog=catalog,
        )

    def _load_entries(
        self,
        root: Path,
        relative_dir: Path,
        resolved_dir: Path,
    ) -> tuple[RuntimeReportDigestProfileCatalogEntry, ...]:
        if not resolved_dir.exists():
            return ()
        entries: list[RuntimeReportDigestProfileCatalogEntry] = []
        for json_path in sorted(resolved_dir.glob('*.json')):
            relative_json = json_path.relative_to(root)
            try:
                payload = json.loads(json_path.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                continue
            if payload.get('profile_kind') != 'RUNTIME_REPORT_OPERATOR_DIGEST_PROFILE':
                continue
            try:
                profile = self._profiler.load_profile(root, profile_path=relative_json)
            except KernelRuntimeReportDigestProfileError as exc:
                raise KernelRuntimeReportDigestProfileCatalogError(str(exc)) from exc
            markdown_candidate = relative_dir / f'{_safe(profile.profile_name)}.md'
            markdown_path = str(markdown_candidate) if (root / markdown_candidate).exists() else None
            entries.append(self._entry_from_profile(profile, json_path=str(relative_json), markdown_path=markdown_path))
        return tuple(entries)

    def _filter_entries(
        self,
        entries: Sequence[RuntimeReportDigestProfileCatalogEntry],
        query: RuntimeReportDigestProfileCatalogQuery,
    ) -> Iterable[RuntimeReportDigestProfileCatalogEntry]:
        profile_name_contains = _normalized(query.profile_name_contains)
        tag = _normalized(query.tag)
        selector_label_contains = _normalized(query.selector_label_contains)
        description_contains = _normalized(query.description_contains)
        for entry in entries:
            if profile_name_contains and profile_name_contains not in entry.profile_name.lower():
                continue
            if tag and tag not in {item.lower() for item in entry.tags}:
                continue
            if selector_label_contains and not any(selector_label_contains in label.lower() for label in entry.selector_labels):
                continue
            if description_contains and description_contains not in entry.description.lower():
                continue
            yield entry

    def _entry_from_profile(
        self,
        profile: RuntimeReportOperatorDigestProfile,
        *,
        json_path: str,
        markdown_path: str | None,
    ) -> RuntimeReportDigestProfileCatalogEntry:
        return RuntimeReportDigestProfileCatalogEntry(
            profile_name=profile.profile_name,
            description=profile.description,
            tags=profile.tags,
            selector_count=len(profile.selectors),
            selector_labels=tuple(entry.label for entry in profile.selectors),
            markdown_path=markdown_path,
            json_path=json_path,
        )


IonRuntimeReportDigestProfileCatalog = KernelRuntimeReportDigestProfileCatalog


def _normalized(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip().lower()
    return cleaned or None


def _safe(value: str | None) -> str:
    if not value:
        return 'runtime-profile'
    safe = re.sub(r'[^0-9A-Za-z._-]+', '-', value).strip('-._')
    return safe or 'runtime-profile'


def _resolve_relative_dir(root: Path, relative_path: Path) -> Path:
    resolved = _resolve_relative_file(root, relative_path)
    return resolved


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRuntimeReportDigestProfileCatalogError(
            f'Absolute output paths are not allowed: {relative_path}'
        )
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelRuntimeReportDigestProfileCatalogError(
            f'Output path escapes workspace root: {relative_path}'
        ) from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
