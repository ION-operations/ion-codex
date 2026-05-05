"""Governed name-lineage helpers for current-phase ION authority resolution.

This module does not try to solve all semantic drift. It implements one bounded
current-phase slice:

1. load the file-backed name-lineage registry,
2. resolve raw incoming names into current authority posture,
3. reject retired ambiguous names from live ingress where silent routing is not lawful,
4. audit active surfaces for stale-name drift, and
5. emit lightweight witness receipts when explicit resolution is requested.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re

from .model import StrEnum


class KernelNameLineageError(Exception):
    """Raised when name-lineage resolution cannot proceed lawfully."""


class NameIngressSurface(StrEnum):
    LIVE_AUTHORITY = "LIVE_AUTHORITY"
    BOOTSTRAP_PACKET = "BOOTSTRAP_PACKET"
    OPEN_QUESTION_ROUTE = "OPEN_QUESTION_ROUTE"
    ANSWER_INGEST = "ANSWER_INGEST"
    OPERATOR_INPUT = "OPERATOR_INPUT"
    ACTIVE_SURFACE_AUDIT = "ACTIVE_SURFACE_AUDIT"
    HISTORICAL_REPLAY = "HISTORICAL_REPLAY"


class NameResolutionDecision(StrEnum):
    ALLOW_AS_AUTHORITY = "ALLOW_AS_AUTHORITY"
    NORMALIZE_TO_CURRENT_TRUE_NAME = "NORMALIZE_TO_CURRENT_TRUE_NAME"
    REQUIRES_EXPLICIT_TRUE_NAME = "REQUIRES_EXPLICIT_TRUE_NAME"
    UNREGISTERED_NAME = "UNREGISTERED_NAME"
    ALLOW_HISTORICAL_REPLAY = "ALLOW_HISTORICAL_REPLAY"


class NameAuditSeverity(StrEnum):
    INFO = "INFO"
    ALERT = "ALERT"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class NameResolution:
    raw_name: str
    surface: NameIngressSurface
    matched: bool
    entity_id: str | None
    entity_kind: str | None
    alias_name: str | None
    alias_status: str | None
    relation_type: str | None
    current_true_name: str | None
    resolved_name: str | None
    decision: NameResolutionDecision
    accepted_for_ingress: bool
    historical_only: bool
    warning_code: str | None = None
    successor_candidates: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RecordedNameResolution:
    receipt_id: str
    created_at: str
    resolution: NameResolution
    receipt_path: str
    ledger_path: str


@dataclass(frozen=True)
class NameAuditFinding:
    path: str
    line_number: int
    matched_name: str
    entity_id: str
    current_true_name: str | None
    decision: NameResolutionDecision
    severity: NameAuditSeverity
    warning_code: str | None
    recommended_action: str
    line_excerpt: str


@dataclass(frozen=True)
class NameAuditResult:
    scanned_paths: tuple[str, ...]
    findings: tuple[NameAuditFinding, ...]
    blocked_count: int
    alert_count: int
    info_count: int


@dataclass(frozen=True)
class _LineageAliasRecord:
    name: str
    alias_status: str
    relation_type: str
    accepted_for_ingress: bool
    historical_only: bool
    live_decision: NameResolutionDecision
    warning_code: str | None
    successor_candidates: tuple[str, ...]


@dataclass(frozen=True)
class _LineageEntityRecord:
    entity_id: str
    entity_kind: str
    current_true_name: str
    notes: str | None
    aliases: tuple[_LineageAliasRecord, ...]


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")
_IGNORED_DIRS = {".git", ".pytest_cache", "__pycache__", "node_modules"}
_DOCUMENT_HISTORICAL_CONTEXT_MARKERS = (
    "historical witness",
    "historical_witness_only",
    "witness only",
    "historical alias",
    "retired_current_phase",
    "retired current phase",
    "historical carrier",
)
_LINE_LINEAGE_CONTEXT_MARKERS = (
    "historical witness",
    "witness only",
    "retirement",
    "retired",
    "historical alias",
    "historical carrier",
    "historical replay",
    "compatibility witness",
    "preserve raw",
    "preserve original",
    "raw token",
    "lineage evidence",
    "excluded_entities",
    "historical_witness_only",
    "retired_current_phase",
)


class KernelNameLineageManager:
    """Resolve and audit governed names against the current-phase lineage registry."""

    _REGISTRY_RELATIVE_PATH = Path("03_registry/name_lineage_registry.yaml")

    def resolve_name(
        self,
        raw_name: str,
        *,
        surface: NameIngressSurface = NameIngressSurface.LIVE_AUTHORITY,
        strict: bool = False,
    ) -> NameResolution:
        normalized = raw_name.strip()
        if not normalized:
            raise KernelNameLineageError("Name resolution requires a non-empty raw_name.")

        entity, alias = self._lookup_alias(normalized)
        if entity is None or alias is None:
            return NameResolution(
                raw_name=normalized,
                surface=surface,
                matched=False,
                entity_id=None,
                entity_kind=None,
                alias_name=None,
                alias_status=None,
                relation_type=None,
                current_true_name=None,
                resolved_name=normalized,
                decision=NameResolutionDecision.UNREGISTERED_NAME,
                accepted_for_ingress=True,
                historical_only=False,
                notes=("UNREGISTERED_NAME",),
            )

        if surface is NameIngressSurface.HISTORICAL_REPLAY and alias.historical_only:
            return NameResolution(
                raw_name=normalized,
                surface=surface,
                matched=True,
                entity_id=entity.entity_id,
                entity_kind=entity.entity_kind,
                alias_name=alias.name,
                alias_status=alias.alias_status,
                relation_type=alias.relation_type,
                current_true_name=entity.current_true_name,
                resolved_name=normalized,
                decision=NameResolutionDecision.ALLOW_HISTORICAL_REPLAY,
                accepted_for_ingress=True,
                historical_only=True,
                warning_code=alias.warning_code,
                successor_candidates=alias.successor_candidates,
                notes=("HISTORICAL_REPLAY_PRESERVES_RAW_NAME",),
            )

        resolved_name = entity.current_true_name
        notes: list[str] = []
        if alias.live_decision is NameResolutionDecision.NORMALIZE_TO_CURRENT_TRUE_NAME:
            notes.append(
                f"Preserve raw token `{normalized}` for provenance and use `{entity.current_true_name}` for live authority."
            )
        elif alias.live_decision is NameResolutionDecision.REQUIRES_EXPLICIT_TRUE_NAME:
            resolved_name = None
            notes.append(
                f"`{normalized}` is not a lawful live authority name in the current phase."
            )
            if alias.successor_candidates:
                notes.append(
                    "Choose an explicit current true name instead: "
                    + ", ".join(alias.successor_candidates)
                )
            if strict:
                raise KernelNameLineageError(" ".join(notes))

        return NameResolution(
            raw_name=normalized,
            surface=surface,
            matched=True,
            entity_id=entity.entity_id,
            entity_kind=entity.entity_kind,
            alias_name=alias.name,
            alias_status=alias.alias_status,
            relation_type=alias.relation_type,
            current_true_name=entity.current_true_name,
            resolved_name=resolved_name,
            decision=alias.live_decision,
            accepted_for_ingress=alias.accepted_for_ingress,
            historical_only=alias.historical_only,
            warning_code=alias.warning_code,
            successor_candidates=alias.successor_candidates,
            notes=tuple(notes),
        )

    def resolve_required_name(
        self,
        raw_name: str,
        *,
        surface: NameIngressSurface = NameIngressSurface.LIVE_AUTHORITY,
    ) -> NameResolution:
        return self.resolve_name(raw_name, surface=surface, strict=True)

    def render_resolution_note(self, resolution: NameResolution) -> str | None:
        if resolution.decision is NameResolutionDecision.ALLOW_AS_AUTHORITY:
            return None
        if resolution.decision is NameResolutionDecision.UNREGISTERED_NAME:
            return "UNREGISTERED_NAME_PRESERVED_AS_RAW_INPUT"
        if resolution.decision is NameResolutionDecision.ALLOW_HISTORICAL_REPLAY:
            return "HISTORICAL_REPLAY_PRESERVED_RAW_NAME"
        if resolution.resolved_name is None:
            code = resolution.warning_code or resolution.decision.value
            return f"{code}:{resolution.raw_name}"
        code = resolution.warning_code or resolution.decision.value
        return f"{code}:{resolution.raw_name}->{resolution.resolved_name}"

    def record_resolution(
        self,
        workspace_root: str | Path,
        resolution: NameResolution,
        *,
        created_at: str | None = None,
        receipts_dir: str = "ION/05_context/history/name_lineage_resolution_receipts",
        ledger_path: str = "ION/05_context/history/name_lineage_resolution_ledger.json",
    ) -> RecordedNameResolution:
        root = Path(workspace_root).resolve()
        timestamp = created_at or _iso_now()
        receipt_id = name_lineage_resolution_receipt_id(
            resolution.raw_name,
            resolution.surface.value,
            timestamp,
        )
        receipt_relative_path = Path(receipts_dir) / f"{receipt_id}.name_lineage_resolution_receipt.json"
        ledger_relative_path = Path(ledger_path)
        resolved_receipt_path = root / receipt_relative_path
        resolved_ledger_path = root / ledger_relative_path
        resolved_receipt_path.parent.mkdir(parents=True, exist_ok=True)
        resolved_ledger_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "receipt_id": receipt_id,
            "created_at": timestamp,
            "resolution": _resolution_payload(resolution),
        }
        resolved_receipt_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        rows: list[dict[str, object]] = []
        if resolved_ledger_path.exists():
            existing = json.loads(resolved_ledger_path.read_text(encoding="utf-8"))
            if isinstance(existing, list):
                rows = existing
        rows.append(
            {
                "receipt_id": receipt_id,
                "created_at": timestamp,
                "raw_name": resolution.raw_name,
                "surface": resolution.surface.value,
                "decision": resolution.decision.value,
                "resolved_name": resolution.resolved_name,
                "warning_code": resolution.warning_code,
                "receipt_path": str(receipt_relative_path),
            }
        )
        resolved_ledger_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return RecordedNameResolution(
            receipt_id=receipt_id,
            created_at=timestamp,
            resolution=resolution,
            receipt_path=str(receipt_relative_path),
            ledger_path=str(ledger_relative_path),
        )

    def audit_active_surfaces(
        self,
        workspace_root: str | Path,
        *,
        paths: tuple[str, ...] = (),
        include_historical: bool = False,
    ) -> NameAuditResult:
        root = Path(workspace_root).resolve()
        payload = self._registry_payload()
        policy = payload.get("surface_policy", {})
        selected_paths = list(paths) if paths else list(policy.get("active_surface_roots", ()))
        if include_historical:
            selected_paths.extend(policy.get("historical_surface_roots", ()))
        files = self._iter_scan_files(root, selected_paths)
        findings: list[NameAuditFinding] = []
        stale_aliases = [
            (entity, alias)
            for entity in self._records()
            for alias in entity.aliases
            if alias.alias_status != "CURRENT_TRUE_NAME"
        ]
        for file_path in files:
            relative = str(file_path.relative_to(root))
            path_class = self._path_severity_class(relative, policy)
            try:
                text = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            document_context = _document_context_class(path_class, text)
            lines = text.splitlines()
            for line_number, line in enumerate(lines, start=1):
                for entity, alias in stale_aliases:
                    if not _line_contains_alias(line, alias.name):
                        continue
                    start = max(0, line_number - 2)
                    stop = min(len(lines), line_number + 2)
                    context_window = "\n".join(lines[start:stop])
                    effective_context = _line_context_class(document_context, context_window)
                    findings.append(
                        NameAuditFinding(
                            path=relative,
                            line_number=line_number,
                            matched_name=alias.name,
                            entity_id=entity.entity_id,
                            current_true_name=entity.current_true_name,
                            decision=alias.live_decision,
                            severity=_severity_for_alias(alias.live_decision, effective_context),
                            warning_code=alias.warning_code,
                            recommended_action=_recommended_action(alias, entity.current_true_name),
                            line_excerpt=line.strip(),
                        )
                    )
        findings.sort(key=lambda item: (item.path, item.line_number, item.matched_name))
        return NameAuditResult(
            scanned_paths=tuple(str(path.relative_to(root)) for path in files),
            findings=tuple(findings),
            blocked_count=sum(1 for item in findings if item.severity is NameAuditSeverity.BLOCK),
            alert_count=sum(1 for item in findings if item.severity is NameAuditSeverity.ALERT),
            info_count=sum(1 for item in findings if item.severity is NameAuditSeverity.INFO),
        )

    def registry_path(self) -> Path:
        return self._content_root() / self._REGISTRY_RELATIVE_PATH

    def _lookup_alias(self, raw_name: str) -> tuple[_LineageEntityRecord | None, _LineageAliasRecord | None]:
        normalized = raw_name.strip().casefold()
        for entity in self._records():
            for alias in entity.aliases:
                if alias.name.casefold() == normalized:
                    return entity, alias
        return None, None

    def _registry_payload(self) -> dict[str, object]:
        return json.loads(self.registry_path().read_text(encoding="utf-8"))

    def _records(self) -> tuple[_LineageEntityRecord, ...]:
        payload = self._registry_payload()
        records: list[_LineageEntityRecord] = []
        for item in payload.get("records", ()):
            if not isinstance(item, dict):
                continue
            aliases: list[_LineageAliasRecord] = []
            for alias in item.get("aliases", ()):
                if not isinstance(alias, dict):
                    continue
                aliases.append(
                    _LineageAliasRecord(
                        name=str(alias.get("name", "")).strip(),
                        alias_status=str(alias.get("alias_status", "")).strip(),
                        relation_type=str(alias.get("relation_type", "")).strip(),
                        accepted_for_ingress=bool(alias.get("accepted_for_ingress", False)),
                        historical_only=bool(alias.get("historical_only", False)),
                        live_decision=NameResolutionDecision(str(alias.get("live_decision", NameResolutionDecision.UNREGISTERED_NAME.value))),
                        warning_code=(None if alias.get("warning_code") is None else str(alias.get("warning_code")).strip() or None),
                        successor_candidates=tuple(str(item).strip() for item in alias.get("successor_candidates", ()) if str(item).strip()),
                    )
                )
            records.append(
                _LineageEntityRecord(
                    entity_id=str(item.get("entity_id", "")).strip(),
                    entity_kind=str(item.get("entity_kind", "")).strip(),
                    current_true_name=str(item.get("current_true_name", "")).strip(),
                    notes=(None if item.get("notes") is None else str(item.get("notes")).strip() or None),
                    aliases=tuple(aliases),
                )
            )
        return tuple(records)

    def _content_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    def _iter_scan_files(self, workspace_root: Path, relative_paths: list[str]) -> tuple[Path, ...]:
        files: list[Path] = []
        seen: set[Path] = set()
        for relative in relative_paths:
            candidate = (workspace_root / relative).resolve()
            if not candidate.exists():
                continue
            if candidate.is_file():
                if candidate not in seen:
                    files.append(candidate)
                    seen.add(candidate)
                continue
            for path in sorted(candidate.rglob("*")):
                if any(part in _IGNORED_DIRS or part.endswith(".egg-info") for part in path.parts):
                    continue
                if path.is_file() and path not in seen:
                    files.append(path)
                    seen.add(path)
        return tuple(files)

    def _path_severity_class(self, relative_path: str, policy: dict[str, object]) -> str:
        lineage_roots = tuple(str(item) for item in policy.get("lineage_surface_roots", ()))
        historical_roots = tuple(str(item) for item in policy.get("historical_surface_roots", ()))
        if any(relative_path == root or relative_path.startswith(f"{root}/") for root in lineage_roots):
            return "LINEAGE"
        if any(relative_path == root or relative_path.startswith(f"{root}/") for root in historical_roots):
            return "HISTORICAL"
        return "ACTIVE"


def name_lineage_resolution_receipt_id(raw_name: str, surface: str, created_at: str) -> str:
    return f"name-lineage-{_slug(raw_name)}-{_slug(surface)}-{_slug(created_at)}"


def _resolution_payload(resolution: NameResolution) -> dict[str, object]:
    return {
        "raw_name": resolution.raw_name,
        "surface": resolution.surface.value,
        "matched": resolution.matched,
        "entity_id": resolution.entity_id,
        "entity_kind": resolution.entity_kind,
        "alias_name": resolution.alias_name,
        "alias_status": resolution.alias_status,
        "relation_type": resolution.relation_type,
        "current_true_name": resolution.current_true_name,
        "resolved_name": resolution.resolved_name,
        "decision": resolution.decision.value,
        "accepted_for_ingress": resolution.accepted_for_ingress,
        "historical_only": resolution.historical_only,
        "warning_code": resolution.warning_code,
        "successor_candidates": list(resolution.successor_candidates),
        "notes": list(resolution.notes),
    }


def _line_contains_alias(line: str, alias: str) -> bool:
    pattern = re.compile(rf"(?<![0-9A-Za-z_]){re.escape(alias)}(?![0-9A-Za-z_])", flags=re.IGNORECASE)
    return bool(pattern.search(line))


def _document_context_class(path_class: str, text: str) -> str:
    if path_class != "ACTIVE":
        return path_class
    header = "\n".join(text.splitlines()[:24]).casefold()
    if any(marker in header for marker in _DOCUMENT_HISTORICAL_CONTEXT_MARKERS):
        return "HISTORICAL"
    return path_class


def _line_context_class(document_context: str, context_window: str) -> str:
    if document_context != "ACTIVE":
        return document_context
    lowered = context_window.casefold()
    if any(marker in lowered for marker in _LINE_LINEAGE_CONTEXT_MARKERS):
        return "LINEAGE"
    return document_context


def _severity_for_alias(decision: NameResolutionDecision, path_class: str) -> NameAuditSeverity:
    if path_class in {"LINEAGE", "HISTORICAL"}:
        return NameAuditSeverity.INFO
    if decision is NameResolutionDecision.REQUIRES_EXPLICIT_TRUE_NAME:
        return NameAuditSeverity.BLOCK
    if decision is NameResolutionDecision.NORMALIZE_TO_CURRENT_TRUE_NAME:
        return NameAuditSeverity.ALERT
    return NameAuditSeverity.INFO


def _recommended_action(alias: _LineageAliasRecord, current_true_name: str | None) -> str:
    if alias.live_decision is NameResolutionDecision.NORMALIZE_TO_CURRENT_TRUE_NAME and current_true_name:
        return f"Replace active-surface usage with `{current_true_name}` and preserve `{alias.name}` only in lineage or provenance."
    if alias.successor_candidates:
        return (
            "Remove the stale authority token and replace it with an explicit current true name: "
            + ", ".join(alias.successor_candidates)
        )
    return "Remove the stale authority token from active control surfaces and preserve it only in lineage."


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
