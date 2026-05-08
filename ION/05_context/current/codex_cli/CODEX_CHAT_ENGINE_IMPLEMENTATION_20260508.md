# Codex Chat Engine Implementation

date: 2026-05-08
status: IMPLEMENTED
authority: non-production, non-live

## Decision

Functionality takes priority over visual UI. The Codex Chat app now has a
dedicated chat-engine layer under the renderer. The engine owns message
interpretation, context mount, skill activation, native lens selection, model
move, response mode, carrier strategy, and response contract.

## Implemented Surfaces

- `ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md`
- `ION/03_registry/ion_native_lens_registry.yaml`
- `ION/04_packages/kernel/ion_codex_chat_engine.py`
- `ION/04_packages/kernel/ion_dual_codex_chat.py`
- `ION/04_packages/kernel/ion_codex_chat_app_ui.py`
- `ION/04_packages/kernel/ion_codex_solo_context.py`
- `ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py`
- `ION/04_packages/kernel/ion_codex_queue_runner.py`
- `ION/tests/test_kernel_ion_codex_chat_engine.py`
- `ION/tests/test_kernel_ion_dual_codex_chat.py`
- `ION/tests/test_kernel_ion_codex_queue_runner.py`
- `ION/tests/test_kernel_ion_chatgpt_browser_connector_e2e_flow.py`

## Behavior

The engine selects one response mode per turn:

- `answer`
- `clarify`
- `plan`
- `queue_work`
- `recover`
- `ion_handoff`

The engine then selects skill activation, native ION lenses, model move, context
refs, carrier strategy, response contract, and a conversational local response.

Normal chat now routes through the `codex-chat-answer` skill and GPT-5.5 model
move. Queued work routes through `codex-solo-work`, Mason/Codex native lens, and
the existing proof-gated Codex work queue. The queue request now preserves the
chat-engine turn and skill activation metadata so the Codex queue runner prompt
can carry the chat route into the actual Codex CLI worker.

## Native Lenses

The native registry maps ION roles into lightweight chat-engine lenses:
Persona, Relay, Steward, Vizier, Thoth, Mason/Codex, Nemesis, Vice, Scribe,
Context Cartographer, Ionologist, Template Curator, Vestige, and Atlas.

These are support lenses and routing hints, not extra user chores.

## Validation

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_codex_chat_engine.py ION/tests/test_kernel_ion_skill_activation.py ION/tests/test_kernel_ion_codex_solo_context.py ION/tests/test_kernel_ion_dual_codex_chat.py ION/tests/test_kernel_ion_codex_queue_runner.py ION/tests/test_kernel_ion_chatgpt_browser_connector_e2e_flow.py ION/tests/test_kernel_ion_local_cockpit_app.py ION/tests/test_kernel_ion_chatgpt_browser_mcp_http_preview.py -q
55 passed
```

## Non-Claims

This does not yet prove live ChatGPT-browser-grade answer quality. It creates
the routing, context, carrier, and proof contract that the GPT-5.5 Codex chat
response path should use. No production, live execution, provider API,
credential, or state-acceptance authority is granted.
