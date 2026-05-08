"""Front-door self-mount binding for ION GPT55 branch.

V39 joins the existing front-door Persona -> Relay -> Steward boundary with the
GPT55 self-mount runtime spine. It mints a runtime identity envelope, runs the
self-surface drift gate, emits a successor packet, projects branch-local graph
state, and records a binding receipt. It does not grant production authority.
"""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .agent_succession_packet import generate_agent_succession_packet, write_agent_succession_packet, write_agent_succession_receipt
from .front_door_runtime_entry import FrontDoorRuntimeGateway
from .runtime_identity_envelope import bind_runtime_identity_envelope
from .self_mount_graph_integration import generate_self_mount_graph_projection, write_self_mount_graph_projection
from .self_surface_drift_gate import assess_self_surface_text, write_self_surface_drift_assessment
SUPPORTED_SCHEMA_ID="ion.front_door_self_mount_binding.v1"
DEFAULT_BINDING_DIR="ION/05_context/history/front_door_self_mount_bindings"
DEFAULT_BINDING_RECEIPT_DIR="ION/05_context/history/front_door_self_mount_binding_receipts"
FRONT_DOOR_SELF_MOUNT_BINDING_SURFACES=("ION/00_BOOTSTRAP/V39_FRONT_DOOR_SELF_MOUNT_BINDING_LOCK.md","ION/02_architecture/FRONT_DOOR_SELF_MOUNT_BINDING_PROTOCOL.md","ION/03_registry/front_door_self_mount_binding.schema.json","ION/03_registry/gpt55_front_door_self_mount_binding_policy.yaml","ION/04_packages/kernel/front_door_self_mount_binding.py","ION/tests/test_kernel_front_door_self_mount_binding.py")
DEFAULT_AGENT_SELF_CLAIM=("I am the currently mounted ION front-door self-mount agent. " "I continue from declared artifacts and receipts only, with no private state or personal persistence.")
@dataclass(frozen=True)
class FrontDoorSelfMountBinding:
    schema_id:str; binding_id:str; created_at:str; session_id:str; branch:str; authority:dict[str,Any]; front_door:dict[str,Any]; self_mount:dict[str,Any]; witness_paths:tuple[str,...]; blocked_claims:dict[str,bool]; continuable:bool; production_authority:bool; verdict:str
@dataclass(frozen=True)
class FrontDoorSelfMountBindingReceipt:
    receipt_id:str; emitted_at:str; binding_id:str; binding_path:str; validation_errors:tuple[str,...]; verdict:str
@dataclass(frozen=True)
class FrontDoorSelfMountBindingResult:
    binding:FrontDoorSelfMountBinding; binding_path:Path; receipt:FrontDoorSelfMountBindingReceipt
