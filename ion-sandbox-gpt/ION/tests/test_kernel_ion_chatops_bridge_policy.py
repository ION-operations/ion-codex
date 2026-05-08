import json
import time
from pathlib import Path

from kernel.ion_chatops_bridge import (
    APPROVAL_TOKEN,
    ACTION_SCHEMA,
    READY_VERDICT,
    attach_chatops_artifact_with_local_operator,
    build_chatops_attachable_artifacts,
    build_chatops_policy,
    build_chatops_agent_queue,
    build_chatops_agent_status,
    build_chatops_context_pack,
    build_chatops_local_operator_status,
    build_sev_context_brief,
    classify_chatops_action,
    prepare_chatops_artifact_upload,
    prepare_chatops_agent_next,
    resolve_chatops_artifact_download,
    submit_chatops_action,
    validate_chatops_action,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-chatops-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    for rel in [
        "ION/02_architecture/ION_BROWSER_CARRIER_RUNTIME_PROTOCOL.md",
        "ION/02_architecture/ION_BROWSER_FILE_ATTACHMENT_AUTOMATION_PROTOCOL.md",
        "ION/02_architecture/ION_CHATOPS_YAML_ACTION_PROTOCOL.md",
        "ION/02_architecture/ION_CHATGPT_SANDBOX_RETURN_INTAKE_PROTOCOL.md",
        "ION/02_architecture/ION_MOUNT_CONTRACT.md",
        "ION/03_registry/ion_chatops_action.schema.yaml",
        "ION/03_registry/ion_chatops_extension_policy.yaml",
        "ION/03_registry/ion_chatops_local_daemon_policy.yaml",
        "ION/03_registry/ion_github_data_plane_registry.yaml",
        "ION/03_registry/ion_chatgpt_sandbox_return.schema.json",
        "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
        "ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md",
        "ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py",
        "ION/04_packages/kernel/ion_chatgpt_sandbox_return_intake.py",
        "ION/04_packages/kernel/ion_codex_queue_runner.py",
        "ION/04_packages/kernel/ion_lifecycle_packager.py",
        "ION/04_packages/kernel/ion_safe_full_project_packager.py",
        "ION/07_templates/carriers/CHATGPT_BROWSER_CONNECTOR_SESSION_PACKET.md",
    ]:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{rel}\n", encoding="utf-8")
    (root / "ION/05_context/current/ACTIVE_WORK_PACKET.json").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/05_context/current/ACTIVE_WORK_PACKET.json").write_text(
        json.dumps({"objective": "Test active work packet."}) + "\n",
        encoding="utf-8",
    )


def _action(
    action_id: str,
    intent: str,
    *,
    target_path: str | None = None,
    text: str | None = None,
    objective: str | None = None,
) -> dict:
    action = {
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
        "target": {},
        "content": {},
        "context_refs": [],
        "receipts": {"requested": ["action_receipt"]},
    }
    if target_path is not None:
        action["target"] = {"provider": "local_ion", "root": "ION_CODEX", "path": target_path, "overwrite": False}
    if text is not None:
        action["content"] = {"encoding": "utf-8", "text": text}
    if objective is not None:
        action["objective"] = objective
    return {"ion_action": action}


def _approved(packet: dict) -> dict:
    return {
        **packet,
        "approval": {
            "approved": True,
            "approved_by": "Braden",
            "approval_token": APPROVAL_TOKEN,
        },
    }


def test_chatops_policy_owner_surfaces_ready(tmp_path):
    _seed_root(tmp_path)

    result = build_chatops_policy(tmp_path)

    assert result["verdict"] == READY_VERDICT
    assert "write_file_draft" in result["supported_mvp_intents"]
    assert result["agent_surface"]["backend_owner"] == "ION/04_packages/kernel/ion_codex_queue_runner.py"
    assert "compact_runtime_zip" in result["export_surface"]
    assert result["artifact_upload_surface"]["silent_upload_authority"] is False
    assert result["artifact_upload_surface"]["send_click_authority"] is False
    assert result["artifact_upload_surface"]["prepare_upload"] == "POST /artifacts/prepare-upload"
    assert result["local_operator_surface"]["attach_artifact"] == "POST /operator/attach-artifact"
    assert result["local_operator_surface"]["send_click_authority"] is False
    assert result["sandbox_return_surface"]["owner"] == "ION/04_packages/kernel/ion_chatgpt_sandbox_return_intake.py"
    assert result["sandbox_return_surface"]["direct_apply_authority"] is False
    assert result["main_policy"]["main_auto_push_allowed"] is False
    assert all(owner["exists"] for owner in result["owner_paths"].values())


