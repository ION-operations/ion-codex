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
-> Attachables
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

Implemented local-operator lane:

```text
Artifacts tab
-> Local Attach
-> Braden approval
-> daemon upload ticket
-> local operator target check
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
