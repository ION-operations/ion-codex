"""Evidence bundle assembly for the certified summary-refresh demo."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any

from .summary_refresh_demo_certification import certify_summary_refresh_demo
from .summary_refresh_demo_replay import infer_workspace_root

DEFAULT_EVIDENCE_BUNDLE_DIR = "ION/05_context/history/demo_evidence_bundles"

@dataclass(frozen=True)
class SummaryRefreshDemoEvidenceBundle:
    bundle_id: str
    emitted_at: str
    workspace_root: str
    bundle_dir: str
    certified: bool
    certification_verdict: str
    failure_reasons: tuple[str, ...]
    certification_report_path: str
    doctor_report_path: str
    project_root_smoke_report_path: str
    isolated_full_commit_report_path: str
    copied_reports: dict[str, str]
    commands: dict[str, str]
    readiness: dict[str, Any]
    certification: dict[str, Any]
    boundaries: dict[str, bool]

class SummaryRefreshDemoEvidenceBundleError(Exception):
    """Raised when evidence bundle generation is blocked."""

def create_summary_refresh_demo_evidence_bundle(*, workspace_root: str | Path | None = None, created_at: str | None = None, raw_user_text: str = "Please certify and bundle the ION summary-refresh release demo evidence.", session_id_prefix: str = "summary-refresh-demo-evidence-bundle", bundle_root: str | Path = DEFAULT_EVIDENCE_BUNDLE_DIR, allow_blocked: bool = False, run_project_smoke: bool = True, run_isolated_full_commit: bool = True, print_summary: bool = False) -> tuple[SummaryRefreshDemoEvidenceBundle, Path]:
    root = infer_workspace_root(workspace_root)
    emitted = created_at or _utc_now()
    certification_report, certification_path = certify_summary_refresh_demo(workspace_root=root, created_at=emitted, raw_user_text=raw_user_text, session_id_prefix=session_id_prefix, run_project_smoke=run_project_smoke, run_isolated_full_commit=run_isolated_full_commit)
    if not certification_report.certified and not allow_blocked:
        raise SummaryRefreshDemoEvidenceBundleError("certification_not_certified:" + ",".join(certification_report.failure_reasons))
    bundle_id = _stable_id("summary-refresh-demo-evidence-bundle", root.as_posix(), emitted)
    bundle_dir = root / Path(bundle_root) / bundle_id
    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    (bundle_dir / "reports").mkdir(parents=True, exist_ok=True)
    doctor_report_path = Path(certification_report.doctor.get("report_path", ""))
    doctor_report = _read_json_if_exists(doctor_report_path)
    project_report_path = Path(doctor_report.get("project_root_smoke", {}).get("report_path", ""))
    isolated_report_path = Path(doctor_report.get("isolated_full_commit", {}).get("report_path", ""))
    copied = {
        "certification_report": _copy_report(certification_path, bundle_dir / "reports"),
        "doctor_report": _copy_report(doctor_report_path, bundle_dir / "reports"),
        "project_root_smoke_report": _copy_report(project_report_path, bundle_dir / "reports"),
        "isolated_full_commit_report": _copy_report(isolated_report_path, bundle_dir / "reports"),
    }
    commands = {
        "certify": "PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_certification --workspace-root .",
        "doctor": "PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_doctor --workspace-root .",
        "replay_no_commit": "PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_replay --workspace-root . --no-commit --no-dispatch",
        "replay_full_land_in_fresh_workspace": "PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_replay --workspace-root <fresh-workspace>",
    }
    bundle = SummaryRefreshDemoEvidenceBundle(
        bundle_id=bundle_id,
        emitted_at=emitted,
        workspace_root=root.as_posix(),
        bundle_dir=bundle_dir.relative_to(root).as_posix(),
        certified=bool(certification_report.certified),
        certification_verdict=str(certification_report.verdict),
        failure_reasons=tuple(certification_report.failure_reasons),
        certification_report_path=_rel(root, certification_path),
        doctor_report_path=_rel(root, doctor_report_path),
        project_root_smoke_report_path=_rel(root, project_report_path),
        isolated_full_commit_report_path=_rel(root, isolated_report_path),
        copied_reports=copied,
        commands=commands,
        readiness=dict(certification_report.readiness),
        certification={
            "certification_id": certification_report.certification_id,
            "doctor_id": certification_report.doctor.get("doctor_id", ""),
            "project_root_smoke_passed": certification_report.doctor.get("project_root_smoke_passed", False),
            "project_root_smoke_bounded_commits": certification_report.doctor.get("project_root_smoke_bounded_commits", -1),
            "isolated_full_commit_passed": certification_report.doctor.get("isolated_full_commit_passed", False),
            "isolated_bounded_commits": certification_report.doctor.get("isolated_bounded_commits", 0),
            "isolated_committed_nodes": certification_report.doctor.get("isolated_committed_nodes", 0),
            "isolated_committed_edges": certification_report.doctor.get("isolated_committed_edges", 0),
            "isolated_workspace": certification_report.doctor.get("isolated_workspace", ""),
        },
        boundaries={"source_summary_rewrite": False, "source_file_mutation": False, "registry_mutation": False, "schedule_mutation": False, "agent_activation": False, "global_graph_canon_claim": False, "constitutional_ratification_claim": False, "evidence_copy_only": True},
    )
    manifest_path = write_evidence_bundle_manifest(bundle_dir, bundle)
    write_evidence_bundle_readme(bundle_dir, bundle, manifest_path)
    if print_summary:
        print(format_evidence_bundle_summary(bundle, manifest_path))
    return bundle, manifest_path

def write_evidence_bundle_manifest(bundle_dir: Path, bundle: SummaryRefreshDemoEvidenceBundle) -> Path:
    path = bundle_dir / "summary_refresh_demo_evidence_bundle_manifest.json"
    path.write_text(json.dumps(_to_jsonable(bundle), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def write_evidence_bundle_readme(bundle_dir: Path, bundle: SummaryRefreshDemoEvidenceBundle, manifest_path: Path) -> Path:
    path = bundle_dir / "README.md"
    lines = ["# Summary Refresh Demo Evidence Bundle", "", f"**Bundle ID:** `{bundle.bundle_id}`", f"**Verdict:** `{bundle.certification_verdict}`", f"**Certified:** `{bundle.certified}`", f"**Manifest:** `{manifest_path.name}`", "", "## Core command", "", "```bash", bundle.commands["certify"], "```", "", "## Evidence counts", "", f"- Project-root smoke passed: `{bundle.certification['project_root_smoke_passed']}`", f"- Project-root smoke bounded commits: `{bundle.certification['project_root_smoke_bounded_commits']}`", f"- Isolated full commit passed: `{bundle.certification['isolated_full_commit_passed']}`", f"- Isolated bounded commits: `{bundle.certification['isolated_bounded_commits']}`", f"- Isolated committed nodes: `{bundle.certification['isolated_committed_nodes']}`", f"- Isolated committed edges: `{bundle.certification['isolated_committed_edges']}`", "", "## Boundary", "", "This bundle is evidence-only. It does not claim full product completion, global graph canon, source-summary rewrite authority, agent activation authority, or constitutional ratification.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path

def format_evidence_bundle_summary(bundle: SummaryRefreshDemoEvidenceBundle, manifest_path: Path) -> str:
    return "\n".join(["ION summary-refresh demo evidence bundle complete.", f"bundle_id: {bundle.bundle_id}", f"manifest: {manifest_path.as_posix()}", f"certified: {bundle.certified}", f"verdict: {bundle.certification_verdict}", f"bundle_dir: {bundle.bundle_dir}", f"certification_report: {bundle.certification_report_path}", f"doctor_report: {bundle.doctor_report_path}", f"isolated_bounded_commits: {bundle.certification['isolated_bounded_commits']}", f"isolated_committed_nodes: {bundle.certification['isolated_committed_nodes']}", f"isolated_committed_edges: {bundle.certification['isolated_committed_edges']}"])

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create an evidence bundle for the certified ION summary-refresh demo.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--created-at", default=None)
    parser.add_argument("--text", default="Please certify and bundle the ION summary-refresh release demo evidence.")
    parser.add_argument("--session-id-prefix", default="summary-refresh-demo-evidence-bundle")
    parser.add_argument("--bundle-root", default=DEFAULT_EVIDENCE_BUNDLE_DIR)
    parser.add_argument("--allow-blocked", action="store_true")
    parser.add_argument("--skip-project-smoke", action="store_true")
    parser.add_argument("--skip-isolated-full-commit", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser(); args = parser.parse_args(argv)
    try:
        bundle, manifest_path = create_summary_refresh_demo_evidence_bundle(workspace_root=args.workspace_root, created_at=args.created_at, raw_user_text=args.text, session_id_prefix=args.session_id_prefix, bundle_root=args.bundle_root, allow_blocked=args.allow_blocked, run_project_smoke=not args.skip_project_smoke, run_isolated_full_commit=not args.skip_isolated_full_commit)
    except Exception as exc:
        print(f"summary-refresh demo evidence bundle failed: {exc}", file=__import__("sys").stderr); return 1
    if args.json: print(json.dumps(_to_jsonable(bundle), indent=2, sort_keys=True))
    else: print(format_evidence_bundle_summary(bundle, manifest_path))
    return 0 if bundle.certified else 2

def _copy_report(path: Path, output_dir: Path) -> str:
    if not path or not path.as_posix() or path.as_posix() == ".": return ""
    if not path.exists() or not path.is_file(): return ""
    output = output_dir / path.name
    shutil.copy2(path, output)
    return output.relative_to(output_dir.parent).as_posix()

def _read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path or not path.as_posix() or path.as_posix() == ".": return {}
    if not path.exists() or not path.is_file(): return {}
    return json.loads(path.read_text(encoding="utf-8"))

def _rel(root: Path, path: Path) -> str:
    if not path or not path.as_posix() or path.as_posix() == ".": return ""
    try: return path.relative_to(root).as_posix()
    except ValueError: return path.as_posix()

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\n".join(part for part in parts if part).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"

def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"): return {k: _to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple): return [_to_jsonable(v) for v in value]
    if isinstance(value, list): return [_to_jsonable(v) for v in value]
    if isinstance(value, dict): return {str(k): _to_jsonable(v) for k, v in value.items()}
    return value

if __name__ == "__main__": raise SystemExit(main())
