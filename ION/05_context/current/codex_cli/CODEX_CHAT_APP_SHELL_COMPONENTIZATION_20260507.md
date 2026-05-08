---
type: implementation_orchestration
authority: A3_OPERATIONAL
created: 2026-05-07
status: IMPLEMENTED
production_authority: false
live_execution_authority: false
---

# Codex Chat App Shell Componentization

## Purpose

Move the active Codex Chat UI renderer out of the state/orchestration module and
into a dedicated app-shell module so the UI can evolve as a real application
surface instead of accumulating inside the chat model owner.

## Boundary

Preserved owners:

- `ion_dual_codex_chat.py` remains the model, lane, Capsule context, queue,
  turn trace, proof return, and ION comms owner.
- `ion_codex_chat_app_ui.py` owns the rendered Codex Chat shell only.
- The route continues to call `render_dual_codex_chat_html(...)` for import
  compatibility, but that function delegates to the dedicated UI module.

No second queue, second agent system, production authority, live authority,
secret surface, or raw hidden reasoning surface was added.

## UI Product Rules

- The rendered app identifies itself as `ION Codex Chat`.
- The chat region is `Codex Chat`.
- The prompt placeholder is `Ask Codex`.
- The composer uses one submit button, `Send`.
- Chat vs work execution is a mode selector: `Chat` or `Run task`.
- Inspector content remains in collapsed drawers: Timeline, Agents, Context,
  Runs, Receipts, ION Comms, and Settings.
- Historical receipt text that says "Codex Capsule Chat" is normalized before it
  appears in the user-facing app shell.

## Acceptance

- focused tests pass;
- real-root HTML smoke confirms required product strings are present;
- real-root HTML smoke confirms the old confusing strings are absent;
- active render path is delegated through `ion_codex_chat_app_ui.py`;
- obsolete in-file HTML/CSS renderer blocks were removed from
  `ion_dual_codex_chat.py`;
- Capsule receipt records this componentization pass.
