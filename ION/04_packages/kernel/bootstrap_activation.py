"""Supervised bootstrap activation wrapper over init -> emit -> daemon.

This module orchestrates the already-lawful bootstrap layers without collapsing
those layers into hidden behavior. It leaves packet, bridge, and daemon receipts
visible and adds one activation summary receipt linking them.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re

from .bootstrap_bridge import KernelBootstrapSignalBridge
from .bootstrap_init import (
    DEFAULT_BOOTSTRAP_COMPLETION_SIGNAL,
    DEFAULT_BOOTSTRAP_CONSTRAINTS,
    DEFAULT_BOOTSTRAP_DELIVERABLES,
    DEFAULT_BOOTSTRAP_GOAL,
    DEFAULT_BOOTSTRAP_REQUIREMENTS,
    DEFAULT_BOOTSTRAP_SOURCE_CONTEXT,
    DEFAULT_BOOTSTRAP_TARGET,
    DEFAULT_BOOTSTRAP_TITLE,
    KernelBootstrapInitWriter,
)
from .daemon_service import DaemonServiceRequest, DaemonServiceStatus, KernelDaemonService
from .graph import KernelGraph
from .index import KernelIndex
from .model import KernelRecord
from .store import KernelStore

BOOTSTRAP_ACTIVATION_RECEIPTS_RELATIVE = Path("ION/05_context/history/bootstrap_activation_receipts")
_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelBootstrapActivationError(Exception):
    """Raised when one bootstrap activation ceremony cannot complete lawfully."""


@dataclass(frozen=True)
class BootstrapActivationReceipt(KernelRecord):
    activation_id: str
    created_at: str
    packet_path: str
    packet_archived_path: str
    init_receipt_path: str
    init_agent_lineage_receipt_path: str | None
    init_needed_from_lineage_receipt_path: str | None
    bridge_receipt_path: str
    daemon_service_receipt_path: str | None
    daemon_service_status: str
    signal_id: str
    signal_type: str
    signal_path: str
    target: str


@dataclass(frozen=True)
class BootstrapActivationResult:
    init_result: object
    bridge_result: object
    daemon_receipt: object
    activation_receipt: BootstrapActivationReceipt
    activation_receipt_path: str


class KernelBootstrapActivationManager:
    """Run the explicit bootstrap activation ceremony through existing layers."""

    def __init__(
        self,
        *,
        init_writer: KernelBootstrapInitWriter | None = None,
        signal_bridge: KernelBootstrapSignalBridge | None = None,
        daemon_service: KernelDaemonService | None = None,
    ) -> None:
        self._init_writer = init_writer or KernelBootstrapInitWriter()
        self._signal_bridge = signal_bridge or KernelBootstrapSignalBridge()
        self._daemon_service = daemon_service or KernelDaemonService()

    def activate(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        workspace_root: str | Path,
        title: str = DEFAULT_BOOTSTRAP_TITLE,
        goal: str = DEFAULT_BOOTSTRAP_GOAL,
        target: str = DEFAULT_BOOTSTRAP_TARGET,
        agent: str | None = None,
        template: str = "RESEARCH",
        priority: str = "P1_HIGH",
        from_actor: str = "Operator",
        bootstrap_signal_type: str = "BLOCKED",
        bootstrap_needed_from: str | None = None,
        bootstrap_blocker: str | None = None,
        bootstrap_error: str | None = None,
        bootstrap_recoverable: bool | None = None,
        source_context: tuple[str, ...] = DEFAULT_BOOTSTRAP_SOURCE_CONTEXT,
        requirements: tuple[str, ...] = DEFAULT_BOOTSTRAP_REQUIREMENTS,
        deliverables: tuple[str, ...] = DEFAULT_BOOTSTRAP_DELIVERABLES,
        constraints: tuple[str, ...] = DEFAULT_BOOTSTRAP_CONSTRAINTS,
        completion_signal: str = DEFAULT_BOOTSTRAP_COMPLETION_SIGNAL,
        packet_path: str | Path | None = None,
        bootstrap_dir: str | Path = "ION/05_context/inbox/bootstrap",
        init_receipts_dir: str | Path = "ION/05_context/history/bootstrap_init_receipts",
        archive_dir: str | Path = "ION/05_context/inbox/bootstrap/archive",
        signals_dir: str | Path = "ION/05_context/signals",
        bridge_receipts_dir: str | Path = "ION/05_context/history/bootstrap_bridge_receipts",
        activation_receipts_dir: str | Path = BOOTSTRAP_ACTIVATION_RECEIPTS_RELATIVE,
        max_steps: int = 1,
        explicit_approval: bool = True,
        actor: str = "OPERATOR",
        action_timestamp: str | None = None,
    ) -> BootstrapActivationResult:
        root = Path(workspace_root).resolve()
        timestamp = action_timestamp or _iso_now()
        init_result = self._init_writer.write_init(
            root,
            title=title,
            goal=goal,
            target=target,
            agent=agent,
            template=template,
            priority=priority,
            from_actor=from_actor,
            bootstrap_signal_type=bootstrap_signal_type,
            bootstrap_needed_from=bootstrap_needed_from,
            bootstrap_blocker=bootstrap_blocker,
            bootstrap_error=bootstrap_error,
            bootstrap_recoverable=bootstrap_recoverable,
            source_context=source_context,
            requirements=requirements,
            deliverables=deliverables,
            constraints=constraints,
            completion_signal=completion_signal,
            packet_path=packet_path,
            bootstrap_dir=bootstrap_dir,
            receipts_dir=init_receipts_dir,
            created_at=timestamp,
        )
        bridge_result = self._signal_bridge.bridge(
            root,
            packet_path=init_result.preparation.packet_path.relative_to(root),
            bootstrap_dir=bootstrap_dir,
            archive_dir=archive_dir,
            signals_dir=signals_dir,
            receipts_dir=bridge_receipts_dir,
            emitted_at=timestamp,
        )
        daemon_receipt = self._daemon_service.run(
            store,
            index,
            graph,
            DaemonServiceRequest(
                workspace_root=root,
                explicit_approval=explicit_approval,
                max_steps=max_steps,
                actor=actor,
                action_timestamp=timestamp,
            ),
        )
        activation_receipt = BootstrapActivationReceipt(
            activation_id=f"bootstrap-activation-{_safe_id(bridge_result.preparation.signal.signal_id)}",
            created_at=timestamp,
            packet_path=str(init_result.preparation.receipt.packet_path),
            packet_archived_path=str(init_result.preparation.receipt.packet_path).replace("ION/05_context/inbox/bootstrap/", "ION/05_context/inbox/bootstrap/archive/"),
            init_receipt_path=str(init_result.preparation.receipt_path.relative_to(root)),
            init_agent_lineage_receipt_path=init_result.preparation.receipt.agent_lineage_receipt_path,
            init_needed_from_lineage_receipt_path=init_result.preparation.receipt.needed_from_lineage_receipt_path,
            bridge_receipt_path=str(bridge_result.preparation.receipt_path.relative_to(root)),
            daemon_service_receipt_path=daemon_receipt.service_receipt_path,
            daemon_service_status=daemon_receipt.status,
            signal_id=bridge_result.preparation.signal.signal_id,
            signal_type=bridge_result.preparation.signal.signal_type.value,
            signal_path=str(bridge_result.preparation.signal_path.relative_to(root)),
            target=bridge_result.preparation.signal.target,
        )
        activation_receipt_path = _resolve_relative_file(
            root,
            Path(activation_receipts_dir) / f"{activation_receipt.activation_id}.bootstrap_activation_receipt.json",
        )
        activation_receipt_path.parent.mkdir(parents=True, exist_ok=True)
        activation_receipt_path.write_text(
            json.dumps(activation_receipt.to_dict(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return BootstrapActivationResult(
            init_result=init_result,
            bridge_result=bridge_result,
            daemon_receipt=daemon_receipt,
            activation_receipt=activation_receipt,
            activation_receipt_path=str(activation_receipt_path.relative_to(root)),
        )


IonBootstrapActivationManager = KernelBootstrapActivationManager


def _safe_id(text: str) -> str:
    safe = _SAFE_ID_RE.sub("-", text.lower()).strip("-")
    return safe or "bootstrap"


def _resolve_relative_file(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelBootstrapActivationError(f"Absolute paths are not allowed: {relative_path}")
    resolved = (root / relative_path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelBootstrapActivationError(f"Path escapes workspace root: {relative_path}") from exc
    return resolved


def _iso_now() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()
