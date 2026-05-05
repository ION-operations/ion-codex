"""ION V106 front-door proof trace.

Materializes one deterministic proof that an operator message can move through
the existing front-door runtime path:

operator message -> Persona ingress -> Relay packet -> Steward queue/dispatch
-> controlled Steward output -> Relay return -> Persona response -> receipts.

This is a proof trace, not a live Steward reasoning claim and not production
authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .conversational_receipt import (
    build_conversational_receipt,
    make_event,
    validate_conversational_receipt,
    write_conversational_receipt,
)
from .front_door_chat_orchestration import FrontDoorChatOrchestrationAdapter
from .front_stage_council_receipt import (
    build_front_stage_council_receipt,
    validate_front_stage_council_receipt,
    write_front_stage_council_receipt,
)

SCHEMA_ID = "ion.front_door_proof_trace.v1"
PROJECTION_MODE = "DETERMINISTIC_FRONT_DOOR_PROOF_TRACE"
CURRENT = Path("ION/05_context/current")
HISTORY = Path("ION/05_context/history/front_door_proof_traces")
OUTPUT = CURRENT / "ACTIVE_FRONT_DOOR_PROOF_TRACE.json"

DEFAULT_OPERATOR_MESSAGE = (
    "V106 front-door proof trace: verify operator message through Relay, "
    "Steward, Persona, and receipts."
)
DEFAULT_CONTROLLED_OUTPUT = (
    "Deterministic front-door proof output: the operator message was routed "
    "through Persona Interface ingress, Relay semantic boundary, Steward work "
    "queue dispatch, Relay return, Persona response, and receipt surfaces. "
    "This proof grants no production authority."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("::".join(part for part in parts if part).encode("utf-8")).hexdigest()[:18]
    return f"{prefix}-{digest}"


def _rel(root: Path, path: str | Path | None) -> str | None:
    if path is None:
        return None
    candidate = Path(path)
    if not candidate.is_absolute():
        return candidate.as_posix()
    try:
        return candidate.resolve().relative_to(root).as_posix()
    except ValueError:
        return candidate.as_posix()


def _exists(root: Path, rel_path: str | None) -> bool:
    if not rel_path:
        return False
    candidate = Path(rel_path)
    if candidate.is_absolute():
        return candidate.exists()
    return (root / candidate).exists()


def _stage(
    *,
    sequence: int,
    stage: str,
    organ: str,
    status: str,
    artifact_id: str | None = None,
    witness_path: str | None = None,
    receipt_id: str | None = None,
    detail: str = "",
) -> dict[str, Any]:
    return {
        "sequence": sequence,
        "stage": stage,
        "organ": organ,
        "status": status,
        "artifact_id": artifact_id,
        "witness_path": witness_path,
        "receipt_id": receipt_id,
        "detail": detail,
    }


def _compact_paths(paths: list[str | None]) -> list[str]:
    seen: set[str] = set()
    compacted: list[str] = []
    for path in paths:
        if not path:
            continue
        if path in seen:
            continue
        seen.add(path)
        compacted.append(path)
    return compacted


def _dispatch_packet_path(turn_result: Any, root: Path) -> str | None:
    dispatch_result = getattr(turn_result, "dispatch_result", None)
    if dispatch_result is None:
        return None
    kernel_dispatch = getattr(dispatch_result, "dispatch_result", None)
    packet_path = getattr(kernel_dispatch, "packet_path", None)
    return _rel(root, packet_path)


def build_front_door_proof_trace(
    ion_root: str | Path = ".",
    *,
    operator_message: str = DEFAULT_OPERATOR_MESSAGE,
    controlled_system_output: str = DEFAULT_CONTROLLED_OUTPUT,
    session_id: str | None = None,
    user_ref: str = "user.sovereign",
    visible_persona_name: str | None = None,
    created_at: str | None = None,
    dispatch: bool = True,
) -> dict[str, Any]:
    root = Path(ion_root).resolve()
    emitted_at = created_at or utc_now()
    resolved_session_id = session_id or _stable_id("fdsession", emitted_at, operator_message)

    adapter = FrontDoorChatOrchestrationAdapter()
    turn = adapter.submit_user_turn(
        workspace_root=root,
        raw_user_text=operator_message,
        session_id=resolved_session_id,
        user_ref=user_ref,
        visible_persona_name=visible_persona_name,
        relation_context_refs=("ION/02_architecture/FRONT_DOOR_RUNTIME_ENTRY_PROTOCOL.md",),
        carrier_ref="api://front-door-proof-trace",
        created_at=emitted_at,
        dispatch=dispatch,
    )
    returned = adapter.prepare_system_return(
        workspace_root=root,
        controlled_system_output=controlled_system_output,
        session_id=resolved_session_id,
        user_ref=user_ref,
        source_system_ref="steward.proof_trace_output",
        visible_persona_name=visible_persona_name,
        style_notes=(
            "deterministic proof trace",
            "do not claim live autonomous Steward reasoning",
            "do not grant production authority",
        ),
        created_at=emitted_at,
    )

    council_receipt = build_front_stage_council_receipt(
        claim_text=controlled_system_output,
        claim_summary="Deterministic front-door path proof output.",
        claim_class="C2",
        persona_state="RENDER_READY",
        relay_state="GROUNDED",
        steward_verdict="APPROVED_WITH_SCOPE",
        risk_level="LOW",
        emitted_at=emitted_at,
        notes=(
            "V106 proof trace only; Steward verdict is deterministic test projection.",
            "No production authority or live model-provider authority is granted.",
        ),
    )
    council_errors = list(validate_front_stage_council_receipt(council_receipt))
    council_path = _rel(root, write_front_stage_council_receipt(root, council_receipt))

    conversation_receipt = build_conversational_receipt(
        events=(
            make_event(
                "PROVISIONAL_UTTERANCE",
                controlled_system_output,
                claim_class="C2",
                timestamp=emitted_at,
                provisional=True,
                council_receipt_id=council_receipt.receipt_id,
            ),
            make_event(
                "RATIFICATION",
                controlled_system_output,
                claim_class="C2",
                timestamp=emitted_at,
                provisional=False,
                council_receipt_id=council_receipt.receipt_id,
            ),
        ),
        emitted_at=emitted_at,
        final_claim=controlled_system_output,
    )
    conversation_errors = list(validate_conversational_receipt(conversation_receipt))
    conversation_path = _rel(root, write_conversational_receipt(root, conversation_receipt))

    ingress = turn.ingress
    runtime_return = returned.return_result
    dispatch_packet_path = _dispatch_packet_path(turn, root)
    dispatch_result = getattr(turn, "dispatch_result", None)
    work_unit_status = str(turn.steward_work_unit.status)
    queue_item_status = str(turn.queue_item.status)
    if dispatch_result is not None:
        kernel_dispatch = getattr(dispatch_result, "dispatch_result", None)
        work_unit_after = getattr(kernel_dispatch, "work_unit_after", None)
        work_unit_status = str(getattr(work_unit_after, "status", work_unit_status))
        queue_item_status = "DISPATCHED"
    work_unit_path = f"ION/05_context/history/kernel_store/work_units/{turn.steward_work_unit.work_unit_id}.json"
    context_package_path = (
        f"ION/05_context/history/kernel_store/context_packages/{turn.context_package.context_package_id}.json"
    )

    ingress_witnesses = [_rel(root, path) for path in ingress.receipt.witness_paths]
    return_witnesses = [_rel(root, path) for path in runtime_return.receipt.witness_paths]
    api_witnesses = [_rel(root, path) for path in turn.api_entry.receipt.witness_paths]
    session_receipt_witnesses: list[str | None] = []
    session_receipt_id = None
    if dispatch_result is not None:
        session_receipt_id = dispatch_result.session_receipt.receipt_id
        session_receipt_witnesses = [_rel(root, path) for path in dispatch_result.session_receipt.witness_paths]

    witness_paths = _compact_paths(
        [
            *ingress_witnesses,
            *api_witnesses,
            work_unit_path,
            context_package_path,
            dispatch_packet_path,
            *session_receipt_witnesses,
            *return_witnesses,
            council_path,
            conversation_path,
        ]
    )
    missing_witness_paths = [path for path in witness_paths if not _exists(root, path)]
    validation_errors = council_errors + conversation_errors
    if str(turn.api_entry.receipt.status) != "ACCEPTED":
        validation_errors.append(f"api_runtime_entry_not_accepted: {turn.api_entry.receipt.status}")
    proof_complete = not missing_witness_paths and not validation_errors and dispatch_packet_path is not None
    trace_id = _stable_id(
        "fdproof",
        resolved_session_id,
        ingress.persona_ingress.message_id,
        runtime_return.persona_response.response_id,
        council_receipt.receipt_id,
        conversation_receipt.receipt_id,
    )
    proof_trace_path = (HISTORY / f"{trace_id}.front_door_proof_trace.json").as_posix()

    stage_sequence = [
        _stage(
            sequence=10,
            stage="operator_message_received",
            organ="operator",
            status="accepted",
            artifact_id=ingress.persona_ingress.message_id,
            witness_path=ingress_witnesses[0] if ingress_witnesses else None,
            receipt_id=ingress.receipt.receipt_id,
            detail="Operator message entered Persona Interface ingress.",
        ),
        _stage(
            sequence=20,
            stage="relay_semantic_boundary_packet",
            organ="relay",
            status="accepted",
            artifact_id=ingress.relay_packet.packet_id,
            witness_path=ingress_witnesses[1] if len(ingress_witnesses) > 1 else None,
            receipt_id=ingress.receipt.receipt_id,
            detail="Relay normalized the user text into a semantic boundary packet.",
        ),
        _stage(
            sequence=30,
            stage="steward_routing_envelope",
            organ="steward",
            status="accepted",
            artifact_id=ingress.steward_envelope.envelope_id,
            witness_path=ingress_witnesses[2] if len(ingress_witnesses) > 2 else None,
            receipt_id=ingress.receipt.receipt_id,
            detail="Steward routing envelope was derived from the Relay packet.",
        ),
        _stage(
            sequence=40,
            stage="runtime_session_entry",
            organ="kernel",
            status=str(turn.api_entry.receipt.status),
            artifact_id=turn.api_entry.intent.intent_id,
            receipt_id=turn.api_entry.receipt.receipt_id,
            detail=turn.api_entry.receipt.detail,
        ),
        _stage(
            sequence=50,
            stage="steward_work_unit_created",
            organ="steward",
            status=work_unit_status,
            artifact_id=turn.steward_work_unit.work_unit_id,
            witness_path=work_unit_path,
            detail="Steward work unit and context package were persisted to kernel store.",
        ),
        _stage(
            sequence=60,
            stage="context_package_created",
            organ="kernel",
            status="accepted",
            artifact_id=turn.context_package.context_package_id,
            witness_path=context_package_path,
            detail="Front-door Steward context package was persisted.",
        ),
        _stage(
            sequence=70,
            stage="queue_item_dispatched",
            organ="kernel",
            status=queue_item_status,
            artifact_id=turn.queue_item.item_id,
            witness_path=dispatch_packet_path,
            receipt_id=session_receipt_id,
            detail="Runtime session queue item was dispatched to kernel packet path.",
        ),
        _stage(
            sequence=80,
            stage="controlled_steward_output",
            organ="steward",
            status="approved_with_scope",
            artifact_id="steward.proof_trace_output",
            receipt_id=council_receipt.receipt_id,
            detail="Deterministic proof output stands in for live Steward return.",
        ),
        _stage(
            sequence=90,
            stage="relay_return_package",
            organ="relay",
            status="accepted",
            artifact_id=runtime_return.relay_return.return_id,
            witness_path=return_witnesses[0] if return_witnesses else None,
            receipt_id=runtime_return.receipt.receipt_id,
            detail="Relay prepared controlled reexpression for Persona Interface.",
        ),
        _stage(
            sequence=100,
            stage="persona_response_package",
            organ="persona",
            status="accepted",
            artifact_id=runtime_return.persona_response.response_id,
            witness_path=return_witnesses[1] if len(return_witnesses) > 1 else None,
            receipt_id=runtime_return.receipt.receipt_id,
            detail="Persona response package was materialized for user-facing render.",
        ),
        _stage(
            sequence=110,
            stage="front_stage_council_receipt",
            organ="steward",
            status=council_receipt.emission_permission.lower(),
            artifact_id=council_receipt.receipt_id,
            witness_path=council_path,
            receipt_id=council_receipt.receipt_id,
            detail="Front-stage council classified the proof output as scoped proposal emission.",
        ),
        _stage(
            sequence=120,
            stage="conversational_receipt",
            organ="persona",
            status=conversation_receipt.conversation_status.lower(),
            artifact_id=conversation_receipt.receipt_id,
            witness_path=conversation_path,
            receipt_id=conversation_receipt.receipt_id,
            detail="Conversational receipt ratified the deterministic proof response.",
        ),
    ]

    return {
        "schema_id": SCHEMA_ID,
        "trace_id": trace_id,
        "generated_at": emitted_at,
        "projection_mode": PROJECTION_MODE,
        "session_id": resolved_session_id,
        "operator_message": operator_message,
        "controlled_system_output": controlled_system_output,
        "role_chain": {
            "persona_interface": ingress.persona_ingress.persona_role_ref,
            "relay": ingress.relay_packet.relay_role_ref,
            "steward": ingress.steward_envelope.target_role_ref,
        },
        "boundary_proof": {
            "persona_ingress_id": ingress.persona_ingress.message_id,
            "relay_packet_id": ingress.relay_packet.packet_id,
            "steward_envelope_id": ingress.steward_envelope.envelope_id,
            "api_entry_intent_id": turn.api_entry.intent.intent_id,
            "api_entry_receipt_id": turn.api_entry.receipt.receipt_id,
            "steward_work_unit_id": turn.steward_work_unit.work_unit_id,
            "context_package_id": turn.context_package.context_package_id,
            "queue_item_id": turn.queue_item.item_id,
            "dispatch_packet_path": dispatch_packet_path,
            "relay_return_id": runtime_return.relay_return.return_id,
            "persona_response_id": runtime_return.persona_response.response_id,
            "front_stage_receipt_id": council_receipt.receipt_id,
            "conversational_receipt_id": conversation_receipt.receipt_id,
        },
        "steward_verdict": {
            "verdict": council_receipt.steward_verdict,
            "mode": PROJECTION_MODE,
            "claim_class": council_receipt.claim_class,
            "emission_permission": council_receipt.emission_permission,
            "repair_required": council_receipt.repair_required,
            "live_steward_reasoning": False,
        },
        "receipts": {
            "front_door_ingress_receipt_id": ingress.receipt.receipt_id,
            "front_door_return_receipt_id": runtime_return.receipt.receipt_id,
            "runtime_session_dispatch_receipt_id": session_receipt_id,
            "front_stage_council_receipt_id": council_receipt.receipt_id,
            "conversational_receipt_id": conversation_receipt.receipt_id,
        },
        "stage_sequence": stage_sequence,
        "witness_paths": witness_paths,
        "missing_witness_paths": missing_witness_paths,
        "validation_errors": validation_errors,
        "proof_trace_path": proof_trace_path,
        "proof_complete": proof_complete,
        "verdict": "ION_FRONT_DOOR_PROOF_TRACE_READY" if proof_complete else "ION_FRONT_DOOR_PROOF_TRACE_BLOCKED",
        "mutation_scope": "front_door_proof_trace_artifacts_only",
        "production_authority": False,
        "live_execution_authority": False,
    }


def write_front_door_proof_trace(
    ion_root: str | Path = ".",
    *,
    output: str | Path | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    root = Path(ion_root).resolve()
    trace = build_front_door_proof_trace(root, **kwargs)
    history_path = root / trace["proof_trace_path"]
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(json.dumps(trace, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    active_path = root / (Path(output) if output else OUTPUT)
    active_path.parent.mkdir(parents=True, exist_ok=True)
    active_path.write_text(json.dumps(trace, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return trace


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Materialize an ION V106 front-door proof trace.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--operator-message", default=DEFAULT_OPERATOR_MESSAGE)
    parser.add_argument("--controlled-system-output", default=DEFAULT_CONTROLLED_OUTPUT)
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--created-at", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--no-dispatch", action="store_true")
    parser.add_argument("--write", action="store_true", help="Write ACTIVE_FRONT_DOOR_PROOF_TRACE.json")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    kwargs = {
        "operator_message": args.operator_message,
        "controlled_system_output": args.controlled_system_output,
        "session_id": args.session_id,
        "created_at": args.created_at,
        "dispatch": not args.no_dispatch,
    }
    trace = (
        write_front_door_proof_trace(args.ion_root, output=args.output, **kwargs)
        if args.write
        else build_front_door_proof_trace(args.ion_root, **kwargs)
    )
    if args.json:
        print(json.dumps(trace, indent=2, sort_keys=True))
    else:
        print(trace["verdict"])
    return 0 if trace["proof_complete"] else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
