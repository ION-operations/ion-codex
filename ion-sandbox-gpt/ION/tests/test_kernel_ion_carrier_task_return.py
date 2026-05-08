import json
from pathlib import Path

from kernel.ion_carrier_task_return import record_task_return


def _write_json(root: Path, rel: str, value: dict) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _seed_return_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    authority = root / "ION/REPO_AUTHORITY.md"
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text("# authority\n", encoding="utf-8")
    (root / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
    (root / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    context_file = root / "ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md"
    context_file.parent.mkdir(parents=True, exist_ok=True)
    context_file.write_text("# protocol\nRequired context\n", encoding="utf-8")
    _write_json(
        root,
        "ION/05_context/current/execution_cycles/test/01_receipt.json",
        {
            "schema_id": "ion.cursor_task_context_load_receipt.v1",
            "required_context_reads": [
                {
                    "path": "ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md",
                    "kind": "file",
                    "required": True,
                }
            ],
        },
    )
    _write_json(
        root,
        "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
        {
            "schema_id": "ion.carrier_cycle_plan.v1",
            "execution_bundle_root": "ION/05_context/current/execution_cycles/test",
            "role_spawn_plan": [
                {
                    "index": 1,
                    "role": "steward",
                    "spawn": True,
                    "carrier_slot": "codex_extension_task",
                    "context_package_path": "ION/05_context/current/execution_cycles/test/01_steward.md",
                    "context_load_receipt_path": "ION/05_context/current/execution_cycles/test/01_receipt.json",
                }
            ],
        },
    )
    _write_json(root, "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json", {"spawn_queue": [{"index": 1, "role": "steward"}]})


def _context_proof() -> str:
    return """### CONTEXT PROOF
- path: ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md
  status: file_present
  line_count: 2
  sha256: abc
  excerpt: "# protocol"
"""


def _template_action_proof() -> str:
    return """### TEMPLATE ACTION PROOF
template_id: ion.template.audit_observation.v1
action_id: carrier_task_return_contract_check
result: accepted_state_delta_candidate
touched_paths:
  - ION/04_packages/kernel/ion_carrier_task_return.py
"""


def test_task_return_requires_context_and_template_action_proofs(tmp_path: Path) -> None:
    _seed_return_root(tmp_path)

    result = record_task_return(
        tmp_path,
        role="steward",
        index=1,
        task_output_text=_context_proof() + "\n" + _template_action_proof(),
    )

    assert result["accepted"] is True
    assert result["evaluation"]["context_proof"]["accepted"] is True
    assert result["evaluation"]["template_action"]["accepted"] is True
    assert result["record"]["template_id"] == "ion.template.audit_observation.v1"


def test_task_return_rejects_context_only_output(tmp_path: Path) -> None:
    _seed_return_root(tmp_path)

    result = record_task_return(
        tmp_path,
        role="steward",
        index=1,
        task_output_text=_context_proof() + "\n### ROLE PASS\ncontext only is insufficient\n",
    )

    assert result["accepted"] is False
    assert result["evaluation"]["context_proof"]["accepted"] is True
    assert result["evaluation"]["template_action"]["accepted"] is False
    assert "template_action:missing_template_action_proof_heading" in result["record"]["findings"]
