"""V46 local visual harness prototype.

This module gives the Visual Agent line a bounded local/dev-only capture surface.
It hashes and references explicitly supplied local visual artifacts, then composes
V44 visual observation and V45 visual diagnosis objects. It does not drive an
unrestricted browser, use credentials, submit forms, mutate DOM persistently, or
claim production authority.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from .visual_observation_packet import build_visual_observation_packet
from .visual_diagnosis_receipt import build_visual_diagnosis_receipt, build_browser_harness_plan

SCHEMA_ID = "ion.local_visual_harness_capture.v1"
VERSION = "V46_LOCAL_VISUAL_HARNESS_PROTOTYPE"
DEFAULT_REPORT_DIR = "ION/05_context/history/visual_harness_reports"

ALLOWED_TARGET_KINDS = (
    "local_html",
    "local_preview",
    "local_static_file",
    "authorized_local_url_placeholder",
)
ALLOWED_CAPTURE_MODES = (
    "SCREENSHOT_REF",
    "DOM_SNAPSHOT_FILE",
    "VIEWPORT_METADATA",
    "ACCESSIBILITY_TREE_FILE",
    "CONSOLE_LOG_SUMMARY_FILE",
    "COMPOSED_LOCAL_CAPTURE",
)
STEWARD_GATE_STATUSES = ("APPROVED_LOCAL_DEV_ONLY", "STEWARD_REVIEW_REQUIRED", "BLOCKED")

FORBIDDEN_CAPABILITIES: dict[str, bool] = {
    "unrestricted_browser_control": False,
    "credential_sensitive_action": False,
    "destructive_action": False,
    "form_submission": False,
    "purchase_or_submission": False,
    "account_operation": False,
    "persistent_dom_mutation_without_authority": False,
    "network_side_effects": False,
    "production_authority": False,
}

@dataclass(frozen=True)
class LocalVisualArtifact:
    artifact_type: str
    path: str
    sha256: str
    size_bytes: int
    evidence_ref: str

@dataclass(frozen=True)
class LocalVisualHarnessCapture:
    schema_id: str
    version: str
    capture_id: str
    emitted_at: str
    target: str
    target_kind: str
    viewport: str | None
    capture_modes: tuple[str, ...]
    artifacts: tuple[LocalVisualArtifact, ...]
    visual_observation_packet_id: str | None
    visual_diagnosis_receipt_id: str | None
    authority_scope: str
    steward_gate_required: bool
    steward_gate_status: str
    harness_verdict: str
    production_authority: bool = False
    forbidden_capabilities: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CAPABILITIES))


def build_local_visual_harness_capture(
    *,
    workspace_root: str | Path,
    target: str,
    target_kind: str = "local_preview",
    viewport: str | None = "1440x900",
    capture_modes: Iterable[str] = ("COMPOSED_LOCAL_CAPTURE",),
    screenshot_path: str | Path | None = None,
    dom_snapshot_path: str | Path | None = None,
    accessibility_tree_path: str | Path | None = None,
    console_log_summary_path: str | Path | None = None,
    steward_gate_status: str = "APPROVED_LOCAL_DEV_ONLY",
    emitted_at: str | None = None,
) -> LocalVisualHarnessCapture:
    if target_kind not in ALLOWED_TARGET_KINDS:
        raise ValueError(f"invalid target_kind: {target_kind}")
    modes = tuple(capture_modes)
    invalid_modes = [mode for mode in modes if mode not in ALLOWED_CAPTURE_MODES]
    if invalid_modes:
        raise ValueError(f"invalid capture_modes: {invalid_modes}")
    if steward_gate_status not in STEWARD_GATE_STATUSES:
        raise ValueError(f"invalid steward_gate_status: {steward_gate_status}")

    timestamp = emitted_at or _utc_now()
    root = Path(workspace_root).resolve()

    artifact_specs = (
        ("screenshot", screenshot_path),
        ("dom_snapshot", dom_snapshot_path),
        ("accessibility_tree", accessibility_tree_path),
        ("console_log_summary", console_log_summary_path),
    )
    artifacts: list[LocalVisualArtifact] = []
    if steward_gate_status != "BLOCKED":
        for artifact_type, maybe_path in artifact_specs:
            if maybe_path is None:
                continue
            artifacts.append(_artifact_from_path(root, artifact_type, maybe_path))

    observation_packet_id: str | None = None
    diagnosis_receipt_id: str | None = None
    if steward_gate_status != "BLOCKED":
        screenshot_refs = tuple(a.evidence_ref for a in artifacts if a.artifact_type == "screenshot")
        dom_refs = tuple(a.evidence_ref for a in artifacts if a.artifact_type == "dom_snapshot")
        observation = build_visual_observation_packet(
            mode="OBSERVE",
            target=target,
            viewport=viewport,
            screenshot_refs=screenshot_refs,
            dom_refs=dom_refs,
            emitted_at=timestamp,
        )
        harness_plan = build_browser_harness_plan(
            target_scope="authorized local/dev visual target",
            stage="LOCAL_DEV_CAPTURE_DRAFT" if steward_gate_status == "APPROVED_LOCAL_DEV_ONLY" else "STEWARD_REVIEW_REQUIRED",
            emitted_at=timestamp,
        )
        diagnosis = build_visual_diagnosis_receipt(
            target=target,
            observation_packet_ids=[observation.packet_id],
            screenshot_refs=screenshot_refs,
            dom_refs=dom_refs,
            harness_plan=harness_plan,
            emitted_at=timestamp,
        )
        observation_packet_id = observation.packet_id
        diagnosis_receipt_id = diagnosis.receipt_id

    verdict = _verdict(steward_gate_status, tuple(artifacts))
    capture_id = _stable_id("lvh", VERSION, timestamp, target, target_kind, steward_gate_status, str(len(artifacts)), verdict)
    return LocalVisualHarnessCapture(
        schema_id=SCHEMA_ID,
        version=VERSION,
        capture_id=capture_id,
        emitted_at=timestamp,
        target=target,
        target_kind=target_kind,
        viewport=viewport,
        capture_modes=modes,
        artifacts=tuple(artifacts),
        visual_observation_packet_id=observation_packet_id,
        visual_diagnosis_receipt_id=diagnosis_receipt_id,
        authority_scope="LOCAL_DEV_CAPTURE_ONLY",
        steward_gate_required=True,
        steward_gate_status=steward_gate_status,
        harness_verdict=verdict,
        production_authority=False,
        forbidden_capabilities=dict(FORBIDDEN_CAPABILITIES),
    )


def validate_local_visual_harness_capture(capture: LocalVisualHarnessCapture) -> tuple[str, ...]:
    errors: list[str] = []
    if capture.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if capture.version != VERSION:
        errors.append("version mismatch")
    if capture.target_kind not in ALLOWED_TARGET_KINDS:
        errors.append(f"invalid target_kind: {capture.target_kind}")
    for mode in capture.capture_modes:
        if mode not in ALLOWED_CAPTURE_MODES:
            errors.append(f"invalid capture_mode: {mode}")
    if capture.authority_scope != "LOCAL_DEV_CAPTURE_ONLY":
        errors.append("local visual harness authority must remain LOCAL_DEV_CAPTURE_ONLY")
    if capture.steward_gate_required is not True:
        errors.append("local visual harness requires Steward/VZ gate")
    if capture.steward_gate_status not in STEWARD_GATE_STATUSES:
        errors.append(f"invalid steward_gate_status: {capture.steward_gate_status}")
    if capture.production_authority is not False:
        errors.append("local visual harness must not grant production authority")
    for key, allowed in capture.forbidden_capabilities.items():
        if allowed is not False:
            errors.append(f"forbidden capability {key!r} must be false")
    if capture.steward_gate_status == "BLOCKED":
        if capture.artifacts:
            errors.append("blocked harness capture must not include operational artifacts")
        if capture.visual_observation_packet_id or capture.visual_diagnosis_receipt_id:
            errors.append("blocked harness capture must not compose observation/diagnosis IDs")
    elif not capture.artifacts:
        errors.append("approved/review local visual harness capture should include at least one local evidence artifact")
    return tuple(errors)


def write_local_visual_harness_capture(workspace_root: str | Path, capture: LocalVisualHarnessCapture, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{capture.capture_id}.local_visual_harness_capture.json"
    path.write_text(json.dumps(_to_jsonable(capture), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_local_visual_harness_summary(capture: LocalVisualHarnessCapture) -> str:
    return "\n".join([
        f"version: {capture.version}",
        f"capture_id: {capture.capture_id}",
        f"target: {capture.target}",
        f"target_kind: {capture.target_kind}",
        f"artifacts: {len(capture.artifacts)}",
        f"steward_gate_status: {capture.steward_gate_status}",
        f"authority_scope: {capture.authority_scope}",
        f"harness_verdict: {capture.harness_verdict}",
        f"visual_observation_packet_id: {capture.visual_observation_packet_id}",
        f"visual_diagnosis_receipt_id: {capture.visual_diagnosis_receipt_id}",
        f"production_authority: {capture.production_authority}",
    ])


def _artifact_from_path(root: Path, artifact_type: str, path: str | Path) -> LocalVisualArtifact:
    resolved = (root / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"local visual harness path escapes workspace root: {path}") from exc
    if not resolved.exists() or not resolved.is_file():
        raise ValueError(f"local visual harness artifact does not exist: {path}")
    digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
    rel = resolved.relative_to(root).as_posix()
    return LocalVisualArtifact(
        artifact_type=artifact_type,
        path=rel,
        sha256=digest,
        size_bytes=resolved.stat().st_size,
        evidence_ref=f"localfile://{rel}#sha256={digest}",
    )


def _verdict(steward_gate_status: str, artifacts: tuple[LocalVisualArtifact, ...]) -> str:
    if steward_gate_status == "BLOCKED":
        return "LOCAL_VISUAL_HARNESS_BLOCKED_BY_STEWARD"
    if steward_gate_status == "STEWARD_REVIEW_REQUIRED":
        return "LOCAL_VISUAL_HARNESS_REVIEW_REQUIRED"
    if artifacts:
        return "LOCAL_VISUAL_HARNESS_CAPTURE_RECORDED"
    return "LOCAL_VISUAL_HARNESS_NO_ARTIFACTS"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]


def _to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, tuple):
        return [_to_jsonable(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    return obj


def _prepare_demo_files(root: Path) -> tuple[str, str]:
    demo_dir = root / "ION/05_context/sandboxes/local_visual_harness_demo"
    demo_dir.mkdir(parents=True, exist_ok=True)
    screenshot = demo_dir / "demo_screenshot.txt"
    dom = demo_dir / "demo_dom_snapshot.html"
    if not screenshot.exists():
        screenshot.write_text("placeholder screenshot evidence for V46 local/dev harness\n", encoding="utf-8")
    if not dom.exists():
        dom.write_text("<main data-ion-demo='v46'>Local visual harness demo DOM</main>\n", encoding="utf-8")
    return screenshot.relative_to(root).as_posix(), dom.relative_to(root).as_posix()


def _scenario(name: str, workspace_root: str | Path) -> LocalVisualHarnessCapture:
    root = Path(workspace_root).resolve()
    timestamp = "2026-04-25T06:46:00+00:00"
    if name == "blocked":
        return build_local_visual_harness_capture(
            workspace_root=root,
            target="credentialed browser workflow",
            target_kind="authorized_local_url_placeholder",
            steward_gate_status="BLOCKED",
            emitted_at=timestamp,
        )
    screenshot, dom = _prepare_demo_files(root)
    status = "STEWARD_REVIEW_REQUIRED" if name == "review" else "APPROVED_LOCAL_DEV_ONLY"
    return build_local_visual_harness_capture(
        workspace_root=root,
        target="local UI preview",
        target_kind="local_preview",
        viewport="1440x900",
        screenshot_path=screenshot,
        dom_snapshot_path=dom,
        steward_gate_status=status,
        emitted_at=timestamp,
    )


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a V46 local visual harness capture receipt.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--scenario", choices=["capture", "review", "blocked"], default="capture")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    capture = _scenario(args.scenario, args.workspace_root)
    errors = validate_local_visual_harness_capture(capture)
    if args.write:
        print(f"capture_path: {write_local_visual_harness_capture(args.workspace_root, capture)}")
    print(format_local_visual_harness_summary(capture))
    if errors:
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 3 if capture.steward_gate_status == "BLOCKED" else 2
    if capture.steward_gate_status == "BLOCKED":
        return 3
    return 0

if __name__ == "__main__":
    raise SystemExit(_main())
