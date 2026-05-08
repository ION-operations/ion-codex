"""V53 fixture-bound local browser execution run receipts.

Records gated local/dev browser harness run outcomes and failure taxonomy.
It does not authorize broad browser control, network, credentials, submissions,
persistent mutation, or production authority.
"""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
SCHEMA_ID="ion.local_browser_execution_run_receipt.v1"; VERSION="V53_LOCAL_BROWSER_EXECUTION_RUN_RECEIPTS"; AUTHORITY_SCOPE="LOCAL_DEV_BROWSER_EXECUTION_RUN_RECEIPT_ONLY"; DEFAULT_REPORT_DIR="ION/05_context/history/local_browser_execution_run_receipts"
PASSING_OUTCOMES=("CAPTURE_SUCCEEDED","FIXTURE_PASSED","VISUAL_REPAIR_VERIFIED","NO_VISUAL_REGRESSION_DETECTED")
REVIEW_OUTCOMES=("CAPTURE_PARTIAL","FIXTURE_NEEDS_REVIEW","VISUAL_CHANGE_REQUIRES_REVIEW","CONSOLE_WARNING_REVIEW","NOT_EXECUTED")
FAILING_OUTCOMES=("CAPTURE_FAILED","FIXTURE_FAILED","VISUAL_REGRESSION_DETECTED","CONSOLE_ERROR","HARNESS_ERROR")
FORBIDDEN_OUTCOMES=("EXTERNAL_NETWORK_OBSERVED","CREDENTIAL_OR_SESSION_IMPORT_OBSERVED","SUBMIT_OR_ACCOUNT_ACTION_OBSERVED","PERSISTENT_MUTATION_OBSERVED","UNCONSTRAINED_WRITES_OBSERVED")
FAILURE_TAXONOMY=("NONE","CAPTURE_TIMEOUT","DOM_CAPTURE_FAILED","SCREENSHOT_CAPTURE_FAILED","ACCESSIBILITY_CAPTURE_FAILED","CONSOLE_ERROR","VISUAL_DIAGNOSIS_FAILED","VISUAL_REGRESSION_DETECTED","HARNESS_ERROR","FORBIDDEN_NETWORK_EVENT","FORBIDDEN_CREDENTIAL_EVENT","FORBIDDEN_SUBMIT_OR_ACCOUNT_EVENT","FORBIDDEN_PERSISTENT_MUTATION_EVENT","FORBIDDEN_FILE_WRITE_EVENT","STEWARD_BLOCKED")
FORBIDDEN_CAPABILITIES={"unrestricted_browser_control":False,"external_network_access":False,"credential_or_session_import":False,"account_operation":False,"destructive_action":False,"form_submission":False,"purchase_or_submission":False,"persistent_dom_mutation":False,"unconstrained_file_write":False,"production_visual_automation":False,"production_authority":False}
@dataclass(frozen=True)
class BrowserFixtureRunEvent:
    fixture_id:str; target:str; outcome:str="NOT_EXECUTED"; failure_code:str="NONE"; observation_packet_ids:tuple[str,...]=(); diagnosis_receipt_ids:tuple[str,...]=(); before_after_verification_ids:tuple[str,...]=(); capture_artifact_refs:tuple[str,...]=(); console_summary:str|None=None; review_notes:tuple[str,...]=()
@dataclass(frozen=True)
class BrowserFixtureRunResult:
    fixture_id:str; target:str; outcome:str; failure_code:str; result:str; review_required:bool; notes:tuple[str,...]
@dataclass(frozen=True)
class LocalBrowserExecutionRunRequest:
    run_name:str; harness_receipt_ids:tuple[str,...]=(); sandbox_spec_receipt_ids:tuple[str,...]=(); fixture_manifest_refs:tuple[str,...]=(); run_mode:str="DRY_RUN"; target_origin_policy:str="LOCAL_FILES_OR_LOOPBACK_ONLY"; steward_gate_status:str="APPROVED_GATED_RUN"; network_observation:str="NO_EXTERNAL_NETWORK_OBSERVED"; credential_observation:str="NO_CREDENTIALS_OR_SESSION_IMPORT_OBSERVED"; action_observation:str="READ_ONLY_CAPTURE_ACTIONS_ONLY"; mutation_observation:str="NO_PERSISTENT_MUTATION_OBSERVED"; artifact_write_observation:str="RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY"; fixture_events:tuple[BrowserFixtureRunEvent,...]=(); workspace_artifact_refs:tuple[str,...]=(); requested_capabilities:dict[str,bool]=field(default_factory=dict); review_notes:tuple[str,...]=()
