# Codex Chat Response Carrier Service Enablement

date: 2026-05-08
status: IMPLEMENTED
authority: non-production, non-live

## Summary

Enabled the Codex Chat response carrier in the local `ion-mcp-preview` user
service environment and verified the authenticated cockpit chat path.

## Service Env

The user-service drop-in now contains response-carrier env gates:

```text
ION_CODEX_CHAT_RESPONSE_CARRIER_ENABLED
ION_CODEX_CHAT_RESPONSE_CARRIER_TIMEOUT_SECONDS
ION_CODEX_CHAT_RESPONSE_CARRIER_CAPTURE_JSON
ION_CODEX_CHAT_RESPONSE_CARRIER_SANDBOX
```

Secret-bearing env values remain outside repo docs.

## Validation

Systemd:

```text
systemctl --user daemon-reload
systemctl --user restart ion-mcp-preview.service
systemctl --user is-active ion-mcp-preview.service
```

Result:

```text
active
```

Service model check:

```text
carrier_enabled: true
carrier_verdict: ION_CODEX_CHAT_RESPONSE_CARRIER_READY
carrier_sandbox: workspace-write
carrier_timeout: 240
```

Authenticated `/cockpit/chat/turn` smoke:

```text
ok: true
assistant_author: codex_chat_engine
carrier_status: RETURN_CAPTURED
carrier_ok: true
```

Carrier run:

```text
ION/05_context/current/codex_capsule_chat/response_runs/codex_chat_response_20260508T143135Z679115_authenticated_cockpit_carrier_smoke_answer_in_one_concise_sentence_with_/run.json
```

Run proof:

```text
status: RETURN_CAPTURED
returncode: 0
unexpected_worktree_changes: []
selected_model: gpt-5.5
selected_reasoning_effort: medium
```

## Next

Use the cockpit chat normally and inspect quality. The next engineering work is
to improve response prompt shaping, conversation continuity, and UI surfacing
around carrier status, not to add another chat system.
