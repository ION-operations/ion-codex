# ION ChatOps Bridge Extension

Browser-side carrier adapter for Sev/ChatGPT Browser.

MVP behavior:

- detect rendered ChatGPT YAML/code blocks containing `ion_action:`;
- parse the strict `ion.chatops.action.v1` subset, including simple YAML lists;
- send candidates to the background worker;
- validate actions against the localhost daemon;
- show a compact top status rail near the ChatGPT header controls;
- show Rescan and Onboard controls in the top rail;
- fetch a compact Sev carrier onboarding/context brief from the local daemon and
  paste it into ChatGPT;
- render composer-attached tabs and an upward drawer for Status, Action, Agent,
  Packages, Sandbox, Automation, Artifacts, Diagnostics, and Log views;
- anchor composer tabs to the full visible composer shell, including uploaded
  image/file thumbnails when ChatGPT expands the composer;
- show subtle visual capture borders for composer input, attach/send/voice
  controls, selected source chips such as GitHub, and uploaded thumbnails;
- annotate rendered code/YAML blocks with compact workflow badges such as
  `ION CODE #N` and `ION YAML #N · valid`;
- show Codex queue runner status/queue and approval-gated prepare/start controls
  backed by `kernel.ion_codex_queue_runner`;
- request pasteable context packs and approval-gated package ZIPs backed by the
  existing lifecycle and safe full-project packagers;
- list ChatGPT sandbox returns and request approval-gated diff preview or
  Codex review queueing through the sandbox return intake owner;
- list attachable local package/inbox artifacts and request approval-gated
  browser drop tickets from the local daemon;
- attempt a visible ChatGPT drag/drop for an approved artifact without clicking
  Send;
- request approval-gated local operator attachment of an approved artifact
  through the daemon without clicking Send;
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

The Diagnostics tab includes the DOM capture registry. It shows whether the
extension sees the composer input, send/attach/voice controls, selected source
planes such as GitHub, uploaded thumbnails, and YAML/code block status. These
markers are visual perception aids only; they do not click, send, upload, or
mutate ION state.

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

## File And ZIP Attachment Lane

Protocol owner: `ION/02_architecture/ION_BROWSER_FILE_ATTACHMENT_AUTOMATION_PROTOCOL.md`

The Artifacts tab includes the first guarded file lane:

- `Attachables`: lists files the daemon considers safe to present for browser
  attachment from bounded package/inbox roots.
- `Preview Target`: draws a temporary green ring around the exact ChatGPT
  attach/add-file control the extension currently sees.
- `Dry Run Attach`: prepares the selected artifact and asks the daemon to
  validate target geometry/backend state without moving the pointer.
- `Drop Latest`: asks Braden for approval, asks the daemon for a one-use-ish
  localhost download ticket, fetches the file as a browser `File`, and attempts
  visible `dragenter`/`dragover`/`drop` events against the ChatGPT composer.
- `Local Attach`: asks Braden for approval, prepares a daemon upload ticket, and
  asks the local operator helper to open the ChatGPT attach control and select
  the exact approved artifact through the OS file picker. This path is
  `xdotool`-first on Linux, uses extension-provided screen coordinates, and
  fails closed if the active window is not a browser/ChatGPT surface, the attach
  target is stale/missing, or the file picker is not detected.

`Local Attach` performs a daemon dry run before any mouse movement. If geometry
is missing, stale, near the screen origin, outside the display, or not near the
composer, the daemon blocks with `LOCAL_OPERATOR_TARGET_GEOMETRY_INVALID`.

`Attachables` intentionally shows a compact selected-artifact summary rather
than dumping the full daemon JSON. The selected artifact is the same latest
candidate used by `Drop Latest` and `Local Attach`.

Browsers do not allow ordinary page scripts to set local file inputs to
arbitrary paths. ChatGPT or the browser may also reject synthetic drag/drop.
When that happens, the panel still provides the manifest/hash/receipt so Braden
can use `Local Attach`, the manual attach picker, or a future native/debugger
lane.

The intended ION path is:

1. local daemon creates or exposes a public-safe package with manifest and
   sha256;
2. extension shows exact file path, size, hash, and intended chat target;
3. Braden approves the attach operation;
4. extension uses the most reliable available browser path:
   - approved visible synthetic drag/drop where accepted;
   - approved local operator file-picker assistance where available;
   - user-visible attach picker guidance;
   - approved downloaded package handoff;
   - future Chrome-extension/native or debugger-mediated upload lane if
     explicitly gated;
5. ION records the package/export receipt and any returned sandbox artifact.

No file should be uploaded without explicit user approval, a manifest, and a
receipt when ION state is touched. This MVP does not click Send.
