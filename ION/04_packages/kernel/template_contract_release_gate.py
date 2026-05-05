"""Release/checkpoint gate for template contract projection alignment.

V19 makes the V18 audit actionable: production contract-bound automation and
release/checkpoint validation can require an ALIGNED source/projection audit.

This module is read-only except for explicit gate receipt emission.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from .template_contract_projection_audit import (
    TemplateContractProjectionAuditError,
    audit_template_contract_projection,
)


@dataclass(frozen=True)
class TemplateContractReleaseGateDecision:
    gate_id: str
    emitted_at: str
    gate_name: str
    audit_id: str
    audit_verdict: str
    allowed: bool
    blocked_reason: str
    source_contract_count: int
    projection_contract_count: int
    mutation_allowed: bool = False


class TemplateContractReleaseGateError(Exception):
    """Raised when template contract release/checkpoint gate blocks."""


def evaluate_template_contract_release_gate(
    workspace_root: Path,
    *,
    emitted_at: str | None = None,
    gate_name: str = "template_contract_projection_release_gate",
) -> TemplateContractReleaseGateDecision:
    """Evaluate whether contract-bound production/release paths may proceed."""

    root = Path(workspace_root)
    timestamp = emitted_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    gate_id = _stable_id("template-contract-release-gate", root.as_posix(), timestamp, gate_name)

    try:
        audit = audit_template_contract_projection(root, emitted_at=timestamp)
    except TemplateContractProjectionAuditError as exc:
        return TemplateContractReleaseGateDecision(
            gate_id=gate_id,
            emitted_at=timestamp,
            gate_name=gate_name,
            audit_id="AUDIT_ERROR",
            audit_verdict="AUDIT_ERROR",
            allowed=False,
            blocked_reason=f"AUDIT_ERROR:{exc}",
            source_contract_count=0,
            projection_contract_count=0,
        )

    if audit.verdict == "ALIGNED":
        return TemplateContractReleaseGateDecision(
            gate_id=gate_id,
            emitted_at=timestamp,
            gate_name=gate_name,
            audit_id=audit.audit_id,
            audit_verdict=audit.verdict,
            allowed=True,
            blocked_reason="",
            source_contract_count=audit.source_contract_count,
            projection_contract_count=audit.projection_contract_count,
        )

    return TemplateContractReleaseGateDecision(
        gate_id=gate_id,
        emitted_at=timestamp,
        gate_name=gate_name,
        audit_id=audit.audit_id,
        audit_verdict=audit.verdict,
        allowed=False,
        blocked_reason=f"CONTRACT_PROJECTION_AUDIT_NOT_ALIGNED:{audit.verdict}",
        source_contract_count=audit.source_contract_count,
        projection_contract_count=audit.projection_contract_count,
    )


def require_template_contract_release_gate(
    workspace_root: Path,
    *,
    emitted_at: str | None = None,
    gate_name: str = "template_contract_projection_release_gate",
) -> TemplateContractReleaseGateDecision:
    """Evaluate gate and raise if blocked."""

    decision = evaluate_template_contract_release_gate(
        workspace_root,
        emitted_at=emitted_at,
        gate_name=gate_name,
    )
    if not decision.allowed:
        raise TemplateContractReleaseGateError(decision.blocked_reason)
    return decision


def write_template_contract_release_gate_receipt(
    workspace_root: Path,
    decision: TemplateContractReleaseGateDecision,
) -> Path:
    output_dir = Path(workspace_root) / "ION/05_context/history/template_contract_release_gates"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{decision.gate_id}.template_contract_release_gate_receipt.json"
    if path.exists():
        return path
    path.write_text(json.dumps(_to_jsonable(decision), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


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
