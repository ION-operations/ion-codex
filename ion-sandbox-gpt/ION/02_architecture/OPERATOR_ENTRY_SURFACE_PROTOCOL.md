---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-04-08T23:10:00-04:00
status: ACTIVE
purpose: Define the unified operator entry surface for supervised runtime carriage of the canonical workflow
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/02_architecture/SUPERVISED_DAEMON_SERVICE_PROTOCOL.md
  - ION/02_architecture/MANUAL_AUTOMATION_FALLBACK_PROTOCOL.md
  - ION/04_packages/kernel/operator_cli.py
---

# Operator Entry Surface Protocol

## Principle

The operator entry surface does not create a second workflow. It exposes the same canonical workflow through one discoverable invocation plane.

## Required capabilities

A lawful operator entry surface must expose:
- runtime status, including latest horizon tightening and latest available enactment receipt when present
- preferred runtime start / drain / stop
- explicit operator-control mutations
- bounded daemon-service invocation
- bounded recovery/replay invocation
- bounded child-work issuance invocation
- bounded external execution export / return invocation
- packet validation
- packet enactment for packet-ready horizon candidates
- manual/sequential route scaffolding

## Store and packet defaults

When an explicit store root is not supplied, the operator entry surface defaults to:
- `ION/05_context/history/kernel_store/`

When an explicit packet-output root is not supplied for daemon/replay runs, it defaults to:
- `ION/05_context/history/dispatch_packets/`

These defaults are operator-facing convenience paths, not new authority classes.

## Backward compatibility

Legacy sequential/manual route rendering remains valid. The operator entry surface may delegate old route invocations into the sequential kernel router rather than breaking them.

## Output law

The operator entry surface may render human-readable text or JSON, but JSON output is the preferred machine-facing surface for:
- receipts
- status snapshots and enacted-horizon receipt projection
- service results
- scripted/manual automation fallback

## Safety law

The operator entry surface must not:
- bypass automation policy,
- bypass operator controls,
- bypass governed write,
- promote external returns directly into truth,
- or hide multi-step actions behind one command.

Every command remains one bounded carrier over one lawful workflow step.

## Runtime/session clarification

The operator entry surface may invoke runtime/session and API-entry commands.
It does **not** itself mint session identity, own session-local queue law, or
replace API carrier-boundary authority.
Those surfaces now remain explicitly governed by the emitted Lane C
runtime/session trio.
