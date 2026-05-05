# ION ChatOps Local Bridge

This localhost daemon accepts approved `ion_action` packets from the browser
extension and writes bounded ION actions, receipts, drafts, and Codex work
packets.

Run from the ION shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages \
  python3 -S ION/09_integrations/local_daemon/ion_chatops_bridge/ion_chatops_daemon.py \
  --ion-root . --serve --host 127.0.0.1 --port 8767
```

MVP endpoints:

```text
GET  /health
GET  /policy
POST /actions/validate
POST /actions/submit
GET  /actions/{action_id}
GET  /receipts/{receipt_id}
GET  /sandbox/returns
GET  /sandbox/returns/{return_id}
GET  /artifacts/attachables
GET  /artifacts/download/{download_token}
POST /artifacts/prepare-upload
POST /sandbox/returns/register
POST /sandbox/returns/file
POST /sandbox/returns/commit
POST /sandbox/returns/diff-preview
POST /sandbox/returns/queue-review
```

The daemon does not expose shell, delete, credential access, production deploy,
or git push. It writes receipts under
`ION/05_context/current/chatops_bridge/receipts/`.

The sandbox return endpoints land review material only under
`ION/05_context/inbox/chatgpt_sandbox_returns/` and use
`ION/04_packages/kernel/ion_chatgpt_sandbox_return_intake.py`. They do not apply
patches to live source; `queue-review` only creates a bounded Codex review work
packet.

The artifact endpoints expose only approved package/inbox candidates from
bounded ION roots. `prepare-upload` requires Braden approval, writes a download
ticket receipt, and serves a localhost file stream for the browser extension to
attempt a visible ChatGPT drag/drop. It does not click Send, apply patches, or
upload anything silently.
