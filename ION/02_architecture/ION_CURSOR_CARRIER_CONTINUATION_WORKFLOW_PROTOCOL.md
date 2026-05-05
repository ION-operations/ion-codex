# ION Cursor Carrier Continuation Workflow Protocol — V84

## Purpose

This protocol makes the Cursor parent chat a carrier-control lane instead of an
improvised agent. The operator may say only `continue`, `proceed`, or `resume`;
the carrier must still know how to refresh state, spawn the next lawful role
workers, and stop only at explicit gates.

## Invariant

The parent Cursor chat is not STEWARD, MASON, VIZIER, NEMESIS, RELAY, or PERSONA.
It is the carrier that refreshes packets, launches bounded Task carrier slots,
collects evidence, runs gates, and returns accepted packets to STEWARD/RELAY.

## Mandatory turn sequence

1. Resolve shell root: `pyproject.toml` and `ION/REPO_AUTHORITY.md` must be at
   the same root.
2. Run the continuation entrypoint:

   ```bash
   PYTHONPATH=ION/04_packages python3 -m kernel.ion_carrier_continue --ion-root . --carrier cursor --operator-message "<verbatim operator message>" --json
   ```

3. Read `ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json`.
4. Read `ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json`.
5. Execute only `role_spawn_plan` rows with `spawn=true`, in ascending `index`.
6. For each row, use `context_package_path` as the executable Task package.
7. Reject returns that do not begin with `### CONTEXT PROOF`.
8. Validate returns against `context_load_receipt_path` using
   `kernel.ion_context_proof_gate`.
9. Send accepted returns to STEWARD integration.
10. Use RELAY/PERSONA only for visible reporting when routed.

## Forbidden behavior

The parent carrier must not:

- ask the operator which agents to spawn when a valid spawn plan exists;
- do role work itself in the parent chat;
- spawn from boot files, MINI, CAPSULE, or `session_packet_path` alone;
- treat `I read the context file` as onboarding proof;
- reuse stale active plans when `ion_carrier_continue` can regenerate them;
- claim production or live execution authority.

## Human gate

Human intervention is required only when:

- `ACTIVE_CARRIER_TURN_PACKET.json` has `blocked_by_findings=true`;
- a required capability is missing;
- a Task return fails the context-proof gate;
- the active packet declares an explicit human approval point;
- a change would exceed the packet's allowed paths or authority ceiling.
