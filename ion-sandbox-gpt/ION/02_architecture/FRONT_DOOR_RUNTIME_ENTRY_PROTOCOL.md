# Front-Door Runtime Entry Protocol

## Status
A3_OPERATIONAL_PATCH  
Date: 2026-04-24  
Canon status: NOT_FINAL_CANON

## Purpose

This protocol makes the front-door split executable in runtime artifacts rather
than only documented in roster and template surfaces.

The required runtime topology is:

```text
User -> Persona Interface -> Relay -> Steward
```

Return path:

```text
Steward / system output -> Relay -> Persona Interface -> User
```

## Governing rule

Runtime entrypoints must not collapse:

- Persona Interface
- Relay
- Steward

into one role, carrier, or continuity lane.

A browser, API, or chat adapter may mount a single LLM carrier to perform more
than one step sequentially, but the persisted artifacts must still preserve the
role boundaries.

## Executable surface

The current runtime adapter is:

```text
ION/04_packages/kernel/front_door_runtime_entry.py
```

It provides:

- `FrontDoorRuntimeGateway.ingest_user_message(...)`
- `FrontDoorRuntimeGateway.prepare_persona_response(...)`

and the CLI command family:

```text
python -m kernel front-door ingest ...
python -m kernel front-door return ...
```

## Ingress path

On user ingress the gateway must persist:

1. Persona Interface ingress artifact
2. Relay semantic-boundary packet
3. Steward routing envelope
4. front-door receipt

The Steward envelope must consume the Relay semantic-boundary packet, not raw user
text alone.

## Return path

On system return the gateway must persist:

1. Relay return package
2. Persona Interface response package
3. front-door receipt

Persona styling may alter presentation but must not alter authority, factual
content, or system-state meaning.

## Forbidden collapses

- Relay may not be used as the Persona Interface role.
- Persona Interface may not act as Steward/orchestrator.
- Steward may not claim user-bonded persona continuity.
- Raw user wording may not become governed system truth without Relay
  semantic-boundary translation.
- Persona style may not become semantic truth.

## Authority posture

The front-door runtime entry path is not a governed-write path by itself.
It creates boundary artifacts and routing envelopes. Deeper state changes still
must pass through kernel routing, validation, and governed-write law.
