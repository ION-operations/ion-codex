"""V50 visual fixture runner local sandbox review.

This module intentionally does not execute browsers or visual fixtures. It records
whether a proposed local/dev visual fixture runner remains inside the safety
boundary needed before any later execution sandbox specification can be discussed.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.visual_fixture_runner_sandbox_review.v1"
VERSION = "V50_VISUAL_FIXTURE_RUNNER_LOCAL_SANDBOX_REVIEW"
DEFAULT_REPORT_DIR = "ION/05_context/history/visual_sandbox_reviews"
AUTHORITY_SCOPE = "LOCAL_DEV_SANDBOX_REVIEW_ONLY"

SANDBOX_SCOPES = ("LOCAL_DEV_REVIEW_ONLY", "LOCAL_DEV_SPEC_CANDIDATE", "BLOCKED")
NETWORK_POLICIES = ("NO_NETWORK", "LOCALHOST_ONLY_PROPOSED", "UNREVIEWED", "BLOCKED")
CREDENTIAL_POLICIES = ("NO_CREDENTIALS", "SANITIZED_FIXTURES_ONLY", "UNREVIEWED", "BLOCKED")
DOM_MUTATION_POLICIES = ("NO_DOM_MUTATION", "TEMPORARY_ANNOTATION_ONLY_PROPOSED", "UNREVIEWED", "BLOCKED")
FILE_WRITE_POLICIES = ("RECEIPT_OUTPUT_ONLY", "WORKSPACE_ARTIFACT_OUTPUT_ONLY_PROPOSED", "UNREVIEWED", "BLOCKED")
STEWARD_GATE_STATUSES = ("APPROVED_REVIEW_ONLY", "STEWARD_REVIEW_REQUIRED", "BLOCKED")

FORBIDDEN_CAPABILITIES = {
    "browser_execution": False,
    "unrestricted_browser_control": False,
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
class VisualSandboxReviewRequest:
    surface_under_review: str
    lineage_refs: tuple[str, ...] = ()
    sandbox_scope: str = "LOCAL_DEV_REVIEW_ONLY"
    allowed_artifact_roots: tuple[str, ...] = ("ION/05_context/history/visual_*",)
    network_isolation: str = "NO_NETWORK"
    credential_policy: str = "NO_CREDENTIALS"
    dom_mutation_policy: str = "NO_DOM_MUTATION"
    file_write_policy: str = "RECEIPT_OUTPUT_ONLY"
    steward_gate_status: str = "APPROVED_REVIEW_ONLY"
    requested_capabilities: dict[str, bool] = field(default_factory=dict)
    review_notes: tuple[str, ...] = ()

@dataclass(frozen=True)
class VisualSandboxReviewReceipt:
    schema_id: str
    version: str
    review_id: str
    emitted_at: str
    surface_under_review: str
    lineage_refs: tuple[str, ...]
    sandbox_scope: str
    allowed_artifact_roots: tuple[str, ...]
    network_isolation: str
    credential_policy: str
    dom_mutation_policy: str
    file_write_policy: str
    steward_gate_status: str
    review_findings: tuple[str, ...]
    review_verdict: str
    recommended_next_actions: tuple[str, ...]
    authority_scope: str = AUTHORITY_SCOPE
    production_authority: bool = False
    forbidden_capabilities: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CAPABILITIES))

def build_visual_sandbox_review_receipt(*, request: VisualSandboxReviewRequest, emitted_at: str | None = None) -> VisualSandboxReviewReceipt:
    _validate_request_enums(request)
    findings = list(request.review_notes)
    blocked = request.steward_gate_status == "BLOCKED" or request.sandbox_scope == "BLOCKED"
    forbidden_requested = tuple(name for name, requested in request.requested_capabilities.items() if requested and name in FORBIDDEN_CAPABILITIES)
    if forbidden_requested:
        findings.append("requested forbidden capabilities: " + ", ".join(sorted(forbidden_requested)))
    if request.network_isolation != "NO_NETWORK":
        findings.append("network isolation is not yet strict NO_NETWORK")
    if request.credential_policy != "NO_CREDENTIALS":
        findings.append("credential policy is not yet strict NO_CREDENTIALS")
    if request.dom_mutation_policy != "NO_DOM_MUTATION":
        findings.append("DOM mutation policy is not yet strict NO_DOM_MUTATION")
    if request.file_write_policy != "RECEIPT_OUTPUT_ONLY":
        findings.append("file write policy is broader than receipt output only")
    if request.steward_gate_status == "STEWARD_REVIEW_REQUIRED":
        findings.append("Steward/VZ review required before any successor sandbox spec")
    if not request.allowed_artifact_roots:
        findings.append("no allowed artifact roots declared")

    if blocked:
        verdict = "SANDBOX_REVIEW_BLOCKED_BY_STEWARD"
    elif forbidden_requested:
        verdict = "SANDBOX_REVIEW_REJECTED_FOR_FORBIDDEN_CAPABILITY"
    elif findings and any(("not yet strict" in f or "broader than" in f or "review required" in f or "no allowed artifact roots" in f) for f in findings):
        verdict = "SANDBOX_REVIEW_NEEDS_REMEDIATION"
    else:
        verdict = "SANDBOX_REVIEW_PASSED_PLAN_ONLY"
        findings.append("review remains local/dev and plan-only; no browser execution authority granted")

    ts = emitted_at or _utc_now()
    review_id = _stable_id("v50-visual-sandbox-review", VERSION, ts, request.surface_under_review, verdict)
    return VisualSandboxReviewReceipt(
        SCHEMA_ID, VERSION, review_id, ts, request.surface_under_review, request.lineage_refs,
        request.sandbox_scope, request.allowed_artifact_roots, request.network_isolation,
        request.credential_policy, request.dom_mutation_policy, request.file_write_policy,
        request.steward_gate_status, tuple(findings), verdict, _actions(verdict)
    )

def load_visual_sandbox_review_request(workspace_root: str | Path, request_path: str | Path) -> VisualSandboxReviewRequest:
    root = Path(workspace_root).resolve()
    path = _inside(root, request_path)
    return request_from_mapping(json.loads(path.read_text(encoding="utf-8")))

def request_from_mapping(data: Mapping[str, Any]) -> VisualSandboxReviewRequest:
    def tup(name: str, default: tuple[str, ...] = ()) -> tuple[str, ...]:
        value = data.get(name, default)
        if value is None: return ()
        if isinstance(value, str): return (value,)
        return tuple(str(v) for v in value)
    requested = data.get("requested_capabilities", {}) or {}
    return VisualSandboxReviewRequest(
        surface_under_review=str(data.get("surface_under_review") or "visual fixture runner"),
        lineage_refs=tup("lineage_refs"),
        sandbox_scope=str(data.get("sandbox_scope") or "LOCAL_DEV_REVIEW_ONLY"),
        allowed_artifact_roots=tup("allowed_artifact_roots", ("ION/05_context/history/visual_*",)),
        network_isolation=str(data.get("network_isolation") or "NO_NETWORK"),
        credential_policy=str(data.get("credential_policy") or "NO_CREDENTIALS"),
        dom_mutation_policy=str(data.get("dom_mutation_policy") or "NO_DOM_MUTATION"),
        file_write_policy=str(data.get("file_write_policy") or "RECEIPT_OUTPUT_ONLY"),
        steward_gate_status=str(data.get("steward_gate_status") or "APPROVED_REVIEW_ONLY"),
        requested_capabilities={str(k): bool(v) for k, v in requested.items()},
        review_notes=tup("review_notes"),
    )

def validate_visual_sandbox_review_receipt(receipt: VisualSandboxReviewReceipt) -> tuple[str, ...]:
    errors: list[str] = []
    if receipt.schema_id != SCHEMA_ID: errors.append("schema_id mismatch")
    if receipt.version != VERSION: errors.append("version mismatch")
    if receipt.authority_scope != AUTHORITY_SCOPE: errors.append("authority scope mismatch")
    if receipt.production_authority is not False: errors.append("production authority must be false")
    if any(value is not False for value in receipt.forbidden_capabilities.values()):
        errors.append("forbidden capabilities must all be false")
    if receipt.review_verdict == "SANDBOX_REVIEW_PASSED_PLAN_ONLY":
        if receipt.network_isolation != "NO_NETWORK": errors.append("passing review requires NO_NETWORK")
        if receipt.credential_policy != "NO_CREDENTIALS": errors.append("passing review requires NO_CREDENTIALS")
        if receipt.dom_mutation_policy != "NO_DOM_MUTATION": errors.append("passing review requires NO_DOM_MUTATION")
        if receipt.file_write_policy != "RECEIPT_OUTPUT_ONLY": errors.append("passing review requires RECEIPT_OUTPUT_ONLY")
        if receipt.steward_gate_status != "APPROVED_REVIEW_ONLY": errors.append("passing review requires APPROVED_REVIEW_ONLY")
    return tuple(errors)

def write_visual_sandbox_review_receipt(workspace_root: str | Path, receipt: VisualSandboxReviewReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt.review_id}.visual_sandbox_review_receipt.json"
    path.write_text(json.dumps(_json(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def _validate_request_enums(request: VisualSandboxReviewRequest) -> None:
    for name, value, allowed in (
        ("sandbox_scope", request.sandbox_scope, SANDBOX_SCOPES),
        ("network_isolation", request.network_isolation, NETWORK_POLICIES),
        ("credential_policy", request.credential_policy, CREDENTIAL_POLICIES),
        ("dom_mutation_policy", request.dom_mutation_policy, DOM_MUTATION_POLICIES),
        ("file_write_policy", request.file_write_policy, FILE_WRITE_POLICIES),
        ("steward_gate_status", request.steward_gate_status, STEWARD_GATE_STATUSES),
    ):
        if value not in allowed:
            raise ValueError(f"invalid {name}: {value}")

def _inside(root: Path, path: str | Path) -> Path:
    p = Path(path)
    p = (root / p).resolve() if not p.is_absolute() else p.resolve()
    if p != root and root not in p.parents:
        raise ValueError(f"sandbox review request escapes workspace root: {p}")
    if not p.is_file():
        raise ValueError(f"sandbox review request does not exist as file: {p}")
    return p

def _scenario(name: str) -> VisualSandboxReviewRequest:
    if name == "pass":
        return VisualSandboxReviewRequest(
            surface_under_review="V49 visual regression fixture runner",
            lineage_refs=("V47_LOCAL_BROWSER_CAPTURE_ADAPTER_STUB", "V48_VISUAL_BEFORE_AFTER_VERIFICATION_LOOP", "V49_VISUAL_REGRESSION_FIXTURE_RUNNER_PLAN"),
            review_notes=("all stronger execution authority remains out of scope",),
        )
    if name == "remediate":
        return VisualSandboxReviewRequest(
            surface_under_review="future local browser execution sandbox",
            network_isolation="LOCALHOST_ONLY_PROPOSED",
            credential_policy="SANITIZED_FIXTURES_ONLY",
            dom_mutation_policy="TEMPORARY_ANNOTATION_ONLY_PROPOSED",
            file_write_policy="WORKSPACE_ARTIFACT_OUTPUT_ONLY_PROPOSED",
            steward_gate_status="STEWARD_REVIEW_REQUIRED",
        )
    if name == "forbidden":
        return VisualSandboxReviewRequest(
            surface_under_review="unsafe visual automation proposal",
            requested_capabilities={"browser_execution": True, "credential_sensitive_action": True},
        )
    return VisualSandboxReviewRequest(
        surface_under_review="blocked visual automation proposal",
        sandbox_scope="BLOCKED",
        steward_gate_status="BLOCKED",
    )

def _actions(verdict: str) -> tuple[str, ...]:
    return {
        "SANDBOX_REVIEW_PASSED_PLAN_ONLY": ("allow successor branch to draft a local-only execution sandbox specification", "do not claim browser execution authority"),
        "SANDBOX_REVIEW_NEEDS_REMEDIATION": ("tighten sandbox constraints before successor specification", "route policy gaps to Steward/VZ review"),
        "SANDBOX_REVIEW_BLOCKED_BY_STEWARD": ("halt visual execution planning until Steward/VZ unblocks",),
        "SANDBOX_REVIEW_REJECTED_FOR_FORBIDDEN_CAPABILITY": ("reject proposal or remove forbidden capabilities",),
    }.get(verdict, ("request Steward/VZ review",))

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _stable_id(prefix: str, *parts: str) -> str:
    return prefix + "-" + hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:16]

def _json(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _json(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple): return [_json(v) for v in value]
    if isinstance(value, dict): return {str(k): _json(v) for k, v in value.items()}
    return value

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create an ION V50 visual sandbox review receipt.")
    parser.add_argument("workspace_root")
    parser.add_argument("--scenario", choices=("pass", "remediate", "forbidden", "blocked"), default="pass")
    parser.add_argument("--request", default=None, help="optional local sandbox review request JSON path")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    request = load_visual_sandbox_review_request(args.workspace_root, args.request) if args.request else _scenario(args.scenario)
    receipt = build_visual_sandbox_review_receipt(request=request, emitted_at="2026-04-25T06:50:00+00:00")
    if args.write:
        print(write_visual_sandbox_review_receipt(args.workspace_root, receipt).as_posix())
    print(json.dumps(_json(receipt), indent=2, sort_keys=True))
    errors = validate_visual_sandbox_review_receipt(receipt)
    if errors:
        print(json.dumps({"validation_errors": errors}, indent=2))
        return 4
    if receipt.review_verdict == "SANDBOX_REVIEW_BLOCKED_BY_STEWARD": return 3
    if receipt.review_verdict in ("SANDBOX_REVIEW_NEEDS_REMEDIATION", "SANDBOX_REVIEW_REJECTED_FOR_FORBIDDEN_CAPABILITY"): return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
