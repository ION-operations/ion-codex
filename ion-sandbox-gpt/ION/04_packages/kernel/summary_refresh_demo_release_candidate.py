"""Release-candidate capsule assembly for the certified summary-refresh demo."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any

from .summary_refresh_demo_evidence_bundle import (
    SummaryRefreshDemoEvidenceBundle,
    SummaryRefreshDemoEvidenceBundleError,
    create_summary_refresh_demo_evidence_bundle,
)
from .summary_refresh_demo_replay import infer_workspace_root


DEFAULT_RELEASE_CANDIDATE_DIR = "ION/05_context/history/demo_release_candidates"


@dataclass(frozen=True)
class SummaryRefreshDemoReleaseCandidate:
    release_candidate_id: str
    emitted_at: str
    workspace_root: str
    release_candidate_dir: str
    verdict: str
    certified: bool
    failure_reasons: tuple[str, ...]
    evidence_bundle_id: str
    evidence_bundle_dir: str
    evidence_bundle_manifest_path: str
    copied_evidence_bundle_dir: str
    checksums_path: str
    commands_path: str
    readme_path: str
    commands: dict[str, str]
    readiness: dict[str, Any]
    certification: dict[str, Any]
    boundaries: dict[str, bool]


class SummaryRefreshDemoReleaseCandidateError(Exception):
    """Raised when release-candidate capsule creation is blocked."""


def create_summary_refresh_demo_release_candidate(
    *,
    workspace_root: str | Path | None = None,
    created_at: str | None = None,
    raw_user_text: str = "Please certify, bundle, and package the ION summary-refresh release candidate.",
    session_id_prefix: str = "summary-refresh-demo-release-candidate",
    release_candidate_root: str | Path = DEFAULT_RELEASE_CANDIDATE_DIR,
    allow_blocked: bool = False,
    run_project_smoke: bool = True,
    run_isolated_full_commit: bool = True,
    print_summary: bool = False,
) -> tuple[SummaryRefreshDemoReleaseCandidate, Path]:
    root = infer_workspace_root(workspace_root)
    emitted = created_at or _utc_now()

    try:
        bundle, bundle_manifest_path = create_summary_refresh_demo_evidence_bundle(
            workspace_root=root,
            created_at=emitted,
            raw_user_text=raw_user_text,
            session_id_prefix=session_id_prefix,
            allow_blocked=allow_blocked,
            run_project_smoke=run_project_smoke,
            run_isolated_full_commit=run_isolated_full_commit,
        )
    except SummaryRefreshDemoEvidenceBundleError as exc:
        if not allow_blocked:
            raise SummaryRefreshDemoReleaseCandidateError(str(exc)) from exc
        raise

    if not bundle.certified and not allow_blocked:
        raise SummaryRefreshDemoReleaseCandidateError(
            "evidence_bundle_not_certified:" + ",".join(bundle.failure_reasons)
        )

    rc_id = _stable_id("summary-refresh-demo-release-candidate", root.as_posix(), emitted)
    rc_dir = root / Path(release_candidate_root) / rc_id
    if rc_dir.exists():
        shutil.rmtree(rc_dir)
    rc_dir.mkdir(parents=True, exist_ok=True)

    copied_bundle_dir = rc_dir / "evidence_bundle"
    source_bundle_dir = root / bundle.bundle_dir
    if source_bundle_dir.exists() and source_bundle_dir.is_dir():
        shutil.copytree(source_bundle_dir, copied_bundle_dir)
    else:
        copied_bundle_dir.mkdir(parents=True, exist_ok=True)

    commands = {
        "certify": "PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_certification --workspace-root .",
        "doctor": "PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_doctor --workspace-root .",
        "evidence_bundle": "PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_evidence_bundle --workspace-root .",
        "release_candidate": "PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_release_candidate --workspace-root .",
        "safe_replay_no_commit": "PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_replay --workspace-root . --no-commit --no-dispatch",
    }

    candidate = SummaryRefreshDemoReleaseCandidate(
        release_candidate_id=rc_id,
        emitted_at=emitted,
        workspace_root=root.as_posix(),
        release_candidate_dir=rc_dir.relative_to(root).as_posix(),
        verdict="RELEASE_CANDIDATE" if bundle.certified else "BLOCKED",
        certified=bundle.certified,
        failure_reasons=tuple(bundle.failure_reasons),
        evidence_bundle_id=bundle.bundle_id,
        evidence_bundle_dir=bundle.bundle_dir,
        evidence_bundle_manifest_path=_rel(root, bundle_manifest_path),
        copied_evidence_bundle_dir=copied_bundle_dir.relative_to(rc_dir).as_posix(),
        checksums_path="CHECKSUMS.sha256",
        commands_path="COMMANDS.sh",
        readme_path="README.md",
        commands=commands,
        readiness=dict(bundle.readiness),
        certification=dict(bundle.certification),
        boundaries={
            "source_summary_rewrite": False,
            "source_file_mutation": False,
            "registry_mutation": False,
            "schedule_mutation": False,
            "agent_activation": False,
            "global_graph_canon_claim": False,
            "constitutional_ratification_claim": False,
            "release_candidate_packaging_only": True,
        },
    )

    manifest_path = write_release_candidate_manifest(rc_dir, candidate)
    write_release_candidate_commands(rc_dir, candidate)
    write_release_candidate_readme(rc_dir, candidate, manifest_path)
    write_release_candidate_checksums(rc_dir)

    if print_summary:
        print(format_release_candidate_summary(candidate, manifest_path))
    return candidate, manifest_path


def write_release_candidate_manifest(
    release_candidate_dir: Path,
    candidate: SummaryRefreshDemoReleaseCandidate,
) -> Path:
    path = release_candidate_dir / "summary_refresh_demo_release_candidate_manifest.json"
    path.write_text(json.dumps(_to_jsonable(candidate), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_release_candidate_commands(
    release_candidate_dir: Path,
    candidate: SummaryRefreshDemoReleaseCandidate,
) -> Path:
    path = release_candidate_dir / "COMMANDS.sh"
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        "# ION summary-refresh demo release-candidate commands",
    ]
    for name, command in candidate.commands.items():
        lines.append("")
        lines.append(f"# {name}")
        lines.append(command)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_release_candidate_readme(
    release_candidate_dir: Path,
    candidate: SummaryRefreshDemoReleaseCandidate,
    manifest_path: Path,
) -> Path:
    path = release_candidate_dir / "README.md"
    lines = [
        "# Summary Refresh Demo Release Candidate",
        "",
        f"**Release Candidate ID:** `{candidate.release_candidate_id}`",
        f"**Verdict:** `{candidate.verdict}`",
        f"**Certified:** `{candidate.certified}`",
        f"**Manifest:** `{manifest_path.name}`",
        "",
        "## Run",
        "",
        "```bash",
        candidate.commands["release_candidate"],
        "```",
        "",
        "## Evidence",
        "",
        f"- Evidence bundle ID: `{candidate.evidence_bundle_id}`",
        f"- Copied evidence bundle: `{candidate.copied_evidence_bundle_dir}`",
        f"- Isolated bounded commits: `{candidate.certification.get('isolated_bounded_commits', 0)}`",
        f"- Isolated committed nodes: `{candidate.certification.get('isolated_committed_nodes', 0)}`",
        f"- Isolated committed edges: `{candidate.certification.get('isolated_committed_edges', 0)}`",
        "",
        "## Boundary",
        "",
        "This release candidate packages certified demo evidence only. It does not claim full product completion, global graph canon, source-summary rewrite authority, agent activation authority, or constitutional ratification.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_release_candidate_checksums(release_candidate_dir: Path) -> Path:
    path = release_candidate_dir / "CHECKSUMS.sha256"
    lines: list[str] = []
    for file_path in sorted(release_candidate_dir.rglob("*")):
        if file_path.is_file() and file_path.name != "CHECKSUMS.sha256":
            digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {file_path.relative_to(release_candidate_dir).as_posix()}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def format_release_candidate_summary(candidate: SummaryRefreshDemoReleaseCandidate, manifest_path: Path) -> str:
    return "\n".join(
        [
            "ION summary-refresh demo release candidate complete.",
            f"release_candidate_id: {candidate.release_candidate_id}",
            f"manifest: {manifest_path.as_posix()}",
            f"verdict: {candidate.verdict}",
            f"certified: {candidate.certified}",
            f"release_candidate_dir: {candidate.release_candidate_dir}",
            f"evidence_bundle_id: {candidate.evidence_bundle_id}",
            f"isolated_bounded_commits: {candidate.certification.get('isolated_bounded_commits', 0)}",
            f"isolated_committed_nodes: {candidate.certification.get('isolated_committed_nodes', 0)}",
            f"isolated_committed_edges: {candidate.certification.get('isolated_committed_edges', 0)}",
        ]
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a release-candidate capsule for the certified ION summary-refresh demo.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--created-at", default=None)
    parser.add_argument("--text", default="Please certify, bundle, and package the ION summary-refresh release candidate.")
    parser.add_argument("--session-id-prefix", default="summary-refresh-demo-release-candidate")
    parser.add_argument("--release-candidate-root", default=DEFAULT_RELEASE_CANDIDATE_DIR)
    parser.add_argument("--allow-blocked", action="store_true")
    parser.add_argument("--skip-project-smoke", action="store_true")
    parser.add_argument("--skip-isolated-full-commit", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        candidate, manifest_path = create_summary_refresh_demo_release_candidate(
            workspace_root=args.workspace_root,
            created_at=args.created_at,
            raw_user_text=args.text,
            session_id_prefix=args.session_id_prefix,
            release_candidate_root=args.release_candidate_root,
            allow_blocked=args.allow_blocked,
            run_project_smoke=not args.skip_project_smoke,
            run_isolated_full_commit=not args.skip_isolated_full_commit,
        )
    except Exception as exc:
        print(f"summary-refresh demo release candidate failed: {exc}", file=__import__("sys").stderr)
        return 1
    if args.json:
        print(json.dumps(_to_jsonable(candidate), indent=2, sort_keys=True))
    else:
        print(format_release_candidate_summary(candidate, manifest_path))
    return 0 if candidate.certified else 2


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
