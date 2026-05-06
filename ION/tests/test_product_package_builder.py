from __future__ import annotations

import importlib.util
import json
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
    assert (out / "ION_ENGINE/doctrine/ION_CORE.md").exists()
    assert (out / "ION_ENGINE/reference/ION_FUNDAMENTALS.md").exists()
    assert (out / "ION_DATA_SCHEMA/schemas/ion_data_manifest.schema.json").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/GPT_INSTRUCTIONS.md").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/STARTUP_BEHAVIOR.md").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/STATE_UPDATE_PROTOCOL.md").exists()
    assert (out / "ION_CUSTOM_GPT_ADAPTER/templates/MOUNT_REPORT_TEMPLATE.md").exists()
    assert (out / "ION_STARTER_DATA/ION_DATA_MANIFEST.json").exists()
    assert (out / "ION_STARTER_DATA/PACKETS/open_packets.json").exists()
    assert (out / "ION_STARTER_DATA/DECISIONS/decision_ledger.json").exists()
    assert (out / "ION_STARTER_DATA/ARTIFACTS/artifact_manifest.json").exists()
    assert (out / "tools/validate_data_package.py").exists()
    assert (out / "tools/build_starter_zip.py").exists()
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
    assert packets["schema_id"] == "ion.open_packets.v1"
    assert decisions["schema_id"] == "ion.decision_ledger.v1"
    assert artifacts["schema_id"] == "ion.artifact_manifest.v1"