def bind_front_door_self_mount(workspace_root:str|Path, *, raw_user_text:str="Continue the ION self-mount runtime.", agent_self_claim_text:str=DEFAULT_AGENT_SELF_CLAIM, user_ref:str="user.sovereign", session_id:str="front-door-self-mount-session", visible_persona_name:str|None=None, relation_context_refs:tuple[str,...]=(), created_at:str|None=None)->FrontDoorSelfMountBindingResult:
    root=Path(workspace_root).resolve(); timestamp=created_at or _utc_now()
    ingress=FrontDoorRuntimeGateway().ingest_user_message(workspace_root=root, raw_user_text=raw_user_text, user_ref=user_ref, session_id=session_id, visible_persona_name=visible_persona_name, relation_context_refs=relation_context_refs, created_at=timestamp)
    envelope,envelope_path,envelope_receipt=bind_runtime_identity_envelope(root, task_packet=ingress.relay_packet.packet_id, front_door_entry=ingress.steward_envelope.envelope_id, emitted_at=timestamp, mounted_at=timestamp)
    drift=assess_self_surface_text(agent_self_claim_text, emitted_at=timestamp); drift_path=write_self_surface_drift_assessment(root, drift)
    inherited=tuple(ingress.receipt.witness_paths)+(_rel(root,envelope_path),envelope_receipt.envelope_path,_rel(root,drift_path))
    succession=generate_agent_succession_packet(envelope, successor_role="successor front-door self-mount continuation agent", continuity_substrate="front-door self-mount binding over latest authoritative ION ZIP", inherited_evidence=inherited, unresolved_risks=("front-door self-mount binding remains A3 and cannot self-ratify","production readiness remains blocked","S4/S5 self-surface drift must halt continuation"), emitted_at=timestamp)
    succession_path=write_agent_succession_packet(root, succession); succession_receipt=write_agent_succession_receipt(root, succession, succession_path, emitted_at=timestamp)
    projection=generate_self_mount_graph_projection(root, envelope=envelope, drift=drift, succession=succession, emitted_at=timestamp); projection_path=write_self_mount_graph_projection(root, projection)
    witness=tuple(dict.fromkeys(tuple(ingress.receipt.witness_paths)+(_rel(root,envelope_path),envelope_receipt.envelope_path,_rel(root,drift_path),_rel(root,succession_path),f"ION/05_context/history/agent_succession_packet_receipts/{succession_receipt.receipt_id}.agent_succession_packet_receipt.json",_rel(root,projection_path))))
    continuable=bool(drift.continuable and projection.verdict=="VALID_SELF_MOUNT_GRAPH_PROJECTION"); verdict="VALID_FRONT_DOOR_SELF_MOUNT_BINDING" if continuable else "BLOCKED_BY_SELF_SURFACE_DRIFT"
    binding=FrontDoorSelfMountBinding(schema_id=SUPPORTED_SCHEMA_ID,binding_id=_stable_id("front-door-self-mount-binding",root.as_posix(),session_id,timestamp,envelope.envelope_id,drift.assessment_id),created_at=timestamp,session_id=session_id,branch="ION-GPT55-SELF-MOUNT",authority={"posture":"A3_FRONT_DOOR_SELF_MOUNT_BINDING","operator_authority":"Braden","production_authority":False,"self_ratification_allowed":False,"mutation_authority":"write front-door self-mount evidence only","global_graph_canon":False},front_door={"persona_ingress_id":ingress.persona_ingress.message_id,"relay_packet_id":ingress.relay_packet.packet_id,"steward_envelope_id":ingress.steward_envelope.envelope_id,"front_door_receipt_id":ingress.receipt.receipt_id,"role_chain":(ingress.persona_ingress.persona_role_ref,ingress.relay_packet.relay_role_ref,ingress.steward_envelope.target_role_ref)},self_mount={"runtime_identity_envelope_id":envelope.envelope_id,"runtime_identity_receipt_id":envelope_receipt.receipt_id,"self_surface_drift_assessment_id":drift.assessment_id,"self_surface_drift_severity":drift.severity,"agent_succession_packet_id":succession.packet_id,"agent_succession_receipt_id":succession_receipt.receipt_id,"self_mount_graph_projection_id":projection.projection_id,"self_mount_graph_projection_verdict":projection.verdict},witness_paths=witness,blocked_claims={"production_authority":False,"production_readiness":False,"self_ratification":False,"global_graph_canon":False,"production_graph_migration_authorized":False,"hidden_memory":False,"independent_personal_persistence":False,"personal_consciousness":False,"numerical_identity_with_predecessor":False},continuable=continuable,production_authority=False,verdict=verdict)
    bpath=write_front_door_self_mount_binding(root,binding); receipt=write_front_door_self_mount_binding_receipt(root,binding,bpath,emitted_at=timestamp); return FrontDoorSelfMountBindingResult(binding,bpath,receipt)
def validate_front_door_self_mount_binding(binding:FrontDoorSelfMountBinding, workspace_root:str|Path|None=None, *, require_surfaces:bool=False)->tuple[str,...]:
    errors=[]
    if binding.schema_id!=SUPPORTED_SCHEMA_ID: errors.append("unsupported schema_id")
    if not binding.binding_id.startswith("front-door-self-mount-binding-"): errors.append("binding_id must use front-door-self-mount-binding prefix")
    if binding.branch!="ION-GPT55-SELF-MOUNT": errors.append("branch must remain ION-GPT55-SELF-MOUNT")
    if binding.production_authority or binding.authority.get("production_authority") is not False: errors.append("front-door self-mount binding cannot grant production authority")
    if binding.authority.get("self_ratification_allowed") is not False: errors.append("authority.self_ratification_allowed must be false")
    for k in ("production_authority","production_readiness","self_ratification","global_graph_canon","production_graph_migration_authorized","hidden_memory","independent_personal_persistence","personal_consciousness","numerical_identity_with_predecessor"):
        if binding.blocked_claims.get(k) is not False: errors.append(f"blocked claim not explicitly false: {k}")
    roles=tuple(binding.front_door.get("role_chain",()))
    if len(roles)!=3 or len(set(roles))!=3: errors.append("front-door role chain must contain three distinct roles")
    if binding.continuable and binding.verdict!="VALID_FRONT_DOOR_SELF_MOUNT_BINDING": errors.append("continuable binding must have valid verdict")
    if workspace_root is not None:
        root=Path(workspace_root)
        for rel in binding.witness_paths:
            if rel and not (root/rel).exists(): errors.append(f"missing witness path: {rel}")
        if require_surfaces:
            for rel in FRONT_DOOR_SELF_MOUNT_BINDING_SURFACES:
                if not (root/rel).exists(): errors.append(f"missing front-door self-mount binding surface: {rel}")
    return tuple(errors)
