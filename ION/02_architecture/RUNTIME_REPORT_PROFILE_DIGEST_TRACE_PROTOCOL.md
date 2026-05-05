# Runtime Report Profile Digest Trace Protocol

## Purpose

The Runtime Report Profile Digest Trace protocol defines a bounded read-only bridge from one lawful digest-profile selection into the downstream H1 operator digest rendered from that profile.

## Scope

This protocol applies to:

- direct digest-profile selection by profile name or governed profile path
- digest-profile selection through H4 browser entries
- delegated rendering through the existing H2 `write_profile_digest_packet(...)` path
- read-only trace packetization over the resulting profile-to-digest bridge

## Invariants

- Profile-to-digest tracing is downstream witness behavior only.
- Browser-selected traces must resolve through lawful H2 profile definitions.
- Digest rendering must delegate through the existing H2-to-H1 path.
- Trace packets may describe generated digest artifacts, but do not become digest authority.
- Trace packets do not become kernel truth, runtime authority, route authority, or control-plane state.

## Selection Modes

- `PROFILE_NAME`
- `PROFILE_PATH`
- `BROWSER_ENTRY`

Exactly one selection mode must be active for any trace request.

## Governed Outputs

- profile-rendered digest packets remain under `ION/05_context/runtime_reports/governance/digests/profiles/`
- profile-digest trace packets are written under `ION/05_context/runtime_reports/governance/digest_profiles/traces/`

## Boundary

The profile-digest trace layer is read-only and downstream. It preserves the lawful chain:

`profile browser/catalog → digest profile definition → operator digest`

It does not bypass H2/H1, and it does not promote browsing, profiles, digests, or traces into authority.
