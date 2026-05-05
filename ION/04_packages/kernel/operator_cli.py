"""Operator-facing CLI surface for the active ION kernel.

This module exposes the preferred supervised runtime surfaces through one discoverable
entrypoint. It does not replace the canonical workflow; it gives operators and working
agents a stable way to drive that workflow without importing modules by hand.
"""

from __future__ import annotations

from contextlib import redirect_stdout
from dataclasses import asdict, is_dataclass
import argparse
from io import StringIO
import json
from pathlib import Path
from typing import Any, Sequence

from .automation_policy import (
    AutomationStage,
    CalibrationStatus,
    ContextMode,
    PromotionAction,
    RouteStage,
)
from .allocator import KernelAllocator
from .authority_lineage import KernelAuthorityLineageManager
from .branch_controls import KernelBranchControlManager
from .branch_horizon_sync import KernelBranchHorizonSynchronizer
from .branch_rescheduling import KernelBranchRescheduler
from .settlement import KernelBranchSettlementManager
from .bootstrap_bridge import KernelBootstrapSignalBridge
from .bootstrap_activation import KernelBootstrapActivationManager
from .bootstrap_init import (
    DEFAULT_BOOTSTRAP_COMPLETION_SIGNAL,
    DEFAULT_BOOTSTRAP_CONSTRAINTS,
    DEFAULT_BOOTSTRAP_DELIVERABLES,
    DEFAULT_BOOTSTRAP_GOAL,
    DEFAULT_BOOTSTRAP_REQUIREMENTS,
    DEFAULT_BOOTSTRAP_SOURCE_CONTEXT,
    DEFAULT_BOOTSTRAP_TARGET,
    DEFAULT_BOOTSTRAP_TITLE,
    KernelBootstrapInitWriter,
)
from .child_work_service import (
    ChildAgentBinding,
    ChildWorkSelectionMode,
    ChildWorkServiceRequest,
    KernelChildWorkService,
)
from .continuation import KernelContextPerfectContinuationManager
from .daemon_service import DaemonServiceRequest, KernelDaemonService
from .equivalence import KernelManualAutomationEquivalenceManager
from .execution import ExecutionSubmission
from .external_execution_bridge import (
    ExternalExecutionActionMode,
    ExternalExecutionBridgeRequest,
    KernelExternalExecutionBridge,
)
from .executor_registry import KernelExecutorCapabilityRegistry
from .graph import KernelGraph
from .horizon_state import KernelHorizonStateManager
from .index import KernelIndex
from .model import (
    ArtifactOperation,
    AuthorityClass,
    ExecutorAvailability,
    ExecutorCapability,
    ExecutorTrustClass,
    FallbackSuitability,
    OpenQuestion,
    ProducedArtifact,
    ProposedSignal,
    ScheduleCarrier,
    TierOneDoctrine,
    WorkPriority,
)
from .name_lineage import KernelNameLineageManager, NameIngressSurface
from .operational_hardening import (
    KernelOperationalHardeningManager,
    SupervisedRuntimeShutdownRequest,
    SupervisedRuntimeStartupRequest,
)
from .packet_validation import render_packet_validation, render_takeover_role_session, validate_packet_path, validate_packet_text, workflow_packet_types
from .operator_control import DaemonServiceControlMode, KernelOperatorControlManager
from .question_answers import KernelQuestionAnswerIngestor, KernelQuestionAnswerProjectionBuilder, QuestionAnswerSubmission
from .recovery_replay import (
    KernelRecoveryReplayManager,
    RecoveryReplayRequest,
    RecoveryReplaySelectionMode,
)
from .root_authority_bundle import KernelRootAuthorityBundleError, KernelRootAuthorityBundleManager
from .root_authority_bundle import build_snapshot as build_root_authority_bundle_snapshot
from .root_authority_bundle import render_snapshot as render_root_authority_bundle_snapshot
from .scheduler import KernelScheduler
from .schedule_controls import KernelScheduleControlManager
from .schedule_dispatch_reconciliation import KernelScheduleDispatchReconciliationManager
from .schedule_completion_release import KernelScheduleCompletionReleaseManager
from .schedule_settlement import KernelScheduleSettlementManager
from .schedule_lineage import KernelScheduleLineageArchiveManager
from .schedule_lineage_replay import KernelScheduleLineageReplayManager
from .schedule_resume_projection import KernelScheduleResumeProjectionManager
from .schedule_resume_bundle import KernelScheduleResumeBundleMaterializationManager
from .schedule_takeover_activation import KernelScheduleTakeoverActivationManager
from .schedule_handoff_capsule import KernelScheduleActivationHandoffCapsuleManager
from .schedule_handoff_entry_rehearsal import KernelScheduleHandoffEntryRehearsalManager
from .schedule_executor_start_packet import KernelScheduleExecutorStartPacketManager
from .reviews import REVIEW_DOMAIN
from .sequential_kernel import Workstream, default_repo_root
from .signal_followups import SIGNAL_FOLLOWUP_DOMAIN
from .store import KernelStore
from .takeover import KernelTakeoverManager, render_takeover_assessment


LEGACY_WORKSTREAMS = {workstream.value for workstream in Workstream}
DEFAULT_STORE_RELATIVE_PATH = Path("ION/05_context/history/kernel_store")
DEFAULT_PACKET_OUTPUT_RELATIVE_PATH = Path("ION/05_context/history/dispatch_packets")


class KernelOperatorCliError(Exception):
    """Raised when one operator CLI command cannot be parsed or executed lawfully."""


