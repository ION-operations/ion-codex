"""V51 local browser execution sandbox specification.

This module intentionally does not launch a browser, navigate a page, execute
JavaScript, mutate a DOM, submit forms, or touch credentials. It records whether
a proposed future local/dev browser execution sandbox specification stays inside
ION's visual-agent safety boundary.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

SCHEMA_ID = "ion.local_browser_execution_sandbox_spec.v1"
VERSION = "V51_LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC"
DEFAULT_REPORT_DIR = "ION/05_context/history/local_browser_execution_sandbox_specs"
AUTHORITY_SCOPE = "LOCAL_DEV_BROWSER_EXECUTION_SANDBOX_SPEC_ONLY"

SANDBOX_SPEC_STATUSES = ("SPEC_ONLY", "STEWARD_REVIEW_REQUIRED", "BLOCKED")
TARGET_ORIGIN_POLICIES = ("LOCAL_FILES_OR_LOOPBACK_ONLY", "LOOPBACK_ONLY", "UNREVIEWED", "BLOCKED")
NETWORK_POLICIES = ("NO_EXTERNAL_NETWORK", "NO_NETWORK", "UNREVIEWED", "BLOCKED")
CREDENTIAL_POLICIES = ("NO_CREDENTIALS_OR_SESSION_IMPORT", "SANITIZED_TEST_FIXTURES_ONLY", "UNREVIEWED", "BLOCKED")
NAVIGATION_POLICIES = ("FIXTURE_MANIFEST_ONLY", "SINGLE_URL_ALLOWLIST_ONLY", "UNREVIEWED", "BLOCKED")
MUTATION_POLICIES = ("NO_PERSISTENT_MUTATION", "TEMPORARY_TEST_INSTRUMENTATION_ONLY", "UNREVIEWED", "BLOCKED")
FILE_WRITE_POLICIES = ("RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY", "RECEIPTS_ONLY", "UNREVIEWED", "BLOCKED")
STEWARD_GATE_STATUSES = ("APPROVED_SPEC_ONLY", "STEWARD_REVIEW_REQUIRED", "BLOCKED")

FORBIDDEN_CAPABILITIES: dict[str, bool] = {
    "live_browser_execution_authorized": False,
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
class LocalBrowserExecutionSandboxSpecRequest:
    spec_name: str
    lineage_refs: tuple[str, ...] = ()
    sandbox_spec_status: str = "SPEC_ONLY"
    target_origin_policy: str = "LOCAL_FILES_OR_LOOPBACK_ONLY"
    network_policy: str = "NO_EXTERNAL_NETWORK"
    credential_policy: str = "NO_CREDENTIALS_OR_SESSION_IMPORT"
    navigation_policy: str = "FIXTURE_MANIFEST_ONLY"
    mutation_policy: str = "NO_PERSISTENT_MUTATION"
    file_write_policy: str = "RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY"
    steward_gate_status: str = "APPROVED_SPEC_ONLY"
    required_controls: tuple[str, ...] = (
        "ephemeral_browser_profile",
        "fixture_manifest_required",
        "capture_artifact_hashing",
        "no_persistent_dom_mutation",
        "steward_receipt_required_before_execution_adapter",
    )
    requested_capabilities: dict[str, bool] = field(default_factory=dict)
    review_notes: tuple[str, ...] = ()

@dataclass(frozen=True)
class LocalBrowserExecutionSandboxSpecReceipt:
    schema_id: str
    version: str
    spec_id: str
    emitted_at: str
    spec_name: str
    lineage_refs: tuple[str, ...]
    sandbox_spec_status: str
    target_origin_policy: str
    network_policy: str
    credential_policy: str
    navigation_policy: str
    mutation_policy: str
    file_write_policy: str
    steward_gate_status: str
    required_controls: tuple[str, ...]
    review_findings: tuple[str, ...]
    spec_verdict: str
    recommended_next_actions: tuple[str, ...]
    authority_scope: str = AUTHORITY_SCOPE
    browser_execution_authorized: bool = False
    production_authority: bool = False
    forbidden_capabilities: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CAPABILITIES))

def build_local_browser_execution_sandbox_spec_receipt(*, request: LocalBrowserExecutionSandboxSpecRequest, emitted_at: str | None = None) -> LocalBrowserExecutionSandboxSpecReceipt:
    _validate_request_enums(request)
    findings = list(request.review_notes)
    blocked = request.sandbox_spec_status == "BLOCKED" or request.steward_gate_status == "BLOCKED"
    forbidden_requested = tuple(name for name, requested in request.requested_capabilities.items() if requested and name in FORBIDDEN_CAPABILITIES)
    if forbidden_requested:
        findings.append("requested forbidden capabilities: " + ", ".join(sorted(forbidden_requested)))
    if request.target_origin_policy not in ("LOCAL_FILES_OR_LOOPBACK_ONLY", "LOOPBACK_ONLY"):
        findings.append("target origin policy is not restricted to local files or loopback")
    if request.network_policy not in ("NO_EXTERNAL_NETWORK", "NO_NETWORK"):
        findings.append("network policy is not restricted against external network access")
    if request.credential_policy != "NO_CREDENTIALS_OR_SESSION_IMPORT":
        findings.append("credential policy permits or has not ruled out credential/session import")
    if request.navigation_policy not in ("FIXTURE_MANIFEST_ONLY", "SINGLE_URL_ALLOWLIST_ONLY"):
        findings.append("navigation policy is not fixture/allowlist constrained")
    if request.mutation_policy not in ("NO_PERSISTENT_MUTATION", "TEMPORARY_TEST_INSTRUMENTATION_ONLY"):
        findings.append("mutation policy is not constrained against persistent mutation")
    if request.file_write_policy not in ("RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY", "RECEIPTS_ONLY"):
        findings.append("file write policy is not constrained to receipts/capture artifacts")
    if request.steward_gate_status == "STEWARD_REVIEW_REQUIRED" or request.sandbox_spec_status == "STEWARD_REVIEW_REQUIRED":
        findings.append("Steward/VZ review required before any execution adapter prototype")
    missing_controls = tuple(control for control in ("ephemeral_browser_profile", "fixture_manifest_required", "capture_artifact_hashing", "steward_receipt_required_before_execution_adapter") if control not in request.required_controls)
    if missing_controls:
        findings.append("missing required controls: " + ", ".join(missing_controls))

    if blocked:
        verdict = "LOCAL_BROWSER_SANDBOX_SPEC_BLOCKED_BY_STEWARD"
    elif forbidden_requested:
        verdict = "LOCAL_BROWSER_SANDBOX_SPEC_REJECTED_FOR_FORBIDDEN_CAPABILITY"
    elif findings and any(_needs_remediation(finding) for finding in findings):
        verdict = "LOCAL_BROWSER_SANDBOX_SPEC_NEEDS_REMEDIATION"
    else:
        verdict = "LOCAL_BROWSER_SANDBOX_SPEC_ACCEPTED_SPEC_ONLY"
        findings.append("spec accepted as local/dev specification only; no live browser execution authority granted")

    ts = emitted_at or _utc_now()
    spec_id = _stable_id("v51-local-browser-execution-sandbox-spec", VERSION, ts, request.spec_name, verdict)
    return LocalBrowserExecutionSandboxSpecReceipt(
        SCHEMA_ID,
        VERSION,
        spec_id,
        ts,
        request.spec_name,
        request.lineage_refs,
        request.sandbox_spec_status,
        request.target_origin_policy,
        request.network_policy,
        request.credential_policy,
        request.navigation_policy,
        request.mutation_policy,
        request.file_write_policy,
        request.steward_gate_status,
        request.required_controls,
        tuple(findings),
        verdict,
        _actions(verdict),
    )

def load_local_browser_execution_sandbox_spec_request(workspace_root: str | Path, request_path: str | Path) -> LocalBrowserExecutionSandboxSpecRequest:
    root = Path(workspace_root).resolve()
    path = _inside(root, request_path)
    return request_from_mapping(json.loads(path.read_text(encoding="utf-8")))

def request_from_mapping(data: Mapping[str, Any]) -> LocalBrowserExecutionSandboxSpecRequest:
    def tup(name: str, default: tuple[str, ...] = ()) -> tuple[str, ...]:
        value = data.get(name, default)
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        return tuple(str(v) for v in value)
    requested = data.get("requested_capabilities", {}) or {}
    return LocalBrowserExecutionSandboxSpecRequest(
        spec_name=str(data.get("spec_name") or "local browser execution sandbox specification"),
        lineage_refs=tup("lineage_refs"),
        sandbox_spec_status=str(data.get("sandbox_spec_status") or "SPEC_ONLY"),
        target_origin_policy=str(data.get("target_origin_policy") or "LOCAL_FILES_OR_LOOPBACK_ONLY"),
        network_policy=str(data.get("network_policy") or "NO_EXTERNAL_NETWORK"),
        credential_policy=str(data.get("credential_policy") or "NO_CREDENTIALS_OR_SESSION_IMPORT"),
        navigation_policy=str(data.get("navigation_policy") or "FIXTURE_MANIFEST_ONLY"),
        mutation_policy=str(data.get("mutation_policy") or "NO_PERSISTENT_MUTATION"),
        file_write_policy=str(data.get("file_write_policy") or "RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY"),
        steward_gate_status=str(data.get("steward_gate_status") or "APPROVED_SPEC_ONLY"),
        required_controls=tup("required_controls", LocalBrowserExecutionSandboxSpecRequest.__dataclass_fields__["required_controls"].default),
        requested_capabilities={str(k): bool(v) for k, v in requested.items()},
        review_notes=tup("review_notes"),
    )

def validate_local_browser_execution_sandbox_spec_receipt(receipt: LocalBrowserExecutionSandboxSpecReceipt) -> tuple[str, ...]:
    errors: list[str] = []
    if receipt.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if receipt.version != VERSION:
        errors.append("version mismatch")
    if receipt.authority_scope != AUTHORITY_SCOPE:
        errors.append("authority scope mismatch")
    if receipt.browser_execution_authorized is not False:
        errors.append("browser execution must not be authorized by V51")
    if receipt.production_authority is not False:
        errors.append("production authority must be false")
    if any(value is not False for value in receipt.forbidden_capabilities.values()):
        errors.append("forbidden capabilities must all be false")
    if receipt.spec_verdict == "LOCAL_BROWSER_SANDBOX_SPEC_ACCEPTED_SPEC_ONLY":
        strict = {
            "target_origin_policy": receipt.target_origin_policy in ("LOCAL_FILES_OR_LOOPBACK_ONLY", "LOOPBACK_ONLY"),
            "network_policy": receipt.network_policy in ("NO_EXTERNAL_NETWORK", "NO_NETWORK"),
            "credential_policy": receipt.credential_policy == "NO_CREDENTIALS_OR_SESSION_IMPORT",
            "navigation_policy": receipt.navigation_policy in ("FIXTURE_MANIFEST_ONLY", "SINGLE_URL_ALLOWLIST_ONLY"),
            "mutation_policy": receipt.mutation_policy in ("NO_PERSISTENT_MUTATION", "TEMPORARY_TEST_INSTRUMENTATION_ONLY"),
            "file_write_policy": receipt.file_write_policy in ("RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY", "RECEIPTS_ONLY"),
            "steward_gate_status": receipt.steward_gate_status == "APPROVED_SPEC_ONLY",
        }
        for name, ok in strict.items():
            if not ok:
                errors.append(f"accepted spec requires strict {name}")
    return tuple(errors)

def write_local_browser_execution_sandbox_spec_receipt(workspace_root: str | Path, receipt: LocalBrowserExecutionSandboxSpecReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt.spec_id}.local_browser_execution_sandbox_spec_receipt.json"
    path.write_text(json.dumps(_json(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def _validate_request_enums(request: LocalBrowserExecutionSandboxSpecRequest) -> None:
    for name, value, allowed in (
        ("sandbox_spec_status", request.sandbox_spec_status, SANDBOX_SPEC_STATUSES),
        ("target_origin_policy", request.target_origin_policy, TARGET_ORIGIN_POLICIES),
        ("network_policy", request.network_policy, NETWORK_POLICIES),
        ("credential_policy", request.credential_policy, CREDENTIAL_POLICIES),
        ("navigation_policy", request.navigation_policy, NAVIGATION_POLICIES),
        ("mutation_policy", request.mutation_policy, MUTATION_POLICIES),
        ("file_write_policy", request.file_write_policy, FILE_WRITE_POLICIES),
        ("steward_gate_status", request.steward_gate_status, STEWARD_GATE_STATUSES),
    ):
        if value not in allowed:
            raise ValueError(f"invalid {name}: {value}")

def _needs_remediation(finding: str) -> bool:
    markers = (
        "not restricted",
        "permits or has not ruled out",
        "not fixture/allowlist constrained",
        "not constrained",
        "review required",
        "missing required controls",
    )
    return any(marker in finding for marker in markers)

def _inside(root: Path, path: str | Path) -> Path:
    p = Path(path)
    p = (root / p).resolve() if not p.is_absolute() else p.resolve()
    if p != root and root not in p.parents:
        raise ValueError(f"sandbox spec request escapes workspace root: {p}")
    if not p.is_file():
        raise ValueError(f"sandbox spec request does not exist as file: {p}")
    return p

def _scenario(name: str) -> LocalBrowserExecutionSandboxSpecRequest:
    if name == "accepted":
        return LocalBrowserExecutionSandboxSpecRequest(
            spec_name="V51 local browser execution sandbox spec",
            lineage_refs=("V50_VISUAL_FIXTURE_RUNNER_LOCAL_SANDBOX_REVIEW",),
            review_notes=("execution remains a future adapter concern",),
        )
    if name == "remediate":
        return LocalBrowserExecutionSandboxSpecRequest(
            spec_name="underconstrained browser sandbox spec",
            target_origin_policy="UNREVIEWED",
            network_policy="UNREVIEWED",
            credential_policy="SANITIZED_TEST_FIXTURES_ONLY",
            navigation_policy="UNREVIEWED",
            mutation_policy="UNREVIEWED",
            file_write_policy="UNREVIEWED",
            steward_gate_status="STEWARD_REVIEW_REQUIRED",
        )
    if name == "forbidden":
        return LocalBrowserExecutionSandboxSpecRequest(
            spec_name="unsafe browser automation spec",
            requested_capabilities={"live_browser_execution_authorized": True, "external_network_access": True},
        )
    return LocalBrowserExecutionSandboxSpecRequest(
        spec_name="blocked browser sandbox spec",
        sandbox_spec_status="BLOCKED",
        steward_gate_status="BLOCKED",
    )

def _actions(verdict: str) -> tuple[str, ...]:
    return {
        "LOCAL_BROWSER_SANDBOX_SPEC_ACCEPTED_SPEC_ONLY": (
            "allow successor branch to prototype a local-only execution harness behind explicit Steward/VZ gate",
            "do not claim live browser execution authority from this spec",
        ),
        "LOCAL_BROWSER_SANDBOX_SPEC_NEEDS_REMEDIATION": (
            "tighten target origin, network, credential, navigation, mutation, and artifact-write controls",
            "route unresolved constraints to Steward/VZ before any execution prototype",
        ),
        "LOCAL_BROWSER_SANDBOX_SPEC_REJECTED_FOR_FORBIDDEN_CAPABILITY": (
            "remove forbidden capability requests",
            "restart from local/dev-only fixture execution constraints",
        ),
        "LOCAL_BROWSER_SANDBOX_SPEC_BLOCKED_BY_STEWARD": (
            "halt local browser execution planning until Steward/VZ unblocks",
        ),
    }[verdict]

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _stable_id(prefix: str, *parts: str) -> str:
    return f"{prefix}-{hashlib.sha256(chr(10).join(parts).encode('utf-8')).hexdigest()[:16]}"

def _json(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _json(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_json(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _json(v) for k, v in value.items()}
    return value

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emit a V51 local browser execution sandbox specification receipt.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--request", default=None)
    parser.add_argument("--scenario", choices=("accepted", "remediate", "forbidden", "blocked"), default="accepted")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    request = load_local_browser_execution_sandbox_spec_request(args.workspace_root, args.request) if args.request else _scenario(args.scenario)
    receipt = build_local_browser_execution_sandbox_spec_receipt(request=request, emitted_at="2026-04-25T07:10:00+00:00")
    if args.write:
        print(write_local_browser_execution_sandbox_spec_receipt(args.workspace_root, receipt).as_posix())
    if args.json:
        print(json.dumps(_json(receipt), indent=2, sort_keys=True))
    else:
        print(f"verdict={receipt.spec_verdict} authority={receipt.authority_scope} execution_authorized={receipt.browser_execution_authorized}")
    errors = validate_local_browser_execution_sandbox_spec_receipt(receipt)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 4
    if receipt.spec_verdict.endswith("BLOCKED_BY_STEWARD") or receipt.spec_verdict.endswith("REJECTED_FOR_FORBIDDEN_CAPABILITY"):
        return 3
    if receipt.spec_verdict.endswith("NEEDS_REMEDIATION"):
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
