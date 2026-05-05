# RUNTIME REPORT ARTIFACT PROTOCOL

## Purpose

Define the D1 rule for materializing selected runtime-state packets as bounded generated artifacts.

## Covered packet families

- scope status reports
- planner-manifest packets
- review packets

## Output discipline

Runtime report artifacts must:
- write only under an explicit workspace root supplied at call time
- default to governed relative paths under `ION/05_context/runtime_reports/`
- reject absolute paths
- reject relative paths that escape the workspace root

## Authority class

All emitted runtime report artifacts are `GENERATED_STATE`.
They are operational visibility surfaces, not doctrine, not ratified truth, and not runtime authority.

## File form

Each emitted artifact must contain:
- self-classifying frontmatter including artifact kind, authority class, generated time, and source ref
- the rendered packet body produced by the C4 reporting layer

## Constraints

- Emission may write files, but it may not mutate kernel records.
- Emission must preserve continuity-law separation: prose continuity remains distinct from machine-readable runtime state.
- Emission must not imply dispatch permission when runtime posture blocks dispatch.
- Emission must not create a new persistence family or autonomous reporting daemon claim.