def main(argv: Sequence[str] | None = None) -> int:
    import sys

    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in LEGACY_WORKSTREAMS:
        from .sequential_kernel import main as sequential_main

        return sequential_main(argv)

    parser = _build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, "command", None):
        parser.print_help()
        return 0

    workspace_root = _resolve_workspace_root(getattr(args, "workspace_root", None))
    output_format = getattr(args, "format", "text")

    if args.command == "status":
        payload = _command_status(workspace_root, getattr(args, "store_root", None))
        return _emit(payload, output_format)

    if args.command == "bundle":
        payload = _command_bundle(args, workspace_root)
        _emit(payload, output_format)
        return 0 if args.bundle_command not in {"validate", "record-exercise", "record-external-return"} or payload.get("valid") else 1

    if args.command == "runtime":
        payload = _command_runtime(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "control":
        payload = _command_control(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "daemon":
        payload = _command_daemon(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "replay":
        payload = _command_replay(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "child":
        payload = _command_child(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "external":
        payload = _command_external(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "packet":
        payload = _command_packet(args, workspace_root)
        _emit(payload, output_format)
        return 0 if payload["valid"] else 1

    if args.command == "bootstrap":
        payload = _command_bootstrap(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "schedule":
        payload = _command_schedule(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "capability":
        payload = _command_capability(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "question":
        payload = _command_question(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "equivalence":
        payload = _command_equivalence(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "continuation":
        payload = _command_continuation(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "lineage":
        payload = _command_lineage(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "authority":
        payload = _command_authority(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "allocator":
        payload = _command_allocator(args, workspace_root)
        return _emit(payload, output_format)

    if args.command == "route":
        from .sequential_kernel import main as sequential_main

        seq_argv = [args.workstream, args.objective]
        if args.repo_root:
            seq_argv.extend(["--repo-root", args.repo_root])
        for directive in args.directive:
            seq_argv.extend(["--directive", directive])
        if args.output:
            seq_argv.extend(["--output", args.output])
        if args.source_task:
            seq_argv.extend(["--source-task", args.source_task])
        if args.execution_root:
            seq_argv.extend(["--execution-root", args.execution_root])
        buffer = StringIO()
        with redirect_stdout(buffer):
            exit_code = sequential_main(seq_argv)
        payload = {
            "command": "route",
            "exit_code": exit_code,
            "trace_text": buffer.getvalue(),
        }
        return _emit(payload, output_format)

    raise KernelOperatorCliError(f"Unhandled command: {args.command}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Operate the active ION workflow carriers through one CLI surface.")
    subparsers = parser.add_subparsers(dest="command")

    status = subparsers.add_parser("status", help="Render supervised-runtime and kernel-state status.")
    _add_workspace_args(status)
    status.add_argument("--store-root", help="Optional explicit kernel store root.")
    status.add_argument("--format", choices=("text", "json"), default="text")

    bundle = subparsers.add_parser("bundle", help="Inspect or validate the root-authority startup bundle.")
    _add_workspace_args(bundle)
    bundle.add_argument("--format", choices=("text", "json"), default="text")
    bundle_sub = bundle.add_subparsers(dest="bundle_command", required=True)

    bundle_sub.add_parser("snapshot", help="Render the current root-authority bundle snapshot.")
    bundle_sub.add_parser("validate", help="Validate the current root-authority bundle anchors and manifest posture.")
    bundle_record = bundle_sub.add_parser("record-exercise", help="Persist one durable current-carrier exercise receipt for the root-authority bundle.")
    bundle_record.add_argument("--store-root", help="Optional explicit kernel store root.")
    bundle_record.add_argument("--carrier-key", choices=("cursor_codex", "browser_chatgpt", "claude_code"), default="cursor_codex")
    bundle_record.add_argument("--execution-mode", default="BRANCH_LOCAL_EDITABLE_INSTALL")
    bundle_record.add_argument("--executor", default="STEWARD")
    bundle_record.add_argument("--created-at")
    bundle_external = bundle_sub.add_parser("materialize-external-exercise-brief", help="Materialize one external-carrier exercise brief for the root-authority bundle.")
    bundle_external.add_argument("--carrier-key", choices=("browser_chatgpt", "claude_code"), required=True)
    bundle_external.add_argument("--output", help="Optional explicit output path.")
    bundle_external.add_argument("--created-at")
    bundle_return = bundle_sub.add_parser("materialize-external-return-stub", help="Materialize one fillable external return stub for a browser or Claude bundle exercise.")
    bundle_return.add_argument("--carrier-key", choices=("browser_chatgpt", "claude_code"), required=True)
    bundle_return.add_argument("--output", help="Optional explicit output path.")
    bundle_return.add_argument("--created-at")
    bundle_record_external = bundle_sub.add_parser("record-external-return", help="Persist one completed external return packet as q004 carrier evidence.")
    bundle_record_external.add_argument("--store-root", help="Optional explicit kernel store root.")
    bundle_record_external.add_argument("--carrier-key", choices=("browser_chatgpt", "claude_code"), required=True)
    bundle_record_external.add_argument("--input", required=True, help="Path to the completed EXTERNAL_RETURN packet.")
    bundle_record_external.add_argument("--created-at")

    runtime = subparsers.add_parser("runtime", help="Start or stop the supervised runtime mode.")
    _add_workspace_args(runtime)
    runtime.add_argument("--format", choices=("text", "json"), default="text")
    runtime_sub = runtime.add_subparsers(dest="runtime_command", required=True)

    start = runtime_sub.add_parser("start", help="Enable the preferred supervised runtime mode.")
    _add_runtime_policy_args(start)
    start.add_argument("--reason", default="Enable supervised runtime")
    start.add_argument("--actor", default="OPERATOR")
    start.add_argument("--approval", action="store_true", help="Provide explicit approval when required.")
    start.add_argument("--timestamp")

    drain = runtime_sub.add_parser("drain", help="Drain the supervised runtime mode.")
    drain.add_argument("--reason", default="Drain supervised runtime")
    drain.add_argument("--actor", default="OPERATOR")
    drain.add_argument("--timestamp")

    stop = runtime_sub.add_parser("stop", help="Stop the supervised runtime mode.")
    stop.add_argument("--reason", default="Stop supervised runtime")
    stop.add_argument("--actor", default="OPERATOR")
    stop.add_argument("--timestamp")

    control = subparsers.add_parser("control", help="Mutate explicit operator-control state.")
    _add_workspace_args(control)
    control.add_argument("--format", choices=("text", "json"), default="text")
    control_sub = control.add_subparsers(dest="control_command", required=True)

    mode = control_sub.add_parser("service-mode", help="Set the daemon service control mode directly.")
    mode.add_argument("mode", choices=[mode.value for mode in DaemonServiceControlMode])
    mode.add_argument("--reason", required=True)
    mode.add_argument("--actor", default="OPERATOR")
    mode.add_argument("--timestamp")

    hold = control_sub.add_parser("hold-scope", help="Hold one scope explicitly.")
    hold.add_argument("scope_type")
    hold.add_argument("scope_ref")
    hold.add_argument("--reason", required=True)
    hold.add_argument("--actor", default="OPERATOR")
    hold.add_argument("--timestamp")

    resume = control_sub.add_parser("resume-scope", help="Resume one held scope explicitly.")
    resume.add_argument("scope_type")
    resume.add_argument("scope_ref")
    resume.add_argument("--actor", default="OPERATOR")
    resume.add_argument("--timestamp")

    daemon = subparsers.add_parser("daemon", help="Invoke the supervised daemon-service carrier.")
    _add_workspace_args(daemon)
    daemon.add_argument("--store-root", help="Optional explicit kernel store root.")
    daemon.add_argument("--format", choices=("text", "json"), default="text")
    daemon_sub = daemon.add_subparsers(dest="daemon_command", required=True)

    run = daemon_sub.add_parser("run", help="Run the bounded daemon-service carrier.")
    _add_runtime_policy_args(run)
    run.add_argument("--max-steps", type=int, default=25)
    run.add_argument("--scope-type")
    run.add_argument("--scope-ref")
    run.add_argument("--approval", action="store_true")
    run.add_argument("--dry-run", action="store_true")
    run.add_argument("--packet-output-root")
    run.add_argument("--repo-root")
    run.add_argument("--actor", default="OPERATOR")
    run.add_argument("--timestamp")

    replay = subparsers.add_parser("replay", help="Replay lawful interrupted daemon-service runs.")
    _add_workspace_args(replay)
    replay.add_argument("--store-root", help="Optional explicit kernel store root.")
    replay.add_argument("--format", choices=("text", "json"), default="text")
    replay_sub = replay.add_subparsers(dest="replay_command", required=True)

    replay_latest = replay_sub.add_parser("latest", help="Replay the latest resumable daemon-service run.")
    replay_latest.add_argument("--approval", action="store_true")
    replay_latest.add_argument("--allow-stale", action="store_true")
    replay_latest.add_argument("--dry-run", action="store_true")
    replay_latest.add_argument("--max-steps", type=int)
    replay_latest.add_argument("--packet-output-root")
    replay_latest.add_argument("--repo-root")
    replay_latest.add_argument("--stale-after-seconds", type=int, default=4 * 60 * 60)
    replay_latest.add_argument("--actor", default="OPERATOR")
    replay_latest.add_argument("--notes")
    replay_latest.add_argument("--timestamp")

    replay_receipt = replay_sub.add_parser("receipt", help="Replay from one explicit daemon-service receipt.")
    replay_receipt.add_argument("service_receipt_path")
    replay_receipt.add_argument("--approval", action="store_true")
    replay_receipt.add_argument("--allow-stale", action="store_true")
    replay_receipt.add_argument("--dry-run", action="store_true")
    replay_receipt.add_argument("--max-steps", type=int)
    replay_receipt.add_argument("--packet-output-root")
    replay_receipt.add_argument("--repo-root")
    replay_receipt.add_argument("--stale-after-seconds", type=int, default=4 * 60 * 60)
    replay_receipt.add_argument("--actor", default="OPERATOR")
    replay_receipt.add_argument("--notes")
    replay_receipt.add_argument("--timestamp")

    child = subparsers.add_parser("child", help="Issue supervised child work.")
    _add_workspace_args(child)
    child.add_argument("--store-root", help="Optional explicit kernel store root.")
    child.add_argument("--format", choices=("text", "json"), default="text")
    child_sub = child.add_subparsers(dest="child_command", required=True)

    issue_manifest = child_sub.add_parser("issue-manifest", help="Issue child work from a planner manifest.")
    _add_child_args(issue_manifest)
    issue_manifest.add_argument("manifest_id")

    issue_delta = child_sub.add_parser("issue-delta", help="Issue child work from a resolved question/delta pair.")
    _add_child_args(issue_delta)
    issue_delta.add_argument("question_id")
    issue_delta.add_argument("work_unit_id")
    issue_delta.add_argument("delta_id")

    external = subparsers.add_parser("external", help="Bridge one bounded external execution step.")
    _add_workspace_args(external)

    packet = subparsers.add_parser("packet", help="Validate canonical markdown workflow packets.")
    _add_workspace_args(packet)
    packet.add_argument("--format", choices=("text", "json"), default="text")
    packet_sub = packet.add_subparsers(dest="packet_command", required=True)

    validate = packet_sub.add_parser("validate", help="Validate one canonical markdown packet.")
    validate.add_argument("path", help="Packet path, relative to the workspace root unless absolute.")
    validate.add_argument("--expected-type", choices=workflow_packet_types())
    validate.add_argument("--legacy", action="store_true", help="Downgrade missing normalized structure to warnings where possible.")

    takeover_assess = packet_sub.add_parser("assess-takeover", help="Assess whether one canonical packet is sufficient for bounded takeover.")
    takeover_assess.add_argument("path", help="Packet path, relative to the workspace root unless absolute.")
    takeover_assess.add_argument("--expected-type", choices=workflow_packet_types())
    takeover_assess.add_argument("--legacy", action="store_true", help="Downgrade missing normalized structure to warnings where possible.")

    takeover_render = packet_sub.add_parser("render-takeover-role-session", help="Render one derived role-session packet from bounded takeover context.")
    takeover_render.add_argument("path", help="Packet path, relative to the workspace root unless absolute.")
    takeover_render.add_argument("--role", required=True)
    takeover_render.add_argument("--expected-type", choices=workflow_packet_types())
    takeover_render.add_argument("--legacy", action="store_true", help="Downgrade missing normalized structure to warnings where possible.")
    takeover_render.add_argument("--created-at")
    takeover_render.add_argument("--status", default="ACTIVE")
    takeover_render.add_argument("--output", help="Optional output packet path, relative to the workspace root unless absolute.")

    takeover_record = packet_sub.add_parser("record-takeover", help="Persist one durable takeover-assessment receipt for a canonical packet.")
    takeover_record.add_argument("path", help="Packet path, relative to the workspace root unless absolute.")
    takeover_record.add_argument("--store-root", help="Optional explicit kernel store root.")
    takeover_record.add_argument("--expected-type", choices=workflow_packet_types())
    takeover_record.add_argument("--legacy", action="store_true", help="Downgrade missing normalized structure to warnings where possible.")
    takeover_record.add_argument("--created-at")

    enact = packet_sub.add_parser("enact-horizon", help="Render or write one canonical packet from a packet-ready horizon candidate.")
    enact.add_argument("scope_type")
    enact.add_argument("scope_ref")
    enact.add_argument("--store-root", help="Optional explicit kernel store root.")
    enact.add_argument("--packet-type", choices=[item for item in workflow_packet_types() if item != "task"])
    enact.add_argument("--output", help="Optional output packet path, relative to the workspace root unless absolute.")
    enact.add_argument("--created-at")
    enact.add_argument("--status", default="ACTIVE")
    enact.add_argument("--sender", default="HORIZON")
    enact.add_argument("--receiver")
    enact.add_argument("--target-surface")
    enact.add_argument("--automation-surface")
    enact.add_argument("--reason")

    external.add_argument("--store-root", help="Optional explicit kernel store root.")
    external.add_argument("--format", choices=("text", "json"), default="text")
    external_sub = external.add_subparsers(dest="external_command", required=True)

    export = external_sub.add_parser("export", help="Export one lawful external execution packet.")
    _add_runtime_policy_args(export)
    export.add_argument("work_unit_id")
    export.add_argument("--approval", action="store_true")
    export.add_argument("--dry-run", action="store_true")
    export.add_argument("--actor", default="OPERATOR")
    export.add_argument("--timestamp")

    accept = external_sub.add_parser("accept-return", help="Accept one bounded external execution return.")
    _add_runtime_policy_args(accept)
    accept.add_argument("work_unit_id")
    accept.add_argument("submission_json")
    accept.add_argument("--approval", action="store_true")
    accept.add_argument("--dry-run", action="store_true")
    accept.add_argument("--actor", default="OPERATOR")
    accept.add_argument("--timestamp")

    bootstrap = subparsers.add_parser("bootstrap", help="Initialize or bridge bootstrap task packets into canonical daemon pressure.")
    _add_workspace_args(bootstrap)
    bootstrap.add_argument("--format", choices=("text", "json"), default="text")
    bootstrap_sub = bootstrap.add_subparsers(dest="bootstrap_command", required=True)

    bootstrap_init = bootstrap_sub.add_parser("init", help="Write one canonical bootstrap task packet into the visible inbox lane.")
    bootstrap_init.add_argument("--title", default=DEFAULT_BOOTSTRAP_TITLE)
    bootstrap_init.add_argument("--goal", default=DEFAULT_BOOTSTRAP_GOAL)
    bootstrap_init.add_argument("--target", default=DEFAULT_BOOTSTRAP_TARGET)
    bootstrap_init.add_argument("--agent", default="Steward")
    bootstrap_init.add_argument("--template", default="RESEARCH")
    bootstrap_init.add_argument("--priority", default=WorkPriority.P1_HIGH.value, choices=[item.value for item in WorkPriority])
    bootstrap_init.add_argument("--from-actor", default="Operator")
    bootstrap_init.add_argument("--bootstrap-signal-type", default="BLOCKED", choices=("BLOCKED", "TASK_FAILED", "TASK_COMPLETE"))
    bootstrap_init.add_argument("--bootstrap-needed-from", default="Steward")
    bootstrap_init.add_argument("--bootstrap-blocker")
    bootstrap_init.add_argument("--bootstrap-error")
    bootstrap_init.add_argument("--bootstrap-recoverable", action="store_true")
    bootstrap_init.add_argument("--source-context", action="append", default=[])
    bootstrap_init.add_argument("--requirement", action="append", default=[])
    bootstrap_init.add_argument("--deliverable", action="append", default=[])
    bootstrap_init.add_argument("--constraint", action="append", default=[])
    bootstrap_init.add_argument("--completion-signal")
    bootstrap_init.add_argument("--packet-path", help="Optional output bootstrap task path relative to the workspace root unless absolute.")
    bootstrap_init.add_argument("--bootstrap-dir", default="ION/05_context/inbox/bootstrap")
    bootstrap_init.add_argument("--receipts-dir", default="ION/05_context/history/bootstrap_init_receipts")
    bootstrap_init.add_argument("--timestamp")

    bootstrap_emit = bootstrap_sub.add_parser("emit", help="Emit one canonical daemon signal from one bootstrap task packet.")
    bootstrap_emit.add_argument("path", nargs="?", help="Optional bootstrap task path relative to the workspace root unless absolute.")
    bootstrap_emit.add_argument("--bootstrap-dir", default="ION/05_context/inbox/bootstrap")
    bootstrap_emit.add_argument("--archive-dir", default="ION/05_context/inbox/bootstrap/archive")
    bootstrap_emit.add_argument("--signals-dir", default="ION/05_context/signals")
    bootstrap_emit.add_argument("--receipts-dir", default="ION/05_context/history/bootstrap_bridge_receipts")
    bootstrap_emit.add_argument("--timestamp")

    bootstrap_activate = bootstrap_sub.add_parser("activate", help="Run the explicit bootstrap activation ceremony over init, emit, and daemon surfaces.")
    bootstrap_activate.add_argument("--title", default=DEFAULT_BOOTSTRAP_TITLE)
    bootstrap_activate.add_argument("--goal", default=DEFAULT_BOOTSTRAP_GOAL)
    bootstrap_activate.add_argument("--target", default=DEFAULT_BOOTSTRAP_TARGET)
    bootstrap_activate.add_argument("--agent", default="Steward")
    bootstrap_activate.add_argument("--template", default="RESEARCH")
    bootstrap_activate.add_argument("--priority", default=WorkPriority.P1_HIGH.value, choices=[item.value for item in WorkPriority])
    bootstrap_activate.add_argument("--from-actor", default="Operator")
    bootstrap_activate.add_argument("--bootstrap-signal-type", default="BLOCKED", choices=("BLOCKED", "TASK_FAILED", "TASK_COMPLETE"))
    bootstrap_activate.add_argument("--bootstrap-needed-from", default="Steward")
    bootstrap_activate.add_argument("--bootstrap-blocker")
    bootstrap_activate.add_argument("--bootstrap-error")
    bootstrap_activate.add_argument("--bootstrap-recoverable", action="store_true")
    bootstrap_activate.add_argument("--source-context", action="append", default=[])
    bootstrap_activate.add_argument("--requirement", action="append", default=[])
    bootstrap_activate.add_argument("--deliverable", action="append", default=[])
    bootstrap_activate.add_argument("--constraint", action="append", default=[])
    bootstrap_activate.add_argument("--completion-signal")
    bootstrap_activate.add_argument("--packet-path")
    bootstrap_activate.add_argument("--bootstrap-dir", default="ION/05_context/inbox/bootstrap")
    bootstrap_activate.add_argument("--init-receipts-dir", default="ION/05_context/history/bootstrap_init_receipts")
    bootstrap_activate.add_argument("--archive-dir", default="ION/05_context/inbox/bootstrap/archive")
    bootstrap_activate.add_argument("--signals-dir", default="ION/05_context/signals")
    bootstrap_activate.add_argument("--bridge-receipts-dir", default="ION/05_context/history/bootstrap_bridge_receipts")
    bootstrap_activate.add_argument("--activation-receipts-dir", default="ION/05_context/history/bootstrap_activation_receipts")
    bootstrap_activate.add_argument("--approval", action="store_true")
    bootstrap_activate.add_argument("--max-steps", type=int, default=1)
    bootstrap_activate.add_argument("--actor", default="OPERATOR")
    bootstrap_activate.add_argument("--timestamp")

    route = subparsers.add_parser("route", help="Render the sequential/manual carrier route scaffold.")
    route.add_argument("workstream", choices=[workstream.value for workstream in Workstream])
    route.add_argument("objective")
    route.add_argument("--repo-root")
    route.add_argument("--directive", action="append", default=[])
    route.add_argument("--output")
    route.add_argument("--source-task")
    route.add_argument("--execution-root")
    route.add_argument("--format", choices=("text", "json"), default="text")

    schedule = subparsers.add_parser("schedule", help="Inspect or record scheduler projections through the current L1 carrier-binding law.")
    _add_workspace_args(schedule)
    schedule.add_argument("--store-root", help="Optional explicit kernel store root.")
    schedule.add_argument("--format", choices=("text", "json"), default="text")
    schedule_sub = schedule.add_subparsers(dest="schedule_command", required=True)

    snapshot = schedule_sub.add_parser("snapshot", help="Render the current schedule projection.")
    snapshot.add_argument("--scope-type")
    snapshot.add_argument("--scope-ref")

    record = schedule_sub.add_parser("record", help="Persist one scheduling receipt for the selected candidate.")
    record.add_argument("--scope-type")
    record.add_argument("--scope-ref")
    record.add_argument("--created-at")

    maintain = schedule_sub.add_parser("maintain", help="Evaluate stale / retry / reassignment posture for one scope.")
    maintain.add_argument("--scope-type", required=True)
    maintain.add_argument("--scope-ref", required=True)
    maintain.add_argument("--stale-after-seconds", type=int, default=1800)
    maintain.add_argument("--created-at")

    reconcile = schedule_sub.add_parser("reconcile", help="Reconcile schedule witness with active assignment / dispatch reality for one scope.")
    reconcile.add_argument("--scope-type", required=True)
    reconcile.add_argument("--scope-ref", required=True)
    reconcile.add_argument("--created-at")
    reconcile.add_argument("--packet-output-root")

    release_completion = schedule_sub.add_parser("release-completion", help="Reconcile terminal completion / assignment release for one scope.")
    release_completion.add_argument("--scope-type", required=True)
    release_completion.add_argument("--scope-ref", required=True)
    release_completion.add_argument("--created-at")

    settle = schedule_sub.add_parser("settle", help="Settle a completed schedule line and reopen future posture when warranted.")
    settle.add_argument("--scope-type", required=True)
    settle.add_argument("--scope-ref", required=True)
    settle.add_argument("--created-at")

    archive_lineage = schedule_sub.add_parser("archive-lineage", help="Compact settled schedule lineage into one explicit archival witness.")
    archive_lineage.add_argument("--scope-type", required=True)
    archive_lineage.add_argument("--scope-ref", required=True)
    archive_lineage.add_argument("--created-at")

    replay_lineage = schedule_sub.add_parser("replay-lineage", help="Replay archived schedule lineage and reconstruct the active cycle.")
    replay_lineage.add_argument("--scope-type", required=True)
    replay_lineage.add_argument("--scope-ref", required=True)
    replay_lineage.add_argument("--created-at")

    project_resume = schedule_sub.add_parser("project-resume", help="Project replayed active-cycle state into a bounded handoff / resume packet.")
    project_resume.add_argument("--scope-type", required=True)
    project_resume.add_argument("--scope-ref", required=True)
    project_resume.add_argument("--created-at")
    project_resume.add_argument("--output")
    project_resume.add_argument("--status", default="ACTIVE")
    project_resume.add_argument("--role")

    materialize_resume_bundle = schedule_sub.add_parser("materialize-resume-bundle", help="Materialize the latest resume projection into a context-perfect continuation bundle.")
    materialize_resume_bundle.add_argument("--scope-type", required=True)
    materialize_resume_bundle.add_argument("--scope-ref", required=True)
    materialize_resume_bundle.add_argument("--created-at")
    materialize_resume_bundle.add_argument("--packet-output")
    materialize_resume_bundle.add_argument("--bundle-output-root")
    materialize_resume_bundle.add_argument("--status", default="ACTIVE")
    materialize_resume_bundle.add_argument("--role")

    validate_activation = schedule_sub.add_parser("validate-activation", help="Validate the latest continuation bundle as a takeover-entry activation artifact.")
    validate_activation.add_argument("--scope-type", required=True)
    validate_activation.add_argument("--scope-ref", required=True)
    validate_activation.add_argument("--created-at")
    validate_activation.add_argument("--summary-output")
    validate_activation.add_argument("--status", default="ACTIVE")
    validate_activation.add_argument("--role")

    materialize_handoff_capsule = schedule_sub.add_parser("materialize-handoff-capsule", help="Materialize the validated activation summary into one compact handoff capsule.")
    materialize_handoff_capsule.add_argument("--scope-type", required=True)
    materialize_handoff_capsule.add_argument("--scope-ref", required=True)
    materialize_handoff_capsule.add_argument("--created-at")
    materialize_handoff_capsule.add_argument("--output-root")
    materialize_handoff_capsule.add_argument("--status", default="ACTIVE")
    materialize_handoff_capsule.add_argument("--role")

    rehearse_handoff_entry = schedule_sub.add_parser("rehearse-handoff-entry", help="Rehearse direct executor entry from the compact handoff capsule.")
    rehearse_handoff_entry.add_argument("--scope-type", required=True)
    rehearse_handoff_entry.add_argument("--scope-ref", required=True)
    rehearse_handoff_entry.add_argument("--created-at")
    rehearse_handoff_entry.add_argument("--summary-output")
    rehearse_handoff_entry.add_argument("--manifest-output")
    rehearse_handoff_entry.add_argument("--status", default="ACTIVE")

    materialize_executor_start_packet = schedule_sub.add_parser("materialize-executor-start-packet", help="Materialize one explicit executor-start packet from a successful handoff-entry rehearsal.")
    materialize_executor_start_packet.add_argument("--scope-type", required=True)
    materialize_executor_start_packet.add_argument("--scope-ref", required=True)
    materialize_executor_start_packet.add_argument("--created-at")
    materialize_executor_start_packet.add_argument("--packet-output")
    materialize_executor_start_packet.add_argument("--manifest-output")
    materialize_executor_start_packet.add_argument("--status", default="ACTIVE")
    materialize_executor_start_packet.add_argument("--role")

    capability = subparsers.add_parser("capability", help="Inspect or register executor capability records.")
    _add_workspace_args(capability)
    capability.add_argument("--store-root", help="Optional explicit kernel store root.")
    capability.add_argument("--format", choices=("text", "json"), default="text")
    capability_sub = capability.add_subparsers(dest="capability_command", required=True)

    capability_snapshot = capability_sub.add_parser("snapshot", help="Render the current executor capability registry snapshot.")
    capability_snapshot.add_argument("--include-inactive", action="store_true")

    capability_register = capability_sub.add_parser("register", help="Register or replace one executor capability record.")
    capability_register.add_argument("capability_id")
    capability_register.add_argument("executor_id")
    capability_register.add_argument("--personal-name", required=True)
    capability_register.add_argument("--role", required=True)
    capability_register.add_argument("--structural-identity", required=True)
    capability_register.add_argument("--carrier", required=True, choices=[item.value for item in ScheduleCarrier])
    capability_register.add_argument("--trust-class", required=True, choices=[item.value for item in ExecutorTrustClass])
    capability_register.add_argument("--availability", default=ExecutorAvailability.AVAILABLE.value, choices=[item.value for item in ExecutorAvailability])
    capability_register.add_argument("--max-concurrency", type=int, default=1)
    capability_register.add_argument("--active-assignments", type=int, default=0)
    capability_register.add_argument("--scope-type", action="append", default=[])
    capability_register.add_argument("--domain", action="append", default=[])
    capability_register.add_argument("--packet-family", action="append", default=[])
    capability_register.add_argument("--alias", action="append", default=[])
    capability_register.add_argument("--side-effect-constraint", action="append", default=[])
    capability_register.add_argument("--fallback-suitability", default=FallbackSuitability.PRIMARY.value, choices=[item.value for item in FallbackSuitability])
    capability_register.add_argument("--notes")
    capability_register.add_argument("--created-at")

    question = subparsers.add_parser("question", help="Inspect or resolve reviewer and signal follow-up questions.")
    _add_workspace_args(question)
    question.add_argument("--store-root", help="Optional explicit kernel store root.")
    question.add_argument("--format", choices=("text", "json"), default="text")
    question_sub = question.add_subparsers(dest="question_command", required=True)

    question_queue = question_sub.add_parser("queue", help="Render one reviewer/follow-up queue view.")
    question_queue.add_argument("--reviewer")
    question_queue.add_argument("--domain", action="append", choices=(REVIEW_DOMAIN, SIGNAL_FOLLOWUP_DOMAIN), default=[])
    question_queue.add_argument("--pending-limit", type=int)
    question_queue.add_argument("--answer-limit", type=int)
    question_queue.add_argument("--record", action="store_true")
    question_queue.add_argument("--generated-at")

    question_answer = question_sub.add_parser("answer", help="Persist one explicit answer for a review or follow-up question.")
    question_answer.add_argument("question_id")
    question_answer.add_argument("--answered-by")
    question_answer.add_argument("--resolution", required=True)
    question_answer.add_argument("--evidence", action="append", default=[])
    question_answer.add_argument("--notes")
    question_answer.add_argument("--answered-at")

    equivalence = subparsers.add_parser("equivalence", help="Rehearse or inspect manual/automation equivalence proof.")
    _add_workspace_args(equivalence)
    equivalence.add_argument("--store-root", help="Optional explicit kernel store root.")
    equivalence.add_argument("--format", choices=("text", "json"), default="text")
    equivalence_sub = equivalence.add_subparsers(dest="equivalence_command", required=True)

    equivalence_snapshot = equivalence_sub.add_parser("snapshot", help="Render the latest manual/automation equivalence receipt.")
    equivalence_snapshot.add_argument("--scope-type")
    equivalence_snapshot.add_argument("--scope-ref")

    equivalence_rehearse = equivalence_sub.add_parser(
        "rehearse-horizon",
        help="Enact automation and manual packets from one packet-ready horizon candidate and persist one equivalence receipt.",
    )
    equivalence_rehearse.add_argument("scope_type")
    equivalence_rehearse.add_argument("scope_ref")
    equivalence_rehearse.add_argument("--automation-packet-type", default="cursor_handoff", choices=("handoff", "cursor_handoff"))
    equivalence_rehearse.add_argument("--automation-output")
    equivalence_rehearse.add_argument("--manual-output")
    equivalence_rehearse.add_argument("--created-at")
    equivalence_rehearse.add_argument("--automation-sender", default="HORIZON")
    equivalence_rehearse.add_argument("--automation-receiver", default="Automation carrier")
    equivalence_rehearse.add_argument("--automation-target-surface", default="Supervised runtime / automation carrier")
    equivalence_rehearse.add_argument("--manual-operator", default="OPERATOR")
    equivalence_rehearse.add_argument("--manual-automation-surface", default="supervised runtime")
    equivalence_rehearse.add_argument("--manual-reason", default="manual/automation equivalence rehearsal")

    continuation = subparsers.add_parser(
        "continuation",
        help="Prove or inspect context-perfect continuation bundles.",
    )
    _add_workspace_args(continuation)
    continuation.add_argument("--store-root", help="Optional explicit kernel store root.")
    continuation.add_argument("--format", choices=("text", "json"), default="text")
    continuation_sub = continuation.add_subparsers(dest="continuation_command", required=True)

    continuation_snapshot = continuation_sub.add_parser(
        "snapshot",
        help="Render the latest context-perfect continuation receipt.",
    )
    continuation_snapshot.add_argument("--scope-type")
    continuation_snapshot.add_argument("--scope-ref")

    continuation_prove = continuation_sub.add_parser(
        "prove-packet",
        help="Materialize one takeover-sufficient packet into a context-perfect continuation bundle.",
    )
    continuation_prove.add_argument("path", help="Packet path, relative to the workspace root unless absolute.")
    continuation_prove.add_argument("--expected-type", choices=workflow_packet_types())
    continuation_prove.add_argument("--legacy", action="store_true", help="Downgrade missing normalized structure to warnings where possible.")
    continuation_prove.add_argument("--repo-root", help="Optional root used to resolve packet required reads.")
    continuation_prove.add_argument("--role", default="FreshExecutor")
    continuation_prove.add_argument("--output-root", help="Optional bundle root path, relative to the workspace root unless absolute.")
    continuation_prove.add_argument("--created-at")
    continuation_prove.add_argument("--status", default="ACTIVE")

    lineage = subparsers.add_parser(
        "lineage",
        help="Resolve governed names or audit stale-name drift in active surfaces.",
    )
    _add_workspace_args(lineage)
    lineage.add_argument("--format", choices=("text", "json"), default="text")
    lineage_sub = lineage.add_subparsers(dest="lineage_command", required=True)

    lineage_resolve = lineage_sub.add_parser(
        "resolve",
        help="Resolve one raw incoming name through the current-phase lineage registry.",
    )
    lineage_resolve.add_argument("name")
    lineage_resolve.add_argument(
        "--surface",
        default=NameIngressSurface.OPERATOR_INPUT.value,
        choices=[item.value for item in NameIngressSurface],
    )
    lineage_resolve.add_argument("--strict", action="store_true")
    lineage_resolve.add_argument("--record", action="store_true")
    lineage_resolve.add_argument("--created-at")

    lineage_audit = lineage_sub.add_parser(
        "audit-active-surfaces",
        help="Scan active surfaces for stale governed names.",
    )
    lineage_audit.add_argument("path", nargs="*")
    lineage_audit.add_argument("--include-historical", action="store_true")

    authority = subparsers.add_parser("authority", help="Resolve or audit stale authority names against current-phase lineage truth.")
    _add_workspace_args(authority)
    authority.add_argument("--format", choices=("text", "json"), default="text")
    authority_sub = authority.add_subparsers(dest="authority_command", required=True)

    authority_resolve = authority_sub.add_parser("resolve", help="Resolve one authority name for one bounded surface.")
    authority_resolve.add_argument("surface", help="Bounded authority surface to resolve against the lineage registry.")
    authority_resolve.add_argument("name", nargs="?", help="Optional explicit name to resolve; omit to see the current default authority.")

    authority_surface = authority_sub.add_parser("show-surface", help="Render one surface record from the authority lineage registry.")
    authority_surface.add_argument("surface", help="Bounded authority surface to inspect.")

    authority_name = authority_sub.add_parser("show-name", help="Render one authority-name record from the lineage registry.")
    authority_name.add_argument("name", help="Authority name to inspect.")

    authority_audit = authority_sub.add_parser("audit-active-surfaces", help="Scan the active control surfaces for stale aliases that should no longer steer fresh runtime defaults.")
    authority_alignment = authority_sub.add_parser("audit-registry-alignment", help="Check the surface-specific authority registry against the richer name-lineage registry so the two cannot silently drift after consolidation.")

    allocator = subparsers.add_parser(
        "allocator",
        help="Inspect or persist bounded child-branch allocation under one committed parent.",
    )
    _add_workspace_args(allocator)
    allocator.add_argument("--store-root", help="Optional explicit kernel store root.")
    allocator.add_argument("--format", choices=("text", "json"), default="text")
    allocator_sub = allocator.add_subparsers(dest="allocator_command", required=True)

    allocator_snapshot = allocator_sub.add_parser(
        "snapshot-children",
        help="Render the bounded child-branch allocation projection for one committed parent work unit.",
    )
    allocator_snapshot.add_argument("parent_work_unit_id")
    allocator_snapshot.add_argument("--max-branches", type=int)

    allocator_claim = allocator_sub.add_parser(
        "claim-children",
        help="Persist explicit branch-claim receipts for selected child branches under one committed parent work unit.",
    )
    allocator_claim.add_argument("parent_work_unit_id")
    allocator_claim.add_argument("--max-branches", type=int)
    allocator_claim.add_argument("--created-at")

    allocator_posture = allocator_sub.add_parser(
        "assess-branch-posture",
        help="Render and persist one M3 branch budget / recursion / drift posture receipt for a committed parent work unit.",
    )
    allocator_posture.add_argument("parent_work_unit_id")
    allocator_posture.add_argument("--max-branches", type=int)
    allocator_posture.add_argument("--created-at")
    allocator_posture.add_argument("--apply-decay", action="store_true")

    allocator_settlement_snapshot = allocator_sub.add_parser(
        "snapshot-settlement",
        help="Render the bounded fan-in / settlement projection for one committed parent work unit.",
    )
    allocator_settlement_snapshot.add_argument("parent_work_unit_id")
    allocator_settlement_snapshot.add_argument("--created-at")

    allocator_settle = allocator_sub.add_parser(
        "settle-children",
        help="Persist one bounded fan-in / merge / review settlement receipt for the active child returns.",
    )
    allocator_settle.add_argument("parent_work_unit_id")
    allocator_settle.add_argument("--created-at")

    allocator_sync = allocator_sub.add_parser(
        "sync-future-posture",
        help="Synchronize bounded branch posture back into parent horizon and schedule state.",
    )
    allocator_sync.add_argument("parent_work_unit_id")
    allocator_sync.add_argument("--max-branches", type=int)
    allocator_sync.add_argument("--created-at")

    allocator_reschedule = allocator_sub.add_parser(
        "reschedule-after-sync",
        help="Re-evaluate the parent schedule after synchronized branch future changes and witness any rebinding.",
    )
    allocator_reschedule.add_argument("parent_work_unit_id")
    allocator_reschedule.add_argument("--created-at")

    return parser


def _add_workspace_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workspace-root", help="Repo/workspace root containing the active ION root.")


def _add_runtime_policy_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--context-mode", default=ContextMode.IDE_MANUAL.value, choices=[item.value for item in ContextMode])
    parser.add_argument("--automation-stage", default=AutomationStage.MANUAL.value, choices=[item.value for item in AutomationStage])
    parser.add_argument("--route-stage", default=RouteStage.ACTIVE.value, choices=[item.value for item in RouteStage])
    parser.add_argument("--calibration-status", default=CalibrationStatus.INSUFFICIENT_DATA.value, choices=[item.value for item in CalibrationStatus])
    parser.add_argument("--threshold-action", choices=[item.value for item in PromotionAction])
    parser.add_argument("--review-required", action="store_true")
    parser.add_argument("--manual-fallback-required", action="store_true")
    parser.add_argument("--no-supervisor", action="store_true")


def _add_child_args(parser: argparse.ArgumentParser) -> None:
    _add_runtime_policy_args(parser)
    parser.add_argument("--repo-root")
    parser.add_argument("--constitution-excerpt", required=True)
    parser.add_argument("--template-spec", required=True)
    parser.add_argument("--kernel-excerpt")
    parser.add_argument("--agent-binding", action="append", default=[], help="role_key=personal|role|structural|tier|domain|chassis|specialty")
    parser.add_argument("--approval", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--created-by", default="OPERATOR")
    parser.add_argument("--notes")
    parser.add_argument("--expires-at")
    parser.add_argument("--actor", default="OPERATOR")
    parser.add_argument("--timestamp")


def _command_status(workspace_root: Path, store_root_arg: str | None) -> dict[str, Any]:
    store_root = _resolve_store_root(workspace_root, store_root_arg)
    hardening = KernelOperationalHardeningManager()
    snapshot = hardening.build_status_snapshot(workspace_root)
    store = KernelStore(store_root)
    index = KernelIndex()
    index.build_from_store(store)
    graph = KernelGraph()
    graph.build_from_index(index)
    horizon_manager = KernelHorizonStateManager()
    scheduler = KernelScheduler()
    registry = KernelExecutorCapabilityRegistry()
    takeover = KernelTakeoverManager()
    equivalence = KernelManualAutomationEquivalenceManager()
    continuation = KernelContextPerfectContinuationManager()
    allocator = KernelAllocator()
    branch_controls = KernelBranchControlManager()
    settlement = KernelBranchSettlementManager()
    branch_sync = KernelBranchHorizonSynchronizer()
    branch_rescheduler = KernelBranchRescheduler()
    schedule_controls = KernelScheduleControlManager()
    completion_release = KernelScheduleCompletionReleaseManager()
    settlement_manager = KernelScheduleSettlementManager()
    lineage_manager = KernelScheduleLineageArchiveManager()
    resume_manager = KernelScheduleResumeProjectionManager()
    resume_bundle_manager = KernelScheduleResumeBundleMaterializationManager()
    takeover_activation_manager = KernelScheduleTakeoverActivationManager()
    handoff_capsule_manager = KernelScheduleActivationHandoffCapsuleManager()
    handoff_entry_rehearsal_manager = KernelScheduleHandoffEntryRehearsalManager()
    executor_start_packet_manager = KernelScheduleExecutorStartPacketManager()
    bundle_manager = KernelRootAuthorityBundleManager()
    horizon_records = index.records_by_type("horizon_state")
    latest_horizon_projection = None
    if horizon_records:
        latest_record = sorted(
            horizon_records,
            key=lambda item: (getattr(item, "updated_at", ""), getattr(item, "horizon_id", "")),
        )[-1]
        latest_horizon_projection = horizon_manager.render_scope_projection(
            index,
            latest_record.scope_type,
            latest_record.scope_ref,
        )
    latest_horizon_enactment_receipt = horizon_manager.render_enactment_receipt_projection(
        horizon_manager.latest_enactment_receipt(index)
    )
    schedule_projection = scheduler.build_schedule_projection(index, graph)
    latest_schedule_projection = None
    if schedule_projection.candidates:
        latest_schedule_projection = scheduler.render_schedule_projection(schedule_projection)
    latest_schedule_receipt = scheduler.render_schedule_receipt_projection(
        scheduler.latest_schedule_receipt(index)
    )
    latest_takeover_receipt = takeover.render_takeover_receipt_projection(
        takeover.latest_takeover_receipt(index)
    )
    latest_manual_automation_equivalence_receipt = equivalence.render_equivalence_receipt_projection(
        equivalence.latest_equivalence_receipt(index)
    )
    latest_context_perfect_continuation_receipt = continuation.render_continuation_receipt_projection(
        continuation.latest_continuation_receipt(index)
    )
    latest_branch_claim_receipt = allocator.render_branch_claim_receipt_projection(
        allocator.latest_branch_claim_receipt(index)
    )
    latest_branch_control_receipt = branch_controls.render_receipt_projection(
        branch_controls.latest_branch_control_receipt(index)
    )
    latest_branch_settlement_receipt = settlement.render_receipt_projection(
        settlement.latest_settlement_receipt(index)
    )
    executor_capability_snapshot = registry.render_snapshot(registry.build_snapshot(index))
    return {
        "command": "status",
        "workspace_root": str(workspace_root),
        "store_root": str(store_root),
        "status_snapshot": snapshot,
        "store_counts": {record_type: store.count(record_type) for record_type in KernelStore.supported_record_types()},
        "store_total": store.count(),
        "latest_horizon_projection": latest_horizon_projection,
        "latest_horizon_enactment_receipt": latest_horizon_enactment_receipt,
        "latest_schedule_projection": latest_schedule_projection,
        "latest_schedule_receipt": latest_schedule_receipt,
        "latest_schedule_control_receipt": schedule_controls.render_receipt_projection(schedule_controls.latest_receipt(index)),
        "latest_takeover_receipt": latest_takeover_receipt,
        "latest_manual_automation_equivalence_receipt": latest_manual_automation_equivalence_receipt,
        "latest_context_perfect_continuation_receipt": latest_context_perfect_continuation_receipt,
        "latest_branch_claim_receipt": latest_branch_claim_receipt,
        "latest_branch_control_receipt": latest_branch_control_receipt,
        "latest_branch_settlement_receipt": latest_branch_settlement_receipt,
        "latest_branch_horizon_sync_receipt": branch_sync.render_receipt_projection(branch_sync.latest_receipt(index)),
        "latest_branch_reschedule_receipt": branch_rescheduler.render_receipt_projection(branch_rescheduler.latest_receipt(index)),
        "latest_schedule_dispatch_reconciliation_receipt": KernelScheduleDispatchReconciliationManager().render_receipt_projection(KernelScheduleDispatchReconciliationManager().latest_receipt(index)),
        "latest_schedule_completion_release_receipt": completion_release.render_receipt_projection(completion_release.latest_receipt(index)),
        "latest_schedule_settlement_receipt": settlement_manager.render_receipt_projection(settlement_manager.latest_receipt(index)),
        "latest_schedule_lineage_archive_receipt": lineage_manager.render_receipt_projection(lineage_manager.latest_receipt(index)),
        "latest_schedule_lineage_replay_receipt": KernelScheduleLineageReplayManager().render_receipt_projection(KernelScheduleLineageReplayManager().latest_receipt(index)),
        "latest_schedule_resume_projection_receipt": resume_manager.render_receipt_projection(resume_manager.latest_receipt(index)),
        "latest_schedule_resume_bundle_materialization_receipt": resume_bundle_manager.render_receipt_projection(resume_bundle_manager.latest_receipt(index)),
        "latest_schedule_takeover_entry_activation_receipt": takeover_activation_manager.render_receipt_projection(takeover_activation_manager.latest_receipt(index)),
        "latest_schedule_activation_handoff_capsule_receipt": handoff_capsule_manager.render_receipt_projection(handoff_capsule_manager.latest_receipt(index)),
        "latest_schedule_handoff_entry_rehearsal_receipt": handoff_entry_rehearsal_manager.render_receipt_projection(handoff_entry_rehearsal_manager.latest_receipt(index)),
        "latest_schedule_executor_start_packet_materialization_receipt": executor_start_packet_manager.render_receipt_projection(executor_start_packet_manager.latest_receipt(index)),
        "latest_root_authority_bundle_exercise_receipt": bundle_manager.render_receipt_projection(bundle_manager.latest_receipt(index)),
        "latest_root_authority_bundle_external_return_receipt": bundle_manager.render_external_return_receipt_projection(bundle_manager.latest_external_return_receipt(index)),
        "executor_capability_snapshot": executor_capability_snapshot,
    }


def _command_bundle(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    if args.bundle_command == "record-exercise":
        store_root = _resolve_store_root(workspace_root, getattr(args, "store_root", None))
        store = KernelStore(store_root)
        index = KernelIndex()
        index.build_from_store(store)
        manager = KernelRootAuthorityBundleManager()
        try:
            receipt = manager.record_exercise(
                store,
                index,
                workspace_root=workspace_root,
                carrier_key=getattr(args, "carrier_key", "cursor_codex"),
                execution_mode=getattr(args, "execution_mode", "BRANCH_LOCAL_EDITABLE_INSTALL"),
                executor_identity=getattr(args, "executor", None),
                created_at=getattr(args, "created_at", None),
            )
        except KernelRootAuthorityBundleError as exc:
            return {
                "command": "bundle.record_exercise",
                "store_root": str(store_root),
                "carrier_key": getattr(args, "carrier_key", "cursor_codex"),
                "execution_mode": getattr(args, "execution_mode", "BRANCH_LOCAL_EDITABLE_INSTALL"),
                "executor_identity": getattr(args, "executor", None),
                "valid": False,
                "error": str(exc),
                "warnings": ["UNPROVEN_EXTERNAL_CARRIER_RECEIPT_REFUSED"],
            }
        return {
            "command": "bundle.record_exercise",
            "store_root": str(store_root),
            **(manager.render_receipt_projection(receipt) or {}),
        }
    if args.bundle_command == "materialize-external-exercise-brief":
        manager = KernelRootAuthorityBundleManager()
        brief = manager.materialize_external_exercise_brief(
            workspace_root=workspace_root,
            carrier_key=getattr(args, "carrier_key", None),
            created_at=getattr(args, "created_at", None),
            output_path=getattr(args, "output", None),
        )
        return {
            "command": "bundle.materialize_external_exercise_brief",
            **manager.render_external_brief_projection(brief),
        }
    if args.bundle_command == "materialize-external-return-stub":
        manager = KernelRootAuthorityBundleManager()
        stub = manager.materialize_external_return_stub(
            workspace_root=workspace_root,
            carrier_key=getattr(args, "carrier_key", None),
            created_at=getattr(args, "created_at", None),
            output_path=getattr(args, "output", None),
        )
        return {
            "command": "bundle.materialize_external_return_stub",
            **manager.render_external_return_stub_projection(stub),
        }
    if args.bundle_command == "record-external-return":
        store_root = _resolve_store_root(workspace_root, getattr(args, "store_root", None))
        store = KernelStore(store_root)
        index = KernelIndex()
        index.build_from_store(store)
        manager = KernelRootAuthorityBundleManager()
        try:
            receipt = manager.record_external_return(
                store,
                index,
                workspace_root=workspace_root,
                carrier_key=getattr(args, "carrier_key", None),
                input_path=getattr(args, "input", None),
                created_at=getattr(args, "created_at", None),
            )
        except KernelRootAuthorityBundleError as exc:
            return {
                "command": "bundle.record_external_return",
                "store_root": str(store_root),
                "carrier_key": getattr(args, "carrier_key", None),
                "input_path": str(getattr(args, "input", "")),
                "valid": False,
                "error": str(exc),
            }
        return {
            "command": "bundle.record_external_return",
            "store_root": str(store_root),
            **(manager.render_external_return_receipt_projection(receipt) or {}),
        }
    snapshot = build_root_authority_bundle_snapshot(workspace_root)
    return {
        "command": f"bundle.{args.bundle_command}",
        **render_root_authority_bundle_snapshot(snapshot),
    }


def _command_runtime(args: argparse.Namespace, workspace_root: Path) -> Any:
    hardening = KernelOperationalHardeningManager()
    if args.runtime_command == "start":
        return hardening.start_supervised_runtime(
            SupervisedRuntimeStartupRequest(
                workspace_root=workspace_root,
                context_mode=_parse_context_mode(args.context_mode),
                automation_stage=_parse_automation_stage(args.automation_stage),
                route_stage=_parse_route_stage(args.route_stage),
                calibration_status=_parse_calibration_status(args.calibration_status),
                threshold_action=_parse_threshold_action(args.threshold_action),
                review_required=args.review_required,
                manual_fallback_required=args.manual_fallback_required,
                supervisor_present=not args.no_supervisor,
                explicit_approval=args.approval,
                actor=args.actor,
                reason=args.reason,
                action_timestamp=args.timestamp,
            )
        )
    if args.runtime_command == "drain":
        return hardening.shutdown_supervised_runtime(
            SupervisedRuntimeShutdownRequest(
                workspace_root=workspace_root,
                actor=args.actor,
                reason=args.reason,
                drain=True,
                action_timestamp=args.timestamp,
            )
        )
    if args.runtime_command == "stop":
        return hardening.shutdown_supervised_runtime(
            SupervisedRuntimeShutdownRequest(
                workspace_root=workspace_root,
                actor=args.actor,
                reason=args.reason,
                drain=False,
                action_timestamp=args.timestamp,
            )
        )
    raise KernelOperatorCliError(f"Unhandled runtime command: {args.runtime_command}")


def _command_control(args: argparse.Namespace, workspace_root: Path) -> Any:
    manager = KernelOperatorControlManager()
    if args.control_command == "service-mode":
        return manager.set_service_mode(
            workspace_root,
            mode=DaemonServiceControlMode(args.mode),
            reason=args.reason,
            actor=args.actor,
            created_at=args.timestamp,
        )
    if args.control_command == "hold-scope":
        return manager.hold_scope(
            workspace_root,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            reason=args.reason,
            actor=args.actor,
            created_at=args.timestamp,
        )
    if args.control_command == "resume-scope":
        return manager.resume_scope(
            workspace_root,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            actor=args.actor,
            created_at=args.timestamp,
        )
    raise KernelOperatorCliError(f"Unhandled control command: {args.control_command}")


def _command_daemon(args: argparse.Namespace, workspace_root: Path) -> Any:
    store, index, graph = _load_runtime_state(workspace_root, args.store_root)
    service = KernelDaemonService()
    if args.daemon_command == "run":
        return service.run(
            store,
            index,
            graph,
            DaemonServiceRequest(
                workspace_root=workspace_root,
                max_steps=args.max_steps,
                scope_type=args.scope_type,
                scope_ref=args.scope_ref,
                context_mode=_parse_context_mode(args.context_mode),
                automation_stage=_parse_automation_stage(args.automation_stage),
                route_stage=_parse_route_stage(args.route_stage),
                calibration_status=_parse_calibration_status(args.calibration_status),
                threshold_action=_parse_threshold_action(args.threshold_action),
                review_required=args.review_required,
                manual_fallback_required=args.manual_fallback_required,
                supervisor_present=not args.no_supervisor,
                explicit_approval=args.approval,
                dry_run=args.dry_run,
                packet_output_root=args.packet_output_root or str(_default_packet_output_root(workspace_root)),
                repo_root=args.repo_root or workspace_root,
                actor=args.actor,
                action_timestamp=args.timestamp,
            ),
        )
    raise KernelOperatorCliError(f"Unhandled daemon command: {args.daemon_command}")


def _command_replay(args: argparse.Namespace, workspace_root: Path) -> Any:
    store, index, graph = _load_runtime_state(workspace_root, args.store_root)
    manager = KernelRecoveryReplayManager()
    selection_mode = (
        RecoveryReplaySelectionMode.LATEST_RESUMABLE
        if args.replay_command == "latest"
        else RecoveryReplaySelectionMode.EXPLICIT_SERVICE_RECEIPT
    )
    return manager.replay_daemon_service(
        store,
        index,
        graph,
        RecoveryReplayRequest(
            workspace_root=workspace_root,
            selection_mode=selection_mode,
            service_receipt_path=getattr(args, "service_receipt_path", None),
            stale_after_seconds=args.stale_after_seconds,
            current_timestamp=args.timestamp,
            explicit_approval=args.approval,
            supervisor_present=True,
            allow_stale_replay=args.allow_stale,
            dry_run=args.dry_run,
            max_steps_override=args.max_steps,
            packet_output_root=args.packet_output_root or str(_default_packet_output_root(workspace_root)),
            repo_root=args.repo_root or workspace_root,
            actor=args.actor,
            notes=args.notes,
        ),
    )


def _command_child(args: argparse.Namespace, workspace_root: Path) -> Any:
    store, index, graph = _load_runtime_state(workspace_root, args.store_root)
    service = KernelChildWorkService()
    selection_mode = (
        ChildWorkSelectionMode.MANIFEST
        if args.child_command == "issue-manifest"
        else ChildWorkSelectionMode.QUESTION_DELTA
    )
    return service.issue_child_work(
        store,
        index,
        graph,
        ChildWorkServiceRequest(
            workspace_root=workspace_root,
            repo_root=Path(args.repo_root).resolve() if args.repo_root else workspace_root,
            doctrine=TierOneDoctrine(
                constitution_excerpt=args.constitution_excerpt,
                template_spec=args.template_spec,
                kernel_excerpt=args.kernel_excerpt,
            ),
            selection_mode=selection_mode,
            manifest_id=getattr(args, "manifest_id", None),
            question_id=getattr(args, "question_id", None),
            work_unit_id=getattr(args, "work_unit_id", None),
            delta_id=getattr(args, "delta_id", None),
            agent_bindings=_parse_agent_bindings(args.agent_binding),
            context_mode=_parse_context_mode(args.context_mode),
            automation_stage=_parse_automation_stage(args.automation_stage),
            route_stage=_parse_route_stage(args.route_stage),
            calibration_status=_parse_calibration_status(args.calibration_status),
            threshold_action=_parse_threshold_action(args.threshold_action),
            review_required=(True if args.review_required else None),
            manual_fallback_required=(True if args.manual_fallback_required else None),
            supervisor_present=not args.no_supervisor,
            explicit_approval=args.approval,
            dry_run=args.dry_run,
            created_by=args.created_by,
            notes=args.notes,
            expires_at=args.expires_at,
            actor=args.actor,
            action_timestamp=args.timestamp,
        ),
    )


def _command_external(args: argparse.Namespace, workspace_root: Path) -> Any:
    store, index, graph = _load_runtime_state(workspace_root, args.store_root)
    bridge = KernelExternalExecutionBridge()
    if args.external_command == "export":
        request = ExternalExecutionBridgeRequest(
            workspace_root=workspace_root,
            action_mode=ExternalExecutionActionMode.EXPORT_DISPATCH_PACKET,
            work_unit_id=args.work_unit_id,
            context_mode=_parse_context_mode(args.context_mode),
            automation_stage=_parse_automation_stage(args.automation_stage),
            route_stage=_parse_route_stage(args.route_stage),
            calibration_status=_parse_calibration_status(args.calibration_status),
            threshold_action=_parse_threshold_action(args.threshold_action),
            review_required=args.review_required,
            manual_fallback_required=args.manual_fallback_required,
            supervisor_present=not args.no_supervisor,
            explicit_approval=args.approval,
            dry_run=args.dry_run,
            actor=args.actor,
            action_timestamp=args.timestamp,
        )
    else:
        request = ExternalExecutionBridgeRequest(
            workspace_root=workspace_root,
            action_mode=ExternalExecutionActionMode.ACCEPT_EXECUTION_RETURN,
            work_unit_id=args.work_unit_id,
            submission=_load_execution_submission(Path(args.submission_json)),
            context_mode=_parse_context_mode(args.context_mode),
            automation_stage=_parse_automation_stage(args.automation_stage),
            route_stage=_parse_route_stage(args.route_stage),
            calibration_status=_parse_calibration_status(args.calibration_status),
            threshold_action=_parse_threshold_action(args.threshold_action),
            review_required=args.review_required,
            manual_fallback_required=args.manual_fallback_required,
            supervisor_present=not args.no_supervisor,
            explicit_approval=args.approval,
            dry_run=args.dry_run,
            actor=args.actor,
            action_timestamp=args.timestamp,
        )
    return bridge.bridge(store, index, graph, request)





def _command_packet(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    if args.packet_command == "validate":
        packet_path = _resolve_packet_path(workspace_root, args.path)
        result = validate_packet_path(
            packet_path,
            expected_type=getattr(args, "expected_type", None),
            allow_legacy=bool(getattr(args, "legacy", False)),
        )
        return {
            "command": "packet.validate",
            "path": str(packet_path),
            "packet_type": result.packet_type,
            "expected_type": result.expected_type,
            "valid": result.valid,
            "frontmatter_present": result.frontmatter_present,
            "title": result.title,
            "sections_present": list(result.sections_present),
            "errors": [_to_jsonable(message) for message in result.errors],
            "warnings": [_to_jsonable(message) for message in result.warnings],
        }

    if args.packet_command == "assess-takeover":
        manager = KernelTakeoverManager()
        assessment = manager.assess_packet_path(
            _resolve_packet_path(workspace_root, args.path),
            expected_type=getattr(args, "expected_type", None),
            allow_legacy=bool(getattr(args, "legacy", False)),
        )
        return {
            "command": "packet.assess_takeover",
            "path": assessment.path,
            "packet_type": assessment.packet_type,
            "title": assessment.title,
            "packet_created_at": assessment.created_at,
            "packet_status": assessment.status,
            "objective": assessment.objective,
            "scope_binding": assessment.scope_binding,
            "target_executor": assessment.target_executor,
            "required_reads": list(assessment.required_reads),
            "next_action": assessment.next_action,
            "expected_output": list(assessment.expected_output),
            "warnings": list(assessment.warnings),
            "valid": assessment.valid,
        }

    if args.packet_command == "render-takeover-role-session":
        source_path = _resolve_packet_path(workspace_root, args.path)
        manager = KernelTakeoverManager()
        assessment = manager.assess_packet_path(
            source_path,
            expected_type=getattr(args, "expected_type", None),
            allow_legacy=bool(getattr(args, "legacy", False)),
        )
        created_at = getattr(args, "created_at", None) or _json_iso_now()
        content = render_takeover_role_session(
            assessment,
            role=args.role,
            created_at=created_at,
            status=getattr(args, "status", "ACTIVE"),
        )
        output_path = None
        output_relative_path = None
        if getattr(args, "output", None):
            output_path = _resolve_packet_path(workspace_root, args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content, encoding="utf-8")
            output_relative_path = _relative_to_workspace(output_path, workspace_root)
        validation = validate_packet_text(content, expected_type="role_session")
        return {
            "command": "packet.render_takeover_role_session",
            "source_packet_path": str(source_path),
            "output_path": (None if output_path is None else str(output_path)),
            "output_relative_path": output_relative_path,
            "role": args.role,
            "created_at": created_at,
            "status": getattr(args, "status", "ACTIVE"),
            "content": content,
            "valid": validation.valid,
            "warnings": [_to_jsonable(message) for message in validation.warnings],
        }

    if args.packet_command == "record-takeover":
        packet_path = _resolve_packet_path(workspace_root, args.path)
        store_root = _resolve_store_root(workspace_root, getattr(args, "store_root", None))
        store = KernelStore(store_root)
        index = KernelIndex()
        index.build_from_store(store)
        manager = KernelTakeoverManager()
        receipt = manager.record_packet_takeover(
            store,
            index,
            packet_path,
            expected_type=getattr(args, "expected_type", None),
            allow_legacy=bool(getattr(args, "legacy", False)),
            workspace_root=workspace_root,
            created_at=getattr(args, "created_at", None),
        )
        return {
            "command": "packet.record_takeover",
            "valid": True,
            **(manager.render_takeover_receipt_projection(receipt) or {}),
        }

    if args.packet_command == "enact-horizon":
        store_root = _resolve_store_root(workspace_root, getattr(args, "store_root", None))
        store = KernelStore(store_root)
        index = KernelIndex()
        index.build_from_store(store)
        manager = KernelHorizonStateManager()
        result = manager.enact_packet_for_scope(
            index,
            args.scope_type,
            args.scope_ref,
            store=store,
            packet_type=getattr(args, "packet_type", None),
            workspace_root=workspace_root,
            output_path=getattr(args, "output", None),
            created_at=getattr(args, "created_at", None),
            status=getattr(args, "status", "ACTIVE"),
            sender=getattr(args, "sender", None),
            receiver=getattr(args, "receiver", None),
            target_surface=getattr(args, "target_surface", None),
            automation_surface=getattr(args, "automation_surface", None),
            reason=getattr(args, "reason", None),
        )
        return {
            "command": "packet.enact_horizon",
            "scope_type": result.scope_type,
            "scope_ref": result.scope_ref,
            "status": result.status,
            "packet_type": result.packet_type,
            "packet_path": result.packet_path,
            "packet_relative_path": result.packet_relative_path,
            "receipt_id": result.receipt_id,
            "candidate_item_id": result.candidate_item_id,
            "candidate_title": result.candidate_title,
            "source_layer": (None if result.source_layer is None else result.source_layer.value),
            "source_horizon_ids": list(result.source_horizon_ids),
            "requested_reads": list(result.requested_reads),
            "warnings": list(result.warnings),
            "content": result.content,
            "valid": result.valid,
        }

    raise KernelOperatorCliError(f"Unhandled packet command: {args.packet_command}")



def _bootstrap_common_kwargs(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "title": args.title,
        "goal": args.goal,
        "target": args.target,
        "agent": args.agent,
        "template": args.template,
        "priority": args.priority,
        "from_actor": args.from_actor,
        "bootstrap_signal_type": args.bootstrap_signal_type,
        "bootstrap_needed_from": args.bootstrap_needed_from,
        "bootstrap_blocker": args.bootstrap_blocker,
        "bootstrap_error": args.bootstrap_error,
        "bootstrap_recoverable": (True if args.bootstrap_recoverable else None),
        "source_context": (tuple(args.source_context) if args.source_context else DEFAULT_BOOTSTRAP_SOURCE_CONTEXT),
        "requirements": (tuple(args.requirement) if args.requirement else DEFAULT_BOOTSTRAP_REQUIREMENTS),
        "deliverables": (tuple(args.deliverable) if args.deliverable else DEFAULT_BOOTSTRAP_DELIVERABLES),
        "constraints": (tuple(args.constraint) if args.constraint else DEFAULT_BOOTSTRAP_CONSTRAINTS),
        "completion_signal": (args.completion_signal or DEFAULT_BOOTSTRAP_COMPLETION_SIGNAL),
    }


def _command_bootstrap(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    if args.bootstrap_command == "init":
        writer = KernelBootstrapInitWriter()
        result = writer.write_init(
            workspace_root,
            **_bootstrap_common_kwargs(args),
            packet_path=args.packet_path,
            bootstrap_dir=getattr(args, "bootstrap_dir", "ION/05_context/inbox/bootstrap"),
            receipts_dir=getattr(args, "receipts_dir", "ION/05_context/history/bootstrap_init_receipts"),
            created_at=getattr(args, "timestamp", None),
        )
        prep = result.preparation
        return {
            "command": "bootstrap.init",
            "packet_path": _relative_to_workspace(prep.packet_path, workspace_root),
            "receipt_path": _relative_to_workspace(prep.receipt_path, workspace_root),
            "target": prep.receipt.target,
            "signal_type": prep.receipt.signal_type,
            "agent": prep.receipt.agent,
            "priority": prep.receipt.priority,
            "valid": True,
        }

    bridge = KernelBootstrapSignalBridge()
    if args.bootstrap_command == "emit":
        result = bridge.bridge(
            workspace_root,
            packet_path=getattr(args, "path", None),
            bootstrap_dir=getattr(args, "bootstrap_dir", "ION/05_context/inbox/bootstrap"),
            archive_dir=getattr(args, "archive_dir", "ION/05_context/inbox/bootstrap/archive"),
            signals_dir=getattr(args, "signals_dir", "ION/05_context/signals"),
            receipts_dir=getattr(args, "receipts_dir", "ION/05_context/history/bootstrap_bridge_receipts"),
            emitted_at=getattr(args, "timestamp", None),
        )
        prep = result.preparation
        return {
            "command": "bootstrap.emit",
            "packet_path": _relative_to_workspace(prep.packet_path, workspace_root),
            "packet_archived_path": _relative_to_workspace(prep.packet_archived_path, workspace_root),
            "signal_id": prep.signal.signal_id,
            "signal_type": prep.signal.signal_type.value,
            "signal_path": _relative_to_workspace(prep.signal_path, workspace_root),
            "receipt_path": _relative_to_workspace(prep.receipt_path, workspace_root),
            "target": prep.signal.target,
            "source_work_unit": prep.signal.source_work_unit,
        }

    if args.bootstrap_command == "activate":
        store, index, graph = _load_runtime_state(workspace_root, None)
        manager = KernelBootstrapActivationManager()
        result = manager.activate(
            store,
            index,
            graph,
            workspace_root=workspace_root,
            **_bootstrap_common_kwargs(args),
            packet_path=args.packet_path,
            bootstrap_dir=args.bootstrap_dir,
            init_receipts_dir=args.init_receipts_dir,
            archive_dir=args.archive_dir,
            signals_dir=args.signals_dir,
            bridge_receipts_dir=args.bridge_receipts_dir,
            activation_receipts_dir=args.activation_receipts_dir,
            max_steps=args.max_steps,
            explicit_approval=args.approval,
            actor=args.actor,
            action_timestamp=args.timestamp,
        )
        return {
            "command": "bootstrap.activate",
            "packet_path": result.activation_receipt.packet_path,
            "packet_archived_path": result.activation_receipt.packet_archived_path,
            "signal_id": result.activation_receipt.signal_id,
            "signal_type": result.activation_receipt.signal_type,
            "signal_path": result.activation_receipt.signal_path,
            "daemon_service_status": result.activation_receipt.daemon_service_status,
            "daemon_service_receipt_path": result.activation_receipt.daemon_service_receipt_path,
            "activation_receipt_path": result.activation_receipt_path,
            "target": result.activation_receipt.target,
        }
    raise KernelOperatorCliError(f"Unhandled bootstrap command: {args.bootstrap_command}")


def _command_lineage(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    manager = KernelNameLineageManager()
    if args.lineage_command == "resolve":
        resolution = manager.resolve_name(
            args.name,
            surface=NameIngressSurface(getattr(args, "surface", NameIngressSurface.OPERATOR_INPUT.value)),
            strict=getattr(args, "strict", False),
        )
        payload: dict[str, Any] = {
            "command": "lineage.resolve",
            "raw_name": resolution.raw_name,
            "surface": resolution.surface.value,
            "matched": resolution.matched,
            "entity_id": resolution.entity_id,
            "entity_kind": resolution.entity_kind,
            "alias_name": resolution.alias_name,
            "alias_status": resolution.alias_status,
            "relation_type": resolution.relation_type,
            "current_true_name": resolution.current_true_name,
            "resolved_name": resolution.resolved_name,
            "decision": resolution.decision.value,
            "accepted_for_ingress": resolution.accepted_for_ingress,
            "historical_only": resolution.historical_only,
            "warning_code": resolution.warning_code,
            "successor_candidates": list(resolution.successor_candidates),
            "notes": list(resolution.notes),
        }
        if getattr(args, "record", False):
            recorded = manager.record_resolution(
                workspace_root,
                resolution,
                created_at=getattr(args, "created_at", None),
            )
            payload["receipt_id"] = recorded.receipt_id
            payload["receipt_path"] = recorded.receipt_path
            payload["ledger_path"] = recorded.ledger_path
        return payload

    if args.lineage_command == "audit-active-surfaces":
        result = manager.audit_active_surfaces(
            workspace_root,
            paths=tuple(getattr(args, "path", ()) or ()),
            include_historical=getattr(args, "include_historical", False),
        )
        return {
            "command": "lineage.audit_active_surfaces",
            "scanned_paths": list(result.scanned_paths),
            "blocked_count": result.blocked_count,
            "alert_count": result.alert_count,
            "info_count": result.info_count,
            "findings": [
                {
                    "path": item.path,
                    "line_number": item.line_number,
                    "matched_name": item.matched_name,
                    "entity_id": item.entity_id,
                    "current_true_name": item.current_true_name,
                    "decision": item.decision.value,
                    "severity": item.severity.value,
                    "warning_code": item.warning_code,
                    "recommended_action": item.recommended_action,
                    "line_excerpt": item.line_excerpt,
                }
                for item in result.findings
            ],
        }
    raise KernelOperatorCliError(f"Unhandled lineage command: {args.lineage_command}")


def _command_authority(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    manager = KernelAuthorityLineageManager()
    if args.authority_command == "resolve":
        resolution = manager.resolve_authority(workspace_root, args.surface, getattr(args, "name", None))
        return {
            "command": "authority.resolve",
            "surface": resolution.surface,
            "requested_name": resolution.requested_name,
            "resolved_name": resolution.resolved_name,
            "status": resolution.status,
            "warning": resolution.warning,
        }
    if args.authority_command == "show-surface":
        record = manager.surface_record(workspace_root, args.surface)
        return {
            "command": "authority.show-surface",
            **manager.render_surface_record(record),
        }
    if args.authority_command == "show-name":
        record = manager.name_record(workspace_root, args.name)
        return {
            "command": "authority.show-name",
            **manager.render_name_record(record),
        }
    if args.authority_command == "audit-active-surfaces":
        report = manager.audit_active_surfaces(workspace_root)
        return {
            "command": "authority.audit-active-surfaces",
            "scan_paths": list(report.scan_paths),
            "findings": [
                {
                    "surface": item.surface,
                    "path": item.path,
                    "line_number": item.line_number,
                    "matched_name": item.matched_name,
                    "resolves_to": item.resolves_to,
                    "severity": item.severity,
                    "line_text": item.line_text,
                }
                for item in report.findings
            ],
        }
    if args.authority_command == "audit-registry-alignment":
        report = manager.audit_registry_alignment(workspace_root)
        return {
            "command": "authority.audit-registry-alignment",
            "findings": [
                {
                    "surface": item.surface,
                    "authority_name": item.authority_name,
                    "severity": item.severity,
                    "issue_code": item.issue_code,
                    "message": item.message,
                }
                for item in report.findings
            ],
        }
    raise KernelOperatorCliError(f"Unhandled authority command: {args.authority_command}")

def _command_schedule(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    store, index, graph = _load_runtime_state(workspace_root, args.store_root)
    scheduler = KernelScheduler()
    scope_type = getattr(args, "scope_type", None)
    scope_ref = getattr(args, "scope_ref", None)

    if args.schedule_command == "snapshot":
        projection = scheduler.build_schedule_projection(
            index,
            graph,
            scope_type=scope_type,
            scope_ref=scope_ref,
        )
        return {
            "command": "schedule.snapshot",
            **scheduler.render_schedule_projection(projection),
        }

    if args.schedule_command == "record":
        receipt = scheduler.record_selected_candidate(
            store,
            index,
            graph,
            scope_type=scope_type,
            scope_ref=scope_ref,
            created_at=getattr(args, "created_at", None),
        )
        return {
            "command": "schedule.record",
            **(scheduler.render_schedule_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "maintain":
        controls = KernelScheduleControlManager()
        receipt = controls.maintain_schedule(
            store,
            index,
            graph,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            stale_after_seconds=getattr(args, "stale_after_seconds", 1800),
            generated_at=getattr(args, "created_at", None),
        )
        return {
            "command": "schedule.maintain",
            **(controls.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "reconcile":
        reconciliation = KernelScheduleDispatchReconciliationManager()
        receipt = reconciliation.reconcile(
            store,
            index,
            graph,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            generated_at=getattr(args, "created_at", None),
            packet_output_root=(getattr(args, "packet_output_root", None) or str(_default_packet_output_root(workspace_root))),
        )
        return {
            "command": "schedule.reconcile",
            **(reconciliation.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "release-completion":
        release_manager = KernelScheduleCompletionReleaseManager()
        receipt = release_manager.reconcile_release(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            generated_at=getattr(args, "created_at", None),
        )
        return {
            "command": "schedule.release_completion",
            **(release_manager.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "settle":
        settlement_manager = KernelScheduleSettlementManager()
        receipt = settlement_manager.settle_and_reenter(
            store,
            index,
            graph,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            generated_at=getattr(args, "created_at", None),
        )
        return {
            "command": "schedule.settle",
            **(settlement_manager.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "archive-lineage":
        lineage_manager = KernelScheduleLineageArchiveManager()
        receipt = lineage_manager.archive_lineage(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            generated_at=getattr(args, "created_at", None),
        )
        return {
            "command": "schedule.archive_lineage",
            **(lineage_manager.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "replay-lineage":
        replay_manager = KernelScheduleLineageReplayManager()
        receipt = replay_manager.replay_lineage(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            generated_at=getattr(args, "created_at", None),
        )
        return {
            "command": "schedule.replay_lineage",
            **(replay_manager.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "project-resume":
        resume_manager = KernelScheduleResumeProjectionManager()
        receipt = resume_manager.project_resume(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            workspace_root=workspace_root,
            output_path=getattr(args, "output", None),
            generated_at=getattr(args, "created_at", None),
            status=getattr(args, "status", "ACTIVE"),
            role=getattr(args, "role", None),
        )
        return {
            "command": "schedule.project_resume",
            **(resume_manager.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "materialize-resume-bundle":
        resume_bundle_manager = KernelScheduleResumeBundleMaterializationManager()
        receipt = resume_bundle_manager.materialize_bundle(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            workspace_root=workspace_root,
            generated_at=getattr(args, "created_at", None),
            packet_output_path=getattr(args, "packet_output", None),
            bundle_output_root=getattr(args, "bundle_output_root", None),
            status=getattr(args, "status", "ACTIVE"),
            role=getattr(args, "role", None),
        )
        return {
            "command": "schedule.materialize_resume_bundle",
            **(resume_bundle_manager.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "validate-activation":
        takeover_activation_manager = KernelScheduleTakeoverActivationManager()
        receipt = takeover_activation_manager.validate_activation(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            workspace_root=workspace_root,
            generated_at=getattr(args, "created_at", None),
            summary_output_path=getattr(args, "summary_output", None),
            status=getattr(args, "status", "ACTIVE"),
            role=getattr(args, "role", None),
        )
        return {
            "command": "schedule.validate_activation",
            **(takeover_activation_manager.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "materialize-handoff-capsule":
        handoff_capsule_manager = KernelScheduleActivationHandoffCapsuleManager()
        receipt = handoff_capsule_manager.materialize_handoff_capsule(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            workspace_root=workspace_root,
            generated_at=getattr(args, "created_at", None),
            output_root=getattr(args, "output_root", None),
            status=getattr(args, "status", "ACTIVE"),
            role=getattr(args, "role", None),
        )
        return {
            "command": "schedule.materialize_handoff_capsule",
            **(handoff_capsule_manager.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "rehearse-handoff-entry":
        handoff_entry_rehearsal_manager = KernelScheduleHandoffEntryRehearsalManager()
        receipt = handoff_entry_rehearsal_manager.rehearse_entry(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            workspace_root=workspace_root,
            generated_at=getattr(args, "created_at", None),
            summary_output_path=getattr(args, "summary_output", None),
            manifest_output_path=getattr(args, "manifest_output", None),
            status=getattr(args, "status", "ACTIVE"),
        )
        return {
            "command": "schedule.rehearse_handoff_entry",
            **(handoff_entry_rehearsal_manager.render_receipt_projection(receipt) or {}),
        }

    if args.schedule_command == "materialize-executor-start-packet":
        executor_start_packet_manager = KernelScheduleExecutorStartPacketManager()
        receipt = executor_start_packet_manager.materialize_executor_start_packet(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            workspace_root=workspace_root,
            generated_at=getattr(args, "created_at", None),
            packet_output_path=getattr(args, "packet_output", None),
            manifest_output_path=getattr(args, "manifest_output", None),
            status=getattr(args, "status", "ACTIVE"),
            role=getattr(args, "role", None),
        )
        return {
            "command": "schedule.materialize_executor_start_packet",
            **(executor_start_packet_manager.render_receipt_projection(receipt) or {}),
        }

    raise KernelOperatorCliError(f"Unhandled schedule command: {args.schedule_command}")


def _command_capability(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    store_root = _resolve_store_root(workspace_root, getattr(args, "store_root", None))
    store = KernelStore(store_root)
    index = KernelIndex()
    index.build_from_store(store)
    registry = KernelExecutorCapabilityRegistry()

    if args.capability_command == "snapshot":
        snapshot = registry.build_snapshot(
            index,
            include_inactive=bool(getattr(args, "include_inactive", False)),
        )
        return {
            "command": "capability.snapshot",
            **registry.render_snapshot(snapshot),
        }

    if args.capability_command == "register":
        created_at = getattr(args, "created_at", None) or _json_iso_now()
        capability = ExecutorCapability(
            capability_id=args.capability_id,
            executor_id=args.executor_id,
            created_at=created_at,
            updated_at=created_at,
            personal_name=args.personal_name,
            role=args.role,
            structural_identity=args.structural_identity,
            carrier=ScheduleCarrier(args.carrier),
            trust_class=ExecutorTrustClass(args.trust_class),
            availability=ExecutorAvailability(args.availability),
            max_concurrency=args.max_concurrency,
            active_assignments=args.active_assignments,
            supported_scope_types=tuple(args.scope_type),
            domain_fitness=tuple(args.domain),
            supported_packet_families=tuple(args.packet_family),
            fallback_suitability=FallbackSuitability(args.fallback_suitability),
            aliases=tuple(args.alias),
            side_effect_constraints=tuple(args.side_effect_constraint),
            notes=args.notes,
        )
        registered = registry.register(store, index, capability)
        return {
            "command": "capability.register",
            **registry.render_capability(registered),
        }

    raise KernelOperatorCliError(f"Unhandled capability command: {args.capability_command}")


def _command_question(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    store, index, graph = _load_runtime_state(workspace_root, getattr(args, "store_root", None))
    domains = tuple(getattr(args, "domain", ()) or ()) or None
    projection_builder = KernelQuestionAnswerProjectionBuilder()

    if args.question_command == "queue":
        reviewer = getattr(args, "reviewer", None)
        pending_limit = getattr(args, "pending_limit", None)
        answer_limit = getattr(args, "answer_limit", None)
        full_pending = projection_builder.pending_questions(
            index,
            reviewer=reviewer,
            domains=domains,
            limit=None,
        )
        full_recent = projection_builder.recent_answers(
            index,
            reviewer=reviewer,
            domains=domains,
            limit=None,
        )
        if getattr(args, "record", False):
            result = projection_builder.persist_reviewer_queue_projection(
                store,
                index,
                graph,
                reviewer=reviewer,
                domains=domains,
                pending_limit=pending_limit,
                answer_limit=answer_limit,
                generated_at=getattr(args, "generated_at", None),
            )
            queue = result.queue
            return {
                "command": "question.queue",
                "reviewer": queue.reviewer,
                "domains": list(queue.domains),
                "recorded": True,
                "projection_id": result.projection.projection_id,
                "generated_at": result.projection.generated_at,
                "pending_total": result.projection.pending_total_count,
                "recent_answer_total": result.projection.recent_answer_total_count,
                "pending_questions": [_render_open_question(question) for question in queue.pending_questions],
                "recent_answers": [_render_question_answer_projection(item) for item in queue.recent_answers],
            }
        queue = projection_builder.reviewer_queue(
            index,
            reviewer=reviewer,
            domains=domains,
            pending_limit=pending_limit,
            answer_limit=answer_limit,
        )
        return {
            "command": "question.queue",
            "reviewer": queue.reviewer,
            "domains": list(queue.domains),
            "recorded": False,
            "pending_total": len(full_pending),
            "recent_answer_total": len(full_recent),
            "pending_questions": [_render_open_question(question) for question in queue.pending_questions],
            "recent_answers": [_render_question_answer_projection(item) for item in queue.recent_answers],
        }

    if args.question_command == "answer":
        question_record = index.get("open_question", args.question_id)
        answered_by = getattr(args, "answered_by", None)
        if answered_by is None:
            if question_record is None or not isinstance(question_record, OpenQuestion):
                raise KernelOperatorCliError(
                    f"Unknown open question: {args.question_id}"
                )
            answered_by = question_record.needed_from
            if not answered_by:
                raise KernelOperatorCliError(
                    "question.answer requires --answered-by when the question does not declare needed_from."
                )
        ingestor = KernelQuestionAnswerIngestor()
        result = ingestor.ingest_answer(
            store,
            index,
            graph,
            QuestionAnswerSubmission(
                question_id=args.question_id,
                answered_by=answered_by,
                resolution=args.resolution,
                resolution_evidence=tuple(getattr(args, "evidence", ()) or ()),
                answered_at=getattr(args, "answered_at", None),
                notes=getattr(args, "notes", None),
            ),
        )
        projection = projection_builder.projection_for_answer(index, result.persisted_answer.answer_id)
        return {
            "command": "question.answer",
            "question_id": result.persisted_answer.question_id,
            "answer_id": result.persisted_answer.answer_id,
            "answered_by": result.persisted_answer.answered_by,
            "synthesized_work_unit": result.preparation.synthesized_work_unit is not None,
            "resolution": result.persisted_answer.resolution,
            "resolution_evidence": list(result.persisted_answer.resolution_evidence),
            "notes": result.persisted_answer.notes,
            "question": _render_open_question(result.resolution_result.question_after),
            "work_unit": _render_work_unit_summary(projection.work_unit),
        }

    raise KernelOperatorCliError(f"Unhandled question command: {args.question_command}")


def _command_equivalence(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    store_root = _resolve_store_root(workspace_root, getattr(args, "store_root", None))
    store = KernelStore(store_root)
    index = KernelIndex()
    index.build_from_store(store)
    manager = KernelManualAutomationEquivalenceManager()

    if args.equivalence_command == "snapshot":
        receipt = manager.latest_equivalence_receipt(
            index,
            scope_type=getattr(args, "scope_type", None),
            scope_ref=getattr(args, "scope_ref", None),
        )
        return {
            "command": "equivalence.snapshot",
            **(manager.render_equivalence_receipt_projection(receipt) or {}),
        }

    if args.equivalence_command == "rehearse-horizon":
        receipt = manager.rehearse_horizon_equivalence(
            store,
            index,
            scope_type=args.scope_type,
            scope_ref=args.scope_ref,
            workspace_root=workspace_root,
            automation_packet_type=args.automation_packet_type,
            automation_output_path=getattr(args, "automation_output", None),
            manual_output_path=getattr(args, "manual_output", None),
            created_at=getattr(args, "created_at", None),
            automation_sender=getattr(args, "automation_sender", "HORIZON"),
            automation_receiver=getattr(args, "automation_receiver", "Automation carrier"),
            automation_target_surface=getattr(args, "automation_target_surface", "Supervised runtime / automation carrier"),
            manual_operator=getattr(args, "manual_operator", "OPERATOR"),
            manual_automation_surface=getattr(args, "manual_automation_surface", "supervised runtime"),
            manual_reason=getattr(args, "manual_reason", "manual/automation equivalence rehearsal"),
        )
        return {
            "command": "equivalence.rehearse_horizon",
            **(manager.render_equivalence_receipt_projection(receipt) or {}),
        }

    raise KernelOperatorCliError(f"Unhandled equivalence command: {args.equivalence_command}")


def _command_continuation(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    store_root = _resolve_store_root(workspace_root, getattr(args, "store_root", None))
    store = KernelStore(store_root)
    index = KernelIndex()
    index.build_from_store(store)
    manager = KernelContextPerfectContinuationManager()

    if args.continuation_command == "snapshot":
        receipt = manager.latest_continuation_receipt(
            index,
            scope_type=getattr(args, "scope_type", None),
            scope_ref=getattr(args, "scope_ref", None),
        )
        return {
            "command": "continuation.snapshot",
            **(manager.render_continuation_receipt_projection(receipt) or {}),
        }

    if args.continuation_command == "prove-packet":
        repo_root_arg = getattr(args, "repo_root", None)
        repo_root = None
        if repo_root_arg is not None:
            repo_candidate = Path(repo_root_arg)
            repo_root = repo_candidate.resolve() if repo_candidate.is_absolute() else (workspace_root / repo_candidate).resolve()
        receipt = manager.prove_packet_continuation(
            store,
            index,
            _resolve_packet_path(workspace_root, args.path),
            workspace_root=workspace_root,
            repo_root=repo_root,
            expected_type=getattr(args, "expected_type", None),
            allow_legacy=bool(getattr(args, "legacy", False)),
            role=getattr(args, "role", "FreshExecutor"),
            output_root=getattr(args, "output_root", None),
            created_at=getattr(args, "created_at", None),
            status=getattr(args, "status", "ACTIVE"),
        )
        return {
            "command": "continuation.prove_packet",
            **(manager.render_continuation_receipt_projection(receipt) or {}),
        }

    raise KernelOperatorCliError(f"Unhandled continuation command: {args.continuation_command}")


def _command_allocator(args: argparse.Namespace, workspace_root: Path) -> dict[str, Any]:
    store, index, graph = _load_runtime_state(workspace_root, getattr(args, "store_root", None))
    allocator = KernelAllocator()
    branch_controls = KernelBranchControlManager()

    if args.allocator_command == "snapshot-children":
        projection = allocator.build_children_projection(
            index,
            graph,
            args.parent_work_unit_id,
            max_branches=getattr(args, "max_branches", None),
        )
        return {
            "command": "allocator.snapshot_children",
            **allocator.render_projection(projection),
        }

    if args.allocator_command == "claim-children":
        projection = allocator.build_children_projection(
            index,
            graph,
            args.parent_work_unit_id,
            max_branches=getattr(args, "max_branches", None),
            generated_at=getattr(args, "created_at", None),
        )
        receipts = allocator.persist_branch_claims(
            store,
            index,
            graph,
            args.parent_work_unit_id,
            max_branches=getattr(args, "max_branches", None),
            created_at=getattr(args, "created_at", None),
        )
        return {
            "command": "allocator.claim_children",
            **allocator.render_projection(projection),
            "persisted_receipt_ids": [receipt.receipt_id for receipt in receipts],
        }

    if args.allocator_command == "assess-branch-posture":
        projection = branch_controls.build_posture(
            index,
            args.parent_work_unit_id,
            generated_at=getattr(args, "created_at", None),
            max_branches=getattr(args, "max_branches", None),
        )
        receipt = branch_controls.persist_posture(
            store,
            index,
            args.parent_work_unit_id,
            generated_at=getattr(args, "created_at", None),
            max_branches=getattr(args, "max_branches", None),
            apply_decay=getattr(args, "apply_decay", False),
        )
        return {
            "command": "allocator.assess_branch_posture",
            **branch_controls.render_projection(projection),
            "persisted_receipt_id": receipt.receipt_id,
        }

    settlement = KernelBranchSettlementManager()
    branch_sync = KernelBranchHorizonSynchronizer()
    branch_rescheduler = KernelBranchRescheduler()

    if args.allocator_command == "snapshot-settlement":
        projection = settlement.build_settlement_projection(
            index,
            args.parent_work_unit_id,
            generated_at=getattr(args, "created_at", None),
        )
        return {
            "command": "allocator.snapshot_settlement",
            **settlement.render_projection(projection),
        }

    if args.allocator_command == "settle-children":
        projection = settlement.build_settlement_projection(
            index,
            args.parent_work_unit_id,
            generated_at=getattr(args, "created_at", None),
        )
        receipt, merge_proposal = settlement.persist_settlement(
            store,
            index,
            args.parent_work_unit_id,
            created_at=getattr(args, "created_at", None),
        )
        return {
            "command": "allocator.settle_children",
            **settlement.render_projection(projection),
            "receipt_id": receipt.receipt_id,
            "merge_proposal_id": (None if merge_proposal is None else merge_proposal.proposal_id),
        }

    if args.allocator_command == "sync-future-posture":
        receipt = branch_sync.synchronize_parent_scope(
            store,
            index,
            graph,
            args.parent_work_unit_id,
            generated_at=getattr(args, "created_at", None),
            max_branches=getattr(args, "max_branches", None),
        )
        return {
            "command": "allocator.sync_future_posture",
            **branch_sync.render_receipt_projection(receipt),
        }

    if args.allocator_command == "reschedule-after-sync":
        receipt = branch_rescheduler.reschedule_after_sync(
            store,
            index,
            graph,
            args.parent_work_unit_id,
            generated_at=getattr(args, "created_at", None),
        )
        return {
            "command": "allocator.reschedule_after_sync",
            **branch_rescheduler.render_receipt_projection(receipt),
        }

    raise KernelOperatorCliError(f"Unhandled allocator command: {args.allocator_command}")


def _resolve_packet_path(workspace_root: Path, packet_path: str) -> Path:
    candidate = Path(packet_path)
    if candidate.is_absolute():
        return candidate.resolve()
    return (workspace_root / candidate).resolve()


def _resolve_workspace_root(value: str | None) -> Path:
    return Path(value).resolve() if value else default_repo_root()


def _json_iso_now() -> str:
    from datetime import datetime

    return datetime.now().astimezone().isoformat(timespec="seconds")


def _resolve_store_root(workspace_root: Path, explicit: str | None) -> Path:
    return Path(explicit).resolve() if explicit else (workspace_root / DEFAULT_STORE_RELATIVE_PATH).resolve()


def _default_packet_output_root(workspace_root: Path) -> Path:
    return (workspace_root / DEFAULT_PACKET_OUTPUT_RELATIVE_PATH).resolve()


def _load_runtime_state(workspace_root: Path, store_root_arg: str | None) -> tuple[KernelStore, KernelIndex, KernelGraph]:
    store = KernelStore(_resolve_store_root(workspace_root, store_root_arg))
    index = KernelIndex()
    index.build_from_store(store)
    graph = KernelGraph()
    graph.build_from_index(index)
    return store, index, graph


def _parse_context_mode(value: str) -> ContextMode:
    return ContextMode(value)


def _parse_automation_stage(value: str) -> AutomationStage:
    return AutomationStage(value)


def _parse_route_stage(value: str) -> RouteStage:
    return RouteStage(value)


def _parse_calibration_status(value: str) -> CalibrationStatus:
    return CalibrationStatus(value)


def _parse_threshold_action(value: str | None) -> PromotionAction | None:
    return None if value is None else PromotionAction(value)


def _parse_agent_bindings(items: list[str]) -> dict[str, ChildAgentBinding] | None:
    if not items:
        return None
    bindings: dict[str, ChildAgentBinding] = {}
    for item in items:
        key, sep, payload = item.partition("=")
        if not sep:
            raise KernelOperatorCliError("agent-binding entries must use role_key=personal|role|structural|tier|domain|chassis|specialty")
        fields = payload.split("|")
        if len(fields) != 7:
            raise KernelOperatorCliError("agent-binding payload must contain 7 pipe-delimited fields")
        personal, role, structural, tier_text, domain, chassis, specialty = fields
        bindings[key] = ChildAgentBinding(
            personal_name=personal,
            role=role,
            structural_identity=structural,
            tier=int(tier_text),
            domain=domain,
            chassis=chassis,
            specialty=specialty,
        )
    return bindings


def _load_execution_submission(path: Path) -> ExecutionSubmission:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise KernelOperatorCliError("submission_json must contain a JSON object")
    artifacts_payload = payload.get("produced_artifacts", [])
    if not isinstance(artifacts_payload, list):
        raise KernelOperatorCliError("produced_artifacts must be a JSON list")
    produced_artifacts = tuple(
        ProducedArtifact(
            path=str(item["path"]),
            content=str(item["content"]),
            operation=ArtifactOperation(str(item["operation"])),
            authority_class=AuthorityClass(str(item["authority_class"])),
        )
        for item in artifacts_payload
        if isinstance(item, dict)
    )
    signals_payload = payload.get("proposed_signals", [])
    if not isinstance(signals_payload, list):
        raise KernelOperatorCliError("proposed_signals must be a JSON list")
    proposed_signals = tuple(
        ProposedSignal(
            signal_type=str(item["signal_type"]),
            target=str(item["target"]),
            payload=dict(item.get("payload", {})),
        )
        for item in signals_payload
        if isinstance(item, dict)
    )
    return ExecutionSubmission(
        produced_artifacts=produced_artifacts,
        confidence=float(payload["confidence"]),
        context_version=(None if payload.get("context_version") is None else str(payload.get("context_version"))),
        proposed_signals=proposed_signals,
        contradictions=tuple(str(item) for item in payload.get("contradictions", ())),
        notes=(None if payload.get("notes") is None else str(payload.get("notes"))),
        delta_id=(None if payload.get("delta_id") is None else str(payload.get("delta_id"))),
        created_at=(None if payload.get("created_at") is None else str(payload.get("created_at"))),
    )


def _render_open_question(question: Any) -> dict[str, Any]:
    return {
        "question_id": question.question_id,
        "created_at": question.created_at,
        "domain": question.domain,
        "needed_from": question.needed_from,
        "priority": question.priority,
        "status": question.status,
        "origin_work_unit": question.origin_work_unit,
        "scope_ref": question.scope_ref,
        "question_text": question.question_text,
        "blocking": list(question.blocking),
        "linked_artifacts": list(question.linked_artifacts),
        "resolution": question.resolution,
        "resolved_by": question.resolved_by,
        "resolved_at": question.resolved_at,
    }


def _render_question_answer_projection(projection: Any) -> dict[str, Any]:
    return {
        "answer_id": projection.answer.answer_id,
        "question_id": projection.answer.question_id,
        "answered_by": projection.answer.answered_by,
        "created_at": projection.answer.created_at,
        "question_domain": projection.answer.question_domain,
        "resolution": projection.answer.resolution,
        "resolution_evidence": list(projection.answer.resolution_evidence),
        "work_unit": _render_work_unit_summary(projection.work_unit),
        "question": _render_open_question(projection.question),
    }


def _render_work_unit_summary(work_unit: Any) -> dict[str, Any]:
    return {
        "work_unit_id": work_unit.work_unit_id,
        "created_at": work_unit.created_at,
        "protocol_id": work_unit.protocol_id,
        "transition_id": work_unit.transition_id,
        "context_version": work_unit.context_version,
        "agent_personal_name": work_unit.agent_personal_name,
        "agent_role": work_unit.agent_role,
        "agent_structural_id": work_unit.agent_structural_id,
        "agent_domain": work_unit.agent_domain,
        "chassis": work_unit.chassis,
        "scope_type": work_unit.scope_type,
        "scope_ref": work_unit.scope_ref,
        "bound_template": work_unit.bound_template,
        "priority": work_unit.priority,
        "status": work_unit.status,
        "allowed_writes": list(work_unit.allowed_writes),
        "allowed_next_actions": list(work_unit.allowed_next_actions),
        "open_questions_in_scope": list(work_unit.open_questions_in_scope),
    }


def _emit(payload: Any, output_format: str) -> int:
    if output_format == "json":
        print(json.dumps(_to_jsonable(payload), indent=2, sort_keys=True))
        return 0
    print(_to_text(payload))
    return 0


def _to_jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    return value


def _to_text(payload: Any) -> str:
    if isinstance(payload, dict) and payload.get("command") == "status":
        snapshot = payload["status_snapshot"]
        data = _to_jsonable(snapshot)
        lines = [
            "ION Operator Status",
            f"workspace_root: {payload['workspace_root']}",
            f"store_root: {payload['store_root']}",
            f"preferred_active_mode: {data['preferred_active_mode']}",
            f"service_mode: {data['operator_control_state']['service_mode']}",
            f"latest_daemon_service_status: {data['latest_daemon_service_status']}",
            f"child_work_service_events: {data['child_work_service_events']}",
            f"recovery_replay_events: {data['recovery_replay_events']}",
            f"external_execution_events: {data['external_execution_events']}",
        ]
        latest_horizon = payload.get("latest_horizon_projection")
        if latest_horizon is not None:
            tightening = latest_horizon["tightening"]
            lines.extend([
                f"latest_horizon_scope: {latest_horizon['scope_type']}:{latest_horizon['scope_ref']}",
                f"horizon_tightening_status: {tightening['status']}",
                f"horizon_packet_ready: {tightening['packet_ready']}",
            ])
            if tightening.get("candidate_title"):
                lines.append(f"horizon_candidate: {tightening['candidate_title']}")
        latest_receipt = payload.get("latest_horizon_enactment_receipt")
        if latest_receipt is not None:
            lines.extend([
                f"latest_horizon_enactment_receipt: {latest_receipt['receipt_id']}",
                f"latest_horizon_enactment_scope: {latest_receipt['scope_type']}:{latest_receipt['scope_ref']}",
                f"latest_horizon_enactment_packet: {latest_receipt['packet_type']}",
            ])
            if latest_receipt.get("candidate_title"):
                lines.append(f"latest_horizon_enactment_candidate: {latest_receipt['candidate_title']}")
            if latest_receipt.get("packet_relative_path"):
                lines.append(f"latest_horizon_enactment_path: {latest_receipt['packet_relative_path']}")
        latest_takeover = payload.get("latest_takeover_receipt")
        if latest_takeover is not None:
            lines.extend([
                f"latest_takeover_receipt: {latest_takeover['receipt_id']}",
                f"latest_takeover_scope: {latest_takeover['scope_type']}:{latest_takeover['scope_ref']}",
                f"latest_takeover_packet: {latest_takeover['packet_type']}",
            ])
            if latest_takeover.get("packet_relative_path"):
                lines.append(f"latest_takeover_path: {latest_takeover['packet_relative_path']}")
        latest_equivalence = payload.get("latest_manual_automation_equivalence_receipt")
        if latest_equivalence is not None:
            lines.extend([
                f"latest_manual_automation_equivalence_receipt: {latest_equivalence['receipt_id']}",
                f"latest_manual_automation_equivalence_scope: {latest_equivalence['scope_type']}:{latest_equivalence['scope_ref']}",
                f"latest_manual_automation_equivalence_candidate: {latest_equivalence['candidate_title']}",
            ])
            if latest_equivalence.get("automation_packet_relative_path"):
                lines.append(
                    f"latest_manual_automation_equivalence_automation_path: {latest_equivalence['automation_packet_relative_path']}"
                )
            if latest_equivalence.get("manual_packet_relative_path"):
                lines.append(
                    f"latest_manual_automation_equivalence_manual_path: {latest_equivalence['manual_packet_relative_path']}"
                )
        latest_continuation = payload.get("latest_context_perfect_continuation_receipt")
        if latest_continuation is not None:
            lines.extend([
                f"latest_context_perfect_continuation_receipt: {latest_continuation['receipt_id']}",
                f"latest_context_perfect_continuation_scope: {latest_continuation['scope_type']}:{latest_continuation['scope_ref']}",
                f"latest_context_perfect_continuation_packet: {latest_continuation['packet_type']}",
            ])
            if latest_continuation.get("bundle_root_relative_path"):
                lines.append(
                    f"latest_context_perfect_continuation_bundle: {latest_continuation['bundle_root_relative_path']}"
                )
        latest_branch_claim = payload.get("latest_branch_claim_receipt")
        if latest_branch_claim is not None:
            lines.extend([
                f"latest_branch_claim_receipt: {latest_branch_claim['receipt_id']}",
                f"latest_branch_claim_parent: {latest_branch_claim['parent_scope_type']}:{latest_branch_claim['parent_scope_ref']}",
                f"latest_branch_claim_branch: {latest_branch_claim['branch_work_unit_id']}",
            ])
            if latest_branch_claim.get("selected_executor_id"):
                lines.append(
                    f"latest_branch_claim_executor: {latest_branch_claim['selected_executor_id']}"
                )
        latest_branch_settlement = payload.get("latest_branch_settlement_receipt")
        if latest_branch_settlement is not None:
            lines.extend([
                f"latest_branch_settlement_receipt: {latest_branch_settlement['receipt_id']}",
                f"latest_branch_settlement_parent: {latest_branch_settlement['parent_scope_type']}:{latest_branch_settlement['parent_scope_ref']}",
                f"latest_branch_settlement_outcome: {latest_branch_settlement['outcome']}",
            ])
            if latest_branch_settlement.get("merge_proposal_id"):
                lines.append(
                    f"latest_branch_settlement_merge_proposal: {latest_branch_settlement['merge_proposal_id']}"
                )
        latest_bundle_exercise = payload.get("latest_root_authority_bundle_exercise_receipt")
        if latest_bundle_exercise is not None:
            lines.extend([
                f"latest_root_authority_bundle_exercise_receipt: {latest_bundle_exercise['receipt_id']}",
                f"latest_root_authority_bundle_exercise_carrier: {latest_bundle_exercise['carrier_key']}",
                f"latest_root_authority_bundle_exercise_mode: {latest_bundle_exercise['execution_mode']}",
                f"latest_root_authority_bundle_exercise_valid: {'yes' if latest_bundle_exercise.get('valid') else 'no'}",
            ])
        latest_bundle_external_return = payload.get("latest_root_authority_bundle_external_return_receipt")
        if latest_bundle_external_return is not None:
            lines.extend([
                f"latest_root_authority_bundle_external_return_receipt: {latest_bundle_external_return['receipt_id']}",
                f"latest_root_authority_bundle_external_return_carrier: {latest_bundle_external_return['carrier_key']}",
                f"latest_root_authority_bundle_external_return_status: {latest_bundle_external_return['external_return_status']}",
                f"latest_root_authority_bundle_external_return_valid: {'yes' if latest_bundle_external_return.get('valid') else 'no'}",
            ])
        lines.append("store_counts:")
        for key, value in payload["store_counts"].items():
            lines.append(f"  - {key}: {value}")
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") in {"bundle.snapshot", "bundle.validate"}:
        lines = [
            "ION Root Authority Bundle",
            f"bundle_root: {payload['bundle_root_relative_path']}",
            f"manifest_path: {payload['manifest_relative_path']}",
            f"status: {payload.get('status') or 'UNKNOWN'}",
            f"valid: {'yes' if payload.get('valid') else 'no'}",
        ]
        if payload.get("shared_entry"):
            lines.append(f"shared_entry: {payload['shared_entry']}")
        if payload.get("forward_path_anchor"):
            lines.append(f"forward_path_anchor: {payload['forward_path_anchor']}")
        carrier_entries = payload.get("carrier_entries") or {}
        if carrier_entries:
            lines.append("carrier_entries:")
            for key in sorted(carrier_entries):
                lines.append(f"  - {key}: {carrier_entries[key]}")
        missing = payload.get("missing_paths") or []
        if missing:
            lines.append("missing_paths:")
            lines.extend(f"  - {item}" for item in missing)
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "bundle.record_exercise":
        lines = [
            "ION Root Authority Bundle Exercise",
            f"carrier_key: {payload['carrier_key']}",
            f"execution_mode: {payload['execution_mode']}",
            f"valid: {'yes' if payload.get('valid') else 'no'}",
        ]
        if payload.get("receipt_id"):
            lines.append(f"receipt_id: {payload['receipt_id']}")
        if payload.get("bundle_status"):
            lines.append(f"bundle_status: {payload['bundle_status']}")
        if payload.get("executor_identity"):
            lines.append(f"executor_identity: {payload['executor_identity']}")
        if payload.get("carrier_entry_path"):
            lines.append(f"carrier_entry_path: {payload['carrier_entry_path']}")
        if payload.get("error"):
            lines.append(f"error: {payload['error']}")
        if payload.get("next_action"):
            lines.append(f"next_action: {payload['next_action']}")
        missing = payload.get("missing_paths") or []
        if missing:
            lines.append("missing_paths:")
            lines.extend(f"  - {item}" for item in missing)
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "bundle.materialize_external_exercise_brief":
        lines = [
            "ION Root Authority External Exercise Brief",
            f"carrier_key: {payload['carrier_key']}",
            f"carrier_label: {payload['carrier_label']}",
            f"output_path: {payload['output_path']}",
            f"valid: {'yes' if payload.get('valid') else 'no'}",
        ]
        if payload.get("shared_entry"):
            lines.append(f"shared_entry: {payload['shared_entry']}")
        if payload.get("carrier_entry_path"):
            lines.append(f"carrier_entry_path: {payload['carrier_entry_path']}")
        if payload.get("forward_path_anchor"):
            lines.append(f"forward_path_anchor: {payload['forward_path_anchor']}")
        warnings = payload.get("warnings") or []
        if warnings:
            lines.append("warnings:")
            lines.extend(f"  - {item}" for item in warnings)
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "bundle.materialize_external_return_stub":
        lines = [
            "ION Root Authority External Return Stub",
            f"carrier_key: {payload['carrier_key']}",
            f"carrier_label: {payload['carrier_label']}",
            f"output_path: {payload['output_path']}",
            f"governing_packet: {payload['governing_packet']}",
            f"valid: {'yes' if payload.get('valid') else 'no'}",
        ]
        warnings = payload.get("warnings") or []
        if warnings:
            lines.append("warnings:")
            lines.extend(f"  - {item}" for item in warnings)
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "bundle.record_external_return":
        lines = [
            "ION Root Authority External Return Receipt",
            f"carrier_key: {payload.get('carrier_key')}",
            f"valid: {'yes' if payload.get('valid') else 'no'}",
        ]
        if payload.get("receipt_id"):
            lines.append(f"receipt_id: {payload['receipt_id']}")
        if payload.get("external_return_status"):
            lines.append(f"external_return_status: {payload['external_return_status']}")
        if payload.get("governing_packet"):
            lines.append(f"governing_packet: {payload['governing_packet']}")
        if payload.get("source_relative_path"):
            lines.append(f"source_relative_path: {payload['source_relative_path']}")
        elif payload.get("input_path"):
            lines.append(f"source_path: {payload['input_path']}")
        if payload.get("archived_packet_relative_path"):
            lines.append(f"archived_packet_relative_path: {payload['archived_packet_relative_path']}")
        elif payload.get("archived_packet_path"):
            lines.append(f"archived_packet_path: {payload['archived_packet_path']}")
        if payload.get("packet_checksum"):
            lines.append(f"packet_checksum: {payload['packet_checksum']}")
        if payload.get("error"):
            lines.append(f"error: {payload['error']}")
        if payload.get("next_action"):
            lines.append(f"next_action: {payload['next_action']}")
        warnings = payload.get("warnings") or []
        if warnings:
            lines.append("warnings:")
            lines.extend(f"  - {item}" for item in warnings)
        targets = payload.get("targets") or []
        if targets:
            lines.append("targets:")
            lines.extend(f"  - {item}" for item in targets)
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "question.queue":
        lines = [
            "ION Reviewer Queue",
            f"reviewer: {payload.get('reviewer') or 'ALL'}",
            f"domains: {', '.join(payload.get('domains', []))}",
            f"recorded: {'yes' if payload.get('recorded') else 'no'}",
            f"pending_total: {payload.get('pending_total', 0)}",
            f"recent_answer_total: {payload.get('recent_answer_total', 0)}",
        ]
        if payload.get("projection_id"):
            lines.append(f"projection_id: {payload['projection_id']}")
        pending = payload.get("pending_questions") or []
        if pending:
            lines.append("pending_questions:")
            lines.extend(
                f"  - {item['question_id']} [{item['priority']}] {item['needed_from']}: {item['question_text']}"
                for item in pending
            )
        recent = payload.get("recent_answers") or []
        if recent:
            lines.append("recent_answers:")
            lines.extend(
                f"  - {item['answer_id']} -> {item['question_id']} by {item['answered_by']}"
                for item in recent
            )
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "question.answer":
        lines = [
            "ION Question Answer",
            f"question_id: {payload['question_id']}",
            f"answer_id: {payload['answer_id']}",
            f"answered_by: {payload['answered_by']}",
            f"synthesized_work_unit: {'yes' if payload.get('synthesized_work_unit') else 'no'}",
            f"question_status: {payload['question']['status']}",
            f"work_unit_id: {payload['work_unit']['work_unit_id']}",
            f"resolution: {payload['resolution']}",
        ]
        evidence = payload.get("resolution_evidence") or []
        if evidence:
            lines.append("resolution_evidence:")
            lines.extend(f"  - {item}" for item in evidence)
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "packet.validate":
        from .packet_validation import PacketValidationMessage, PacketValidationResult

        result = PacketValidationResult(
            path=str(payload.get("path")),
            packet_type=payload.get("packet_type"),
            expected_type=payload.get("expected_type"),
            title=payload.get("title"),
            frontmatter_present=bool(payload.get("frontmatter_present")),
            valid=bool(payload.get("valid")),
            errors=tuple(PacketValidationMessage(**item) for item in payload.get("errors", [])),
            warnings=tuple(PacketValidationMessage(**item) for item in payload.get("warnings", [])),
            frontmatter={},
            sections_present=tuple(payload.get("sections_present", [])),
        )
        return render_packet_validation(result)
    if isinstance(payload, dict) and payload.get("command") == "packet.assess_takeover":
        from .packet_validation import PacketTakeoverAssessment

        assessment = PacketTakeoverAssessment(
            path=payload.get("path"),
            packet_type=str(payload.get("packet_type")),
            title=payload.get("title"),
            created_at=payload.get("packet_created_at"),
            status=payload.get("packet_status"),
            objective=str(payload.get("objective") or ""),
            scope_binding=payload.get("scope_binding"),
            target_executor=payload.get("target_executor"),
            required_reads=tuple(payload.get("required_reads", [])),
            next_action=payload.get("next_action"),
            expected_output=tuple(payload.get("expected_output", [])),
            warnings=tuple(payload.get("warnings", [])),
            valid=bool(payload.get("valid")),
        )
        return render_takeover_assessment(assessment)
    if isinstance(payload, dict) and payload.get("command") == "packet.render_takeover_role_session":
        lines = [
            "ION Packet Takeover Role Session",
            f"source_packet_path: {payload['source_packet_path']}",
            f"role: {payload['role']}",
            f"created_at: {payload['created_at']}",
            f"status: {payload['status']}",
            f"valid: {'yes' if payload['valid'] else 'no'}",
        ]
        if payload.get("output_relative_path"):
            lines.append(f"output_path: {payload['output_relative_path']}")
        elif payload.get("output_path"):
            lines.append(f"output_path: {payload['output_path']}")
        if payload.get("warnings"):
            lines.append("warnings:")
            lines.extend(f"  - {warning['code']}: {warning['message']}" for warning in payload["warnings"])
        if payload.get("content"):
            lines.extend(["", payload["content"]])
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "packet.record_takeover":
        lines = [
            "ION Packet Takeover Receipt",
            f"receipt_id: {payload['receipt_id']}",
            f"scope: {payload['scope_type']}:{payload['scope_ref']}",
            f"packet_type: {payload['packet_type']}",
            f"objective: {payload['objective']}",
            f"valid: {'yes' if payload['valid'] else 'no'}",
        ]
        if payload.get("packet_relative_path"):
            lines.append(f"packet_path: {payload['packet_relative_path']}")
        elif payload.get("packet_path"):
            lines.append(f"packet_path: {payload['packet_path']}")
        if payload.get("target_executor"):
            lines.append(f"target_executor: {payload['target_executor']}")
        warnings = payload.get("warnings") or []
        if warnings:
            lines.append("warnings:")
            lines.extend(f"  - {warning}" for warning in warnings)
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "equivalence.snapshot":
        if not payload:
            return "{}"
        if "receipt_id" not in payload:
            return "ION Manual/Automation Equivalence\nreceipt: NONE"
        lines = [
            "ION Manual/Automation Equivalence",
            f"receipt_id: {payload['receipt_id']}",
            f"scope: {payload['scope_type']}:{payload['scope_ref']}",
            f"candidate: {payload['candidate_title']}",
            f"automation_packet_type: {payload['automation_packet_type']}",
            f"manual_packet_type: {payload['manual_packet_type']}",
            f"equivalent: {'yes' if payload['equivalent'] else 'no'}",
        ]
        if payload.get("automation_packet_relative_path"):
            lines.append(f"automation_packet_path: {payload['automation_packet_relative_path']}")
        if payload.get("manual_packet_relative_path"):
            lines.append(f"manual_packet_path: {payload['manual_packet_relative_path']}")
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "equivalence.rehearse_horizon":
        lines = [
            "ION Manual/Automation Equivalence Rehearsal",
            f"receipt_id: {payload['receipt_id']}",
            f"scope: {payload['scope_type']}:{payload['scope_ref']}",
            f"candidate: {payload['candidate_title']}",
            f"automation_packet_type: {payload['automation_packet_type']}",
            f"manual_packet_type: {payload['manual_packet_type']}",
            f"equivalent: {'yes' if payload['equivalent'] else 'no'}",
        ]
        if payload.get("automation_packet_relative_path"):
            lines.append(f"automation_packet_path: {payload['automation_packet_relative_path']}")
        if payload.get("manual_packet_relative_path"):
            lines.append(f"manual_packet_path: {payload['manual_packet_relative_path']}")
        if payload.get("warnings"):
            lines.append("warnings:")
            lines.extend(f"  - {warning}" for warning in payload["warnings"])
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "schedule.materialize_resume_bundle":
        lines = [
            "ION Schedule Resume Bundle Materialization",
            f"receipt_id: {payload['receipt_id']}",
            f"scope: {payload['scope_type']}:{payload['scope_ref']}",
            f"materialization_action: {payload['materialization_action']}",
            f"active_cycle_stage: {payload['active_cycle_stage']}",
        ]
        if payload.get("continuation_bundle_root_relative_path"):
            lines.append(f"bundle_root: {payload['continuation_bundle_root_relative_path']}")
        if payload.get("packet_relative_path"):
            lines.append(f"packet_path: {payload['packet_relative_path']}")
        if payload.get("warnings"):
            lines.append("warnings:")
            lines.extend(f"  - {warning}" for warning in payload["warnings"])
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "continuation.snapshot":
        if not payload:
            return "{}"
        if "receipt_id" not in payload:
            return "ION Context-Perfect Continuation\nreceipt: NONE"
        lines = [
            "ION Context-Perfect Continuation",
            f"receipt_id: {payload['receipt_id']}",
            f"scope: {payload['scope_type']}:{payload['scope_ref']}",
            f"packet_type: {payload['packet_type']}",
            f"context_perfect: {'yes' if payload['context_perfect'] else 'no'}",
        ]
        if payload.get("bundle_root_relative_path"):
            lines.append(f"bundle_root: {payload['bundle_root_relative_path']}")
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "continuation.prove_packet":
        lines = [
            "ION Context-Perfect Continuation Proof",
            f"receipt_id: {payload['receipt_id']}",
            f"scope: {payload['scope_type']}:{payload['scope_ref']}",
            f"packet_type: {payload['packet_type']}",
            f"context_perfect: {'yes' if payload['context_perfect'] else 'no'}",
        ]
        if payload.get("packet_relative_path"):
            lines.append(f"packet_path: {payload['packet_relative_path']}")
        if payload.get("bundle_root_relative_path"):
            lines.append(f"bundle_root: {payload['bundle_root_relative_path']}")
        if payload.get("bundle_role_session_relative_path"):
            lines.append(f"role_session_path: {payload['bundle_role_session_relative_path']}")
        if payload.get("warnings"):
            lines.append("warnings:")
            lines.extend(f"  - {warning}" for warning in payload["warnings"])
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "allocator.snapshot_children":
        lines = [
            "ION Bounded Branch Allocation Snapshot",
            f"allocation_id: {payload['allocation_id']}",
            f"parent_scope: {payload['parent_scope_type']}:{payload['parent_scope_ref']}",
            f"selected_claims: {len(payload.get('selected_claims', []))}",
            f"deferred_claims: {len(payload.get('deferred_claims', []))}",
        ]
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "allocator.claim_children":
        lines = [
            "ION Bounded Branch Claims",
            f"allocation_id: {payload['allocation_id']}",
            f"parent_scope: {payload['parent_scope_type']}:{payload['parent_scope_ref']}",
            f"selected_claims: {len(payload.get('selected_claims', []))}",
            f"deferred_claims: {len(payload.get('deferred_claims', []))}",
        ]
        persisted = payload.get("persisted_receipt_ids") or []
        if persisted:
            lines.append("persisted_receipts:")
            lines.extend(f"  - {item}" for item in persisted)
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "allocator.snapshot_settlement":
        lines = [
            "ION Bounded Fan-In Settlement Snapshot",
            f"settlement_id: {payload['settlement_id']}",
            f"parent_scope: {payload['parent_scope_type']}:{payload['parent_scope_ref']}",
            f"outcome: {payload['outcome']}",
            f"branches: {len(payload.get('branches', []))}",
        ]
        if payload.get("conflict_paths"):
            lines.append("conflict_paths:")
            lines.extend(f"  - {item}" for item in payload["conflict_paths"])
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "allocator.settle_children":
        lines = [
            "ION Bounded Fan-In Settlement",
            f"receipt_id: {payload['receipt_id']}",
            f"settlement_id: {payload['settlement_id']}",
            f"parent_scope: {payload['parent_scope_type']}:{payload['parent_scope_ref']}",
            f"outcome: {payload['outcome']}",
            f"branches: {len(payload.get('branches', []))}",
        ]
        if payload.get("merge_proposal_id"):
            lines.append(f"merge_proposal_id: {payload['merge_proposal_id']}")
        if payload.get("conflict_paths"):
            lines.append("conflict_paths:")
            lines.extend(f"  - {item}" for item in payload["conflict_paths"])
        if payload.get("review_reasons"):
            lines.append("review_reasons:")
            lines.extend(f"  - {item}" for item in payload["review_reasons"])
        return "\n".join(lines)
    if isinstance(payload, dict) and payload.get("command") == "packet.enact_horizon":
        lines = [
            "ION Horizon Packet Enactment",
            f"scope: {payload['scope_type']}:{payload['scope_ref']}",
            f"status: {payload['status']}",
            f"valid: {'yes' if payload['valid'] else 'no'}",
            f"packet_type: {payload.get('packet_type') or 'NONE'}",
        ]
        if payload.get("candidate_title"):
            lines.append(f"candidate: {payload['candidate_title']}")
        if payload.get("receipt_id"):
            lines.append(f"receipt_id: {payload['receipt_id']}")
        if payload.get("packet_relative_path"):
            lines.append(f"packet_path: {payload['packet_relative_path']}")
        warnings = payload.get("warnings") or []
        if warnings:
            lines.append("warnings:")
            lines.extend(f"  - {warning}" for warning in warnings)
        if payload.get("content"):
            lines.extend(["", payload["content"]])
        return "\n".join(lines)
    return json.dumps(_to_jsonable(payload), indent=2, sort_keys=True)


def _relative_to_workspace(path: Path, workspace_root: Path) -> str | None:
    try:
        return str(path.relative_to(workspace_root))
    except ValueError:
        return None
