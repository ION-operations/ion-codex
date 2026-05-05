"""Bounded horizon-state persistence and tightening for the live ION kernel stack.

K3 turns the doctrine of immediate / near / far orchestration into machine-readable
kernel state. The helper in this module may tighten horizon pressure toward one next
window, but it must not silently skip packet law.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re

from .index import KernelIndex
from .model import HorizonEnactmentReceipt, HorizonLayer, HorizonRecord, HorizonWorkItem
from .packet_validation import validate_packet_text
from .store import KernelStore


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")
_ALLOWED_PRIORITIES = frozenset({"P0_CRITICAL", "P1_HIGH", "P2_NORMAL", "P3_LOW"})
_PRIORITY_ORDER = {"P0_CRITICAL": 0, "P1_HIGH": 1, "P2_NORMAL": 2, "P3_LOW": 3}
_ENACTABLE_PACKET_TYPES = frozenset({"handoff", "role_session", "cursor_handoff", "manual_automation_fallback"})


class KernelHorizonStateError(Exception):
    """Raised when one bounded horizon-state operation cannot be prepared lawfully."""


@dataclass(frozen=True)
class HorizonStatePreparation:
    record: HorizonRecord
    replaced_existing: bool


@dataclass(frozen=True)
class HorizonStateResult:
    preparation: HorizonStatePreparation
    persisted_record: HorizonRecord


@dataclass(frozen=True)
class HorizonScopeSummary:
    scope_type: str
    scope_ref: str
    immediate: HorizonRecord | None = None
    near: HorizonRecord | None = None
    far: HorizonRecord | None = None

    @property
    def state_refs(self) -> tuple[str, ...]:
        refs = []
        for record in (self.immediate, self.near, self.far):
            if record is not None:
                refs.append(record.horizon_id)
        return tuple(refs)

    def compact_summary(self) -> str:
        parts: list[str] = []
        for record in (self.immediate, self.near, self.far):
            if record is not None:
                parts.append(f"{record.horizon_layer.value}={len(record.work_items)}")
        return "; ".join(parts) or "no-horizon-state"


@dataclass(frozen=True)
class HorizonTighteningResult:
    scope_type: str
    scope_ref: str
    status: str
    source_layer: HorizonLayer | None
    source_horizon_ids: tuple[str, ...]
    candidate_item: HorizonWorkItem | None
    candidate_summary: str | None
    packet_ready: bool
    packet_type_hint: str | None
    requested_reads: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    next_window_hint: str | None = None


@dataclass(frozen=True)
class HorizonPacketEnactmentResult:
    scope_type: str
    scope_ref: str
    status: str
    packet_type: str | None
    source_layer: HorizonLayer | None
    source_horizon_ids: tuple[str, ...]
    candidate_item_id: str | None
    candidate_title: str | None
    packet_path: str | None
    packet_relative_path: str | None
    receipt_id: str | None
    content: str | None
    valid: bool
    requested_reads: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


class KernelHorizonStateManager:
    """Persist and tighten immediate / near / far horizon records."""

    def prepare_record(
        self,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        horizon_layer: HorizonLayer,
        summary: str,
        work_items: tuple[HorizonWorkItem, ...] = (),
        governing_refs: tuple[str, ...] = (),
        linked_manifest_id: str | None = None,
        linked_automation_state_id: str | None = None,
        horizon_id: str | None = None,
        created_at: str | None = None,
        updated_at: str | None = None,
        notes: str | None = None,
    ) -> HorizonStatePreparation:
        scope_type = scope_type.strip().upper()
        scope_ref = scope_ref.strip()
        summary = summary.strip()
        if not scope_type or not scope_ref:
            raise KernelHorizonStateError("scope_type and scope_ref are required")
        if not summary:
            raise KernelHorizonStateError("summary is required")

        normalized_items = self._normalize_items(horizon_layer, work_items)
        if horizon_layer is HorizonLayer.IMMEDIATE and not normalized_items:
            raise KernelHorizonStateError("IMMEDIATE horizon requires at least one work item")

        resolved_horizon_id = horizon_id or horizon_record_id(scope_type, scope_ref, horizon_layer)
        existing = index.get("horizon_state", resolved_horizon_id)
        timestamp = updated_at or _iso_now()
        record = HorizonRecord(
            horizon_id=resolved_horizon_id,
            created_at=created_at or getattr(existing, "created_at", timestamp),
            updated_at=timestamp,
            scope_type=scope_type,
            scope_ref=scope_ref,
            horizon_layer=horizon_layer,
            summary=summary,
            work_items=normalized_items,
            governing_refs=tuple(governing_refs),
            linked_manifest_id=linked_manifest_id,
            linked_automation_state_id=linked_automation_state_id,
            notes=notes,
        )
        return HorizonStatePreparation(record=record, replaced_existing=existing is not None)

    def upsert_record(self, store: KernelStore, index: KernelIndex, **kwargs: object) -> HorizonStateResult:
        preparation = self.prepare_record(index, **kwargs)
        if preparation.replaced_existing:
            store.replace(preparation.record)
            index.record_changed(preparation.record)
        else:
            store.create(preparation.record)
            index.record_added(preparation.record)
        return HorizonStateResult(preparation=preparation, persisted_record=preparation.record)

    def scope_summary(self, index: KernelIndex, scope_type: str, scope_ref: str) -> HorizonScopeSummary:
        normalized_scope_type = scope_type.strip().upper()
        normalized_scope_ref = scope_ref.strip()
        records = [
            record
            for record in index.horizon_states_for_scope(normalized_scope_type, normalized_scope_ref)
            if isinstance(record, HorizonRecord)
        ]
        latest = {
            layer: self._latest_for_layer(records, layer)
            for layer in HorizonLayer
        }
        return HorizonScopeSummary(
            scope_type=normalized_scope_type,
            scope_ref=normalized_scope_ref,
            immediate=latest[HorizonLayer.IMMEDIATE],
            near=latest[HorizonLayer.NEAR],
            far=latest[HorizonLayer.FAR],
        )

    def tighten_for_scope(self, index: KernelIndex, scope_type: str, scope_ref: str) -> HorizonTighteningResult:
        summary = self.scope_summary(index, scope_type, scope_ref)
        records = [record for record in (summary.immediate, summary.near, summary.far) if record is not None]
        if not records:
            return HorizonTighteningResult(
                scope_type=summary.scope_type,
                scope_ref=summary.scope_ref,
                status="NO_HORIZON_STATE",
                source_layer=None,
                source_horizon_ids=(),
                candidate_item=None,
                candidate_summary=None,
                packet_ready=False,
                packet_type_hint=None,
                warnings=("No horizon records are available for this scope.",),
            )

        source_record = next((record for record in (summary.immediate, summary.near, summary.far) if record and record.work_items), None)
        if source_record is None:
            return HorizonTighteningResult(
                scope_type=summary.scope_type,
                scope_ref=summary.scope_ref,
                status="NO_WORK_ITEMS",
                source_layer=None,
                source_horizon_ids=summary.state_refs,
                candidate_item=None,
                candidate_summary=None,
                packet_ready=False,
                packet_type_hint=None,
                warnings=("Horizon records exist but contain no work items.",),
            )

        candidate = self._select_candidate(source_record)
        warnings: list[str] = []
        if candidate is None:
            return HorizonTighteningResult(
                scope_type=summary.scope_type,
                scope_ref=summary.scope_ref,
                status="NO_WORK_ITEMS",
                source_layer=source_record.horizon_layer,
                source_horizon_ids=summary.state_refs,
                candidate_item=None,
                candidate_summary=source_record.summary,
                packet_ready=False,
                packet_type_hint=None,
                warnings=("No selectable horizon work item was found.",),
            )

        packet_ready = self._candidate_packet_ready(source_record.horizon_layer, candidate)
        if not packet_ready:
            if candidate.dependency_refs:
                warnings.append("Candidate still carries unresolved dependencies.")
            if source_record.horizon_layer is not HorizonLayer.IMMEDIATE and not candidate.packet_ready:
                warnings.append("Candidate is not yet packet-ready and must still be packetized explicitly.")
            status = "REQUIRES_PACKETIZATION"
        else:
            status = "READY_IMMEDIATE"

        if source_record.horizon_layer is HorizonLayer.FAR:
            warnings.append("Candidate originated from FAR horizon and should be tightened through explicit review.")

        requested_reads = tuple(dict.fromkeys(tuple(source_record.governing_refs) + tuple(candidate.target_refs)))
        return HorizonTighteningResult(
            scope_type=summary.scope_type,
            scope_ref=summary.scope_ref,
            status=status,
            source_layer=source_record.horizon_layer,
            source_horizon_ids=summary.state_refs,
            candidate_item=candidate,
            candidate_summary=source_record.summary,
            packet_ready=packet_ready,
            packet_type_hint=("handoff" if packet_ready else "role_session"),
            requested_reads=requested_reads,
            warnings=tuple(warnings),
            next_window_hint=candidate.next_window_hint,
        )

    def render_report(self, record: HorizonRecord) -> str:
        lines = [
            f"# Horizon State — {record.scope_type}:{record.scope_ref}",
            "",
            f"- Layer: {record.horizon_layer.value}",
            f"- Summary: {record.summary}",
            f"- Work Item Count: {len(record.work_items)}",
        ]
        if record.linked_manifest_id:
            lines.append(f"- Linked Manifest: {record.linked_manifest_id}")
        if record.linked_automation_state_id:
            lines.append(f"- Linked Automation State: {record.linked_automation_state_id}")
        lines.extend(["", "## Work Items", ""])
        if not record.work_items:
            lines.append("- NONE")
        else:
            for item in record.work_items:
                readiness = "READY" if item.packet_ready else "PENDING"
                executor = item.executor_hint or "UNSPECIFIED"
                lines.append(f"- {item.item_id}: {item.title} [{readiness}] priority={item.priority} executor={executor}")
                lines.append(f"  - {item.summary}")
                if item.target_refs:
                    lines.append(f"  - targets: {', '.join(item.target_refs)}")
                if item.dependency_refs:
                    lines.append(f"  - dependencies: {', '.join(item.dependency_refs)}")
        return "\n".join(lines) + "\n"

    def render_scope_projection(self, index: KernelIndex, scope_type: str, scope_ref: str) -> dict[str, object]:
        summary = self.scope_summary(index, scope_type, scope_ref)
        tightening = self.tighten_for_scope(index, scope_type, scope_ref)
        return {
            "scope_type": summary.scope_type,
            "scope_ref": summary.scope_ref,
            "records": {
                "IMMEDIATE": _record_projection(summary.immediate),
                "NEAR": _record_projection(summary.near),
                "FAR": _record_projection(summary.far),
            },
            "tightening": {
                "status": tightening.status,
                "source_layer": (None if tightening.source_layer is None else tightening.source_layer.value),
                "packet_ready": tightening.packet_ready,
                "packet_type_hint": tightening.packet_type_hint,
                "candidate_item_id": (None if tightening.candidate_item is None else tightening.candidate_item.item_id),
                "candidate_title": (None if tightening.candidate_item is None else tightening.candidate_item.title),
                "candidate_summary": tightening.candidate_summary,
                "requested_reads": list(tightening.requested_reads),
                "warnings": list(tightening.warnings),
                "next_window_hint": tightening.next_window_hint,
            },
        }

    def latest_enactment_receipt(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> HorizonEnactmentReceipt | None:
        if scope_type is not None and scope_ref is not None:
            receipts = index.horizon_enactment_receipts_for_scope(scope_type.strip().upper(), scope_ref.strip())
        else:
            receipts = index.records_by_type("horizon_enactment_receipt")
        typed = [record for record in receipts if isinstance(record, HorizonEnactmentReceipt)]
        if not typed:
            return None
        typed.sort(key=lambda item: (item.created_at, item.receipt_id))
        return typed[-1]

    def render_enactment_receipt_projection(self, receipt: HorizonEnactmentReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_layer": (None if receipt.source_layer is None else receipt.source_layer.value),
            "source_horizon_ids": list(receipt.source_horizon_ids),
            "candidate_item_id": receipt.candidate_item_id,
            "candidate_title": receipt.candidate_title,
            "packet_type": receipt.packet_type,
            "packet_path": receipt.packet_path,
            "packet_relative_path": receipt.packet_relative_path,
            "requested_reads": list(receipt.requested_reads),
            "warnings": list(receipt.warnings),
        }

    def enact_packet_for_scope(
        self,
        index: KernelIndex,
        scope_type: str,
        scope_ref: str,
        *,
        store: KernelStore | None = None,
        packet_type: str | None = None,
        workspace_root: str | Path | None = None,
        output_path: str | Path | None = None,
        created_at: str | None = None,
        status: str = "ACTIVE",
        sender: str | None = None,
        receiver: str | None = None,
        target_surface: str | None = None,
        automation_surface: str | None = None,
        reason: str | None = None,
    ) -> HorizonPacketEnactmentResult:
        tightening = self.tighten_for_scope(index, scope_type, scope_ref)
        candidate = tightening.candidate_item
        if candidate is None or not tightening.packet_ready:
            return HorizonPacketEnactmentResult(
                scope_type=tightening.scope_type,
                scope_ref=tightening.scope_ref,
                status=f"REFUSED_{tightening.status}",
                packet_type=None,
                source_layer=tightening.source_layer,
                source_horizon_ids=tightening.source_horizon_ids,
                candidate_item_id=(None if candidate is None else candidate.item_id),
                candidate_title=(None if candidate is None else candidate.title),
                packet_path=None,
                packet_relative_path=None,
                receipt_id=None,
                content=None,
                valid=False,
                requested_reads=tightening.requested_reads,
                warnings=tightening.warnings,
            )

        resolved_packet_type = (packet_type or tightening.packet_type_hint or "handoff").strip().lower()
        if resolved_packet_type not in _ENACTABLE_PACKET_TYPES:
            raise KernelHorizonStateError(f"Unsupported horizon enactment packet type: {resolved_packet_type}")

        content = self._render_packet_enactment(
            tightening,
            packet_type=resolved_packet_type,
            created_at=(created_at or _iso_now()),
            status=status.strip() or "ACTIVE",
            sender=((sender or "HORIZON").strip() or "HORIZON"),
            receiver=((receiver or candidate.executor_hint or "OPERATOR").strip() or "OPERATOR"),
            target_surface=((target_surface or candidate.executor_hint or "IDE chat / executor").strip() or "IDE chat / executor"),
            automation_surface=((automation_surface or "horizon enactment bridge").strip() or "horizon enactment bridge"),
            reason=((reason or "packet-ready horizon candidate requires explicit operator enactment").strip() or "packet-ready horizon candidate requires explicit operator enactment"),
        )
        validation = validate_packet_text(content, expected_type=resolved_packet_type)
        if not validation.valid:
            codes = ", ".join(message.code for message in validation.errors) or "unknown"
            raise KernelHorizonStateError(f"Rendered horizon enactment packet failed validation: {codes}")

        packet_path: str | None = None
        packet_relative_path: str | None = None
        if output_path is not None:
            resolved_output = self._resolve_output_path(workspace_root, output_path)
            resolved_output.parent.mkdir(parents=True, exist_ok=True)
            resolved_output.write_text(content, encoding="utf-8")
            packet_path = str(resolved_output)
            if workspace_root is not None:
                try:
                    packet_relative_path = str(resolved_output.relative_to(Path(workspace_root).resolve()))
                except ValueError:
                    packet_relative_path = str(resolved_output)

        receipt_id = None
        if store is not None:
            receipt = self._persist_enactment_receipt(
                store,
                index,
                tightening=tightening,
                packet_type=resolved_packet_type,
                packet_path=packet_path,
                packet_relative_path=packet_relative_path,
                created_at=(created_at or _iso_now()),
            )
            receipt_id = receipt.receipt_id

        warnings = list(tightening.warnings)
        warnings.append("Generated scaffold remains within canonical packet law; operator intent is still required to execute it.")
        return HorizonPacketEnactmentResult(
            scope_type=tightening.scope_type,
            scope_ref=tightening.scope_ref,
            status="ENACTED",
            packet_type=resolved_packet_type,
            source_layer=tightening.source_layer,
            source_horizon_ids=tightening.source_horizon_ids,
            candidate_item_id=candidate.item_id,
            candidate_title=candidate.title,
            packet_path=packet_path,
            packet_relative_path=packet_relative_path,
            receipt_id=receipt_id,
            content=content,
            valid=True,
            requested_reads=tightening.requested_reads,
            warnings=tuple(warnings),
        )

    def _persist_enactment_receipt(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        tightening: HorizonTighteningResult,
        packet_type: str,
        packet_path: str | None,
        packet_relative_path: str | None,
        created_at: str,
    ) -> HorizonEnactmentReceipt:
        candidate = _required_candidate(tightening)
        receipt = HorizonEnactmentReceipt(
            receipt_id=horizon_enactment_receipt_id(
                tightening.scope_type,
                tightening.scope_ref,
                candidate.item_id,
                created_at,
            ),
            created_at=created_at,
            scope_type=tightening.scope_type,
            scope_ref=tightening.scope_ref,
            source_horizon_ids=tightening.source_horizon_ids,
            source_layer=tightening.source_layer,
            candidate_item_id=candidate.item_id,
            candidate_title=candidate.title,
            packet_type=packet_type,
            packet_path=packet_path,
            packet_relative_path=packet_relative_path,
            requested_reads=tightening.requested_reads,
            warnings=_enactment_warnings(tightening),
        )
        if index.exists("horizon_enactment_receipt", receipt.receipt_id):
            store.replace(receipt)
            index.record_changed(receipt)
        else:
            store.create(receipt)
            index.record_added(receipt)
        return receipt

    def _normalize_items(self, horizon_layer: HorizonLayer, work_items: tuple[HorizonWorkItem, ...]) -> tuple[HorizonWorkItem, ...]:
        normalized: list[HorizonWorkItem] = []
        seen_ids: set[str] = set()
        for item in work_items:
            item_id = item.item_id.strip()
            title = item.title.strip()
            summary = item.summary.strip()
            priority = item.priority.strip().upper() or "P2_NORMAL"
            if not item_id or not title or not summary:
                raise KernelHorizonStateError("each horizon work item requires item_id, title, and summary")
            if item_id in seen_ids:
                raise KernelHorizonStateError("horizon work item ids must be unique within one record")
            if priority not in _ALLOWED_PRIORITIES:
                raise KernelHorizonStateError(f"Unsupported horizon work item priority: {item.priority}")
            if horizon_layer is HorizonLayer.IMMEDIATE:
                if not item.packet_ready:
                    raise KernelHorizonStateError("IMMEDIATE horizon items must already be packet_ready")
                if item.dependency_refs:
                    raise KernelHorizonStateError("IMMEDIATE horizon items must not carry unresolved dependencies")
                if not (item.executor_hint or "").strip():
                    raise KernelHorizonStateError("IMMEDIATE horizon items require executor_hint")
            seen_ids.add(item_id)
            normalized.append(
                HorizonWorkItem(
                    item_id=item_id,
                    title=title,
                    summary=summary,
                    executor_hint=((item.executor_hint or "").strip() or None),
                    target_refs=tuple(str(ref).strip() for ref in item.target_refs if str(ref).strip()),
                    dependency_refs=tuple(str(ref).strip() for ref in item.dependency_refs if str(ref).strip()),
                    packet_ready=bool(item.packet_ready),
                    priority=priority,
                    blocking_notes=tuple(str(note).strip() for note in item.blocking_notes if str(note).strip()),
                    next_window_hint=((item.next_window_hint or "").strip() or None),
                )
            )
        return tuple(normalized)

    @staticmethod
    def _latest_for_layer(records: list[HorizonRecord], layer: HorizonLayer) -> HorizonRecord | None:
        candidates = [record for record in records if record.horizon_layer is layer]
        if not candidates:
            return None
        candidates.sort(key=lambda item: (item.updated_at, item.horizon_id))
        return candidates[-1]

    @staticmethod
    def _select_candidate(record: HorizonRecord) -> HorizonWorkItem | None:
        if not record.work_items:
            return None
        return sorted(
            record.work_items,
            key=lambda item: (
                _PRIORITY_ORDER.get(item.priority, 99),
                0 if item.packet_ready else 1,
                item.item_id,
            ),
        )[0]

    @staticmethod
    def _candidate_packet_ready(layer: HorizonLayer, item: HorizonWorkItem) -> bool:
        if layer is HorizonLayer.IMMEDIATE:
            return True
        return bool(item.packet_ready and not item.dependency_refs and (item.executor_hint or "").strip())

    @staticmethod
    def _resolve_output_path(workspace_root: str | Path | None, output_path: str | Path) -> Path:
        candidate = Path(output_path)
        if candidate.is_absolute():
            return candidate.resolve()
        if workspace_root is None:
            return candidate.resolve()
        return (Path(workspace_root).resolve() / candidate).resolve()

    def _render_packet_enactment(
        self,
        tightening: HorizonTighteningResult,
        *,
        packet_type: str,
        created_at: str,
        status: str,
        sender: str,
        receiver: str,
        target_surface: str,
        automation_surface: str,
        reason: str,
    ) -> str:
        candidate = tightening.candidate_item
        if candidate is None:
            raise KernelHorizonStateError("Cannot render enactment packet without a candidate item")
        if packet_type == "handoff":
            return _render_handoff_packet(tightening, created_at=created_at, status=status, sender=sender, receiver=receiver)
        if packet_type == "role_session":
            return _render_role_session_packet(tightening, created_at=created_at, status=status, role=receiver)
        if packet_type == "cursor_handoff":
            return _render_cursor_handoff_packet(tightening, created_at=created_at, status=status, target_surface=target_surface)
        if packet_type == "manual_automation_fallback":
            return _render_manual_fallback_packet(
                tightening,
                created_at=created_at,
                status=status,
                automation_surface=automation_surface,
                reason=reason,
                operator=receiver,
            )
        raise KernelHorizonStateError(f"Unhandled horizon enactment packet type: {packet_type}")


IonHorizonStateManager = KernelHorizonStateManager


def horizon_record_id(scope_type: str, scope_ref: str, horizon_layer: HorizonLayer) -> str:
    clean_scope_type = _SAFE_ID_RE.sub("-", scope_type.lower()).strip("-") or "scope"
    clean_scope_ref = _SAFE_ID_RE.sub("-", scope_ref.lower()).strip("-") or "state"
    return f"horizon-{clean_scope_type}-{clean_scope_ref}-{horizon_layer.value.lower()}"


def horizon_enactment_receipt_id(scope_type: str, scope_ref: str, candidate_item_id: str, created_at: str) -> str:
    clean_scope_type = _SAFE_ID_RE.sub("-", scope_type.lower()).strip("-") or "scope"
    clean_scope_ref = _SAFE_ID_RE.sub("-", scope_ref.lower()).strip("-") or "state"
    clean_item = _SAFE_ID_RE.sub("-", candidate_item_id.lower()).strip("-") or "candidate"
    clean_created_at = _SAFE_ID_RE.sub("-", created_at.lower()).strip("-") or "timestamp"
    return f"horizon-enactment-{clean_scope_type}-{clean_scope_ref}-{clean_item}-{clean_created_at}"


def _record_projection(record: HorizonRecord | None) -> dict[str, object] | None:
    if record is None:
        return None
    return {
        "horizon_id": record.horizon_id,
        "updated_at": record.updated_at,
        "summary": record.summary,
        "work_item_count": len(record.work_items),
    }


def _render_handoff_packet(
    tightening: HorizonTighteningResult,
    *,
    created_at: str,
    status: str,
    sender: str,
    receiver: str,
) -> str:
    candidate = _required_candidate(tightening)
    lines = [
        "---",
        "type: handoff",
        "template: HANDOFF",
        f"created: {created_at}",
        f"status: {status}",
        f"from: {sender}",
        f"to: {receiver}",
        f"objective: {candidate.title}",
        "---",
        "",
        f"# Handoff: {candidate.title}",
        "",
        "## From",
        "",
        sender,
        "",
        "## To",
        "",
        receiver,
        "",
        "## What was completed",
        "",
        f"- Tightened a packet-ready horizon candidate for `{tightening.scope_type}:{tightening.scope_ref}`.",
        f"- scope: {tightening.scope_type}:{tightening.scope_ref}",
        f"- Source layer: {tightening.source_layer.value if tightening.source_layer is not None else 'UNKNOWN'}.",
        "- Preserved the candidate inside the canonical packet family rather than bypassing packet law.",
        "",
        "## What remains",
        "",
        f"- Execute the bounded step `{candidate.title}`.",
        f"- Preserve follow-up proof and handoff state for `{tightening.scope_type}:{tightening.scope_ref}`.",
        "",
        "## Exact artifacts to read",
        "",
    ]
    lines.extend(_render_bullets(tightening.requested_reads, empty_text="- no explicit read refs were carried by the tightened candidate"))
    lines.extend([
        "",
        "## Risks / warnings",
        "",
    ])
    lines.extend(_render_bullets(_enactment_warnings(tightening), empty_text="- bounded enactment scaffold only"))
    lines.extend([
        "",
        "## Requested next action",
        "",
        f"- Carry `{candidate.title}` through the normal supervised or manual execution loop.",
    ])
    return "\n".join(lines) + "\n"


def _render_role_session_packet(
    tightening: HorizonTighteningResult,
    *,
    created_at: str,
    status: str,
    role: str,
) -> str:
    candidate = _required_candidate(tightening)
    lines = [
        "---",
        "type: role_session",
        "template: ROLE_SESSION",
        f"created: {created_at}",
        f"status: {status}",
        f"role: {role}",
        f"objective: {candidate.title}",
        "---",
        "",
        f"# Role Session: {role}",
        "",
        "## Role",
        "",
        role,
        "",
        "## Purpose",
        "",
        f"Execute the packet-ready horizon candidate `{candidate.title}` without leaving canonical packet law.",
        "",
        "## Source Task / Objective",
        "",
        f"- scope: {tightening.scope_type}:{tightening.scope_ref}",
        f"- objective: {candidate.summary}",
        "",
        "## Required Reads",
        "",
    ]
    lines.extend(_render_bullets(tightening.requested_reads, empty_text="- no explicit read refs were carried by the tightened candidate"))
    lines.extend([
        "",
        "## Expected Output",
        "",
        "- one bounded execution pass",
        "- preserved follow-up packet or refusal if new blockers appear",
        "",
        "## Next Target",
        "",
        "- next_role: operator or explicit follow-up executor",
        "",
        "## Notes",
        "",
    ])
    lines.extend(_render_bullets(_enactment_warnings(tightening), empty_text="- bounded enactment scaffold only"))
    return "\n".join(lines) + "\n"


def _render_cursor_handoff_packet(
    tightening: HorizonTighteningResult,
    *,
    created_at: str,
    status: str,
    target_surface: str,
) -> str:
    candidate = _required_candidate(tightening)
    lines = [
        "---",
        "type: cursor_handoff",
        "template: CURSOR_HANDOFF",
        f"created: {created_at}",
        f"status: {status}",
        f"target_surface: {target_surface}",
        f"objective: {candidate.title}",
        "---",
        "",
        f"# Cursor Handoff: {candidate.title}",
        "",
        "## Role / chassis target",
        "",
        target_surface,
        "",
        "## Load order",
        "",
        "1. horizon tightening projection",
        "2. required read refs",
        "3. target scope files",
        "",
        "## Exact files to read first",
        "",
    ]
    lines.extend(_render_bullets(tightening.requested_reads, empty_text="- no explicit read refs were carried by the tightened candidate"))
    lines.extend([
        "",
        "## Task to perform",
        "",
        f"- scope: {tightening.scope_type}:{tightening.scope_ref}",
        f"- bounded step: Carry the packet-ready horizon candidate `{candidate.title}` into one bounded execution pass.",
        "",
        "## Boundaries",
        "",
    ])
    lines.extend(_render_bullets(_enactment_warnings(tightening), empty_text="- no hidden packet emission"))
    lines.extend([
        "",
        "## Expected output artifact",
        "",
        "- one canonical packet or bounded execution artifact tied to this scope",
    ])
    return "\n".join(lines) + "\n"


def _render_manual_fallback_packet(
    tightening: HorizonTighteningResult,
    *,
    created_at: str,
    status: str,
    automation_surface: str,
    reason: str,
    operator: str,
) -> str:
    candidate = _required_candidate(tightening)
    lines = [
        "---",
        "type: manual_automation_fallback",
        "template: MANUAL_AUTOMATION_FALLBACK",
        f"created: {created_at}",
        f"status: {status}",
        f"automation_surface: {automation_surface}",
        f"reason: {reason}",
        "---",
        "",
        f"# Manual Automation Fallback: {candidate.title}",
        "",
        "## Carrier blocked or disabled",
        "",
        f"- Automation carrier / service: {automation_surface}",
        f"- Why unavailable: {reason}",
        "- Current automation mode / operator-control posture: explicit operator enactment",
        "",
        "## Lawful bounded inputs",
        "",
        f"- Governing task / manifest / packet refs: {', '.join(tightening.requested_reads) if tightening.requested_reads else 'none recorded'}",
        f"- Current scope / work id: {tightening.scope_type}:{tightening.scope_ref}",
        "- Allowed writes: one enacted packet scaffold or its direct successor",
        "- Blocking review / policy state: none beyond preserved packet law",
        "",
        "## Manual fallback step",
        "",
        f"- Exact single step being carried manually: {candidate.title}",
        "- Expected output family: canonical packet family",
        f"- Proposed follow-up / handoff target: {operator}",
        "",
        "## Outputs emitted",
        "",
        "- Receipts / signals / handoff generated: bounded enactment scaffold",
        "- Proposal surfaces generated: none beyond the canonical packet",
        f"- Unresolved risk preserved: {'; '.join(_enactment_warnings(tightening))}",
    ]
    return "\n".join(lines) + "\n"


def _required_candidate(tightening: HorizonTighteningResult) -> HorizonWorkItem:
    if tightening.candidate_item is None:
        raise KernelHorizonStateError("enactment requires one tightened horizon candidate")
    return tightening.candidate_item


def _enactment_warnings(tightening: HorizonTighteningResult) -> tuple[str, ...]:
    base = list(tightening.warnings)
    base.append("generated scaffold only; operator judgment remains required")
    return tuple(dict.fromkeys(base))


def _render_bullets(items: tuple[str, ...] | list[str], *, empty_text: str) -> list[str]:
    values = [str(item).strip() for item in items if str(item).strip()]
    if not values:
        return [empty_text]
    return [f"- {item}" for item in values]


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
