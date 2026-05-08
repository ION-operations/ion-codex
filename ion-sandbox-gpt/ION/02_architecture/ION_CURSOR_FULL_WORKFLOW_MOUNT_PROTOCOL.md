---
type: protocol
authority: A2_OPERATIONAL
status: ACTIVE
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION — Cursor full workflow mount (RELAY → STEWARD → subagent)

## Purpose

Define how the **Cursor parent carrier**, once mounted through **RELAY** packet correlation and **STEWARD** task-scoped orchestration, may lawfully request **named ION role** mounts on **Cursor Task** carrier slots.

## Spawn stack (authoritative order)

1. **Cursor carrier** — parent chat on confirmed shell root.
2. **RELAY packet channel** — correlation id, persona-visible briefing discipline.
3. **STEWARD orchestration authority** — `TASK_SCOPED_LOCAL_ORCHESTRATION` only; no production claims.
4. **Spawn request** — validated spawn packet (schema + `evaluate_v75_spawn_packet`).
5. **Named ION role mount** — `agent_name` + existing `role_boot` under `ION/03_registry/boots/`.
6. **Bounded Work packet / Context package** — non-empty mission surface; allowed and forbidden paths required.
7. **Subagent execution** — Task slot; chassis only.
8. **Proposal return** — never self-integrated.
9. **STEWARD integration** — accept / reject / reroute.
10. **RELAY report** — final status for relay-facing surfaces.

## Law

- A **Cursor subagent** is a **carrier slot**, not a free-floating assistant. It must carry a **named ION role** with boot path, **authority ceiling**, **allowed_paths**, **forbidden_paths**, **validation_commands**, and **return_contract**.
- **Relay** owns packet channel truth; **Steward** owns orchestration integration; the **subagent** does not broaden scope or self-assign role.

## Surfaces

- Mount guide: `ION/docs/cursor/CURSOR_FULL_WORKFLOW_MOUNT_GUIDE.md`
- Cursor rule: `.cursor/rules/ion-full-workflow-mount.mdc`
- Spawn packet template: `ION/docs/cursor/ION_SUBAGENT_SPAWN_PACKET_TEMPLATE.md`
- Spawn readiness: `ION/docs/cursor/ION_SUBAGENT_SPAWN_READINESS_GUIDE.md`
- Schema: `ION/03_registry/cursor_subagent_role_mount.schema.json`
- Audit: `kernel.v75_cursor_subagent_spawn_readiness_audit`

## Status projection

- Live workflow status packet: `ION/docs/cursor/ION_LIVE_WORKFLOW_STATUS_PACKET.md` (witness / projection; not execution authority).
