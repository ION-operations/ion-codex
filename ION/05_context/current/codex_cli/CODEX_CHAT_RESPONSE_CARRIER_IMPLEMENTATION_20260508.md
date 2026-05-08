# Codex Chat Response Carrier Implementation

date: 2026-05-08
status: IMPLEMENTED
authority: non-production, non-live
active_root: /home/sev/ION - Production/ION_CODEX FULL

## Summary

Implemented the response-only Codex CLI carrier under the existing Codex Chat
Engine. Normal `respond_only` chat turns can now use a real Codex CLI final
message when the carrier env gate is enabled, while preserving the local chat
engine response contract as fallback.

## Implemented

- `ION/04_packages/kernel/ion_codex_chat_response_carrier.py`
- `ION/tests/test_kernel_ion_codex_chat_response_carrier.py`
- `ION/04_packages/kernel/ion_dual_codex_chat.py`
- `ION/04_packages/kernel/ion_codex_chat_app_ui.py`
- `ION/tests/test_kernel_ion_dual_codex_chat.py`
- `ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md`

## Behavior

`record_chat_turn(... execution_mode="respond_only")` now:

1. mounts Capsule context;
2. builds a Codex Chat Engine turn;
3. selects skill, native lenses, model move, and response contract;
4. calls the response carrier if enabled;
5. uses the Codex CLI final message as the assistant response when the carrier
   succeeds;
6. falls back to the local chat-engine response contract when disabled or
   blocked;
7. records a `codex_chat_response_carrier` trace event either way.

The carrier stores run artifacts under:

```text
ION/05_context/current/codex_capsule_chat/response_runs/
```

Each run captures:

- prompt;
- run packet;
- stdout;
- stderr;
- JSONL events when enabled;
- latest Codex final message;
- selected model and reasoning effort;
- selected skill and native lenses;
- worktree drift status.

## Sandbox Decision

Initial live testing showed that this local Codex CLI cannot initialize a nested
session under `--sandbox read-only`; it fails before model execution with a
read-only filesystem session error.

The implemented live command therefore uses:

```text
codex exec ... --sandbox workspace-write --ephemeral --output-last-message <path> --json
```

The prompt explicitly declares response-only/no-file-edit policy, and the
carrier compares `git status --short` before and after the Codex run. A
response-only run is blocked if unexpected worktree changes appear.

## Env Gate

The carrier remains disabled unless explicitly enabled:

```text
ION_CODEX_CHAT_RESPONSE_CARRIER_ENABLED=1
ION_CODEX_CHAT_RESPONSE_CARRIER_TIMEOUT_SECONDS=240
ION_CODEX_CHAT_RESPONSE_CARRIER_CAPTURE_JSON=1
ION_CODEX_CHAT_RESPONSE_CARRIER_SANDBOX=workspace-write
```

The current service was not modified outside the project root in this pass.

## Validation

Offline test slice:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_codex_chat_response_carrier.py ION/tests/test_kernel_ion_codex_chat_engine.py ION/tests/test_kernel_ion_skill_activation.py ION/tests/test_kernel_ion_codex_solo_context.py ION/tests/test_kernel_ion_dual_codex_chat.py ION/tests/test_kernel_ion_codex_queue_runner.py ION/tests/test_kernel_ion_chatgpt_browser_connector_e2e_flow.py ION/tests/test_kernel_ion_local_cockpit_app.py ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py -q
62 passed
```

Live carrier-module smoke, run outside the current Codex tool sandbox so nested
Codex CLI could create its session:

```text
status: RETURN_CAPTURED
ok: true
response_preview: Current Capsule status is C-022 PLANNED, with no blocker recorded.
unexpected_worktree_changes: []
```

Service smoke:

```text
systemctl --user restart ion-mcp-preview.service
systemctl --user is-active ion-mcp-preview.service
curl -fsS http://127.0.0.1:8765/health
```

Result:

```text
active
ION_CHATGPT_BROWSER_HTTP_MCP_PREVIEW_READY
```

`/cockpit/chat` still redirects to login when unauthenticated.

## Non-Claims

This does not grant production authority, live execution authority, secrets
authority, deployment authority, git push authority, or state acceptance. It
does not replace the existing Codex work queue. It does not expose hidden chain
of thought.
