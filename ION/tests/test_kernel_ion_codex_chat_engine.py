from pathlib import Path

from kernel.ion_codex_chat_engine import (
    build_codex_chat_carrier_objective,
    build_codex_chat_engine_turn,
    classify_response_mode,
    load_native_lens_registry,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    files = {
        "ION/REPO_AUTHORITY.md": "# authority\n",
        "ION/03_registry/agent_context_system_registry.yaml": "legacy_surfaces_policy: {}\n",
        "ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_OPERATING_CONTEXT_V105.md": "# lead\n",
        "ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md": "# research\n",
        "ION/02_architecture/CODEX_CAPSULE_OPERATING_PROTOCOL.md": "# capsule protocol\n",
        "ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md": "# skill protocol\n",
        "ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md": "# chat engine protocol\n",
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md": "# rebuild\n",
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md": "# ui\n",
        "ION/03_registry/ion_native_lens_registry.yaml": """
schema_id: ion.native_lens_registry.v1
production_authority: false
live_execution_authority: false
secrets_authority: false
default_lenses: [persona, context_cartographer]
lenses:
  - lens_id: persona
    display_name: Persona
    role_id: role.persona_interface
    purpose: User-facing clarity.
    model_stage_id: persona_response
    template_refs: [ION/07_templates/bindings/PERSONA_INTERFACE__USER_RESPONSE.md]
  - lens_id: context_cartographer
    display_name: Context Cartographer
    role_id: role.context_cartographer
    purpose: Context mount.
    model_stage_id: relay_ingress
    template_refs: [ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md]
  - lens_id: mason_codex
    display_name: Mason/Codex
    role_id: role.mason
    purpose: Bounded implementation.
    model_stage_id: mason_codex_work
    template_refs: [ION/07_templates/bindings/MASON__CODE.md]
  - lens_id: steward
    display_name: Steward
    role_id: role.steward
    purpose: Authority and risk.
    model_stage_id: steward_route
    template_refs: [ION/07_templates/bindings/STEWARD__TASK.md]
  - lens_id: scribe
    display_name: Scribe
    role_id: role.scribe
    purpose: Receipts.
    model_stage_id: relay_return
    template_refs: [ION/07_templates/reports/STATUS_REPORT.md]
""",
        "ION/03_registry/ion_skill_registry.yaml": """
schema_id: ion.skill_registry.v1
production_authority: false
live_execution_authority: false
secrets_authority: false
principle: Skills activate workflows; templates govern proof.
global_proof_contract:
  context_proof_required: true
skills:
  - skill_id: codex-chat-answer
    display_name: Codex Chat Answer
    class: user_visible
    purpose: Answer normal chat.
    trigger_summary: Default chat.
    preferred_model: gpt-5.5
    default_reasoning_effort: medium
    activates_templates: [ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md]
    template_bindings: []
    context_mount: {required_packages: [minimum_working_capsule, mini_lookup_index, mission_active_package], route_deeper_packages: [active_authority_package, route_depth_package]}
    allowed_authority: {read_context: true, queue_work: false, write_files: false, production_authority: false, live_execution_authority: false, secrets_authority: false}
    proof_contract: {context_proof_required: true, template_action_proof_required: false, receipt_required: false}
    ui: {label: Chat, drawer_visible: true, user_chore: false}
  - skill_id: codex-solo-work
    display_name: Codex Work
    class: user_visible
    purpose: Queue bounded Codex work.
    trigger_summary: Run task.
    preferred_model: gpt-5.3-codex
    default_reasoning_effort: medium
    activates_templates: [ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md]
    template_bindings: [ION/07_templates/bindings/MASON__CODE.md]
    context_mount: {required_packages: [minimum_working_capsule], route_deeper_packages: [evidence_receipt_package]}
    allowed_authority: {read_context: true, queue_work: true, write_files: bounded_scoped_only, production_authority: false, live_execution_authority: false, secrets_authority: false}
    proof_contract: {context_proof_required: true, template_action_proof_required: true, receipt_required: true}
    ui: {label: Work, drawer_visible: true, user_chore: false}
  - skill_id: codex-recovery
    display_name: Recovery
    class: user_visible
    purpose: Recover drift.
    trigger_summary: Recovery.
    preferred_model: gpt-5.5
    default_reasoning_effort: high
    activates_templates: [ION/07_templates/reports/AUDIT.md]
    template_bindings: []
    context_mount: {required_packages: [recovery_package], route_deeper_packages: [evidence_receipt_package]}
    allowed_authority: {read_context: true, queue_work: false, write_files: false, production_authority: false, live_execution_authority: false, secrets_authority: false}
    proof_contract: {context_proof_required: true, template_action_proof_required: true, receipt_required: true}
    ui: {label: Recover, drawer_visible: true, user_chore: false}
  - skill_id: ion-full-workflow-handoff
    display_name: ION Handoff
    class: bridge
    purpose: Full ION handoff.
    trigger_summary: ION lane.
    preferred_model: gpt-5.3-codex-spark
    default_reasoning_effort: low
    activates_templates: [ION/07_templates/bindings/RELAY__HANDOFF.md]
    template_bindings: []
    context_mount: {required_packages: [mission_active_package], route_deeper_packages: [route_depth_package]}
    allowed_authority: {read_context: true, queue_work: bounded_existing_queue_only, write_files: false, production_authority: false, live_execution_authority: false, secrets_authority: false}
    proof_contract: {context_proof_required: true, template_action_proof_required: true, receipt_required: true}
    ui: {label: ION Handoff, drawer_visible: true, user_chore: false}
  - skill_id: template-curation
    display_name: Template Curation
    class: specialist
    purpose: Govern templates and skills.
    trigger_summary: Governance.
    preferred_model: gpt-5.5
    default_reasoning_effort: high
    activates_templates: [ION/07_templates/actions/TEMPLATE_DEVELOPMENT.md]
    template_bindings: []
    context_mount: {required_packages: [active_authority_package], route_deeper_packages: [route_depth_package]}
    allowed_authority: {read_context: true, queue_work: false, write_files: scoped_governance_surfaces_only, production_authority: false, live_execution_authority: false, secrets_authority: false}
    proof_contract: {context_proof_required: true, template_action_proof_required: true, receipt_required: true}
    ui: {label: Templates, drawer_visible: true, user_chore: false}
""",
    }
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.strip() + "\n", encoding="utf-8")


