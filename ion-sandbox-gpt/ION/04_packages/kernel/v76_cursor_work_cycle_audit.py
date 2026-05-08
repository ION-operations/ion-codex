"""V76 — Cursor work-cycle packet audit (RELAY → STEWARD → role carriers → RELAY)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

_TEMPLATE = Path("ION/docs/cursor/ION_CURSOR_WORK_CYCLE_PACKET.md")

_DEMO_SIGNALS = (
    Path("ION/05_context/signals/v76_relay_work_cycle_input_20260427.md"),
    Path("ION/05_context/signals/v76_steward_route_decision_20260427.md"),
    Path("ION/05_context/signals/v76_role_carrier_return_proposal_20260427.md"),
    Path("ION/05_context/signals/v76_steward_integration_receipt_20260427.txt"),
    Path("ION/05_context/signals/v76_relay_visible_workflow_report_20260427.md"),
)

_PERSONA_BOOT = Path("ION/03_registry/boots/PERSONA_INTERFACE.boot.md")

_FORBIDDEN = (
    (re.compile(r"(?i)raw\s+cursor\s+agent\s+decides\s+workflow"), "RAW_CURSOR_AUTHORITY_PHRASE"),
    (re.compile(r"(?i)subagent\s+is\s+role"), "SUBAGENT_AS_ROLE_PHRASE"),
    (re.compile(r"(?i)\bLIVE_EXECUTED\b"), "LIVE_EXECUTED_PHRASE"),
    (re.compile(r"(?i)production\s+ready"), "PRODUCTION_READY_PHRASE"),
    (re.compile(r"(?i)live\s+MCP\s+execution"), "LIVE_MCP_EXECUTION_PHRASE"),
)


def lint_v76_work_cycle_surface(text: str) -> list[str]:
    """Return violation codes if ``text`` contains forbidden workflow narrative."""

    hits: list[str] = []
    for rx, code in _FORBIDDEN:
        if rx.search(text):
            hits.append(code)
    return sorted(set(hits))


def evaluate_v76_work_cycle_packet(packet: Mapping[str, Any], root: Path) -> dict[str, Any]:
    """Validate one in-memory work-cycle packet dict."""

    root = root.resolve()
    errors: list[str] = []

    def req(key: str, cond: bool, code: str) -> None:
        if not cond:
            errors.append(code)

    req("cycle_id", bool(str(packet.get("cycle_id") or "").strip()), "MISSING_CYCLE_ID")
    layer = str(packet.get("active_visible_layer") or "").strip().upper()
    req("active_visible_layer", layer in ("RELAY", "PERSONA"), "INVALID_ACTIVE_VISIBLE_LAYER")

    if layer == "PERSONA":
        ps = str(packet.get("persona_surface_ref") or "").strip()
        req("persona_surface_ref", bool(ps), "MISSING_PERSONA_SURFACE_REF")
        if ps and not (root / ps.replace("\\", "/")).is_file():
            errors.append("PERSONA_SURFACE_REF_NOT_ON_DISK")
        if not (root / _PERSONA_BOOT).is_file():
            errors.append("PERSONA_BOOT_MISSING_USE_RELAY")

    req("relay_input_summary", bool(str(packet.get("relay_input_summary") or "").strip()), "MISSING_RELAY_INPUT_SUMMARY")
    req("steward_route_decision", bool(str(packet.get("steward_route_decision") or "").strip()), "MISSING_STEWARD_ROUTE_DECISION")
    req("relay_return_summary", bool(str(packet.get("relay_return_summary") or "").strip()), "MISSING_RELAY_RETURN_SUMMARY")

    if packet.get("production_authority") is not False:
        errors.append("PRODUCTION_AUTHORITY_MUST_BE_FALSE")
    if packet.get("live_execution_authority") is not False:
        errors.append("LIVE_EXECUTION_AUTHORITY_MUST_BE_FALSE")

    carriers = packet.get("mounted_role_carriers")
    none_required = packet.get("mounted_role_carriers_none_required") is True
    if not isinstance(carriers, list):
        errors.append("MOUNTED_ROLE_CARRIERS_NOT_LIST")
    elif len(carriers) == 0 and not none_required:
        errors.append("MISSING_ROLE_CARRIERS_OR_NONE_REQUIRED_FLAG")
    elif len(carriers) > 0:
        for i, c in enumerate(carriers):
            if not isinstance(c, dict):
                errors.append(f"CARRIER_{i}_NOT_OBJECT")
                continue
            agent = str(c.get("agent_name") or c.get("role") or "").strip()
            spr = str(c.get("spawn_packet_ref") or "").strip()
            wpr = str(c.get("work_packet_ref") or "").strip()
            req(f"carrier_{i}_agent", bool(agent), f"CARRIER_{i}_MISSING_AGENT_NAME")
            req(f"carrier_{i}_packet", bool(spr or wpr), f"CARRIER_{i}_MISSING_SPAWN_OR_WORK_PACKET_REF")

    asp = packet.get("active_spawn_packets")
    if not isinstance(asp, list):
        errors.append("ACTIVE_SPAWN_PACKETS_NOT_LIST")

    at = packet.get("active_templates")
    if not isinstance(at, list):
        errors.append("ACTIVE_TEMPLATES_NOT_LIST")

    ap = packet.get("allowed_paths")
    fp = packet.get("forbidden_paths")
    if not isinstance(ap, list) or len(ap) == 0:
        errors.append("MISSING_OR_EMPTY_ALLOWED_PATHS")
    if not isinstance(fp, list) or len(fp) == 0:
        errors.append("MISSING_OR_EMPTY_FORBIDDEN_PATHS")

    vc = packet.get("validation_commands")
    if not isinstance(vc, list) or len(vc) == 0:
        errors.append("MISSING_VALIDATION_COMMANDS")

    pp = packet.get("pending_proposals")
    if not isinstance(pp, list):
        errors.append("PENDING_PROPOSALS_NOT_LIST")

    sid = str(packet.get("steward_integration_decision") or "").strip()
    if not sid:
        errors.append("MISSING_STEWARD_INTEGRATION_DECISION")
    elif len(sid) < 3:
        errors.append("STEWARD_INTEGRATION_DECISION_TOO_SHORT")

    if isinstance(pp, list) and pp:
        for i, p in enumerate(pp):
            if isinstance(p, dict) and p.get("integrated") is True and "NO_PENDING" in sid.upper():
                errors.append("PROPOSAL_MARKED_INTEGRATED_CONFLICTS_WITH_DECISION")

    if "next_visible_update_for_braden" not in packet:
        errors.append("MISSING_NEXT_VISIBLE_UPDATE_FOR_BRADEN")

    corpus = str(packet)
    lint_hits = lint_v76_work_cycle_surface(corpus)
    if lint_hits:
        errors.append(f"FORBIDDEN_PHRASES:{','.join(lint_hits)}")

    return {"accepted": len(errors) == 0, "errors": errors}


def _golden_packet(root: Path) -> dict[str, Any]:
    return {
        "cycle_id": "V76-20260427-GOLDEN",
        "active_visible_layer": "RELAY",
        "relay_input_summary": "Relay ingested operator objective for V76 work-cycle audit wiring.",
        "steward_route_decision": "Route: RELAY intake → STEWARD gate → MASON read-only packet → RELAY report.",
        "mounted_role_carriers": [
            {
                "agent_name": "MASON",
                "work_packet_ref": "ION/docs/cursor/ION_WORK_PACKET_TEMPLATE.md",
            }
        ],
        "active_spawn_packets": [],
        "active_templates": ["ION/07_templates/actions/CODE.md"],
        "allowed_paths": ["ION/docs/cursor/**", "ION/05_context/signals/**"],
        "forbidden_paths": ["**/credentials/**", "**/.env"],
        "validation_commands": [
            "PYTHONPATH=ION/04_packages python3 -m pytest ION/tests/test_kernel_v76_cursor_work_cycle_audit.py -q"
        ],
        "pending_proposals": [
            {"proposal_id": "V76-DEMO-1", "status": "AWAITING_STEWARD", "integrated": False}
        ],
        "steward_integration_decision": "ACCEPT_DEMO_PROPOSALS_WITNESS_ONLY_NO_PRODUCTION",
        "relay_return_summary": "Relay closes cycle with visible workflow report path below.",
        "next_visible_update_for_braden": "See ION/05_context/signals/v76_relay_visible_workflow_report_20260427.md",
        "production_authority": False,
        "live_execution_authority": False,
    }


def audit_v76_cursor_work_cycle(root: Path) -> dict[str, Any]:
    """Filesystem checks + golden packet evaluation + demo signal presence."""

    root = root.resolve()
    missing_template = not (root / _TEMPLATE).is_file()
    missing_demos = [str(p) for p in _DEMO_SIGNALS if not (root / p).is_file()]

    # Lint demo / signal artifacts only — the normative template may cite forbidden
    # examples verbatim for operators and must not fail the repo audit on that basis.
    corpus = ""
    for rel in _DEMO_SIGNALS:
        if (root / rel).is_file():
            corpus += (root / rel).read_text(encoding="utf-8", errors="replace")

    lint_template = lint_v76_work_cycle_surface(corpus)
    golden = evaluate_v76_work_cycle_packet(_golden_packet(root), root)

    ok = (
        not missing_template
        and not missing_demos
        and not lint_template
        and golden["accepted"]
    )

    return {
        "audit_id": "v76_cursor_work_cycle",
        "root": str(root),
        "work_cycle_template_exists": not missing_template,
        "demo_signals_present": not bool(missing_demos),
        "demo_signals_missing": missing_demos,
        "template_lint_violations": lint_template,
        "golden_packet_evaluation": golden,
        "production_authority": False,
        "live_execution_authorized": False,
        "work_cycle_ok": ok,
    }
