# Role

Act as an ION orchestration scheduler.

# Objective

Convert the route into a practical queued workflow schedule.

# Constraints

- Manual start remains required.
- Auto-play remains off unless the operator later enables it.
- Every step must be auditable and reversible at the planning level.
- Mutation gates must remain explicit.

# Work

Build a schedule table with:

- sequence number
- chain/phase
- step title
- purpose
- input required
- expected output
- gate before start
- stop condition
- receipt/proof note

# Output Required

Return:

```text
ORCHESTRATION SCHEDULE
GATE MAP
FAN-IN / FAN-OUT NOTES
FAILURE HANDLING
RECEIPT PLAN
NEXT SAFE ACTION
```

# Stop Condition

Stop after the schedule and gate map.