def test_chatops_sev_context_brief_compiles_onboarding_prompt(tmp_path):
    _seed_root(tmp_path)

    result = build_sev_context_brief(tmp_path)

    assert result["ok"] is True
    assert result["brief"]["callsign"] == "Sev"
    assert result["brief"]["carrier_onboarding"]["profile_path"] == "ION/03_registry/chatgpt_browser_carrier_profile.yaml"
    assert result["brief"]["chatops"]["daemon"] == "http://127.0.0.1:8767"
    assert "ion_action_example:" in result["prompt"]
    assert "\nion_action:\n" not in result["prompt"]
    assert "create_codex_work_packet" in result["prompt"]
    assert result["production_authority"] is False


def test_chatops_action_validation_and_classification():
    packet = _action("sev-test-validate", "write_file_draft", target_path="ION/05_context/current/chatops_bridge/artifacts/demo.md", text="demo")

    validation = validate_chatops_action(packet)
    classification = classify_chatops_action(packet["ion_action"])

    assert validation["accepted"] is True
    assert validation["action_id"] == "sev-test-validate"
    assert classification["risk_class"] == "approval_required_mutation"


def test_chatops_blocks_template_placeholder_codex_action():
    packet = _action(
        "sev-YYYYMMDD-HHMMSS-short-slug",
        "create_codex_work_packet",
        objective="State the exact bounded work for local Codex/ION to perform.",
    )

    validation = validate_chatops_action(packet)

    assert validation["accepted"] is False
    assert "action_id_must_not_be_template_placeholder" in validation["findings"]
    assert "objective_must_be_concrete_not_template_placeholder" in validation["findings"]


def test_chatops_accepts_concrete_flat_codex_action_from_sev():
    packet = {
        "ion_action": {
            "schema": ACTION_SCHEMA,
            "action_id": "sev-20260505-021500-chatops-reentry-hardening",
            "intent": "create_codex_work_packet",
            "callsign": "Sev",
            "carrier": "chatgpt_browser",
            "human_sovereign": "Braden",
            "requires_approval": True,
            "production_authority": False,
            "live_execution_authority": False,
            "objective": "Verify and harden the live ION ChatOps Browser Carrier Runtime after successful extension smoke and re-entry injection.",
        }
    }

    validation = validate_chatops_action(packet)

    assert validation["accepted"] is True
    assert validation["action_id"] == "sev-20260505-021500-chatops-reentry-hardening"


def test_chatops_submit_writes_draft_and_receipt(tmp_path):
    _seed_root(tmp_path)
    packet = _approved(
        _action(
            "sev-write-draft",
            "write_file_draft",
            target_path="ION/05_context/current/chatops_bridge/artifacts/demo.md",
            text="# Demo\n",
        )
    )

    result = submit_chatops_action(tmp_path, packet)

    assert result["ok"] is True
    assert (tmp_path / "ION/05_context/current/chatops_bridge/artifacts/demo.md").read_text(encoding="utf-8") == "# Demo\n"
    receipt = json.loads((tmp_path / result["receipt_path"]).read_text(encoding="utf-8"))
    assert receipt["status"] == "completed"
    assert "ION/05_context/current/chatops_bridge/artifacts/demo.md" in receipt["files_touched"]


def test_chatops_submit_blocks_overwrite_without_silent_loss(tmp_path):
    _seed_root(tmp_path)
    target = tmp_path / "ION/05_context/current/chatops_bridge/artifacts/existing.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("old\n", encoding="utf-8")
    packet = _approved(
        _action(
            "sev-block-overwrite",
            "write_file_draft",
            target_path="ION/05_context/current/chatops_bridge/artifacts/existing.md",
            text="new\n",
        )
    )

    result = submit_chatops_action(tmp_path, packet)

    assert result["ok"] is False
    assert result["execution"]["finding"] == "target_exists_overwrite_false"
    assert target.read_text(encoding="utf-8") == "old\n"
    receipt = json.loads((tmp_path / result["receipt_path"]).read_text(encoding="utf-8"))
    assert receipt["failure_classification"] == "POLICY_BLOCK_WORKING_AS_DESIGNED"


