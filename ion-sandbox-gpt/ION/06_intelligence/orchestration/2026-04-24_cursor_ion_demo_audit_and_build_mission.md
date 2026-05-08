# Cursor / Codex CLI Mission Packet — ION Ultimate AI Chat Demo Audit and Build

## Mission status

A3 operational mission packet. This is not final law. It is a bounded build/audit mission for Cursor IDE / Codex CLI / GPT-5.5-class coding agents.

## Mission objective

Audit this branch and build the narrowest impressive demo proving ION as an evented living context graph powering an advanced AI chat assistant.

The demo must show:

```text
User
  -> Persona Interface
  -> Relay semantic-boundary packet
  -> Steward graph-region route
  -> evented template-file graph operation
  -> validation / reaction / receipt
  -> Relay return
  -> Persona Interface response
  -> User
```

## Core thesis to preserve

```text
ION is a living context graph operated by lawful agents through templates.
ION is materialized as an evented, template-instantiated file system.
ION files are template-instantiated graph objects.
A valid completed template file is an automation event surface.
```

## Role boundaries

Do not collapse roles.

- Persona Interface owns user-facing relationship, style, final response rendering.
- Relay owns semantic-boundary translation, packetization, digesting, and persona-ready return packages.
- Steward owns graph-region orchestration and work routing.
- Specialists operate bounded graph regions.
- Daemon/scheduler/indexer react only through lawful event protocols and receipts.

## Audit targets

1. Verify the front-door runtime files exist and tests pass.
2. Verify evented template contract/runtime files exist and tests pass.
3. Verify template registry tracks context-graph, evented-file, and front-door surfaces.
4. Search for stale claims that reduce ION to only AI OS, prompt memory, chat wrapper, or agent framework.
5. Search for role collapse, especially Relay owning Persona or Steward duties.
6. Search for evented-file collapse, especially completion treated as acceptance or daemon detection treated as authority.
7. Search for missing receipts after graph mutation, scheduling, warning, settlement, refusal, or no-action.
8. Search for branch-specific claims written as final canon.
9. Report all stale surfaces with file path, line/context, severity, and recommended action.

## Build target

Build a minimal but impressive CLI/API-local demo path first. Browser UI can come after the proof is solid.

### Demo scenario A — summary refresh

User asks for a project summary refresh.

Expected chain:

1. Persona Interface ingress created.
2. Relay semantic-boundary packet created.
3. Steward routing envelope created.
4. Runtime session and WorkUnit created.
5. Summary-refresh template file instantiated.
6. File reaches completion threshold.
7. Completion validator accepts it.
8. Event extractor derives graph effect.
9. Reaction router schedules index/summary update.
10. Receipt emitted.
11. Relay return package created.
12. Persona response package created.

### Demo scenario B — dependency change

A completed dependency-change template file triggers:

- validation;
- dependency edge extraction;
- affected-surface warning;
- scheduler item or specialist activation;
- receipt.

### Demo scenario C — contradiction note

A completed contradiction note triggers:

- validation;
- contradiction graph node/edge;
- Nemesis review schedule;
- receipt;
- no silent harmonization.

## Required outputs

1. `ION/06_intelligence/orchestration/DEMO_AUDIT_REPORT.md`
2. `ION/06_intelligence/orchestration/DEMO_BUILD_PLAN.md`
3. executable demo module or CLI command if feasible
4. tests proving the demo path
5. patch report listing changed files
6. blockers if not feasible

## Required proof discipline

Do not fake the demo. If a path is only witness/projection, mark it as witness/projection. If a branch-specific surface is not merged, mark it branch-specific. If a runtime step is not implemented, add it as a blocker rather than pretending it exists.

## Suggested test command set

Run at least:

```bash
PYTHONPATH="$PWD/04_packages" python -m unittest discover -s tests -p test_kernel_front_door_runtime_entry.py -v
PYTHONPATH="$PWD/04_packages" python -m unittest discover -s tests -p test_kernel_front_door_chat_orchestration.py -v
PYTHONPATH="$PWD/04_packages" python -m unittest discover -s tests -p test_kernel_template_metadata_contracts.py -v
PYTHONPATH="$PWD/04_packages" python -m unittest discover -s tests -p test_kernel_template_completion_events.py -v
PYTHONPATH="$PWD/04_packages" python -m unittest discover -s tests -p test_kernel_contract_bound_event_runtime.py -v
PYTHONPATH="$PWD/04_packages" python -m unittest discover -s tests -p test_kernel_context_graph_ontology_adapter.py -v
```

## Success condition

The branch is demo-ready when a user turn can be transformed into a front-door graph operation and at least one template completion event can trigger a validated, receipted graph reaction, with Persona/Relay/Steward boundaries preserved.
