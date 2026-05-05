"""Read-only local GitHub data-plane audit for ION."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from .ion_carrier_onboard import resolve_shell_root_from_ion_root

SCHEMA_ID = "ion.github_data_plane_audit.v1"
READY_VERDICT = "ION_GITHUB_DATA_PLANE_AUDIT_READY"
BLOCKED_VERDICT = "ION_GITHUB_DATA_PLANE_AUDIT_BLOCKED"

EXPECTED_REMOTE_URLS = {
    "https://github.com/ION-operations/ion-codex.git",
    "git@github.com:ION-operations/ion-codex.git",
}

DEFAULT_ALLOWED_PUSH_BRANCH_PATTERNS = [
    "work/*",
    "docs/*",
    "agent/*",
    "data-plane/*",
]

REQUIRED_OWNER_PATHS = {
    "data_plane_protocol": "ION/02_architecture/ION_GITHUB_DATA_PLANE_PROTOCOL.md",
    "work_daemon_protocol": "ION/02_architecture/ION_GITHUB_WORK_DAEMON_PROTOCOL.md",
    "data_plane_registry": "ION/03_registry/ion_github_data_plane_registry.yaml",
    "prior_art_consolidation": "ION/05_context/current/github_data_plane/PRIOR_ART_CONSOLIDATION_2026-05-04.md",
}

FAILURE_CLASSES = [
    "GITHUB_DATA_PLANE_NOT_CONFIGURED",
    "GITHUB_AUTH_UNAVAILABLE",
    "GIT_WORKTREE_DIRTY_OR_UNSAFE",
    "GIT_SECRET_SCAN_BLOCK",
    "CARRIER_ADAPTER_FAILURE",
    "DAEMON_FAILURE",
    "ION_CORE_FAILURE",
]


def _resolve_root(root: str | Path | None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    return resolve_shell_root_from_ion_root(root)


def _sanitize_text(value: str) -> str:
    # Remove credentials embedded in URLs while preserving enough host/path
    # evidence to diagnose remote alignment.
    return re.sub(r"(https?://)[^/\s:@]+(?::[^/\s@]+)?@", r"\1***@", value)


def _run_git(args: list[str], cwd: Path, *, trim_stdout: bool = True) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            check=False,
        )
    except FileNotFoundError:
        return 127, "", "git command not found"
    except subprocess.TimeoutExpired:
        return 124, "", "git command timed out"
    stdout = proc.stdout.strip() if trim_stdout else proc.stdout
    return proc.returncode, _sanitize_text(stdout), _sanitize_text(proc.stderr.strip())


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _parse_registry_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"true", "yes", "1"}:
        return True
    if normalized in {"false", "no", "0"}:
        return False
    return None


def _registry_scalar(text: str, key: str) -> str | None:
    pattern = re.compile(rf"^\s*{re.escape(key)}:\s*(.*?)\s*$")
    for line in text.splitlines():
        match = pattern.match(line)
        if match:
            return match.group(1).strip().strip('"').strip("'")
    return None


def _load_registry(shell_root: Path) -> dict[str, Any]:
    path = shell_root / REQUIRED_OWNER_PATHS["data_plane_registry"]
    if not path.exists():
        return {"path": REQUIRED_OWNER_PATHS["data_plane_registry"], "exists": False}
    text = _read_text(path)
    return {
        "path": REQUIRED_OWNER_PATHS["data_plane_registry"],
        "exists": True,
        "active_branch": _registry_scalar(text, "active_branch"),
        "active_remote": _sanitize_text(_registry_scalar(text, "active_remote") or ""),
        "first_commit_pushed": _parse_registry_bool(_registry_scalar(text, "first_commit_pushed")),
        "setup_state": _registry_scalar(text, "setup_state"),
        "consolidation_artifact": _registry_scalar(text, "consolidation_artifact"),
    }


def _normalize_porcelain_path(raw_path: str) -> str:
    path = raw_path.strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1].strip()
    if len(path) >= 2 and path[0] == '"' and path[-1] == '"':
        path = path[1:-1]
    return path.replace('\\"', '"')


def _parse_porcelain(output: str) -> dict[str, Any]:
    staged: list[str] = []
    unstaged: list[str] = []
    untracked: list[str] = []
    conflicts: list[str] = []
    buckets: Counter[str] = Counter()

    for line in output.splitlines():
        if not line.strip():
            continue
        status = line[:2]
        path = _normalize_porcelain_path(line[3:] if len(line) > 3 else "")
        bucket = path.split("/", 1)[0] if "/" in path else (path.split("\\", 1)[0] if path else "(unknown)")
        buckets[bucket] += 1

        x, y = status[0], status[1]
        if status == "??":
            untracked.append(path)
            continue
        if x != " ":
            staged.append(path)
        if y != " ":
            unstaged.append(path)
        if x == "U" or y == "U" or status in {"AA", "DD"}:
            conflicts.append(path)

    return {
        "staged_count": len(staged),
        "unstaged_count": len(unstaged),
        "untracked_count": len(untracked),
        "conflict_count": len(conflicts),
        "worktree_clean": not staged and not unstaged and not untracked and not conflicts,
        "top_level_buckets": dict(buckets.most_common(12)),
        "samples": {
            "staged": staged[:20],
            "unstaged": unstaged[:20],
            "untracked": untracked[:20],
            "conflicts": conflicts[:20],
        },
    }


def _git_probe(shell_root: Path) -> dict[str, Any]:
    code, repo_root, err = _run_git(["rev-parse", "--show-toplevel"], shell_root)
    if code == 127:
        return {
            "git_command_available": False,
            "git_present": False,
            "failure_classification": "CARRIER_ADAPTER_FAILURE",
            "error": err,
        }
    if code != 0:
        return {
            "git_command_available": True,
            "git_present": False,
            "failure_classification": "GITHUB_DATA_PLANE_NOT_CONFIGURED",
            "error": err or "not a git repository",
        }

    code, branch, _ = _run_git(["branch", "--show-current"], shell_root)
    current_branch = branch if code == 0 and branch else "(detached)"

    code, head_commit, _ = _run_git(["rev-parse", "--verify", "HEAD"], shell_root)
    has_commits = code == 0 and bool(head_commit)
    if not has_commits:
        head_commit = None

    code, origin, _ = _run_git(["remote", "get-url", "origin"], shell_root)
    origin_url = origin if code == 0 and origin else None
    origin_contains_inline_credentials = bool(origin_url and re.search(r"^https?://\*\*\*@", origin_url))

    code, upstream, _ = _run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], shell_root)
    upstream_value = upstream if code == 0 and upstream else None
    ahead = 0
    behind = 0
    if upstream_value:
        code, counts, _ = _run_git(["rev-list", "--left-right", "--count", f"{upstream_value}...HEAD"], shell_root)
        if code == 0 and counts:
            parts = counts.split()
            if len(parts) == 2 and all(part.isdigit() for part in parts):
                behind = int(parts[0])
                ahead = int(parts[1])

    code, porcelain, status_err = _run_git(["status", "--porcelain"], shell_root, trim_stdout=False)
    status_summary = _parse_porcelain(porcelain if code == 0 else "")

    return {
        "git_command_available": True,
        "git_present": True,
        "repo_root": repo_root,
        "shell_root_is_repo_root": Path(repo_root).resolve() == shell_root.resolve(),
        "current_branch": current_branch,
        "head_commit": head_commit,
        "has_commits": has_commits,
        "origin_url": origin_url,
        "origin_configured": bool(origin_url),
        "origin_contains_inline_credentials": origin_contains_inline_credentials,
        "upstream": upstream_value,
        "ahead": ahead,
        "behind": behind,
        "status_error": status_err if code != 0 else None,
        "worktree": status_summary,
    }


def audit_github_data_plane(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    findings: list[str] = []
    warnings: list[str] = []

    owner_paths: dict[str, dict[str, Any]] = {}
    for label, rel in REQUIRED_OWNER_PATHS.items():
        exists = (shell_root / rel).exists()
        owner_paths[label] = {"path": rel, "exists": exists}
        if not exists:
            findings.append(f"missing_owner_surface:{label}:{rel}")

    registry = _load_registry(shell_root)
    git = _git_probe(shell_root)

    if not git.get("git_present"):
        findings.append("git_not_configured_at_shell_root")
    if git.get("origin_contains_inline_credentials"):
        findings.append("origin_url_contains_inline_credentials")
    if git.get("git_present") and not git.get("shell_root_is_repo_root"):
        findings.append("git_repo_root_mismatch")
    if git.get("git_present") and not git.get("origin_configured"):
        findings.append("origin_remote_missing")

    expected_branch = registry.get("active_branch") or "main"
    active_remote = registry.get("active_remote") or ""
    remote_alignment = "NOT_EVALUATED"
    branch_alignment = "NOT_EVALUATED"
    if git.get("git_present"):
        branch_alignment = "MATCHES_REGISTRY" if git.get("current_branch") == expected_branch else "MISMATCH"
        if branch_alignment == "MISMATCH":
            findings.append("active_branch_mismatch")

        origin_url = git.get("origin_url")
        if origin_url:
            remote_alignment = (
                "MATCHES_REGISTRY"
                if origin_url == active_remote or origin_url in EXPECTED_REMOTE_URLS
                else "MISMATCH"
            )
            if remote_alignment == "MISMATCH":
                findings.append("active_remote_mismatch")
        else:
            remote_alignment = "MISSING"

        if git.get("worktree", {}).get("conflict_count", 0):
            findings.append("worktree_conflicts_present")
        if not git.get("has_commits"):
            warnings.append("no_local_commits_yet")
        if git.get("upstream") is None:
            warnings.append("no_upstream_tracking_branch")

    first_commit_pushed = registry.get("first_commit_pushed")
    if first_commit_pushed is True:
        first_commit_status = "REGISTRY_SAYS_PUSHED_NOT_NETWORK_VERIFIED"
    elif git.get("has_commits"):
        first_commit_status = "LOCAL_COMMITS_PRESENT_PUSH_NOT_VERIFIED"
    else:
        first_commit_status = "NO_LOCAL_COMMITS_YET"

    readiness_blockers: list[str] = []
    if not git.get("git_present"):
        readiness_blockers.append("git_not_configured")
    if git.get("git_present") and not git.get("origin_configured"):
        readiness_blockers.append("origin_remote_missing")
    if branch_alignment == "MISMATCH":
        readiness_blockers.append("active_branch_mismatch")
    if remote_alignment == "MISMATCH":
        readiness_blockers.append("active_remote_mismatch")
    if git.get("worktree", {}).get("conflict_count", 0):
        readiness_blockers.append("worktree_conflicts_present")

    first_commit_readiness = {
        "can_prepare_human_review_commit": not readiness_blockers,
        "commit_allowed_by_audit": False,
        "push_allowed_by_audit": False,
        "first_commit_status": first_commit_status,
        "blockers": readiness_blockers,
        "required_runtime_policy_gates": [
            "ion_runtime_git_push_authority_profile",
            "stage_exact_paths",
            "review_staged_diff",
            "run_validation",
            "run_secret_scan",
            "record_action_receipt",
            "declare_rollback_path",
            "authorize_commit_or_push_by_ion_policy",
        ],
        "push_branch_policy": {
            "main_auto_push_allowed": False,
            "main_update_path": "pull_request_or_merge_gate",
            "default_allowed_push_branch_patterns": DEFAULT_ALLOWED_PUSH_BRANCH_PATTERNS,
        },
        "human_gate_posture": "BOOTSTRAP_OR_BREAK_GLASS_ONLY_NOT_PER_PUSH_FINAL_LAW",
    }

    failure_classification = None
    if findings:
        if any(finding == "git_not_configured_at_shell_root" for finding in findings):
            failure_classification = "GITHUB_DATA_PLANE_NOT_CONFIGURED"
        elif any(finding == "worktree_conflicts_present" for finding in findings):
            failure_classification = "GIT_WORKTREE_DIRTY_OR_UNSAFE"
        elif any(finding.startswith("missing_owner_surface") for finding in findings):
            failure_classification = "ION_CORE_FAILURE"
        else:
            failure_classification = "CARRIER_ADAPTER_FAILURE"

    accepted = not findings
    return {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT if accepted else BLOCKED_VERDICT,
        "accepted": accepted,
        "root": str(shell_root),
        "owner_paths": owner_paths,
        "registry": registry,
        "git": git,
        "registry_alignment": {
            "expected_branch": expected_branch,
            "branch_alignment": branch_alignment,
            "expected_remote": active_remote,
            "remote_alignment": remote_alignment,
            "setup_state": registry.get("setup_state"),
            "first_commit_pushed": first_commit_pushed,
        },
        "first_commit_readiness": first_commit_readiness,
        "failure_classes": FAILURE_CLASSES,
        "failure_classification": failure_classification,
        "findings": findings,
        "warnings": warnings,
        "network_access_used": False,
        "github_mutation_performed": False,
        "git_mutation_performed": False,
        "commit_authority": False,
        "push_authority": False,
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ION GitHub data-plane readiness without mutating git or GitHub.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = audit_github_data_plane(args.ion_root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
