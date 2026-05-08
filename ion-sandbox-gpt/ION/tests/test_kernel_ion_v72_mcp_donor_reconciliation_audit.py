from pathlib import Path

from kernel.ion_v72_mcp_donor_reconciliation_audit import (
    CURRENT_TRUNK_MCP_SURFACES,
    FORBIDDEN_DONOR_RUNTIME_PREFIXES,
    REQUIRED_DONOR_SURFACES,
    build_v72_mcp_donor_reconciliation_audit,
)


def seed_required(root: Path):
    for rel in REQUIRED_DONOR_SURFACES + CURRENT_TRUNK_MCP_SURFACES:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("seed\n", encoding="utf-8")


def test_v72_mcp_donor_reconciliation_passes_when_required_surfaces_exist(tmp_path):
    seed_required(tmp_path)

    audit = build_v72_mcp_donor_reconciliation_audit(
        tmp_path,
        generated_at="2026-05-02T00:00:00+00:00",
    )

    assert audit.schema_id == "ion.v72_mcp_donor_reconciliation_audit.v1"
    assert audit.reconciliation_verdict == "V72_MCP_DONOR_RECONCILIATION_PASS"
    assert audit.missing_donor_surface_count == 0
    assert audit.forbidden_runtime_file_count == 0
    assert audit.production_authority is False
    assert audit.live_execution_authority is False


def test_v72_mcp_donor_reconciliation_blocks_missing_surface(tmp_path):
    seed_required(tmp_path)
    (tmp_path / REQUIRED_DONOR_SURFACES[0]).unlink()

    audit = build_v72_mcp_donor_reconciliation_audit(
        tmp_path,
        generated_at="2026-05-02T00:00:00+00:00",
    )

    assert audit.reconciliation_verdict == "V72_MCP_DONOR_RECONCILIATION_REVIEW_REQUIRED"
    assert REQUIRED_DONOR_SURFACES[0] in audit.missing_donor_surfaces


def test_v72_mcp_donor_reconciliation_blocks_hot_runtime_receipt_restore(tmp_path):
    seed_required(tmp_path)
    runtime_file = tmp_path / FORBIDDEN_DONOR_RUNTIME_PREFIXES[0] / "sessions" / "old.json"
    runtime_file.parent.mkdir(parents=True, exist_ok=True)
    runtime_file.write_text("{}\n", encoding="utf-8")

    audit = build_v72_mcp_donor_reconciliation_audit(
        tmp_path,
        generated_at="2026-05-02T00:00:00+00:00",
    )

    assert audit.reconciliation_verdict == "V72_MCP_DONOR_RECONCILIATION_REVIEW_REQUIRED"
    assert audit.forbidden_runtime_file_count == 1
    assert audit.donor_runtime_receipts_restored is True


def test_current_repository_has_restored_v72_mcp_donor_surfaces():
    repo = Path(__file__).resolve().parents[2]
    audit = build_v72_mcp_donor_reconciliation_audit(repo)

    assert audit.reconciliation_verdict == "V72_MCP_DONOR_RECONCILIATION_PASS"
    assert audit.local_bridge_present is True
    assert audit.client_certification_present is True
    assert audit.transport_preview_present is True
    assert audit.hosted_auth_alpha_present is True
    assert audit.cursor_bridge_preserved is True
