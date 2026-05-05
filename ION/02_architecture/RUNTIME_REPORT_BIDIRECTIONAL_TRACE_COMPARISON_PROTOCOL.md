# Runtime Report Bidirectional Trace Comparison Protocol

## Purpose

Define a bounded read-only witness packet that can place two or more lawful bidirectional profile↔digest traces side by side without creating a new ranking or authority surface.

## Scope

This protocol sits downstream from:
- I3 bidirectional trace packets
- I1 profile-to-digest trace packets
- I2 digest reverse-trace packets
- H2 digest profiles
- H3 digest-profile catalog packets
- H4 digest-profile browser packets

## Lawful behavior

- A comparison must include at least two lawful bidirectional-trace inputs.
- Each input must be exactly one of:
  - a live lawful bidirectional selector, or
  - a written bidirectional-trace JSON packet
- The comparison must surface structural agreement and divergence explicitly.
- Any asymmetry already present inside a bidirectional trace must be carried through, not hidden.
- The comparison may summarize structure, but it must not rank traces or declare one bridge superior.

## Boundaries

- Read-only only
- No daemon
- No control plane
- No promotion into kernel truth, runtime authority, route authority, digest authority, profile authority, bidirectional-trace authority, or comparison authority

## Governed outputs

Comparison packets may be written under:

`ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/comparisons/`
