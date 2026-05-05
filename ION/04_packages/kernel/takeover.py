"""L2 handoff/takeover normalization surfaces for the active ION kernel stack.

This module makes takeover sufficiency durable and operator-visible. Validation still
belongs to packet law, but L2 adds explicit assessment receipts so continuation is not
only a transient parser result.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import hashlib
import re

from .index import KernelIndex
from .model import TakeoverAssessmentReceipt
from .packet_validation import PacketTakeoverAssessment, assess_packet_takeover_path, parse_workflow_packet_path
from .store import KernelStore


class KernelTakeoverError(Exception):
    """Raised when one bounded takeover operation cannot be completed lawfully."""


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelTakeoverManager:
    """Assess, persist, and project bounded packet-takeover sufficiency."""

    def assess_packet_path(
        self,
        path: str | Path,
        *,
        expected_type: str | None = None,
        allow_legacy: bool = False,
    ) -> PacketTakeoverAssessment:
        return assess_packet_takeover_path(
            path,
            expected_type=expected_type,
            allow_legacy=allow_legacy,
        )

    def record_packet_takeover(
        self,
        store: KernelStore,
        index: KernelIndex,
        path: str | Path,
        *,
        expected_type: str | None = None,
        allow_legacy: bool = False,
        workspace_root: str | Path | None = None,
        created_at: str | None = None,
    ) -> TakeoverAssessmentReceipt:
        packet_path = Path(path).resolve()
        assessment = self.assess_packet_path(
            packet_path,
            expected_type=expected_type,
            allow_legacy=allow_legacy,
        )
        return self.persist_takeover_receipt(
            store,
            index,
            assessment,
            packet_path=packet_path,
            workspace_root=workspace_root,
            created_at=created_at,
        )

    def persist_takeover_receipt(
        self,
        store: KernelStore,
        index: KernelIndex,
        assessment: PacketTakeoverAssessment,
        *,
        packet_path: str | Path,
        workspace_root: str | Path | None = None,
        created_at: str | None = None,
    ) -> TakeoverAssessmentReceipt:
        if not assessment.valid:
            problems = "; ".join(assessment.warnings) or "insufficient takeover context"
            raise KernelTakeoverError(f"Cannot persist takeover receipt from insufficient packet: {problems}")
        if not assessment.scope_binding:
            raise KernelTakeoverError("Takeover receipt requires one explicit scope binding.")

        scope_type, scope_ref = _split_scope_binding(assessment.scope_binding)
        resolved_packet_path = Path(packet_path).resolve()
        packet_text = resolved_packet_path.read_text(encoding="utf-8")
        parsed = parse_workflow_packet_path(
            resolved_packet_path,
            expected_type=assessment.packet_type,
        )
        packet_checksum = _content_checksum(packet_text)
        timestamp = created_at or _iso_now()
        receipt = TakeoverAssessmentReceipt(
            receipt_id=takeover_assessment_receipt_id(
                scope_type,
                scope_ref,
                assessment.packet_type,
                packet_checksum,
                timestamp,
            ),
            created_at=timestamp,
            scope_type=scope_type,
            scope_ref=scope_ref,
            packet_path=str(resolved_packet_path),
            packet_relative_path=_packet_relative_path(resolved_packet_path, workspace_root),
            packet_checksum=packet_checksum,
            packet_type=assessment.packet_type,
            packet_title=assessment.title,
            packet_created_at=assessment.created_at,
            packet_status=assessment.status,
            objective=assessment.objective,
            target_executor=assessment.target_executor,
            required_reads=assessment.required_reads,
            next_action=assessment.next_action,
            expected_output=assessment.expected_output,
            warnings=assessment.warnings,
        )
        if parsed.packet_type != assessment.packet_type:
            raise KernelTakeoverError("Packet assessment and parsed packet type diverged unexpectedly.")
        if index.exists("takeover_assessment_receipt", receipt.receipt_id):
            store.replace(receipt)
            index.record_changed(receipt)
        else:
            store.create(receipt)
            index.record_added(receipt)
        return receipt

    def latest_takeover_receipt(
        self,
        index: KernelIndex,
        scope_type: str | None = None,
        scope_ref: str | None = None,
    ) -> TakeoverAssessmentReceipt | None:
        normalized_scope = _normalize_scope_filter(scope_type, scope_ref)
        if normalized_scope is None:
            receipts = [
                record
                for record in index.records_by_type("takeover_assessment_receipt")
                if isinstance(record, TakeoverAssessmentReceipt)
            ]
        else:
            receipts = index.takeover_assessment_receipts_for_scope(
                normalized_scope[0],
                normalized_scope[1],
            )
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_takeover_receipt_projection(
        self,
        receipt: TakeoverAssessmentReceipt | None,
    ) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "packet_path": receipt.packet_path,
            "packet_relative_path": receipt.packet_relative_path,
            "packet_checksum": receipt.packet_checksum,
            "packet_type": receipt.packet_type,
            "packet_title": receipt.packet_title,
            "packet_created_at": receipt.packet_created_at,
            "packet_status": receipt.packet_status,
            "objective": receipt.objective,
            "target_executor": receipt.target_executor,
            "required_reads": list(receipt.required_reads),
            "next_action": receipt.next_action,
            "expected_output": list(receipt.expected_output),
            "warnings": list(receipt.warnings),
        }


def render_takeover_assessment(assessment: PacketTakeoverAssessment) -> str:
    lines = [
        "ION Packet Takeover Assessment",
        f"path: {assessment.path or '<memory>'}",
        f"packet_type: {assessment.packet_type}",
        f"valid: {'yes' if assessment.valid else 'no'}",
        f"objective: {assessment.objective or 'NONE'}",
        f"scope_binding: {assessment.scope_binding or 'NONE'}",
        f"target_executor: {assessment.target_executor or 'NONE'}",
    ]
    if assessment.title:
        lines.append(f"title: {assessment.title}")
    if assessment.created_at:
        lines.append(f"packet_created_at: {assessment.created_at}")
    if assessment.status:
        lines.append(f"packet_status: {assessment.status}")
    lines.append("required_reads:")
    if assessment.required_reads:
        lines.extend(f"  - {item}" for item in assessment.required_reads)
    else:
        lines.append("  - NONE")
    lines.append(f"next_action: {assessment.next_action or 'NONE'}")
    lines.append("expected_output:")
    if assessment.expected_output:
        lines.extend(f"  - {item}" for item in assessment.expected_output)
    else:
        lines.append("  - NONE")
    lines.append("warnings:")
    if assessment.warnings:
        lines.extend(f"  - {warning}" for warning in assessment.warnings)
    else:
        lines.append("  - NONE")
    return "\n".join(lines)


def takeover_assessment_receipt_id(
    scope_type: str,
    scope_ref: str,
    packet_type: str,
    packet_checksum: str,
    created_at: str,
) -> str:
    clean_scope_type = _SAFE_ID_RE.sub("-", scope_type.lower()).strip("-") or "scope"
    clean_scope_ref = _SAFE_ID_RE.sub("-", scope_ref.lower()).strip("-") or "state"
    clean_packet_type = _SAFE_ID_RE.sub("-", packet_type.lower()).strip("-") or "packet"
    clean_checksum = _SAFE_ID_RE.sub("-", packet_checksum.lower()).strip("-")[:12] or "checksum"
    clean_created_at = _SAFE_ID_RE.sub("-", created_at.lower()).strip("-") or "timestamp"
    return f"takeover-{clean_scope_type}-{clean_scope_ref}-{clean_packet_type}-{clean_checksum}-{clean_created_at}"


def _packet_relative_path(packet_path: Path, workspace_root: str | Path | None) -> str | None:
    if workspace_root is None:
        return None
    try:
        return str(packet_path.relative_to(Path(workspace_root).resolve()))
    except ValueError:
        return None


def _split_scope_binding(scope_binding: str) -> tuple[str, str]:
    scope_type, sep, scope_ref = scope_binding.partition(":")
    normalized_scope_type = scope_type.strip().upper()
    normalized_scope_ref = scope_ref.strip()
    if not sep or not normalized_scope_type or not normalized_scope_ref:
        raise KernelTakeoverError(f"Invalid scope binding for takeover receipt: {scope_binding!r}")
    return normalized_scope_type, normalized_scope_ref


def _normalize_scope_filter(
    scope_type: str | None,
    scope_ref: str | None,
) -> tuple[str, str] | None:
    if scope_type is None and scope_ref is None:
        return None
    if not scope_type or not scope_ref:
        raise KernelTakeoverError("scope_type and scope_ref must be provided together.")
    return scope_type.strip().upper(), scope_ref.strip()


def _content_checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
