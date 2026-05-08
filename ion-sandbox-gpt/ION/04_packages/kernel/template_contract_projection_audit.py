"""Template contract source/projection alignment audit.

This module compares the human-governance YAML registry against the dependency-
free JSON runtime projection. It intentionally uses a small line-oriented YAML
extractor for contract metadata so kernel-safe tests do not require PyYAML.

It is read-only except for explicit audit receipt emission.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


SOURCE_RELATIVE_PATH = "ION/03_registry/template_metadata_contract_registry.yaml"
PROJECTION_RELATIVE_PATH = "ION/03_registry/template_metadata_contract_registry.projection.json"


class TemplateContractProjectionAuditError(Exception):
    """Raised when template contract projection audit cannot proceed."""


@dataclass(frozen=True)
class ContractSummary:
    template_id: str
    canonical_name: str = ""
    version: str = ""
    contract_status: str = ""


@dataclass(frozen=True)
class ContractFieldMismatch:
    template_id: str
    field: str
    source_value: str
    projection_value: str


@dataclass(frozen=True)
class TemplateContractProjectionAudit:
    audit_id: str
    emitted_at: str
    source_registry_path: str
    projection_path: str
    verdict: str
    source_contract_count: int
    projection_contract_count: int
    missing_in_projection: tuple[str, ...]
    extra_in_projection: tuple[str, ...]
    field_mismatches: tuple[ContractFieldMismatch, ...]
    duplicate_source_template_ids: tuple[str, ...]
    duplicate_projection_template_ids: tuple[str, ...]
    mutation_allowed: bool = False


def audit_template_contract_projection(
    workspace_root: Path,
    *,
    emitted_at: str | None = None,
) -> TemplateContractProjectionAudit:
    root = Path(workspace_root)
    timestamp = emitted_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    source_path = root / SOURCE_RELATIVE_PATH
    projection_path = root / PROJECTION_RELATIVE_PATH
    audit_id = _stable_id("template-contract-projection-audit", root.as_posix(), timestamp)

    if not source_path.exists():
        return TemplateContractProjectionAudit(
            audit_id=audit_id,
            emitted_at=timestamp,
            source_registry_path=source_path.as_posix(),
            projection_path=projection_path.as_posix(),
            verdict="SOURCE_MISSING",
            source_contract_count=0,
            projection_contract_count=0,
            missing_in_projection=(),
            extra_in_projection=(),
            field_mismatches=(),
            duplicate_source_template_ids=(),
            duplicate_projection_template_ids=(),
        )

    if not projection_path.exists():
        source_contracts, source_dupes = read_source_contract_summaries(source_path)
        return TemplateContractProjectionAudit(
            audit_id=audit_id,
            emitted_at=timestamp,
            source_registry_path=source_path.as_posix(),
            projection_path=projection_path.as_posix(),
            verdict="PROJECTION_MISSING",
            source_contract_count=len(source_contracts),
            projection_contract_count=0,
            missing_in_projection=tuple(sorted(source_contracts)),
            extra_in_projection=(),
            field_mismatches=(),
            duplicate_source_template_ids=tuple(sorted(source_dupes)),
            duplicate_projection_template_ids=(),
        )

    source_contracts, source_dupes = read_source_contract_summaries(source_path)
    projection_contracts, projection_dupes, source_pointer = read_projection_contract_summaries(projection_path)

    missing = tuple(sorted(set(source_contracts) - set(projection_contracts)))
    extra = tuple(sorted(set(projection_contracts) - set(source_contracts)))
    mismatches: list[ContractFieldMismatch] = []

    for template_id in sorted(set(source_contracts) & set(projection_contracts)):
        source = source_contracts[template_id]
        projection = projection_contracts[template_id]
        for field in ("canonical_name", "version", "contract_status"):
            source_value = getattr(source, field)
            projection_value = getattr(projection, field)
            if source_value != projection_value:
                mismatches.append(
                    ContractFieldMismatch(
                        template_id=template_id,
                        field=field,
                        source_value=source_value,
                        projection_value=projection_value,
                    )
                )

    if source_pointer and source_pointer != SOURCE_RELATIVE_PATH:
        mismatches.append(
            ContractFieldMismatch(
                template_id="__projection__",
                field="source_registry",
                source_value=SOURCE_RELATIVE_PATH,
                projection_value=source_pointer,
            )
        )

    verdict = "ALIGNED"
    if missing or extra or mismatches or source_dupes or projection_dupes:
        verdict = "MISMATCH"

    return TemplateContractProjectionAudit(
        audit_id=audit_id,
        emitted_at=timestamp,
        source_registry_path=source_path.as_posix(),
        projection_path=projection_path.as_posix(),
        verdict=verdict,
        source_contract_count=len(source_contracts),
        projection_contract_count=len(projection_contracts),
        missing_in_projection=missing,
        extra_in_projection=extra,
        field_mismatches=tuple(mismatches),
        duplicate_source_template_ids=tuple(sorted(source_dupes)),
        duplicate_projection_template_ids=tuple(sorted(projection_dupes)),
    )


def read_source_contract_summaries(path: Path) -> tuple[dict[str, ContractSummary], set[str]]:
    """Extract minimal contract summaries from the source YAML registry.

    This is not a general YAML parser. It is a kernel-safe extractor for the
    subset of registry fields required by the alignment audit.
    """

    contracts: dict[str, ContractSummary] = {}
    duplicates: set[str] = set()
    current: dict[str, str] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("- template_id:"):
            if current:
                _add_contract_summary(current, contracts, duplicates)
            current = {"template_id": _clean_value(stripped.split(":", 1)[1])}
            continue
        if current is not None and any(
            stripped.startswith(prefix)
            for prefix in ("canonical_name:", "version:", "contract_status:")
        ):
            key, value = stripped.split(":", 1)
            current[key.strip()] = _clean_value(value)

    if current:
        _add_contract_summary(current, contracts, duplicates)

    return contracts, duplicates


def read_projection_contract_summaries(path: Path) -> tuple[dict[str, ContractSummary], set[str], str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise TemplateContractProjectionAuditError(f"projection unreadable: {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise TemplateContractProjectionAuditError("projection root must be object")

    contracts_raw = data.get("contracts")
    if not isinstance(contracts_raw, list):
        raise TemplateContractProjectionAuditError("projection contracts must be list")

    contracts: dict[str, ContractSummary] = {}
    duplicates: set[str] = set()
    for item in contracts_raw:
        if not isinstance(item, dict):
            continue
        template_id = str(item.get("template_id") or "")
        if not template_id:
            continue
        summary = ContractSummary(
            template_id=template_id,
            canonical_name=str(item.get("canonical_name") or ""),
            version=str(item.get("version") or ""),
            contract_status=str(item.get("contract_status") or ""),
        )
        if template_id in contracts:
            duplicates.add(template_id)
        contracts[template_id] = summary

    return contracts, duplicates, str(data.get("source_registry") or "")


def write_template_contract_projection_audit_receipt(
    workspace_root: Path,
    audit: TemplateContractProjectionAudit,
) -> Path:
    output_dir = Path(workspace_root) / "ION/05_context/history/template_contract_projection_audits"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{audit.audit_id}.template_contract_projection_audit.json"
    if path.exists():
        return path
    path.write_text(json.dumps(_to_jsonable(audit), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _add_contract_summary(raw: dict[str, str], contracts: dict[str, ContractSummary], duplicates: set[str]) -> None:
    template_id = raw.get("template_id", "")
    if not template_id:
        return
    if template_id in contracts:
        duplicates.add(template_id)
    contracts[template_id] = ContractSummary(
        template_id=template_id,
        canonical_name=raw.get("canonical_name", ""),
        version=raw.get("version", ""),
        contract_status=raw.get("contract_status", ""),
    )


def _clean_value(value: str) -> str:
    return value.strip().strip('"').strip("'")


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    return value
