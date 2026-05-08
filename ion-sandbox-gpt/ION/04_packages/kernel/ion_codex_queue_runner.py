"""Bounded Codex queue runner for ChatGPT Browser MCP work packets.

This module is a local carrier adapter over the existing ChatGPT connector
Codex work queue. It does not create a second work system and it does not expose
arbitrary shell. The only executable path is the fixed Codex CLI carrier command
for an already queued ``QUEUED_FOR_CODEX_CARRIER`` packet.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import resolve_shell_root_from_ion_root

SCHEMA_ID = "ion.codex_queue_runner.v1"
READY_VERDICT = "ION_CODEX_QUEUE_RUNNER_READY"
BLOCKED_VERDICT = "ION_CODEX_QUEUE_RUNNER_BLOCKED"
CONNECTOR_STATE_DIR = Path("ION/05_context/current/chatgpt_connector")
CODEX_WORK_REQUESTS_DIR = CONNECTOR_STATE_DIR / "codex_work_requests"
CODEX_QUEUE_RUNS_DIR = CONNECTOR_STATE_DIR / "codex_queue_runs"
RUNTIME_DIR = CONNECTOR_STATE_DIR / "runtime"
RUNNER_STATE_PATH = RUNTIME_DIR / "codex_queue_runner_state.json"
CODEX_WORK_QUEUE_INDEX = Path("ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json")
DEFAULT_CODEX_TIMEOUT_SECONDS = 1800
MAX_CODEX_TIMEOUT_SECONDS = 7200

FAILURE_CLASSES = (
    "BACKEND_CODEX_FAILURE",
    "CARRIER_ADAPTER_FAILURE",
    "CODEX_CLI_FAILURE",
    "DAEMON_FAILURE",
    "ION_CORE_FAILURE",
)

ACTIVE_RUN_STATUSES = {
    "CLAIMED_BY_CODEX_QUEUE_RUNNER",
    "CODEX_QUEUE_RUNNER_WORKER_STARTED",
    "CODEX_CLI_RUNNING",
}

TERMINAL_RUN_STATUSES = {
    "RETURN_RECORDED_PROOF_ACCEPTED",
    "RETURN_RECORDED_PROOF_BLOCKED",
    "CODEX_CLI_EXIT_NONZERO",
    "CODEX_CLI_TIMEOUT",
    "DAEMON_WORKER_EXITED_WITHOUT_FINALIZATION",
}

DEFAULT_CONTEXT_READS = (
    "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json",
    "ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json",
    "ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py",
    "ION/04_packages/kernel/ion_carrier_task_return.py",
    "ION/04_packages/kernel/ion_carrier_continue.py",
    "ION/04_packages/kernel/ion_codex_queue_runner.py",
    "ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md",
    "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
    "ION/03_registry/codex_cli_carrier_profile.yaml",
    "ION/04_packages/kernel/ion_cockpit_view_model.py",
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:80] or "codex_queue"


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _resolve_root(root: str | Path | None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    if candidate.is_dir() and (candidate / "ION").exists():
        return candidate
    return resolve_shell_root_from_ion_root(root)


def _safe_rel_path(root: Path, value: str) -> Path:
    rel = Path(value)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("path must be repo-relative and may not escape the repo root")
    target = (root / rel).resolve()
    target.relative_to(root)
    return target


def _connector_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _load_request(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"invalid work request JSON: {path}")
    return payload


def _request_paths(root: Path) -> list[Path]:
    request_root = root / CODEX_WORK_REQUESTS_DIR
    if not request_root.exists():
        return []
    return sorted((path for path in request_root.glob("*.json") if path.is_file()), key=lambda path: path.name)


def _queued_request_paths(root: Path) -> list[Path]:
    queued: list[Path] = []
    for path in _request_paths(root):
        payload = _load_request(path)
        if payload.get("status") == "QUEUED_FOR_CODEX_CARRIER":
            queued.append(path)
    return queued


def _latest_files(root: Path, rel: Path, *, limit: int = 5) -> list[dict[str, Any]]:
    base = root / rel
    if not base.exists():
        return []
    paths = sorted((path for path in base.glob("*.json") if path.is_file()), key=lambda path: path.stat().st_mtime, reverse=True)
    return [
        {
            "path": _connector_rel(path, root),
            "name": path.name,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
        }
        for path in paths[:limit]
    ]


def _latest_run_packets(root: Path, *, limit: int = 5) -> list[dict[str, Any]]:
    base = root / CODEX_QUEUE_RUNS_DIR
    if not base.exists():
        return []
    paths = sorted((path for path in base.rglob("run.json") if path.is_file()), key=lambda path: path.stat().st_mtime, reverse=True)
    runs: list[dict[str, Any]] = []
    for path in paths[:limit]:
        payload = _read_json(path) or {}
        runs.append({
            "path": _connector_rel(path, root),
            "run_id": payload.get("run_id"),
            "request_id": payload.get("request_id"),
            "status": payload.get("status"),
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
        })
    return runs


def _pid_running(pid: int | None) -> bool:
    if not pid or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _run_output_presence(root: Path, run: Mapping[str, Any]) -> dict[str, bool]:
    return {
        key.replace("_path", "_exists"): bool(run.get(key) and (root / str(run.get(key))).exists())
        for key in ("stdout_path", "stderr_path", "last_message_path")
    }


def _refresh_codex_work_queue_index(root: Path) -> dict[str, Any]:
    from .ion_chatgpt_browser_mcp_connector_contract import call_chatgpt_connector_tool

    result = call_chatgpt_connector_tool(root, "ion_codex_work_queue", {"limit": 100})
    queue = dict(result.get("data") or {})
    _write_json(root / CODEX_WORK_QUEUE_INDEX, queue)
    return queue


def build_codex_queue_runner_status(root: str | Path | None = None, *, reconcile: bool = True) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    reconciliation = reconcile_codex_queue_runner_state(shell_root, write=True) if reconcile else {
        "schema_id": "ion.codex_queue_runner_reconciliation.v1",
        "ok": True,
        "write": False,
        "action": "not_requested",
    }
    state = _read_json(shell_root / RUNNER_STATE_PATH) or {}
    active = state.get("active_run") if isinstance(state.get("active_run"), dict) else None
    active_pid = int(active.get("pid")) if active and active.get("pid") else None
    active_running = _pid_running(active_pid)
    queued = _queued_request_paths(shell_root)
    return {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT,
        "runner_state_path": RUNNER_STATE_PATH.as_posix(),
        "queue_path": CODEX_WORK_QUEUE_INDEX.as_posix(),
        "queued_request_count": len(queued),
        "next_request_path": _connector_rel(queued[0], shell_root) if queued else None,
        "active_run": active,
        "active_process_running": active_running,
        "stale_active_run_detected": bool(reconciliation.get("stale_active_run_detected")),
        "reconciliation": reconciliation,
        "latest_runs": _latest_run_packets(shell_root, limit=5),
        "failure_classes": list(FAILURE_CLASSES),
        "manual_proceed_relay_required": False,
        "automation_surface": "ion_codex_queue_process_once",
        "autorun_loop_state": "NOT_STARTED_PROCESS_ONCE_AVAILABLE",
        "production_authority": False,
        "live_execution_authority": False,
    }


def _context_receipt_for_request(request_rel: str, request: Mapping[str, Any] | None = None) -> dict[str, Any]:
    request_context_reads: list[str] = []
    if request:
        for item in request.get("required_context_reads") or []:
            if isinstance(item, Mapping):
                path = str(item.get("path") or "").strip()
            else:
                path = str(item or "").strip()
            if path:
                request_context_reads.append(path)
    paths = [request_rel, *request_context_reads, *DEFAULT_CONTEXT_READS]
    ordered: list[str] = []
    seen: set[str] = set()
    for path in paths:
        if path not in seen:
            ordered.append(path)
            seen.add(path)
    return {
        "schema_id": "ion.context_load_receipt.v1",
        "required_context_reads": [
            {"kind": "file", "path": path, "required": True}
            for path in ordered
        ],
    }


def _build_prompt(request: Mapping[str, Any], request_rel: str, context_receipt_rel: str) -> str:
    objective = str(request.get("objective") or "")
    return "\n".join([
        "carrier_mount:",
        "  title: \"ION Codex Queue Runner Work Packet\"",
        "  carrier: \"Codex CLI\"",
        "  carrier_identity: \"CODEX_CLI_CARRIER\"",
        "  ion_identity_claim: false",
        "  production_authority: false",
        "  live_execution_authority: false",
        "",
        "mission:",
        "  primary_goal: >",
        f"    {objective}",
        "",
        "hard_boundaries:",
        "  - \"Do not claim to be ION, STEWARD, RELAY, PERSONA, or sovereign authority.\"",
        "  - \"Do not push git.\"",
        "  - \"Do not deploy production.\"",
        "  - \"Do not read, print, store, or request secrets/API keys/tokens.\"",
        "  - \"Do not delete files. If removal seems needed, propose lifecycle transition only.\"",
        "  - \"Do not mutate outside the current repo shell root.\"",
        "  - \"Reuse existing ION queue, task-return, carrier-message, and receipt owners.\"",
        "",
        "required_context:",
        f"  work_request_path: \"{request_rel}\"",
        f"  context_receipt_path: \"{context_receipt_rel}\"",
        "  instruction: \"Read the work request and every required path in the context receipt before writing.\"",
        "",
        "return_contract:",
        "  required_sections:",
        "    - \"### CONTEXT PROOF\"",
        "    - \"### TEMPLATE ACTION PROOF\"",
        "    - \"### VALIDATION\"",
        "    - \"### RESULT\"",
        "  template_id: \"ion.template.autonomous_loop.local_worker.v1\"",
        "  action_id_hint: \"codex_queue_runner_process_once\"",
        "  context_proof_requirement: \"Mention every required context path with line/excerpt/sha256 evidence.\"",
        "  result_requirement: \"State touched paths, tests, remaining blockers, and next lawful moves.\"",
        "",
    ])


def _select_request(root: Path, request_path: str | None) -> tuple[Path | None, str | None]:
    if request_path:
        try:
            path = _safe_rel_path(root, request_path)
            path.relative_to((root / CODEX_WORK_REQUESTS_DIR).resolve())
        except (ValueError, RuntimeError):
            return None, "request_path_not_bounded_to_codex_work_requests"
        if not path.exists():
            return None, "request_path_missing"
        return path, None
    queued = _queued_request_paths(root)
    if not queued:
        return None, "no_queued_codex_work_request"
    return queued[0], None


def _write_run_packet(path: Path, payload: Mapping[str, Any]) -> None:
    value = dict(payload)
    value["updated_at"] = _now()
    _write_json(path, value)


def prepare_codex_queue_run(
    root: str | Path | None = None,
    *,
    request_path: str | None = None,
    claim: bool = False,
    codex_binary: str = "codex",
    timeout_seconds: int = DEFAULT_CODEX_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    selected, finding = _select_request(shell_root, request_path)
    if finding or selected is None:
        return {
            "schema_id": SCHEMA_ID,
            "ok": False,
            "finding": finding or "request_selection_failed",
            "production_authority": False,
            "live_execution_authority": False,
        }
    request = _load_request(selected)
    request_rel = _connector_rel(selected, shell_root)
    now = _now()
    run_id = f"codex_run_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(str(request.get('request_id') or selected.stem))}"
    run_dir = shell_root / CODEX_QUEUE_RUNS_DIR / run_id
    counter = 1
    while run_dir.exists():
        run_id = f"codex_run_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(str(request.get('request_id') or selected.stem))}_{counter}"
        run_dir = shell_root / CODEX_QUEUE_RUNS_DIR / run_id
        counter += 1
    run_dir.mkdir(parents=True, exist_ok=False)
    context_receipt = _context_receipt_for_request(request_rel, request)
    context_receipt_path = run_dir / "context_receipt.json"
    prompt_path = run_dir / "prompt.md"
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"
    last_message_path = run_dir / "latest_return.md"
    run_packet_path = run_dir / "run.json"
    _write_json(context_receipt_path, context_receipt)
    prompt = _build_prompt(request, request_rel, _connector_rel(context_receipt_path, shell_root))
    prompt_path.write_text(prompt, encoding="utf-8")
    timeout = min(max(int(timeout_seconds), 30), MAX_CODEX_TIMEOUT_SECONDS)
    run = {
        "schema_id": "ion.codex_queue_runner_run.v1",
        "run_id": run_id,
        "created_at": now,
        "updated_at": now,
        "status": "CLAIMED_BY_CODEX_QUEUE_RUNNER" if claim else "PREPARED_NOT_STARTED",
        "request_id": request.get("request_id"),
        "request_path": request_rel,
        "run_dir": _connector_rel(run_dir, shell_root),
        "prompt_path": _connector_rel(prompt_path, shell_root),
        "context_receipt_path": _connector_rel(context_receipt_path, shell_root),
        "stdout_path": _connector_rel(stdout_path, shell_root),
        "stderr_path": _connector_rel(stderr_path, shell_root),
        "last_message_path": _connector_rel(last_message_path, shell_root),
        "run_packet_path": _connector_rel(run_packet_path, shell_root),
        "codex_command": [
            codex_binary,
            "exec",
            "--sandbox",
            "workspace-write",
            "--output-last-message",
            _connector_rel(last_message_path, shell_root),
        ],
        "timeout_seconds": timeout,
        "failure_classification": None,
        "production_authority": False,
        "live_execution_authority": False,
    }
    _write_run_packet(run_packet_path, run)
    if claim:
        request["status"] = "CLAIMED_BY_CODEX_QUEUE_RUNNER"
        request["updated_at"] = now
        runs = list(request.get("codex_queue_runner_runs") or [])
        runs.append(_connector_rel(run_packet_path, shell_root))
        request["codex_queue_runner_runs"] = runs
        _write_json(selected, request)
        _refresh_codex_work_queue_index(shell_root)
    return {
        "schema_id": SCHEMA_ID,
        "ok": True,
        "run": run,
        "context_receipt": context_receipt,
        "prepared_only": not claim,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _update_runner_state(root: Path, state: Mapping[str, Any]) -> None:
    payload = dict(state)
    payload.setdefault("schema_id", "ion.codex_queue_runner_state.v1")
    payload["updated_at"] = _now()
    payload.setdefault("production_authority", False)
    payload.setdefault("live_execution_authority", False)
    _write_json(root / RUNNER_STATE_PATH, payload)


def process_codex_queue_once(
    root: str | Path | None = None,
    *,
    request_path: str | None = None,
    start: bool = False,
    background: bool = True,
    codex_binary: str = "codex",
    timeout_seconds: int = DEFAULT_CODEX_TIMEOUT_SECONDS,
    task_output_override: str | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    status = build_codex_queue_runner_status(shell_root)
    if start and status.get("active_process_running"):
        return {
            "schema_id": SCHEMA_ID,
            "ok": False,
            "finding": "codex_queue_runner_already_active",
            "active_run": status.get("active_run"),
            "production_authority": False,
            "live_execution_authority": False,
        }
    prepared = prepare_codex_queue_run(
        shell_root,
        request_path=request_path,
        claim=start,
        codex_binary=codex_binary,
        timeout_seconds=timeout_seconds,
    )
    if not prepared.get("ok") or not start:
        return prepared
    run = dict(prepared["run"])
    run_packet = shell_root / str(run["run_packet_path"])
    if background:
        env = os.environ.copy()
        packages = str(shell_root / "ION/04_packages")
        env["PYTHONPATH"] = f"{packages}:{env.get('PYTHONPATH', '')}" if env.get("PYTHONPATH") else packages
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        cmd = [
            sys.executable,
            "-S",
            "-m",
            "kernel.ion_codex_queue_runner",
            "--ion-root",
            str(shell_root),
            "--worker-run",
            str(run_packet.relative_to(shell_root)),
            "--json",
        ]
        stdout = (run_packet.parent / "worker_stdout.log").open("wb")
        stderr = (run_packet.parent / "worker_stderr.log").open("wb")
        proc = subprocess.Popen(cmd, cwd=shell_root, stdout=stdout, stderr=stderr, env=env, start_new_session=True)
        run["status"] = "CODEX_QUEUE_RUNNER_WORKER_STARTED"
        run["pid"] = proc.pid
        run["worker_command"] = cmd
        _write_run_packet(run_packet, run)
        _update_runner_state(shell_root, {
            "active_run": {
                "run_id": run["run_id"],
                "pid": proc.pid,
                "run_packet_path": run["run_packet_path"],
                "request_path": run["request_path"],
                "started_at": _now(),
            },
            "latest_run": run["run_packet_path"],
            "manual_proceed_relay_required": False,
        })
        return {
            "schema_id": SCHEMA_ID,
            "ok": True,
            "result": "CODEX_QUEUE_RUNNER_WORKER_STARTED",
            "run": run,
            "manual_proceed_relay_required": False,
            "production_authority": False,
            "live_execution_authority": False,
        }
    worker = run_codex_queue_worker(shell_root, run_packet, task_output_override=task_output_override)
    return {
        "schema_id": SCHEMA_ID,
        "ok": bool(worker.get("ok")),
        "result": worker.get("result"),
        "run": worker.get("run"),
        "submit_result": worker.get("submit_result"),
        "manual_proceed_relay_required": False,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _update_request_status(root: Path, request_rel: str, *, status: str, failure_classification: str | None = None) -> None:
    request_path = root / request_rel
    payload = _load_request(request_path)
    payload["status"] = status
    payload["updated_at"] = _now()
    if failure_classification:
        payload["failure_classification"] = failure_classification
    _write_json(request_path, payload)
    _refresh_codex_work_queue_index(root)


def reconcile_codex_queue_runner_state(root: str | Path | None = None, *, write: bool = False) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    state_path = shell_root / RUNNER_STATE_PATH
    state = _read_json(state_path) or {}
    active = state.get("active_run") if isinstance(state.get("active_run"), dict) else None
    now = _now()
    result: dict[str, Any] = {
        "schema_id": "ion.codex_queue_runner_reconciliation.v1",
        "ok": True,
        "write": bool(write),
        "runner_state_path": RUNNER_STATE_PATH.as_posix(),
        "stale_active_run_detected": False,
        "active_process_running": False,
        "action": "no_active_run",
        "production_authority": False,
        "live_execution_authority": False,
    }

    latest_run_rel = str(state.get("latest_run") or "").strip()
    if not active:
        if latest_run_rel:
            _classify_terminal_run_if_needed(shell_root, latest_run_rel, write=write, result=result)
        return result

    active_pid = int(active.get("pid")) if active.get("pid") else None
    active_running = _pid_running(active_pid)
    result["active_process_running"] = active_running
    result["active_run"] = active
    if active_running:
        result["action"] = "active_run_still_running"
        return result

    result["stale_active_run_detected"] = True
    result["action"] = "clear_stale_active_reference"
    run_rel = str(active.get("run_packet_path") or "")
    if not run_rel:
        result["finding"] = "active_run_missing_run_packet_path"
        if write:
            _update_runner_state(shell_root, {
                "active_run": None,
                "latest_run": latest_run_rel or None,
                "manual_proceed_relay_required": False,
            })
        return result

    try:
        run_path = _safe_rel_path(shell_root, run_rel)
    except ValueError:
        result["finding"] = "active_run_run_packet_path_not_repo_relative"
        if write:
            _update_runner_state(shell_root, {
                "active_run": None,
                "latest_run": latest_run_rel or run_rel,
                "manual_proceed_relay_required": False,
            })
        return result

    run = _read_json(run_path)
    if not isinstance(run, dict):
        result["finding"] = "active_run_run_packet_missing_or_invalid"
        if write:
            _update_runner_state(shell_root, {
                "active_run": None,
                "latest_run": latest_run_rel or run_rel,
                "manual_proceed_relay_required": False,
            })
        return result

    previous_status = str(run.get("status") or "")
    result["run_packet_path"] = _connector_rel(run_path, shell_root)
    result["previous_run_status"] = previous_status
    result["output_presence"] = _run_output_presence(shell_root, run)

    if previous_status in ACTIVE_RUN_STATUSES:
        result["action"] = "mark_daemon_failure_and_clear_active"
        if write:
            run["status"] = "DAEMON_WORKER_EXITED_WITHOUT_FINALIZATION"
            run["completed_at"] = now
            run["failure_classification"] = "DAEMON_FAILURE"
            run["daemon_reconciliation"] = {
                "reconciled_at": now,
                "reason": "active_pid_not_running_before_worker_finalized",
                "previous_status": previous_status,
                "pid": active_pid,
                "output_presence": result["output_presence"],
            }
            _write_run_packet(run_path, run)
            request_rel = str(run.get("request_path") or active.get("request_path") or "")
            if request_rel:
                _update_request_status(
                    shell_root,
                    request_rel,
                    status="CODEX_QUEUE_RUNNER_FAILED",
                    failure_classification="DAEMON_FAILURE",
                )
    elif previous_status == "RETURN_RECORDED_PROOF_BLOCKED" and not run.get("failure_classification"):
        result["action"] = "classify_proof_blocked_terminal_run_and_clear_active"
        if write:
            run["failure_classification"] = "BACKEND_CODEX_FAILURE"
            _write_run_packet(run_path, run)
            request_rel = str(run.get("request_path") or active.get("request_path") or "")
            if request_rel:
                _update_request_status(
                    shell_root,
                    request_rel,
                    status="RETURN_RECORDED_PROOF_BLOCKED",
                    failure_classification="BACKEND_CODEX_FAILURE",
                )
    elif previous_status not in TERMINAL_RUN_STATUSES:
        result["action"] = "mark_unknown_stale_run_failed_and_clear_active"
        if write:
            run["status"] = "DAEMON_WORKER_EXITED_WITHOUT_FINALIZATION"
            run["completed_at"] = now
            run["failure_classification"] = "DAEMON_FAILURE"
            run["daemon_reconciliation"] = {
                "reconciled_at": now,
                "reason": "active_pid_not_running_with_unknown_run_status",
                "previous_status": previous_status,
                "pid": active_pid,
                "output_presence": result["output_presence"],
            }
            _write_run_packet(run_path, run)
            request_rel = str(run.get("request_path") or active.get("request_path") or "")
            if request_rel:
                _update_request_status(
                    shell_root,
                    request_rel,
                    status="CODEX_QUEUE_RUNNER_FAILED",
                    failure_classification="DAEMON_FAILURE",
                )

    if write:
        _update_runner_state(shell_root, {
            "active_run": None,
            "latest_run": _connector_rel(run_path, shell_root),
            "manual_proceed_relay_required": False,
        })
    return result


def _classify_terminal_run_if_needed(
    root: Path,
    run_rel: str,
    *,
    write: bool,
    result: dict[str, Any],
) -> None:
    try:
        run_path = _safe_rel_path(root, run_rel)
    except ValueError:
        result["latest_run_finding"] = "latest_run_path_not_repo_relative"
        return
    run = _read_json(run_path)
    if not isinstance(run, dict):
        result["latest_run_finding"] = "latest_run_packet_missing_or_invalid"
        return
    if run.get("status") != "RETURN_RECORDED_PROOF_BLOCKED" or run.get("failure_classification"):
        return
    result["latest_run_failure_classification_missing"] = True
    result["latest_run_packet_path"] = _connector_rel(run_path, root)
    if not write:
        return
    run["failure_classification"] = "BACKEND_CODEX_FAILURE"
    _write_run_packet(run_path, run)
    request_rel = str(run.get("request_path") or "")
    if request_rel:
        _update_request_status(
            root,
            request_rel,
            status="RETURN_RECORDED_PROOF_BLOCKED",
            failure_classification="BACKEND_CODEX_FAILURE",
        )
    result["latest_run_failure_classification_updated"] = True


def run_codex_queue_worker(
    root: str | Path | None,
    run_packet_path: str | Path,
    *,
    task_output_override: str | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    run_path = Path(run_packet_path)
    if not run_path.is_absolute():
        run_path = shell_root / run_path
    run = _read_json(run_path)
    if not isinstance(run, dict):
        raise ValueError(f"invalid run packet: {run_packet_path}")
    run["status"] = "CODEX_CLI_RUNNING"
    run["started_at"] = _now()
    _write_run_packet(run_path, run)
    request_rel = str(run["request_path"])
    task_output = task_output_override
    returncode: int | None = None
    timed_out = False
    if task_output is None:
        command = list(run["codex_command"])
        prompt = (shell_root / str(run["prompt_path"])).read_text(encoding="utf-8")
        try:
            completed = subprocess.run(
                command,
                cwd=shell_root,
                input=prompt,
                text=True,
                capture_output=True,
                timeout=int(run.get("timeout_seconds") or DEFAULT_CODEX_TIMEOUT_SECONDS),
                check=False,
            )
            returncode = completed.returncode
            (shell_root / str(run["stdout_path"])).write_text(completed.stdout, encoding="utf-8", errors="replace")
            (shell_root / str(run["stderr_path"])).write_text(completed.stderr, encoding="utf-8", errors="replace")
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            returncode = None
            (shell_root / str(run["stdout_path"])).write_text(str(exc.stdout or ""), encoding="utf-8", errors="replace")
            (shell_root / str(run["stderr_path"])).write_text(str(exc.stderr or "codex command timed out"), encoding="utf-8", errors="replace")
        last_message = shell_root / str(run["last_message_path"])
        if last_message.exists():
            task_output = last_message.read_text(encoding="utf-8", errors="replace")
        else:
            task_output = (shell_root / str(run["stdout_path"])).read_text(encoding="utf-8", errors="replace")
    else:
        (shell_root / str(run["last_message_path"])).write_text(task_output, encoding="utf-8")
        (shell_root / str(run["stdout_path"])).write_text("", encoding="utf-8")
        (shell_root / str(run["stderr_path"])).write_text("", encoding="utf-8")
        returncode = 0

    if timed_out:
        run["status"] = "CODEX_CLI_TIMEOUT"
        run["failure_classification"] = "CODEX_CLI_FAILURE"
        _write_run_packet(run_path, run)
        _update_request_status(shell_root, request_rel, status="CODEX_QUEUE_RUNNER_FAILED", failure_classification="CODEX_CLI_FAILURE")
        return {"schema_id": SCHEMA_ID, "ok": False, "result": "CODEX_CLI_TIMEOUT", "run": run}
    if returncode not in {0, None}:
        run["status"] = "CODEX_CLI_EXIT_NONZERO"
        run["returncode"] = returncode
        run["failure_classification"] = "CODEX_CLI_FAILURE"
        _write_run_packet(run_path, run)
        _update_request_status(shell_root, request_rel, status="CODEX_QUEUE_RUNNER_FAILED", failure_classification="CODEX_CLI_FAILURE")
        return {"schema_id": SCHEMA_ID, "ok": False, "result": "CODEX_CLI_EXIT_NONZERO", "run": run}

    from .ion_chatgpt_browser_mcp_connector_contract import call_chatgpt_connector_tool

    context_receipt = _read_json(shell_root / str(run["context_receipt_path"])) or {}
    request = _load_request(shell_root / request_rel)
    submit = call_chatgpt_connector_tool(
        shell_root,
        "ion_submit_task_return",
        {
            "task_output_text": task_output,
            "context_receipt": context_receipt,
            "work_request_id": str(request.get("request_id") or ""),
            "work_request_path": request_rel,
        },
    )
    accepted = bool((submit.get("data") or {}).get("accepted_for_carrier_intake"))
    run["status"] = "RETURN_RECORDED_PROOF_ACCEPTED" if accepted else "RETURN_RECORDED_PROOF_BLOCKED"
    run["returncode"] = returncode
    run["failure_classification"] = None if accepted else "BACKEND_CODEX_FAILURE"
    run["submit_result"] = submit.get("data")
    run["completed_at"] = _now()
    _write_run_packet(run_path, run)
    if not accepted:
        _update_request_status(
            shell_root,
            request_rel,
            status="RETURN_RECORDED_PROOF_BLOCKED",
            failure_classification="BACKEND_CODEX_FAILURE",
        )
    _update_runner_state(shell_root, {
        "active_run": None,
        "latest_run": _connector_rel(run_path, shell_root),
        "manual_proceed_relay_required": False,
    })
    return {
        "schema_id": SCHEMA_ID,
        "ok": accepted,
        "result": run["status"],
        "run": run,
        "submit_result": submit,
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ION bounded Codex queue runner.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--process-once", action="store_true")
    parser.add_argument("--reconcile", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--start", action="store_true")
    parser.add_argument("--request-path", default=None)
    parser.add_argument("--codex-binary", default="codex")
    parser.add_argument("--timeout-seconds", type=int, default=DEFAULT_CODEX_TIMEOUT_SECONDS)
    parser.add_argument("--worker-run", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.worker_run:
        result = run_codex_queue_worker(args.ion_root, args.worker_run)
        ok = bool(result.get("ok"))
    elif args.reconcile:
        result = reconcile_codex_queue_runner_state(args.ion_root, write=args.write)
        ok = bool(result.get("ok"))
    elif args.process_once:
        result = process_codex_queue_once(
            args.ion_root,
            request_path=args.request_path,
            start=args.start,
            background=True,
            codex_binary=args.codex_binary,
            timeout_seconds=args.timeout_seconds,
        )
        ok = bool(result.get("ok"))
    else:
        result = build_codex_queue_runner_status(args.ion_root)
        ok = result.get("verdict") == READY_VERDICT

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result.get("verdict") or result.get("result") or ("OK" if ok else "BLOCKED"))
        if result.get("finding"):
            print(f"- {result['finding']}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
