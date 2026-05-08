"""V55 visual closure graph projection: branch-local query state only."""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
SCHEMA_ID="ion.visual_closure_graph_projection.v1"; VERSION="V55_VISUAL_CLOSURE_GRAPH_PROJECTION"; AUTHORITY_SCOPE="BRANCH_LOCAL_VISUAL_CLOSURE_GRAPH_PROJECTION_ONLY"; DEFAULT_REPORT_DIR="ION/05_context/history/visual_closure_graph_projection_reports"
FORBIDDEN_CAPABILITIES={"unrestricted_browser_control":False,"external_network_access":False,"credential_or_session_import":False,"account_operation":False,"destructive_action":False,"form_submission":False,"purchase_or_submission":False,"persistent_dom_mutation":False,"production_visual_automation":False,"production_graph_canon":False,"production_authority":False}
CLOSED="VISUAL_ISSUE_CLOSED_WITH_RUN_EVIDENCE"; REVIEW="VISUAL_ISSUE_CLOSURE_NEEDS_REVIEW"; FOLLOWUP="VISUAL_ISSUE_CLOSURE_NEEDS_FOLLOWUP"; REGRESSION="VISUAL_ISSUE_CLOSURE_REGRESSION_REQUIRES_REVIEW"; REJECTED="VISUAL_ISSUE_CLOSURE_REJECTED_FOR_FORBIDDEN_EVENT"; BLOCKED="VISUAL_ISSUE_CLOSURE_BLOCKED_BY_STEWARD"
@dataclass(frozen=True)
class VisualClosureBindingInput:
    issue_id:str; target:str; closure_binding_id:str; closure_verdict:str; diagnosis_receipt_ids:tuple[str,...]=(); before_after_verification_ids:tuple[str,...]=(); local_browser_run_receipt_ids:tuple[str,...]=(); observation_packet_ids:tuple[str,...]=(); evidence_refs:tuple[str,...]=(); resolved_findings:tuple[str,...]=(); persistent_findings:tuple[str,...]=(); regression_findings:tuple[str,...]=(); recommended_next_actions:tuple[str,...]=()
@dataclass(frozen=True)
class GraphNode: node_id:str; node_kind:str; label:str; status:str="recorded"; metadata:dict[str,Any]=field(default_factory=dict)
@dataclass(frozen=True)
class GraphEdge: edge_id:str; source:str; target:str; relation:str; metadata:dict[str,Any]=field(default_factory=dict)
@dataclass(frozen=True)
class VisualClosureGraphProjectionRequest:
    projection_name:str; workflow_id:str; bindings:tuple[VisualClosureBindingInput,...]; steward_gate_status:str="APPROVED_GRAPH_PROJECTION"; requested_capabilities:dict[str,bool]=field(default_factory=dict); notes:tuple[str,...]=()
@dataclass(frozen=True)
class VisualClosureGraphProjectionReceipt:
    schema_id:str; version:str; projection_id:str; emitted_at:str; projection_name:str; workflow_id:str; authority_scope:str; steward_gate_status:str; projection_verdict:str; nodes:tuple[GraphNode,...]; edges:tuple[GraphEdge,...]; open_issue_count:int; closed_issue_count:int; review_issue_count:int; followup_issue_count:int; regressed_issue_count:int; blocked_issue_count:int; projection_findings:tuple[str,...]; recommended_next_actions:tuple[str,...]; production_authority:bool=False; global_graph_canon_authorized:bool=False; production_graph_migration_authorized:bool=False; unrestricted_browser_control_authorized:bool=False; forbidden_capabilities:dict[str,bool]=field(default_factory=lambda:dict(FORBIDDEN_CAPABILITIES))
