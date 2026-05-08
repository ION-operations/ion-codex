"""M16 handoff-capsule executor-entry rehearsal surfaces."""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
import re

from .index import KernelIndex
from .model import ScheduleHandoffEntryRehearsalReceipt
from .schedule_handoff_capsule import KernelScheduleActivationHandoffCapsuleManager
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleHandoffEntryRehearsalError(Exception):
    """Raised when M16 handoff-capsule executor-entry rehearsal cannot complete lawfully."""


class KernelScheduleHandoffEntryRehearsalManager:
    def __init__(self) -> None:
        self._handoff_capsule_manager = KernelScheduleActivationHandoffCapsuleManager()

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M16_HANDOFF_ENTRY_REHEARSAL_V1",
            "notes": (
                "M16 replays entry directly from the compact handoff capsule rather than reopening the broader chain manually.",
                "The rehearsal remains subordinate to the existing activation, continuation bundle, and takeover proof chain.",
                "Success means the capsule alone contains enough bounded entry context for the next executor to begin lawfully.",
            ),
        }

    def rehearse_entry(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        workspace_root: str | Path,
        generated_at: str | None = None,
        summary_output_path: str | Path | None = None,
        manifest_output_path: str | Path | None = None,
        status: str = "ACTIVE",
    ) -> ScheduleHandoffEntryRehearsalReceipt:
        timestamp = generated_at or _iso_now()
        workspace = Path(workspace_root).resolve()
        capsule_receipt = self._handoff_capsule_manager.latest_receipt(index, scope_type, scope_ref)
        if capsule_receipt is None:
            raise KernelScheduleHandoffEntryRehearsalError(
                f"No schedule activation handoff capsule receipt exists for {scope_type}:{scope_ref}"
            )
        warnings = list(capsule_receipt.warnings)
        action = "NO_HANDOFF_CAPSULE_READY"
        ready = False
        summary_path = None
        manifest_path = None
        if capsule_receipt.handoff_capsule_ready:
            missing = []
            capsule_root = _resolve_required_path(workspace, capsule_receipt.handoff_capsule_root_relative_path)
            capsule_json = _resolve_required_path(workspace, capsule_receipt.handoff_capsule_json_relative_path)
            capsule_markdown = _resolve_required_path(workspace, capsule_receipt.handoff_capsule_markdown_relative_path)
            capsule_manifest = _resolve_required_path(workspace, capsule_receipt.handoff_capsule_manifest_relative_path)
            activation_summary = _resolve_required_path(workspace, capsule_receipt.activation_summary_relative_path)
            entry_packet = _resolve_required_path(workspace, capsule_receipt.entry_packet_relative_path)
            bundle_root = _resolve_required_path(workspace, capsule_receipt.continuation_bundle_root_relative_path)
            for name, path in (
                ("handoff_capsule_root", capsule_root),
                ("handoff_capsule_json", capsule_json),
                ("handoff_capsule_markdown", capsule_markdown),
                ("handoff_capsule_manifest", capsule_manifest),
                ("activation_summary", activation_summary),
                ("entry_packet", entry_packet),
                ("continuation_bundle_root", bundle_root),
            ):
                if path is None or not path.exists():
                    missing.append(name)
            if missing:
                action = "HANDOFF_CAPSULE_MISSING_FILES"
                warnings.append("MISSING_ENTRY_FILES:" + ",".join(missing))
            else:
                manifest_payload = _load_json(capsule_manifest)
                capsule_payload = _load_json(capsule_json)
                metadata = capsule_payload.get("metadata") or {}
                missing_context = []
                for key in (
                    "activation_summary_relative_path",
                    "continuation_bundle_root_relative_path",
                    "entry_packet_relative_path",
                    "required_reads",
                    "source_schedule_takeover_entry_activation_receipt_id",
                ):
                    value = manifest_payload.get(key, metadata.get(key))
                    if value in (None, "", [], ()): 
                        missing_context.append(key)
                handoff_text = str(capsule_payload.get("handoff") or "").strip()
                next_action = str(capsule_payload.get("next_action") or "").strip()
                now_text = str(capsule_payload.get("now") or "").strip()
                if not handoff_text:
                    missing_context.append("handoff")
                if not next_action:
                    missing_context.append("next_action")
                if not now_text:
                    missing_context.append("now")
                if missing_context:
                    action = "HANDOFF_CAPSULE_INSUFFICIENT_ENTRY_CONTEXT"
                    warnings.append("MISSING_ENTRY_CONTEXT:" + ",".join(dict.fromkeys(missing_context)))
                else:
                    summary_path = _resolve_summary_output(workspace, summary_output_path, capsule_root, scope_type, scope_ref, timestamp)
                    summary_path.parent.mkdir(parents=True, exist_ok=True)
                    summary_path.write_text(
                        _render_entry_rehearsal_summary(
                            created_at=timestamp,
                            status=status,
                            scope_type=scope_type,
                            scope_ref=scope_ref,
                            target_executor=(capsule_receipt.capsule_callsign or capsule_receipt.target_executor),
                            active_candidate_title=capsule_receipt.active_candidate_title,
                            active_cycle_stage=capsule_receipt.active_cycle_stage,
                            capsule_json_relative_path=capsule_receipt.handoff_capsule_json_relative_path,
                            capsule_markdown_relative_path=capsule_receipt.handoff_capsule_markdown_relative_path,
                            capsule_manifest_relative_path=capsule_receipt.handoff_capsule_manifest_relative_path,
                            activation_summary_relative_path=capsule_receipt.activation_summary_relative_path,
                            continuation_bundle_root_relative_path=capsule_receipt.continuation_bundle_root_relative_path,
                            entry_packet_relative_path=capsule_receipt.entry_packet_relative_path,
                            required_reads=capsule_receipt.required_reads,
                            next_action=capsule_receipt.next_action,
                        ) + "\n",
                        encoding="utf-8",
                    )
                    manifest_path = _resolve_manifest_output(workspace, manifest_output_path, capsule_root, scope_type, scope_ref, timestamp)
                    manifest_path.parent.mkdir(parents=True, exist_ok=True)
                    manifest_path.write_text(
                        json.dumps(
                            {
                                "proof_kind": "SCHEDULE_HANDOFF_ENTRY_REHEARSAL",
                                "created_at": timestamp,
                                "scope_type": scope_type,
                                "scope_ref": scope_ref,
                                "target_executor": capsule_receipt.target_executor,
                                "capsule_id": capsule_receipt.capsule_id,
                                "active_cycle_stage": capsule_receipt.active_cycle_stage,
                                "handoff_capsule_json_relative_path": capsule_receipt.handoff_capsule_json_relative_path,
                                "handoff_capsule_markdown_relative_path": capsule_receipt.handoff_capsule_markdown_relative_path,
                                "handoff_capsule_manifest_relative_path": capsule_receipt.handoff_capsule_manifest_relative_path,
                                "activation_summary_relative_path": capsule_receipt.activation_summary_relative_path,
                                "continuation_bundle_root_relative_path": capsule_receipt.continuation_bundle_root_relative_path,
                                "entry_packet_relative_path": capsule_receipt.entry_packet_relative_path,
                                "entry_rehearsal_summary_relative_path": _relative_to_root(summary_path, workspace),
                                "required_reads": list(capsule_receipt.required_reads),
                                "source_schedule_activation_handoff_capsule_receipt_id": capsule_receipt.receipt_id,
                            },
                            indent=2,
                            sort_keys=True,
                        ) + "\n",
                        encoding="utf-8",
                    )
                    action = "REHEARSED_DIRECT_ENTRY"
                    ready = True
        else:
            warnings.append("HANDOFF_CAPSULE_NOT_READY")

        receipt = ScheduleHandoffEntryRehearsalReceipt(
            receipt_id=schedule_handoff_entry_rehearsal_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_activation_handoff_capsule_receipt_id=capsule_receipt.receipt_id,
            source_schedule_takeover_entry_activation_receipt_id=capsule_receipt.source_schedule_takeover_entry_activation_receipt_id,
            source_schedule_resume_bundle_materialization_receipt_id=capsule_receipt.source_schedule_resume_bundle_materialization_receipt_id,
            source_schedule_resume_projection_receipt_id=capsule_receipt.source_schedule_resume_projection_receipt_id,
            source_schedule_lineage_replay_receipt_id=capsule_receipt.source_schedule_lineage_replay_receipt_id,
            source_schedule_lineage_archive_receipt_id=capsule_receipt.source_schedule_lineage_archive_receipt_id,
            source_context_perfect_continuation_receipt_id=capsule_receipt.source_context_perfect_continuation_receipt_id,
            source_takeover_assessment_receipt_id=capsule_receipt.source_takeover_assessment_receipt_id,
            work_unit_id=capsule_receipt.work_unit_id,
            active_candidate_id=capsule_receipt.active_candidate_id,
            active_candidate_title=capsule_receipt.active_candidate_title,
            active_cycle_stage=capsule_receipt.active_cycle_stage,
            entry_rehearsal_action=action,
            entry_rehearsal_ready=ready,
            target_executor=(capsule_receipt.capsule_callsign or capsule_receipt.target_executor),
            selected_capability_id=capsule_receipt.selected_capability_id,
            selected_capability_executor_id=capsule_receipt.selected_capability_executor_id,
            selected_capability_carrier=capsule_receipt.selected_capability_carrier,
            capsule_id=capsule_receipt.capsule_id,
            capsule_type=capsule_receipt.capsule_type,
            capsule_callsign=capsule_receipt.capsule_callsign,
            handoff_capsule_root_relative_path=capsule_receipt.handoff_capsule_root_relative_path,
            handoff_capsule_json_relative_path=capsule_receipt.handoff_capsule_json_relative_path,
            handoff_capsule_markdown_relative_path=capsule_receipt.handoff_capsule_markdown_relative_path,
            handoff_capsule_manifest_relative_path=capsule_receipt.handoff_capsule_manifest_relative_path,
            entry_rehearsal_summary_path=(None if summary_path is None else str(summary_path)),
            entry_rehearsal_summary_relative_path=(None if summary_path is None else _relative_to_root(summary_path, workspace)),
            entry_rehearsal_manifest_relative_path=(None if manifest_path is None else _relative_to_root(manifest_path, workspace)),
            continuation_bundle_root_relative_path=capsule_receipt.continuation_bundle_root_relative_path,
            activation_summary_relative_path=capsule_receipt.activation_summary_relative_path,
            entry_packet_relative_path=capsule_receipt.entry_packet_relative_path,
            required_reads=capsule_receipt.required_reads,
            next_action=(capsule_receipt.next_action if ready else None),
            warnings=tuple(dict.fromkeys(warnings)),
        )
        store.create(receipt)
        index.record_added(receipt)
        return receipt

    def latest_receipt(self, index: KernelIndex, scope_type: str | None = None, scope_ref: str | None = None) -> ScheduleHandoffEntryRehearsalReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [r for r in index.records_by_type("schedule_handoff_entry_rehearsal_receipt") if isinstance(r, ScheduleHandoffEntryRehearsalReceipt)]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_handoff_entry_rehearsal_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleHandoffEntryRehearsalError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleHandoffEntryRehearsalReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_activation_handoff_capsule_receipt_id": receipt.source_schedule_activation_handoff_capsule_receipt_id,
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
            "entry_rehearsal_action": receipt.entry_rehearsal_action,
            "entry_rehearsal_ready": receipt.entry_rehearsal_ready,
            "target_executor": receipt.target_executor,
            "selected_capability_id": receipt.selected_capability_id,
            "selected_capability_executor_id": receipt.selected_capability_executor_id,
            "selected_capability_carrier": None if receipt.selected_capability_carrier is None else receipt.selected_capability_carrier.value,
            "capsule_id": receipt.capsule_id,
            "capsule_type": receipt.capsule_type,
            "capsule_callsign": receipt.capsule_callsign,
            "handoff_capsule_root_relative_path": receipt.handoff_capsule_root_relative_path,
            "handoff_capsule_json_relative_path": receipt.handoff_capsule_json_relative_path,
            "handoff_capsule_markdown_relative_path": receipt.handoff_capsule_markdown_relative_path,
            "handoff_capsule_manifest_relative_path": receipt.handoff_capsule_manifest_relative_path,
            "entry_rehearsal_summary_path": receipt.entry_rehearsal_summary_path,
            "entry_rehearsal_summary_relative_path": receipt.entry_rehearsal_summary_relative_path,
            "entry_rehearsal_manifest_relative_path": receipt.entry_rehearsal_manifest_relative_path,
            "continuation_bundle_root_relative_path": receipt.continuation_bundle_root_relative_path,
            "activation_summary_relative_path": receipt.activation_summary_relative_path,
            "entry_packet_relative_path": receipt.entry_packet_relative_path,
            "required_reads": list(receipt.required_reads),
            "next_action": receipt.next_action,
            "warnings": list(receipt.warnings),
        }


