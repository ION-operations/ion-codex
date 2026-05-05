import json
import subprocess
from pathlib import Path

from kernel.ion_chatops_bridge import ACTION_SCHEMA, HARD_GATED_INTENTS, SUPPORTED_INTENTS


def test_chatops_schema_registry_names_supported_and_hard_gated_intents():
    text = Path("ION/03_registry/ion_chatops_action.schema.yaml").read_text(encoding="utf-8")

    assert f"action_schema: {ACTION_SCHEMA}" in text
    for intent in SUPPORTED_INTENTS:
        assert f"  - {intent}" in text
    for intent in HARD_GATED_INTENTS:
        assert f"  - {intent}" in text


def test_chatops_policy_registry_preserves_main_branch_gate():
    text = Path("ION/03_registry/ion_chatops_local_daemon_policy.yaml").read_text(encoding="utf-8")

    assert "main_auto_push_allowed: false" in text
    assert "scoped_branch_push_allowed: policy_gated_later" in text
    assert "  - sev/" in text


def test_chatops_extension_manifest_references_loadable_dist_files():
    extension_root = Path("ION/09_integrations/browser_extension/ion_chatops_bridge")
    manifest = json.loads((extension_root / "manifest.json").read_text(encoding="utf-8"))

    background = manifest["background"]["service_worker"]
    content_scripts = manifest["content_scripts"][0]["js"]

    assert (extension_root / background).is_file()
    for script in content_scripts:
        assert (extension_root / script).is_file()

    for icon in manifest["icons"].values():
        assert (extension_root / icon).is_file()
    for icon in manifest["action"]["default_icon"].values():
        assert (extension_root / icon).is_file()


def test_chatops_extension_live_smoke_yaml_simulation():
    result = subprocess.run(
        ["node", "ION/09_integrations/browser_extension/ion_chatops_bridge/tests/live_smoke_parser_simulation.js"],
        check=True,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["candidate"] == "ion_chatops_candidate"
    assert payload["action_id"] == "sev-20260505-0001-smoke"
    assert payload["receipts"] == ["file_write_receipt", "sha256_receipt"]
