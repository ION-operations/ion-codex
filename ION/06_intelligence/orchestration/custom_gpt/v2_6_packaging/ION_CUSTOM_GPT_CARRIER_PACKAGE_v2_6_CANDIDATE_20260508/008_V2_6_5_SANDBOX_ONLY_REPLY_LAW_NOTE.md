# v2.6.5 Sandbox-Only Reply Law Note

Generated: 2026-05-09T01:32:42Z

This revision makes the Custom GPT response path stricter.

The carrier should not answer the user by freehand chat. Every visible user
reply must be a direct copy or rendering of the Persona Interface response
produced by the sandbox/package workflow:

```text
Persona ingress -> Relay boundary -> Steward route -> needed domain/agent/skill
-> proof/non-claims/receipt/export posture -> Persona handoff
```

If no route, domain, agent, or skill fits the request, the carrier must create a
candidate domain/agent proposal in sandbox text first, then hand off through
Persona. If the workflow is blocked, it must reply only with
`persona_gate_blocked`, the missing proof, and the next unblocker.

Validation:

- `001_GPT_INSTRUCTIONS_PASTE_8K.md` is 7,806 characters.
- Active-root instruction-gate test passed.
- Package-local instruction-gate test passed.

Non-claims:

- This does not create accepted canon domains automatically.
- This does not grant production or live execution authority.
- This does not authorize default Action/MCP calls.
