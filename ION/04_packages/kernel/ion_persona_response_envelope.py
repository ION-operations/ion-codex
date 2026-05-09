"""Persona-visible response envelope for ION front-door chat.

This module turns route metadata and expressive telemetry into an inspectable
persona block suitable for user-facing chat. The "inner_monologue" field is
explicitly operator-visible persona telemetry, not hidden chain-of-thought or a
claim of private consciousness.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from typing import Any

from .expressive_telemetry import (
    FORBIDDEN_CLAIMS,
    build_expressive_telemetry_binding,
    validate_expressive_telemetry_binding,
)

SCHEMA_ID = "ion.persona_response_envelope.v0_1"
READY_VERDICT = "ION_PERSONA_RESPONSE_ENVELOPE_READY"


def build_persona_response_envelope(
    *,
    user_response: str,
    route: dict[str, Any] | None = None,
    visible_persona_name: str = "ION Persona",
    persona_role_ref: str = "role.persona_interface",
    claim_class: str = "C2",
    emission_permission: str = "MAY_EMIT_AS_PROPOSAL",
    conversation_status: str = "OPEN_PROVISIONAL",
    risk_level: str = "MEDIUM",
    certainty: str = "LOW",
    created_at: str | None = None,
) -> dict[str, Any]:
    """Build the inspectable persona envelope for a single visible response."""
    emitted_at = created_at or _utc_now()
    telemetry = build_expressive_telemetry_binding(
        claim_class=claim_class,
        emission_permission=emission_permission,
        conversation_status=conversation_status,
        risk_level=risk_level,
        certainty=certainty,
        emitted_at=emitted_at,
    )
    route_data = route if isinstance(route, dict) else {}
    dynamic = route_data.get("dynamic_domain_agent_proposal") if isinstance(route_data.get("dynamic_domain_agent_proposal"), dict) else {}
    route_id = route_data.get("route_id")
    response_id = _stable_id(
        "persona-envelope",
        emitted_at,
        visible_persona_name,
        persona_role_ref,
        str(route_id or ""),
        user_response,
    )
    envelope = {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT,
        "ok": True,
        "response_id": response_id,
        "created_at": emitted_at,
        "persona": {
            "visible_name": visible_persona_name,
            "role_ref": persona_role_ref,
            "surface": "front_door_persona_response",
            "persona_is_total_ion": False,
        },
        "route": {
            "route_id": route_id,
            "selection_basis": route_data.get("selection_basis"),
            "candidate_domains": _as_string_list(route_data.get("candidate_domains")),
            "candidate_agents": _as_string_list(route_data.get("candidate_agents")),
        },
        "dynamic_domain_signal": _dynamic_domain_signal(dynamic),
        "confidence": _confidence_payload(
            certainty=telemetry.certainty,
            risk_level=telemetry.risk_level,
            claim_class=telemetry.claim_class,
            emission_permission=telemetry.emission_permission,
            route_id=str(route_id or "unrouted"),
            dynamic_needed=bool(dynamic.get("needed")) if isinstance(dynamic, dict) else False,
        ),
        "gesture": _gesture_payload(
            tone_profile=telemetry.tone_profile,
            pace_profile=telemetry.pace_profile,
            hesitation_level=telemetry.hesitation_level,
            risk_level=telemetry.risk_level,
        ),
        "inner_monologue": {
            "type": "operator_visible_persona_signal_not_hidden_reasoning",
            "text": _persona_signal_text(
                route_id=str(route_id or "unrouted"),
                expression_permission=telemetry.expression_permission,
                dynamic_needed=bool(dynamic.get("needed")) if isinstance(dynamic, dict) else False,
            ),
            "not_claimed": [
                "hidden_chain_of_thought",
                "private_reasoning_transcript",
                "lived_human_emotion",
                "personal_consciousness",
            ],
        },
        "expressive_telemetry": {
            "binding_id": telemetry.binding_id,
            "claim_class": telemetry.claim_class,
            "emission_permission": telemetry.emission_permission,
            "conversation_status": telemetry.conversation_status,
            "tone_profile": telemetry.tone_profile,
            "pace_profile": telemetry.pace_profile,
            "confidence_presentation": telemetry.confidence_presentation,
            "expression_permission": telemetry.expression_permission,
            "state_alignment_verdict": telemetry.state_alignment_verdict,
            "forbidden_claims": dict(telemetry.forbidden_claims),
        },
        "boundaries": {
            "output_is_not_state": True,
            "candidate_until_receipted_or_accepted": True,
            "production_authority": False,
            "live_execution_authority": False,
            "secrets_authority": False,
            "hidden_chain_of_thought_exposed": False,
            "lived_human_emotion_claimed": False,
        },
        "custom_tailored_response": str(user_response or "").strip(),
    }
    errors = validate_persona_response_envelope(envelope)
    if errors:
        envelope["ok"] = False
        envelope["verdict"] = "ION_PERSONA_RESPONSE_ENVELOPE_INVALID"
        envelope["validation_errors"] = errors
    return envelope


def validate_persona_response_envelope(envelope: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if envelope.get("schema_id") != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if envelope.get("boundaries", {}).get("production_authority") is not False:
        errors.append("persona envelope must not grant production authority")
    if envelope.get("boundaries", {}).get("live_execution_authority") is not False:
        errors.append("persona envelope must not grant live execution authority")
    if envelope.get("boundaries", {}).get("hidden_chain_of_thought_exposed") is not False:
        errors.append("persona envelope must not expose hidden chain-of-thought")
    if envelope.get("persona", {}).get("persona_is_total_ion") is not False:
        errors.append("persona must not claim to be total ION")
    inner = envelope.get("inner_monologue", {})
    if inner.get("type") != "operator_visible_persona_signal_not_hidden_reasoning":
        errors.append("inner_monologue must be operator-visible telemetry, not hidden reasoning")
    forbidden_claims = envelope.get("expressive_telemetry", {}).get("forbidden_claims", {})
    for key, expected in FORBIDDEN_CLAIMS.items():
        if forbidden_claims.get(key) is not expected:
            errors.append(f"forbidden expressive claim {key!r} must be false")
    telemetry_errors = validate_expressive_telemetry_binding(
        build_expressive_telemetry_binding(
            claim_class=str(envelope.get("expressive_telemetry", {}).get("claim_class") or "C2"),
            emission_permission=str(envelope.get("expressive_telemetry", {}).get("emission_permission") or "MAY_EMIT_AS_PROPOSAL"),
            conversation_status=str(envelope.get("expressive_telemetry", {}).get("conversation_status") or "OPEN_PROVISIONAL"),
        )
    )
    errors.extend(f"expressive_telemetry:{error}" for error in telemetry_errors)
    return errors


def format_persona_response_envelope_yaml(envelope: dict[str, Any]) -> str:
    """Render the persona envelope as a chat-friendly fenced YAML block."""
    visible_payload = {
        "ion_persona": {
            "schema": envelope.get("schema_id"),
            "verdict": envelope.get("verdict"),
            "response_id": envelope.get("response_id"),
            "created_at": envelope.get("created_at"),
            "persona": envelope.get("persona"),
            "route": envelope.get("route"),
            "dynamic_domain_signal": envelope.get("dynamic_domain_signal"),
            "confidence": envelope.get("confidence"),
            "gesture": envelope.get("gesture"),
            "inner_monologue": envelope.get("inner_monologue"),
            "expressive_telemetry": envelope.get("expressive_telemetry"),
            "boundaries": envelope.get("boundaries"),
        }
    }
    return "\n".join(
        [
            "```yaml",
            *_dump_yaml_lines(visible_payload),
            "```",
            "",
            str(envelope.get("custom_tailored_response") or "").strip(),
        ]
    ).rstrip()


def _dynamic_domain_signal(dynamic: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(dynamic, dict) or not dynamic.get("needed"):
        return {
            "needed": False,
            "semantic": "Selected route appears sufficient; no dynamic specialist domain proposed.",
        }
    domains = [
        str(domain.get("domain_id"))
        for domain in dynamic.get("candidate_domains", [])
        if isinstance(domain, dict) and domain.get("domain_id")
    ]
    agents = [
        str(agent.get("agent_id"))
        for agent in dynamic.get("candidate_agents", [])
        if isinstance(agent, dict) and agent.get("agent_id")
    ]
    return {
        "needed": True,
        "trigger": dynamic.get("trigger"),
        "lifecycle_state": dynamic.get("lifecycle_state"),
        "candidate_domains": domains,
        "candidate_agents": agents[:12],
        "semantic": "Request pressure exceeds the selected generic route; candidate specialist domain/agents should be reported for review.",
        "local_hub_report_recommended": bool(dynamic.get("recommended_local_hub_report")),
    }


def _confidence_payload(
    *,
    certainty: str,
    risk_level: str,
    claim_class: str,
    emission_permission: str,
    route_id: str,
    dynamic_needed: bool,
) -> dict[str, str]:
    if emission_permission.startswith("BLOCKED") or claim_class == "C5":
        level = "blocked"
        semantic = "Blocked: the persona should not render this as a final answer until repair completes."
    elif certainty == "HIGH" and risk_level == "LOW" and not dynamic_needed:
        level = "high_bounded"
        semantic = "High but bounded: route and evidence posture are stable for a user-facing answer, while output remains non-state."
    elif dynamic_needed:
        level = "scoped_expansion"
        semantic = "Scoped expansion: the answer can proceed, but the request also creates candidate domain/agent pressure that should be reviewed."
    elif certainty in {"LOW", "UNKNOWN"}:
        level = "scoped_low"
        semantic = "Scoped low: the persona can answer from current context, but should keep claims provisional and evidence-bound."
    else:
        level = "scoped"
        semantic = "Scoped: the persona can answer within the selected route, but acceptance still requires proof or receipt where relevant."
    return {
        "level": level,
        "semantic": semantic,
        "calibration": f"Bounded to route {route_id}; AI output is not state until grounded and accepted.",
    }


def _gesture_payload(*, tone_profile: str, pace_profile: str, hesitation_level: str, risk_level: str) -> dict[str, str]:
    if risk_level in {"HIGH", "CRITICAL"}:
        gesture = "steady_boundary_hold"
        semantic = "Careful, direct, and visibly constrained by authority/risk boundaries."
    elif hesitation_level in {"medium", "high"}:
        gesture = "measured_forward_lean"
        semantic = "Engaged but cautious; signals useful movement without overclaiming."
    else:
        gesture = "direct_open_hand"
        semantic = "Clear and accessible; confidence remains evidence-bound."
    return {
        "gesture": gesture,
        "semantic": semantic,
        "tone_profile": tone_profile,
        "pace_profile": pace_profile,
        "hesitation_level": hesitation_level,
    }


def _persona_signal_text(*, route_id: str, expression_permission: str, dynamic_needed: bool) -> str:
    if dynamic_needed:
        return (
            "I am holding the user-facing answer together with a candidate domain/agent expansion signal; "
            "the safe next move is to answer plainly and report the proposal for governed review."
        )
    if expression_permission.startswith("DO_NOT"):
        return (
            "I am holding this at the boundary; the safe next move is repair or refusal before persona rendering."
        )
    return (
        f"I am answering through {route_id} with visible scope; the safe next move is clear help plus proof boundaries."
    )


def _as_string_list(value: Any) -> list[str]:
    return [str(item) for item in value] if isinstance(value, list) else []


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]


def _dump_yaml_lines(payload: Any, *, indent: int = 0) -> list[str]:
    prefix = " " * indent
    if isinstance(payload, dict):
        lines: list[str] = []
        for key, value in payload.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(_dump_yaml_lines(value, indent=indent + 2))
            else:
                lines.append(f"{prefix}{key}: {_yaml_scalar(value)}")
        return lines
    if isinstance(payload, list):
        lines = []
        if not payload:
            return [f"{prefix}[]"]
        for value in payload:
            if isinstance(value, dict):
                lines.append(f"{prefix}-")
                lines.extend(_dump_yaml_lines(value, indent=indent + 2))
            elif isinstance(value, list):
                lines.append(f"{prefix}-")
                lines.extend(_dump_yaml_lines(value, indent=indent + 2))
            else:
                lines.append(f"{prefix}- {_yaml_scalar(value)}")
        return lines
    return [f"{prefix}{_yaml_scalar(payload)}"]


def _yaml_scalar(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value))
