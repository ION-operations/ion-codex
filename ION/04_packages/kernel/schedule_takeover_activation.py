"""M14 continuation-bundle takeover entry / activation validation surfaces."""

from __future__ import annotations

from datetime import datetime
import hashlib
from pathlib import Path
import re

from .authority_lineage import resolve_explicit_authority_override
from .executor_registry import KernelExecutorCapabilityRegistry
from .index import KernelIndex
from .model import ContextPerfectContinuationReceipt, ScheduleCarrier, ScheduleTakeoverEntryActivationReceipt
from .schedule_resume_bundle import KernelScheduleResumeBundleMaterializationManager
from .store import KernelStore
from .takeover import KernelTakeoverManager

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleTakeoverActivationError(Exception):
    """Raised when M14 takeover-entry activation validation cannot complete lawfully."""


class KernelScheduleTakeoverActivationManager:
    def __init__(self) -> None:
        self._bundle_manager = KernelScheduleResumeBundleMaterializationManager()
        self._takeover_manager = KernelTakeoverManager()
        self._registry = KernelExecutorCapabilityRegistry()

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M14_CONTINUATION_BUNDLE_TAKEOVER_ENTRY_V1",
            "notes": (
                "M14 evaluates the latest schedule-derived continuation bundle as an executor-entry activation artifact.",
                "Validation remains subordinate to continuation and takeover proof law.",
                "Activation validation never dispatches work; it only proves readiness and writes one minimal entry summary.",
            ),
        }

    def validate_activation(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        workspace_root: str | Path,
        generated_at: str | None = None,
        summary_output_path: str | Path | None = None,
        role: str | None = None,
        status: str = "ACTIVE",
    ) -> ScheduleTakeoverEntryActivationReceipt:
        timestamp = generated_at or _iso_now()
        workspace = Path(workspace_root).resolve()
        bundle_receipt = self._bundle_manager.latest_receipt(index, scope_type, scope_ref)
        if bundle_receipt is None:
            raise KernelScheduleTakeoverActivationError(
                f"No schedule resume bundle materialization receipt exists for {scope_type}:{scope_ref}"
            )

        continuation_receipt = None
        if bundle_receipt.source_context_perfect_continuation_receipt_id:
            maybe = index.get("context_perfect_continuation_receipt", bundle_receipt.source_context_perfect_continuation_receipt_id)
            if isinstance(maybe, ContextPerfectContinuationReceipt):
                continuation_receipt = maybe

        warnings = list(bundle_receipt.warnings)
        action = "NO_CONTINUATION_BUNDLE_AVAILABLE"
        ready = False
        takeover_receipt = None
        selected_capability = None
        entry_packet_path = None
        entry_packet_relative_path = None
        entry_packet_checksum = None
        entry_packet_type = None
        summary_path = None
        target_executor = (role or bundle_receipt.target_executor or "FreshExecutor").strip() or "FreshExecutor"
        next_action = bundle_receipt.next_action
        if (role or "").strip():
            override = resolve_explicit_authority_override(
                workspace,
                "continuation_target_executor",
                role,
                created_at=timestamp,
            )
            if override.resolved_name is not None:
                target_executor = override.resolved_name
            warnings.extend(override.warnings)
            warnings.extend(
                f"AUTHORITY_LINEAGE_RECEIPT[continuation_target_executor] {path}"
                for path in override.receipt_paths
            )

        if continuation_receipt is not None and bundle_receipt.continuation_bundle_role_session_relative_path:
            role_session_path = (workspace / bundle_receipt.continuation_bundle_role_session_relative_path).resolve()
            manifest_path = None
            if bundle_receipt.continuation_bundle_manifest_relative_path:
                manifest_path = (workspace / bundle_receipt.continuation_bundle_manifest_relative_path).resolve()
            if not role_session_path.exists() or manifest_path is None or not manifest_path.exists():
                action = "BUNDLE_INCOMPLETE"
                if not role_session_path.exists():
                    warnings.append("MISSING_ROLE_SESSION")
                if manifest_path is None or not manifest_path.exists():
                    warnings.append("MISSING_MANIFEST")
            else:
                assessment = self._takeover_manager.assess_packet_path(role_session_path, expected_type="role_session", allow_legacy=False)
                takeover_receipt = self._takeover_manager.persist_takeover_receipt(
                    store,
                    index,
                    assessment,
                    packet_path=role_session_path,
                    workspace_root=workspace,
                    created_at=timestamp,
                )
                selection = self._registry.select_capability(
                    index,
                    preferred_carrier=ScheduleCarrier.IDE_MANUAL,
                    scope_type=scope_type,
                    scope_ref=scope_ref,
                    executor_hint=target_executor,
                    packet_family="role_session",
                )
                selected_capability = selection.selected_capability
                warnings.extend(selection.warnings)
                entry_packet_type = "role_session"
                entry_packet_path = str(role_session_path)
                entry_packet_relative_path = _relative_to_root(role_session_path, workspace)
                entry_packet_checksum = hashlib.sha256(role_session_path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
                if not assessment.valid:
                    action = "TAKEOVER_ENTRY_INVALID"
                    warnings.extend(assessment.warnings)
                elif selected_capability is None:
                    action = "TAKEOVER_ENTRY_REQUIRES_EXECUTOR"
                    warnings.append("NO_ELIGIBLE_EXECUTOR_CAPABILITY")
                else:
                    action = "ACTIVATION_READY"
                    ready = True
                    summary_path = _resolve_summary_output(workspace, summary_output_path, continuation_receipt.bundle_root_path, scope_type, scope_ref, timestamp)
                    summary_path.parent.mkdir(parents=True, exist_ok=True)
                    summary_path.write_text(
                        _render_activation_summary(
                            created_at=timestamp,
                            status=status,
                            target_executor=target_executor,
                            capability_id=selected_capability.capability_id,
                            carrier=selected_capability.carrier.value,
                            scope_type=scope_type,
                            scope_ref=scope_ref,
                            active_candidate_title=bundle_receipt.active_candidate_title,
                            active_cycle_stage=bundle_receipt.active_cycle_stage,
                            required_reads=bundle_receipt.required_reads,
                            next_action=bundle_receipt.next_action,
                            bundle_root_relative_path=bundle_receipt.continuation_bundle_root_relative_path,
                            role_session_relative_path=bundle_receipt.continuation_bundle_role_session_relative_path,
                            manifest_relative_path=bundle_receipt.continuation_bundle_manifest_relative_path,
                        ),
                        encoding="utf-8",
                    )
                    next_action = (
                        f"Enter through the validated continuation bundle for {scope_type}:{scope_ref} using "
                        f"{target_executor} and the activation summary."
                    )
        else:
            warnings.append("NO_CONTINUATION_BUNDLE")

        receipt = ScheduleTakeoverEntryActivationReceipt(
            receipt_id=schedule_takeover_entry_activation_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_resume_bundle_materialization_receipt_id=bundle_receipt.receipt_id,
            source_schedule_resume_projection_receipt_id=bundle_receipt.source_schedule_resume_projection_receipt_id,
            source_schedule_lineage_replay_receipt_id=bundle_receipt.source_schedule_lineage_replay_receipt_id,
            source_schedule_lineage_archive_receipt_id=bundle_receipt.source_schedule_lineage_archive_receipt_id,
            source_context_perfect_continuation_receipt_id=bundle_receipt.source_context_perfect_continuation_receipt_id,
            source_takeover_assessment_receipt_id=(None if takeover_receipt is None else takeover_receipt.receipt_id),
            work_unit_id=bundle_receipt.work_unit_id,
            active_candidate_id=bundle_receipt.active_candidate_id,
            active_candidate_title=bundle_receipt.active_candidate_title,
            active_cycle_stage=bundle_receipt.active_cycle_stage,
            activation_action=action,
            activation_ready=ready,
            target_executor=target_executor,
            selected_capability_id=(None if selected_capability is None else selected_capability.capability_id),
            selected_capability_executor_id=(None if selected_capability is None else selected_capability.executor_id),
            selected_capability_carrier=(None if selected_capability is None else selected_capability.carrier),
            entry_packet_type=entry_packet_type,
            entry_packet_path=entry_packet_path,
            entry_packet_relative_path=entry_packet_relative_path,
            entry_packet_checksum=entry_packet_checksum,
            continuation_bundle_root_path=bundle_receipt.continuation_bundle_root_path,
            continuation_bundle_root_relative_path=bundle_receipt.continuation_bundle_root_relative_path,
            continuation_bundle_manifest_relative_path=bundle_receipt.continuation_bundle_manifest_relative_path,
            continuation_bundle_role_session_relative_path=bundle_receipt.continuation_bundle_role_session_relative_path,
            activation_summary_path=(None if summary_path is None else str(summary_path)),
            activation_summary_relative_path=(None if summary_path is None else _relative_to_root(summary_path, workspace)),
            required_reads=bundle_receipt.required_reads,
            next_action=next_action,
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_receipt(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleTakeoverEntryActivationReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type("schedule_takeover_entry_activation_receipt") if isinstance(r, ScheduleTakeoverEntryActivationReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_takeover_entry_activation_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleTakeoverActivationError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleTakeoverEntryActivationReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_resume_bundle_materialization_receipt_id": receipt.source_schedule_resume_bundle_materialization_receipt_id,
            "source_schedule_resume_projection_receipt_id": receipt.source_schedule_resume_projection_receipt_id,
            "source_schedule_lineage_replay_receipt_id": receipt.source_schedule_lineage_replay_receipt_id,
            "source_schedule_lineage_archive_receipt_id": receipt.source_schedule_lineage_archive_receipt_id,
            "source_context_perfect_continuation_receipt_id": receipt.source_context_perfect_continuation_receipt_id,
            "source_takeover_assessment_receipt_id": receipt.source_takeover_assessment_receipt_id,
            "work_unit_id": receipt.work_unit_id,
            "active_candidate_id": receipt.active_candidate_id,
            "active_candidate_title": receipt.active_candidate_title,
            "active_cycle_stage": receipt.active_cycle_stage,
            "activation_action": receipt.activation_action,
            "activation_ready": receipt.activation_ready,
            "target_executor": receipt.target_executor,
            "selected_capability_id": receipt.selected_capability_id,
            "selected_capability_executor_id": receipt.selected_capability_executor_id,
            "selected_capability_carrier": None if receipt.selected_capability_carrier is None else receipt.selected_capability_carrier.value,
            "entry_packet_type": receipt.entry_packet_type,
            "entry_packet_path": receipt.entry_packet_path,
            "entry_packet_relative_path": receipt.entry_packet_relative_path,
            "entry_packet_checksum": receipt.entry_packet_checksum,
            "continuation_bundle_root_path": receipt.continuation_bundle_root_path,
            "continuation_bundle_root_relative_path": receipt.continuation_bundle_root_relative_path,
            "continuation_bundle_manifest_relative_path": receipt.continuation_bundle_manifest_relative_path,
            "continuation_bundle_role_session_relative_path": receipt.continuation_bundle_role_session_relative_path,
            "activation_summary_path": receipt.activation_summary_path,
            "activation_summary_relative_path": receipt.activation_summary_relative_path,
            "required_reads": list(receipt.required_reads),
            "next_action": receipt.next_action,
            "warnings": list(receipt.warnings),
        }


IonScheduleTakeoverEntryActivationManager = KernelScheduleTakeoverActivationManager


def schedule_takeover_entry_activation_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-activation-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _resolve_summary_output(workspace: Path, output_path: str | Path | None, bundle_root_path: str | None, scope_type: str, scope_ref: str, created_at: str) -> Path:
    if output_path is not None:
        out = Path(output_path)
        if not out.is_absolute():
            out = workspace / out
        return out.resolve()
    if bundle_root_path:
        return (Path(bundle_root_path).resolve() / '03_takeover_activation_summary.md').resolve()
    return (workspace / 'ION/05_context/history/schedule_activation_entries' / _slug(scope_type) / _slug(scope_ref) / f'{_slug(created_at)}.md').resolve()


def _render_activation_summary(*, created_at: str, status: str, target_executor: str, capability_id: str, carrier: str, scope_type: str, scope_ref: str, active_candidate_title: str | None, active_cycle_stage: str, required_reads: tuple[str, ...], next_action: str | None, bundle_root_relative_path: str | None, role_session_relative_path: str | None, manifest_relative_path: str | None) -> str:
    lines = [
        '---',
        'type: role_session',
        f'created: {created_at}',
        f'status: {status}',
        f'role: {target_executor}',
        f'scope: {scope_type}:{scope_ref}',
        'purpose: M14 takeover entry activation summary',
        '---',
        '',
        f'# Activation Entry — {target_executor}',
        '',
        f'- candidate: {active_candidate_title or "NONE"}',
        f'- active_cycle_stage: {active_cycle_stage}',
        f'- selected_capability_id: {capability_id}',
        f'- carrier: {carrier}',
        f'- bundle_root: {bundle_root_relative_path or "NONE"}',
        f'- role_session_path: {role_session_relative_path or "NONE"}',
        f'- manifest_path: {manifest_relative_path or "NONE"}',
        '',
        '## Required Reads',
    ]
    if required_reads:
        lines.extend(f'- {item}' for item in required_reads)
    else:
        lines.append('- NONE')
    lines.extend(['', '## Next Action', next_action or 'No next action recorded.', ''])
    return "\n".join(lines) + "\n"


def _relative_to_root(path: Path, root: str | Path | None) -> str | None:
    if root is None:
        return None
    try:
        return str(path.resolve().relative_to(Path(root).resolve()))
    except ValueError:
        return None


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub('-', value.lower()).strip('-') or 'value'


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec='seconds')
