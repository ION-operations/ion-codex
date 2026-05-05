from pathlib import Path

from kernel.ion_codex_extension_carrier_audit import (
    audit_codex_extension_carrier,
    write_codex_extension_carrier_audit,
)


def test_codex_extension_carrier_audit_current_tree_ready():
    result = audit_codex_extension_carrier(Path.cwd())

    assert result["schema_id"] == "ion.codex_extension_carrier_audit.v1"
    assert result["verdict"] == "ION_CODEX_EXTENSION_CARRIER_READY"
    assert result["capability_claims"]["host_subagents"] == "UNPROVEN_IN_THIS_AUDIT"
    assert result["production_authority"] is False
    assert result["live_execution_authority"] is False


def test_codex_extension_carrier_audit_blocks_incomplete_root(tmp_path):
    (tmp_path / "ION").mkdir(parents=True)
    (tmp_path / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (tmp_path / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")

    result = audit_codex_extension_carrier(tmp_path)

    assert result["verdict"] == "ION_CODEX_EXTENSION_CARRIER_BLOCKED"
    assert any(item.startswith("missing_profile:") for item in result["findings"])


def test_write_codex_extension_carrier_audit(tmp_path):
    root = Path.cwd()
    output = tmp_path / "CODEX_EXTENSION_CARRIER_AUDIT_V106.json"

    result = write_codex_extension_carrier_audit(root, output=output)

    assert output.exists()
    assert result["verdict"] == "ION_CODEX_EXTENSION_CARRIER_READY"
