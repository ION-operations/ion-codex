"""ION V106 lifecycle package manifest and root-integrity audit.

This module binds the V102 context lifecycle classifier to package planning and
adds an explicit zip-root audit for the recurring carrier failure where a
package is zipped with an extra wrapper directory. It does not delete, move, or
compress evidence and does not claim production authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ion_context_lifecycle import (
    REPORT_REL as CONTEXT_LIFECYCLE_AUDIT_REL,
    build_context_lifecycle_report,
    context_lifecycle_report_to_dict,
)

VERSION_LINE = "V106_LIFECYCLE_AWARE_PACKAGE_ROOT_INTEGRITY"
SCHEMA_ID = "ion.lifecycle_package_manifest.v1"
ZIP_AUDIT_SCHEMA_ID = "ion.package_zip_root_audit.v1"
POLICY_VERSION = "V102_CONTEXT_METABOLISM_AND_LIFECYCLE"

ROOT_REQUIRED_FILES = ("pyproject.toml", "ION/REPO_AUTHORITY.md")
PACKAGE_CLASSES = ("FULL_PROJECT", "COMPACT_RUNTIME", "FORENSIC_ARCHIVE")
OUTPUT_BY_PACKAGE_CLASS = {
    "FULL_PROJECT": Path("ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_FULL_PROJECT_V106.json"),
    "COMPACT_RUNTIME": Path("ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_COMPACT_RUNTIME_V106.json"),
    "FORENSIC_ARCHIVE": Path("ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_FORENSIC_ARCHIVE_V106.json"),
}
PACKAGE_OUTPUT_DIR = Path("ION/06_artifacts/packages")
SKIP_PACKAGE_PREFIXES = (
    ".git",
    ".pytest_cache",
    "ION/06_artifacts/packages",
)
SKIP_PACKAGE_PARTS = {"__pycache__", "node_modules"}
SKIP_PACKAGE_SUFFIXES = (".pyc", ".pyo", ".zip")


@dataclass(frozen=True)
class ZipRootAudit:
    schema_id: str
    zip_path: str
    root_confirmed: bool
    verdict: str
    archive_root_mode: str
    required_at_archive_root: tuple[str, ...]
    missing_at_archive_root: tuple[str, ...]
    wrapped_root_prefix: str | None
    wrapped_required_paths: tuple[str, ...]
    findings: tuple[str, ...]


@dataclass(frozen=True)
class LifecyclePackageManifest:
    schema_id: str
    version_line: str
    package_class: str
    package_manifest_id: str
    created_at: str
    source_root: str
    root_confirmed: bool
    root_required_files: tuple[str, ...]
    root_missing_files: tuple[str, ...]
    archive_root_policy: str
    lifecycle_policy_version: str
    context_lifecycle_audit_path: str
    production_authority: bool
    mutation_performed: bool
    zip_creation_performed: bool
    zip_path: str | None
    zip_sha256: str | None
    included_hot_context: tuple[str, ...]
    included_warm_context: tuple[str, ...]
    included_cold_context: tuple[str, ...]
    included_quarantine_context: tuple[str, ...]
    excluded_package_sidecar_context: tuple[str, ...]
    excluded_forensic_context: tuple[str, ...]
    zip_root_audit: dict[str, Any] | None
    verdict: str
    findings: tuple[str, ...]


def _shell_root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def _asdict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: _asdict(val) for key, val in asdict(value).items()}
    if isinstance(value, tuple):
        return [_asdict(v) for v in value]
    if isinstance(value, list):
        return [_asdict(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _asdict(v) for k, v in value.items()}
    return value


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def lifecycle_package_manifest_to_dict(manifest: LifecyclePackageManifest) -> dict[str, Any]:
    value = _asdict(manifest)
    assert isinstance(value, dict)
    return value


def zip_root_audit_to_dict(audit: ZipRootAudit) -> dict[str, Any]:
    value = _asdict(audit)
    assert isinstance(value, dict)
    return value


def prove_shell_root(root: str | Path) -> dict[str, Any]:
    shell = _shell_root(root)
    missing = tuple(rel for rel in ROOT_REQUIRED_FILES if not (shell / rel).exists())
    present = tuple(rel for rel in ROOT_REQUIRED_FILES if (shell / rel).exists())
    return {
        "schema_id": "ion.package_shell_root_proof.v1",
        "shell_root": shell.as_posix(),
        "root_confirmed": not missing,
        "required_present": present,
        "required_missing": missing,
        "verdict": "ROOT_CONFIRMED" if not missing else "ROOT_NOT_CONFIRMED",
    }


def audit_zip_root(zip_path: str | Path) -> ZipRootAudit:
    path = Path(zip_path).expanduser().resolve()
    if not path.exists():
        return ZipRootAudit(
            schema_id=ZIP_AUDIT_SCHEMA_ID,
            zip_path=path.as_posix(),
            root_confirmed=False,
            verdict="ZIP_NOT_FOUND",
            archive_root_mode="ZIP_NOT_FOUND",
            required_at_archive_root=ROOT_REQUIRED_FILES,
            missing_at_archive_root=ROOT_REQUIRED_FILES,
            wrapped_root_prefix=None,
            wrapped_required_paths=(),
            findings=("zip_file_not_found",),
        )

    with zipfile.ZipFile(path) as package:
        files = {name.rstrip("/") for name in package.namelist() if name and not name.endswith("/")}

    missing_at_root = tuple(rel for rel in ROOT_REQUIRED_FILES if rel not in files)
    if not missing_at_root:
        return ZipRootAudit(
            schema_id=ZIP_AUDIT_SCHEMA_ID,
            zip_path=path.as_posix(),
            root_confirmed=True,
            verdict="ZIP_ROOT_CONFIRMED",
            archive_root_mode="CANONICAL_ARCHIVE_ROOT",
            required_at_archive_root=ROOT_REQUIRED_FILES,
            missing_at_archive_root=(),
            wrapped_root_prefix=None,
            wrapped_required_paths=ROOT_REQUIRED_FILES,
            findings=("zip_root_invariant_confirmed",),
        )

    candidate_prefixes: set[str] = set()
    for name in files:
        for required in ROOT_REQUIRED_FILES:
            suffix = f"/{required}"
            if name.endswith(suffix):
                candidate_prefixes.add(name[: -len(suffix)])

    wrapped_prefixes = [
        prefix
        for prefix in sorted(candidate_prefixes)
        if all(f"{prefix}/{required}" in files for required in ROOT_REQUIRED_FILES)
    ]
    if len(wrapped_prefixes) == 1:
        prefix = wrapped_prefixes[0]
        return ZipRootAudit(
            schema_id=ZIP_AUDIT_SCHEMA_ID,
            zip_path=path.as_posix(),
            root_confirmed=False,
            verdict="WRAPPED_ROOT_DETECTED",
            archive_root_mode="WRAPPED_SHELL_ROOT",
            required_at_archive_root=ROOT_REQUIRED_FILES,
            missing_at_archive_root=missing_at_root,
            wrapped_root_prefix=prefix,
            wrapped_required_paths=tuple(f"{prefix}/{required}" for required in ROOT_REQUIRED_FILES),
            findings=(
                "zip_archive_has_single_wrapped_shell_root",
                "extracting_archive_places_shell_root_below_extraction_target",
            ),
        )
    if wrapped_prefixes:
        return ZipRootAudit(
            schema_id=ZIP_AUDIT_SCHEMA_ID,
            zip_path=path.as_posix(),
            root_confirmed=False,
            verdict="MULTIPLE_WRAPPED_ROOTS_DETECTED",
            archive_root_mode="AMBIGUOUS_WRAPPED_SHELL_ROOTS",
            required_at_archive_root=ROOT_REQUIRED_FILES,
            missing_at_archive_root=missing_at_root,
            wrapped_root_prefix=None,
            wrapped_required_paths=tuple(
                f"{prefix}/{required}" for prefix in wrapped_prefixes for required in ROOT_REQUIRED_FILES
            ),
            findings=("zip_archive_contains_multiple_candidate_shell_roots",),
        )
    return ZipRootAudit(
        schema_id=ZIP_AUDIT_SCHEMA_ID,
        zip_path=path.as_posix(),
        root_confirmed=False,
        verdict="ROOT_INVARIANT_FAILED",
        archive_root_mode="MISSING_CANONICAL_SHELL_ROOT",
        required_at_archive_root=ROOT_REQUIRED_FILES,
        missing_at_archive_root=missing_at_root,
        wrapped_root_prefix=None,
        wrapped_required_paths=(),
        findings=("zip_archive_missing_required_shell_root_files",),
    )


def _context_lists(report: dict[str, Any], package_class: str) -> dict[str, tuple[str, ...]]:
    hot: list[str] = []
    warm: list[str] = []
    cold: list[str] = []
    quarantine: list[str] = []
    sidecars: list[str] = []
    excluded: list[str] = []

    for artifact in report.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        rel_path = str(artifact.get("rel_path", ""))
        lifecycle_class = str(artifact.get("lifecycle_class", ""))
        if not rel_path:
            continue
        if Path(rel_path).name.startswith("LIFECYCLE_PACKAGE_MANIFEST_") and Path(rel_path).suffix == ".json":
            sidecars.append(rel_path)
            continue

        if lifecycle_class == "HOT_RUNTIME_STATE":
            hot.append(rel_path)
        elif lifecycle_class.startswith("WARM"):
            if package_class in {"FULL_PROJECT", "FORENSIC_ARCHIVE"}:
                warm.append(rel_path)
            else:
                excluded.append(rel_path)
        elif lifecycle_class == "COLD_HISTORY":
            if package_class in {"FULL_PROJECT", "FORENSIC_ARCHIVE"}:
                cold.append(rel_path)
            else:
                excluded.append(rel_path)
        elif lifecycle_class == "QUARANTINE_CANDIDATE":
            if package_class == "FORENSIC_ARCHIVE":
                quarantine.append(rel_path)
            else:
                excluded.append(rel_path)
        elif package_class == "FORENSIC_ARCHIVE":
            cold.append(rel_path)
        else:
            excluded.append(rel_path)

    return {
        "included_hot_context": tuple(sorted(hot)),
        "included_warm_context": tuple(sorted(warm)),
        "included_cold_context": tuple(sorted(cold)),
        "included_quarantine_context": tuple(sorted(quarantine)),
        "excluded_package_sidecar_context": tuple(sorted(sidecars)),
        "excluded_forensic_context": tuple(sorted(excluded)),
    }


def _is_skipped_package_path(rel: Path) -> bool:
    rel_posix = rel.as_posix()
    if any(rel_posix == prefix or rel_posix.startswith(f"{prefix}/") for prefix in SKIP_PACKAGE_PREFIXES):
        return True
    if any(part in SKIP_PACKAGE_PARTS for part in rel.parts):
        return True
    if rel.name.startswith("LIFECYCLE_PACKAGE_MANIFEST_") and rel.suffix == ".json":
        return True
    return rel.suffix in SKIP_PACKAGE_SUFFIXES


def _add_existing_path(shell: Path, rel: str | Path, files: set[Path]) -> None:
    rel_path = Path(rel)
    path = shell / rel_path
    if not path.exists():
        return
    if path.is_file() and not _is_skipped_package_path(rel_path):
        files.add(rel_path)
        return
    if path.is_dir():
        for child in sorted(path.rglob("*")):
            if not child.is_file() or child.is_symlink():
                continue
            child_rel = child.relative_to(shell)
            if not _is_skipped_package_path(child_rel):
                files.add(child_rel)


def _all_project_files(shell: Path) -> tuple[Path, ...]:
    files: set[Path] = set()
    for child in sorted(shell.rglob("*")):
        if not child.is_file() or child.is_symlink():
            continue
        rel = child.relative_to(shell)
        if not _is_skipped_package_path(rel):
            files.add(rel)
    return tuple(sorted(files, key=lambda p: p.as_posix()))


def package_file_set(shell: Path, manifest: LifecyclePackageManifest) -> tuple[Path, ...]:
    """Return canonical archive-relative paths for a package class."""

    package_class = manifest.package_class
    if package_class == "FULL_PROJECT":
        return _all_project_files(shell)

    files: set[Path] = set()
    for rel in ROOT_REQUIRED_FILES:
        _add_existing_path(shell, rel, files)

    if package_class == "COMPACT_RUNTIME":
        compact_roots = (
            "ION/00_BOOTSTRAP",
            "ION/02_architecture",
            "ION/03_registry",
            "ION/04_agents",
            "ION/04_packages",
            "ION/05_context/signals",
            "ION/07_templates",
            "ION/08_ui",
            "ION/09_integrations",
            "ION/docs/consolidation",
            "ION/tests",
        )
        for rel in compact_roots:
            _add_existing_path(shell, rel, files)
        for rel in manifest.included_hot_context:
            _add_existing_path(shell, rel, files)
        for rel in manifest.excluded_forensic_context:
            excluded = Path(rel)
            files = {
                item for item in files
                if item != excluded and excluded not in item.parents
            }
    elif package_class == "FORENSIC_ARCHIVE":
        for rel in (
            *manifest.included_warm_context,
            *manifest.included_cold_context,
            *manifest.included_quarantine_context,
            *manifest.excluded_forensic_context,
            "ION/05_context/signals",
            "ION/docs/consolidation",
        ):
            _add_existing_path(shell, rel, files)

    return tuple(sorted(files, key=lambda p: p.as_posix()))


def build_lifecycle_package_manifest(
    root: str | Path,
    *,
    package_class: str = "COMPACT_RUNTIME",
    emitted_at: str | None = None,
    zip_path: str | Path | None = None,
    zip_creation_performed: bool = False,
    zip_sha256: str | None = None,
) -> LifecyclePackageManifest:
    if package_class not in PACKAGE_CLASSES:
        raise ValueError(f"package_class must be one of {', '.join(PACKAGE_CLASSES)}")

    shell = _shell_root(root)
    timestamp = emitted_at or _now()
    root_proof = prove_shell_root(shell)
    lifecycle_report = context_lifecycle_report_to_dict(build_context_lifecycle_report(shell, emitted_at=timestamp))
    context = _context_lists(lifecycle_report, package_class)
    zip_audit = audit_zip_root(zip_path) if zip_path else None

    findings: list[str] = []
    if not root_proof["root_confirmed"]:
        findings.append("shell_root_required_files_missing")
    if package_class == "COMPACT_RUNTIME" and context["excluded_forensic_context"]:
        findings.append("compact_runtime_excludes_non_hot_context_by_default")
    if zip_audit and not zip_audit.root_confirmed:
        findings.extend(zip_audit.findings)

    if not root_proof["root_confirmed"]:
        verdict = "ROOT_NOT_CONFIRMED"
    elif zip_audit and not zip_audit.root_confirmed:
        verdict = "PACKAGE_ZIP_ROOT_REVIEW_REQUIRED"
    elif zip_creation_performed and package_class == "COMPACT_RUNTIME" and context["excluded_forensic_context"]:
        verdict = "PACKAGE_ZIP_READY_WITH_EXCLUSIONS"
    elif zip_creation_performed:
        verdict = "PACKAGE_ZIP_READY"
    elif package_class == "COMPACT_RUNTIME" and context["excluded_forensic_context"]:
        verdict = "PACKAGE_MANIFEST_READY_WITH_EXCLUSIONS"
    else:
        verdict = "PACKAGE_MANIFEST_READY"

    if not findings:
        findings.append("package_manifest_ready_without_mutation")

    manifest_id = _stable_id("lifecycle-package-manifest", package_class, shell.as_posix(), timestamp, verdict)
    return LifecyclePackageManifest(
        schema_id=SCHEMA_ID,
        version_line=VERSION_LINE,
        package_class=package_class,
        package_manifest_id=manifest_id,
        created_at=timestamp,
        source_root=shell.as_posix(),
        root_confirmed=bool(root_proof["root_confirmed"]),
        root_required_files=ROOT_REQUIRED_FILES,
        root_missing_files=tuple(root_proof["required_missing"]),
        archive_root_policy="pyproject.toml and ION/REPO_AUTHORITY.md must be at archive root; wrapper-directory zips require repackaging",
        lifecycle_policy_version=POLICY_VERSION,
        context_lifecycle_audit_path=CONTEXT_LIFECYCLE_AUDIT_REL.as_posix(),
        production_authority=False,
        mutation_performed=False,
        zip_creation_performed=zip_creation_performed,
        zip_path=str(Path(zip_path).expanduser().resolve()) if zip_path else None,
        zip_sha256=zip_sha256,
        zip_root_audit=zip_root_audit_to_dict(zip_audit) if zip_audit else None,
        verdict=verdict,
        findings=tuple(findings),
        **context,
    )


def create_lifecycle_package_zip(
    root: str | Path,
    *,
    package_class: str = "COMPACT_RUNTIME",
    output_zip: str | Path | None = None,
    write_manifest: bool = True,
    emitted_at: str | None = None,
) -> LifecyclePackageManifest:
    """Materialize a package zip with canonical archive-root paths.

    The source tree is not moved, deleted, or rewritten. The only mutation is
    creating a package artifact and optional sidecar manifest.
    """

    if package_class not in PACKAGE_CLASSES:
        raise ValueError(f"package_class must be one of {', '.join(PACKAGE_CLASSES)}")

    shell = _shell_root(root)
    timestamp = emitted_at or _now()
    initial = build_lifecycle_package_manifest(shell, package_class=package_class, emitted_at=timestamp)
    if not initial.root_confirmed:
        return initial

    if output_zip is None:
        safe_stamp = timestamp.replace(":", "").replace("+", "Z")
        output_path = shell / PACKAGE_OUTPUT_DIR / f"ION_{package_class}_{safe_stamp}.zip"
    else:
        candidate = Path(output_zip).expanduser()
        output_path = candidate if candidate.is_absolute() else shell / candidate
    output_path.parent.mkdir(parents=True, exist_ok=True)

    files = package_file_set(shell, initial)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for rel in files:
            source = shell / rel
            info = zipfile.ZipInfo(rel.as_posix())
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            package.writestr(info, source.read_bytes())

    sha = _sha256_file(output_path)
    manifest = build_lifecycle_package_manifest(
        shell,
        package_class=package_class,
        emitted_at=timestamp,
        zip_path=output_path,
        zip_creation_performed=True,
        zip_sha256=sha,
    )
    if write_manifest:
        write_lifecycle_package_manifest(shell, manifest)
    return manifest


def write_lifecycle_package_manifest(
    root: str | Path,
    manifest: LifecyclePackageManifest | None = None,
    *,
    package_class: str = "COMPACT_RUNTIME",
    output: str | Path | None = None,
) -> Path:
    shell = _shell_root(root)
    manifest = manifest or build_lifecycle_package_manifest(shell, package_class=package_class)
    rel = Path(output) if output else OUTPUT_BY_PACKAGE_CLASS[manifest.package_class]
    path = shell / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(lifecycle_package_manifest_to_dict(manifest), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build ION lifecycle package manifest and audit package zip root.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--package-class", choices=PACKAGE_CLASSES, default="COMPACT_RUNTIME")
    parser.add_argument("--audit-zip", default=None, help="Optional package zip to audit for archive-root invariant.")
    parser.add_argument("--create-zip", action="store_true", help="Create a canonical-root package zip.")
    parser.add_argument("--zip-output", default=None, help="Optional output zip path. Relative paths are resolved under ion-root.")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--output", default=None, help="Optional output path relative to ion-root.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.create_zip:
        manifest = create_lifecycle_package_zip(
            args.ion_root,
            package_class=args.package_class,
            output_zip=args.zip_output,
            write_manifest=True,
        )
    else:
        manifest = build_lifecycle_package_manifest(args.ion_root, package_class=args.package_class, zip_path=args.audit_zip)
    if args.write_manifest:
        write_lifecycle_package_manifest(args.ion_root, manifest, output=args.output)
    if args.json:
        print(json.dumps(lifecycle_package_manifest_to_dict(manifest), indent=2, sort_keys=True))
    else:
        print(f"ION_LIFECYCLE_PACKAGE_{manifest.verdict}")
        for finding in manifest.findings:
            print(f"- {finding}")
    return 0 if manifest.verdict != "ROOT_NOT_CONFIRMED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
