
"""M13 resume-projection continuation bundle materialization surfaces."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re

from .authority_lineage import resolve_explicit_authority_override
from .continuation import KernelContextPerfectContinuationManager
from .index import KernelIndex
from .model import ScheduleResumeBundleMaterializationReceipt, ScheduleResumeProjectionReceipt
from .schedule_resume_projection import KernelScheduleResumeProjectionManager
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleResumeBundleMaterializationError(Exception):
    """Raised when M13 resume-bundle materialization cannot complete lawfully."""


class KernelScheduleResumeBundleMaterializationManager:
    def __init__(self) -> None:
        self._resume_manager = KernelScheduleResumeProjectionManager()
        self._continuation_manager = KernelContextPerfectContinuationManager()

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M13_RESUME_BUNDLE_MATERIALIZATION_V1",
            "notes": (
                "M13 turns an M12 resume projection into one context-perfect continuation bundle.",
                "Materialization must remain subordinate to existing continuation / takeover proof law.",
                "When no lawful resume packet exists, M13 must persist explicit no-bundle witness instead of faking continuation.",
            ),
        }

    def materialize_bundle(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        workspace_root: str | Path,
        generated_at: str | None = None,
        packet_output_path: str | Path | None = None,
        bundle_output_root: str | Path | None = None,
        status: str = "ACTIVE",
        role: str | None = None,
    ) -> ScheduleResumeBundleMaterializationReceipt:
        timestamp = generated_at or _iso_now()
        workspace = Path(workspace_root).resolve()
        explicit_role = (role or "").strip() or None
        projection = self._resume_manager.latest_receipt(index, scope_type, scope_ref)
        if projection is None:
            raise KernelScheduleResumeBundleMaterializationError(
                f"No schedule resume projection receipt exists for {scope_type}:{scope_ref}"
            )

        active_projection = projection
        if active_projection.resume_ready and not active_projection.packet_path:
            packet_output = packet_output_path or _default_packet_output(scope_type, scope_ref, timestamp)
            active_projection = self._resume_manager.project_resume(
                store,
                index,
                scope_type=scope_type,
                scope_ref=scope_ref,
                workspace_root=workspace,
                output_path=packet_output,
                generated_at=timestamp,
                status=status,
                role=explicit_role,
            )

        action = "NO_RESUME_PACKET_AVAILABLE"
        continuation_receipt = None
        warnings = list(active_projection.warnings)
        target_executor = (active_projection.target_executor or "FreshExecutor").strip() or "FreshExecutor"
        if explicit_role is not None and active_projection.packet_path:
            override = resolve_explicit_authority_override(
                workspace,
                "continuation_target_executor",
                explicit_role,
                created_at=timestamp,
            )
            if override.resolved_name is not None:
                target_executor = override.resolved_name
            warnings.extend(override.warnings)
            warnings.extend(
                f"AUTHORITY_LINEAGE_RECEIPT[continuation_target_executor] {path}"
                for path in override.receipt_paths
            )
        if active_projection.resume_ready and active_projection.packet_path:
            continuation_receipt = self._continuation_manager.prove_packet_continuation(
                store,
                index,
                active_projection.packet_path,
                workspace_root=workspace,
                repo_root=workspace,
                expected_type="role_session",
                allow_legacy=False,
                role=target_executor,
                authority_resolve_role=False,
                output_root=bundle_output_root or _default_bundle_output(scope_type, scope_ref, timestamp),
                created_at=timestamp,
                status=status,
            )
            action = "MATERIALIZED_CONTINUATION_BUNDLE"
            warnings.extend(continuation_receipt.warnings)

        receipt = ScheduleResumeBundleMaterializationReceipt(
            receipt_id=schedule_resume_bundle_materialization_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_resume_projection_receipt_id=active_projection.receipt_id,
            source_schedule_lineage_replay_receipt_id=active_projection.source_schedule_lineage_replay_receipt_id,
            source_schedule_lineage_archive_receipt_id=active_projection.source_schedule_lineage_archive_receipt_id,
            source_context_perfect_continuation_receipt_id=(None if continuation_receipt is None else continuation_receipt.receipt_id),
            work_unit_id=active_projection.work_unit_id,
            active_candidate_id=active_projection.active_candidate_id,
            active_candidate_title=active_projection.active_candidate_title,
            active_cycle_stage=active_projection.active_cycle_stage,
            materialization_action=action,
            resume_ready=active_projection.resume_ready,
            packet_type=active_projection.packet_type,
            packet_path=active_projection.packet_path,
            packet_relative_path=active_projection.packet_relative_path,
            packet_checksum=active_projection.packet_checksum,
            target_executor=target_executor,
            required_reads=active_projection.required_reads,
            next_action=active_projection.next_action,
            continuation_bundle_root_path=(None if continuation_receipt is None else continuation_receipt.bundle_root_path),
            continuation_bundle_root_relative_path=(None if continuation_receipt is None else continuation_receipt.bundle_root_relative_path),
            continuation_bundle_packet_relative_path=(None if continuation_receipt is None else continuation_receipt.bundle_packet_relative_path),
            continuation_bundle_role_session_relative_path=(None if continuation_receipt is None else continuation_receipt.bundle_role_session_relative_path),
            continuation_bundle_manifest_relative_path=(None if continuation_receipt is None else continuation_receipt.bundle_manifest_relative_path),
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_receipt(
        self,
        index: KernelIndex,
        scope_type: str | None = None,
        scope_ref: str | None = None,
    ) -> ScheduleResumeBundleMaterializationReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [
                r for r in index.records_by_type("schedule_resume_bundle_materialization_receipt")
                if isinstance(r, ScheduleResumeBundleMaterializationReceipt)
            ]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_resume_bundle_materialization_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleResumeBundleMaterializationError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleResumeBundleMaterializationReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_resume_projection_receipt_id": receipt.source_schedule_resume_projection_receipt_id,
            "source_schedule_lineage_replay_receipt_id": receipt.source_schedule_lineage_replay_receipt_id,
            "source_schedule_lineage_archive_receipt_id": receipt.source_schedule_lineage_archive_receipt_id,
            "source_context_perfect_continuation_receipt_id": receipt.source_context_perfect_continuation_receipt_id,
            "work_unit_id": receipt.work_unit_id,
            "active_candidate_id": receipt.active_candidate_id,
            "active_candidate_title": receipt.active_candidate_title,
            "active_cycle_stage": receipt.active_cycle_stage,
            "materialization_action": receipt.materialization_action,
            "resume_ready": receipt.resume_ready,
            "packet_type": receipt.packet_type,
            "packet_path": receipt.packet_path,
            "packet_relative_path": receipt.packet_relative_path,
            "packet_checksum": receipt.packet_checksum,
            "target_executor": receipt.target_executor,
            "required_reads": list(receipt.required_reads),
            "next_action": receipt.next_action,
            "continuation_bundle_root_path": receipt.continuation_bundle_root_path,
            "continuation_bundle_root_relative_path": receipt.continuation_bundle_root_relative_path,
            "continuation_bundle_packet_relative_path": receipt.continuation_bundle_packet_relative_path,
            "continuation_bundle_role_session_relative_path": receipt.continuation_bundle_role_session_relative_path,
            "continuation_bundle_manifest_relative_path": receipt.continuation_bundle_manifest_relative_path,
            "warnings": list(receipt.warnings),
        }


IonScheduleResumeBundleMaterializationManager = KernelScheduleResumeBundleMaterializationManager


def schedule_resume_bundle_materialization_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-resume-bundle-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _default_packet_output(scope_type: str, scope_ref: str, created_at: str) -> str:
    return (
        f"ION/05_context/history/schedule_resume_packets/{_slug(scope_type)}/{_slug(scope_ref)}/{_slug(created_at)}/01_role_session.md"
    )


def _default_bundle_output(scope_type: str, scope_ref: str, created_at: str) -> str:
    return (
        f"ION/05_context/history/schedule_resume_continuation/{_slug(scope_type)}/{_slug(scope_ref)}/{_slug(created_at)}"
    )


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
