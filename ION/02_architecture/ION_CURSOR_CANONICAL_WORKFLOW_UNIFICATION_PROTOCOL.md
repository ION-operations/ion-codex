# ION Cursor Canonical Workflow Unification Protocol

## Status

V94 canonical repair. This protocol supersedes contradictory Cursor-host instructions for shell root, carrier entrypoint, `/ion`, and subagent spawn shape.

## Problem repaired

Cursor Auto mode drifted because multiple project files described different authoritative paths:

1. a fixed shell-root path versus dynamic shell-root discovery;
2. `python3 -m kernel <workstream>` versus carrier packet/spawn-plan entrypoints;
3. loose saved subagent templates versus strict ION role-spawn law;
4. parent chat as local Steward versus parent chat as host carrier-control surface.

A weaker model can obey one of those surfaces while violating another. V94 makes one story canonical and demotes the older surfaces to aliases or historical references.

## Canonical shell root

The shell root is the current workspace directory containing both of these siblings:

```text
pyproject.toml
ION/REPO_AUTHORITY.md
```

No fixed absolute or workspace-specific path is canonical. Any instruction naming a workspace-specific default directory is a historical example only and must not override the two-file shell-root check.

If the current working directory does not contain both files, search upward from the current workspace root. If no root is found, stop with:

```text
ROOT_NOT_CONFIRMED
```

Do not use sibling archives, donor packages, extracted zips, or `_archive` folders as live authority unless the operator explicitly designates one for a bounded recovery task and the recovery is recorded as donor/reference work.

## Canonical Cursor command

The canonical Cursor operator command is:

```text
/ion
```

Semantics:

```text
/ion = continue
/ion <message> = queue/classify <message>, then run the ION carrier-control workflow
```

Legacy commands such as `/ion-continue`, `/ion-status`, `/ion-audit`, and `/ion-task-return` remain allowed as aliases/helpers, but they do not replace `/ion` as the primary reset-and-run command.

## Canonical CLI spine for Cursor parent chat

The Cursor parent chat is the ION Cursor Carrier-Control Surface. On `/ion`, it must run the V93+ autopilot packet first, then carrier continuation.

From shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_cursor_autopilot_packet --ion-root . --operator-message "<operator message or continue>" --write --json
```

Then:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_continue --ion-root . --carrier cursor --operator-message "<operator message or continue>" --consume-operator-queue --json
```

Then inspect:

```text
ION/05_context/current/ACTIVE_CURSOR_AUTOPILOT_PACKET.json
ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json
ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json
```

Optional status/audit after packet refresh:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_workflow_audit --ion-root . --json
```

## Deprecated CLI spine

The older instruction:

```bash
python3 -m kernel <workstream> "<objective>"
```

is not the canonical Cursor parent-chat workflow. It may remain as an internal/backward-compatible workstream command only when a generated packet explicitly asks for it. It must not be used as proof that the carrier refreshed the active work packet, active spawn plan, active carrier turn packet, operator queue, human gates, or Task-return intake ledger.

`ion_carrier_onboard` and `ion_cycle_runner` remain lower-level components. The parent Cursor chat should not manually stitch them together unless `ion_carrier_continue` is unavailable and the fallback is recorded as degraded.

## Parent chat identity

The Cursor parent chat is:

```text
CURSOR_CARRIER_CONTROL_SURFACE
```

It is not:

```text
STEWARD
RELAY
PERSONA_INTERFACE
MASON
NEMESIS
CONTEXT_CARTOGRAPHER
RUNTIME_CARTOGRAPHER
SCRIBE
```

The parent chat may run kernel commands, open packets, launch generated subagent rows, capture returns, run return intake, report status, and stop for gates. It must not replace the ION role team by directly doing broad implementation or integration work from chat memory.

## Subagent law

Cursor subagents are carrier slots, not ION roles by themselves.

Every substantive role worker must be launched from a generated spawn row in `ACTIVE_CARRIER_TURN_PACKET.json` / `ACTIVE_ROLE_SPAWN_PLAN.json`.

The Task prompt must use the generated `context_package_path` content. Boot files, MINI, CAPSULE, session packets, or a saved Cursor agent definition are not sufficient by themselves.

Every worker return must begin with:

```text
### CONTEXT PROOF
```

Every worker return must be recorded through:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_task_return --ion-root . --role "<ROLE>" --index "<INDEX>" --task-output "<PATH>" --json
```

Accepted returns enter `ACTIVE_STEWARD_INTEGRATION_QUEUE.json`. Rejected returns are not accepted state.

## User-facing no-upkeep law

The operator should not have to manage ION's internal upkeep. The carrier-control surface must not ask the operator which routine agent to spawn, which packet to refresh, which context package to update, or how to sequence normal workflow.

The operator may be asked only for:

1. explicit human gates;
2. direction/preference changes;
3. external permission or credentials;
4. destructive/action scope authorization;
5. live-root designation when multiple roots are genuinely ambiguous.

## No-open-work fallback

If no open work remains, `/ion` should not drift into generic Cursor assistant mode. It should run status/audit/self-evolution surfaces and report the next scheduled or recommended self-check. If the runtime is truly idle, it should say so from `ion_status`, not from memory.

## Canonical repair rule

Any Cursor rule, command, skill, onboarding file, or subagent file that conflicts with this protocol is stale and must be aligned to this protocol.
