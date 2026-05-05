# T44 — MCP Automation Surface

## Scope

Machine-readable MCP-facing metadata for supervised external execution packets.

## Required structure

### MCPAutomationSurface

Must include:
- `resource_kind`
- `resource_name`
- `transport`
- `tool_name`
- `request_schema`
- `response_schema`

## Minimum export packet fields

An external execution packet must include:
- bridge kind
- generation time
- authority class
- work unit id
- serialized dispatch/context payload
- serialized MCP automation surface
- explicit boundary declaration

## Boundary declaration

The packet must state at minimum:
- kernel truth is not external
- external write authority is proposed-commit only
- governed write remains required downstream
- allowed writes
- allowed next actions
