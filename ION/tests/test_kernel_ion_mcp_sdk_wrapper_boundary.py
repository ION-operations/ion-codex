from __future__ import annotations

from pathlib import Path

from kernel.ion_mcp_sdk_wrapper_boundary import (
    ALLOWED_RESOLUTIONS,
    HOSTED_ALPHA_ENDPOINT,
    VERSION,
    build_hosted_http_alpha_boundary_report,
    build_sdk_wrapper_decision,
    build_hosted_http_alpha_profile,
)


def test_v68_sdk_decision_keeps_local_bridge_canonical() -> None:
    decision = build_sdk_wrapper_decision()
    assert decision.version == VERSION
    assert decision.local_bridge_remains_canonical is True
    assert decision.official_sdk_required_for_local is False
    assert decision.live_execution_authorized is False
    assert decision.hosted_cloud_certified is False
    assert decision.oauth_certified is False


def test_v68_hosted_http_alpha_profile_is_not_public_certification() -> None:
    profile = build_hosted_http_alpha_profile()
    assert profile.endpoint_path == HOSTED_ALPHA_ENDPOINT
    assert profile.public_hosting_certified is False
    assert profile.oauth_certified is False
    assert profile.tls_required_before_public_exposure is True
    assert "LIVE_EXECUTED" not in set(profile.allowed_resolutions)


def test_v68_boundary_report_passes_without_live_authority(tmp_path: Path) -> None:
    ion_root = Path(__file__).resolve().parents[1]
    report = build_hosted_http_alpha_boundary_report(ion_root, tmp_path / "state")
    assert report.version == VERSION
    assert report.passed is True
    assert report.hosted_cloud_certified is False
    assert report.oauth_certified is False
    assert report.public_endpoint_certified is False
    assert report.official_sdk_runtime_required is False
    assert report.forbidden_resolution_seen is False
    assert report.live_execution_authorized_seen is False
    assert report.kernel_truth_mutation_seen is False
    assert set(report.allowed_resolutions) == set(ALLOWED_RESOLUTIONS)
    assert report.tool_contracts
    assert all(contract.live_execution_authorized is False for contract in report.tool_contracts)


def test_v68_boundary_report_refuses_live_paths(tmp_path: Path) -> None:
    ion_root = Path(__file__).resolve().parents[1]
    report = build_hosted_http_alpha_boundary_report(ion_root, tmp_path / "state")
    refusal_steps = [step for step in report.steps if step.execution_resolution == "REFUSED"]
    assert refusal_steps
    assert any("execute_live" in step.method for step in refusal_steps)
    assert any("provider.dispatch" in step.method for step in refusal_steps)
    assert any("live_candidate" in step.method for step in refusal_steps)
    assert all(step.live_execution_authorized is False for step in refusal_steps)
    assert all(step.kernel_truth_mutated is False for step in refusal_steps)


def test_v68_report_serializes_to_dict(tmp_path: Path) -> None:
    ion_root = Path(__file__).resolve().parents[1]
    report = build_hosted_http_alpha_boundary_report(ion_root, tmp_path / "state")
    payload = report.to_dict()
    assert payload["version"] == VERSION
    assert payload["passed"] is True
    assert payload["hosted_cloud_certified"] is False
    assert payload["oauth_certified"] is False
    assert payload["live_execution_authorized_seen"] is False
