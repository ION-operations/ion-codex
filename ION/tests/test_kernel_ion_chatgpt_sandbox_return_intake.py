import json
from pathlib import Path

from kernel.ion_chatgpt_sandbox_return_intake import (
    ACTIVE_QUEUE_PATH,
    BLOCKED_VERDICT,
    INBOX_ROOT,
    READY_VERDICT,
    build_sandbox_return_diff_preview,
    build_sandbox_return_queue_projection,
    commit_sandbox_return,
    queue_sandbox_return_codex_review,
    register_sandbox_return,
    validate_sandbox_return_manifest,
    write_sandbox_return_file,
)
from kernel.ion_chatops_bridge import APPROVAL_TOKEN, register_chatops_sandbox_return


RETURN_ID = "sev-20260505-041500-chatops-ui-return"


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-sandbox-return-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")


def _packet(return_id: str = RETURN_ID) -> dict:
    return {
        "return_id": return_id,
        "summary_text": "# Sandbox Return\n\nReview this patch only as inbox evidence.",
        "source_snapshot": {
            "package_path_seen_by_chatgpt": "ION_CODEX_7.zip",
            "package_sha256": "unknown-unless-provided-or-computed",
            "archive_root_confirmed": True,
            "expected_root_markers": ["pyproject.toml", "ION/REPO_AUTHORITY.md"],
        },
        "changed_paths": ["ION/09_integrations/browser_extension/ion_chatops_bridge/README.md"],
        "sandbox_validation": {
            "commands_run": [],
            "passed": None,
            "limitations": ["sandbox only"],
        },
    }


def _approved(packet: dict) -> dict:
    return {
        **packet,
        "approval": {
            "approved": True,
            "approved_by": "Braden",
            "approval_token": APPROVAL_TOKEN,
        },
    }


def _patch_text() -> str:
    return "\n".join(
        [
            "diff --git a/ION/09_integrations/browser_extension/ion_chatops_bridge/README.md b/ION/09_integrations/browser_extension/ion_chatops_bridge/README.md",
            "--- a/ION/09_integrations/browser_extension/ion_chatops_bridge/README.md",
            "+++ b/ION/09_integrations/browser_extension/ion_chatops_bridge/README.md",
            "@@ -1,3 +1,4 @@",
            " # ION ChatOps Bridge Extension",
            "+",
            "+Sandbox return test line.",
            "",
        ]
    )


def test_sandbox_return_manifest_validation_requires_false_authority_values():
    manifest = {
        "schema_id": "ion.chatgpt_sandbox_return.v1",
        "return_id": RETURN_ID,
        "created_at": "2026-05-05T04:15:00Z",
        "authoring_carrier": {"callsign": "Sev", "carrier": "chatgpt_browser", "sandbox": True},
        "human_sovereign": "Braden",
        "source_snapshot": {
            "archive_root_confirmed": True,
            "expected_root_markers": ["pyproject.toml", "ION/REPO_AUTHORITY.md"],
        },
        "base_assumptions": {
            "production_authority": False,
            "live_execution_authority": True,
            "direct_apply_authority": False,
            "git_push_authority": False,
        },
        "changed_paths": [],
        "sandbox_validation": {},
        "receipts_requested": ["sandbox_return_intake_receipt"],
    }

    result = validate_sandbox_return_manifest(manifest)

    assert result["accepted"] is False
    assert "live_execution_authority_must_be_false" in result["findings"]


def test_register_sandbox_return_writes_manifest_summary_queue_and_receipt(tmp_path):
    _seed_root(tmp_path)

    result = register_sandbox_return(tmp_path, _packet())

    assert result["ok"] is True
    assert result["verdict"] == READY_VERDICT
    return_root = tmp_path / INBOX_ROOT / RETURN_ID
    assert (return_root / "SANDBOX_RETURN_MANIFEST.json").exists()
    assert (return_root / "SUMMARY.md").exists()
    assert (tmp_path / ACTIVE_QUEUE_PATH).exists()
    queue = json.loads((tmp_path / ACTIVE_QUEUE_PATH).read_text(encoding="utf-8"))
    assert queue["return_count"] == 1
    assert queue["returns"][0]["status"] == "RETURN_DRAFT_WRITTEN"
    assert (tmp_path / result["receipt_path"]).exists()


def test_register_blocks_duplicate_return_id(tmp_path):
    _seed_root(tmp_path)
    assert register_sandbox_return(tmp_path, _packet())["ok"] is True

    result = register_sandbox_return(tmp_path, _packet())

    assert result["ok"] is False
    assert result["verdict"] == BLOCKED_VERDICT
    assert "return_id_already_exists" in result["validation"]["findings"]


def test_sandbox_return_file_commit_diff_preview_and_queue_review(tmp_path):
    _seed_root(tmp_path)
    register_sandbox_return(tmp_path, _packet())

    file_result = write_sandbox_return_file(
        tmp_path,
        RETURN_ID,
        "PATCH.diff",
        {"content": {"encoding": "utf-8", "text": _patch_text()}},
    )
    commit_result = commit_sandbox_return(tmp_path, RETURN_ID)
    after_commit_write = write_sandbox_return_file(
        tmp_path,
        RETURN_ID,
        "LATE.md",
        {"text": "blocked"},
    )
    preview_result = build_sandbox_return_diff_preview(tmp_path, RETURN_ID)
    review_result = queue_sandbox_return_codex_review(tmp_path, RETURN_ID)
    projection = build_sandbox_return_queue_projection(tmp_path)

    assert file_result["ok"] is True
    assert commit_result["ok"] is True
    assert commit_result["status"] == "RETURN_COMMITTED_FOR_REVIEW"
    assert after_commit_write["ok"] is False
    assert after_commit_write["finding"] == "return_is_committed_immutable"
    assert preview_result["ok"] is True
    assert preview_result["direct_apply_performed"] is False
    assert preview_result["changed_paths"] == ["ION/09_integrations/browser_extension/ion_chatops_bridge/README.md"]
    assert review_result["ok"] is True
    assert review_result["packet_path"].startswith("ION/05_context/current/chatgpt_connector/codex_work_requests/")
    latest = projection["returns"][0]
    assert latest["status"] == "CODEX_REVIEW_QUEUED"
    assert latest["committed"] is True


def test_sandbox_return_file_blocks_path_escape(tmp_path):
    _seed_root(tmp_path)
    register_sandbox_return(tmp_path, _packet())

    result = write_sandbox_return_file(tmp_path, RETURN_ID, "../PATCH.diff", {"text": "escape"})

    assert result["ok"] is False
    assert result["finding"] == "path_escape"


def test_chatops_sandbox_register_requires_braden_approval(tmp_path):
    _seed_root(tmp_path)

    blocked = register_chatops_sandbox_return(tmp_path, _packet("sev-20260505-041501-no-approval"))
    accepted = register_chatops_sandbox_return(tmp_path, _approved(_packet("sev-20260505-041502-approved")))

    assert blocked["ok"] is False
    assert blocked["finding"] == "approval_failed"
    assert accepted["ok"] is True
