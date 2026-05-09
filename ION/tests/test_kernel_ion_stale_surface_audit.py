import json
from pathlib import Path

from kernel.ion_stale_surface_audit import build_stale_surface_audit, write_stale_surface_audit


def _minimal_root(tmp_path: Path, packet: dict | None = None) -> Path:
    (tmp_path / "pyproject.toml").write_text("[project]\nname = \"test\"\n", encoding="utf-8")
    (tmp_path / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    (tmp_path / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    active = tmp_path / "ION/05_context/current/ACTIVE_WORK_PACKET.json"
    active.parent.mkdir(parents=True, exist_ok=True)
    active.write_text(json.dumps(packet or _good_gpt_packet(), indent=2) + "\n", encoding="utf-8")
    return tmp_path


def _good_gpt_packet() -> dict:
    return {
        "carrier": "GPT_SANDBOX_CARRIER",
        "active_template": "ION/07_templates/carriers/SINGLE_CARRIER_SEQUENTIAL_PACKET.md",
        "role_phase_sequence": [
            "PERSONA_INTERFACE_INGRESS",
            "RELAY",
            "STEWARD",
            "VIZIER",
            "MASON",
            "NEMESIS_OR_VICE_REVIEW",
            "SCRIBE",
            "STEWARD_FINAL",
            "PERSONA_INTERFACE_RESPONSE",
        ],
    }


def test_stale_surface_audit_ready_for_gpt_sandbox(tmp_path: Path):
    root = _minimal_root(tmp_path)
    report = build_stale_surface_audit(root)

    assert report["verdict"] == "ION_STALE_SURFACE_AUDIT_READY"
    assert not [item for item in report["findings"] if item.get("severity") == "block"]
    assert report["active_template"] == "ION/07_templates/carriers/SINGLE_CARRIER_SEQUENTIAL_PACKET.md"
    assert report["phase_sequence"][0] == "PERSONA_INTERFACE_INGRESS"
    assert report["phase_sequence"][-1] == "PERSONA_INTERFACE_RESPONSE"


def test_stale_surface_audit_writes_active_report(tmp_path: Path):
    root = _minimal_root(tmp_path)
    report = write_stale_surface_audit(root)

    assert report["verdict"] == "ION_STALE_SURFACE_AUDIT_READY"
    assert (root / "ION/05_context/current/ACTIVE_STALE_SURFACE_AUDIT.json").exists()


def test_stale_surface_audit_blocks_old_gpt_sandbox_cursor_packet(tmp_path: Path):
    root = _minimal_root(
        tmp_path,
        {
            "carrier": "GPT_SANDBOX_CARRIER",
            "active_template": "ION/docs/cursor/ION_CURSOR_WORK_CYCLE_PACKET.md",
            "role_phase_sequence": ["RELAY", "STEWARD", "RELAY"],
        },
    )

    report = build_stale_surface_audit(root)

    assert report["verdict"] == "ION_STALE_SURFACE_AUDIT_BLOCKED"
    kinds = {item["kind"] for item in report["findings"]}
    assert "gpt_sandbox_cursor_template_default" in kinds
    assert "missing_persona_ingress_phase" in kinds
    assert "missing_persona_response_phase" in kinds


def test_cursor_relay_rule_has_no_manual_gate_fallback_phrase(tmp_path: Path):
    root = _minimal_root(tmp_path)
    rule = root / ".cursor/rules/ion-carrier-relay-mediation.mdc"
    rule.parent.mkdir(parents=True, exist_ok=True)
    rule.write_text("Manual compliance judgment cannot replace this gate.\n", encoding="utf-8")

    text = (root / ".cursor/rules/ion-carrier-relay-mediation.mdc").read_text(encoding="utf-8")

    assert "Run or manually apply" not in text
    assert "Manual compliance judgment cannot replace this gate." in text
