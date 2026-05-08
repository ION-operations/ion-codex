"""V52 gated local browser execution harness prototype.

This is a policy/receipt surface only. It validates a proposed local/dev harness
posture; it does not run a browser or grant unrestricted control.
"""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.local_browser_execution_harness.v1"
VERSION = "V52_LOCAL_BROWSER_EXECUTION_HARNESS_PROTOTYPE_GATED"
AUTHORITY_SCOPE = "LOCAL_DEV_BROWSER_EXECUTION_HARNESS_GATED_PROTOTYPE"
DEFAULT_REPORT_DIR = "ION/05_context/history/local_browser_execution_harness_receipts"
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
REQUIRED_CONTROLS = (
    "steward_gate_required", "fixture_manifest_required", "local_or_loopback_targets_only",
    "no_external_network", "no_credentials_or_session_import", "no_submit_or_account_actions",
    "no_persistent_dom_mutation", "capture_artifact_hashing", "receipt_required",
)
ENUMS = {
    "execution_mode": ("DRY_RUN_ONLY", "STATIC_LOCAL_ARTIFACT_CAPTURE", "LOOPBACK_CAPTURE_PLAN_ONLY", "STEWARD_REVIEW_REQUIRED", "BLOCKED"),
    "target_origin_policy": ("LOCAL_FILES_OR_LOOPBACK_ONLY", "LOOPBACK_ONLY", "LOCAL_FILES_ONLY", "UNREVIEWED", "BLOCKED"),
    "network_policy": ("NO_EXTERNAL_NETWORK", "NO_NETWORK", "UNREVIEWED", "BLOCKED"),
    "credential_policy": ("NO_CREDENTIALS_OR_SESSION_IMPORT", "SANITIZED_TEST_FIXTURES_ONLY", "UNREVIEWED", "BLOCKED"),
    "navigation_policy": ("FIXTURE_MANIFEST_ONLY", "SINGLE_URL_ALLOWLIST_ONLY", "UNREVIEWED", "BLOCKED"),
    "mutation_policy": ("NO_PERSISTENT_MUTATION", "TEMPORARY_TEST_INSTRUMENTATION_ONLY", "UNREVIEWED", "BLOCKED"),
    "action_policy": ("NO_SUBMIT_OR_ACCOUNT_ACTIONS", "READ_ONLY_CAPTURE_ACTIONS_ONLY", "UNREVIEWED", "BLOCKED"),
    "file_write_policy": ("RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY", "RECEIPTS_ONLY", "UNREVIEWED", "BLOCKED"),
    "steward_gate_status": ("APPROVED_GATED_PROTOTYPE", "STEWARD_REVIEW_REQUIRED", "BLOCKED"),
}

@dataclass(frozen=True)
class LocalBrowserExecutionHarnessRequest:
    harness_name: str
    sandbox_spec_receipt_ids: tuple[str, ...] = ()
    fixture_manifest_refs: tuple[str, ...] = ()
    lineage_refs: tuple[str, ...] = ()
    execution_mode: str = "DRY_RUN_ONLY"
    target_origin_policy: str = "LOCAL_FILES_OR_LOOPBACK_ONLY"
    network_policy: str = "NO_EXTERNAL_NETWORK"
    credential_policy: str = "NO_CREDENTIALS_OR_SESSION_IMPORT"
    navigation_policy: str = "FIXTURE_MANIFEST_ONLY"
    mutation_policy: str = "NO_PERSISTENT_MUTATION"
    action_policy: str = "NO_SUBMIT_OR_ACCOUNT_ACTIONS"
    file_write_policy: str = "RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY"
    steward_gate_status: str = "APPROVED_GATED_PROTOTYPE"
    required_controls: tuple[str, ...] = REQUIRED_CONTROLS
    workspace_artifact_refs: tuple[str, ...] = ()
    requested_capabilities: dict[str, bool] = field(default_factory=dict)
    review_notes: tuple[str, ...] = ()

