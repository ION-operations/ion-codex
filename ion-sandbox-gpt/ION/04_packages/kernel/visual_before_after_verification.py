"""V48 visual before/after verification loop."""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence
SCHEMA_ID='ion.visual_before_after_verification.v1'; VERSION='V48_VISUAL_BEFORE_AFTER_VERIFICATION_LOOP'; DEFAULT_REPORT_DIR='ION/05_context/history/visual_before_after_verification_receipts'
ALLOWED_VERIFICATION_MODES=('DIAGNOSTIC_COMPARISON_ONLY','LOCAL_ARTIFACT_HASH_COMPARISON','EVIDENCE_REFERENCE_COMPARISON','STEWARD_REVIEW_REQUIRED'); STEWARD_GATE_STATUSES=('APPROVED_VERIFY_ONLY','STEWARD_REVIEW_REQUIRED','BLOCKED'); CONFIDENCE_LEVELS=('LOW','MEDIUM','HIGH')
FORBIDDEN_CAPABILITIES={'unrestricted_browser_control':False,'credential_sensitive_action':False,'account_operation':False,'destructive_action':False,'form_submission':False,'purchase_or_submission':False,'persistent_dom_mutation':False,'production_visual_automation':False,'production_authority':False}
@dataclass(frozen=True)
class VisualArtifactComparison:
    label:str; before_ref:str; after_ref:str; before_sha256:str|None=None; after_sha256:str|None=None; changed:bool|None=None; comparison_note:str|None=None
@dataclass(frozen=True)
class VisualBeforeAfterVerificationReceipt:
    schema_id:str; version:str; verification_id:str; emitted_at:str; target:str; verification_mode:str; before_observation_packet_ids:tuple[str,...]; after_observation_packet_ids:tuple[str,...]; before_diagnosis_receipt_ids:tuple[str,...]; after_diagnosis_receipt_ids:tuple[str,...]; before_evidence_refs:tuple[str,...]; after_evidence_refs:tuple[str,...]; artifact_comparisons:tuple[VisualArtifactComparison,...]; resolved_findings:tuple[str,...]; persistent_findings:tuple[str,...]; new_findings:tuple[str,...]; regression_findings:tuple[str,...]; confidence:str; steward_gate_status:str; verification_verdict:str; recommended_next_actions:tuple[str,...]; authority_scope:str; repair_verified:bool; review_required:bool; production_authority:bool=False; forbidden_capabilities:dict[str,bool]=field(default_factory=lambda:dict(FORBIDDEN_CAPABILITIES))

def build_visual_before_after_verification_receipt(*, target:str, verification_mode:str='DIAGNOSTIC_COMPARISON_ONLY', before_observation_packet_ids:Iterable[str]=(), after_observation_packet_ids:Iterable[str]=(), before_diagnosis_receipt_ids:Iterable[str]=(), after_diagnosis_receipt_ids:Iterable[str]=(), before_evidence_refs:Iterable[str]=(), after_evidence_refs:Iterable[str]=(), artifact_comparisons:Iterable[VisualArtifactComparison]=(), resolved_findings:Iterable[str]=(), persistent_findings:Iterable[str]=(), new_findings:Iterable[str]=(), regression_findings:Iterable[str]=(), confidence:str='MEDIUM', steward_gate_status:str='APPROVED_VERIFY_ONLY', recommended_next_actions:Iterable[str]=(), emitted_at:str|None=None)->VisualBeforeAfterVerificationReceipt:
    if verification_mode not in ALLOWED_VERIFICATION_MODES: raise ValueError(f'invalid verification_mode: {verification_mode}')
    if confidence not in CONFIDENCE_LEVELS: raise ValueError(f'invalid confidence: {confidence}')
    if steward_gate_status not in STEWARD_GATE_STATUSES: raise ValueError(f'invalid steward_gate_status: {steward_gate_status}')
    vals=[tuple(x) for x in (before_observation_packet_ids,after_observation_packet_ids,before_diagnosis_receipt_ids,after_diagnosis_receipt_ids,before_evidence_refs,after_evidence_refs,artifact_comparisons,resolved_findings,persistent_findings,new_findings,regression_findings,recommended_next_actions)]
    bo,ao,bd,ad,br,ar,comp,res,pers,new,reg,acts=vals
    verdict,verified,review=_derive(steward_gate_status,bool(ao or ad or ar or comp),res,pers,new,reg,comp)
    ts=emitted_at or _utc_now(); rid=_stable_id('visual-before-after',VERSION,ts,target,verdict,'|'.join(res),'|'.join(reg))
    return VisualBeforeAfterVerificationReceipt(SCHEMA_ID,VERSION,rid,ts,target,verification_mode,bo,ao,bd,ad,br,ar,comp,res,pers,new,reg,confidence,steward_gate_status,verdict,acts or _actions(verdict),'VISUAL_BEFORE_AFTER_VERIFY_REPORT_ONLY',verified,review)

