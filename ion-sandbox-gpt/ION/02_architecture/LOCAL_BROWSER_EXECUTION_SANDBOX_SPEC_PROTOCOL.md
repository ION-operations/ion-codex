# Local Browser Execution Sandbox Specification Protocol

Version: V51_LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC  
Authority class: A3 planning/runtime-specification candidate  
Production authority: false

## Purpose

This protocol defines the strict local/dev sandbox contract for any future ION Visual Agent browser execution adapter.

V51 is deliberately a specification layer only. It does not run browsers. It does not grant a model or agent permission to operate a user browser. It does not authorize networked browsing, account sessions, destructive actions, submissions, purchases, or production visual automation.

## Background

The Visual Agent line now includes:

1. visual observation packets,
2. visual diagnosis receipts,
3. local visual harness receipts,
4. local browser capture adapter stubs,
5. before/after verification receipts,
6. visual regression fixture runner plans,
7. sandbox/security review receipts.

V51 adds the missing contract that must exist before an execution adapter can be safely prototyped.

## Required sandbox properties

A compliant future local browser execution sandbox must require:

- ephemeral browser profile,
- local fixture manifest,
- local files or loopback-only target origin,
- no external network access,
- no credentials or session import,
- fixture/allowlist-only navigation,
- no persistent DOM mutation,
- receipt/capture-artifact-only writes,
- hashed capture artifacts,
- explicit Steward/VZ gate before execution prototype,
- explicit refusal for credential-sensitive, destructive, purchase, account, and submission actions.

## Receipt requirement

Every sandbox specification must produce a `LocalBrowserExecutionSandboxSpecReceipt` containing:

- spec id,
- lineage refs,
- target-origin policy,
- network policy,
- credential policy,
- navigation policy,
- mutation policy,
- file-write policy,
- required controls,
- review findings,
- spec verdict,
- recommended next actions,
- forbidden capabilities set to false.

## Verdicts

V51 supports four verdicts:

- `LOCAL_BROWSER_SANDBOX_SPEC_ACCEPTED_SPEC_ONLY`
- `LOCAL_BROWSER_SANDBOX_SPEC_NEEDS_REMEDIATION`
- `LOCAL_BROWSER_SANDBOX_SPEC_REJECTED_FOR_FORBIDDEN_CAPABILITY`
- `LOCAL_BROWSER_SANDBOX_SPEC_BLOCKED_BY_STEWARD`

Only the accepted verdict permits a successor branch to prototype a local-only execution harness, and even then V51 itself does not grant execution authority.

## Hard prohibitions

V51 does not authorize:

- live browser execution,
- unrestricted browser control,
- external network access,
- credential/session import,
- account operation,
- destructive action,
- form submission,
- purchase/submission action,
- persistent DOM mutation,
- production visual automation,
- production readiness.

## Successor branch

The next lawful branch may prototype a local execution harness only if it preserves the constraints defined here and remains behind Steward/VZ gating.
