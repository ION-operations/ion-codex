# Runtime Report Bidirectional Trace Protocol

## Purpose

Define a bounded read-only witness packet that can present the lawful profile→digest path and the digest→profile path together without creating a new authority surface.

## Scope

This protocol sits downstream from:
- H2 digest profiles
- H3 digest-profile catalog packets
- H4 digest-profile browser packets
- I1 profile-to-digest trace packets
- I2 digest-to-profile reverse-trace packets

## Lawful behavior

- A bidirectional trace must start from exactly one side:
  - a lawful forward profile selection, or
  - a lawful reverse digest selection
- The packet must compose the existing I1/I2 paths rather than bypass them.
- When one direction is missing, any reconstruction must be labeled explicitly as reconstruction.
- Any mismatch between the two directions must be surfaced as explicit asymmetry, not hidden.

## Boundaries

- Read-only only
- No daemon
- No control plane
- No promotion into kernel truth, runtime authority, route authority, digest authority, profile authority, or bidirectional-trace authority

## Governed outputs

Bidirectional trace packets may be written under:

`ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/`
