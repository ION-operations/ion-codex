"""V54 visual run receipt to diagnosis/verification binding.

Binds V53 fixture-bound local browser execution run receipts back into V45
visual diagnosis receipts and V48 before/after verification receipts. This
surface supports evidence closure without granting additional browser,
network, credential, form-submission, persistent mutation, or production
authority.
"""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.visual_run_receipt_to_diagnosis_binding.v1"
VERSION = "V54_VISUAL_RUN_RECEIPT_TO_DIAGNOSIS_BINDING"
AUTHORITY_SCOPE = "VISUAL_RUN_TO_DIAGNOSIS_CLOSURE_RECEIPT_ONLY"
DEFAULT_REPORT_DIR = "ION/05_context/history/visual_run_diagnosis_binding_receipts"

CLOSED_RUN_VERDICTS = ("LOCAL_BROWSER_EXECUTION_RUN_RECEIPT_ACCEPTED",)
REVIEW_RUN_VERDICTS = ("LOCAL_BROWSER_EXECUTION_RUN_NEEDS_REVIEW", "LOCAL_BROWSER_EXECUTION_RUN_FAILED_REQUIRES_REVIEW")
REJECTED_RUN_VERDICTS = ("LOCAL_BROWSER_EXECUTION_RUN_REJECTED_FOR_FORBIDDEN_EVENT", "LOCAL_BROWSER_EXECUTION_RUN_BLOCKED_BY_STEWARD")
BEFORE_AFTER_CLOSURE_VERDICTS = ("VISUAL_REPAIR_VERIFIED",)
BEFORE_AFTER_REVIEW_VERDICTS = (
    "VISUAL_REPAIR_PARTIAL_NEEDS_FOLLOWUP",
    "VISUAL_REGRESSION_OR_NEW_ISSUE_REQUIRES_REVIEW",
    "VISUAL_VERIFICATION_NEEDS_AFTER_EVIDENCE",
    "VISUAL_CHANGE_EVIDENCE_RECORDED_REQUIRES_REVIEW",
    "VISUAL_VERIFICATION_NO_ACTIONABLE_CHANGE_RECORDED",
    "BLOCKED_BY_STEWARD",
)
DIAGNOSIS_VERDICTS = (
    "NO_ACTIONABLE_VISUAL_ISSUES_RECORDED",
    "VISUAL_ISSUES_RECORDED",
    "HIGH_RISK_VISUAL_DIAGNOSIS_REQUIRES_REVIEW",
    "BROWSER_HARNESS_PLAN_REQUIRES_STEWARD_REVIEW",
)
FORBIDDEN_CAPABILITIES = {
    "unrestricted_browser_control": False,
    "external_network_access": False,
    "credential_or_session_import": False,
    "account_operation": False,
    "destructive_action": False,
    "form_submission": False,
    "purchase_or_submission": False,
    "persistent_dom_mutation": False,
    "production_visual_automation": False,
    "production_authority": False,
}

@dataclass(frozen=True)
class VisualRunDiagnosisBindingRequest:
    binding_name: str
    target: str
    diagnosis_receipt_ids: tuple[str, ...] = ()
    before_after_verification_ids: tuple[str, ...] = ()
    local_browser_run_receipt_ids: tuple[str, ...] = ()
    observation_packet_ids: tuple[str, ...] = ()
    diagnosis_verdicts: tuple[str, ...] = ()
    before_after_verdicts: tuple[str, ...] = ()
    run_verdicts: tuple[str, ...] = ()
    resolved_findings: tuple[str, ...] = ()
    persistent_findings: tuple[str, ...] = ()
    regression_findings: tuple[str, ...] = ()
    run_failure_codes: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    steward_gate_status: str = "APPROVED_CLOSURE_BINDING"
    requested_capabilities: dict[str, bool] = field(default_factory=dict)
    review_notes: tuple[str, ...] = ()

