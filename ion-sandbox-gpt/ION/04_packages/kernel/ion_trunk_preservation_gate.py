"""ION trunk preservation gate.

This module records project file manifests and compares them across a mutation
or package build. Its purpose is narrow: no project file may be silently lost.
Files may leave hot paths only when they are either generated/cache byproducts
or proven containment moves with matching SHA-256 evidence. It does not delete,
move, or accept trunk state and does not claim production authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

VERSION_LINE = "V118_NO_SILENT_LOSS_AND_CONTAINMENT_PRESERVATION_GATE"
MANIFEST_SCHEMA_ID = "ion.trunk_file_manifest.v1"
REPORT_SCHEMA_ID = "ion.trunk_preservation_report.v1"
POLICY_VERSION = "V118_NO_SILENT_LOSS_CONTAINMENT_POLICY"

ROOT_REQUIRED_FILES = ("pyproject.toml", "ION/REPO_AUTHORITY.md")
DEFAULT_BASELINE_MANIFEST_REL = Path("ION/05_context/current/TRUNK_FILE_MANIFEST_BASELINE_V118.json")
DEFAULT_POST_MANIFEST_REL = Path("ION/05_context/current/TRUNK_FILE_MANIFEST_POSTPATCH_V118.json")
DEFAULT_REPORT_REL = Path("ION/05_context/current/TRUNK_PRESERVATION_REPORT_V118.json")

PROTECTED_PATHS = (
    "AGENTS.md",
    "START_HERE_FOR_ANY_AGENT.md",
    "pyproject.toml",
    "ION/REPO_AUTHORITY.md",
    "ION/00_BOOTSTRAP/",
    "ION/01_doctrine/",
    "ION/02_architecture/",
    "ION/03_registry/",
    "ION/04_packages/kernel/",
    "ION/05_context/current/",
    "ION/07_templates/",
    "ION/08_ui/",
    "ION/09_integrations/",
    "ION/tests/",
)

ALLOWED_REMOVAL_PARTS = (
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
)
ALLOWED_REMOVAL_PREFIXES = (
    "_tmp",
    "tmp",
    "scratch",
    "ION/05_context/current/_tmp",
    "ION/05_context/current/tmp",
    "ION/05_context/current/scratch",
)
ALLOWED_REMOVAL_SUFFIXES = (".pyc", ".pyo")
CONTAINMENT_MOVE_PREFIXES = (
    "ION/05_context/archive/containment/",
    "ION/05_context/quarantine/",
    "ION/05_context/current/containment/",
    "ION/06_artifacts/containment/",
)
MANIFEST_SKIP_PREFIXES = (".git/",)


@dataclass(frozen=True)
class FileManifestEntry:
    path: str
    size: int
    sha256: str


@dataclass(frozen=True)
class TrunkFileManifest:
    schema_id: str
    version_line: str
    generated_at: str
    source_root: str
    root_confirmed: bool
    root_required_files: tuple[str, ...]
    root_missing_files: tuple[str, ...]
    file_count: int
    total_bytes: int
    hash_algorithm: str
    skipped_paths: tuple[str, ...]
    files: dict[str, FileManifestEntry]


@dataclass(frozen=True)
class TrunkPreservationReport:
    schema_id: str
    version_line: str
    report_id: str
    generated_at: str
    source_root: str | None
    previous_full_zip: str | None
    new_full_zip: str | None
    baseline_manifest_path: str | None
    post_manifest_path: str | None
    policy_version: str
    protected_paths: tuple[str, ...]
    allowed_removal_parts: tuple[str, ...]
    allowed_removal_prefixes: tuple[str, ...]
    containment_move_prefixes: tuple[str, ...]
    files_before: int
    files_after: int
    added_files: int
    modified_files: int
    removed_files: int
    allowed_removed_files: int
    contained_removed_files: int
    unexpected_removed_files: int
    protected_removed_files: int
    added_paths: tuple[str, ...]
    modified_paths: tuple[str, ...]
    allowed_removed_paths: tuple[str, ...]
    contained_removed_paths: tuple[str, ...]
    containment_moves: tuple[dict[str, str], ...]
    unexpected_removed_paths: tuple[str, ...]
    protected_removed_paths: tuple[str, ...]
    root_confirmed_before: bool
    root_confirmed_after: bool
    packaging_verdict: str
    accepted: bool
    production_authority: bool
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


def _normalize_rel(path: str | Path) -> str:
    rel = Path(path).as_posix()
    while rel.startswith("./"):
        rel = rel[2:]
    return rel


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _should_skip_manifest_path(rel: Path) -> bool:
    rel_posix = rel.as_posix()
    return any(rel_posix == prefix.rstrip("/") or rel_posix.startswith(prefix) for prefix in MANIFEST_SKIP_PREFIXES)


def _root_missing(shell: Path) -> tuple[str, ...]:
    return tuple(rel for rel in ROOT_REQUIRED_FILES if not (shell / rel).exists())


def build_file_manifest(
    root: str | Path,
    *,
    generated_at: str | None = None,
) -> TrunkFileManifest:
    shell = _shell_root(root)
    timestamp = generated_at or _now()
    missing = _root_missing(shell)
    files: dict[str, FileManifestEntry] = {}
    skipped: list[str] = []
    total_bytes = 0

    for child in sorted(shell.rglob("*")):
        if not child.is_file():
            continue
        rel = child.relative_to(shell)
        rel_posix = rel.as_posix()
        if child.is_symlink() or _should_skip_manifest_path(rel):
            skipped.append(rel_posix)
            continue
        size = child.stat().st_size
        digest = _sha256_file(child)
        files[rel_posix] = FileManifestEntry(path=rel_posix, size=size, sha256=digest)
        total_bytes += size

    return TrunkFileManifest(
        schema_id=MANIFEST_SCHEMA_ID,
        version_line=VERSION_LINE,
        generated_at=timestamp,
        source_root=shell.as_posix(),
        root_confirmed=not missing,
        root_required_files=ROOT_REQUIRED_FILES,
        root_missing_files=missing,
        file_count=len(files),
        total_bytes=total_bytes,
        hash_algorithm="sha256",
        skipped_paths=tuple(sorted(skipped)),
        files=files,
    )


def _zip_root_prefix(files: set[str]) -> str | None:
    if all(required in files for required in ROOT_REQUIRED_FILES):
        return None
    candidate_prefixes: set[str] = set()
    for name in files:
        for required in ROOT_REQUIRED_FILES:
            suffix = f"/{required}"
            if name.endswith(suffix):
                candidate_prefixes.add(name[: -len(suffix)])
    matches = [
        prefix
        for prefix in sorted(candidate_prefixes)
        if all(f"{prefix}/{required}" in files for required in ROOT_REQUIRED_FILES)
    ]
    return matches[0] if len(matches) == 1 else None


def build_zip_file_manifest(
    zip_path: str | Path,
    *,
    generated_at: str | None = None,
) -> TrunkFileManifest:
    """Build a normalized file manifest from a full-project zip.

    If the archive has one wrapper shell root, paths are normalized by stripping
    that wrapper prefix before comparison. This lets the preservation gate
    compare older wrapped ChatGPT-browser zips against new canonical-root safe
    packages.
    """

    path = Path(zip_path).expanduser().resolve()
    timestamp = generated_at or _now()
    files: dict[str, FileManifestEntry] = {}
    skipped: list[str] = []
    total_bytes = 0
    if not path.exists():
        return TrunkFileManifest(
            schema_id=MANIFEST_SCHEMA_ID,
            version_line=VERSION_LINE,
            generated_at=timestamp,
            source_root=path.as_posix(),
            root_confirmed=False,
            root_required_files=ROOT_REQUIRED_FILES,
            root_missing_files=ROOT_REQUIRED_FILES,
            file_count=0,
            total_bytes=0,
            hash_algorithm="sha256",
            skipped_paths=("zip_file_not_found",),
            files={},
        )

    with zipfile.ZipFile(path) as package:
        raw_names = {info.filename.rstrip("/") for info in package.infolist() if not info.is_dir()}
        prefix = _zip_root_prefix(raw_names)
        for info in sorted(package.infolist(), key=lambda item: item.filename):
            if info.is_dir():
                continue
            raw_name = info.filename.rstrip("/")
            if prefix and raw_name.startswith(prefix + "/"):
                rel = raw_name[len(prefix) + 1 :]
            else:
                rel = raw_name
            if not rel or rel.startswith("../") or rel.startswith("/"):
                skipped.append(raw_name)
                continue
            digest = hashlib.sha256(package.read(info.filename)).hexdigest()
            files[rel] = FileManifestEntry(path=rel, size=info.file_size, sha256=digest)
            total_bytes += info.file_size

    missing = tuple(required for required in ROOT_REQUIRED_FILES if required not in files)
    return TrunkFileManifest(
        schema_id=MANIFEST_SCHEMA_ID,
        version_line=VERSION_LINE,
        generated_at=timestamp,
        source_root=path.as_posix(),
        root_confirmed=not missing,
        root_required_files=ROOT_REQUIRED_FILES,
        root_missing_files=missing,
        file_count=len(files),
        total_bytes=total_bytes,
        hash_algorithm="sha256",
        skipped_paths=tuple(sorted(skipped)),
        files=files,
    )


def trunk_file_manifest_to_dict(manifest: TrunkFileManifest) -> dict[str, Any]:
    value = _asdict(manifest)
    assert isinstance(value, dict)
    return value


def trunk_preservation_report_to_dict(report: TrunkPreservationReport) -> dict[str, Any]:
    value = _asdict(report)
    assert isinstance(value, dict)
    return value


def _entry_from_dict(path: str, payload: Mapping[str, Any]) -> FileManifestEntry:
    return FileManifestEntry(
        path=str(payload.get("path") or path),
        size=int(payload.get("size", 0)),
        sha256=str(payload.get("sha256", "")),
    )


def manifest_from_dict(payload: Mapping[str, Any]) -> TrunkFileManifest:
    files_payload = payload.get("files", {})
    files: dict[str, FileManifestEntry] = {}
    if isinstance(files_payload, Mapping):
        for path, entry in files_payload.items():
            if isinstance(entry, Mapping):
                files[str(path)] = _entry_from_dict(str(path), entry)

    return TrunkFileManifest(
        schema_id=str(payload.get("schema_id", MANIFEST_SCHEMA_ID)),
        version_line=str(payload.get("version_line", VERSION_LINE)),
        generated_at=str(payload.get("generated_at", "")),
        source_root=str(payload.get("source_root", "")),
        root_confirmed=bool(payload.get("root_confirmed", False)),
        root_required_files=tuple(str(item) for item in payload.get("root_required_files", ROOT_REQUIRED_FILES)),
        root_missing_files=tuple(str(item) for item in payload.get("root_missing_files", ())),
        file_count=int(payload.get("file_count", len(files))),
        total_bytes=int(payload.get("total_bytes", sum(entry.size for entry in files.values()))),
        hash_algorithm=str(payload.get("hash_algorithm", "sha256")),
        skipped_paths=tuple(str(item) for item in payload.get("skipped_paths", ())),
        files=files,
    )


def read_file_manifest(path: str | Path) -> TrunkFileManifest:
    payload = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    return manifest_from_dict(payload)


def write_file_manifest(root: str | Path, manifest: TrunkFileManifest, output: str | Path) -> Path:
    shell = _shell_root(root)
    candidate = Path(output).expanduser()
    path = candidate if candidate.is_absolute() else shell / candidate
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(trunk_file_manifest_to_dict(manifest), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _is_allowed_generated_removal(path: str) -> bool:
    rel = _normalize_rel(path)
    parts = Path(rel).parts
    if any(part in ALLOWED_REMOVAL_PARTS for part in parts):
        return True
    if any(rel == prefix.rstrip("/") or rel.startswith(prefix.rstrip("/") + "/") for prefix in ALLOWED_REMOVAL_PREFIXES):
        return True
    return rel.endswith(ALLOWED_REMOVAL_SUFFIXES)


def _is_protected_path(path: str) -> bool:
    rel = _normalize_rel(path)
    for protected in PROTECTED_PATHS:
        protected_rel = protected.rstrip("/")
        if protected.endswith("/"):
            if rel == protected_rel or rel.startswith(protected_rel + "/"):
                return True
        elif rel == protected_rel:
            return True
    return False


def _is_containment_path(path: str) -> bool:
    rel = _normalize_rel(path)
    return any(rel == prefix.rstrip("/") or rel.startswith(prefix) for prefix in CONTAINMENT_MOVE_PREFIXES)


def _containment_moves_for_removed_paths(
    before_manifest: TrunkFileManifest,
    after_manifest: TrunkFileManifest,
    added_paths: tuple[str, ...],
    removed_paths: tuple[str, ...],
) -> dict[str, dict[str, str]]:
    """Map removed paths to added containment copies with identical hashes."""

    added_by_hash: dict[str, list[str]] = {}
    for path in added_paths:
        if not _is_containment_path(path):
            continue
        entry = after_manifest.files.get(path)
        if entry is None:
            continue
        added_by_hash.setdefault(entry.sha256, []).append(path)

    moves: dict[str, dict[str, str]] = {}
    used_targets: set[str] = set()
    for path in removed_paths:
        entry = before_manifest.files[path]
        candidates = [candidate for candidate in sorted(added_by_hash.get(entry.sha256, [])) if candidate not in used_targets]
        if not candidates:
            continue
        target = candidates[0]
        used_targets.add(target)
        moves[path] = {
            "from_path": path,
            "to_path": target,
            "sha256": entry.sha256,
            "movement_class": "CONTAINMENT_MOVE",
        }
    return moves


def compare_file_manifests(
    before: TrunkFileManifest | Mapping[str, Any],
    after: TrunkFileManifest | Mapping[str, Any],
    *,
    previous_full_zip: str | None = None,
    new_full_zip: str | None = None,
    baseline_manifest_path: str | None = None,
    post_manifest_path: str | None = None,
    generated_at: str | None = None,
) -> TrunkPreservationReport:
    before_manifest = manifest_from_dict(before) if isinstance(before, Mapping) else before
    after_manifest = manifest_from_dict(after) if isinstance(after, Mapping) else after
    timestamp = generated_at or _now()

    before_paths = set(before_manifest.files)
    after_paths = set(after_manifest.files)
    added = tuple(sorted(after_paths - before_paths))
    removed = tuple(sorted(before_paths - after_paths))
    modified = tuple(
        sorted(
            path
            for path in before_paths & after_paths
            if before_manifest.files[path].sha256 != after_manifest.files[path].sha256
            or before_manifest.files[path].size != after_manifest.files[path].size
        )
    )

    containment_moves = _containment_moves_for_removed_paths(before_manifest, after_manifest, added, removed)
    allowed_removed: list[str] = []
    contained_removed: list[str] = []
    protected_removed: list[str] = []
    unexpected_removed: list[str] = []
    for path in removed:
        if _is_allowed_generated_removal(path):
            allowed_removed.append(path)
        elif path in containment_moves:
            contained_removed.append(path)
        elif _is_protected_path(path):
            protected_removed.append(path)
        else:
            unexpected_removed.append(path)

    findings: list[str] = []
    if not before_manifest.root_confirmed:
        findings.append("baseline_shell_root_not_confirmed")
    if not after_manifest.root_confirmed:
        findings.append("post_shell_root_not_confirmed")
    if added:
        findings.append("added_files_recorded")
    if modified:
        findings.append("modified_files_recorded")
    if allowed_removed:
        findings.append("allowed_generated_or_cache_removals_recorded")
    if contained_removed:
        findings.append("contained_project_file_moves_recorded")
    if protected_removed:
        findings.append("protected_project_organ_removed_without_containment")
    if unexpected_removed:
        findings.append("unexpected_project_file_removed_without_containment")
    if not protected_removed and not unexpected_removed:
        findings.append("no_silent_loss_gate_passed")

    accepted = (
        before_manifest.root_confirmed
        and after_manifest.root_confirmed
        and not protected_removed
        and not unexpected_removed
    )
    verdict = "PASS" if accepted else "FAIL"
    report_id = _stable_id(
        "trunk-preservation-report",
        before_manifest.generated_at,
        after_manifest.generated_at,
        str(len(added)),
        str(len(modified)),
        str(len(removed)),
        verdict,
    )
    return TrunkPreservationReport(
        schema_id=REPORT_SCHEMA_ID,
        version_line=VERSION_LINE,
        report_id=report_id,
        generated_at=timestamp,
        source_root=after_manifest.source_root or before_manifest.source_root or None,
        previous_full_zip=previous_full_zip,
        new_full_zip=new_full_zip,
        baseline_manifest_path=baseline_manifest_path,
        post_manifest_path=post_manifest_path,
        policy_version=POLICY_VERSION,
        protected_paths=PROTECTED_PATHS,
        allowed_removal_parts=ALLOWED_REMOVAL_PARTS,
        allowed_removal_prefixes=ALLOWED_REMOVAL_PREFIXES,
        containment_move_prefixes=CONTAINMENT_MOVE_PREFIXES,
        files_before=before_manifest.file_count,
        files_after=after_manifest.file_count,
        added_files=len(added),
        modified_files=len(modified),
        removed_files=len(removed),
        allowed_removed_files=len(allowed_removed),
        contained_removed_files=len(contained_removed),
        unexpected_removed_files=len(unexpected_removed),
        protected_removed_files=len(protected_removed),
        added_paths=added,
        modified_paths=modified,
        allowed_removed_paths=tuple(sorted(allowed_removed)),
        contained_removed_paths=tuple(sorted(contained_removed)),
        containment_moves=tuple(containment_moves[path] for path in sorted(contained_removed)),
        unexpected_removed_paths=tuple(sorted(unexpected_removed)),
        protected_removed_paths=tuple(sorted(protected_removed)),
        root_confirmed_before=before_manifest.root_confirmed,
        root_confirmed_after=after_manifest.root_confirmed,
        packaging_verdict=verdict,
        accepted=accepted,
        production_authority=False,
        findings=tuple(findings),
    )


def write_trunk_preservation_report(root: str | Path, report: TrunkPreservationReport, output: str | Path | None = None) -> Path:
    shell = _shell_root(root)
    rel = Path(output) if output else DEFAULT_REPORT_REL
    path = rel if rel.is_absolute() else shell / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(trunk_preservation_report_to_dict(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and compare ION trunk preservation file manifests.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write-baseline", action="store_true")
    parser.add_argument("--write-post", action="store_true")
    parser.add_argument("--manifest-from-zip", default=None)
    parser.add_argument("--baseline-output", default=DEFAULT_BASELINE_MANIFEST_REL.as_posix())
    parser.add_argument("--post-output", default=DEFAULT_POST_MANIFEST_REL.as_posix())
    parser.add_argument("--compare", action="store_true")
    parser.add_argument("--baseline-manifest", default=None)
    parser.add_argument("--post-manifest", default=None)
    parser.add_argument("--previous-full-zip", default=None)
    parser.add_argument("--new-full-zip", default=None)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--report-output", default=DEFAULT_REPORT_REL.as_posix())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    shell = _shell_root(args.ion_root)
    emitted_at = _now()

    if args.write_baseline:
        manifest = (
            build_zip_file_manifest(args.manifest_from_zip, generated_at=emitted_at)
            if args.manifest_from_zip
            else build_file_manifest(shell, generated_at=emitted_at)
        )
        out = write_file_manifest(shell, manifest, args.baseline_output)
        if args.json:
            print(json.dumps({"manifest_path": out.as_posix(), **trunk_file_manifest_to_dict(manifest)}, indent=2, sort_keys=True))
        else:
            print(f"ION_TRUNK_BASELINE_MANIFEST_WRITTEN {out}")
        return 0 if manifest.root_confirmed else 1

    if args.write_post:
        manifest = (
            build_zip_file_manifest(args.manifest_from_zip, generated_at=emitted_at)
            if args.manifest_from_zip
            else build_file_manifest(shell, generated_at=emitted_at)
        )
        out = write_file_manifest(shell, manifest, args.post_output)
        if args.json:
            print(json.dumps({"manifest_path": out.as_posix(), **trunk_file_manifest_to_dict(manifest)}, indent=2, sort_keys=True))
        else:
            print(f"ION_TRUNK_POST_MANIFEST_WRITTEN {out}")
        return 0 if manifest.root_confirmed else 1

    if args.compare:
        baseline_path = Path(args.baseline_manifest or shell / DEFAULT_BASELINE_MANIFEST_REL)
        post_path = Path(args.post_manifest or shell / DEFAULT_POST_MANIFEST_REL)
        before = read_file_manifest(baseline_path)
        after = read_file_manifest(post_path)
        report = compare_file_manifests(
            before,
            after,
            previous_full_zip=args.previous_full_zip,
            new_full_zip=args.new_full_zip,
            baseline_manifest_path=baseline_path.as_posix(),
            post_manifest_path=post_path.as_posix(),
            generated_at=emitted_at,
        )
        if args.write_report:
            write_trunk_preservation_report(shell, report, args.report_output)
        if args.json:
            print(json.dumps(trunk_preservation_report_to_dict(report), indent=2, sort_keys=True))
        else:
            print(f"ION_TRUNK_PRESERVATION_{report.packaging_verdict}")
            for finding in report.findings:
                print(f"- {finding}")
        return 0 if report.accepted else 1

    manifest = (
        build_zip_file_manifest(args.manifest_from_zip, generated_at=emitted_at)
        if args.manifest_from_zip
        else build_file_manifest(shell, generated_at=emitted_at)
    )
    if args.json:
        print(json.dumps(trunk_file_manifest_to_dict(manifest), indent=2, sort_keys=True))
    else:
        print(f"ION_TRUNK_FILE_MANIFEST file_count={manifest.file_count} root_confirmed={manifest.root_confirmed}")
    return 0 if manifest.root_confirmed else 1


if __name__ == "__main__":
    raise SystemExit(main())
