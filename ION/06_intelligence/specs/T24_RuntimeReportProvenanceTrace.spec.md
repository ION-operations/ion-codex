# T24 — Runtime Report Provenance Trace Schema

## Intent

Specify the read-only lineage packet that resolves one runtime-report receipt across downstream witness layers.

## Scope

Applies only to downstream runtime-report witness surfaces produced after visibility projection.

## Required selector fields

### Provenance selector
- `entry_index: integer | null`
- `packet_index_pointer: string | null`
- `source_ref: string | null`
- `trigger_event: string | null`
- `artifact_kind: string | null`

At least one selector field must be present.

## Required trace fields

### Provenance trace
- `generated_at: string`
- `read_only_mode: boolean`
- `packet_index_path: string`
- `entry_index: integer`
- `packet_index_pointer: string | null`
- `trigger_event: string`
- `artifact_kind: string`
- `source_ref: string`
- `source_family: string`
- `reason: string | null`
- `runtime_refs: string[]`
- `layers: ProvenanceLayer[]`

### Provenance layer
- `layer_name: string`
- `label: string`
- `targets: ProvenanceTarget[]`

### Provenance target
- `target_kind: string`
- `label: string`
- `relative_path: string`
- `target_ref: string`
- `exists: boolean`
- `anchor_kind: string | null`
- `anchor_fragment: string | null`

## Required layer families

A complete trace supports these layer names:
- `ARTIFACT`
- `GOVERNANCE_REFLECTION`
- `GOVERNANCE_AGGREGATION`
- `VISIBILITY_PROJECTION`
- `NAVIGATION_PACKETS`
- `BROWSER_BUNDLES`
- `CROSSLINK_PACKETS`

Layers may contain zero targets when the corresponding downstream files were never written.

## Non-goals

- no new persistence family
- no background lineage crawler
- no authority promotion
- no write-capable UI or control plane

## Verification minimum

1. A trace can resolve from a packet-index pointer or entry index.
2. Artifact, reflection, aggregation, and visibility targets preserve normalized anchors or JSON pointers when present.
3. Navigation/browser/crosslink layers can detect matching downstream packet files when they exist.
4. Missing downstream files remain explicit empty layers.
5. Full kernel suite remains green.
