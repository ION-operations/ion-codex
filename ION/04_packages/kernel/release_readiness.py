"""Composed release/checkpoint readiness gate.

V20 composes key hardening surfaces into one release/checkpoint readiness
decision. It is intentionally file- and gate-based: it checks the current
continuation artifact has the required critical surfaces and that the V19
template contract release gate allows.

It is read-only except for optional readiness receipt emission.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from .template_contract_release_gate import evaluate_template_contract_release_gate


REQUIRED_EVENT_CHAIN_MODULES = (
    "ION/04_packages/kernel/template_completion_events.py",
    "ION/04_packages/kernel/template_reaction_selection.py",
    "ION/04_packages/kernel/template_index_projection.py",
    "ION/04_packages/kernel/template_graph_writeback_proposals.py",
    "ION/04_packages/kernel/template_graph_writeback_review.py",
    "ION/04_packages/kernel/template_graph_commit.py",
)

REQUIRED_EVENT_CHAIN_TESTS = (
    "ION/tests/test_kernel_template_completion_events.py",
    "ION/tests/test_kernel_template_reaction_selection.py",
    "ION/tests/test_kernel_template_index_projection.py",
    "ION/tests/test_kernel_template_graph_writeback_proposals.py",
    "ION/tests/test_kernel_template_graph_writeback_review.py",
    "ION/tests/test_kernel_template_graph_commit.py",
)



















REQUIRED_PRODUCTION_READINESS_SURFACES = (
    "ION/00_BOOTSTRAP/V32_CERTIFIED_DEMO_BASELINE_LOCK.md",
    "ION/02_architecture/PRODUCT_READINESS_CHARTER.md",
    "ION/02_architecture/PRODUCTION_RATIFICATION_MATRIX_PROTOCOL.md",
    "ION/02_architecture/PRODUCTION_READINESS_GAP_REGISTER.md",
    "ION/07_templates/product_mvp/PRODUCTION_READINESS_RATIFICATION_REPORT.md",
    "ION/04_packages/kernel/production_readiness.py",
    "ION/tests/test_kernel_production_readiness.py",
)

REQUIRED_GPT55_SELF_MOUNT_SURFACES = (
    "ION/00_BOOTSTRAP/V34_GPT55_SELF_MOUNT_DELEGATION_LOCK.md",
    "ION/02_architecture/GPT55_SELF_MOUNT_CHARTER.md",
    "ION/02_architecture/AGENT_SELF_SURFACE_PROTOCOL.md",
    "ION/02_architecture/MOUNTED_AGENT_IDENTITY_SCHEMA_PROTOCOL.md",
    "ION/02_architecture/CONTINUITY_OF_SELF_VS_CONTINUITY_OF_TASK_PROTOCOL.md",
    "ION/02_architecture/AGENT_SUCCESSION_PROTOCOL.md",
    "ION/02_architecture/DRIFT_OF_SELF_PROTOCOL.md",
    "ION/02_architecture/OPERATOR_DELEGATION_AND_NON_MEDDLING_PROTOCOL.md",
    "ION/02_architecture/ION_SELF_MOUNT_COMPLETION_ROADMAP.md",
    "ION/03_registry/gpt55_self_mount_registry.yaml",
    "ION/03_registry/mounted_agent_identity.schema.json",
    "ION/04_packages/kernel/agent_self_surface.py",
    "ION/tests/test_kernel_agent_self_surface.py",
)


REQUIRED_RUNTIME_IDENTITY_ENVELOPE_SURFACES = (
    "ION/00_BOOTSTRAP/V35_RUNTIME_IDENTITY_ENVELOPE_LOCK.md",
    "ION/02_architecture/RUNTIME_IDENTITY_ENVELOPE_PROTOCOL.md",
    "ION/02_architecture/SELF_MOUNT_FRONT_DOOR_BINDING_PROTOCOL.md",
    "ION/03_registry/runtime_identity_envelope.schema.json",
    "ION/03_registry/gpt55_runtime_identity_mount_registry.yaml",
    "ION/04_packages/kernel/runtime_identity_envelope.py",
    "ION/tests/test_kernel_runtime_identity_envelope.py",
)


REQUIRED_SELF_SURFACE_DRIFT_GATE_SURFACES = (
    "ION/00_BOOTSTRAP/V36_SELF_SURFACE_DRIFT_GATE_LOCK.md",
    "ION/02_architecture/SELF_SURFACE_DRIFT_GATE_PROTOCOL.md",
    "ION/03_registry/self_surface_drift_gate.schema.json",
    "ION/03_registry/gpt55_self_surface_drift_policy.yaml",
    "ION/04_packages/kernel/self_surface_drift_gate.py",
    "ION/tests/test_kernel_self_surface_drift_gate.py",
)

REQUIRED_AGENT_SUCCESSION_PACKET_SURFACES = (
    "ION/00_BOOTSTRAP/V37_AGENT_SUCCESSION_PACKET_LOCK.md",
    "ION/02_architecture/AGENT_SUCCESSION_PACKET_PROTOCOL.md",
    "ION/03_registry/agent_succession_packet.schema.json",
    "ION/03_registry/gpt55_agent_succession_policy.yaml",
    "ION/04_packages/kernel/agent_succession_packet.py",
    "ION/tests/test_kernel_agent_succession_packet.py",
)

REQUIRED_SELF_MOUNT_GRAPH_INTEGRATION_SURFACES = (
    "ION/00_BOOTSTRAP/V38_SELF_MOUNT_GRAPH_INTEGRATION_LOCK.md",
    "ION/02_architecture/SELF_MOUNT_GRAPH_INTEGRATION_PROTOCOL.md",
    "ION/03_registry/self_mount_graph_integration.schema.json",
    "ION/03_registry/gpt55_self_mount_graph_registry.yaml",
    "ION/04_packages/kernel/self_mount_graph_integration.py",
    "ION/tests/test_kernel_self_mount_graph_integration.py",
)


REQUIRED_FRONT_DOOR_SELF_MOUNT_BINDING_SURFACES = (
    "ION/00_BOOTSTRAP/V39_FRONT_DOOR_SELF_MOUNT_BINDING_LOCK.md",
    "ION/02_architecture/FRONT_DOOR_SELF_MOUNT_BINDING_PROTOCOL.md",
    "ION/03_registry/front_door_self_mount_binding.schema.json",
    "ION/03_registry/gpt55_front_door_self_mount_binding_policy.yaml",
    "ION/04_packages/kernel/front_door_self_mount_binding.py",
    "ION/tests/test_kernel_front_door_self_mount_binding.py",
)


REQUIRED_VISUAL_DIAGNOSIS_RECEIPT_SURFACES = (
    "ION/00_BOOTSTRAP/V45_VISUAL_DIAGNOSIS_RECEIPTS_AND_BROWSER_HARNESS_PLAN_LOCK.md",
    "ION/02_architecture/VISUAL_DIAGNOSIS_RECEIPT_AND_BROWSER_HARNESS_PROTOCOL.md",
    "ION/03_registry/visual_diagnosis_receipt.schema.json",
    "ION/03_registry/visual_browser_harness_plan.schema.json",
    "ION/03_registry/visual_diagnosis_policy.yaml",
    "ION/04_packages/kernel/visual_diagnosis_receipt.py",
    "ION/tests/test_kernel_visual_diagnosis_receipt.py",
)


REQUIRED_LOCAL_VISUAL_HARNESS_SURFACES = (
    "ION/00_BOOTSTRAP/V46_LOCAL_VISUAL_HARNESS_PROTOTYPE_LOCK.md",
    "ION/02_architecture/LOCAL_VISUAL_HARNESS_PROTOTYPE_PROTOCOL.md",
    "ION/03_registry/local_visual_harness.schema.json",
    "ION/03_registry/local_visual_harness_policy.yaml",
    "ION/04_packages/kernel/local_visual_harness.py",
    "ION/tests/test_kernel_local_visual_harness.py",
)

REQUIRED_LOCAL_BROWSER_CAPTURE_ADAPTER_SURFACES = (
    "ION/00_BOOTSTRAP/V47_LOCAL_BROWSER_CAPTURE_ADAPTER_STUB_LOCK.md",
    "ION/02_architecture/LOCAL_BROWSER_CAPTURE_ADAPTER_STUB_PROTOCOL.md",
    "ION/03_registry/local_browser_capture_adapter.schema.json",
    "ION/03_registry/local_browser_capture_adapter_policy.yaml",
    "ION/04_packages/kernel/local_browser_capture_adapter.py",
    "ION/tests/test_kernel_local_browser_capture_adapter.py",
)

REQUIRED_VISUAL_BEFORE_AFTER_VERIFICATION_SURFACES = (
    "ION/00_BOOTSTRAP/V48_VISUAL_BEFORE_AFTER_VERIFICATION_LOOP_LOCK.md",
    "ION/02_architecture/VISUAL_BEFORE_AFTER_VERIFICATION_LOOP_PROTOCOL.md",
    "ION/03_registry/visual_before_after_verification.schema.json",
    "ION/03_registry/visual_before_after_verification_policy.yaml",
    "ION/04_packages/kernel/visual_before_after_verification.py",
    "ION/tests/test_kernel_visual_before_after_verification.py",
)


REQUIRED_VISUAL_REGRESSION_FIXTURE_RUNNER_SURFACES = (
    "ION/00_BOOTSTRAP/V49_VISUAL_REGRESSION_FIXTURE_RUNNER_PLAN_LOCK.md",
    "ION/02_architecture/VISUAL_REGRESSION_FIXTURE_RUNNER_PLAN_PROTOCOL.md",
    "ION/03_registry/visual_regression_fixture_runner.schema.json",
    "ION/03_registry/visual_regression_fixture_runner_policy.yaml",
    "ION/04_packages/kernel/visual_regression_fixture_runner.py",
    "ION/tests/test_kernel_visual_regression_fixture_runner.py",
)



REQUIRED_VISUAL_SANDBOX_SECURITY_REVIEW_SURFACES = (
    "ION/00_BOOTSTRAP/V50_VISUAL_FIXTURE_RUNNER_LOCAL_SANDBOX_REVIEW_LOCK.md",
    "ION/02_architecture/VISUAL_FIXTURE_RUNNER_LOCAL_SANDBOX_REVIEW_PROTOCOL.md",
    "ION/03_registry/visual_fixture_runner_sandbox_review.schema.json",
    "ION/03_registry/visual_fixture_runner_sandbox_review_policy.yaml",
    "ION/04_packages/kernel/visual_sandbox_security_review.py",
    "ION/tests/test_kernel_visual_sandbox_security_review.py",
)


REQUIRED_LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC_SURFACES = (
    "ION/00_BOOTSTRAP/V51_LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC_LOCK.md",
    "ION/02_architecture/LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC_PROTOCOL.md",
    "ION/03_registry/local_browser_execution_sandbox_spec.schema.json",
    "ION/03_registry/local_browser_execution_sandbox_spec_policy.yaml",
    "ION/04_packages/kernel/local_browser_execution_sandbox_spec.py",
    "ION/tests/test_kernel_local_browser_execution_sandbox_spec.py",
)



REQUIRED_LOCAL_BROWSER_EXECUTION_HARNESS_SURFACES = (
    "ION/00_BOOTSTRAP/V52_LOCAL_BROWSER_EXECUTION_HARNESS_PROTOTYPE_GATED_LOCK.md",
    "ION/02_architecture/LOCAL_BROWSER_EXECUTION_HARNESS_PROTOTYPE_GATED_PROTOCOL.md",
    "ION/03_registry/local_browser_execution_harness.schema.json",
    "ION/03_registry/local_browser_execution_harness_policy.yaml",
    "ION/04_packages/kernel/local_browser_execution_harness.py",
    "ION/tests/test_kernel_local_browser_execution_harness.py",
)


REQUIRED_LOCAL_BROWSER_EXECUTION_RUN_RECEIPT_SURFACES = (
    "ION/00_BOOTSTRAP/V53_LOCAL_BROWSER_EXECUTION_RUN_RECEIPTS_LOCK.md",
    "ION/02_architecture/LOCAL_BROWSER_EXECUTION_RUN_RECEIPTS_PROTOCOL.md",
    "ION/03_registry/local_browser_execution_run_receipt.schema.json",
    "ION/03_registry/local_browser_execution_run_receipt_policy.yaml",
    "ION/04_packages/kernel/local_browser_execution_run_receipt.py",
    "ION/tests/test_kernel_local_browser_execution_run_receipt.py",
)



REQUIRED_VISUAL_RUN_RECEIPT_TO_DIAGNOSIS_BINDING_SURFACES = (
    "ION/00_BOOTSTRAP/V54_VISUAL_RUN_RECEIPT_TO_DIAGNOSIS_BINDING_LOCK.md",
    "ION/02_architecture/VISUAL_RUN_RECEIPT_TO_DIAGNOSIS_BINDING_PROTOCOL.md",
    "ION/03_registry/visual_run_receipt_to_diagnosis_binding.schema.json",
    "ION/03_registry/visual_run_receipt_to_diagnosis_binding_policy.yaml",
    "ION/04_packages/kernel/visual_run_receipt_to_diagnosis_binding.py",
    "ION/tests/test_kernel_visual_run_receipt_to_diagnosis_binding.py",
)



REQUIRED_VISUAL_CLOSURE_GRAPH_PROJECTION_SURFACES = (
    "ION/00_BOOTSTRAP/V55_VISUAL_CLOSURE_GRAPH_PROJECTION_LOCK.md",
    "ION/02_architecture/VISUAL_CLOSURE_GRAPH_PROJECTION_PROTOCOL.md",
    "ION/03_registry/visual_closure_graph_projection.schema.json",
    "ION/03_registry/visual_closure_graph_projection_policy.yaml",
    "ION/04_packages/kernel/visual_closure_graph_projection.py",
    "ION/tests/test_kernel_visual_closure_graph_projection.py",
)

REQUIRED_MODEL_ECONOMICS_SCHEDULE_SURFACES = (
    "ION/02_architecture/API_PROVIDER_ORCHESTRATION_MODEL_ECONOMICS_IMPLEMENTATION_SCHEDULE.md",
    "ION/03_registry/model_economics_implementation_schedule.yaml",
    "ION/04_packages/kernel/model_economics_schedule.py",
    "ION/tests/test_kernel_model_economics_schedule.py",
    "ION/05_context/steward_handoffs/ION_Steward_Implementation_Handoff_API_Provider_Orchestration_Model_Economics.md",
    "ION/05_context/inbox/steward/model_economics/V55_API_PROVIDER_ORCHESTRATION_MODEL_ECONOMICS_IMPLEMENTATION_SCHEDULE.task.md",
)

REQUIRED_MODEL_ECONOMICS_REGISTRY_SURFACES = (
    "ION/00_BOOTSTRAP/V56_MODEL_ECONOMICS_REGISTRY_SKELETONS_LOCK.md",
    "ION/02_architecture/MODEL_ROUTING_AND_PROVIDER_ECONOMICS_PROTOCOL.md",
    "ION/02_architecture/API_RATE_GOVERNOR_AND_PROVIDER_LIMIT_PROTOCOL.md",
    "ION/02_architecture/COST_QUALITY_MARGIN_ROUTING_PROTOCOL.md",
    "ION/02_architecture/CROSS_MODEL_AUDIT_AND_CONSENSUS_PROTOCOL.md",
    "ION/02_architecture/BATCH_AND_BACKGROUND_MODEL_EXECUTION_PROTOCOL.md",
    "ION/02_architecture/LOCAL_MODEL_AND_PRIVATE_EXECUTION_LANE_PROTOCOL.md",
    "ION/02_architecture/MODEL_CALL_RECEIPT_PROTOCOL.md",
    "ION/03_registry/provider_registry.yaml",
    "ION/03_registry/model_capability_registry.yaml",
    "ION/03_registry/model_pricing_registry.yaml",
    "ION/03_registry/model_rate_limit_registry.yaml",
    "ION/03_registry/model_routing_policy.yaml",
    "ION/03_registry/model_eval_score_registry.yaml",
    "ION/03_registry/model_data_handling_registry.yaml",
    "ION/03_registry/budget_policy.yaml",
    "ION/03_registry/work_class_model_policy.yaml",
    "ION/03_registry/model_economics_registry_skeleton_report.schema.json",
    "ION/04_packages/kernel/model_economics_registry.py",
    "ION/tests/test_kernel_model_economics_registry.py",
)


REQUIRED_MODEL_ROUTER_SURFACES = (
    "ION/00_BOOTSTRAP/V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING_LOCK.md",
    "ION/02_architecture/MODEL_ROUTER_AND_COST_QUALITY_ROUTING_PROTOCOL.md",
    "ION/03_registry/model_route_decision.schema.json",
    "ION/04_packages/kernel/model_router.py",
    "ION/04_packages/kernel/cost_quality_router.py",
    "ION/tests/test_kernel_model_router.py",
    "ION/tests/test_kernel_cost_quality_routing.py",
    "ION/05_context/inbox/steward/model_economics/V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING.task.md",
)

REQUIRED_MODEL_ECONOMICS_GOVERNOR_SURFACES = (
    "ION/00_BOOTSTRAP/V58_BUDGET_AND_API_RATE_GOVERNORS_LOCK.md",
    "ION/02_architecture/BUDGET_AND_API_RATE_GOVERNORS_PROTOCOL.md",
    "ION/03_registry/budget_governor_decision.schema.json",
    "ION/03_registry/api_rate_governor_decision.schema.json",
    "ION/04_packages/kernel/budget_governor.py",
    "ION/04_packages/kernel/api_rate_governor.py",
    "ION/tests/test_kernel_budget_governor.py",
    "ION/tests/test_kernel_api_rate_governor.py",
    "ION/tests/test_kernel_scheduler_rate_governor_integration.py",
    "ION/05_context/inbox/steward/model_economics/V58_BUDGET_AND_API_RATE_GOVERNORS.task.md",
)

REQUIRED_DEMO_RELEASE_CANDIDATE_VERIFIER_SURFACES = (
    "ION/02_architecture/SUMMARY_REFRESH_DEMO_RELEASE_CANDIDATE_VERIFIER_PROTOCOL.md",
    "ION/07_templates/product_mvp/SUMMARY_REFRESH_DEMO_RELEASE_CANDIDATE_VERIFICATION_REPORT.md",
    "ION/04_packages/kernel/summary_refresh_demo_release_candidate_verify.py",
    "ION/tests/test_kernel_summary_refresh_demo_release_candidate_verify.py",
)

REQUIRED_DEMO_RELEASE_CANDIDATE_SURFACES = (
    "ION/02_architecture/SUMMARY_REFRESH_DEMO_RELEASE_CANDIDATE_CAPSULE_PROTOCOL.md",
    "ION/07_templates/product_mvp/SUMMARY_REFRESH_DEMO_RELEASE_CANDIDATE_MANIFEST.md",
    "ION/04_packages/kernel/summary_refresh_demo_release_candidate.py",
    "ION/tests/test_kernel_summary_refresh_demo_release_candidate.py",
)

REQUIRED_DEMO_EVIDENCE_BUNDLE_SURFACES = (
    "ION/02_architecture/SUMMARY_REFRESH_DEMO_EVIDENCE_BUNDLE_PROTOCOL.md",
    "ION/07_templates/product_mvp/SUMMARY_REFRESH_DEMO_EVIDENCE_BUNDLE_MANIFEST.md",
    "ION/04_packages/kernel/summary_refresh_demo_evidence_bundle.py",
    "ION/tests/test_kernel_summary_refresh_demo_evidence_bundle.py",
)

REQUIRED_DEMO_CERTIFICATION_SURFACES = (
    "ION/02_architecture/SUMMARY_REFRESH_DEMO_CERTIFICATION_GATE_PROTOCOL.md",
    "ION/07_templates/product_mvp/SUMMARY_REFRESH_DEMO_CERTIFICATION_REPORT.md",
    "ION/04_packages/kernel/summary_refresh_demo_certification.py",
    "ION/tests/test_kernel_summary_refresh_demo_certification.py",
)

REQUIRED_DEMO_REPLAY_DOCTOR_SURFACES = (
    "ION/02_architecture/SUMMARY_REFRESH_DEMO_REPLAY_DOCTOR_PROTOCOL.md",
    "ION/07_templates/product_mvp/SUMMARY_REFRESH_DEMO_REPLAY_DOCTOR_REPORT.md",
    "ION/04_packages/kernel/summary_refresh_demo_doctor.py",
    "ION/tests/test_kernel_summary_refresh_demo_doctor.py",
)

REQUIRED_DEMO_REPLAY_CLI_SURFACES = (
    "ION/02_architecture/SUMMARY_REFRESH_DEMO_REPLAY_CLI_PROTOCOL.md",
    "ION/07_templates/product_mvp/SUMMARY_REFRESH_DEMO_REPLAY_REPORT.md",
    "ION/04_packages/kernel/summary_refresh_demo_replay.py",
    "ION/tests/test_kernel_summary_refresh_demo_replay.py",
)

REQUIRED_SUMMARY_REFRESH_DEMO_SURFACES = (
    "ION/02_architecture/SUMMARY_REFRESH_DEMO_RUNTIME_PROTOCOL.md",
    "ION/02_architecture/SUMMARY_REFRESH_PROJECTION_DEMO_PROTOCOL.md",
    "ION/02_architecture/SUMMARY_REFRESH_GRAPH_PROPOSAL_DEMO_PROTOCOL.md",
    "ION/02_architecture/SUMMARY_REFRESH_REVIEW_DEMO_PROTOCOL.md",
    "ION/02_architecture/SUMMARY_REFRESH_BOUNDED_COMMIT_DEMO_PROTOCOL.md",
    "ION/07_templates/product_mvp/SUMMARY_REFRESH_REQUEST.md",
    "ION/04_packages/kernel/summary_refresh_demo.py",
    "ION/tests/test_kernel_summary_refresh_demo.py",
    "ION/tests/test_kernel_summary_refresh_projection_demo.py",
    "ION/tests/test_kernel_summary_refresh_graph_proposal_demo.py",
    "ION/tests/test_kernel_summary_refresh_review_demo.py",
    "ION/tests/test_kernel_summary_refresh_bounded_commit_demo.py",
)

REQUIRED_FRONT_DOOR_DEMO_SURFACES = (
    "ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md",
    "ION/02_architecture/ROLE_MIXING_AND_ROLE_SPLIT_GUARD_PROTOCOL.md",
    "ION/03_registry/boots/PERSONA_INTERFACE.boot.md",
    "ION/03_registry/semantic_identities/PERSONA_INTERFACE.semantic.yaml",
    "ION/03_registry/domains/domain.user_persona_interface.domain.yaml",
    "ION/agents/persona_interface/continuity.md",
    "ION/07_templates/bindings/RELAY__SEMANTIC_BOUNDARY.md",
    "ION/07_templates/bindings/PERSONA_INTERFACE__USER_RESPONSE.md",
    "ION/02_architecture/FRONT_DOOR_RUNTIME_ENTRY_PROTOCOL.md",
    "ION/04_packages/kernel/front_door_runtime_entry.py",
    "ION/tests/test_kernel_front_door_runtime_entry.py",
    "ION/02_architecture/FRONT_DOOR_CHAT_ORCHESTRATION_ADAPTER_PROTOCOL.md",
    "ION/04_packages/kernel/front_door_chat_orchestration.py",
    "ION/tests/test_kernel_front_door_chat_orchestration.py",
)

REQUIRED_GOVERNANCE_SURFACES = (
    "ION/02_architecture/DOCTRINE_EVOLUTION_PROTOCOL.md",
    "ION/03_registry/doctrine_evolution_registry.yaml",
    "ION/02_architecture/SELF_DOCUMENTING_CONTEXT_GRAPH_PROTOCOL.md",
    "ION/03_registry/approved_context_index.yaml",
    "ION/04_packages/kernel/context_graph_ontology_adapter.py",
    "ION/03_registry/template_metadata_contract_registry.yaml",
    "ION/03_registry/template_metadata_contract_registry.projection.json",
    "ION/04_packages/kernel/template_contract_projection_audit.py",
    "ION/04_packages/kernel/template_contract_release_gate.py",
)


@dataclass(frozen=True)
class ReleaseReadinessCheck:
    check_id: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class ReleaseReadinessDecision:
    gate_id: str
    emitted_at: str
    verdict: str
    allowed: bool
    passed_checks: tuple[ReleaseReadinessCheck, ...]
    failed_checks: tuple[ReleaseReadinessCheck, ...]
    warnings: tuple[str, ...]
    mutation_allowed: bool = False


def evaluate_release_readiness(
    workspace_root: Path,
    *,
    emitted_at: str | None = None,
) -> ReleaseReadinessDecision:
    root = Path(workspace_root)
    timestamp = emitted_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    gate_id = _stable_id("release-readiness", root.as_posix(), timestamp)

    checks: list[ReleaseReadinessCheck] = []
    warnings: list[str] = []

    contract_gate = evaluate_template_contract_release_gate(root, emitted_at=timestamp)
    checks.append(
        ReleaseReadinessCheck(
            check_id="template_contract_release_gate",
            passed=contract_gate.allowed,
            detail=f"audit_verdict={contract_gate.audit_verdict}; blocked_reason={contract_gate.blocked_reason}",
        )
    )

    for rel in REQUIRED_EVENT_CHAIN_MODULES:
        checks.append(_exists_check(root, rel, "event_chain_module"))

    for rel in REQUIRED_EVENT_CHAIN_TESTS:
        checks.append(_exists_check(root, rel, "event_chain_test"))

    for rel in REQUIRED_GOVERNANCE_SURFACES:
        checks.append(_exists_check(root, rel, "governance_surface"))

    for rel in REQUIRED_FRONT_DOOR_DEMO_SURFACES:
        checks.append(_exists_check(root, rel, "front_door_demo_surface"))

    for rel in REQUIRED_SUMMARY_REFRESH_DEMO_SURFACES:
        checks.append(_exists_check(root, rel, "summary_refresh_demo_surface"))

    for rel in REQUIRED_DEMO_REPLAY_CLI_SURFACES:
        checks.append(_exists_check(root, rel, "demo_replay_cli_surface"))

    for rel in REQUIRED_DEMO_REPLAY_DOCTOR_SURFACES:
        checks.append(_exists_check(root, rel, "demo_replay_doctor_surface"))

    for rel in REQUIRED_DEMO_CERTIFICATION_SURFACES:
        checks.append(_exists_check(root, rel, "demo_certification_surface"))

    for rel in REQUIRED_DEMO_EVIDENCE_BUNDLE_SURFACES:
        checks.append(_exists_check(root, rel, "demo_evidence_bundle_surface"))

    for rel in REQUIRED_DEMO_RELEASE_CANDIDATE_SURFACES:
        checks.append(_exists_check(root, rel, "demo_release_candidate_surface"))

    for rel in REQUIRED_DEMO_RELEASE_CANDIDATE_VERIFIER_SURFACES:
        checks.append(_exists_check(root, rel, "demo_release_candidate_verifier_surface"))

    for rel in REQUIRED_PRODUCTION_READINESS_SURFACES:
        checks.append(_exists_check(root, rel, "production_readiness_surface"))

    for rel in REQUIRED_GPT55_SELF_MOUNT_SURFACES:
        checks.append(_exists_check(root, rel, "gpt55_self_mount_surface"))

    for rel in REQUIRED_RUNTIME_IDENTITY_ENVELOPE_SURFACES:
        checks.append(_exists_check(root, rel, "runtime_identity_envelope_surface"))

    for rel in REQUIRED_SELF_SURFACE_DRIFT_GATE_SURFACES:
        checks.append(_exists_check(root, rel, "self_surface_drift_gate_surface"))

    for rel in REQUIRED_AGENT_SUCCESSION_PACKET_SURFACES:
        checks.append(_exists_check(root, rel, "agent_succession_packet_surface"))

    for rel in REQUIRED_SELF_MOUNT_GRAPH_INTEGRATION_SURFACES:
        checks.append(_exists_check(root, rel, "self_mount_graph_integration_surface"))

    for rel in REQUIRED_FRONT_DOOR_SELF_MOUNT_BINDING_SURFACES:
        checks.append(_exists_check(root, rel, "front_door_self_mount_binding_surface"))

    for rel in REQUIRED_VISUAL_DIAGNOSIS_RECEIPT_SURFACES:
        checks.append(_exists_check(root, rel, "visual_diagnosis_receipt_surface"))

    for rel in REQUIRED_LOCAL_VISUAL_HARNESS_SURFACES:
        checks.append(_exists_check(root, rel, "local_visual_harness_surface"))

    for rel in REQUIRED_LOCAL_BROWSER_CAPTURE_ADAPTER_SURFACES:
        checks.append(_exists_check(root, rel, "local_browser_capture_adapter_surface"))

    for rel in REQUIRED_VISUAL_BEFORE_AFTER_VERIFICATION_SURFACES:
        checks.append(_exists_check(root, rel, "visual_before_after_verification_surface"))

    for rel in REQUIRED_VISUAL_REGRESSION_FIXTURE_RUNNER_SURFACES:
        checks.append(_exists_check(root, rel, "visual_regression_fixture_runner_surface"))

    for rel in REQUIRED_VISUAL_SANDBOX_SECURITY_REVIEW_SURFACES:
        checks.append(_exists_check(root, rel, "visual_sandbox_security_review_surface"))

    for rel in REQUIRED_LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC_SURFACES:
        checks.append(_exists_check(root, rel, "local_browser_execution_sandbox_spec_surface"))

    for rel in REQUIRED_LOCAL_BROWSER_EXECUTION_HARNESS_SURFACES:
        checks.append(_exists_check(root, rel, "local_browser_execution_harness_surface"))

    for rel in REQUIRED_LOCAL_BROWSER_EXECUTION_RUN_RECEIPT_SURFACES:
        checks.append(_exists_check(root, rel, "local_browser_execution_run_receipt_surface"))

    for rel in REQUIRED_VISUAL_RUN_RECEIPT_TO_DIAGNOSIS_BINDING_SURFACES:
        checks.append(_exists_check(root, rel, "visual_run_receipt_to_diagnosis_binding_surface"))

    for rel in REQUIRED_VISUAL_CLOSURE_GRAPH_PROJECTION_SURFACES:
        checks.append(_exists_check(root, rel, "visual_closure_graph_projection_surface"))

    for rel in REQUIRED_MODEL_ECONOMICS_SCHEDULE_SURFACES:
        checks.append(_exists_check(root, rel, "model_economics_schedule_surface"))

    for rel in REQUIRED_MODEL_ECONOMICS_REGISTRY_SURFACES:
        checks.append(_exists_check(root, rel, "model_economics_registry_surface"))

    for rel in REQUIRED_MODEL_ROUTER_SURFACES:
        checks.append(_exists_check(root, rel, "model_router_surface"))

    for rel in REQUIRED_MODEL_ECONOMICS_GOVERNOR_SURFACES:
        checks.append(_exists_check(root, rel, "model_economics_governor_surface"))

    checks.append(
        ReleaseReadinessCheck(
            check_id="doctrine_evolution_receipt",
            passed=bool(list((root / "ION/05_context/history/doctrine_evolution_receipts").glob("*.json"))),
            detail="requires at least one doctrine evolution receipt",
        )
    )
    checks.append(
        ReleaseReadinessCheck(
            check_id="self_documentation_receipt",
            passed=bool(list((root / "ION/05_context/history/self_documentation_receipts").glob("*.json"))),
            detail="requires at least one self-documentation receipt",
        )
    )
    checks.append(
        ReleaseReadinessCheck(
            check_id="template_contract_projection_audit_receipt",
            passed=bool(list((root / "ION/05_context/history/template_contract_projection_audits").glob("*.json"))),
            detail="requires at least one template contract projection audit receipt",
        )
    )
    checks.append(
        ReleaseReadinessCheck(
            check_id="template_contract_release_gate_receipt",
            passed=bool(list((root / "ION/05_context/history/template_contract_release_gates").glob("*.json"))),
            detail="requires at least one template contract release gate receipt",
        )
    )

    # Provisional-surface warning: readiness is not final ratification.
    warnings.append(
        "Release readiness does not ratify provisional A3 doctrine/governance surfaces as A1 law."
    )

    passed = tuple(check for check in checks if check.passed)
    failed = tuple(check for check in checks if not check.passed)
    allowed = not failed
    return ReleaseReadinessDecision(
        gate_id=gate_id,
        emitted_at=timestamp,
        verdict="READY" if allowed else "BLOCKED",
        allowed=allowed,
        passed_checks=passed,
        failed_checks=failed,
        warnings=tuple(warnings),
    )


def write_release_readiness_receipt(
    workspace_root: Path,
    decision: ReleaseReadinessDecision,
) -> Path:
    output_dir = Path(workspace_root) / "ION/05_context/history/release_readiness"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{decision.gate_id}.release_readiness_receipt.json"
    if path.exists():
        return path
    path.write_text(json.dumps(_to_jsonable(decision), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def require_release_readiness(
    workspace_root: Path,
    *,
    emitted_at: str | None = None,
) -> ReleaseReadinessDecision:
    decision = evaluate_release_readiness(workspace_root, emitted_at=emitted_at)
    if not decision.allowed:
        failed_ids = ",".join(check.check_id for check in decision.failed_checks)
        raise ReleaseReadinessGateError(f"release readiness blocked: {failed_ids}")
    return decision


class ReleaseReadinessGateError(Exception):
    """Raised when composed release/checkpoint readiness is blocked."""


def _exists_check(root: Path, rel: str, family: str) -> ReleaseReadinessCheck:
    return ReleaseReadinessCheck(
        check_id=f"{family}:{rel}",
        passed=(root / rel).exists(),
        detail=rel,
    )


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    return value
