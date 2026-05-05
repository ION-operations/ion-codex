from pathlib import Path

from kernel.ion_cursor_canonical_workflow_audit import audit_cursor_canonical_workflow


def test_cursor_canonical_workflow_audit_accepts_repo_root():
    root = Path(__file__).resolve().parents[2]
    result = audit_cursor_canonical_workflow(root)
    assert result.accepted, result
    assert result.status == "ION_CURSOR_CANONICAL_WORKFLOW_READY"
