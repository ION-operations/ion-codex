# RUNTIME REPORT DIGEST PROFILE PROTOCOL

## Purpose

The digest-profile layer introduces **named selector-sets** for recurring runtime-report operator digests.
It exists to let operators define a stable digest recipe once and then render the corresponding H1 digest repeatedly without retyping selector families.

This layer is:
- read-only
- downstream from runtime-report witness surfaces
- downstream from G4 family summaries and H1 operator digests
- non-authoritative

This layer is **not**:
- kernel truth
- doctrine
- runtime authority
- route authority
- profile authority

## Core Objects

### `RuntimeReportDigestProfileSelector`
A labeled wrapper around one `RuntimeReportTemporalSelector`.

### `RuntimeReportOperatorDigestProfile`
A named profile with:
- `profile_name`
- `description`
- `tags`
- one or more labeled selectors
- read-only semantics

### `KernelRuntimeReportDigestProfiler`
The bounded manager that:
- validates profile definitions
- writes profile definition packets
- loads named profiles from governed paths
- renders H1 digests from profiles by delegating into `KernelRuntimeReportOperatorDigester`

## Governed Paths

Profile definitions live under:
- `ION/05_context/runtime_reports/governance/digest_profiles/`

Profile-rendered digests live under:
- `ION/05_context/runtime_reports/governance/digests/profiles/`

## Boundary

Digest profiles are **named selection definitions only**.
They may drive recurring digest rendering, but they do not outrank or replace:
- packet-index visibility
- provenance traces
- temporal provenance
- family summaries
- operator digests

They remain downstream descriptive configuration over witness material.
