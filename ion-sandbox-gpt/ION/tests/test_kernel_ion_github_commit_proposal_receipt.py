import json
import subprocess
from pathlib import Path

from kernel.ion_github_commit_proposal_receipt import (
    BLOCKED_VERDICT,
    READY_VERDICT,
    build_github_commit_proposal_receipt,
)


def _run_git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)
    return proc.stdout.strip()


def _write_owner_surfaces(root: Path, *, branch: str = "main", remote: str = "https://github.com/ION-operations/ion-codex.git") -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"proposal-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    (root / "ION/02_architecture").mkdir(parents=True, exist_ok=True)
    (root / "ION/02_architecture/ION_GITHUB_DATA_PLANE_PROTOCOL.md").write_text("# data plane\n", encoding="utf-8")
    (root / "ION/02_architecture/ION_GITHUB_WORK_DAEMON_PROTOCOL.md").write_text("# daemon\n", encoding="utf-8")
    (root / "ION/05_context/current/github_data_plane").mkdir(parents=True, exist_ok=True)
    (root / "ION/05_context/current/github_data_plane/PRIOR_ART_CONSOLIDATION_2026-05-04.md").write_text("# prior art\n", encoding="utf-8")
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


def test_commit_proposal_writes_receipt_and_manifest_without_git_mutation(tmp_path):
    _write_owner_surfaces(tmp_path)
    _init_repo(tmp_path)
    (tmp_path / "ION/example.md").write_text("example\n", encoding="utf-8")

    result = build_github_commit_proposal_receipt(tmp_path, write=True)
    status = _run_git(tmp_path, "status", "--porcelain")

    assert result["verdict"] == READY_VERDICT
    assert result["git_mutation_performed"] is False
    assert result["github_mutation_performed"] is False
    assert result["policy"]["commit_authority"] is False
    assert result["policy"]["push_authority"] is False
    assert result["secret_scan"]["accepted"] is True
    assert "ION/example.md" in json.loads((tmp_path / result["path_manifest_path"]).read_text(encoding="utf-8"))["paths"]
    assert (tmp_path / result["proposal_path"]).exists()
    assert "A  " not in status


def test_commit_proposal_blocks_and_redacts_secret_like_content(tmp_path):
    _write_owner_surfaces(tmp_path)
    _init_repo(tmp_path)
    secret_value = "ghp_" + ("A" * 36)
    (tmp_path / "ION/leak.md").write_text(f"token = {secret_value}\n", encoding="utf-8")

    result = build_github_commit_proposal_receipt(tmp_path, write=False)
    payload = json.dumps(result, sort_keys=True)

    assert result["verdict"] == BLOCKED_VERDICT
    assert result["failure_classification"] == "GIT_SECRET_SCAN_BLOCK"
    assert "secret_scan_block" in result["findings"]
    assert secret_value not in payload
    assert result["secret_scan"]["findings"][0]["excerpt"].startswith("<redacted:")


def test_commit_proposal_ignores_placeholder_secret_examples(tmp_path):
    _write_owner_surfaces(tmp_path)
    _init_repo(tmp_path)
    (tmp_path / "ION/example.md").write_text('export OPENAI_API_KEY="..."\n', encoding="utf-8")

    result = build_github_commit_proposal_receipt(tmp_path, write=False)

    assert result["verdict"] == READY_VERDICT
    assert result["secret_scan"]["accepted"] is True


def test_commit_proposal_can_run_fixed_validation_commands(monkeypatch, tmp_path):
    _write_owner_surfaces(tmp_path)
    _init_repo(tmp_path)
    (tmp_path / "ION/example.md").write_text("example\n", encoding="utf-8")

    def fake_run_validation(root: Path):
        return [{"command": ["fixed"], "returncode": 0, "passed": True, "stdout_tail": "ok", "stderr_tail": ""}]

    monkeypatch.setattr("kernel.ion_github_commit_proposal_receipt._run_validation", fake_run_validation)

    result = build_github_commit_proposal_receipt(tmp_path, write=False, run_validation=True)

    assert result["verdict"] == READY_VERDICT
    assert result["validation"]["passed"] is True
    assert result["validation"]["commands"][0]["command"] == ["fixed"]
