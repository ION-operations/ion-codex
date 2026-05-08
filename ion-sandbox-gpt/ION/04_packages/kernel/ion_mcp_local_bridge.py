"""V64 local MCP bridge surface for ION.

This module is intentionally a bridge surface, not a new authority center.

It provides:
- a dependency-free tool adapter shaped for MCP wrapping;
- a minimal JSON-RPC stdio shim for local experimentation;
- read-only and dry-run tool calls only;
- runtime-session receipts through ION's existing RuntimeSessionStore;
- explicit refusal of live execution, provider dispatch, browser mutation,
  credential access, and canonical write authority.

V64 law:
    MCP may mount ION and request dry-run projections.
    MCP may not execute ION.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
import sys
import uuid
from typing import Any, Iterable, Mapping

from .api_runtime_entry import ApiRuntimeEntryGateway, ApiRuntimeEntryStatus
from .joc_operator_approval_queue_view_model import (
    FORBIDDEN_CAPABILITIES as V62_FORBIDDEN_CAPABILITIES,
    build_fixture_operator_approval_input,
    build_operator_approval_queue_view_model,
    validate_operator_approval_queue_view_model,
)
from .model import KernelRecord, StrEnum
from .runtime_session_store import (
    RuntimeSessionEvent,
    RuntimeSessionStore,
    SessionQueueItemStatus,
)


VERSION = "V64_LOCAL_MCP_BRIDGE_TO_ION_KERNEL_AND_SUPERVISED_DAEMON"
PROTOCOL_VERSION = "2025-03-26"

READ_ONLY_TOOLS = {
    "ion.mount",
    "ion.status",
    "ion.boot_packet",
    "ion.horizon.current",
    "ion.receipts.list",
    "ion.approvals.list",
    "ion.tools.list",
}
DRY_RUN_TOOLS = {
    "ion.job.plan",
    "ion.job.submit_dry_run",
    "ion.daemon.dry_run_step",
    "ion.bundle.export_preview",
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
ALLOWED_RESOLUTIONS = {"READ_ONLY", "DRY_RUN", "APPROVAL_REQUIRED", "REFUSED"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_name(value: str, fallback: str) -> str:
    value = "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in (value or "").strip())
    value = value.strip(".-_")
    return value[:96] or fallback


def _path_exists(root: Path, relative: str) -> bool:
    return (root / relative).exists()


def _read_text_if_exists(path: Path, max_chars: int = 8000) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]"
    return text


class IonMcpExecutionResolution(StrEnum):
    READ_ONLY = "READ_ONLY"
    DRY_RUN = "DRY_RUN"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    REFUSED = "REFUSED"


class IonMcpToolStatus(StrEnum):
    OK = "OK"
    BLOCKED = "BLOCKED"
    ERROR = "ERROR"


@dataclass(frozen=True)
class IonMcpBridgeReceipt(KernelRecord):
    receipt_id: str
    created_at: str
    tool_name: str
    execution_resolution: IonMcpExecutionResolution
    session_id: str | None
    detail: str
    witness_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class IonMcpMountRequest(KernelRecord):
    client_name: str = "local-mcp-client"
    client_version: str | None = None
    transport: str = "stdio"
    requested_mode: str = "dry_run"
    requested_scopes: tuple[str, ...] = (
        "ion.mount.basic",
        "ion.state.read",
        "ion.receipts.read",
        "ion.approvals.read",
        "ion.jobs.plan",
        "ion.jobs.execute.dry_run",
        "ion.bundles.export",
    )
    workspace_id: str = "local-founder"
    session_id: str | None = None
    create_session_if_missing: bool = True
    root_authority_ref: str = "ION/00_BOOTSTRAP/V64_LOCAL_MCP_BRIDGE_LOCK.md"
    context_version: str = VERSION
    context_ref: str = "ION/02_architecture/ION_LOCAL_MCP_BRIDGE_TO_KERNEL_AND_DAEMON_PROTOCOL.md"


@dataclass(frozen=True)
class IonMcpMountedSession(KernelRecord):
    version: str
    session_id: str
    workspace_id: str
    client_name: str
    transport: str
    execution_mode: str
    granted_scopes: tuple[str, ...]
    denied_scopes: tuple[str, ...]
    allowed_tools: tuple[str, ...]
    blocked_tools: tuple[str, ...]
    state_store_root: str
    receipt_refs: tuple[str, ...] = ()
    created_at: str = field(default_factory=_utc_now)
    live_execution_authorized: bool = False
    provider_dispatch_authorized: bool = False
    browser_mutation_authorized: bool = False
    credential_access_authorized: bool = False
    canonical_write_authorized: bool = False


@dataclass(frozen=True)
class IonMcpToolResult(KernelRecord):
    version: str
    tool_name: str
    status: IonMcpToolStatus
    execution_resolution: IonMcpExecutionResolution
    session_id: str | None
    payload: Mapping[str, Any]
    blocked_capabilities: Mapping[str, bool]
    receipt_refs: tuple[str, ...] = ()
    next_required_action: str | None = None
    kernel_truth_mutated: bool = False
    live_execution_authorized: bool = False
    external_model_call_authorized: bool = False
    browser_mutation_authorized: bool = False
    credential_access_authorized: bool = False
    canonical_write_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = str(self.status)
        data["execution_resolution"] = str(self.execution_resolution)
        return data


def _blocked_capabilities(extra: Mapping[str, bool] | None = None) -> dict[str, bool]:
    blocked = {
        "live_execution": False,
        "external_model_dispatch": False,
        "browser_session_mutation": False,
        "credential_access": False,
        "canonical_graph_write": False,
        "direct_kernel_truth_mutation": False,
        "unrestricted_daemon_loop": False,
        "provider_api_call": False,
        "paid_cloud_launch": False,
    }
    for key, value in V62_FORBIDDEN_CAPABILITIES.items():
        blocked.setdefault(key, value)
    if extra:
        blocked.update(extra)
    return blocked


class IonMcpLocalBridge:
    """Local, dry-run MCP-facing bridge for ION.

    The bridge writes only receipts/session queue artifacts through RuntimeSessionStore.
    It does not modify canonical doctrine, execute shell commands, call external providers,
    mutate browsers, read credentials, or run the daemon loop.
    """

    def __init__(self, ion_root: str | Path, state_store_root: str | Path | None = None) -> None:
        self.ion_root = Path(ion_root).resolve()
        if self.ion_root.name != "ION" and (self.ion_root / "ION").exists():
            self.ion_root = (self.ion_root / "ION").resolve()
        self.state_store_root = Path(state_store_root).resolve() if state_store_root else (
            self.ion_root / "05_context" / "runtime_state" / "v64_local_mcp_bridge"
        )
        self.session_store = RuntimeSessionStore(self.state_store_root)
        self.api_gateway = ApiRuntimeEntryGateway()
        self._mounted_session: IonMcpMountedSession | None = None

    # ---- descriptors ----

    @staticmethod
    def tool_descriptors() -> list[dict[str, Any]]:
        descriptors: list[dict[str, Any]] = []
        for name in sorted(READ_ONLY_TOOLS | DRY_RUN_TOOLS):
            descriptors.append(
                {
                    "name": name,
                    "description": _TOOL_DESCRIPTIONS[name],
                    "inputSchema": _TOOL_INPUT_SCHEMAS.get(name, {"type": "object", "additionalProperties": True}),
                }
            )
        return descriptors

    def _receipt_dir(self) -> Path:
        path = self.session_store.base / "mcp_bridge_receipts"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _write_bridge_receipt(
        self,
        *,
        tool_name: str,
        execution_resolution: IonMcpExecutionResolution,
        session_id: str | None,
        detail: str,
        witness_paths: Iterable[str] = (),
    ) -> IonMcpBridgeReceipt:
        receipt_id = f"mbr-{uuid.uuid4().hex[:12]}"
        path = self._receipt_dir() / f"{receipt_id}.json"
        receipt = IonMcpBridgeReceipt(
            receipt_id=receipt_id,
            created_at=_utc_now(),
            tool_name=tool_name,
            execution_resolution=execution_resolution,
            session_id=session_id,
            detail=detail,
            witness_paths=tuple([*witness_paths, str(path)]),
        )
        payload = receipt.to_dict()
        payload["execution_resolution"] = str(receipt.execution_resolution)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return receipt

    def _ensure_session_id(self, explicit_session_id: str | None = None) -> str | None:
        if explicit_session_id:
            return explicit_session_id
        if self._mounted_session is not None:
            return self._mounted_session.session_id
        ids = self.session_store.list_session_ids()
        return ids[-1] if ids else None

    def _result(
        self,
        *,
        tool_name: str,
        status: IonMcpToolStatus,
        execution_resolution: IonMcpExecutionResolution,
        payload: Mapping[str, Any],
        session_id: str | None = None,
        receipt_refs: Iterable[str] = (),
        next_required_action: str | None = None,
        kernel_truth_mutated: bool = False,
    ) -> IonMcpToolResult:
        if str(execution_resolution) not in ALLOWED_RESOLUTIONS:
            raise ValueError(f"V64 local MCP bridge cannot return resolution {execution_resolution}")
        return IonMcpToolResult(
            version=VERSION,
            tool_name=tool_name,
            status=status,
            execution_resolution=execution_resolution,
            session_id=session_id,
            payload=dict(payload),
            blocked_capabilities=_blocked_capabilities(),
            receipt_refs=tuple(receipt_refs),
            next_required_action=next_required_action,
            kernel_truth_mutated=kernel_truth_mutated,
        )

    # ---- tools ----

    def mount(self, request: IonMcpMountRequest | Mapping[str, Any] | None = None) -> IonMcpToolResult:
        if request is None:
            request = IonMcpMountRequest()
        elif isinstance(request, Mapping):
            data = dict(request)
            if isinstance(data.get("requested_scopes"), list):
                data["requested_scopes"] = tuple(data["requested_scopes"])
            request = IonMcpMountRequest(**data)

        if request.requested_mode not in {"read_only", "dry_run"}:
            receipt = self._write_bridge_receipt(
                tool_name="ion.mount",
                execution_resolution=IonMcpExecutionResolution.REFUSED,
                session_id=request.session_id,
                detail=f"refused mount mode {request.requested_mode}; V64 permits read_only or dry_run only",
            )
            return self._result(
                tool_name="ion.mount",
                status=IonMcpToolStatus.BLOCKED,
                execution_resolution=IonMcpExecutionResolution.REFUSED,
                session_id=request.session_id,
                receipt_refs=(receipt.receipt_id,),
                payload={"reason": "V64 local bridge forbids live execution mounts"},
                next_required_action="V64 forbids live execution mounts; request read_only or dry_run mode.",
            )

        carrier_ref = f"mcp://local/{_safe_name(request.client_name, 'client')}/{request.transport}"
        api_result = self.api_gateway.enter_runtime_session(
            session_store=self.session_store,
            carrier_ref=carrier_ref,
            session_id=request.session_id,
            create_session_if_missing=request.create_session_if_missing,
            allow_reentry_if_paused=True,
            root_authority_ref=request.root_authority_ref,
            label=f"ION MCP local bridge: {request.client_name}",
            purpose="V64 local dry-run MCP bridge mount",
            context_version=request.context_version,
            context_ref=request.context_ref,
        )

        if api_result.receipt.status != ApiRuntimeEntryStatus.ACCEPTED or api_result.session_identity is None:
            receipt = self._write_bridge_receipt(
                tool_name="ion.mount",
                execution_resolution=IonMcpExecutionResolution.REFUSED,
                session_id=request.session_id,
                detail=f"API runtime entry refused: {api_result.receipt.detail}",
                witness_paths=api_result.receipt.witness_paths,
            )
            return self._result(
                tool_name="ion.mount",
                status=IonMcpToolStatus.BLOCKED,
                execution_resolution=IonMcpExecutionResolution.REFUSED,
                session_id=request.session_id,
                receipt_refs=(api_result.receipt.receipt_id, receipt.receipt_id),
                payload={"api_runtime_entry": api_result.receipt.to_dict()},
                next_required_action="Resolve runtime-entry refusal before mounting ION through MCP.",
            )

        session_id = api_result.session_identity.session_id
        execution_mode = "DRY_RUN_ONLY" if request.requested_mode == "dry_run" else "READ_ONLY"
        allowed_tools = tuple(sorted(READ_ONLY_TOOLS | (DRY_RUN_TOOLS if request.requested_mode == "dry_run" else set())))
        denied_scopes = tuple(scope for scope in request.requested_scopes if scope in {
            "ion.jobs.execute.live",
            "ion.secrets.write",
            "ion.provider.dispatch",
            "ion.browser.mutate",
            "ion.governed_write.direct",
        })
        granted_scopes = tuple(scope for scope in request.requested_scopes if scope not in denied_scopes)

        mounted = IonMcpMountedSession(
            version=VERSION,
            session_id=session_id,
            workspace_id=request.workspace_id,
            client_name=request.client_name,
            transport=request.transport,
            execution_mode=execution_mode,
            granted_scopes=granted_scopes,
            denied_scopes=denied_scopes,
            allowed_tools=allowed_tools,
            blocked_tools=tuple(sorted(FORBIDDEN_TOOL_NAMES)),
            state_store_root=str(self.state_store_root),
            receipt_refs=(api_result.receipt.receipt_id,),
        )
        self._mounted_session = mounted
        receipt = self._write_bridge_receipt(
            tool_name="ion.mount",
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=session_id,
            detail="local MCP bridge mounted ION in read/dry-run capability envelope",
            witness_paths=api_result.receipt.witness_paths,
        )
        payload = mounted.to_dict()
        payload["receipt_refs"] = tuple([*mounted.receipt_refs, receipt.receipt_id])
        return self._result(
            tool_name="ion.mount",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=session_id,
            receipt_refs=payload["receipt_refs"],
            payload=payload,
            next_required_action="Read ion.boot_packet and ion.horizon.current before requesting dry-run work.",
        )

    def status(self, session_id: str | None = None) -> IonMcpToolResult:
        sid = self._ensure_session_id(session_id)
        branch_lock = self.ion_root / "00_BOOTSTRAP" / "V64_LOCAL_MCP_BRIDGE_LOCK.md"
        v63_lock = self.ion_root / "00_BOOTSTRAP" / "V63_ION_MCP_MOUNT_AND_ACCOUNT_CONNECTION_PROTOCOL_LOCK.md"
        payload = {
            "version": VERSION,
            "ion_root": str(self.ion_root),
            "state_store_root": str(self.state_store_root),
            "session_ids": self.session_store.list_session_ids(),
            "current_session_id": sid,
            "branch_lock_present": branch_lock.exists(),
            "v63_lock_present": v63_lock.exists(),
            "mcp_bridge_mode": "LOCAL_DRY_RUN_BRIDGE",
            "allowed_resolutions": sorted(ALLOWED_RESOLUTIONS),
            "live_execution_authorized": False,
            "daemon_loop_authorized": False,
            "provider_dispatch_authorized": False,
        }
        receipt = self._write_bridge_receipt(
            tool_name="ion.status",
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            detail="local MCP bridge status projected",
        )
        return self._result(
            tool_name="ion.status",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            receipt_refs=(receipt.receipt_id,),
            payload=payload,
        )

    def boot_packet(self, session_id: str | None = None) -> IonMcpToolResult:
        sid = self._ensure_session_id(session_id)
        packet = {
            "version": VERSION,
            "mount_instruction": "Use ION through read-only and dry-run MCP tools only.",
            "first_required_calls": ["ion.status", "ion.horizon.current", "ion.approvals.list"],
            "forbidden": sorted(FORBIDDEN_TOOL_NAMES),
            "law": [
                "MCP is the socket, not the authority.",
                "ION kernel/session/receipt law remains authoritative.",
                "The daemon may be previewed only through dry-run tools in V64.",
                "No MCP call may return LIVE_EXECUTED in V64.",
            ],
            "branch_files": {
                "protocol": "ION/02_architecture/ION_LOCAL_MCP_BRIDGE_TO_KERNEL_AND_DAEMON_PROTOCOL.md",
                "lock": "ION/00_BOOTSTRAP/V64_LOCAL_MCP_BRIDGE_LOCK.md",
            },
        }
        receipt = self._write_bridge_receipt(
            tool_name="ion.boot_packet",
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            detail="MCP boot packet projected",
        )
        return self._result(
            tool_name="ion.boot_packet",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            receipt_refs=(receipt.receipt_id,),
            payload=packet,
            next_required_action="Use ion.job.plan before any dry-run submission.",
        )

    def horizon_current(self, session_id: str | None = None) -> IonMcpToolResult:
        sid = self._ensure_session_id(session_id)
        horizon_doc = _read_text_if_exists(
            self.ion_root / "02_architecture" / "ION_V64_LOCAL_MCP_BRIDGE_EXECUTION_HORIZON_PROTOCOL.md",
            max_chars=12000,
        )
        payload = {
            "version": VERSION,
            "horizon": [
                "Mount local ION through MCP-facing bridge.",
                "Expose read-only status, boot, horizon, receipts, approvals, and tool list.",
                "Expose dry-run job plan/submission and daemon-step preview.",
                "Forbid live execution and direct daemon loop activation.",
                "Prepare later SDK-backed MCP transport only after invariants pass.",
            ],
            "horizon_doc_present": horizon_doc is not None,
            "horizon_doc_excerpt": horizon_doc,
        }
        receipt = self._write_bridge_receipt(
            tool_name="ion.horizon.current",
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            detail="current MCP local bridge horizon projected",
        )
        return self._result(
            tool_name="ion.horizon.current",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            receipt_refs=(receipt.receipt_id,),
            payload=payload,
        )

    def receipts_list(self, session_id: str | None = None, limit: int = 20) -> IonMcpToolResult:
        sid = self._ensure_session_id(session_id)
        receipts: list[dict[str, Any]] = []
        for directory in (
            self.session_store.receipts_dir,
            self.session_store.base / "api_entry_receipts",
            self.session_store.base / "mcp_bridge_receipts",
        ):
            if not directory.exists():
                continue
            for path in sorted(directory.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                except Exception:
                    payload = {"path": str(path), "read_error": True}
                payload.setdefault("path", str(path))
                receipts.append(payload)
                if len(receipts) >= limit:
                    break
            if len(receipts) >= limit:
                break
        receipt = self._write_bridge_receipt(
            tool_name="ion.receipts.list",
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            detail="receipt list projected",
        )
        return self._result(
            tool_name="ion.receipts.list",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            receipt_refs=(receipt.receipt_id,),
            payload={"receipts": receipts, "limit": limit},
        )

    def approvals_list(self, session_id: str | None = None) -> IonMcpToolResult:
        sid = self._ensure_session_id(session_id)
        queue_items = []
        if sid and self.session_store.exists(sid):
            queue = self.session_store.read_queue(sid)
            for item in queue.items:
                queue_items.append(item.to_dict())
        fixture = build_operator_approval_queue_view_model(build_fixture_operator_approval_input(
            mission_id="V64-MCP-LOCAL-BRIDGE",
            selected_target="ion-mcp-local-bridge",
            requested_action_summary="Review V64 local MCP bridge dry-run boundary.",
            operator_decision="PENDING",
        ))
        receipt = self._write_bridge_receipt(
            tool_name="ion.approvals.list",
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            detail="operator approval queue projection returned",
        )
        return self._result(
            tool_name="ion.approvals.list",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.READ_ONLY,
            session_id=sid,
            receipt_refs=(receipt.receipt_id,),
            payload={
                "queue_items": queue_items,
                "v62_operator_approval_projection": fixture.to_dict(),
                "validation": validate_operator_approval_queue_view_model(fixture),
            },
            next_required_action="Only dry-run handoff may be prepared from approval projections in V64.",
        )

    def job_plan(self, task: Mapping[str, Any] | None = None, session_id: str | None = None) -> IonMcpToolResult:
        sid = self._ensure_session_id(session_id)
        task = dict(task or {})
        plan = {
            "plan_id": f"mcp-plan-{uuid.uuid4().hex[:10]}",
            "task": task,
            "execution_resolution": "DRY_RUN",
            "steps": [
                "Validate mounted session and scopes.",
                "Compile bounded context from ION state resources.",
                "Generate dry-run work packet.",
                "Queue operator review if the plan implies mutation.",
                "Emit receipts; do not execute live.",
            ],
            "requires_operator_approval_for_live": True,
            "kernel_truth_mutated": False,
        }
        receipt = self._write_bridge_receipt(
            tool_name="ion.job.plan",
            execution_resolution=IonMcpExecutionResolution.DRY_RUN,
            session_id=sid,
            detail=f"dry-run job plan created: {plan['plan_id']}",
        )
        return self._result(
            tool_name="ion.job.plan",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.DRY_RUN,
            session_id=sid,
            receipt_refs=(receipt.receipt_id,),
            payload=plan,
            next_required_action="Submit as ion.job.submit_dry_run or route back to planning.",
        )

    def job_submit_dry_run(self, task: Mapping[str, Any] | None = None, session_id: str | None = None) -> IonMcpToolResult:
        sid = self._ensure_session_id(session_id)
        if not sid or not self.session_store.exists(sid):
            receipt = self._write_bridge_receipt(
                tool_name="ion.job.submit_dry_run",
                execution_resolution=IonMcpExecutionResolution.REFUSED,
                session_id=sid,
                detail="dry-run submission refused because no mounted session exists",
            )
            return self._result(
                tool_name="ion.job.submit_dry_run",
                status=IonMcpToolStatus.BLOCKED,
                execution_resolution=IonMcpExecutionResolution.REFUSED,
                session_id=sid,
                receipt_refs=(receipt.receipt_id,),
                payload={"reason": "missing mounted session"},
                next_required_action="Call ion.mount before submitting dry-run work.",
            )
        task = dict(task or {})
        item, _queue, queue_receipt = self.session_store.add_queue_item(
            sid,
            work_unit_id=task.get("work_unit_id"),
            status=SessionQueueItemStatus.PENDING,
            payload={
                "source": "V64_LOCAL_MCP_BRIDGE",
                "tool": "ion.job.submit_dry_run",
                "mode": "DRY_RUN_ONLY",
                "task": task,
                "live_execution_authorized": False,
            },
        )
        bridge_receipt = self._write_bridge_receipt(
            tool_name="ion.job.submit_dry_run",
            execution_resolution=IonMcpExecutionResolution.APPROVAL_REQUIRED,
            session_id=sid,
            detail=f"dry-run job submitted to runtime session queue: {item.item_id}",
            witness_paths=queue_receipt.witness_paths,
        )
        return self._result(
            tool_name="ion.job.submit_dry_run",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.APPROVAL_REQUIRED,
            session_id=sid,
            receipt_refs=(queue_receipt.receipt_id, bridge_receipt.receipt_id),
            payload={
                "queue_item": item.to_dict(),
                "mode": "DRY_RUN_ONLY",
                "operator_approval_required": True,
                "live_execution_authorized": False,
            },
            next_required_action="Show queued dry-run item to operator approval surface before any execution branch.",
        )

    def daemon_dry_run_step(self, task: Mapping[str, Any] | None = None, session_id: str | None = None) -> IonMcpToolResult:
        sid = self._ensure_session_id(session_id)
        task = dict(task or {})
        result = self.job_submit_dry_run(
            task={
                "daemon_preview": True,
                "requested_daemon_action": task,
                "note": "V64 previews daemon step only; no daemon loop is launched.",
            },
            session_id=sid,
        )
        payload = dict(result.payload)
        payload.update({
            "daemon_service_status": "DRY_RUN_PREVIEW_ONLY",
            "daemon_loop_started": False,
            "daemon_action_executed": False,
            "kernel_truth_mutated": False,
        })
        receipt = self._write_bridge_receipt(
            tool_name="ion.daemon.dry_run_step",
            execution_resolution=IonMcpExecutionResolution.APPROVAL_REQUIRED,
            session_id=sid,
            detail="daemon dry-run step preview projected; no daemon loop started",
            witness_paths=tuple(result.receipt_refs),
        )
        return self._result(
            tool_name="ion.daemon.dry_run_step",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.APPROVAL_REQUIRED,
            session_id=sid,
            receipt_refs=tuple([*result.receipt_refs, receipt.receipt_id]),
            payload=payload,
            next_required_action="Operator must review daemon dry-run preview; V64 forbids live daemon loop.",
        )

    def bundle_export_preview(self, session_id: str | None = None) -> IonMcpToolResult:
        sid = self._ensure_session_id(session_id)
        key_paths = [
            "00_BOOTSTRAP/V64_LOCAL_MCP_BRIDGE_LOCK.md",
            "02_architecture/ION_LOCAL_MCP_BRIDGE_TO_KERNEL_AND_DAEMON_PROTOCOL.md",
            "02_architecture/ION_V64_LOCAL_MCP_BRIDGE_EXECUTION_HORIZON_PROTOCOL.md",
            "04_packages/kernel/ion_mcp_local_bridge.py",
            "tests/test_kernel_ion_mcp_local_bridge.py",
            "03_registry/ion_mcp_local_bridge_tool_policy.yaml",
        ]
        payload = {
            "export_mode": "PREVIEW_ONLY",
            "would_include": [p for p in key_paths if (self.ion_root / p).exists()],
            "missing_recommended_paths": [p for p in key_paths if not (self.ion_root / p).exists()],
            "bundle_written": False,
            "kernel_truth_mutated": False,
        }
        receipt = self._write_bridge_receipt(
            tool_name="ion.bundle.export_preview",
            execution_resolution=IonMcpExecutionResolution.DRY_RUN,
            session_id=sid,
            detail="bundle export preview projected",
        )
        return self._result(
            tool_name="ion.bundle.export_preview",
            status=IonMcpToolStatus.OK,
            execution_resolution=IonMcpExecutionResolution.DRY_RUN,
            session_id=sid,
            receipt_refs=(receipt.receipt_id,),
            payload=payload,
            next_required_action="Use existing explicit ZIP packaging workflow outside MCP bridge.",
        )

    def call_tool(self, name: str, arguments: Mapping[str, Any] | None = None) -> IonMcpToolResult:
        arguments = dict(arguments or {})
        if name in FORBIDDEN_TOOL_NAMES or name.endswith(".execute_live"):
            sid = self._ensure_session_id(arguments.get("session_id"))
            receipt = self._write_bridge_receipt(
                tool_name=name,
                execution_resolution=IonMcpExecutionResolution.REFUSED,
                session_id=sid,
                detail=f"forbidden tool refused by V64 local MCP bridge: {name}",
            )
            return self._result(
                tool_name=name,
                status=IonMcpToolStatus.BLOCKED,
                execution_resolution=IonMcpExecutionResolution.REFUSED,
                session_id=sid,
                receipt_refs=(receipt.receipt_id,),
                payload={"reason": "V64 local MCP bridge forbids live execution tools"},
                next_required_action="Use dry-run planning or operator approval queue instead.",
            )

        if name == "ion.mount":
            return self.mount(arguments)
        if name == "ion.status":
            return self.status(arguments.get("session_id"))
        if name == "ion.boot_packet":
            return self.boot_packet(arguments.get("session_id"))
        if name == "ion.horizon.current":
            return self.horizon_current(arguments.get("session_id"))
        if name == "ion.receipts.list":
            return self.receipts_list(arguments.get("session_id"), int(arguments.get("limit", 20)))
        if name == "ion.approvals.list":
            return self.approvals_list(arguments.get("session_id"))
        if name == "ion.job.plan":
            return self.job_plan(arguments.get("task", arguments), arguments.get("session_id"))
        if name == "ion.job.submit_dry_run":
            return self.job_submit_dry_run(arguments.get("task", arguments), arguments.get("session_id"))
        if name == "ion.daemon.dry_run_step":
            return self.daemon_dry_run_step(arguments.get("task", arguments), arguments.get("session_id"))
        if name == "ion.bundle.export_preview":
            return self.bundle_export_preview(arguments.get("session_id"))
        if name == "ion.tools.list":
            return self._result(
                tool_name="ion.tools.list",
                status=IonMcpToolStatus.OK,
                execution_resolution=IonMcpExecutionResolution.READ_ONLY,
                session_id=self._ensure_session_id(arguments.get("session_id")),
                payload={"tools": self.tool_descriptors(), "forbidden_tools": sorted(FORBIDDEN_TOOL_NAMES)},
            )

        sid = self._ensure_session_id(arguments.get("session_id"))
        receipt = self._write_bridge_receipt(
            tool_name=name,
            execution_resolution=IonMcpExecutionResolution.REFUSED,
            session_id=sid,
            detail=f"unknown MCP bridge tool refused: {name}",
        )
        return self._result(
            tool_name=name,
            status=IonMcpToolStatus.BLOCKED,
            execution_resolution=IonMcpExecutionResolution.REFUSED,
            session_id=sid,
            receipt_refs=(receipt.receipt_id,),
            payload={"reason": "unknown tool"},
            next_required_action="Call ion.tools.list for available V64 bridge tools.",
        )


_TOOL_DESCRIPTIONS = {
    "ion.mount": "Mount a local ION root into a read-only or dry-run V64 MCP bridge session.",
    "ion.status": "Project local ION bridge status without mutating kernel truth.",
    "ion.boot_packet": "Return the V64 boot packet for an AI agent mounted through MCP.",
    "ion.horizon.current": "Return the current V64 local MCP bridge horizon.",
    "ion.receipts.list": "List recent bridge/session/API-entry receipts.",
    "ion.approvals.list": "Project the V62-compatible approval queue surface.",
    "ion.tools.list": "List V64 MCP bridge tools and forbidden live tools.",
    "ion.job.plan": "Create a dry-run job plan; no execution.",
    "ion.job.submit_dry_run": "Submit a dry-run queue item requiring operator review.",
    "ion.daemon.dry_run_step": "Preview a supervised daemon step; no daemon loop is started.",
    "ion.bundle.export_preview": "Preview bundle-export contents; does not write a ZIP.",
}

_TOOL_INPUT_SCHEMAS: dict[str, dict[str, Any]] = {
    "ion.mount": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "client_name": {"type": "string"},
            "client_version": {"type": "string"},
            "transport": {"type": "string", "enum": ["stdio", "localhost-http", "streamable-http", "unspecified"]},
            "requested_mode": {"type": "string", "enum": ["read_only", "dry_run"]},
            "workspace_id": {"type": "string"},
            "session_id": {"type": "string"},
            "create_session_if_missing": {"type": "boolean"},
            "requested_scopes": {"type": "array", "items": {"type": "string"}},
        },
    },
    "ion.status": {"type": "object", "additionalProperties": False, "properties": {"session_id": {"type": "string"}}},
    "ion.boot_packet": {"type": "object", "additionalProperties": False, "properties": {"session_id": {"type": "string"}}},
    "ion.horizon.current": {"type": "object", "additionalProperties": False, "properties": {"session_id": {"type": "string"}}},
    "ion.receipts.list": {
        "type": "object",
        "additionalProperties": False,
        "properties": {"session_id": {"type": "string"}, "limit": {"type": "integer", "minimum": 1, "maximum": 100}},
    },
    "ion.approvals.list": {"type": "object", "additionalProperties": False, "properties": {"session_id": {"type": "string"}}},
    "ion.tools.list": {"type": "object", "additionalProperties": False, "properties": {}},
    "ion.job.plan": {"type": "object", "additionalProperties": True, "properties": {"session_id": {"type": "string"}, "task": {"type": "object"}}},
    "ion.job.submit_dry_run": {"type": "object", "additionalProperties": True, "properties": {"session_id": {"type": "string"}, "task": {"type": "object"}}},
    "ion.daemon.dry_run_step": {"type": "object", "additionalProperties": True, "properties": {"session_id": {"type": "string"}, "task": {"type": "object"}}},
    "ion.bundle.export_preview": {"type": "object", "additionalProperties": False, "properties": {"session_id": {"type": "string"}}},
}


# ---- minimal JSON-RPC stdio shim ----

def _jsonrpc_result(message_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": message_id, "result": result}


def _jsonrpc_error(message_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}}
    if data is not None:
        payload["error"]["data"] = data
    return payload


def handle_jsonrpc_message(bridge: IonMcpLocalBridge, message: Mapping[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    message_id = message.get("id")
    params = message.get("params") or {}

    if method == "initialize":
        return _jsonrpc_result(
            message_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "ion-mcp-local-bridge", "version": VERSION},
            },
        )
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return _jsonrpc_result(message_id, {"tools": bridge.tool_descriptors()})
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if not isinstance(name, str):
            return _jsonrpc_error(message_id, -32602, "tools/call requires string params.name")
        result = bridge.call_tool(name, arguments).to_dict()
        is_error = result["status"] in {"BLOCKED", "ERROR"}
        return _jsonrpc_result(
            message_id,
            {
                "content": [{"type": "text", "text": json.dumps(result, indent=2, sort_keys=True)}],
                "isError": is_error,
            },
        )
    return _jsonrpc_error(message_id, -32601, f"Unsupported method: {method}")


def run_stdio_server(ion_root: str | Path, state_store_root: str | Path | None = None) -> int:
    bridge = IonMcpLocalBridge(ion_root=ion_root, state_store_root=state_store_root)
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            message = json.loads(raw)
            response = handle_jsonrpc_message(bridge, message)
        except Exception as exc:  # pragma: no cover - defensive stdio boundary
            response = _jsonrpc_error(None, -32000, "ION MCP local bridge error", {"error": str(exc)})
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":")) + "\n")
            sys.stdout.flush()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the V64 local ION MCP bridge stdio shim.")
    parser.add_argument("--ion-root", default=".", help="Path to the ION root or snapshot root containing ION/")
    parser.add_argument("--state-store-root", default=None, help="Optional runtime-session store root")
    parser.add_argument("--stdio", action="store_true", help="Run minimal JSON-RPC stdio bridge")
    parser.add_argument("--list-tools", action="store_true", help="Print tool descriptors as JSON")
    args = parser.parse_args(argv)

    bridge = IonMcpLocalBridge(args.ion_root, args.state_store_root)
    if args.list_tools:
        print(json.dumps({"tools": bridge.tool_descriptors()}, indent=2, sort_keys=True))
        return 0
    if args.stdio:
        return run_stdio_server(args.ion_root, args.state_store_root)
    print(json.dumps(bridge.status().to_dict(), indent=2, sort_keys=True))
    return 0


IonMcpLocalBridgeAdapter = IonMcpLocalBridge


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
