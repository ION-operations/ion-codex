# T30 — Runtime Report Digest Profile Catalog

## Intent

Add a bounded read-only catalog/index layer over H2 digest-profile definitions so named
profiles can be listed, summarized, filtered, and packetized for operator browsing.

## Inputs

- Workspace root
- Digest profile definitions under `ION/05_context/runtime_reports/governance/digest_profiles/`
- Optional query fields:
  - `profile_name_contains`
  - `tag`
  - `selector_label_contains`
  - `description_contains`
  - `limit`

## Outputs

- In-memory catalog result with matched profile entries
- Governed markdown/json packets under:
  - `ION/05_context/runtime_reports/governance/digest_profiles/catalog/`

## Guarantees

- Read-only mode only
- Downstream from digest profiles and operator digests
- No promotion into doctrine, kernel truth, route authority, runtime authority, or catalog authority
