import zipfile
from pathlib import Path

from kernel.ion_safe_full_project_packager import create_safe_full_project_package
from kernel.ion_trunk_preservation_gate import build_file_manifest


def seed_root(root: Path):
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
    (root / "START_HERE_FOR_ANY_AGENT.md").write_text("# start\n", encoding="utf-8")


def test_safe_full_project_packager_creates_canonical_root_zip_and_excludes_cache(tmp_path):
    seed_root(tmp_path)
    (tmp_path / "ION/04_packages/kernel").mkdir(parents=True)
    (tmp_path / "ION/04_packages/kernel/example.py").write_text("VALUE = 1\n", encoding="utf-8")
    cache_file = tmp_path / ".pytest_cache/v/cache/nodeids"
    cache_file.parent.mkdir(parents=True)
    cache_file.write_text("cache\n", encoding="utf-8")

    zip_path = tmp_path / "out/full.zip"
    result = create_safe_full_project_package(
        tmp_path,
        output_zip=zip_path,
        write_manifests=True,
        write_report=True,
        emitted_at="2026-05-02T00:00:00+00:00",
    )

    assert result.accepted is True
    assert result.zip_creation_performed is True
    assert result.zip_sha256
    assert result.zip_root_audit
    assert result.zip_root_audit["verdict"] == "ZIP_ROOT_CONFIRMED"
    assert result.preservation_report["unexpected_removed_files"] == 0
    assert result.preservation_report["protected_removed_files"] == 0
    with zipfile.ZipFile(zip_path) as package:
        names = set(package.namelist())
        mode = (package.getinfo("pyproject.toml").external_attr >> 16) & 0o777
    assert "pyproject.toml" in names
    assert "ION/REPO_AUTHORITY.md" in names
    assert "ION/04_packages/kernel/example.py" in names
    assert not any(name.startswith("CURSOR- ION/") for name in names)
    assert ".pytest_cache/v/cache/nodeids" not in names
    assert mode == 0o644


def test_safe_full_project_packager_blocks_when_baseline_lost_protected_file(tmp_path):
    seed_root(tmp_path)
    protected = tmp_path / "ION/08_ui/widget.tsx"
    protected.parent.mkdir(parents=True)
    protected.write_text("export const value = 1;\n", encoding="utf-8")
    baseline = build_file_manifest(tmp_path, generated_at="2026-05-02T00:00:00+00:00")
    protected.unlink()

    result = create_safe_full_project_package(
        tmp_path,
        output_zip=tmp_path / "out/full.zip",
        baseline_manifest=baseline,
        write_manifests=False,
        write_report=False,
        emitted_at="2026-05-02T00:01:00+00:00",
    )

    assert result.accepted is False
    assert result.zip_creation_performed is False
    assert result.zip_path is None
    assert result.preservation_report["packaging_verdict"] == "FAIL"
    assert result.preservation_report["protected_removed_files"] == 1
    assert not (tmp_path / "out/full.zip").exists()


def test_safe_full_project_packager_records_added_zip_without_removals(tmp_path):
    seed_root(tmp_path)
    result = create_safe_full_project_package(
        tmp_path,
        output_zip=tmp_path / "out/full.zip",
        write_manifests=True,
        write_report=True,
        emitted_at="2026-05-02T00:00:00+00:00",
    )

    report = result.preservation_report
    assert report["packaging_verdict"] == "PASS"
    assert report["removed_files"] == 0
    assert report["unexpected_removed_files"] == 0
    assert report["protected_removed_files"] == 0
    assert report["added_files"] >= 1
    assert any(path.endswith("out/full.zip") or path == "out/full.zip" for path in report["added_paths"])


def test_safe_full_project_packager_can_compare_previous_wrapped_zip_to_new_canonical_zip(tmp_path):
    seed_root(tmp_path)
    previous_zip = tmp_path / "previous.zip"
    with zipfile.ZipFile(previous_zip, "w") as package:
        package.writestr("CURSOR- ION/pyproject.toml", "[project]\nname = \"ion-test\"\n")
        package.writestr("CURSOR- ION/ION/REPO_AUTHORITY.md", "# authority\n")
        package.writestr("CURSOR- ION/AGENTS.md", "# agents\n")
        package.writestr("CURSOR- ION/START_HERE_FOR_ANY_AGENT.md", "# start\n")
        package.writestr("CURSOR- ION/.pytest_cache/v/cache/nodeids", "cache\n")

    result = create_safe_full_project_package(
        tmp_path,
        output_zip=tmp_path / "out/full.zip",
        previous_full_zip=previous_zip.as_posix(),
        write_manifests=True,
        write_report=True,
        emitted_at="2026-05-02T00:00:00+00:00",
    )

    assert result.accepted is True
    assert result.preservation_report["previous_full_zip"] == previous_zip.as_posix()
    assert result.preservation_report["new_full_zip"].endswith("out/full.zip")
    assert result.preservation_report["allowed_removed_files"] == 1
    assert result.preservation_report["unexpected_removed_files"] == 0
    assert result.preservation_report["protected_removed_files"] == 0