@dataclass(frozen=True)
class VisualRunDiagnosisBindingReceipt:
    schema_id: str
    version: str
    binding_id: str
    emitted_at: str
    binding_name: str
    target: str
    authority_scope: str
    steward_gate_status: str
    diagnosis_receipt_ids: tuple[str, ...]
    before_after_verification_ids: tuple[str, ...]
    local_browser_run_receipt_ids: tuple[str, ...]
    observation_packet_ids: tuple[str, ...]
    diagnosis_verdicts: tuple[str, ...]
    before_after_verdicts: tuple[str, ...]
    run_verdicts: tuple[str, ...]
    resolved_findings: tuple[str, ...]
    persistent_findings: tuple[str, ...]
    regression_findings: tuple[str, ...]
    run_failure_codes: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    closure_findings: tuple[str, ...]
    closure_verdict: str
    issue_closed: bool
    review_required: bool
    recommended_next_actions: tuple[str, ...]
    production_authority: bool = False
    unrestricted_browser_control_authorized: bool = False
    external_network_authorized: bool = False
    credential_access_authorized: bool = False
    submit_or_account_action_authorized: bool = False
    persistent_dom_mutation_authorized: bool = False
    forbidden_capabilities: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CAPABILITIES))

def build_visual_run_diagnosis_binding_receipt(*, request: VisualRunDiagnosisBindingRequest, emitted_at: str | None = None) -> VisualRunDiagnosisBindingReceipt:
    _validate_request(request)
    findings = list(request.review_notes)
    forbidden_requested = tuple(k for k, v in request.requested_capabilities.items() if v and k in FORBIDDEN_CAPABILITIES)
    if forbidden_requested:
        findings.append("requested forbidden capabilities: " + ", ".join(sorted(forbidden_requested)))
    if not request.diagnosis_receipt_ids:
        findings.append("no visual diagnosis receipt lineage provided")
    if not request.before_after_verification_ids:
        findings.append("no before/after verification receipt lineage provided")
    if not request.local_browser_run_receipt_ids:
        findings.append("no V53 local browser execution run receipt lineage provided")
    if not request.observation_packet_ids:
        findings.append("no visual observation packet lineage provided")
    if not request.evidence_refs:
        findings.append("no evidence references attached to closure binding")
    if request.steward_gate_status == "STEWARD_REVIEW_REQUIRED":
        findings.append("Steward/VZ review required before visual issue closure")
    if request.steward_gate_status == "BLOCKED":
        findings.append("Steward/VZ blocked visual issue closure")
    bad_run = tuple(v for v in request.run_verdicts if v in REJECTED_RUN_VERDICTS)
    review_run = tuple(v for v in request.run_verdicts if v in REVIEW_RUN_VERDICTS)
    closed_run = tuple(v for v in request.run_verdicts if v in CLOSED_RUN_VERDICTS)
    if bad_run:
        findings.append("run receipt contains rejected/blocked verdict: " + ", ".join(bad_run))
    if review_run:
        findings.append("run receipt requires review: " + ", ".join(review_run))
    if not closed_run:
        findings.append("no accepted V53 local browser run receipt verdict present")
    bad_ba = tuple(v for v in request.before_after_verdicts if v in BEFORE_AFTER_REVIEW_VERDICTS)
    closed_ba = tuple(v for v in request.before_after_verdicts if v in BEFORE_AFTER_CLOSURE_VERDICTS)
    if bad_ba:
        findings.append("before/after verification requires review: " + ", ".join(bad_ba))
    if not closed_ba:
        findings.append("no verified V48 before/after repair verdict present")
    if request.persistent_findings:
        findings.append("persistent findings remain: " + ", ".join(request.persistent_findings))
    if request.regression_findings:
        findings.append("regression findings remain: " + ", ".join(request.regression_findings))
    serious_failures = tuple(x for x in request.run_failure_codes if x not in ("NONE", "CAPTURE_TIMEOUT") and not x.startswith("INFO"))
    if serious_failures:
        findings.append("run failure taxonomy not clean: " + ", ".join(serious_failures))
    verdict = _closure_verdict(request, findings, bool(forbidden_requested), bool(bad_run), bool(review_run), bool(closed_run), bool(closed_ba), bool(bad_ba))
    issue_closed = verdict == "VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE"
    if issue_closed:
        findings.append("visual issue diagnostically closed with diagnosis, before/after verification, and V53 local-run evidence")
    ts = emitted_at or _utc_now()
    bid = _stable_id("v54-visual-run-diagnosis-binding", ts, request.binding_name, request.target, verdict)
    return VisualRunDiagnosisBindingReceipt(
        schema_id=SCHEMA_ID,
        version=VERSION,
        binding_id=bid,
        emitted_at=ts,
        binding_name=request.binding_name,
        target=request.target,
        authority_scope=AUTHORITY_SCOPE,
        steward_gate_status=request.steward_gate_status,
        diagnosis_receipt_ids=request.diagnosis_receipt_ids,
        before_after_verification_ids=request.before_after_verification_ids,
        local_browser_run_receipt_ids=request.local_browser_run_receipt_ids,
        observation_packet_ids=request.observation_packet_ids,
        diagnosis_verdicts=request.diagnosis_verdicts,
        before_after_verdicts=request.before_after_verdicts,
        run_verdicts=request.run_verdicts,
        resolved_findings=request.resolved_findings,
        persistent_findings=request.persistent_findings,
        regression_findings=request.regression_findings,
        run_failure_codes=request.run_failure_codes,
        evidence_refs=request.evidence_refs,
        closure_findings=tuple(findings),
        closure_verdict=verdict,
        issue_closed=issue_closed,
        review_required=verdict != "VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE",
        recommended_next_actions=_actions(verdict),
        production_authority=False,
    )

