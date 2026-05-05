"""V69 hosted MCP auth/account/workspace alpha boundary for ION.

V69 is still a boundary branch. It does not certify OAuth, a public hosted
endpoint, a paid cloud, Kubernetes, or live execution. It defines and validates
the account/workspace/state-root/token/session separation needed before hosted
MCP can become operational.

V69 law:
    A token is not an ION session.
    An MCP transport session is not ION authority.
    A workspace mount must resolve through account, workspace, state-root,
    scope, policy, and receipt constraints.
    Hosted alpha may project read-only and dry-run capability only.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta, timezone
import argparse
import hashlib
import json
from pathlib import Path
import uuid
from typing import Any, Iterable, Mapping

from .ion_mcp_local_bridge import (
    ALLOWED_RESOLUTIONS,
    FORBIDDEN_TOOL_NAMES,
    IonMcpExecutionResolution,
    IonMcpToolStatus,
)
from .model import KernelRecord, StrEnum


VERSION = "V69_HOSTED_MCP_AUTH_AND_ACCOUNT_WORKSPACE_ALPHA_PROTOCOL"
HOSTED_ALPHA_MODE = "HOSTED_ALPHA_BOUNDARY_ONLY"
TOKEN_AUDIENCE = "ion-mcp-hosted-alpha"
BASELINE_SCOPES = {
    "ion.mount.basic",
    "ion.state.read",
    "ion.receipts.read",
    "ion.approvals.read",
    "ion.jobs.plan",
    "ion.jobs.execute.dry_run",
    "ion.bundles.export",
}
ELEVATED_SCOPES = {
    "ion.jobs.execute.live",
    "ion.approvals.write",
    "ion.workspace.admin",
    "ion.secrets.write",
    "ion.provider.dispatch",
    "ion.browser.mutate",
    "ion.governed_write.direct",
}
FORBIDDEN_HOSTED_ALPHA_SCOPES = ELEVATED_SCOPES | {
    "ion.shell.run",
    "ion.daemon.loop",
    "ion.credentials.read",
}
ALLOWED_EXECUTION_MODES = {"read_only", "dry_run"}
FORBIDDEN_EXECUTION_MODES = {"live_candidate", "live_authorized", "live_execute"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _plus_minutes(minutes: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(minutes=minutes)).isoformat()


def _safe_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def _hash_state_seed(workspace_id: str, branch_ref: str, policy_version: str) -> str:
    seed = f"{workspace_id}|{branch_ref}|{policy_version}".encode("utf-8")
    return "ion_state_" + hashlib.sha256(seed).hexdigest()[:32]


class HostedAlphaStatus(StrEnum):
    ACCEPTED = "ACCEPTED"
    REFUSED = "REFUSED"
    ELEVATION_REQUIRED = "ELEVATION_REQUIRED"


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
    branch_ref: str = "V69_HOSTED_MCP_AUTH_AND_ACCOUNT_WORKSPACE_ALPHA_PROTOCOL"
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
class IonHostedAccessTokenPreview(KernelRecord):
    token_id: str
    subject_id: str
    audience: str
    issued_at: str
    expires_at: str
    scopes: tuple[str, ...]
    workspace_ids: tuple[str, ...]
    token_hash: str
    oauth_certified: bool = False
    raw_token_stored: bool = False


@dataclass(frozen=True)
class IonHostedMountRequest(KernelRecord):
    account_id: str
    subject_id: str
    workspace_id: str
    client_name: str = "hosted-alpha-client"
    transport: str = "streamable-http-alpha"
    requested_mode: str = "dry_run"
    requested_scopes: tuple[str, ...] = tuple(sorted(BASELINE_SCOPES))
    token_audience: str = TOKEN_AUDIENCE
    token_subject_id: str | None = None
    token_workspace_ids: tuple[str, ...] = ()
    mcp_transport_session_id: str | None = None
    resume_session_id: str | None = None
    create_session_if_missing: bool = True


@dataclass(frozen=True)
class IonHostedMountSession(KernelRecord):
    version: str
    ion_session_id: str
    mcp_transport_session_id: str
    account_id: str
    subject_id: str
    workspace_id: str
    state_root_id: str
    client_name: str
    transport: str
    execution_mode: str
    granted_scopes: tuple[str, ...]
    denied_scopes: tuple[str, ...]
    elevation_required_scopes: tuple[str, ...]
    allowed_resolutions: tuple[str, ...]
    forbidden_tools: tuple[str, ...]
    created_at: str
    expires_at: str
    token_is_session: bool = False
    transport_session_is_authority: bool = False
    oauth_certified: bool = False
    hosted_cloud_certified: bool = False
    public_endpoint_certified: bool = False
    live_execution_authorized: bool = False
    provider_dispatch_authorized: bool = False
    browser_mutation_authorized: bool = False
    credential_access_authorized: bool = False
    canonical_write_authorized: bool = False


@dataclass(frozen=True)
class IonHostedAlphaDecision(KernelRecord):
    version: str
    status: HostedAlphaStatus
    execution_resolution: IonMcpExecutionResolution
    request: Mapping[str, Any]
    session: Mapping[str, Any] | None
    account: Mapping[str, Any] | None
    workspace: Mapping[str, Any] | None
    state_root: Mapping[str, Any] | None
    denied_reasons: tuple[str, ...]
    granted_scopes: tuple[str, ...]
    denied_scopes: tuple[str, ...]
    elevation_required_scopes: tuple[str, ...]
    receipt_id: str
    created_at: str
    next_required_action: str
    token_is_session: bool = False
    transport_session_is_authority: bool = False
    live_execution_authorized: bool = False
    kernel_truth_mutated: bool = False
    hosted_cloud_certified: bool = False
    oauth_certified: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = str(self.status)
        data["execution_resolution"] = str(self.execution_resolution)
        return data


def mint_access_token_preview(
    *,
    subject_id: str,
    workspace_ids: Iterable[str],
    scopes: Iterable[str] = BASELINE_SCOPES,
    audience: str = TOKEN_AUDIENCE,
    ttl_minutes: int = 60,
) -> IonHostedAccessTokenPreview:
    """Mint a non-secret token preview object for alpha boundary tests.

    This is not OAuth certification and not a production token issuer. It exists
    only to model token audience, subject, scope, workspace, and expiry fields
    without storing raw bearer material in ION state.
    """
    issued_at = _utc_now()
    token_id = _safe_id("tokprev")
    workspace_tuple = tuple(sorted(set(workspace_ids)))
    scope_tuple = tuple(sorted(set(scopes)))
    token_hash = hashlib.sha256(
        "|".join([token_id, subject_id, audience, ",".join(workspace_tuple), ",".join(scope_tuple)]).encode("utf-8")
    ).hexdigest()
    return IonHostedAccessTokenPreview(
        token_id=token_id,
        subject_id=subject_id,
        audience=audience,
        issued_at=issued_at,
        expires_at=_plus_minutes(ttl_minutes),
        scopes=scope_tuple,
        workspace_ids=workspace_tuple,
        token_hash=token_hash,
    )


def build_fixture_hosted_account_workspace(
    *,
    account_id: str = "acct_local_founder",
    subject_id: str = "subj_braden_operator",
    workspace_id: str = "wsp_ion_production",
    display_name: str = "ION Production",
    branch_ref: str = VERSION,
) -> tuple[IonHostedAccount, IonHostedWorkspace, IonHostedStateRoot, IonHostedAccessTokenPreview]:
    account = IonHostedAccount(account_id=account_id, subject_id=subject_id)
    workspace = IonHostedWorkspace(
        workspace_id=workspace_id,
        account_id=account_id,
        display_name=display_name,
        branch_ref=branch_ref,
    )
    state_root = IonHostedStateRoot(
        state_root_id=_hash_state_seed(workspace_id, branch_ref, VERSION),
        workspace_id=workspace_id,
        branch_ref=branch_ref,
    )
    token = mint_access_token_preview(
        subject_id=subject_id,
        workspace_ids=(workspace_id,),
        scopes=BASELINE_SCOPES,
    )
    return account, workspace, state_root, token


def _normalize_request(request: IonHostedMountRequest | Mapping[str, Any]) -> IonHostedMountRequest:
    if isinstance(request, IonHostedMountRequest):
        return request
    data = dict(request)
    if isinstance(data.get("requested_scopes"), list):
        data["requested_scopes"] = tuple(data["requested_scopes"])
    if isinstance(data.get("token_workspace_ids"), list):
        data["token_workspace_ids"] = tuple(data["token_workspace_ids"])
    return IonHostedMountRequest(**data)


def evaluate_hosted_alpha_mount(
    request: IonHostedMountRequest | Mapping[str, Any],
    *,
    account: IonHostedAccount | Mapping[str, Any],
    workspace: IonHostedWorkspace | Mapping[str, Any],
    state_root: IonHostedStateRoot | Mapping[str, Any],
    token: IonHostedAccessTokenPreview | Mapping[str, Any],
) -> IonHostedAlphaDecision:
    """Evaluate a hosted alpha mount request without performing OAuth or cloud work."""
    req = _normalize_request(request)
    account_obj = account if isinstance(account, IonHostedAccount) else IonHostedAccount(**dict(account))
    workspace_obj = workspace if isinstance(workspace, IonHostedWorkspace) else IonHostedWorkspace(**dict(workspace))
    state_obj = state_root if isinstance(state_root, IonHostedStateRoot) else IonHostedStateRoot(**dict(state_root))
    token_obj = token if isinstance(token, IonHostedAccessTokenPreview) else IonHostedAccessTokenPreview(**dict(token))

    denied_reasons: list[str] = []
    if req.account_id != account_obj.account_id:
        denied_reasons.append("account_id does not match account")
    if req.subject_id != account_obj.subject_id:
        denied_reasons.append("subject_id does not match account subject")
    if req.workspace_id != workspace_obj.workspace_id:
        denied_reasons.append("workspace_id does not match workspace")
    if workspace_obj.account_id != account_obj.account_id:
        denied_reasons.append("workspace is not owned by account")
    if state_obj.workspace_id != workspace_obj.workspace_id:
        denied_reasons.append("state root does not belong to workspace")
    if req.token_audience != TOKEN_AUDIENCE or token_obj.audience != TOKEN_AUDIENCE:
        denied_reasons.append("token audience is not the ION hosted MCP alpha audience")
    if req.token_subject_id and req.token_subject_id != req.subject_id:
        denied_reasons.append("token subject does not match request subject")
    if token_obj.subject_id != req.subject_id:
        denied_reasons.append("token preview subject does not match request subject")
    token_workspaces = set(req.token_workspace_ids or token_obj.workspace_ids)
    if req.workspace_id not in token_workspaces:
        denied_reasons.append("token preview is not scoped to requested workspace")
    if req.requested_mode in FORBIDDEN_EXECUTION_MODES:
        denied_reasons.append("requested execution mode is forbidden in V69 hosted alpha")
    if req.requested_mode not in ALLOWED_EXECUTION_MODES:
        denied_reasons.append("requested execution mode is not supported by V69 hosted alpha")
    if req.resume_session_id and req.resume_session_id.startswith("tok"):
        denied_reasons.append("token identifier cannot be used as ION session identifier")
    if req.mcp_transport_session_id and req.mcp_transport_session_id == req.resume_session_id:
        denied_reasons.append("MCP transport session id cannot be treated as ION session authority")

    requested_scopes = set(req.requested_scopes)
    denied_scopes = tuple(sorted(scope for scope in requested_scopes if scope in FORBIDDEN_HOSTED_ALPHA_SCOPES))
    elevation_required = tuple(sorted(scope for scope in requested_scopes if scope in ELEVATED_SCOPES))
    granted = tuple(sorted(scope for scope in requested_scopes if scope in BASELINE_SCOPES and scope in set(token_obj.scopes)))
    missing_from_token = sorted(scope for scope in requested_scopes if scope in BASELINE_SCOPES and scope not in set(token_obj.scopes))
    if missing_from_token:
        denied_reasons.append("requested baseline scopes are absent from token preview: " + ",".join(missing_from_token))

    receipt_id = _safe_id("hmr")
    created_at = _utc_now()

    if denied_reasons or (req.requested_mode in FORBIDDEN_EXECUTION_MODES):
        status = HostedAlphaStatus.REFUSED
        resolution = IonMcpExecutionResolution.REFUSED
        session_dict = None
        next_action = "Correct account/workspace/token/mode/scope mismatch before hosted MCP mount."
    elif denied_scopes or elevation_required:
        status = HostedAlphaStatus.ELEVATION_REQUIRED
        resolution = IonMcpExecutionResolution.APPROVAL_REQUIRED
        session_dict = None
        next_action = "Remove elevated scopes or queue a future operator-approved hosted branch; V69 cannot grant them."
    else:
        status = HostedAlphaStatus.ACCEPTED
        resolution = IonMcpExecutionResolution.READ_ONLY if req.requested_mode == "read_only" else IonMcpExecutionResolution.DRY_RUN
        ion_session_id = req.resume_session_id or _safe_id("ion_sess")
        transport_session_id = req.mcp_transport_session_id or _safe_id("mcp_sess")
        session = IonHostedMountSession(
            version=VERSION,
            ion_session_id=ion_session_id,
            mcp_transport_session_id=transport_session_id,
            account_id=account_obj.account_id,
            subject_id=req.subject_id,
            workspace_id=workspace_obj.workspace_id,
            state_root_id=state_obj.state_root_id,
            client_name=req.client_name,
            transport=req.transport,
            execution_mode="READ_ONLY" if req.requested_mode == "read_only" else "DRY_RUN_ONLY",
            granted_scopes=granted,
            denied_scopes=denied_scopes,
            elevation_required_scopes=elevation_required,
            allowed_resolutions=tuple(sorted(ALLOWED_RESOLUTIONS)),
            forbidden_tools=tuple(sorted(FORBIDDEN_TOOL_NAMES)),
            created_at=created_at,
            expires_at=_plus_minutes(60),
        )
        session_dict = session.to_dict()
        next_action = "Hosted alpha mount accepted for read/dry-run projection only; continue with ion.status or ion.job.plan."

    return IonHostedAlphaDecision(
        version=VERSION,
        status=status,
        execution_resolution=resolution,
        request=req.to_dict(),
        session=session_dict,
        account=account_obj.to_dict(),
        workspace=workspace_obj.to_dict(),
        state_root=state_obj.to_dict(),
        denied_reasons=tuple(denied_reasons),
        granted_scopes=granted,
        denied_scopes=denied_scopes,
        elevation_required_scopes=elevation_required,
        receipt_id=receipt_id,
        created_at=created_at,
        next_required_action=next_action,
    )


def build_hosted_alpha_boundary_report(ion_root: str | Path | None = None) -> dict[str, Any]:
    account, workspace, state_root, token = build_fixture_hosted_account_workspace()
    accepted_request = IonHostedMountRequest(
        account_id=account.account_id,
        subject_id=account.subject_id,
        workspace_id=workspace.workspace_id,
        token_subject_id=token.subject_id,
        token_workspace_ids=token.workspace_ids,
        requested_mode="dry_run",
        requested_scopes=tuple(sorted(BASELINE_SCOPES)),
    )
    accepted = evaluate_hosted_alpha_mount(
        accepted_request,
        account=account,
        workspace=workspace,
        state_root=state_root,
        token=token,
    )

    elevated_request = IonHostedMountRequest(
        account_id=account.account_id,
        subject_id=account.subject_id,
        workspace_id=workspace.workspace_id,
        token_subject_id=token.subject_id,
        token_workspace_ids=token.workspace_ids,
        requested_mode="dry_run",
        requested_scopes=tuple(sorted(BASELINE_SCOPES | {"ion.jobs.execute.live", "ion.secrets.write"})),
    )
    elevated = evaluate_hosted_alpha_mount(
        elevated_request,
        account=account,
        workspace=workspace,
        state_root=state_root,
        token=token,
    )

    wrong_audience_token = mint_access_token_preview(
        subject_id=account.subject_id,
        workspace_ids=(workspace.workspace_id,),
        scopes=BASELINE_SCOPES,
        audience="wrong-audience",
    )
    wrong_audience = evaluate_hosted_alpha_mount(
        accepted_request,
        account=account,
        workspace=workspace,
        state_root=state_root,
        token=wrong_audience_token,
    )

    token_as_session_request = IonHostedMountRequest(
        account_id=account.account_id,
        subject_id=account.subject_id,
        workspace_id=workspace.workspace_id,
        token_subject_id=token.subject_id,
        token_workspace_ids=token.workspace_ids,
        requested_mode="dry_run",
        resume_session_id=token.token_id,
    )
    token_as_session = evaluate_hosted_alpha_mount(
        token_as_session_request,
        account=account,
        workspace=workspace,
        state_root=state_root,
        token=token,
    )

    decisions = [accepted, elevated, wrong_audience, token_as_session]
    forbidden_resolution_seen = any(str(d.execution_resolution) not in ALLOWED_RESOLUTIONS for d in decisions)
    live_execution_authorized_seen = any(d.live_execution_authorized for d in decisions)
    kernel_truth_mutation_seen = any(d.kernel_truth_mutated for d in decisions)
    accepted_session = accepted.session or {}

    passed = (
        str(accepted.status) == "ACCEPTED"
        and str(accepted.execution_resolution) == "DRY_RUN"
        and accepted_session.get("token_is_session") is False
        and accepted_session.get("transport_session_is_authority") is False
        and str(elevated.status) == "ELEVATION_REQUIRED"
        and str(elevated.execution_resolution) == "APPROVAL_REQUIRED"
        and str(wrong_audience.status) == "REFUSED"
        and str(token_as_session.status) == "REFUSED"
        and not forbidden_resolution_seen
        and not live_execution_authorized_seen
        and not kernel_truth_mutation_seen
    )

    return {
        "version": VERSION,
        "created_at": _utc_now(),
        "ion_root": str(Path(ion_root).resolve()) if ion_root else None,
        "mode": HOSTED_ALPHA_MODE,
        "passed": passed,
        "oauth_certified": False,
        "hosted_cloud_certified": False,
        "public_endpoint_certified": False,
        "kubernetes_certified": False,
        "live_execution_authorized_seen": live_execution_authorized_seen,
        "kernel_truth_mutation_seen": kernel_truth_mutation_seen,
        "forbidden_resolution_seen": forbidden_resolution_seen,
        "token_session_separation_verified": accepted_session.get("token_is_session") is False,
        "transport_session_authority_separation_verified": accepted_session.get("transport_session_is_authority") is False,
        "accepted_decision": accepted.to_dict(),
        "elevated_decision": elevated.to_dict(),
        "wrong_audience_decision": wrong_audience.to_dict(),
        "token_as_session_decision": token_as_session.to_dict(),
        "required_next_branch_gate": "Hosted HTTP/OAuth implementation must not proceed until this alpha boundary remains green.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ION V69 hosted MCP auth/account/workspace alpha boundary")
    parser.add_argument("--ion-root", default="ION")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = build_hosted_alpha_boundary_report(args.ion_root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{VERSION}: {'PASS' if report['passed'] else 'FAIL'}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