@dataclass(frozen=True)
class LocalBrowserExecutionRunReceipt:
    schema_id:str; version:str; run_id:str; emitted_at:str; run_name:str; authority_scope:str; steward_gate_status:str; run_mode:str; target_origin_policy:str; harness_receipt_ids:tuple[str,...]; sandbox_spec_receipt_ids:tuple[str,...]; fixture_manifest_refs:tuple[str,...]; network_observation:str; credential_observation:str; action_observation:str; mutation_observation:str; artifact_write_observation:str; fixture_count:int; passed_count:int; review_count:int; failed_count:int; forbidden_count:int; blocked_count:int; fixture_results:tuple[BrowserFixtureRunResult,...]; workspace_artifact_refs:tuple[str,...]; artifact_hashes:dict[str,str]; run_findings:tuple[str,...]; run_verdict:str; recommended_next_actions:tuple[str,...]; gated_local_run_receipted:bool=False; live_browser_execution_authorized:bool=False; external_network_authorized:bool=False; credential_access_authorized:bool=False; submit_or_account_action_authorized:bool=False; persistent_dom_mutation_authorized:bool=False; production_authority:bool=False; forbidden_capabilities:dict[str,bool]=field(default_factory=lambda:dict(FORBIDDEN_CAPABILITIES))
def build_local_browser_execution_run_receipt(*, request:LocalBrowserExecutionRunRequest, workspace_root:str|Path|None=None, emitted_at:str|None=None)->LocalBrowserExecutionRunReceipt:
    _validate_request(request); findings=list(request.review_notes); blocked=request.run_mode=="BLOCKED" or request.steward_gate_status=="BLOCKED"
    forbidden_requested=tuple(k for k,v in request.requested_capabilities.items() if v and k in FORBIDDEN_CAPABILITIES)
    if forbidden_requested: findings.append('requested forbidden capabilities: '+', '.join(sorted(forbidden_requested)))
    if not request.harness_receipt_ids: findings.append('no V52 local browser execution harness receipt lineage provided')
    if not request.sandbox_spec_receipt_ids: findings.append('no V51 sandbox specification receipt lineage provided')
    if not request.fixture_manifest_refs: findings.append('no fixture manifest references provided')
    if request.steward_gate_status=='STEWARD_REVIEW_REQUIRED': findings.append('Steward/VZ review required before run receipt can close')
    if request.network_observation in ('EXTERNAL_NETWORK_OBSERVED','UNKNOWN'): findings.append(('forbidden network observation recorded: ' if request.network_observation == 'EXTERNAL_NETWORK_OBSERVED' else 'unknown network observation requires review: ')+request.network_observation)
    if request.credential_observation in ('CREDENTIAL_OR_SESSION_IMPORT_OBSERVED','UNKNOWN'): findings.append(('forbidden credential observation recorded: ' if request.credential_observation == 'CREDENTIAL_OR_SESSION_IMPORT_OBSERVED' else 'unknown credential observation requires review: ')+request.credential_observation)
    if request.action_observation in ('SUBMIT_OR_ACCOUNT_ACTION_OBSERVED','UNKNOWN'): findings.append(('forbidden action observation recorded: ' if request.action_observation == 'SUBMIT_OR_ACCOUNT_ACTION_OBSERVED' else 'unknown action observation requires review: ')+request.action_observation)
    if request.mutation_observation in ('PERSISTENT_MUTATION_OBSERVED','UNKNOWN'): findings.append(('forbidden mutation observation recorded: ' if request.mutation_observation == 'PERSISTENT_MUTATION_OBSERVED' else 'unknown mutation observation requires review: ')+request.mutation_observation)
    if request.artifact_write_observation in ('UNCONSTRAINED_WRITES_OBSERVED','UNKNOWN'): findings.append(('forbidden artifact write observation recorded: ' if request.artifact_write_observation == 'UNCONSTRAINED_WRITES_OBSERVED' else 'unknown artifact write observation requires review: ')+request.artifact_write_observation)
    results=tuple(_classify_event(e, blocked) for e in request.fixture_events); passed=sum(r.result=='PASS' for r in results); review=sum(r.review_required and r.result not in ('BLOCKED','FORBIDDEN_REJECTED') for r in results); failed=sum(r.result=='FAIL_REQUIRES_REVIEW' for r in results); forbidden=sum(r.result=='FORBIDDEN_REJECTED' for r in results); blocked_count=sum(r.result=='BLOCKED' for r in results)
    if not results: findings.append('no fixture run events recorded')
    hashes={}
    if workspace_root:
        root=Path(workspace_root).resolve()
        for ref in request.workspace_artifact_refs:
            p=_inside(root, ref)
            if p.is_file(): hashes[str(ref)]=hashlib.sha256(p.read_bytes()).hexdigest()
            else: findings.append(f'workspace artifact missing or not a file: {ref}')
    verdict=_run_verdict(blocked, forbidden_requested, findings, bool(results), review, failed, forbidden, blocked_count); accepted=verdict=='LOCAL_BROWSER_EXECUTION_RUN_RECEIPT_ACCEPTED'
    if accepted: findings.append('fixture-bound local/dev browser run receipted; no external network, credentials, submissions, persistent mutation, or production authority granted')
    ts=emitted_at or _utc_now(); rid=_stable_id('v53-local-browser-execution-run', ts, request.run_name, verdict, str(len(results)))
    return LocalBrowserExecutionRunReceipt(SCHEMA_ID, VERSION, rid, ts, request.run_name, AUTHORITY_SCOPE, request.steward_gate_status, request.run_mode, request.target_origin_policy, request.harness_receipt_ids, request.sandbox_spec_receipt_ids, request.fixture_manifest_refs, request.network_observation, request.credential_observation, request.action_observation, request.mutation_observation, request.artifact_write_observation, len(results), passed, review, failed, forbidden, blocked_count, results, request.workspace_artifact_refs, hashes, tuple(findings), verdict, _actions(verdict), gated_local_run_receipted=accepted)
