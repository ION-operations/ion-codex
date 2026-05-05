from kernel.ion_mcp_hosted_auth_alpha import (
    BASELINE_SCOPES,
    IonHostedMountRequest,
    TOKEN_AUDIENCE,
    build_fixture_hosted_account_workspace,
    build_hosted_alpha_boundary_report,
    evaluate_hosted_alpha_mount,
    mint_access_token_preview,
)


def test_v69_boundary_report_passes_without_live_authority():
    report = build_hosted_alpha_boundary_report("ION")
    assert report["passed"] is True
    assert report["oauth_certified"] is False
    assert report["hosted_cloud_certified"] is False
    assert report["public_endpoint_certified"] is False
    assert report["live_execution_authorized_seen"] is False
    assert report["kernel_truth_mutation_seen"] is False
    assert report["token_session_separation_verified"] is True
    assert report["transport_session_authority_separation_verified"] is True


def test_v69_accepts_baseline_dry_run_mount_only():
    account, workspace, state_root, token = build_fixture_hosted_account_workspace()
    decision = evaluate_hosted_alpha_mount(
        IonHostedMountRequest(
            account_id=account.account_id,
            subject_id=account.subject_id,
            workspace_id=workspace.workspace_id,
            token_subject_id=token.subject_id,
            token_workspace_ids=token.workspace_ids,
            requested_mode="dry_run",
            requested_scopes=tuple(sorted(BASELINE_SCOPES)),
        ),
        account=account,
        workspace=workspace,
        state_root=state_root,
        token=token,
    )
    assert str(decision.status) == "ACCEPTED"
    assert str(decision.execution_resolution) == "DRY_RUN"
    assert decision.session is not None
    assert decision.session["token_is_session"] is False
    assert decision.session["transport_session_is_authority"] is False
    assert decision.session["live_execution_authorized"] is False


def test_v69_refuses_wrong_token_audience():
    account, workspace, state_root, _token = build_fixture_hosted_account_workspace()
    wrong_token = mint_access_token_preview(
        subject_id=account.subject_id,
        workspace_ids=(workspace.workspace_id,),
        scopes=BASELINE_SCOPES,
        audience="wrong-audience",
    )
    decision = evaluate_hosted_alpha_mount(
        IonHostedMountRequest(
            account_id=account.account_id,
            subject_id=account.subject_id,
            workspace_id=workspace.workspace_id,
            token_subject_id=wrong_token.subject_id,
            token_workspace_ids=wrong_token.workspace_ids,
            requested_mode="dry_run",
            requested_scopes=tuple(sorted(BASELINE_SCOPES)),
            token_audience=TOKEN_AUDIENCE,
        ),
        account=account,
        workspace=workspace,
        state_root=state_root,
        token=wrong_token,
    )
    assert str(decision.status) == "REFUSED"
    assert str(decision.execution_resolution) == "REFUSED"
    assert any("audience" in reason for reason in decision.denied_reasons)


def test_v69_live_scope_requires_elevation_not_execution():
    account, workspace, state_root, token = build_fixture_hosted_account_workspace()
    decision = evaluate_hosted_alpha_mount(
        IonHostedMountRequest(
            account_id=account.account_id,
            subject_id=account.subject_id,
            workspace_id=workspace.workspace_id,
            token_subject_id=token.subject_id,
            token_workspace_ids=token.workspace_ids,
            requested_mode="dry_run",
            requested_scopes=tuple(sorted(set(BASELINE_SCOPES) | {"ion.jobs.execute.live"})),
        ),
        account=account,
        workspace=workspace,
        state_root=state_root,
        token=token,
    )
    assert str(decision.status) == "ELEVATION_REQUIRED"
    assert str(decision.execution_resolution) == "APPROVAL_REQUIRED"
    assert "ion.jobs.execute.live" in decision.denied_scopes
    assert decision.session is None
    assert decision.live_execution_authorized is False


def test_v69_refuses_token_identifier_as_session_identifier():
    account, workspace, state_root, token = build_fixture_hosted_account_workspace()
    decision = evaluate_hosted_alpha_mount(
        IonHostedMountRequest(
            account_id=account.account_id,
            subject_id=account.subject_id,
            workspace_id=workspace.workspace_id,
            token_subject_id=token.subject_id,
            token_workspace_ids=token.workspace_ids,
            requested_mode="dry_run",
            requested_scopes=tuple(sorted(BASELINE_SCOPES)),
            resume_session_id=token.token_id,
        ),
        account=account,
        workspace=workspace,
        state_root=state_root,
        token=token,
    )
    assert str(decision.status) == "REFUSED"
    assert any("token identifier" in reason for reason in decision.denied_reasons)
