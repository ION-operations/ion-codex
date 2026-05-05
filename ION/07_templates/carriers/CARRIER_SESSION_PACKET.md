# Carrier Session Packet

## Session ID

## Carrier
- carrier_profile:
- carrier_level:
- host:
- default_return_agent: CURRENT_CARRIER

## Active Task
- task_id:
- task_title:
- task_packet_path:

## Active Authority Inputs
- repo authority:
- current operating packet:
- mount contract:
- carrier profile:
- active carrier onboarding packet:
- active spawn plan:
- carrier level decision:
- role/context surfaces:
- compiled context bundle:
- execution packet template:

## Current Mode
manual_single_carrier / tool_assisted / host_native_spawn / ion_native_orchestrated / api_runtime

## Allowed Operations
| operation | allowed? | proof required |
|---|---|---|

## Forbidden Operations
| operation | reason |
|---|---|

## Return Handling
All work returns to CURRENT_CARRIER unless otherwise specified.

Task returns require context proof, template-action proof, result, and receipt
or handoff state. Unproofed worker output is not current truth.

## Journal / Receipt
- journal path:
- receipt path:
