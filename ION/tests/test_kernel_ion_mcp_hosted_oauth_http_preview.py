from __future__ import annotations

from pathlib import Path

from kernel.ion_mcp_hosted_auth_alpha import (
    BASELINE_SCOPES,
    TOKEN_AUDIENCE,
    IonHostedAccessTokenPreview,
    build_fixture_hosted_account_workspace,
)
from kernel.ion_mcp_hosted_oauth_http_preview import (
    HOSTED_HTTP_PATH,
    OAuthPreviewStatus,
    HostedHttpPreviewStatus,
    IonHostedHttpPreviewRequest,
    IonOAuthAuthorizationRequestPreview,
    IonOAuthTokenRequestPreview,
    _b64url_digest,
    _jsonrpc_message,
    build_v70_oauth_http_preview_report,
    exchange_authorization_code_preview,
    handle_hosted_streamable_http_oauth_preview_request,
    issue_authorization_code_preview,
)


def test_v70_oauth_pkce_preview_issues_token_without_raw_token_storage():
    account, workspace, _state_root, _token = build_fixture_hosted_account_workspace()
    verifier = "unit-test-verifier"
    auth_code = issue_authorization_code_preview(
        IonOAuthAuthorizationRequestPreview(
            client_id="client",
            redirect_uri="http://localhost/callback",
            subject_id=account.subject_id,
            workspace_id=workspace.workspace_id,
            requested_scopes=tuple(sorted(BASELINE_SCOPES | {"ion.jobs.execute.live"})),
            code_challenge=_b64url_digest(verifier),
        ),
        account=account,
        workspace=workspace,
    )
    assert auth_code.status == OAuthPreviewStatus.AUTHORIZED
    token_decision = exchange_authorization_code_preview(
        auth_code,
        IonOAuthTokenRequestPreview(
            grant_type="authorization_code",
            authorization_code_id=str(auth_code.authorization_code_id),
            client_id="client",
            redirect_uri="http://localhost/callback",
            code_verifier=verifier,
            requested_scopes=auth_code.requested_scopes,
        ),
    )
    assert token_decision.status == OAuthPreviewStatus.TOKEN_ISSUED
    assert token_decision.raw_token_stored is False
    assert token_decision.live_execution_authorized is False
    assert "ion.jobs.execute.live" in token_decision.denied_scopes
    assert token_decision.token is not None
    token = IonHostedAccessTokenPreview(**dict(token_decision.token))
    assert token.audience == TOKEN_AUDIENCE
    assert token.raw_token_stored is False


def test_v70_wrong_pkce_verifier_is_refused():
    account, workspace, _state_root, _token = build_fixture_hosted_account_workspace()
    auth_code = issue_authorization_code_preview(
        IonOAuthAuthorizationRequestPreview(
            client_id="client",
            redirect_uri="http://localhost/callback",
            subject_id=account.subject_id,
            workspace_id=workspace.workspace_id,
            requested_scopes=tuple(sorted(BASELINE_SCOPES)),
            code_challenge=_b64url_digest("right-verifier"),
        ),
        account=account,
        workspace=workspace,
    )
    denied = exchange_authorization_code_preview(
        auth_code,
        IonOAuthTokenRequestPreview(
            grant_type="authorization_code",
            authorization_code_id=str(auth_code.authorization_code_id),
            client_id="client",
            redirect_uri="http://localhost/callback",
            code_verifier="wrong-verifier",
            requested_scopes=auth_code.requested_scopes,
        ),
    )
    assert denied.status == OAuthPreviewStatus.REFUSED
    assert denied.token is None


def test_v70_http_preview_requires_bearer_header():
    account, workspace, state_root, token = build_fixture_hosted_account_workspace()
    response = handle_hosted_streamable_http_oauth_preview_request(
        IonHostedHttpPreviewRequest(
            method="POST",
            path=HOSTED_HTTP_PATH,
            headers={"Content-Type": "application/json"},
            body=_jsonrpc_message(1, "tools/list", {}),
        ),
        ion_root=Path("ION"),
        account=account,
        workspace=workspace,
        state_root=state_root,
        token=token,
    )
    assert response.status == HostedHttpPreviewStatus.REFUSED
    assert response.http_status == 401
    assert response.live_execution_authorized is False


def test_v70_report_preserves_no_live_execution_boundary():
    report = build_v70_oauth_http_preview_report(Path("ION"))
    assert report["passed"] is True
    assert report["oauth_certified"] is False
    assert report["hosted_cloud_certified"] is False
    assert report["public_endpoint_certified"] is False
    assert report["kubernetes_certified"] is False
    assert report["live_execution_authorized_seen"] is False
    assert report["kernel_truth_mutation_seen"] is False
    assert report["forbidden_resolution_seen"] is False
    assert report["token_is_session"] is False
    assert report["transport_session_is_authority"] is False
