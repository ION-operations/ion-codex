from pathlib import Path

from kernel.ion_sandbox_preflight import (
    SANDBOX_ENVIRONMENT_CONTRACT_RELATIVE_PATH,
    build_gpt_sandbox_preflight,
    write_gpt_sandbox_preflight,
)


def _repo_root() -> Path:
    root = Path.cwd()
    assert (root / "pyproject.toml").exists()
    assert (root / "ION/REPO_AUTHORITY.md").exists()
    return root


def test_gpt_sandbox_environment_contract_exists():
    root = _repo_root()
    assert (root / SANDBOX_ENVIRONMENT_CONTRACT_RELATIVE_PATH).exists()


def test_gpt_sandbox_preflight_reconciles_current_package_ready():
    root = _repo_root()
    report = build_gpt_sandbox_preflight(root, carrier="GPT_SANDBOX_CARRIER")

    assert report["preflight_verdict"] == "ION_GPT_SANDBOX_PREFLIGHT_READY"
    assert report["shell_root_confirmed"] is True
    assert report["contract_exists"] is True
    assert report["carrier_profile_exists"] is True
    assert report["active_work_packet_exists"] is True
    assert report["sandbox_boundary"]["can_edit_sandbox_copy"] is True
    assert report["sandbox_boundary"]["can_export_candidate_zip"] is True
    assert report["sandbox_boundary"]["can_patch_live_repo"] is False
    assert report["sandbox_boundary"]["can_push_git"] is False
    assert report["sandbox_boundary"]["production_authority"] is False
    assert report["sandbox_boundary"]["live_execution_authority"] is False
    assert not [item for item in report["capability_findings"] if item.get("severity") == "block"]


def test_gpt_sandbox_preflight_blocks_authority_inflation():
    root = _repo_root()
    report = build_gpt_sandbox_preflight(
        root,
        carrier="GPT_SANDBOX_CARRIER",
        host_observed_capabilities={"production_authority": True},
    )

    assert report["preflight_verdict"] == "ION_GPT_SANDBOX_PREFLIGHT_BLOCKED"
    assert any(item["kind"] == "authority_not_false" for item in report["capability_findings"])


def test_gpt_sandbox_preflight_write_outputs_active_report():
    root = _repo_root()
    report = write_gpt_sandbox_preflight(root, carrier="GPT_SANDBOX_CARRIER")

    output_rel = report["preflight_report_path"]
    assert output_rel == "ION/05_context/current/ACTIVE_GPT_SANDBOX_PREFLIGHT.json"
    assert (root / output_rel).exists()
