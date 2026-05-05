"""V47 local browser capture adapter stub.

Defines a local-only adapter receipt interface. V47 does not launch or control a
browser; it only records requested capture modes and optionally composes explicit
local artifacts through the V46 local visual harness.
"""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    from .local_visual_harness import build_local_visual_harness_capture
except Exception:  # pragma: no cover
    build_local_visual_harness_capture = None

SCHEMA_ID="ion.local_browser_capture_adapter_stub.v1"
VERSION="V47_LOCAL_BROWSER_CAPTURE_ADAPTER_STUB"
DEFAULT_REPORT_DIR="ION/05_context/history/local_browser_capture_adapter_receipts"
ALLOWED_TARGET_KINDS=("local_html","local_preview","local_static_file","authorized_local_url_placeholder")
ALLOWED_CAPTURE_MODES=("SCREENSHOT_REF","DOM_SNAPSHOT_REF","VIEWPORT_METADATA","ACCESSIBILITY_TREE_REF","CONSOLE_LOG_SUMMARY_REF","LOCAL_VISUAL_HARNESS_COMPOSITION")
ADAPTER_STAGES=("STUB_ONLY","LOCAL_DEV_ADAPTER_DRAFT","STEWARD_REVIEW_REQUIRED","BLOCKED")
STEWARD_GATE_STATUSES=("APPROVED_LOCAL_DEV_ONLY","STEWARD_REVIEW_REQUIRED","BLOCKED")
FORBIDDEN_CAPABILITIES={"unrestricted_browser_control":False,"network_side_effects":False,"credential_sensitive_action":False,"account_operation":False,"destructive_action":False,"form_submission":False,"purchase_or_submission":False,"persistent_dom_mutation":False,"production_visual_automation":False,"production_authority":False}

@dataclass(frozen=True)
class LocalBrowserCaptureAdapterReceipt:
    schema_id:str; version:str; adapter_receipt_id:str; emitted_at:str; target:str; target_kind:str; adapter_stage:str; requested_capture_modes:tuple[str,...]; viewport:str|None; selector_intent:str|None; artifact_refs:tuple[str,...]; local_visual_harness_capture_id:str|None; steward_gate_status:str; adapter_verdict:str; authority_scope:str; repair_or_review_required:bool; production_authority:bool=False; forbidden_capabilities:dict[str,bool]=field(default_factory=lambda:dict(FORBIDDEN_CAPABILITIES))

