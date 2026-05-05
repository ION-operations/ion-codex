"""M15 activation-summary handoff capsule materialization surfaces."""
from __future__ import annotations
from datetime import datetime
import json
from pathlib import Path
import re
from .authority_lineage import resolve_explicit_authority_override
from .capsule_manager import KernelCapsuleManager
from .index import KernelIndex
from .model import ScheduleActivationHandoffCapsuleReceipt
from .schedule_takeover_activation import KernelScheduleTakeoverActivationManager
from .store import KernelStore
from .threshold import AutomationStage, ContextMode
_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")
class KernelScheduleActivationHandoffCapsuleError(Exception):
    """Raised when M15 handoff capsule materialization cannot complete lawfully."""
class KernelScheduleActivationHandoffCapsuleManager:
    def __init__(self) -> None:
        self._activation_manager = KernelScheduleTakeoverActivationManager()
    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M15_ACTIVATION_HANDOFF_CAPSULE_V1",
            "notes": (
                "M15 turns the validated M14 activation summary into one compact PRE-style handoff capsule.",
                "The capsule remains subordinate to the continuation bundle and takeover-entry validation chain.",
                "Materialization never replaces authoritative bundle/receipt history; it only creates one compact next-executor entry artifact.",
            ),
        }
    def materialize_handoff_capsule(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        workspace_root: str | Path,
        generated_at: str | None = None,
        output_root: str | Path | None = None,
        role: str | None = None,
        status: str = "ACTIVE",
    ) -> ScheduleActivationHandoffCapsuleReceipt:
        timestamp = generated_at or _iso_now()
        workspace = Path(workspace_root).resolve()
        activation = self._activation_manager.latest_receipt(index, scope_type, scope_ref)
        if activation is None:
            raise KernelScheduleActivationHandoffCapsuleError(
                f"No schedule takeover-entry activation receipt exists for {scope_type}:{scope_ref}"
            )
        warnings = list(activation.warnings)
        action = "NO_ACTIVATION_READY_CAPSULE"
        ready = False
        capsule = None
        capsule_root = None
        capsule_json_path = None
        capsule_markdown_path = None
        capsule_manifest_path = None
        callsign = (role or activation.target_executor or "FreshExecutor").strip() or "FreshExecutor"
        if (role or "").strip():
            override = resolve_explicit_authority_override(
                workspace,
                "continuation_target_executor",
                role,
                created_at=timestamp,
            )
            if override.resolved_name is not None:
                callsign = override.resolved_name
            warnings.extend(override.warnings)
            warnings.extend(
                f"AUTHORITY_LINEAGE_RECEIPT[continuation_target_executor] {path}"
                for path in override.receipt_paths
            )
        if activation.activation_ready and activation.activation_summary_path and activation.continuation_bundle_root_path:
            summary_path = Path(activation.activation_summary_path).resolve()
            bundle_root = Path(activation.continuation_bundle_root_path).resolve()
            if not summary_path.exists():
                warnings.append("MISSING_ACTIVATION_SUMMARY")
            else:
                capsule_root = _resolve_output_root(workspace, output_root, bundle_root, scope_type, scope_ref, timestamp)
                capsule_root.mkdir(parents=True, exist_ok=True)
                capsule_dir = capsule_root / "capsules"
                manager = KernelCapsuleManager(capsule_dir, callsign=callsign)
                mission = activation.active_candidate_title or f"Enter validated continuation for {scope_type}:{scope_ref}"
                now = f"Validated activation is ready for {scope_type}:{scope_ref}; enter through the compact handoff capsule."
                next_action = activation.next_action or f"Use the handoff capsule to enter the continuation bundle for {scope_type}:{scope_ref}."
                evidence = tuple(
                    dict.fromkeys(
                        tuple(
                            item
                            for item in (
                                activation.receipt_id,
                                activation.source_schedule_resume_bundle_materialization_receipt_id,
                                activation.source_schedule_resume_projection_receipt_id,
                                activation.source_schedule_lineage_replay_receipt_id,
                                activation.source_schedule_lineage_archive_receipt_id,
                                activation.source_context_perfect_continuation_receipt_id,
                                activation.source_takeover_assessment_receipt_id,
                                activation.activation_summary_relative_path,
                                activation.continuation_bundle_root_relative_path,
                                activation.continuation_bundle_manifest_relative_path,
                                activation.continuation_bundle_role_session_relative_path,
                            )
                            if item
                        )
                    )
                )
                must_not = (
                    "Do not bypass the required reads listed by the validated activation chain.",
                    "Do not mutate outside the bound continuation scope.",
                    "Do not treat the capsule as authority over the underlying continuation bundle or receipts.",
                )
                handoff = _render_handoff_text(
                    target_executor=callsign,
                    scope_type=scope_type,
                    scope_ref=scope_ref,
                    active_candidate_title=activation.active_candidate_title,
                    active_cycle_stage=activation.active_cycle_stage,
                    activation_summary_relative_path=activation.activation_summary_relative_path,
                    continuation_bundle_root_relative_path=activation.continuation_bundle_root_relative_path,
                    continuation_bundle_role_session_relative_path=activation.continuation_bundle_role_session_relative_path,
                    next_action=next_action,
                )
                metadata = {
                    "status": status,
                    "scope_type": scope_type,
                    "scope_ref": scope_ref,
                    "active_cycle_stage": activation.active_cycle_stage,
                    "work_unit_id": activation.work_unit_id,
                    "active_candidate_id": activation.active_candidate_id,
                    "active_candidate_title": activation.active_candidate_title,
                    "source_schedule_takeover_entry_activation_receipt_id": activation.receipt_id,
                    "source_schedule_resume_bundle_materialization_receipt_id": activation.source_schedule_resume_bundle_materialization_receipt_id,
                    "source_schedule_resume_projection_receipt_id": activation.source_schedule_resume_projection_receipt_id,
                    "source_schedule_lineage_replay_receipt_id": activation.source_schedule_lineage_replay_receipt_id,
                    "source_schedule_lineage_archive_receipt_id": activation.source_schedule_lineage_archive_receipt_id,
                    "source_context_perfect_continuation_receipt_id": activation.source_context_perfect_continuation_receipt_id,
                    "source_takeover_assessment_receipt_id": activation.source_takeover_assessment_receipt_id,
                    "selected_capability_id": activation.selected_capability_id,
                    "selected_capability_executor_id": activation.selected_capability_executor_id,
                    "selected_capability_carrier": None if activation.selected_capability_carrier is None else activation.selected_capability_carrier.value,
                    "activation_summary_relative_path": activation.activation_summary_relative_path,
                    "continuation_bundle_root_relative_path": activation.continuation_bundle_root_relative_path,
                    "continuation_bundle_manifest_relative_path": activation.continuation_bundle_manifest_relative_path,
                    "continuation_bundle_role_session_relative_path": activation.continuation_bundle_role_session_relative_path,
                    "entry_packet_relative_path": activation.entry_packet_relative_path,
                    "required_reads": list(activation.required_reads),
                }
                capsule = manager.write_pre(
                    mission=mission,
                    now=now,
                    must_not=must_not,
                    evidence=evidence,
                    next_action=next_action,
                    handoff=handoff,
                    context_mode=ContextMode.IDE_MANUAL,
                    automation_stage=AutomationStage.MANUAL,
                    route_surface="SCHEDULE_ACTIVATION_HANDOFF_CAPSULE",
                    confidence_band="HIGH",
                    drift_status="CLEAR",
                    metadata=metadata,
                )
                capsule_json_path = _latest_capsule_path(capsule_dir)
                capsule_markdown_path = (capsule_root / "01_handoff_capsule.md").resolve()
                capsule_markdown_path.write_text(manager.render_projection(capsule) + "\n", encoding="utf-8")
                capsule_manifest_path = (capsule_root / "02_handoff_capsule_manifest.json").resolve()
                capsule_manifest_path.write_text(
                    json.dumps(
                        {
                            "proof_kind": "SCHEDULE_ACTIVATION_HANDOFF_CAPSULE",
                            "created_at": timestamp,
                            "scope_type": scope_type,
                            "scope_ref": scope_ref,
                            "target_executor": callsign,
                            "capsule_id": capsule.capsule_id,
                            "capsule_type": capsule.capsule_type,
                            "capsule_json_relative_path": _relative_to_root(capsule_json_path, workspace),
                            "capsule_markdown_relative_path": _relative_to_root(capsule_markdown_path, workspace),
                            "activation_summary_relative_path": activation.activation_summary_relative_path,
                            "continuation_bundle_root_relative_path": activation.continuation_bundle_root_relative_path,
                            "continuation_bundle_manifest_relative_path": activation.continuation_bundle_manifest_relative_path,
                            "continuation_bundle_role_session_relative_path": activation.continuation_bundle_role_session_relative_path,
                            "entry_packet_relative_path": activation.entry_packet_relative_path,
                            "required_reads": list(activation.required_reads),
                            "source_schedule_takeover_entry_activation_receipt_id": activation.receipt_id,
                        },
                        indent=2,
                        sort_keys=True,
                    ) + "\n",
                    encoding="utf-8",
                )
                action = "MATERIALIZED_HANDOFF_CAPSULE"
                ready = True
        elif not activation.activation_ready:
            warnings.append("ACTIVATION_NOT_READY")
        receipt = ScheduleActivationHandoffCapsuleReceipt(
            receipt_id=schedule_activation_handoff_capsule_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_takeover_entry_activation_receipt_id=activation.receipt_id,
            source_schedule_resume_bundle_materialization_receipt_id=activation.source_schedule_resume_bundle_materialization_receipt_id,
            source_schedule_resume_projection_receipt_id=activation.source_schedule_resume_projection_receipt_id,
            source_schedule_lineage_replay_receipt_id=activation.source_schedule_lineage_replay_receipt_id,
            source_schedule_lineage_archive_receipt_id=activation.source_schedule_lineage_archive_receipt_id,
            source_context_perfect_continuation_receipt_id=activation.source_context_perfect_continuation_receipt_id,
            source_takeover_assessment_receipt_id=activation.source_takeover_assessment_receipt_id,
            work_unit_id=activation.work_unit_id,
            active_candidate_id=activation.active_candidate_id,
            active_candidate_title=activation.active_candidate_title,
            active_cycle_stage=activation.active_cycle_stage,
            capsule_materialization_action=action,
            handoff_capsule_ready=ready,
            target_executor=callsign,
            selected_capability_id=activation.selected_capability_id,
            selected_capability_executor_id=activation.selected_capability_executor_id,
            selected_capability_carrier=activation.selected_capability_carrier,
            capsule_id=(None if capsule is None else capsule.capsule_id),
            capsule_type=(None if capsule is None else capsule.capsule_type),
            capsule_callsign=(None if capsule is None else capsule.callsign),
            handoff_capsule_root_path=(None if capsule_root is None else str(capsule_root)),
            handoff_capsule_root_relative_path=(None if capsule_root is None else _relative_to_root(capsule_root, workspace)),
            handoff_capsule_json_relative_path=(None if capsule_json_path is None else _relative_to_root(capsule_json_path, workspace)),
            handoff_capsule_markdown_relative_path=(None if capsule_markdown_path is None else _relative_to_root(capsule_markdown_path, workspace)),
            handoff_capsule_manifest_relative_path=(None if capsule_manifest_path is None else _relative_to_root(capsule_manifest_path, workspace)),
            continuation_bundle_root_relative_path=activation.continuation_bundle_root_relative_path,
            activation_summary_relative_path=activation.activation_summary_relative_path,
            entry_packet_relative_path=activation.entry_packet_relative_path,
            required_reads=activation.required_reads,
            next_action=activation.next_action,
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt
    def latest_receipt(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleActivationHandoffCapsuleReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type("schedule_activation_handoff_capsule_receipt") if isinstance(r, ScheduleActivationHandoffCapsuleReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_activation_handoff_capsule_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleActivationHandoffCapsuleError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]
    def render_receipt_projection(self, receipt: ScheduleActivationHandoffCapsuleReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_takeover_entry_activation_receipt_id": receipt.source_schedule_takeover_entry_activation_receipt_id,
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
            "capsule_materialization_action": receipt.capsule_materialization_action,
            "handoff_capsule_ready": receipt.handoff_capsule_ready,
            "target_executor": receipt.target_executor,
            "selected_capability_id": receipt.selected_capability_id,
            "selected_capability_executor_id": receipt.selected_capability_executor_id,
            "selected_capability_carrier": None if receipt.selected_capability_carrier is None else receipt.selected_capability_carrier.value,
            "capsule_id": receipt.capsule_id,
            "capsule_type": receipt.capsule_type,
            "capsule_callsign": receipt.capsule_callsign,
            "handoff_capsule_root_path": receipt.handoff_capsule_root_path,
            "handoff_capsule_root_relative_path": receipt.handoff_capsule_root_relative_path,
            "handoff_capsule_json_relative_path": receipt.handoff_capsule_json_relative_path,
            "handoff_capsule_markdown_relative_path": receipt.handoff_capsule_markdown_relative_path,
            "handoff_capsule_manifest_relative_path": receipt.handoff_capsule_manifest_relative_path,
            "continuation_bundle_root_relative_path": receipt.continuation_bundle_root_relative_path,
            "activation_summary_relative_path": receipt.activation_summary_relative_path,
            "entry_packet_relative_path": receipt.entry_packet_relative_path,
            "required_reads": list(receipt.required_reads),
            "next_action": receipt.next_action,
            "warnings": list(receipt.warnings),
        }
def schedule_activation_handoff_capsule_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-handoff-capsule-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"
def _resolve_output_root(workspace: Path, output_root: str | Path | None, bundle_root: Path, scope_type: str, scope_ref: str, created_at: str) -> Path:
    if output_root is not None:
        out = Path(output_root)
        if not out.is_absolute():
            out = workspace / out
        return out.resolve()
    return (bundle_root / "04_handoff_capsule").resolve()
def _latest_capsule_path(capsule_dir: Path) -> Path:
    candidates = sorted(capsule_dir.glob("*.json"))
    if not candidates:
        raise KernelScheduleActivationHandoffCapsuleError("No capsule file was written during handoff capsule materialization.")
    return candidates[-1].resolve()
def _render_handoff_text(*, target_executor: str, scope_type: str, scope_ref: str, active_candidate_title: str | None, active_cycle_stage: str, activation_summary_relative_path: str | None, continuation_bundle_root_relative_path: str | None, continuation_bundle_role_session_relative_path: str | None, next_action: str | None) -> str:
    lines = [
        f"Validated takeover entry is ready for {target_executor}.",
        f"Scope: {scope_type}:{scope_ref}",
        f"Active cycle stage: {active_cycle_stage}",
        f"Candidate: {active_candidate_title or 'NONE'}",
        f"Activation summary: {activation_summary_relative_path or 'NONE'}",
        f"Continuation bundle root: {continuation_bundle_root_relative_path or 'NONE'}",
        f"Role-session path: {continuation_bundle_role_session_relative_path or 'NONE'}",
        f"Next action: {next_action or 'NONE'}",
    ]
    return "\n".join(lines)
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
