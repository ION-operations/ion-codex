# /ion-continue — Alias for /ion

`/ion-continue` is retained only as a compatibility helper.

Canonical command:

```text
/ion
```

If invoked, execute the same V94 sequence as `/ion` with operator message `continue`:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_cursor_autopilot_packet --ion-root . --operator-message "continue" --write --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_continue --ion-root . --carrier cursor --operator-message "continue" --consume-operator-queue --json
```

Then follow `ACTIVE_CURSOR_AUTOPILOT_PACKET.json`, `ACTIVE_CARRIER_TURN_PACKET.json`, and `ACTIVE_ROLE_SPAWN_PLAN.json`.

## Hook-state binding

Before and after continuation, inspect `ION/05_context/current/ACTIVE_CURSOR_HOOK_STATE.json` when present. If hook state is missing or stale, do not treat that as authority failure by itself; run `/ion` / `ion_carrier_continue`, refresh packet state, and report the degraded hook condition through status/audit.
