# RUNTIME REPORT DIGEST PROFILE CATALOG PROTOCOL

## Purpose

Define a bounded, read-only catalog and index surface over named runtime-report digest
profiles. The catalog exists to list, summarize, and browse lawful H2 profile definitions
without promoting those definitions into kernel truth or bypassing the existing
profile-to-digest rendering path.

## Rules

1. Catalog entries must be derived from profile definition JSON whose `profile_kind` is
   `RUNTIME_REPORT_OPERATOR_DIGEST_PROFILE`.
2. The catalog must remain read-only and downstream from both digest profiles and operator
   digests rendered through them.
3. Querying the catalog may filter by profile name, tag, selector label, description, and
   bounded limit.
4. Catalog write-out is governed file emission only and does not mutate store, index,
   graph, doctrine, route authority, runtime authority, or profile authority.

## Governed Outputs

- `ION/05_context/runtime_reports/governance/digest_profiles/catalog/`

## Boundary

The catalog is a browse/list surface over named digest-profile definitions. It is not a
control plane, not a daemon surface, and not an authority layer.
