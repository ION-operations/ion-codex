"""Certification gate for the complete ION summary-refresh release demo."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from .summary_refresh_demo_doctor import (
    SummaryRefreshDemoReplayDoctorReport,
    format_doctor_summary,
    run_summary_refresh_demo_doctor,
)
from .summary_refresh_demo_replay import infer_workspace_root


DEFAULT_CERTIFICATION_REPORT_DIR = "ION/05_context/history/demo_certification_reports"


@dataclass(frozen=True)
class SummaryRefreshDemoCertificationReport:
    certification_id: str
    emitted_at: str
    workspace_root: str
    verdict: str
    certified: bool
    failure_reasons: tuple[str, ...]
    readiness: dict[str, Any]
    doctor: dict[str, Any]
    boundaries: dict[str, bool]


def certify_summary_refresh_demo(
    *,
    workspace_root: str | Path | None = None,
    created_at: str | None = None,
    raw_user_text: str = "Please certify the ION summary-refresh release demo.",
    session_id_prefix: str = "summary-refresh-demo-certification",
    report_dir: str | Path = DEFAULT_CERTIFICATION_REPORT_DIR,
    run_project_smoke: bool = True,
    run_isolated_full_commit: bool = True,
    print_summary: bool = False,
) -> tuple[SummaryRefreshDemoCertificationReport, Path]:
    root = infer_workspace_root(workspace_root)
    emitted = created_at or _utc_now()
    certification_id = _stable_id("summary-refresh-demo-certification", root.as_posix(), emitted)

    doctor_report, doctor_path = run_summary_refresh_demo_doctor(
        workspace_root=root,
        created_at=emitted,
        run_project_smoke=run_project_smoke,
        run_isolated_full_commit=run_isolated_full_commit,
        raw_user_text=raw_user_text,
        session_id_prefix=session_id_prefix,
    )

    failures = _evaluate_failures(doctor_report)
    certified = not failures

    report = SummaryRefreshDemoCertificationReport(
        certification_id=certification_id,
        emitted_at=emitted,
        workspace_root=root.as_posix(),
        verdict="CERTIFIED" if certified else "BLOCKED",
        certified=certified,
        failure_reasons=tuple(failures),
        readiness=dict(doctor_report.release_readiness),
        doctor={
            "doctor_id": doctor_report.doctor_id,
            "report_path": doctor_path.as_posix(),
            "project_root_smoke_enabled": doctor_report.project_root_smoke.enabled,
            "project_root_smoke_passed": doctor_report.project_root_smoke.passed,
            "project_root_smoke_bounded_commits": doctor_report.project_root_smoke.bounded_commits,
            "isolated_full_commit_enabled": doctor_report.isolated_full_commit.enabled,
            "isolated_full_commit_passed": doctor_report.isolated_full_commit.passed,
            "isolated_bounded_commits": doctor_report.isolated_full_commit.bounded_commits,
            "isolated_committed_nodes": doctor_report.isolated_full_commit.committed_nodes,
            "isolated_committed_edges": doctor_report.isolated_full_commit.committed_edges,
            "isolated_workspace": doctor_report.isolated_full_commit.isolated_workspace,
        },
        boundaries={
            "source_summary_rewrite": False,
            "source_file_mutation": False,
            "registry_mutation": False,
            "schedule_mutation": False,
            "agent_activation": False,
            "global_graph_canon_claim": False,
            "project_root_commit_attempted": doctor_report.boundaries.get("project_root_commit_attempted", True),
            "isolated_commit_only": doctor_report.boundaries.get("isolated_commit_only", False),
        },
    )
    report_path = write_certification_report(root, report, report_dir=report_dir)
    if print_summary:
        print(format_certification_summary(report, report_path))
    return report, report_path


def write_certification_report(
    workspace_root: Path,
    report: SummaryRefreshDemoCertificationReport,
    *,
    report_dir: str | Path = DEFAULT_CERTIFICATION_REPORT_DIR,
) -> Path:
    output_dir = workspace_root / Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{report.certification_id}.summary_refresh_demo_certification_report.json"
    path.write_text(json.dumps(_to_jsonable(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_certification_summary(report: SummaryRefreshDemoCertificationReport, report_path: Path) -> str:
    doctor = report.doctor
    lines = [
        "ION summary-refresh demo certification complete.",
        f"certification_report: {report_path.as_posix()}",
        f"verdict: {report.verdict}",
        f"certified: {report.certified}",
        f"readiness: {report.readiness.get('verdict')} allowed={report.readiness.get('allowed')} failed={report.readiness.get('failed_checks')}",
        f"project_root_smoke: passed={doctor['project_root_smoke_passed']} commits={doctor['project_root_smoke_bounded_commits']}",
        f"isolated_full_commit: passed={doctor['isolated_full_commit_passed']} commits={doctor['isolated_bounded_commits']} nodes={doctor['isolated_committed_nodes']} edges={doctor['isolated_committed_edges']}",
        f"isolated_workspace: {doctor['isolated_workspace'] or '(none)'}",
    ]
    if report.failure_reasons:
        lines.append("failure_reasons: " + "; ".join(report.failure_reasons))
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Certify the ION summary-refresh release demo.")
    parser.add_argument("--workspace-root", default=".", help="Directory containing ION/; defaults to current directory.")
    parser.add_argument("--created-at", default=None)
    parser.add_argument("--text", default="Please certify the ION summary-refresh release demo.")
    parser.add_argument("--session-id-prefix", default="summary-refresh-demo-certification")
    parser.add_argument("--report-dir", default=DEFAULT_CERTIFICATION_REPORT_DIR)
    parser.add_argument("--skip-project-smoke", action="store_true")
    parser.add_argument("--skip-isolated-full-commit", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        report, report_path = certify_summary_refresh_demo(
            workspace_root=args.workspace_root,
            created_at=args.created_at,
            raw_user_text=args.text,
            session_id_prefix=args.session_id_prefix,
            report_dir=args.report_dir,
            run_project_smoke=not args.skip_project_smoke,
            run_isolated_full_commit=not args.skip_isolated_full_commit,
        )
    except Exception as exc:
        print(f"summary-refresh demo certification failed: {exc}", file=__import__("sys").stderr)
        return 1

    if args.json:
        print(json.dumps(_to_jsonable(report), indent=2, sort_keys=True))
    else:
        print(format_certification_summary(report, report_path))
    return 0 if report.certified else 2


def _evaluate_failures(doctor_report: SummaryRefreshDemoReplayDoctorReport) -> list[str]:
    failures: list[str] = []
    readiness = doctor_report.release_readiness
    if not readiness.get("allowed"):
        failures.append(f"release_readiness_not_allowed:{readiness.get('verdict')}")
    if not doctor_report.project_root_smoke.enabled:
        failures.append("project_root_smoke_not_run")
    elif not doctor_report.project_root_smoke.passed:
        failures.append(f"project_root_smoke_failed:{doctor_report.project_root_smoke.error}")
    if doctor_report.project_root_smoke.bounded_commits != 0:
        failures.append("project_root_smoke_attempted_or_recorded_bounded_commit")
    if not doctor_report.isolated_full_commit.enabled:
        failures.append("isolated_full_commit_not_run")
    elif not doctor_report.isolated_full_commit.passed:
        failures.append(f"isolated_full_commit_failed:{doctor_report.isolated_full_commit.error}")
    if doctor_report.isolated_full_commit.bounded_commits < 1:
        failures.append("isolated_full_commit_missing_bounded_commit")
    if doctor_report.isolated_full_commit.committed_nodes < 2:
        failures.append("isolated_full_commit_missing_committed_nodes")
    if doctor_report.isolated_full_commit.committed_edges < 4:
        failures.append("isolated_full_commit_missing_committed_edges")
    if doctor_report.boundaries.get("project_root_commit_attempted"):
        failures.append("project_root_commit_attempted")
    if not doctor_report.boundaries.get("isolated_commit_only"):
        failures.append("isolated_commit_only_boundary_missing")
    for key in ("registry_mutation", "schedule_mutation", "agent_activation", "global_graph_canon_claim"):
        if doctor_report.boundaries.get(key):
            failures.append(f"forbidden_boundary_true:{key}")
    return failures


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
