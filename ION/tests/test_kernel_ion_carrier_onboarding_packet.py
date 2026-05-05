from pathlib import Path

from kernel.ion_carrier_onboarding_packet import (
    build_carrier_onboarding_packet,
    write_carrier_onboarding_packet,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    (root / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    (root / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)


def _write(root: Path, rel: str, text: str = "surface\n") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_onboarding_surfaces(root: Path) -> None:
    _write(root, "ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md", "# ION Current Operating Packet\n")
    _write(root, "ION/02_architecture/ION_MOUNT_CONTRACT.md", "# mount contract\n")
    _write(root, "ION/03_registry/chatgpt_browser_carrier_profile.yaml", "carrier_id: CHATGPT_BROWSER_CARRIER\n")
    _write(root, "ION/05_context/current/ACTIVE_WORK_PACKET.json", "{}\n")
    _write(root, "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json", "{}\n")
    _write(root, "ION/03_registry/boots/RELAY.boot.md")
    _write(root, "ION/03_registry/boots/STEWARD.boot.md")
    _write(root, "ION/05_context/current/agent_context_systems/RELAY.context_system.md")
    _write(root, "ION/05_context/current/agent_context_systems/STEWARD.context_system.md")
    _write(root, "ION/05_context/current/execution_cycles/2026-test/01_COMPILED_STEWARD_CONTEXT_BUNDLE.md")
    _write(root, "ION/07_templates/carriers/CARRIER_MOUNT_PROOF.md")
    _write(root, "ION/07_templates/carriers/CARRIER_SESSION_PACKET.md")
    _write(root, "ION/07_templates/carriers/CHATGPT_BROWSER_CONNECTOR_SESSION_PACKET.md")


def test_carrier_onboarding_packet_uses_ion_native_order_not_root_markdown(tmp_path):
    _seed_root(tmp_path)
    _seed_onboarding_surfaces(tmp_path)
    (tmp_path / "START_HERE_FOR_ANY_AGENT.md").write_text("stale start here\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("stale agents\n", encoding="utf-8")

    packet = build_carrier_onboarding_packet(tmp_path, carrier_id="chatgpt_browser")

    assert packet["onboarding_verdict"] == "ION_CARRIER_ONBOARDING_PACKET_READY"
    assert packet["correct_onboarding_order"] == [
        "confirm_shell_root",
        "read_current_operating_packet",
        "resolve_carrier_identity_from_profile",
        "load_mount_contract",
        "load_active_packets",
        "load_role_context_surfaces_and_compiled_bundles",
        "load_execution_packet_templates",
        "execute_context_proof_template_action_proof_task_return_receipt_flow",
    ]
    assert packet["current_operating_packet"]["path"] == "ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md"
    assert packet["carrier_profile"]["path"] == "ION/03_registry/chatgpt_browser_carrier_profile.yaml"
    assert packet["mount_contract"]["path"] == "ION/02_architecture/ION_MOUNT_CONTRACT.md"
    assert packet["root_markdown_onboarding_authority"] is False
    assert packet["root_markdown_status"]["START_HERE_FOR_ANY_AGENT.md"]["exists"] is True
    assert packet["root_markdown_status"]["START_HERE_FOR_ANY_AGENT.md"]["authority"] is False
    assert "root_markdown_present_but_not_onboarding_authority" in packet["findings"]
    assert packet["production_authority"] is False
    assert packet["live_execution_authority"] is False


def test_carrier_onboarding_packet_records_active_packets_templates_and_proof_flow(tmp_path):
    _seed_root(tmp_path)
    _seed_onboarding_surfaces(tmp_path)

    packet = build_carrier_onboarding_packet(tmp_path, carrier_id="chatgpt_browser")

    assert any(surface["path"] == "ION/05_context/current/ACTIVE_WORK_PACKET.json" for surface in packet["active_packets"])
    assert any(surface["path"].endswith("COMPILED_STEWARD_CONTEXT_BUNDLE.md") for surface in packet["compiled_context_bundles"])
    assert any(surface["path"] == "ION/07_templates/carriers/CHATGPT_BROWSER_CONNECTOR_SESSION_PACKET.md" for surface in packet["execution_packet_templates"])
    assert [step["step"] for step in packet["proof_flow"]] == [
        "context_proof",
        "template_action_proof",
        "task_return_intake",
        "receipt_flow",
    ]


def test_carrier_onboarding_packet_resolves_sev_callsign_alias(tmp_path):
    _seed_root(tmp_path)
    _seed_onboarding_surfaces(tmp_path)
    _write(
        tmp_path,
        "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
        "\n".join([
            "carrier_id: CHATGPT_BROWSER_CARRIER",
            "project_facing_callsign: Sev",
            "callsign_authority: carrier_continuity_label_only_not_ion_authority",
            "callsign_decision_receipt: ION/05_context/current/chatgpt_connector/decisions/decision.json",
            "",
        ]),
    )

    packet = build_carrier_onboarding_packet(tmp_path, carrier_id="sev")

    assert packet["carrier_profile"]["path"] == "ION/03_registry/chatgpt_browser_carrier_profile.yaml"
    assert packet["carrier_profile_metadata"]["carrier_id"] == "CHATGPT_BROWSER_CARRIER"
    assert packet["carrier_profile_metadata"]["project_facing_callsign"] == "Sev"
    assert packet["carrier_profile_metadata"]["callsign_authority"] == "carrier_continuity_label_only_not_ion_authority"


def test_write_carrier_onboarding_packet_writes_active_current_packet(tmp_path):
    _seed_root(tmp_path)
    _seed_onboarding_surfaces(tmp_path)

    packet = write_carrier_onboarding_packet(tmp_path, carrier_id="chatgpt_browser")

    out = tmp_path / "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json"
    assert out.exists()
    assert packet["schema_id"] == "ion.carrier_onboarding_packet.v1"
    assert "ION_CARRIER_ONBOARDING_PACKET_READY" in out.read_text(encoding="utf-8")
