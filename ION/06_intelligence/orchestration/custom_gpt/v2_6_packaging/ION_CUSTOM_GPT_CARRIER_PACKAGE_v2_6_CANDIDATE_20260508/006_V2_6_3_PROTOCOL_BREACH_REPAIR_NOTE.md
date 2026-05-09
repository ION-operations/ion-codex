# v2.6.3 Protocol Breach Repair Note

Generated: 2026-05-08T22:40:10Z

This revision repairs the Custom GPT carrier breach observed in the GPT sandbox
self-audit.

The defect was real: the uploaded package could still present a stale GPT
sandbox active work packet that pointed at the Cursor work-cycle template and
omitted Persona Interface ingress/response phases. That made it easier for the
carrier to collapse package mounting, connector reachability, local hub state,
and accepted ION state into one claim.

Repairs:

- GPT sandbox onboarding now selects
  `ION/07_templates/carriers/SINGLE_CARRIER_SEQUENTIAL_PACKET.md`.
- GPT sandbox role phase order now starts with `PERSONA_INTERFACE_INGRESS` and
  ends with `PERSONA_INTERFACE_RESPONSE`.
- GPT sandbox capability profile declares `can_use_mcp: false`,
  `production_authority: false`, and `live_execution_authority: false`.
- Sandbox preflight ignores stale active-packet capabilities from other carrier
  ids.
- Stale surface audit blocks GPT sandbox packets that still use Cursor template
  defaults or omit Persona ingress/response phases.
- Connector containment is explicit: if the user challenges Action/MCP usage,
  all Action Gateway and MCP calls are disabled immediately until a specific
  connector action is explicitly re-enabled.
- Mount taxonomy is explicit: uploaded package/sandbox mounted, sandbox
  preflight ready, connector reachable, local hub state read, external agents
  invoked, and state accepted/receipted are separate claims.
- Protocol disputes require a visible Persona envelope or an explicit
  `persona_gate_blocked` declaration.

Validation:

- Active-root focused regression suite: 28 passed.
- Package-local focused regression suite: 28 passed.
- Package GPT sandbox active packet regenerated after tests.
- Package preflight verdict: `ION_GPT_SANDBOX_PREFLIGHT_READY`.
- Package stale surface verdict: `ION_STALE_SURFACE_AUDIT_READY`.
- Package active packet gate check: GPT sandbox carrier, single-carrier
  template, no MCP capability, Persona ingress/response phases present.
- JSON/YAML parse checks passed for generated package state and Action schemas.

Non-claims:

- This package does not grant production authority.
- This package does not grant live execution authority.
- This package does not certify connector runtime health.
- This package does not accept GPT sandbox self-audit output as state without
  Steward/human acceptance.