def build_visual_closure_graph_projection_receipt(*, request:VisualClosureGraphProjectionRequest, emitted_at:str|None=None)->VisualClosureGraphProjectionReceipt:
    _validate_request(request); findings=list(request.notes); forbidden=tuple(k for k,v in request.requested_capabilities.items() if v and k in FORBIDDEN_CAPABILITIES)
    if forbidden: findings.append("requested forbidden capabilities: "+", ".join(sorted(forbidden)))
    if request.steward_gate_status=="BLOCKED": findings.append("Steward/VZ blocked graph projection")
    if not request.bindings: findings.append("no V54 closure bindings supplied for graph projection")
    nodes:dict[str,GraphNode]={}; edges:list[GraphEdge]=[]; counts={"open":0,"closed":0,"needs_review":0,"needs_followup":0,"regressed":0,"blocked":0}
    for b in request.bindings:
        status=_status_for_verdict(b.closure_verdict); counts[status]+=1; issue=f"visual_issue:{b.issue_id}"; target=f"target_surface:{_slug(b.target)}"
        nodes.setdefault(issue,GraphNode(issue,"visual_issue",b.issue_id,status,{"closure_verdict":b.closure_verdict})); nodes.setdefault(target,GraphNode(target,"target_surface",b.target)); edges.append(_edge(issue,target,"targets"))
        closure=f"closure_binding:{b.closure_binding_id}"; nodes.setdefault(closure,GraphNode(closure,"closure_binding_receipt",b.closure_binding_id,status,{"closure_verdict":b.closure_verdict})); edges.append(_edge(issue,closure,"has_closure_binding"))
        for kind, rel, vals in [("observation_packet","observed_by",b.observation_packet_ids),("diagnosis_receipt","diagnosed_by",b.diagnosis_receipt_ids),("before_after_verification_receipt","verified_by",b.before_after_verification_ids),("local_browser_run_receipt","run_evidenced_by",b.local_browser_run_receipt_ids),("evidence_ref","has_evidence_ref",b.evidence_refs)]:
            for v in vals:
                nid=f"{kind}:{_slug(v) if kind=='evidence_ref' else v}"; nodes.setdefault(nid,GraphNode(nid,kind,v)); edges.append(_edge(issue,nid,rel))
        findings.append(f"visual issue {b.issue_id} {'closed with run evidence' if status=='closed' else 'remains '+status}")
    if forbidden: verdict="VISUAL_CLOSURE_GRAPH_PROJECTION_REJECTED_FOR_FORBIDDEN_CAPABILITY"
    elif request.steward_gate_status=="BLOCKED": verdict="VISUAL_CLOSURE_GRAPH_PROJECTION_BLOCKED_BY_STEWARD"
    elif counts["regressed"]: verdict="VISUAL_CLOSURE_GRAPH_PROJECTION_REGRESSION_REQUIRES_REVIEW"
    elif counts["blocked"]: verdict="VISUAL_CLOSURE_GRAPH_PROJECTION_BLOCKED_ISSUES_PRESENT"
    elif counts["needs_followup"] or counts["needs_review"] or counts["open"]: verdict="VISUAL_CLOSURE_GRAPH_PROJECTION_OPEN_ITEMS_PRESENT"
    elif counts["closed"]: verdict="VISUAL_CLOSURE_GRAPH_PROJECTION_ALL_SUPPLIED_ISSUES_CLOSED"
    else: verdict="VISUAL_CLOSURE_GRAPH_PROJECTION_EMPTY_REQUIRES_REVIEW"
    ts=emitted_at or _utc_now(); pid=_stable_id("v55-visual-closure-graph",ts,request.projection_name,request.workflow_id,verdict)
    return VisualClosureGraphProjectionReceipt(SCHEMA_ID,VERSION,pid,ts,request.projection_name,request.workflow_id,AUTHORITY_SCOPE,request.steward_gate_status,verdict,tuple(nodes.values()),tuple(edges),counts["open"],counts["closed"],counts["needs_review"],counts["needs_followup"],counts["regressed"],counts["blocked"],tuple(findings),tuple(_actions(verdict)))
def validate_visual_closure_graph_projection_receipt(r:VisualClosureGraphProjectionReceipt)->tuple[str,...]:
    e=[]
    if r.schema_id!=SCHEMA_ID: e.append("schema_id mismatch")
    if r.version!=VERSION: e.append("version mismatch")
    if r.authority_scope!=AUTHORITY_SCOPE: e.append("authority scope mismatch")
    if r.production_authority or r.global_graph_canon_authorized or r.production_graph_migration_authorized: e.append("production/global graph authority flags must remain false")
    if r.unrestricted_browser_control_authorized or any(r.forbidden_capabilities.values()): e.append("forbidden authority flags must remain false")
    ids={n.node_id for n in r.nodes}
    for edge in r.edges:
        if edge.source not in ids or edge.target not in ids: e.append("edge references missing node")
    return tuple(e)
def write_visual_closure_graph_projection_receipt(workspace_root:str|Path, receipt:VisualClosureGraphProjectionReceipt, *, output_dir:str|Path=DEFAULT_REPORT_DIR)->Path:
    out=Path(workspace_root)/output_dir; out.mkdir(parents=True, exist_ok=True); p=out/f"{receipt.projection_id}.json"; p.write_text(json.dumps(_to_json(receipt),indent=2,sort_keys=True)+"\n"); return p
