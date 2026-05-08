from __future__ import annotations

import importlib.util
import json
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BUILDER_PATH = REPO_ROOT / "ION/09_integrations/product_packager/ion_product_package_builder.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("ion_product_package_builder", BUILDER_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_product_package_builder_creates_required_shape(tmp_path: Path):
    builder = load_builder()
    out = tmp_path / "ION_PRODUCT_PACKAGE"
    result = builder.build_package(out, REPO_ROOT)

    assert result["output_root"] == str(out.resolve())
    assert (out / "README.md").exists()
    assert (out / "PRODUCT_PACKAGE_SPEC.md").exists()
    assert (out / "SOURCE_PROVENANCE.json").exists()
    assert (out / "PRODUCT_SOURCE_MAP.json").exists()
    assert (out / "BUILD_RECEIPT.json").exists()
    assert (out / "ION_ENGINE_COVERAGE_MANIFEST.json").exists()
    assert (out / "ION_ENGINE/doctrine/ION_CORE.md").exists()
    assert (out / "ION_ENGINE/reference/ION_FUNDAMENTALS.md").exists()
    assert (out / "ION_ENGINE/roles/STEWARD.md").exists()
    assert (out / "ION_ENGINE/roles/VIZIER.md").exists()
    assert (out / "ION_ENGINE/templates/PROJECT_INGESTION.md").exists()
    assert (out / "ION_ENGINE/templates/BUILD.md").exists()
    assert (out / "ION_ENGINE/runtime_modes/CUSTOM_GPT_SANDBOX.md").exists()
    assert (out / "ION_ENGINE/runtime_modes/GITHUB_DATA_PLANE.md").exists()
    assert (out / "ION_DATA_SCHEMA/schemas/ion_data_manifest.schema.json").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/GPT_INSTRUCTIONS.md").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/STARTUP_BEHAVIOR.md").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/FIRST_RUN_BEHAVIOR.md").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/PERSONA_INTERFACE_RULES.md").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/STATE_UPDATE_PROTOCOL.md").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/templates/MOUNT_REPORT_TEMPLATE.md").exists()
    assert (out / "ION_STARTER_DATA/ION_DATA_MANIFEST.json").exists()
    assert (out / "ION_STARTER_DATA/PACKETS/open_packets.json").exists()
    assert (out / "ION_STARTER_DATA/DECISIONS/decision_ledger.json").exists()
    assert (out / "ION_STARTER_DATA/ARTIFACTS/artifact_manifest.json").exists()
    assert (out / "ION_STARTER_DATA/PERSONA/persona_state.json").exists()
    assert (out / "ION_DATA_SCHEMA/schemas/persona_interface.schema.json").exists()
    assert (out / "tools/validate_data_package.py").exists()
    assert (out / "tools/build_starter_zip.py").exists()
    assert (out / "tests/test_engine_coverage_manifest.py").exists()
    assert (out / "ION_PRODUCT_DOCS/RUNTIME_BOUNDARY_MATRIX.md").exists()
    assert (out / "dist/ION_CONTINUITY_DATA_BLANK_v1.zip").exists()

    provenance = json.loads((out / "SOURCE_PROVENANCE.json").read_text(encoding="utf-8"))
    assert provenance["authority"] == "generated_projection_not_source_truth"
    assert provenance["source_commit"]


