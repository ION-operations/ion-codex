"""V74 — Template substrate and optional restoration provenance audit."""

from __future__ import annotations

from pathlib import Path
from typing import Any


_STEWARD_BINDINGS = (
    "ION/07_templates/bindings/STEWARD__TASK.md",
    "ION/07_templates/bindings/STEWARD__STATUS_REPORT.md",
    "ION/07_templates/bindings/STEWARD__PROPOSAL.md",
)

_ACTION_SURFACES = (
    "ION/07_templates/actions/CURSOR_HANDOFF.md",
    "ION/07_templates/actions/MANUAL_AUTOMATION_FALLBACK.md",
)

_PROVENANCE_REL = "ION/docs/consolidation/TEMPLATE_RESTORATION_PROVENANCE_MANIFEST.md"


def _template_file_count(tdir: Path) -> int:
    if not tdir.is_dir():
        return 0
    return sum(1 for p in tdir.rglob("*") if p.is_file())


def _find_template_development_path(root: Path) -> str | None:
    tdir = root / "ION/07_templates"
    if not tdir.is_dir():
        return None
    for p in tdir.rglob("TEMPLATE_DEVELOPMENT.md"):
        if p.is_file():
            return str(p.relative_to(root))
    return None


def _restoration_rows_in_manifest(text: str) -> bool:
    return "status:" in text.lower() and "restored" in text.lower()


def _mini_capsule_only_substrate(tdir: Path, file_count: int) -> bool:
    """True when ``07_templates`` looks like MINI/CAPSULE-only filler (not lawful substrate)."""

    if not tdir.is_dir() or file_count == 0:
        return False
    names = {p.name.lower() for p in tdir.rglob("*") if p.is_file()}
    junk = names <= {"mini.md", "capsule.md", "readme.md"}
    actions_ok = (tdir / "actions").is_dir() and any((tdir / "actions").iterdir())
    bindings_ok = (tdir / "bindings").is_dir() and any((tdir / "bindings").iterdir())
    if actions_ok and bindings_ok:
        return False
    if file_count <= 4 and junk:
        return True
    if file_count <= 2:
        return True
    return False


def audit_v74_template_binding_restoration(root: Path) -> dict[str, Any]:
    root = root.resolve()
    tdir = root / "ION/07_templates"
    file_count = _template_file_count(tdir)
    template_dev_rel = _find_template_development_path(root)

    steward_status: dict[str, str] = {}
    for rel in _STEWARD_BINDINGS:
        p = root / rel
        steward_status[rel] = "present" if p.is_file() else "needs_review"

    action_status: dict[str, str] = {}
    for rel in _ACTION_SURFACES:
        p = root / rel
        action_status[rel] = "present" if p.is_file() else "missing"

    mini_capsule_substitute = _mini_capsule_only_substrate(tdir, file_count)

    manifest_path = root / _PROVENANCE_REL
    manifest_exists = manifest_path.is_file()
    restoration_evidence = manifest_exists and _restoration_rows_in_manifest(
        manifest_path.read_text(encoding="utf-8", errors="replace")
    )
    provenance_manifest_ok = (not restoration_evidence) or manifest_exists

    steward_required_ok = all(v == "present" for v in steward_status.values())
    handoff_ok = action_status.get(_ACTION_SURFACES[0]) == "present"
    manual_fallback_ok = action_status.get(_ACTION_SURFACES[1]) == "present"

    template_substrate_ok = (
        tdir.is_dir()
        and file_count > 0
        and not mini_capsule_substitute
        and steward_required_ok
        and handoff_ok
        and manual_fallback_ok
    )

    return {
        "audit_id": "v74_template_binding_restoration",
        "root": str(root),
        "templates_dir_exists": tdir.is_dir(),
        "template_file_count": file_count,
        "template_development_path": template_dev_rel,
        "template_development_ok": template_dev_rel is not None,
        "steward_bindings": steward_status,
        "action_surfaces": action_status,
        "mini_capsule_substitute_detected": mini_capsule_substitute,
        "provenance_manifest_path": _PROVENANCE_REL if manifest_exists else None,
        "provenance_manifest_ok": provenance_manifest_ok,
        "restoration_evidence_in_manifest": restoration_evidence,
        "production_authority": False,
        "live_execution_authorized": False,
        "template_substrate_ok": template_substrate_ok,
    }