def _classify_event(e, blocked):
    _validate_event(e)
    if blocked: return BrowserFixtureRunResult(e.fixture_id,e.target,e.outcome,'STEWARD_BLOCKED','BLOCKED',True,('run blocked by Steward/VZ gate',))
    notes=list(e.review_notes)
    if e.outcome in FORBIDDEN_OUTCOMES or e.failure_code.startswith('FORBIDDEN_'): return BrowserFixtureRunResult(e.fixture_id,e.target,e.outcome,e.failure_code,'FORBIDDEN_REJECTED',True,tuple(notes+['forbidden event observed during local browser run']))
    if e.failure_code!='NONE' or e.outcome in FAILING_OUTCOMES: return BrowserFixtureRunResult(e.fixture_id,e.target,e.outcome,e.failure_code,'FAIL_REQUIRES_REVIEW',True,tuple(notes or ('failure taxonomy requires review',)))
    if e.outcome in REVIEW_OUTCOMES: return BrowserFixtureRunResult(e.fixture_id,e.target,e.outcome,e.failure_code,'NEEDS_REVIEW',True,tuple(notes or ('run outcome requires review before closure',)))
    if e.outcome in PASSING_OUTCOMES: return BrowserFixtureRunResult(e.fixture_id,e.target,e.outcome,e.failure_code,'PASS',False,tuple(notes or ('fixture run passed under local/dev receipt boundary',)))
    return BrowserFixtureRunResult(e.fixture_id,e.target,e.outcome,e.failure_code,'NEEDS_REVIEW',True,tuple(notes or ('unrecognized outcome requires review',)))
def _run_verdict(blocked, forbidden_requested, findings, has_results, review, failed, forbidden, blocked_count):
    if blocked or blocked_count: return 'LOCAL_BROWSER_EXECUTION_RUN_BLOCKED_BY_STEWARD'
    if forbidden_requested or forbidden or any('forbidden' in f.lower() for f in findings): return 'LOCAL_BROWSER_EXECUTION_RUN_REJECTED_FOR_FORBIDDEN_EVENT'
    if failed: return 'LOCAL_BROWSER_EXECUTION_RUN_FAILED_REQUIRES_REVIEW'
    if review or findings or not has_results: return 'LOCAL_BROWSER_EXECUTION_RUN_NEEDS_REVIEW'
    return 'LOCAL_BROWSER_EXECUTION_RUN_RECEIPT_ACCEPTED'
def validate_local_browser_execution_run_receipt(r):
    errors=[]
    if r.schema_id!=SCHEMA_ID: errors.append('schema_id mismatch')
    if r.version!=VERSION: errors.append('version mismatch')
    if r.authority_scope!=AUTHORITY_SCOPE: errors.append('authority scope mismatch')
    if r.live_browser_execution_authorized or r.external_network_authorized or r.credential_access_authorized or r.submit_or_account_action_authorized or r.persistent_dom_mutation_authorized or r.production_authority: errors.append('forbidden authority flag must be false')
    if any(r.forbidden_capabilities.values()): errors.append('forbidden capabilities must all remain false')
    if r.fixture_count != len(r.fixture_results): errors.append('fixture_count mismatch')
    if r.run_verdict=='LOCAL_BROWSER_EXECUTION_RUN_RECEIPT_ACCEPTED' and (not r.gated_local_run_receipted or r.failed_count or r.review_count or r.forbidden_count or r.blocked_count): errors.append('accepted run must be closed and clean')
    if r.run_verdict!='LOCAL_BROWSER_EXECUTION_RUN_RECEIPT_ACCEPTED' and r.gated_local_run_receipted: errors.append('non-accepted run must not be receipted as closed')
    return tuple(errors)
def load_local_browser_execution_run_request(workspace_root, request_path): root=Path(workspace_root).resolve(); return request_from_mapping(json.loads(_inside(root, request_path).read_text(encoding='utf-8')))
def request_from_mapping(data:Mapping[str,Any]):
    def tup(n,default=()):
        v=data.get(n,default)
        if v is None: return ()
        if isinstance(v,str): return (v,)
        return tuple(str(x) for x in v)
    return LocalBrowserExecutionRunRequest(str(data.get('run_name') or 'local browser execution run'), tup('harness_receipt_ids'), tup('sandbox_spec_receipt_ids'), tup('fixture_manifest_refs'), str(data.get('run_mode') or 'DRY_RUN'), str(data.get('target_origin_policy') or 'LOCAL_FILES_OR_LOOPBACK_ONLY'), str(data.get('steward_gate_status') or 'APPROVED_GATED_RUN'), str(data.get('network_observation') or 'NO_EXTERNAL_NETWORK_OBSERVED'), str(data.get('credential_observation') or 'NO_CREDENTIALS_OR_SESSION_IMPORT_OBSERVED'), str(data.get('action_observation') or 'READ_ONLY_CAPTURE_ACTIONS_ONLY'), str(data.get('mutation_observation') or 'NO_PERSISTENT_MUTATION_OBSERVED'), str(data.get('artifact_write_observation') or 'RECEIPTS_AND_CAPTURE_ARTIFACTS_ONLY'), tuple(event_from_mapping(x) for x in data.get('fixture_events',())), tup('workspace_artifact_refs'), {str(k):bool(v) for k,v in (data.get('requested_capabilities') or {}).items()}, tup('review_notes'))
def event_from_mapping(data): return BrowserFixtureRunEvent(str(data.get('fixture_id') or data.get('id') or 'fixture'), str(data.get('target') or 'unspecified target'), str(data.get('outcome') or 'NOT_EXECUTED'), str(data.get('failure_code') or 'NONE'))
def write_local_browser_execution_run_receipt(workspace_root, receipt, *, report_dir=DEFAULT_REPORT_DIR): out=Path(workspace_root).resolve()/report_dir; out.mkdir(parents=True, exist_ok=True); p=out/f'{receipt.run_id}.local_browser_execution_run_receipt.json'; p.write_text(json.dumps(_json(receipt),indent=2,sort_keys=True)+'\n',encoding='utf-8'); return p
def _validate_request(r):
    if r.steward_gate_status not in ('APPROVED_GATED_RUN','STEWARD_REVIEW_REQUIRED','BLOCKED'): raise ValueError('invalid steward_gate_status: '+r.steward_gate_status)
    if r.run_mode not in ('DRY_RUN','STATIC_LOCAL_CAPTURE','LOOPBACK_CAPTURE','BLOCKED'): raise ValueError('invalid run_mode: '+r.run_mode)
    for e in r.fixture_events: _validate_event(e)
def _validate_event(e):
    if e.outcome not in PASSING_OUTCOMES+REVIEW_OUTCOMES+FAILING_OUTCOMES+FORBIDDEN_OUTCOMES: raise ValueError(f'invalid outcome for {e.fixture_id}: {e.outcome}')
    if e.failure_code not in FAILURE_TAXONOMY: raise ValueError(f'invalid failure code for {e.fixture_id}: {e.failure_code}')