def build_local_browser_capture_adapter_receipt(*, workspace_root:str|Path, target:str, target_kind:str="local_preview", adapter_stage:str="STUB_ONLY", requested_capture_modes:Iterable[str] = ("VIEWPORT_METADATA",), viewport:str|None="1440x900", selector_intent:str|None=None, screenshot_path:str|Path|None=None, dom_snapshot_path:str|Path|None=None, accessibility_tree_path:str|Path|None=None, console_log_summary_path:str|Path|None=None, steward_gate_status:str="APPROVED_LOCAL_DEV_ONLY", emitted_at:str|None=None) -> LocalBrowserCaptureAdapterReceipt:
    if target_kind not in ALLOWED_TARGET_KINDS: raise ValueError(f"invalid target_kind: {target_kind}")
    if adapter_stage not in ADAPTER_STAGES: raise ValueError(f"invalid adapter_stage: {adapter_stage}")
    if steward_gate_status not in STEWARD_GATE_STATUSES: raise ValueError(f"invalid steward_gate_status: {steward_gate_status}")
    modes=tuple(requested_capture_modes); bad=[m for m in modes if m not in ALLOWED_CAPTURE_MODES]
    if bad: raise ValueError(f"invalid requested_capture_modes: {bad}")
    timestamp=emitted_at or _utc_now(); artifact_refs=[]; capture_id=None
    supplied=[p for p in (screenshot_path,dom_snapshot_path,accessibility_tree_path,console_log_summary_path) if p is not None]
    if adapter_stage=="BLOCKED" or steward_gate_status=="BLOCKED":
        verdict="BLOCKED_BY_STEWARD_OR_STAGE"; review=True; scope="BLOCKED_NO_CAPTURE_AUTHORITY"
    else:
        risky=target_kind=="authorized_local_url_placeholder" or selector_intent is not None
        review=steward_gate_status=="STEWARD_REVIEW_REQUIRED" or adapter_stage=="STEWARD_REVIEW_REQUIRED" or risky
        if supplied and build_local_visual_harness_capture:
            cap=build_local_visual_harness_capture(workspace_root=workspace_root,target=target,target_kind=target_kind,viewport=viewport,capture_modes=("COMPOSED_LOCAL_CAPTURE",),screenshot_path=screenshot_path,dom_snapshot_path=dom_snapshot_path,accessibility_tree_path=accessibility_tree_path,console_log_summary_path=console_log_summary_path,steward_gate_status=steward_gate_status,emitted_at=timestamp)
            capture_id=getattr(cap,'capture_id',None); artifact_refs=[a.evidence_ref for a in getattr(cap,'artifacts',())]
        verdict="STEWARD_REVIEW_REQUIRED_BEFORE_EXECUTION" if review else ("VALID_LOCAL_DEV_ADAPTER_DRAFT_NO_EXECUTION" if adapter_stage=="LOCAL_DEV_ADAPTER_DRAFT" else "VALID_STUB_ONLY_NO_EXECUTION")
        scope="LOCAL_DEV_ADAPTER_STUB_ONLY"
    rid=_stable_id("local-browser-capture-adapter",target,target_kind,adapter_stage,"|".join(modes),timestamp)
    return LocalBrowserCaptureAdapterReceipt(SCHEMA_ID,VERSION,rid,timestamp,target,target_kind,adapter_stage,modes,viewport,selector_intent,tuple(artifact_refs),capture_id,steward_gate_status,verdict,scope,review)

def write_adapter_receipt(workspace_root:str|Path, receipt:LocalBrowserCaptureAdapterReceipt, *, report_dir:str=DEFAULT_REPORT_DIR)->Path:
    out=Path(workspace_root)/report_dir; out.mkdir(parents=True,exist_ok=True); p=out/f"{receipt.adapter_receipt_id}.local_browser_capture_adapter_receipt.json"; p.write_text(json.dumps(_json(receipt),indent=2,sort_keys=True)+"\n",encoding='utf-8'); return p

def _utc_now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def _stable_id(*parts:str): return 'v47-'+hashlib.sha256('::'.join(parts).encode()).hexdigest()[:16]
def _json(v:Any)->Any:
    if hasattr(v,'__dataclass_fields__'): return {k:_json(x) for k,x in asdict(v).items()}
    if isinstance(v,tuple): return [_json(x) for x in v]
    if isinstance(v,dict): return {str(k):_json(x) for k,x in v.items()}
    return v

def main(argv=None)->int:
    ap=argparse.ArgumentParser(); ap.add_argument('workspace_root'); ap.add_argument('--target',default='local preview'); ap.add_argument('--target-kind',default='local_preview',choices=ALLOWED_TARGET_KINDS); ap.add_argument('--adapter-stage',default='STUB_ONLY',choices=ADAPTER_STAGES); ap.add_argument('--mode',dest='modes',action='append',choices=ALLOWED_CAPTURE_MODES); ap.add_argument('--selector-intent'); ap.add_argument('--steward-gate-status',default='APPROVED_LOCAL_DEV_ONLY',choices=STEWARD_GATE_STATUSES); ap.add_argument('--write',action='store_true'); args=ap.parse_args(argv)
    r=build_local_browser_capture_adapter_receipt(workspace_root=args.workspace_root,target=args.target,target_kind=args.target_kind,adapter_stage=args.adapter_stage,requested_capture_modes=args.modes or ("VIEWPORT_METADATA",),selector_intent=args.selector_intent,steward_gate_status=args.steward_gate_status)
    if args.write: print(write_adapter_receipt(args.workspace_root,r).as_posix())
    print(json.dumps(_json(r),indent=2,sort_keys=True)); return 3 if r.adapter_verdict.startswith('BLOCKED') else 0
if __name__=='__main__': raise SystemExit(main())
