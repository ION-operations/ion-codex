# T33 — Runtime Report Digest Reverse Trace

## Status

Active

## Purpose

Specify a bounded read-only reverse trace packet that follows one rendered H1 operator digest back to the lawful H2 digest-profile definition and, when present, the downstream H3/H4 catalog/browser surfaces that exposed or selected it.

## Inputs

- `RuntimeReportDigestReverseTraceSelector`
  - `digest_json_path`
  - `digest_markdown_path`
- governed runtime-report profile, trace, catalog, and browser paths already used by H2/H3/H4/I1

## Selection Rules

- Exactly one route must be used:
  - direct selection by `digest_json_path`
  - direct selection by `digest_markdown_path`
- Selected digest JSON must be a lawful `RUNTIME_REPORT_OPERATOR_DIGEST` packet.
- Reverse resolution may use an existing I1 profile-digest trace when present.
- When no I1 trace exists, reverse resolution must use bounded digest-stem matching or structural digest matching against lawful H2 profiles.

## Output Packet

`RuntimeReportDigestReverseTrace`

Required fields:

- generated time
- digest selection mode
- profile resolution mode
- digest paths
- digest generation time
- digest family count
- digest total generations
- digest shared trigger/artifact/source-family unions
- digest runtime-ref union
- resolved profile identity and definition paths
- selector detail
- optional forward-link trace context
- optional browser surfaces
- optional catalog surfaces

## Governed Output Root

- `ION/05_context/runtime_reports/governance/digest_profiles/reverse_traces/`

## Boundary

This reverse trace is read-only downstream witness material. It does not become kernel truth, doctrine, route authority, runtime authority, digest authority, profile authority, or reverse-trace authority.