def _validate_request(request:VisualClosureGraphProjectionRequest)->None:
    if not request.projection_name.strip(): raise ValueError("projection_name is required")
    if not request.workflow_id.strip(): raise ValueError("workflow_id is required")
    allowed={CLOSED,REVIEW,FOLLOWUP,REGRESSION,REJECTED,BLOCKED}
    for b in request.bindings:
        if not b.issue_id.strip() or not b.target.strip() or not b.closure_binding_id.strip(): raise ValueError("binding issue_id, target, and closure_binding_id are required")
        if b.closure_verdict not in allowed: raise ValueError(f"unknown closure verdict: {b.closure_verdict}")
def _status_for_verdict(v:str)->str: return {CLOSED:"closed",REVIEW:"needs_review",FOLLOWUP:"needs_followup",REGRESSION:"regressed",REJECTED:"blocked",BLOCKED:"blocked"}[v]
def _actions(v:str)->list[str]:
    if v.endswith("ALL_SUPPLIED_ISSUES_CLOSED"): return ["surface closed visual issue state when asked","preserve V54/V55 receipts"]
    if "REJECTED" in v: return ["remove forbidden capability request","rerun Steward/VZ review"]
    if "BLOCKED" in v: return ["hold until Steward/VZ unblock"]
    if "REGRESSION" in v: return ["route regressed issue back to diagnosis"]
    if "OPEN_ITEMS" in v: return ["route open visual issues into next Visual Agent queue"]
    return ["attach V54 closure bindings before using projection"]
def _edge(s:str,t:str,r:str)->GraphEdge: return GraphEdge(_stable_id("edge",s,r,t),s,t,r)
def _stable_id(*parts:str)->str: return hashlib.sha256("::".join(map(str,parts)).encode()).hexdigest()[:24]
def _slug(v:str)->str: return "".join(ch.lower() if ch.isalnum() else "-" for ch in v).strip("-")[:96] or "item"
def _utc_now()->str: return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def _to_json(o:Any)->Any:
    if hasattr(o,"__dataclass_fields__"): return {k:_to_json(v) for k,v in asdict(o).items()}
    if isinstance(o,tuple): return [_to_json(x) for x in o]
    if isinstance(o,list): return [_to_json(x) for x in o]
    if isinstance(o,dict): return {k:_to_json(v) for k,v in o.items()}
    return o
def _binding(issue_id:str, verdict:str)->VisualClosureBindingInput:
    return VisualClosureBindingInput(issue_id,"ION visual demo surface",f"v54-{issue_id}",verdict,(f"diag-{issue_id}",),(f"ba-{issue_id}",),(f"run-{issue_id}",),(f"obs-{issue_id}",),(f"screenshots/{issue_id}.png",))
def _scenario(name:str)->VisualClosureGraphProjectionRequest:
    if name=="closed": return VisualClosureGraphProjectionRequest("closed projection","visual-workflow",(_binding("issue-closed",CLOSED),))
    if name=="mixed": return VisualClosureGraphProjectionRequest("mixed projection","visual-workflow",(_binding("issue-closed",CLOSED),_binding("issue-followup",FOLLOWUP)))
    if name=="regression": return VisualClosureGraphProjectionRequest("regression projection","visual-workflow",(_binding("issue-regressed",REGRESSION),))
    if name=="blocked": return VisualClosureGraphProjectionRequest("blocked projection","visual-workflow",(_binding("issue-blocked",BLOCKED),),steward_gate_status="BLOCKED")
    if name=="forbidden": return VisualClosureGraphProjectionRequest("forbidden projection","visual-workflow",(_binding("issue-forbidden",CLOSED),),requested_capabilities={"production_graph_canon":True})
    return VisualClosureGraphProjectionRequest("empty projection","visual-workflow",())
def _main(argv:Sequence[str]|None=None)->int:
    ap=argparse.ArgumentParser(); ap.add_argument("--scenario",choices=["closed","mixed","regression","blocked","forbidden","empty"],default="closed"); ap.add_argument("--workspace-root",default="."); ap.add_argument("--write",action="store_true"); a=ap.parse_args(argv)
    r=build_visual_closure_graph_projection_receipt(request=_scenario(a.scenario)); errs=validate_visual_closure_graph_projection_receipt(r)
    if a.write: write_visual_closure_graph_projection_receipt(a.workspace_root,r)
    print(json.dumps(_to_json(r),indent=2,sort_keys=True));
    return 3 if errs or "REJECTED" in r.projection_verdict or "BLOCKED" in r.projection_verdict else (0 if r.projection_verdict.endswith("ALL_SUPPLIED_ISSUES_CLOSED") else 2)
if __name__=="__main__": raise SystemExit(_main())
