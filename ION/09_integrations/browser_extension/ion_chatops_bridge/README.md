# ION ChatOps Bridge Extension

Browser-side carrier adapter for Sev/ChatGPT Browser.

MVP behavior:

- detect rendered ChatGPT YAML/code blocks containing `ion_action:`;
- parse the strict `ion.chatops.action.v1` subset, including simple YAML lists;
- send candidates to the background worker;
- validate actions against the localhost daemon;
- show a compact in-page toolbar near the ChatGPT header controls;
- show Rescan and Onboard controls in the toolbar;
- fetch a compact Sev carrier onboarding/context brief from the local daemon and
  paste it into ChatGPT;
- expand downward into tabbed Status, Action, Agent, Packages, Sandbox,
  Diagnostics, and Log views;
- show Codex queue runner status/queue and approval-gated prepare/start controls
  backed by `kernel.ion_codex_queue_runner`;
- request pasteable context packs and approval-gated package ZIPs backed by the
  existing lifecycle and safe full-project packagers;
- list ChatGPT sandbox returns and request approval-gated diff preview or
  Codex review queueing through the sandbox return intake owner;
- show an approval modal for Braden;
- insert a known-good Sev re-entry prompt into the ChatGPT composer;
- keep fabricated smoke/Codex work-packet actions under Diagnostics as local bridge tests;
- submit approved actions to `http://127.0.0.1:8767/actions/submit`;
- paste or copy compact receipt summaries.

The extension is not an authority source. It does not write files directly,
access credentials, push git, or run shell commands.

## Load Unpacked

This MVP includes plain JavaScript under `dist/` so Chrome can load it without a
TypeScript build step:

1. Open `chrome://extensions`.
2. Enable Developer mode.
3. Select **Load unpacked**.
4. Choose this directory:
   `ION/09_integrations/browser_extension/ion_chatops_bridge/`

The `src/` TypeScript files are the source scaffold for the later build system.
For now, keep `dist/content.js` and `dist/background.js` in sync when behavior
changes.

The extension icon assets live in `icons/` and are wired into both the manifest
extension icon set and the toolbar action icon.

## Emergency Safe Mode

If ChatGPT fails to load with the extension enabled, disable the content script
without uninstalling the extension:

```js
localStorage.setItem("ION_CHATOPS_SAFE_MODE", "disabled")
```

Then reload ChatGPT. The content script exits early and prints a compact console
message. To re-enable it:

```js
localStorage.removeItem("ION_CHATOPS_SAFE_MODE")
sessionStorage.removeItem("ION_CHATOPS_SAFE_MODE")
```

Reload the page after removing the flag.

Automatic scanning is deliberately throttled. MutationObserver events schedule a
single debounced scan over code/YAML-bearing surfaces, ignore the extension's own
panel/modal updates, and avoid broad whole-page scans. Use the manual `Rescan`
button after ChatGPT finishes rendering a YAML block.

## YAML Subset

The MVP parser supports the canonical `ion.chatops.action.v1` shape used by Sev:

- nested mappings by indentation;
- flat Sev metadata aliases such as `callsign`, `carrier`, `human_sovereign`,
  and `requires_approval`, which are canonicalized into `actor` and `authority`;
- scalar strings, booleans, numbers, `null`, and `[]`;
- block scalars with `text: |`;
- scalar lists such as `receipts.requested`;
- default receipts for MVP intents when a flat action omits `receipts`;
- optional ChatGPT code fence or `YAML` label text around the action block.

It does not support arbitrary YAML anchors, aliases, flow maps, or mixed
list-of-object structures. Larger artifacts should move through refs or the
daemon artifact flow rather than advanced YAML syntax.

A known-good smoke action is available at `examples/SEV_CHATOPS_SMOKE.yaml`.
If ChatGPT emits prose about YAML instead of a top-level `ion_action:` mapping,
the extension will correctly reject it as `missing_top_level_ion_action`.

Normal operation is not driven by the local test buttons. Sev should render a
real YAML/code block whose first YAML key is `ion_action`. ChatGPT may display
that as a styled code block rather than literal triple-backtick text; the
extension detects the rendered block and Braden approves or rejects the
resulting action.

Use the expanded Diagnostics tab only for local bridge checks:

- `Onboard`: fetches the current ION status, Sev carrier profile/onboarding
  summary, active queue paths, and ChatOps policy from the daemon, then inserts
  that boot context into ChatGPT. The inserted context uses
  `ion_action_example`, not a runnable top-level `ion_action`, so it cannot
  accidentally enqueue placeholder work.
- `Submit Smoke Test`: submits a known-good `write_file_draft` action through the approval
  modal and daemon.
- `Queue Codex Test Work`: submits a `create_codex_work_packet` action so local Codex can
  inspect the repo and return through ION receipts.

The Agent tab is the local Codex carrier cockpit. `Status` and `Queue` are
read/status projections. `Prepare Next` writes a prepared run packet but does
not start Codex. `Start One` starts one bounded queue-runner worker after
Braden approval.

The Packages tab is for moving context into ChatGPT or another carrier sandbox.
`Context Pack` pastes a compact current-state packet into the composer.
`Compact ZIP` and `Safe Full ZIP` create local package artifacts through the
existing ION packagers and copy the resulting path, sha256, and receipt summary.

The Sandbox tab projects returns under
`ION/05_context/inbox/chatgpt_sandbox_returns/`. `Returns` is a read-only queue
projection. `Diff Preview` runs the bounded preview/check path for the latest
return after Braden approval. `Queue Review` creates a focused Codex review
packet after Braden approval. None of these controls apply patches to live
source.