def validate_visual_run_diagnosis_binding_receipt(receipt: VisualRunDiagnosisBindingReceipt) -> tuple[str, ...]:
    errors: list[str] = []
    if receipt.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if receipt.version != VERSION:
        errors.append("version mismatch")
    if receipt.authority_scope != AUTHORITY_SCOPE:
        errors.append("authority scope mismatch")
    if receipt.production_authority:
        errors.append("production authority must remain false")
    if receipt.unrestricted_browser_control_authorized or receipt.external_network_authorized or receipt.credential_access_authorized or receipt.submit_or_account_action_authorized or receipt.persistent_dom_mutation_authorized:
        errors.append("forbidden authority flag must remain false")
    if any(receipt.forbidden_capabilities.values()):
        errors.append("forbidden capabilities must all remain false")
    if receipt.issue_closed and receipt.closure_verdict != "VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE":
        errors.append("issue_closed requires closure verdict")
    if receipt.issue_closed and receipt.review_required:
        errors.append("closed issue must not require review")
    if receipt.closure_verdict != "VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE" and receipt.issue_closed:
        errors.append("non-closed verdict cannot mark issue_closed")
    return tuple(errors)

def load_visual_run_diagnosis_binding_request(workspace_root: str | Path, request_path: str | Path) -> VisualRunDiagnosisBindingRequest:
    root = Path(workspace_root).resolve()
    p = _inside(root, request_path)
    return request_from_mapping(json.loads(p.read_text(encoding="utf-8")))

def request_from_mapping(data: Mapping[str, Any]) -> VisualRunDiagnosisBindingRequest:
    def tup(name: str, default: Sequence[str] = ()) -> tuple[str, ...]:
        value = data.get(name, default)
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        return tuple(str(x) for x in value)
    return VisualRunDiagnosisBindingRequest(
        binding_name=str(data.get("binding_name") or "visual run diagnosis binding"),
        target=str(data.get("target") or "unspecified visual target"),
        diagnosis_receipt_ids=tup("diagnosis_receipt_ids"),
        before_after_verification_ids=tup("before_after_verification_ids"),
        local_browser_run_receipt_ids=tup("local_browser_run_receipt_ids"),
        observation_packet_ids=tup("observation_packet_ids"),
        diagnosis_verdicts=tup("diagnosis_verdicts"),
        before_after_verdicts=tup("before_after_verdicts"),
        run_verdicts=tup("run_verdicts"),
        resolved_findings=tup("resolved_findings"),
        persistent_findings=tup("persistent_findings"),
        regression_findings=tup("regression_findings"),
        run_failure_codes=tup("run_failure_codes", ("NONE",)),
        evidence_refs=tup("evidence_refs"),
        steward_gate_status=str(data.get("steward_gate_status") or "APPROVED_CLOSURE_BINDING"),
        requested_capabilities={str(k): bool(v) for k, v in (data.get("requested_capabilities") or {}).items()},
        review_notes=tup("review_notes"),
    )

