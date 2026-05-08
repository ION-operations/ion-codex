from pathlib import Path
import json

from kernel.ion_stale_surface_audit import build_stale_surface_audit, write_stale_surface_audit


def _repo_root() -> Path:
    root = Path.cwd()
    assert (root / "pyproject.toml").exists()
    assert (root / "ION/REPO_AUTHORITY.md").exists()
    return root


def test_stale_surface_audit_ready_for_gpt_sandbox():
    root = _repo_root()
    report = build_stale_surface_audit(root)

    assert report["verdict"] == "ION_STALE_SURFACE_AUDIT_READY"
    assert not [item for item in report["findings"] if item.get("severity") == "block"]
    assert report["active_template"] == "ION/07_templates/carriers/SINGLE_CARRIER_SEQUENTIAL_PACKET.md"
    assert report["phase_sequence"][0] == "PERSONA_INTERFACE_INGRESS"
    assert report["phase_sequence"][-1] == "PERSONA_INTERFACE_RESPONSE"


def test_stale_surface_audit_writes_active_report():
    root = _repo_root()
    report = write_stale_surface_audit(root)

    assert report["verdict"] == "ION_STALE_SURFACE_AUDIT_READY"
    assert (root / "ION/05_context/current/ACTIVE_STALE_SURFACE_AUDIT.json").exists()


def test_cursor_relay_rule_has_no_manual_gate_fallback_phrase():
    root = _repo_root()
    rule_path = root / ".cursor/rules/ion-carrier-relay-mediation.mdc"
    if not rule_path.exists():
        manifest = json.loads((root / "PRODUCT_MANIFEST.json").read_text(encoding="utf-8"))
        assert manifest["release_track"] == "custom_gpt_portable_sandbox"
        assert manifest["cursor_ide_lane"]["included"] is False
        return

    text = rule_path.read_text(encoding="utf-8")

    assert "Run or manually apply" not in text
    assert "Manual compliance judgment cannot replace this gate." in text
