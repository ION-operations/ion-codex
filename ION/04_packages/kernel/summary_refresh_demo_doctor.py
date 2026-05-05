"""Operator doctor for the ION summary-refresh demo replay.

The doctor runs two complementary checks:

1. Project-root no-commit replay, safe when existing bounded graph-state files
   are already present.
2. Isolated fresh-workspace LAND replay, proving the full bounded commit path
   without colliding with live project graph-state files.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any

from .release_readiness import evaluate_release_readiness
from .summary_refresh_demo_replay import (
    SummaryRefreshDemoReplayReport,
    format_replay_summary,
    infer_workspace_root,
    run_summary_refresh_demo_replay,
)


DEFAULT_DOCTOR_REPORT_DIR = "ION/05_context/history/demo_replay_doctor_reports"
DEFAULT_SANDBOX_DIR = "ION/05_context/sandboxes/demo_replay_doctor"


@dataclass(frozen=True)
class DemoReplayDoctorModeResult:
    enabled: bool
    passed: bool
    report_path: str
    bounded_commits: int
    committed_nodes: int
    committed_edges: int
    isolated_workspace: str = ""
    error: str = ""


@dataclass(frozen=True)
class SummaryRefreshDemoReplayDoctorReport:
    doctor_id: str
    emitted_at: str
    workspace_root: str
    release_readiness: dict[str, Any]
    project_root_smoke: DemoReplayDoctorModeResult
    isolated_full_commit: DemoReplayDoctorModeResult
    boundaries: dict[str, bool]


def run_summary_refresh_demo_doctor(
    *,
    workspace_root: str | Path | None = None,
    created_at: str | None = None,
    run_project_smoke: bool = True,
    run_isolated_full_commit: bool = True,
    raw_user_text: str = "Please replay and validate the ION summary-refresh demo.",
    session_id_prefix: str = "summary-refresh-demo-doctor",
    report_dir: str | Path = DEFAULT_DOCTOR_REPORT_DIR,
    sandbox_dir: str | Path = DEFAULT_SANDBOX_DIR,
    print_summary: bool = False,
) -> tuple[SummaryRefreshDemoReplayDoctorReport, Path]:
    root = infer_workspace_root(workspace_root)
    emitted = created_at or _utc_now()
    doctor_id = _stable_id("summary-refresh-demo-doctor", root.as_posix(), emitted)

    readiness = evaluate_release_readiness(root, emitted_at=emitted)
    readiness_payload = {
        "verdict": readiness.verdict,
        "allowed": readiness.allowed,
        "passed_checks": len(readiness.passed_checks),
        "failed_checks": len(readiness.failed_checks),
        "failed_check_ids": [check.check_id for check in readiness.failed_checks],
    }

    project_result = _disabled_mode()
    if run_project_smoke:
        project_result = _run_project_smoke(
            root=root,
            emitted=emitted,
            raw_user_text=raw_user_text,
            session_id=f"{session_id_prefix}-project-root",
        )

    isolated_result = _disabled_mode()
    if run_isolated_full_commit:
        isolated_result = _run_isolated_full_commit(
            root=root,
            doctor_id=doctor_id,
            emitted=emitted,
            raw_user_text=raw_user_text,
            session_id=f"{session_id_prefix}-isolated",
            sandbox_dir=Path(sandbox_dir),
        )

    report = SummaryRefreshDemoReplayDoctorReport(
        doctor_id=doctor_id,
        emitted_at=emitted,
        workspace_root=root.as_posix(),
        release_readiness=readiness_payload,
        project_root_smoke=project_result,
        isolated_full_commit=isolated_result,
        boundaries={
            "project_root_commit_attempted": False,
            "isolated_commit_only": bool(run_isolated_full_commit),
            "source_summary_rewrite": False,
            "source_file_mutation": False,
            "registry_mutation": False,
            "schedule_mutation": False,
            "agent_activation": False,
            "global_graph_canon_claim": False,
        },
    )
    report_path = write_doctor_report(root, report, report_dir=report_dir)
    if print_summary:
        print(format_doctor_summary(report, report_path))
    return report, report_path


def write_doctor_report(
    workspace_root: Path,
    report: SummaryRefreshDemoReplayDoctorReport,
    *,
    report_dir: str | Path = DEFAULT_DOCTOR_REPORT_DIR,
) -> Path:
    output_dir = workspace_root / Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{report.doctor_id}.summary_refresh_demo_replay_doctor_report.json"
    path.write_text(json.dumps(_to_jsonable(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_doctor_summary(report: SummaryRefreshDemoReplayDoctorReport, report_path: Path) -> str:
    lines = [
        "ION summary-refresh demo replay doctor complete.",
        f"doctor_report: {report_path.as_posix()}",
        f"readiness: {report.release_readiness['verdict']} allowed={report.release_readiness['allowed']} failed={report.release_readiness['failed_checks']}",
        f"project_root_smoke: passed={report.project_root_smoke.passed} commits={report.project_root_smoke.bounded_commits} report={report.project_root_smoke.report_path}",
        f"isolated_full_commit: passed={report.isolated_full_commit.passed} commits={report.isolated_full_commit.bounded_commits} nodes={report.isolated_full_commit.committed_nodes} edges={report.isolated_full_commit.committed_edges}",
        f"isolated_workspace: {report.isolated_full_commit.isolated_workspace or '(none)'}",
    ]
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the ION summary-refresh demo replay doctor.")
    parser.add_argument("--workspace-root", default=".", help="Directory containing ION/; defaults to current directory.")
    parser.add_argument("--created-at", default=None)
    parser.add_argument("--text", default="Please replay and validate the ION summary-refresh demo.")
    parser.add_argument("--session-id-prefix", default="summary-refresh-demo-doctor")
    parser.add_argument("--report-dir", default=DEFAULT_DOCTOR_REPORT_DIR)
    parser.add_argument("--sandbox-dir", default=DEFAULT_SANDBOX_DIR)
    parser.add_argument("--skip-project-smoke", action="store_true")
    parser.add_argument("--skip-isolated-full-commit", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        report, report_path = run_summary_refresh_demo_doctor(
            workspace_root=args.workspace_root,
            created_at=args.created_at,
            run_project_smoke=not args.skip_project_smoke,
            run_isolated_full_commit=not args.skip_isolated_full_commit,
            raw_user_text=args.text,
            session_id_prefix=args.session_id_prefix,
            report_dir=args.report_dir,
            sandbox_dir=args.sandbox_dir,
            print_summary=False,
        )
    except Exception as exc:
        print(f"summary-refresh demo replay doctor failed: {exc}", file=__import__("sys").stderr)
        return 1

    if args.json:
        print(json.dumps(_to_jsonable(report), indent=2, sort_keys=True))
    else:
        print(format_doctor_summary(report, report_path))
    return 0


def _run_project_smoke(
    *,
    root: Path,
    emitted: str,
    raw_user_text: str,
    session_id: str,
) -> DemoReplayDoctorModeResult:
    try:
        replay, path = run_summary_refresh_demo_replay(
            workspace_root=root,
            raw_user_text=raw_user_text,
            session_id=session_id,
            created_at=emitted,
            run_bounded_commit=False,
            dispatch=False,
        )
        return _mode_result_from_replay(replay, path, isolated_workspace="", expect_commit=False)
    except Exception as exc:
        return DemoReplayDoctorModeResult(
            enabled=True,
            passed=False,
            report_path="",
            bounded_commits=0,
            committed_nodes=0,
            committed_edges=0,
            error=str(exc),
        )


def _run_isolated_full_commit(
    *,
    root: Path,
    doctor_id: str,
    emitted: str,
    raw_user_text: str,
    session_id: str,
    sandbox_dir: Path,
) -> DemoReplayDoctorModeResult:
    isolated = root / sandbox_dir / doctor_id
    if isolated.exists():
        shutil.rmtree(isolated)
    projection_src = root / "ION/03_registry/template_metadata_contract_registry.projection.json"
    projection_dst = isolated / "ION/03_registry/template_metadata_contract_registry.projection.json"
    projection_dst.parent.mkdir(parents=True, exist_ok=True)
    projection_dst.write_text(projection_src.read_text(encoding="utf-8"), encoding="utf-8")

    try:
        replay, path = run_summary_refresh_demo_replay(
            workspace_root=isolated,
            raw_user_text=raw_user_text,
            session_id=session_id,
            created_at=emitted,
            run_bounded_commit=True,
        )
        return _mode_result_from_replay(
            replay,
            path,
            isolated_workspace=isolated.relative_to(root).as_posix(),
            expect_commit=True,
        )
    except Exception as exc:
        return DemoReplayDoctorModeResult(
            enabled=True,
            passed=False,
            report_path="",
            bounded_commits=0,
            committed_nodes=0,
            committed_edges=0,
            isolated_workspace=isolated.relative_to(root).as_posix(),
            error=str(exc),
        )


def _mode_result_from_replay(
    replay: SummaryRefreshDemoReplayReport,
    path: Path,
    *,
    isolated_workspace: str,
    expect_commit: bool,
) -> DemoReplayDoctorModeResult:
    commits = replay.counts["bounded_commits"]
    passed = commits > 0 if expect_commit else commits == 0
    return DemoReplayDoctorModeResult(
        enabled=True,
        passed=passed,
        report_path=path.as_posix(),
        bounded_commits=commits,
        committed_nodes=replay.counts["committed_nodes"],
        committed_edges=replay.counts["committed_edges"],
        isolated_workspace=isolated_workspace,
    )


def _disabled_mode() -> DemoReplayDoctorModeResult:
    return DemoReplayDoctorModeResult(
        enabled=False,
        passed=True,
        report_path="",
        bounded_commits=0,
        committed_nodes=0,
        committed_edges=0,
    )


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