def test_product_package_starter_manifest_is_candidate_state(tmp_path: Path):
    builder = load_builder()
    out = tmp_path / "ION_PRODUCT_PACKAGE"
    builder.build_package(out, REPO_ROOT)

    manifest = json.loads((out / "ION_STARTER_DATA/ION_DATA_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["schema_id"] == "ion.data_manifest.v1"
    assert manifest["authority"] == "portable_data_candidate_not_engine_truth"
    assert manifest["migration_required"] is False

    receipt_lines = (out / "ION_STARTER_DATA/RECEIPTS/receipt_ledger.jsonl").read_text(encoding="utf-8").splitlines()
    assert receipt_lines
    first_receipt = json.loads(receipt_lines[0])
    assert first_receipt["schema_id"] == "ion.receipt.v1"
    assert first_receipt["receipt_type"] == "starter_data_bootstrap"

    packets = json.loads((out / "ION_STARTER_DATA/PACKETS/open_packets.json").read_text(encoding="utf-8"))
    decisions = json.loads((out / "ION_STARTER_DATA/DECISIONS/decision_ledger.json").read_text(encoding="utf-8"))
    artifacts = json.loads((out / "ION_STARTER_DATA/ARTIFACTS/artifact_manifest.json").read_text(encoding="utf-8"))
    persona = json.loads((out / "ION_STARTER_DATA/PERSONA/persona_state.json").read_text(encoding="utf-8"))
    assert packets["schema_id"] == "ion.open_packets.v1"
    assert decisions["schema_id"] == "ion.decision_ledger.v1"
    assert artifacts["schema_id"] == "ion.artifact_manifest.v1"
    assert persona["schema_id"] == "ion.persona_interface.v1"


def test_product_package_starter_state_is_seeded_for_first_run(tmp_path: Path):
    builder = load_builder()
    out = tmp_path / "ION_PRODUCT_PACKAGE"
    builder.build_package(out, REPO_ROOT)

    domains = json.loads((out / "ION_STARTER_DATA/DOMAINS/domain_registry.json").read_text(encoding="utf-8"))
    domain_ids = {domain["domain_id"] for domain in domains["domains"]}
    assert set(builder.SEEDED_DOMAIN_IDS) <= domain_ids

    first_run = (out / "ION_CUSTOM_GPT_ADAPTER/FIRST_RUN_BEHAVIOR.md").read_text(encoding="utf-8")
    assert "What are we working on?" in first_run
    assert "No continuity package is mounted" in first_run
    assert "Do not open with" in first_run


def test_product_package_starter_zip_uses_data_package_root(tmp_path: Path):
    builder = load_builder()
    out = tmp_path / "ION_PRODUCT_PACKAGE"
    result = builder.build_package(out, REPO_ROOT)

    assert result["zip_manifest"]["zip_root"] == "data_package_root"
    with zipfile.ZipFile(out / "dist/ION_CONTINUITY_DATA_BLANK_v1.zip") as archive:
        names = set(archive.namelist())
    assert "ION_DATA_MANIFEST.json" in names
    assert "PERSONA/persona_state.json" in names
    assert "ION_STARTER_DATA/ION_DATA_MANIFEST.json" not in names


def test_product_package_engine_coverage_manifest_paths_exist(tmp_path: Path):
    builder = load_builder()
    out = tmp_path / "ION_PRODUCT_PACKAGE"
    builder.build_package(out, REPO_ROOT)

    manifest = json.loads((out / "ION_ENGINE_COVERAGE_MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["schema_id"] == "ion.product_engine_coverage_manifest.v1"
    assert manifest["counts"]["role_dossiers"] == len(builder.ROLE_DOSSIERS)
    assert manifest["counts"]["template_dossiers"] == len(builder.TEMPLATE_DOCS)
    assert manifest["counts"]["runtime_modes"] == len(builder.RUNTIME_MODES)
    for paths in manifest["required_groups"].values():
        for rel in paths:
            assert (out / rel).exists(), rel

    role_text = (out / "ION_ENGINE/roles/VIZIER.md").read_text(encoding="utf-8")
    assert "Chief Architect" in role_text
    assert "Chief_Architect.Interface.Continuity_Architect" in role_text

    boundary = (out / "ION_PRODUCT_DOCS/RUNTIME_BOUNDARY_MATRIX.md").read_text(encoding="utf-8")
    assert "CUSTOM_GPT_SANDBOX" in boundary
    assert "not the full local ION runtime" in boundary
