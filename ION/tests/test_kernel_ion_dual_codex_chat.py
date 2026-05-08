import json
from pathlib import Path

from kernel import ion_dual_codex_chat
from kernel.ion_codex_chat_app_ui import render_codex_chat_app_html
from kernel.ion_codex_solo_context import (
    CAPSULE_PATH,
    CONTEXT_PACKAGES_PATH,
    HOT_CONTEXT_PATH,
    LONG_HORIZON_PATH,
    MINI_PATH,
    READY_VERDICT,
)
from kernel.ion_dual_codex_chat import (
    WRITE_CONFIRMATION_TOKEN,
    build_dual_codex_chat_model,
    queue_chat_codex_work_packet,
    record_chat_turn,
    render_dual_codex_chat_html,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    for rel, text in {
        "ION/REPO_AUTHORITY.md": "# authority\n",
        "ION/03_registry/agent_context_system_registry.yaml": "legacy_surfaces_policy: {}\n",
        "ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_OPERATING_CONTEXT_V105.md": "# lead\n",
        "ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md": "# research\n",
        "ION/02_architecture/CODEX_CAPSULE_OPERATING_PROTOCOL.md": "# capsule operating protocol\n",
        "ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md": "# skill activation protocol\n",
        "ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md": "# chat engine protocol\n",
        "ION/03_registry/ion_native_lens_registry.yaml": (
            "schema_id: ion.native_lens_registry.v1\n"
            "production_authority: false\n"
            "live_execution_authority: false\n"
            "secrets_authority: false\n"
            "default_lenses: [persona, context_cartographer]\n"
            "lenses:\n"
            "  - lens_id: persona\n"
            "    display_name: Persona\n"
            "    role_id: role.persona_interface\n"
            "    purpose: User-facing clarity.\n"
            "    use_when: [normal_chat]\n"
            "    model_stage_id: persona_response\n"
            "    template_refs: [ION/07_templates/bindings/PERSONA_INTERFACE__USER_RESPONSE.md]\n"
            "  - lens_id: context_cartographer\n"
            "    display_name: Context Cartographer\n"
            "    role_id: role.context_cartographer\n"
            "    purpose: Context mount and drift prevention.\n"
            "    use_when: [normal_chat, context_mount]\n"
            "    model_stage_id: relay_ingress\n"
            "    template_refs: [ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md]\n"
            "  - lens_id: mason_codex\n"
            "    display_name: Mason/Codex\n"
            "    role_id: role.mason\n"
            "    purpose: Bounded implementation.\n"
            "    use_when: [queue_work]\n"
            "    model_stage_id: mason_codex_work\n"
            "    template_refs: [ION/07_templates/bindings/MASON__CODE.md]\n"
            "  - lens_id: steward\n"
            "    display_name: Steward\n"
            "    role_id: role.steward\n"
            "    purpose: Authority and risk.\n"
            "    use_when: [mutation]\n"
            "    model_stage_id: steward_route\n"
            "    template_refs: [ION/07_templates/bindings/STEWARD__TASK.md]\n"
            "  - lens_id: scribe\n"
            "    display_name: Scribe\n"
            "    role_id: role.scribe\n"
            "    purpose: Receipts.\n"
            "    use_when: [receipt]\n"
            "    model_stage_id: relay_return\n"
            "    template_refs: [ION/07_templates/reports/STATUS_REPORT.md]\n"
        ),
        "ION/03_registry/ion_skill_registry.yaml": (
            "schema_id: ion.skill_registry.v1\n"
            "production_authority: false\n"
            "live_execution_authority: false\n"
            "secrets_authority: false\n"
            "principle: Skills activate workflows; templates govern proof.\n"
            "global_proof_contract:\n"
            "  context_proof_required: true\n"
            "skills:\n"
            "  - skill_id: codex-chat-answer\n"
            "    display_name: Codex Chat Answer\n"
            "    class: user_visible\n"
            "    purpose: Answer normal chat.\n"
            "    trigger_summary: Default chat.\n"
            "    model_stage_id: persona_response\n"
            "    preferred_model: gpt-5.5\n"
            "    default_reasoning_effort: medium\n"
            "    activates_templates:\n"
            "      - ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md\n"
            "    template_bindings: []\n"
            "    context_mount:\n"
            "      required_packages: [minimum_working_capsule, mini_lookup_index, mission_active_package]\n"
            "      route_deeper_packages: [active_authority_package, route_depth_package]\n"
            "    allowed_authority:\n"
            "      read_context: true\n"
            "      queue_work: false\n"
            "      write_files: false\n"
            "      production_authority: false\n"
            "      live_execution_authority: false\n"
            "      secrets_authority: false\n"
            "    proof_contract:\n"
            "      context_proof_required: true\n"
            "      template_action_proof_required: false\n"
            "      receipt_required: false\n"
            "    ui: {label: Chat, drawer_visible: true, user_chore: false}\n"
            "  - skill_id: codex-solo-work\n"
            "    display_name: Codex Work\n"
            "    class: user_visible\n"
            "    purpose: Queue bounded Codex work.\n"
            "    trigger_summary: Run task.\n"
            "    model_stage_id: mason_codex_work\n"
            "    preferred_model: gpt-5.3-codex\n"
            "    default_reasoning_effort: medium\n"
            "    activates_templates:\n"
            "      - ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md\n"
            "      - ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md\n"
            "    template_bindings: []\n"
            "    context_mount:\n"
            "      required_packages: [minimum_working_capsule, mini_lookup_index, active_authority_package, mission_active_package]\n"
            "      route_deeper_packages: [route_depth_package, evidence_receipt_package]\n"
            "    allowed_authority:\n"
            "      read_context: true\n"
            "      queue_work: true\n"
            "      write_files: bounded_scoped_only\n"
            "      production_authority: false\n"
            "      live_execution_authority: false\n"
            "      secrets_authority: false\n"
            "    proof_contract:\n"
            "      context_proof_required: true\n"
            "      template_action_proof_required: true\n"
            "      receipt_required: true\n"
            "    ui: {label: Work, drawer_visible: true, user_chore: false}\n"
            "  - skill_id: codex-recovery\n"
            "    display_name: Recovery\n"
            "    class: user_visible\n"
            "    purpose: Recover drift.\n"
            "    trigger_summary: Recovery.\n"
            "    model_stage_id: steward_route\n"
            "    preferred_model: gpt-5.5\n"
            "    default_reasoning_effort: high\n"
            "    activates_templates: [ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md]\n"
            "    template_bindings: []\n"
            "    context_mount: {required_packages: [minimum_working_capsule], route_deeper_packages: [recovery_package]}\n"
            "    allowed_authority: {read_context: true, queue_work: false, write_files: false, production_authority: false, live_execution_authority: false, secrets_authority: false}\n"
            "    proof_contract: {context_proof_required: true, template_action_proof_required: true, receipt_required: true}\n"
            "    ui: {label: Recover, drawer_visible: true, user_chore: false}\n"
            "  - skill_id: ion-full-workflow-handoff\n"
            "    display_name: ION Handoff\n"
            "    class: bridge\n"
            "    purpose: Full ION handoff.\n"
            "    trigger_summary: ION lane.\n"
            "    model_stage_id: relay_ingress\n"
            "    preferred_model: gpt-5.3-codex-spark\n"
            "    default_reasoning_effort: low\n"
            "    activates_templates: [ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md]\n"
            "    template_bindings: []\n"
            "    context_mount: {required_packages: [active_authority_package], route_deeper_packages: [route_depth_package]}\n"
            "    allowed_authority: {read_context: true, queue_work: bounded_existing_queue_only, write_files: false, production_authority: false, live_execution_authority: false, secrets_authority: false}\n"
            "    proof_contract: {context_proof_required: true, template_action_proof_required: true, receipt_required: true}\n"
            "    ui: {label: ION Handoff, drawer_visible: true, user_chore: false}\n"
            "  - skill_id: template-curation\n"
            "    display_name: Template Curation\n"
            "    class: specialist\n"
            "    purpose: Govern skills and templates.\n"
            "    trigger_summary: Skills/templates.\n"
            "    model_stage_id: vizier_plan\n"
            "    preferred_model: gpt-5.5\n"
            "    default_reasoning_effort: high\n"
            "    activates_templates: [ION/07_templates/actions/TEMPLATE_DEVELOPMENT.md]\n"
            "    template_bindings: []\n"
            "    context_mount: {required_packages: [active_authority_package], route_deeper_packages: [route_depth_package]}\n"
            "    allowed_authority: {read_context: true, queue_work: false, write_files: scoped_governance_surfaces_only, production_authority: false, live_execution_authority: false, secrets_authority: false}\n"
            "    proof_contract: {context_proof_required: true, template_action_proof_required: true, receipt_required: true}\n"
            "    ui: {label: Templates, drawer_visible: true, user_chore: false}\n"
        ),
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md": "# orchestration\n",
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md": "# ui orchestration\n",
    }.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def _write_json(root: Path, rel: str, payload: dict) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_chat_proof_packets(root: Path, *, request_id: str, request_rel: str, accepted: bool) -> tuple[str, str]:
    run_rel = f"ION/05_context/current/chatgpt_connector/codex_queue_runs/run_{request_id}/run.json"
    return_rel = f"ION/05_context/current/chatgpt_connector/task_returns/return_{request_id}.json"
    status = "RETURN_RECORDED_PROOF_ACCEPTED" if accepted else "RETURN_RECORDED_PROOF_BLOCKED"
    _write_json(
        root,
        request_rel,
        {
            "schema_id": "ion.chatgpt_browser_connector_codex_work_request.v1",
            "request_id": request_id,
            "packet_path": request_rel,
            "status": status,
            "latest_context_proof_accepted": accepted,
            "latest_template_action_proof_accepted": accepted,
            "codex_queue_runner_runs": [run_rel],
            "return_packet_paths": [return_rel],
            "latest_return_packet_path": return_rel,
        },
    )
    _write_json(
        root,
        run_rel,
        {
            "schema_id": "ion.codex_queue_runner_run.v1",
            "run_id": f"run_{request_id}",
            "request_id": request_id,
            "request_path": request_rel,
            "run_packet_path": run_rel,
            "status": status,
            "last_message_path": f"ION/05_context/current/chatgpt_connector/codex_queue_runs/run_{request_id}/latest_return.md",
        },
    )
    _write_json(
        root,
        return_rel,
        {
            "schema_id": "ion.chatgpt_browser_connector_task_return_packet.v1",
            "work_request_id": request_id,
            "work_request_path": request_rel,
            "accepted_for_carrier_intake": accepted,
            "task_output_preview": "### RESULT\nCodex return proof for the originating chat turn.",
            "context_proof_result": {"accepted": accepted, "findings": [] if accepted else ["missing_required_path"]},
            "template_action_proof_result": {
                "accepted": accepted,
                "findings": [] if accepted else ["touched_paths_missing"],
                "touched_paths": ["ION/04_packages/kernel/ion_dual_codex_chat.py"],
            },
        },
    )
    return run_rel, return_rel


def test_capsule_chat_model_includes_codex_solo_context(tmp_path: Path):
    _seed_root(tmp_path)
    response_run = tmp_path / "ION/05_context/current/codex_capsule_chat/response_runs/fake_response/run.json"
    response_run.parent.mkdir(parents=True, exist_ok=True)
    response_run.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_chat_response_carrier_run.v1",
                "run_id": "fake_response",
                "created_at": "2026-05-08T00:00:00+00:00",
                "updated_at": "2026-05-08T00:00:01+00:00",
                "status": "RETURN_CAPTURED",
                "ok": True,
                "selected_model": "gpt-5.5",
                "selected_reasoning_effort": "medium",
                "prompt_path": "ION/05_context/current/codex_capsule_chat/response_runs/fake_response/prompt.md",
                "latest_return_path": "ION/05_context/current/codex_capsule_chat/response_runs/fake_response/latest_return.md",
                "events_path": "ION/05_context/current/codex_capsule_chat/response_runs/fake_response/events.jsonl",
                "response_sha256": "abc123",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    model = build_dual_codex_chat_model(tmp_path, write=True)

    assert model["verdict"] == "ION_CODEX_CAPSULE_CHAT_READY"
    assert model["product"]["primary_lane_id"] == "codex_general"
    assert model["product"]["dual_chat_infrastructure"] is False
    assert model["ion_comms"]["creates_second_queue"] is False
    assert model["ui"]["schema_id"] == "ion.codex_capsule_chat_ui_model.v1"
    assert model["ui"]["layout"]["primary_surface"] == "main_chat"
    assert model["ui"]["composer"]["primary_label"] == "Send"
    assert model["ui"]["composer"]["run_label"] == "Run task"
    assert "context" in model["ui"]["drawers"]
    assert "capsule" in model["ui"]["drawers"]
    assert model["turn_traces"]["schema_id"] == "ion.codex_capsule_chat_turn_trace_index.v1"
    assert model["turn_traces"]["raw_hidden_reasoning_exposed"] is False
    assert model["agents"]["schema_id"] == "ion.codex_capsule_chat_agent_surface.v1"
    assert model["agents"]["creates_second_agent_system"] is False
    assert model["skills"]["schema_id"] == "ion.skill_surface.v1"
    assert model["skills"]["current_activation"]["skill_id"] == "codex-chat-answer"
    assert model["skills"]["current_activation"]["state_acceptance_granted"] is False
    assert model["skills"]["current_activation"]["activates_templates"]
    assert model["chat_engine"]["schema_id"] == "ion.codex_chat_engine_surface.v1"
    assert model["chat_engine"]["ok"] is True
    assert model["assistant_work_routes"]["schema_id"] == "ion.assistant_work_route_surface.v0_1"
    assert model["assistant_work_routes"]["candidate_only"] is True
    assert "assistant_work_routes" in model["ui"]["drawers"]
    assert model["chat_response_carrier"]["schema_id"] == "ion.codex_chat_response_carrier_status.v1"
    assert model["chat_response_carrier"]["enabled"] is False
    assert model["response_runs"]["schema_id"] == "ion.codex_chat_response_run_surface.v1"
    assert model["response_runs"]["record_count"] == 1
    assert model["response_runs"]["records"][0]["prompt_path"].endswith("prompt.md")
    assert model["ui"]["drawers"]["runs"]["response_runs"]["records"][0]["latest_return_path"].endswith("latest_return.md")
    assert model["codex_solo_context"]["verdict"] == READY_VERDICT
    assert model["lanes"]["codex_general"]["context_substrate"]["active_context"]["minimum_context_path"] == CAPSULE_PATH.as_posix()
    assert model["lanes"]["codex_general"]["context_substrate"]["paths"]["hot_context"] == HOT_CONTEXT_PATH.as_posix()
    assert model["model_moves"]["routing_posture"] == "conserve_main_bank"
    assert model["mini_auto_post"]["last_turn_id"].startswith("mini_")
    turns = model["lanes"]["codex_general"]["turns"]
    assert turns[-1]["author"] == "ion_context"
    assert turns[-1]["kind"] == "mini_auto_post"
    assert "ION Mini capsule brief" in turns[-1]["message"]


def test_capsule_chat_html_is_single_primary_chat_with_secondary_ion_comms(tmp_path: Path):
    _seed_root(tmp_path)

    model = build_dual_codex_chat_model(tmp_path, write=True)
    html = render_dual_codex_chat_html(model, base_path="/chat")

    assert render_codex_chat_app_html(model, base_path="/chat") == html
    assert 'data-ui="ion-codex-chat-app"' in html
    assert 'class="capsule-left-rail"' in html
    assert 'class="capsule-left-drawer"' in html
    assert 'class="capsule-main-chat"' in html
    assert 'class="capsule-inspector"' in html
    assert 'class="capsule-right-rail"' in html
    assert 'class="capsule-activity-strip"' in html
    assert 'aria-label="Codex Chat"' in html
    assert 'class="composer-mode"' in html
    assert "ION Codex Chat" in html
    assert "Ask Codex" in html
    assert "Run task" in html
    assert "Codex Capsule Chat" not in html
    assert "Message Codex Capsule" not in html
    assert "Run with Codex" not in html
    assert "Timeline" in html
    assert "Response Carrier Runs" in html
    assert "Agents" in html
    assert "Skills" in html
    assert "Context Lens" in html
    assert "top-page-tabs" in html
    assert "inspector-tabs" in html
    assert "data-page-target=\"context\"" in html
    assert "data-left-drawer-target=\"composer\"" in html
    assert "data-inspector-target=\"evidence\"" in html
    assert "data-timeline-filter=\"task_return\"" in html
    assert "Codex Chat Answer" in html
    assert "Active Template Gates" in html
    assert "Chat Engine" in html
    assert "Assistant Work Routes" in html
    assert "candidate_route_metadata_only_no_registry_or_product_law_mutation" in html
    assert "Native Lenses" in html
    assert "Response Carrier" in html
    assert "Trace Event Flow" in html
    assert "Memory View" in html
    assert "Memory Windows" in html
    assert "Available Agents" in html
    assert "No separate agent system" in html
    assert "No recent agent invocations." in html
    assert "/chat/turn" in html
    assert "data-busy-label=\"Sending...\"" in html
    assert "Codex is working on this response. The carrier can take a few seconds" in html
    assert "form.dataset.submitting === \"true\"" in html
    assert "\"Accept\": \"application/json\"" in html
    assert "textarea.value = \"\"" in html
    assert "payload.execution_status_turn" in html
    assert "Write to this lane" not in html
    assert "Queue proof-gated Codex work packet" not in html
    assert "Pin explicit memory" not in html


def test_codex_chat_ui_model_has_joc_shell_behavior_contract(tmp_path: Path):
    _seed_root(tmp_path)

    model = build_dual_codex_chat_model(tmp_path, write=True)
    ui = model["ui"]

    assert ui["layout"]["mode"] == "joc_shell_chat_first"
    assert ui["layout"]["zones"] == [
        "top_bar",
        "left_icon_rail",
        "left_drawer",
        "main_work_surface",
        "right_inspector",
        "right_icon_rail",
        "bottom_timeline",
    ]
    assert [tab["id"] for tab in ui["top_bar"]["page_tabs"]] == ["chat", "context", "runs", "agents", "receipts", "settings"]
    assert [item["id"] for item in ui["left_rail"]] == ["composer", "models", "skills", "context-lens", "run-mode"]
    assert ui["left_drawer"]["active_panel_id"] == "composer"
    assert [item["id"] for item in ui["right_rail"]] == ["assistant", "context", "evidence", "system", "settings"]
    assert [lane["id"] for lane in ui["bottom_timeline"]["lanes"]] == ["all", "runner", "work_request", "task_return"]


def test_codex_chat_ui_renderer_is_componentized():
    app_path = Path(ion_dual_codex_chat.__file__).with_name("ion_codex_chat_app_ui.py")
    module_names = {
        "ion_codex_chat_shell_ui.py",
        "ion_codex_chat_main_ui.py",
        "ion_codex_chat_left_drawer_ui.py",
        "ion_codex_chat_right_inspector_ui.py",
        "ion_codex_chat_timeline_ui.py",
        "ion_codex_chat_memory_visualization_ui.py",
        "ion_codex_chat_assets_ui.py",
        "ion_codex_chat_ui_common.py",
    }

    assert len(app_path.read_text(encoding="utf-8").splitlines()) <= 40
    for name in module_names:
        path = app_path.with_name(name)
        assert path.exists(), name
        assert path.read_text(encoding="utf-8").strip()


def test_codex_general_turn_creates_visible_assistant_response(tmp_path: Path):
    _seed_root(tmp_path)

    result = record_chat_turn(tmp_path, lane_id="codex_general", message="Help me inspect the capsule setup.")

    assert result["ok"] is True
    assert result["assistant_turn"]["author"] == "codex_chat_engine"
    assert result["assistant_turn"]["kind"] == "assistant_response"
    assert "Codex Capsule context" in result["assistant_turn"]["message"] or "Capsule context" in result["assistant_turn"]["message"]
    assert CAPSULE_PATH.as_posix() in result["assistant_turn"]["context_refs"]
    assert result["assistant_turn"]["response_mode"] == "answer"
    assert result["assistant_turn"]["chat_engine"]["response_contract"]["quality_target"] == "chatgpt_browser_level_or_better"
    turns = result["model"]["lanes"]["codex_general"]["turns"]
    assert any(turn["kind"] == "assistant_response" for turn in turns)
    groups = result["model"]["ui"]["conversation"]["turn_groups"]
    assert groups[-1]["user_turn"]["message"] == "Help me inspect the capsule setup."
    assert groups[-1]["assistant_turns"]
    assert groups[-1]["turn_trace"]["event_count"] >= 3
    event_types = [event["event_type"] for event in groups[-1]["turn_trace"]["events"]]
    assert "context_mount" in event_types
    assert "skill_activation" in event_types
    assert "chat_engine" in event_types
    assert "assistant_work_route" in event_types
    assert "codex_chat_response_carrier" in event_types
    assert "assistant_response" in event_types
    assert "execution_bridge" in event_types
    html = render_dual_codex_chat_html(result["model"], base_path="/chat")
    assert "Turn trace" in html
    assert "Trace Event Flow" in html
    assert "context_mount" in html
    assert "skill_activation" in html
    assert "chat_engine" in html
    assert "Raw hidden reasoning is not exposed." in html
    assert result["turn"]["skill_activation"]["skill_id"] == "codex-chat-answer"
    assert result["turn"]["chat_engine"]["model_move"]["selected_model"] == "gpt-5.5"
    assert result["turn"]["chat_engine"]["assistant_work_route"]["candidate_only"] is True
    assert result["assistant_turn"]["response_carrier"]["status"] == "CARRIER_DISABLED"
    assert result["queue_result"] is None


def test_playwright_pending_smoke_turn_is_ephemeral(tmp_path: Path):
    _seed_root(tmp_path)

    result = record_chat_turn(
        tmp_path,
        lane_id="codex_general",
        message="playwright-pending-smoke-123: reply exactly playwright-ok",
    )

    assert result["ok"] is True
    assert result["assistant_turn"]["message"] == "playwright-ok"
    assert result["turn"]["kind"] == "playwright_smoke_probe"
    assert result["turn"]["persistence"] == "ephemeral_not_saved"
    assert result["smoke_probe"]["production_state_mutated"] is False
    assert result["assistant_turn"]["response_carrier"]["status"] == "BYPASSED_FOR_EPHEMERAL_PLAYWRIGHT_SMOKE"

    model = build_dual_codex_chat_model(tmp_path, write=True)
    messages = [
        str(turn.get("message") or "")
        for turn in model["lanes"]["codex_general"]["turns"]
        if isinstance(turn, dict)
    ]
    assert not any("playwright-pending-smoke-" in message for message in messages)
    assert "playwright-ok" not in messages


def test_memory_visualization_projects_context_windows_and_protocol_manifest(tmp_path: Path):
    _seed_root(tmp_path)

    result = record_chat_turn(tmp_path, lane_id="codex_general", message="How should this chat use Capsule context?")

    visualization = result["model"]["memory_visualization"]
    assert visualization["schema_id"] == "ion.codex_chat_memory_visualization.v1"
    assert visualization["selected_turn_id"] == result["turn"]["turn_id"]
    assert visualization["raw_hidden_reasoning_exposed"] is False
    assert visualization["production_authority"] is False
    assert visualization["live_execution_authority"] is False

    segments = visualization["memory_segments"]
    window_classes = {segment["window_class"] for segment in segments}
    assert {"LIVE_INPUT", "ACTIVE_CONTEXT", "HOT_CONTEXT", "MINI_LOOKUP", "LONG_HORIZON"}.issubset(window_classes)
    assert all(segment["raw_hidden_reasoning_exposed"] is False for segment in segments)
    assert any(segment["segment_id"] == "context:capsule" for segment in segments)
    assert any(segment["segment_id"] == "context:long_horizon" for segment in segments)
    assert any(segment["selection_signals"] == ["capsule_minimum_context"] for segment in segments)

    edges = visualization["context_route_edges"]
    assert any(edge["edge_type"] == "retrieved" for edge in edges)
    assert any(edge["from_segment_id"] == f"turn:{result['turn']['turn_id']}" for edge in edges)

    manifest = visualization["protocol_manifest_summary"]
    assert manifest["current_branch_id"] == "answer"
    assert manifest["c1_c2_c3_mode"] == "C2_REACTIVE_WORKER"
    assert manifest["required_human_acceptance"] is False
    assert CAPSULE_PATH.as_posix() in manifest["next_files_or_sources"]

    package_summary = visualization["prompt_package_summary"]
    assert package_summary["minimum_context"] == CAPSULE_PATH.as_posix()
    assert package_summary["mini_role"] == "lookup_receipt_index_not_primary_prompt"

    selected = visualization["selected_turn_context"]
    assert selected["schema_id"] == "ion.codex_chat_selected_turn_context.v1"
    assert selected["selected_segment_id"] == f"turn:{result['turn']['turn_id']}"
    assert "context:capsule" in selected["directly_related_segment_ids"]
    assert "context:mini" in selected["directly_related_segment_ids"]
    assert any(item.startswith("turn:") for item in selected["active_prompt_segment_ids"])
    assert selected["raw_hidden_reasoning_exposed"] is False

    layers = {layer["layer_id"]: layer for layer in visualization["context_matryoshka_layers"]}
    assert set(layers) == {"active_crucible", "priority_capsule", "x_ray_dag", "background_swarm"}
    assert "LIVE_INPUT" in layers["active_crucible"]["window_classes"]
    assert layers["priority_capsule"]["segment_count"] >= 2
    assert layers["background_swarm"]["segment_count"] >= 1

    token_summary = visualization["token_budget_summary"]
    assert token_summary["estimated_total_tokens"] > 0
    assert token_summary["max_context_tokens_authoritative"] is False

    event_types = {event["event_type"] for event in visualization["carrier_phase_events"]}
    assert {"context_mount", "skill_activation", "chat_engine", "assistant_response"}.issubset(event_types)
    assert result["model"]["ui"]["drawers"]["context"]["memory_visualization"]["schema_id"] == visualization["schema_id"]


def test_memory_visualization_html_exposes_smart_context_layers(tmp_path: Path):
    _seed_root(tmp_path)

    result = record_chat_turn(tmp_path, lane_id="codex_general", message="Show me how context is being routed.")
    html = render_dual_codex_chat_html(result["model"], base_path="/chat")

    assert "Context Budget" in html
    assert "Selected Turn Context" in html
    assert "Memory Strata" in html
    assert "Contextual Matryoshka" in html
    assert "Context Route Graph" in html
    assert "Compaction Timeline" in html
    assert "Protocol Manifest" in html
    assert "Source Ref Drilldown" in html
    assert "Selected Context Node" in html
    assert "Active Crucible" in html
    assert "Priority Capsule" in html
    assert "X-Ray DAG" in html
    assert "Background Swarm" in html
    assert "data-memory-selection-panel" in html
    assert "data-memory-segment-id=\"context:capsule\"" in html
    assert "data-memory-turn-id=" in html
    assert "data-memory-selection-field=\"turn\"" in html
    assert "data-route-edge-id=" in html
    assert "data-route-from=" in html
    assert "data-route-edge-filter=\"compressed_to\"" in html
    assert "data-route-edge-type=\"retrieved\"" in html
    assert "route-summary-grid" in html
    assert "data-source-ref=" in html
    assert "data-source-kind=\"source_ref\"" in html
    assert "data-source-group=" in html
    assert "data-source-group-filter=" in html
    assert "data-source-ref-lane=" in html
    assert "data-trace-event-id=" in html
    assert "data-trace-type=\"context_mount\"" in html
    assert "data-chat-turn-id=" in html
    assert "selectMemorySegment" in html
    assert "selectRouteEdge" in html
    assert "selectSourceRef" in html
    assert "selectTraceEvent" in html
    assert "persistMemorySelection" in html
    assert "restoreMemorySelection" in html
    assert "sourceGroupFilter" in html
    assert "ion.codexChat.selectedInspection" in html
    assert "is-selected-memory" in html
    assert "data-memory-window-class=\"LIVE_INPUT\"" in html
    assert "data-memory-window-class=\"ACTIVE_CONTEXT\"" in html
    assert "data-memory-window-class=\"MINI_LOOKUP\"" in html
    assert "data-memory-window-class=\"LONG_HORIZON\"" in html
    assert "retrieved" in html
    assert "compressed_to" in html
    assert "raw_hidden_reasoning_exposed" not in html


def test_memory_visualization_redacts_secret_like_values(tmp_path: Path):
    _seed_root(tmp_path)

    result = record_chat_turn(
        tmp_path,
        lane_id="codex_general",
        message="Please reason about this without exposing token=abc123456789.",
    )

    visualization = result["model"]["memory_visualization"]
    previews = "\n".join(segment["text_preview"] for segment in visualization["memory_segments"])
    assert "abc123456789" not in previews
    assert "token=[REDACTED]" in previews
    forbidden_refs = {item["ref"] for item in visualization["forbidden_or_omitted_refs"]}
    assert "raw_hidden_chain_of_thought" in forbidden_refs
    assert "secret_token_values" in forbidden_refs


def test_codex_general_turn_uses_response_carrier_when_available(tmp_path: Path, monkeypatch):
    _seed_root(tmp_path)

    def fake_response_carrier(_root, *, operator_message, chat_engine_turn, codex_solo_context=None, prior_turns=None):
        return {
            "schema_id": "ion.codex_chat_response_carrier_run.v1",
            "ok": True,
            "status": "RETURN_CAPTURED_FAKE",
            "response_text": f"Carrier response for: {operator_message}",
            "response_sha256": "abc123",
            "run": {
                "run_packet_path": "ION/05_context/current/codex_capsule_chat/response_runs/fake/run.json",
                "latest_return_path": "ION/05_context/current/codex_capsule_chat/response_runs/fake/latest_return.md",
                "events_path": "ION/05_context/current/codex_capsule_chat/response_runs/fake/events.jsonl",
            },
            "production_authority": False,
            "live_execution_authority": False,
        }

    monkeypatch.setattr(ion_dual_codex_chat, "run_codex_chat_response_carrier", fake_response_carrier)

    result = record_chat_turn(tmp_path, lane_id="codex_general", message="Give a real chat answer.")

    assert result["ok"] is True
    assert result["assistant_turn"]["message"] == "Carrier response for: Give a real chat answer."
    assert result["assistant_turn"]["response_carrier"]["status"] == "RETURN_CAPTURED_FAKE"
    groups = result["model"]["ui"]["conversation"]["turn_groups"]
    event_types = [event["event_type"] for event in groups[-1]["turn_trace"]["events"]]
    assert "codex_chat_response_carrier" in event_types
    html = render_dual_codex_chat_html(result["model"], base_path="/chat")
    assert "Carrier response for: Give a real chat answer." in html


def test_codex_general_turn_can_queue_same_message_for_codex(tmp_path: Path, monkeypatch):
    _seed_root(tmp_path)
    captured: dict[str, str] = {}

    def fake_connector(_root, tool_name, args):
        captured["tool_name"] = tool_name
        captured["objective"] = args["objective"]
        captured["request_kind"] = args["request_kind"]
        captured["engine_mode"] = args["ion_chat_engine_turn"]["response_mode"]
        return {
            "ok": True,
            "data": {
                "request_id": "codex_req_chat_turn",
                "packet_path": "ION/05_context/current/chatgpt_connector/codex_work_requests/chat_turn.json",
            },
        }

    monkeypatch.setattr(ion_dual_codex_chat, "call_chatgpt_connector_tool", fake_connector)

    result = record_chat_turn(
        tmp_path,
        lane_id="codex_general",
        message="Implement this from chat.",
        execution_mode="queue_for_codex",
    )

    assert result["ok"] is True
    assert result["execution_mode"] == "queue_for_codex"
    assert result["queue_result"]["ok"] is True
    assert result["queue_result"]["queue_link"]["request_id"] == "codex_req_chat_turn"
    assert result["queue_result"]["queue_link"]["source_turn_id"] == result["turn"]["turn_id"]
    assert result["runner_result"] is None
    assert result["execution_status_turn"]["kind"] == "execution_status"
    assert "Codex execution bridge status." in result["execution_status_turn"]["message"]
    assert captured["tool_name"] == "ion_request_codex_work_packet"
    assert captured["request_kind"] == "codex_work"
    assert captured["engine_mode"] == "queue_work"
    assert "Operator objective:\nImplement this from chat." in captured["objective"]
    turns = result["model"]["lanes"]["codex_general"]["turns"]
    assert any(turn.get("kind") == "execution_status" for turn in turns)


def test_codex_task_return_hydrates_under_originating_chat_turn(tmp_path: Path, monkeypatch):
    _seed_root(tmp_path)
    request_rel = "ION/05_context/current/chatgpt_connector/codex_work_requests/chat_turn.json"

    def fake_connector(_root, _tool_name, _args):
        return {
            "ok": True,
            "data": {
                "request_id": "codex_req_chat_turn",
                "packet_path": request_rel,
            },
        }

    monkeypatch.setattr(ion_dual_codex_chat, "call_chatgpt_connector_tool", fake_connector)

    result = record_chat_turn(
        tmp_path,
        lane_id="codex_general",
        message="Implement this from chat and show me the proof.",
        execution_mode="queue_for_codex",
    )
    _run_rel, return_rel = _write_chat_proof_packets(
        tmp_path,
        request_id="codex_req_chat_turn",
        request_rel=request_rel,
        accepted=True,
    )

    model = build_dual_codex_chat_model(tmp_path, write=True)
    hydration = model["codex_queue"]["return_hydration"]
    assert hydration["record_count"] == 1
    assert hydration["accepted_count"] == 1
    record = hydration["records"][0]
    assert record["source_turn_id"] == result["turn"]["turn_id"]
    assert record["proof_status"] == "accepted"
    assert record["latest_return_path"] == return_rel
    groups = model["ui"]["conversation"]["turn_groups"]
    assert groups[-1]["return_records"][0]["request_id"] == "codex_req_chat_turn"
    assert any(event["event_type"] == "proof_return" for event in groups[-1]["turn_trace"]["events"])
    html = render_dual_codex_chat_html(model, base_path="/chat")
    assert "Proof accepted" in html
    assert "ion_submit_task_return" in html
    assert return_rel in html


def test_blocked_codex_task_return_is_visible_as_blocked_proof(tmp_path: Path, monkeypatch):
    _seed_root(tmp_path)
    request_rel = "ION/05_context/current/chatgpt_connector/codex_work_requests/chat_turn_blocked.json"

    def fake_connector(_root, _tool_name, _args):
        return {
            "ok": True,
            "data": {
                "request_id": "codex_req_chat_turn_blocked",
                "packet_path": request_rel,
            },
        }

    monkeypatch.setattr(ion_dual_codex_chat, "call_chatgpt_connector_tool", fake_connector)

    record_chat_turn(
        tmp_path,
        lane_id="codex_general",
        message="Run this but surface refusal proof if it fails.",
        execution_mode="queue_for_codex",
    )
    _write_chat_proof_packets(
        tmp_path,
        request_id="codex_req_chat_turn_blocked",
        request_rel=request_rel,
        accepted=False,
    )

    model = build_dual_codex_chat_model(tmp_path, write=True)
    hydration = model["codex_queue"]["return_hydration"]
    assert hydration["blocked_count"] == 1
    assert hydration["records"][0]["proof_status"] == "blocked"
    html = render_dual_codex_chat_html(model, base_path="/chat")
    assert "Proof blocked" in html
    assert "missing_required_path" in html


def test_codex_general_turn_refuses_runner_start_without_env(tmp_path: Path, monkeypatch):
    _seed_root(tmp_path)

    def fake_connector(_root, _tool_name, _args):
        return {
            "ok": True,
            "data": {
                "request_id": "codex_req_chat_turn",
                "packet_path": "ION/05_context/current/chatgpt_connector/codex_work_requests/chat_turn.json",
            },
        }

    monkeypatch.setattr(ion_dual_codex_chat, "call_chatgpt_connector_tool", fake_connector)
    monkeypatch.delenv("ION_CODEX_CAPSULE_CHAT_ALLOW_RUNNER_START", raising=False)

    result = record_chat_turn(
        tmp_path,
        lane_id="codex_general",
        message="Run this if allowed.",
        execution_mode="queue_and_start",
    )

    assert result["ok"] is True
    assert result["queue_result"]["ok"] is True
    assert result["runner_result"]["ok"] is False
    assert result["runner_result"]["finding"] == "runner_start_not_enabled"
    assert result["execution_status_turn"]["runner_result"]["finding"] == "runner_start_not_enabled"


def test_ion_lane_turn_creates_full_pipeline_projection(tmp_path: Path):
    _seed_root(tmp_path)

    result = record_chat_turn(tmp_path, lane_id="ion_system", message="Route this through ION.")

    assert result["ok"] is True
    assert result["pipeline_run"]["status"] == "PIPELINE_PROJECTED_AWAITING_PROOF_GATED_WORK"
    assert len(result["pipeline_run"]["stages"]) == 8
    steward = result["pipeline_run"]["stages"][1]
    assert steward["stage_id"] == "steward_route"
    assert steward["model_move"]["selected_model"] == "gpt-5.5"
    assert steward["model_move"]["selected_reasoning_effort"] == "high"


def test_codex_general_queue_blocks_when_solo_context_route_missing(tmp_path: Path, monkeypatch):
    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("connector should not be called when solo route is blocked")

    monkeypatch.setattr(ion_dual_codex_chat, "call_chatgpt_connector_tool", fail_if_called)

    result = queue_chat_codex_work_packet(
        tmp_path,
        lane_id="codex_general",
        objective="Do the work.",
        confirmation=WRITE_CONFIRMATION_TOKEN,
    )

    assert result["ok"] is False
    assert result["finding"] == "codex_solo_context_not_ready"


def test_codex_general_queue_carries_hot_context_refs(tmp_path: Path, monkeypatch):
    _seed_root(tmp_path)
    captured: dict[str, str] = {}

    def fake_connector(_root, tool_name, args):
        captured["tool_name"] = tool_name
        captured["objective"] = args["objective"]
        captured["model_move"] = args["codex_model_move"]
        captured["required_context_reads"] = args["required_context_reads"]
        captured["request_kind"] = args["request_kind"]
        captured["chat_engine"] = args["ion_chat_engine_turn"]
        return {
            "ok": True,
            "data": {
                "request_id": "codex_req_test",
                "packet_path": "ION/05_context/current/chatgpt_connector/codex_work_requests/test.json",
            },
        }

    monkeypatch.setattr(ion_dual_codex_chat, "call_chatgpt_connector_tool", fake_connector)

    result = queue_chat_codex_work_packet(
        tmp_path,
        lane_id="codex_general",
        objective="Implement a focused fix.",
        confirmation=WRITE_CONFIRMATION_TOKEN,
    )

    assert result["ok"] is True
    assert captured["tool_name"] == "ion_request_codex_work_packet"
    assert CAPSULE_PATH.as_posix() in captured["objective"]
    assert HOT_CONTEXT_PATH.as_posix() in captured["objective"]
    assert MINI_PATH.as_posix() in captured["objective"]
    assert LONG_HORIZON_PATH.as_posix() in captured["objective"]
    assert CONTEXT_PACKAGES_PATH.as_posix() in captured["objective"]
    assert "Minimum working context" in captured["objective"]
    assert "Context package selector" in captured["objective"]
    assert "Codex model move:" in captured["objective"]
    assert "Chat engine route:" in captured["objective"]
    assert "Native lenses:" in captured["objective"]
    assert "Candidate Assistant Work route:" in captured["objective"]
    assert "Skill activation:" in captured["objective"]
    assert "Codex Work (codex-solo-work)" in captured["objective"]
    assert "Operator objective:\nImplement a focused fix." in captured["objective"]
    assert captured["model_move"]["selected_model"] == "gpt-5.3-codex"
    assert captured["model_move"]["selected_reasoning_effort"] == "medium"
    assert captured["request_kind"] == "codex_work"
    assert captured["chat_engine"]["response_mode"] == "queue_work"
    assert captured["required_context_reads"][0]["path"] == CAPSULE_PATH.as_posix()
    assert result["queue_link"]["context_refs"][0] == CAPSULE_PATH.as_posix()
    assert result["queue_link"]["skill_activation"]["skill_id"] == "codex-solo-work"
    assert result["queue_link"]["chat_engine"]["carrier_strategy"]["mode"] == "existing_codex_work_queue"
    assert result["queue_link"]["model_move"]["selected_model"] == "gpt-5.3-codex"
    assert HOT_CONTEXT_PATH.as_posix() in result["queue_link"]["context_refs"]
    assert result["codex_solo_post"]["capsule_entry_id"] == "C-001"
    turns = result["model"]["lanes"]["codex_general"]["turns"]
    assert turns[-1]["kind"] == "mini_auto_post"
    assert "LAST_RECEIPT: Queued Codex solo work packet" in turns[-1]["message"]
