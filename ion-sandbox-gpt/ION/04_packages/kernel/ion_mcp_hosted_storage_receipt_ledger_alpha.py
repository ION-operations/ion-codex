"""V71 hosted MCP storage and receipt-ledger alpha for ION.

V71 defines the hosted storage substrate needed after V70's OAuth/HTTP
preview, without claiming public cloud certification, Kubernetes, or live
execution. The module is intentionally dependency-light and local-preview
friendly: it models account/workspace metadata, content-addressed state-root
snapshots, append-only receipt events, bundle/object references, and replay/export
contracts.

V71 law:
    Storage is not execution.
    A state root is content-addressed evidence, not a mutable live workspace.
    A receipt ledger is append-only evidence, not alternate execution authority.
    Hosted storage alpha may record mount/planning/dry-run receipts only.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from enum import Enum
import argparse
import hashlib
import json
import uuid
from pathlib import Path
from typing import Any, Iterable, Mapping


VERSION = "V71_HOSTED_MCP_STORAGE_AND_RECEIPT_LEDGER_ALPHA"
STORAGE_ALPHA_MODE = "HOSTED_STORAGE_RECEIPT_LEDGER_ALPHA_ONLY"
TOKEN_AUDIENCE = "ion-mcp-hosted-alpha"
FORBIDDEN_LIVE_RESOLUTION = "LIVE_EXECUTED"
ALLOWED_RESOLUTIONS = {"READ_ONLY", "DRY_RUN", "APPROVAL_REQUIRED", "REFUSED"}
BASELINE_SCOPES = {
    "ion.mount.basic",
    "ion.state.read",
    "ion.receipts.read",
    "ion.approvals.read",
    "ion.jobs.plan",
    "ion.jobs.execute.dry_run",
    "ion.bundles.export",
}
FORBIDDEN_TOOL_NAMES = {
    "ion.execute",
    "ion.job.execute_live",
    "ion.daemon.run",
    "ion.daemon.loop",
    "ion.shell.run",
    "ion.browser.mutate",
    "ion.provider.dispatch",
    "ion.secrets.read",
    "ion.secrets.write",
    "ion.governed_write.direct",
}
ALLOWED_EVENT_KINDS = {
    "MOUNT_RECEIPT",
    "STATE_ROOT_SNAPSHOT",
    "DRY_RUN_PLAN",
    "DRY_RUN_SUBMISSION",
    "APPROVAL_QUEUE_PROJECTION",
    "BUNDLE_EXPORT_PREVIEW",
    "ROLLBACK_PREVIEW",
    "REPLAY_PREVIEW",
}
FORBIDDEN_EVENT_KINDS = {
    "LIVE_EXECUTION",
    "SHELL_EXECUTION",
    "BROWSER_MUTATION",
    "PROVIDER_DISPATCH",
    "SECRET_READ",
    "SECRET_WRITE",
    "GOVERNED_WRITE_DIRECT",
    "DAEMON_LOOP_ACTIVATION",
}


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


def _safe_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def _hash_state_seed(workspace_id: str, branch_ref: str, policy_version: str) -> str:
    return "ion_state_" + _sha256_text(f"{workspace_id}|{branch_ref}|{policy_version}")[:32]


class HostedStorageAlphaStatus(StrEnum):
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"
    DEGRADED = "DEGRADED"


@dataclass(frozen=True)
class IonHostedAccount(KernelRecord):
    account_id: str
    subject_id: str
    organization_id: str | None = None
    account_role: str = "owner"
    created_at: str = field(default_factory=_utc_now)


@dataclass(frozen=True)
class IonHostedWorkspace(KernelRecord):
    workspace_id: str
    account_id: str
    display_name: str
    workspace_role: str = "operator"
    branch_ref: str = VERSION
    policy_version: str = VERSION
    created_at: str = field(default_factory=_utc_now)


@dataclass(frozen=True)
class IonHostedStateRoot(KernelRecord):
    state_root_id: str
    workspace_id: str
    branch_ref: str
    content_addressed: bool = True
    mutable_directly_by_mcp: bool = False
    created_at: str = field(default_factory=_utc_now)


@dataclass(frozen=True)
class IonHostedStorageObjectRef(KernelRecord):
    object_ref: str
    object_kind: str
    workspace_id: str
    content_hash: str
    byte_length: int
    created_at: str = field(default_factory=_utc_now)
    mutable_directly_by_mcp: bool = False
    contains_secret_material: bool = False
    production_object_storage_certified: bool = False


@dataclass(frozen=True)
class IonHostedStateRootSnapshot(KernelRecord):
    state_root_id: str
    workspace_id: str
    branch_ref: str
    snapshot_hash: str
    parent_state_root_id: str | None
    receipt_event_id: str
    object_ref: str
    created_at: str = field(default_factory=_utc_now)
    content_addressed: bool = True
    mutable_directly_by_mcp: bool = False
    kernel_truth_mutated: bool = False
    live_execution_authorized: bool = False


@dataclass(frozen=True)
class IonHostedReceiptEvent(KernelRecord):
    event_id: str
    workspace_id: str
    state_root_id: str
    event_kind: str
    execution_resolution: str
    subject_id: str
    tool_name: str
    payload_hash: str
    previous_event_hash: str | None
    event_hash: str
    created_at: str = field(default_factory=_utc_now)
    receipt_authority: str = STORAGE_ALPHA_MODE
    kernel_truth_mutated: bool = False
    live_execution_authorized: bool = False
    raw_secret_material_stored: bool = False


@dataclass(frozen=True)
class IonHostedBundlePreview(KernelRecord):
    bundle_id: str
    workspace_id: str
    state_root_id: str
    receipt_event_ids: tuple[str, ...]
    object_refs: tuple[str, ...]
    bundle_manifest_hash: str
    created_at: str = field(default_factory=_utc_now)
    export_is_preview_only: bool = True
    production_bundle_certified: bool = False
    live_execution_authorized: bool = False


@dataclass(frozen=True)
class IonHostedStorageLedgerState(KernelRecord):
    version: str
    account: IonHostedAccount
    workspace: IonHostedWorkspace
    state_root: IonHostedStateRoot
    object_refs: tuple[IonHostedStorageObjectRef, ...]
    receipt_events: tuple[IonHostedReceiptEvent, ...]
    snapshots: tuple[IonHostedStateRootSnapshot, ...]
    bundles: tuple[IonHostedBundlePreview, ...]
    latest_event_hash: str | None
    hosted_cloud_certified: bool = False
    public_endpoint_certified: bool = False
    kubernetes_certified: bool = False
    production_object_storage_certified: bool = False
    live_execution_authorized: bool = False
    kernel_truth_mutated: bool = False


@dataclass(frozen=True)
class IonHostedStorageBoundaryReport(KernelRecord):
    version: str
    status: HostedStorageAlphaStatus
    passed: bool
    created_at: str
    account_id: str
    workspace_id: str
    state_root_id: str
    object_ref_count: int
    receipt_event_count: int
    snapshot_count: int
    bundle_preview_count: int
    latest_event_hash: str | None
    allowed_resolutions: tuple[str, ...]
    forbidden_tool_count: int
    event_chain_verified: bool
    content_addressed_state_root_verified: bool
    append_only_ledger_verified: bool
    bundle_preview_verified: bool
    hosted_cloud_certified: bool
    public_endpoint_certified: bool
    kubernetes_certified: bool
    production_object_storage_certified: bool
    live_execution_authorized_seen: bool
    kernel_truth_mutation_seen: bool
    forbidden_resolution_seen: bool
    forbidden_event_seen: bool
    denied_reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = str(self.status)
        return data


class IonHostedStorageReceiptLedgerAlpha:
    """Append-only hosted-storage alpha ledger."""

    def __init__(self, account: IonHostedAccount, workspace: IonHostedWorkspace, state_root: IonHostedStateRoot):
        self.account = account
        self.workspace = workspace
        self.state_root = state_root
        self._objects: list[IonHostedStorageObjectRef] = []
        self._events: list[IonHostedReceiptEvent] = []
        self._snapshots: list[IonHostedStateRootSnapshot] = []
        self._bundles: list[IonHostedBundlePreview] = []

    @classmethod
    def fixture(cls) -> "IonHostedStorageReceiptLedgerAlpha":
        account = IonHostedAccount(account_id="acct_local_founder", subject_id="subj_braden_operator")
        workspace = IonHostedWorkspace(workspace_id="wsp_ion_production", account_id=account.account_id, display_name="ION Production")
        state_root = IonHostedStateRoot(
            state_root_id=_hash_state_seed(workspace.workspace_id, workspace.branch_ref, workspace.policy_version),
            workspace_id=workspace.workspace_id,
            branch_ref=workspace.branch_ref,
        )
        return cls(account=account, workspace=workspace, state_root=state_root)

    @property
    def latest_event_hash(self) -> str | None:
        return self._events[-1].event_hash if self._events else None

    def put_object_preview(self, *, object_kind: str, payload: Mapping[str, Any]) -> IonHostedStorageObjectRef:
        text = _canonical_json(dict(payload))
        content_hash = "sha256:" + _sha256_text(text)
        ref = IonHostedStorageObjectRef(
            object_ref=f"ion://object/{self.workspace.workspace_id}/{object_kind}/{content_hash[7:23]}",
            object_kind=object_kind,
            workspace_id=self.workspace.workspace_id,
            content_hash=content_hash,
            byte_length=len(text.encode("utf-8")),
        )
        self._objects.append(ref)
        return ref

    def append_receipt_event(self, *, event_kind: str, execution_resolution: str, tool_name: str, payload: Mapping[str, Any], subject_id: str | None = None) -> IonHostedReceiptEvent:
        if event_kind in FORBIDDEN_EVENT_KINDS:
            raise ValueError(f"forbidden event kind for V71 storage alpha: {event_kind}")
        if event_kind not in ALLOWED_EVENT_KINDS:
            raise ValueError(f"unknown event kind for V71 storage alpha: {event_kind}")
        if execution_resolution not in ALLOWED_RESOLUTIONS:
            raise ValueError(f"forbidden execution resolution for V71 storage alpha: {execution_resolution}")
        if tool_name in FORBIDDEN_TOOL_NAMES:
            raise ValueError(f"forbidden tool may not create V71 receipt event: {tool_name}")
        payload_hash = "sha256:" + _sha256_text(_canonical_json(dict(payload)))
        previous = self.latest_event_hash
        event_core = {
            "workspace_id": self.workspace.workspace_id,
            "state_root_id": self.state_root.state_root_id,
            "event_kind": event_kind,
            "execution_resolution": execution_resolution,
            "subject_id": subject_id or self.account.subject_id,
            "tool_name": tool_name,
            "payload_hash": payload_hash,
            "previous_event_hash": previous,
            "version": VERSION,
        }
        event_hash = "sha256:" + _sha256_text(_canonical_json(event_core))
        event = IonHostedReceiptEvent(
            event_id=_safe_id("receipt_evt"),
            workspace_id=self.workspace.workspace_id,
            state_root_id=self.state_root.state_root_id,
            event_kind=event_kind,
            execution_resolution=execution_resolution,
            subject_id=subject_id or self.account.subject_id,
            tool_name=tool_name,
            payload_hash=payload_hash,
            previous_event_hash=previous,
            event_hash=event_hash,
        )
        self._events.append(event)
        return event

    def snapshot_state_root_preview(self, *, payload: Mapping[str, Any], parent_state_root_id: str | None = None) -> IonHostedStateRootSnapshot:
        obj = self.put_object_preview(object_kind="state-root-snapshot", payload=payload)
        event = self.append_receipt_event(
            event_kind="STATE_ROOT_SNAPSHOT",
            execution_resolution="READ_ONLY",
            tool_name="ion.state.snapshot_preview",
            payload={"object_ref": obj.object_ref, "content_hash": obj.content_hash, "parent_state_root_id": parent_state_root_id},
        )
        snapshot_id = "ion_state_snapshot_" + _sha256_text(obj.content_hash + event.event_hash)[:32]
        snapshot = IonHostedStateRootSnapshot(
            state_root_id=snapshot_id,
            workspace_id=self.workspace.workspace_id,
            branch_ref=self.workspace.branch_ref,
            snapshot_hash=obj.content_hash,
            parent_state_root_id=parent_state_root_id,
            receipt_event_id=event.event_id,
            object_ref=obj.object_ref,
        )
        self._snapshots.append(snapshot)
        return snapshot

    def create_bundle_export_preview(self) -> IonHostedBundlePreview:
        manifest = {
            "workspace_id": self.workspace.workspace_id,
            "state_root_id": self.state_root.state_root_id,
            "receipt_event_ids": [event.event_id for event in self._events],
            "object_refs": [obj.object_ref for obj in self._objects],
            "version": VERSION,
            "export_is_preview_only": True,
        }
        manifest_hash = "sha256:" + _sha256_text(_canonical_json(manifest))
        self.append_receipt_event(
            event_kind="BUNDLE_EXPORT_PREVIEW",
            execution_resolution="DRY_RUN",
            tool_name="ion.bundle.export_preview",
            payload={"bundle_manifest_hash": manifest_hash},
        )
        bundle = IonHostedBundlePreview(
            bundle_id="ion_bundle_preview_" + manifest_hash[7:23],
            workspace_id=self.workspace.workspace_id,
            state_root_id=self.state_root.state_root_id,
            receipt_event_ids=tuple(event.event_id for event in self._events),
            object_refs=tuple(obj.object_ref for obj in self._objects),
            bundle_manifest_hash=manifest_hash,
        )
        self._bundles.append(bundle)
        return bundle

    def state(self) -> IonHostedStorageLedgerState:
        return IonHostedStorageLedgerState(
            version=VERSION,
            account=self.account,
            workspace=self.workspace,
            state_root=self.state_root,
            object_refs=tuple(self._objects),
            receipt_events=tuple(self._events),
            snapshots=tuple(self._snapshots),
            bundles=tuple(self._bundles),
            latest_event_hash=self.latest_event_hash,
        )


def verify_event_chain(events: Iterable[IonHostedReceiptEvent]) -> bool:
    previous: str | None = None
    for event in events:
        if event.previous_event_hash != previous:
            return False
        core = {
            "workspace_id": event.workspace_id,
            "state_root_id": event.state_root_id,
            "event_kind": event.event_kind,
            "execution_resolution": event.execution_resolution,
            "subject_id": event.subject_id,
            "tool_name": event.tool_name,
            "payload_hash": event.payload_hash,
            "previous_event_hash": event.previous_event_hash,
            "version": VERSION,
        }
        if event.event_hash != "sha256:" + _sha256_text(_canonical_json(core)):
            return False
        previous = event.event_hash
    return True


def build_storage_alpha_fixture_report() -> IonHostedStorageBoundaryReport:
    ledger = IonHostedStorageReceiptLedgerAlpha.fixture()
    ledger.append_receipt_event(
        event_kind="MOUNT_RECEIPT",
        execution_resolution="READ_ONLY",
        tool_name="ion.mount",
        payload={"audience": TOKEN_AUDIENCE, "scopes": sorted(BASELINE_SCOPES), "mode": "dry_run"},
    )
    ledger.append_receipt_event(
        event_kind="DRY_RUN_PLAN",
        execution_resolution="DRY_RUN",
        tool_name="ion.job.plan",
        payload={"task": "hosted storage alpha dry-run plan", "live_execution": False},
    )
    ledger.snapshot_state_root_preview(
        payload={"workspace_id": ledger.workspace.workspace_id, "branch_ref": ledger.workspace.branch_ref, "state_root_id": ledger.state_root.state_root_id, "storage_alpha_mode": STORAGE_ALPHA_MODE}
    )
    ledger.create_bundle_export_preview()
    state = ledger.state()
    events = state.receipt_events
    denied: list[str] = []
    forbidden_resolution_seen = any(event.execution_resolution not in ALLOWED_RESOLUTIONS for event in events)
    forbidden_event_seen = any(event.event_kind in FORBIDDEN_EVENT_KINDS for event in events)
    live_execution_authorized_seen = any(event.live_execution_authorized for event in events) or state.live_execution_authorized
    kernel_truth_mutation_seen = any(event.kernel_truth_mutated for event in events) or state.kernel_truth_mutated
    event_chain_verified = verify_event_chain(events)
    content_addressed_state_root_verified = all(s.content_addressed and s.snapshot_hash.startswith("sha256:") for s in state.snapshots)
    append_only_ledger_verified = event_chain_verified and all(event.previous_event_hash == (events[i-1].event_hash if i else None) for i, event in enumerate(events))
    bundle_preview_verified = bool(state.bundles) and all(bundle.export_is_preview_only and not bundle.production_bundle_certified for bundle in state.bundles)
    for condition, reason in [
        (forbidden_resolution_seen, "forbidden execution resolution observed"),
        (forbidden_event_seen, "forbidden event kind observed"),
        (live_execution_authorized_seen, "live execution authorization observed"),
        (kernel_truth_mutation_seen, "kernel truth mutation observed"),
        (not event_chain_verified, "receipt event chain failed verification"),
        (not content_addressed_state_root_verified, "state-root snapshot was not content-addressed"),
        (not bundle_preview_verified, "bundle export preview invariant failed"),
    ]:
        if condition:
            denied.append(reason)
    passed = not denied
    return IonHostedStorageBoundaryReport(
        version=VERSION,
        status=HostedStorageAlphaStatus.ACCEPTED if passed else HostedStorageAlphaStatus.REFUSED,
        passed=passed,
        created_at=_utc_now(),
        account_id=state.account.account_id,
        workspace_id=state.workspace.workspace_id,
        state_root_id=state.state_root.state_root_id,
        object_ref_count=len(state.object_refs),
        receipt_event_count=len(state.receipt_events),
        snapshot_count=len(state.snapshots),
        bundle_preview_count=len(state.bundles),
        latest_event_hash=state.latest_event_hash,
        allowed_resolutions=tuple(sorted(ALLOWED_RESOLUTIONS)),
        forbidden_tool_count=len(FORBIDDEN_TOOL_NAMES),
        event_chain_verified=event_chain_verified,
        content_addressed_state_root_verified=content_addressed_state_root_verified,
        append_only_ledger_verified=append_only_ledger_verified,
        bundle_preview_verified=bundle_preview_verified,
        hosted_cloud_certified=False,
        public_endpoint_certified=False,
        kubernetes_certified=False,
        production_object_storage_certified=False,
        live_execution_authorized_seen=live_execution_authorized_seen,
        kernel_truth_mutation_seen=kernel_truth_mutation_seen,
        forbidden_resolution_seen=forbidden_resolution_seen,
        forbidden_event_seen=forbidden_event_seen,
        denied_reasons=tuple(denied),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run V71 hosted storage/receipt-ledger alpha boundary report.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    parser.add_argument("--output", type=Path, help="Optional path to write JSON report.")
    args = parser.parse_args(argv)
    report = build_storage_alpha_fixture_report()
    text = json.dumps(report.to_dict(), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    if args.json:
        print(text)
    else:
        print(f"{VERSION}: {'PASSED' if report.passed else 'FAILED'}")
        print(f"receipt_events={report.receipt_event_count} snapshots={report.snapshot_count} bundles={report.bundle_preview_count}")
    return 0 if report.passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
