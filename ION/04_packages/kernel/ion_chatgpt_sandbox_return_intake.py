"""ChatGPT sandbox return intake.

This owner receives review material produced by Sev/ChatGPT Browser in a
sandbox. It never applies patches to source. Sandbox output lands as inbox
evidence, receives receipts, and can queue a bounded Codex review packet.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import resolve_shell_root_from_ion_root

SCHEMA_ID = "ion.chatgpt_sandbox_return_intake.v1"
MANIFEST_SCHEMA_ID = "ion.chatgpt_sandbox_return.v1"
QUEUE_SCHEMA_ID = "ion.chatgpt_sandbox_return_queue.v1"
RECEIPT_SCHEMA_ID = "ion.chatgpt_sandbox_return_receipt.v1"
READY_VERDICT = "ION_CHATGPT_SANDBOX_RETURN_INTAKE_READY"
BLOCKED_VERDICT = "ION_CHATGPT_SANDBOX_RETURN_INTAKE_BLOCKED"

INBOX_ROOT = Path("ION/05_context/inbox/chatgpt_sandbox_returns")
ACTIVE_QUEUE_PATH = Path("ION/05_context/current/ACTIVE_CHATGPT_SANDBOX_RETURN_QUEUE.json")
RECEIPTS_DIR = Path("ION/05_context/current/chatgpt_sandbox_returns/receipts")

REQUIRED_MARKERS = ("pyproject.toml", "ION/REPO_AUTHORITY.md")
RETURN_ID_RE = re.compile(r"^sev-\d{8}-\d{6}-[a-z0-9][a-z0-9_-]{1,80}$")
PROTECTED_PATH_TOKENS = (
    "/.git/",
    ".env",
    "secret",
    "token",
    "credential",
    "vault",
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:96] or "sandbox_return"


def _resolve_root(root: str | Path | None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    return resolve_shell_root_from_ion_root(root)


def _repo_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _return_root(root: Path, return_id: str) -> Path:
    return root / INBOX_ROOT / return_id


def _has_protected_token(rel: str) -> bool:
    lowered = f"/{rel.lower()}"
    return any(token in lowered for token in PROTECTED_PATH_TOKENS)


def _validate_repo_rel_value(value: str, *, allow_files_overlay: bool = False) -> str | None:
    rel = value.replace("\\", "/").strip()
    if not rel:
        return "path_required"
    if rel.startswith("/") or rel.startswith("../") or "/../" in rel or rel.endswith("/.."):
        return "path_escape"
    if _has_protected_token(rel):
        return "protected_path_token"
    if allow_files_overlay:
        return None
    if rel.startswith("files/"):
        return "files_overlay_prefix_not_allowed_here"
    return None


def _safe_return_file_path(root: Path, return_id: str, rel_path: str) -> tuple[Path | None, str | None]:
    finding = _validate_repo_rel_value(rel_path, allow_files_overlay=True)
    if finding:
        return None, finding
    base = _return_root(root, return_id).resolve()
    target = (base / rel_path).resolve()
    try:
        target.relative_to(base)
    except ValueError:
        return None, "path_escape"
    return target, None


def _queue_default() -> dict[str, Any]:
    return {
        "schema_id": QUEUE_SCHEMA_ID,
        "created_at": _now(),
        "updated_at": _now(),
        "return_count": 0,
        "returns": [],
        "production_authority": False,
        "live_execution_authority": False,
    }


def _load_queue(root: Path) -> dict[str, Any]:
    queue = _read_json(root / ACTIVE_QUEUE_PATH)
    if not queue:
        return _queue_default()
    if not isinstance(queue.get("returns"), list):
        queue["returns"] = []
    return queue


def _write_queue(root: Path, queue: Mapping[str, Any]) -> str:
    payload = dict(queue)
    payload["updated_at"] = _now()
    payload["return_count"] = len(payload.get("returns") or [])
    _write_json(root / ACTIVE_QUEUE_PATH, payload)
    return ACTIVE_QUEUE_PATH.as_posix()


def _upsert_queue_item(root: Path, return_id: str, update: Mapping[str, Any]) -> str:
    queue = _load_queue(root)
    returns = [item for item in queue.get("returns", []) if isinstance(item, dict)]
    existing = next((item for item in returns if item.get("return_id") == return_id), None)
    if existing is None:
        existing = {
            "return_id": return_id,
            "created_at": _now(),
            "status": "RETURN_DRAFT_WRITTEN",
        }
        returns.append(existing)
    existing.update(dict(update))
    existing["updated_at"] = _now()
    queue["returns"] = returns
    return _write_queue(root, queue)


def _write_receipt(
    root: Path,
    *,
    operation: str,
    return_id: str,
    status: str,
    result: Mapping[str, Any],
    files_touched: list[str] | None = None,
    failure_classification: str | None = None,
) -> str:
    receipt_id = f"sandbox_return_receipt_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{_safe_slug(return_id)}_{_safe_slug(operation)}"
    receipt = {
        "schema_id": RECEIPT_SCHEMA_ID,
        "receipt_id": receipt_id,
        "return_id": return_id,
        "operation": operation,
        "created_at": _now(),
        "actor": {
            "callsign": "Sev",
            "carrier": "chatgpt_browser",
            "sandbox": True,
        },
        "human_sovereign": "Braden",
        "status": status,
        "files_touched": list(files_touched or []),
        "validation": {"result": dict(result)},
        "failure_classification": failure_classification,
        "production_authority": False,
        "live_execution_authority": False,
        "direct_apply_authority": False,
        "git_push_authority": False,
    }
    path = root / RECEIPTS_DIR / f"{_safe_slug(receipt_id)}.json"
    _write_json(path, receipt)
    return _repo_rel(path, root)


def _normalize_manifest(packet: Mapping[str, Any]) -> dict[str, Any]:
    manifest = dict(packet.get("manifest")) if isinstance(packet.get("manifest"), Mapping) else {}
    return_id = str(packet.get("return_id") or manifest.get("return_id") or "").strip()
    source_snapshot = manifest.get("source_snapshot") if isinstance(manifest.get("source_snapshot"), Mapping) else {}
    if isinstance(packet.get("source_snapshot"), Mapping):
        source_snapshot = {**source_snapshot, **dict(packet["source_snapshot"])}
    base_assumptions = manifest.get("base_assumptions") if isinstance(manifest.get("base_assumptions"), Mapping) else {}
    changed_paths = packet.get("changed_paths", manifest.get("changed_paths", []))
    sandbox_validation = packet.get("sandbox_validation", manifest.get("sandbox_validation", {}))
    return {
        "schema_id": MANIFEST_SCHEMA_ID,
        "return_id": return_id,
        "created_at": str(manifest.get("created_at") or packet.get("created_at") or _now()),
        "authoring_carrier": {
            "callsign": "Sev",
            "carrier": "chatgpt_browser",
            "sandbox": True,
        },
        "human_sovereign": "Braden",
        "source_snapshot": {
            "package_path_seen_by_chatgpt": source_snapshot.get("package_path_seen_by_chatgpt"),
            "package_sha256": source_snapshot.get("package_sha256", "unknown-unless-provided-or-computed"),
            "archive_root_confirmed": source_snapshot.get("archive_root_confirmed") is True,
            "expected_root_markers": list(source_snapshot.get("expected_root_markers") or REQUIRED_MARKERS),
        },
        "base_assumptions": {
            "production_authority": base_assumptions.get("production_authority") is True,
            "live_execution_authority": base_assumptions.get("live_execution_authority") is True,
            "direct_apply_authority": base_assumptions.get("direct_apply_authority") is True,
            "git_push_authority": base_assumptions.get("git_push_authority") is True,
        },
        "changed_paths": list(changed_paths or []),
        "intended_review_commands": list(
            packet.get(
                "intended_review_commands",
                manifest.get(
                    "intended_review_commands",
                    [
                        f"git apply --check {INBOX_ROOT.as_posix()}/{return_id}/PATCH.diff",
                        "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests -q -p no:cacheprovider",
                    ],
                ),
            )
            or []
        ),
        "sandbox_validation": dict(sandbox_validation) if isinstance(sandbox_validation, Mapping) else {},
        "receipts_requested": list(
            packet.get(
                "receipts_requested",
                manifest.get(
                    "receipts_requested",
                    [
                        "sandbox_return_intake_receipt",
                        "sha256_receipt",
                        "diff_preview_receipt",
                        "codex_review_packet_receipt",
                    ],
                ),
            )
            or []
        ),
    }


def validate_sandbox_return_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    findings: list[str] = []
    warnings: list[str] = []
    if manifest.get("schema_id") != MANIFEST_SCHEMA_ID:
        findings.append("schema_id_must_be_ion_chatgpt_sandbox_return_v1")
    return_id = str(manifest.get("return_id") or "").strip()
    if not RETURN_ID_RE.match(return_id):
        findings.append("return_id_must_match_sev_yyyymmdd_hhmmss_slug")
    carrier = manifest.get("authoring_carrier") if isinstance(manifest.get("authoring_carrier"), Mapping) else {}
    if carrier.get("callsign") != "Sev":
        findings.append("authoring_carrier_callsign_must_be_Sev")
    if carrier.get("carrier") != "chatgpt_browser":
        findings.append("authoring_carrier_must_be_chatgpt_browser")
    if carrier.get("sandbox") is not True:
        findings.append("authoring_carrier_sandbox_must_be_true")
    if manifest.get("human_sovereign") != "Braden":
        findings.append("human_sovereign_must_be_Braden")
    snapshot = manifest.get("source_snapshot") if isinstance(manifest.get("source_snapshot"), Mapping) else {}
    if snapshot.get("archive_root_confirmed") is not True:
        findings.append("archive_root_confirmed_must_be_true")
    markers = set(snapshot.get("expected_root_markers") or [])
    for marker in REQUIRED_MARKERS:
        if marker not in markers:
            findings.append(f"expected_root_marker_missing:{marker}")
    assumptions = manifest.get("base_assumptions") if isinstance(manifest.get("base_assumptions"), Mapping) else {}
    for key in ("production_authority", "live_execution_authority", "direct_apply_authority", "git_push_authority"):
        if assumptions.get(key) is not False:
            findings.append(f"{key}_must_be_false")
    changed_paths = manifest.get("changed_paths")
    if not isinstance(changed_paths, list):
        findings.append("changed_paths_must_be_list")
    else:
        for rel in changed_paths:
            if not isinstance(rel, str):
                findings.append("changed_path_must_be_string")
                continue
            finding = _validate_repo_rel_value(rel)
            if finding:
                findings.append(f"changed_path_{finding}:{rel}")
    if not manifest.get("receipts_requested"):
        warnings.append("receipts_requested_empty")
    return {
        "schema_id": "ion.chatgpt_sandbox_return_manifest_validation.v1",
        "accepted": not findings,
        "return_id": return_id or None,
        "findings": findings,
        "warnings": warnings,
        "production_authority": False,
        "live_execution_authority": False,
        "direct_apply_authority": False,
        "git_push_authority": False,
    }


def register_sandbox_return(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    manifest = _normalize_manifest(packet)
    validation = validate_sandbox_return_manifest(manifest)
    return_id = str(manifest.get("return_id") or "invalid_sandbox_return")
    summary = str(packet.get("summary_text") or packet.get("summary") or "").strip()
    if not summary:
        validation["accepted"] = False
        validation["findings"].append("summary_text_required")
    target_root = _return_root(shell_root, return_id)
    if target_root.exists():
        validation["accepted"] = False
        validation["findings"].append("return_id_already_exists")
    if not validation["accepted"]:
        receipt_path = _write_receipt(
            shell_root,
            operation="register",
            return_id=return_id,
            status="rejected",
            result=validation,
            failure_classification="POLICY_BLOCK_WORKING_AS_DESIGNED",
        )
        return {
            "schema_id": "ion.chatgpt_sandbox_return_register_result.v1",
            "ok": False,
            "verdict": BLOCKED_VERDICT,
            "finding": "validation_failed",
            "validation": validation,
            "receipt_path": receipt_path,
            "production_authority": False,
            "live_execution_authority": False,
        }
    target_root.mkdir(parents=True, exist_ok=False)
    manifest_path = target_root / "SANDBOX_RETURN_MANIFEST.json"
    summary_path = target_root / "SUMMARY.md"
    _write_json(manifest_path, manifest)
    summary_path.write_text(summary + "\n", encoding="utf-8")
    files = [_repo_rel(manifest_path, shell_root), _repo_rel(summary_path, shell_root)]
    queue_path = _upsert_queue_item(
        shell_root,
        return_id,
        {
            "status": "RETURN_DRAFT_WRITTEN",
            "return_root": _repo_rel(target_root, shell_root),
            "manifest_path": files[0],
            "summary_path": files[1],
            "changed_path_count": len(manifest.get("changed_paths") or []),
            "blocked_findings": [],
        },
    )
    result = {
        "ok": True,
        "return_id": return_id,
        "return_root": _repo_rel(target_root, shell_root),
        "manifest_path": files[0],
        "summary_path": files[1],
        "queue_path": queue_path,
        "sha256": {rel: _sha256_file(shell_root / rel) for rel in files},
    }
    receipt_path = _write_receipt(shell_root, operation="register", return_id=return_id, status="completed", result=result, files_touched=files + [queue_path])
    _upsert_queue_item(shell_root, return_id, {"latest_receipt_path": receipt_path})
    return {
        "schema_id": "ion.chatgpt_sandbox_return_register_result.v1",
        "ok": True,
        "verdict": READY_VERDICT,
        "receipt_path": receipt_path,
        **result,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _return_is_committed(root: Path, return_id: str) -> bool:
    return (_return_root(root, return_id) / "RETURN_COMMITTED.json").exists()


def write_sandbox_return_file(root: str | Path | None, return_id: str, rel_path: str, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    base = _return_root(shell_root, return_id)
    target, finding = _safe_return_file_path(shell_root, return_id, rel_path)
    if finding or target is None:
        result = {"ok": False, "finding": finding}
    elif not base.exists():
        result = {"ok": False, "finding": "return_id_not_registered"}
    elif _return_is_committed(shell_root, return_id):
        result = {"ok": False, "finding": "return_is_committed_immutable"}
    elif target.exists():
        result = {"ok": False, "finding": "target_exists_overwrite_false"}
    else:
        content = packet.get("content") if isinstance(packet.get("content"), Mapping) else {}
        if "content_b64" in packet:
            data = base64.b64decode(str(packet.get("content_b64") or ""), validate=True)
        else:
            text = str(packet.get("text") if "text" in packet else content.get("text") or "")
            data = text.encode(str(content.get("encoding") or packet.get("encoding") or "utf-8"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        rel = _repo_rel(target, shell_root)
        result = {"ok": True, "path": rel, "sha256": _sha256_bytes(data), "bytes": len(data)}
    status = "completed" if result.get("ok") else "failed"
    files = [result["path"]] if result.get("ok") else []
    receipt_path = _write_receipt(
        shell_root,
        operation="file",
        return_id=return_id,
        status=status,
        result=result,
        files_touched=files,
        failure_classification=None if result.get("ok") else "POLICY_BLOCK_WORKING_AS_DESIGNED",
    )
    if result.get("ok"):
        _upsert_queue_item(shell_root, return_id, {"status": "RETURN_DRAFT_WRITTEN", "latest_receipt_path": receipt_path})
    return {
        "schema_id": "ion.chatgpt_sandbox_return_file_result.v1",
        "verdict": READY_VERDICT if result.get("ok") else BLOCKED_VERDICT,
        "receipt_path": receipt_path,
        **result,
        "production_authority": False,
        "live_execution_authority": False,
    }


def commit_sandbox_return(root: str | Path | None, return_id: str) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    base = _return_root(shell_root, return_id)
    findings: list[str] = []
    if not base.exists():
        findings.append("return_id_not_registered")
    if _return_is_committed(shell_root, return_id):
        findings.append("return_already_committed")
    manifest_path = base / "SANDBOX_RETURN_MANIFEST.json"
    summary_path = base / "SUMMARY.md"
    if not manifest_path.exists():
        findings.append("manifest_missing")
    if not summary_path.exists():
        findings.append("summary_missing")
    manifest = _read_json(manifest_path) or {}
    validation = validate_sandbox_return_manifest(manifest) if manifest else {"accepted": False, "findings": ["manifest_missing"], "warnings": []}
    if not validation.get("accepted"):
        findings.extend([f"manifest:{finding}" for finding in validation.get("findings", [])])
    if findings:
        result = {"ok": False, "return_id": return_id, "findings": findings}
        receipt_path = _write_receipt(
            shell_root,
            operation="commit",
            return_id=return_id,
            status="failed",
            result=result,
            failure_classification="POLICY_BLOCK_WORKING_AS_DESIGNED",
        )
        return {"schema_id": "ion.chatgpt_sandbox_return_commit_result.v1", "ok": False, "verdict": BLOCKED_VERDICT, "receipt_path": receipt_path, **result}
    files = sorted(path for path in base.rglob("*") if path.is_file())
    file_refs = [
        {
            "path": _repo_rel(path, shell_root),
            "sha256": _sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for path in files
    ]
    commit_marker = base / "RETURN_COMMITTED.json"
    commit_payload = {
        "schema_id": "ion.chatgpt_sandbox_return_commit.v1",
        "return_id": return_id,
        "committed_at": _now(),
        "status": "RETURN_COMMITTED_FOR_REVIEW",
        "file_count": len(file_refs),
        "files": file_refs,
        "production_authority": False,
        "live_execution_authority": False,
        "direct_apply_authority": False,
        "git_push_authority": False,
    }
    _write_json(commit_marker, commit_payload)
    marker_rel = _repo_rel(commit_marker, shell_root)
    result = {
        "ok": True,
        "return_id": return_id,
        "status": "RETURN_COMMITTED_FOR_REVIEW",
        "return_root": _repo_rel(base, shell_root),
        "commit_marker_path": marker_rel,
        "file_count": len(file_refs),
        "patch_path": _repo_rel(base / "PATCH.diff", shell_root) if (base / "PATCH.diff").exists() else None,
    }
    receipt_path = _write_receipt(shell_root, operation="commit", return_id=return_id, status="completed", result=result, files_touched=[marker_rel])
    _upsert_queue_item(shell_root, return_id, {**result, "latest_receipt_path": receipt_path})
    return {"schema_id": "ion.chatgpt_sandbox_return_commit_result.v1", "verdict": READY_VERDICT, "receipt_path": receipt_path, **result}


def _patch_changed_paths(patch_text: str) -> list[str]:
    paths: list[str] = []
    for line in patch_text.splitlines():
        if line.startswith("+++ b/"):
            rel = line[len("+++ b/"):].strip()
            if rel != "/dev/null" and rel not in paths:
                paths.append(rel)
    return paths


def _run_git_apply(root: Path, patch_path: Path, arg: str) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            ["git", "apply", arg, patch_path.as_posix()],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
        return {
            "available": True,
            "returncode": completed.returncode,
            "stdout": completed.stdout[-4000:],
            "stderr": completed.stderr[-4000:],
        }
    except Exception as exc:  # pragma: no cover - depends on host git
        return {"available": False, "error": str(exc)}


def build_sandbox_return_diff_preview(root: str | Path | None, return_id: str) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    base = _return_root(shell_root, return_id)
    patch_path = base / "PATCH.diff"
    if not patch_path.exists():
        result = {"ok": False, "return_id": return_id, "finding": "patch_diff_missing"}
        receipt_path = _write_receipt(shell_root, operation="diff_preview", return_id=return_id, status="failed", result=result, failure_classification="POLICY_BLOCK_WORKING_AS_DESIGNED")
        return {"schema_id": "ion.chatgpt_sandbox_return_diff_preview_result.v1", "verdict": BLOCKED_VERDICT, "receipt_path": receipt_path, **result}
    patch_text = patch_path.read_text(encoding="utf-8", errors="replace")
    changed_paths = _patch_changed_paths(patch_text)
    blocked_findings = [f"changed_path_{finding}:{rel}" for rel in changed_paths if (finding := _validate_repo_rel_value(rel))]
    check = _run_git_apply(shell_root, patch_path, "--check")
    stat = _run_git_apply(shell_root, patch_path, "--stat")
    preview = {
        "schema_id": "ion.chatgpt_sandbox_return_diff_preview.v1",
        "return_id": return_id,
        "created_at": _now(),
        "patch_path": _repo_rel(patch_path, shell_root),
        "changed_paths": changed_paths,
        "changed_path_count": len(changed_paths),
        "line_count": len(patch_text.splitlines()),
        "git_apply_check": check,
        "git_apply_stat": stat,
        "blocked_findings": blocked_findings,
        "direct_apply_performed": False,
        "production_authority": False,
        "live_execution_authority": False,
        "direct_apply_authority": False,
        "git_push_authority": False,
    }
    preview_path = base / "DIFF_PREVIEW.json"
    _write_json(preview_path, preview)
    result = {
        "ok": not blocked_findings,
        "return_id": return_id,
        "preview_path": _repo_rel(preview_path, shell_root),
        "changed_paths": changed_paths,
        "blocked_findings": blocked_findings,
        "git_apply_check_returncode": check.get("returncode"),
        "direct_apply_performed": False,
    }
    receipt_path = _write_receipt(
        shell_root,
        operation="diff_preview",
        return_id=return_id,
        status="completed" if result["ok"] else "failed",
        result=result,
        files_touched=[_repo_rel(preview_path, shell_root)],
        failure_classification=None if result["ok"] else "POLICY_BLOCK_WORKING_AS_DESIGNED",
    )
    _upsert_queue_item(shell_root, return_id, {"status": "DIFF_PREVIEW_READY", "latest_receipt_path": receipt_path, **result})
    return {"schema_id": "ion.chatgpt_sandbox_return_diff_preview_result.v1", "verdict": READY_VERDICT if result["ok"] else BLOCKED_VERDICT, "receipt_path": receipt_path, **result}


def queue_sandbox_return_codex_review(root: str | Path | None, return_id: str) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    base = _return_root(shell_root, return_id)
    if not _return_is_committed(shell_root, return_id):
        result = {"ok": False, "return_id": return_id, "finding": "return_not_committed_for_review"}
        receipt_path = _write_receipt(shell_root, operation="queue_review", return_id=return_id, status="failed", result=result, failure_classification="POLICY_BLOCK_WORKING_AS_DESIGNED")
        return {"schema_id": "ion.chatgpt_sandbox_return_queue_review_result.v1", "verdict": BLOCKED_VERDICT, "receipt_path": receipt_path, **result}
    manifest = _read_json(base / "SANDBOX_RETURN_MANIFEST.json") or {}
    patch_rel = _repo_rel(base / "PATCH.diff", shell_root) if (base / "PATCH.diff").exists() else None
    objective = "\n".join(
        [
            f"Review ChatGPT sandbox return {return_id}.",
            "Treat sandbox output as inbox evidence, not accepted state.",
            f"Manifest: {_repo_rel(base / 'SANDBOX_RETURN_MANIFEST.json', shell_root)}",
            f"Summary: {_repo_rel(base / 'SUMMARY.md', shell_root)}",
            f"Patch: {patch_rel or 'none'}",
            f"Changed paths: {json.dumps(manifest.get('changed_paths') or [])}",
            "Check manifest/source snapshot/path authority. Do not apply to live source.",
            "If applying for review, use a temporary review root. Run focused tests and return CONTEXT PROOF, TEMPLATE ACTION PROOF, VALIDATION, and RESULT.",
        ]
    )
    from .ion_chatgpt_browser_mcp_connector_contract import call_chatgpt_connector_tool

    connector = call_chatgpt_connector_tool(
        shell_root,
        "ion_request_codex_work_packet",
        {
            "objective": objective,
            "confirmation": "ION_BOUNDED_WRITE_CONFIRMED",
        },
    )
    ok = bool(connector.get("ok"))
    data = connector.get("data") if isinstance(connector.get("data"), Mapping) else {}
    result = {
        "ok": ok,
        "return_id": return_id,
        "connector_result": connector,
        "request_id": data.get("request_id"),
        "packet_path": data.get("packet_path"),
    }
    receipt_path = _write_receipt(
        shell_root,
        operation="queue_review",
        return_id=return_id,
        status="completed" if ok else "failed",
        result=result,
        files_touched=[str(data.get("packet_path"))] if data.get("packet_path") else [],
        failure_classification=None if ok else "ION_PACKET_WRITE_FAILURE",
    )
    if ok:
        _upsert_queue_item(shell_root, return_id, {"status": "CODEX_REVIEW_QUEUED", "latest_receipt_path": receipt_path, "codex_review_packet_path": data.get("packet_path"), "codex_review_request_id": data.get("request_id")})
    return {"schema_id": "ion.chatgpt_sandbox_return_queue_review_result.v1", "verdict": READY_VERDICT if ok else BLOCKED_VERDICT, "receipt_path": receipt_path, **result}


def build_sandbox_return_queue_projection(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    queue = _load_queue(shell_root)
    known = {item.get("return_id"): dict(item) for item in queue.get("returns", []) if isinstance(item, Mapping) and item.get("return_id")}
    inbox = shell_root / INBOX_ROOT
    if inbox.exists():
        for path in sorted([p for p in inbox.iterdir() if p.is_dir()]):
            return_id = path.name
            known.setdefault(
                return_id,
                {
                    "return_id": return_id,
                    "status": "RETURN_DRAFT_WRITTEN",
                    "return_root": _repo_rel(path, shell_root),
                },
            )
    records: list[dict[str, Any]] = []
    for return_id, item in sorted(known.items(), key=lambda pair: str(pair[1].get("updated_at") or pair[1].get("created_at") or ""), reverse=True):
        base = _return_root(shell_root, str(return_id))
        manifest = _read_json(base / "SANDBOX_RETURN_MANIFEST.json") or {}
        changed_paths = manifest.get("changed_paths") if isinstance(manifest.get("changed_paths"), list) else []
        records.append(
            {
                **item,
                "return_id": return_id,
                "return_root": _repo_rel(base, shell_root) if base.exists() else item.get("return_root"),
                "manifest_path": _repo_rel(base / "SANDBOX_RETURN_MANIFEST.json", shell_root) if (base / "SANDBOX_RETURN_MANIFEST.json").exists() else item.get("manifest_path"),
                "summary_path": _repo_rel(base / "SUMMARY.md", shell_root) if (base / "SUMMARY.md").exists() else item.get("summary_path"),
                "patch_path": _repo_rel(base / "PATCH.diff", shell_root) if (base / "PATCH.diff").exists() else item.get("patch_path"),
                "diff_preview_path": _repo_rel(base / "DIFF_PREVIEW.json", shell_root) if (base / "DIFF_PREVIEW.json").exists() else item.get("preview_path"),
                "committed": _return_is_committed(shell_root, str(return_id)),
                "changed_path_count": len(changed_paths),
                "changed_paths": changed_paths[:20],
            }
        )
    return {
        "schema_id": "ion.chatgpt_sandbox_return_queue_projection.v1",
        "ok": True,
        "verdict": READY_VERDICT,
        "queue_path": ACTIVE_QUEUE_PATH.as_posix(),
        "inbox_root": INBOX_ROOT.as_posix(),
        "return_count": len(records),
        "returns": records,
        "production_authority": False,
        "live_execution_authority": False,
        "direct_apply_authority": False,
        "git_push_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ION ChatGPT sandbox return intake.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--register-json", default=None)
    parser.add_argument("--return-id", default=None)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--diff-preview", action="store_true")
    parser.add_argument("--queue-review", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.register_json:
        packet = json.loads(Path(args.register_json).read_text(encoding="utf-8"))
        result = register_sandbox_return(args.ion_root, packet)
    elif args.commit:
        result = commit_sandbox_return(args.ion_root, str(args.return_id or ""))
    elif args.diff_preview:
        result = build_sandbox_return_diff_preview(args.ion_root, str(args.return_id or ""))
    elif args.queue_review:
        result = queue_sandbox_return_codex_review(args.ion_root, str(args.return_id or ""))
    else:
        result = build_sandbox_return_queue_projection(args.ion_root)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json or args.list else result.get("verdict"))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
