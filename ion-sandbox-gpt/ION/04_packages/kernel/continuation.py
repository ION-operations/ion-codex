"""L4 context-perfect continuation proof surfaces for the active ION kernel stack.

This module proves one bounded claim: a takeover-sufficient packet can materialize
the exact context it names into a reproducible bundle so a fresh executor can
continue without hidden reconstruction.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import hashlib
import json
import re

from .authority_lineage import resolve_explicit_authority_override
from .index import KernelIndex
from .model import ContextPerfectContinuationReceipt, ContinuationReadWitness
from .packet_validation import render_takeover_role_session
from .store import KernelStore
from .takeover import KernelTakeoverManager


class KernelContextPerfectContinuationError(Exception):
    """Raised when one bounded continuation proof cannot be completed lawfully."""


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelContextPerfectContinuationManager:
    """Materialize one packet's explicit continuation context into a durable bundle."""

    def __init__(self) -> None:
        self._takeover_manager = KernelTakeoverManager()

    def prove_packet_continuation(
        self,
        store: KernelStore,
        index: KernelIndex,
        path: str | Path,
        *,
        workspace_root: str | Path,
        repo_root: str | Path | None = None,
        expected_type: str | None = None,
        allow_legacy: bool = False,
        role: str = "FreshExecutor",
        authority_resolve_role: bool = True,
        output_root: str | Path | None = None,
        created_at: str | None = None,
        status: str = "ACTIVE",
    ) -> ContextPerfectContinuationReceipt:
        workspace = Path(workspace_root).resolve()
        source_root = Path(repo_root).resolve() if repo_root is not None else workspace
        packet_path = Path(path).resolve()
        assessment = self._takeover_manager.assess_packet_path(
            packet_path,
            expected_type=expected_type,
            allow_legacy=allow_legacy,
        )
        if not assessment.valid:
            problems = "; ".join(assessment.warnings) or "insufficient takeover context"
            raise KernelContextPerfectContinuationError(
                f"Continuation proof requires a takeover-sufficient packet: {problems}"
            )
        if not assessment.scope_binding:
            raise KernelContextPerfectContinuationError(
                "Continuation proof requires one explicit scope binding."
            )
        if not assessment.required_reads:
            raise KernelContextPerfectContinuationError(
                "Continuation proof requires explicit required reads."
            )
        if not assessment.next_action:
            raise KernelContextPerfectContinuationError(
                "Continuation proof requires one explicit next action."
            )

        timestamp = created_at or _iso_now()
        takeover_receipt = self._takeover_manager.persist_takeover_receipt(
            store,
            index,
            assessment,
            packet_path=packet_path,
            workspace_root=workspace,
            created_at=timestamp,
        )
        scope_type, scope_ref = _split_scope_binding(assessment.scope_binding)
        bundle_root = _resolve_bundle_root(
            workspace,
            scope_type,
            scope_ref,
            assessment.packet_type,
            timestamp,
            output_root,
        )
        bundle_root.mkdir(parents=True, exist_ok=True)

        packet_text = packet_path.read_text(encoding="utf-8")
        packet_bundle_path = bundle_root / "00_source_packet.md"
        packet_bundle_path.write_text(packet_text, encoding="utf-8")

        requested_role = (role or "FreshExecutor").strip() or "FreshExecutor"
        resolved_role = requested_role
        lineage_warnings: list[str] = []
        lineage_receipt_paths: list[str] = []
        if authority_resolve_role:
            override = resolve_explicit_authority_override(
                workspace,
                "continuation_target_executor",
                requested_role,
                created_at=timestamp,
            )
            if override.resolved_name is not None:
                resolved_role = override.resolved_name
            lineage_warnings.extend(override.warnings)
            lineage_receipt_paths.extend(override.receipt_paths)

        role_session_text = render_takeover_role_session(
            assessment,
            role=resolved_role,
            created_at=timestamp,
            status=status,
        )
        role_session_path = bundle_root / "01_role_session.md"
        role_session_path.write_text(role_session_text, encoding="utf-8")

        loaded_reads = tuple(
            _materialize_required_read(
                read_ref=read_ref,
                bundle_root=bundle_root,
                source_root=source_root,
                workspace_root=workspace,
            )
            for read_ref in assessment.required_reads
        )

        manifest_path = bundle_root / "02_manifest.json"
        manifest_payload = {
            "proof_kind": "CONTEXT_PERFECT_CONTINUATION",
            "created_at": timestamp,
            "scope_type": scope_type,
            "scope_ref": scope_ref,
            "packet_type": assessment.packet_type,
            "packet_path": str(packet_path),
            "packet_relative_path": _relative_to_root(packet_path, workspace),
            "objective": assessment.objective,
            "next_action": assessment.next_action,
            "required_reads": list(assessment.required_reads),
            "loaded_reads": [
                {
                    "source_path": witness.source_path,
                    "source_relative_path": witness.source_relative_path,
                    "bundle_relative_path": witness.bundle_relative_path,
                    "checksum": witness.checksum,
                    "byte_count": witness.byte_count,
                    "line_count": witness.line_count,
                }
                for witness in loaded_reads
            ],
            "role_session_relative_path": _relative_to_root(role_session_path, workspace),
            "lineage_receipt_paths": lineage_receipt_paths,
        }
        manifest_path.write_text(
            json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        receipt = ContextPerfectContinuationReceipt(
            receipt_id=context_perfect_continuation_receipt_id(
                scope_type,
                scope_ref,
                assessment.packet_type,
                _content_checksum(packet_text),
                timestamp,
            ),
            created_at=timestamp,
            scope_type=scope_type,
            scope_ref=scope_ref,
            packet_type=assessment.packet_type,
            packet_path=str(packet_path),
            packet_relative_path=_relative_to_root(packet_path, workspace),
            packet_checksum=_content_checksum(packet_text),
            packet_title=assessment.title,
            packet_created_at=assessment.created_at,
            packet_status=assessment.status,
            objective=assessment.objective,
            next_action=assessment.next_action,
            takeover_receipt_id=takeover_receipt.receipt_id,
            bundle_root_path=str(bundle_root),
            bundle_root_relative_path=_relative_to_root(bundle_root, workspace),
            bundle_packet_relative_path=_relative_to_root(packet_bundle_path, workspace),
            bundle_role_session_relative_path=_relative_to_root(role_session_path, workspace),
            bundle_manifest_relative_path=_relative_to_root(manifest_path, workspace),
            role_session_checksum=_content_checksum(role_session_text),
            required_reads=assessment.required_reads,
            loaded_reads=loaded_reads,
            context_perfect=True,
            warnings=tuple(dict.fromkeys(tuple(assessment.warnings) + tuple(lineage_warnings))),
        )
        if index.exists("context_perfect_continuation_receipt", receipt.receipt_id):
            store.replace(receipt)
            index.record_changed(receipt)
        else:
            store.create(receipt)
            index.record_added(receipt)
        return receipt

    def latest_continuation_receipt(
        self,
        index: KernelIndex,
        scope_type: str | None = None,
        scope_ref: str | None = None,
    ) -> ContextPerfectContinuationReceipt | None:
        normalized_scope = _normalize_scope_filter(scope_type, scope_ref)
        if normalized_scope is None:
            receipts = [
                record
                for record in index.records_by_type("context_perfect_continuation_receipt")
                if isinstance(record, ContextPerfectContinuationReceipt)
            ]
        else:
            receipts = index.context_perfect_continuation_receipts_for_scope(
                normalized_scope[0],
                normalized_scope[1],
            )
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_continuation_receipt_projection(
        self,
        receipt: ContextPerfectContinuationReceipt | None,
    ) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "packet_type": receipt.packet_type,
            "packet_path": receipt.packet_path,
            "packet_relative_path": receipt.packet_relative_path,
            "packet_checksum": receipt.packet_checksum,
            "packet_title": receipt.packet_title,
            "packet_created_at": receipt.packet_created_at,
            "packet_status": receipt.packet_status,
            "objective": receipt.objective,
            "next_action": receipt.next_action,
            "takeover_receipt_id": receipt.takeover_receipt_id,
            "bundle_root_path": receipt.bundle_root_path,
            "bundle_root_relative_path": receipt.bundle_root_relative_path,
            "bundle_packet_relative_path": receipt.bundle_packet_relative_path,
            "bundle_role_session_relative_path": receipt.bundle_role_session_relative_path,
            "bundle_manifest_relative_path": receipt.bundle_manifest_relative_path,
            "role_session_checksum": receipt.role_session_checksum,
            "required_reads": list(receipt.required_reads),
            "loaded_reads": [
                {
                    "source_path": witness.source_path,
                    "source_relative_path": witness.source_relative_path,
                    "bundle_relative_path": witness.bundle_relative_path,
                    "checksum": witness.checksum,
                    "byte_count": witness.byte_count,
                    "line_count": witness.line_count,
                }
                for witness in receipt.loaded_reads
            ],
            "context_perfect": receipt.context_perfect,
            "warnings": list(receipt.warnings),
        }