def compare_local_artifacts(*, workspace_root:str|Path, before_path:str|Path, after_path:str|Path, label:str='visual_artifact', comparison_note:str|None=None)->VisualArtifactComparison:
    root=Path(workspace_root).resolve(); before=_inside(root,before_path); after=_inside(root,after_path); bh=_sha(before); ah=_sha(after)
    return VisualArtifactComparison(label,f'localfile://{before.relative_to(root).as_posix()}',f'localfile://{after.relative_to(root).as_posix()}',bh,ah,bh!=ah,comparison_note)

def validate_visual_before_after_verification_receipt(r:VisualBeforeAfterVerificationReceipt)->tuple[str,...]:
    e=[]
    if r.schema_id!=SCHEMA_ID: e.append('schema_id mismatch')
    if r.version!=VERSION: e.append('version mismatch')
    if r.authority_scope!='VISUAL_BEFORE_AFTER_VERIFY_REPORT_ONLY': e.append('authority scope mismatch')
    if r.production_authority is not False: e.append('production authority must be false')
    if any(v is not False for v in r.forbidden_capabilities.values()): e.append('forbidden capabilities must be false')
    if r.repair_verified and r.verification_verdict!='VISUAL_REPAIR_VERIFIED': e.append('repair_verified requires verified verdict')
    if r.regression_findings and not r.review_required: e.append('regression requires review')
    return tuple(e)

def write_visual_before_after_verification_receipt(workspace_root:str|Path, receipt:VisualBeforeAfterVerificationReceipt, *, report_dir:str=DEFAULT_REPORT_DIR)->Path:
    out=Path(workspace_root)/report_dir; out.mkdir(parents=True,exist_ok=True); p=out/f'{receipt.verification_id}.visual_before_after_verification_receipt.json'; p.write_text(json.dumps(_json(receipt),indent=2,sort_keys=True)+'\n',encoding='utf-8'); return p

def _derive(gate,after,res,pers,new,reg,comp):
    if gate=='BLOCKED': return 'BLOCKED_BY_STEWARD',False,True
    if not after: return 'VISUAL_VERIFICATION_NEEDS_AFTER_EVIDENCE',False,True
    if reg or new: return 'VISUAL_REGRESSION_OR_NEW_ISSUE_REQUIRES_REVIEW',False,True
    if pers: return 'VISUAL_REPAIR_PARTIAL_NEEDS_FOLLOWUP',False,True
    if res: return 'VISUAL_REPAIR_VERIFIED',True,gate=='STEWARD_REVIEW_REQUIRED'
    if comp and any(c.changed for c in comp): return 'VISUAL_CHANGE_EVIDENCE_RECORDED_REQUIRES_REVIEW',False,True
    return 'VISUAL_VERIFICATION_NO_ACTIONABLE_CHANGE_RECORDED',False,gate=='STEWARD_REVIEW_REQUIRED'
