# Runtime Report Digest Reverse Trace Protocol

## Purpose

The Runtime Report Digest Reverse Trace protocol defines a bounded read-only bridge from one rendered H1 operator digest back to the lawful H2 digest-profile definition and, when present, the H3/H4 catalog/browser surfaces that exposed or selected that profile.

## Scope

This protocol applies to:

- direct digest selection by governed digest JSON or markdown path
- reverse resolution into lawful H2 digest-profile definitions
- optional use of existing I1 profile-digest traces as forward evidence
- optional discovery of downstream H3 catalog packets and H4 browser packets that contain the resolved profile
- read-only reverse trace packetization over the resulting digest-to-profile bridge

## Invariants

- Reverse tracing is downstream witness behavior only.
- Reverse tracing must not bypass H2 profile definitions.
- When an I1 forward trace exists, it may be used as lawful evidence linking the digest to the profile and browser selection context.
- When no I1 forward trace exists, profile resolution may only occur through bounded digest-stem matching or structural digest matching against lawful H2 profiles.
- Reverse-trace packets may describe catalogs, browsers, profiles, and digests, but do not become digest authority, profile authority, or control-plane state.

## Selection Modes

- `DIGEST_JSON_PATH`
- `DIGEST_MARKDOWN_PATH`

Exactly one selection mode must be active for any reverse-trace request.

## Profile Resolution Modes

- `FORWARD_TRACE`
- `DIGEST_STEM`
- `DIGEST_MATCH`

Exactly one profile-resolution mode must be active for any reverse trace.

## Governed Outputs

- digest-profile reverse trace packets are written under `ION/05_context/runtime_reports/governance/digest_profiles/reverse_traces/`
- any referenced I1 forward traces remain under `ION/05_context/runtime_reports/governance/digest_profiles/traces/`
- referenced H3/H4 catalog/browser packets remain in their existing governed roots

## Boundary

The digest reverse-trace layer is read-only and downstream. It preserves the lawful chain:

`operator digest -> digest profile definition -> catalog/browser witness surfaces`

It does not promote digests, profiles, catalogs, browsers, or traces into authority.