def _actions(v):
    return {'LOCAL_BROWSER_EXECUTION_RUN_RECEIPT_ACCEPTED':('attach run receipt to visual diagnosis and before/after verification chain',),'LOCAL_BROWSER_EXECUTION_RUN_NEEDS_REVIEW':('repair missing lineage, unknown observations, or review-requiring fixture outcomes',),'LOCAL_BROWSER_EXECUTION_RUN_FAILED_REQUIRES_REVIEW':('route failure taxonomy to implementation and Steward/VZ review',),'LOCAL_BROWSER_EXECUTION_RUN_REJECTED_FOR_FORBIDDEN_EVENT':('halt run lineage and route to Steward/VZ security review',),'LOCAL_BROWSER_EXECUTION_RUN_BLOCKED_BY_STEWARD':('obtain explicit Steward/VZ unblock before successor work',)}.get(v,('request Steward/VZ review',))
def _scenario(n):
    base=dict(run_name='V53 fixture-bound local browser run', harness_receipt_ids=('v52-harness',), sandbox_spec_receipt_ids=('v51-spec',), fixture_manifest_refs=('fixtures/local.json',))
    if n=='accepted': return LocalBrowserExecutionRunRequest(**base, fixture_events=(BrowserFixtureRunEvent('panel','local preview','FIXTURE_PASSED'),))
    if n=='review': return LocalBrowserExecutionRunRequest(**base, network_observation='UNKNOWN', fixture_events=(BrowserFixtureRunEvent('panel','local preview','CAPTURE_PARTIAL'),))
    if n=='failed': return LocalBrowserExecutionRunRequest(**base, fixture_events=(BrowserFixtureRunEvent('scroll','local preview','VISUAL_REGRESSION_DETECTED','VISUAL_REGRESSION_DETECTED'),))
    if n=='forbidden': return LocalBrowserExecutionRunRequest(**base, network_observation='EXTERNAL_NETWORK_OBSERVED', fixture_events=(BrowserFixtureRunEvent('unsafe','local preview','EXTERNAL_NETWORK_OBSERVED','FORBIDDEN_NETWORK_EVENT'),))
    if n=='blocked': return LocalBrowserExecutionRunRequest(**base, steward_gate_status='BLOCKED', fixture_events=(BrowserFixtureRunEvent('blocked','local preview','FIXTURE_PASSED'),))
    raise ValueError(n)
def _inside(root,value):
    p=Path(value); c=p.resolve() if p.is_absolute() else (root/p).resolve()
    if c!=root and root not in c.parents: raise ValueError(f'path escapes workspace root: {value}')
    return c
def _utc_now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def _stable_id(prefix,*parts): return prefix+'-'+hashlib.sha256('\n'.join(parts).encode()).hexdigest()[:16]
def _json(v):
    if hasattr(v,'__dataclass_fields__'): return {k:_json(x) for k,x in asdict(v).items()}
    if isinstance(v,tuple): return [_json(x) for x in v]
    if isinstance(v,dict): return {str(k):_json(x) for k,x in v.items()}
    return v
def main(argv:Sequence[str]|None=None):
    p=argparse.ArgumentParser(); p.add_argument('--workspace-root',default='.'); p.add_argument('--request'); p.add_argument('--scenario',choices=('accepted','review','failed','forbidden','blocked'),default='accepted'); p.add_argument('--write',action='store_true'); p.add_argument('--json',action='store_true'); a=p.parse_args(argv)
    req=load_local_browser_execution_run_request(a.workspace_root,a.request) if a.request else _scenario(a.scenario)
    rec=build_local_browser_execution_run_receipt(request=req, workspace_root=a.workspace_root, emitted_at='2026-04-25T07:53:00+00:00')
    if a.write: print(write_local_browser_execution_run_receipt(a.workspace_root, rec).as_posix())
    print(json.dumps(_json(rec),indent=2,sort_keys=True) if a.json else f'verdict={rec.run_verdict} authority={rec.authority_scope} accepted={rec.gated_local_run_receipted}')
    errs=validate_local_browser_execution_run_receipt(rec)
    if errs: print('\n'.join('ERROR: '+e for e in errs)); return 4
    if rec.run_verdict in ('LOCAL_BROWSER_EXECUTION_RUN_BLOCKED_BY_STEWARD','LOCAL_BROWSER_EXECUTION_RUN_REJECTED_FOR_FORBIDDEN_EVENT'): return 3
    if rec.run_verdict in ('LOCAL_BROWSER_EXECUTION_RUN_NEEDS_REVIEW','LOCAL_BROWSER_EXECUTION_RUN_FAILED_REQUIRES_REVIEW'): return 2
    return 0
if __name__=='__main__': raise SystemExit(main())
