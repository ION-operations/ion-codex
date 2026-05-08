import json
import zipfile
from pathlib import Path

from kernel.ion_trunk_preservation_gate import (
    build_file_manifest,
    build_zip_file_manifest,
    compare_file_manifests,
    trunk_preservation_report_to_dict,
    write_file_manifest,
)


def seed_root(root: Path):
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")


def test_protected_file_deletion_blocks_preservation_report(tmp_path):
    seed_root(tmp_path)
    protected = tmp_path / "ION/04_packages/kernel/protected_module.py"
    protected.parent.mkdir(parents=True, exist_ok=True)
    protected.write_text("VALUE = 1\n", encoding="utf-8")
    before = build_file_manifest(tmp_path, generated_at="2026-05-02T00:00:00+00:00")
    protected.unlink()
    after = build_file_manifest(tmp_path, generated_at="2026-05-02T00:01:00+00:00")

    report = compare_file_manifests(before, after, generated_at="2026-05-02T00:02:00+00:00")

    assert report.accepted is False
    assert report.packaging_verdict == "FAIL"
    assert report.protected_removed_files == 1
    assert report.unexpected_removed_files == 0
    assert report.protected_removed_paths == ("ION/04_packages/kernel/protected_module.py",)


def test_protected_file_move_to_containment_is_allowed_with_hash_proof(tmp_path):
    seed_root(tmp_path)
    protected = tmp_path / "ION/04_packages/kernel/protected_module.py"
    protected.parent.mkdir(parents=True, exist_ok=True)
    protected.write_text("VALUE = 1\n", encoding="utf-8")
    before = build_file_manifest(tmp_path, generated_at="2026-05-02T00:00:00+00:00")

    containment = tmp_path / "ION/05_context/archive/containment/V118/protected_module.py"
    containment.parent.mkdir(parents=True, exist_ok=True)
    containment.write_text(protected.read_text(encoding="utf-8"), encoding="utf-8")
    protected.unlink()
    after = build_file_manifest(tmp_path, generated_at="2026-05-02T00:01:00+00:00")

    report = compare_file_manifests(before, after, generated_at="2026-05-02T00:02:00+00:00")

    assert report.accepted is True
    assert report.packaging_verdict == "PASS"
    assert report.removed_files == 1
    assert report.contained_removed_files == 1
    assert report.protected_removed_files == 0
    assert report.unexpected_removed_files == 0
    assert report.contained_removed_paths == ("ION/04_packages/kernel/protected_module.py",)
    assert report.containment_moves[0]["to_path"] == "ION/05_context/archive/containment/V118/protected_module.py"
    assert report.containment_moves[0]["sha256"] == before.files["ION/04_packages/kernel/protected_module.py"].sha256


def test_cache_file_removal_is_allowed_under_policy(tmp_path):
    seed_root(tmp_path)
    cache_file = tmp_path / "ION/04_packages/kernel/__pycache__/module.cpython-313.pyc"
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_bytes(b"cache")
    before = build_file_manifest(tmp_path, generated_at="2026-05-02T00:00:00+00:00")
    cache_file.unlink()
    after = build_file_manifest(tmp_path, generated_at="2026-05-02T00:01:00+00:00")

    report = compare_file_manifests(before, after, generated_at="2026-05-02T00:02:00+00:00")

    assert report.accepted is True
    assert report.packaging_verdict == "PASS"
    assert report.allowed_removed_files == 1
    assert report.protected_removed_files == 0
    assert report.unexpected_removed_files == 0


def test_added_modified_removed_counts_are_emitted(tmp_path):
    seed_root(tmp_path)
    (tmp_path / "ION/02_architecture/a.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/02_architecture/a.md").write_text("a\n", encoding="utf-8")
    (tmp_path / "ION/docs/old.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/docs/old.md").write_text("old\n", encoding="utf-8")
    before = build_file_manifest(tmp_path, generated_at="2026-05-02T00:00:00+00:00")

    (tmp_path / "ION/02_architecture/a.md").write_text("a changed\n", encoding="utf-8")
    (tmp_path / "ION/docs/old.md").unlink()
    (tmp_path / "ION/docs/new.md").write_text("new\n", encoding="utf-8")
    after = build_file_manifest(tmp_path, generated_at="2026-05-02T00:01:00+00:00")

    report = compare_file_manifests(before, after, generated_at="2026-05-02T00:02:00+00:00")
    payload = trunk_preservation_report_to_dict(report)

    assert payload["files_before"] == before.file_count
    assert payload["files_after"] == after.file_count
    assert payload["added_files"] == 1
    assert payload["modified_files"] == 1
    assert payload["removed_files"] == 1
    assert payload["unexpected_removed_files"] == 1
    assert payload["protected_removed_files"] == 0
    assert payload["packaging_verdict"] == "FAIL"


def test_manifest_write_roundtrip_uses_path_size_and_hash(tmp_path):
    seed_root(tmp_path)
    (tmp_path / "AGENTS.md").write_text("agent law\n", encoding="utf-8")
    manifest = build_file_manifest(tmp_path, generated_at="2026-05-02T00:00:00+00:00")

    out = write_file_manifest(tmp_path, manifest, "manifest.json")
    payload = json.loads(out.read_text(encoding="utf-8"))

    assert payload["schema_id"] == "ion.trunk_file_manifest.v1"
    assert payload["root_confirmed"] is True
    assert payload["file_count"] == 3
    assert payload["files"]["AGENTS.md"]["size"] == len("agent law\n")
    assert payload["files"]["AGENTS.md"]["sha256"]


def test_zip_manifest_normalizes_single_wrapped_shell_root(tmp_path):
    zip_path = tmp_path / "wrapped.zip"
    with zipfile.ZipFile(zip_path, "w") as package:
        package.writestr("CURSOR- ION/pyproject.toml", "[project]\n")
        package.writestr("CURSOR- ION/ION/REPO_AUTHORITY.md", "# authority\n")
        package.writestr("CURSOR- ION/ION/02_architecture/protocol.md", "protocol\n")

    manifest = build_zip_file_manifest(zip_path, generated_at="2026-05-02T00:00:00+00:00")

    assert manifest.root_confirmed is True
    assert "pyproject.toml" in manifest.files
    assert "ION/REPO_AUTHORITY.md" in manifest.files
    assert "ION/02_architecture/protocol.md" in manifest.files
    assert not any(path.startswith("CURSOR- ION/") for path in manifest.files)
