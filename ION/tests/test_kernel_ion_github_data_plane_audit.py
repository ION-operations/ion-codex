import json
import subprocess
from pathlib import Path

from kernel.ion_github_data_plane_audit import (
    READY_VERDICT,
    SCHEMA_ID,
    audit_github_data_plane,
)


def _run_git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)


def _write_owner_surfaces(root: Path, *, branch: str = "main", remote: str = "https://github.com/ION-operations/ion-codex.git") -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"audit-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    (root / "ION/02_architecture").mkdir(parents=True, exist_ok=True)
    (root / "ION/02_architecture/ION_GITHUB_DATA_PLANE_PROTOCOL.md").write_text("# data plane\n", encoding="utf-8")
    (root / "ION/02_architecture/ION_GITHUB_WORK_DAEMON_PROTOCOL.md").write_text("# daemon\n", encoding="utf-8")
    (root / "ION/05_context/current/github_data_plane").mkdir(parents=True, exist_ok=True)
    (root / "ION/05_context/current/github_data_plane/PRIOR_ART_CONSOLIDATION_2026-05-04.md").write_text(
        "# prior art\n",
        encoding="utf-8",
    )
    (root / "ION/03_registry").mkdir(parents=True, exist_ok=True)
    (root / "ION/03_registry/ion_github_data_plane_registry.yaml").write_text(
        "\n".join(
            [
                "schema_id: ion.github_data_plane_registry.v1",
                "local_root:",
                f"  active_branch: {branch}",
                f"  active_remote: {remote}",
                "  first_commit_pushed: false",
                "  setup_state: CONFIGURED_LOCAL_REMOTE_READY_NO_COMMIT_PUSH",
                "prior_art:",
                "  consolidation_artifact: ION/05_context/current/github_data_plane/PRIOR_ART_CONSOLIDATION_2026-05-04.md",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _init_repo(root: Path, *, remote: str = "https://github.com/ION-operations/ion-codex.git") -> None:
    _run_git(root, "init")
    _run_git(root, "branch", "-M", "main")
    _run_git(root, "remote", "add", "origin", remote)


def test_github_data_plane_audit_reports_current_repo_without_mutation():
    result = audit_github_data_plane(Path.cwd())

    assert result["schema_id"] == SCHEMA_ID
    assert result["accepted"] is True
    assert result["verdict"] == READY_VERDICT
    assert result["git"]["git_present"] is True
    assert result["git"]["origin_configured"] is True
    assert result["registry_alignment"]["branch_alignment"] in {"MATCHES_REGISTRY", "ALLOWED_WORK_BRANCH"}
    assert result["registry_alignment"]["remote_alignment"] == "MATCHES_REGISTRY"
    assert result["network_access_used"] is False
    assert result["github_mutation_performed"] is False
    assert result["git_mutation_performed"] is False
    assert result["commit_authority"] is False
    assert result["push_authority"] is False
    assert "ion_runtime_git_push_authority_profile" in result["first_commit_readiness"]["required_runtime_policy_gates"]
    assert result["first_commit_readiness"]["push_branch_policy"]["main_auto_push_allowed"] is False
    assert result["first_commit_readiness"]["push_branch_policy"]["main_update_path"] == "pull_request_or_merge_gate"
    assert result["first_commit_readiness"]["human_gate_posture"] == "BOOTSTRAP_OR_BREAK_GLASS_ONLY_NOT_PER_PUSH_FINAL_LAW"


def test_github_data_plane_audit_blocks_non_git_root(tmp_path):
    _write_owner_surfaces(tmp_path)

    result = audit_github_data_plane(tmp_path)

    assert result["accepted"] is False
    assert result["failure_classification"] == "GITHUB_DATA_PLANE_NOT_CONFIGURED"
    assert "git_not_configured_at_shell_root" in result["findings"]
    assert result["first_commit_readiness"]["can_prepare_human_review_commit"] is False


def test_github_data_plane_audit_handles_first_commit_ready_repo(tmp_path):
    _write_owner_surfaces(tmp_path)
    _init_repo(tmp_path)
    (tmp_path / "ION/example.md").write_text("example\n", encoding="utf-8")

    result = audit_github_data_plane(tmp_path)

    assert result["accepted"] is True
    assert result["git"]["has_commits"] is False
    assert result["git"]["worktree"]["untracked_count"] >= 1
    assert result["first_commit_readiness"]["can_prepare_human_review_commit"] is True
    assert result["first_commit_readiness"]["first_commit_status"] == "NO_LOCAL_COMMITS_YET"


def test_github_data_plane_audit_accepts_allowed_work_branch(tmp_path):
    _write_owner_surfaces(tmp_path)
    _init_repo(tmp_path)
    _run_git(tmp_path, "checkout", "-b", "docs/public-data-plane-policy")

    result = audit_github_data_plane(tmp_path)

    assert result["accepted"] is True
    assert result["registry_alignment"]["branch_alignment"] == "ALLOWED_WORK_BRANCH"
    assert "active_branch_mismatch" not in result["findings"]


def test_github_data_plane_audit_parses_dirty_worktree_counts(tmp_path):
    _write_owner_surfaces(tmp_path)
    _init_repo(tmp_path)
    _run_git(tmp_path, "config", "user.email", "test@example.com")
    _run_git(tmp_path, "config", "user.name", "ION Test")
    tracked = tmp_path / "tracked.txt"
    tracked.write_text("one\n", encoding="utf-8")
    _run_git(tmp_path, "add", "tracked.txt")
    _run_git(tmp_path, "commit", "-m", "initial")
    tracked.write_text("two\n", encoding="utf-8")
    staged = tmp_path / "staged.txt"
    staged.write_text("staged\n", encoding="utf-8")
    _run_git(tmp_path, "add", "staged.txt")
    untracked = tmp_path / "untracked.txt"
    untracked.write_text("untracked\n", encoding="utf-8")

    result = audit_github_data_plane(tmp_path)

    assert result["accepted"] is True
    assert result["git"]["worktree"]["staged_count"] >= 1
    assert result["git"]["worktree"]["unstaged_count"] >= 1
    assert result["git"]["worktree"]["untracked_count"] >= 1


def test_github_data_plane_audit_sanitizes_inline_remote_credentials(tmp_path):
    secret_remote = "https://user:supersecret@example.com/org/repo.git"
    _write_owner_surfaces(tmp_path, remote="https://example.com/org/repo.git")
    _init_repo(tmp_path, remote=secret_remote)

    result = audit_github_data_plane(tmp_path)
    payload = json.dumps(result, sort_keys=True)

    assert "supersecret" not in payload
    assert result["accepted"] is False
    assert "origin_url_contains_inline_credentials" in result["findings"]
