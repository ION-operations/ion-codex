# T31 — Runtime Report Digest Profile Browser

## Intent

Provide a bounded read-only browser layer over named runtime-report digest-profile
catalog entries and lawful profile definitions.

## Guarantees

- Loads profiles only through lawful H2/H3 surfaces
- Renders browse packets in markdown, HTML, and JSON
- Supports optional sidecar catalog packet emission
- Preserves downstream-only witness semantics

## Output Roots

- `ION/05_context/runtime_reports/governance/digest_profiles/browser/`
- optional catalog sidecars under `ION/05_context/runtime_reports/governance/digest_profiles/catalog/`

## Non-Goals

- No daemon or background refresh loop
- No mutable control plane
- No authority promotion
