"""Right inspector drawer renderers for Codex Chat."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .ion_codex_chat_memory_visualization_ui import render_memory_visualization_body
from .ion_codex_chat_timeline_ui import render_timeline_body
from .ion_codex_chat_ui_common import display_summary, drawer, e, mini_brief, state_pill


def _agent_label(agent: Mapping[str, Any]) -> str:
    return str(agent.get("display_name") or agent.get("agent_display_name") or agent.get("role_id") or agent.get("agent_role_id") or "agent")


def _agents_body(agents: Mapping[str, Any]) -> str:
    available = [agent for agent in agents.get("available_agents", []) if isinstance(agent, Mapping)] if isinstance(agents.get("available_agents"), list) else []
    invocations = [item for item in agents.get("recent_invocations", []) if isinstance(item, Mapping)] if isinstance(agents.get("recent_invocations"), list) else []
    agent_rows = []
    for agent in available[:8]:
        context_paths = agent.get("context_paths") if isinstance(agent.get("context_paths"), list) else []
        agent_rows.append(
            '<li class="agent-row">'
            f'<b>{e(_agent_label(agent))}</b>'
            f'{state_pill("invocable" if agent.get("invocable") else "missing context")}'
            f'<code>{e(agent.get("role_id") or agent.get("agent_id"))}</code>'
            f'<span>{e(len(context_paths))} context refs</span>'
            "</li>"
        )
    if not agent_rows:
        agent_rows.append('<li class="agent-row"><b>No agents discovered</b><span></span><code>none</code><span>0 context refs</span></li>')
    invocation_rows = []
    for item in invocations[:6]:
        invocation_rows.append(
            '<article class="invocation-card">'
            f'<div><b>{e(item.get("agent_display_name") or item.get("agent_role_id") or "Agent")}</b>{state_pill(item.get("status"))}</div>'
            f'<code>{e(item.get("invocation_id") or item.get("path"))}</code>'
            f'<p>{e(item.get("codex_work_request_path") or "No work request path.")}</p>'
            "</article>"
        )
    if not invocation_rows:
        invocation_rows.append('<p class="empty-note">No recent agent invocations.</p>')
    return (
        f"<p>Broker: <code>{e(agents.get('broker_owner'))}</code></p>"
        f"<p>No separate agent system: <code>{e(not bool(agents.get('creates_second_agent_system')))}</code></p>"
        '<div class="drawer-kpis">'
        f'<div class="drawer-kpi"><span>Available</span><b>{e(agents.get("agent_count") or len(available))}</b></div>'
        f'<div class="drawer-kpi"><span>Invocations</span><b>{e(agents.get("invocation_count") or len(invocations))}</b></div>'
        f'<div class="drawer-kpi"><span>Second system</span><b>{e(agents.get("creates_second_agent_system", False))}</b></div>'
        '</div>'
        '<h3>Available Agents</h3>'
        f'<ul class="agent-list">{"".join(agent_rows)}</ul>'
        '<h3>Broker Invocations</h3>'
        f'<div class="invocation-list">{"".join(invocation_rows)}</div>'
    )


def _skills_body(skills: Mapping[str, Any]) -> str:
    current = skills.get("current_activation") if isinstance(skills.get("current_activation"), Mapping) else {}
    cards = []
    for skill in skills.get("skills", []) if isinstance(skills.get("skills"), list) else []:
        if not isinstance(skill, Mapping):
            continue
        templates = skill.get("activates_templates") if isinstance(skill.get("activates_templates"), list) else []
        cards.append(
            '<article class="skill-card">'
            f'<div><b>{e(skill.get("display_name") or skill.get("skill_id"))}</b>{state_pill(skill.get("class"))}</div>'
            f'<code>{e(skill.get("skill_id"))}</code>'
            f'<p>{e(skill.get("purpose"))}</p>'
            f'<p>Templates: <code>{e(len(templates))}</code> · queue: <code>{e(skill.get("queue_work"))}</code> · writes: <code>{e(skill.get("write_files"))}</code></p>'
            "</article>"
        )
    if not cards:
        cards.append('<p class="empty-note">No skills registered.</p>')
    active_templates = current.get("activates_templates") if isinstance(current.get("activates_templates"), list) else []
    template_rows = "".join(f"<li><code>{e(item)}</code></li>" for item in active_templates[:8]) or "<li>No active templates.</li>"
    return (
        f"<p>Principle: <code>{e(skills.get('principle') or 'skills_activate_templates_templates_gate_proof')}</code></p>"
        f"<p>Registry: <code>{e(skills.get('registry_path'))}</code></p>"
        '<div class="drawer-kpis">'
        f'<div class="drawer-kpi"><span>Skills</span><b>{e(skills.get("skill_count") or 0)}</b></div>'
        f'<div class="drawer-kpi"><span>Current</span><b>{e(current.get("display_name") or "none")}</b></div>'
        f'<div class="drawer-kpi"><span>State Gate</span><b>{e(current.get("state_acceptance_granted", False))}</b></div>'
        '</div>'
        '<h3>Active Template Gates</h3>'
        f"<ul>{template_rows}</ul>"
        '<h3>Registered Skills</h3>'
        f'<div class="skill-list">{"".join(cards)}</div>'
    )


def _chat_engine_body(engine: Mapping[str, Any]) -> str:
    lenses = engine.get("lenses") if isinstance(engine.get("lenses"), list) else []
    lens_rows = []
    for lens in lenses[:10]:
        if not isinstance(lens, Mapping):
            continue
        lens_rows.append(
            '<li class="agent-row">'
            f'<b>{e(lens.get("display_name") or lens.get("lens_id"))}</b>'
            f'{state_pill(lens.get("model_stage_id"))}'
            f'<code>{e(lens.get("role_id") or lens.get("lens_id"))}</code>'
            f'<span>{e(lens.get("purpose"))}</span>'
            "</li>"
        )
    if not lens_rows:
        lens_rows.append('<li class="agent-row"><b>No lenses discovered</b><span></span><code>none</code><span></span></li>')
    modes = engine.get("response_modes") if isinstance(engine.get("response_modes"), list) else []
    return (
        f"<p>Target: <code>{e(engine.get('quality_target'))}</code></p>"
        f"<p>Policy: <code>{e(engine.get('policy'))}</code></p>"
        '<div class="drawer-kpis">'
        f'<div class="drawer-kpi"><span>Lenses</span><b>{e(engine.get("lens_count") or len(lenses))}</b></div>'
        f'<div class="drawer-kpi"><span>Modes</span><b>{e(len(modes))}</b></div>'
        f'<div class="drawer-kpi"><span>Ready</span><b>{e(engine.get("ok", False))}</b></div>'
        '</div>'
        '<h3>Native Lenses</h3>'
        f'<ul class="agent-list">{"".join(lens_rows)}</ul>'
    )


def _assistant_work_routes_body(routes: Mapping[str, Any]) -> str:
    route_ids = routes.get("route_ids") if isinstance(routes.get("route_ids"), list) else []
    route_rows = "".join(f"<li><code>{e(route_id)}</code></li>" for route_id in route_ids[:12]) or "<li>No candidate routes discovered.</li>"
    findings = routes.get("findings") if isinstance(routes.get("findings"), list) else []
    finding_rows = "".join(f"<li><code>{e(finding)}</code></li>" for finding in findings[:8]) or "<li>No findings.</li>"
    return (
        f"<p>Verdict: <code>{e(routes.get('verdict'))}</code>{state_pill('candidate only')}</p>"
        f"<p>Registry: <code>{e(routes.get('route_registry_path'))}</code></p>"
        f"<p>Map: <code>{e(routes.get('candidate_map_path') or 'unavailable')}</code></p>"
        f"<p>Policy: <code>{e(routes.get('policy'))}</code></p>"
        '<div class="drawer-kpis">'
        f'<div class="drawer-kpi"><span>Routes</span><b>{e(routes.get("route_count") or len(route_ids))}</b></div>'
        f'<div class="drawer-kpi"><span>Mapped</span><b>{e(routes.get("mapped_route_count") or 0)}</b></div>'
        f'<div class="drawer-kpi"><span>Ready</span><b>{e(routes.get("ok", False))}</b></div>'
        '</div>'
        '<h3>Candidate Routes</h3>'
        f"<ul>{route_rows}</ul>"
        '<h3>Findings</h3>'
        f"<ul>{finding_rows}</ul>"
    )


def _carrier_body(carrier: Mapping[str, Any]) -> str:
    return (
        f"<p>Verdict: <code>{e(carrier.get('verdict'))}</code></p>"
        f"<p>Enabled by: <code>{e(carrier.get('enabled_env'))}</code></p>"
        '<div class="drawer-kpis">'
        f'<div class="drawer-kpi"><span>Enabled</span><b>{e(carrier.get("enabled", False))}</b></div>'
        f'<div class="drawer-kpi"><span>Sandbox</span><b>{e(carrier.get("sandbox") or "unknown")}</b></div>'
        f'<div class="drawer-kpi"><span>Timeout</span><b>{e(carrier.get("timeout_seconds") or 0)}</b></div>'
        '</div>'
        f"<p>Run root: <code>{e(carrier.get('run_root'))}</code></p>"
        f"<p>Fallback: <code>{e(carrier.get('fallback_when_disabled'))}</code></p>"
        f"<p>Direct provider API: <code>{e(carrier.get('direct_provider_api'))}</code></p>"
    )


def _runs_body(runs: Mapping[str, Any]) -> str:
    runner = runs.get("runner") if isinstance(runs.get("runner"), Mapping) else {}
    work_items = runs.get("latest_work_requests") if isinstance(runs.get("latest_work_requests"), list) else []
    returns = runs.get("latest_task_returns") if isinstance(runs.get("latest_task_returns"), list) else []
    hydration = runs.get("return_hydration") if isinstance(runs.get("return_hydration"), Mapping) else {}
    linked = hydration.get("records") if isinstance(hydration.get("records"), list) else []
    response_runs = runs.get("response_runs") if isinstance(runs.get("response_runs"), Mapping) else {}
    response_records = response_runs.get("records") if isinstance(response_runs.get("records"), list) else []
    work_rows = "".join(f"<li><code>{e(item.get('path'))}</code></li>" for item in work_items if isinstance(item, Mapping)) or "<li>No recent work requests.</li>"
    return_rows = "".join(f"<li><code>{e(item.get('path'))}</code></li>" for item in returns if isinstance(item, Mapping)) or "<li>No recent task returns.</li>"
    linked_rows = "".join(
        f"<li><code>{e(item.get('proof_status'))}</code> {e(item.get('request_id'))}<br><code>{e(item.get('latest_return_path') or item.get('request_path'))}</code></li>"
        for item in linked[:5]
        if isinstance(item, Mapping)
    ) or "<li>No chat-linked proof returns yet.</li>"
    response_rows = []
    for item in response_records[:6]:
        if not isinstance(item, Mapping):
            continue
        response_rows.append(
            '<article class="invocation-card response-run-card">'
            f'<div><b>{e(item.get("status") or "response run")}</b>{state_pill(item.get("selected_model") or "model")}</div>'
            f'<code>{e(item.get("run_id") or item.get("path"))}</code>'
            f'<p>prompt <code>{e(item.get("prompt_path") or "none")}</code></p>'
            f'<p>return <code>{e(item.get("latest_return_path") or "none")}</code></p>'
            f'<p>events <code>{e(item.get("events_path") or "none")}</code></p>'
            "</article>"
        )
    if not response_rows:
        response_rows.append('<p class="empty-note">No response carrier runs yet.</p>')
    return (
        f"<p>Runner active: <code>{e(runner.get('active_process_running', False))}</code></p>"
        '<div class="drawer-kpis">'
        f'<div class="drawer-kpi"><span>Queued</span><b>{e(runner.get("queued_request_count", 0))}</b></div>'
        f'<div class="drawer-kpi"><span>Responses</span><b>{e(response_runs.get("record_count", 0))}</b></div>'
        f'<div class="drawer-kpi"><span>Latest</span><b>{e(response_runs.get("latest_status") or "none")}</b></div>'
        '</div>'
        '<h3>Response Carrier Runs</h3>'
        f'<div class="invocation-list">{"".join(response_rows)}</div>'
        '<h3>Work Requests</h3>'
        f"<ul>{work_rows}</ul>"
        '<h3>Task Returns</h3>'
        f"<ul>{return_rows}</ul>"
        '<h3>Linked Proof</h3>'
        f"<ul>{linked_rows}</ul>"
    )


def render_inspector(drawers: Mapping[str, Any]) -> str:
    timeline = drawers.get("timeline") if isinstance(drawers.get("timeline"), Mapping) else {}
    skills = drawers.get("skills") if isinstance(drawers.get("skills"), Mapping) else {}
    chat_engine = drawers.get("chat_engine") if isinstance(drawers.get("chat_engine"), Mapping) else {}
    assistant_work_routes = drawers.get("assistant_work_routes") if isinstance(drawers.get("assistant_work_routes"), Mapping) else {}
    carrier = drawers.get("carrier") if isinstance(drawers.get("carrier"), Mapping) else {}
    agents = drawers.get("agents") if isinstance(drawers.get("agents"), Mapping) else {}
    context = drawers.get("context") if isinstance(drawers.get("context"), Mapping) else {}
    if not context:
        context = drawers.get("capsule") if isinstance(drawers.get("capsule"), Mapping) else {}
    runs = drawers.get("runs") if isinstance(drawers.get("runs"), Mapping) else {}
    receipts = drawers.get("receipts") if isinstance(drawers.get("receipts"), Mapping) else {}
    ion = drawers.get("ion") if isinstance(drawers.get("ion"), Mapping) else {}
    settings = drawers.get("settings") if isinstance(drawers.get("settings"), Mapping) else {}

    recent_rows = context.get("recent_rows") if isinstance(context.get("recent_rows"), list) else []
    context_rows = "".join(
        f"<li><code>{e(row.get('id'))}</code> {e(row.get('status'))}: {e(display_summary(row.get('summary')))}</li>"
        for row in recent_rows
        if isinstance(row, Mapping)
    ) or "<li>No context receipts found.</li>"

    runner = runs.get("runner") if isinstance(runs.get("runner"), Mapping) else {}

    execution = settings.get("execution_bridge") if isinstance(settings.get("execution_bridge"), Mapping) else {}
    response_carrier = settings.get("response_carrier") if isinstance(settings.get("response_carrier"), Mapping) else carrier
    memory_visualization = context.get("memory_visualization") if isinstance(context.get("memory_visualization"), Mapping) else {}
    panels = {
        "assistant": [
            drawer("chat-engine", "Chat Engine", chat_engine.get("lens_count") or 0, _chat_engine_body(chat_engine)),
            drawer("assistant-work-routes", "Assistant Work Routes", assistant_work_routes.get("route_count") or 0, _assistant_work_routes_body(assistant_work_routes)),
            drawer("carrier", "Response Carrier", "On" if carrier.get("enabled") else "Fallback", _carrier_body(carrier)),
        ],
        "context": [
            drawer("memory-visualization", "Memory View", (memory_visualization.get("token_budget_summary") or {}).get("segment_count") if isinstance(memory_visualization.get("token_budget_summary"), Mapping) else "projection", render_memory_visualization_body(memory_visualization)),
            drawer("context", "Context", context.get("route_ok"), f"<ul>{context_rows}</ul><h3>Mini</h3><pre class=\"mini-text\">{e(mini_brief(context.get('mini_text')))}</pre>"),
            drawer("skills", "Skills", skills.get("skill_count") or 0, _skills_body(skills)),
        ],
        "evidence": [
            drawer("timeline", "Timeline", timeline.get("trace_count") or 0, render_timeline_body(timeline)),
            drawer("runs", "Runs", runner.get("queued_request_count", 0), _runs_body(runs)),
            drawer("receipts", "Receipts", "Capsule", f"<p>History: <code>{e(receipts.get('history_path'))}</code></p>"),
        ],
        "system": [
            drawer("agents", "Agents", agents.get("agent_count") or 0, _agents_body(agents)),
            drawer("ion", "ION Comms", ion.get("mode"), f"<p>Second queue: <code>{e(ion.get('creates_second_queue'))}</code></p><p>Second agent system: <code>{e(ion.get('creates_second_agent_system'))}</code></p>"),
        ],
        "settings": [
            drawer("settings", "Settings", "Local", f"<p>Execution default: <code>{e(execution.get('default_mode'))}</code></p><p>Runner start enabled: <code>{e(execution.get('runner_start_enabled', False))}</code></p><p>Response carrier: <code>{e(response_carrier.get('enabled', False))}</code></p><p>Memory: <code>{e(settings.get('memory_path'))}</code></p>"),
        ],
    }
    tabs = [
        ("assistant", "Assistant"),
        ("context", "Context"),
        ("evidence", "Evidence"),
        ("system", "System"),
        ("settings", "Settings"),
    ]
    tab_buttons = "".join(
        f'<button class="inspector-tab{" is-active" if tab_id == "assistant" else ""}" type="button" data-inspector-target="{e(tab_id)}">{e(label)}</button>'
        for tab_id, label in tabs
    )
    panel_html = "".join(
        f'<section class="inspector-panel{" is-active" if tab_id == "assistant" else ""}" data-inspector-panel="{e(tab_id)}"{" hidden" if tab_id != "assistant" else ""}>{"".join(panels[tab_id])}</section>'
        for tab_id, _label in tabs
    )
    return (
        '<aside class="capsule-inspector" aria-label="Codex inspector">'
        f'<div class="inspector-tabs" role="tablist" aria-label="Inspector tabs">{tab_buttons}</div>'
        f"{panel_html}</aside>"
    )
