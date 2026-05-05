---
type: template
template_name: AGENT_SPAWN
created: 2026-04-03T16:27:55-04:00
status: OPTIONAL_FUTURE
---

# TEMPLATE — AGENT_SPAWN

Use this when a role is explicitly creating a bounded auxiliary agent, subagent, or
parallel execution slice.

## Required sections

```markdown
# Agent Spawn: <title>

## Purpose

## Parent role

## Target role or subagent identity

## Scope

## Read set

## Write set

## Expected output

## Stop conditions
```

## Invariants

1. Spawn only when the extra parallelism is justified.
2. Scope and write boundaries must be explicit.
3. The parent role retains consolidation responsibility.
4. If low-burn sequential routing is sufficient, do not spawn.

## Cursor Task binding (IDE carrier)

When the spawn target is a Cursor **Task** subagent:

1. **Target identity** = **ION boot truename** under `ION/03_registry/boots/*.boot.md`, not a generic worker label. Validate with `kernel.cursor_subagent_ion_role_registry.validate_cursor_subagent_role_packet` (`packet_ok` must be true).
2. **Prompt** = Context Package per `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md`; include boot path and required bindings from the boot in the opening block.
3. **Task `description`** must start with `ION/<ROLE>/` matching `agent_name`.
4. **Chassis** = `subagent_type` + `readonly` per carrier mount law; **role** remains the mounted ION identity in the packet body.
5. Operator checklist: `ION/docs/cursor/CURSOR_SUBAGENT_ION_ROLE_SPAWN.md`.
