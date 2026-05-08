"""Executor fleet lifecycle store (bounded Target 2 slice).

Target 2 / Slice 1:

- Reincorporate the smallest concrete fleet-lifecycle witness from the Victus/Gemini line
  (spawn/suspend/terminate/heartbeat/stale detection) into the current branch;
- Do so as a bounded store + receipts center, without importing swarm, server shells, or
  theatrical role mythology.

This module tracks *fleet membership* and basic lifecycle events. It does not try to
replace executor-work lifecycle (which remains governed by EXECUTOR_LIFECYCLE_PROTOCOL).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import uuid
from typing import Any, Iterable

from .model import KernelRecord, StrEnum


_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_id(value: str, label: str) -> str:
    if not _ID_RE.match(value) or ".." in value or "/" in value or "\\" in value:
        raise FleetLifecycleStoreError(f"Invalid {label}: {value!r}")
    return value


class FleetLifecycleStoreError(Exception):
    """Raised when one fleet lifecycle store operation fails."""


class FleetMemberState(StrEnum):
    BOOTING = "BOOTING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    TERMINATED = "TERMINATED"


class FleetEvent(StrEnum):
    FLEET_CREATED = "FLEET_CREATED"
    MEMBER_SPAWNED = "MEMBER_SPAWNED"
    MEMBER_HEARTBEAT = "MEMBER_HEARTBEAT"
    MEMBER_SUSPENDED = "MEMBER_SUSPENDED"
    MEMBER_TERMINATED = "MEMBER_TERMINATED"
    MEMBER_STALE_SUSPENDED = "MEMBER_STALE_SUSPENDED"


@dataclass(frozen=True)
class FleetIdentity(KernelRecord):
    fleet_id: str
    created_at: str
    label: str | None = None
    purpose: str | None = None


@dataclass(frozen=True)
class FleetMemberIdentity(KernelRecord):
    member_id: str
    fleet_id: str
    callsign: str
    branch: str
    authority_class: str | None
    created_at: str
    state: FleetMemberState
    last_heartbeat_at: str | None = None
    suspension_reason: str | None = None
    termination_reason: str | None = None


@dataclass(frozen=True)
class FleetReceipt(KernelRecord):
    receipt_id: str
    event: FleetEvent
    fleet_id: str
    member_id: str | None
    created_at: str
    detail: str
    witness_paths: tuple[str, ...] = ()


def _json_dump(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _json_read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class FleetLifecycleStore:
    """Filesystem-backed fleet lifecycle witness + receipts."""

    def __init__(self, root_dir: str | Path) -> None:
        self.root = Path(root_dir)
        self.base = self.root / "fleet_lifecycle"
        self.fleets_dir = self.base / "fleets"
        self.members_dir = self.base / "members"
        self.receipts_dir = self.base / "receipts"
        for d in (self.fleets_dir, self.members_dir, self.receipts_dir):
            d.mkdir(parents=True, exist_ok=True)

    def _fleet_path(self, fleet_id: str) -> Path:
        return self.fleets_dir / f"{_validate_id(fleet_id, 'fleet_id')}.json"

    def _member_path(self, member_id: str) -> Path:
        return self.members_dir / f"{_validate_id(member_id, 'member_id')}.json"

    def _receipt_path(self, receipt_id: str) -> Path:
        return self.receipts_dir / f"{_validate_id(receipt_id, 'receipt_id')}.json"

    def create_fleet(
        self,
        *,
        fleet_id: str | None = None,
        label: str | None = None,
        purpose: str | None = None,
        created_at: str | None = None,
    ) -> tuple[FleetIdentity, FleetReceipt]:
        fid = fleet_id or f"fleet-{uuid.uuid4().hex[:10]}"
        if self._fleet_path(fid).exists():
            raise FleetLifecycleStoreError(f"Fleet already exists: {fid}")
        identity = FleetIdentity(
            fleet_id=fid,
            created_at=created_at or _utc_now(),
            label=label,
            purpose=purpose,
        )
        _json_dump(self._fleet_path(fid), identity.to_dict())
        receipt = self.create_receipt(
            fleet_id=fid,
            member_id=None,
            event=FleetEvent.FLEET_CREATED,
            detail="fleet created",
            witness_paths=(str(self._fleet_path(fid)),),
        )
        return identity, receipt

    def list_fleet_ids(self) -> list[str]:
        return sorted(p.stem for p in self.fleets_dir.glob("*.json"))

    def read_fleet(self, fleet_id: str) -> FleetIdentity:
        path = self._fleet_path(fleet_id)
        if not path.exists():
            raise FleetLifecycleStoreError(f"Missing fleet: {fleet_id}")
        return FleetIdentity(**_json_read(path))

    def list_members(self, *, fleet_id: str | None = None) -> list[FleetMemberIdentity]:
        members: list[FleetMemberIdentity] = []
        for p in self.members_dir.glob("*.json"):
            raw = _json_read(p)
            raw["state"] = FleetMemberState(raw["state"])
            m = FleetMemberIdentity(**raw)
            if fleet_id is None or m.fleet_id == fleet_id:
                members.append(m)
        return sorted(members, key=lambda m: m.member_id)

    def read_member(self, member_id: str) -> FleetMemberIdentity:
        path = self._member_path(member_id)
        if not path.exists():
            raise FleetLifecycleStoreError(f"Missing fleet member: {member_id}")
        raw = _json_read(path)
        raw["state"] = FleetMemberState(raw["state"])
        return FleetMemberIdentity(**raw)

    def _write_member(self, member: FleetMemberIdentity) -> None:
        payload = member.to_dict()
        payload["state"] = str(member.state)
        _json_dump(self._member_path(member.member_id), payload)

    def create_receipt(
        self,
        *,
        fleet_id: str,
        member_id: str | None,
        event: FleetEvent,
        detail: str,
        witness_paths: Iterable[str] = (),
        created_at: str | None = None,
        receipt_id: str | None = None,
    ) -> FleetReceipt:
        receipt = FleetReceipt(
            receipt_id=receipt_id or f"flr-{uuid.uuid4().hex[:12]}",
            event=event,
            fleet_id=fleet_id,
            member_id=member_id,
            created_at=created_at or _utc_now(),
            detail=detail,
            witness_paths=tuple(witness_paths),
        )
        _json_dump(self._receipt_path(receipt.receipt_id), receipt.to_dict())
        return receipt

    def spawn_member(
        self,
        *,
        fleet_id: str,
        callsign: str,
        branch: str,
        authority_class: str | None = None,
        member_id: str | None = None,
        created_at: str | None = None,
    ) -> tuple[FleetMemberIdentity, FleetReceipt]:
        if not self._fleet_path(fleet_id).exists():
            raise FleetLifecycleStoreError(f"Missing fleet: {fleet_id}")
        mid = member_id or f"m-{uuid.uuid4().hex[:10]}"
        if self._member_path(mid).exists():
            raise FleetLifecycleStoreError(f"Fleet member already exists: {mid}")
        created_at = created_at or _utc_now()
        member = FleetMemberIdentity(
            member_id=mid,
            fleet_id=fleet_id,
            callsign=callsign,
            branch=branch,
            authority_class=authority_class,
            created_at=created_at,
            state=FleetMemberState.BOOTING,
            last_heartbeat_at=created_at,
        )
        self._write_member(member)
        receipt = self.create_receipt(
            fleet_id=fleet_id,
            member_id=mid,
            event=FleetEvent.MEMBER_SPAWNED,
            detail=f"member spawned: {callsign} ({branch})",
            witness_paths=(str(self._member_path(mid)),),
        )
        return member, receipt

    def record_heartbeat(
        self,
        *,
        member_id: str,
        heartbeat_at: str | None = None,
    ) -> tuple[FleetMemberIdentity, FleetReceipt]:
        member = self.read_member(member_id)
        hb = heartbeat_at or _utc_now()
        new_state = member.state
        # BOOTING becomes ACTIVE on first observed heartbeat.
        if member.state == FleetMemberState.BOOTING:
            new_state = FleetMemberState.ACTIVE
        updated = FleetMemberIdentity(
            **{
                **member.to_dict(),
                "state": new_state,
                "last_heartbeat_at": hb,
            }
        )
        self._write_member(updated)
        receipt = self.create_receipt(
            fleet_id=updated.fleet_id,
            member_id=member_id,
            event=FleetEvent.MEMBER_HEARTBEAT,
            detail=f"heartbeat recorded: {hb}",
            witness_paths=(str(self._member_path(member_id)),),
        )
        return updated, receipt

    def suspend_member(
        self,
        *,
        member_id: str,
        reason: str,
        suspended_at: str | None = None,
        stale: bool = False,
    ) -> tuple[FleetMemberIdentity, FleetReceipt]:
        member = self.read_member(member_id)
        if member.state == FleetMemberState.TERMINATED:
            raise FleetLifecycleStoreError(f"Cannot suspend terminated member: {member_id}")
        updated = FleetMemberIdentity(
            **{
                **member.to_dict(),
                "state": FleetMemberState.SUSPENDED,
                "suspension_reason": reason,
            }
        )
        self._write_member(updated)
        receipt = self.create_receipt(
            fleet_id=updated.fleet_id,
            member_id=member_id,
            event=FleetEvent.MEMBER_STALE_SUSPENDED if stale else FleetEvent.MEMBER_SUSPENDED,
            detail=f"suspended: {reason}",
            witness_paths=(str(self._member_path(member_id)),),
            created_at=suspended_at,
        )
        return updated, receipt

    def terminate_member(
        self,
        *,
        member_id: str,
        reason: str,
        terminated_at: str | None = None,
    ) -> tuple[FleetMemberIdentity, FleetReceipt]:
        member = self.read_member(member_id)
        updated = FleetMemberIdentity(
            **{
                **member.to_dict(),
                "state": FleetMemberState.TERMINATED,
                "termination_reason": reason,
            }
        )
        self._write_member(updated)
        receipt = self.create_receipt(
            fleet_id=updated.fleet_id,
            member_id=member_id,
            event=FleetEvent.MEMBER_TERMINATED,
            detail=f"terminated: {reason}",
            witness_paths=(str(self._member_path(member_id)),),
            created_at=terminated_at,
        )
        return updated, receipt

    def suspend_stale_members(
        self,
        *,
        fleet_id: str,
        stale_after_seconds: int = 300,
        now: datetime | None = None,
    ) -> tuple[list[FleetMemberIdentity], list[FleetReceipt]]:
        """Suspend stale members (no heartbeat for stale_after_seconds)."""
        if not self._fleet_path(fleet_id).exists():
            raise FleetLifecycleStoreError(f"Missing fleet: {fleet_id}")
        now_dt = now or datetime.now(timezone.utc)
        updated_members: list[FleetMemberIdentity] = []
        receipts: list[FleetReceipt] = []
        for member in self.list_members(fleet_id=fleet_id):
            if member.state in (FleetMemberState.SUSPENDED, FleetMemberState.TERMINATED):
                continue
            if not member.last_heartbeat_at:
                continue
            last = datetime.fromisoformat(member.last_heartbeat_at)
            delta = (now_dt - last).total_seconds()
            if delta > stale_after_seconds:
                updated, r = self.suspend_member(
                    member_id=member.member_id,
                    reason="Stale heartbeat threshold exceeded",
                    stale=True,
                )
                updated_members.append(updated)
                receipts.append(r)
        return updated_members, receipts