def schedule_handoff_entry_rehearsal_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-handoff-entry-rehearsal-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _resolve_summary_output(workspace: Path, output_path: str | Path | None, capsule_root: Path, scope_type: str, scope_ref: str, created_at: str) -> Path:
    if output_path is not None:
        out = Path(output_path)
        if not out.is_absolute():
            out = workspace / out
        return out.resolve()
    return (capsule_root / '03_executor_entry_rehearsal.md').resolve()


def _resolve_manifest_output(workspace: Path, output_path: str | Path | None, capsule_root: Path, scope_type: str, scope_ref: str, created_at: str) -> Path:
    if output_path is not None:
        out = Path(output_path)
        if not out.is_absolute():
            out = workspace / out
        return out.resolve()
    return (capsule_root / '04_executor_entry_rehearsal_manifest.json').resolve()


def _resolve_required_path(workspace: Path, relative_path: str | None) -> Path | None:
    if not relative_path:
        return None
    candidate = Path(relative_path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (workspace / candidate).resolve()


def _load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(payload, dict):
        raise KernelScheduleHandoffEntryRehearsalError(f"Expected JSON object at {path}")
    return payload


def _render_entry_rehearsal_summary(*, created_at: str, status: str, scope_type: str, scope_ref: str, target_executor: str | None, active_candidate_title: str | None, active_cycle_stage: str, capsule_json_relative_path: str | None, capsule_markdown_relative_path: str | None, capsule_manifest_relative_path: str | None, activation_summary_relative_path: str | None, continuation_bundle_root_relative_path: str | None, entry_packet_relative_path: str | None, required_reads: tuple[str, ...], next_action: str | None) -> str:
    lines = [
        '# Executor-entry rehearsal',
        '',
        f'- created_at: {created_at}',
        f'- status: {status}',
        f'- scope: {scope_type}:{scope_ref}',
        f'- target_executor: {target_executor or "UNKNOWN"}',
        f'- active_cycle_stage: {active_cycle_stage}',
        f'- active_candidate_title: {active_candidate_title or "UNKNOWN"}',
        f'- handoff_capsule_json_relative_path: {capsule_json_relative_path or "UNKNOWN"}',
        f'- handoff_capsule_markdown_relative_path: {capsule_markdown_relative_path or "UNKNOWN"}',
        f'- handoff_capsule_manifest_relative_path: {capsule_manifest_relative_path or "UNKNOWN"}',
        f'- activation_summary_relative_path: {activation_summary_relative_path or "UNKNOWN"}',
        f'- continuation_bundle_root_relative_path: {continuation_bundle_root_relative_path or "UNKNOWN"}',
        f'- entry_packet_relative_path: {entry_packet_relative_path or "UNKNOWN"}',
        '',
        '## Required reads',
    ]
    if required_reads:
        lines.extend(f'- {item}' for item in required_reads)
    else:
        lines.append('- NONE')
    lines.extend(['', '## Next action', next_action or 'NONE'])
    return '\n'.join(lines)



def _relative_to_root(path: Path, workspace_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(workspace_root.resolve()))
    except ValueError:
        return str(path.resolve())


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub('-', value.lower()).strip('-') or 'value'


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec='seconds')
