"""M17 executor-start packet materialization surfaces."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

from .authority_lineage import resolve_explicit_authority_override
from .index import KernelIndex
from .model import ScheduleExecutorStartPacketMaterializationReceipt
from .packet_validation import validate_packet_text
from .schedule_handoff_entry_rehearsal import KernelScheduleHandoffEntryRehearsalManager
from .store import KernelStore

_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class KernelScheduleExecutorStartPacketError(Exception):
    """Raised when M17 executor-start packet materialization cannot complete lawfully."""


class KernelScheduleExecutorStartPacketManager:
    def __init__(self) -> None:
        self._rehearsal_manager = KernelScheduleHandoffEntryRehearsalManager()

    def policy_surface(self) -> dict[str, object]:
        return {
            "policy_id": "M17_EXECUTOR_START_PACKET_V1",
            "notes": (
                "M17 materializes one explicit executor-start packet only from a successful M16 handoff-entry rehearsal.",
                "The packet remains subordinate to the capsule, activation, and continuation witness chain that M16 already proved.",
                "Materialization must not widen into hidden continuation expansion or planner behavior beyond the rehearsed entry path.",
            ),
        }

    def materialize_executor_start_packet(
        self,
        store: KernelStore,
        index: KernelIndex,
        *,
        scope_type: str,
        scope_ref: str,
        workspace_root: str | Path,
        generated_at: str | None = None,
        packet_output_path: str | Path | None = None,
        manifest_output_path: str | Path | None = None,
        status: str = "ACTIVE",
        role: str | None = None,
    ) -> ScheduleExecutorStartPacketMaterializationReceipt:
        timestamp = generated_at or _iso_now()
        workspace = Path(workspace_root).resolve()
        rehearsal = self._rehearsal_manager.latest_receipt(index, scope_type, scope_ref)
        if rehearsal is None:
            raise KernelScheduleExecutorStartPacketError(
                f"No schedule handoff entry rehearsal receipt exists for {scope_type}:{scope_ref}"
            )

        warnings = list(rehearsal.warnings)
        action = "ENTRY_REHEARSAL_NOT_READY"
        ready = False
        packet_path = None
        manifest_path = None
        packet_checksum = None
        packet_type = None
        packet_required_reads = tuple(rehearsal.required_reads)
        next_action = rehearsal.next_action
        target_executor = (role or rehearsal.target_executor or rehearsal.capsule_callsign or "FreshExecutor").strip() or "FreshExecutor"
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

        if rehearsal.entry_rehearsal_ready:
            missing = []
            capsule_root = _resolve_required_path(workspace, rehearsal.handoff_capsule_root_relative_path)
            capsule_json = _resolve_required_path(workspace, rehearsal.handoff_capsule_json_relative_path)
            capsule_markdown = _resolve_required_path(workspace, rehearsal.handoff_capsule_markdown_relative_path)
            capsule_manifest = _resolve_required_path(workspace, rehearsal.handoff_capsule_manifest_relative_path)
            rehearsal_summary = _resolve_required_path(workspace, rehearsal.entry_rehearsal_summary_relative_path)
            rehearsal_manifest = _resolve_required_path(workspace, rehearsal.entry_rehearsal_manifest_relative_path)
            activation_summary = _resolve_required_path(workspace, rehearsal.activation_summary_relative_path)
            entry_packet = _resolve_required_path(workspace, rehearsal.entry_packet_relative_path)
            bundle_root = _resolve_required_path(workspace, rehearsal.continuation_bundle_root_relative_path)
            for name, path in (
                ("handoff_capsule_root", capsule_root),
                ("handoff_capsule_json", capsule_json),
                ("handoff_capsule_markdown", capsule_markdown),
                ("handoff_capsule_manifest", capsule_manifest),
                ("entry_rehearsal_summary", rehearsal_summary),
                ("entry_rehearsal_manifest", rehearsal_manifest),
                ("activation_summary", activation_summary),
                ("entry_packet", entry_packet),
                ("continuation_bundle_root", bundle_root),
            ):
                if path is None or not path.exists():
                    missing.append(name)
            if missing:
                action = "ENTRY_REHEARSAL_MISSING_FILES"
                warnings.append("MISSING_EXECUTOR_START_INPUTS:" + ",".join(missing))
            else:
                capsule_payload = _load_json(capsule_json)
                capsule_manifest_payload = _load_json(capsule_manifest)
                rehearsal_manifest_payload = _load_json(rehearsal_manifest)
                missing_context = []
                for key in (
                    "handoff_capsule_json_relative_path",
                    "handoff_capsule_markdown_relative_path",
                    "activation_summary_relative_path",
                    "continuation_bundle_root_relative_path",
                    "entry_packet_relative_path",
                    "entry_rehearsal_summary_relative_path",
                    "required_reads",
                    "source_schedule_activation_handoff_capsule_receipt_id",
                ):
                    value = rehearsal_manifest_payload.get(key)
                    if value in (None, "", [], ()):
                        missing_context.append(key)
                for key in (
                    "activation_summary_relative_path",
                    "continuation_bundle_root_relative_path",
                    "entry_packet_relative_path",
                    "required_reads",
                    "source_schedule_takeover_entry_activation_receipt_id",
                ):
                    value = capsule_manifest_payload.get(key, (capsule_payload.get("metadata") or {}).get(key))
                    if value in (None, "", [], ()):
                        missing_context.append(key)
                for key in ("handoff", "next_action", "now"):
                    value = str(capsule_payload.get(key) or "").strip()
                    if not value:
                        missing_context.append(key)
                if missing_context:
                    action = "ENTRY_REHEARSAL_INSUFFICIENT_START_CONTEXT"
                    warnings.append("MISSING_EXECUTOR_START_CONTEXT:" + ",".join(dict.fromkeys(missing_context)))
                else:
                    packet_required_reads = _executor_start_required_reads(rehearsal)
                    packet_text = _render_executor_start_packet(
                        created_at=timestamp,
                        status=status,
                        scope_type=scope_type,
                        scope_ref=scope_ref,
                        target_executor=target_executor,
                        active_candidate_title=rehearsal.active_candidate_title,
                        active_cycle_stage=rehearsal.active_cycle_stage,
                        capsule_id=rehearsal.capsule_id,
                        source_schedule_handoff_entry_rehearsal_receipt_id=rehearsal.receipt_id,
                        source_schedule_activation_handoff_capsule_receipt_id=rehearsal.source_schedule_activation_handoff_capsule_receipt_id,
                        source_schedule_takeover_entry_activation_receipt_id=rehearsal.source_schedule_takeover_entry_activation_receipt_id,
                        handoff_capsule_markdown_relative_path=rehearsal.handoff_capsule_markdown_relative_path,
                        handoff_capsule_manifest_relative_path=rehearsal.handoff_capsule_manifest_relative_path,
                        entry_rehearsal_summary_relative_path=rehearsal.entry_rehearsal_summary_relative_path,
                        entry_rehearsal_manifest_relative_path=rehearsal.entry_rehearsal_manifest_relative_path,
                        activation_summary_relative_path=rehearsal.activation_summary_relative_path,
                        continuation_bundle_root_relative_path=rehearsal.continuation_bundle_root_relative_path,
                        entry_packet_relative_path=rehearsal.entry_packet_relative_path,
                        required_reads=packet_required_reads,
                        next_action=next_action,
                    )
                    validation = validate_packet_text(packet_text, expected_type="role_session", allow_legacy=False)
                    if not validation.valid:
                        action = "EXECUTOR_START_PACKET_INVALID"
                        warnings.extend(
                            f"INVALID_EXECUTOR_START_PACKET:{message.code}"
                            for message in validation.errors
                        )
                    else:
                        packet_path = _resolve_packet_output(
                            workspace,
                            packet_output_path,
                            capsule_root,
                            scope_type,
                            scope_ref,
                            timestamp,
                        )
                        packet_path.parent.mkdir(parents=True, exist_ok=True)
                        packet_path.write_text(packet_text, encoding="utf-8")
                        packet_checksum = hashlib.sha256(packet_text.encode("utf-8")).hexdigest()
                        packet_type = "role_session"
                        manifest_path = _resolve_manifest_output(
                            workspace,
                            manifest_output_path,
                            capsule_root,
                            scope_type,
                            scope_ref,
                            timestamp,
                        )
                        manifest_path.parent.mkdir(parents=True, exist_ok=True)
                        manifest_path.write_text(
                            json.dumps(
                                {
                                    "proof_kind": "SCHEDULE_EXECUTOR_START_PACKET",
                                    "created_at": timestamp,
                                    "scope_type": scope_type,
                                    "scope_ref": scope_ref,
                                    "target_executor": target_executor,
                                    "packet_type": packet_type,
                                    "packet_relative_path": _relative_to_root(packet_path, workspace),
                                    "packet_checksum": packet_checksum,
                                    "handoff_capsule_json_relative_path": rehearsal.handoff_capsule_json_relative_path,
                                    "handoff_capsule_markdown_relative_path": rehearsal.handoff_capsule_markdown_relative_path,
                                    "handoff_capsule_manifest_relative_path": rehearsal.handoff_capsule_manifest_relative_path,
                                    "entry_rehearsal_summary_relative_path": rehearsal.entry_rehearsal_summary_relative_path,
                                    "entry_rehearsal_manifest_relative_path": rehearsal.entry_rehearsal_manifest_relative_path,
                                    "activation_summary_relative_path": rehearsal.activation_summary_relative_path,
                                    "continuation_bundle_root_relative_path": rehearsal.continuation_bundle_root_relative_path,
                                    "entry_packet_relative_path": rehearsal.entry_packet_relative_path,
                                    "required_reads": list(packet_required_reads),
                                    "source_schedule_handoff_entry_rehearsal_receipt_id": rehearsal.receipt_id,
                                    "source_schedule_activation_handoff_capsule_receipt_id": rehearsal.source_schedule_activation_handoff_capsule_receipt_id,
                                    "source_schedule_takeover_entry_activation_receipt_id": rehearsal.source_schedule_takeover_entry_activation_receipt_id,
                                    "source_schedule_resume_bundle_materialization_receipt_id": rehearsal.source_schedule_resume_bundle_materialization_receipt_id,
                                },
                                indent=2,
                                sort_keys=True,
                            )
                            + "\n",
                            encoding="utf-8",
                        )
                        action = "MATERIALIZED_EXECUTOR_START_PACKET"
                        ready = True
        else:
            warnings.append("ENTRY_REHEARSAL_NOT_READY")

        receipt = ScheduleExecutorStartPacketMaterializationReceipt(
            receipt_id=schedule_executor_start_packet_materialization_receipt_id(scope_type, scope_ref, timestamp),
            created_at=timestamp,
            policy_id=self.policy_surface()["policy_id"],
            scope_type=scope_type,
            scope_ref=scope_ref,
            source_schedule_handoff_entry_rehearsal_receipt_id=rehearsal.receipt_id,
            source_schedule_activation_handoff_capsule_receipt_id=rehearsal.source_schedule_activation_handoff_capsule_receipt_id,
            source_schedule_takeover_entry_activation_receipt_id=rehearsal.source_schedule_takeover_entry_activation_receipt_id,
            source_schedule_resume_bundle_materialization_receipt_id=rehearsal.source_schedule_resume_bundle_materialization_receipt_id,
            source_schedule_resume_projection_receipt_id=rehearsal.source_schedule_resume_projection_receipt_id,
            source_schedule_lineage_replay_receipt_id=rehearsal.source_schedule_lineage_replay_receipt_id,
            source_schedule_lineage_archive_receipt_id=rehearsal.source_schedule_lineage_archive_receipt_id,
            source_context_perfect_continuation_receipt_id=rehearsal.source_context_perfect_continuation_receipt_id,
            source_takeover_assessment_receipt_id=rehearsal.source_takeover_assessment_receipt_id,
            work_unit_id=rehearsal.work_unit_id,
            active_candidate_id=rehearsal.active_candidate_id,
            active_candidate_title=rehearsal.active_candidate_title,
            active_cycle_stage=rehearsal.active_cycle_stage,
            executor_start_action=action,
            executor_start_ready=ready,
            target_executor=target_executor,
            selected_capability_id=rehearsal.selected_capability_id,
            selected_capability_executor_id=rehearsal.selected_capability_executor_id,
            selected_capability_carrier=rehearsal.selected_capability_carrier,
            capsule_id=rehearsal.capsule_id,
            capsule_type=rehearsal.capsule_type,
            capsule_callsign=rehearsal.capsule_callsign,
            handoff_capsule_root_relative_path=rehearsal.handoff_capsule_root_relative_path,
            handoff_capsule_json_relative_path=rehearsal.handoff_capsule_json_relative_path,
            handoff_capsule_markdown_relative_path=rehearsal.handoff_capsule_markdown_relative_path,
            handoff_capsule_manifest_relative_path=rehearsal.handoff_capsule_manifest_relative_path,
            entry_rehearsal_summary_relative_path=rehearsal.entry_rehearsal_summary_relative_path,
            entry_rehearsal_manifest_relative_path=rehearsal.entry_rehearsal_manifest_relative_path,
            executor_start_packet_type=packet_type,
            executor_start_packet_path=(None if packet_path is None else str(packet_path)),
            executor_start_packet_relative_path=(None if packet_path is None else _relative_to_root(packet_path, workspace)),
            executor_start_packet_checksum=packet_checksum,
            executor_start_manifest_relative_path=(None if manifest_path is None else _relative_to_root(manifest_path, workspace)),
            continuation_bundle_root_relative_path=rehearsal.continuation_bundle_root_relative_path,
            activation_summary_relative_path=rehearsal.activation_summary_relative_path,
            entry_packet_relative_path=rehearsal.entry_packet_relative_path,
            required_reads=packet_required_reads,
            next_action=(next_action if ready else None),
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
    ) -> ScheduleExecutorStartPacketMaterializationReceipt | None:
        if scope_type is None and scope_ref is None:
            receipts = [
                record
                for record in index.records_by_type("schedule_executor_start_packet_materialization_receipt")
                if isinstance(record, ScheduleExecutorStartPacketMaterializationReceipt)
            ]
        elif scope_type is not None and scope_ref is not None:
            receipts = index.schedule_executor_start_packet_materialization_receipts_for_scope(scope_type, scope_ref)
        else:
            raise KernelScheduleExecutorStartPacketError("scope_type and scope_ref must be provided together")
        if not receipts:
            return None
        receipts.sort(key=lambda item: (item.created_at, item.receipt_id))
        return receipts[-1]

    def render_receipt_projection(self, receipt: ScheduleExecutorStartPacketMaterializationReceipt | None) -> dict[str, object] | None:
        if receipt is None:
            return None
        return {
            "receipt_id": receipt.receipt_id,
            "created_at": receipt.created_at,
            "policy_id": receipt.policy_id,
            "scope_type": receipt.scope_type,
            "scope_ref": receipt.scope_ref,
            "source_schedule_handoff_entry_rehearsal_receipt_id": receipt.source_schedule_handoff_entry_rehearsal_receipt_id,
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
            "executor_start_action": receipt.executor_start_action,
            "executor_start_ready": receipt.executor_start_ready,
            "target_executor": receipt.target_executor,
            "selected_capability_id": receipt.selected_capability_id,
            "selected_capability_executor_id": receipt.selected_capability_executor_id,
            "selected_capability_carrier": (None if receipt.selected_capability_carrier is None else receipt.selected_capability_carrier.value),
            "capsule_id": receipt.capsule_id,
            "capsule_type": receipt.capsule_type,
            "capsule_callsign": receipt.capsule_callsign,
            "handoff_capsule_root_relative_path": receipt.handoff_capsule_root_relative_path,
            "handoff_capsule_json_relative_path": receipt.handoff_capsule_json_relative_path,
            "handoff_capsule_markdown_relative_path": receipt.handoff_capsule_markdown_relative_path,
            "handoff_capsule_manifest_relative_path": receipt.handoff_capsule_manifest_relative_path,
            "entry_rehearsal_summary_relative_path": receipt.entry_rehearsal_summary_relative_path,
            "entry_rehearsal_manifest_relative_path": receipt.entry_rehearsal_manifest_relative_path,
            "executor_start_packet_type": receipt.executor_start_packet_type,
            "executor_start_packet_path": receipt.executor_start_packet_path,
            "executor_start_packet_relative_path": receipt.executor_start_packet_relative_path,
            "executor_start_packet_checksum": receipt.executor_start_packet_checksum,
            "executor_start_manifest_relative_path": receipt.executor_start_manifest_relative_path,
            "continuation_bundle_root_relative_path": receipt.continuation_bundle_root_relative_path,
            "activation_summary_relative_path": receipt.activation_summary_relative_path,
            "entry_packet_relative_path": receipt.entry_packet_relative_path,
            "required_reads": list(receipt.required_reads),
            "next_action": receipt.next_action,
            "warnings": list(receipt.warnings),
        }


def schedule_executor_start_packet_materialization_receipt_id(scope_type: str, scope_ref: str, created_at: str) -> str:
    return f"schedule-executor-start-packet-{_slug(scope_type)}-{_slug(scope_ref)}-{_slug(created_at)}"


def _resolve_packet_output(
    workspace: Path,
    output_path: str | Path | None,
    capsule_root: Path | None,
    scope_type: str,
    scope_ref: str,
    created_at: str,
) -> Path:
    if output_path is not None:
        out = Path(output_path)
        if not out.is_absolute():
            out = workspace / out
        return out.resolve()
    if capsule_root is not None:
        return (capsule_root / "05_executor_start_packet.md").resolve()
    return (
        workspace
        / "ION/05_context/history/schedule_executor_start_packets"
        / _slug(scope_type)
        / _slug(scope_ref)
        / _slug(created_at)
        / "01_role_session.md"
    ).resolve()


def _resolve_manifest_output(
    workspace: Path,
    output_path: str | Path | None,
    capsule_root: Path | None,
    scope_type: str,
    scope_ref: str,
    created_at: str,
) -> Path:
    if output_path is not None:
        out = Path(output_path)
        if not out.is_absolute():
            out = workspace / out
        return out.resolve()
    if capsule_root is not None:
        return (capsule_root / "06_executor_start_packet_manifest.json").resolve()
    return (
        workspace
        / "ION/05_context/history/schedule_executor_start_packets"
        / _slug(scope_type)
        / _slug(scope_ref)
        / _slug(created_at)
        / "02_executor_start_packet_manifest.json"
    ).resolve()


def _resolve_required_path(workspace: Path, relative_path: str | None) -> Path | None:
    if not relative_path:
        return None
    candidate = Path(relative_path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (workspace / candidate).resolve()


def _load_json(path: Path | None) -> dict[str, object]:
    if path is None:
        raise KernelScheduleExecutorStartPacketError("Expected JSON path but received None.")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise KernelScheduleExecutorStartPacketError(f"Expected JSON object at {path}")
    return payload


def _executor_start_required_reads(receipt: ScheduleExecutorStartPacketMaterializationReceipt | object) -> tuple[str, ...]:
    reads: list[str] = []
    for item in (
        getattr(receipt, "handoff_capsule_markdown_relative_path", None),
        getattr(receipt, "handoff_capsule_manifest_relative_path", None),
        getattr(receipt, "entry_rehearsal_summary_relative_path", None),
        getattr(receipt, "entry_rehearsal_manifest_relative_path", None),
        getattr(receipt, "activation_summary_relative_path", None),
        getattr(receipt, "entry_packet_relative_path", None),
        getattr(receipt, "continuation_bundle_root_relative_path", None),
        *tuple(getattr(receipt, "required_reads", ()) or ()),
    ):
        value = str(item).strip() if item else ""
        if value and value not in reads:
            reads.append(value)
    return tuple(reads)


def _render_executor_start_packet(
    *,
    created_at: str,
    status: str,
    scope_type: str,
    scope_ref: str,
    target_executor: str,
    active_candidate_title: str | None,
    active_cycle_stage: str,
    capsule_id: str | None,
    source_schedule_handoff_entry_rehearsal_receipt_id: str,
    source_schedule_activation_handoff_capsule_receipt_id: str,
    source_schedule_takeover_entry_activation_receipt_id: str,
    handoff_capsule_markdown_relative_path: str | None,
    handoff_capsule_manifest_relative_path: str | None,
    entry_rehearsal_summary_relative_path: str | None,
    entry_rehearsal_manifest_relative_path: str | None,
    activation_summary_relative_path: str | None,
    continuation_bundle_root_relative_path: str | None,
    entry_packet_relative_path: str | None,
    required_reads: tuple[str, ...],
    next_action: str | None,
) -> str:
    objective = (
        f"Start one bounded executor step from the rehearsed handoff capsule for {scope_type}:{scope_ref}"
    )
    purpose = next_action or objective
    expected_output = (
        f"One bounded continuation artifact or explicit blocker for {scope_type}:{scope_ref} without widening beyond the rehearsed capsule entry path."
    )
    lines = [
        "---",
        "type: role_session",
        "template: ROLE_SESSION",
        f"created: {created_at}",
        f"status: {status}",
        f"role: {target_executor}",
        f"objective: {objective}",
        "---",
        "",
        f"# Role Session: {target_executor}",
        "",
        "## Role",
        "",
        target_executor,
        "",
        "## Purpose",
        "",
        purpose,
        "",
        "## Source Task / Objective",
        "",
        f"- scope: {scope_type}:{scope_ref}",
        f"- source_schedule_handoff_entry_rehearsal_receipt_id: {source_schedule_handoff_entry_rehearsal_receipt_id}",
        f"- source_schedule_activation_handoff_capsule_receipt_id: {source_schedule_activation_handoff_capsule_receipt_id}",
        f"- source_schedule_takeover_entry_activation_receipt_id: {source_schedule_takeover_entry_activation_receipt_id}",
        f"- active_cycle_stage: {active_cycle_stage}",
        f"- active_candidate_title: {active_candidate_title or 'UNKNOWN'}",
        f"- capsule_id: {capsule_id or 'UNKNOWN'}",
        f"- handoff_capsule_markdown_relative_path: {handoff_capsule_markdown_relative_path or 'UNKNOWN'}",
        f"- handoff_capsule_manifest_relative_path: {handoff_capsule_manifest_relative_path or 'UNKNOWN'}",
        f"- entry_rehearsal_summary_relative_path: {entry_rehearsal_summary_relative_path or 'UNKNOWN'}",
        f"- entry_rehearsal_manifest_relative_path: {entry_rehearsal_manifest_relative_path or 'UNKNOWN'}",
        f"- activation_summary_relative_path: {activation_summary_relative_path or 'UNKNOWN'}",
        f"- continuation_bundle_root_relative_path: {continuation_bundle_root_relative_path or 'UNKNOWN'}",
        f"- entry_packet_relative_path: {entry_packet_relative_path or 'UNKNOWN'}",
        "",
        "## Required Reads",
        "",
    ]
    if required_reads:
        lines.extend(f"- {item}" for item in required_reads)
    else:
        lines.append("- NONE")
    lines.extend(
        [
            "",
            "## Expected Output",
            "",
            f"- {expected_output}",
            "",
            "## Next Target",
            "",
            "- next_role: operator or explicit follow-up executor",
            "",
            "## Notes",
            "",
            "- Derived only from a successful M16 executor-entry rehearsal.",
            "- Preserve the capsule, activation, and continuation linkage exactly as written.",
            "- Do not reopen broader context or invent planner behavior outside this packet.",
        ]
    )
    return "\n".join(lines) + "\n"


def _relative_to_root(path: Path, workspace_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(workspace_root.resolve()))
    except ValueError:
        return str(path.resolve())


def _slug(value: str) -> str:
    return _SAFE_ID_RE.sub("-", value.lower()).strip("-") or "value"


def _iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")
