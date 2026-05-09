# v2.6 Delta Note

This candidate package keeps the v1.4 sandbox package compatible while adding a
clearer Custom GPT front door.

## Preserved From v1.4

- Root `pyproject.toml`
- Root `ION/REPO_AUTHORITY.md`
- ION runtime body under `ION/`
- Product adapter surfaces under `product/`
- Starter data under `product/starter_data/`

## Added In v2.6

- `000_READ_FIRST_MOUNT_ORDER.md`
- `001_GPT_INSTRUCTIONS_PASTE.md`
- `010_HOT_BOOT/` boot layers
- `020_ACTIVE_STATE_INDEX/`
- `030_CUSTOM_GPT_ADAPTER/` operational references
- `040_PRODUCT_DOCS/` short explainer and journal index
- `050_STARTER_DATA/` direct starter-data alias
- `060_ACTION_SCHEMAS/` Action Gateway and MCP JSON-RPC schemas/references
- `070_BROWSER_EXTENSION_YAML_BRIDGE/` extension/YAML bridge references
- `090_VALIDATION/` v2.6 manifest and receipt surfaces

## Overlayed Active-Root Surfaces

- dynamic domain/agent route compiler
- persona response envelope
- custom GPT Action Gateway
- dynamic domain fission protocol
- persona visible envelope protocol
- v2.5 saved-file references

## Non-Claims

This package is candidate builder-ready, not production-ready. It does not prove
the live local hub, tunnel, or Actions are healthy without current connector
returns.
