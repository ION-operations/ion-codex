#!/usr/bin/env python3
"""V120 ChatGPT browser connector contract wrapper.

This wrapper is intentionally not a hosted HTTPS MCP server. It exposes the
local contract self-test so a deployable connector cannot be confused with an
audited contract scaffold.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from kernel.ion_chatgpt_browser_mcp_connector_contract import (
    audit_chatgpt_browser_mcp_connector_contract,
    call_chatgpt_connector_tool,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="ION ChatGPT browser connector contract wrapper.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--tool", default=None)
    parser.add_argument("--arguments-json", default="{}")
    args = parser.parse_args()

    root = Path(args.ion_root).resolve()
    if args.self_test:
        result = audit_chatgpt_browser_mcp_connector_contract(root)
    elif args.tool:
        result = call_chatgpt_connector_tool(root, args.tool, json.loads(args.arguments_json or "{}"))
    else:
        result = audit_chatgpt_browser_mcp_connector_contract(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("accepted", False) or result.get("ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())

