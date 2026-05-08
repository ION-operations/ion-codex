"""Codex CLI response carrier for Capsule-backed Codex Chat turns.

This module owns response-only Codex CLI runs. It does not replace the bounded
Codex work queue; implementation work still belongs to ``ion_codex_queue_runner``.
The carrier is for normal chat answers under the Codex Chat Engine contract.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .ion_codex_chat_engine import build_codex_chat_carrier_objective
from .ion_codex_model_moves import codex_exec_args_from_model_move, summarize_model_move
from .ion_codex_solo_context import (
    CAPSULE_PATH,
    HOT_CONTEXT_PATH,
    MINI_PATH,
    WITNESS_POLICY,
    build_codex_solo_context_model,
)


SCHEMA_ID = "ion.codex_chat_response_carrier_run.v1"
STATUS_SCHEMA_ID = "ion.codex_chat_response_carrier_status.v1"
READY_VERDICT = "ION_CODEX_CHAT_RESPONSE_CARRIER_READY"
DISABLED_VERDICT = "ION_CODEX_CHAT_RESPONSE_CARRIER_DISABLED"
BLOCKED_VERDICT = "ION_CODEX_CHAT_RESPONSE_CARRIER_BLOCKED"

RUNS_DIR = Path("ION/05_context/current/codex_capsule_chat/response_runs")

ENABLED_ENV = "ION_CODEX_CHAT_RESPONSE_CARRIER_ENABLED"
START_MODE_ENV = "ION_CODEX_CHAT_RESPONSE_CARRIER_START_MODE"
TIMEOUT_ENV = "ION_CODEX_CHAT_RESPONSE_CARRIER_TIMEOUT_SECONDS"
CAPTURE_JSON_ENV = "ION_CODEX_CHAT_RESPONSE_CARRIER_CAPTURE_JSON"
CODEX_BINARY_ENV = "ION_CODEX_CHAT_RESPONSE_CARRIER_CODEX_BINARY"
SANDBOX_ENV = "ION_CODEX_CHAT_RESPONSE_CARRIER_SANDBOX"

DEFAULT_TIMEOUT_SECONDS = 240
MAX_TIMEOUT_SECONDS = 900
TRUTHY = {"1", "true", "yes", "on", "enabled"}


SubprocessRunner = Callable[..., subprocess.CompletedProcess[str]]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _now_token() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ%f")


def _resolve_root(root: str | Path | None = None) -> Path:
    return Path(root or ".").expanduser().resolve()


def _connector_rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _trim(value: Any, *, limit: int = 12000) -> str:
    return str(value or "").replace("\r\n", "\n").strip()[:limit]


def _safe_slug(value: Any, *, limit: int = 72) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(value or "").lower()).strip("_")[:limit] or "chat_response"


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def _read_text(path: Path, *, limit: int = 24000) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def _truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in TRUTHY


def carrier_enabled(env: Mapping[str, str] | None = None) -> bool:
    source = env if env is not None else os.environ
    return _truthy(source.get(ENABLED_ENV))


def _capture_json_enabled(env: Mapping[str, str] | None = None) -> bool:
    source = env if env is not None else os.environ
    raw = source.get(CAPTURE_JSON_ENV)
    return True if raw is None else _truthy(raw)


def _timeout_seconds(value: Any = None, env: Mapping[str, str] | None = None) -> int:
    source = env if env is not None else os.environ
    raw = value if value is not None else source.get(TIMEOUT_ENV)
    try:
        parsed = int(raw or DEFAULT_TIMEOUT_SECONDS)
    except (TypeError, ValueError):
        parsed = DEFAULT_TIMEOUT_SECONDS
    return min(max(parsed, 30), MAX_TIMEOUT_SECONDS)


def _start_mode(env: Mapping[str, str] | None = None) -> str:
    source = env if env is not None else os.environ
    mode = str(source.get(START_MODE_ENV) or "foreground").strip().lower()
    return mode if mode in {"foreground"} else "foreground"


def _sandbox_mode(env: Mapping[str, str] | None = None) -> str:
    source = env if env is not None else os.environ
    mode = str(source.get(SANDBOX_ENV) or "workspace-write").strip()
    return mode if mode in {"read-only", "workspace-write"} else "workspace-write"


def _git_status_set(root: Path) -> set[str]:
    try:
        completed = subprocess.run(
            ["git", "status", "--short"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )
    except Exception:
        return set()
    if completed.returncode != 0:
        return set()
    return {line.rstrip() for line in completed.stdout.splitlines() if line.strip()}


def build_chat_response_carrier_status(
    root: str | Path | None = None,
    *,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    enabled = carrier_enabled(env)
    return {
        "schema_id": STATUS_SCHEMA_ID,
        "verdict": READY_VERDICT if enabled else DISABLED_VERDICT,
        "ok": True,
        "enabled": enabled,
        "enabled_env": ENABLED_ENV,
        "start_mode": _start_mode(env),
        "start_mode_env": START_MODE_ENV,
        "timeout_seconds": _timeout_seconds(env=env),
        "timeout_env": TIMEOUT_ENV,
        "capture_json": _capture_json_enabled(env),
        "capture_json_env": CAPTURE_JSON_ENV,
        "codex_binary": (env or os.environ).get(CODEX_BINARY_ENV, "codex"),
        "codex_binary_env": CODEX_BINARY_ENV,
        "run_root": RUNS_DIR.as_posix(),
        "sandbox": _sandbox_mode(env),
        "sandbox_env": SANDBOX_ENV,
        "ephemeral": True,
        "response_only_no_write_policy": True,
        "worktree_drift_detection": True,
        "uses_codex_cli": True,
        "direct_provider_api": False,
        "fallback_when_disabled": "local_chat_engine_response_contract",
        "active_root": shell_root.as_posix(),
        "production_authority": False,
        "live_execution_authority": False,
        "provider_api_dispatch_authorized": False,
        "state_acceptance_granted": False,
    }


def _latest_capsule_rows_text(codex_solo_context: Mapping[str, Any]) -> str:
    capsule = codex_solo_context.get("capsule") if isinstance(codex_solo_context.get("capsule"), Mapping) else {}
    rows = capsule.get("recent_rows") if isinstance(capsule.get("recent_rows"), list) else []
    lines = []
    for row in rows[-6:]:
        if isinstance(row, Mapping):
            lines.append(f"- {row.get('id')} {row.get('status')}: {row.get('summary')}")
    return "\n".join(lines) or "- No Capsule rows available."


def _mini_text(codex_solo_context: Mapping[str, Any]) -> str:
    mini = codex_solo_context.get("mini") if isinstance(codex_solo_context.get("mini"), Mapping) else {}
    return _trim(mini.get("text") or "", limit=5000)


def _hot_context_excerpt(root: Path) -> str:
    text = _read_text(root / HOT_CONTEXT_PATH, limit=9000)
    if not text:
        return "Hot context file unavailable; rely on Capsule rows, Mini lookup, and chat engine context refs."
    return _trim(text, limit=9000)


def _context_package_summary(codex_solo_context: Mapping[str, Any]) -> str:
    packages_model = codex_solo_context.get("context_packages") if isinstance(codex_solo_context.get("context_packages"), Mapping) else {}
    selected = packages_model.get("selected_by_default") if isinstance(packages_model.get("selected_by_default"), list) else []
    packages = packages_model.get("packages") if isinstance(packages_model.get("packages"), list) else []
    lines = []
    for package in packages[:10]:
        if not isinstance(package, Mapping):
            continue
        package_id = str(package.get("package_id") or "unknown")
        marker = "selected" if package_id in selected else "available"
        refs = package.get("path_refs") if isinstance(package.get("path_refs"), list) else []
        ref_text = ", ".join(str(ref) for ref in refs[:3])
        lines.append(
            f"- {package_id} [{marker}; {package.get('context_type') or 'context'}]: "
            f"{package.get('load_policy') or 'load as needed'}"
            + (f" / refs: {ref_text}" if ref_text else "")
        )
    return "\n".join(lines) or "- Context package selector unavailable."


def _root_boundary_lines(shell_root: Path) -> list[str]:
    lines = [
        f"- Work only in the active root named above: {shell_root.as_posix()}",
        "- This is response-only chat. Do not edit files.",
    ]
    if shell_root.as_posix().endswith("/ION_CODEX FULL"):
        lines.append("- Do not create, use, or repair older /home/sev/ION - Production/ION_CODEX paths.")
    return lines


def build_chat_response_prompt(
    root: str | Path | None,
    *,
    operator_message: str,
    chat_engine_turn: Mapping[str, Any],
    codex_solo_context: Mapping[str, Any] | None = None,
    prior_turns: list[Mapping[str, Any]] | None = None,
) -> str:
    shell_root = _resolve_root(root)
    codex_solo = dict(codex_solo_context) if isinstance(codex_solo_context, Mapping) else build_codex_solo_context_model(shell_root, write=False)
    model_move = chat_engine_turn.get("model_move") if isinstance(chat_engine_turn.get("model_move"), Mapping) else {}
    prior_lines = []
    for turn in (prior_turns or [])[-8:]:
        if not isinstance(turn, Mapping):
            continue
        author = str(turn.get("author") or "unknown")
        message = _trim(turn.get("message") or "", limit=800)
        if message:
            prior_lines.append(f"{author}: {message}")
    prior_text = "\n".join(prior_lines) or "No prior visible chat turns supplied."
    engine_objective = build_codex_chat_carrier_objective(chat_engine_turn, operator_message)
    return "\n".join([
        "ION Codex Chat response carrier.",
        "",
        "ACTIVE ROOT:",
        shell_root.as_posix(),
        "",
        "ROOT BOUNDARY:",
        *_root_boundary_lines(shell_root),
        "",
        "CAPSULE POLICY:",
        f"- {WITNESS_POLICY}",
        f"- Minimum context: {CAPSULE_PATH.as_posix()}",
        f"- Mini lookup index: {MINI_PATH.as_posix()}",
        f"- Hot context: {HOT_CONTEXT_PATH.as_posix()}",
        "",
        "RECENT CAPSULE ROWS:",
        _latest_capsule_rows_text(codex_solo),
        "",
        "MINI LOOKUP BRIEF:",
        _mini_text(codex_solo) or "Mini unavailable.",
        "",
        "HOT CONTEXT EXCERPT:",
        _hot_context_excerpt(shell_root),
        "",
        "CONTEXT PACKAGE SELECTOR:",
        _context_package_summary(codex_solo),
        "",
        "CHAT ENGINE CONTRACT:",
        engine_objective,
        "",
        "MODEL MOVE:",
        f"- {summarize_model_move(model_move)}",
        "",
        "VISIBLE CHAT HISTORY:",
        prior_text,
        "",
        "VISIBLE ANSWER RULES:",
        "- Answer Sev directly and conversationally.",
        "- Answer the actual user message first; use ION/Capsule details as support, not ceremony.",
        "- Preserve continuity from Visible Chat History, Capsule rows, Hot Context, and Context Package Selector.",
        "- Keep ION internals out of the visible answer unless they clarify the answer.",
        "- Do not expose hidden chain of thought.",
        "- Do not claim you changed files, accepted state, deployed, or used secrets.",
        "- If live status is not directly available in the mounted context, say what is known and what is not known.",
        "- If the message requires implementation, explain that it belongs in Run task / proof-gated Codex work.",
        "- Ask one concise clarifying question only when necessary.",
        "",
        "OPERATOR MESSAGE:",
        _trim(operator_message, limit=8000),
    ])


def _codex_command(
    *,
    codex_binary: str,
    root: Path,
    model_move: Mapping[str, Any],
    latest_return_rel: str,
    capture_json: bool,
    sandbox: str,
) -> list[str]:
    command = [
        codex_binary,
        "exec",
        *codex_exec_args_from_model_move(model_move),
        "--sandbox",
        sandbox,
        "--cd",
        root.as_posix(),
        "--ephemeral",
        "--output-last-message",
        latest_return_rel,
    ]
    if capture_json:
        command.append("--json")
    return command


def prepare_codex_chat_response_run(
    root: str | Path | None,
    *,
    operator_message: str,
    chat_engine_turn: Mapping[str, Any],
    codex_solo_context: Mapping[str, Any] | None = None,
    prior_turns: list[Mapping[str, Any]] | None = None,
    codex_binary: str | None = None,
    timeout_seconds: int | None = None,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    now = _now()
    run_id = f"codex_chat_response_{_now_token()}_{_safe_slug(operator_message)}"
    run_dir = shell_root / RUNS_DIR / run_id
    counter = 1
    while run_dir.exists():
        run_id = f"codex_chat_response_{_now_token()}_{_safe_slug(operator_message)}_{counter}"
        run_dir = shell_root / RUNS_DIR / run_id
        counter += 1
    run_dir.mkdir(parents=True, exist_ok=False)
    prompt_path = run_dir / "prompt.md"
    latest_return_path = run_dir / "latest_return.md"
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"
    events_path = run_dir / "events.jsonl"
    run_path = run_dir / "run.json"
    prompt = build_chat_response_prompt(
        shell_root,
        operator_message=operator_message,
        chat_engine_turn=chat_engine_turn,
        codex_solo_context=codex_solo_context,
        prior_turns=prior_turns,
    )
    prompt_path.write_text(prompt, encoding="utf-8")
    model_move = chat_engine_turn.get("model_move") if isinstance(chat_engine_turn.get("model_move"), Mapping) else {}
    capture_json = _capture_json_enabled(env)
    sandbox = _sandbox_mode(env)
    binary = codex_binary or (env or os.environ).get(CODEX_BINARY_ENV, "codex")
    latest_return_rel = _connector_rel(latest_return_path, shell_root)
    run = {
        "schema_id": SCHEMA_ID,
        "run_id": run_id,
        "created_at": now,
        "updated_at": now,
        "status": "PREPARED_NOT_STARTED",
        "operator_message_sha256": _sha256_text(_trim(operator_message)),
        "run_dir": _connector_rel(run_dir, shell_root),
        "run_packet_path": _connector_rel(run_path, shell_root),
        "prompt_path": _connector_rel(prompt_path, shell_root),
        "latest_return_path": latest_return_rel,
        "stdout_path": _connector_rel(stdout_path, shell_root),
        "stderr_path": _connector_rel(stderr_path, shell_root),
        "events_path": _connector_rel(events_path, shell_root),
        "codex_command": _codex_command(
            codex_binary=binary,
            root=shell_root,
            model_move=model_move,
            latest_return_rel=latest_return_rel,
            capture_json=capture_json,
            sandbox=sandbox,
        ),
        "timeout_seconds": _timeout_seconds(timeout_seconds, env),
        "capture_json": capture_json,
        "sandbox": sandbox,
        "chat_engine_turn": dict(chat_engine_turn),
        "skill_activation": dict(chat_engine_turn.get("skill_activation")) if isinstance(chat_engine_turn.get("skill_activation"), Mapping) else {},
        "native_lenses": list(chat_engine_turn.get("native_lenses")) if isinstance(chat_engine_turn.get("native_lenses"), list) else [],
        "selected_model": model_move.get("selected_model"),
        "selected_reasoning_effort": model_move.get("selected_reasoning_effort"),
        "model_move_summary": summarize_model_move(model_move),
        "production_authority": False,
        "live_execution_authority": False,
        "provider_api_dispatch_authorized": False,
        "state_acceptance_granted": False,
    }
    _write_json(run_path, run)
    return {"schema_id": SCHEMA_ID, "ok": True, "run": run, "prompt": prompt}


def _update_run(shell_root: Path, run: Mapping[str, Any], updates: Mapping[str, Any]) -> dict[str, Any]:
    run_path = shell_root / str(run["run_packet_path"])
    payload = _read_json(run_path)
    payload.update(dict(updates))
    payload["updated_at"] = _now()
    _write_json(run_path, payload)
    return payload


def _result_from_run(shell_root: Path, run: Mapping[str, Any], *, ok: bool, status: str, finding: str | None = None) -> dict[str, Any]:
    latest_return = shell_root / str(run["latest_return_path"])
    response_text = _trim(_read_text(latest_return), limit=60000)
    payload = _update_run(shell_root, run, {
        "status": status,
        "finding": finding,
        "ok": ok,
        "response_text": response_text,
        "response_sha256": _sha256_text(response_text) if response_text else None,
        "completed_at": _now(),
    })
    return {
        "schema_id": SCHEMA_ID,
        "ok": ok,
        "status": status,
        "finding": finding,
        "run": payload,
        "run_id": payload.get("run_id"),
        "run_packet_path": payload.get("run_packet_path"),
        "response_text": response_text,
        "response_sha256": payload.get("response_sha256"),
        "production_authority": False,
        "live_execution_authority": False,
        "provider_api_dispatch_authorized": False,
        "state_acceptance_granted": False,
    }


def run_codex_chat_response_carrier(
    root: str | Path | None,
    *,
    operator_message: str,
    chat_engine_turn: Mapping[str, Any],
    codex_solo_context: Mapping[str, Any] | None = None,
    prior_turns: list[Mapping[str, Any]] | None = None,
    enabled: bool | None = None,
    response_override: str | None = None,
    subprocess_runner: SubprocessRunner | None = None,
    codex_binary: str | None = None,
    timeout_seconds: int | None = None,
    env: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    should_run = carrier_enabled(env) if enabled is None else bool(enabled)
    if not should_run and response_override is None:
        return {
            "schema_id": SCHEMA_ID,
            "ok": False,
            "status": "CARRIER_DISABLED",
            "finding": "chat_response_carrier_disabled",
            "enabled_env": ENABLED_ENV,
            "response_text": "",
            "production_authority": False,
            "live_execution_authority": False,
            "provider_api_dispatch_authorized": False,
            "state_acceptance_granted": False,
        }
    prepared = prepare_codex_chat_response_run(
        shell_root,
        operator_message=operator_message,
        chat_engine_turn=chat_engine_turn,
        codex_solo_context=codex_solo_context,
        prior_turns=prior_turns,
        codex_binary=codex_binary,
        timeout_seconds=timeout_seconds,
        env=env,
    )
    run = prepared["run"]
    prompt = str(prepared["prompt"])
    latest_return_path = shell_root / str(run["latest_return_path"])
    stdout_path = shell_root / str(run["stdout_path"])
    stderr_path = shell_root / str(run["stderr_path"])
    events_path = shell_root / str(run["events_path"])
    if response_override is not None:
        latest_return_path.write_text(_trim(response_override, limit=60000), encoding="utf-8")
        stdout_path.write_text("", encoding="utf-8")
        stderr_path.write_text("", encoding="utf-8")
        events_path.write_text("", encoding="utf-8")
        return _result_from_run(shell_root, run, ok=True, status="RETURN_CAPTURED_FAKE")

    _update_run(shell_root, run, {"status": "CODEX_CLI_RUNNING", "started_at": _now()})
    runner = subprocess_runner or subprocess.run
    before_status = _git_status_set(shell_root)
    try:
        completed = runner(
            list(run["codex_command"]),
            cwd=shell_root,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=int(run.get("timeout_seconds") or DEFAULT_TIMEOUT_SECONDS),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else str(exc.stdout or "")
        stderr = exc.stderr if isinstance(exc.stderr, str) else str(exc.stderr or "codex command timed out")
        stdout_path.write_text(stdout, encoding="utf-8", errors="replace")
        stderr_path.write_text(stderr, encoding="utf-8", errors="replace")
        events_path.write_text(stdout if run.get("capture_json") else "", encoding="utf-8", errors="replace")
        return _result_from_run(shell_root, run, ok=False, status="CODEX_CLI_TIMEOUT", finding="codex_cli_timeout")

    stdout_path.write_text(completed.stdout or "", encoding="utf-8", errors="replace")
    stderr_path.write_text(completed.stderr or "", encoding="utf-8", errors="replace")
    events_path.write_text((completed.stdout or "") if run.get("capture_json") else "", encoding="utf-8", errors="replace")
    after_status = _git_status_set(shell_root)
    unexpected_changes = sorted(after_status - before_status)
    _update_run(shell_root, run, {"returncode": completed.returncode, "unexpected_worktree_changes": unexpected_changes})
    response_text = _trim(_read_text(latest_return_path), limit=60000)
    if completed.returncode != 0:
        return _result_from_run(shell_root, run, ok=False, status="CODEX_CLI_EXIT_NONZERO", finding="codex_cli_exit_nonzero")
    if unexpected_changes:
        return _result_from_run(shell_root, run, ok=False, status="UNEXPECTED_WORKTREE_CHANGES", finding="response_only_carrier_modified_worktree")
    if not response_text:
        return _result_from_run(shell_root, run, ok=False, status="CODEX_CLI_NO_RESPONSE", finding="latest_return_missing_or_empty")
    return _result_from_run(shell_root, run, ok=True, status="RETURN_CAPTURED")