@dataclass(frozen=True)
class LocalBrowserExecutionHarnessReceipt:
    schema_id: str
    version: str
    harness_id: str
    emitted_at: str
    harness_name: str
    authority_scope: str
    harness_verdict: str
    sandbox_spec_receipt_ids: tuple[str, ...]
    fixture_manifest_refs: tuple[str, ...]
    execution_mode: str
    target_origin_policy: str
    network_policy: str
    credential_policy: str
    navigation_policy: str
    mutation_policy: str
    action_policy: str
    file_write_policy: str
    steward_gate_status: str
    required_controls: tuple[str, ...]
    workspace_artifact_refs: tuple[str, ...]
    artifact_hashes: dict[str, str]
    review_findings: tuple[str, ...]
    recommended_next_actions: tuple[str, ...]
    gated_local_execution_prototype_authorized: bool = False
    live_browser_execution_authorized: bool = False
    external_network_authorized: bool = False
    credential_access_authorized: bool = False
    persistent_dom_mutation_authorized: bool = False
    production_authority: bool = False
    forbidden_capabilities: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CAPABILITIES))

def build_local_browser_execution_harness_receipt(*, request: LocalBrowserExecutionHarnessRequest, workspace_root: str | Path | None = None, emitted_at: str | None = None) -> LocalBrowserExecutionHarnessReceipt:
    _validate(request)
    findings = list(request.review_notes)
    forbidden = tuple(k for k, v in request.requested_capabilities.items() if v and k in FORBIDDEN_CAPABILITIES)
    if forbidden: findings.append("requested forbidden capabilities: " + ", ".join(sorted(forbidden)))
    if not request.sandbox_spec_receipt_ids: findings.append("no V51 sandbox specification receipt lineage provided")
    if not request.fixture_manifest_refs: findings.append("no fixture manifest references provided")
    if request.steward_gate_status == "STEWARD_REVIEW_REQUIRED": findings.append("Steward/VZ review required before gated local harness prototype use")
    if request.execution_mode not in ("DRY_RUN_ONLY", "STATIC_LOCAL_ARTIFACT_CAPTURE", "LOOPBACK_CAPTURE_PLAN_ONLY"): findings.append("execution mode is not within gated local prototype modes")
    if request.network_policy not in ("NO_EXTERNAL_NETWORK", "NO_NETWORK"): findings.append("network policy is not restricted against external network access")
    if request.credential_policy != "NO_CREDENTIALS_OR_SESSION_IMPORT": findings.append("credential policy permits or has not ruled out credential/session import")
    if request.action_policy not in ("NO_SUBMIT_OR_ACCOUNT_ACTIONS", "READ_ONLY_CAPTURE_ACTIONS_ONLY"): findings.append("action policy does not forbid submit/account actions")
    if request.mutation_policy not in ("NO_PERSISTENT_MUTATION", "TEMPORARY_TEST_INSTRUMENTATION_ONLY"): findings.append("mutation policy is not constrained against persistent mutation")
    missing = tuple(c for c in REQUIRED_CONTROLS if c not in request.required_controls)
    if missing: findings.append("missing required controls: " + ", ".join(missing))
    hashes = {}
    if workspace_root:
        root = Path(workspace_root).resolve()
        for ref in request.workspace_artifact_refs:
            p = _inside(root, ref)
            if p.is_file(): hashes[str(ref)] = hashlib.sha256(p.read_bytes()).hexdigest()
            else: findings.append(f"workspace artifact missing or not a file: {ref}")
    if request.steward_gate_status == "BLOCKED" or request.execution_mode == "BLOCKED": verdict = "LOCAL_BROWSER_HARNESS_BLOCKED_BY_STEWARD"
    elif forbidden: verdict = "LOCAL_BROWSER_HARNESS_REJECTED_FOR_FORBIDDEN_CAPABILITY"
    elif findings: verdict = "LOCAL_BROWSER_HARNESS_NEEDS_REVIEW"
    else:
        verdict = "LOCAL_BROWSER_HARNESS_GATED_PROTOTYPE_READY"
        findings.append("gated local/dev harness prototype accepted; no external network, credentials, submissions, persistent DOM mutation, or production authority granted")
    ts = emitted_at or _utc_now(); accepted = verdict == "LOCAL_BROWSER_HARNESS_GATED_PROTOTYPE_READY"
    return LocalBrowserExecutionHarnessReceipt(SCHEMA_ID, VERSION, _stable_id('v52-local-browser-execution-harness', ts, request.harness_name, verdict), ts, request.harness_name, AUTHORITY_SCOPE, verdict, request.sandbox_spec_receipt_ids, request.fixture_manifest_refs, request.execution_mode, request.target_origin_policy, request.network_policy, request.credential_policy, request.navigation_policy, request.mutation_policy, request.action_policy, request.file_write_policy, request.steward_gate_status, request.required_controls, request.workspace_artifact_refs, hashes, tuple(findings), _actions(verdict), gated_local_execution_prototype_authorized=accepted)

