"""Bounded recovery and replay support for supervised daemon service runs.

This module does not create hidden auto-resume behavior. It classifies daemon-service
receipts as resumable or non-resumable, detects stale resumable runs, and allows an
operator to replay a bounded service run lawfully.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re

from .daemon_service import DaemonServiceRequest, DaemonServiceStatus, KernelDaemonService
from .graph import KernelGraph
from .index import KernelIndex
from .model import StrEnum
from .store import KernelStore


class KernelRecoveryReplayError(Exception):
    """Raised when recovery/replay inputs are malformed or unsafe."""


class RecoveryReplaySelectionMode(StrEnum):
    EXPLICIT_SERVICE_RECEIPT = "EXPLICIT_SERVICE_RECEIPT"
    LATEST_RESUMABLE = "LATEST_RESUMABLE"


class RecoveryReplayStatus(StrEnum):
    REPLAYED = "REPLAYED"
    DRY_RUN = "DRY_RUN"
    NO_RESUMABLE_CANDIDATE = "NO_RESUMABLE_CANDIDATE"
    NON_RESUMABLE = "NON_RESUMABLE"
    STALE_REQUIRES_APPROVAL = "STALE_REQUIRES_APPROVAL"
    CONTROL_BLOCKED = "CONTROL_BLOCKED"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"


@dataclass(frozen=True)
class RecoveryReplayRequest:
    workspace_root: str | Path
    selection_mode: RecoveryReplaySelectionMode = RecoveryReplaySelectionMode.LATEST_RESUMABLE
    service_receipt_path: str | Path | None = None
    stale_after_seconds: int = 4 * 60 * 60
    current_timestamp: str | None = None
    explicit_approval: bool = False
    supervisor_present: bool = True
    allow_stale_replay: bool = False
    dry_run: bool = False
    max_steps_override: int | None = None
    packet_output_root: str | Path | None = None
    repo_root: str | Path | None = None
    actor: str = "OPERATOR"
    notes: str | None = None


@dataclass(frozen=True)
class ServiceRecoveryClassification:
    source_receipt_path: str
    service_status: str
    loop_status: str | None
    resumable: bool
    recovery_classification: str
    stale: bool
    age_seconds: int | None
    is_replay: bool
    replay_of_service_receipt_path: str | None


@dataclass(frozen=True)
class RecoveryReplayReceipt:
    status: RecoveryReplayStatus
    requested_at: str
    selection_mode: RecoveryReplaySelectionMode
    classification: ServiceRecoveryClassification | None = None
    source_service_receipt_path: str | None = None
    replayed_service_receipt_path: str | None = None
    replayed_service_status: str | None = None
    replay_receipt_path: str | None = None
    replay_ledger_path: str | None = None
    notes: tuple[str, ...] = ()


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelRecoveryReplayManager:
    """Classify and replay lawful daemon-service recovery candidates."""

    def __init__(self, *, daemon_service: KernelDaemonService | None = None) -> None:
        self._daemon_service = daemon_service or KernelDaemonService()

    def classify_service_receipt(
        self,
        workspace_root: str | Path,
        service_receipt_path: str | Path,
        *,
        current_timestamp: str | None = None,
        stale_after_seconds: int = 4 * 60 * 60,
    ) -> ServiceRecoveryClassification:
        workspace = Path(workspace_root).resolve()
        relative_path = _normalize_relative_path(service_receipt_path)
        payload = _load_json(_resolve_relative_file(workspace, relative_path))
        requested_at = str(payload["requested_at"])
        now_text = current_timestamp or _iso_now()
        age_seconds = _seconds_between(requested_at, now_text)
        recovery_payload = payload.get("recovery", {})
        if not isinstance(recovery_payload, dict):
            raise KernelRecoveryReplayError("daemon service recovery payload must be a mapping")
        replay_payload = payload.get("replay", {})
        if not isinstance(replay_payload, dict):
            raise KernelRecoveryReplayError("daemon service replay payload must be a mapping")
        loop_payload = payload.get("loop_result")
        loop_status = None
        if isinstance(loop_payload, dict):
            loop_status = None if loop_payload.get("status") is None else str(loop_payload.get("status"))
        resumable = bool(recovery_payload.get("resumable", False))
        stale = resumable and age_seconds is not None and age_seconds > stale_after_seconds
        return ServiceRecoveryClassification(
            source_receipt_path=str(relative_path),
            service_status=str(payload["status"]),
            loop_status=loop_status,
            resumable=resumable,
            recovery_classification=str(recovery_payload.get("classification", "UNKNOWN")),
            stale=stale,
            age_seconds=age_seconds,
            is_replay=bool(replay_payload.get("is_replay", False)),
            replay_of_service_receipt_path=(None if replay_payload.get("replay_of_service_receipt_path") is None else str(replay_payload.get("replay_of_service_receipt_path"))),
        )

    def replay_daemon_service(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        request: RecoveryReplayRequest,
    ) -> RecoveryReplayReceipt:
        workspace = Path(request.workspace_root).resolve()
        requested_at = request.current_timestamp or _iso_now()
        source_receipt_path = self._select_source_receipt(workspace, request)
        if source_receipt_path is None:
            return self._finalize(
                workspace,
                requested_at=requested_at,
                selection_mode=request.selection_mode,
                status=RecoveryReplayStatus.NO_RESUMABLE_CANDIDATE,
                notes=("NO_RESUMABLE_DAEMON_SERVICE_RECEIPT",),
            )

        classification = self.classify_service_receipt(
            workspace,
            source_receipt_path,
            current_timestamp=requested_at,
            stale_after_seconds=request.stale_after_seconds,
        )
        if not classification.resumable:
            return self._finalize(
                workspace,
                requested_at=requested_at,
                selection_mode=request.selection_mode,
                status=RecoveryReplayStatus.NON_RESUMABLE,
                classification=classification,
                source_service_receipt_path=classification.source_receipt_path,
                notes=(f"NON_RESUMABLE::{classification.recovery_classification}",),
            )
        if classification.stale and not (request.explicit_approval or request.allow_stale_replay):
            return self._finalize(
                workspace,
                requested_at=requested_at,
                selection_mode=request.selection_mode,
                status=RecoveryReplayStatus.STALE_REQUIRES_APPROVAL,
                classification=classification,
                source_service_receipt_path=classification.source_receipt_path,
                notes=("STALE_RESUMABLE_REQUIRES_APPROVAL",),
            )
        if request.dry_run:
            return self._finalize(
                workspace,
                requested_at=requested_at,
                selection_mode=request.selection_mode,
                status=RecoveryReplayStatus.DRY_RUN,
                classification=classification,
                source_service_receipt_path=classification.source_receipt_path,
                notes=("RECOVERY_REPLAY_DRY_RUN",),
            )

        replay_request = self._build_replay_request(
            workspace,
            classification,
            replay_requested_at=requested_at,
            request=request,
        )
        daemon_receipt = self._daemon_service.run(store, index, graph, replay_request)
        status = _map_daemon_service_status(daemon_receipt.status)
        notes = [f"REPLAY_SOURCE::{classification.recovery_classification}"]
        if classification.stale:
            notes.append("STALE_REPLAY_APPROVED")
        return self._finalize(
            workspace,
            requested_at=requested_at,
            selection_mode=request.selection_mode,
            status=status,
            classification=classification,
            source_service_receipt_path=classification.source_receipt_path,
            replayed_service_receipt_path=daemon_receipt.service_receipt_path,
            replayed_service_status=daemon_receipt.status,
            notes=tuple(notes),
        )

    def _select_source_receipt(self, workspace_root: Path, request: RecoveryReplayRequest) -> str | None:
        if request.selection_mode is RecoveryReplaySelectionMode.EXPLICIT_SERVICE_RECEIPT:
            if request.service_receipt_path is None:
                raise KernelRecoveryReplayError("Explicit replay selection requires service_receipt_path.")
            return str(_normalize_relative_path(request.service_receipt_path))

        ledger_path = _resolve_relative_file(workspace_root, Path("ION/05_context/history/daemon_service_ledger.json"))
        if not ledger_path.exists():
            return None
        rows = _load_json(ledger_path)
        if not isinstance(rows, list):
            raise KernelRecoveryReplayError("daemon service ledger must contain a JSON list")
        resumable_rows = [
            row for row in rows
            if isinstance(row, dict) and bool(row.get("resumable")) and row.get("receipt_path")
        ]
        if not resumable_rows:
            return None
        latest = resumable_rows[-1]
        return str(latest["receipt_path"])

    def _build_replay_request(
        self,
        workspace_root: Path,
        classification: ServiceRecoveryClassification,
        *,
        replay_requested_at: str,
        request: RecoveryReplayRequest,
    ) -> DaemonServiceRequest:
        source_payload = _load_json(_resolve_relative_file(workspace_root, Path(classification.source_receipt_path)))
        request_payload = source_payload.get("request")
        if not isinstance(request_payload, dict):
            raise KernelRecoveryReplayError("daemon service receipt must include request payload")
        return DaemonServiceRequest(
            workspace_root=workspace_root,
            max_steps=(request.max_steps_override if request.max_steps_override is not None else int(request_payload.get("max_steps", 25))),
            scope_type=(None if request_payload.get("scope_type") is None else str(request_payload.get("scope_type"))),
            scope_ref=(None if request_payload.get("scope_ref") is None else str(request_payload.get("scope_ref"))),
            context_mode=str_to_context_mode(str(request_payload.get("context_mode", "IDE_MANUAL"))),
            automation_stage=str_to_automation_stage(str(request_payload.get("automation_stage", "ASSISTED"))),
            route_stage=str_to_route_stage(str(request_payload.get("route_stage", "ACTIVE"))),
            calibration_status=str_to_calibration_status(str(request_payload.get("calibration_status", "INSUFFICIENT_DATA"))),
            threshold_action=str_to_threshold_action(request_payload.get("threshold_action")),
            review_required=bool(request_payload.get("review_required", False)),
            manual_fallback_required=bool(request_payload.get("manual_fallback_required", False)),
            supervisor_present=request.supervisor_present,
            explicit_approval=request.explicit_approval,
            dry_run=False,
            packet_output_root=(request.packet_output_root if request.packet_output_root is not None else request_payload.get("packet_output_root")),
            repo_root=(request.repo_root if request.repo_root is not None else request_payload.get("repo_root")),
            actor=request.actor,
            action_timestamp=replay_requested_at,
            replay_of_service_receipt_path=classification.source_receipt_path,
            replay_reason=(request.notes or f"RECOVERY_REPLAY::{classification.recovery_classification}"),
        )

    def _finalize(
        self,
        workspace_root: Path,
        *,
        requested_at: str,
        selection_mode: RecoveryReplaySelectionMode,
        status: RecoveryReplayStatus,
        classification: ServiceRecoveryClassification | None = None,
        source_service_receipt_path: str | None = None,
        replayed_service_receipt_path: str | None = None,
        replayed_service_status: str | None = None,
        notes: tuple[str, ...] = (),
        receipts_dir: str = "ION/05_context/history/recovery_replay_receipts",
        ledger_path: str = "ION/05_context/history/recovery_replay_ledger.json",
    ) -> RecoveryReplayReceipt:
        event_id = _replay_event_id(requested_at)
        receipt_relative_path = Path(receipts_dir) / f"{event_id}.recovery_replay_receipt.json"
        ledger_relative_path = Path(ledger_path)
        resolved_receipt_path = _resolve_relative_file(workspace_root, receipt_relative_path)
        resolved_ledger_path = _resolve_relative_file(workspace_root, ledger_relative_path)
        resolved_receipt_path.parent.mkdir(parents=True, exist_ok=True)
        resolved_ledger_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "requested_at": requested_at,
            "status": status.value,
            "selection_mode": selection_mode.value,
            "source_service_receipt_path": source_service_receipt_path,
            "classification": None if classification is None else {
                "source_receipt_path": classification.source_receipt_path,
                "service_status": classification.service_status,
                "loop_status": classification.loop_status,
                "resumable": classification.resumable,
                "recovery_classification": classification.recovery_classification,
                "stale": classification.stale,
                "age_seconds": classification.age_seconds,
                "is_replay": classification.is_replay,
                "replay_of_service_receipt_path": classification.replay_of_service_receipt_path,
            },
            "replayed_service_receipt_path": replayed_service_receipt_path,
            "replayed_service_status": replayed_service_status,
            "notes": list(notes),
        }
        resolved_receipt_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        rows: list[dict[str, object]] = []
        if resolved_ledger_path.exists():
            existing = _load_json(resolved_ledger_path)
            if not isinstance(existing, list):
                raise KernelRecoveryReplayError("recovery replay ledger must contain a JSON list")
            rows = existing
        rows.append(
            {
                "event_id": event_id,
                "created_at": requested_at,
                "status": status.value,
                "selection_mode": selection_mode.value,
                "source_service_receipt_path": source_service_receipt_path,
                "replayed_service_receipt_path": replayed_service_receipt_path,
                "replayed_service_status": replayed_service_status,
                "receipt_path": str(receipt_relative_path),
            }
        )
        resolved_ledger_path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return RecoveryReplayReceipt(
            status=status,
            requested_at=requested_at,
            selection_mode=selection_mode,
            classification=classification,
            source_service_receipt_path=source_service_receipt_path,
            replayed_service_receipt_path=replayed_service_receipt_path,
            replayed_service_status=replayed_service_status,
            replay_receipt_path=str(receipt_relative_path),
            replay_ledger_path=str(ledger_relative_path),
            notes=notes,
        )


IonRecoveryReplayManager = KernelRecoveryReplayManager


def _map_daemon_service_status(status: str) -> RecoveryReplayStatus:
    if status == DaemonServiceStatus.EXECUTED:
        return RecoveryReplayStatus.REPLAYED
    if status == DaemonServiceStatus.DRY_RUN:
        return RecoveryReplayStatus.DRY_RUN
    if status == DaemonServiceStatus.CONTROL_BLOCKED:
        return RecoveryReplayStatus.CONTROL_BLOCKED
    if status == DaemonServiceStatus.POLICY_BLOCKED:
        return RecoveryReplayStatus.POLICY_BLOCKED
    return RecoveryReplayStatus.APPROVAL_REQUIRED


def _replay_event_id(requested_at: str) -> str:
    safe = _SAFE_ID_RE.sub("-", requested_at.lower()).strip("-") or "replay"
    return f"recovery-replay-{safe}"


def _normalize_relative_path(path_like: str | Path) -> Path:
    path = Path(path_like)
    if path.is_absolute():
        raise KernelRecoveryReplayError("service receipt paths must be relative to workspace_root")
    return path


def _resolve_relative_file(workspace_root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelRecoveryReplayError("relative_path must be relative to workspace_root")
    return workspace_root / relative_path


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _seconds_between(earlier: str, later: str) -> int | None:
    try:
        first = datetime.fromisoformat(earlier)
        second = datetime.fromisoformat(later)
    except ValueError:
        return None
    return int((second - first).total_seconds())


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


# Small local adapters to avoid widening daemon-service imports.
def str_to_context_mode(value: str):
    from .threshold import ContextMode
    return ContextMode(value)


def str_to_automation_stage(value: str):
    from .threshold import AutomationStage
    return AutomationStage(value)


def str_to_route_stage(value: str):
    from .threshold import RouteStage
    return RouteStage(value)


def str_to_calibration_status(value: str):
    from .threshold import CalibrationStatus
    return CalibrationStatus(value)


def str_to_threshold_action(value):
    if value is None:
        return None
    from .threshold import PromotionAction
    return PromotionAction(str(value))
