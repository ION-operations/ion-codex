"""Single-command replay surface for the full summary-refresh demo.

Run with:

    PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_replay --workspace-root .

The command writes a JSON replay report and prints a concise artifact summary.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from .summary_refresh_demo import SummaryRefreshDemoRunner
from .template_contract_registry import load_template_contract_registry_projection


DEFAULT_REPORT_DIR = "ION/05_context/history/demo_replay_reports"


@dataclass(frozen=True)
class SummaryRefreshDemoReplayReport:
    report_id: str
    emitted_at: str
    workspace_root: str
    session_id: str
    user_ref: str
    summary_target: str
    review_verdict: str
    run_bounded_commit: bool
    demo_id: str
    persona_response_text: str
    artifact_paths: dict[str, Any]
    counts: dict[str, int]
    boundaries: dict[str, bool]


def infer_workspace_root(path: str | Path | None = None) -> Path:
    """Infer project workspace root.

    The workspace root is the directory containing the ``ION`` directory. If
    called from inside the ION directory, return its parent.
    """

    base = Path(path or ".").resolve()
    if (base / "ION").is_dir():
        return base
    if base.name == "ION" and (base / "04_packages").is_dir():
        return base.parent
    # Walk upward to make the command convenient from subdirectories.
    for candidate in (base, *base.parents):
        if (candidate / "ION").is_dir():
            return candidate
        if candidate.name == "ION" and (candidate / "04_packages").is_dir():
            return candidate.parent
    return base


def run_summary_refresh_demo_replay(
    *,
    workspace_root: str | Path | None = None,
    raw_user_text: str = "Please refresh the current ION project summary.",
    session_id: str = "summary-refresh-demo-replay",
    user_ref: str = "user.sovereign",
    summary_target: str = "ION current project",
    visible_persona_name: str | None = None,
    review_verdict: str = "LAND",
    reviewer: str = "Steward",
    review_reason: str | None = None,
    run_bounded_commit: bool = True,
    created_at: str | None = None,
    report_dir: str | Path = DEFAULT_REPORT_DIR,
    print_summary: bool = False,
    dispatch: bool = True,
) -> tuple[SummaryRefreshDemoReplayReport, Path]:
    root = infer_workspace_root(workspace_root)
    emitted = created_at or _utc_now()
    contracts = load_template_contract_registry_projection(root, strict=True)
    result = SummaryRefreshDemoRunner().run(
        workspace_root=root,
        raw_user_text=raw_user_text,
        session_id=session_id,
        user_ref=user_ref,
        summary_target=summary_target,
        visible_persona_name=visible_persona_name,
        created_at=emitted,
        template_contracts=contracts,
        review_verdict=review_verdict,
        reviewer=reviewer,
        review_reason=review_reason
        or "Demo replay review verdict supplied by summary-refresh replay command.",
        run_bounded_commit=run_bounded_commit,
        dispatch=dispatch,
    )

    artifact_paths = {
        "request_path": result.request_path,
        "front_door_ingress_witness_paths": list(result.front_door_turn.ingress.receipt.witness_paths),
        "front_door_return_witness_paths": list(result.return_result.return_result.receipt.witness_paths),
        "completion_witness_paths": list(result.completion_receipt.witness_paths),
        "reaction_selection_witness_paths": list(result.reaction_receipt.selection_witness_paths),
        "projection_path": result.projection_receipt.projection_path,
        "proposal_path": result.proposal_receipt.proposal_path,
        "review_paths": list(result.review_receipt.review_paths),
        "commit_paths": list(result.commit_receipt.commit_paths) if result.commit_receipt is not None else [],
        "demo_receipt_path": (
            f"ION/05_context/history/summary_refresh_demo_receipts/"
            f"{result.demo_id}.summary_refresh_demo_receipt.json"
        ),
    }
    counts = {
        "completion_events": result.completion_receipt.completed_count,
        "selected_reactions": result.reaction_receipt.selected_reaction_count,
        "refused_reactions": result.reaction_receipt.refused_reaction_count,
        "projection_entries": result.projection_receipt.projected_entry_count,
        "projection_deferred_reactions": result.projection_receipt.deferred_reaction_count,
        "proposed_nodes": result.proposal_receipt.proposed_node_count,
        "proposed_edges": result.proposal_receipt.proposed_edge_count,
        "reviewed_proposals": result.review_receipt.reviewed_proposal_count,
        "land_reviews": result.review_receipt.land_count,
        "hold_reviews": result.review_receipt.hold_count,
        "escalate_reviews": result.review_receipt.escalate_count,
        "bounded_commits": result.commit_receipt.committed_review_count if result.commit_receipt is not None else 0,
        "committed_nodes": result.commit_receipt.committed_node_count if result.commit_receipt is not None else 0,
        "committed_edges": result.commit_receipt.committed_edge_count if result.commit_receipt is not None else 0,
    }
    report_id = _stable_id("summary-refresh-demo-replay", result.demo_id, emitted, review_verdict)
    report = SummaryRefreshDemoReplayReport(
        report_id=report_id,
        emitted_at=emitted,
        workspace_root=root.as_posix(),
        session_id=session_id,
        user_ref=user_ref,
        summary_target=summary_target,
        review_verdict=review_verdict,
        run_bounded_commit=run_bounded_commit,
        demo_id=result.demo_id,
        persona_response_text=result.return_result.return_result.persona_response.user_facing_text,
        artifact_paths=artifact_paths,
        counts=counts,
        boundaries={
            "source_summary_rewrite": False,
            "source_file_mutation": False,
            "registry_mutation": False,
            "schedule_mutation": False,
            "agent_activation": False,
            "global_graph_canon_claim": False,
            "bounded_event_graph_commit_only": result.commit_receipt is not None,
        },
    )
    report_path = write_replay_report(root, report, report_dir=report_dir)
    if print_summary:
        print(format_replay_summary(report, report_path))
    return report, report_path


def write_replay_report(
    workspace_root: Path,
    report: SummaryRefreshDemoReplayReport,
    *,
    report_dir: str | Path = DEFAULT_REPORT_DIR,
) -> Path:
    output_dir = workspace_root / Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{report.report_id}.summary_refresh_demo_replay_report.json"
    path.write_text(json.dumps(_to_jsonable(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_replay_summary(report: SummaryRefreshDemoReplayReport, report_path: Path) -> str:
    paths = report.artifact_paths
    counts = report.counts
    lines = [
        "ION summary-refresh demo replay complete.",
        f"report: {report_path.as_posix()}",
        f"demo_id: {report.demo_id}",
        f"review_verdict: {report.review_verdict}",
        f"bounded_commits: {counts['bounded_commits']}",
        f"request: {paths['request_path']}",
        f"completion_witnesses: {', '.join(paths['completion_witness_paths'])}",
        f"reaction_witnesses: {', '.join(paths['reaction_selection_witness_paths'])}",
        f"projection: {paths['projection_path']}",
        f"proposal: {paths['proposal_path']}",
        f"reviews: {', '.join(paths['review_paths'])}",
        f"commits: {', '.join(paths['commit_paths']) if paths['commit_paths'] else '(none)'}",
        f"demo_receipt: {paths['demo_receipt_path']}",
    ]
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Replay the full ION summary-refresh demo.")
    parser.add_argument("--workspace-root", default=".", help="Directory containing ION/; defaults to current directory.")
    parser.add_argument("--text", default="Please refresh the current ION project summary.", help="User text to feed through Persona Interface.")
    parser.add_argument("--session-id", default="summary-refresh-demo-replay")
    parser.add_argument("--user-ref", default="user.sovereign")
    parser.add_argument("--summary-target", default="ION current project")
    parser.add_argument("--visible-persona-name", default=None)
    parser.add_argument("--review-verdict", choices=("LAND", "HOLD", "ESCALATE"), default="LAND")
    parser.add_argument("--reviewer", default="Steward")
    parser.add_argument("--review-reason", default=None)
    parser.add_argument("--created-at", default=None)
    parser.add_argument("--report-dir", default=DEFAULT_REPORT_DIR)
    parser.add_argument("--no-commit", action="store_true", help="Do not run Phase 6 bounded commit even if review verdict is LAND.")
    parser.add_argument("--no-dispatch", action="store_true", help="Do not dispatch the front-door queue item; useful for repeatable project-root smokes.")
    parser.add_argument("--json", action="store_true", help="Print the full replay report JSON instead of text summary.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    try:
        report, report_path = run_summary_refresh_demo_replay(
            workspace_root=args.workspace_root,
            raw_user_text=args.text,
            session_id=args.session_id,
            user_ref=args.user_ref,
            summary_target=args.summary_target,
            visible_persona_name=args.visible_persona_name,
            review_verdict=args.review_verdict,
            reviewer=args.reviewer,
            review_reason=args.review_reason,
            run_bounded_commit=not args.no_commit,
            created_at=args.created_at,
            report_dir=args.report_dir,
            print_summary=False,
            dispatch=not args.no_dispatch,
        )
    except Exception as exc:
        print(f"summary-refresh demo replay failed: {exc}", file=__import__("sys").stderr)
        return 1

    if args.json:
        print(json.dumps(_to_jsonable(report), indent=2, sort_keys=True))
    else:
        print(format_replay_summary(report, report_path))
    return 0


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