def validate_local_browser_execution_harness_receipt(receipt: LocalBrowserExecutionHarnessReceipt) -> tuple[str, ...]:
    errors=[]
    if receipt.schema_id != SCHEMA_ID: errors.append('schema_id mismatch')
    if receipt.version != VERSION: errors.append('version mismatch')
    if receipt.authority_scope != AUTHORITY_SCOPE: errors.append('authority scope mismatch')
    if receipt.live_browser_execution_authorized or receipt.external_network_authorized or receipt.credential_access_authorized or receipt.persistent_dom_mutation_authorized or receipt.production_authority: errors.append('forbidden authority flag must be false')
    if any(receipt.forbidden_capabilities.values()): errors.append('forbidden capabilities must all remain false')
    if receipt.harness_verdict == 'LOCAL_BROWSER_HARNESS_GATED_PROTOTYPE_READY' and not receipt.gated_local_execution_prototype_authorized: errors.append('accepted harness must authorize gated prototype')
    if receipt.harness_verdict != 'LOCAL_BROWSER_HARNESS_GATED_PROTOTYPE_READY' and receipt.gated_local_execution_prototype_authorized: errors.append('non-accepted harness must not authorize gated prototype')
    return tuple(errors)

def load_local_browser_execution_harness_request(workspace_root: str | Path, request_path: str | Path) -> LocalBrowserExecutionHarnessRequest:
    root=Path(workspace_root).resolve(); p=_inside(root, request_path); return request_from_mapping(json.loads(p.read_text(encoding='utf-8')))
def request_from_mapping(data: Mapping[str, Any]) -> LocalBrowserExecutionHarnessRequest:
    def tup(n, default=()):
        v=data.get(n, default)
        if v is None: return ()
        if isinstance(v, str): return (v,)
        return tuple(str(x) for x in v)
    return LocalBrowserExecutionHarnessRequest(str(data.get('harness_name') or 'local browser execution harness prototype'), tup('sandbox_spec_receipt_ids'), tup('fixture_manifest_refs'), tup('lineage_refs'), str(data.get('execution_mode') or 'DRY_RUN_ONLY'), str(data.get('target_origin_policy') or 'LOCAL_FILES_OR_LOOPBACK_ONLY'), str(data.get('network_policy') or 'NO_EXTERNAL_NETWORK'), str(data.get('credential_policy') or 'NO_CREDENTIALS_OR_SESSION_IMPORT'), str(data.get('navigation_policy') or 'FIXTURE_MANIFEST_ONLY'), str(data.get('mutation_policy') or 'NO_PERSISTENT_MUTATION'), str(data.get('action_policy') or 'NO_SUBMIT_OR_ACCOUNT_ACTIONS'), str(data.get('file_write_policy') or 'RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY'), str(data.get('steward_gate_status') or 'APPROVED_GATED_PROTOTYPE'), tup('required_controls', REQUIRED_CONTROLS), tup('workspace_artifact_refs'), {str(k): bool(v) for k,v in (data.get('requested_capabilities') or {}).items()}, tup('review_notes'))
