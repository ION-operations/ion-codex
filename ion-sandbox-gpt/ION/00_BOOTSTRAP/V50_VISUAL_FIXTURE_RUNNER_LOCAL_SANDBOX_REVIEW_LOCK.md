# V50 Visual Fixture Runner Local Sandbox Review Lock

Version: V50_VISUAL_FIXTURE_RUNNER_LOCAL_SANDBOX_REVIEW  
Authority: A3 visual-agent sandbox/security review gate  
Production status: NOT_PRODUCTION_AUTHORIZED

## Purpose

V50 freezes a sandbox/security review layer before ION is allowed to consider any stronger visual fixture execution, browser automation, DOM instrumentation, or visual-agent computer-control adapter.

V50 does **not** execute browsers. It does **not** create a live automation sandbox. It creates a review receipt that records whether a proposed visual fixture runner or capture adapter is still limited to local/dev evidence and whether forbidden capabilities remain blocked.

## Locked authority

Current authorized posture remains:

`LOCAL_DEV_SANDBOX_REVIEW_ONLY`

The Visual Agent may review planned local/dev visual fixture execution constraints, required isolation, artifact roots, evidence policies, and forbidden capabilities. It may not claim live browser execution authority, network authority, credential access, form submission authority, destructive action authority, persistent DOM mutation authority, or production visual automation authority.

## Next lawful move

`V51_LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC` may define a stricter local-only sandbox specification after V50 review passes, but it must still avoid production visual automation claims unless separately ratified.
