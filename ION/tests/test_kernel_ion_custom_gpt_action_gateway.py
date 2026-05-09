import json
from pathlib import Path

from kernel.ion_chatops_bridge import ACTION_SCHEMA, APPROVAL_TOKEN
from kernel.ion_custom_gpt_action_gateway import (
    READY_VERDICT,
    build_gateway_health,
    build_gateway_policy_surface,
    build_recent_gateway_receipts,
    submit_gateway_action_packet,
    validate_gateway_action_packet,
    validate_gateway_auth,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-gateway-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    for rel in [
        "ION/02_architecture/ION_BROWSER_CARRIER_RUNTIME_PROTOCOL.md",
        "ION/02_architecture/ION_BROWSER_FILE_ATTACHMENT_AUTOMATION_PROTOCOL.md",
        "ION/02_architecture/ION_CHATOPS_YAML_ACTION_PROTOCOL.md",
        "ION/02_architecture/ION_CHATGPT_SANDBOX_RETURN_INTAKE_PROTOCOL.md",
        "ION/02_architecture/ION_CUSTOM_GPT_ACTION_GATEWAY_PROTOCOL.md",
        "ION/03_registry/ion_chatops_action.schema.yaml",
        "ION/03_registry/ion_chatops_extension_policy.yaml",
        "ION/03_registry/ion_chatops_local_daemon_policy.yaml",
        "ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml",
        "ION/03_registry/ion_github_data_plane_registry.yaml",
        "ION/03_registry/ion_chatgpt_sandbox_return.schema.json",
        "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
        "ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md",
        "ION/04_packages/kernel/ion_chatops_bridge.py",
        "ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py",
        "ION/04_packages/kernel/ion_chatgpt_sandbox_return_intake.py",
        "ION/04_packages/kernel/ion_codex_queue_runner.py",
        "ION/04_packages/kernel/ion_agent_invocation_broker.py",
        "ION/04_packages/kernel/ion_lifecycle_packager.py",
        "ION/04_packages/kernel/ion_safe_full_project_packager.py",
        "ION/09_integrations/custom_gpt_action_gateway/openapi.yaml",
    ]:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{rel}\n", encoding="utf-8")
    policy = root / "ION/03_registry/ion_custom_gpt_action_gateway_policy.yaml"
    policy.write_text(
        "\n".join(
            [
                "schema_id: ion.custom_gpt_action_gateway_policy.v1",
                "status: draft_non_production",
                "production_authority: false",
                "live_execution_authority: false",
                "listen_host: 127.0.0.1",
                "listen_port: 8777",
                "public_transport: cloudflare_tunnel",
                "auth:",
                "  required: true",
                "  scheme: bearer",
                "  token_env_var: ION_ACTION_GATEWAY_TOKEN",
                "  token_sha256_env_var: ION_ACTION_GATEWAY_TOKEN_SHA256",
                "limits:",
                "  max_body_bytes: 262144",
                "  require_idempotency_key_for_mutation: true",
                "allowed_get_paths:",
                "  - /health",
                "  - /policy",
                "allowed_post_paths:",
                "  - /actions/validate",
                "  - /actions/submit",
                "supported_mvp_intents:",
                "  - register_artifact",
                "  - write_file_draft",
                "  - create_codex_work_packet",
                "  - create_github_issue_draft",
                "hard_gated_intents:",
                "  - delete_file",
                "  - overwrite_protected_file",
                "  - push_main",
                "  - access_credential",
                "  - production_deploy",
                "  - broad_shell",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / "ION/05_context/current/ACTIVE_WORK_PACKET.json").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/05_context/current/ACTIVE_WORK_PACKET.json").write_text(
        json.dumps({"objective": "Gateway test active work packet."}) + "\n",
        encoding="utf-8",
    )


def _seed_assistant_work_routes(root: Path) -> None:
    registry = root / "ION/05_context/current/ai_assistant_work/registries/AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        "\n".join(
            [
                "schema: ion.ai_assistant_work.route_registry.v0_1",
                "status: candidate_current_state_not_accepted_canon",
                "routes:",
                "- route_id: route.ui_specialist_work",
                "  trigger_patterns:",
                "  - frontend component",
                "  - accessibility",
                "  required_domains:",
                "  - ui_ux_domain",
                "  primary_agents:",
                "  - UI_ARCHITECT",
                "  output_contract:",
                "    include:",
                "    - screen states",
                "    forbid:",
                "    - visual polish without state/a11y proof",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    compiler_dir = root / "ION/05_context/current/ai_assistant_work/route_compiler"
    compiler_dir.mkdir(parents=True, exist_ok=True)
    (compiler_dir / "AI_ASSISTANT_WORK_ROUTE_COMPILER_CANDIDATE_MAP_20260508T182500Z.json").write_text(
        json.dumps(
            {
                "route_mappings": [
                    {
                        "route_id": "route.ui_specialist_work",
                        "active_skill_candidates": ["codex-solo-work"],
                        "active_lens_candidates": ["vizier", "mason_codex", "nemesis"],
                        "template_spec_candidates": ["screen_state_matrix_packet"],
                    }
                ]
            }
        )
        + "\n",
        encoding="utf-8",
    )


def _seed_assistant_work_fission(root: Path) -> None:
    fission = root / "ION/05_context/current/ai_assistant_work/fission/AI_ASSISTANT_WORK_DOMAIN_FISSION_CANDIDATES_V0_1.yaml"
    fission.parent.mkdir(parents=True, exist_ok=True)
    fission.write_text(
        "\n".join(
            [
                "schema: ion.ai_assistant_work.domain_fission_candidates.v0_1",
                "status: candidate_current_state_not_accepted_canon",
                "candidate_count: 1",
                "candidates:",
                "- candidate_domain_id: pr_agent_work_domain",
                "  title: PR Agent Work Domain",
                "  parent_domains:",
                "  - review_security_domain",
                "  - testing_quality_domain",
                "  rationale: PR-agent work combines diff review, CI evidence, lockfile analysis, review comments, and merge settlement.",
                "  pressure_signals:",
                "  - CI and lockfile evidence need specialized proof",
                "  proposed_primary_agents:",
                "  - PR_REVIEW_STEWARD",
                "  - CI_EVIDENCE_TRIAGER",
                "  - LOCKFILE_AUDITOR",
                "  proposed_template_packets:",
                "  - pr_review_packet",
                "  - ci_evidence_triage_packet",
                "  proposed_protocols:",
                "  - merge_requires_settlement_receipt",
                "  critical_state_surfaces:",
                "  - diff_state",
                "  - ci_state",
                "  - lockfile_state",
                "  settlement_route: review_return_to_settlement_steward",
                "  status: fission_candidate_not_accepted_domain",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _action(action_id: str, intent: str = "register_artifact") -> dict:
    return {
        "ion_action": {
            "schema": ACTION_SCHEMA,
            "action_id": action_id,
            "intent": intent,
            "actor": {"callsign": "Sev", "carrier": "chatgpt_browser"},
            "authority": {
                "human_sovereign": "Braden",
                "requires_approval": True,
                "production_authority": False,
                "live_execution_authority": False,
            },
            "artifact_refs": [{"provider": "local_ion", "path": "ION/05_context/current/demo.md"}],
            "context_refs": [],
            "receipts": {"requested": ["action_receipt"]},
        }
    }


def _approved(packet: dict, *, idempotency_key: str = "gateway-test-key") -> dict:
    return {
        **packet,
        "idempotency_key": idempotency_key,
        "operator_approval_evidence": {
            "approved": True,
            "approved_by": "Braden",
            "approval_token": APPROVAL_TOKEN,
        },
    }


def test_gateway_health_returns_non_production_status(tmp_path):
    _seed_root(tmp_path)

    result = build_gateway_health(tmp_path)

    assert result["ok"] is True
    assert result["verdict"] == READY_VERDICT
    assert result["production_authority"] is False
    assert result["live_execution_authority"] is False


def test_gateway_policy_surface_imports_chatops_hard_gates(tmp_path):
    _seed_root(tmp_path)

    result = build_gateway_policy_surface(tmp_path)

    assert result["verdict"] == READY_VERDICT
    assert "delete_file" in result["hard_gated_intents"]
    assert "delete_file" in result["imported_chatops_hard_gated_intents"]
    assert result["auth"]["required"] is True
    assert "secret-token" not in json.dumps(result)


def test_gateway_auth_rejects_missing_and_accepts_valid_token(monkeypatch, tmp_path):
    _seed_root(tmp_path)
    policy = build_gateway_policy_surface(tmp_path)
    monkeypatch.setenv("ION_ACTION_GATEWAY_TOKEN", "secret-token")

    missing = validate_gateway_auth({}, policy)
    valid = validate_gateway_auth({"Authorization": "Bearer secret-token"}, policy)
    invalid = validate_gateway_auth({"Authorization": "Bearer wrong"}, policy)

    assert missing["ok"] is False
    assert missing["refusal_class"] == "AUTH_MISSING"
    assert valid["ok"] is True
    assert "secret-token" not in json.dumps(valid)
    assert invalid["ok"] is False
    assert invalid["refusal_class"] == "AUTH_INVALID"


def test_gateway_validate_does_not_write_receipts(tmp_path):
    _seed_root(tmp_path)

    result = validate_gateway_action_packet(tmp_path, _action("gateway-validate-only"))

    assert result["ok"] is True
    assert result["assistant_work_route"]["candidate_only"] is True
    assert not (tmp_path / "ION/05_context/current/action_gateway/receipts").exists()


def test_gateway_validate_attaches_candidate_assistant_work_route(tmp_path):
    _seed_root(tmp_path)
    _seed_assistant_work_routes(tmp_path)
    packet = _action("gateway-ui-route", intent="create_codex_work_packet")
    packet["ion_action"]["objective"] = "Draft a frontend component with accessibility and screen states."

    result = validate_gateway_action_packet(tmp_path, packet)

    route = result["assistant_work_route"]
    assert result["ok"] is True
    assert route["ok"] is True
    assert route["gateway_validation_only"] is True
    assert route["gateway_packet_validated"] is True
    assert route["route_id"] == "route.ui_specialist_work"
    assert route["candidate_only"] is True
    assert route["authority_boundary"]["mutates_ION_03_registry"] is False
    assert route["authority_boundary"]["mutates_product_front_door"] is False


def test_gateway_validate_surfaces_dynamic_domain_agent_proposal(tmp_path):
    _seed_root(tmp_path)
    _seed_assistant_work_routes(tmp_path)
    _seed_assistant_work_fission(tmp_path)
    packet = _action("gateway-pr-dynamic-route", intent="create_codex_work_packet")
    packet["ion_action"]["objective"] = "Review PR branch, classify CI failure evidence, inspect lockfile diff risk, and prepare merge settlement."

    result = validate_gateway_action_packet(tmp_path, packet)

    route = result["assistant_work_route"]
    proposal = route["dynamic_domain_agent_proposal"]
    assert result["ok"] is True
    assert route["gateway_validation_only"] is True
    assert proposal["needed"] is True
    assert proposal["trigger"] == "fission_candidate_match"
    assert proposal["recommended_local_hub_report"] is True
    assert proposal["candidate_domains"][0]["domain_id"] == "pr_agent_work_domain"
    assert "CI_EVIDENCE_TRIAGER" in [agent["agent_id"] for agent in proposal["candidate_agents"]]
    assert proposal["authority_boundary"]["requires_explicit_acceptance_to_land"] is True


def test_gateway_submit_requires_idempotency_key(tmp_path):
    _seed_root(tmp_path)

    result = submit_gateway_action_packet(tmp_path, _action("gateway-no-idempotency"))

    assert result["ok"] is False
    assert result["refusal_class"] == "IDEMPOTENCY_KEY_REQUIRED"
    assert (tmp_path / result["gateway_receipt_path"]).exists()


def test_gateway_submit_requires_operator_approval_evidence(tmp_path):
    _seed_root(tmp_path)
    packet = {**_action("gateway-no-approval"), "idempotency_key": "missing-approval"}

    result = submit_gateway_action_packet(tmp_path, packet)

    assert result["ok"] is False
    assert result["refusal_class"] == "OPERATOR_APPROVAL_REQUIRED"
    assert (tmp_path / result["gateway_receipt_path"]).exists()


def test_gateway_rejects_production_and_live_authority(tmp_path):
    _seed_root(tmp_path)
    packet = _approved(_action("gateway-authority-refusal"))
    packet["ion_action"]["authority"]["production_authority"] = True
    packet["ion_action"]["authority"]["live_execution_authority"] = True

    result = submit_gateway_action_packet(tmp_path, packet)

    assert result["ok"] is False
    assert result["refusal_class"] == "PRODUCTION_AUTHORITY_REFUSED"


def test_gateway_hard_gated_intent_rejected_before_owner_submit(tmp_path):
    _seed_root(tmp_path)
    packet = _approved(_action("gateway-hard-gated", intent="delete_file"))

    result = submit_gateway_action_packet(tmp_path, packet)

    assert result["ok"] is False
    assert result["refusal_class"] == "INTENT_HARD_GATED"
    receipts = build_recent_gateway_receipts(tmp_path)
    assert receipts["gateway_receipts"]


def test_gateway_submit_routes_to_chatops_owner_and_blocks_replay(tmp_path):
    _seed_root(tmp_path)
    packet = _approved(_action("gateway-register-artifact"), idempotency_key="replay-key")

    first = submit_gateway_action_packet(tmp_path, packet)
    second = submit_gateway_action_packet(tmp_path, packet)

    assert first["ok"] is True
    assert first["owner"] == "ION/04_packages/kernel/ion_chatops_bridge.py"
    assert (tmp_path / first["gateway_receipt_path"]).exists()
    assert (tmp_path / first["owner_result"]["receipt_path"]).exists()
    assert second["ok"] is False
    assert second["refusal_class"] == "IDEMPOTENCY_REPLAY_BLOCKED"
