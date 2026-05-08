import json
from pathlib import Path

from kernel.ion_carrier_onboard import onboard_carrier
from kernel.ion_carrier_continue import continue_carrier
from kernel.ion_carrier_onboarding_packet import build_carrier_onboarding_packet
from kernel.ion_github_data_plane_audit import audit_github_data_plane
from kernel.ion_status import build_ion_status
from kernel.ion_sandbox_preflight import build_gpt_sandbox_preflight


def _repo_root() -> Path:
    root = Path.cwd()
    assert (root / "pyproject.toml").exists()
    assert (root / "ION/REPO_AUTHORITY.md").exists()
    return root


def test_gpt_sandbox_package_root_markers_and_status_ready():
    root = _repo_root()

    required = [
        "PRODUCT_MANIFEST.json",
        "VALIDATION_REPORT.json",
        "product/custom_gpt_adapter/CUSTOM_GPT_INSTRUCTIONS_8000.md",
        "product/custom_gpt_adapter/knowledge_manifest.json",
        "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
        "ION/07_templates/carriers/GPT_SANDBOX_CARRIER_SESSION_PACKET.md",
        "product/starter_data/ION_DATA_MANIFEST.json",
    ]
    for rel in required:
        assert (root / rel).exists(), rel

    status = build_ion_status(root)
    assert status["verdict"] == "ION_STATUS_READY"
    assert status["production_authority"] is False
    assert status["live_execution_authority"] is False
    assert status.get("missing_state_surfaces") == []


def test_gpt_sandbox_carrier_alias_mounts_sandbox_profile_and_template():
    root = _repo_root()

    packet = build_carrier_onboarding_packet(root, carrier_id="GPT_SANDBOX_CARRIER")
    assert packet["root_confirmed"] is True
    assert packet["onboarding_verdict"] == "ION_CARRIER_ONBOARDING_PACKET_READY"
    assert packet["carrier_profile"]["path"] == "ION/03_registry/gpt_sandbox_carrier_profile.yaml"
    assert packet["carrier_profile_metadata"]["carrier_id"] == "GPT_SANDBOX_CARRIER"
    assert packet["carrier_profile_metadata"]["production_authority"] is False
    assert packet["carrier_profile_metadata"]["live_execution_authority"] is False

    template_paths = {item["path"] for item in packet["execution_packet_templates"]}
    assert "ION/07_templates/carriers/GPT_SANDBOX_CARRIER_SESSION_PACKET.md" in template_paths


def test_gpt_sandbox_active_work_packet_uses_registry_capabilities():
    root = _repo_root()

    result = onboard_carrier(
        root,
        carrier="GPT_SANDBOX_CARRIER",
        objective="verify GPT sandbox capability projection",
        force=True,
    )

    caps = result["packet"]["carrier_capabilities"]
    assert result["onboarding_verdict"] == "ION_DEFAULT_CARRIER_ONBOARDING_READY"
    assert caps["carrier"] == "GPT_SANDBOX_CARRIER"
    assert caps["can_read_files"] is True
    assert caps["can_edit_files"] is True
    assert caps["can_run_tests"] is True
    assert caps["can_spawn_carrier_slots"] is False
    assert caps["can_use_mcp"] is False
    assert caps["production_authority"] is False
    assert caps["live_execution_authority"] is False


def test_gpt_sandbox_continue_defaults_to_sandbox_mode_label():
    root = _repo_root()

    result = continue_carrier(
        root,
        carrier="GPT_SANDBOX_CARRIER",
        operator_message="status",
        max_spawn_rows=0,
    )

    assert result["mode"] == "gpt-sandbox"
    assert result["production_authority"] is False
    assert result["live_execution_authority"] is False


def test_starter_data_seeded_domains_validate():
    root = _repo_root()
    manifest = json.loads((root / "product/starter_data/ION_DATA_MANIFEST.json").read_text(encoding="utf-8"))
    domains = json.loads((root / "product/starter_data/DOMAINS/domain_registry.json").read_text(encoding="utf-8"))
    context = json.loads((root / "product/starter_data/CONTEXT/context_graph.json").read_text(encoding="utf-8"))
    persona = json.loads((root / "product/starter_data/PERSONA/persona_state.json").read_text(encoding="utf-8"))

    assert manifest["schema_id"] in {"ion.data_manifest.v1", "ion.data_zip_manifest.v1"}
    assert len(domains["domains"]) == 13
    assert len(context["nodes"]) == 13
    assert len(context["edges"]) == 52
    assert persona.get("active", str(persona.get("status", "")).lower() == "active") is True


def test_custom_gpt_knowledge_manifest_paths_exist():
    root = _repo_root()
    manifest = json.loads((root / "product/custom_gpt_adapter/knowledge_manifest.json").read_text(encoding="utf-8"))

    path_groups = [
        "adapter_docs",
        "operational_root_surfaces",
        "starter_data",
        "product_docs",
        "source_reference_docs",
        "added_surfaces",
    ]
    for group in path_groups:
        for rel in manifest[group]:
            assert (root / rel).exists(), f"{group}: {rel}"


def test_github_data_plane_optional_in_gpt_sandbox_package_without_git():
    root = _repo_root()
    result = audit_github_data_plane(root)

    assert result["network_access_used"] is False
    assert result["github_mutation_performed"] is False
    assert result["git_mutation_performed"] is False
    assert result["commit_authority"] is False
    assert result["push_authority"] is False
    if not result["git"].get("git_present"):
        assert result["product_manifest"]["sandbox_package_mode"] is True
        assert result["failure_classification"] == "GITHUB_DATA_PLANE_ABSENT_BY_PACKAGE_POLICY"
        assert "git_absent_by_gpt_sandbox_package_policy" in result["findings"]



def test_gpt_sandbox_preflight_ready_for_package():
    root = _repo_root()
    report = build_gpt_sandbox_preflight(root, carrier="GPT_SANDBOX_CARRIER")

    assert report["preflight_verdict"] == "ION_GPT_SANDBOX_PREFLIGHT_READY"
    assert report["contract_exists"] is True
    assert report["sandbox_boundary"]["can_export_candidate_zip"] is True
    assert report["sandbox_boundary"]["can_patch_live_repo"] is False
    assert report["sandbox_boundary"]["production_authority"] is False
    assert report["sandbox_boundary"]["live_execution_authority"] is False
