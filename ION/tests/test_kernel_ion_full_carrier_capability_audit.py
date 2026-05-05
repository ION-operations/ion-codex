from pathlib import Path

from kernel.ion_full_carrier_capability_audit import (
    BOUNDED_PROJECT_VISIBILITY_TOOLS,
    AGENT_INVOCATION_BROKER_TOOLS,
    CODEX_QUEUE_AUTOMATION_TOOLS,
    FAILURE_CLASSES,
    FIRST_FULL_CARRIER_TOOLS,
    audit_full_carrier_capability,
)


def test_full_carrier_capability_audit_separates_adapter_gap_from_core_failure():
    result = audit_full_carrier_capability(Path.cwd())

    assert result["schema_id"] == "ion.full_carrier_capability_audit.v1"
    assert result["verdict"] == "ION_FULL_CARRIER_CAPABILITY_AUDIT_READY"
    assert result["accepted"] is True
    assert set(result["exposed_first_full_carrier_tools"]) == FIRST_FULL_CARRIER_TOOLS
    assert set(result["exposed_bounded_project_visibility_tools"]) == BOUNDED_PROJECT_VISIBILITY_TOOLS
    assert set(result["exposed_codex_queue_automation_tools"]) == CODEX_QUEUE_AUTOMATION_TOOLS
    assert set(result["exposed_agent_invocation_broker_tools"]) == AGENT_INVOCATION_BROKER_TOOLS
    assert result["missing_first_full_carrier_tools"] == []
    assert result["missing_bounded_project_visibility_tools"] == []
    assert result["missing_codex_queue_automation_tools"] == []
    assert result["missing_agent_invocation_broker_tools"] == []
    assert "ION_CORE_FAILURE" in FAILURE_CLASSES
    assert "CARRIER_ADAPTER_FAILURE" in FAILURE_CLASSES
    assert "CODEX_CLI_FAILURE" in FAILURE_CLASSES
    assert "DAEMON_FAILURE" in FAILURE_CLASSES
    assert "AGENT_INVOCATION_FAILURE" in FAILURE_CLASSES
    assert "BACKEND_CODEX_FAILURE" in FAILURE_CLASSES
    assert result["adapter_gaps"][0]["classification"] == "CAPABILITY_NOT_YET_IMPLEMENTED"
    assert result["adapter_gaps"][0]["ion_core_failure"] is False


def test_full_carrier_owner_surfaces_exist():
    result = audit_full_carrier_capability(Path.cwd())

    for owner in result["owner_paths"].values():
        assert owner["exists"] is True