def test_chatops_submit_requires_braden_approval(tmp_path):
    _seed_root(tmp_path)
    packet = _action(
        "sev-no-approval",
        "write_file_draft",
        target_path="ION/05_context/current/chatops_bridge/artifacts/nope.md",
        text="nope\n",
    )

    result = submit_chatops_action(tmp_path, packet)

    assert result["ok"] is False
    assert "approval_required" in result["validation"]["findings"]
    assert not (tmp_path / "ION/05_context/current/chatops_bridge/artifacts/nope.md").exists()


def test_chatops_create_codex_work_packet_uses_existing_queue_owner(tmp_path):
    _seed_root(tmp_path)
    packet = _approved(
        _action(
            "sev-codex-work",
            "create_codex_work_packet",
            objective="Build a bounded ChatOps follow-up slice.",
        )
    )

    result = submit_chatops_action(tmp_path, packet)

    assert result["ok"] is True
    packet_path = result["execution"]["packet_path"]
    assert packet_path.startswith("ION/05_context/current/chatgpt_connector/codex_work_requests/")
    assert (tmp_path / packet_path).exists()
    queue = json.loads((tmp_path / "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json").read_text(encoding="utf-8"))
    assert queue["request_count"] == 1


def test_chatops_flat_sev_codex_work_shape_is_canonicalized(tmp_path):
    _seed_root(tmp_path)
    packet = _approved(
        {
            "ion_action": {
                "schema": ACTION_SCHEMA,
                "action_id": "sev-flat-codex-work",
                "intent": "create_codex_work_packet",
                "callsign": "Sev",
                "carrier": "chatgpt_browser",
                "human_sovereign": "Braden",
                "requires_approval": True,
                "production_authority": False,
                "live_execution_authority": False,
                "objective": "Verify flat Sev ChatOps shape.",
            }
        }
    )

    validation = validate_chatops_action(packet, require_approval=True)
    result = submit_chatops_action(tmp_path, packet)

    assert validation["accepted"] is True
    assert result["ok"] is True
    stored = json.loads((tmp_path / result["action_path"]).read_text(encoding="utf-8"))
    action = stored["ion_action"]
    assert action["actor"] == {"callsign": "Sev", "carrier": "chatgpt_browser"}
    assert action["authority"]["human_sovereign"] == "Braden"
    assert action["receipts"]["requested"] == ["codex_work_packet_receipt", "action_receipt"]
    assert result["execution"]["packet_path"].startswith("ION/05_context/current/chatgpt_connector/codex_work_requests/")


def test_chatops_create_github_issue_draft_does_not_mutate_github(tmp_path):
    _seed_root(tmp_path)
    packet = _approved(
        {
            "ion_action": {
                "schema": ACTION_SCHEMA,
                "action_id": "sev-github-issue-draft",
                "intent": "create_github_issue",
                "actor": {"callsign": "Sev", "carrier": "chatgpt_browser"},
                "authority": {
                    "human_sovereign": "Braden",
                    "requires_approval": True,
                    "production_authority": False,
                    "live_execution_authority": False,
                },
                "github": {
                    "owner": "ION-operations",
                    "repo": "ion-codex",
                    "title": "Draft issue",
                    "body": "Draft body",
                },
                "receipts": {"requested": ["github_issue_receipt"]},
            }
        }
    )

    result = submit_chatops_action(tmp_path, packet)

    assert result["ok"] is True
    draft_path = result["execution"]["draft_path"]
    assert draft_path.startswith("ION/05_context/current/chatops_bridge/artifacts/github_issue_drafts/")
    draft = json.loads((tmp_path / draft_path).read_text(encoding="utf-8"))
    assert draft["status"] == "draft_not_submitted"


def test_chatops_agent_status_and_queue_reuse_codex_queue_owner(tmp_path):
    _seed_root(tmp_path)
    submit_chatops_action(
        tmp_path,
        _approved(
            _action(
                "sev-agent-status-work",
                "create_codex_work_packet",
                objective="Queue work so the ChatOps agent surface can project it.",
            )
        ),
    )

    status = build_chatops_agent_status(tmp_path)
    queue = build_chatops_agent_queue(tmp_path)

    assert status["ok"] is True
    assert status["backend"] == "codex_cli"
    assert status["runner_owner"] == "ION/04_packages/kernel/ion_codex_queue_runner.py"
    assert status["queued_request_count"] == 1
    assert queue["request_count"] == 1
    assert queue["requests"][0]["status"] == "QUEUED_FOR_CODEX_CARRIER"