IonContextPerfectContinuationManager = KernelContextPerfectContinuationManager


def context_perfect_continuation_receipt_id(
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
    return (
        f"context-perfect-continuation-{clean_scope_type}-{clean_scope_ref}-"
        f"{clean_packet_type}-{clean_checksum}-{clean_created_at}"
    )


def _materialize_required_read(
    *,
    read_ref: str,
    bundle_root: Path,
    source_root: Path,
    workspace_root: Path,
) -> ContinuationReadWitness:
    source_path = _resolve_read_ref(source_root, read_ref)
    if not source_path.exists():
        raise KernelContextPerfectContinuationError(
            f"Required read is missing for continuation proof: {read_ref}"
        )
    if not source_path.is_file():
        raise KernelContextPerfectContinuationError(
            f"Required read is not a file for continuation proof: {read_ref}"
        )
    destination = bundle_root / "reads" / _bundle_read_relative_path(read_ref)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = source_path.read_bytes()
    destination.write_bytes(payload)
    return ContinuationReadWitness(
        source_path=str(source_path),
        source_relative_path=_relative_to_root(source_path, source_root),
        bundle_relative_path=_relative_to_root(destination, workspace_root) or str(destination),
        checksum=hashlib.sha256(payload).hexdigest(),
        byte_count=len(payload),
        line_count=_count_lines(payload),
    )


def _resolve_read_ref(source_root: Path, read_ref: str) -> Path:
    candidate = Path(read_ref)
    resolved = candidate.resolve() if candidate.is_absolute() else (source_root / candidate).resolve()
    try:
        resolved.relative_to(source_root)
    except ValueError as exc:
        raise KernelContextPerfectContinuationError(
            f"Required read escapes the continuation source root: {read_ref}"
        ) from exc
    return resolved


def _resolve_bundle_root(
    workspace_root: Path,
    scope_type: str,
    scope_ref: str,
    packet_type: str,
    created_at: str,
    output_root: str | Path | None,
) -> Path:
    if output_root is not None:
        candidate = Path(output_root)
        resolved = candidate.resolve() if candidate.is_absolute() else (workspace_root / candidate).resolve()
    else:
        slug = _slugify(f"{scope_type}_{scope_ref}_{packet_type}_{created_at}")
        resolved = (
            workspace_root / "ION/05_context/history/context_perfect_continuation" / slug
        ).resolve()
    try:
        resolved.relative_to(workspace_root)
    except ValueError as exc:
        raise KernelContextPerfectContinuationError(
            "Continuation proof bundle must remain within the workspace root."
        ) from exc
    return resolved


def _bundle_read_relative_path(read_ref: str) -> str:
    candidate = Path(read_ref)
    if candidate.is_absolute():
        return f"external/{_slugify(read_ref)}"
    clean = candidate.as_posix().strip("/")
    if not clean or clean.startswith("../"):
        raise KernelContextPerfectContinuationError(
            f"Invalid relative required read for continuation proof: {read_ref}"
        )
    return clean


def _split_scope_binding(scope_binding: str) -> tuple[str, str]:
    scope_type, sep, scope_ref = scope_binding.partition(":")
    normalized_scope_type = scope_type.strip().upper()
    normalized_scope_ref = scope_ref.strip()
    if not sep or not normalized_scope_type or not normalized_scope_ref:
        raise KernelContextPerfectContinuationError(
            f"Invalid scope binding for continuation proof: {scope_binding!r}"
        )
    return normalized_scope_type, normalized_scope_ref


def _normalize_scope_filter(
    scope_type: str | None,
    scope_ref: str | None,
) -> tuple[str, str] | None:
    if scope_type is None and scope_ref is None:
        return None
    if not scope_type or not scope_ref:
        raise KernelContextPerfectContinuationError(
            "scope_type and scope_ref must be provided together."
        )
    return scope_type.strip().upper(), scope_ref.strip()


def _relative_to_root(path: Path, root: Path) -> str | None:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return None


def _content_checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _count_lines(payload: bytes) -> int:
    if not payload:
        return 0
    return payload.count(b"\n") + (0 if payload.endswith(b"\n") else 1)


def _slugify(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "continuation"


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
