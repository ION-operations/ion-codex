"""Runtime/session authority store.

Target 1 reincorporation slice:

- Establish a first-class runtime/session authority center (persisted session + queue state
  and receipts).
- Keep it distinct from scheduler law, activation authority, and reporting.

This module is deliberately small and boring. It is not a daemon loop, not a server,
and not a scheduler. It is the durable substrate that runtime/session reintegration
can build on without collapsing boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import uuid
from typing import Any, Iterable, Optional

from .model import KernelRecord, StrEnum


_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_id(value: str, label: str) -> str:
    if not _ID_RE.match(value) or ".." in value or "/" in value or "\\" in value:
        raise RuntimeSessionStoreError(f"Invalid {label}: {value!r}")
    return value


class RuntimeSessionStoreError(Exception):
    """Raised when one runtime/session store operation fails."""


class RuntimeSessionEvent(StrEnum):
    CREATED = "CREATED"
    CARRIER_BOUND = "CARRIER_BOUND"
    CONTEXT_BOUND = "CONTEXT_BOUND"
    QUEUE_ITEM_ADDED = "QUEUE_ITEM_ADDED"
    QUEUE_ITEM_STATUS_UPDATED = "QUEUE_ITEM_STATUS_UPDATED"
    DISPATCHED_WORK_UNIT = "DISPATCHED_WORK_UNIT"
    PAUSED = "PAUSED"
    REENTERED = "REENTERED"
    CLOSED = "CLOSED"


class RuntimeCarrierKind(StrEnum):
    IDE_MANUAL = "IDE_MANUAL"
    SUPERVISED_RUNTIME = "SUPERVISED_RUNTIME"
    EXTERNAL_API = "EXTERNAL_API"
    SWARM_CHILD = "SWARM_CHILD"


class RuntimeSessionLifecycleState(StrEnum):
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    CLOSED = "CLOSED"


class SessionQueueItemStatus(StrEnum):
    PENDING = "PENDING"
    DISPATCH_READY = "DISPATCH_READY"
    DISPATCHED = "DISPATCHED"
    DONE = "DONE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class RuntimeSessionIdentity(KernelRecord):
    session_id: str
    created_at: str
    label: str | None = None
    purpose: str | None = None


@dataclass(frozen=True)
class RuntimeSessionAuthority(KernelRecord):
    authority_id: str
    session_id: str
    created_at: str
    root_authority_ref: str
    lifecycle_state: RuntimeSessionLifecycleState = RuntimeSessionLifecycleState.ACTIVE
    updated_at: str | None = None
    notes: str | None = None
    last_transition_detail: str | None = None


@dataclass(frozen=True)
class RuntimeSessionCarrierBinding(KernelRecord):
    binding_id: str
    session_id: str
    bound_at: str
    carrier_kind: RuntimeCarrierKind
    carrier_ref: str


@dataclass(frozen=True)
class RuntimeSessionContextBinding(KernelRecord):
    binding_id: str
    session_id: str
    bound_at: str
    context_version: str
    context_ref: str


@dataclass(frozen=True)
class RuntimeSessionReceipt(KernelRecord):
    receipt_id: str
    event: RuntimeSessionEvent
    session_id: str
    created_at: str
    detail: str
    witness_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class SessionQueueItem(KernelRecord):
    item_id: str
    created_at: str
    status: SessionQueueItemStatus
    work_unit_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SessionQueue(KernelRecord):
    session_id: str
    updated_at: str
    items: tuple[SessionQueueItem, ...] = ()


def _json_dump(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _json_read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class RuntimeSessionStore:
    """Filesystem-backed runtime/session authority center."""

    def __init__(self, root_dir: str | Path) -> None:
        self.root = Path(root_dir)
        self.base = self.root / "runtime_sessions"
        self.sessions_dir = self.base / "sessions"
        self.authorities_dir = self.base / "authorities"
        self.carrier_dir = self.base / "carrier_bindings"
        self.context_dir = self.base / "context_bindings"
        self.receipts_dir = self.base / "receipts"
        self.queues_dir = self.base / "queues"
        for d in (
            self.sessions_dir,
            self.authorities_dir,
            self.carrier_dir,
            self.context_dir,
            self.receipts_dir,
            self.queues_dir,
        ):
            d.mkdir(parents=True, exist_ok=True)

    # --- paths ---

    def _session_path(self, session_id: str) -> Path:
        return self.sessions_dir / f"{_validate_id(session_id, 'session_id')}.json"

    def _authority_path(self, session_id: str) -> Path:
        return self.authorities_dir / f"{_validate_id(session_id, 'session_id')}.json"

    def _carrier_path(self, session_id: str) -> Path:
        return self.carrier_dir / f"{_validate_id(session_id, 'session_id')}.json"

    def _context_path(self, session_id: str) -> Path:
        return self.context_dir / f"{_validate_id(session_id, 'session_id')}.json"

    def _queue_path(self, session_id: str) -> Path:
        return self.queues_dir / f"{_validate_id(session_id, 'session_id')}.json"

    def _receipt_path(self, receipt_id: str) -> Path:
        return self.receipts_dir / f"{_validate_id(receipt_id, 'receipt_id')}.json"

    def _write_authority(self, authority: RuntimeSessionAuthority) -> None:
        payload = authority.to_dict()
        payload["lifecycle_state"] = str(authority.lifecycle_state)
        _json_dump(self._authority_path(authority.session_id), payload)

    # --- session ---

    def create_receipt(
        self,
        session_id: str,
        *,
        event: RuntimeSessionEvent,
        detail: str,
        witness_paths: Iterable[str] = (),
        created_at: str | None = None,
        receipt_id: str | None = None,
    ) -> RuntimeSessionReceipt:
        if not self.exists(session_id):
            raise RuntimeSessionStoreError(f"Missing session: {session_id}")
        receipt = RuntimeSessionReceipt(
            receipt_id=receipt_id or f"rsr-{uuid.uuid4().hex[:12]}",
            event=event,
            session_id=session_id,
            created_at=created_at or _utc_now(),
            detail=detail,
            witness_paths=tuple(witness_paths),
        )
        _json_dump(self._receipt_path(receipt.receipt_id), receipt.to_dict())
        return receipt

    def exists(self, session_id: str) -> bool:
        return self._session_path(session_id).exists()

    def list_session_ids(self) -> list[str]:
        return sorted(p.stem for p in self.sessions_dir.glob("*.json"))

    def create_session(
        self,
        session_id: str,
        *,
        root_authority_ref: str,
        label: str | None = None,
        purpose: str | None = None,
        created_at: str | None = None,
    ) -> tuple[RuntimeSessionIdentity, RuntimeSessionAuthority, RuntimeSessionReceipt]:
        if self.exists(session_id):
            raise RuntimeSessionStoreError(f"Session already exists: {session_id}")

        created_at = created_at or _utc_now()
        identity = RuntimeSessionIdentity(
            session_id=session_id,
            created_at=created_at,
            label=label,
            purpose=purpose,
        )
        authority = RuntimeSessionAuthority(
            authority_id=f"rsa-{uuid.uuid4().hex[:12]}",
            session_id=session_id,
            created_at=created_at,
            root_authority_ref=root_authority_ref,
            lifecycle_state=RuntimeSessionLifecycleState.ACTIVE,
            updated_at=created_at,
            notes=None,
            last_transition_detail="runtime session created",
        )
        queue = SessionQueue(session_id=session_id, updated_at=created_at, items=())

        receipt = RuntimeSessionReceipt(
            receipt_id=f"rsr-{uuid.uuid4().hex[:12]}",
            event=RuntimeSessionEvent.CREATED,
            session_id=session_id,
            created_at=_utc_now(),
            detail="runtime session created",
            witness_paths=(
                str(self._session_path(session_id)),
                str(self._authority_path(session_id)),
                str(self._queue_path(session_id)),
            ),
        )

        _json_dump(self._session_path(session_id), identity.to_dict())
        self._write_authority(authority)
        _json_dump(self._queue_path(session_id), queue.to_dict())
        _json_dump(self._receipt_path(receipt.receipt_id), receipt.to_dict())
        return identity, authority, receipt

    def read_identity(self, session_id: str) -> RuntimeSessionIdentity:
        path = self._session_path(session_id)
        if not path.exists():
            raise RuntimeSessionStoreError(f"Missing session: {session_id}")
        return RuntimeSessionIdentity(**_json_read(path))

    def read_authority(self, session_id: str) -> RuntimeSessionAuthority:
        path = self._authority_path(session_id)
        if not path.exists():
            raise RuntimeSessionStoreError(f"Missing session authority: {session_id}")
        payload = _json_read(path)
        payload["lifecycle_state"] = RuntimeSessionLifecycleState(
            payload.get("lifecycle_state", RuntimeSessionLifecycleState.ACTIVE.value)
        )
        payload.setdefault("updated_at", payload.get("created_at"))
        payload.setdefault("notes", None)
        payload.setdefault("last_transition_detail", None)
        return RuntimeSessionAuthority(**payload)

    def read_carrier_binding(self, session_id: str) -> RuntimeSessionCarrierBinding | None:
        path = self._carrier_path(session_id)
        if not path.exists():
            return None
        payload = _json_read(path)
        payload["carrier_kind"] = RuntimeCarrierKind(payload["carrier_kind"])
        return RuntimeSessionCarrierBinding(**payload)

    def read_context_binding(self, session_id: str) -> RuntimeSessionContextBinding | None:
        path = self._context_path(session_id)
        if not path.exists():
            return None
        return RuntimeSessionContextBinding(**_json_read(path))

    # --- bindings ---

    def bind_carrier(
        self,
        session_id: str,
        *,
        carrier_kind: RuntimeCarrierKind,
        carrier_ref: str,
        bound_at: str | None = None,
    ) -> tuple[RuntimeSessionCarrierBinding, RuntimeSessionReceipt]:
        if not self.exists(session_id):
            raise RuntimeSessionStoreError(f"Missing session: {session_id}")
        bound_at = bound_at or _utc_now()
        binding = RuntimeSessionCarrierBinding(
            binding_id=f"rsc-{uuid.uuid4().hex[:12]}",
            session_id=session_id,
            bound_at=bound_at,
            carrier_kind=carrier_kind,
            carrier_ref=carrier_ref,
        )
        receipt = RuntimeSessionReceipt(
            receipt_id=f"rsr-{uuid.uuid4().hex[:12]}",
            event=RuntimeSessionEvent.CARRIER_BOUND,
            session_id=session_id,
            created_at=_utc_now(),
            detail=f"carrier bound: {carrier_kind}",
            witness_paths=(str(self._carrier_path(session_id)),),
        )
        payload = binding.to_dict()
        payload["carrier_kind"] = str(binding.carrier_kind)
        _json_dump(self._carrier_path(session_id), payload)
        _json_dump(self._receipt_path(receipt.receipt_id), receipt.to_dict())
        return binding, receipt

    def bind_context(
        self,
        session_id: str,
        *,
        context_version: str,
        context_ref: str,
        bound_at: str | None = None,
    ) -> tuple[RuntimeSessionContextBinding, RuntimeSessionReceipt]:
        if not self.exists(session_id):
            raise RuntimeSessionStoreError(f"Missing session: {session_id}")
        bound_at = bound_at or _utc_now()
        binding = RuntimeSessionContextBinding(
            binding_id=f"rctx-{uuid.uuid4().hex[:12]}",
            session_id=session_id,
            bound_at=bound_at,
            context_version=context_version,
            context_ref=context_ref,
        )
        receipt = RuntimeSessionReceipt(
            receipt_id=f"rsr-{uuid.uuid4().hex[:12]}",
            event=RuntimeSessionEvent.CONTEXT_BOUND,
            session_id=session_id,
            created_at=_utc_now(),
            detail=f"context bound: {context_version}",
            witness_paths=(str(self._context_path(session_id)),),
        )
        _json_dump(self._context_path(session_id), binding.to_dict())
        _json_dump(self._receipt_path(receipt.receipt_id), receipt.to_dict())
        return binding, receipt

    def _transition_lifecycle_state(
        self,
        session_id: str,
        *,
        expected_states: Iterable[RuntimeSessionLifecycleState],
        next_state: RuntimeSessionLifecycleState,
        event: RuntimeSessionEvent,
        detail: str,
        transitioned_at: str | None = None,
        witness_paths: Iterable[str] = (),
    ) -> tuple[RuntimeSessionAuthority, RuntimeSessionReceipt]:
        authority = self.read_authority(session_id)
        allowed = tuple(expected_states)
        if authority.lifecycle_state not in allowed:
            allowed_render = ", ".join(str(item) for item in allowed)
            raise RuntimeSessionStoreError(
                f"Session {session_id} not in expected lifecycle state ({allowed_render}); "
                f"found {authority.lifecycle_state}"
            )
        changed_at = transitioned_at or _utc_now()
        updated = RuntimeSessionAuthority(
            authority_id=authority.authority_id,
            session_id=authority.session_id,
            created_at=authority.created_at,
            root_authority_ref=authority.root_authority_ref,
            lifecycle_state=next_state,
            updated_at=changed_at,
            notes=authority.notes,
            last_transition_detail=detail,
        )
        self._write_authority(updated)
        receipt = RuntimeSessionReceipt(
            receipt_id=f"rsr-{uuid.uuid4().hex[:12]}",
            event=event,
            session_id=session_id,
            created_at=_utc_now(),
            detail=detail,
            witness_paths=tuple(witness_paths),
        )
        _json_dump(self._receipt_path(receipt.receipt_id), receipt.to_dict())
        return updated, receipt

    def pause_session(
        self,
        session_id: str,
        *,
        detail: str = "runtime session paused",
        paused_at: str | None = None,
    ) -> tuple[RuntimeSessionAuthority, RuntimeSessionReceipt]:
        return self._transition_lifecycle_state(
            session_id,
            expected_states=(RuntimeSessionLifecycleState.ACTIVE,),
            next_state=RuntimeSessionLifecycleState.PAUSED,
            event=RuntimeSessionEvent.PAUSED,
            detail=detail,
            transitioned_at=paused_at,
            witness_paths=(
                str(self._authority_path(session_id)),
                str(self._queue_path(session_id)),
            ),
        )

    def reenter_session(
        self,
        session_id: str,
        *,
        detail: str = "runtime session re-entered",
        reentered_at: str | None = None,
        expected_carrier_ref: str | None = None,
        expected_context_version: str | None = None,
        expected_context_ref: str | None = None,
    ) -> tuple[RuntimeSessionAuthority, RuntimeSessionReceipt]:
        if (expected_context_version is None) != (expected_context_ref is None):
            raise RuntimeSessionStoreError(
                "expected_context_version and expected_context_ref must be provided together"
            )
        witness_paths = [str(self._authority_path(session_id))]
        carrier = self.read_carrier_binding(session_id)
        if expected_carrier_ref is not None:
            if carrier is None or carrier.carrier_ref != expected_carrier_ref:
                raise RuntimeSessionStoreError(
                    f"Session {session_id} carrier binding does not match expected carrier"
                )
        if carrier is not None:
            witness_paths.append(str(self._carrier_path(session_id)))
        context = self.read_context_binding(session_id)
        if expected_context_version is not None:
            if context is None or not (
                context.context_version == expected_context_version
                and context.context_ref == expected_context_ref
            ):
                raise RuntimeSessionStoreError(
                    f"Session {session_id} context binding does not match expected context"
                )
        if context is not None:
            witness_paths.append(str(self._context_path(session_id)))
        return self._transition_lifecycle_state(
            session_id,
            expected_states=(RuntimeSessionLifecycleState.PAUSED,),
            next_state=RuntimeSessionLifecycleState.ACTIVE,
            event=RuntimeSessionEvent.REENTERED,
            detail=detail,
            transitioned_at=reentered_at,
            witness_paths=tuple(witness_paths),
        )

    def close_session(
        self,
        session_id: str,
        *,
        detail: str = "runtime session closed",
        closed_at: str | None = None,
    ) -> tuple[RuntimeSessionAuthority, RuntimeSessionReceipt]:
        witness_paths = [
            str(self._authority_path(session_id)),
            str(self._queue_path(session_id)),
        ]
        if self.read_carrier_binding(session_id) is not None:
            witness_paths.append(str(self._carrier_path(session_id)))
        if self.read_context_binding(session_id) is not None:
            witness_paths.append(str(self._context_path(session_id)))
        return self._transition_lifecycle_state(
            session_id,
            expected_states=(
                RuntimeSessionLifecycleState.ACTIVE,
                RuntimeSessionLifecycleState.PAUSED,
            ),
            next_state=RuntimeSessionLifecycleState.CLOSED,
            event=RuntimeSessionEvent.CLOSED,
            detail=detail,
            transitioned_at=closed_at,
            witness_paths=tuple(witness_paths),
        )

    # --- queue ---

    def read_queue(self, session_id: str) -> SessionQueue:
        path = self._queue_path(session_id)
        if not path.exists():
            raise RuntimeSessionStoreError(f"Missing session queue: {session_id}")
        raw = _json_read(path)
        items = tuple(SessionQueueItem(**{
            **it,
            "status": SessionQueueItemStatus(it["status"]),
            "work_unit_id": it.get("work_unit_id"),
        }) for it in raw.get("items", ()))
        return SessionQueue(session_id=raw["session_id"], updated_at=raw["updated_at"], items=items)

    def _write_queue(self, queue: SessionQueue) -> None:
        payload = {
            "session_id": queue.session_id,
            "updated_at": queue.updated_at,
            "items": [
                {
                    "item_id": it.item_id,
                    "created_at": it.created_at,
                    "status": str(it.status),
                    "work_unit_id": it.work_unit_id,
                    "payload": it.payload,
                }
                for it in queue.items
            ],
        }
        _json_dump(self._queue_path(queue.session_id), payload)

    def add_queue_item(
        self,
        session_id: str,
        *,
        work_unit_id: str | None = None,
        payload: dict[str, Any] | None = None,
        status: SessionQueueItemStatus = SessionQueueItemStatus.PENDING,
        item_id: str | None = None,
        created_at: str | None = None,
    ) -> tuple[SessionQueueItem, SessionQueue, RuntimeSessionReceipt]:
        queue = self.read_queue(session_id)
        item_id = item_id or f"q-{uuid.uuid4().hex[:10]}"
        created_at = created_at or _utc_now()
        item = SessionQueueItem(
            item_id=_validate_id(item_id, "item_id"),
            created_at=created_at,
            status=status,
            work_unit_id=work_unit_id,
            payload=payload or {},
        )
        new_queue = SessionQueue(
            session_id=session_id,
            updated_at=_utc_now(),
            items=queue.items + (item,),
        )
        self._write_queue(new_queue)
        receipt = RuntimeSessionReceipt(
            receipt_id=f"rsr-{uuid.uuid4().hex[:12]}",
            event=RuntimeSessionEvent.QUEUE_ITEM_ADDED,
            session_id=session_id,
            created_at=_utc_now(),
            detail=f"queue item added: {item.item_id}",
            witness_paths=(str(self._queue_path(session_id)),),
        )
        _json_dump(self._receipt_path(receipt.receipt_id), receipt.to_dict())
        return item, new_queue, receipt

    def update_queue_item_status(
        self,
        session_id: str,
        *,
        item_id: str,
        status: SessionQueueItemStatus,
    ) -> tuple[SessionQueue, RuntimeSessionReceipt]:
        queue = self.read_queue(session_id)
        found = False
        new_items: list[SessionQueueItem] = []
        for it in queue.items:
            if it.item_id == item_id:
                found = True
                new_items.append(SessionQueueItem(**{**it.to_dict(), "status": status}))
            else:
                new_items.append(it)
        if not found:
            raise RuntimeSessionStoreError(f"Missing queue item: {item_id}")
        new_queue = SessionQueue(
            session_id=session_id,
            updated_at=_utc_now(),
            items=tuple(new_items),
        )
        self._write_queue(new_queue)
        receipt = RuntimeSessionReceipt(
            receipt_id=f"rsr-{uuid.uuid4().hex[:12]}",
            event=RuntimeSessionEvent.QUEUE_ITEM_STATUS_UPDATED,
            session_id=session_id,
            created_at=_utc_now(),
            detail=f"queue item status updated: {item_id} -> {status}",
            witness_paths=(str(self._queue_path(session_id)),),
        )
        _json_dump(self._receipt_path(receipt.receipt_id), receipt.to_dict())
        return new_queue, receipt


IonRuntimeSessionStore = RuntimeSessionStore
