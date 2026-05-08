# Codex Chat Pending-State UX Fix

date: 2026-05-08
status: IMPLEMENTED
authority: non-production, non-live

## Summary

Fixed the cockpit chat submit experience for slow Codex carrier responses.

Before this fix, the browser submitted a blocking form. During a slow response,
the text stayed in the composer, the user message did not appear in the chat,
the send button gave no useful state, and repeated clicks could create
duplicates.

## Implemented

- The chat form now submits through the bundled cockpit app script.
- On submit, the user message is immediately appended to the chat timeline.
- A pending Codex bubble appears immediately.
- The textarea is cleared immediately.
- Send mode controls and the send button are disabled while the request is in
  flight.
- The send button label changes to `Sending...`.
- Duplicate submits are blocked with a `form.dataset.submitting` guard.
- The response carrier result replaces the pending bubble.
- Queue/run execution status is appended when returned.
- The cockpit CSP now allows the bundled inline script and same-origin fetch.

## Validation

Tests:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_codex_chat_response_carrier.py ION/tests/test_kernel_ion_codex_chat_engine.py ION/tests/test_kernel_ion_skill_activation.py ION/tests/test_kernel_ion_codex_solo_context.py ION/tests/test_kernel_ion_dual_codex_chat.py ION/tests/test_kernel_ion_codex_queue_runner.py ION/tests/test_kernel_ion_chatgpt_browser_connector_e2e_flow.py ION/tests/test_kernel_ion_local_cockpit_app.py ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py -q
63 passed
```

Service:

```text
systemctl --user restart ion-mcp-preview.service
systemctl --user is-active ion-mcp-preview.service
```

Result:

```text
active
```

Authenticated served HTML contains:

- `data-busy-label="Sending..."`
- `Codex is working on this response. The carrier can take a few seconds`
- `form.dataset.submitting === "true"`
- `payload.execution_status_turn`
- `textarea.value = ""`

Authenticated post-fix carrier smoke:

```text
ok: true
carrier_status: RETURN_CAPTURED
carrier_ok: true
unexpected_worktree_changes: []
```

## Known Test Gap

Playwright is not installed in this environment, so this pass did not run a
true headless browser click test. The server path, generated HTML, CSP, and
authenticated JSON chat-turn path were tested directly.
