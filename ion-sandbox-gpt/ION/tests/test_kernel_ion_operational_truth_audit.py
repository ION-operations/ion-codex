from kernel.ion_operational_truth_audit import build_operational_truth_audit, write_operational_truth_audit


def _minimal_root(tmp_path):
    (tmp_path / "ION/05_context/current/agent_context_systems").mkdir(parents=True)
    (tmp_path / "ION/04_packages/kernel").mkdir(parents=True)
    (tmp_path / "ION/05_context/signals").mkdir(parents=True)
    (tmp_path / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/REPO_AUTHORITY.md").write_text("authority\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='ion-test'\n", encoding="utf-8")
    return tmp_path


def test_operational_truth_audit_detects_missing_active_state(tmp_path):
    root = _minimal_root(tmp_path)
    audit = build_operational_truth_audit(root, emitted_at="2026-05-02T00:00:00+00:00")
    assert audit.schema_id == "ion.operational_truth_audit.v104"
    assert audit.production_authority is False
    assert audit.open_blocker_count >= 1
    assert any(check.check_id == "active_state_surface" and check.status == "BLOCKER" for check in audit.checks)


def test_operational_truth_audit_writes_report_for_current_shape(tmp_path):
    root = _minimal_root(tmp_path)
    # enough active-state shell to prove report writing without claiming readiness
    for rel in [
        "ACTIVE_WORK_PACKET.json",
        "ACTIVE_ROLE_SPAWN_PLAN.json",
        "ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json",
        "ACTIVE_COCKPIT_VIEW_MODEL.json",
        "ACTIVE_HUMAN_GATE_QUEUE.json",
        "ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
    ]:
        (root / "ION/05_context/current" / rel).write_text("{}\n", encoding="utf-8")
    path = write_operational_truth_audit(root, build_operational_truth_audit(root, emitted_at="2026-05-02T00:00:00+00:00"))
    assert path.exists()
    assert (root / "ION/05_context/signals/v104_operational_truth_audit_receipt_20260502.txt").exists()
