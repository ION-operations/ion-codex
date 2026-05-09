# ION MCP JSON-RPC Action Reference

## Purpose

The MCP JSON-RPC Action lets the Custom GPT call the existing ION HTTP MCP
preview through GPT Actions.

Use it for read/status/tool discovery and bounded tool calls. Do not treat it as
production authority.

## Endpoint

```text
https://ion.helixion.net/mcp
```

## Privacy Policy URL

```text
https://helixion.net/privacy
```

## JSON-RPC Methods

```text
initialize
ping
tools/list
tools/call
```

## Common Calls

List tools:

```json
{
  "jsonrpc": "2.0",
  "id": "tools-list-1",
  "method": "tools/list",
  "params": {}
}
```

Call `ion_status`:

```json
{
  "jsonrpc": "2.0",
  "id": "ion-status-1",
  "method": "tools/call",
  "params": {
    "name": "ion_status",
    "arguments": {}
  }
}
```

Bounded write-capable tools require the explicit confirmation argument when the
tool contract says so:

```json
{
  "confirmation": "ION_BOUNDED_WRITE_CONFIRMED"
}
```

## GPT Use

Start with health/status, `ping`, and `tools/list`. Then use read/status tools
such as current packet, tool manifest, daemon status, queue status, file read,
or registry read. Treat write-capable tools as bounded proposal/queue routes,
not free mutation authority.

## Non-Claims

MCP read success proves only that the tool call returned. It does not prove
external production state, background execution, accepted state, or human
approval unless the returned receipt/proof says so.
