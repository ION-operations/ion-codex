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
```

The daemon does not expose shell, delete, credential access, production deploy,
or git push. It writes receipts under
`ION/05_context/current/chatops_bridge/receipts/`.