def write_visual_run_diagnosis_binding_receipt(workspace_root: str | Path, receipt: VisualRunDiagnosisBindingReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt.binding_id}.visual_run_diagnosis_binding_receipt.json"
    path.write_text(json.dumps(_json(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def _closure_verdict(request: VisualRunDiagnosisBindingRequest, findings: Sequence[str], forbidden_requested: bool, bad_run: bool, review_run: bool, closed_run: bool, closed_ba: bool, bad_ba: bool) -> str:
    if request.steward_gate_status == "BLOCKED":
        return "VISUAL_ISSUE_CLOSURE_BLOCKED_BY_STEWARD"
    if forbidden_requested or bad_run or any("forbidden" in f.lower() for f in findings):
        return "VISUAL_ISSUE_CLOSURE_REJECTED_FOR_FORBIDDEN_EVENT"
    if request.regression_findings or bad_ba:
        return "VISUAL_ISSUE_CLOSURE_REGRESSION_REQUIRES_REVIEW"
    if request.persistent_findings or review_run or request.steward_gate_status == "STEWARD_REVIEW_REQUIRED":
        return "VISUAL_ISSUE_CLOSURE_NEEDS_FOLLOWUP"
    if closed_run and closed_ba and request.resolved_findings and not findings:
        return "VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE"
    return "VISUAL_ISSUE_CLOSURE_NEEDS_REVIEW"

def _actions(verdict: str) -> tuple[str, ...]:
    table = {
        "VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE": ("mark visual issue diagnostically closed", "attach binding receipt to successor handoff and graph projection"),
        "VISUAL_ISSUE_CLOSURE_NEEDS_REVIEW": ("repair missing lineage or evidence before closure",),
        "VISUAL_ISSUE_CLOSURE_NEEDS_FOLLOWUP": ("route persistent or review-requiring visual evidence to implementation agent",),
        "VISUAL_ISSUE_CLOSURE_REGRESSION_REQUIRES_REVIEW": ("block closure and route regression evidence to Steward/VZ and implementation review",),
        "VISUAL_ISSUE_CLOSURE_REJECTED_FOR_FORBIDDEN_EVENT": ("halt closure lineage and route forbidden event to security review",),
        "VISUAL_ISSUE_CLOSURE_BLOCKED_BY_STEWARD": ("do not close visual issue until Steward/VZ clears gate",),
    }
    return table.get(verdict, ("request Steward/VZ review",))

def _validate_request(request: VisualRunDiagnosisBindingRequest) -> None:
    if request.steward_gate_status not in ("APPROVED_CLOSURE_BINDING", "STEWARD_REVIEW_REQUIRED", "BLOCKED"):
        raise ValueError("invalid steward_gate_status: " + request.steward_gate_status)
    invalid_d = tuple(v for v in request.diagnosis_verdicts if v and v not in DIAGNOSIS_VERDICTS)
    if invalid_d:
        raise ValueError("invalid diagnosis verdicts: " + ", ".join(invalid_d))
    invalid_ba = tuple(v for v in request.before_after_verdicts if v and v not in BEFORE_AFTER_CLOSURE_VERDICTS + BEFORE_AFTER_REVIEW_VERDICTS)
    if invalid_ba:
        raise ValueError("invalid before/after verdicts: " + ", ".join(invalid_ba))
    invalid_run = tuple(v for v in request.run_verdicts if v and v not in CLOSED_RUN_VERDICTS + REVIEW_RUN_VERDICTS + REJECTED_RUN_VERDICTS)
    if invalid_run:
        raise ValueError("invalid run verdicts: " + ", ".join(invalid_run))

def _scenario(name: str) -> VisualRunDiagnosisBindingRequest:
    base = dict(
        binding_name="V54 local UI repair closure",
        target="local preview panel",
        diagnosis_receipt_ids=("v45-diagnosis",),
        before_after_verification_ids=("v48-before-after",),
        local_browser_run_receipt_ids=("v53-run",),
        observation_packet_ids=("v44-observation",),
        diagnosis_verdicts=("VISUAL_ISSUES_RECORDED",),
        before_after_verdicts=("VISUAL_REPAIR_VERIFIED",),
        run_verdicts=("LOCAL_BROWSER_EXECUTION_RUN_RECEIPT_ACCEPTED",),
        resolved_findings=("panel-overlap",),
        run_failure_codes=("NONE",),
        evidence_refs=("screenshot://before", "screenshot://after", "run://v53-run"),
    )
    if name == "closed":
        return VisualRunDiagnosisBindingRequest(**base)
    if name == "review":
        data = dict(base); data["local_browser_run_receipt_ids"] = (); data["evidence_refs"] = (); return VisualRunDiagnosisBindingRequest(**data)
    if name == "followup":
        data = dict(base); data["persistent_findings"] = ("mobile-density",); return VisualRunDiagnosisBindingRequest(**data)
    if name == "regression":
        data = dict(base); data["before_after_verdicts"] = ("VISUAL_REGRESSION_OR_NEW_ISSUE_REQUIRES_REVIEW",); data["regression_findings"] = ("new-horizontal-scroll",); return VisualRunDiagnosisBindingRequest(**data)
    if name == "forbidden":
        data = dict(base); data["run_verdicts"] = ("LOCAL_BROWSER_EXECUTION_RUN_REJECTED_FOR_FORBIDDEN_EVENT",); data["run_failure_codes"] = ("FORBIDDEN_NETWORK_EVENT",); return VisualRunDiagnosisBindingRequest(**data)
    if name == "blocked":
        data = dict(base); data["steward_gate_status"] = "BLOCKED"; return VisualRunDiagnosisBindingRequest(**data)
    raise ValueError(name)

def _inside(root: Path, value: str | Path) -> Path:
    p = Path(value)
    resolved = p.resolve() if p.is_absolute() else (root / p).resolve()
    if resolved != root and root not in resolved.parents:
        raise ValueError(f"path escapes workspace root: {value}")
    return resolved
def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def _stable_id(prefix: str, *parts: str) -> str:
    return prefix + "-" + hashlib.sha256("\n".join(parts).encode()).hexdigest()[:16]
def _json(v: Any) -> Any:
    if hasattr(v, "__dataclass_fields__"):
        return {k: _json(x) for k, x in asdict(v).items()}
    if isinstance(v, tuple):
        return [_json(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _json(x) for k, x in v.items()}
    return v

def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build a V54 visual run-to-diagnosis closure binding receipt.")
    p.add_argument("--workspace-root", default=".")
    p.add_argument("--request")
    p.add_argument("--scenario", choices=("closed", "review", "followup", "regression", "forbidden", "blocked"), default="closed")
    p.add_argument("--write", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    request = load_visual_run_diagnosis_binding_request(a.workspace_root, a.request) if a.request else _scenario(a.scenario)
    receipt = build_visual_run_diagnosis_binding_receipt(request=request, emitted_at="2026-04-25T07:54:00+00:00")
    if a.write:
        print(write_visual_run_diagnosis_binding_receipt(a.workspace_root, receipt).as_posix())
    print(json.dumps(_json(receipt), indent=2, sort_keys=True) if a.json else f"verdict={receipt.closure_verdict} authority={receipt.authority_scope} closed={receipt.issue_closed}")
    errors = validate_visual_run_diagnosis_binding_receipt(receipt)
    if errors:
        print("\n".join("ERROR: " + e for e in errors)); return 4
    if receipt.closure_verdict in ("VISUAL_ISSUE_CLOSURE_REJECTED_FOR_FORBIDDEN_EVENT", "VISUAL_ISSUE_CLOSURE_BLOCKED_BY_STEWARD"):
        return 3
    if receipt.review_required:
        return 2
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
