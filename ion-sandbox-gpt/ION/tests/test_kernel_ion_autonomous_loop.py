import json

from kernel.ion_autonomous_loop import run_autonomous_loop


def test_autonomous_loop_survival_slice_writes_state(tmp_path):
    (tmp_path / "ION" / "05_context" / "current" / "agent_context_systems").mkdir(parents=True)
    (tmp_path / "ION" / "REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION" / "REPO_AUTHORITY.md").write_text("authority\n", encoding="utf-8")

    result = run_autonomous_loop(
        ion_root=tmp_path,
        goal="Find one contradiction and propose one patch",
        max_steps=3,
        write=True,
    )
    assert result["status"] == "PASS"
    assert result["steps_integrated"] == 1
    assert (tmp_path / "ION/05_context/current/LAST_ION_AUTONOMOUS_LOOP_RESULT.json").exists()
    assert (tmp_path / "ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json").exists()
    lead_dev_context = tmp_path / "ION/05_context/current/agent_context_systems/LEAD_DEV_ACTIVE_CONTEXT_PACKAGE_V101.md"
    assert lead_dev_context.exists()
    cockpit = json.loads((tmp_path / "ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json").read_text(encoding="utf-8"))
    assert cockpit["active_line"] == "V103_TEMPORAL_CONTEXT_ENFORCEMENT_RECONCILIATION"
    assert cockpit["context_lifecycle_verdict"] in {"PASS_WITH_LIFECYCLE_MODEL", "REVIEW_REQUIRED"}
