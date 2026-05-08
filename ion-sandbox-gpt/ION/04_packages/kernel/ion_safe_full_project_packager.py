"""ION V118 safe full-project packager.

The safe packager creates canonical archive-root full-project zips only after
the trunk preservation gate has a baseline to compare against. It excludes
generated cache/package byproducts from the archive, writes manifest evidence,
and blocks package creation when a supplied baseline shows protected or
unexpected uncontained removals. Lawful lifecycle movement is represented as
hash-proven containment, quarantine, or archive movement, not silent loss.
"""
from __future__ import annotations

import argparse
import json
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ion_lifecycle_packager import audit_zip_root
from .ion_trunk_preservation_gate import (
    DEFAULT_BASELINE_MANIFEST_REL,
    DEFAULT_POST_MANIFEST_REL,
    DEFAULT_REPORT_REL,
    ROOT_REQUIRED_FILES,
    TrunkFileManifest,
    TrunkPreservationReport,
    build_file_manifest,
    build_zip_file_manifest,
    compare_file_manifests,
    read_file_manifest,
    trunk_file_manifest_to_dict,
    trunk_preservation_report_to_dict,
    write_file_manifest,
    write_trunk_preservation_report,
)

VERSION_LINE = "V118_SAFE_FULL_PROJECT_PACKAGER"
SCHEMA_ID = "ion.safe_full_project_package_result.v1"
PACKAGE_OUTPUT_DIR = Path("ION/06_artifacts/packages")
DEFAULT_ZIP_NAME_PREFIX = "ION_FULL_PROJECT_V118_NO_SILENT_LOSS_CONTAINMENT"

PACKAGE_SKIP_PREFIXES = (
    ".git/",
    ".pytest_cache/",
    ".mypy_cache/",
    ".ruff_cache/",
    "ION/06_artifacts/packages/",
)
PACKAGE_SKIP_PARTS = {"__pycache__", "node_modules"}
PACKAGE_SKIP_SUFFIXES = (".pyc", ".pyo", ".zip")
PACKAGE_SKIP_NAMES = {
    "SAFE_FULL_PROJECT_PACKAGE_RESULT_V107.json",
    "SAFE_FULL_PROJECT_PACKAGE_RESULT_V118.json",
}
PACKAGE_SKIP_NAME_PREFIXES = (
    "TRUNK_FILE_MANIFEST_",
    "TRUNK_PRESERVATION_REPORT_",
    "SAFE_FULL_PROJECT_PACKAGE_RESULT_",
)


@dataclass(frozen=True)
class SafeFullProjectPackageResult:
    schema_id: str
    version_line: str
    generated_at: str
    source_root: str
    zip_creation_attempted: bool
    zip_creation_performed: bool
    zip_path: str | None
    zip_sha256: str | None
    zip_root_audit: dict[str, Any] | None
    baseline_manifest_path: str | None
    post_manifest_path: str | None
    preservation_report_path: str | None
    preservation_report: dict[str, Any]
    excluded_generated_paths: tuple[str, ...]
    accepted: bool
    production_authority: bool
    findings: tuple[str, ...]


def _shell_root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _is_packager_excluded_path(rel: Path) -> bool:
    rel_posix = rel.as_posix()
    if any(rel_posix == prefix.rstrip("/") or rel_posix.startswith(prefix) for prefix in PACKAGE_SKIP_PREFIXES):
        return True
    if any(part in PACKAGE_SKIP_PARTS for part in rel.parts):
        return True
    if rel.name in PACKAGE_SKIP_NAMES:
        return True
    if rel.name.endswith(".json") and any(rel.name.startswith(prefix) for prefix in PACKAGE_SKIP_NAME_PREFIXES):
        return True
    return rel.suffix in PACKAGE_SKIP_SUFFIXES


def full_project_package_file_set(shell: Path) -> tuple[Path, ...]:
    files: list[Path] = []
    for child in sorted(shell.rglob("*")):
        if not child.is_file() or child.is_symlink():
            continue
        rel = child.relative_to(shell)
        if _is_packager_excluded_path(rel):
            continue
        files.append(rel)
    return tuple(sorted(files, key=lambda path: path.as_posix()))


