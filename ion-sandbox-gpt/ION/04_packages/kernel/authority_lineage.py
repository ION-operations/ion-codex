"""Surface-specific authority lineage resolution and stale-name auditing.

This module preserves older role names as lineage evidence while resolving stale
surface aliases into the current working authority for bounded live entry paths.
It stays intentionally narrow: bootstrap ingress, explicit continuation roles,
and operator-facing reporting surfaces.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from .name_lineage import (
    KernelNameLineageManager,
    NameIngressSurface,
    NameResolutionDecision,
    RecordedNameResolution,
)

REGISTRY_RELATIVE = Path("ION/03_registry/authority_lineage_registry.json")


AUTHORITY_SURFACE_TO_NAME_SURFACE: dict[str, NameIngressSurface] = {
    "bootstrap_packet_agent": NameIngressSurface.BOOTSTRAP_PACKET,
    "bootstrap_blocked_escalation": NameIngressSurface.BOOTSTRAP_PACKET,
    "runtime_status_report_from": NameIngressSurface.LIVE_AUTHORITY,
    "continuation_target_executor": NameIngressSurface.LIVE_AUTHORITY,
}


class KernelAuthorityLineageError(Exception):
    """Raised when authority lineage resolution or audit cannot complete lawfully."""


@dataclass(frozen=True)
class AuthorityResolution:
    surface: str
    requested_name: str | None
    resolved_name: str
    status: str
    warning: str | None = None

    @property
    def changed(self) -> bool:
        return self.requested_name is not None and self.requested_name != self.resolved_name


@dataclass(frozen=True)
class AuthorityOverrideResult:
    requested_name: str | None
    resolved_name: str | None
    warnings: tuple[str, ...] = ()
    receipt_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuthorityAuditFinding:
    surface: str
    path: str
    line_number: int
    matched_name: str
    resolves_to: str
    severity: str
    line_text: str


@dataclass(frozen=True)
class AuthorityNameRecord:
    name: str
    status: str
    routes_to: str | None
    historical_summary: tuple[str, ...]
    routes_from_surfaces: tuple[str, ...]


@dataclass(frozen=True)
class AuthoritySurfaceRecord:
    surface: str
    current_authority: str
    route_aliases: dict[str, str]
    description: str | None


@dataclass(frozen=True)
class AuthorityAuditReport:
    scan_paths: tuple[str, ...]
    findings: tuple[AuthorityAuditFinding, ...]


@dataclass(frozen=True)
class AuthorityRegistryAlignmentFinding:
    surface: str
    authority_name: str
    severity: str
    issue_code: str
    message: str


@dataclass(frozen=True)
class AuthorityRegistryAlignmentReport:
    findings: tuple[AuthorityRegistryAlignmentFinding, ...]


class KernelAuthorityLineageManager:
    """Load the registry, resolve surface-specific names, and audit active surfaces."""

    def load_registry(self, workspace_root: str | Path) -> dict[str, Any]:
        root = Path(workspace_root).resolve()
        candidates = [
            _join_relative_path(root, REGISTRY_RELATIVE),
            _join_relative_path(Path(__file__).resolve().parents[3], REGISTRY_RELATIVE),
        ]
        for path in candidates:
            if path.exists():
                return json.loads(path.read_text(encoding="utf-8"))
        raise KernelAuthorityLineageError(f"Authority lineage registry missing: {candidates[0]}")

    def current_authority(self, workspace_root: str | Path, surface: str) -> str:
        registry = self.load_registry(workspace_root)
        surface_record = _surface_record(registry, surface)
        current = surface_record.get("current_authority")
        if not isinstance(current, str) or not current.strip():
            raise KernelAuthorityLineageError(f"Surface {surface} is missing current_authority")
        return current.strip()

    def surface_names(self, workspace_root: str | Path) -> tuple[str, ...]:
        registry = self.load_registry(workspace_root)
        return tuple(sorted(str(name) for name in dict(registry.get("surfaces") or {}).keys()))

    def surface_record(self, workspace_root: str | Path, surface: str) -> AuthoritySurfaceRecord:
        registry = self.load_registry(workspace_root)
        record = _surface_record(registry, surface)
        return AuthoritySurfaceRecord(
            surface=surface,
            current_authority=self.current_authority(workspace_root, surface),
            route_aliases={
                str(key): str(value)
                for key, value in dict(record.get("route_aliases") or {}).items()
                if isinstance(key, str) and isinstance(value, str)
            },
            description=(None if record.get("description") is None else str(record.get("description"))),
        )

    def name_record(self, workspace_root: str | Path, name: str) -> AuthorityNameRecord:
        registry = self.load_registry(workspace_root)
        names = {str(key): value for key, value in dict(registry.get("names") or {}).items()}
        requested = name.strip()
        for candidate, payload in names.items():
            if candidate.casefold() != requested.casefold():
                continue
            routes_from_surfaces = tuple(
                sorted(
                    surface
                    for surface, record in dict(registry.get("surfaces") or {}).items()
                    if isinstance(record, dict) and requested in dict(record.get("route_aliases") or {})
                )
            )
            return AuthorityNameRecord(
                name=candidate,
                status=str(payload.get("status") or "UNKNOWN"),
                routes_to=(None if payload.get("routes_to") is None else str(payload.get("routes_to"))),
                historical_summary=tuple(str(item) for item in payload.get("historical_summary") or ()),
                routes_from_surfaces=routes_from_surfaces,
            )
        raise KernelAuthorityLineageError(f"Unknown authority name: {name}")

    def render_surface_record(self, record: AuthoritySurfaceRecord) -> dict[str, Any]:
        return {
            "surface": record.surface,
            "current_authority": record.current_authority,
            "route_aliases": dict(sorted(record.route_aliases.items())),
            "description": record.description,
        }

    def render_name_record(self, record: AuthorityNameRecord) -> dict[str, Any]:
        return {
            "name": record.name,
            "status": record.status,
            "routes_to": record.routes_to,
            "historical_summary": list(record.historical_summary),
            "routes_from_surfaces": list(record.routes_from_surfaces),
        }

    def resolve_authority(
        self,
        workspace_root: str | Path,
        surface: str,
        requested_name: str | None,
    ) -> AuthorityResolution:
        registry = self.load_registry(workspace_root)
        surface_record = _surface_record(registry, surface)
        current = self.current_authority(workspace_root, surface)
        route_aliases = {
            key.casefold(): (key, value)
            for key, value in dict(surface_record.get("route_aliases") or {}).items()
            if isinstance(key, str) and isinstance(value, str)
        }

        if requested_name is None or not requested_name.strip():
            return AuthorityResolution(
                surface=surface,
                requested_name=None,
                resolved_name=current,
                status="DEFAULT_CURRENT_AUTHORITY",
            )

        requested = requested_name.strip()
        if requested == current:
            return AuthorityResolution(
                surface=surface,
                requested_name=requested,
                resolved_name=current,
                status="CURRENT_AUTHORITY",
            )

        match = route_aliases.get(requested.casefold())
        if match is not None:
            _, resolved = match
            return AuthorityResolution(
                surface=surface,
                requested_name=requested,
                resolved_name=resolved,
                status="ROUTED_STALE_SURFACE_ALIAS",
                warning=(
                    f"{requested} is stale for surface {surface} and was routed to "
                    f"current authority {resolved}."
                ),
            )

        return AuthorityResolution(
            surface=surface,
            requested_name=requested,
            resolved_name=requested,
            status="UNMAPPED_EXPLICIT_NAME",
            warning=(
                f"{requested} is not mapped in the authority lineage registry for "
                f"surface {surface}; preserving explicit request without silent rewrite."
            ),
        )

    def record_resolution(
        self,
        workspace_root: str | Path,
        resolution: AuthorityResolution,
        *,
        created_at: str | None = None,
    ) -> RecordedNameResolution | None:
        if resolution.requested_name is None or resolution.status in {"DEFAULT_CURRENT_AUTHORITY", "CURRENT_AUTHORITY"}:
            return None
        name_surface = AUTHORITY_SURFACE_TO_NAME_SURFACE.get(resolution.surface, NameIngressSurface.LIVE_AUTHORITY)
        manager = KernelNameLineageManager()
        name_resolution = manager.resolve_name(resolution.requested_name, surface=name_surface)
        return manager.record_resolution(workspace_root, name_resolution, created_at=created_at)

    def audit_text(self, workspace_root: str | Path, relative_path: str, text: str) -> AuthorityAuditReport:
        registry = self.load_registry(workspace_root)
        findings = tuple(self._scan_text_for_findings(registry, relative_path, text))
        return AuthorityAuditReport(scan_paths=(relative_path,), findings=findings)

    def audit_active_surfaces(self, workspace_root: str | Path) -> AuthorityAuditReport:
        root = Path(workspace_root).resolve()
        registry = self.load_registry(root)
        scan_paths = tuple(str(item) for item in registry.get("active_surface_scan_paths") or ())
        findings: list[AuthorityAuditFinding] = []
        for relative_path in scan_paths:
            path = _resolve_relative_file(root, Path(relative_path))
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            findings.extend(self._scan_text_for_findings(registry, relative_path, text))
        return AuthorityAuditReport(scan_paths=scan_paths, findings=tuple(findings))

    def audit_registry_alignment(self, workspace_root: str | Path) -> AuthorityRegistryAlignmentReport:
        root = Path(workspace_root).resolve()
        registry = self.load_registry(root)
        name_manager = KernelNameLineageManager()
        findings: list[AuthorityRegistryAlignmentFinding] = []

        for surface, record in dict(registry.get("surfaces") or {}).items():
            current = str(record.get("current_authority") or "").strip()
            if not current:
                findings.append(
                    AuthorityRegistryAlignmentFinding(
                        surface=str(surface),
                        authority_name="",
                        severity="BLOCK",
                        issue_code="MISSING_CURRENT_AUTHORITY",
                        message=f"Surface {surface} is missing current_authority.",
                    )
                )
                continue
            current_resolution = name_manager.resolve_name(
                current,
                surface=NameIngressSurface.LIVE_AUTHORITY,
            )
            if not current_resolution.matched:
                findings.append(
                    AuthorityRegistryAlignmentFinding(
                        surface=str(surface),
                        authority_name=current,
                        severity="BLOCK",
                        issue_code="CURRENT_AUTHORITY_UNREGISTERED_IN_NAME_LINEAGE",
                        message=f"Surface {surface} current authority {current} is not registered in the name-lineage registry.",
                    )
                )
            elif current_resolution.decision is not NameResolutionDecision.ALLOW_AS_AUTHORITY:
                findings.append(
                    AuthorityRegistryAlignmentFinding(
                        surface=str(surface),
                        authority_name=current,
                        severity="BLOCK",
                        issue_code="CURRENT_AUTHORITY_NOT_LIVE_TRUE_NAME",
                        message=(
                            f"Surface {surface} current authority {current} does not resolve as a live true authority "
                            f"(decision={current_resolution.decision.value})."
                        ),
                    )
                )

            for alias, target in dict(record.get("route_aliases") or {}).items():
                alias_name = str(alias).strip()
                target_name = str(target).strip()
                alias_resolution = name_manager.resolve_name(
                    alias_name,
                    surface=NameIngressSurface.LIVE_AUTHORITY,
                )
                if not alias_resolution.matched:
                    findings.append(
                        AuthorityRegistryAlignmentFinding(
                            surface=str(surface),
                            authority_name=alias_name,
                            severity="BLOCK",
                            issue_code="ALIASED_NAME_UNREGISTERED_IN_NAME_LINEAGE",
                            message=f"Surface {surface} alias {alias_name} is not registered in the name-lineage registry.",
                        )
                    )
                    continue
                if not _alias_alignment_matches_target(alias_resolution, target_name):
                    if (
                        alias_resolution.decision is NameResolutionDecision.ALLOW_AS_AUTHORITY
                        and target_name == current
                    ):
                        findings.append(
                            AuthorityRegistryAlignmentFinding(
                                surface=str(surface),
                                authority_name=alias_name,
                                severity="INFO",
                                issue_code="SURFACE_SPECIALIZES_ACTIVE_SPECIALIST",
                                message=(
                                    f"Surface {surface} keeps {alias_name} as a live broader-role name but lawfully narrows this surface to {target_name}."
                                ),
                            )
                        )
                    else:
                        findings.append(
                            AuthorityRegistryAlignmentFinding(
                                surface=str(surface),
                                authority_name=alias_name,
                                severity="BLOCK",
                                issue_code="SURFACE_ROUTE_CONFLICTS_WITH_NAME_LINEAGE",
                                message=(
                                    f"Surface {surface} routes {alias_name} to {target_name}, but name-lineage resolution "
                                    f"yields decision={alias_resolution.decision.value}, current_true_name={alias_resolution.current_true_name}, "
                                    f"successor_candidates={list(alias_resolution.successor_candidates)}."
                                ),
                            )
                        )
                elif alias_resolution.decision is NameResolutionDecision.REQUIRES_EXPLICIT_TRUE_NAME:
                    findings.append(
                        AuthorityRegistryAlignmentFinding(
                            surface=str(surface),
                            authority_name=alias_name,
                            severity="INFO",
                            issue_code="SURFACE_SPECIALIZES_RETIRED_NAME",
                            message=(
                                f"Surface {surface} lawfully specializes retired or witness alias {alias_name} toward {target_name}."
                            ),
                        )
                    )

        return AuthorityRegistryAlignmentReport(findings=tuple(findings))

    def _scan_text_for_findings(
        self,
        registry: dict[str, Any],
        relative_path: str,
        text: str,
    ) -> list[AuthorityAuditFinding]:
        findings: list[AuthorityAuditFinding] = []
        surfaces = dict(registry.get("surfaces") or {})
        lines = text.splitlines()
        for surface, record in surfaces.items():
            route_aliases = dict(record.get("route_aliases") or {})
            for alias, resolved in route_aliases.items():
                pattern = re.compile(rf"\b{re.escape(alias)}\b")
                for line_number, line in enumerate(lines, start=1):
                    if not pattern.search(line):
                        continue
                    severity = _classify_line_severity(line)
                    findings.append(
                        AuthorityAuditFinding(
                            surface=str(surface),
                            path=relative_path,
                            line_number=line_number,
                            matched_name=str(alias),
                            resolves_to=str(resolved),
                            severity=severity,
                            line_text=line.strip(),
                        )
                    )
        return findings


def _alias_alignment_matches_target(resolution: Any, target_name: str) -> bool:
    if resolution.decision is NameResolutionDecision.NORMALIZE_TO_CURRENT_TRUE_NAME:
        return resolution.current_true_name == target_name or resolution.resolved_name == target_name
    if resolution.decision is NameResolutionDecision.ALLOW_AS_AUTHORITY:
        return resolution.current_true_name == target_name or resolution.resolved_name == target_name
    if resolution.decision is NameResolutionDecision.REQUIRES_EXPLICIT_TRUE_NAME:
        return target_name in set(resolution.successor_candidates)
    return False


def lineage_warning(resolution: AuthorityResolution) -> str | None:
    if resolution.warning:
        return (
            f"AUTHORITY_LINEAGE[{resolution.surface}] {resolution.warning} "
            f"(requested={resolution.requested_name!r}, resolved={resolution.resolved_name!r}, status={resolution.status})"
        )
    if resolution.changed:
        return (
            f"AUTHORITY_LINEAGE[{resolution.surface}] requested={resolution.requested_name!r} "
            f"resolved={resolution.resolved_name!r} status={resolution.status}"
        )
    return None


def resolve_explicit_authority_override(
    workspace_root: str | Path | None,
    surface: str,
    requested_name: str | None,
    *,
    created_at: str | None = None,
) -> AuthorityOverrideResult:
    requested = (requested_name or "").strip() or None
    if requested is None:
        return AuthorityOverrideResult(
            requested_name=None,
            resolved_name=None,
        )
    if requested == "FreshExecutor":
        return AuthorityOverrideResult(
            requested_name=requested,
            resolved_name=requested,
        )

    manager = KernelAuthorityLineageManager()
    lookup_root = (
        Path(workspace_root).resolve()
        if workspace_root is not None
        else Path(__file__).resolve().parents[3]
    )
    resolution = manager.resolve_authority(lookup_root, surface, requested)
    warning = lineage_warning(resolution)
    receipt_paths: list[str] = []
    if workspace_root is not None:
        recorded = manager.record_resolution(
            Path(workspace_root).resolve(),
            resolution,
            created_at=created_at,
        )
        if recorded is not None:
            receipt_paths.append(recorded.receipt_path)
    return AuthorityOverrideResult(
        requested_name=requested,
        resolved_name=resolution.resolved_name,
        warnings=(() if warning is None else (warning,)),
        receipt_paths=tuple(receipt_paths),
    )


IonAuthorityLineageManager = KernelAuthorityLineageManager


def _surface_record(registry: dict[str, Any], surface: str) -> dict[str, Any]:
    record = dict((registry.get("surfaces") or {}).get(surface) or {})
    if not record:
        raise KernelAuthorityLineageError(f"Unknown authority surface: {surface}")
    return record


def _classify_line_severity(line: str) -> str:
    lowered = line.lower()
    if "default=" in lowered or " or \"" in lowered or " or '" in lowered:
        return "ACTIVE_DEFAULT_STALE_ALIAS"
    return "ACTIVE_SURFACE_STALE_ALIAS"


def _join_relative_path(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelAuthorityLineageError(f"Absolute paths are not allowed: {relative_path}")
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelAuthorityLineageError(f"Path escapes workspace root: {relative_path}") from exc
    return resolved


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    return _join_relative_path(root, relative_path)
