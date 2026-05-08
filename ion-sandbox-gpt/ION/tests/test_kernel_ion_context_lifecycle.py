import json
from pathlib import Path

from kernel.ion_context_lifecycle import (
    build_context_lifecycle_report,
    classify_context_artifact,
    write_context_lifecycle_report,
)


def test_context_lifecycle_classifies_hot_warm_quarantine_and_template_proposals(tmp_path):
    root = tmp_path
    current = root / "ION/05_context/current"
    current.mkdir(parents=True)
    (current / "ACTIVE_WORK_PACKET.json").write_text("{}\n", encoding="utf-8")
    (current / "LIFECYCLE_PACKAGE_MANIFEST_COMPACT_RUNTIME_V106.json").write_text("{}\n", encoding="utf-8")
    cycle = current / "execution_cycles/2026-05-02T000000Z0000_demo"
    cycle.mkdir(parents=True)
    (cycle / "receipt.md").write_text("receipt\n", encoding="utf-8")
    tmp_root = current / "_tmp_multi_root_session_08"
    tmp_root.mkdir()
    (tmp_root / "copied_root.txt").write_text("foreign root\n", encoding="utf-8")
    proposals = root / "ION/05_context/history/template_graph_writeback_proposals"
    proposals.mkdir(parents=True)
    (proposals / "p.template_graph_writeback_proposal.json").write_text("{}\n", encoding="utf-8")

    report = build_context_lifecycle_report(root, emitted_at="2026-05-02T00:00:00+00:00")
    classes = {artifact.rel_path: artifact.lifecycle_class for artifact in report.artifacts}
    assert classes["ION/05_context/current/ACTIVE_WORK_PACKET.json"] == "HOT_RUNTIME_STATE"
    assert classes["ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_COMPACT_RUNTIME_V106.json"] == "HOT_RUNTIME_STATE"
    assert classes["ION/05_context/current/execution_cycles"] == "WARM_EXECUTION_EVIDENCE"
    assert classes["ION/05_context/current/_tmp_multi_root_session_08"] == "QUARANTINE_CANDIDATE"
    assert classes["ION/05_context/history/template_graph_writeback_proposals"] == "WARM_OR_COLD_TEMPLATE_PROPOSAL_EVIDENCE"
    assert report.mutation_performed is False


def test_context_lifecycle_writes_report_and_signal_without_mutating_evidence(tmp_path):
    root = tmp_path
    (root / "ION/05_context/current/agent_context_systems").mkdir(parents=True)
    (root / "ION/05_context/current/agent_context_systems/LEAD_DEV.md").write_text("context\n", encoding="utf-8")
    report = build_context_lifecycle_report(root, emitted_at="2026-05-02T00:00:00+00:00")
    path = write_context_lifecycle_report(root, report)
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["schema_id"] == "ion.context_lifecycle_report.v1"
    assert data["mutation_performed"] is False
    assert (root / "ION/05_context/signals/v102_context_metabolism_receipt_20260502.txt").exists()
