# T29 — Runtime Report Digest Profile

## Goal
Add a bounded named-profile layer for recurring operator digests.

## Required behavior
- Support profile definitions with a non-empty `profile_name`.
- Require one or more labeled temporal selectors.
- Allow profile definitions to be written under governed runtime-report profile paths.
- Allow profile definitions to be loaded by name or explicit governed relative path.
- Allow H1 operator digests to be rendered from loaded profiles.
- Keep profile definitions read-only and downstream from runtime-report witness surfaces.

## Governed outputs
- `ION/05_context/runtime_reports/governance/digest_profiles/*.md`
- `ION/05_context/runtime_reports/governance/digest_profiles/*.json`
- `ION/05_context/runtime_reports/governance/digests/profiles/*.md`
- `ION/05_context/runtime_reports/governance/digests/profiles/*.json`

## Non-goals
- No daemon or scheduler.
- No mutable UI or control plane.
- No promotion of profile definitions into doctrine, kernel truth, route authority, or runtime authority.
