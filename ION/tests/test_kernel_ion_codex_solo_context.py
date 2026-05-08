import json
from pathlib import Path

from kernel.ion_codex_solo_context import (
    BLOCKED_VERDICT,
    CAPSULE_PATH,
    CONTEXT_PACKAGES_PATH,
    HOT_CONTEXT_PATH,
    LONG_HORIZON_PATH,
    MAX_MINI_LINES,
    MINI_PATH,
    READY_VERDICT,
    WRITE_CONFIRMATION_TOKEN,
    build_codex_solo_context_model,
    build_codex_solo_boot_context,
    compile_codex_solo_long_horizon,
    initialize_codex_solo_context,
    main,
    record_codex_solo_post,
    render_codex_solo_mini,
    validate_codex_solo_route,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    for rel, text in {
        "ION/REPO_AUTHORITY.md": "# authority\n",
        "ION/03_registry/agent_context_system_registry.yaml": "legacy_surfaces_policy: {}\n",
        "ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_OPERATING_CONTEXT_V105.md": "# lead\n",
        "ION/06_intelligence/research/2026-05-07_codex_single_agent_mini_capsule_research.md": "# research\n",
        "ION/02_architecture/CODEX_CAPSULE_OPERATING_PROTOCOL.md": "# capsule operating protocol\n",
        "ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md": "# skill activation protocol\n",
        "ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md": "# chat engine protocol\n",
        "ION/03_registry/ion_skill_registry.yaml": "schema_id: ion.skill_registry.v1\nproduction_authority: false\nlive_execution_authority: false\nsecrets_authority: false\nskills: []\n",
        "ION/03_registry/ion_native_lens_registry.yaml": "schema_id: ion.native_lens_registry.v1\nproduction_authority: false\nlive_execution_authority: false\nsecrets_authority: false\nlenses: []\n",
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md": "# orchestration\n",
        "ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md": "# ui orchestration\n",
    }.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def test_initialize_codex_solo_context_writes_compact_surfaces(tmp_path: Path):
    _seed_root(tmp_path)

    model = initialize_codex_solo_context(tmp_path)

    assert model["verdict"] == READY_VERDICT
    assert (tmp_path / MINI_PATH).exists()
    assert (tmp_path / CAPSULE_PATH).exists()
    assert (tmp_path / HOT_CONTEXT_PATH).exists()
    assert (tmp_path / LONG_HORIZON_PATH).exists()
    assert (tmp_path / CONTEXT_PACKAGES_PATH).exists()
    assert model["mini"]["line_count"] <= MAX_MINI_LINES
    assert model["active_context"]["minimum_context_path"] == CAPSULE_PATH.as_posix()
    assert model["active_context"]["long_horizon_path"] == LONG_HORIZON_PATH.as_posix()
    assert model["capsule"]["minimum_context"] is True
    assert model["context_packages"]["package_count"] >= 6
    assert model["production_authority"] is False
    assert model["live_execution_authority"] is False
    hot_context = (tmp_path / HOT_CONTEXT_PATH).read_text(encoding="utf-8")
    assert "Codex Solo HOT_CONTEXT" in hot_context
    assert "## MINIMUM WORKING CAPSULE" in hot_context
    assert hot_context.index("## MINIMUM WORKING CAPSULE") < hot_context.index("## MINI LOOKUP INDEX")
    assert "## LONG HORIZON CAPSULE INDEX" in hot_context
    assert "## CONTEXT PACKAGE SELECTOR" in hot_context


def test_mini_renderer_enforces_line_limit_and_indexes_capsule_rows():
    entries = [{"path": f"ION/path_{idx}.md", "required": True} for idx in range(40)]
    capsule_rows = [
        {"id": f"C-{idx:03d}", "date": "2026-05-07", "summary": f"summary {idx}", "status": "DONE"}
        for idx in range(40)
    ]

    mini = render_codex_solo_mini(
        mission="mission",
        phase="phase",
        now="now",
        blocker="none",
        next_action="next",
        active_template="template",
        route_entries=entries,
        capsule_rows=capsule_rows,
    )

    assert len(mini.splitlines()) <= MAX_MINI_LINES
    assert "ROLE: lookup/receipt index" in mini
    assert "C-039" in mini
    assert "C-000" not in mini
    assert "ION/path_0.md" not in mini
    assert "ION/path_39.md" not in mini


def test_route_validation_blocks_missing_required_file(tmp_path: Path):
    _seed_root(tmp_path)
    missing = [{"path": "ION/missing.md", "required": True, "classification": "active_context"}]

    result = validate_codex_solo_route(tmp_path, entries=missing)

    assert result["ok"] is False
    assert "required_route_missing:ION/missing.md" in result["findings"]


def test_route_validation_requires_historical_label_for_absolute_paths(tmp_path: Path):
    _seed_root(tmp_path)
    entries = [{"path": "/home/sev/old/MINI.md", "required": False, "classification": "active_context"}]

    result = validate_codex_solo_route(tmp_path, entries=entries)

    assert result["ok"] is False
    assert "absolute_route_requires_historical_witness:/home/sev/old/MINI.md" in result["findings"]


def test_record_post_appends_capsule_and_updates_mini(tmp_path: Path):
    _seed_root(tmp_path)
    initialize_codex_solo_context(tmp_path)

    result = record_codex_solo_post(
        tmp_path,
        summary="Queued a compact Codex solo work unit",
        evidence_paths=["ION/example_receipt.json"],
        status="QUEUED",
        next_action="Wait for task return",
    )

    capsule = (tmp_path / CAPSULE_PATH).read_text(encoding="utf-8")
    mini = (tmp_path / MINI_PATH).read_text(encoding="utf-8")
    assert result["capsule_entry_id"] == "C-001"
    assert "| C-001 |" in capsule
    assert "Queued a compact Codex solo work unit" in capsule
    assert "ROLE: lookup/receipt index" in mini
    assert "LAST_RECEIPT: Queued a compact Codex solo work unit" in mini
    assert "NEXT: Wait for task return" in mini


def test_boot_context_is_read_only_and_capsule_first(tmp_path: Path):
    _seed_root(tmp_path)
    initialize_codex_solo_context(tmp_path)
    history_before = sorted((tmp_path / "ION/05_context/current/codex_solo/history").glob("*"))

    result = build_codex_solo_boot_context(tmp_path, max_bytes=4096)

    history_after = sorted((tmp_path / "ION/05_context/current/codex_solo/history").glob("*"))
    assert result["schema_id"] == "ion.codex_solo_boot_context.v1"
    assert result["ok"] is True
    assert "ION Codex Solo Boot Context" in result["context"]
    assert "## Loaded HOT_CONTEXT" in result["context"]
    assert "## MINIMUM WORKING CAPSULE" in result["context"]
    assert history_after == history_before


def test_cli_status_and_boot_context_emit_expected_output(tmp_path: Path, capsys):
    _seed_root(tmp_path)
    initialize_codex_solo_context(tmp_path)

    assert main(["--ion-root", str(tmp_path), "status", "--json"]) == 0
    status_payload = json.loads(capsys.readouterr().out)
    assert status_payload["verdict"] == READY_VERDICT

    assert main(["--ion-root", str(tmp_path), "boot-context", "--max-bytes", "4096"]) == 0
    output = capsys.readouterr().out
    assert "ION Codex Solo Boot Context" in output
    assert "Treat Capsule as minimum working context" in output


def test_cli_post_requires_confirmation(tmp_path: Path, capsys):
    _seed_root(tmp_path)
    initialize_codex_solo_context(tmp_path)

    result = main([
        "--ion-root",
        str(tmp_path),
        "post",
        "--summary",
        "Attempt without confirmation",
        "--confirmation",
        "wrong",
        "--json",
    ])

    payload = json.loads(capsys.readouterr().out)
    assert result == 3
    assert payload["ok"] is False
    assert payload["required_confirmation"] == WRITE_CONFIRMATION_TOKEN


def test_cli_post_records_capsule_receipt(tmp_path: Path, capsys):
    _seed_root(tmp_path)
    initialize_codex_solo_context(tmp_path)

    result = main([
        "--ion-root",
        str(tmp_path),
        "post",
        "--summary",
        "Recorded Codex session receipt",
        "--evidence",
        "ION/example.md",
        "--status",
        "IMPLEMENTED",
        "--confirmation",
        WRITE_CONFIRMATION_TOKEN,
        "--json",
    ])

    payload = json.loads(capsys.readouterr().out)
    capsule = (tmp_path / CAPSULE_PATH).read_text(encoding="utf-8")
    assert result == 0
    assert payload["ok"] is True
    assert payload["capsule_entry_id"] == "C-001"
    assert "Recorded Codex session receipt" in capsule
    assert "ION/example.md" in capsule


def test_long_horizon_groups_capsule_rows_into_epochs(tmp_path: Path):
    _seed_root(tmp_path)
    initialize_codex_solo_context(tmp_path)
    for idx in range(23):
        record_codex_solo_post(
            tmp_path,
            summary=f"Completed unit {idx}",
            evidence_paths=[f"ION/evidence_{idx}.json"],
            status="DONE",
        )

    long_horizon = compile_codex_solo_long_horizon(tmp_path, write=True)

    assert long_horizon["capsule_entry_count"] == 23
    assert long_horizon["epoch_count"] == 3
    assert long_horizon["epochs"][0]["row_start"] == "C-001"
    assert long_horizon["epochs"][-1]["row_end"] == "C-023"
    assert (tmp_path / LONG_HORIZON_PATH).exists()


def test_model_reports_blocked_when_default_route_missing(tmp_path: Path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    model = build_codex_solo_context_model(tmp_path)

    assert model["verdict"] == BLOCKED_VERDICT
    assert model["ok"] is False
