"""ION skill activation registry and deterministic selector.

Skills are the ergonomic activation layer for workflows. Templates remain the
proof contracts. This module is intentionally read-only: it projects which
skill should be active for a chat/work turn and exposes the template/context
contracts that still govern acceptance.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:  # pragma: no cover - import availability is environment-specific
    import yaml
except Exception:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


SCHEMA_ID = "ion.skill_activation.v1"
REGISTRY_SCHEMA_ID = "ion.skill_registry.v1"
READY_VERDICT = "ION_SKILL_ACTIVATION_READY"
BLOCKED_VERDICT = "ION_SKILL_ACTIVATION_BLOCKED"

SKILL_REGISTRY_PATH = Path("ION/03_registry/ion_skill_registry.yaml")
SKILL_PROTOCOL_PATH = Path("ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md")

QUEUE_EXECUTION_MODES = {"queue_for_codex", "queue_and_start"}
RECOVERY_TERMS = (
    "wrong root",
    "old root",
    "drift",
    "confusing",
    "confused",
    "failed ui",
    "failure",
    "recover",
    "forensic",
    "forensics",
    "not responding",
    "doesn't respond",
    "does not respond",
    "illogical",
)
TEMPLATE_TERMS = (
    "skill",
    "skills",
    "template",
    "templates",
    "binding",
    "bindings",
    "proof contract",
    "governance",
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _resolve_root(root: str | Path | None = None) -> Path:
    return Path(root or ".").expanduser().resolve()


def _read_yaml(path: Path) -> dict[str, Any] | None:
    if not path.exists() or yaml is None:
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def _as_list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _as_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _skill_id(skill: Mapping[str, Any]) -> str:
    return str(skill.get("skill_id") or "").strip()


def _skills_by_id(registry: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for raw in _as_list(registry.get("skills")):
        if not isinstance(raw, Mapping):
            continue
        skill = dict(raw)
        skill_id = _skill_id(skill)
        if skill_id:
            result[skill_id] = skill
    return result


def load_ion_skill_registry(root: str | Path | None = None) -> dict[str, Any]:
    """Load and validate the active ION skill registry."""

    shell_root = _resolve_root(root)
    registry_path = shell_root / SKILL_REGISTRY_PATH
    protocol_path = shell_root / SKILL_PROTOCOL_PATH
    findings: list[str] = []
    if yaml is None:
        findings.append("pyyaml_unavailable")
    if not protocol_path.exists():
        findings.append(f"skill_protocol_missing:{SKILL_PROTOCOL_PATH.as_posix()}")
    payload = _read_yaml(registry_path)
    if payload is None:
        findings.append(f"skill_registry_missing_or_invalid:{SKILL_REGISTRY_PATH.as_posix()}")
        return {
            "schema_id": REGISTRY_SCHEMA_ID,
            "verdict": BLOCKED_VERDICT,
            "ok": False,
            "generated_at": _now(),
            "registry_path": SKILL_REGISTRY_PATH.as_posix(),
            "protocol_path": SKILL_PROTOCOL_PATH.as_posix(),
            "findings": findings,
            "skills": [],
            "skill_count": 0,
            "production_authority": False,
            "live_execution_authority": False,
            "secrets_authority": False,
        }

    if payload.get("schema_id") != REGISTRY_SCHEMA_ID:
        findings.append("skill_registry_schema_id_unexpected")
    for key in ("production_authority", "live_execution_authority", "secrets_authority"):
        if payload.get(key) is not False:
            findings.append(f"{key}_must_be_false")

    normalized_skills: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in _as_list(payload.get("skills")):
        if not isinstance(raw, Mapping):
            findings.append("skill_entry_not_object")
            continue
        skill = dict(raw)
        skill_id = _skill_id(skill)
        if not skill_id:
            findings.append("skill_id_missing")
            continue
        if skill_id in seen:
            findings.append(f"skill_id_duplicate:{skill_id}")
            continue
        seen.add(skill_id)
        if not _as_list(skill.get("activates_templates")):
            findings.append(f"skill_templates_missing:{skill_id}")
        authority = _as_dict(skill.get("allowed_authority"))
        for key in ("production_authority", "live_execution_authority", "secrets_authority"):
            if authority.get(key) is not False:
                findings.append(f"skill_{key}_must_be_false:{skill_id}")
        proof = _as_dict(skill.get("proof_contract"))
        if proof.get("context_proof_required") is not True:
            findings.append(f"skill_context_proof_not_required:{skill_id}")
        normalized_skills.append(skill)

    ok = not findings
    return {
        **payload,
        "schema_id": REGISTRY_SCHEMA_ID,
        "verdict": READY_VERDICT if ok else BLOCKED_VERDICT,
        "ok": ok,
        "generated_at": _now(),
        "registry_path": SKILL_REGISTRY_PATH.as_posix(),
        "protocol_path": SKILL_PROTOCOL_PATH.as_posix(),
        "findings": findings,
        "skills": normalized_skills,
        "skill_count": len(normalized_skills),
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }


def choose_ion_skill(
    registry: Mapping[str, Any],
    *,
    lane_id: str,
    objective: str,
    execution_mode: str | None = None,
    requested_skill_id: str | None = None,
) -> tuple[dict[str, Any] | None, str]:
    """Choose a skill deterministically from lane, execution mode, and text."""

    skills = _skills_by_id(registry)
    if requested_skill_id:
        skill = skills.get(requested_skill_id)
        if skill:
            return skill, "operator_or_callsite_requested_skill"
        return None, f"requested_skill_unknown:{requested_skill_id}"

    text = str(objective or "").lower()
    mode = str(execution_mode or "").strip()
    selected = "codex-chat-answer"
    reason = "default_respond_only_codex_chat"
    if lane_id == "ion_system":
        selected = "ion-full-workflow-handoff"
        reason = "ion_lane_uses_existing_full_ion_handoff"
    elif any(term in text for term in RECOVERY_TERMS):
        selected = "codex-recovery"
        reason = "recovery_trigger_detected"
    elif mode in QUEUE_EXECUTION_MODES:
        selected = "codex-solo-work"
        reason = "codex_queue_execution_mode"
    elif any(term in text for term in TEMPLATE_TERMS):
        selected = "template-curation"
        reason = "skill_template_governance_language_detected"
    return skills.get(selected), reason


def _package_ref_index(codex_solo_context: Mapping[str, Any] | None) -> dict[str, list[str]]:
    context = codex_solo_context if isinstance(codex_solo_context, Mapping) else {}
    package_model = context.get("context_packages") if isinstance(context.get("context_packages"), Mapping) else {}
    packages = package_model.get("packages") if isinstance(package_model.get("packages"), list) else []
    refs: dict[str, list[str]] = {}
    for raw in packages:
        if not isinstance(raw, Mapping):
            continue
        package_id = str(raw.get("package_id") or "").strip()
        path_refs = [str(ref) for ref in _as_list(raw.get("path_refs")) if ref]
        if package_id:
            refs[package_id] = path_refs
    return refs


def _refs_for_packages(codex_solo_context: Mapping[str, Any] | None, package_ids: list[str]) -> list[str]:
    indexed = _package_ref_index(codex_solo_context)
    refs: list[str] = []
    for package_id in package_ids:
        for ref in indexed.get(package_id, []):
            if ref not in refs:
                refs.append(ref)
    return refs


def build_ion_skill_activation(
    root: str | Path | None = None,
    *,
    lane_id: str,
    objective: str,
    execution_mode: str | None = None,
    codex_solo_context: Mapping[str, Any] | None = None,
    model_move: Mapping[str, Any] | None = None,
    requested_skill_id: str | None = None,
) -> dict[str, Any]:
    """Build a read-only skill activation record for a turn or model refresh."""

    registry = load_ion_skill_registry(root)
    skill, reason = choose_ion_skill(
        registry,
        lane_id=lane_id,
        objective=objective,
        execution_mode=execution_mode,
        requested_skill_id=requested_skill_id,
    )
    if skill is None:
        return {
            "schema_id": SCHEMA_ID,
            "verdict": BLOCKED_VERDICT,
            "ok": False,
            "generated_at": _now(),
            "selection_reason": reason,
            "registry": {
                "ok": registry.get("ok"),
                "registry_path": registry.get("registry_path"),
                "protocol_path": registry.get("protocol_path"),
                "findings": registry.get("findings", []),
            },
            "production_authority": False,
            "live_execution_authority": False,
            "secrets_authority": False,
        }

    context_mount = _as_dict(skill.get("context_mount"))
    default_mount = _as_dict(registry.get("default_context_mount"))
    required_packages = [
        str(value)
        for value in _as_list(context_mount.get("required_packages") or default_mount.get("required_packages"))
        if value
    ]
    route_deeper_packages = [
        str(value)
        for value in _as_list(context_mount.get("route_deeper_packages") or default_mount.get("route_deeper_packages"))
        if value
    ]
    selected_model = (model_move or {}).get("selected_model") or skill.get("preferred_model")
    reasoning = (model_move or {}).get("selected_reasoning_effort") or skill.get("default_reasoning_effort")
    proof_contract = {
        **_as_dict(registry.get("global_proof_contract")),
        **_as_dict(skill.get("proof_contract")),
    }
    authority = {
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
        **_as_dict(skill.get("allowed_authority")),
    }
    authority["production_authority"] = False
    authority["live_execution_authority"] = False
    authority["secrets_authority"] = False
    activation = {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT if registry.get("ok") else BLOCKED_VERDICT,
        "ok": bool(registry.get("ok")),
        "generated_at": _now(),
        "skill_id": skill.get("skill_id"),
        "display_name": skill.get("display_name"),
        "skill_class": skill.get("class"),
        "purpose": skill.get("purpose"),
        "selection_reason": reason,
        "lane_id": lane_id,
        "execution_mode": execution_mode,
        "context_mount": {
            "required_packages": required_packages,
            "route_deeper_packages": route_deeper_packages,
            "required_refs": _refs_for_packages(codex_solo_context, required_packages),
            "route_deeper_refs": _refs_for_packages(codex_solo_context, route_deeper_packages),
        },
        "model_route": {
            "model_stage_id": skill.get("model_stage_id"),
            "preferred_model": skill.get("preferred_model"),
            "default_reasoning_effort": skill.get("default_reasoning_effort"),
            "selected_model": selected_model,
            "selected_reasoning_effort": reasoning,
            "model_move": dict(model_move) if isinstance(model_move, Mapping) else None,
        },
        "activates_templates": [str(value) for value in _as_list(skill.get("activates_templates")) if value],
        "template_bindings": [str(value) for value in _as_list(skill.get("template_bindings")) if value],
        "proof_contract": proof_contract,
        "authority": authority,
        "ui": _as_dict(skill.get("ui")),
        "registry": {
            "registry_path": registry.get("registry_path"),
            "protocol_path": registry.get("protocol_path"),
            "findings": registry.get("findings", []),
            "principle": registry.get("principle"),
        },
        "state_acceptance_granted": False,
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }
    return json.loads(json.dumps(activation))


def build_ion_skill_surface(
    root: str | Path | None = None,
    *,
    lane_id: str = "codex_general",
    objective: str = "model refresh",
    execution_mode: str = "respond_only",
    codex_solo_context: Mapping[str, Any] | None = None,
    model_move: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    registry = load_ion_skill_registry(root)
    current = build_ion_skill_activation(
        root,
        lane_id=lane_id,
        objective=objective,
        execution_mode=execution_mode,
        codex_solo_context=codex_solo_context,
        model_move=model_move,
    )
    skill_cards = []
    for skill in _as_list(registry.get("skills")):
        if not isinstance(skill, Mapping):
            continue
        authority = _as_dict(skill.get("allowed_authority"))
        skill_cards.append({
            "skill_id": skill.get("skill_id"),
            "display_name": skill.get("display_name"),
            "class": skill.get("class"),
            "purpose": skill.get("purpose"),
            "trigger_summary": skill.get("trigger_summary"),
            "label": _as_dict(skill.get("ui")).get("label"),
            "activates_templates": [str(value) for value in _as_list(skill.get("activates_templates")) if value],
            "template_binding_count": len(_as_list(skill.get("template_bindings"))),
            "queue_work": authority.get("queue_work", False),
            "write_files": authority.get("write_files", False),
            "production_authority": False,
            "live_execution_authority": False,
        })
    return {
        "schema_id": "ion.skill_surface.v1",
        "verdict": registry.get("verdict"),
        "ok": registry.get("ok"),
        "registry_path": registry.get("registry_path"),
        "protocol_path": registry.get("protocol_path"),
        "principle": registry.get("principle"),
        "skill_count": len(skill_cards),
        "skills": skill_cards,
        "current_activation": current,
        "findings": registry.get("findings", []),
        "policy": "skills_activate_templates_templates_gate_proof",
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }
