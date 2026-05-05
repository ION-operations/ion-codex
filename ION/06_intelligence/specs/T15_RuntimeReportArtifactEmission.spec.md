# T15 — Runtime Report Artifact Emission Schema

## Scope

Defines the D1 contract for emitting selected runtime-state packets as bounded generated-state artifacts.

## Required emitter

### KernelRuntimeReportArtifactEmitter
Must support:
- `emit_scope_status_artifact(...)`
- `emit_planner_manifest_artifact(...)`
- `emit_review_packet_artifact(...)`

## Required artifact kinds

- `SCOPE_STATUS`
- `PLANNER_MANIFEST`
- `REVIEW`

## Default governed output roots

- `ION/05_context/runtime_reports/status/`
- `ION/05_context/runtime_reports/planner_manifests/`
- `ION/05_context/runtime_reports/reviews/`

## Required artifact metadata

Each emitted file must include:
- `artifact_kind`
- `authority_class`
- `generated_at`
- `source_ref`
- `relative_output_path`
- `runtime_refs` when present

## Required classification

All emitted runtime report artifacts are `GENERATED_STATE`.

## Constraints

- Output paths must be relative to the provided workspace root.
- Absolute output paths are invalid.
- Paths escaping the workspace root are invalid.
- Emission may write files but may not mutate kernel store/index/graph state.
- The packet body must come from the existing runtime reporting layer.