def write_local_browser_execution_harness_receipt(workspace_root: str | Path, receipt: LocalBrowserExecutionHarnessReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    out=Path(workspace_root).resolve()/report_dir; out.mkdir(parents=True, exist_ok=True); p=out/f"{receipt.harness_id}.local_browser_execution_harness_receipt.json"; p.write_text(json.dumps(_json(receipt), indent=2, sort_keys=True)+'\n', encoding='utf-8'); return p
def _validate(request):
    for name, allowed in ENUMS.items():
        val=getattr(request, name)
        if val not in allowed: raise ValueError(f'invalid {name}: {val}')
def _inside(root, value):
    p=Path(value); c=p.resolve() if p.is_absolute() else (root/p).resolve()
    if c != root and root not in c.parents: raise ValueError(f'path escapes workspace root: {value}')
    return c
def _actions(verdict):
    if verdict == 'LOCAL_BROWSER_HARNESS_GATED_PROTOTYPE_READY': return ('write run receipts for every fixture-bound run', 'continue toward V53 only under no-network/credential/submission boundaries')
    if verdict == 'LOCAL_BROWSER_HARNESS_NEEDS_REVIEW': return ('repair underconstrained harness policies', 'repeat Steward/VZ review')
    if verdict == 'LOCAL_BROWSER_HARNESS_REJECTED_FOR_FORBIDDEN_CAPABILITY': return ('remove forbidden capabilities', 'do not run harness')
    return ('do not run harness', 'obtain Steward/VZ unblock')
def _scenario(name):
    if name=='ready': return LocalBrowserExecutionHarnessRequest('V52 ready', ('v51-spec',), ('fixtures/local.json',))
    if name=='review': return LocalBrowserExecutionHarnessRequest('V52 review', (), (), network_policy='UNREVIEWED', steward_gate_status='STEWARD_REVIEW_REQUIRED')
    if name=='forbidden': return LocalBrowserExecutionHarnessRequest('V52 forbidden', ('v51-spec',), ('fixtures/local.json',), requested_capabilities={'external_network_access': True})
    if name=='blocked': return LocalBrowserExecutionHarnessRequest('V52 blocked', ('v51-spec',), ('fixtures/local.json',), steward_gate_status='BLOCKED')
    raise ValueError(name)
def _utc_now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def _stable_id(prefix, *parts): return prefix+'-'+hashlib.sha256('\n'.join(parts).encode()).hexdigest()[:16]
def _json(v):
    if hasattr(v, '__dataclass_fields__'): return {k:_json(x) for k,x in asdict(v).items()}
    if isinstance(v, tuple): return [_json(x) for x in v]
    if isinstance(v, dict): return {str(k):_json(x) for k,x in v.items()}
    return v
def main(argv: Sequence[str] | None = None):
    p=argparse.ArgumentParser(); p.add_argument('--workspace-root', default='.'); p.add_argument('--request'); p.add_argument('--scenario', choices=('ready','review','forbidden','blocked'), default='ready'); p.add_argument('--write', action='store_true'); p.add_argument('--json', action='store_true'); a=p.parse_args(argv)
    req=load_local_browser_execution_harness_request(a.workspace_root, a.request) if a.request else _scenario(a.scenario)
    rec=build_local_browser_execution_harness_receipt(request=req, workspace_root=a.workspace_root, emitted_at='2026-04-25T07:20:00+00:00')
    if a.write: print(write_local_browser_execution_harness_receipt(a.workspace_root, rec).as_posix())
    print(json.dumps(_json(rec), indent=2, sort_keys=True) if a.json else f'verdict={rec.harness_verdict} authority={rec.authority_scope} gated={rec.gated_local_execution_prototype_authorized}')
    errs=validate_local_browser_execution_harness_receipt(rec)
    if errs: print('\n'.join('ERROR: '+e for e in errs)); return 4
    if rec.harness_verdict.endswith('BLOCKED_BY_STEWARD') or rec.harness_verdict.endswith('REJECTED_FOR_FORBIDDEN_CAPABILITY'): return 3
    if rec.harness_verdict.endswith('NEEDS_REVIEW'): return 2
    return 0
if __name__ == '__main__': raise SystemExit(main())
