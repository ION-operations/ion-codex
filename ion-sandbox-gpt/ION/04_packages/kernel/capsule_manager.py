"""Bounded capsule lifecycle helper for the live ION kernel stack.

This module ports the useful PRE / POST / recovery discipline from earlier ION roots without
claiming that root markdown projections are now runtime state. Capsules here are durable JSON
records that preserve mission, constraints, and next-action posture across bounded work cycles.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from pathlib import Path
import uuid

from .index import KernelIndex
from .runtime_state_sync import KernelRuntimeStateSync, RuntimeStateSyncResult
from .runtime_report_triggers import RuntimeReportTriggerRequest
from .store import KernelStore
from .threshold import AutomationStage, ContextMode


class KernelCapsuleError(Exception):
    """Raised when one capsule lifecycle operation fails."""


class CapsuleType:
    PRE = "PRE"
    POST = "POST"


@dataclass(frozen=True)
class CapsuleRecord:
    capsule_id: str
    timestamp: str
    capsule_type: str
    callsign: str
    mission: str
    now: str
    must_not: tuple[str, ...]
    evidence: tuple[str, ...]
    next_action: str
    handoff: str = ""
    blocker: str | None = None
    context_mode: str = ContextMode.IDE_MANUAL.value
    automation_stage: str = AutomationStage.MANUAL.value
    route_surface: str | None = None
    confidence_band: str | None = None
    drift_status: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)

    def validate(self) -> tuple[str, ...]:
        errors: list[str] = []
        if self.capsule_type not in {CapsuleType.PRE, CapsuleType.POST}:
            errors.append(f"Unknown capsule type: {self.capsule_type}")
        if not self.callsign.strip():
            errors.append("callsign is required")
        if not self.mission.strip():
            errors.append("mission is required")
        if not self.now.strip():
            errors.append("now is required")
        if not self.next_action.strip():
            errors.append("next_action is required")
        return tuple(errors)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "CapsuleRecord":
        try:
            return cls(
                capsule_id=str(payload["capsule_id"]),
                timestamp=str(payload["timestamp"]),
                capsule_type=str(payload["capsule_type"]),
                callsign=str(payload["callsign"]),
                mission=str(payload["mission"]),
                now=str(payload["now"]),
                must_not=tuple(str(item) for item in payload.get("must_not", [])),
                evidence=tuple(str(item) for item in payload.get("evidence", [])),
                next_action=str(payload["next_action"]),
                handoff=str(payload.get("handoff", "")),
                blocker=(None if payload.get("blocker") is None else str(payload.get("blocker"))),
                context_mode=str(payload.get("context_mode", ContextMode.IDE_MANUAL.value)),
                automation_stage=str(payload.get("automation_stage", AutomationStage.MANUAL.value)),
                route_surface=(None if payload.get("route_surface") is None else str(payload.get("route_surface"))),
                confidence_band=(None if payload.get("confidence_band") is None else str(payload.get("confidence_band"))),
                drift_status=(None if payload.get("drift_status") is None else str(payload.get("drift_status"))),
                metadata=dict(payload.get("metadata") or {}),
            )
        except KeyError as exc:
            raise KernelCapsuleError(f"Malformed capsule payload missing key: {exc.args[0]}") from exc


@dataclass(frozen=True)
class CapsuleDriftCheckResult:
    drift_detected: bool
    reasons: tuple[str, ...]
    capsule: CapsuleRecord | None = None


class KernelCapsuleManager:
    """Persist PRE / POST capsule records and recover the latest durable posture."""

    def __init__(
        self,
        capsule_dir: str | Path,
        *,
        callsign: str = "ion",
        store: KernelStore | None = None,
        index: KernelIndex | None = None,
        runtime_state_sync: KernelRuntimeStateSync | None = None,
        default_scope_type: str | None = None,
        default_scope_ref: str | None = None,
        governing_refs: tuple[str, ...] = (),
    ) -> None:
        self._dir = Path(capsule_dir).resolve()
        self._dir.mkdir(parents=True, exist_ok=True)
        self._callsign = callsign
        self._current_pre: CapsuleRecord | None = None
        self._mission: str = ""
        self._must_not: tuple[str, ...] = ()
        self._store = store
        self._index = index
        self._runtime_state_sync = runtime_state_sync or KernelRuntimeStateSync()
        self._default_scope_type = default_scope_type
        self._default_scope_ref = default_scope_ref
        self._governing_refs = tuple(governing_refs)
        self._last_runtime_state_sync: RuntimeStateSyncResult | None = None

    def write_pre(
        self,
        *,
        mission: str,
        now: str,
        must_not: list[str] | tuple[str, ...],
        evidence: list[str] | tuple[str, ...],
        next_action: str,
        handoff: str = "",
        blocker: str | None = None,
        context_mode: ContextMode = ContextMode.IDE_MANUAL,
        automation_stage: AutomationStage = AutomationStage.MANUAL,
        route_surface: str | None = None,
        confidence_band: str | None = None,
        drift_status: str | None = None,
        metadata: dict[str, object] | None = None,
        state_scope_type: str | None = None,
        state_scope_ref: str | None = None,
        governing_refs: tuple[str, ...] = (),
        route_targets: tuple[str, ...] = (),
        loop_position: str | None = None,
        promotion_criteria: tuple[str, ...] = (),
        artifact_trigger_request: RuntimeReportTriggerRequest | None = None,
    ) -> CapsuleRecord:
        capsule = CapsuleRecord(
            capsule_id=_capsule_id(CapsuleType.PRE),
            timestamp=_now(),
            capsule_type=CapsuleType.PRE,
            callsign=self._callsign,
            mission=mission,
            now=now,
            must_not=tuple(must_not),
            evidence=tuple(evidence),
            next_action=next_action,
            handoff=handoff,
            blocker=blocker,
            context_mode=context_mode.value,
            automation_stage=automation_stage.value,
            route_surface=route_surface,
            confidence_band=confidence_band,
            drift_status=drift_status,
            metadata=dict(metadata or {}),
        )
        self._persist_validated(capsule)
        self._current_pre = capsule
        self._mission = capsule.mission
        self._must_not = capsule.must_not
        self._sync_runtime_state(
            capsule,
            state_scope_type=state_scope_type,
            state_scope_ref=state_scope_ref,
            governing_refs=governing_refs,
            route_targets=route_targets,
            loop_position=loop_position,
            promotion_criteria=promotion_criteria,
            artifact_trigger_request=artifact_trigger_request,
        )
        return capsule

    def write_post(
        self,
        *,
        now: str,
        evidence: list[str] | tuple[str, ...],
        next_action: str,
        handoff: str,
        blocker: str | None = None,
        context_mode: ContextMode | None = None,
        automation_stage: AutomationStage | None = None,
        route_surface: str | None = None,
        confidence_band: str | None = None,
        drift_status: str | None = None,
        metadata: dict[str, object] | None = None,
        state_scope_type: str | None = None,
        state_scope_ref: str | None = None,
        governing_refs: tuple[str, ...] = (),
        route_targets: tuple[str, ...] = (),
        loop_position: str | None = None,
        promotion_criteria: tuple[str, ...] = (),
        artifact_trigger_request: RuntimeReportTriggerRequest | None = None,
    ) -> CapsuleRecord:
        if not self._mission:
            recovered = self.recover(prefer_post=False)
            if recovered is not None:
                self._mission = recovered.mission
                self._must_not = recovered.must_not
        if not self._mission:
            raise KernelCapsuleError("Cannot write POST capsule before a PRE or recoverable capsule exists.")
        capsule = CapsuleRecord(
            capsule_id=_capsule_id(CapsuleType.POST),
            timestamp=_now(),
            capsule_type=CapsuleType.POST,
            callsign=self._callsign,
            mission=self._mission,
            now=now,
            must_not=self._must_not,
            evidence=tuple(evidence),
            next_action=next_action,
            handoff=handoff,
            blocker=blocker,
            context_mode=(context_mode.value if context_mode is not None else ContextMode.IDE_MANUAL.value),
            automation_stage=(automation_stage.value if automation_stage is not None else AutomationStage.MANUAL.value),
            route_surface=route_surface,
            confidence_band=confidence_band,
            drift_status=drift_status,
            metadata=dict(metadata or {}),
        )
        self._persist_validated(capsule)
        self._sync_runtime_state(
            capsule,
            state_scope_type=state_scope_type,
            state_scope_ref=state_scope_ref,
            governing_refs=governing_refs,
            route_targets=route_targets,
            loop_position=loop_position,
            promotion_criteria=promotion_criteria,
            artifact_trigger_request=artifact_trigger_request,
        )
        return capsule

    def recover(self, *, prefer_post: bool = True) -> CapsuleRecord | None:
        candidates = self._sorted_capsule_paths()
        if prefer_post:
            for capsule in self._read_capsules(candidates):
                if capsule.capsule_type == CapsuleType.POST:
                    self._mission = capsule.mission
                    self._must_not = capsule.must_not
                    return capsule
        for capsule in self._read_capsules(candidates):
            self._mission = capsule.mission
            self._must_not = capsule.must_not
            if capsule.capsule_type == CapsuleType.PRE:
                self._current_pre = capsule
            return capsule
        return None

    def last_capsule(self) -> CapsuleRecord | None:
        for capsule in self._read_capsules(self._sorted_capsule_paths()[:1]):
            return capsule
        return None

    def check_drift(
        self,
        *,
        current_mission: str | None = None,
        current_next_action: str | None = None,
        current_context_mode: ContextMode | None = None,
    ) -> CapsuleDriftCheckResult:
        capsule = self.last_capsule()
        if capsule is None:
            return CapsuleDriftCheckResult(False, ("NO_CAPSULE_PRESENT",), None)
        reasons: list[str] = []
        if current_mission is not None and current_mission != capsule.mission:
            reasons.append("MISSION_DRIFT")
        if current_next_action is not None and current_next_action != capsule.next_action:
            reasons.append("NEXT_ACTION_DRIFT")
        if current_context_mode is not None and current_context_mode.value != capsule.context_mode:
            reasons.append("CONTEXT_MODE_DRIFT")
        return CapsuleDriftCheckResult(bool(reasons), tuple(reasons), capsule)

    @property
    def mission(self) -> str:
        return self._mission

    @property
    def must_not(self) -> tuple[str, ...]:
        return self._must_not

    @property
    def last_runtime_state_sync(self) -> RuntimeStateSyncResult | None:
        return self._last_runtime_state_sync

    def capsule_count(self) -> int:
        return len(list(self._dir.glob("*.json")))

    def render_projection(self, capsule: CapsuleRecord) -> str:
        lines = [
            f"# {capsule.capsule_type} CAPSULE — {capsule.callsign}",
            "",
            f"- Mission: {capsule.mission}",
            f"- Now: {capsule.now}",
            f"- Next Action: {capsule.next_action}",
            f"- Context Mode: {capsule.context_mode}",
            f"- Automation Stage: {capsule.automation_stage}",
        ]
        if capsule.route_surface:
            lines.append(f"- Route Surface: {capsule.route_surface}")
        if capsule.blocker:
            lines.append(f"- Blocker: {capsule.blocker}")
        if capsule.must_not:
            lines.extend(["", "## Must Not", ""])
            lines.extend(f"- {item}" for item in capsule.must_not)
        if capsule.evidence:
            lines.extend(["", "## Evidence", ""])
            lines.extend(f"- {item}" for item in capsule.evidence)
        if capsule.handoff:
            lines.extend(["", "## Handoff", "", capsule.handoff])
        return "\n".join(lines) + "\n"

    def _sync_runtime_state(
        self,
        capsule: CapsuleRecord,
        *,
        state_scope_type: str | None,
        state_scope_ref: str | None,
        governing_refs: tuple[str, ...],
        route_targets: tuple[str, ...],
        loop_position: str | None,
        promotion_criteria: tuple[str, ...],
        artifact_trigger_request: RuntimeReportTriggerRequest | None,
    ) -> None:
        if self._store is None or self._index is None:
            return
        scope_type = state_scope_type or self._default_scope_type or str(capsule.metadata.get("scope_type") or "").strip() or None
        scope_ref = state_scope_ref or self._default_scope_ref or str(capsule.metadata.get("scope_ref") or "").strip() or None
        if not scope_type or not scope_ref:
            return
        self._last_runtime_state_sync = self._runtime_state_sync.sync_capsule(
            self._store,
            self._index,
            capsule,
            owner_scope_type=scope_type,
            owner_scope_id=scope_ref,
            steward=self._callsign,
            governing_refs=tuple(dict.fromkeys(tuple(governing_refs) + self._governing_refs)),
            loop_position=loop_position,
            route_targets=route_targets,
            promotion_criteria=promotion_criteria,
            artifact_trigger_request=artifact_trigger_request,
        )

    def _persist_validated(self, capsule: CapsuleRecord) -> Path:
        errors = capsule.validate()
        if errors:
            raise KernelCapsuleError(f"Invalid capsule: {', '.join(errors)}")
        path = self._dir / _capsule_filename(capsule)
        path.write_text(json.dumps(capsule.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def _sorted_capsule_paths(self) -> list[Path]:
        return sorted(self._dir.glob("*.json"), reverse=True)

    def _read_capsules(self, paths: list[Path]):
        for path in paths:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                capsule = CapsuleRecord.from_dict(payload)
                if capsule.validate():
                    continue
                yield capsule
            except (json.JSONDecodeError, KernelCapsuleError, TypeError, ValueError):
                continue


IonCapsuleManager = KernelCapsuleManager


def _capsule_id(prefix: str) -> str:
    return f"{prefix.lower()}-{uuid.uuid4().hex[:12]}"


def _capsule_filename(capsule: CapsuleRecord) -> str:
    safe_timestamp = capsule.timestamp.replace(":", "-")
    return f"{safe_timestamp}_{capsule.capsule_type.lower()}_{capsule.capsule_id}.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
