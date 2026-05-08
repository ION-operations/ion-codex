# ION V72 MCP Donor Reconciliation Protocol

## Purpose

This protocol prevents a known branch-loss event from becoming another open-ended consolidation loop.

V72 is older than the current trunk but contains a stronger MCP substrate than the V105/V107 recovery line. V108 therefore performs a bounded donor reconciliation: import the missing MCP substrate surfaces without reverting the project, without broad archaeology, and without importing old runtime receipts into hot context.

## Non-reversion law

```text
A donor branch may restore a named capability family.
A donor branch may not become current authority merely because it contains a stronger organ.
```

V108 keeps the current trunk as the live operational line and treats V72 as a capability donor.

## Scope

Allowed donor imports:

```text
bootstrap locks
architecture protocols
registry schemas/policies
kernel modules
tests
docs/guides
example MCP client configs
handoff/provenance notes
```

Forbidden hot-trunk imports:

```text
old runtime session receipts
old queue/session state
old generated run state
old donor working directories
```

## Current bridge preservation

The V92/V105/V107 Cursor MCP control bridge is not replaced by V72. It remains the current carrier-facing MCP control surface.

V72 restores lower/substrate MCP abilities: local bridge, client config/certification, transport preview, hosted auth boundary, and related docs/tests.

## Required audit

The V108 audit must prove:

```text
required V72 donor surfaces exist;
current Cursor MCP bridge surfaces still exist;
forbidden V72 runtime receipts are absent from hot trunk;
no live execution authority is granted;
production authority remains false.
```

## Relationship to no-silent-loss law

V108 was originally layered on top of the V107 preservation gate. Current donor reconciliation must use the V118 no-silent-loss containment preservation gate: donor files may be restored or moved to containment, but project files must not silently vanish and protected or unexpected uncontained removals must block packaging.