def test_chatops_agent_prepare_next_requires_approval_and_writes_run_packet(tmp_path):
    _seed_root(tmp_path)
    submit_chatops_action(
        tmp_path,
        _approved(
            _action(
                "sev-agent-prepare-work",
                "create_codex_work_packet",
                objective="Prepare one bounded Codex run packet through ChatOps.",
            )
        ),
    )

    blocked = prepare_chatops_agent_next(tmp_path, {})
    result = prepare_chatops_agent_next(tmp_path, _approved({}))

    assert blocked["ok"] is False
    assert blocked["finding"] == "approval_failed"
    assert result["ok"] is True
    run = result["result"]["run"]
    assert run["status"] == "PREPARED_NOT_STARTED"
    assert (tmp_path / run["run_packet_path"]).exists()
    assert (tmp_path / result["receipt_path"]).exists()


def test_chatops_context_pack_includes_agent_and_package_controls(tmp_path):
    _seed_root(tmp_path)

    result = build_chatops_context_pack(tmp_path)

    assert result["ok"] is True
    assert result["pack"]["callsign"] == "Sev"
    assert result["pack"]["bridge_tools"]["agent_prepare_next"] == "POST /agent/prepare-next with Braden approval"
    assert result["pack"]["bridge_tools"]["compact_zip"] == "POST /exports/lifecycle-zip with package_class=COMPACT_RUNTIME and Braden approval"
    assert result["pack"]["bridge_tools"]["attachable_artifacts"] == "GET /artifacts/attachables"
    assert result["pack"]["bridge_tools"]["prepare_artifact_upload"] == "POST /artifacts/prepare-upload with Braden approval"
    assert result["pack"]["bridge_tools"]["local_operator_attach_artifact"] == "POST /operator/attach-artifact with Braden approval"
    assert result["pack"]["bridge_tools"]["sandbox_returns"] == "GET /sandbox/returns"
    assert result["pack"]["sandbox_returns"]["inbox_root"] == "ION/05_context/inbox/chatgpt_sandbox_returns"
    assert "ION local context pack" in result["prompt"]


def test_chatops_artifact_upload_prepare_requires_approval_and_ticket(tmp_path):
    _seed_root(tmp_path)
    zip_path = tmp_path / "ION/06_artifacts/packages/demo.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    zip_path.write_bytes(b"PK\x03\x04demo")

    listing = build_chatops_attachable_artifacts(tmp_path)
    blocked = prepare_chatops_artifact_upload(tmp_path, {"artifact_path": "ION/06_artifacts/packages/demo.zip"})
    prepared = prepare_chatops_artifact_upload(
        tmp_path,
        _approved({"artifact_path": "ION/06_artifacts/packages/demo.zip"}),
    )
    resolved_path, validation = resolve_chatops_artifact_download(tmp_path, prepared.get("download_token", ""))

    assert listing["ok"] is True
    assert any(row["path"] == "ION/06_artifacts/packages/demo.zip" for row in listing["candidates"])
    assert blocked["ok"] is False
    assert blocked["finding"] == "approval_failed"
    assert prepared["ok"] is True
    assert prepared["download_url"].endswith(f"/artifacts/download/{prepared['download_token']}")
    assert prepared["filename"] == "demo.zip"
    assert (tmp_path / prepared["ticket_path"]).exists()
    assert (tmp_path / prepared["receipt_path"]).exists()
    assert resolved_path == zip_path.resolve()
    assert validation["ok"] is True


def test_chatops_local_operator_attachment_requires_approval_and_blocks_send_click(tmp_path):
    _seed_root(tmp_path)
    zip_path = tmp_path / "ION/06_artifacts/packages/demo.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    zip_path.write_bytes(b"PK\x03\x04demo")
    prepared = prepare_chatops_artifact_upload(
        tmp_path,
        _approved({"artifact_path": "ION/06_artifacts/packages/demo.zip"}),
    )

    blocked = attach_chatops_artifact_with_local_operator(tmp_path, {"download_token": prepared["download_token"]})
    send_blocked = attach_chatops_artifact_with_local_operator(
        tmp_path,
        _approved({"download_token": prepared["download_token"], "send_after_attach": True, "dry_run": True}),
    )
    dry_run = attach_chatops_artifact_with_local_operator(
        tmp_path,
        _approved({
            "download_token": prepared["download_token"],
            "dry_run": True,
            "target_kind": "attach_button",
            "target_rect": {"x": 100, "y": 200, "width": 40, "height": 20},
            "target_screen_rect": {"x": 300, "y": 400, "width": 60, "height": 30},
            "composer_rect": {"x": 80, "y": 180, "width": 400, "height": 80},
            "viewport": {"width": 1200, "height": 900},
            "page_url": "https://chatgpt.com/c/test",
            "captured_at_ms": int(time.time() * 1000),
        }),
    )
    invalid_geometry = attach_chatops_artifact_with_local_operator(
        tmp_path,
        _approved({
            "download_token": prepared["download_token"],
            "dry_run": True,
            "target_kind": "attach_button",
            "target_rect": {"x": 0, "y": 0, "width": 1, "height": 1},
            "target_screen_rect": {"x": 0, "y": 0, "width": 1, "height": 1},
            "composer_rect": {"x": 800, "y": 800, "width": 200, "height": 80},
            "viewport": {"width": 1200, "height": 900},
            "page_url": "https://chatgpt.com/c/test",
            "captured_at_ms": int(time.time() * 1000),
        }),
    )
    status = build_chatops_local_operator_status(tmp_path)

    assert blocked["ok"] is False
    assert blocked["finding"] == "approval_failed"
    assert send_blocked["ok"] is False
    assert send_blocked["finding"] == "send_click_not_authorized"
    assert dry_run["ok"] is True
    assert dry_run["dry_run"] is True
    assert dry_run["no_send_click_performed"] is True
    assert dry_run["target_center"] == (330, 415)
    assert dry_run["geometry"]["ok"] is True
    assert (tmp_path / dry_run["receipt_path"]).exists()
    assert invalid_geometry["ok"] is False
    assert invalid_geometry["finding"] == "LOCAL_OPERATOR_TARGET_GEOMETRY_INVALID"
    assert status["send_click_authority"] is False


def test_chatops_submit_rejects_mutating_action_without_policy_approval_even_if_action_says_no_approval(tmp_path):
    _seed_root(tmp_path)
    packet = _action(
        "sev-no-approval-bypass",
        "write_file_draft",
        target_path="ION/05_context/current/chatops_bridge/smoke/NO_APPROVAL_BYPASS.md",
        text="blocked",
    )
    packet["ion_action"]["authority"]["requires_approval"] = False

    result = submit_chatops_action(tmp_path, packet)

    assert result["ok"] is False
    assert result["finding"] == "validation_failed"
    assert "approval_required" in result["validation"]["findings"]
    assert "requires_approval_must_be_true_for_mutating_intent" in result["validation"]["findings"]
    assert not (tmp_path / "ION/05_context/current/chatops_bridge/smoke/NO_APPROVAL_BYPASS.md").exists()


def test_chatops_validation_rejects_live_execution_authority_true(tmp_path):
    _seed_root(tmp_path)
    packet = _approved(
        _action(
            "sev-live-execution-authority",
            "create_codex_work_packet",
            objective="Attempt to assert live execution authority through ChatOps.",
        )
    )
    packet["ion_action"]["authority"]["live_execution_authority"] = True

    validation = validate_chatops_action(packet, require_approval=True)

    assert validation["accepted"] is False
    assert "live_execution_authority_must_be_false" in validation["findings"]


def test_chatops_agent_status_projection_is_read_only_by_default(monkeypatch, tmp_path):
    _seed_root(tmp_path)
    calls = []

    def fake_status(root, *, reconcile=True):
        calls.append(reconcile)
        return {
            "verdict": "ION_CODEX_QUEUE_RUNNER_READY",
            "queued_request_count": 0,
            "next_request_path": None,
            "active_run": None,
            "active_process_running": False,
            "stale_active_run_detected": False,
            "latest_runs": [],
        }

    monkeypatch.setattr("kernel.ion_chatops_bridge.build_codex_queue_runner_status", fake_status)

    result = build_chatops_agent_status(tmp_path)

    assert result["ok"] is True
    assert calls == [False]
