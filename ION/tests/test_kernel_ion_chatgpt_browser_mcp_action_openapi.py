from pathlib import Path

import yaml

OPENAPI_PATH = Path("ION/09_integrations/chatgpt_browser_mcp_action/openapi.yaml")


def test_mcp_action_openapi_targets_existing_ion_mcp_endpoint():
    doc = yaml.safe_load(OPENAPI_PATH.read_text(encoding="utf-8"))

    assert doc["openapi"] == "3.1.0"
    assert doc["servers"][0]["url"] == "https://ion.helixion.net"
    assert "/mcp" in doc["paths"]
    assert doc["paths"]["/mcp"]["post"]["operationId"] == "ionMcpJsonRpc"
    assert "/health" in doc["paths"]
    assert "/app/status.json" in doc["paths"]


def test_mcp_action_openapi_exposes_jsonrpc_mcp_methods_and_tools():
    doc = yaml.safe_load(OPENAPI_PATH.read_text(encoding="utf-8"))
    schemas = doc["components"]["schemas"]
    method_enum = schemas["IonMcpJsonRpcRequest"]["properties"]["method"]["enum"]
    tool_enum = schemas["IonMcpJsonRpcParams"]["properties"]["name"]["enum"]

    assert {"initialize", "tools/list", "tools/call", "ping"} <= set(method_enum)
    assert "ion_status" in tool_enum
    assert "ion_file_read" in tool_enum
    assert "ion_tool_manifest" in tool_enum
    assert "ion_agent_invoke" in tool_enum
    assert "ion_queue_operator_message" in tool_enum
    assert "arbitrary_shell" not in tool_enum


def test_mcp_action_openapi_has_explicit_object_properties_for_gpt_actions():
    doc = yaml.safe_load(OPENAPI_PATH.read_text(encoding="utf-8"))
    schemas = doc.get("components", {}).get("schemas", {})

    def assert_schema(schema, location):
        if not isinstance(schema, dict):
            return
        if schema.get("type") == "object":
            assert "properties" in schema, f"object schema missing properties at {location}"
        for key, value in schema.items():
            if key == "$ref":
                continue
            if isinstance(value, dict):
                assert_schema(value, f"{location}.{key}")
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    assert_schema(item, f"{location}.{key}[{index}]")

    for schema_name, schema in schemas.items():
        assert_schema(schema, f"components.schemas.{schema_name}")

    for path_name, path_item in doc["paths"].items():
        for method_name, operation in path_item.items():
            for status_code, response in operation.get("responses", {}).items():
                media = response.get("content", {}).get("application/json", {})
                schema = media.get("schema", {})
                assert schema.get("$ref"), f"response schema should use explicit component ref at {path_name} {method_name} {status_code}"
