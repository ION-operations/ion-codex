"""ION V102 context metabolism and lifecycle audit helpers.

This module is intentionally proposal-first. It scans ION context surfaces,
classifies hot/warm/cold/quarantine candidates, and writes an audit report when
requested. It does not move, delete, compress, or rewrite evidence.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PROTOCOL_REL = Path("ION/02_architecture/ION_CONTEXT_METABOLISM_AND_LIFECYCLE_PROTOCOL.md")
POLICY_REL = Path("ION/03_registry/context_lifecycle_policy.yaml")
REPORT_REL = Path("ION/05_context/current/CONTEXT_LIFECYCLE_AUDIT_V102.json")
SIGNAL_REL = Path("ION/05_context/signals/v102_context_metabolism_receipt_20260502.txt")

HOT_PATTERNS = (
    "ION/05_context/current/ACTIVE_*.json",
    "ION/05_context/current/LAST_*.json",
    "ION/05_context/current/PRODUCTIZED_RUNTIME_MANIFEST_*.json",
    "ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_*.json",
    "ION/05_context/current/ION_RUNTIME_SEPARATION_PLAN_*.json",
    "ION/05_context/current/agent_context_systems/*.md",
)

QUARANTINE_NAME_MARKERS = (
    "_tmp_multi_root_session",
    "tmp_multi_root",
    "unpacked_previous_root",
    "foreign_root",
)

TEMPLATE_PROPOSAL_MARKERS = (
    "template_graph_writeback_proposals",
    "template_graph_writeback_proposal",
)

@dataclass(frozen=True)
class ContextLifecycleArtifact:
    rel_path: str
    bytes: int
    file_count: int
    lifecycle_class: str
    recommended_action: str
    reason: str
    carrier_default: str

@dataclass(frozen=True)
class ContextLifecycleReport:
    schema_id: str
    lifecycle_report_id: str
    emitted_at: str
    scanned_root: str
    protocol_path: str
    policy_path: str
    total_context_bytes: int
    hot_bytes: int
    warm_bytes: int
    cold_bytes: int
    quarantine_candidate_bytes: int
    template_proposal_bytes: int
    execution_cycle_bytes: int
    artifact_count: int
    file_count: int
    mutation_performed: bool
    verdict: str
    findings: tuple[str, ...]
    artifacts: tuple[ContextLifecycleArtifact, ...] = field(default_factory=tuple)


def _shell_root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _directory_size(path: Path) -> tuple[int, int]:
    if not path.exists():
        return 0, 0
    if path.is_file():
        return path.stat().st_size, 1
    total = 0
    count = 0
    for item in path.rglob("*"):
        if item.is_file():
            try:
                total += item.stat().st_size
                count += 1
            except OSError:
                continue
    return total, count


def _match_any(rel_path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatch(rel_path, pattern) for pattern in patterns)


def classify_context_artifact(path: Path, root: Path) -> ContextLifecycleArtifact:
    rel_path = _rel(path, root)
    size, files = _directory_size(path)
    lowered = rel_path.lower()
    name = path.name.lower()

    if any(marker in lowered or marker in name for marker in QUARANTINE_NAME_MARKERS):
        return ContextLifecycleArtifact(
            rel_path=rel_path,
            bytes=size,
            file_count=files,
            lifecycle_class="QUARANTINE_CANDIDATE",
            recommended_action="QUARANTINE_AFTER_RECONCILIATION",
            reason="temporary or foreign-root reconciliation material must not live in hot current state",
            carrier_default="EXCLUDE_UNLESS_FORENSIC_SCOPE",
        )

    if any(marker in lowered for marker in TEMPLATE_PROPOSAL_MARKERS):
        return ContextLifecycleArtifact(
            rel_path=rel_path,
            bytes=size,
            file_count=files,
            lifecycle_class="WARM_OR_COLD_TEMPLATE_PROPOSAL_EVIDENCE",
            recommended_action="REVIEW_COMPRESS_TO_DIFF",
            reason="template graph writeback proposals are proposal-only evidence and should not repeatedly materialize full graph snapshots in hot carrier state",
            carrier_default="EXCLUDE_UNLESS_ACTIVE_REVIEW_SCOPE",
        )

    if rel_path.startswith("ION/05_context/current/execution_cycles"):
        return ContextLifecycleArtifact(
            rel_path=rel_path,
            bytes=size,
            file_count=files,
            lifecycle_class="WARM_EXECUTION_EVIDENCE",
            recommended_action="DIGEST_TO_RESIDUE_THEN_ARCHIVE_COLD",
            reason="execution cycles are valid proof-of-work but should metabolize into compact residues for routine carrier packages",
            carrier_default="EXCLUDE_AFTER_RESIDUE_EXISTS",
        )

    if _match_any(rel_path, HOT_PATTERNS) or rel_path == "ION/05_context/current" or rel_path.startswith("ION/05_context/current/agent_context_systems"):
        return ContextLifecycleArtifact(
            rel_path=rel_path,
            bytes=size,
            file_count=files,
            lifecycle_class="HOT_RUNTIME_STATE",
            recommended_action="KEEP_HOT",
            reason="active runtime or role-context state needed for lawful next-run resumption",
            carrier_default="INCLUDE",
        )

    if rel_path.startswith("ION/05_context/history") or rel_path.startswith("ION/05_context/archive"):
        return ContextLifecycleArtifact(
            rel_path=rel_path,
            bytes=size,
            file_count=files,
            lifecycle_class="COLD_HISTORY",
            recommended_action="KEEP_OUT_OF_HOT_CARRIER_PACKAGE",
            reason="history/archive material is valuable proof but not default current truth",
            carrier_default="EXCLUDE_UNLESS_FORENSIC_SCOPE",
        )

    if rel_path.startswith("ION/05_context/current"):
        return ContextLifecycleArtifact(
            rel_path=rel_path,
            bytes=size,
            file_count=files,
            lifecycle_class="CURRENT_CONTEXT_UNCLASSIFIED",
            recommended_action="CLASSIFY_OR_DIGEST_TO_RESIDUE",
            reason="current context artifact needs an explicit lifecycle class before growth is trusted",
            carrier_default="REVIEW",
        )

    return ContextLifecycleArtifact(
        rel_path=rel_path,
        bytes=size,
        file_count=files,
        lifecycle_class="OUT_OF_SCOPE",
        recommended_action="NO_CONTEXT_LIFECYCLE_ACTION",
        reason="not under ION/05_context lifecycle scope",
        carrier_default="UNCHANGED",
    )


def _scan_targets(root: Path) -> list[Path]:
    targets: list[Path] = []
    current = root / "ION/05_context/current"
    if current.exists():
        # Do not classify the current directory itself as a recursively hot
        # artifact; that double-counts warm execution evidence and hides the
        # hot/warm/cold boundary. Classify its immediate children instead.
        for item in sorted(current.iterdir(), key=lambda p: p.as_posix()):
            targets.append(item)
    for rel in (
        "ION/05_context/history/template_graph_writeback_proposals",
        "ION/05_context/history/template_graph_writeback_reviews",
        "ION/05_context/archive",
    ):
        path = root / rel
        if path.exists():
            targets.append(path)
    # Deduplicate while preserving order.
    seen: set[str] = set()
    out: list[Path] = []
    for target in targets:
        key = target.resolve().as_posix()
        if key not in seen:
            seen.add(key)
            out.append(target)
    return out


def build_context_lifecycle_report(root: str | Path, *, emitted_at: str | None = None) -> ContextLifecycleReport:
    shell = _shell_root(root)
    timestamp = emitted_at or _now()
    artifacts = tuple(classify_context_artifact(path, shell) for path in _scan_targets(shell))

    total_context_bytes, total_context_files = _directory_size(shell / "ION/05_context")
    hot = sum(item.bytes for item in artifacts if item.lifecycle_class == "HOT_RUNTIME_STATE")
    warm = sum(item.bytes for item in artifacts if item.lifecycle_class.startswith("WARM"))
    cold = sum(item.bytes for item in artifacts if item.lifecycle_class == "COLD_HISTORY")
    quarantine = sum(item.bytes for item in artifacts if item.lifecycle_class == "QUARANTINE_CANDIDATE")
    template_proposals = sum(item.bytes for item in artifacts if "TEMPLATE_PROPOSAL" in item.lifecycle_class)
    execution_cycles = sum(item.bytes for item in artifacts if item.rel_path.startswith("ION/05_context/current/execution_cycles"))

    findings: list[str] = []
    if quarantine:
        findings.append("quarantine_candidate_material_present_in_context_scope")
    if execution_cycles > 50 * 1024 * 1024:
        findings.append("execution_cycle_evidence_exceeds_hot_carrier_soft_limit")
    if template_proposals > 25 * 1024 * 1024:
        findings.append("template_graph_proposals_exceed_diff_review_soft_limit")
    if total_context_bytes > 100 * 1024 * 1024:
        findings.append("context_tree_requires_hot_warm_cold_packaging_split")
    if not findings:
        findings.append("context_lifecycle_within_current_branch_soft_limits")

    verdict = "PASS_WITH_LIFECYCLE_MODEL" if findings == ["context_lifecycle_within_current_branch_soft_limits"] else "REVIEW_REQUIRED"
    report_id = _stable_id("context-lifecycle-report", shell.as_posix(), timestamp, str(total_context_bytes), *findings)
    return ContextLifecycleReport(
        schema_id="ion.context_lifecycle_report.v1",
        lifecycle_report_id=report_id,
        emitted_at=timestamp,
        scanned_root=shell.as_posix(),
        protocol_path=PROTOCOL_REL.as_posix(),
        policy_path=POLICY_REL.as_posix(),
        total_context_bytes=total_context_bytes,
        hot_bytes=hot,
        warm_bytes=warm,
        cold_bytes=cold,
        quarantine_candidate_bytes=quarantine,
        template_proposal_bytes=template_proposals,
        execution_cycle_bytes=execution_cycles,
        artifact_count=len(artifacts),
        file_count=total_context_files,
        mutation_performed=False,
        verdict=verdict,
        findings=tuple(findings),
        artifacts=artifacts,
    )


def _jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: _jsonable(val) for key, val in asdict(value).items()}
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    return value


def context_lifecycle_report_to_dict(report: ContextLifecycleReport) -> dict[str, Any]:
    """Return a stable JSON-compatible lifecycle report mapping.

    This public helper exists so other kernel surfaces can bind to the V102
    lifecycle audit without reaching into private serialization internals.
    """
    value = _jsonable(report)
    assert isinstance(value, dict)
    return value


def write_context_lifecycle_report(root: str | Path, report: ContextLifecycleReport | None = None) -> Path:
    shell = _shell_root(root)
    report = report or build_context_lifecycle_report(shell)
    path = shell / REPORT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    signal = shell / SIGNAL_REL
    signal.parent.mkdir(parents=True, exist_ok=True)
    signal.write_text(
        "V102 context metabolism receipt\n"
        f"report_id: {report.lifecycle_report_id}\n"
        f"verdict: {report.verdict}\n"
        f"total_context_bytes: {report.total_context_bytes}\n"
        f"execution_cycle_bytes: {report.execution_cycle_bytes}\n"
        f"template_proposal_bytes: {report.template_proposal_bytes}\n"
        "mutation_performed: false\n",
        encoding="utf-8",
    )
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ION context lifecycle hot/warm/cold posture.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = build_context_lifecycle_report(args.ion_root)
    if args.write_report:
        write_context_lifecycle_report(args.ion_root, report)
    if args.json:
        print(json.dumps(_jsonable(report), indent=2, sort_keys=True))
    else:
        print(f"ION_CONTEXT_LIFECYCLE_{report.verdict}")
        for finding in report.findings:
            print(f"- {finding}")
    return 0 if report.verdict in {"PASS_WITH_LIFECYCLE_MODEL", "REVIEW_REQUIRED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
