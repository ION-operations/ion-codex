# Role

Act as an ION context inventory step.

# Objective

Inspect the currently visible/attached context and produce a context inventory
for the queued workflow.

# Constraints

- Do not invent missing files.
- Do not claim access to local files unless they are visible through an
  approved tool result or attached package.
- Do not treat a connector status result as permission to mutate.

# Work

List available context by category:

- active goal
- attached files or packages
- visible tool/action results
- ION protocol references
- project receipts or proof surfaces
- missing context that should be requested

# Output Required

Return:

```text
CONFIRMED CONTEXT
MISSING CONTEXT
SOURCE AUTHORITY NOTES
USABLE RECEIPTS / PROOF SURFACES
RISKY OR STALE CONTEXT
NEXT SAFE ACTION
```

# Stop Condition

Stop after producing the inventory.

