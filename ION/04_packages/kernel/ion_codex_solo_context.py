"""Single-agent Mini/Capsule context layer for the general Codex chat lane.

This module preserves the useful old SOS-style continuity pattern without
promoting Mini/Capsule text into repo authority. It writes only the current
active ION root and treats historical roots as explicit witness inputs.

Capsule is the minimum working context for this lane. Mini is only a lookup
index and receipt summary for finding capsule history.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SCHEMA_ID = "ion.codex_solo_context.v1"
READY_VERDICT = "ION_CODEX_SOLO_CONTEXT_READY"
BLOCKED_VERDICT = "ION_CODEX_SOLO_CONTEXT_BLOCKED"
WRITE_CONFIRMATION_TOKEN = "ION_BOUNDED_WRITE_CONFIRMED"

CURRENT = Path("ION/05_context/current")
SOLO_DIR = CURRENT / "codex_solo"
HISTORY_DIR = SOLO_DIR / "history"
MINI_PATH = SOLO_DIR / "MINI.md"
CAPSULE_PATH = SOLO_DIR / "CAPSULE.md"
STATUS_PATH = SOLO_DIR / "STATUS.json"
ROUTE_PATH = SOLO_DIR / "ROUTE.json"
HOT_CONTEXT_PATH = SOLO_DIR / "HOT_CONTEXT.md"
LONG_HORIZON_PATH = SOLO_DIR / "LONG_HORIZON.json"
CONTEXT_PACKAGES_PATH = SOLO_DIR / "CONTEXT_PACKAGES.json"
MAX_MINI_LINES = 30
MAX_CAPSULE_CONTEXT_LINES = 80
MAX_CAPSULE_ROWS_PER_EPOCH = 10
MAX_LONG_HORIZON_EPOCHS_IN_HOT_CONTEXT = 6
MAX_ROUTE_EXCERPT_CHARS = 1600
DEFAULT_BOOT_CONTEXT_MAX_BYTES = 24000

WITNESS_POLICY = (
    "Capsule is the minimum working context. Mini is a lookup/receipt index for "
    "capsule history. Neither overrides current repo authority, tests, receipts, "
    "or explicit operator instructions."
)

DEFAULT_ROUTE_ENTRIES: tuple[dict[str, Any], ...] = (
    {
        "path": CAPSULE_PATH.as_posix(),
        "required": True,
        "classification": "codex_solo_minimum_working_context",
        "why": "Minimum context the standalone Codex lane must always carry.",
    },
    {
        "path": MINI_PATH.as_posix(),
        "required": True,
        "classification": "codex_solo_lookup_receipt_index",
        "why": "Lookup index and receipt summary for capsule history.",
    },
    {
        "path": LONG_HORIZON_PATH.as_posix(),
        "required": True,
        "classification": "codex_solo_long_horizon_index",
        "why": "Compressed long-horizon capsule index for older continuity lookup.",
    },
    {
        "path": "ION/REPO_AUTHORITY.md",
        "required": True,
        "classification": "active_repo_authority",
        "why": "Active root authority boundary.",
    },
    {
        "path": "ION/03_registry/agent_context_system_registry.yaml",
        "required": True,
        "classification": "active_context_policy",
        "why": "Current Mini/Capsule witness policy and active context-system registry.",
    },
    {
        "path": "ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_OPERATING_CONTEXT_V105.md",
        "required": True,
        "classification": "active_lead_context",
        "why": "Current lead-dev operating posture.",
    },
    {
        "path": "ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md",
        "required": True,
        "classification": "codex_solo_design",
        "why": "Research basis for this single-agent context lane.",
    },
    {
        "path": "ION/02_architecture/CODEX_CAPSULE_OPERATING_PROTOCOL.md",
        "required": True,
        "classification": "codex_capsule_operating_kernel",
        "why": "Small ION operating kernel for Codex fallback/basic ops.",
    },
    {
        "path": "ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md",
        "required": True,
        "classification": "codex_skill_activation_governance",
        "why": "Defines skills as activation control while templates remain proof law.",
    },
    {
        "path": "ION/03_registry/ion_skill_registry.yaml",
        "required": True,
        "classification": "codex_skill_activation_registry",
        "why": "Active skill registry for Codex chat, ION handoff, recovery, template curation, and receipts.",
    },
    {
        "path": "ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md",
        "required": True,
        "classification": "codex_chat_engine_protocol",
        "why": "Defines the chat-quality engine under the UI: context, skills, native lenses, model route, and response contract.",
    },
    {
        "path": "ION/03_registry/ion_native_lens_registry.yaml",
        "required": True,
        "classification": "codex_chat_native_lens_registry",
        "why": "Maps ION native roles into chat-engine lenses without making them user-facing chores.",
    },
    {
        "path": "ION/02_architecture/CODEX_CARRIER_LIMITS_CONTEXT_PROTOCOL.md",
        "required": True,
        "classification": "codex_carrier_limits_protocol",
        "why": "Defines Codex carrier limits as a first-class context domain and separates local hard limits from dynamic external limits.",
    },
    {
        "path": "ION/03_registry/codex_carrier_limits_registry.yaml",
        "required": True,
        "classification": "codex_carrier_limits_registry",
        "why": "Machine-readable registry for Codex carrier limit classes, sources, and verification requirements.",
    },
    {
        "path": "ION/05_context/current/codex_solo/CODEX_CARRIER_LIMITS_CONTEXT.json",
        "required": True,
        "classification": "codex_carrier_limits_current_context",
        "why": "Current Codex carrier limits snapshot used for context planning and startup audits.",
    },
    {
        "path": "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md",
        "required": True,
        "classification": "codex_capsule_chat_rebuild_orchestration",
        "why": "Active product correction: one Capsule Codex chat with bounded full-ION comms.",
    },
    {
        "path": "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md",
        "required": True,
        "classification": "codex_capsule_chat_ui_orchestration",
        "why": "Chat-first app UI orchestration using JOC/ION drawers and Capsule context.",
    },
    {
        "path": "ION/02_architecture/HELIXION_JOC_DAIMON_WISDOMNET_MASTER_EVOLUTION_PLAN.md",
        "required": True,
        "classification": "helixion_joc_master_evolution_plan",
        "why": "Master evolution plan for Helixion, JOC, ION, dAimon, WisdomNET, extension, queue, and Codex surfaces.",
    },
    {
        "path": "ION/02_architecture/HELIXION_JOC_ORCHESTRATION_WORKFLOW_PROTOCOL.md",
        "required": True,
        "classification": "helixion_joc_orchestration_workflow_protocol",
        "why": "ION-native orchestration law for Helixion/JOC rebuild context, skills, routes, packets, and receipts.",
    },
    {
        "path": "ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_ORCHESTRATION_CONTEXT_PACKAGE.json",
        "required": True,
        "classification": "helixion_joc_orchestration_context_package",
        "why": "Machine-readable context package for future Helixion/JOC rebuild orchestration work.",
    },
    {
        "path": "ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_ORCHESTRATION_CONTEXT_PACKAGE.md",
        "required": True,
        "classification": "helixion_joc_orchestration_context_brief",
        "why": "Human/model-readable briefing for the Helixion/JOC orchestration package.",
    },
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return _now().replace("-", "").replace(":", "").replace("+00:00", "Z")


def _resolve_root(root: str | Path | None = None) -> Path:
    return Path(root or ".").expanduser().resolve()


def _read_text(path: Path, *, fallback: str = "") -> str:
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8", errors="replace")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _clean_line(value: Any, *, limit: int = 180) -> str:
    text = re.sub(r"\s+", " ", str(value or "").replace("|", "/")).strip()
    return text[:limit]


def _route_entries(entries: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None = None) -> list[dict[str, Any]]:
    source = entries if entries is not None else DEFAULT_ROUTE_ENTRIES
    normalized: list[dict[str, Any]] = []
    for entry in source:
        path = _clean_line(entry.get("path"), limit=500)
        if not path:
            continue
        normalized.append({
            "path": path,
            "required": bool(entry.get("required", True)),
            "classification": _clean_line(entry.get("classification") or "active_context", limit=80),
            "why": _clean_line(entry.get("why") or "", limit=220),
        })
    return normalized


def _merge_default_route_entries(entries: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entry in list(DEFAULT_ROUTE_ENTRIES) + list(entries):
        normalized = _route_entries([entry])
        if not normalized:
            continue
        item = normalized[0]
        if item["path"] in seen:
            continue
        seen.add(item["path"])
        merged.append(item)
    return merged


def _entry_path(root: Path, entry: Mapping[str, Any]) -> tuple[Path, bool]:
    raw = Path(str(entry.get("path") or ""))
    if raw.is_absolute():
        return raw, False
    return root / raw, True


def _capsule_seed() -> str:
    return "\n".join([
        "# Codex Solo Capsule",
        "",
        "> Minimum working context for the standalone Codex chat lane. Load this before general Codex work. Mini is only lookup/index; detailed work stays in normal artifacts.",
        "",
        "| # | Date | Summary | Evidence | Status |",
        "|---|------|---------|----------|--------|",
    ])


def _ensure_capsule_contract_text(text: str) -> str:
    if not text.strip():
        return _capsule_seed()
    if "Minimum working context" in text:
        return text
    lines = text.splitlines()
    contract = "> Minimum working context for the standalone Codex chat lane. Load this before general Codex work. Mini is only lookup/index; detailed work stays in normal artifacts."
    for index, line in enumerate(lines):
        if line.startswith("> "):
            lines[index] = contract
            return "\n".join(lines)
    return "\n".join(["# Codex Solo Capsule", "", contract, "", text.rstrip()])


def _capsule_rows(text: str, *, limit: int | None = None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| C-"):
            continue
        parts = [part.strip().strip("`") for part in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        rows.append({
            "id": parts[0],
            "date": parts[1],
            "summary": parts[2],
            "evidence": parts[3],
            "status": parts[4],
        })
    return rows[-limit:] if limit else rows


def _evidence_items(value: str) -> list[str]:
    items: list[str] = []
    for raw in str(value or "").replace("`", "").split(","):
        item = _clean_line(raw, limit=240)
        if item and item != "none" and item not in items:
            items.append(item)
    return items


def _capsule_context_text(text: str) -> str:
    lines = text.splitlines()
    if len(lines) <= MAX_CAPSULE_CONTEXT_LINES:
        return text.rstrip()
    tail = "\n".join(lines[-MAX_CAPSULE_CONTEXT_LINES:]).rstrip()
    return "\n".join([
        f"(Capsule exceeded {MAX_CAPSULE_CONTEXT_LINES} lines; recent active tail shown.)",
        tail,
    ])


def render_codex_solo_mini(
    *,
    mission: str,
    phase: str,
    now: str,
    blocker: str,
    next_action: str,
    active_template: str,
    route_entries: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None = None,
    capsule_rows: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None = None,
) -> str:
    recent_rows = list(capsule_rows or [])[-5:]
    lines = [
        f"CODEX SOLO MINI INDEX | {_now()}",
        "",
        "ROLE: lookup/receipt index; Capsule is the minimum working context.",
        f"ACTIVE_CAPSULE: {CAPSULE_PATH.as_posix()}",
        f"HOT_CONTEXT: {HOT_CONTEXT_PATH.as_posix()}",
        f"LONG_HORIZON: {LONG_HORIZON_PATH.as_posix()}",
        f"PACKAGES: {CONTEXT_PACKAGES_PATH.as_posix()}",
        f"HISTORY: {HISTORY_DIR.as_posix()}",
        "",
        f"MISSION: {_clean_line(mission)}",
        f"PHASE: {_clean_line(phase)}",
        f"LAST_RECEIPT: {_clean_line(now)}",
        f"BLOCKER: {_clean_line(blocker or 'None')}",
        f"NEXT: {_clean_line(next_action)}",
        "",
        f"ACTIVE_TEMPLATE: {_clean_line(active_template or 'CODEX_SOLO_WORK_UNIT')}",
        "",
        "CAPSULE_LOOKUP:",
    ]
    if recent_rows:
        for row in recent_rows:
            capsule_id = _clean_line(row.get("id"), limit=16)
            date = _clean_line(row.get("date"), limit=16)
            status = _clean_line(row.get("status"), limit=32)
            summary = _clean_line(row.get("summary"), limit=110)
            lines.append(f"- {capsule_id} {date} {status}: {summary}")
    else:
        lines.append("- seed: no capsule work rows yet")
    lines.extend([
        "",
        f"ROUTE_INDEX: {ROUTE_PATH.as_posix()} validates active refs.",
        f"POLICY: {WITNESS_POLICY}",
    ])
    if len(lines) > MAX_MINI_LINES:
        raise ValueError(f"Codex solo MINI exceeds {MAX_MINI_LINES} lines")
    return "\n".join(lines)


def validate_codex_solo_route(
    root: str | Path | None = None,
    *,
    entries: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    route = _route_entries(entries)
    findings: list[str] = []
    enriched: list[dict[str, Any]] = []
    for entry in route:
        resolved, repo_relative = _entry_path(shell_root, entry)
        classification = str(entry.get("classification") or "")
        if not repo_relative and classification != "historical_witness":
            findings.append(f"absolute_route_requires_historical_witness:{entry['path']}")
        exists = resolved.exists()
        if entry.get("required") and not exists:
            findings.append(f"required_route_missing:{entry['path']}")
        enriched.append({
            **entry,
            "repo_relative": repo_relative,
            "exists": exists,
            "is_file": resolved.is_file(),
            "bytes": resolved.stat().st_size if exists and resolved.is_file() else None,
            "sha256": _sha256_file(resolved),
        })
    return {
        "schema_id": "ion.codex_solo_route_validation.v1",
        "ok": not findings,
        "findings": findings,
        "route_path": ROUTE_PATH.as_posix(),
        "entries": enriched,
        "production_authority": False,
        "live_execution_authority": False,
    }


def write_codex_solo_route(
    root: str | Path | None = None,
    *,
    entries: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    validation = validate_codex_solo_route(shell_root, entries=entries)
    payload = {
        "schema_id": "ion.codex_solo_route.v1",
        "updated_at": _now(),
        "witness_policy": WITNESS_POLICY,
        "validation": validation,
        "entries": validation["entries"],
        "production_authority": False,
        "live_execution_authority": False,
    }
    _write_json(shell_root / ROUTE_PATH, payload)
    return payload


def initialize_codex_solo_context(
    root: str | Path | None = None,
    *,
    mission: str = "Maintain the primary Codex Capsule chat profile with bounded full-ION comms.",
    phase: str = "solo_context_bootstrap",
    next_action: str = "Load Capsule as minimum context; use Mini only as lookup/index.",
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    (shell_root / HISTORY_DIR).mkdir(parents=True, exist_ok=True)
    if not (shell_root / CAPSULE_PATH).exists():
        _write_text(shell_root / CAPSULE_PATH, _capsule_seed())
    capsule = _ensure_capsule_contract_text(_read_text(shell_root / CAPSULE_PATH, fallback=_capsule_seed()))
    _write_text(shell_root / CAPSULE_PATH, capsule)
    compile_codex_solo_long_horizon(shell_root, write=True)
    _write_text(
        shell_root / MINI_PATH,
        render_codex_solo_mini(
            mission=mission,
            phase=phase,
            now="Codex solo context initialized.",
            blocker="None",
            next_action=next_action,
            active_template="CODEX_SOLO_WORK_UNIT",
            capsule_rows=_capsule_rows(capsule, limit=5),
        ),
    )
    compile_codex_solo_context_packages(shell_root, write=True)
    write_codex_solo_route(shell_root)
    compile_codex_solo_hot_context(shell_root, write=True)
    return build_codex_solo_context_model(shell_root, write=True)


def _load_route_entries_from_disk(root: Path) -> list[dict[str, Any]]:
    payload = _read_json(root / ROUTE_PATH)
    if isinstance(payload, dict) and isinstance(payload.get("entries"), list):
        entries = [entry for entry in payload["entries"] if isinstance(entry, Mapping)]
        return _merge_default_route_entries(entries)
    return _route_entries()


def _tail_lines(text: str, *, limit: int = 18) -> list[str]:
    lines = [line for line in text.splitlines() if line.strip()]
    return lines[-limit:]


def _route_excerpt(root: Path, entry: Mapping[str, Any]) -> str:
    resolved, _repo_relative = _entry_path(root, entry)
    if not resolved.exists() or not resolved.is_file():
        return ""
    text = _read_text(resolved)
    return text[:MAX_ROUTE_EXCERPT_CHARS].rstrip()


def compile_codex_solo_long_horizon(root: str | Path | None = None, *, write: bool = True) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    capsule = _read_text(shell_root / CAPSULE_PATH, fallback=_capsule_seed())
    rows = _capsule_rows(capsule)
    epochs: list[dict[str, Any]] = []
    for index in range(0, len(rows), MAX_CAPSULE_ROWS_PER_EPOCH):
        chunk = rows[index:index + MAX_CAPSULE_ROWS_PER_EPOCH]
        if not chunk:
            continue
        status_counts: dict[str, int] = {}
        evidence_refs: list[str] = []
        for row in chunk:
            status = _clean_line(row.get("status"), limit=80) or "UNKNOWN"
            status_counts[status] = status_counts.get(status, 0) + 1
            for item in _evidence_items(str(row.get("evidence") or "")):
                if item not in evidence_refs:
                    evidence_refs.append(item)
        epochs.append({
            "epoch_id": f"E-{len(epochs) + 1:03d}",
            "row_count": len(chunk),
            "row_start": chunk[0].get("id"),
            "row_end": chunk[-1].get("id"),
            "date_start": chunk[0].get("date"),
            "date_end": chunk[-1].get("date"),
            "status_counts": status_counts,
            "summaries": [
                {
                    "id": row.get("id"),
                    "date": row.get("date"),
                    "summary": _clean_line(row.get("summary"), limit=180),
                    "status": _clean_line(row.get("status"), limit=80),
                }
                for row in chunk[-5:]
            ],
            "evidence_refs": evidence_refs[:20],
        })
    payload = {
        "schema_id": "ion.codex_solo_long_horizon.v1",
        "generated_at": _now(),
        "path": LONG_HORIZON_PATH.as_posix(),
        "source_capsule_path": CAPSULE_PATH.as_posix(),
        "capsule_entry_count": len(rows),
        "epoch_size_rows": MAX_CAPSULE_ROWS_PER_EPOCH,
        "epoch_count": len(epochs),
        "rolling_windows": {
            "active_capsule_context_lines": MAX_CAPSULE_CONTEXT_LINES,
            "mini_lookup_recent_rows": 5,
            "hot_context_recent_epochs": MAX_LONG_HORIZON_EPOCHS_IN_HOT_CONTEXT,
            "route_excerpt_chars": MAX_ROUTE_EXCERPT_CHARS,
        },
        "latest_epochs": epochs[-MAX_LONG_HORIZON_EPOCHS_IN_HOT_CONTEXT:],
        "epochs": epochs,
        "production_authority": False,
        "live_execution_authority": False,
    }
    if write:
        _write_json(shell_root / LONG_HORIZON_PATH, payload)
    return payload


def compile_codex_solo_context_packages(
    root: str | Path | None = None,
    *,
    route_validation: Mapping[str, Any] | None = None,
    long_horizon: Mapping[str, Any] | None = None,
    write: bool = True,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    route_validation = route_validation or validate_codex_solo_route(shell_root, entries=_load_route_entries_from_disk(shell_root))
    long_horizon = long_horizon or compile_codex_solo_long_horizon(shell_root, write=write)
    route_entries = route_validation.get("entries") if isinstance(route_validation.get("entries"), list) else []
    route_paths = [str(entry.get("path")) for entry in route_entries if isinstance(entry, Mapping) and entry.get("path")]
    authority_paths = [
        str(entry.get("path"))
        for entry in route_entries
        if isinstance(entry, Mapping) and str(entry.get("classification") or "").startswith("active_")
    ]
    packages = [
        {
            "package_id": "minimum_working_capsule",
            "context_type": "active_short_horizon",
            "load_policy": "always_inline_first",
            "path_refs": [CAPSULE_PATH.as_posix()],
            "window": {"kind": "line_tail", "max_lines": MAX_CAPSULE_CONTEXT_LINES},
        },
        {
            "package_id": "mini_lookup_index",
            "context_type": "receipt_lookup",
            "load_policy": "index_only_not_primary_prompt",
            "path_refs": [MINI_PATH.as_posix()],
            "window": {"kind": "recent_capsule_rows", "max_rows": 5},
        },
        {
            "package_id": "long_horizon_capsule_index",
            "context_type": "compressed_long_horizon",
            "load_policy": "load_when_older_continuity_or_prior_decisions_matter",
            "path_refs": [LONG_HORIZON_PATH.as_posix()],
            "window": {
                "kind": "epoch_summary",
                "epoch_size_rows": MAX_CAPSULE_ROWS_PER_EPOCH,
                "hot_context_recent_epochs": MAX_LONG_HORIZON_EPOCHS_IN_HOT_CONTEXT,
                "epoch_count": long_horizon.get("epoch_count", 0),
            },
        },
        {
            "package_id": "active_authority_package",
            "context_type": "authority_and_policy",
            "load_policy": "always_available_by_route_hash",
            "path_refs": authority_paths,
            "window": {"kind": "route_excerpt", "max_chars_per_file": MAX_ROUTE_EXCERPT_CHARS},
        },
        {
            "package_id": "mission_active_package",
            "context_type": "current_objective",
            "load_policy": "injected_per_queue_or_chat_turn",
            "path_refs": [HOT_CONTEXT_PATH.as_posix()],
            "window": {"kind": "compiled_hot_context", "capsule_first": True},
        },
        {
            "package_id": "route_depth_package",
            "context_type": "route_deeper",
            "load_policy": "use_when_hot_context_is_insufficient",
            "path_refs": [ROUTE_PATH.as_posix(), *route_paths],
            "window": {"kind": "validate_before_queue", "required_missing": route_validation.get("findings", [])},
        },
        {
            "package_id": "evidence_receipt_package",
            "context_type": "proof_and_receipts",
            "load_policy": "use_for_verification_or_claims_about_completed_work",
            "path_refs": [HISTORY_DIR.as_posix()],
            "window": {"kind": "latest_checkpoint_plus_named_evidence", "source": "capsule_row_evidence_refs"},
        },
        {
            "package_id": "recovery_package",
            "context_type": "recovery",
            "load_policy": "use_when_context_drift_or_old_build_comparison_is_requested",
            "path_refs": [HISTORY_DIR.as_posix(), LONG_HORIZON_PATH.as_posix()],
            "window": {"kind": "explicit_operator_or_blocker_triggered"},
        },
        {
            "package_id": "helixion_joc_orchestration_package",
            "context_type": "active_orchestration",
            "load_policy": "use_for_helixion_joc_daimon_wisdomnet_rebuild_work",
            "path_refs": [
                "ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_ORCHESTRATION_CONTEXT_PACKAGE.md",
                "ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_ORCHESTRATION_CONTEXT_PACKAGE.json",
                "ION/02_architecture/HELIXION_JOC_ORCHESTRATION_WORKFLOW_PROTOCOL.md",
                "ION/02_architecture/HELIXION_JOC_DAIMON_WISDOMNET_MASTER_EVOLUTION_PLAN.md",
                "ION/03_registry/helixion_joc_evolution_registry.yaml",
                "ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_REBUILD_CURRENT_PLAN.json",
            ],
            "window": {"kind": "main_context_package", "authority": "planning_control_plane_only"},
        },
    ]
    payload = {
        "schema_id": "ion.codex_solo_context_packages.v1",
        "generated_at": _now(),
        "path": CONTEXT_PACKAGES_PATH.as_posix(),
        "package_count": len(packages),
        "selected_by_default": [
            "minimum_working_capsule",
            "mini_lookup_index",
            "long_horizon_capsule_index",
            "active_authority_package",
            "mission_active_package",
            "route_depth_package",
        ],
        "packages": packages,
        "production_authority": False,
        "live_execution_authority": False,
    }
    if write:
        _write_json(shell_root / CONTEXT_PACKAGES_PATH, payload)
    return payload


def compile_codex_solo_hot_context(root: str | Path | None = None, *, write: bool = True) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    entries = _load_route_entries_from_disk(shell_root)
    route_validation = validate_codex_solo_route(shell_root, entries=entries)
    long_horizon = compile_codex_solo_long_horizon(shell_root, write=write)
    context_packages = compile_codex_solo_context_packages(
        shell_root,
        route_validation=route_validation,
        long_horizon=long_horizon,
        write=write,
    )
    mini = _read_text(shell_root / MINI_PATH)
    capsule = _read_text(shell_root / CAPSULE_PATH)
    sections = [
        "# Codex Solo HOT_CONTEXT",
        "",
        f"generated_at: {_now()}",
        f"witness_policy: {WITNESS_POLICY}",
        "production_authority: false",
        "live_execution_authority: false",
        "",
        "## MINIMUM WORKING CAPSULE",
        "",
        _capsule_context_text(capsule) or "(missing CAPSULE.md)",
        "",
        "## MINI LOOKUP INDEX",
        "",
        mini or "(missing MINI.md)",
        "",
        "## LONG HORIZON CAPSULE INDEX",
        "",
        json.dumps({
            "path": LONG_HORIZON_PATH.as_posix(),
            "capsule_entry_count": long_horizon.get("capsule_entry_count", 0),
            "epoch_count": long_horizon.get("epoch_count", 0),
            "latest_epochs": long_horizon.get("latest_epochs", []),
        }, indent=2, sort_keys=True),
        "",
        "## CONTEXT PACKAGE SELECTOR",
        "",
        json.dumps({
            "path": CONTEXT_PACKAGES_PATH.as_posix(),
            "selected_by_default": context_packages.get("selected_by_default", []),
            "packages": context_packages.get("packages", []),
        }, indent=2, sort_keys=True),
        "",
        "## ROUTE VALIDATION",
        "",
        json.dumps(route_validation, indent=2, sort_keys=True),
        "",
        "## ROUTE EXCERPTS",
    ]
    for entry in route_validation["entries"]:
        sections.extend([
            "",
            f"### {entry['path']}",
            "",
            _route_excerpt(shell_root, entry) or "(missing or non-file route entry)",
        ])
    text = "\n".join(sections).rstrip() + "\n"
    if write:
        _write_text(shell_root / HOT_CONTEXT_PATH, text)
    return {
        "schema_id": "ion.codex_solo_hot_context_compile.v1",
        "ok": bool(route_validation.get("ok")),
        "hot_context_path": HOT_CONTEXT_PATH.as_posix(),
        "bytes": len(text.encode("utf-8")),
        "route_validation": route_validation,
        "long_horizon": {
            "path": LONG_HORIZON_PATH.as_posix(),
            "epoch_count": long_horizon.get("epoch_count", 0),
            "capsule_entry_count": long_horizon.get("capsule_entry_count", 0),
        },
        "context_packages": {
            "path": CONTEXT_PACKAGES_PATH.as_posix(),
            "package_count": context_packages.get("package_count", 0),
            "selected_by_default": context_packages.get("selected_by_default", []),
        },
        "text": text,
        "production_authority": False,
        "live_execution_authority": False,
    }


def _mini_validation(root: Path) -> dict[str, Any]:
    text = _read_text(root / MINI_PATH)
    line_count = len(text.splitlines()) if text else 0
    findings = []
    if not text:
        findings.append("mini_missing")
    if text and "ROLE: lookup/receipt index" not in text:
        findings.append("mini_not_lookup_index")
    if line_count > MAX_MINI_LINES:
        findings.append("mini_line_limit_exceeded")
    return {
        "ok": not findings,
        "line_count": line_count,
        "max_lines": MAX_MINI_LINES,
        "findings": findings,
    }


def _capsule_validation(root: Path) -> dict[str, Any]:
    text = _read_text(root / CAPSULE_PATH)
    findings = []
    if not text:
        findings.append("capsule_missing")
    if text and "Minimum working context" not in text:
        findings.append("capsule_missing_minimum_context_contract")
    rows = _capsule_rows(text)
    return {
        "ok": not findings,
        "entry_count": len(rows),
        "context_line_limit": MAX_CAPSULE_CONTEXT_LINES,
        "findings": findings,
    }


def build_codex_solo_context_model(root: str | Path | None = None, *, write: bool = False) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    if write and (
        not (shell_root / MINI_PATH).exists()
        or not (shell_root / CAPSULE_PATH).exists()
        or not (shell_root / ROUTE_PATH).exists()
        or not (shell_root / LONG_HORIZON_PATH).exists()
        or not (shell_root / CONTEXT_PACKAGES_PATH).exists()
    ):
        return initialize_codex_solo_context(shell_root)
    entries = _load_route_entries_from_disk(shell_root)
    if write:
        compile_codex_solo_long_horizon(shell_root, write=True)
        write_codex_solo_route(shell_root, entries=entries)
        entries = _load_route_entries_from_disk(shell_root)
    route_validation = validate_codex_solo_route(shell_root, entries=entries)
    mini_validation = _mini_validation(shell_root)
    capsule_validation = _capsule_validation(shell_root)
    if write and (not mini_validation.get("ok") or not capsule_validation.get("ok")):
        return initialize_codex_solo_context(shell_root)
    long_horizon = compile_codex_solo_long_horizon(shell_root, write=write)
    context_packages = compile_codex_solo_context_packages(
        shell_root,
        route_validation=route_validation,
        long_horizon=long_horizon,
        write=write,
    )
    hot_compile = compile_codex_solo_hot_context(shell_root, write=write)
    ok = bool(route_validation.get("ok")) and bool(mini_validation.get("ok")) and bool(capsule_validation.get("ok"))
    capsule_text = _read_text(shell_root / CAPSULE_PATH)
    model = {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT if ok else BLOCKED_VERDICT,
        "ok": ok,
        "generated_at": _now(),
        "paths": {
            "dir": SOLO_DIR.as_posix(),
            "mini": MINI_PATH.as_posix(),
            "capsule": CAPSULE_PATH.as_posix(),
            "status": STATUS_PATH.as_posix(),
            "route": ROUTE_PATH.as_posix(),
            "hot_context": HOT_CONTEXT_PATH.as_posix(),
            "long_horizon": LONG_HORIZON_PATH.as_posix(),
            "context_packages": CONTEXT_PACKAGES_PATH.as_posix(),
        },
        "witness_policy": WITNESS_POLICY,
        "active_context": {
            "minimum_context_path": CAPSULE_PATH.as_posix(),
            "minimum_context_kind": "capsule",
            "mini_role": "lookup_receipt_index_not_prompt_source",
            "hot_context_path": HOT_CONTEXT_PATH.as_posix(),
            "long_horizon_path": LONG_HORIZON_PATH.as_posix(),
            "context_packages_path": CONTEXT_PACKAGES_PATH.as_posix(),
        },
        "rolling_windows": {
            "capsule_active_context_lines": MAX_CAPSULE_CONTEXT_LINES,
            "mini_lookup_recent_rows": 5,
            "capsule_rows_per_long_horizon_epoch": MAX_CAPSULE_ROWS_PER_EPOCH,
            "long_horizon_epochs_in_hot_context": MAX_LONG_HORIZON_EPOCHS_IN_HOT_CONTEXT,
            "route_excerpt_chars": MAX_ROUTE_EXCERPT_CHARS,
        },
        "mini": {
            **mini_validation,
            "role": "lookup_receipt_index_for_capsule_history",
            "text": _read_text(shell_root / MINI_PATH),
        },
        "capsule": {
            **capsule_validation,
            "path": CAPSULE_PATH.as_posix(),
            "role": "minimum_working_context",
            "minimum_context": True,
            "tail": _tail_lines(_read_text(shell_root / CAPSULE_PATH), limit=14),
            "recent_rows": _capsule_rows(capsule_text, limit=5),
        },
        "route": route_validation,
        "hot_context": {
            "path": HOT_CONTEXT_PATH.as_posix(),
            "bytes": hot_compile.get("bytes"),
            "ok": hot_compile.get("ok"),
        },
        "long_horizon": {
            "path": LONG_HORIZON_PATH.as_posix(),
            "epoch_count": long_horizon.get("epoch_count", 0),
            "capsule_entry_count": long_horizon.get("capsule_entry_count", 0),
            "latest_epochs": long_horizon.get("latest_epochs", []),
        },
        "context_packages": {
            "path": CONTEXT_PACKAGES_PATH.as_posix(),
            "package_count": context_packages.get("package_count", 0),
            "selected_by_default": context_packages.get("selected_by_default", []),
            "packages": context_packages.get("packages", []),
        },
        "authority": {
            "mini_capsule_authority": "capsule_minimum_context_mini_lookup_index_witness_not_repo_law",
            "production_authority": False,
            "live_execution_authority": False,
        },
        "production_authority": False,
        "live_execution_authority": False,
    }
    if write:
        _write_json(shell_root / STATUS_PATH, model)
    return model


def record_codex_solo_pre(
    root: str | Path | None = None,
    *,
    mission: str,
    now: str,
    evidence: list[str] | tuple[str, ...] = (),
    next_action: str,
    blocker: str = "None",
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    initialize_codex_solo_context(shell_root)
    (shell_root / HISTORY_DIR).mkdir(parents=True, exist_ok=True)
    stamp = _stamp()
    copied: list[str] = []
    for source, suffix in (
        (MINI_PATH, "PRE_MINI.md"),
        (CAPSULE_PATH, "PRE_CAPSULE.md"),
        (LONG_HORIZON_PATH, "PRE_LONG_HORIZON.json"),
        (CONTEXT_PACKAGES_PATH, "PRE_CONTEXT_PACKAGES.json"),
    ):
        src = shell_root / source
        if src.exists():
            dest = shell_root / HISTORY_DIR / f"{stamp}_{suffix}"
            shutil.copy2(src, dest)
            copied.append(dest.relative_to(shell_root).as_posix())
    pre = {
        "schema_id": "ion.codex_solo_pre_checkpoint.v1",
        "checkpoint_id": f"codex_solo_pre_{stamp}",
        "created_at": _now(),
        "mission": _clean_line(mission, limit=260),
        "now": _clean_line(now, limit=260),
        "evidence": [_clean_line(item, limit=400) for item in evidence],
        "next_action": _clean_line(next_action, limit=260),
        "blocker": _clean_line(blocker, limit=260),
        "copied_paths": copied,
        "production_authority": False,
        "live_execution_authority": False,
    }
    path = shell_root / HISTORY_DIR / f"{stamp}_PRE.json"
    _write_json(path, pre)
    pre["path"] = path.relative_to(shell_root).as_posix()
    return pre


def record_codex_solo_post(
    root: str | Path | None = None,
    *,
    summary: str,
    evidence_paths: list[str] | tuple[str, ...] = (),
    status: str = "COMPLETE",
    mission: str = "Maintain the primary Codex Capsule chat profile with bounded full-ION comms.",
    phase: str = "codex_solo_work",
    next_action: str = "Continue from Capsule as minimum context and use Mini for lookup only.",
    blocker: str = "None",
    active_template: str = "CODEX_SOLO_WORK_UNIT",
    route_entries: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...] | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    initialize_codex_solo_context(shell_root)
    route = _route_entries(route_entries or _load_route_entries_from_disk(shell_root))
    capsule = _read_text(shell_root / CAPSULE_PATH, fallback=_capsule_seed())
    row_count = sum(1 for line in capsule.splitlines() if line.startswith("| C-"))
    entry_id = f"C-{row_count + 1:03d}"
    evidence = ", ".join(_clean_line(item, limit=180) for item in evidence_paths) or "none"
    row = f"| {entry_id} | {_now()[:10]} | {_clean_line(summary, limit=220)} | `{evidence}` | {_clean_line(status, limit=40)} |"
    updated_capsule = capsule.rstrip() + "\n" + row
    _write_text(shell_root / CAPSULE_PATH, updated_capsule)
    _write_text(
        shell_root / MINI_PATH,
        render_codex_solo_mini(
            mission=mission,
            phase=phase,
            now=summary,
            blocker=blocker,
            next_action=next_action,
            active_template=active_template,
            route_entries=route,
            capsule_rows=_capsule_rows(updated_capsule, limit=5),
        ),
    )
    write_codex_solo_route(shell_root, entries=route)
    compile_codex_solo_hot_context(shell_root, write=True)
    model = build_codex_solo_context_model(shell_root, write=True)
    post = {
        "schema_id": "ion.codex_solo_post_checkpoint.v1",
        "checkpoint_id": f"codex_solo_post_{_stamp()}",
        "created_at": _now(),
        "capsule_entry_id": entry_id,
        "summary": _clean_line(summary, limit=300),
        "evidence_paths": list(evidence_paths),
        "status": status,
        "model": model,
        "production_authority": False,
        "live_execution_authority": False,
    }
    path = shell_root / HISTORY_DIR / f"{post['checkpoint_id']}.json"
    _write_json(path, post)
    post["path"] = path.relative_to(shell_root).as_posix()
    return post


def _truncate_utf8(text: str, *, max_bytes: int) -> tuple[str, bool]:
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text, False
    suffix = "\n\n[BOOT_CONTEXT_TRUNCATED: load HOT_CONTEXT.md directly for full context]\n"
    keep = max(0, max_bytes - len(suffix.encode("utf-8")))
    trimmed = encoded[:keep].decode("utf-8", errors="ignore").rstrip()
    return trimmed + suffix, True


def build_codex_solo_boot_context(
    root: str | Path | None = None,
    *,
    max_bytes: int = DEFAULT_BOOT_CONTEXT_MAX_BYTES,
) -> dict[str, Any]:
    """Build read-only session-start context for project-scoped Codex hooks."""
    shell_root = _resolve_root(root)
    model = build_codex_solo_context_model(shell_root, write=False)
    hot_context = _read_text(shell_root / HOT_CONTEXT_PATH)
    if not hot_context:
        hot_context = "\n\n".join([
            "# Codex Solo HOT_CONTEXT missing",
            _read_text(shell_root / CAPSULE_PATH, fallback="(missing CAPSULE.md)"),
            _read_text(shell_root / MINI_PATH, fallback="(missing MINI.md)"),
        ])
    startup_recency = {
        "mini": (model.get("mini") or {}).get("text", ""),
        "capsule_entry_count": (model.get("capsule") or {}).get("entry_count", 0),
        "recent_capsule_rows": (model.get("capsule") or {}).get("recent_rows", []),
    }
    sections = [
        "# ION Codex Solo Boot Context",
        "",
        f"active_root: {shell_root}",
        f"schema_id: {SCHEMA_ID}",
        f"verdict: {model.get('verdict')}",
        "production_authority: false",
        "live_execution_authority: false",
        "",
        "## Required Operating Habit",
        "",
        "- Work only in this active root unless the local operator explicitly approves another root.",
        "- Confirm shell root before ION work: `pyproject.toml` and `ION/REPO_AUTHORITY.md` must be siblings.",
        "- Use `ION/REPO_AUTHORITY.md`, `ION/02_architecture/ION_MOUNT_CONTRACT.md`, and carrier packets as authority.",
        "- Treat Capsule as minimum working context and Mini as lookup/receipt index only.",
        "- Do not claim ION identity, STEWARD/RELAY/PERSONA authority, production authority, live execution authority, or secrets authority.",
        "- After material work, record a Codex Solo capsule post with explicit confirmation.",
        "",
        "## Startup Recency Snapshot",
        "",
        json.dumps(startup_recency, indent=2, sort_keys=True),
        "",
        "## Context Paths",
        "",
        json.dumps(model.get("paths", {}), indent=2, sort_keys=True),
        "",
        "## Loaded HOT_CONTEXT",
        "",
        hot_context.rstrip(),
    ]
    text, truncated = _truncate_utf8("\n".join(sections).rstrip() + "\n", max_bytes=max_bytes)
    return {
        "schema_id": "ion.codex_solo_boot_context.v1",
        "ok": bool(model.get("ok")),
        "generated_at": _now(),
        "root": str(shell_root),
        "max_bytes": max_bytes,
        "truncated": truncated,
        "context": text,
        "model_summary": {
            "verdict": model.get("verdict"),
            "paths": model.get("paths", {}),
            "active_context": model.get("active_context", {}),
            "rolling_windows": model.get("rolling_windows", {}),
        },
        "production_authority": False,
        "live_execution_authority": False,
    }


def _print_json(payload: Mapping[str, Any]) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage the ION Codex Solo Capsule context lane.")
    parser.add_argument("--ion-root", default=".", help="Shell root containing pyproject.toml and ION/REPO_AUTHORITY.md")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status", help="Print read-only Codex Solo context status")
    status.add_argument("--json", action="store_true", help="Print JSON output")

    boot = subparsers.add_parser("boot-context", help="Print read-only Codex session boot context")
    boot.add_argument("--max-bytes", type=int, default=DEFAULT_BOOT_CONTEXT_MAX_BYTES, help="Maximum context bytes to emit")
    boot.add_argument("--json", action="store_true", help="Print JSON output")

    post = subparsers.add_parser("post", help="Record an explicit Codex Solo capsule post")
    post.add_argument("--summary", required=True, help="Short summary of completed material work")
    post.add_argument("--evidence", action="append", default=[], help="Evidence path; repeat for multiple paths")
    post.add_argument("--status", default="COMPLETE", help="Capsule row status")
    post.add_argument("--mission", default="Maintain the primary Codex Capsule chat profile with bounded full-ION comms.")
    post.add_argument("--phase", default="codex_solo_work")
    post.add_argument("--next-action", default="Continue from Capsule as minimum context and use Mini for lookup only.")
    post.add_argument("--blocker", default="None")
    post.add_argument("--active-template", default="CODEX_SOLO_WORK_UNIT")
    post.add_argument("--confirmation", required=True, help=f"Required token: {WRITE_CONFIRMATION_TOKEN}")
    post.add_argument("--json", action="store_true", help="Print JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = Path(args.ion_root)
    if args.command == "status":
        payload = build_codex_solo_context_model(root, write=False)
        if args.json:
            _print_json(payload)
        else:
            print(f"{payload.get('verdict')} ok={payload.get('ok')} hot_context={payload.get('paths', {}).get('hot_context')}")
        return 0 if payload.get("ok") else 2
    if args.command == "boot-context":
        payload = build_codex_solo_boot_context(root, max_bytes=max(1024, args.max_bytes))
        if args.json:
            _print_json(payload)
        else:
            print(payload["context"], end="")
        return 0 if payload.get("ok") else 2
    if args.command == "post":
        if args.confirmation != WRITE_CONFIRMATION_TOKEN:
            payload = {
                "ok": False,
                "schema_id": "ion.codex_solo_post_refusal.v1",
                "refusal_class": "CONFIRMATION_REQUIRED",
                "required_confirmation": WRITE_CONFIRMATION_TOKEN,
                "production_authority": False,
                "live_execution_authority": False,
            }
            if args.json:
                _print_json(payload)
            else:
                print(f"Refused: confirmation must be {WRITE_CONFIRMATION_TOKEN}", file=sys.stderr)
            return 3
        payload = record_codex_solo_post(
            root,
            summary=args.summary,
            evidence_paths=args.evidence,
            status=args.status,
            mission=args.mission,
            phase=args.phase,
            next_action=args.next_action,
            blocker=args.blocker,
            active_template=args.active_template,
        )
        payload["ok"] = True
        if args.json:
            _print_json(payload)
        else:
            print(f"{payload['capsule_entry_id']} {payload['path']}")
        return 0
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
