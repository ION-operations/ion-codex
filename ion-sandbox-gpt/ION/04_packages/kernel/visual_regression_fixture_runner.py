"""V49 visual regression fixture runner plan.

This module intentionally does not execute browsers. It records local/dev fixture
plans and pre-captured visual verification outcomes so repeatable visual checks
can be discussed, reviewed, and receipted before any stronger visual automation
authority is considered.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_ID = "ion.visual_regression_fixture_runner.v1"
VERSION = "V49_VISUAL_REGRESSION_FIXTURE_RUNNER_PLAN"
DEFAULT_REPORT_DIR = "ION/05_context/history/visual_regression_fixture_runs"
AUTHORITY_SCOPE = "LOCAL_DEV_VISUAL_FIXTURE_PLAN_AND_REPORT_ONLY"

ALLOWED_FIXTURE_MODES = (
    "STATIC_ARTIFACT_REFERENCE_CHECK",
    "PRECAPTURED_BEFORE_AFTER_VERIFICATION",
    "HARNESS_PLAN_ONLY",
    "STEWARD_REVIEW_REQUIRED",
)

STEWARD_GATE_STATUSES = ("APPROVED_PLAN_ONLY", "STEWARD_REVIEW_REQUIRED", "BLOCKED")

PASSING_VERDICTS = (
    "VISUAL_REPAIR_VERIFIED",
    "VISUAL_REGRESSION_BASELINE_MATCHED",
    "NO_VISUAL_REGRESSION_DETECTED",
)

REVIEW_VERDICTS = (
    "VISUAL_REPAIR_PARTIAL_NEEDS_FOLLOWUP",
    "VISUAL_CHANGE_EVIDENCE_RECORDED_REQUIRES_REVIEW",
    "VISUAL_VERIFICATION_NO_ACTIONABLE_CHANGE_RECORDED",
    "VISUAL_VERIFICATION_NEEDS_AFTER_EVIDENCE",
    "NOT_EXECUTED_PLAN_ONLY",
)

FAILING_VERDICTS = (
    "VISUAL_REGRESSION_OR_NEW_ISSUE_REQUIRES_REVIEW",
    "VISUAL_REGRESSION_DETECTED",
    "VISUAL_FIXTURE_FAILED",
)

FORBIDDEN_CAPABILITIES = {
    "unrestricted_browser_control": False,
    "browser_execution": False,
    "network_side_effects": False,
    "credential_sensitive_action": False,
    "account_operation": False,
    "destructive_action": False,
    "form_submission": False,
    "purchase_or_submission": False,
    "persistent_dom_mutation": False,
    "production_visual_automation": False,
    "production_authority": False,
}

@dataclass(frozen=True)
class VisualRegressionFixture:
    fixture_id: str
    target: str
    mode: str = "HARNESS_PLAN_ONLY"
    expected_verdict: str = "VISUAL_REPAIR_VERIFIED"
    actual_verdict: str | None = None
    before_refs: tuple[str, ...] = ()
    after_refs: tuple[str, ...] = ()
    before_after_verification_receipt_ids: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    steward_review_required: bool = False
    implementation_hint: str | None = None

@dataclass(frozen=True)
class VisualRegressionFixtureResult:
    fixture_id: str
    target: str
    result: str
    expected_verdict: str
    actual_verdict: str
    review_required: bool
    notes: tuple[str, ...]

@dataclass(frozen=True)
class VisualRegressionFixtureRunReceipt:
    schema_id: str
    version: str
    run_id: str
    emitted_at: str
    suite_id: str
    suite_target: str
    steward_gate_status: str
    fixture_count: int
    passed_count: int
    failed_count: int
    review_count: int
    blocked_count: int
    fixture_results: tuple[VisualRegressionFixtureResult, ...]
    suite_verdict: str
    recommended_next_actions: tuple[str, ...]
    authority_scope: str = AUTHORITY_SCOPE
    production_authority: bool = False
    forbidden_capabilities: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CAPABILITIES))


def build_visual_regression_fixture_run_receipt(
    *,
    suite_id: str,
    suite_target: str,
    fixtures: Iterable[VisualRegressionFixture],
    steward_gate_status: str = "APPROVED_PLAN_ONLY",
    emitted_at: str | None = None,
) -> VisualRegressionFixtureRunReceipt:
    if steward_gate_status not in STEWARD_GATE_STATUSES:
        raise ValueError(f"invalid steward_gate_status: {steward_gate_status}")
    fixture_tuple = tuple(fixtures)
    for fixture in fixture_tuple:
        if fixture.mode not in ALLOWED_FIXTURE_MODES:
            raise ValueError(f"invalid fixture mode for {fixture.fixture_id}: {fixture.mode}")
    results = tuple(_classify_fixture(fixture, steward_gate_status) for fixture in fixture_tuple)
    passed = sum(1 for r in results if r.result == "PASS")
    failed = sum(1 for r in results if r.result == "FAIL_REQUIRES_REVIEW")
    review = sum(1 for r in results if r.review_required and r.result != "BLOCKED")
    blocked = sum(1 for r in results if r.result == "BLOCKED")
    suite_verdict = _suite_verdict(steward_gate_status, passed, failed, review, blocked, len(results))
    ts = emitted_at or _utc_now()
    run_id = _stable_id("v49-visual-fixture-run", VERSION, ts, suite_id, suite_verdict, str(len(results)))
    return VisualRegressionFixtureRunReceipt(
        SCHEMA_ID,
        VERSION,
        run_id,
        ts,
        suite_id,
        suite_target,
        steward_gate_status,
        len(results),
        passed,
        failed,
        review,
        blocked,
        results,
        suite_verdict,
        _actions(suite_verdict),
    )


def load_visual_regression_fixture_manifest(workspace_root: str | Path, manifest_path: str | Path) -> tuple[str, str, tuple[VisualRegressionFixture, ...]]:
    root = Path(workspace_root).resolve()
    manifest = _inside(root, manifest_path)
    data = json.loads(manifest.read_text(encoding="utf-8"))
    suite_id = str(data.get("suite_id") or "visual-regression-suite")
    suite_target = str(data.get("suite_target") or data.get("target") or "unspecified visual target")
    fixtures = tuple(_fixture_from_mapping(item) for item in data.get("fixtures", ()))
    return suite_id, suite_target, fixtures


def validate_visual_regression_fixture_run_receipt(receipt: VisualRegressionFixtureRunReceipt) -> tuple[str, ...]:
    errors: list[str] = []
    if receipt.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if receipt.version != VERSION:
        errors.append("version mismatch")
    if receipt.authority_scope != AUTHORITY_SCOPE:
        errors.append("authority scope mismatch")
    if receipt.production_authority is not False:
        errors.append("production authority must be false")
    if any(value is not False for value in receipt.forbidden_capabilities.values()):
        errors.append("forbidden capabilities must all be false")
    if receipt.fixture_count != len(receipt.fixture_results):
        errors.append("fixture_count does not match fixture_results length")
    if receipt.suite_verdict == "VISUAL_REGRESSION_FIXTURE_SUITE_PASSED" and (receipt.failed_count or receipt.review_count or receipt.blocked_count):
        errors.append("passed suite cannot have failed/review/blocked counts")
    if receipt.blocked_count and receipt.suite_verdict != "VISUAL_REGRESSION_FIXTURE_SUITE_BLOCKED_BY_STEWARD":
        errors.append("blocked fixtures require blocked suite verdict")
    return tuple(errors)


def write_visual_regression_fixture_run_receipt(workspace_root: str | Path, receipt: VisualRegressionFixtureRunReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt.run_id}.visual_regression_fixture_run_receipt.json"
    path.write_text(json.dumps(_json(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _classify_fixture(fixture: VisualRegressionFixture, steward_gate_status: str) -> VisualRegressionFixtureResult:
    if steward_gate_status == "BLOCKED":
        return VisualRegressionFixtureResult(fixture.fixture_id, fixture.target, "BLOCKED", fixture.expected_verdict, fixture.actual_verdict or "BLOCKED_BY_STEWARD", True, ("suite blocked by Steward/VZ gate",))
    if fixture.mode == "HARNESS_PLAN_ONLY":
        return VisualRegressionFixtureResult(fixture.fixture_id, fixture.target, "PLANNED_NOT_EXECUTED", fixture.expected_verdict, fixture.actual_verdict or "NOT_EXECUTED_PLAN_ONLY", True, ("fixture is planned but has no executable runner authority in V49",))
    actual = fixture.actual_verdict or "NOT_EXECUTED_PLAN_ONLY"
    notes: list[str] = []
    review_required = bool(fixture.steward_review_required or steward_gate_status == "STEWARD_REVIEW_REQUIRED")
    if actual in FAILING_VERDICTS or actual != fixture.expected_verdict:
        review_required = True
        notes.append("actual verdict does not match expected verdict")
        if actual in FAILING_VERDICTS:
            notes.append("actual verdict indicates regression or fixture failure")
        return VisualRegressionFixtureResult(fixture.fixture_id, fixture.target, "FAIL_REQUIRES_REVIEW", fixture.expected_verdict, actual, review_required, tuple(notes))
    if actual in PASSING_VERDICTS:
        if review_required:
            notes.append("passing fixture still requires Steward/VZ review")
            return VisualRegressionFixtureResult(fixture.fixture_id, fixture.target, "PASS_NEEDS_REVIEW", fixture.expected_verdict, actual, True, tuple(notes))
        return VisualRegressionFixtureResult(fixture.fixture_id, fixture.target, "PASS", fixture.expected_verdict, actual, False, ("actual verdict matched expected passing verdict",))
    if actual in REVIEW_VERDICTS:
        return VisualRegressionFixtureResult(fixture.fixture_id, fixture.target, "NEEDS_REVIEW", fixture.expected_verdict, actual, True, ("actual verdict requires review before pass/fail closure",))
    return VisualRegressionFixtureResult(fixture.fixture_id, fixture.target, "NEEDS_REVIEW", fixture.expected_verdict, actual, True, ("unrecognized actual verdict requires review",))


def _suite_verdict(gate: str, passed: int, failed: int, review: int, blocked: int, total: int) -> str:
    if gate == "BLOCKED" or blocked:
        return "VISUAL_REGRESSION_FIXTURE_SUITE_BLOCKED_BY_STEWARD"
    if failed:
        return "VISUAL_REGRESSION_FIXTURE_SUITE_FAILED_REQUIRES_REVIEW"
    if review:
        return "VISUAL_REGRESSION_FIXTURE_SUITE_NEEDS_REVIEW"
    if total and passed == total:
        return "VISUAL_REGRESSION_FIXTURE_SUITE_PASSED"
    return "VISUAL_REGRESSION_FIXTURE_SUITE_PLANNED_NOT_EXECUTED"


def _actions(verdict: str) -> tuple[str, ...]:
    return {
        "VISUAL_REGRESSION_FIXTURE_SUITE_PASSED": ("record repeatable visual fixture suite as passing evidence",),
        "VISUAL_REGRESSION_FIXTURE_SUITE_FAILED_REQUIRES_REVIEW": ("route failed fixtures to Steward/VZ and implementation agent", "do not claim visual repair closure"),
        "VISUAL_REGRESSION_FIXTURE_SUITE_NEEDS_REVIEW": ("collect missing evidence or Steward/VZ review before closure",),
        "VISUAL_REGRESSION_FIXTURE_SUITE_BLOCKED_BY_STEWARD": ("halt fixture-run claims until Steward/VZ unblocks gate",),
        "VISUAL_REGRESSION_FIXTURE_SUITE_PLANNED_NOT_EXECUTED": ("keep as plan-only suite; do not imply execution",),
    }.get(verdict, ("request Steward/VZ review",))


def _fixture_from_mapping(item: Mapping[str, Any]) -> VisualRegressionFixture:
    def tup(name: str) -> tuple[str, ...]:
        value = item.get(name, ())
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        return tuple(str(v) for v in value)
    return VisualRegressionFixture(
        fixture_id=str(item.get("fixture_id") or item.get("id") or "fixture"),
        target=str(item.get("target") or "unspecified target"),
        mode=str(item.get("mode") or "HARNESS_PLAN_ONLY"),
        expected_verdict=str(item.get("expected_verdict") or "VISUAL_REPAIR_VERIFIED"),
        actual_verdict=str(item["actual_verdict"]) if item.get("actual_verdict") is not None else None,
        before_refs=tup("before_refs"),
        after_refs=tup("after_refs"),
        before_after_verification_receipt_ids=tup("before_after_verification_receipt_ids"),
        evidence_refs=tup("evidence_refs"),
        tags=tup("tags"),
        steward_review_required=bool(item.get("steward_review_required", False)),
        implementation_hint=str(item["implementation_hint"]) if item.get("implementation_hint") is not None else None,
    )


def _inside(root: Path, path: str | Path) -> Path:
    p = Path(path)
    p = (root / p).resolve() if not p.is_absolute() else p.resolve()
    if p != root and root not in p.parents:
        raise ValueError(f"fixture manifest escapes workspace root: {p}")
    if not p.is_file():
        raise ValueError(f"fixture manifest does not exist as file: {p}")
    return p


def _scenario(name: str) -> tuple[str, str, tuple[VisualRegressionFixture, ...], str]:
    if name == "passing":
        return "v49-demo-suite", "local preview", (VisualRegressionFixture("panel-overlap", "local preview", "PRECAPTURED_BEFORE_AFTER_VERIFICATION", "VISUAL_REPAIR_VERIFIED", "VISUAL_REPAIR_VERIFIED", before_refs=("before.png",), after_refs=("after.png",)),), "APPROVED_PLAN_ONLY"
    if name == "failed":
        return "v49-demo-suite", "local preview", (VisualRegressionFixture("scroll-regression", "local preview", "PRECAPTURED_BEFORE_AFTER_VERIFICATION", "VISUAL_REPAIR_VERIFIED", "VISUAL_REGRESSION_OR_NEW_ISSUE_REQUIRES_REVIEW"),), "APPROVED_PLAN_ONLY"
    if name == "blocked":
        return "v49-demo-suite", "restricted preview", (VisualRegressionFixture("restricted", "restricted preview", "PRECAPTURED_BEFORE_AFTER_VERIFICATION", "VISUAL_REPAIR_VERIFIED", "VISUAL_REPAIR_VERIFIED"),), "BLOCKED"
    return "v49-plan-suite", "local preview", (VisualRegressionFixture("planned-panel-overlap", "local preview", "HARNESS_PLAN_ONLY"),), "APPROVED_PLAN_ONLY"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    return prefix + "-" + hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:16]


def _json(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _json(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_json(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _json(v) for k, v in value.items()}
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create an ION V49 visual regression fixture runner receipt.")
    parser.add_argument("workspace_root")
    parser.add_argument("--scenario", choices=("planned", "passing", "failed", "blocked"), default="planned")
    parser.add_argument("--manifest", default=None, help="optional local fixture manifest JSON path")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.manifest:
        suite_id, suite_target, fixtures = load_visual_regression_fixture_manifest(args.workspace_root, args.manifest)
        gate = "APPROVED_PLAN_ONLY"
    else:
        suite_id, suite_target, fixtures, gate = _scenario(args.scenario)
    receipt = build_visual_regression_fixture_run_receipt(suite_id=suite_id, suite_target=suite_target, fixtures=fixtures, steward_gate_status=gate, emitted_at="2026-04-25T06:49:00+00:00")
    if args.write:
        print(write_visual_regression_fixture_run_receipt(args.workspace_root, receipt).as_posix())
    print(json.dumps(_json(receipt), indent=2, sort_keys=True))
    errors = validate_visual_regression_fixture_run_receipt(receipt)
    if errors:
        print(json.dumps({"validation_errors": errors}, indent=2))
        return 4
    if receipt.suite_verdict == "VISUAL_REGRESSION_FIXTURE_SUITE_BLOCKED_BY_STEWARD":
        return 3
    if receipt.suite_verdict in ("VISUAL_REGRESSION_FIXTURE_SUITE_FAILED_REQUIRES_REVIEW", "VISUAL_REGRESSION_FIXTURE_SUITE_NEEDS_REVIEW"):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
