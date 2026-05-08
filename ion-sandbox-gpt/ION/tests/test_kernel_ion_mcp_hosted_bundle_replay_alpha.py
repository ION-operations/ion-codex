from kernel.ion_mcp_hosted_bundle_replay_alpha import (
    ALLOWED_RESOLUTIONS,
    build_fixture_ledger,
    export_bundle_preview,
    validate_bundle_import,
    build_replay_plan,
    tamper_bundle,
    build_bundle_replay_alpha_report,
)


def test_v72_exports_preview_only_bundle():
    ledger = build_fixture_ledger()
    envelope = export_bundle_preview(ledger)
    assert envelope.manifest.export_is_preview_only is True
    assert envelope.manifest.production_bundle_certified is False
    assert envelope.live_execution_authorized is False
    assert envelope.kernel_truth_mutated is False
    assert envelope.manifest_hash.startswith("sha256:")


def test_v72_import_accepts_valid_bundle_and_verifies_chain():
    ledger = build_fixture_ledger()
    envelope = export_bundle_preview(ledger)
    result = validate_bundle_import(
        envelope,
        expected_workspace_id=ledger.workspace.workspace_id,
        expected_state_root_id=ledger.state_root.state_root_id,
    )
    assert result.accepted is True
    assert result.event_chain_verified is True
    assert result.manifest_hash_verified is True
    assert result.preview_only_verified is True
    assert result.live_execution_authorized_seen is False


def test_v72_replay_plan_is_preview_only_and_non_mutating():
    envelope = export_bundle_preview(build_fixture_ledger())
    plan = build_replay_plan(envelope)
    assert plan.replay_is_preview_only is True
    assert plan.replay_committed is False
    assert plan.kernel_truth_mutated is False
    assert plan.live_execution_authorized is False
    assert all(step.action != "EXECUTE" for step in plan.steps)
    assert all(step.execution_resolution in ALLOWED_RESOLUTIONS for step in plan.steps)


def test_v72_refuses_tampered_live_bundle():
    ledger = build_fixture_ledger()
    envelope = export_bundle_preview(ledger)
    tampered = tamper_bundle(envelope)
    result = validate_bundle_import(
        tampered,
        expected_workspace_id=ledger.workspace.workspace_id,
        expected_state_root_id=ledger.state_root.state_root_id,
    )
    assert result.accepted is False
    assert result.live_execution_authorized_seen is True
    assert result.forbidden_resolution_seen is True
    assert result.forbidden_event_seen is True
    assert any("live execution" in reason for reason in result.denied_reasons)


def test_v72_boundary_report_passes_without_live_execution():
    report = build_bundle_replay_alpha_report()
    assert report.passed is True
    assert report.import_accepted is True
    assert report.tamper_refusal_verified is True
    assert report.live_execution_authorized_seen is False
    assert report.kernel_truth_mutation_seen is False
    assert report.forbidden_resolution_seen is False
    assert report.forbidden_event_seen is False
    assert report.production_bundle_certified is False
