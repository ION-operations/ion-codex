"""M12 replay-driven active-cycle handoff / resume projection surfaces."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import hashlib
import re

from .authority_lineage import resolve_explicit_authority_override
from .index import KernelIndex
from .model import (
    ScheduleDispatchReconciliationReceipt,
    ScheduleLineageReplayReceipt,
    ScheduleResumeProjectionReceipt,
)
from .packet_validation import validate_packet_text
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleResumeProjectionError(Exception):
    """Raised when replay-driven resume projection cannot be completed."""


class KernelScheduleResumeProjectionManager:
    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M12_SCHEDULE_RESUME_PROJECTION_V1",
            "notes": (
                "M12 turns replayed active-cycle state into one bounded handoff / resume projection.",
                "Projection does not mutate schedule state or archived lineage.",
                "When an active cycle exists, M12 may render one minimal canonical role_session packet for continuation.",
            ),
        }

    def project_resume(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        workspace_root: str | Path | None = None,
        output_path: str | Path | None = None,
        generated_at: str | None = None,
        status: str = "ACTIVE",
        role: str | None = None,
    ) -> ScheduleResumeProjectionReceipt:
        timestamp = generated_at or _iso_now()
        replay = self.latest_replay(index, scope_type, scope_ref)
        if replay is None:
            raise KernelScheduleResumeProjectionError(
                f"No schedule lineage replay receipt exists for {scope_type}:{scope_ref}"
            )

        schedule = None if replay.source_schedule_receipt_id is None else index.get(
            "schedule_receipt", replay.source_schedule_receipt_id
        )
        dispatch = None if replay.source_schedule_dispatch_reconciliation_receipt_id is None else index.get(
            "schedule_dispatch_reconciliation_receipt",
            replay.source_schedule_dispatch_reconciliation_receipt_id,
        )
        if dispatch is not None and not isinstance(dispatch, ScheduleDispatchReconciliationReceipt):
            dispatch = None

        action = "NO_ACTIVE_RESUME_AVAILABLE"
        resume_ready = False
        packet_type = None
        packet_path = None
        packet_relative_path = None
        packet_checksum = None
        packet_title = None
        target_executor = None
        required_reads: tuple[str, ...] = ()
        next_action = "No active cycle resume packet is available for the current replay posture."
        expected_output: tuple[str, ...] = ()
        work_unit_id = None if dispatch is None else dispatch.work_unit_id
        warnings: list[str] = list(replay.warnings)

        if replay.active_cycle_stage in {
            "ACTIVE_SCHEDULED",
            "ACTIVE_DISPATCHED",
            "ACTIVE_COMPLETED_AWAITING_SETTLEMENT",
        } and schedule is not None:
            override = resolve_explicit_authority_override(
                workspace_root,
                "continuation_target_executor",
                role,
                created_at=timestamp,
            )
            warnings.extend(override.warnings)
            warnings.extend(
                f"AUTHORITY_LINEAGE_RECEIPT[continuation_target_executor] {path}"
                for path in override.receipt_paths
            )
            action = "PROJECTED_RESUME_PACKET"
            resume_ready = True
            packet_type = "role_session"
            target_executor = (
                override.resolved_name
                or schedule.selected_executor_id
                or "FreshExecutor"
            ).strip() or "FreshExecutor"
            required_reads = self._required_reads(schedule, dispatch, scope_ref)
            next_action = self._next_action(replay.active_cycle_stage, schedule.candidate_title, dispatch)
            expected_output = self._expected_output(replay.active_cycle_stage, dispatch)
            packet_title = f"Role Session: {target_executor}"
            content = _render_resume_role_session(
                created_at=timestamp,
                status=status,
                role=target_executor,
                scope_type=scope_type,
                scope_ref=scope_ref,
                candidate_title=schedule.candidate_title,
                active_cycle_stage=replay.active_cycle_stage,
                next_action=next_action,
                required_reads=required_reads,
                expected_output=expected_output,
            )
            validation = validate_packet_text(content, expected_type="role_session")
            if not validation.valid:
                problems = ", ".join(message.code for message in validation.errors) or "unknown"
                raise KernelScheduleResumeProjectionError(
                    f"Rendered resume packet failed validation: {problems}"
                )
            packet_checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()
            if output_path is not None:
                resolved_output = _resolve_output_path(workspace_root, output_path)
                resolved_output.parent.mkdir(parents=True, exist_ok=True)
                resolved_output.write_text(content, encoding="utf-8")
                packet_path = str(resolved_output)
                packet_relative_path = _relative_to_root(resolved_output, workspace_root)
        elif replay.active_cycle_stage == "ACTIVE_CYCLE_ALREADY_SETTLED":
            warnings.append("ACTIVE_CYCLE_ALREADY_SETTLED")

        receipt = ScheduleResumeProjectionReceipt(
            receipt_id=schedule_resume_projection_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_lineage_replay_receipt_id=replay.receipt_id,
            source_schedule_lineage_archive_receipt_id=replay.source_schedule_lineage_archive_receipt_id,
            source_schedule_receipt_id=replay.source_schedule_receipt_id,
            source_schedule_dispatch_reconciliation_receipt_id=replay.source_schedule_dispatch_reconciliation_receipt_id,
            source_schedule_completion_release_receipt_id=replay.source_schedule_completion_release_receipt_id,
            source_schedule_settlement_receipt_id=replay.source_schedule_settlement_receipt_id,
            work_unit_id=work_unit_id,
            active_candidate_id=replay.active_candidate_id,
            active_candidate_title=replay.active_candidate_title,
            active_cycle_stage=replay.active_cycle_stage,
            projection_action=action,
            resume_ready=resume_ready,
            packet_type=packet_type,
            packet_path=packet_path,
            packet_relative_path=packet_relative_path,
            packet_checksum=packet_checksum,
            packet_title=packet_title,
            target_executor=target_executor,
            required_reads=required_reads,
            next_action=next_action,
            expected_output=expected_output,
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_replay(
        self,
        index: KernelIndex,
        scope_type: str | None = None,
        scope_ref: str | None = None,
    ) -> ScheduleLineageReplayReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [
                r for r in index.records_by_type("schedule_lineage_replay_receipt")
                if isinstance(r, ScheduleLineageReplayReceipt)
            ]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_lineage_replay_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleResumeProjectionError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def latest_receipt(
        self,
        index: KernelIndex,
        scope_type: str | None = None,
        scope_ref: str | None = None,
    ) -> ScheduleResumeProjectionReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [
                r for r in index.records_by_type("schedule_resume_projection_receipt")
                if isinstance(r, ScheduleResumeProjectionReceipt)
            ]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_resume_projection_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleResumeProjectionError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleResumeProjectionReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_lineage_replay_receipt_id": receipt.source_schedule_lineage_replay_receipt_id,
            "source_schedule_lineage_archive_receipt_id": receipt.source_schedule_lineage_archive_receipt_id,
            "source_schedule_receipt_id": receipt.source_schedule_receipt_id,
            "source_schedule_dispatch_reconciliation_receipt_id": receipt.source_schedule_dispatch_reconciliation_receipt_id,
            "source_schedule_completion_release_receipt_id": receipt.source_schedule_completion_release_receipt_id,
            "source_schedule_settlement_receipt_id": receipt.source_schedule_settlement_receipt_id,
            "work_unit_id": receipt.work_unit_id,
            "active_candidate_id": receipt.active_candidate_id,
            "active_candidate_title": receipt.active_candidate_title,
            "active_cycle_stage": receipt.active_cycle_stage,
            "projection_action": receipt.projection_action,
            "resume_ready": receipt.resume_ready,
            "packet_type": receipt.packet_type,
            "packet_path": receipt.packet_path,
            "packet_relative_path": receipt.packet_relative_path,
            "packet_checksum": receipt.packet_checksum,
            "packet_title": receipt.packet_title,
            "target_executor": receipt.target_executor,
            "required_reads": list(receipt.required_reads),
            "next_action": receipt.next_action,
            "expected_output": list(receipt.expected_output),
            "warnings": list(receipt.warnings),
        }

    @staticmethod
    def _required_reads(schedule, dispatch: ScheduleDispatchReconciliationReceipt | None, scope_ref: str) -> tuple[str, ...]:
        ordered: list[str] = []
        for item in (*schedule.requested_reads, scope_ref):
            if item and item not in ordered:
                ordered.append(item)
        if dispatch is not None and dispatch.dispatch_packet_path and dispatch.dispatch_packet_path not in ordered:
            ordered.append(dispatch.dispatch_packet_path)
        return tuple(ordered)

    @staticmethod
    def _next_action(stage: str, candidate_title: str, dispatch: ScheduleDispatchReconciliationReceipt | None) -> str:
        if stage == "ACTIVE_SCHEDULED":
            return f"Resume the active scheduled cycle `{candidate_title}` by reconciling it into dispatch or assignment progress."
        if stage == "ACTIVE_DISPATCHED":
            target = dispatch.work_unit_id if dispatch is not None and dispatch.work_unit_id else "the active work unit"
            return f"Resume the dispatched active cycle `{candidate_title}` by continuing execution for {target}."
        if stage == "ACTIVE_COMPLETED_AWAITING_SETTLEMENT":
            return f"Resume the active cycle `{candidate_title}` by settling the completed execution and deciding lawful future re-entry."
        return "No active resume step is available."

    @staticmethod
    def _expected_output(stage: str, dispatch: ScheduleDispatchReconciliationReceipt | None) -> tuple[str, ...]:
        if stage == "ACTIVE_SCHEDULED":
            return ("dispatch reconciliation witness", "assignment progress")
        if stage == "ACTIVE_DISPATCHED":
            target = dispatch.work_unit_id if dispatch is not None and dispatch.work_unit_id else "active work unit"
            return (f"terminal execution result for {target}", "commit delta or equivalent execution evidence")
        if stage == "ACTIVE_COMPLETED_AWAITING_SETTLEMENT":
            return ("schedule settlement witness", "future re-entry decision")
        return ()


IonScheduleResumeProjectionManager = KernelScheduleResumeProjectionManager


def schedule_resume_projection_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-resume-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _render_resume_role_session(
    *,
    created_at: str,
    status: str,
    role: str,
    scope_type: str,
    scope_ref: str,
    candidate_title: str,
    active_cycle_stage: str,
    next_action: str,
    required_reads: tuple[str, ...],
    expected_output: tuple[str, ...],
) -> str:
    lines = [
        "---",
        "type: role_session",
        "template: ROLE_SESSION",
        f"created: {created_at}",
        f"status: {status}",
        f"role: {role}",
        f"objective: Resume active cycle for {candidate_title}",
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
        next_action,
        "",
        "## Source Task / Objective",
        "",
        f"- scope: {scope_type}:{scope_ref}",
        f"- active_cycle_stage: {active_cycle_stage}",
        f"- objective: Resume active cycle for {candidate_title}",
        "",
        "## Required Reads",
        "",
    ]
    if required_reads:
        lines.extend(f"- {item}" for item in required_reads)
    else:
        lines.append("- no explicit required reads")
    lines.extend([
        "",
        "## Expected Output",
        "",
    ])
    if expected_output:
        lines.extend(f"- {item}" for item in expected_output)
    else:
        lines.append("- one bounded continuation artifact")
    lines.extend([
        "",
        "## Next Target",
        "",
        "- next_role: operator or explicit follow-up executor",
        "",
        "## Notes",
        "",
        "- Derived from replayed active-cycle witness only.",
        "- Preserve canonical packet, dispatch, and schedule law.",
    ])
    return "\n".join(lines) + "\n"


def _resolve_output_path(workspace_root: str | Path | None, output_path: str | Path) -> Path:
    candidate = Path(output_path)
    if candidate.is_absolute():
        return candidate.resolve()
    if workspace_root is None:
        return candidate.resolve()
    return (Path(workspace_root).resolve() / candidate).resolve()


def _relative_to_root(path: Path, root: str | Path | None) -> str | None:
    if root is None:
        return None
    try:
        return str(path.resolve().relative_to(Path(root).resolve()))
    except ValueError:
        return None


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
