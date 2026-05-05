import json
import zipfile
from pathlib import Path

from kernel.ion_lifecycle_packager import (
    audit_zip_root,
    build_lifecycle_package_manifest,
    create_lifecycle_package_zip,
    write_lifecycle_package_manifest,
)


def write_json(root: Path, rel: str, payload: dict):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def seed_root(root: Path):
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION").mkdir()
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")


def test_compact_runtime_manifest_confirms_root_and_excludes_non_hot_context(tmp_path):
    seed_root(tmp_path)
    write_json(tmp_path, "ION/05_context/current/ACTIVE_WORK_PACKET.json", {"objective": "test"})
    cycle = tmp_path / "ION/05_context/current/execution_cycles/old-cycle"
    cycle.mkdir(parents=True)
    (cycle / "receipt.md").write_text("receipt\n", encoding="utf-8")
    history = tmp_path / "ION/05_context/history/archive"
    history.mkdir(parents=True)
    (history / "old.md").write_text("history\n", encoding="utf-8")
    scratch = tmp_path / "ION/05_context/current/_tmp_multi_root_session_01"
    scratch.mkdir()
    (scratch / "foreign.txt").write_text("foreign\n", encoding="utf-8")

    manifest = build_lifecycle_package_manifest(
        tmp_path,
        package_class="COMPACT_RUNTIME",
        emitted_at="2026-05-02T00:00:00+00:00",
    )

    assert manifest.schema_id == "ion.lifecycle_package_manifest.v1"
    assert manifest.root_confirmed is True
    assert manifest.production_authority is False
    assert manifest.mutation_performed is False
    assert "ION/05_context/current/ACTIVE_WORK_PACKET.json" in manifest.included_hot_context
    assert "ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_COMPACT_RUNTIME_V106.json" not in manifest.included_hot_context
    assert "ION/05_context/current/execution_cycles" in manifest.excluded_forensic_context
    assert "ION/05_context/current/_tmp_multi_root_session_01" in manifest.excluded_forensic_context
    assert manifest.verdict == "PACKAGE_MANIFEST_READY_WITH_EXCLUSIONS"


def test_manifest_fails_when_shell_root_required_files_missing(tmp_path):
    manifest = build_lifecycle_package_manifest(
        tmp_path,
        package_class="COMPACT_RUNTIME",
        emitted_at="2026-05-02T00:00:00+00:00",
    )

    assert manifest.root_confirmed is False
    assert manifest.verdict == "ROOT_NOT_CONFIRMED"
    assert set(manifest.root_missing_files) == {"pyproject.toml", "ION/REPO_AUTHORITY.md"}


def test_zip_root_audit_accepts_canonical_archive_root(tmp_path):
    zip_path = tmp_path / "canonical.zip"
    with zipfile.ZipFile(zip_path, "w") as package:
        package.writestr("pyproject.toml", "[project]\n")
        package.writestr("ION/REPO_AUTHORITY.md", "# authority\n")

    audit = audit_zip_root(zip_path)

    assert audit.root_confirmed is True
    assert audit.verdict == "ZIP_ROOT_CONFIRMED"
    assert audit.archive_root_mode == "CANONICAL_ARCHIVE_ROOT"


def test_zip_root_audit_detects_wrapped_archive_root(tmp_path):
    zip_path = tmp_path / "wrapped.zip"
    with zipfile.ZipFile(zip_path, "w") as package:
        package.writestr("CURSOR- ION/pyproject.toml", "[project]\n")
        package.writestr("CURSOR- ION/ION/REPO_AUTHORITY.md", "# authority\n")

    audit = audit_zip_root(zip_path)

    assert audit.root_confirmed is False
    assert audit.verdict == "WRAPPED_ROOT_DETECTED"
    assert audit.archive_root_mode == "WRAPPED_SHELL_ROOT"
    assert audit.wrapped_root_prefix == "CURSOR- ION"
    assert "zip_archive_has_single_wrapped_shell_root" in audit.findings


def test_write_lifecycle_package_manifest(tmp_path):
    seed_root(tmp_path)
    write_json(tmp_path, "ION/05_context/current/ACTIVE_WORK_PACKET.json", {"objective": "test"})

    manifest = build_lifecycle_package_manifest(
        tmp_path,
        package_class="COMPACT_RUNTIME",
        emitted_at="2026-05-02T00:00:00+00:00",
    )
    out = write_lifecycle_package_manifest(tmp_path, manifest)

    assert out.exists()
    loaded = json.loads(out.read_text(encoding="utf-8"))
    assert loaded["schema_id"] == "ion.lifecycle_package_manifest.v1"
    assert loaded["root_confirmed"] is True


def test_create_compact_runtime_zip_uses_canonical_archive_root_and_excludes_forensic_context(tmp_path):
    seed_root(tmp_path)
    write_json(tmp_path, "ION/05_context/current/ACTIVE_WORK_PACKET.json", {"objective": "test"})
    package_code = tmp_path / "ION/04_packages/kernel"
    package_code.mkdir(parents=True)
    (package_code / "example.py").write_text("VALUE = 1\n", encoding="utf-8")
    cycle = tmp_path / "ION/05_context/current/execution_cycles/old-cycle"
    cycle.mkdir(parents=True)
    (cycle / "receipt.md").write_text("receipt\n", encoding="utf-8")

    zip_path = tmp_path / "out" / "compact.zip"
    manifest = create_lifecycle_package_zip(
        tmp_path,
        package_class="COMPACT_RUNTIME",
        output_zip=zip_path,
        emitted_at="2026-05-02T00:00:00+00:00",
    )

    assert zip_path.exists()
    assert manifest.zip_creation_performed is True
    assert manifest.mutation_performed is False
    assert manifest.zip_sha256
    assert manifest.zip_root_audit
    assert manifest.zip_root_audit["verdict"] == "ZIP_ROOT_CONFIRMED"
    with zipfile.ZipFile(zip_path) as package:
        names = set(package.namelist())
        pyproject_mode = (package.getinfo("pyproject.toml").external_attr >> 16) & 0o777
    assert "pyproject.toml" in names
    assert "ION/REPO_AUTHORITY.md" in names
    assert "ION/04_packages/kernel/example.py" in names
    assert "ION/05_context/current/ACTIVE_WORK_PACKET.json" in names
    assert "ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_COMPACT_RUNTIME_V106.json" not in names
    assert not any(name.startswith("CURSOR- ION/") for name in names)
    assert "ION/05_context/current/execution_cycles/old-cycle/receipt.md" not in names
    assert pyproject_mode == 0o644
