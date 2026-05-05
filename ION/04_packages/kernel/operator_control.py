"""Machine-readable operator controls for supervised automation.

This module persists explicit operator hold / resume / stop state without promoting
those controls into kernel-truth records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
from pathlib import Path
import re

from .model import StrEnum


class KernelOperatorControlError(Exception):
    """Raised when operator control state cannot be loaded or mutated."""


class DaemonServiceControlMode(StrEnum):
    ENABLED = "ENABLED"
    STOPPED = "STOPPED"
    DRAINING = "DRAINING"


@dataclass(frozen=True)
class ScopeHold:
    scope_type: str
    scope_ref: str
    reason: str
    created_at: str
    actor: str | None = None


@dataclass(frozen=True)
class OperatorControlState:
    updated_at: str
    service_mode: DaemonServiceControlMode = DaemonServiceControlMode.ENABLED
    scope_holds: tuple[ScopeHold, ...] = ()
    global_notes: tuple[str, ...] = ()

    def is_scope_held(self, scope_type: str, scope_ref: str) -> bool:
        normalized_type = scope_type.strip().upper()
        normalized_ref = scope_ref.strip()
        return any(
            hold.scope_type == normalized_type and hold.scope_ref == normalized_ref
            for hold in self.scope_holds
        )


@dataclass(frozen=True)
class OperatorControlMutationResult:
    state: OperatorControlState
    event_id: str
    state_path: str
    ledger_path: str


_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelOperatorControlManager:
    """Persist and mutate supervised automation operator controls."""

    def load_state(
        self,
        workspace_root: str | Path,
        *,
        state_relative_path: str = "ION/05_context/history/operator_controls/operator_control_state.json",
    ) -> OperatorControlState:
        state_path = _resolve_relative_file(Path(workspace_root).resolve(), Path(state_relative_path))
        if not state_path.exists():
            return OperatorControlState(updated_at=_iso_now())
        payload = json.loads(state_path.read_text(encoding="utf-8"))
        return _state_from_payload(payload)

    def set_service_mode(
        self,
        workspace_root: str | Path,
        *,
        mode: DaemonServiceControlMode,
        reason: str,
        actor: str | None = None,
        state_relative_path: str = "ION/05_context/history/operator_controls/operator_control_state.json",
        ledger_relative_path: str = "ION/05_context/history/operator_controls/operator_control_ledger.json",
        created_at: str | None = None,
    ) -> OperatorControlMutationResult:
        previous = self.load_state(workspace_root, state_relative_path=state_relative_path)
        updated = OperatorControlState(
            updated_at=created_at or _iso_now(),
            service_mode=mode,
            scope_holds=previous.scope_holds,
            global_notes=tuple(dict.fromkeys(previous.global_notes + (reason,))),
        )
        return self._persist_mutation(
            Path(workspace_root).resolve(),
            updated,
            event_kind="service_mode",
            event_detail={"mode": mode.value, "reason": reason, "actor": actor},
            state_relative_path=Path(state_relative_path),
            ledger_relative_path=Path(ledger_relative_path),
            created_at=created_at or _iso_now(),
        )

    def hold_scope(
        self,
        workspace_root: str | Path,
        *,
        scope_type: str,
        scope_ref: str,
        reason: str,
        actor: str | None = None,
        state_relative_path: str = "ION/05_context/history/operator_controls/operator_control_state.json",
        ledger_relative_path: str = "ION/05_context/history/operator_controls/operator_control_ledger.json",
        created_at: str | None = None,
    ) -> OperatorControlMutationResult:
        normalized_type = scope_type.strip().upper()
        normalized_ref = scope_ref.strip()
        timestamp = created_at or _iso_now()
        previous = self.load_state(workspace_root, state_relative_path=state_relative_path)
        holds = [
            hold
            for hold in previous.scope_holds
            if not (hold.scope_type == normalized_type and hold.scope_ref == normalized_ref)
        ]
        holds.append(
            ScopeHold(
                scope_type=normalized_type,
                scope_ref=normalized_ref,
                reason=reason,
                created_at=timestamp,
                actor=actor,
            )
        )
        updated = OperatorControlState(
            updated_at=timestamp,
            service_mode=previous.service_mode,
            scope_holds=tuple(sorted(holds, key=lambda hold: (hold.scope_type, hold.scope_ref, hold.created_at))),
            global_notes=previous.global_notes,
        )
        return self._persist_mutation(
            Path(workspace_root).resolve(),
            updated,
            event_kind="hold_scope",
            event_detail={"scope_type": normalized_type, "scope_ref": normalized_ref, "reason": reason, "actor": actor},
            state_relative_path=Path(state_relative_path),
            ledger_relative_path=Path(ledger_relative_path),
            created_at=timestamp,
        )

    def resume_scope(
        self,
        workspace_root: str | Path,
        *,
        scope_type: str,
        scope_ref: str,
        actor: str | None = None,
        state_relative_path: str = "ION/05_context/history/operator_controls/operator_control_state.json",
        ledger_relative_path: str = "ION/05_context/history/operator_controls/operator_control_ledger.json",
        created_at: str | None = None,
    ) -> OperatorControlMutationResult:
        normalized_type = scope_type.strip().upper()
        normalized_ref = scope_ref.strip()
        timestamp = created_at or _iso_now()
        previous = self.load_state(workspace_root, state_relative_path=state_relative_path)
        holds = [
            hold
            for hold in previous.scope_holds
            if not (hold.scope_type == normalized_type and hold.scope_ref == normalized_ref)
        ]
        updated = OperatorControlState(
            updated_at=timestamp,
            service_mode=previous.service_mode,
            scope_holds=tuple(holds),
            global_notes=previous.global_notes,
        )
        return self._persist_mutation(
            Path(workspace_root).resolve(),
            updated,
            event_kind="resume_scope",
            event_detail={"scope_type": normalized_type, "scope_ref": normalized_ref, "actor": actor},
            state_relative_path=Path(state_relative_path),
            ledger_relative_path=Path(ledger_relative_path),
            created_at=timestamp,
        )

    def _persist_mutation(
        self,
        workspace_root: Path,
        state: OperatorControlState,
        *,
        event_kind: str,
        event_detail: dict[str, object],
        state_relative_path: Path,
        ledger_relative_path: Path,
        created_at: str,
    ) -> OperatorControlMutationResult:
        state_path = _resolve_relative_file(workspace_root, state_relative_path)
        ledger_path = _resolve_relative_file(workspace_root, ledger_relative_path)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)

        state_payload = {
            "updated_at": state.updated_at,
            "service_mode": state.service_mode.value,
            "scope_holds": [asdict(hold) for hold in state.scope_holds],
            "global_notes": list(state.global_notes),
        }
        state_path.write_text(json.dumps(state_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        ledger_rows: list[dict[str, object]] = []
        if ledger_path.exists():
            existing = json.loads(ledger_path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                raise KernelOperatorControlError("operator control ledger must contain a JSON list.")
            ledger_rows = existing
        event_id = _event_id(event_kind, created_at)
        ledger_rows.append(
            {
                "event_id": event_id,
                "event_kind": event_kind,
                "created_at": created_at,
                "state_path": str(state_relative_path),
                **event_detail,
            }
        )
        ledger_path.write_text(json.dumps(ledger_rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return OperatorControlMutationResult(
            state=state,
            event_id=event_id,
            state_path=str(state_relative_path),
            ledger_path=str(ledger_relative_path),
        )


IonOperatorControlManager = KernelOperatorControlManager


def _state_from_payload(payload: dict[str, object]) -> OperatorControlState:
    try:
        holds_payload = payload.get("scope_holds", ())
        if not isinstance(holds_payload, list):
            raise TypeError("scope_holds must be a list")
        holds = tuple(
            ScopeHold(
                scope_type=str(item["scope_type"]),
                scope_ref=str(item["scope_ref"]),
                reason=str(item["reason"]),
                created_at=str(item["created_at"]),
                actor=(None if item.get("actor") is None else str(item["actor"])),
            )
            for item in holds_payload
            if isinstance(item, dict)
        )
        notes_payload = payload.get("global_notes", ())
        if not isinstance(notes_payload, list):
            raise TypeError("global_notes must be a list")
        return OperatorControlState(
            updated_at=str(payload.get("updated_at") or _iso_now()),
            service_mode=DaemonServiceControlMode(str(payload.get("service_mode") or DaemonServiceControlMode.ENABLED.value)),
            scope_holds=holds,
            global_notes=tuple(str(item) for item in notes_payload),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise KernelOperatorControlError(f"Invalid operator control state payload: {exc}") from exc


def _resolve_relative_file(workspace_root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KernelOperatorControlError("relative_path must be relative to workspace_root")
    return workspace_root / relative_path


def _event_id(event_kind: str, created_at: str) -> str:
    safe = _SAFE_ID_RE.sub("-", created_at.lower()).strip("-") or "event"
    return f"operator-control-{event_kind}-{safe}"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
