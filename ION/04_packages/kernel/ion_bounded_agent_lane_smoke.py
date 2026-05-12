#!/usr/bin/env python3
"""Deterministic smoke probe for the bounded ION agent invocation lane.

Default behavior uses a temporary fake ION root and does not touch the active
connector queue. Pass --root only when intentionally probing a specific root.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from kernel.ion_agent_invocation_broker import (
    create_agent_relay_message,
    invoke_bounded_agent,
    pending_agent_relays,
    recent_agent_invocation_receipts,
    respond_agent_relay,
    settle_agent_invocation,
)


def sample_packet(key: str = "bounded-smoke-idempotency-key") -> dict[str, Any]:
    return {
        "schema_id": "ion.agent_invocation_packet.v1",
        "idempotency_key": key,
        "created_by": "chatgpt_browser",
        "agent_role": "role.context_cartographer",
        "agent_display_name": "CONTEXT_CARTOGRAPHER",
        "objective": "Inspect current browser queue architecture and return a proof-bearing report.",
        "capsule_context": {
            "mode": "refs_and_inline_summary",
            "context_refs": [
                "ION/04_packages/kernel/ion_custom_gpt_action_gateway.py",
                "ION/04_packages/kernel/ion_codex_queue_runner.py",
            ],
            "inline_summary": "Bounded read-only context cartography probe requested by ChatGPT Browser.",
            "required_reads": ["ION/04_packages/kernel/ion_custom_gpt_action_gateway.py"],
            "forbidden_reads": [".env", "secrets", "credentials"],
            "source_posture": "candidate",
        },
        "authority": {
            "production_authority": False,
            "live_execution_authority": False,
            "local_write_authority": "none",
            "requires_operator_approval": False,
            "operator_approval_evidence": None,
            "allowed_paths": ["ION/"],
            "forbidden_paths": [".env", "secrets", "credentials"],
            "hard_gates": [
                "access_credential",
                "broad_shell",
                "delete_file",
                "overwrite_protected_file",
                "production_deploy",
                "push_main",
            ],
        },
        "execution": {
            "backend": "codex_cli",
            "queue": True,
            "max_runtime_seconds": 900,
            "max_steps": 4,
            "stop_condition": "return proof packet, relay question, or blocker",
        },
        "proof_required": {
            "context_receipt": True,
            "template_action_proof": True,
            "changed_files_summary": True,
            "tests_or_validation": True,
            "receipt": True,
        },
        "relay_policy": {
            "allow_relay_to_chatgpt": True,
            "allow_relay_to_operator": True,
            "ask_operator_on_authority_gap": True,
            "no_silent_authority_expansion": True,
        },
        "settlement": {
            "settlement_target": "chatgpt_browser",
            "terminal_states": ["accepted", "blocked", "deferred", "rejected", "failed"],
        },
    }


def run_probe(root: Path) -> dict[str, Any]:
    packet = sample_packet()
    invocation = invoke_bounded_agent(root, packet)
    if not invocation.get("ok"):
        return {"ok": False, "stage": "invoke", "result": invocation}

    relay = create_agent_relay_message(
        root,
        {
            "invocation_id": invocation["invocation_id"],
            "from_agent": "role.context_cartographer",
            "to": "chatgpt_browser",
            "question_type": "route",
            "question": "Which bounded context ref should be inspected first?",
            "evidence_refs": [invocation["capsule_context_path"]],
        },
    )
    if not relay.get("ok"):
        return {"ok": False, "stage": "relay_create", "invocation": invocation, "result": relay}

    pending = pending_agent_relays(root, invocation_id=invocation["invocation_id"])
    response = respond_agent_relay(
        root,
        {
            "schema_id": "ion.agent_relay_response.v1",
            "relay_id": relay["relay_id"],
            "invocation_id": invocation["invocation_id"],
            "answered_by": "chatgpt_browser",
            "response": "Inspect ion_custom_gpt_action_gateway.py first, then queue runner integration.",
            "authority_delta": None,
            "continue": True,
        },
    )
    settlement = settle_agent_invocation(
        root,
        {
            "schema_id": "ion.agent_invocation_settlement.v1",
            "invocation_id": invocation["invocation_id"],
            "terminal_state": "accepted",
            "settled_by": "chatgpt_browser",
            "summary": "Smoke settlement with capsule and relay evidence.",
            "evidence_refs": [invocation["capsule_context_path"], relay["relay_path"]],
        },
    )
    receipts = recent_agent_invocation_receipts(root, limit=20)

    receipt_rows = receipts.get("receipts", []) if isinstance(receipts.get("receipts"), list) else []
    receipt_count = int(receipts.get("count") or receipts.get("receipt_count") or len(receipt_rows))
    ok = bool(
        invocation.get("ok")
        and relay.get("ok")
        and pending.get("count") == 1
        and response.get("ok")
        and settlement.get("ok")
        and receipt_count >= 5
    )
    return {
        "ok": ok,
        "schema_id": "ion.bounded_agent_lane_smoke_result.v1",
        "root": str(root),
        "mutated_active_connector_queue": False,
        "invocation_id": invocation.get("invocation_id"),
        "capsule_context_path": invocation.get("capsule_context_path"),
        "codex_work_request_path": invocation.get("codex_work_request_path"),
        "relay_id": relay.get("relay_id"),
        "pending_relay_count_before_response": pending.get("count"),
        "relay_response_status": response.get("status"),
        "settlement_status": settlement.get("status"),
        "settlement_path": settlement.get("settlement_path"),
        "receipt_count": receipt_count,
        "receipt_events": [item.get("event") for item in receipt_rows],
        "production_authority": False,
        "live_execution_authority": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Smoke probe the bounded ION agent lane.")
    parser.add_argument("--root", type=Path, help="Optional root to mutate. Omit to use a temporary root.")
    parser.add_argument("--json", action="store_true", help="Print compact JSON.")
    args = parser.parse_args()

    if args.root:
        result = run_probe(args.root.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix="ion_bounded_agent_lane_smoke_") as tmp:
            probe_root = Path(tmp)
            (probe_root / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
            (probe_root / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
            result = run_probe(probe_root)

    print(json.dumps(result, indent=None if args.json else 2, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
