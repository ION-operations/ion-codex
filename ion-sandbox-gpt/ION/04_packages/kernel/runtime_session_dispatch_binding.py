"""Bind runtime session queue items to kernel dispatch law.

This is Target 1 / Slice 2: it does *not* import a daemon scheduler or server stack.
It simply provides a truthful bridge:
- session queue items may nominate dispatchable kernel WorkUnits
- kernel dispatch persists WorkUnit DISPATCHED transition and optionally emits packets
- session queue state is updated (DISPATCH_READY -> DISPATCHED) with receipts
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .dispatch import KernelDispatcher, DispatchResult
from .graph import KernelGraph
from .index import KernelIndex
from .store import KernelStore
from .runtime_session_store import (
    RuntimeSessionLifecycleState,
    RuntimeSessionStore,
    RuntimeSessionStoreError,
    RuntimeSessionEvent,
    RuntimeSessionReceipt,
    SessionQueueItemStatus,
)


class RuntimeSessionDispatchBindingError(Exception):
    """Raised when one session-to-kernel dispatch binding fails."""


@dataclass(frozen=True)
class RuntimeSessionQueueDispatchResult:
    session_id: str
    item_id: str
    work_unit_id: str
    dispatch_result: DispatchResult
    session_receipt: RuntimeSessionReceipt


class RuntimeSessionQueueDispatcher:
    """Dispatch a specific session queue item through kernel dispatch law."""

    def __init__(self, *, dispatcher: KernelDispatcher | None = None) -> None:
        self._dispatcher = dispatcher or KernelDispatcher()

    def dispatch_queue_item(
        self,
        *,
        session_store: RuntimeSessionStore,
        kernel_store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        session_id: str,
        item_id: str,
        dispatched_at: str | None = None,
        packet_output_path: str | Path | None = None,
    ) -> RuntimeSessionQueueDispatchResult:
        try:
            authority = session_store.read_authority(session_id)
            queue = session_store.read_queue(session_id)
        except RuntimeSessionStoreError as e:
            raise RuntimeSessionDispatchBindingError(str(e)) from e

        if authority.lifecycle_state != RuntimeSessionLifecycleState.ACTIVE:
            raise RuntimeSessionDispatchBindingError(
                f"Session not dispatchable: {session_id} ({authority.lifecycle_state})"
            )

        item = next((it for it in queue.items if it.item_id == item_id), None)
        if item is None:
            raise RuntimeSessionDispatchBindingError(f"Missing session queue item: {item_id}")
        if item.status != SessionQueueItemStatus.DISPATCH_READY:
            raise RuntimeSessionDispatchBindingError(
                f"Queue item not dispatch-ready: {item_id} ({item.status})"
            )

        # Preferred: first-class field on the queue item.
        work_unit_id = item.work_unit_id
        # Back-compat bridge: older persisted queues may store this under payload.
        if work_unit_id is None:
            maybe = item.payload.get("work_unit_id")
            work_unit_id = maybe if isinstance(maybe, str) else None
        if not isinstance(work_unit_id, str) or not work_unit_id.strip():
            raise RuntimeSessionDispatchBindingError(
                f"Queue item missing work_unit_id: {item_id}"
            )

        dispatch_result = self._dispatcher.dispatch_work_unit(
            kernel_store,
            index,
            graph,
            work_unit_id,
            dispatched_at=dispatched_at,
            packet_output_path=packet_output_path,
        )

        # Update session queue item status to DISPATCHED.
        session_store.update_queue_item_status(
            session_id,
            item_id=item_id,
            status=SessionQueueItemStatus.DISPATCHED,
        )

        receipt = session_store.create_receipt(
            session_id,
            event=RuntimeSessionEvent.DISPATCHED_WORK_UNIT,
            detail=f"dispatched work unit {work_unit_id} from session queue item {item_id}",
            witness_paths=tuple(
                str(p) for p in (
                    (dispatch_result.packet_path,) if dispatch_result.packet_path is not None else ()
                )
            ),
        )

        return RuntimeSessionQueueDispatchResult(
            session_id=session_id,
            item_id=item_id,
            work_unit_id=work_unit_id,
            dispatch_result=dispatch_result,
            session_receipt=receipt,
        )


IonRuntimeSessionQueueDispatcher = RuntimeSessionQueueDispatcher
