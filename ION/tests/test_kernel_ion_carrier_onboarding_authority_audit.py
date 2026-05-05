from pathlib import Path

from kernel.ion_carrier_onboarding_authority_audit import (
    build_carrier_onboarding_authority_audit,
    write_carrier_onboarding_authority_audit,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    for rel in (
        "ION/02_architecture/ION_CARRIER_ONBOARDING_AUTHORITY_PROTOCOL.md",
        "ION/02_architecture/ION_DEFAULT_CARRIER_ONBOARDING_PROTOCOL.md",
        "ION/02_architecture/ION_CARRIER_RUNTIME_FOUNDATION_PROTOCOL.md",
        "ION/02_architecture/CODEX_EXTENSION_CARRIER_PROTOCOL.md",
        "ION/03_registry/codex_extension_carrier_profile.yaml",
        "ION/03_registry/gpt55_runtime_identity_mount_registry.yaml",
        "ION/03_registry/boots/STEWARD.boot.md",
        "ION/03_registry/boots/RELAY.boot.md",
        "ION/03_registry/boots/MASON.boot.md",
        "ION/03_registry/boots/NEMESIS.boot.md",
        "ION/07_templates/carriers/CARRIER_MOUNT_PROOF.md",
        "ION/07_templates/carriers/CARRIER_SESSION_PACKET.md",
        "ION/07_templates/carriers/CARRIER_CAPABILITY_SURVEY.md",
        "ION/07_templates/carriers/CODEX_EXTENSION_EXECUTION_PACKET.md",
    ):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("authority surface\n", encoding="utf-8")


def test_carrier_onboarding_authority_audit_accepts_registry_template_onboarding_without_root_docs(tmp_path):
    _seed_root(tmp_path)

    audit = build_carrier_onboarding_authority_audit(tmp_path, emitted_at="2026-05-03T00:00:00+00:00")

    assert audit.accepted is True
    assert audit.verdict == "ION_CARRIER_ONBOARDING_AUTHORITY_READY"
    assert audit.authority_surface_present_count == audit.authority_surface_count
    assert audit.optional_root_onboarding_files_present == 0
    assert audit.stale_cursor_root_patterns_present == 0
    assert audit.procedural_root_patterns_present == 0
    assert audit.forbidden_active_root_read_patterns_present == 0
    assert "carrier_registry_template_onboarding_surfaces_present" in audit.findings
    assert "optional_root_onboarding_shims_retired_from_hot_root" in audit.findings


def test_carrier_onboarding_authority_audit_blocks_v94_cursor_root_onboarding(tmp_path):
    _seed_root(tmp_path)
    stale = "# START HERE - ION Cursor Carrier, V94\nRun the V94 CLI spine\nUse `/ion` as the reset-and-run command\n"
    (tmp_path / "START_HERE_FOR_ANY_AGENT.md").write_text(stale, encoding="utf-8")

    audit = build_carrier_onboarding_authority_audit(tmp_path, emitted_at="2026-05-03T00:00:00+00:00")

    assert audit.accepted is False
    assert audit.verdict == "ION_CARRIER_ONBOARDING_AUTHORITY_BLOCKED"
    assert audit.stale_cursor_root_patterns_present > 0
    assert "stale_cursor_root_onboarding_patterns_present" in audit.findings


def test_carrier_onboarding_authority_audit_blocks_procedural_root_onboarding(tmp_path):
    _seed_root(tmp_path)
    procedural = (
        "# Any Agent Start\n\n"
        "## Current Protocol Anchors\n\n"
        "Run `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages "
        "python3 -S -m kernel.ion_status --ion-root . --json`.\n\n"
        "Read ACTIVE_WORK_PACKET and ACTIVE_ROLE_SPAWN_PLAN before work.\n"
    )
    (tmp_path / "AGENTS.md").write_text(procedural, encoding="utf-8")

    audit = build_carrier_onboarding_authority_audit(tmp_path, emitted_at="2026-05-03T00:00:00+00:00")

    assert audit.accepted is False
    assert audit.verdict == "ION_CARRIER_ONBOARDING_AUTHORITY_BLOCKED"
    assert audit.optional_root_onboarding_files_present == 1
    assert audit.procedural_root_patterns_present > 0
    assert "procedural_root_onboarding_patterns_present" in audit.findings


def test_carrier_onboarding_authority_audit_blocks_active_surface_requiring_retired_root_files(tmp_path):
    _seed_root(tmp_path)
    hook = tmp_path / ".cursor/hooks/ion_session_start_persona_mount.py"
    hook.parent.mkdir(parents=True)
    hook.write_text(
        "Read **AGENTS.md** at workspace root and `START_HERE_FOR_ANY_AGENT.md` before work.\n",
        encoding="utf-8",
    )

    audit = build_carrier_onboarding_authority_audit(tmp_path, emitted_at="2026-05-03T00:00:00+00:00")

    assert audit.accepted is False
    assert audit.verdict == "ION_CARRIER_ONBOARDING_AUTHORITY_BLOCKED"
    assert audit.forbidden_active_root_read_patterns_present > 0
    assert "active_surface_requires_retired_root_onboarding" in audit.findings


def test_carrier_onboarding_authority_audit_blocks_repo_authority_start_here_bundle_as_first_read(tmp_path):
    _seed_root(tmp_path)
    (tmp_path / "ION/REPO_AUTHORITY.md").write_text(
        "For workspace-level onboarding, the preferred first surface is now:\n\n"
        "`ION/05_context/exports/2026-04-17_root_authority_bundle/START_HERE.md`\n\n"
        "Use that bundle before either `STATUS.md`.\n",
        encoding="utf-8",
    )

    audit = build_carrier_onboarding_authority_audit(tmp_path, emitted_at="2026-05-03T00:00:00+00:00")

    assert audit.accepted is False
    assert audit.verdict == "ION_CARRIER_ONBOARDING_AUTHORITY_BLOCKED"
    assert audit.forbidden_active_root_read_patterns_present > 0
    assert "active_surface_requires_retired_root_onboarding" in audit.findings


def test_carrier_onboarding_authority_audit_blocks_stale_operator_visible_last_run(tmp_path):
    _seed_root(tmp_path)
    stale_run = tmp_path / "ION/05_context/current/OPERATOR_VISIBLE_LAST_RUN.md"
    stale_run.parent.mkdir(parents=True, exist_ok=True)
    stale_run.write_text(
        "required_read_order:\n"
        "- START_HERE_FOR_ANY_AGENT.md\n"
        "- ION/05_context/exports/2026-04-17_root_authority_bundle/START_HERE.md\n",
        encoding="utf-8",
    )

    audit = build_carrier_onboarding_authority_audit(tmp_path, emitted_at="2026-05-03T00:00:00+00:00")

    assert audit.accepted is False
    assert audit.verdict == "ION_CARRIER_ONBOARDING_AUTHORITY_BLOCKED"
    assert audit.forbidden_active_root_read_patterns_present > 0
    assert "active_surface_requires_retired_root_onboarding" in audit.findings


def test_carrier_onboarding_authority_audit_blocks_stale_tmp_onboard(tmp_path):
    _seed_root(tmp_path)
    tmp_onboard = tmp_path / "ION/05_context/current/_tmp_onboard.json"
    tmp_onboard.parent.mkdir(parents=True, exist_ok=True)
    tmp_onboard.write_text(
        '{"required_read_order":["START_HERE_FOR_ANY_AGENT.md","ION/05_context/exports/2026-04-17_root_authority_bundle/START_HERE.md"]}\n',
        encoding="utf-8",
    )

    audit = build_carrier_onboarding_authority_audit(tmp_path, emitted_at="2026-05-03T00:00:00+00:00")

    assert audit.accepted is False
    assert audit.verdict == "ION_CARRIER_ONBOARDING_AUTHORITY_BLOCKED"
    assert audit.forbidden_active_root_read_patterns_present > 0
    assert "active_surface_requires_retired_root_onboarding" in audit.findings


def test_carrier_onboarding_authority_audit_writes_report(tmp_path):
    _seed_root(tmp_path)

    path = write_carrier_onboarding_authority_audit(tmp_path)

    assert path.exists()
    assert path.name == "CARRIER_ONBOARDING_AUTHORITY_AUDIT_V123.json"
