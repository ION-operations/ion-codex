import json
from pathlib import Path

from kernel.ion_active_state_integrity_audit import (
    audit_active_state_integrity,
    write_active_state_integrity_audit,
)


def write_json(root: Path, rel: str, payload: dict):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def seed_root(root: Path):
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    (root / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)


def test_active_state_integrity_accepts_relative_active_paths(tmp_path: Path):
    seed_root(tmp_path)
    write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
        {"role_spawn_plan": [{"context_package_path": "ION/05_context/current/execution_cycles/01_steward.md"}]},
    )

    audit = audit_active_state_integrity(tmp_path)

    assert audit["accepted"] is True
    assert audit["verdict"] == "ION_ACTIVE_STATE_INTEGRITY_READY"
    assert audit["findings"] == []


def test_active_state_integrity_blocks_pytest_temp_paths(tmp_path: Path):
    seed_root(tmp_path)
    write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
        {"role_spawn_plan": [{"context_package_path": "/tmp/pytest-of-sev/test/cycle/01_steward.md"}]},
    )

    audit = audit_active_state_integrity(tmp_path)

    assert audit["accepted"] is False
    assert audit["verdict"] == "ION_ACTIVE_STATE_INTEGRITY_BLOCKED"
    assert audit["findings"][0]["json_path"] == "role_spawn_plan[0].context_package_path"


def test_write_active_state_integrity_audit(tmp_path: Path):
    seed_root(tmp_path)
    write_json(tmp_path, "ION/05_context/current/ACTIVE_WORK_PACKET.json", {"objective": "test"})

    audit = write_active_state_integrity_audit(tmp_path)

    out = tmp_path / "ION/05_context/current/ACTIVE_STATE_INTEGRITY_AUDIT.json"
    assert out.exists()
    assert json.loads(out.read_text(encoding="utf-8"))["schema_id"] == audit["schema_id"]
