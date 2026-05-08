"""V78 — canonical ION mount contract audit (RELAY-first, STEWARD route, role_phase_sequence)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

_CONTRACT = Path("ION/02_architecture/ION_MOUNT_CONTRACT.md")

_CONTRACT_REQUIRED = (
    ("RELAY", "RELAY_PHASE_OR_RELAY_FIRST"),
    ("STEWARD", "STEWARD_MENTION"),
    ("role_phase_sequence", "ROLE_PHASE_SEQUENCE"),
    ("One carrier may traverse multiple", "ONE_CARRIER_MULTI_ROLE"),
    ("optional", "SUBAGENT_OR_OPTIONAL_MENTION"),
    ("not roles", "SUBAGENT_NOT_ROLES"),
    ("WorkPacket", "WORKPACKET"),
    ("ContextPackage", "CONTEXTPACKAGE"),
    ("template", "TEMPLATE_MENTION"),
    ("receipt", "RECEIPT_MENTION"),
    ("No production authority", "NO_PRODUCTION_AUTHORITY"),
    ("No live execution authority", "NO_LIVE_EXECUTION"),
    ("MINI/CAPSULE are not primary", "MINI_CAPSULE_NOT_PRIMARY"),
    ("selected carrier profile", "SELECTED_CARRIER_PROFILE"),
    ("carrier execution packet template", "CARRIER_EXECUTION_PACKET_TEMPLATE"),
    ("retired from hot mount authority", "ROOT_MARKDOWN_RETIRED_FROM_HOT_AUTHORITY"),
    ("kernel.ion_carrier_continue", "CARRIER_CONTINUE_ENTRYPOINT"),
)

_FORBIDDEN = (
    (re.compile(r"(?i)raw\s+cursor\s+agent\s+decides\s+workflow"), "RAW_CURSOR_AUTHORITY_PHRASE"),
    (re.compile(r"(?i)subagent\s+is\s+role"), "SUBAGENT_AS_ROLE_PHRASE"),
)


def lint_v78_mount_packet_surface(text: str) -> list[str]:
    hits: list[str] = []
    for rx, code in _FORBIDDEN:
        if rx.search(text):
            hits.append(code)
    return sorted(set(hits))


def evaluate_mount_sequence(packet: Mapping[str, Any], root: Path) -> dict[str, Any]:
    """Validate an in-memory mount / cycle sequence packet (V78 shape)."""

    root = root.resolve()
    errors: list[str] = []

    def req(cond: bool, code: str) -> None:
        if not cond:
            errors.append(code)

    corpus = str(packet)
    lint_hits = lint_v78_mount_packet_surface(corpus)
    if lint_hits:
        errors.append(f"FORBIDDEN_PHRASES:{','.join(lint_hits)}")

    seq = packet.get("role_phase_sequence")
    req(isinstance(seq, list) and len(seq) > 0, "MISSING_OR_EMPTY_ROLE_PHASE_SEQUENCE")

    if isinstance(seq, list) and seq:
        roles_upper = [str(r).strip().upper() for r in seq]
        req(roles_upper[0] == "RELAY", "RELAY_NOT_FIRST")
        req(roles_upper[-1] == "RELAY", "RELAY_NOT_LAST_CLOSEOUT")
        req(roles_upper.count("STEWARD") >= 2, "STEWARD_INTEGRATION_PHASE_MISSING_OR_SINGLE_STEWARD_ONLY")

    req(packet.get("production_authority") is False, "PRODUCTION_AUTHORITY_MUST_BE_FALSE")
    req(packet.get("live_execution_authority") is False, "LIVE_EXECUTION_AUTHORITY_MUST_BE_FALSE")
    req(packet.get("mini_capsule_primary_context_authority") is False, "MINI_CAPSULE_PRIMARY_MUST_BE_FALSE")

    if packet.get("subagent_required") is True:
        errors.append("SUBAGENT_REQUIRED_TRUE_CONFLICTS_OPTIONAL_SLOTS_LAW")

    req(packet.get("one_carrier_traverses_multiple_roles") is True, "ONE_CARRIER_MULTI_ROLE_FLAG_REQUIRED")

    phases = packet.get("phases")
    req(isinstance(phases, list) and len(phases) == len(seq or []), "PHASES_LIST_MISMATCH_WITH_SEQUENCE")

    if isinstance(phases, list) and isinstance(seq, list) and len(phases) == len(seq):
        integrate_ok = False
        for i, ph in enumerate(phases):
            if not isinstance(ph, dict):
                errors.append(f"PHASE_{i}_NOT_OBJECT")
                continue
            role = str(ph.get("role") or "").strip().upper()
            exp = str(seq[i]).strip().upper()
            req(role == exp, f"PHASE_{i}_ROLE_MISMATCH")
            wpr = str(ph.get("work_packet_ref") or "").strip()
            cpr = str(ph.get("context_package_ref") or "").strip()
            tpl = str(ph.get("template_path") or ph.get("active_template") or "").strip()
            req(bool(wpr), f"PHASE_{i}_MISSING_WORK_PACKET_REF")
            req(bool(cpr), f"PHASE_{i}_MISSING_CONTEXT_PACKAGE_REF")
            req(bool(tpl), f"PHASE_{i}_MISSING_TEMPLATE_PATH")
            if role == "MASON":
                req(ph.get("outputs_are_proposals") is True, f"PHASE_{i}_MASON_MUST_MARK_PROPOSALS")
            if role == "STEWARD" and ph.get("steward_integrates_proposals") is True:
                integrate_ok = True
            if role == "RELAY" and i == len(phases) - 1:
                rh = str(ph.get("receipt_or_handoff") or ph.get("receipt_required_path") or "").strip()
                req(bool(rh), "FINAL_RELAY_MISSING_RECEIPT_OR_HANDOFF")

        if not integrate_ok:
            errors.append("MISSING_STEWARD_INTEGRATION_FLAG_ON_STEWARD_PHASE")

    return {"accepted": len(errors) == 0, "errors": errors, "root": str(root)}


def _golden_packet(root: Path) -> dict[str, Any]:
    return {
        "carrier_id": "V78-GOLDEN-CARRIER",
        "role_phase_sequence": ["RELAY", "STEWARD", "MASON", "STEWARD", "RELAY"],
        "one_carrier_traverses_multiple_roles": True,
        "subagent_required": False,
        "production_authority": False,
        "live_execution_authority": False,
        "mini_capsule_primary_context_authority": False,
        "phases": [
            {
                "role": "RELAY",
                "work_packet_ref": "ION/docs/cursor/ION_WORK_PACKET_TEMPLATE.md",
                "context_package_ref": "ION/05_context/signals/v78_canonical_mount_demo_packet_20260427.json",
                "template_path": "ION/07_templates/actions/AGENT_SPAWN.md",
            },
            {
                "role": "STEWARD",
                "work_packet_ref": "ION/docs/cursor/ION_WORK_PACKET_TEMPLATE.md",
                "context_package_ref": "ION/05_context/signals/v78_canonical_mount_demo_packet_20260427.json",
                "template_path": "ION/07_templates/README.md",
                "steward_route_decision": "Route to MASON then integrate proposals.",
            },
            {
                "role": "MASON",
                "work_packet_ref": "ION/docs/cursor/ION_WORK_PACKET_TEMPLATE.md",
                "context_package_ref": "ION/05_context/signals/v78_canonical_mount_demo_packet_20260427.json",
                "template_path": "ION/07_templates/actions/CODE.md",
                "outputs_are_proposals": True,
            },
            {
                "role": "STEWARD",
                "work_packet_ref": "ION/docs/cursor/ION_WORK_PACKET_TEMPLATE.md",
                "context_package_ref": "ION/05_context/signals/v78_canonical_mount_demo_packet_20260427.json",
                "template_path": "ION/07_templates/README.md",
                "steward_integrates_proposals": True,
            },
            {
                "role": "RELAY",
                "work_packet_ref": "ION/docs/cursor/ION_WORK_PACKET_TEMPLATE.md",
                "context_package_ref": "ION/05_context/signals/v78_canonical_mount_demo_packet_20260427.json",
                "template_path": "ION/07_templates/README.md",
                "receipt_or_handoff": "ION/docs/consolidation/V78_ION_CANONICAL_MOUNT_CONTRACT_REPORT_20260427.md",
            },
        ],
    }


def audit_v78_ion_mount_contract(root: Path) -> dict[str, Any]:
    """Filesystem + contract text + golden mount-sequence evaluation."""

    root = root.resolve()
    contract_path = root / _CONTRACT
    contract_exists = contract_path.is_file()

    missing_phrases: list[str] = []
    contract_text = ""
    if contract_exists:
        contract_text = contract_path.read_text(encoding="utf-8", errors="replace")
        for needle, code in _CONTRACT_REQUIRED:
            if needle not in contract_text:
                missing_phrases.append(code)

    golden = evaluate_mount_sequence(_golden_packet(root), root)

    ok = (
        contract_exists
        and not missing_phrases
        and golden["accepted"]
        and "Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`."
        in contract_text
    )

    return {
        "audit_id": "v78_ion_mount_contract",
        "root": str(root),
        "mount_contract_path": str(_CONTRACT),
        "mount_contract_exists": contract_exists,
        "contract_required_phrases_missing": missing_phrases,
        "supersession_line_in_contract": "Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`."
        in contract_text,
        "golden_sequence_evaluation": golden,
        "mount_contract_ok": ok,
    }
