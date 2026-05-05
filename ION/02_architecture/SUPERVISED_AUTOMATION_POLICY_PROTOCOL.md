# SUPERVISED AUTOMATION POLICY PROTOCOL

## Purpose

Define the first truthful policy gate for supervised automation in the live ION root.
This protocol does not create autonomy.
It decides when a bounded automation action is allowed, blocked, held, or requires explicit approval.

## Core law

1. Operator stop beats all other runtime pressure.
2. Operator hold beats action execution but does not erase state.
3. Supervised automation requires an explicit supervising operator.
4. Manual-context automation may run only under stricter approval.
5. Suspended or disabled automation posture may not be silently bypassed.
6. Threshold hold / rollback posture must be honored.
7. Review pressure must raise approval or block requirements before stronger action classes proceed.

## First action classes

- `START_DAEMON_SERVICE`
- `RUN_DAEMON_STEP`
- `ISSUE_CHILD_WORK`
- `APPLY_GOVERNED_WRITE`
- `ESCALATE_REVIEW`
- `EMIT_RUNTIME_REPORT`

## Decision classes

- `ALLOW`
- `REQUIRE_APPROVAL`
- `HOLD`
- `BLOCK`

## First-pass decision matrix

### Operator control

- service stop => `BLOCK`
- scope hold => `HOLD`

### Automation posture

- `DISABLED` => `BLOCK`
- `SUSPENDED` => `HOLD`

### Supervision

For service start, daemon steps, child issuance, and governed writes:
- no supervising operator => `BLOCK`

### Threshold pressure

- rollback / hold recommendation => `HOLD`
- review recommendation => `REQUIRE_APPROVAL`

### Review pressure

For child issuance and governed writes:
- explicit review requirement => `REQUIRE_APPROVAL`

### Manual-context rule

In `IDE_MANUAL` context, stronger automation actions remain supervised and may require explicit approval even when otherwise lawful.

## Non-goals

- no hidden daemon scheduler
- no autonomy claim
- no authority promotion of policy packets