def test_chat_engine_registry_loads_native_lenses(tmp_path: Path):
    _seed_root(tmp_path)

    registry = load_native_lens_registry(tmp_path)

    assert registry["ok"] is True
    assert registry["lens_count"] == 5
    assert registry["production_authority"] is False


def test_chat_engine_normal_answer_uses_gpt55_and_capsule_context(tmp_path: Path):
    _seed_root(tmp_path)

    turn = build_codex_chat_engine_turn(
        tmp_path,
        lane_id="codex_general",
        message="How should we proceed with the chat engine?",
        execution_mode="respond_only",
    )

    assert turn["ok"] is True
    assert turn["response_mode"] == "answer"
    assert turn["selected_skill"]["skill_id"] == "codex-chat-answer"
    assert turn["model_move"]["selected_model"] == "gpt-5.5"
    assert turn["response_contract"]["quality_target"] == "chatgpt_browser_level_or_better"
    assert "ION/05_context/current/codex_solo/CAPSULE.md" in turn["context_mount"]["context_refs"]
    assert any(lens["lens_id"] == "persona" for lens in turn["native_lenses"])
    assert turn["assistant_work_route"]["candidate_only"] is True
    assert turn["assistant_work_route"]["ok"] is False


def test_chat_engine_queue_work_selects_mason_codex_and_existing_queue_strategy(tmp_path: Path):
    _seed_root(tmp_path)

    turn = build_codex_chat_engine_turn(
        tmp_path,
        lane_id="codex_general",
        message="Implement the chat engine response contract.",
        execution_mode="queue_for_codex",
    )

    assert turn["response_mode"] == "queue_work"
    assert turn["selected_skill"]["skill_id"] == "codex-solo-work"
    assert turn["model_move"]["selected_model"] == "gpt-5.3-codex"
    assert turn["carrier_strategy"]["mode"] == "existing_codex_work_queue"
    assert any(lens["lens_id"] == "mason_codex" for lens in turn["native_lenses"])
    assert turn["authority"]["state_acceptance_granted"] is False
    assert turn["assistant_work_route"]["policy"] == "chat_continues_without_candidate_assistant_work_route"


def test_chat_engine_carrier_objective_is_user_facing_and_bounded(tmp_path: Path):
    _seed_root(tmp_path)
    turn = build_codex_chat_engine_turn(
        tmp_path,
        lane_id="codex_general",
        message="Explain how Capsule helps the chat.",
        execution_mode="respond_only",
    )

    objective = build_codex_chat_carrier_objective(turn, "Explain how Capsule helps the chat.")

    assert "Codex chat response packet." in objective
    assert "Answer conversationally and directly." in objective
    assert "Do not expose raw hidden reasoning." in objective
    assert "Candidate Assistant Work route:" in objective
    assert "Operator message:" in objective
    assert "ION/05_context/current/codex_solo/CAPSULE.md" in objective


def test_response_mode_recovery_precedes_queue_intent():
    assert classify_response_mode(
        lane_id="codex_general",
        message="Recover from wrong root drift and fix the route",
        execution_mode="queue_for_codex",
    ) == "recover"
