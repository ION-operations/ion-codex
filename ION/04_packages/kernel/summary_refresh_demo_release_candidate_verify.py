"""Independent verifier for summary-refresh demo release-candidate capsules."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from .summary_refresh_demo_replay import infer_workspace_root


DEFAULT_RELEASE_CANDIDATE_ROOT = "ION/05_context/history/demo_release_candidates"
DEFAULT_VERIFICATION_REPORT_DIR = "ION/05_context/history/demo_release_candidate_verifications"


@dataclass(frozen=True)
class SummaryRefreshDemoReleaseCandidateVerification:
    verification_id: str
    emitted_at: str
    workspace_root: str
    release_candidate_dir: str
    verdict: str
    verified: bool
    failure_reasons: tuple[str, ...]
    manifest_path: str
    checksums_path: str
    commands_path: str
    readme_path: str
    evidence_bundle_dir: str
    checked_file_count: int
    checksum_mismatch_count: int
    boundary_claims_ok: bool
    manifest_summary: dict[str, Any]


class SummaryRefreshDemoReleaseCandidateVerificationError(Exception):
    """Raised when verification cannot locate a candidate."""


def verify_summary_refresh_demo_release_candidate(
    *,
    workspace_root: str | Path | None = None,
    release_candidate_dir: str | Path | None = None,
    emitted_at: str | None = None,
    allow_blocked: bool = False,
    report_dir: str | Path = DEFAULT_VERIFICATION_REPORT_DIR,
    print_summary: bool = False,
) -> tuple[SummaryRefreshDemoReleaseCandidateVerification, Path]:
    root = infer_workspace_root(workspace_root)
    timestamp = emitted_at or _utc_now()
    candidate_dir = resolve_release_candidate_dir(root, release_candidate_dir)
    verification_id = _stable_id("summary-refresh-demo-rc-verification", candidate_dir.as_posix(), timestamp)

    failures: list[str] = []
    manifest_path = candidate_dir / "summary_refresh_demo_release_candidate_manifest.json"
    checksums_path = candidate_dir / "CHECKSUMS.sha256"
    commands_path = candidate_dir / "COMMANDS.sh"
    readme_path = candidate_dir / "README.md"

    manifest: dict[str, Any] = {}
    if not candidate_dir.exists() or not candidate_dir.is_dir():
        failures.append("release_candidate_dir_missing")
    if not manifest_path.exists():
        failures.append("manifest_missing")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"manifest_unreadable:{exc}")

    for label, path in (
        ("checksums_missing", checksums_path),
        ("commands_missing", commands_path),
        ("readme_missing", readme_path),
    ):
        if not path.exists() or not path.is_file():
            failures.append(label)

    evidence_dir = candidate_dir / str(manifest.get("copied_evidence_bundle_dir", "evidence_bundle"))
    if not evidence_dir.exists() or not evidence_dir.is_dir():
        failures.append("copied_evidence_bundle_missing")

    if manifest:
        if manifest.get("verdict") != "RELEASE_CANDIDATE" and not allow_blocked:
            failures.append(f"manifest_verdict_not_release_candidate:{manifest.get('verdict')}")
        if manifest.get("certified") is not True and not allow_blocked:
            failures.append("manifest_not_certified")
        _check_required_command(manifest, "certify", failures)
        _check_required_command(manifest, "doctor", failures)
        _check_required_command(manifest, "evidence_bundle", failures)
        _check_required_command(manifest, "release_candidate", failures)

    checked_count, mismatch_count, checksum_failures = verify_checksum_file(candidate_dir, checksums_path)
    failures.extend(checksum_failures)

    boundary_ok = _boundary_claims_ok(manifest)
    if not boundary_ok:
        failures.append("forbidden_boundary_claim_true")

    verified = not failures
    verification = SummaryRefreshDemoReleaseCandidateVerification(
        verification_id=verification_id,
        emitted_at=timestamp,
        workspace_root=root.as_posix(),
        release_candidate_dir=_rel(root, candidate_dir),
        verdict="VERIFIED" if verified else "FAILED",
        verified=verified,
        failure_reasons=tuple(failures),
        manifest_path=_rel(root, manifest_path),
        checksums_path=_rel(root, checksums_path),
        commands_path=_rel(root, commands_path),
        readme_path=_rel(root, readme_path),
        evidence_bundle_dir=_rel(root, evidence_dir),
        checked_file_count=checked_count,
        checksum_mismatch_count=mismatch_count,
        boundary_claims_ok=boundary_ok,
        manifest_summary={
            "release_candidate_id": manifest.get("release_candidate_id", ""),
            "verdict": manifest.get("verdict", ""),
            "certified": manifest.get("certified", False),
            "evidence_bundle_id": manifest.get("evidence_bundle_id", ""),
        },
    )
    report_path = write_release_candidate_verification_report(root, verification, report_dir=report_dir)
    if print_summary:
        print(format_release_candidate_verification_summary(verification, report_path))
    return verification, report_path


def resolve_release_candidate_dir(root: Path, release_candidate_dir: str | Path | None = None) -> Path:
    if release_candidate_dir:
        path = Path(release_candidate_dir)
        return path if path.is_absolute() else root / path

    candidates_root = root / DEFAULT_RELEASE_CANDIDATE_ROOT
    candidates = [
        p for p in candidates_root.iterdir()
        if p.is_dir() and (p / "summary_refresh_demo_release_candidate_manifest.json").exists()
    ] if candidates_root.exists() else []
    if not candidates:
        raise SummaryRefreshDemoReleaseCandidateVerificationError("no_release_candidate_capsules_found")
    return sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]


def verify_checksum_file(candidate_dir: Path, checksums_path: Path) -> tuple[int, int, list[str]]:
    failures: list[str] = []
    checked = 0
    mismatches = 0
    if not checksums_path.exists() or not checksums_path.is_file():
        return 0, 0, failures

    for idx, line in enumerate(checksums_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            expected, rel = line.split("  ", 1)
        except ValueError:
            failures.append(f"checksum_line_malformed:{idx}")
            continue
        path = candidate_dir / rel
        if not path.exists() or not path.is_file():
            failures.append(f"checksum_file_missing:{rel}")
            mismatches += 1
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        checked += 1
        if actual != expected:
            failures.append(f"checksum_mismatch:{rel}")
            mismatches += 1
    return checked, mismatches, failures


def write_release_candidate_verification_report(
    workspace_root: Path,
    verification: SummaryRefreshDemoReleaseCandidateVerification,
    *,
    report_dir: str | Path = DEFAULT_VERIFICATION_REPORT_DIR,
) -> Path:
    output_dir = workspace_root / Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{verification.verification_id}.summary_refresh_demo_release_candidate_verification_report.json"
    path.write_text(json.dumps(_to_jsonable(verification), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_release_candidate_verification_summary(
    verification: SummaryRefreshDemoReleaseCandidateVerification,
    report_path: Path,
) -> str:
    return "\n".join(
        [
            "ION summary-refresh demo release-candidate verification complete.",
            f"verification_report: {report_path.as_posix()}",
            f"release_candidate_dir: {verification.release_candidate_dir}",
            f"verdict: {verification.verdict}",
            f"verified: {verification.verified}",
            f"checked_files: {verification.checked_file_count}",
            f"checksum_mismatches: {verification.checksum_mismatch_count}",
            f"boundary_claims_ok: {verification.boundary_claims_ok}",
            f"failure_reasons: {', '.join(verification.failure_reasons) if verification.failure_reasons else '(none)'}",
        ]
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Verify an ION summary-refresh demo release-candidate capsule.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--release-candidate-dir", default=None)
    parser.add_argument("--emitted-at", default=None)
    parser.add_argument("--allow-blocked", action="store_true")
    parser.add_argument("--report-dir", default=DEFAULT_VERIFICATION_REPORT_DIR)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        verification, report_path = verify_summary_refresh_demo_release_candidate(
            workspace_root=args.workspace_root,
            release_candidate_dir=args.release_candidate_dir,
            emitted_at=args.emitted_at,
            allow_blocked=args.allow_blocked,
            report_dir=args.report_dir,
        )
    except Exception as exc:
        print(f"summary-refresh demo release-candidate verification failed: {exc}", file=__import__("sys").stderr)
        return 1

    if args.json:
        print(json.dumps(_to_jsonable(verification), indent=2, sort_keys=True))
    else:
        print(format_release_candidate_verification_summary(verification, report_path))
    return 0 if verification.verified else 2


def _check_required_command(manifest: dict[str, Any], command_name: str, failures: list[str]) -> None:
    commands = manifest.get("commands", {})
    value = commands.get(command_name, "")
    if not value or "python -S -m kernel." not in value:
        failures.append(f"required_command_missing_or_invalid:{command_name}")


def _boundary_claims_ok(manifest: dict[str, Any]) -> bool:
    boundaries = manifest.get("boundaries", {})
    forbidden = (
        "source_summary_rewrite",
        "source_file_mutation",
        "registry_mutation",
        "schedule_mutation",
        "agent_activation",
        "global_graph_canon_claim",
        "constitutional_ratification_claim",
    )
    return all(boundaries.get(key) is False for key in forbidden)


def _rel(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\n".join(part for part in parts if part).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    return value


if __name__ == "__main__":
    raise SystemExit(main())
