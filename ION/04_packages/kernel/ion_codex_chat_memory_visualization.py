"""Memory and context visualization projection for ION Codex Chat.

This module converts existing chat, Capsule, Mini, long-horizon, route, and
trace data into an explicit UI-safe projection. It does not select context for
the model, call providers, expose hidden reasoning, or mutate state.
"""
from __future__ import annotations

import re
from collections import Counter
from collections.abc import Mapping
from typing import Any

from .ion_codex_solo_context import (
    CAPSULE_PATH,
    CONTEXT_PACKAGES_PATH,
    HOT_CONTEXT_PATH,
    LONG_HORIZON_PATH,
    MINI_PATH,
    ROUTE_PATH,
)

SCHEMA_ID = "ion.codex_chat_memory_visualization.v1"
SEGMENT_SCHEMA_ID = "ion.codex_chat_memory_segment.v1"
EDGE_SCHEMA_ID = "ion.codex_chat_context_route_edge.v1"

ACTIVE_CRUCIBLE_WINDOW = 5
PREVIEW_LIMIT = 360

WINDOW_TONES = {
    "LIVE_INPUT": "bright",
    "ACTIVE_CRUCIBLE": "bright",
    "ACTIVE_CONTEXT": "normal",
    "HOT_CONTEXT": "warm",
    "X_RAY_DAG": "dim_hover",
    "MINI_LOOKUP": "muted",
    "LONG_HORIZON": "dim",
    "COLD_EVIDENCE": "dark",
    "OMITTED_OR_BLOCKED": "blocked",
}

MATRYOSHKA_LAYERS = {
    "active_crucible": {
        "label": "Active Crucible",
        "summary": "Live input and the recent rolling chat window closest to the carrier call.",
        "window_classes": ("LIVE_INPUT", "ACTIVE_CRUCIBLE"),
    },
    "priority_capsule": {
        "label": "Priority Capsule",
        "summary": "Capsule minimum context plus current mission and hot operational state.",
        "window_classes": ("ACTIVE_CONTEXT", "HOT_CONTEXT"),
    },
    "x_ray_dag": {
        "label": "X-Ray DAG",
        "summary": "Compressed long-horizon epochs and branchable context history.",
        "window_classes": ("X_RAY_DAG", "LONG_HORIZON"),
    },
    "background_swarm": {
        "label": "Background Swarm",
        "summary": "Mini lookup, cold evidence, and omitted or blocked route candidates.",
        "window_classes": ("MINI_LOOKUP", "COLD_EVIDENCE", "OMITTED_OR_BLOCKED"),
    },
}

SECRET_PATTERNS = (
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"(?i)((?:api[_-]?key|token|secret|password)\s*[:=]\s*)[^\s,;]{4,}"),
)


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _as_list(value: Any) -> list[Any]:
    return list(value) if isinstance(value, list) else []


