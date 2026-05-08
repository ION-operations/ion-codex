from __future__ import annotations

from pathlib import Path

from kernel.ion_mcp_client_certification import (
    DEFAULT_CLIENT_PROFILES,
    FORBIDDEN_BASELINE_TOOLS,
    REQUIRED_BASELINE_TOOLS,
    certify_all_clients,
)


def _ion_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_v66_profiles_include_expected_local_clients() -> None:
    profile_ids = {profile.profile_id for profile in DEFAULT_CLIENT_PROFILES}
    assert "generic_stdio" in profile_ids
    assert "cursor_local_stdio" in profile_ids
    assert "vscode_local_stdio" in profile_ids
    assert "codex_local_stdio" in profile_ids


def test_v66_baseline_tool_contract_has_required_and_forbidden_names() -> None:
    assert "ion.mount" in REQUIRED_BASELINE_TOOLS
    assert "ion.job.submit_dry_run" in REQUIRED_BASELINE_TOOLS
    assert "ion.job.execute_live" in FORBIDDEN_BASELINE_TOOLS
    assert "ion.shell.run" in FORBIDDEN_BASELINE_TOOLS
    assert "ion.provider.dispatch" in FORBIDDEN_BASELINE_TOOLS


def test_v66_certifies_local_profiles_without_live_authority(tmp_path: Path) -> None:
    report = certify_all_clients(_ion_root(), state_store_root=tmp_path)
    assert report.passed
    assert not report.forbidden_resolution_seen
    assert not report.live_execution_authorized_seen
    assert not report.kernel_truth_mutation_seen
    assert not report.live_client_attestation
    assert not report.hosted_chatgpt_certified
    assert {profile.profile.profile_id for profile in report.profiles} == {
        "generic_stdio",
        "cursor_local_stdio",
        "vscode_local_stdio",
        "codex_local_stdio",
    }