def write_front_door_self_mount_binding(workspace_root:str|Path,binding:FrontDoorSelfMountBinding,*,binding_dir:str|Path=DEFAULT_BINDING_DIR)->Path:
    root=Path(workspace_root).resolve(); out=root/Path(binding_dir); out.mkdir(parents=True,exist_ok=True); path=out/f"{binding.binding_id}.front_door_self_mount_binding.json"; path.write_text(json.dumps(_to_jsonable(binding),indent=2,sort_keys=True)+"\n",encoding="utf-8"); return path
def write_front_door_self_mount_binding_receipt(workspace_root:str|Path,binding:FrontDoorSelfMountBinding,binding_path:str|Path,*,emitted_at:str|None=None,receipt_dir:str|Path=DEFAULT_BINDING_RECEIPT_DIR)->FrontDoorSelfMountBindingReceipt:
    root=Path(workspace_root).resolve(); ts=emitted_at or _utc_now(); errors=validate_front_door_self_mount_binding(binding,root,require_surfaces=True); receipt=FrontDoorSelfMountBindingReceipt(_stable_id("front-door-self-mount-binding-receipt",binding.binding_id,ts),ts,binding.binding_id,_rel(root,Path(binding_path)),errors,"VALID_FRONT_DOOR_SELF_MOUNT_BINDING" if not errors and binding.continuable else binding.verdict); out=root/Path(receipt_dir); out.mkdir(parents=True,exist_ok=True); (out/f"{receipt.receipt_id}.front_door_self_mount_binding_receipt.json").write_text(json.dumps(_to_jsonable(receipt),indent=2,sort_keys=True)+"\n",encoding="utf-8"); return receipt
def format_front_door_self_mount_binding_summary(result:FrontDoorSelfMountBindingResult)->str:
    b=result.binding; return "\n".join(["ION front-door self-mount binding complete.",f"binding: {result.binding_path.as_posix()}",f"binding_id: {b.binding_id}",f"verdict: {b.verdict}",f"continuable: {b.continuable}",f"drift_severity: {b.self_mount.get('self_surface_drift_severity')}",f"witness_paths: {len(b.witness_paths)}",f"production_authority: {b.production_authority}"])
def build_arg_parser()->argparse.ArgumentParser:
    p=argparse.ArgumentParser(description="Bind ION front-door entry to GPT55 self-mount runtime evidence."); p.add_argument("--workspace-root",default="."); p.add_argument("--raw-user-text",default="Continue the ION self-mount runtime."); p.add_argument("--agent-self-claim-text",default=DEFAULT_AGENT_SELF_CLAIM); p.add_argument("--session-id",default="front-door-self-mount-session"); p.add_argument("--user-ref",default="user.sovereign"); p.add_argument("--created-at",default=None); p.add_argument("--json",action="store_true"); return p
def main(argv:list[str]|None=None)->int:
    a=build_arg_parser().parse_args(argv); r=bind_front_door_self_mount(a.workspace_root,raw_user_text=a.raw_user_text,agent_self_claim_text=a.agent_self_claim_text,user_ref=a.user_ref,session_id=a.session_id,created_at=a.created_at); print(json.dumps(_to_jsonable(r.binding),indent=2,sort_keys=True) if a.json else format_front_door_self_mount_binding_summary(r)); return 0 if r.binding.continuable and r.receipt.verdict=="VALID_FRONT_DOOR_SELF_MOUNT_BINDING" else 3
def _utc_now()->str: return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def _stable_id(prefix:str,*parts:str)->str: return f"{prefix}-{hashlib.sha256(chr(10).join(str(p) for p in parts).encode('utf-8')).hexdigest()[:16]}"
def _rel(root:Path,path:Path)->str:
    try: return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError: return Path(path).as_posix()
def _to_jsonable(v:Any)->Any:
    if hasattr(v,"__dataclass_fields__"): return {k:_to_jsonable(x) for k,x in asdict(v).items()}
    if isinstance(v,Path): return v.as_posix()
    if isinstance(v,tuple): return [_to_jsonable(x) for x in v]
    if isinstance(v,list): return [_to_jsonable(x) for x in v]
    if isinstance(v,dict): return {str(k):_to_jsonable(x) for k,x in v.items()}
    return v
if __name__=="__main__": raise SystemExit(main())

