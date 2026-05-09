from pathlib import Path

import yaml


REPO_PACKAGE_ROOT = Path(
    "ION/06_intelligence/orchestration/custom_gpt/v2_6_packaging/"
    "ION_CUSTOM_GPT_CARRIER_PACKAGE_v2_6_CANDIDATE_20260508"
)


def _package_root() -> Path:
    if Path("001_GPT_INSTRUCTIONS_PASTE.md").exists():
        return Path(".")
    return REPO_PACKAGE_ROOT


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_custom_gpt_instructions_contain_connector_containment_override():
    package_root = _package_root()
    instructions = _text(package_root / "001_GPT_INSTRUCTIONS_PASTE.md")

    assert "## Connector Containment Override" in instructions
    assert "all Action Gateway and MCP calls are disabled immediately" in instructions
    assert "until the user explicitly re-enables a specific connector action" in instructions
    assert "## Mount Taxonomy" in instructions
    assert "uploaded package/sandbox mounted" in instructions
    assert "connector reachable" in instructions
    assert "state accepted or receipted" in instructions
    assert "When the ION package is mounted, this GPT is ION" in instructions
    assert "## Always-On ION Workflow Law" in instructions
    assert "NO_WORKFLOW_OBJECT_NO_SUBSTANTIVE_RESPONSE" in instructions
    assert "The chat window is only the Persona Interface output channel" in instructions
    assert "sandbox/package ION workflow is the work surface" in instructions
    assert "Do not compose substantive" in instructions
    assert "Do not speak as a detached chatbot" in instructions
    assert "Every substantive final answer must be the Persona Interface response" in instructions
    assert "## Sandbox-Only Reply Law" in instructions
    assert "Do not answer the user by freehand chat" in instructions
    assert "Persona ingress -> Relay boundary -> Steward route" in instructions
    assert "candidate domain/agent" in instructions
    assert "then hand off through Persona" in instructions


def test_custom_gpt_8k_instruction_kernel_stays_under_builder_limit():
    package_root = _package_root()
    instructions = _text(package_root / "001_GPT_INSTRUCTIONS_PASTE_8K.md")

    assert len(instructions) < 8000
    assert "AI output is not state" in instructions
    assert "## Connector Containment Override" in instructions
    assert "all Action Gateway and MCP calls are disabled immediately" in instructions
    assert "## Mount Taxonomy" in instructions
    assert "Actions are explicit-use only" in instructions
    assert "Do not use Action Gateway/MCP to mount ION" in instructions
    assert "persona_gate_blocked" in instructions
    assert "When the ION package is mounted, this GPT is ION" in instructions
    assert "## Always-On ION Workflow Law" in instructions
    assert "NO_WORKFLOW_OBJECT_NO_SUBSTANTIVE_RESPONSE" in instructions
    assert "The chat window is only the Persona Interface output channel" in instructions
    assert "mounted sandbox/package ION workflow is the work surface" in instructions
    assert "Do not compose substantive answers directly in chat" in instructions
    assert "Do not speak as a detached chatbot" in instructions
    assert "Every substantive final answer must be the Persona Interface response" in instructions
    assert "## Sandbox-Only Reply Law" in instructions
    assert "Do not answer by freehand chat" in instructions
    assert "Every visible user reply must be a direct copy/rendering" in instructions
    assert "candidate domain/agent proposal" in instructions


def test_action_selection_boot_disables_tools_after_connector_dispute():
    package_root = _package_root()
    boot = _text(package_root / "010_HOT_BOOT/BOOT_3_ACTIONS_MCP_TOOL_SELECTION.md")

    assert "explicit-use connector surfaces" in boot
    assert "disable all" in boot
    assert "until the user explicitly re-enables one exact connector action" in boot


def test_front_door_protocol_requires_persona_gate_for_protocol_disputes():
    protocol = _text(Path("ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md"))

    assert "## 5.1 Protocol Dispute Response Gate" in protocol
    assert "persona_gate_blocked" in protocol
    assert "Connector-use disputes activate connector containment" in protocol


def test_action_openapi_descriptions_are_explicit_use_only():
    gateway = yaml.safe_load(Path("ION/09_integrations/custom_gpt_action_gateway/openapi.yaml").read_text(encoding="utf-8"))
    mcp = yaml.safe_load(Path("ION/09_integrations/chatgpt_browser_mcp_action/openapi.yaml").read_text(encoding="utf-8"))

    assert "Explicit-use-only" in gateway["info"]["description"]
    assert "Do not call this Action to mount ION" in gateway["info"]["description"]
    assert "Explicit-use-only" in mcp["info"]["description"]
    assert "Do not call this Action to mount ION" in mcp["info"]["description"]
