from pathlib import Path

from kernel.ion_temporal_context_enforcement_audit import (
    build_temporal_context_enforcement_audit,
    write_temporal_context_enforcement_audit,
)


def _write(root: Path, rel: str, text: str = "x\n") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_temporal_context_audit_detects_present_but_partial_enforcement(tmp_path):
    # Minimal representative project with the exact surfaces needed to prove
    # the audit is checking wiring, not inventing new doctrine.
    from kernel.ion_temporal_context_enforcement_audit import TEMPORAL_KERNEL_SURFACES, TEMPORAL_PROTOCOLS

    for rel in TEMPORAL_PROTOCOLS:
        _write(tmp_path, rel)
    for rel in TEMPORAL_KERNEL_SURFACES:
        _write(tmp_path, rel)
    _write(tmp_path, "ION/04_packages/kernel/ion_autonomous_loop.py", "build_context_lifecycle_report\ncontext_lifecycle_report_to_dict\nwrite_context_lifecycle_report\n")
    _write(tmp_path, "ION/03_registry/context_lifecycle_policy.yaml")
    _write(tmp_path, "ION/tests/test_kernel_ion_context_lifecycle.py")

    audit = build_temporal_context_enforcement_audit(tmp_path, emitted_at="2026-05-02T00:00:00+00:00")
    assert audit.autonomous_loop_binds_context_lifecycle is True
    assert audit.autonomous_loop_writes_context_lifecycle_report is True
    assert audit.packaging_gate_present is False
    assert audit.verdict == "SYSTEM_PRESENT_AND_PARTIALLY_ENFORCED"
    assert "carrier_release_packaging_gate_not_yet_bound_to_context_lifecycle" in audit.findings


def test_temporal_context_audit_detects_v106_lifecycle_package_gate(tmp_path):
    # V106 made lifecycle-aware compact-runtime/forensic-archive packaging real.
    # The V103 audit must detect that current gate, not keep looking only for
    # older candidate release-packager filenames.
    from kernel.ion_temporal_context_enforcement_audit import TEMPORAL_KERNEL_SURFACES, TEMPORAL_PROTOCOLS

    for rel in TEMPORAL_PROTOCOLS:
        _write(tmp_path, rel)
    for rel in TEMPORAL_KERNEL_SURFACES:
        _write(tmp_path, rel)
    _write(tmp_path, "ION/04_packages/kernel/ion_autonomous_loop.py", "build_context_lifecycle_report\ncontext_lifecycle_report_to_dict\nwrite_context_lifecycle_report\n")
    _write(
        tmp_path,
        "ION/04_packages/kernel/ion_lifecycle_packager.py",
        "build_context_lifecycle_report\nexcluded_forensic_context\nCOMPACT_RUNTIME\nFORENSIC_ARCHIVE\naudit_zip_root\n",
    )
    _write(tmp_path, "ION/03_registry/ion_lifecycle_package_manifest.schema.json")
    _write(tmp_path, "ION/03_registry/context_lifecycle_policy.yaml")
    _write(tmp_path, "ION/tests/test_kernel_ion_context_lifecycle.py")
    _write(tmp_path, "ION/tests/test_kernel_ion_lifecycle_packager.py")
    _write(tmp_path, "ION/tests/test_kernel_temporal_model.py")

    audit = build_temporal_context_enforcement_audit(tmp_path, emitted_at="2026-05-02T00:00:00+00:00")

    assert audit.packaging_gate_present is True
    assert audit.verdict == "SYSTEM_PRESENT_AND_ENFORCED"
    assert "carrier_release_packaging_gate_bound_to_context_lifecycle" in audit.findings
    assert "carrier_release_packaging_gate_not_yet_bound_to_context_lifecycle" not in audit.findings
    assert any(surface.category == "lifecycle_packaging_gate" for surface in audit.surfaces)


def test_temporal_context_audit_writes_report_without_mutation(tmp_path):
    _write(tmp_path, "ION/04_packages/kernel/ion_autonomous_loop.py", "")
    audit = build_temporal_context_enforcement_audit(tmp_path, emitted_at="2026-05-02T00:00:00+00:00")
    path = write_temporal_context_enforcement_audit(tmp_path, audit)
    assert path.exists()
    assert audit.mutation_performed is False
    assert (tmp_path / "ION/05_context/signals/v103_temporal_context_enforcement_reconciliation_receipt_20260502.txt").exists()