def excluded_generated_package_paths(shell: Path) -> tuple[str, ...]:
    excluded: list[str] = []
    for child in sorted(shell.rglob("*")):
        if not child.is_file() or child.is_symlink():
            continue
        rel = child.relative_to(shell)
        if _is_packager_excluded_path(rel):
            excluded.append(rel.as_posix())
    return tuple(sorted(excluded))


def safe_full_project_package_result_to_dict(result: SafeFullProjectPackageResult) -> dict[str, Any]:
    value = _asdict(result)
    assert isinstance(value, dict)
    return value


def _write_package_zip(shell: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    files = full_project_package_file_set(shell)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for rel in files:
            source = shell / rel
            info = zipfile.ZipInfo(rel.as_posix())
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            package.writestr(info, source.read_bytes())


def _resolve_zip_path(shell: Path, output_zip: str | Path | None, timestamp: str) -> Path:
    if output_zip is not None:
        candidate = Path(output_zip).expanduser()
        return candidate if candidate.is_absolute() else shell / candidate
    safe_stamp = timestamp.replace(":", "").replace("+", "Z")
    return shell / PACKAGE_OUTPUT_DIR / f"{DEFAULT_ZIP_NAME_PREFIX}_{safe_stamp}.zip"


def _write_json_result(shell: Path, result: SafeFullProjectPackageResult, output: str | Path) -> Path:
    candidate = Path(output).expanduser()
    path = candidate if candidate.is_absolute() else shell / candidate
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(safe_full_project_package_result_to_dict(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _block_result(
    *,
    shell: Path,
    timestamp: str,
    report: TrunkPreservationReport,
    baseline_manifest_path: str | None,
    post_manifest_path: str | None,
    preservation_report_path: str | None,
    findings: tuple[str, ...],
) -> SafeFullProjectPackageResult:
    return SafeFullProjectPackageResult(
        schema_id=SCHEMA_ID,
        version_line=VERSION_LINE,
        generated_at=timestamp,
        source_root=shell.as_posix(),
        zip_creation_attempted=True,
        zip_creation_performed=False,
        zip_path=None,
        zip_sha256=None,
        zip_root_audit=None,
        baseline_manifest_path=baseline_manifest_path,
        post_manifest_path=post_manifest_path,
        preservation_report_path=preservation_report_path,
        preservation_report=trunk_preservation_report_to_dict(report),
        excluded_generated_paths=excluded_generated_package_paths(shell),
        accepted=False,
        production_authority=False,
        findings=findings,
    )


def create_safe_full_project_package(
    root: str | Path,
    *,
    output_zip: str | Path | None = None,
    baseline_manifest: str | Path | TrunkFileManifest | None = None,
    previous_full_zip: str | None = None,
    baseline_manifest_output: str | Path = DEFAULT_BASELINE_MANIFEST_REL,
    post_manifest_output: str | Path = DEFAULT_POST_MANIFEST_REL,
    report_output: str | Path = DEFAULT_REPORT_REL,
    result_output: str | Path | None = None,
    write_manifests: bool = True,
    write_report: bool = True,
    emitted_at: str | None = None,
) -> SafeFullProjectPackageResult:
    shell = _shell_root(root)
    timestamp = emitted_at or _now()
    zip_path = _resolve_zip_path(shell, output_zip, timestamp)

    if isinstance(baseline_manifest, TrunkFileManifest):
        baseline = baseline_manifest
        baseline_path: str | None = None
    elif baseline_manifest:
        baseline_path_obj = Path(baseline_manifest).expanduser()
        baseline = read_file_manifest(baseline_path_obj)
        baseline_path = baseline_path_obj.as_posix()
    elif previous_full_zip:
        baseline = build_zip_file_manifest(previous_full_zip, generated_at=timestamp)
        baseline_path = str(Path(previous_full_zip).expanduser().resolve())
        if write_manifests:
            write_file_manifest(shell, baseline, baseline_manifest_output)
    else:
        baseline = build_file_manifest(shell, generated_at=timestamp)
        baseline_path = (shell / baseline_manifest_output).as_posix()
        if write_manifests:
            write_file_manifest(shell, baseline, baseline_manifest_output)

    pre_package_manifest = build_file_manifest(shell, generated_at=timestamp)
    preflight = compare_file_manifests(
        baseline,
        pre_package_manifest,
        previous_full_zip=previous_full_zip,
        new_full_zip=zip_path.as_posix(),
        baseline_manifest_path=baseline_path,
        post_manifest_path=None,
        generated_at=timestamp,
    )
    if not preflight.accepted:
        report_path = None
        if write_report:
            report_path = write_trunk_preservation_report(shell, preflight, report_output).as_posix()
        result = _block_result(
            shell=shell,
            timestamp=timestamp,
            report=preflight,
            baseline_manifest_path=baseline_path,
            post_manifest_path=None,
            preservation_report_path=report_path,
            findings=("safe_full_project_packaging_blocked_by_preservation_preflight", *preflight.findings),
        )
        if result_output:
            _write_json_result(shell, result, result_output)
        return result

    _write_package_zip(shell, zip_path)
    zip_sha = _sha256_file(zip_path)
    post = build_zip_file_manifest(zip_path, generated_at=timestamp) if previous_full_zip else build_file_manifest(shell, generated_at=timestamp)
    post_path = (shell / post_manifest_output).as_posix()
    if write_manifests:
        write_file_manifest(shell, post, post_manifest_output)

    report = compare_file_manifests(
        baseline,
        post,
        previous_full_zip=previous_full_zip,
        new_full_zip=zip_path.as_posix(),
        baseline_manifest_path=baseline_path,
        post_manifest_path=post_path,
        generated_at=timestamp,
    )
    report_path = None
    if write_report:
        report_path = write_trunk_preservation_report(shell, report, report_output).as_posix()

    zip_audit = audit_zip_root(zip_path)
    findings = list(report.findings)
    if zip_audit.root_confirmed:
        findings.append("safe_full_project_zip_root_confirmed")
    else:
        findings.extend(str(item) for item in zip_audit.findings)
    findings.append("generated_cache_and_package_artifacts_excluded_from_archive")

    result = SafeFullProjectPackageResult(
        schema_id=SCHEMA_ID,
        version_line=VERSION_LINE,
        generated_at=timestamp,
        source_root=shell.as_posix(),
        zip_creation_attempted=True,
        zip_creation_performed=True,
        zip_path=zip_path.as_posix(),
        zip_sha256=zip_sha,
        zip_root_audit=zip_audit.__dict__,
        baseline_manifest_path=baseline_path,
        post_manifest_path=post_path,
        preservation_report_path=report_path,
        preservation_report=trunk_preservation_report_to_dict(report),
        excluded_generated_paths=excluded_generated_package_paths(shell),
        accepted=bool(report.accepted and zip_audit.root_confirmed),
        production_authority=False,
        findings=tuple(findings),
    )
    if result_output:
        _write_json_result(shell, result, result_output)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a V118 no-silent-loss safe full-project zip.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--zip-output", default=None)
    parser.add_argument("--baseline-manifest", default=None)
    parser.add_argument("--previous-full-zip", default=None)
    parser.add_argument("--baseline-output", default=DEFAULT_BASELINE_MANIFEST_REL.as_posix())
    parser.add_argument("--post-output", default=DEFAULT_POST_MANIFEST_REL.as_posix())
    parser.add_argument("--report-output", default=DEFAULT_REPORT_REL.as_posix())
    parser.add_argument("--result-output", default=None)
    parser.add_argument("--no-write-manifests", action="store_true")
    parser.add_argument("--no-write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = create_safe_full_project_package(
        args.ion_root,
        output_zip=args.zip_output,
        baseline_manifest=args.baseline_manifest,
        previous_full_zip=args.previous_full_zip,
        baseline_manifest_output=args.baseline_output,
        post_manifest_output=args.post_output,
        report_output=args.report_output,
        result_output=args.result_output,
        write_manifests=not args.no_write_manifests,
        write_report=not args.no_write_report,
    )
    payload = safe_full_project_package_result_to_dict(result)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print("ION_SAFE_FULL_PROJECT_PACKAGE_PASS" if result.accepted else "ION_SAFE_FULL_PROJECT_PACKAGE_FAIL")
        print(f"zip_path: {result.zip_path}")
        print(f"preservation_report_path: {result.preservation_report_path}")
        for finding in result.findings:
            print(f"- {finding}")
    return 0 if result.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
