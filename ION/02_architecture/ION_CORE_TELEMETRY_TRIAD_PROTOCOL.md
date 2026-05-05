# ION Core Telemetry Triad Protocol

```yaml
schema_id: ion.core_telemetry_triad_protocol.v1
version_line: V106_CORE_TELEMETRY_TRIAD_SURFACES
production_authority: false
live_sse_db_authority: false
```

## Purpose

ION must expose runtime truth instead of letting carriers infer it from the
latest chat bubble or latest file timestamp. The first telemetry triad is:

```text
lane timeline
receipt hydration mapper
runtime debug overlay
```

## Required Projections

```text
ION/05_context/current/ACTIVE_LANE_TIMELINE_VIEW_MODEL.json
ION/05_context/current/ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json
ION/05_context/current/ACTIVE_RUNTIME_DEBUG_OVERLAY.json
```

## Integrity Rules

```text
requested lane and effective lane must both be visible
receipt hydration must resolve by utterance_id and/or atom_id, never recency
conflicts must be visible as blocked/conflict records
debug metrics must mark NOT_CONNECTED or PROJECTED_ONLY when live SSE/DB adapters are absent
```

## Non-Claims

These surfaces are runtime projections and UI view models. They do not claim
production readiness, live DB authority, live SSE authority, or accepted worker
state without ION return intake.
