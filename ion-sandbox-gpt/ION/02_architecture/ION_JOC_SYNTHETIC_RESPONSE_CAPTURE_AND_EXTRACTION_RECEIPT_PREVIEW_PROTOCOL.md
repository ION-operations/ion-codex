# ION/JOC Synthetic Response Capture and Extraction Receipt Preview Protocol

## Purpose

This protocol defines how a V64 provider-adapter readiness view may be converted into a V65 synthetic response capture and extraction receipt preview for cockpit rendering.

V65 is deliberately non-executing. It does not call a model provider, mutate a browser session, access credentials, submit a form, launch paid cloud resources, or claim production authority.

## Lineage

```text
V59 mission dispatch/model route preview
→ V61 dispatch authorization governor verdict
→ V62 operator approval queue and dry-run handoff
→ V63 dry-run dispatch execution trace
→ V64 provider adapter readiness and selector health
→ V65 synthetic response capture and extraction receipt preview
```

## Verdicts

```text
SYNTHETIC_RESPONSE_CAPTURE_PREVIEW_READY
BLOCKED_PROVIDER_READINESS_NOT_READY
BLOCKED_MISSING_CAPTURE_EVIDENCE
BLOCKED_FORBIDDEN_CAPABILITY
BLOCKED_LIVE_CAPTURE_REQUESTED
BLOCKED_SYNTHETIC_PAYLOAD_INVALID
```

## Canonical Rule

```text
Synthetic capture can preview the shape of extraction.
It cannot claim provider output, live dispatch, browser observation, or model truth.
```