def _actions(v):
    return {'VISUAL_REPAIR_VERIFIED':('record verified visual repair receipt',),'VISUAL_REPAIR_PARTIAL_NEEDS_FOLLOWUP':('route persistent findings to implementation agent',),'VISUAL_REGRESSION_OR_NEW_ISSUE_REQUIRES_REVIEW':('block verified language and route to Steward/VZ review',),'VISUAL_VERIFICATION_NEEDS_AFTER_EVIDENCE':('capture after evidence before claiming repair',),'BLOCKED_BY_STEWARD':('do not verify until Steward/VZ clears gate',)}.get(v,('request review before treating change as repair',))
def _inside(root,path):
    p=Path(path); p=(root/p).resolve() if not p.is_absolute() else p.resolve()
    if p!=root and root not in p.parents: raise ValueError(f'artifact path escapes workspace root: {p}')
    if not p.is_file(): raise ValueError(f'artifact path does not exist as file: {p}')
    return p
def _sha(p):
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def _utc_now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def _stable_id(*parts): return 'v48-'+hashlib.sha256('::'.join(parts).encode()).hexdigest()[:16]
def _json(v:Any)->Any:
    if hasattr(v,'__dataclass_fields__'): return {k:_json(x) for k,x in asdict(v).items()}
    if isinstance(v,tuple): return [_json(x) for x in v]
    if isinstance(v,dict): return {str(k):_json(x) for k,x in v.items()}
    return v
def _scenario(name,root):
    ts='2026-04-25T06:48:00+00:00'
    if name=='partial': return build_visual_before_after_verification_receipt(target='local UI',before_evidence_refs=('screenshot://before',),after_evidence_refs=('screenshot://after',),resolved_findings=('panel-overlap',),persistent_findings=('mobile-density',),emitted_at=ts)
    if name=='regression': return build_visual_before_after_verification_receipt(target='local UI',before_evidence_refs=('screenshot://before',),after_evidence_refs=('screenshot://after',),regression_findings=('new-scrollbar',),confidence='HIGH',emitted_at=ts)
    if name=='blocked': return build_visual_before_after_verification_receipt(target='restricted workflow',steward_gate_status='BLOCKED',emitted_at=ts)
    if name=='hash':
        r=Path(root); b=r/'ION/05_context/sandboxes/visual_before_after_demo/before.txt'; a=r/'ION/05_context/sandboxes/visual_before_after_demo/after.txt'; b.parent.mkdir(parents=True,exist_ok=True); b.write_text('before',encoding='utf-8'); a.write_text('after',encoding='utf-8'); c=compare_local_artifacts(workspace_root=r,before_path=b,after_path=a); return build_visual_before_after_verification_receipt(target='local artifact',verification_mode='LOCAL_ARTIFACT_HASH_COMPARISON',artifact_comparisons=(c,),emitted_at=ts)
    if name=='missing': return build_visual_before_after_verification_receipt(target='local UI',resolved_findings=('panel-overlap',),emitted_at=ts)
    return build_visual_before_after_verification_receipt(target='local UI',before_evidence_refs=('screenshot://before',),after_evidence_refs=('screenshot://after',),resolved_findings=('panel-overlap',),confidence='HIGH',emitted_at=ts)
def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('workspace_root'); ap.add_argument('--scenario',choices=('verified','partial','regression','blocked','hash','missing'),default='verified'); ap.add_argument('--write',action='store_true'); args=ap.parse_args(argv); r=_scenario(args.scenario,args.workspace_root)
    if args.write: print(write_visual_before_after_verification_receipt(args.workspace_root,r).as_posix())
    print(json.dumps(_json(r),indent=2,sort_keys=True)); errs=validate_visual_before_after_verification_receipt(r)
    if errs: print(json.dumps({'validation_errors':errs},indent=2)); return 4
    if r.verification_verdict=='BLOCKED_BY_STEWARD': return 3
    if r.review_required and not r.repair_verified: return 2
    return 0
if __name__=='__main__': raise SystemExit(main())
