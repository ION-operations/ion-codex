from pathlib import Path

from kernel.v78_ion_mount_contract_audit import audit_v78_ion_mount_contract


def test_v78_mount_contract_no_longer_requires_start_here_as_mount_authority():
    root = Path(__file__).resolve().parents[2]
    result = audit_v78_ion_mount_contract(root)

    assert result["mount_contract_ok"] is True
    assert "start_here_exists" not in result
    assert "start_here_path" not in result
    assert result["contract_required_phrases_missing"] == []
