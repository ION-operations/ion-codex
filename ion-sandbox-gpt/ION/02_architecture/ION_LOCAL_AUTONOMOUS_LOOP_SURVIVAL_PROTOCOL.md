# ION Local Autonomous Loop Survival Protocol V101

```yaml
schema_id: ion.local_autonomous_loop_survival_protocol.v1
version: V101_LOCAL_AUTONOMOUS_LOOP_SURVIVAL_SLICE
production_authority: false
external_execution_authority: false
```

## Purpose

ION must prove that its own workflow can advance without depending on Cursor parent-chat inference, MCP availability, or an external LLM call. V101 defines the first local survival slice: a deterministic autonomous loop accepts a goal, creates a bounded local worker return, validates `CONTEXT PROOF` plus `TEMPLATE ACTION PROOF`, integrates the return through Steward, writes receipts, updates the cockpit projection, and stops with an explicit stop reason.

## Non-negotiable boundaries

This protocol does not claim production readiness. It does not claim real multi-agent autonomy. It does not call external workers. It establishes the minimum file-backed loop that later carrier adapters must satisfy.

## Required transaction

```text
operator goal
→ kernel.ion_autonomous_loop
→ local worker return
→ kernel.ion_template_action_gate
→ kernel.ion_steward_integrate
→ stewardship receipt
→ LAST_ION_AUTONOMOUS_LOOP_RESULT.json
→ ACTIVE_COCKPIT_VIEW_MODEL.json
→ LEAD_DEV_ACTIVE_CONTEXT_PACKAGE_V101.md
```

## Exit condition

The survival slice is valid only when the focused tests pass and the CLI can run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_autonomous_loop --ion-root . --goal "Find one contradiction and propose one patch" --max-steps 3 --write --json
```

## Next lawful move

After V101, the deterministic local worker may be replaced by a bounded worker-adapter interface. That adapter must still return the same proof headings and pass the same gates before Steward integration.
