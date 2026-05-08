"""Commit proposal receipt for the ION GitHub data plane.

This module is intentionally non-authorizing. It does not stage, commit, push,
or mutate GitHub. It writes review evidence that a later ION git capability can
use as a gate input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_github_data_plane_audit import audit_github_data_plane

SCHEMA_ID = "ion.github_commit_proposal_receipt.v1"
READY_VERDICT = "ION_GITHUB_COMMIT_PROPOSAL_READY_FOR_REVIEW"
BLOCKED_VERDICT = "ION_GITHUB_COMMIT_PROPOSAL_BLOCKED"

BASE_DIR = Path("ION/05_context/current/github_data_plane")
PROPOSALS_DIR = BASE_DIR / "commit_proposals"

DEFAULT_COMMIT_MESSAGE = "Initialize ION Codex data plane"
DEFAULT_VALIDATION_COMMANDS = [
    [
        "python3",
        "-m",
        "pytest",
        "ION/tests",
        "-q",
    ],
    [
        "python3",
        "-S",
        "-m",
        "kernel.ion_status",
        "--ion-root",
        ".",
        "--json",
    ],
]

FAILURE_CLASSES = [
    "GITHUB_DATA_PLANE_NOT_CONFIGURED",
    "GIT_WORKTREE_DIRTY_OR_UNSAFE",
    "GIT_SECRET_SCAN_BLOCK",
    "GIT_VALIDATION_BLOCK",
    "CARRIER_ADAPTER_FAILURE",
    "ION_CORE_FAILURE",
]

SECRET_PATTERNS = [
    ("github_token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("openai_project_key", re.compile(r"\bsk-proj-[A-Za-z0-9_-]{20,}\b")),
    ("openai_secret_key", re.compile(r"\bsk-[A-Za-z0-9]{32,}\b")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----")),
    (
        "api_key_assignment",
        re.compile(r"\b(?:OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|GH_TOKEN|API[_-]?KEY)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}", re.IGNORECASE),
    ),
]

PLACEHOLDER_TOKENS = ("...", "<", "example", "placeholder", "redacted", "your_", "xxx")
SKIP_DIR_PARTS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
SKIP_SUFFIXES = {".zip", ".tar", ".gz", ".tgz", ".7z", ".pyc", ".pyo", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf"}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_stamp(value: str) -> str:
    return value.replace(":", "").replace("+00:00", "Z").replace("+", "Z")


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:96] or "commit_proposal"


def _resolve_root(root: str | Path | None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    return resolve_shell_root_from_ion_root(root)


def _repo_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run_git(root: Path, args: list[str], *, trim_stdout: bool = True) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
            check=False,
        )
    except FileNotFoundError:
        return 127, "", "git command not found"
    except subprocess.TimeoutExpired:
        return 124, "", "git command timed out"
    stdout = proc.stdout.strip() if trim_stdout else proc.stdout
    return proc.returncode, stdout, proc.stderr.strip()


def _git_path_set(root: Path) -> tuple[list[str], dict[str, Any]]:
    code, output, error = _run_git(root, ["ls-files", "--cached", "--modified", "--others", "--exclude-standard"], trim_stdout=False)
    if code != 0:
        return [], {"ok": False, "finding": "git_ls_files_failed", "error": error}
    paths = sorted({line.strip() for line in output.splitlines() if line.strip()})
    return paths, {"ok": True, "source": "git ls-files --cached --modified --others --exclude-standard"}


def _path_bucket_counts(paths: list[str]) -> dict[str, int]:
    buckets = Counter(path.split("/", 1)[0] if "/" in path else path for path in paths)
    return dict(buckets.most_common(24))


def _is_scannable_path(path: str) -> bool:
    rel = Path(path)
    if any(part in SKIP_DIR_PARTS for part in rel.parts):
        return False
    return rel.suffix.lower() not in SKIP_SUFFIXES


def _is_placeholder_secret_line(line: str) -> bool:
    lowered = line.lower()
    return any(token in lowered for token in PLACEHOLDER_TOKENS)


def _redacted_finding(path: str, line_number: int, label: str) -> dict[str, Any]:
    return {
        "path": path,
        "line": line_number,
        "pattern": label,
        "excerpt": f"<redacted:{label}>",
    }


def scan_candidate_paths_for_secrets(root: Path, paths: list[str]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    scanned_count = 0
    skipped_count = 0
    for rel in paths:
        if not _is_scannable_path(rel):
            skipped_count += 1
            continue
        path = root / rel
        if not path.is_file() or path.is_symlink():
            skipped_count += 1
            continue
        try:
            raw = path.read_bytes()
        except OSError:
            skipped_count += 1
            continue
        if b"\x00" in raw[:4096]:
            skipped_count += 1
            continue
        text = raw.decode("utf-8", errors="replace")
        scanned_count += 1
        for line_number, line in enumerate(text.splitlines(), start=1):
            if _is_placeholder_secret_line(line):
                continue
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append(_redacted_finding(rel, line_number, label))
    return {
        "schema_id": "ion.git_secret_scan_result.v1",
        "accepted": not findings,
        "scanned_file_count": scanned_count,
        "skipped_file_count": skipped_count,
        "finding_count": len(findings),
        "findings": findings[:100],
        "findings_truncated": len(findings) > 100,
        "secret_values_redacted": True,
    }


def _run_validation(root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    env = os.environ.copy()
    packages = str(root / "ION/04_packages")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    env["PYTHONPATH"] = f"{packages}:{env.get('PYTHONPATH', '')}" if env.get("PYTHONPATH") else packages
    for command in DEFAULT_VALIDATION_COMMANDS:
        try:
            proc = subprocess.run(
                command,
                cwd=root,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=120,
                check=False,
                env=env,
            )
            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()
            results.append({
                "command": command,
                "returncode": proc.returncode,
                "passed": proc.returncode == 0,
                "stdout_tail": stdout[-4000:],
                "stderr_tail": stderr[-2000:],
            })
        except subprocess.TimeoutExpired as exc:
            results.append({
                "command": command,
                "returncode": 124,
                "passed": False,
                "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
                "stderr_tail": "validation command timed out",
            })
    return results


def build_github_commit_proposal_receipt(
    root: str | Path | None = None,
    *,
    action_id: str = "initial-github-data-plane-load",
    commit_message: str = DEFAULT_COMMIT_MESSAGE,
    write: bool = False,
    run_validation: bool = False,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    created_at = _now()
    proposal_id = f"github_commit_proposal_{_safe_stamp(created_at)}_{_safe_slug(action_id)}"
    proposal_rel = (PROPOSALS_DIR / f"{proposal_id}.json").as_posix()
    manifest_rel = (PROPOSALS_DIR / f"{proposal_id}.paths.json").as_posix()

    audit = audit_github_data_plane(shell_root)
    paths, path_source = _git_path_set(shell_root)
    for rel in (proposal_rel, manifest_rel):
        if rel not in paths:
            paths.append(rel)
    paths = sorted(set(paths))

    path_manifest = {
        "schema_id": "ion.github_commit_path_manifest.v1",
        "proposal_id": proposal_id,
        "created_at": created_at,
        "path_count": len(paths),
        "paths": paths,
    }
    path_bucket_counts = _path_bucket_counts(paths)
    secret_scan = scan_candidate_paths_for_secrets(shell_root, paths)
    validations = _run_validation(shell_root) if run_validation else []
    validation_passed = bool(validations) and all(item.get("passed") for item in validations)

    findings: list[str] = []
    if not audit.get("accepted"):
        findings.append("github_data_plane_audit_not_accepted")
    if not path_source.get("ok"):
        findings.append("path_set_collection_failed")
    if not paths:
        findings.append("empty_path_set")
    if not secret_scan.get("accepted"):
        findings.append("secret_scan_block")
    if run_validation and not validation_passed:
        findings.append("validation_block")

    if not audit.get("accepted"):
        failure_classification = audit.get("failure_classification") or "GITHUB_DATA_PLANE_NOT_CONFIGURED"
    elif not secret_scan.get("accepted"):
        failure_classification = "GIT_SECRET_SCAN_BLOCK"
    elif run_validation and not validation_passed:
        failure_classification = "GIT_VALIDATION_BLOCK"
    elif findings:
        failure_classification = "CARRIER_ADAPTER_FAILURE"
    else:
        failure_classification = None

    proposal = {
        "schema_id": SCHEMA_ID,
        "proposal_id": proposal_id,
        "action_id": action_id,
        "created_at": created_at,
        "root": shell_root.as_posix(),
        "status": "ready_for_review" if not findings else "blocked",
        "verdict": READY_VERDICT if not findings else BLOCKED_VERDICT,
        "commit_message": commit_message,
        "target_remote": (audit.get("git") or {}).get("origin_url"),
        "target_branch": (audit.get("git") or {}).get("current_branch"),
        "path_source": path_source,
        "path_manifest_path": manifest_rel,
        "path_count": len(paths),
        "path_bucket_counts": path_bucket_counts,
        "path_samples": paths[:40],
        "secret_scan": secret_scan,
        "validation": {
            "run_validation": run_validation,
            "passed": validation_passed if run_validation else None,
            "commands": validations,
        },
        "audit_summary": {
            "verdict": audit.get("verdict"),
            "accepted": audit.get("accepted"),
            "findings": audit.get("findings"),
            "warnings": audit.get("warnings"),
            "first_commit_status": (audit.get("first_commit_readiness") or {}).get("first_commit_status"),
            "can_prepare_human_review_commit": (audit.get("first_commit_readiness") or {}).get("can_prepare_human_review_commit"),
        },
        "rollback": {
            "pre_push": "No rollback needed before commit/push; no git or GitHub mutation is performed by this proposal.",
            "post_commit_before_push": "Use git reset --soft HEAD~1 only under explicit human/ION gate; do not run automatically.",
            "post_push": "Use git revert <commit> on a follow-up branch/PR unless explicit emergency rollback authority is mounted.",
        },
        "policy": {
            "commit_authority": False,
            "push_authority": False,
            "main_auto_push_allowed": False,
            "main_update_path": "pull_request_or_merge_gate_or_explicit_bootstrap_exception",
            "requires_before_commit_or_push": [
                "review_this_proposal_receipt",
                "review_path_manifest",
                "review_secret_scan",
                "review_validation_results",
                "record_approval_or_runtime_policy_gate",
            ],
        },
        "findings": findings,
        "failure_classification": failure_classification,
        "failure_classes": FAILURE_CLASSES,
        "network_access_used": False,
        "git_mutation_performed": False,
        "github_mutation_performed": False,
        "production_authority": False,
        "live_execution_authority": False,
    }

    if write:
        manifest_path = shell_root / manifest_rel
        proposal_path = shell_root / proposal_rel
        _write_json(manifest_path, path_manifest)
        proposal["path_manifest_sha256"] = _sha256_file(manifest_path)
        _write_json(proposal_path, proposal)
        proposal["proposal_path"] = proposal_rel
        proposal["proposal_sha256"] = _sha256_file(proposal_path)
        _write_json(proposal_path, proposal)
    return proposal


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a non-authorizing ION GitHub commit proposal receipt.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--action-id", default="initial-github-data-plane-load")
    parser.add_argument("--commit-message", default=DEFAULT_COMMIT_MESSAGE)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--run-validation", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = build_github_commit_proposal_receipt(
        args.ion_root,
        action_id=args.action_id,
        commit_message=args.commit_message,
        write=args.write,
        run_validation=args.run_validation,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        if result.get("proposal_path"):
            print(result["proposal_path"])
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["verdict"] == READY_VERDICT else 1


if __name__ == "__main__":
    raise SystemExit(main())
