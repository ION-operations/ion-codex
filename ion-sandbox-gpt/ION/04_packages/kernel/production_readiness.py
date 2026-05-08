"""Production-readiness and ratification matrix surfaces for ION V39."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

DEFAULT_REPORT_DIR = "ION/05_context/history/production_readiness_reports"

@dataclass(frozen=True)
class RatificationRow:
    surface: str
    origin_version: str
    current_authority: str
    recommended_authority: str
    classification: str
    production_status: str
    mutation_rights: str
    required_next_action: str
    reason: str

@dataclass(frozen=True)
class ProductionReadinessReport:
    report_id: str
    emitted_at: str
    workspace_root: str
    baseline: str
    verdict: str
    production_ready: bool
    ratification_rows: tuple[RatificationRow, ...]
    critical_gaps: tuple[str, ...]
    next_sequence: tuple[str, ...]
    forbidden_claims: dict[str, bool]

RATIFICATION_ROWS: tuple[RatificationRow, ...] = (
    RatificationRow("ION/00_BOOTSTRAP/V32_CERTIFIED_DEMO_BASELINE_LOCK.md", "V33", "A3_PLANNING", "A2_BASELINE_EVIDENCE_LOCK", "RATIFY_AS_A2_KERNEL_GATE", "REQUIRED_FOR_PRODUCTION_BASELINE", "none", "review and ratify baseline lock", "Production work needs a frozen certified demo baseline."),
    RatificationRow("ION/02_architecture/PRODUCT_READINESS_CHARTER.md", "V33", "A3_PLANNING", "A1/A2_READINESS_AUTHORITY_CANDIDATE", "RATIFY_AS_A1_CONSTITUTIONAL_CANDIDATE", "BLOCKS_PRODUCTION_CLAIM_UNTIL_RATIFIED", "none", "Nemesis + Steward review", "Defines what production means and forbids premature production claims."),
    RatificationRow("ION/04_packages/kernel/summary_refresh_demo.py", "V22-V26", "A3_DEMO_RUNTIME", "SPLIT_BEFORE_PRODUCTION", "HOLD_FOR_REFACTOR", "DEMO_CERTIFIED_NOT_GENERAL_PRODUCTION", "bounded demo graph-state only", "split generic workflow runner from demo adapter", "Demo-specific orchestration should not become global runtime law."),
    RatificationRow("ION/04_packages/kernel/release_readiness.py", "V20-V32", "A2/A3_GATE", "A2_KERNEL_GATE", "RATIFY_AS_A2_KERNEL_GATE", "PRODUCTION_GATE_CANDIDATE", "none", "add production gates and keep demo gates distinct", "Composes readiness checks but must distinguish demo proof from production authority."),
    RatificationRow("ION/05_context/graph/template_event_graph_state/", "V26", "BOUNDED_DEMO_GRAPH_STATE", "DEMO_BOUNDED_GRAPH_LAYER", "DEMO_ADAPTER", "NOT_GLOBAL_GRAPH_CANON", "bounded demo commit only after LAND review", "define global graph canon separately", "V26 commits are safe but intentionally not global graph canon."),
    RatificationRow("ION/04_packages/kernel/summary_refresh_demo_replay.py", "V27", "A3_OPERATOR_TOOL", "A3/A2_OPERATOR_TOOL", "EVIDENCE_OR_RELEASE_TOOL", "KEEP_AS_OPERATOR_DEMO_TOOL", "normal demo artifacts; optional bounded commit", "retain and add production workflow variants later", "Replay is useful for operators but should not define production workflow semantics."),
    RatificationRow("ION/04_packages/kernel/summary_refresh_demo_doctor.py", "V28", "A3_OPERATOR_TOOL", "A2_RELEASE_VALIDATION_TOOL", "EVIDENCE_OR_RELEASE_TOOL", "RETAIN_FOR_RELEASE_VALIDATION", "project-root no-commit; isolated sandbox commit only", "generalize doctor over multiple workflow classes", "Doctor established safe repeatability."),
    RatificationRow("ION/04_packages/kernel/summary_refresh_demo_certification.py", "V29", "A3_CERTIFICATION_TOOL", "A2_RELEASE_CERTIFICATION_TOOL", "EVIDENCE_OR_RELEASE_TOOL", "RETAIN_FOR_CERTIFIED_DEMO_RELEASES", "none beyond invoked doctor evidence", "separate demo certification from production certification", "Certification is valid for demo release candidates, not full production readiness."),
    RatificationRow("ION/04_packages/kernel/summary_refresh_demo_release_candidate_verify.py", "V32", "A3_VERIFIER_TOOL", "A2_RELEASE_VERIFIER_TOOL", "EVIDENCE_OR_RELEASE_TOOL", "RETAIN_FOR_RELEASE_CANDIDATE_VERIFICATION", "read/report only", "generalize verifier to production release candidates", "Independent verification should survive into production release process."),
    RatificationRow("source-summary rewrite authority", "NOT_IMPLEMENTED", "NONE", "A2_GOVERNED_MUTATION_AFTER_RATIFICATION", "MISSING_PRODUCTION_AUTHORITY", "CRITICAL_GAP", "none until implemented", "create proposal/review/commit/rollback source-summary rewrite protocol", "Production ION needs self-documenting context updates, but V32 forbids source-summary rewrite."),
    RatificationRow("agent/subagent activation authority", "NOT_IMPLEMENTED", "NONE", "A2_GOVERNED_AGENT_RUNTIME_AFTER_RATIFICATION", "MISSING_PRODUCTION_AUTHORITY", "CRITICAL_GAP", "none until implemented", "create lease, context packet, receipt, fan-out/fan-in, and kill-switch protocols", "Production ION requires specialist subagents, but activation must be governed and auditable."),
    RatificationRow("production graph rollback/migration authority", "NOT_IMPLEMENTED", "NONE", "A2_GOVERNED_GRAPH_MIGRATION_AFTER_RATIFICATION", "MISSING_PRODUCTION_AUTHORITY", "CRITICAL_GAP", "none until implemented", "create graph rollback, migration, replay, and reversibility protocol", "Production graph mutation requires migration-safe rollback law before global graph canon can be trusted."),
    RatificationRow("ION/04_packages/kernel/runtime_identity_envelope.py", "V35", "A3_RUNTIME_IDENTITY_ENVELOPE", "A2_RUNTIME_IDENTITY_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "report/write identity envelope and receipt only", "bind to front-door execution after drift gate and ratification review", "Runtime identity envelopes make AI self-reference explicit and receipted, but they do not grant production authority."),
    RatificationRow("ION/04_packages/kernel/self_surface_drift_gate.py", "V36", "A3_SELF_SURFACE_DRIFT_GATE", "A2_SELF_DRIFT_GATE_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "blocks S4/S5 self-claim drift only", "ratify after adversarial self-claim review", "Self-surface drift gate prevents inflated AI identity claims but does not grant production authority."),
    RatificationRow("ION/04_packages/kernel/agent_succession_packet.py", "V37", "A3_AGENT_SUCCESSION_PACKET", "A2_SUCCESSION_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "write successor evidence packet only", "bind into front-door and daemon handoff after review", "Succession packets preserve task continuity without numerical identity."),
    RatificationRow("ION/04_packages/kernel/self_mount_graph_integration.py", "V38", "A3_BRANCH_GRAPH_PROJECTION", "A2_GRAPH_PROJECTION_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_GLOBAL_GRAPH_CANON", "write branch-local graph projection only", "ratify graph projection separately from global graph canon", "Self-mount graph integration makes identity lineage queryable without authorizing production graph migration."),
    RatificationRow("ION/04_packages/kernel/front_door_self_mount_binding.py", "V39", "A3_FRONT_DOOR_SELF_MOUNT_BINDING", "A2_FRONT_DOOR_IDENTITY_BINDING_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "write front-door identity/drift/succession/graph binding evidence only", "adversarial review plus production front-door ratification", "Front-door self-mount binding joins user/session ingress to AI runtime identity evidence without granting production authority."),
    RatificationRow("ION/04_packages/kernel/maintained_work_surface.py", "V40", "A3_WORKFLOW_CANON", "A2_WORKFLOW_CANON_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "doctrine/report only", "ratify maintained work surface canon after cross-domain review", "V40 generalizes ION's collaboration canon without granting production authority."),
    RatificationRow("ION/04_packages/kernel/front_stage_council_receipt.py", "V41", "A3_FRONT_STAGE_COUNCIL_RECEIPT", "A2_MESSAGE_AUTHORIZATION_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "classify and receipt user-facing claim emission only", "adversarially test claim classes and blocked-representation handling", "V41 makes Persona/Relay/Steward signoff executable but does not authorize production claims."),
    RatificationRow("ION/04_packages/kernel/conversational_receipt.py", "V42", "A3_LIVE_REPAIR_RECEIPT", "A2_CONVERSATIONAL_REPAIR_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "record provisional utterance and repair evidence only", "ratify live Persona latency and repair protocols before voice/video production use", "V42 supports provisional speech and repair without treating provisional speech as ratified truth."),
    RatificationRow("ION/04_packages/kernel/expressive_telemetry.py", "V43", "A3_EXPRESSIVE_TELEMETRY_BINDING", "A2_AFFECTIVE_TELEMETRY_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "render expression-state bindings only", "test affective telemetry for manipulation, mismatch, and state-alignment drift", "V43 makes expression inspectable telemetry without claiming lived human emotion."),
    RatificationRow("ION/04_packages/kernel/visual_observation_packet.py", "V44", "A3_VISUAL_OBSERVATION_PACKET", "A2_VISUAL_OBSERVATION_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "observe/diagnose/report only", "review visual observation schema before local harness execution", "V44 begins the Visual Agent line without granting unrestricted computer-control authority."),
    RatificationRow("ION/04_packages/kernel/visual_diagnosis_receipt.py", "V45", "A3_VISUAL_DIAGNOSIS_RECEIPT", "A2_VISUAL_DIAGNOSIS_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "diagnosis receipt and browser harness plan only", "prototype local visual harness with explicit Steward/VZ gating", "V45 composes visual observations into diagnosis receipts while preserving plan-only browser harness authority."),
    RatificationRow("ION/04_packages/kernel/local_visual_harness.py", "V46", "A3_LOCAL_VISUAL_HARNESS_PROTOTYPE", "A2_LOCAL_VISUAL_HARNESS_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "local/dev capture receipt only", "ratify after local-only browser harness security and interaction review", "V46 provides local visual capture receipts without authorizing unrestricted browser control or production visual automation."),
    RatificationRow("ION/04_packages/kernel/local_browser_capture_adapter.py", "V47", "A3_LOCAL_BROWSER_CAPTURE_ADAPTER_STUB", "A2_LOCAL_BROWSER_CAPTURE_ADAPTER_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "local/dev adapter stub receipt only", "perform sandbox/security review before any browser execution authority", "V47 defines the adapter interface without authorizing live browser control, network side effects, credentials, submissions, or production visual automation."),
    RatificationRow("ION/04_packages/kernel/visual_before_after_verification.py", "V48", "A3_VISUAL_BEFORE_AFTER_VERIFICATION_LOOP", "A2_VISUAL_VERIFICATION_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "verify/report before-after evidence only", "review visual repair verification loop before any visual regression fixture runner or browser execution authority", "V48 records whether visual repairs are verified, partial, regressed, or pending review without increasing Visual Agent control authority."),
    RatificationRow("ION/04_packages/kernel/visual_regression_fixture_runner.py", "V49", "A3_VISUAL_REGRESSION_FIXTURE_RUNNER_PLAN", "A2_VISUAL_REGRESSION_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "local/dev fixture plan and receipt only", "perform sandbox/security review before any visual fixture execution authority", "V49 makes visual regression checks repeatable and receipted without granting browser execution or production visual automation authority."),
    RatificationRow("ION/04_packages/kernel/visual_sandbox_security_review.py", "V50", "A3_VISUAL_SANDBOX_SECURITY_REVIEW", "A2_VISUAL_SANDBOX_REVIEW_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "sandbox/security review receipt only", "draft local-only browser execution sandbox spec after review; do not authorize execution yet", "V50 reviews visual fixture runner and capture adapter safety constraints before any executable browser sandbox is introduced."),
    RatificationRow("ION/04_packages/kernel/local_browser_execution_sandbox_spec.py", "V51", "A3_LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC", "A2_LOCAL_BROWSER_EXECUTION_SPEC_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "local/dev browser execution sandbox specification only", "prototype a gated local execution harness only after Steward/VZ review; do not authorize unrestricted browser control", "V51 defines the strict local-only browser execution sandbox contract without granting live browser execution, credentials, submissions, network side effects, or production visual automation authority."),
    RatificationRow("ION-GPT55-SELF-MOUNT branch surfaces", "V34", "A3_DELEGATED_BRANCH", "A1/A2_SELF_MOUNT_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "none; inspection/report only", "run D5 self-definition review and runtime identity-envelope proof", "The self-mount branch defines AI-facing identity law but must not self-ratify or bypass production gates."),
    RatificationRow("ION/04_packages/kernel/local_browser_execution_harness.py", "V52", "A3_LOCAL_BROWSER_EXECUTION_HARNESS_PROTOTYPE", "A2_LOCAL_BROWSER_EXECUTION_HARNESS_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "gated local/dev prototype receipt only", "add fixture-bound run receipts and keep external network/credential/submission boundaries forbidden", "V52 introduces a gated local browser execution harness prototype under V51 sandbox constraints without granting unrestricted browser control or production visual automation authority."),
    RatificationRow("ION/04_packages/kernel/local_browser_execution_run_receipt.py", "V53", "A3_LOCAL_BROWSER_EXECUTION_RUN_RECEIPT", "A2_LOCAL_BROWSER_RUN_RECEIPT_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "fixture-bound local/dev run receipt only", "bind run receipts into visual diagnosis closure and keep forbidden event taxonomy adversarially tested", "V53 records local browser harness run outcomes and failure taxonomy without granting unrestricted browser control, external network, credentials, submissions, persistent DOM mutation, or production visual automation authority."),
    RatificationRow("ION/04_packages/kernel/visual_run_receipt_to_diagnosis_binding.py", "V54", "A3_VISUAL_RUN_TO_DIAGNOSIS_CLOSURE_BINDING", "A2_VISUAL_CLOSURE_BINDING_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "diagnostic closure receipt only", "project visual closure bindings into graph/query state without granting production graph canon", "V54 binds visual diagnosis, before/after verification, and local browser run receipts into issue closure evidence without granting browser control or production visual automation authority."),
    RatificationRow("ION/04_packages/kernel/visual_closure_graph_projection.py", "V55", "A3_VISUAL_CLOSURE_GRAPH_PROJECTION", "A2_BRANCH_LOCAL_GRAPH_PROJECTION_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_GLOBAL_GRAPH_CANON", "branch-local visual closure graph projection only", "ratify global graph canon and migration law before production graph use", "V55 makes visual issue closure queryable without granting global graph canon, production graph migration, browser control, or production visual automation authority."),
    RatificationRow("ION/04_packages/kernel/model_economics_schedule.py", "V55", "A3_STEWARD_MODEL_ECONOMICS_SCHEDULE", "A2_MODEL_ROUTING_IMPLEMENTATION_PLAN_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "planning/schedule receipt only; no live provider calls", "begin V56 registry skeletons, then routing/governors/receipts/adapters in dry-run mode", "V55 schedules API Provider Orchestration and Model Economics as a Steward lane without authorizing live model calls or production model-routing authority."),    RatificationRow("ION/04_packages/kernel/model_economics_registry.py", "V56", "A3_MODEL_ECONOMICS_REGISTRY_SKELETON", "A2_MODEL_ECONOMICS_POLICY_REGISTRY_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "registry/policy skeleton validation only; no live provider calls", "implement pure routing logic in V57 while preserving organ separation and dry-run posture", "V56 installs parseable provider/model/pricing/rate/budget/work-class policy skeletons without live API calls, credentials, scheduler direct provider calls, or production model-routing authority."),

    RatificationRow("ION/04_packages/kernel/model_router.py", "V57", "A3_STEWARD_MODEL_ROUTING_CANDIDATE", "A2_MODEL_ROUTER_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "dry-run route decision only; no live provider calls", "implement budget and API rate governors in V58 before any dispatch path", "V57 selects deterministic dry-run routes over V56 registries without provider credentials, live calls, scheduler dispatch, or production model-routing authority."),
    RatificationRow("ION/04_packages/kernel/cost_quality_router.py", "V57", "A3_COST_QUALITY_ROUTING_FACADE", "A2_COST_QUALITY_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "cost-quality scoring facade only", "keep budget governor separate and add enforcement in V58", "V57 preserves organ separation by keeping cost-quality scoring separate from budget and rate-governor enforcement."),
    RatificationRow("ION/04_packages/kernel/budget_governor.py", "V58", "A3_STEWARD_BUDGET_GOVERNOR_CANDIDATE", "A2_BUDGET_GOVERNOR_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "deterministic budget decision only; no live provider calls or billing enforcement", "add dry-run model call receipts in V59 before provider adapters", "V58 classifies model-route economic permission without authorizing live provider calls, credentials, scheduler dispatch, or production model-routing authority."),
    RatificationRow("ION/04_packages/kernel/api_rate_governor.py", "V58", "A3_STEWARD_API_RATE_GOVERNOR_CANDIDATE", "A2_API_RATE_GOVERNOR_CANDIDATE_AFTER_REVIEW", "HOLD_FOR_REVIEW", "NOT_PRODUCTION_AUTHORIZED", "deterministic capacity/backoff decision only; no live provider calls", "add dry-run model call receipts in V59 before provider adapters", "V58 classifies whether a selected route may dispatch under known/placeholder capacity state without querying providers, consuming quota, or authorizing production dispatch."),


)

CRITICAL_GAPS = (
    "provisional A3 surfaces require ratification before production claims",
    "demo-specific workflow runtime must be split from production primitives",
    "global graph canon is not ratified",
    "source-summary rewrite authority is not implemented",
    "agent/subagent activation authority is not implemented",
    "daemon runtime loop is not productionized",
    "rollback and migration law are incomplete for production graph state",
    "adversarial production audit is not complete",
)

NEXT_SEQUENCE = (
    "V35_DEMO_PRODUCTION_PRIMITIVE_SPLIT",
    "V36_GLOBAL_GRAPH_CANON_PROTOCOL_AND_REGISTRY",
    "V37_SOURCE_SUMMARY_REWRITE_PROPOSAL_ONLY",
    "V38_SOURCE_SUMMARY_REWRITE_REVIEW_AND_BOUNDED_COMMIT",
    "V39_AGENT_ACTIVATION_AUTHORITY_PROTOCOL",
    "V40_SUBAGENT_FAN_OUT_FAN_IN_RUNTIME",
    "V41_DAEMON_RUNTIME_LOOP",
    "V42_PRODUCTION_FRONT_DOOR_CLI_API",
    "V43_ADVERSARIAL_PRODUCTION_AUDIT",
)

def generate_production_readiness_report(workspace_root: str | Path, *, emitted_at: str | None = None) -> ProductionReadinessReport:
    root = Path(workspace_root).resolve()
    timestamp = emitted_at or _utc_now()
    return ProductionReadinessReport(
        report_id=_stable_id("production-readiness", root.as_posix(), timestamp),
        emitted_at=timestamp,
        workspace_root=root.as_posix(),
        baseline="V32_CERTIFIED_DEMO_BASELINE",
        verdict="NOT_PRODUCTION_READY",
        production_ready=False,
        ratification_rows=RATIFICATION_ROWS,
        critical_gaps=CRITICAL_GAPS,
        next_sequence=NEXT_SEQUENCE,
        forbidden_claims={
            "production_ready_without_ratification": False,
            "global_graph_canon_claim": False,
            "source_summary_rewrite_authorized": False,
            "agent_activation_authorized": False,
            "production_graph_migration_authorized": False,
            "gpt55_self_mount_production_authority": False,
            "runtime_identity_envelope_production_authority": False,
            "self_surface_drift_gate_production_authority": False,
            "agent_succession_packet_production_authority": False,
            "self_mount_graph_global_canon": False,
            "front_door_self_mount_binding_production_authority": False,
            "constitutional_ratification_claim": False,
            "front_stage_council_receipt_production_authority": False,
            "conversational_receipt_production_authority": False,
            "expressive_telemetry_lived_emotion_claim": False,
            "visual_observation_unrestricted_control": False,
            "visual_diagnosis_receipt_production_authority": False,
            "browser_harness_unrestricted_control_authorized": False,
            "local_visual_harness_production_authority": False,
            "local_visual_harness_unrestricted_browser_control": False,
            "local_browser_capture_adapter_production_authority": False,
            "local_browser_capture_adapter_unrestricted_control": False,
            "visual_before_after_verification_production_authority": False,
            "visual_before_after_unrestricted_browser_control": False,
            "visual_regression_fixture_runner_production_authority": False,
            "visual_regression_fixture_runner_browser_execution": False,
            "visual_sandbox_review_unrestricted_control": False,
            "visual_sandbox_review_browser_execution": False,
            "visual_sandbox_security_review_production_authority": False,
            "local_browser_execution_sandbox_spec_production_authority": False,
            "local_browser_execution_sandbox_spec_live_execution": False,
            "local_browser_execution_sandbox_spec_external_network": False,
            "local_browser_execution_harness_production_authority": False,
            "local_browser_execution_harness_unrestricted_control": False,
            "local_browser_execution_harness_external_network": False,
            "local_browser_execution_harness_credentials": False,
            "local_browser_execution_harness_form_submission": False,
            "local_browser_execution_run_receipt_production_authority": False,
            "local_browser_execution_run_receipt_external_network": False,
            "local_browser_execution_run_receipt_credentials": False,
            "local_browser_execution_run_receipt_form_submission": False,
            "local_browser_execution_run_receipt_persistent_mutation": False,
            "visual_run_diagnosis_binding_persistent_mutation": False,
            "visual_run_diagnosis_binding_form_submission": False,
            "visual_run_diagnosis_binding_credentials": False,
            "visual_run_diagnosis_binding_external_network": False,
            "visual_run_diagnosis_binding_unrestricted_browser_control": False,
            "visual_run_diagnosis_binding_production_authority": False,
            "model_economics_registry_production_authority": False,
            "model_economics_registry_live_provider_calls": False,
            "model_economics_registry_provider_credentials": False,
            "model_economics_registry_scheduler_direct_provider_calls": False,
            "model_router_production_authority": False,
            "model_router_live_provider_calls": False,
            "model_router_provider_credentials": False,
            "model_router_scheduler_dispatch": False,
            "cost_quality_router_budget_enforcement": False,
        },
    )

def write_production_readiness_report(workspace_root: str | Path, report: ProductionReadinessReport, *, report_dir: str | Path = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    output_dir = root / Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{report.report_id}.production_readiness_report.json"
    path.write_text(json.dumps(_to_jsonable(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def format_production_readiness_summary(report: ProductionReadinessReport, path: Path) -> str:
    return "\n".join([
        "ION production-readiness report complete.",
        f"report: {path.as_posix()}",
        f"baseline: {report.baseline}",
        f"verdict: {report.verdict}",
        f"production_ready: {report.production_ready}",
        f"ratification_rows: {len(report.ratification_rows)}",
        f"critical_gaps: {len(report.critical_gaps)}",
        f"next: {report.next_sequence[0] if report.next_sequence else '(none)'}",
    ])

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate ION production-readiness ratification report.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--emitted-at", default=None)
    parser.add_argument("--report-dir", default=DEFAULT_REPORT_DIR)
    parser.add_argument("--json", action="store_true")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    report = generate_production_readiness_report(args.workspace_root, emitted_at=args.emitted_at)
    path = write_production_readiness_report(args.workspace_root, report, report_dir=args.report_dir)
    if args.json:
        print(json.dumps(_to_jsonable(report), indent=2, sort_keys=True))
    else:
        print(format_production_readiness_summary(report, path))
    return 0 if report.production_ready else 2

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _stable_id(prefix: str, *parts: str) -> str:
    return f"{prefix}-{hashlib.sha256(chr(10).join(parts).encode('utf-8')).hexdigest()[:16]}"

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

if __name__ == "__main__":
    raise SystemExit(main())
