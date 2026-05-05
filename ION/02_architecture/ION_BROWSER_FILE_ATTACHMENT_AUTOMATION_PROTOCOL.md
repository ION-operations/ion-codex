# ION Browser File Attachment Automation Protocol

Status: draft implementation protocol

This protocol defines the bounded path for moving local ION files, ZIPs, and
artifact returns into ChatGPT Browser.

## Invariant

Browser file automation is operator augmentation, not silent upload authority.

```text
visible target
-> preview
-> explicit Braden approval
-> stale-target check
-> execute through a known carrier
-> log
-> receipt when ION state is touched
```

The browser extension may present and assist. The local daemon may package,
hash, ticket, and serve artifacts. Neither surface may upload arbitrary files,
click Send silently, expose secrets, or treat ChatGPT sandbox output as accepted
ION state.

## First Implemented Slice

Owner surfaces:

- `ION/04_packages/kernel/ion_chatops_bridge.py`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/`
- `ION/09_integrations/local_daemon/ion_chatops_bridge/`

Implemented browser-only lane:

```text
Artifacts tab
-> Attachables / Preview Drop Zone / Drop Latest
-> Drop Latest
-> Braden approval
-> daemon upload ticket
-> localhost artifact download
-> visible browser drag/drop attempt
```

This lane is intentionally allowed to fail closed. Browsers and ChatGPT may
reject synthetic drag/drop events. When that happens, the extension must show the
file name, size, sha256, and receipt path so Braden can use the manual attach
picker or a stronger future local macro lane.

ChatGPT accepts ordinary user drag/drop over broad page regions, so the primary
browser target is a page/composer drop zone rather than the attach/add-file
button. The attach button remains useful for a fallback OS file-picker lane.

Implemented local-operator lane:

```text
Artifacts tab
-> Preview Target / Dry Run Attach / Local Attach
-> Braden approval
-> daemon upload ticket
-> local operator geometry check
-> active ChatGPT window check
-> approved file-picker assistance
-> no Send click
-> receipt/log result
```

This lane uses a local desktop automation helper when available. The first
Linux implementation is `xdotool`-first: it can click the approved attach
control using extension-provided screen coordinates, paste/type the exact
approved artifact path into the file picker, and confirm the picker. It must
fail closed if the desktop tool is unavailable, the active window is not a
browser/ChatGPT surface, the attach target is stale/missing, or the file picker
is not detected.

`Local Attach` is still operator-present automation. It does not grant silent
upload authority and does not click Send.

`Local Attach` must dry-run before moving the pointer. Geometry failures are
classified as `LOCAL_OPERATOR_TARGET_GEOMETRY_INVALID` and no mouse movement is
allowed.

## Candidate Artifact Roots

The daemon may expose only bounded candidate material from policy-owned roots,
including:

```text
ION/05_context/current/chatops_bridge/exports/
ION/05_context/current/chatops_bridge/artifacts/
ION/05_context/inbox/chatgpt_sandbox_returns/
ION/06_artifacts/packages/
```

The daemon must reject protected path tokens and files above the configured
browser upload size limit.

## Local Operator Automation Lane

When browser-only drag/drop is unreliable, ION may use a stronger local
connected app lane. That lane is bounded by the daemon policy and remains
visible to the operator.

Permitted mechanisms:

- Chrome Debugger API, if explicitly granted and visible in the UI.
- Native messaging helper.
- Local desktop automation harness such as `xdotool` on Linux/X11.
- OS-level file picker assistance.

Required controls:

- exact target preview,
- operator target calibration when heuristic detection is wrong,
- selected file manifest and sha256,
- Braden approval,
- stale-target re-check,
- visible operation log,
- ION receipt when state is touched,
- no Send click unless separately approved.

Initial daemon endpoints:

```text
GET  /operator/status
POST /operator/attach-artifact
```

`/operator/attach-artifact` accepts only an approved daemon upload ticket and
extension-provided attach target rectangles. It prefers screen coordinates for
desktop automation and retains viewport coordinates as evidence. It verifies
the artifact ticket, rejects `send_after_attach`, records a receipt for
success/failure, and returns `verification: extension_should_confirm_upload_chip`
because ChatGPT upload completion must be observed in the browser surface.

Required geometry evidence:

```text
target_kind: attach_button
target_rect: viewport coordinates
target_screen_rect: desktop/screen coordinates
composer_rect: viewport coordinates
viewport: browser viewport dimensions
page_url: https://chatgpt.com/...
captured_at_ms: current capture timestamp
```

The daemon must reject missing, stale, out-of-viewport, out-of-display,
near-origin, or not-near-composer geometry before any desktop action.

## Calibrated Attach Target

The browser extension must not depend solely on heuristic DOM discovery for the
attach/add-file button. If the preview ring appears on the wrong page element,
the operator may arm a picker, click the real ChatGPT attach/add-file control,
and store a local selector for that element.

Calibration requirements:

```text
Settings -> Pick Attach Target
-> next non-ION page click is captured
-> selector, label, and rect are shown
-> Preview Target must ring that selected control
```

The selector is browser-local state, not ION authority:

```text
ION_CHATOPS_ATTACH_TARGET_SELECTOR
```

If a saved selector is present but the element is hidden, missing, or no longer
near the composer shell, the extension must fail closed and request
re-calibration. It must not silently fall back to a broad heuristic and click an
unrelated page control.

Layout tuning for the composer cockpit is also browser-local state:

```text
ION_CHATOPS_TAB_LIFT_PX
ION_CHATOPS_DRAWER_MAX_PX
```

These settings may adjust visual placement only. They do not expand file,
daemon, Codex, send-click, or git authority.

## Calibrated Drop Zone

The browser extension should support a separate drop-zone calibration path for
direct drag/drop uploads:

```text
Settings -> Pick Drop Zone
-> next non-ION page click is captured
-> selector, label, and rect are shown
-> Preview Drop Zone must ring that selected page/composer drop area
-> Drop Latest dispatches drag/drop events to that selected area
```

The selector is browser-local state:

```text
ION_CHATOPS_DROP_TARGET_SELECTOR
```

If the saved selector is hidden or stale, `Drop Latest` must fail visibly and ask
for re-calibration. It must not silently switch to a risky click target. This is
distinct from `ION_CHATOPS_ATTACH_TARGET_SELECTOR`, which is only for the
fallback file-picker/local-operator lane.

## Non-Authority

This protocol does not grant:

- production authority,
- secret access,
- arbitrary filesystem read,
- broad shell,
- direct source patch application,
- git push,
- silent upload,
- silent send.
