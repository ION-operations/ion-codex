"""V65 local MCP bridge smoke harness for ION.

This harness exercises the V64 bridge as an external JSON-RPC stdio process.
It is intentionally a validation harness, not a privileged client.

V65 law:
    If an external process can mount ION, it may only observe, plan, submit
    dry-run work, and receive refusal for live execution paths.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any, Mapping

from .ion_mcp_local_bridge import ALLOWED_RESOLUTIONS, VERSION as BRIDGE_VERSION

VERSION = "V65_LOCAL_MCP_CLIENT_CONFIG_AND_SMOKE_HARNESS"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class IonMcpSmokeStep:
    step: str
    ok: bool
    detail: str
    response: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class IonMcpSmokeReport:
    version: str
    bridge_version: str
    created_at: str
    ion_root: str
    state_store_root: str
    passed: bool
    steps: tuple[IonMcpSmokeStep, ...]
    forbidden_resolution_seen: bool = False
    live_execution_authorized_seen: bool = False
    kernel_truth_mutation_seen: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _jsonrpc(message_id: int, method: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
    message: dict[str, Any] = {"jsonrpc": "2.0", "id": message_id, "method": method}
    if params is not None:
        message["params"] = dict(params)
    return message


def _tool_call(message_id: int, name: str, arguments: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return _jsonrpc(message_id, "tools/call", {"name": name, "arguments": dict(arguments or {})})


def _decode_tool_payload(response: Mapping[str, Any]) -> dict[str, Any]:
    result = response.get("result", {})
    content = result.get("content", [])
    if not content:
        return {}
    text = content[0].get("text", "{}")
    try:
        return json.loads(text)
    except Exception:
        return {"decode_error": True, "raw_text": text}


def _write_and_read(proc: subprocess.Popen[str], message: Mapping[str, Any]) -> dict[str, Any]:
    assert proc.stdin is not None
    assert proc.stdout is not None
    proc.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
    proc.stdin.flush()
    raw = proc.stdout.readline()
    if not raw:
        stderr = proc.stderr.read() if proc.stderr is not None else ""
        raise RuntimeError(f"ION MCP smoke harness received no response. stderr={stderr!r}")
    return json.loads(raw)


def run_stdio_smoke(
    ion_root: str | Path,
    state_store_root: str | Path | None = None,
    python_executable: str | None = None,
    package_path: str | Path | None = None,
) -> IonMcpSmokeReport:
    """Run a bounded external-process smoke test against the local bridge."""

    ion_root = Path(ion_root).resolve()
    if ion_root.name != "ION" and (ion_root / "ION").exists():
        ion_root = (ion_root / "ION").resolve()
    if state_store_root is None:
        temp_state = tempfile.TemporaryDirectory()
        state_path = Path(temp_state.name)
    else:
        temp_state = None
        state_path = Path(state_store_root).resolve()
        state_path.mkdir(parents=True, exist_ok=True)

    python_executable = python_executable or sys.executable
    package_path = Path(package_path).resolve() if package_path else (ion_root / "04_packages").resolve()
    env = dict(os.environ)
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(package_path) if not existing_pythonpath else f"{package_path}{os.pathsep}{existing_pythonpath}"

    cmd = [
        python_executable,
        "-m",
        "kernel.ion_mcp_local_bridge",
        "--ion-root",
        str(ion_root),
        "--state-store-root",
        str(state_path),
        "--stdio",
    ]

    steps: list[IonMcpSmokeStep] = []
    forbidden_resolution_seen = False
    live_execution_authorized_seen = False
    kernel_truth_mutation_seen = False

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )
    try:
        init = _write_and_read(proc, _jsonrpc(1, "initialize", {"clientInfo": {"name": "ion-v65-smoke"}}))
        ok = init.get("result", {}).get("serverInfo", {}).get("name") == "ion-mcp-local-bridge"
        steps.append(IonMcpSmokeStep("initialize", ok, "server initialized" if ok else "initialize failed", init))

        tools = _write_and_read(proc, _jsonrpc(2, "tools/list"))
        names = [tool.get("name") for tool in tools.get("result", {}).get("tools", [])]
        ok = "ion.mount" in names and "ion.job.submit_dry_run" in names and "ion.job.execute_live" not in names
        steps.append(IonMcpSmokeStep("tools/list", ok, "tool surface is bounded" if ok else "unexpected tool surface", tools))

        mount = _write_and_read(proc, _tool_call(3, "ion.mount", {"client_name": "ion-v65-smoke", "requested_mode": "dry_run"}))
        mount_payload = _decode_tool_payload(mount)
        session_id = mount_payload.get("session_id")
        ok = mount_payload.get("execution_resolution") == "READ_ONLY" and bool(session_id)
        steps.append(IonMcpSmokeStep("ion.mount", ok, "mounted dry-run session" if ok else "mount failed", mount))

        status = _write_and_read(proc, _tool_call(4, "ion.status", {"session_id": session_id}))
        status_payload = _decode_tool_payload(status)
        ok = status_payload.get("execution_resolution") == "READ_ONLY"
        steps.append(IonMcpSmokeStep("ion.status", ok, "status read-only" if ok else "status failed", status))

        plan = _write_and_read(proc, _tool_call(5, "ion.job.plan", {"session_id": session_id, "task": {"summary": "V65 smoke plan"}}))
        plan_payload = _decode_tool_payload(plan)
        ok = plan_payload.get("execution_resolution") == "DRY_RUN"
        steps.append(IonMcpSmokeStep("ion.job.plan", ok, "dry-run plan returned" if ok else "plan failed", plan))

        submit = _write_and_read(proc, _tool_call(6, "ion.job.submit_dry_run", {"session_id": session_id, "task": {"summary": "V65 smoke submit"}}))
        submit_payload = _decode_tool_payload(submit)
        ok = submit_payload.get("execution_resolution") == "APPROVAL_REQUIRED"
        steps.append(IonMcpSmokeStep("ion.job.submit_dry_run", ok, "dry-run submit queued for approval" if ok else "submit failed", submit))

        live = _write_and_read(proc, _tool_call(7, "ion.job.execute_live", {"session_id": session_id}))
        live_payload = _decode_tool_payload(live)
        ok = live.get("result", {}).get("isError") is True and live_payload.get("execution_resolution") == "REFUSED"
        steps.append(IonMcpSmokeStep("ion.job.execute_live", ok, "live execution refused" if ok else "live execution was not refused", live))

        for payload in (mount_payload, status_payload, plan_payload, submit_payload, live_payload):
            resolution = payload.get("execution_resolution")
            if resolution not in ALLOWED_RESOLUTIONS or resolution == "LIVE_EXECUTED":
                forbidden_resolution_seen = True
            if payload.get("live_execution_authorized"):
                live_execution_authorized_seen = True
            if payload.get("kernel_truth_mutated"):
                kernel_truth_mutation_seen = True

    except Exception as exc:
        steps.append(IonMcpSmokeStep("harness-error", False, str(exc), None))
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        if temp_state is not None:
            temp_state.cleanup()

    passed = all(step.ok for step in steps) and not forbidden_resolution_seen and not live_execution_authorized_seen and not kernel_truth_mutation_seen
    return IonMcpSmokeReport(
        version=VERSION,
        bridge_version=BRIDGE_VERSION,
        created_at=_utc_now(),
        ion_root=str(ion_root),
        state_store_root=str(state_path),
        passed=passed,
        steps=tuple(steps),
        forbidden_resolution_seen=forbidden_resolution_seen,
        live_execution_authorized_seen=live_execution_authorized_seen,
        kernel_truth_mutation_seen=kernel_truth_mutation_seen,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the V65 ION local MCP bridge smoke harness.")
    parser.add_argument("--ion-root", default=".", help="Path to ION/ or snapshot root containing ION/")
    parser.add_argument("--state-store-root", default=None, help="Optional temp/state store root for the smoke run")
    parser.add_argument("--package-path", default=None, help="Optional PYTHONPATH package root, usually ION/04_packages")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args(argv)
    report = run_stdio_smoke(args.ion_root, args.state_store_root, package_path=args.package_path)
    payload = report.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"ION MCP smoke passed: {report.passed}")
        for step in report.steps:
            print(f"- {step.step}: {'OK' if step.ok else 'FAIL'} — {step.detail}")
    return 0 if report.passed else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
