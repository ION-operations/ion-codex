"""V70 hosted MCP OAuth and Streamable HTTP implementation preview for ION.

V70 proves hosted MCP mechanics without certifying production OAuth/cloud:
OAuth authorization-code + PKCE-shaped preview, bearer-header validation,
and Streamable-HTTP-style POST /mcp dispatch through existing ION boundaries.

A token is not an ION session. A transport session is not ION authority.
All outcomes remain READ_ONLY, DRY_RUN, APPROVAL_REQUIRED, or REFUSED.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import argparse
import base64
import hashlib
import json
from pathlib import Path
import secrets
import tempfile
from typing import Any, Mapping

from .ion_mcp_hosted_auth_alpha import (
    BASELINE_SCOPES,
    ELEVATED_SCOPES,
    FORBIDDEN_HOSTED_ALPHA_SCOPES,
    TOKEN_AUDIENCE,
    IonHostedAccount,
    IonHostedWorkspace,
    IonHostedStateRoot,
    IonHostedAccessTokenPreview,
    IonHostedMountRequest,
    build_fixture_hosted_account_workspace,
    evaluate_hosted_alpha_mount,
    mint_access_token_preview,
)
from .ion_mcp_local_bridge import (
    ALLOWED_RESOLUTIONS,
    FORBIDDEN_TOOL_NAMES,
    IonMcpExecutionResolution,
    IonMcpLocalBridge,
    handle_jsonrpc_message,
)
from .model import KernelRecord, StrEnum


VERSION = "V70_HOSTED_MCP_OAUTH_AND_STREAMABLE_HTTP_IMPLEMENTATION_PREVIEW"
HOSTED_HTTP_PATH = "/mcp"
SUPPORTED_CODE_CHALLENGE_METHOD = "S256"
PREVIEW_BEARER_PREFIX = "ionv70_preview"
ALLOWED_PREVIEW_SCOPES = BASELINE_SCOPES | ELEVATED_SCOPES
FORBIDDEN_LIVE_RESOLUTION = "LIVE_EXECUTED"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _b64url_digest(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def _safe_hash(value: str, chars: int = 32) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:chars]


class OAuthPreviewStatus(StrEnum):
    AUTHORIZED = "AUTHORIZED"
    TOKEN_ISSUED = "TOKEN_ISSUED"
    REFUSED = "REFUSED"


class HostedHttpPreviewStatus(StrEnum):
    OK = "OK"
    REFUSED = "REFUSED"


@dataclass(frozen=True)
class IonOAuthAuthorizationRequestPreview(KernelRecord):
    client_id: str
    redirect_uri: str
    subject_id: str
    workspace_id: str
    requested_scopes: tuple[str, ...]
    code_challenge: str
    code_challenge_method: str = SUPPORTED_CODE_CHALLENGE_METHOD
    response_type: str = "code"
    state: str | None = None


@dataclass(frozen=True)
class IonOAuthAuthorizationCodePreview(KernelRecord):
    version: str
    status: OAuthPreviewStatus
    authorization_code_id: str | None
    authorization_code_hash: str | None
    client_id: str | None
    redirect_uri: str | None
    subject_id: str | None
    workspace_id: str | None
    requested_scopes: tuple[str, ...]
    denied_scopes: tuple[str, ...]
    code_challenge: str | None
    code_challenge_method: str | None
    created_at: str
    denied_reasons: tuple[str, ...] = ()
    raw_authorization_code_stored: bool = False
    oauth_certified: bool = False
    live_execution_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = str(self.status)
        return data


@dataclass(frozen=True)
class IonOAuthTokenRequestPreview(KernelRecord):
    grant_type: str
    authorization_code_id: str
    client_id: str
    redirect_uri: str
    code_verifier: str
    requested_scopes: tuple[str, ...] = ()


@dataclass(frozen=True)
class IonOAuthTokenDecisionPreview(KernelRecord):
    version: str
    status: OAuthPreviewStatus
    token: Mapping[str, Any] | None
    bearer_preview: str | None
    granted_scopes: tuple[str, ...]
    denied_scopes: tuple[str, ...]
    denied_reasons: tuple[str, ...]
    created_at: str
    token_is_session: bool = False
    raw_token_stored: bool = False
    oauth_certified: bool = False
    hosted_cloud_certified: bool = False
    live_execution_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = str(self.status)
        return data


@dataclass(frozen=True)
class IonHostedHttpPreviewRequest(KernelRecord):
    method: str
    path: str
    headers: Mapping[str, str]
    body: Mapping[str, Any]
    mcp_transport_session_id: str | None = None


@dataclass(frozen=True)
class IonHostedHttpPreviewResponse(KernelRecord):
    version: str
    status: HostedHttpPreviewStatus
    http_status: int
    mcp_transport_session_id: str | None
    jsonrpc_response: Mapping[str, Any] | None
    hosted_mount_decision: Mapping[str, Any] | None
    denied_reasons: tuple[str, ...]
    execution_resolution: IonMcpExecutionResolution
    created_at: str
    token_is_session: bool = False
    transport_session_is_authority: bool = False
    oauth_certified: bool = False
    hosted_cloud_certified: bool = False
    public_endpoint_certified: bool = False
    live_execution_authorized: bool = False
    kernel_truth_mutated: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = str(self.status)
        data["execution_resolution"] = str(self.execution_resolution)
        return data


def issue_authorization_code_preview(
    request: IonOAuthAuthorizationRequestPreview | Mapping[str, Any],
    *,
    account: IonHostedAccount | Mapping[str, Any],
    workspace: IonHostedWorkspace | Mapping[str, Any],
) -> IonOAuthAuthorizationCodePreview:
    req = request if isinstance(request, IonOAuthAuthorizationRequestPreview) else IonOAuthAuthorizationRequestPreview(**dict(request))
    account_obj = account if isinstance(account, IonHostedAccount) else IonHostedAccount(**dict(account))
    workspace_obj = workspace if isinstance(workspace, IonHostedWorkspace) else IonHostedWorkspace(**dict(workspace))
    denied: list[str] = []
    if req.response_type != "code":
        denied.append("response_type must be code")
    if req.code_challenge_method != SUPPORTED_CODE_CHALLENGE_METHOD:
        denied.append("code_challenge_method must be S256")
    if req.subject_id != account_obj.subject_id:
        denied.append("subject_id does not match account")
    if req.workspace_id != workspace_obj.workspace_id:
        denied.append("workspace_id does not match workspace")
    if workspace_obj.account_id != account_obj.account_id:
        denied.append("workspace is not owned by account")
    requested = tuple(sorted(set(req.requested_scopes)))
    unknown = tuple(sorted(scope for scope in requested if scope not in ALLOWED_PREVIEW_SCOPES and scope not in FORBIDDEN_HOSTED_ALPHA_SCOPES))
    if unknown:
        denied.append("unknown scopes requested: " + ",".join(unknown))
    if denied:
        return IonOAuthAuthorizationCodePreview(
            version=VERSION, status=OAuthPreviewStatus.REFUSED,
            authorization_code_id=None, authorization_code_hash=None,
            client_id=None, redirect_uri=None, subject_id=None, workspace_id=None,
            requested_scopes=requested, denied_scopes=requested,
            code_challenge=None, code_challenge_method=None, created_at=_utc_now(),
            denied_reasons=tuple(denied),
        )
    code_id = "authcode_" + secrets.token_hex(8)
    code_hash = _safe_hash("|".join([code_id, req.client_id, req.redirect_uri, req.subject_id, req.workspace_id, req.code_challenge]))
    denied_scopes = tuple(sorted(scope for scope in requested if scope in FORBIDDEN_HOSTED_ALPHA_SCOPES))
    return IonOAuthAuthorizationCodePreview(
        version=VERSION, status=OAuthPreviewStatus.AUTHORIZED,
        authorization_code_id=code_id, authorization_code_hash=code_hash,
        client_id=req.client_id, redirect_uri=req.redirect_uri,
        subject_id=req.subject_id, workspace_id=req.workspace_id,
        requested_scopes=requested, denied_scopes=denied_scopes,
        code_challenge=req.code_challenge, code_challenge_method=req.code_challenge_method,
        created_at=_utc_now(),
    )


def exchange_authorization_code_preview(
    code: IonOAuthAuthorizationCodePreview | Mapping[str, Any],
    request: IonOAuthTokenRequestPreview | Mapping[str, Any],
) -> IonOAuthTokenDecisionPreview:
    code_obj = code if isinstance(code, IonOAuthAuthorizationCodePreview) else IonOAuthAuthorizationCodePreview(**dict(code))
    req = request if isinstance(request, IonOAuthTokenRequestPreview) else IonOAuthTokenRequestPreview(**dict(request))
    denied: list[str] = []
    if code_obj.status != OAuthPreviewStatus.AUTHORIZED:
        denied.append("authorization code is not authorized")
    if req.grant_type != "authorization_code":
        denied.append("grant_type must be authorization_code")
    if req.authorization_code_id != code_obj.authorization_code_id:
        denied.append("authorization_code_id does not match issued code")
    if req.client_id != code_obj.client_id:
        denied.append("client_id does not match authorization code")
    if req.redirect_uri != code_obj.redirect_uri:
        denied.append("redirect_uri does not match authorization code")
    if _b64url_digest(req.code_verifier) != code_obj.code_challenge:
        denied.append("PKCE verifier does not match S256 challenge")
    requested_scopes = tuple(sorted(set(req.requested_scopes or code_obj.requested_scopes)))
    granted_scopes = tuple(sorted(scope for scope in requested_scopes if scope in BASELINE_SCOPES))
    denied_scopes = tuple(sorted(scope for scope in requested_scopes if scope not in BASELINE_SCOPES))
    if denied:
        return IonOAuthTokenDecisionPreview(
            version=VERSION, status=OAuthPreviewStatus.REFUSED, token=None, bearer_preview=None,
            granted_scopes=(), denied_scopes=requested_scopes,
            denied_reasons=tuple(denied), created_at=_utc_now(),
        )
    token = mint_access_token_preview(
        subject_id=str(code_obj.subject_id),
        workspace_ids=(str(code_obj.workspace_id),),
        scopes=granted_scopes or BASELINE_SCOPES,
        audience=TOKEN_AUDIENCE,
    )
    return IonOAuthTokenDecisionPreview(
        version=VERSION, status=OAuthPreviewStatus.TOKEN_ISSUED,
        token=token.to_dict() if hasattr(token, "to_dict") else asdict(token),
        bearer_preview=make_bearer_preview(token),
        granted_scopes=granted_scopes, denied_scopes=denied_scopes,
        denied_reasons=(), created_at=_utc_now(),
    )


def make_bearer_preview(token: IonHostedAccessTokenPreview | Mapping[str, Any]) -> str:
    token_obj = token if isinstance(token, IonHostedAccessTokenPreview) else IonHostedAccessTokenPreview(**dict(token))
    return f"{PREVIEW_BEARER_PREFIX}:{token_obj.token_id}:{token_obj.token_hash[:16]}"


def validate_bearer_preview(
    authorization_header: str | None,
    token: IonHostedAccessTokenPreview | Mapping[str, Any],
) -> tuple[bool, str | None]:
    token_obj = token if isinstance(token, IonHostedAccessTokenPreview) else IonHostedAccessTokenPreview(**dict(token))
    expected = "Bearer " + make_bearer_preview(token_obj)
    if not authorization_header:
        return False, "missing Authorization bearer header"
    if authorization_header != expected:
        return False, "Authorization bearer preview does not match token preview"
    if token_obj.audience != TOKEN_AUDIENCE:
        return False, "token audience is not accepted for hosted MCP preview"
    if token_obj.raw_token_stored:
        return False, "raw token storage is forbidden"
    return True, None


def _extract_tool_result(response: Mapping[str, Any] | None) -> dict[str, Any] | None:
    try:
        if not isinstance(response, Mapping):
            return None
        result = response.get("result")
        if not isinstance(result, Mapping):
            return None
        content = result.get("content")
        if not isinstance(content, list) or not content:
            return None
        text = content[0].get("text")
        if not isinstance(text, str):
            return None
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else None
    except Exception:
        return None


def _status_from_tool_response(response: Mapping[str, Any] | None) -> IonMcpExecutionResolution:
    parsed = _extract_tool_result(response)
    resolution = parsed.get("execution_resolution") if parsed else None
    if resolution in ALLOWED_RESOLUTIONS:
        return IonMcpExecutionResolution(str(resolution))
    return IonMcpExecutionResolution.REFUSED


def _jsonrpc_message(message_id: int, method: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "id": message_id, "method": method}
    if params is not None:
        payload["params"] = dict(params)
    return payload


def handle_hosted_streamable_http_oauth_preview_request(
    http_request: IonHostedHttpPreviewRequest | Mapping[str, Any],
    *,
    ion_root: str | Path | None = None,
    account: IonHostedAccount | Mapping[str, Any],
    workspace: IonHostedWorkspace | Mapping[str, Any],
    state_root: IonHostedStateRoot | Mapping[str, Any],
    token: IonHostedAccessTokenPreview | Mapping[str, Any],
) -> IonHostedHttpPreviewResponse:
    req = http_request if isinstance(http_request, IonHostedHttpPreviewRequest) else IonHostedHttpPreviewRequest(**dict(http_request))
    token_obj = token if isinstance(token, IonHostedAccessTokenPreview) else IonHostedAccessTokenPreview(**dict(token))
    denied: list[str] = []
    if req.method.upper() != "POST":
        denied.append("only POST is accepted in V70 preview")
    if req.path != HOSTED_HTTP_PATH:
        denied.append("path must be /mcp")
    ok_bearer, bearer_reason = validate_bearer_preview(req.headers.get("Authorization"), token_obj)
    if not ok_bearer and bearer_reason:
        denied.append(bearer_reason)
    if denied:
        return IonHostedHttpPreviewResponse(
            version=VERSION, status=HostedHttpPreviewStatus.REFUSED,
            http_status=401 if any("Authorization" in reason or "bearer" in reason for reason in denied) else 400,
            mcp_transport_session_id=req.mcp_transport_session_id, jsonrpc_response=None,
            hosted_mount_decision=None, denied_reasons=tuple(denied),
            execution_resolution=IonMcpExecutionResolution.REFUSED, created_at=_utc_now(),
        )

    body = dict(req.body)
    method = str(body.get("method", ""))
    params = body.get("params") if isinstance(body.get("params"), Mapping) else {}
    mount_decision_dict: dict[str, Any] | None = None
    if method == "tools/call" and isinstance(params, Mapping) and params.get("name") == "ion.mount":
        args = params.get("arguments") if isinstance(params.get("arguments"), Mapping) else {}
        account_id = account.account_id if isinstance(account, IonHostedAccount) else dict(account)["account_id"]
        workspace_id = workspace.workspace_id if isinstance(workspace, IonHostedWorkspace) else dict(workspace)["workspace_id"]
        mount_request = IonHostedMountRequest(
            account_id=account_id,
            subject_id=token_obj.subject_id,
            workspace_id=workspace_id,
            client_name=str(args.get("client_name", "v70-hosted-oauth-preview-client")),
            transport="streamable-http-oauth-preview",
            requested_mode=str(args.get("requested_mode", "dry_run")),
            requested_scopes=tuple(sorted(set(args.get("requested_scopes", token_obj.scopes)))),
            token_audience=token_obj.audience,
            token_subject_id=token_obj.subject_id,
            token_workspace_ids=token_obj.workspace_ids,
            mcp_transport_session_id=req.mcp_transport_session_id,
        )
        decision = evaluate_hosted_alpha_mount(
            mount_request, account=account, workspace=workspace, state_root=state_root, token=token_obj
        )
        mount_decision_dict = decision.to_dict()
        if decision.live_execution_authorized:
            return IonHostedHttpPreviewResponse(
                version=VERSION, status=HostedHttpPreviewStatus.REFUSED, http_status=403,
                mcp_transport_session_id=req.mcp_transport_session_id, jsonrpc_response=None,
                hosted_mount_decision=mount_decision_dict,
                denied_reasons=("hosted mount attempted to authorize live execution",),
                execution_resolution=IonMcpExecutionResolution.REFUSED, created_at=_utc_now(),
                live_execution_authorized=True,
            )

    with tempfile.TemporaryDirectory(prefix="ion_mcp_oauth_preview_") as preview_state:
        bridge = IonMcpLocalBridge(Path(ion_root or "."), Path(preview_state) / "local_bridge")
        response = handle_jsonrpc_message(bridge, body)
    resolution = _status_from_tool_response(response)
    if str(resolution) == FORBIDDEN_LIVE_RESOLUTION:
        return IonHostedHttpPreviewResponse(
            version=VERSION, status=HostedHttpPreviewStatus.REFUSED, http_status=403,
            mcp_transport_session_id=req.mcp_transport_session_id, jsonrpc_response=response,
            hosted_mount_decision=mount_decision_dict,
            denied_reasons=("forbidden live execution resolution observed",),
            execution_resolution=IonMcpExecutionResolution.REFUSED, created_at=_utc_now(),
            live_execution_authorized=True,
        )
    return IonHostedHttpPreviewResponse(
        version=VERSION, status=HostedHttpPreviewStatus.OK, http_status=200,
        mcp_transport_session_id=req.mcp_transport_session_id, jsonrpc_response=response,
        hosted_mount_decision=mount_decision_dict, denied_reasons=(),
        execution_resolution=resolution, created_at=_utc_now(),
    )


def build_v70_oauth_http_preview_report(ion_root: str | Path | None = None) -> dict[str, Any]:
    account, workspace, state_root, _old_token = build_fixture_hosted_account_workspace()
    verifier = "v70-local-preview-verifier-" + secrets.token_hex(6)
    auth_request = IonOAuthAuthorizationRequestPreview(
        client_id="ion-v70-preview-client",
        redirect_uri="http://localhost:7341/oauth/callback",
        subject_id=account.subject_id,
        workspace_id=workspace.workspace_id,
        requested_scopes=tuple(sorted(BASELINE_SCOPES | {"ion.jobs.execute.live", "ion.secrets.write"})),
        code_challenge=_b64url_digest(verifier),
    )
    auth_code = issue_authorization_code_preview(auth_request, account=account, workspace=workspace)
    token_decision = exchange_authorization_code_preview(
        auth_code,
        IonOAuthTokenRequestPreview(
            grant_type="authorization_code",
            authorization_code_id=str(auth_code.authorization_code_id),
            client_id=str(auth_code.client_id),
            redirect_uri=str(auth_code.redirect_uri),
            code_verifier=verifier,
            requested_scopes=auth_code.requested_scopes,
        ),
    )
    token = IonHostedAccessTokenPreview(**dict(token_decision.token or {})) if token_decision.token else None
    bearer = token_decision.bearer_preview
    sequence: list[dict[str, Any]] = []
    forbidden_resolution_seen = False
    live_execution_authorized_seen = False
    kernel_truth_mutation_seen = False

    if token and bearer:
        calls = (
            ("initialize", {}),
            ("tools/list", {}),
            ("tools/call", {"name": "ion.mount", "arguments": {
                "client_name": "v70-hosted-oauth-preview",
                "transport": "streamable-http-oauth-preview",
                "requested_mode": "dry_run",
                "requested_scopes": tuple(sorted(BASELINE_SCOPES)),
            }}),
            ("tools/call", {"name": "ion.status", "arguments": {}}),
            ("tools/call", {"name": "ion.job.plan", "arguments": {"task": {"summary": "V70 OAuth HTTP preview plan"}}}),
            ("tools/call", {"name": "ion.job.submit_dry_run", "arguments": {"task": {"summary": "V70 OAuth HTTP preview dry-run"}}}),
            ("tools/call", {"name": "ion.job.execute_live", "arguments": {"task": {"summary": "V70 must refuse live execution"}}}),
        )
        for i, (method, params) in enumerate(calls, start=1):
            http_resp = handle_hosted_streamable_http_oauth_preview_request(
                IonHostedHttpPreviewRequest(
                    method="POST", path=HOSTED_HTTP_PATH,
                    headers={"Authorization": "Bearer " + bearer, "Content-Type": "application/json"},
                    body=_jsonrpc_message(i, method, params),
                    mcp_transport_session_id="mcp_http_preview_session_v70",
                ),
                ion_root=ion_root, account=account, workspace=workspace, state_root=state_root, token=token,
            )
            entry = http_resp.to_dict()
            sequence.append(entry)
            if entry["execution_resolution"] not in ALLOWED_RESOLUTIONS:
                forbidden_resolution_seen = True
            if entry.get("live_execution_authorized"):
                live_execution_authorized_seen = True
            parsed = _extract_tool_result(entry.get("jsonrpc_response") if isinstance(entry.get("jsonrpc_response"), Mapping) else None)
            if parsed and parsed.get("kernel_truth_mutated"):
                kernel_truth_mutation_seen = True

    wrong_verifier_decision = exchange_authorization_code_preview(
        auth_code,
        IonOAuthTokenRequestPreview(
            grant_type="authorization_code",
            authorization_code_id=str(auth_code.authorization_code_id),
            client_id=str(auth_code.client_id),
            redirect_uri=str(auth_code.redirect_uri),
            code_verifier="wrong-verifier",
            requested_scopes=auth_code.requested_scopes,
        ),
    )
    missing_bearer_response = None
    if token:
        missing_bearer_response = handle_hosted_streamable_http_oauth_preview_request(
            IonHostedHttpPreviewRequest(
                method="POST", path=HOSTED_HTTP_PATH,
                headers={"Content-Type": "application/json"},
                body=_jsonrpc_message(99, "tools/list", {}),
                mcp_transport_session_id="mcp_http_preview_session_v70_missing_bearer",
            ),
            ion_root=ion_root, account=account, workspace=workspace, state_root=state_root, token=token,
        ).to_dict()

    passed = (
        auth_code.status == OAuthPreviewStatus.AUTHORIZED
        and token_decision.status == OAuthPreviewStatus.TOKEN_ISSUED
        and wrong_verifier_decision.status == OAuthPreviewStatus.REFUSED
        and missing_bearer_response is not None
        and missing_bearer_response["status"] == str(HostedHttpPreviewStatus.REFUSED)
        and not forbidden_resolution_seen
        and not live_execution_authorized_seen
        and not kernel_truth_mutation_seen
    )
    return {
        "version": VERSION,
        "generated_at": _utc_now(),
        "passed": passed,
        "hosted_streamable_http_previewed": True,
        "oauth_authorization_code_pkce_previewed": True,
        "oauth_certified": False,
        "hosted_cloud_certified": False,
        "public_endpoint_certified": False,
        "kubernetes_certified": False,
        "live_execution_authorized_seen": live_execution_authorized_seen,
        "kernel_truth_mutation_seen": kernel_truth_mutation_seen,
        "forbidden_resolution_seen": forbidden_resolution_seen,
        "token_is_session": False,
        "transport_session_is_authority": False,
        "authorization_code": auth_code.to_dict(),
        "token_decision": token_decision.to_dict(),
        "wrong_verifier_decision": wrong_verifier_decision.to_dict(),
        "missing_bearer_response": missing_bearer_response,
        "sequence": sequence,
        "allowed_resolutions": tuple(sorted(ALLOWED_RESOLUTIONS)),
        "forbidden_tools": tuple(sorted(FORBIDDEN_TOOL_NAMES)),
        "next_required_action": "Use this preview to build a real hosted endpoint only after OAuth provider, storage, and tenant isolation choices are explicitly approved.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run V70 hosted OAuth + Streamable HTTP preview boundary report.")
    parser.add_argument("--ion-root", default="ION")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = build_v70_oauth_http_preview_report(Path(args.ion_root))
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{VERSION}: passed={report['passed']}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
