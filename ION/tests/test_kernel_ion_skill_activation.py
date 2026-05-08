from pathlib import Path

from kernel.ion_skill_activation import (
    SKILL_PROTOCOL_PATH,
    SKILL_REGISTRY_PATH,
    build_ion_skill_activation,
    build_ion_skill_surface,
    load_ion_skill_registry,
)


def _seed_skill_root(root: Path) -> None:
    (root / SKILL_PROTOCOL_PATH).parent.mkdir(parents=True, exist_ok=True)
    (root / SKILL_PROTOCOL_PATH).write_text("# Skill activation protocol\n", encoding="utf-8")
    path = root / SKILL_REGISTRY_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """
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
    trigger_summary: respond only
    preferred_model: gpt-5.5
    default_reasoning_effort: medium
    activates_templates: [ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md]
    template_bindings: []
    context_mount: {required_packages: [minimum_working_capsule], route_deeper_packages: [route_depth_package]}
    allowed_authority: {read_context: true, queue_work: false, write_files: false, production_authority: false, live_execution_authority: false, secrets_authority: false}
    proof_contract: {context_proof_required: true, template_action_proof_required: false, receipt_required: false}
    ui: {label: Chat, drawer_visible: true, user_chore: false}
  - skill_id: codex-solo-work
    display_name: Codex Work
    class: user_visible
    purpose: Queue bounded Codex work.
    trigger_summary: run task
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
    trigger_summary: recovery
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
    purpose: Route through full ION.
    trigger_summary: ion lane
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
    trigger_summary: governance
    preferred_model: gpt-5.5
    default_reasoning_effort: high
    activates_templates: [ION/07_templates/actions/TEMPLATE_DEVELOPMENT.md]
    template_bindings: []
    context_mount: {required_packages: [active_authority_package], route_deeper_packages: [route_depth_package]}
    allowed_authority: {read_context: true, queue_work: false, write_files: scoped_governance_surfaces_only, production_authority: false, live_execution_authority: false, secrets_authority: false}
    proof_contract: {context_proof_required: true, template_action_proof_required: true, receipt_required: true}
    ui: {label: Templates, drawer_visible: true, user_chore: false}
""".strip()
        + "\n",
        encoding="utf-8",
    )


def test_skill_registry_loads_without_authority_grant(tmp_path: Path):
    _seed_skill_root(tmp_path)

    registry = load_ion_skill_registry(tmp_path)

    assert registry["ok"] is True
    assert registry["skill_count"] == 5
    assert registry["production_authority"] is False
    assert registry["live_execution_authority"] is False


def test_skill_activation_selects_queue_and_keeps_templates_as_gate(tmp_path: Path):
    _seed_skill_root(tmp_path)

    activation = build_ion_skill_activation(
        tmp_path,
        lane_id="codex_general",
        objective="Implement the fix.",
        execution_mode="queue_for_codex",
    )

    assert activation["ok"] is True
    assert activation["skill_id"] == "codex-solo-work"
    assert activation["selection_reason"] == "codex_queue_execution_mode"
    assert activation["state_acceptance_granted"] is False
    assert activation["proof_contract"]["template_action_proof_required"] is True
    assert activation["authority"]["production_authority"] is False


def test_skill_activation_selects_recovery_before_template_language(tmp_path: Path):
    _seed_skill_root(tmp_path)

    activation = build_ion_skill_activation(
        tmp_path,
        lane_id="codex_general",
        objective="Recover from UI drift in the skill drawer.",
        execution_mode="respond_only",
    )

    assert activation["skill_id"] == "codex-recovery"
    assert activation["selection_reason"] == "recovery_trigger_detected"


def test_skill_surface_exposes_current_activation(tmp_path: Path):
    _seed_skill_root(tmp_path)

    surface = build_ion_skill_surface(tmp_path, objective="Explain templates and skills.")

    assert surface["ok"] is True
    assert surface["current_activation"]["skill_id"] == "template-curation"
    assert surface["policy"] == "skills_activate_templates_templates_gate_proof"
