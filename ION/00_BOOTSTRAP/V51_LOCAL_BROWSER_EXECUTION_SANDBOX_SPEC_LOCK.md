# V51 Local Browser Execution Sandbox Specification Lock

Version: V51_LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC  
Authority: A3 visual-agent sandbox specification candidate  
Production authority: false  
Browser execution authority: false

V51 defines the strict local/dev sandbox contract that any future browser execution prototype must satisfy before it can be considered. It does not execute a browser, navigate pages, submit forms, mutate persistent DOM state, import credentials, access accounts, or authorize production visual automation.

The lock preserves the V50 safety posture while allowing ION to reason about the exact control envelope required for a future local-only execution adapter.

Required controls:

- ephemeral browser profile
- fixture manifest required
- capture artifact hashing
- local files or loopback target restriction
- no external network
- no credentials or session import
- fixture/allowlist navigation only
- no persistent DOM mutation
- receipt/capture-artifact writes only
- Steward/VZ gate before any successor execution adapter

Forbidden by this lock:

- live browser execution authority
- unrestricted browser control
- external network access
- credential or session import
- account operations
- destructive actions
- form submissions
- purchases/submissions
- persistent DOM mutation
- production visual automation
- production readiness claims
