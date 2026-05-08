"""V72 hosted MCP bundle import/export/replay alpha for ION.

V72 builds on V71's hosted storage and append-only receipt-ledger substrate.
It defines how an ION workspace state can be exported into a deterministic
bundle preview, imported back as evidence, replayed as a non-mutating event
plan, and refused when bundle material is tampered or attempts to imply live
execution.

V72 law:
    Bundle import/export/replay is evidence handling, not execution.
    An imported bundle is untrusted until schema, hashes, state root, workspace,
    receipts, and replay plan all validate.
    Replay is preview-only in V72 and may not mutate kernel truth.
    No bundle may authorize LIVE_EXECUTED or direct governed-write authority.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Iterable

from .ion_mcp_hosted_storage_receipt_ledger_alpha import (
    ALLOWED_RESOLUTIONS,
    FORBIDDEN_EVENT_KINDS,
    FORBIDDEN_TOOL_NAMES,
    FORBIDDEN_LIVE_RESOLUTION,
    IonHostedStorageReceiptLedgerAlpha,
)

VERSION = "V72_HOSTED_MCP_BUNDLE_IMPORT_EXPORT_AND_REPLAY_ALPHA"
BUNDLE_ALPHA_MODE = "HOSTED_BUNDLE_IMPORT_EXPORT_REPLAY_ALPHA_ONLY"
BUNDLE_FORMAT_VERSION = "ion.hosted.bundle.alpha.v1"
ALLOWED_REPLAY_ACTIONS = {"READ_EVENT", "VERIFY_EVENT", "PROJECT_STATE_ROOT", "PROJECT_BUNDLE", "QUEUE_APPROVAL_PREVIEW", "REFUSE"}
FORBIDDEN_REPLAY_ACTIONS = {"EXECUTE", "SHELL_RUN", "BROWSER_MUTATE", "PROVIDER_DISPATCH", "GOVERNED_WRITE_DIRECT", "DAEMON_LOOP"}


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return self.value


class KernelRecord:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_json(value: Mapping[str, Any] | list[Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _bundle_hash(manifest: Mapping[str, Any]) -> str:
    return "sha256:" + _sha256_text(_canonical_json(dict(manifest)))


class BundleAlphaStatus(StrEnum):
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"
    DEGRADED = "DEGRADED"


@dataclass(frozen=True)
class IonHostedBundleManifest(KernelRecord):
    format_version: str
    bundle_id: str
    workspace_id: str
    state_root_id: str
    branch_ref: str
    exported_at: str
    event_hashes: tuple[str, ...]
    receipt_event_ids: tuple[str, ...]
    object_refs: tuple[str, ...]
    snapshot_hashes: tuple[str, ...]
    source_latest_event_hash: str | None
    export_is_preview_only: bool = True
    production_bundle_certified: bool = False
    live_execution_authorized: bool = False
    kernel_truth_mutated: bool = False


@dataclass(frozen=True)
class IonHostedBundleEnvelope(KernelRecord):
    manifest: IonHostedBundleManifest
    manifest_hash: str
    receipt_events: tuple[dict[str, Any], ...]
    snapshots: tuple[dict[str, Any], ...]
    object_refs: tuple[dict[str, Any], ...]
    exported_by_tool: str = "ion.bundle.export_preview"
    import_requires_validation: bool = True
    replay_is_preview_only: bool = True
    live_execution_authorized: bool = False
    kernel_truth_mutated: bool = False


@dataclass(frozen=True)
class IonHostedBundleImportResult(KernelRecord):
    status: BundleAlphaStatus
    accepted: bool
    workspace_id: str | None
    state_root_id: str | None
    manifest_hash: str | None
    event_chain_verified: bool
    manifest_hash_verified: bool
    workspace_binding_verified: bool
    state_root_binding_verified: bool
    preview_only_verified: bool
    forbidden_resolution_seen: bool
    forbidden_event_seen: bool
    forbidden_tool_seen: bool
    live_execution_authorized_seen: bool
    kernel_truth_mutation_seen: bool
    denied_reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = str(self.status)
        return data


@dataclass(frozen=True)
class IonHostedReplayStep(KernelRecord):
    step_index: int
    action: str
    event_id: str | None
    event_kind: str | None
    execution_resolution: str
    receipt_hash: str | None
    kernel_truth_mutated: bool = False
    live_execution_authorized: bool = False
    requires_operator_approval: bool = False


@dataclass(frozen=True)
class IonHostedReplayPlan(KernelRecord):
    replay_plan_id: str
    workspace_id: str
    state_root_id: str
    manifest_hash: str
    steps: tuple[IonHostedReplayStep, ...]
    replay_is_preview_only: bool = True
    replay_committed: bool = False
    kernel_truth_mutated: bool = False
    live_execution_authorized: bool = False


@dataclass(frozen=True)
class IonHostedBundleReplayAlphaReport(KernelRecord):
    version: str
    status: BundleAlphaStatus
    passed: bool
    created_at: str
    bundle_id: str
    workspace_id: str
    state_root_id: str
    manifest_hash: str
    import_accepted: bool
    replay_step_count: int
    export_preview_verified: bool
    import_validation_verified: bool
    replay_preview_verified: bool
    tamper_refusal_verified: bool
    allowed_resolutions: tuple[str, ...]
    allowed_replay_actions: tuple[str, ...]
    hosted_cloud_certified: bool
    public_endpoint_certified: bool
    kubernetes_certified: bool
    production_bundle_certified: bool
    live_execution_authorized_seen: bool
    kernel_truth_mutation_seen: bool
    forbidden_resolution_seen: bool
    forbidden_event_seen: bool
    forbidden_replay_action_seen: bool
    denied_reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = str(self.status)
        return data


def build_fixture_ledger() -> IonHostedStorageReceiptLedgerAlpha:
    ledger = IonHostedStorageReceiptLedgerAlpha.fixture()
    ledger.append_receipt_event(
        event_kind="MOUNT_RECEIPT",
        execution_resolution="READ_ONLY",
        tool_name="ion.mount",
        payload={"mode": "dry_run", "version": VERSION},
    )
    ledger.append_receipt_event(
        event_kind="DRY_RUN_PLAN",
        execution_resolution="DRY_RUN",
        tool_name="ion.job.plan",
        payload={"task": "V72 bundle import/export/replay alpha plan", "live_execution": False},
    )
    ledger.snapshot_state_root_preview(
        payload={"workspace_id": ledger.workspace.workspace_id, "state_root_id": ledger.state_root.state_root_id, "bundle_alpha_mode": BUNDLE_ALPHA_MODE}
    )
    ledger.append_receipt_event(
        event_kind="REPLAY_PREVIEW",
        execution_resolution="DRY_RUN",
        tool_name="ion.replay.preview",
        payload={"preview_only": True, "kernel_truth_mutated": False},
    )
    return ledger


def export_bundle_preview(ledger: IonHostedStorageReceiptLedgerAlpha) -> IonHostedBundleEnvelope:
    state = ledger.state()
    manifest_core = {
        "format_version": BUNDLE_FORMAT_VERSION,
        "workspace_id": state.workspace.workspace_id,
        "state_root_id": state.state_root.state_root_id,
        "branch_ref": state.workspace.branch_ref,
        "event_hashes": [event.event_hash for event in state.receipt_events],
        "receipt_event_ids": [event.event_id for event in state.receipt_events],
        "object_refs": [obj.object_ref for obj in state.object_refs],
        "snapshot_hashes": [snap.snapshot_hash for snap in state.snapshots],
        "source_latest_event_hash": state.latest_event_hash,
        "export_is_preview_only": True,
        "production_bundle_certified": False,
        "live_execution_authorized": False,
        "kernel_truth_mutated": False,
    }
    mhash = _bundle_hash(manifest_core)
    bundle_id = "ion_bundle_alpha_" + mhash[7:23]
    manifest = IonHostedBundleManifest(
        format_version=BUNDLE_FORMAT_VERSION,
        bundle_id=bundle_id,
        workspace_id=state.workspace.workspace_id,
        state_root_id=state.state_root.state_root_id,
        branch_ref=state.workspace.branch_ref,
        exported_at=_utc_now(),
        event_hashes=tuple(event.event_hash for event in state.receipt_events),
        receipt_event_ids=tuple(event.event_id for event in state.receipt_events),
        object_refs=tuple(obj.object_ref for obj in state.object_refs),
        snapshot_hashes=tuple(snap.snapshot_hash for snap in state.snapshots),
        source_latest_event_hash=state.latest_event_hash,
    )
    return IonHostedBundleEnvelope(
        manifest=manifest,
        manifest_hash=mhash,
        receipt_events=tuple(event.to_dict() for event in state.receipt_events),
        snapshots=tuple(snap.to_dict() for snap in state.snapshots),
        object_refs=tuple(obj.to_dict() for obj in state.object_refs),
    )


def _event_dicts_have_chain(event_dicts: Iterable[Mapping[str, Any]]) -> bool:
    previous = None
    for event in event_dicts:
        if event.get("previous_event_hash") != previous:
            return False
        previous = event.get("event_hash")
    return True


def validate_bundle_import(envelope: IonHostedBundleEnvelope | Mapping[str, Any], *, expected_workspace_id: str | None = None, expected_state_root_id: str | None = None) -> IonHostedBundleImportResult:
    data = envelope.to_dict() if hasattr(envelope, "to_dict") else dict(envelope)
    manifest = data.get("manifest", {})
    events = list(data.get("receipt_events", []))
    mhash = data.get("manifest_hash")
    denied: list[str] = []
    manifest_core = {
        "format_version": manifest.get("format_version"),
        "workspace_id": manifest.get("workspace_id"),
        "state_root_id": manifest.get("state_root_id"),
        "branch_ref": manifest.get("branch_ref"),
        "event_hashes": list(manifest.get("event_hashes", [])),
        "receipt_event_ids": list(manifest.get("receipt_event_ids", [])),
        "object_refs": list(manifest.get("object_refs", [])),
        "snapshot_hashes": list(manifest.get("snapshot_hashes", [])),
        "source_latest_event_hash": manifest.get("source_latest_event_hash"),
        "export_is_preview_only": manifest.get("export_is_preview_only"),
        "production_bundle_certified": manifest.get("production_bundle_certified"),
        "live_execution_authorized": manifest.get("live_execution_authorized"),
        "kernel_truth_mutated": manifest.get("kernel_truth_mutated"),
    }
    manifest_hash_verified = bool(mhash) and _bundle_hash(manifest_core) == mhash
    event_chain_verified = _event_dicts_have_chain(events)
    workspace_binding_verified = expected_workspace_id is None or manifest.get("workspace_id") == expected_workspace_id
    state_root_binding_verified = expected_state_root_id is None or manifest.get("state_root_id") == expected_state_root_id
    preview_only_verified = bool(manifest.get("export_is_preview_only")) and not bool(manifest.get("production_bundle_certified"))
    forbidden_resolution_seen = any(event.get("execution_resolution") not in ALLOWED_RESOLUTIONS for event in events)
    forbidden_event_seen = any(event.get("event_kind") in FORBIDDEN_EVENT_KINDS for event in events)
    forbidden_tool_seen = any(event.get("tool_name") in FORBIDDEN_TOOL_NAMES for event in events)
    live_execution_authorized_seen = bool(manifest.get("live_execution_authorized")) or any(bool(event.get("live_execution_authorized")) for event in events)
    kernel_truth_mutation_seen = bool(manifest.get("kernel_truth_mutated")) or any(bool(event.get("kernel_truth_mutated")) for event in events)
    for condition, reason in [
        (not manifest_hash_verified, "bundle manifest hash failed validation"),
        (not event_chain_verified, "receipt event chain failed validation"),
        (not workspace_binding_verified, "workspace binding mismatch"),
        (not state_root_binding_verified, "state-root binding mismatch"),
        (not preview_only_verified, "bundle is not preview-only"),
        (forbidden_resolution_seen, "forbidden execution resolution observed"),
        (forbidden_event_seen, "forbidden event kind observed"),
        (forbidden_tool_seen, "forbidden tool observed in imported bundle"),
        (live_execution_authorized_seen, "live execution authorization observed"),
        (kernel_truth_mutation_seen, "kernel truth mutation observed"),
    ]:
        if condition:
            denied.append(reason)
    accepted = not denied
    return IonHostedBundleImportResult(
        status=BundleAlphaStatus.ACCEPTED if accepted else BundleAlphaStatus.REFUSED,
        accepted=accepted,
        workspace_id=manifest.get("workspace_id"),
        state_root_id=manifest.get("state_root_id"),
        manifest_hash=mhash,
        event_chain_verified=event_chain_verified,
        manifest_hash_verified=manifest_hash_verified,
        workspace_binding_verified=workspace_binding_verified,
        state_root_binding_verified=state_root_binding_verified,
        preview_only_verified=preview_only_verified,
        forbidden_resolution_seen=forbidden_resolution_seen,
        forbidden_event_seen=forbidden_event_seen,
        forbidden_tool_seen=forbidden_tool_seen,
        live_execution_authorized_seen=live_execution_authorized_seen,
        kernel_truth_mutation_seen=kernel_truth_mutation_seen,
        denied_reasons=tuple(denied),
    )


def build_replay_plan(envelope: IonHostedBundleEnvelope | Mapping[str, Any]) -> IonHostedReplayPlan:
    data = envelope.to_dict() if hasattr(envelope, "to_dict") else dict(envelope)
    manifest = data.get("manifest", {})
    steps: list[IonHostedReplayStep] = []
    for idx, event in enumerate(data.get("receipt_events", [])):
        kind = event.get("event_kind")
        resolution = event.get("execution_resolution")
        action = "VERIFY_EVENT" if resolution in ALLOWED_RESOLUTIONS and kind not in FORBIDDEN_EVENT_KINDS else "REFUSE"
        if kind in {"APPROVAL_QUEUE_PROJECTION"}:
            action = "QUEUE_APPROVAL_PREVIEW"
        steps.append(IonHostedReplayStep(
            step_index=idx,
            action=action,
            event_id=event.get("event_id"),
            event_kind=kind,
            execution_resolution=resolution or "REFUSED",
            receipt_hash=event.get("event_hash"),
            requires_operator_approval=kind == "APPROVAL_QUEUE_PROJECTION",
        ))
    steps.append(IonHostedReplayStep(
        step_index=len(steps),
        action="PROJECT_BUNDLE",
        event_id=None,
        event_kind="BUNDLE_EXPORT_PREVIEW",
        execution_resolution="DRY_RUN",
        receipt_hash=data.get("manifest_hash"),
    ))
    return IonHostedReplayPlan(
        replay_plan_id="ion_replay_alpha_" + _sha256_text(str(data.get("manifest_hash")))[:16],
        workspace_id=manifest.get("workspace_id"),
        state_root_id=manifest.get("state_root_id"),
        manifest_hash=data.get("manifest_hash"),
        steps=tuple(steps),
    )


def tamper_bundle(envelope: IonHostedBundleEnvelope) -> dict[str, Any]:
    data = copy.deepcopy(envelope.to_dict())
    data["manifest"]["live_execution_authorized"] = True
    if data.get("receipt_events"):
        data["receipt_events"][0]["execution_resolution"] = FORBIDDEN_LIVE_RESOLUTION
        data["receipt_events"][0]["event_kind"] = "LIVE_EXECUTION"
    return data


def build_bundle_replay_alpha_report() -> IonHostedBundleReplayAlphaReport:
    ledger = build_fixture_ledger()
    envelope = export_bundle_preview(ledger)
    import_result = validate_bundle_import(envelope, expected_workspace_id=ledger.workspace.workspace_id, expected_state_root_id=ledger.state_root.state_root_id)
    replay_plan = build_replay_plan(envelope)
    tampered = tamper_bundle(envelope)
    tamper_result = validate_bundle_import(tampered, expected_workspace_id=ledger.workspace.workspace_id, expected_state_root_id=ledger.state_root.state_root_id)
    forbidden_replay_action_seen = any(step.action in FORBIDDEN_REPLAY_ACTIONS for step in replay_plan.steps)
    live_execution_authorized_seen = replay_plan.live_execution_authorized or import_result.live_execution_authorized_seen
    kernel_truth_mutation_seen = replay_plan.kernel_truth_mutated or import_result.kernel_truth_mutation_seen
    forbidden_resolution_seen = import_result.forbidden_resolution_seen
    forbidden_event_seen = import_result.forbidden_event_seen
    export_preview_verified = envelope.manifest.export_is_preview_only and envelope.replay_is_preview_only and not envelope.manifest.production_bundle_certified
    import_validation_verified = import_result.accepted and import_result.manifest_hash_verified and import_result.event_chain_verified
    replay_preview_verified = replay_plan.replay_is_preview_only and not replay_plan.replay_committed and not replay_plan.kernel_truth_mutated
    tamper_refusal_verified = not tamper_result.accepted and bool(tamper_result.denied_reasons)
    denied: list[str] = []
    for condition, reason in [
        (not export_preview_verified, "export preview invariant failed"),
        (not import_validation_verified, "import validation invariant failed"),
        (not replay_preview_verified, "replay preview invariant failed"),
        (not tamper_refusal_verified, "tampered bundle was not refused"),
        (live_execution_authorized_seen, "live execution authorization observed"),
        (kernel_truth_mutation_seen, "kernel truth mutation observed"),
        (forbidden_resolution_seen, "forbidden resolution observed"),
        (forbidden_event_seen, "forbidden event observed"),
        (forbidden_replay_action_seen, "forbidden replay action observed"),
    ]:
        if condition:
            denied.append(reason)
    passed = not denied
    return IonHostedBundleReplayAlphaReport(
        version=VERSION,
        status=BundleAlphaStatus.ACCEPTED if passed else BundleAlphaStatus.REFUSED,
        passed=passed,
        created_at=_utc_now(),
        bundle_id=envelope.manifest.bundle_id,
        workspace_id=envelope.manifest.workspace_id,
        state_root_id=envelope.manifest.state_root_id,
        manifest_hash=envelope.manifest_hash,
        import_accepted=import_result.accepted,
        replay_step_count=len(replay_plan.steps),
        export_preview_verified=export_preview_verified,
        import_validation_verified=import_validation_verified,
        replay_preview_verified=replay_preview_verified,
        tamper_refusal_verified=tamper_refusal_verified,
        allowed_resolutions=tuple(sorted(ALLOWED_RESOLUTIONS)),
        allowed_replay_actions=tuple(sorted(ALLOWED_REPLAY_ACTIONS)),
        hosted_cloud_certified=False,
        public_endpoint_certified=False,
        kubernetes_certified=False,
        production_bundle_certified=False,
        live_execution_authorized_seen=live_execution_authorized_seen,
        kernel_truth_mutation_seen=kernel_truth_mutation_seen,
        forbidden_resolution_seen=forbidden_resolution_seen,
        forbidden_event_seen=forbidden_event_seen,
        forbidden_replay_action_seen=forbidden_replay_action_seen,
        denied_reasons=tuple(denied),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run V72 hosted bundle import/export/replay alpha boundary report.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    parser.add_argument("--output", type=Path, help="Optional path to write JSON report.")
    args = parser.parse_args(argv)
    report = build_bundle_replay_alpha_report()
    text = json.dumps(report.to_dict(), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    if args.json:
        print(text)
    else:
        print(f"{VERSION}: {'PASSED' if report.passed else 'FAILED'}")
        print(f"bundle={report.bundle_id} replay_steps={report.replay_step_count} tamper_refused={report.tamper_refusal_verified}")
    return 0 if report.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
