# T32 — Runtime Report Profile Digest Trace

## Status

Active

## Purpose

Specify a bounded read-only trace packet that follows one lawful digest-profile selection into the downstream H1 operator digest it renders.

## Inputs

- `RuntimeReportProfileDigestTraceSelector`
  - `profile_name`
  - `profile_path`
  - `browser_query`
  - `browser_entry_index`
- governed runtime-report paths already used by H2/H4

## Selection Rules

- Exactly one route must be used:
  - direct selection by `profile_name`
  - direct selection by `profile_path`
  - browser selection by `browser_entry_index` with optional `browser_query`
- Browser selection must resolve through lawful H4 browse results.
- Resolved profiles must load through lawful H2 profile-definition JSON.

## Required Delegation

Digest rendering must occur through the existing H2 profile-digest path, which delegates into the H1 operator-digest renderer.

## Output Packet

`RuntimeReportProfileDigestTrace`

Required fields:

- generated time
- selection mode
- resolved profile identity
- definition paths when present
- selector detail
- optional browser-selection context
- rendered digest paths
- digest generation time
- digest family count
- digest total generations
- digest shared trigger/artifact/source-family unions
- digest runtime-ref union

## Governed Output Root

- `ION/05_context/runtime_reports/governance/digest_profiles/traces/`

## Boundary

This trace is read-only downstream witness material. It does not become kernel truth, doctrine, route authority, runtime authority, digest authority, or trace authority.
