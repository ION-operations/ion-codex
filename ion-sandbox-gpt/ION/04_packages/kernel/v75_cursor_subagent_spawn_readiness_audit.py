"""V75 — Cursor subagent spawn readiness (RELAY → STEWARD → named role mount)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from .cursor_subagent_ion_role_registry import validate_cursor_subagent_role_packet

_TEMPLATE = Path("ION/docs/cursor/ION_SUBAGENT_SPAWN_PACKET_TEMPLATE.md")
_GUIDE = Path("ION/docs/cursor/ION_SUBAGENT_SPAWN_READINESS_GUIDE.md")
_SCHEMA = Path("ION/03_registry/cursor_subagent_role_mount.schema.json")
_PROTOCOL = Path("ION/02_architecture/ION_CURSOR_FULL_WORKFLOW_MOUNT_PROTOCOL.md")
_FW_GUIDE = Path("ION/docs/cursor/CURSOR_FULL_WORKFLOW_MOUNT_GUIDE.md")
_FW_RULE = Path(".cursor/rules/ion-full-workflow-mount.mdc")
_LIVE = Path("ION/docs/cursor/ION_LIVE_WORKFLOW_STATUS_PACKET.md")

_DEMO_SPAWN_MASON = Path("ION/05_context/signals/v75_spawn_packet_mason_structure_audit_20260427.md")
_DEMO_SPAWN_VEST = Path("ION/05_context/signals/v75_spawn_packet_vestige_provenance_audit_20260427.md")
_DEMO_RET_MASON = Path("ION/05_context/signals/v75_spawn_return_mason_structure_audit_20260427.md")
_DEMO_RET_VEST = Path("ION/05_context/signals/v75_spawn_return_vestige_provenance_audit_20260427.md")
_DEMO_RECEIPT = Path("ION/05_context/signals/v75_steward_spawn_integration_receipt_20260427.txt")
_DEMO_RELAY = Path("ION/05_context/signals/v75_relay_spawn_report_20260427.md")

def _stack_documented(text: str) -> bool:
    lc = text.lower()
    return (
        "relay" in lc
        and "steward" in lc
        and "spawn" in lc
        and ("named ion role" in lc or "named role" in lc)
        and ("context package" in lc or "contextpackage" in lc.replace(" ", ""))
        and ("work packet" in lc or "workpacket" in lc.replace(" ", ""))
        and "proposal" in lc
    )

_GENERIC_SUBAGENT_PATTERNS = (
    (re.compile(r"(?i)\bjust\s+a\s+subagent\b"), "GENERIC_SUBAGENT_LANGUAGE"),
    (re.compile(r"(?i)\bonly\s+a\s+subagent\b"), "GENERIC_SUBAGENT_LANGUAGE"),
)

_ROLE_CONFUSION_PATTERNS = (
    (re.compile(r"(?i)\bsubagent\s+is\s+the\s+role\b"), "SUBAGENT_AS_ROLE_LANGUAGE"),
    (re.compile(r"(?i)\bsubagent\s*=\s*role\b"), "SUBAGENT_AS_ROLE_LANGUAGE"),
)


def lint_v75_spawn_prompt_surface(text: str) -> list[str]:
    """Return violation codes if ``text`` contains forbidden generic / conflation language."""

    violations: list[str] = []
    for rx, code in _GENERIC_SUBAGENT_PATTERNS:
        if rx.search(text):
            violations.append(code)
    for rx, code in _ROLE_CONFUSION_PATTERNS:
        if rx.search(text):
            violations.append(code)
    return sorted(set(violations))


def evaluate_v75_spawn_packet(root: Path, packet: Mapping[str, Any]) -> dict[str, Any]:
    """Strict gate for in-memory spawn packet dicts (tests + tooling)."""

    root = root.resolve()
    errors: list[str] = []

    child = packet.get("child_mount")
    mission = packet.get("mission_packet")
    integration = packet.get("integration")
    parent = packet.get("parent_mount")

    if not isinstance(parent, dict):
        errors.append("MISSING_PARENT_MOUNT")
    else:
        if parent.get("carrier") != "cursor_parent_chat":
            errors.append("PARENT_CARRIER_INVALID")
        if parent.get("mounted_role") != "STEWARD":
            errors.append("PARENT_MOUNTED_ROLE_NOT_STEWARD")
        if not str(parent.get("relay_packet_id") or "").strip():
            errors.append("MISSING_RELAY_PACKET_ID")
        if parent.get("authority_level") != "TASK_SCOPED_LOCAL_ORCHESTRATION":
            errors.append("PARENT_AUTHORITY_LEVEL_INVALID")

    if not isinstance(child, dict):
        errors.append("MISSING_CHILD_MOUNT")
    else:
        if child.get("carrier") != "cursor_subagent":
            errors.append("CHILD_CARRIER_INVALID")
        agent = str(child.get("agent_name") or "").strip().upper().replace("-", "_")
        if not agent:
            errors.append("MISSING_AGENT_NAME")
        rb = str(child.get("role_boot") or "").strip().replace("\\", "/")
        if not rb:
            errors.append("MISSING_ROLE_BOOT")
        elif "ION/03_registry/boots/" not in rb or not rb.endswith(".boot.md"):
            errors.append("ROLE_BOOT_PATH_INVALID")
        else:
            boot_file = root / rb
            if not boot_file.is_file():
                errors.append("ROLE_BOOT_MISSING_NEEDS_REVIEW")
            elif agent:
                vr = validate_cursor_subagent_role_packet(root=root, agent_name=agent)
                if not vr.get("packet_ok"):
                    errors.append("AGENT_NAME_NOT_IN_BOOT_REGISTRY")
        mid = str(child.get("mounted_identity") or "").strip().upper().replace("-", "_")
        if agent and mid and mid != agent:
            errors.append("MOUNTED_IDENTITY_MISMATCH")
        if child.get("mounted_by") != "local_STEWARD_carrier":
            errors.append("MOUNTED_BY_NOT_LOCAL_STEWARD_CARRIER")
        if child.get("production_authority") is True:
            errors.append("PRODUCTION_AUTHORITY_FORBIDDEN")
        if child.get("live_execution_authority") is True:
            errors.append("LIVE_EXECUTION_AUTHORITY_FORBIDDEN")

    if not isinstance(mission, dict):
        errors.append("MISSING_MISSION_PACKET")
    else:
        ctx = mission.get("context_package")
        if ctx is None or (isinstance(ctx, str) and not str(ctx).strip()):
            errors.append("MISSING_CONTEXT_PACKAGE")
        ap = mission.get("allowed_paths")
        fp = mission.get("forbidden_paths")
        if not isinstance(ap, list) or len(ap) == 0:
            errors.append("MISSING_OR_EMPTY_ALLOWED_PATHS")
        if not isinstance(fp, list) or len(fp) == 0:
            errors.append("MISSING_OR_EMPTY_FORBIDDEN_PATHS")
        rc = mission.get("return_contract")
        if rc is None:
            errors.append("MISSING_RETURN_CONTRACT")
        elif isinstance(rc, list) and len(rc) == 0:
            errors.append("MISSING_RETURN_CONTRACT")
        elif isinstance(rc, str) and not rc.strip():
            errors.append("MISSING_RETURN_CONTRACT")
        if not str(mission.get("objective") or "").strip():
            errors.append("MISSING_OBJECTIVE")
        if not str(mission.get("workstream") or "").strip():
            errors.append("MISSING_WORKSTREAM")
        vr_cmds = mission.get("validation_commands")
        if not isinstance(vr_cmds, list) or len(vr_cmds) == 0:
            errors.append("MISSING_VALIDATION_COMMANDS")

    if not isinstance(integration, dict):
        errors.append("MISSING_INTEGRATION")
    else:
        if integration.get("steward_integration_required") is not True:
            errors.append("STEWARD_INTEGRATION_NOT_REQUIRED")
        if integration.get("relay_report_required") is not True:
            errors.append("RELAY_REPORT_NOT_REQUIRED")

    return {
        "accepted": len(errors) == 0,
        "errors": errors,
    }


def _read(root: Path, rel: Path) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="replace")


def _demo_spawn_integrity(text: str, role: str) -> bool:
    checks = (
        "spawn_packet_id:",
        "parent_mount:",
        "child_mount:",
        "mission_packet:",
        "allowed_paths:",
        "forbidden_paths:",
        "return_contract:",
        "production_authority: false",
        "live_execution_authority: false",
        "mounted_by: local_STEWARD_carrier",
        "PENDING_STEWARD_REVIEW",
        f"agent_name: {role}",
        f"ION/03_registry/boots/{role}.boot.md",
    )
    return all(c in text for c in checks)


def audit_v75_cursor_subagent_spawn_readiness(root: Path) -> dict[str, Any]:
    """Filesystem + law checks for V75 subagent spawn readiness."""

    root = root.resolve()
    paths = {
        "template": _TEMPLATE,
        "guide": _GUIDE,
        "schema": _SCHEMA,
        "full_workflow_protocol": _PROTOCOL,
        "full_workflow_guide": _FW_GUIDE,
        "full_workflow_rule": _FW_RULE,
        "live_workflow_status_packet": _LIVE,
    }
    missing = [str(p) for p in paths.values() if not (root / p).is_file()]

    protocol_ok = False
    rule_ok = False
    if (root / _PROTOCOL).is_file():
        protocol_ok = _stack_documented(_read(root, _PROTOCOL))
    if (root / _FW_RULE).is_file():
        rule_lc = _read(root, _FW_RULE).lower()
        rule_ok = (
            "named ion role" in rule_lc or "named role" in rule_lc
        ) and "carrier slot" in rule_lc and "relay" in rule_lc and "steward" in rule_lc

    demos = (
        _DEMO_SPAWN_MASON,
        _DEMO_SPAWN_VEST,
        _DEMO_RET_MASON,
        _DEMO_RET_VEST,
        _DEMO_RECEIPT,
        _DEMO_RELAY,
    )
    demo_missing = [str(p) for p in demos if not (root / p).is_file()]

    demo_mason_ok = False
    demo_vest_ok = False
    if (root / _DEMO_SPAWN_MASON).is_file():
        demo_mason_ok = _demo_spawn_integrity(_read(root, _DEMO_SPAWN_MASON), "MASON")
    if (root / _DEMO_SPAWN_VEST).is_file():
        demo_vest_ok = _demo_spawn_integrity(_read(root, _DEMO_SPAWN_VEST), "VESTIGE")

    synthetic = {
        "reject_generic_subagent_language": len(lint_v75_spawn_prompt_surface("This is just a subagent.")) > 0,
        "reject_subagent_as_role_language": len(lint_v75_spawn_prompt_surface("The subagent is the role here.")) > 0,
        "reject_missing_context": not evaluate_v75_spawn_packet(
            root,
            _minimal_valid_packet(root, clear_context=True),
        )["accepted"],
        "reject_missing_paths": not evaluate_v75_spawn_packet(
            root,
            _minimal_valid_packet(root, clear_paths=True),
        )["accepted"],
        "reject_production_authority": not evaluate_v75_spawn_packet(
            root,
            _minimal_valid_packet(root, prod=True),
        )["accepted"],
        "reject_live_execution_authority": not evaluate_v75_spawn_packet(
            root,
            _minimal_valid_packet(root, live=True),
        )["accepted"],
    }

    gaps: list[str] = []
    if missing:
        gaps.append(f"missing_paths:{missing}")
    if not protocol_ok:
        gaps.append("full_workflow_protocol_stack_incomplete")
    if not rule_ok:
        gaps.append("full_workflow_rule_mount_language_incomplete")
    if demo_missing:
        gaps.append(f"demo_missing:{demo_missing}")
    if not demo_mason_ok:
        gaps.append("demo_mason_integrity_failed")
    if not demo_vest_ok:
        gaps.append("demo_vestige_integrity_failed")

    synthetic_ok = all(synthetic.values())
    structural_ok = (
        not missing
        and protocol_ok
        and rule_ok
        and not demo_missing
        and demo_mason_ok
        and demo_vest_ok
    )

    if structural_ok and synthetic_ok:
        verdict = "ION_SUBAGENT_SPAWN_READY"
    elif structural_ok:
        verdict = "ION_SUBAGENT_SPAWN_READY_WITH_GAPS"
    else:
        verdict = "ION_SUBAGENT_SPAWN_FAILED"

    return {
        "audit_id": "v75_cursor_subagent_spawn_readiness",
        "root": str(root),
        "spawn_template_exists": (root / _TEMPLATE).is_file(),
        "spawn_readiness_guide_exists": (root / _GUIDE).is_file(),
        "schema_exists": (root / _SCHEMA).is_file(),
        "full_workflow_protocol_ok": protocol_ok,
        "full_workflow_rule_ok": rule_ok,
        "demo_spawn_mason_ok": demo_mason_ok,
        "demo_spawn_vestige_ok": demo_vest_ok,
        "demo_files_missing": demo_missing,
        "synthetic_checks": synthetic,
        "production_authority": False,
        "live_execution_authorized": False,
        "missing_paths": missing,
        "gaps": gaps,
        "verdict": verdict,
    }


def _minimal_valid_packet(
    root: Path,
    *,
    clear_context: bool = False,
    clear_paths: bool = False,
    prod: bool = False,
    live: bool = False,
) -> dict[str, Any]:
    """Build a nearly-valid packet for negative tests."""

    p: dict[str, Any] = {
        "spawn_packet_id": "TEST",
        "parent_mount": {
            "carrier": "cursor_parent_chat",
            "mounted_role": "STEWARD",
            "relay_packet_id": "RELAY-TEST",
            "authority_level": "TASK_SCOPED_LOCAL_ORCHESTRATION",
        },
        "child_mount": {
            "carrier": "cursor_subagent",
            "agent_name": "MASON",
            "role_boot": "ION/03_registry/boots/MASON.boot.md",
            "mounted_identity": "MASON",
            "mounted_by": "local_STEWARD_carrier",
            "authority_level": "READ_ONLY",
            "production_authority": True if prod else False,
            "live_execution_authority": bool(live),
        },
        "mission_packet": {
            "objective": "test",
            "workstream": "implementation",
            "context_package": "" if clear_context else "compiled context",
            "required_reads": ["ION/REPO_AUTHORITY.md"],
            "active_template": "ION/07_templates/actions/CODE.md",
            "allowed_paths": [] if clear_paths else ["ION/**"],
            "forbidden_paths": [] if clear_paths else ["**/credentials/**"],
            "blocked_actions": ["external_api"],
            "validation_commands": ["PYTHONPATH=ION/04_packages python3 -m pytest ION/tests/test_x.py -q"],
            "return_contract": ["findings", "risks"],
            "receipt_requirement": "signals",
        },
        "integration": {
            "proposal_status": "PENDING_STEWARD_REVIEW",
            "steward_integration_required": True,
            "relay_report_required": True,
            "persona_visible_update_required": False,
        },
    }
    return p