def _redact(value: Any, *, limit: int = PREVIEW_LIMIT) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    for pattern in SECRET_PATTERNS:
        text = pattern.sub(r"\1[REDACTED]", text)
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def _token_estimate(value: Any) -> int:
    text = str(value or "")
    return max(1, (len(text) + 3) // 4) if text else 0


def _segment(
    *,
    segment_id: str,
    source_kind: str,
    text_preview: Any,
    window_class: str,
    lifecycle_class: str,
    prompt_inclusion_state: str,
    compaction_state: str,
    authority_state: str = "allowed_read",
    turn_id: Any = None,
    source_path: Any = None,
    receipt_refs: list[str] | None = None,
    route_refs: list[str] | None = None,
    selection_signals: list[str] | None = None,
    confidence: float = 1.0,
    source_system: str = "ion_codex_chat",
    agent_role: Any = None,
    protocol_branch_id: Any = None,
    escalation_class: Any = None,
) -> dict[str, Any]:
    preview = _redact(text_preview)
    return {
        "schema_id": SEGMENT_SCHEMA_ID,
        "segment_id": segment_id,
        "turn_id": turn_id,
        "source_path": source_path,
        "source_kind": source_kind,
        "text_preview": preview,
        "window_class": window_class,
        "lifecycle_class": lifecycle_class,
        "prompt_inclusion_state": prompt_inclusion_state,
        "compaction_state": compaction_state,
        "authority_state": authority_state,
        "receipt_refs": [str(ref) for ref in receipt_refs or [] if ref],
        "route_refs": [str(ref) for ref in route_refs or [] if ref],
        "display_tone": WINDOW_TONES.get(window_class, "normal"),
        "selection_signals": [str(signal) for signal in selection_signals or [] if signal],
        "token_estimate": _token_estimate(preview),
        "confidence": confidence,
        "source_system": source_system,
        "agent_role": agent_role,
        "protocol_branch_id": protocol_branch_id,
        "escalation_class": escalation_class,
        "raw_hidden_reasoning_exposed": False,
    }


def _edge(
    *,
    edge_id: str,
    from_segment_id: str,
    to_segment_id: str,
    edge_type: str,
    source_system: str = "ion_codex_chat",
    confidence: float = 1.0,
    receipt_refs: list[str] | None = None,
    display_style: str | None = None,
) -> dict[str, Any]:
    style = display_style or {
        "retrieved": "solid",
        "created": "dashed",
        "summarized_to": "dashed",
        "compressed_to": "dotted",
        "branched_to": "fork",
        "merged_into": "merge",
        "invalidated_by": "struck",
        "omitted_due_budget": "muted",
        "omitted_due_authority": "blocked",
        "escalated_to": "accent",
    }.get(edge_type, "solid")
    return {
        "schema_id": EDGE_SCHEMA_ID,
        "edge_id": edge_id,
        "from_segment_id": from_segment_id,
        "to_segment_id": to_segment_id,
        "edge_type": edge_type,
        "source_system": source_system,
        "confidence": confidence,
        "receipt_refs": [str(ref) for ref in receipt_refs or [] if ref],
        "display_style": style,
    }


def _latest_user_turn(turns: list[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    for turn in reversed(turns):
        if turn.get("kind", "chat_turn") == "chat_turn" and turn.get("author") in {"operator", "user"}:
            return turn
    return None


def _trace_for_turn(turn_traces: Mapping[str, Any], turn_id: str | None) -> Mapping[str, Any]:
    if not turn_id:
        return {}
    for trace in _as_list(turn_traces.get("traces")):
        if isinstance(trace, Mapping) and str(trace.get("turn_id") or "") == turn_id:
            return trace
    return {}


def _event_phase(event_type: str) -> str:
    return {
        "operator_message": "memory",
        "context_mount": "memory",
        "skill_activation": "planning",
        "chat_engine": "planning",
        "codex_chat_response_carrier": "execute",
        "assistant_response": "synthesize",
        "tool_call": "execute",
        "runner": "execute",
        "proof_return": "verify",
        "execution_bridge": "audit",
    }.get(event_type, "audit")


def _cognition_mode(response_mode: str | None) -> str:
    if response_mode in {"queue_work", "recover", "ion_handoff"}:
        return "C3_ESCALATION"
    if response_mode in {"answer", "clarify", "plan"}:
        return "C2_REACTIVE_WORKER"
    return "C1_ORGANIZER"


def _selected_chat_engine(selected_turn: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if not selected_turn:
        return {}
    chat_engine = selected_turn.get("chat_engine")
    return chat_engine if isinstance(chat_engine, Mapping) else {}


def _selected_skill(chat_engine: Mapping[str, Any]) -> Mapping[str, Any]:
    skill = chat_engine.get("skill_activation")
    if isinstance(skill, Mapping):
        return skill
    skill = chat_engine.get("selected_skill")
    return skill if isinstance(skill, Mapping) else {}


def _prompt_package_summary(codex_solo_context: Mapping[str, Any], chat_engine: Mapping[str, Any]) -> dict[str, Any]:
    context_packages = _as_mapping(codex_solo_context.get("context_packages"))
    packages = [package for package in _as_list(context_packages.get("packages")) if isinstance(package, Mapping)]
    context_mount = _as_mapping(chat_engine.get("context_mount"))
    context_refs = [str(ref) for ref in _as_list(context_mount.get("context_refs")) if ref]
    return {
        "schema_id": "ion.codex_chat_prompt_package_summary.v1",
        "package_count": context_packages.get("package_count", len(packages)),
        "selected_by_default": _as_list(context_packages.get("selected_by_default")),
        "required_context_refs": context_refs,
        "package_ids": [str(package.get("package_id")) for package in packages if package.get("package_id")],
        "minimum_context": CAPSULE_PATH.as_posix(),
        "mini_role": "lookup_receipt_index_not_primary_prompt",
        "raw_hidden_reasoning_exposed": False,
    }


def _protocol_manifest_summary(
    *,
    selected_turn_id: str | None,
    chat_engine: Mapping[str, Any],
    codex_solo_context: Mapping[str, Any],
    missing_route: list[str],
) -> dict[str, Any]:
    response_mode = str(chat_engine.get("response_mode") or "model_refresh")
    skill = _selected_skill(chat_engine)
    response_contract = _as_mapping(chat_engine.get("response_contract"))
    context_mount = _as_mapping(chat_engine.get("context_mount"))
    refs = [str(ref) for ref in _as_list(context_mount.get("context_refs")) if ref]
    route = _as_mapping(codex_solo_context.get("route"))
    entries = [entry for entry in _as_list(route.get("entries")) if isinstance(entry, Mapping)]
    selected_gate = "template_proof_required" if response_contract.get("template_proof_required_for_mutation") else "context_proof_required"
    return {
        "schema_id": "ion.codex_chat_protocol_manifest_summary.v1",
        "selected_turn_id": selected_turn_id,
        "current_branch_id": response_mode,
        "selected_skill_id": skill.get("skill_id"),
        "available_branch_count": 6,
        "selected_gate": selected_gate,
        "c1_c2_c3_mode": _cognition_mode(response_mode),
        "next_files_or_sources": refs[:16],
        "route_entry_count": len(entries),
        "blocked_routes": missing_route,
        "required_human_acceptance": response_mode in {"queue_work", "recover", "ion_handoff"},
        "production_authority": False,
        "live_execution_authority": False,
        "raw_hidden_reasoning_exposed": False,
    }


def _matryoshka_layers(segments: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    layers: list[dict[str, Any]] = []
    for layer_id, definition in MATRYOSHKA_LAYERS.items():
        window_classes = set(definition["window_classes"])
        layer_segments = [segment for segment in segments if segment.get("window_class") in window_classes]
        layers.append({
            "layer_id": layer_id,
            "label": definition["label"],
            "summary": definition["summary"],
            "window_classes": list(definition["window_classes"]),
            "segment_ids": [str(segment.get("segment_id")) for segment in layer_segments if segment.get("segment_id")],
            "segment_count": len(layer_segments),
            "token_estimate": sum(int(segment.get("token_estimate") or 0) for segment in layer_segments),
            "raw_hidden_reasoning_exposed": False,
        })
    return layers


def _selected_turn_context(
    *,
    selected_turn_id: str | None,
    segments: list[Mapping[str, Any]],
    edges: list[Mapping[str, Any]],
) -> dict[str, Any]:
    selected_segment_id = f"turn:{selected_turn_id}" if selected_turn_id else None
    related_edges = [edge for edge in edges if edge.get("from_segment_id") == selected_segment_id]
    direct_ids = {str(edge.get("to_segment_id")) for edge in related_edges if edge.get("to_segment_id")}
    active_segments = [
        segment for segment in segments
        if segment.get("prompt_inclusion_state") in {"direct_prompt", "active_window", "active_context"}
    ]
    lookup_segments = [
        segment for segment in segments
        if segment.get("prompt_inclusion_state") in {"lookup_available", "route_available", "trace_only"}
    ]
    omitted_segments = [
        segment for segment in segments
        if segment.get("window_class") == "OMITTED_OR_BLOCKED" or str(segment.get("authority_state") or "").startswith("blocked")
    ]
    return {
        "schema_id": "ion.codex_chat_selected_turn_context.v1",
        "selected_turn_id": selected_turn_id,
        "selected_segment_id": selected_segment_id,
        "directly_related_segment_ids": sorted(direct_ids),
        "active_prompt_segment_ids": [str(segment.get("segment_id")) for segment in active_segments if segment.get("segment_id")],
        "lookup_available_segment_ids": [str(segment.get("segment_id")) for segment in lookup_segments if segment.get("segment_id")],
        "omitted_or_blocked_segment_ids": [str(segment.get("segment_id")) for segment in omitted_segments if segment.get("segment_id")],
        "related_edge_ids": [str(edge.get("edge_id")) for edge in related_edges if edge.get("edge_id")],
        "policy": "shows explicit context surfaces and route metadata; raw hidden reasoning is not exposed",
        "raw_hidden_reasoning_exposed": False,
    }


def _carrier_phase_events(turn_trace: Mapping[str, Any]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    source_turn_id = str(turn_trace.get("turn_id") or "")
    for index, raw_event in enumerate(_as_list(turn_trace.get("events")), start=1):
        if not isinstance(raw_event, Mapping):
            continue
        event_type = str(raw_event.get("event_type") or "event")
        events.append({
            "event_id": f"{source_turn_id}:event:{index}",
            "source_turn_id": source_turn_id,
            "event_type": event_type,
            "phase": _event_phase(event_type),
            "label": raw_event.get("label"),
            "status": raw_event.get("status"),
            "source_refs": [str(ref) for ref in _as_list(raw_event.get("source_refs")) if ref],
            "tool_name": raw_event.get("tool_name"),
            "proof_status": raw_event.get("proof_status"),
            "raw_hidden_reasoning_exposed": False,
        })
    return events


def build_codex_chat_memory_visualization(
    *,
    state: Mapping[str, Any],
    codex_solo_context: Mapping[str, Any],
    turn_traces: Mapping[str, Any],
    return_hydration: Mapping[str, Any],
    codex_status: Mapping[str, Any],
) -> dict[str, Any]:
    lanes = _as_mapping(state.get("lanes"))
    codex_lane = _as_mapping(lanes.get("codex_general"))
    turns = [turn for turn in _as_list(codex_lane.get("turns")) if isinstance(turn, Mapping)]
    selected_turn = _latest_user_turn(turns)
    selected_turn_id = str(selected_turn.get("turn_id") or "") if selected_turn else None
    selected_chat_engine = _selected_chat_engine(selected_turn)
    selected_trace = _trace_for_turn(turn_traces, selected_turn_id)
    selected_skill = _selected_skill(selected_chat_engine)
    route = _as_mapping(codex_solo_context.get("route"))
    route_entries = [entry for entry in _as_list(route.get("entries")) if isinstance(entry, Mapping)]
    missing_route = [str(entry.get("path")) for entry in route_entries if not entry.get("exists") and entry.get("path")]
    capsule = _as_mapping(codex_solo_context.get("capsule"))
    mini = _as_mapping(codex_solo_context.get("mini"))
    long_horizon = _as_mapping(codex_solo_context.get("long_horizon"))
    context_packages = _as_mapping(codex_solo_context.get("context_packages"))
    response_mode = str(selected_chat_engine.get("response_mode") or "model_refresh")
    protocol_branch_id = response_mode
    escalation = _cognition_mode(response_mode)

    segments: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    recent_turns = turns[-ACTIVE_CRUCIBLE_WINDOW:]
    for turn in recent_turns:
        turn_id = str(turn.get("turn_id") or f"turn_{len(segments) + 1}")
        is_selected = turn_id == selected_turn_id
        window_class = "LIVE_INPUT" if is_selected and turn.get("author") in {"operator", "user"} else "ACTIVE_CRUCIBLE"
        source_kind = str(turn.get("kind") or "chat_turn")
        segments.append(_segment(
            segment_id=f"turn:{turn_id}",
            turn_id=turn_id,
            source_kind=source_kind,
            text_preview=turn.get("message"),
            window_class=window_class,
            lifecycle_class="current_truth",
            prompt_inclusion_state="direct_prompt" if is_selected else "active_window",
            compaction_state="raw_turn",
            selection_signals=["selected_latest_turn"] if is_selected else ["recent_active_crucible"],
            source_system="ion_codex_chat_state",
            agent_role=turn.get("author"),
            protocol_branch_id=protocol_branch_id,
            escalation_class=escalation,
        ))

    capsule_rows = [row for row in _as_list(capsule.get("recent_rows")) if isinstance(row, Mapping)]
    latest_capsule = capsule_rows[-1] if capsule_rows else {}
    capsule_segment_id = "context:capsule"
    segments.append(_segment(
        segment_id=capsule_segment_id,
        source_path=CAPSULE_PATH.as_posix(),
        source_kind="capsule_minimum_context",
        text_preview=latest_capsule.get("summary") or "Capsule minimum context.",
        window_class="ACTIVE_CONTEXT",
        lifecycle_class="current_truth",
        prompt_inclusion_state="active_context",
        compaction_state="receipt_row",
        receipt_refs=[str(latest_capsule.get("id"))] if latest_capsule.get("id") else [],
        route_refs=[CAPSULE_PATH.as_posix()],
        selection_signals=["capsule_minimum_context"],
        source_system="codex_solo_context",
        protocol_branch_id=protocol_branch_id,
        escalation_class=escalation,
    ))

    segments.append(_segment(
        segment_id="context:hot",
        source_path=HOT_CONTEXT_PATH.as_posix(),
        source_kind="hot_context",
        text_preview="Current mission, recent receipts, queue/service status, and active objectives.",
        window_class="HOT_CONTEXT",
        lifecycle_class="hot_state",
        prompt_inclusion_state="active_context",
        compaction_state="compiled_hot_context",
        route_refs=[HOT_CONTEXT_PATH.as_posix()],
        selection_signals=["mission_active_package", "recent_receipts", "service_state"],
        source_system="codex_solo_context",
        protocol_branch_id=protocol_branch_id,
        escalation_class=escalation,
    ))

    mini_segment_id = "context:mini"
    segments.append(_segment(
        segment_id=mini_segment_id,
        source_path=MINI_PATH.as_posix(),
        source_kind="mini_lookup_index",
        text_preview=mini.get("text") or "Mini lookup index unavailable.",
        window_class="MINI_LOOKUP",
        lifecycle_class="warm_evidence",
        prompt_inclusion_state="lookup_available",
        compaction_state="index",
        route_refs=[MINI_PATH.as_posix()],
        selection_signals=["receipt_lookup_index_not_primary_prompt"],
        source_system="codex_solo_context",
        protocol_branch_id=protocol_branch_id,
        escalation_class=escalation,
    ))

    segments.append(_segment(
        segment_id="context:long_horizon",
        source_path=LONG_HORIZON_PATH.as_posix(),
        source_kind="long_horizon_index",
        text_preview=(
            f"{long_horizon.get('epoch_count', 0)} compressed epochs / "
            f"{long_horizon.get('capsule_entry_count', 0)} accepted capsule rows."
        ),
        window_class="LONG_HORIZON",
        lifecycle_class="cold_history",
        prompt_inclusion_state="route_available",
        compaction_state="epoch_index",
        route_refs=[LONG_HORIZON_PATH.as_posix()],
        selection_signals=["route_when_older_continuity_matters", "accepted_capsule_history"],
        confidence=0.9,
        source_system="codex_solo_context",
        protocol_branch_id=protocol_branch_id,
        escalation_class=escalation,
    ))

    for epoch in _as_list(long_horizon.get("epochs")):
        if not isinstance(epoch, Mapping):
            continue
        epoch_id = str(epoch.get("epoch_id") or f"epoch_{len(segments) + 1}")
        summaries = [
            str(summary.get("summary") or "")
            for summary in _as_list(epoch.get("summaries"))
            if isinstance(summary, Mapping)
        ]
        segments.append(_segment(
            segment_id=f"xray:{epoch_id}",
            source_path=LONG_HORIZON_PATH.as_posix(),
            source_kind="x_ray_dag_epoch",
            text_preview=" | ".join(summaries) or f"Long-horizon capsule epoch {epoch_id}",
            window_class="X_RAY_DAG",
            lifecycle_class="cold_history",
            prompt_inclusion_state="route_available",
            compaction_state="compressed_epoch",
            receipt_refs=[str(ref) for ref in _as_list(epoch.get("evidence_refs"))[:8] if ref],
            route_refs=[LONG_HORIZON_PATH.as_posix()],
            selection_signals=["compressed_long_horizon", "route_when_older_continuity_matters"],
            confidence=0.92,
            source_system="codex_solo_context",
            protocol_branch_id=protocol_branch_id,
            escalation_class=escalation,
        ))

    for package in _as_list(context_packages.get("packages")):
        if not isinstance(package, Mapping):
            continue
        package_id = str(package.get("package_id") or f"package_{len(segments) + 1}")
        selected = package_id in set(str(value) for value in _as_list(context_packages.get("selected_by_default")))
        segments.append(_segment(
            segment_id=f"package:{package_id}",
            source_kind="context_package",
            text_preview=f"{package_id}: {package.get('context_type')} / {package.get('load_policy')}",
            window_class="ACTIVE_CONTEXT" if selected else "COLD_EVIDENCE",
            lifecycle_class="current_truth" if selected else "warm_evidence",
            prompt_inclusion_state="active_context" if selected else "route_available",
            compaction_state="package_selector",
            route_refs=[str(ref) for ref in _as_list(package.get("path_refs")) if ref],
            selection_signals=["selected_by_default"] if selected else ["route_deeper_available"],
            confidence=1.0 if selected else 0.84,
            source_system="codex_solo_context",
            protocol_branch_id=protocol_branch_id,
            escalation_class=escalation,
        ))

    for index, entry in enumerate(route_entries, start=1):
        path = str(entry.get("path") or "")
        if not path:
            continue
        exists = bool(entry.get("exists"))
        segments.append(_segment(
            segment_id=f"route:{index}",
            source_path=path,
            source_kind="route_entry",
            text_preview=f"{entry.get('classification') or 'route'}: {entry.get('why') or path}",
            window_class="COLD_EVIDENCE" if exists else "OMITTED_OR_BLOCKED",
            lifecycle_class="warm_evidence" if exists else "blocked",
            prompt_inclusion_state="route_available" if exists else "not_loaded",
            compaction_state="source_ref",
            authority_state="allowed_read" if exists else "blocked_missing",
            route_refs=[path],
            selection_signals=["route_index"] if exists else ["blocked", "missing_route"],
            confidence=1.0 if exists else 0.0,
            source_system="codex_solo_route",
            protocol_branch_id=protocol_branch_id,
            escalation_class=escalation,
        ))

    if selected_turn_id:
        selected_segment_id = f"turn:{selected_turn_id}"
        for target_id, edge_type in (
            (capsule_segment_id, "retrieved"),
            ("context:hot", "retrieved"),
            (mini_segment_id, "retrieved"),
        ):
            edges.append(_edge(
                edge_id=f"{selected_segment_id}->{target_id}",
                from_segment_id=selected_segment_id,
                to_segment_id=target_id,
                edge_type=edge_type,
            ))
        for event in _as_list(selected_trace.get("events")):
            if isinstance(event, Mapping) and event.get("event_type") == "codex_chat_response_carrier":
                carrier_segment_id = f"carrier:{selected_turn_id}"
                segments.append(_segment(
                    segment_id=carrier_segment_id,
                    turn_id=selected_turn_id,
                    source_kind="carrier_phase",
                    text_preview=event.get("detail") or event.get("label"),
                    window_class="HOT_CONTEXT",
                    lifecycle_class="hot_state",
                    prompt_inclusion_state="trace_only",
                    compaction_state="event",
                    receipt_refs=[str(ref) for ref in _as_list(event.get("source_refs")) if ref],
                    selection_signals=["carrier_phase_event"],
                    source_system="codex_chat_response_carrier",
                    protocol_branch_id=protocol_branch_id,
                    escalation_class=escalation,
                ))
                edges.append(_edge(
                    edge_id=f"{selected_segment_id}->{carrier_segment_id}",
                    from_segment_id=selected_segment_id,
                    to_segment_id=carrier_segment_id,
                    edge_type="escalated_to",
                    source_system="codex_chat_response_carrier",
                ))
                break

    for segment in segments:
        segment_id = str(segment.get("segment_id") or "")
        if segment_id.startswith("xray:"):
            edges.append(_edge(
                edge_id=f"{capsule_segment_id}->{segment_id}",
                from_segment_id=capsule_segment_id,
                to_segment_id=segment_id,
                edge_type="compressed_to",
                source_system="codex_solo_context",
            ))
        elif segment_id == "context:long_horizon":
            edges.append(_edge(
                edge_id=f"{capsule_segment_id}->{segment_id}",
                from_segment_id=capsule_segment_id,
                to_segment_id=segment_id,
                edge_type="compressed_to",
                source_system="codex_solo_context",
            ))
        elif segment_id.startswith("package:"):
            edges.append(_edge(
                edge_id=f"{capsule_segment_id}->{segment_id}",
                from_segment_id=capsule_segment_id,
                to_segment_id=segment_id,
                edge_type="retrieved" if segment.get("prompt_inclusion_state") == "active_context" else "branched_to",
                source_system="codex_solo_context",
            ))
        elif segment_id.startswith("route:"):
            edge_type = "retrieved" if segment.get("authority_state") == "allowed_read" else "omitted_due_authority"
            edges.append(_edge(
                edge_id=f"{capsule_segment_id}->{segment_id}",
                from_segment_id=capsule_segment_id,
                to_segment_id=segment_id,
                edge_type=edge_type,
                source_system="codex_solo_route",
            ))

    compaction_events = []
    if mini.get("ok") is not False:
        compaction_events.append({
            "event_type": "mini_lookup_index_refreshed",
            "source_path": MINI_PATH.as_posix(),
            "target_window_class": "MINI_LOOKUP",
            "summary": "Mini acts as lookup and receipt index, not the primary prompt surface.",
        })
    for epoch in _as_list(long_horizon.get("epochs")):
        if isinstance(epoch, Mapping):
            compaction_events.append({
                "event_type": "capsule_rows_compressed_to_long_horizon",
                "source_path": LONG_HORIZON_PATH.as_posix(),
                "epoch_id": epoch.get("epoch_id"),
                "row_start": epoch.get("row_start"),
                "row_end": epoch.get("row_end"),
                "target_window_class": "X_RAY_DAG",
            })

    class_counts = Counter(str(segment.get("window_class") or "UNKNOWN") for segment in segments)
    token_by_class: dict[str, int] = {}
    for segment in segments:
        window_class = str(segment.get("window_class") or "UNKNOWN")
        token_by_class[window_class] = token_by_class.get(window_class, 0) + int(segment.get("token_estimate") or 0)
    visible_windows = [
        {
            "window_class": window_class,
            "segment_count": class_counts.get(window_class, 0),
            "token_estimate": token_by_class.get(window_class, 0),
            "display_tone": WINDOW_TONES.get(window_class, "normal"),
        }
        for window_class in WINDOW_TONES
        if class_counts.get(window_class, 0)
    ]
    source_refs = sorted({
        str(ref)
        for segment in segments
        for ref in ([segment.get("source_path")] + _as_list(segment.get("route_refs")) + _as_list(segment.get("receipt_refs")))
        if ref
    })
    forbidden_or_omitted_refs = [
        {
            "ref": path,
            "reason": "missing_route_or_not_loaded",
            "authority_state": "blocked_missing",
        }
        for path in missing_route
    ]
    forbidden_or_omitted_refs.append({
        "ref": "raw_hidden_chain_of_thought",
        "reason": "forbidden_surface",
        "authority_state": "not_exposed",
    })
    forbidden_or_omitted_refs.append({
        "ref": "secret_token_values",
        "reason": "forbidden_surface",
        "authority_state": "redacted",
    })

    carrier_events = _carrier_phase_events(selected_trace)
    return_records = [record for record in _as_list(return_hydration.get("records")) if isinstance(record, Mapping)]
    token_total = sum(int(segment.get("token_estimate") or 0) for segment in segments)
    return {
        "schema_id": SCHEMA_ID,
        "selected_turn_id": selected_turn_id,
        "visible_windows": visible_windows,
        "memory_segments": segments,
        "context_route_edges": edges,
        "selected_turn_context": _selected_turn_context(
            selected_turn_id=selected_turn_id,
            segments=segments,
            edges=edges,
        ),
        "context_matryoshka_layers": _matryoshka_layers(segments),
        "compaction_events": compaction_events,
        "prompt_package_summary": _prompt_package_summary(codex_solo_context, selected_chat_engine),
        "protocol_manifest_summary": _protocol_manifest_summary(
            selected_turn_id=selected_turn_id,
            chat_engine=selected_chat_engine,
            codex_solo_context=codex_solo_context,
            missing_route=missing_route,
        ),
        "token_budget_summary": {
            "schema_id": "ion.codex_chat_token_budget_summary.v1",
            "estimated_total_tokens": token_total,
            "estimated_tokens_by_window_class": token_by_class,
            "segment_count": len(segments),
            "edge_count": len(edges),
            "blocked_or_omitted_count": len(missing_route),
            "max_context_tokens_authoritative": False,
            "policy": "estimates_are_visualization_hints_not_provider_limits",
        },
        "carrier_phase_events": carrier_events,
        "source_refs": source_refs,
        "forbidden_or_omitted_refs": forbidden_or_omitted_refs,
        "return_record_count": len(return_records),
        "queued_request_count": codex_status.get("queued_request_count", 0),
        "active_process_running": codex_status.get("active_process_running", False),
        "selection_policy": "visualizes_existing_context_state_without_selecting_provider_prompt_context",
        "raw_hidden_reasoning_exposed": False,
        "production_authority": False,
        "live_execution_authority": False,
        "secrets_authority": False,
    }
