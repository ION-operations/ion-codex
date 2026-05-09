# ION Local User Services Systemd Runbook

This runbook makes the local transport stack persistent with `systemd --user`.
It keeps the MCP and Custom GPT Action Gateway endpoints online across shell
exits without changing ION authority rules.

Source templates live in `ION/09_integrations/systemd/user/`.

## Scope

Included:

- ChatOps daemon on `127.0.0.1:8767`.
- MCP preview on `127.0.0.1:8765`.
- Cloudflare tunnel `ion-browser` for `https://ion.helixion.net/mcp`.
- Action Gateway on `127.0.0.1:8777`.
- Cloudflare tunnel `ion-actions` for `https://ion-actions.helixion.net`.
- Local-only cockpit app on `127.0.0.1:8788`.

Excluded:

- Autonomous ION daemon loops.
- Production deploy authority.
- Live execution authority.
- Automatic installation during repo checkout.

## Operator Install Procedure

Render the templates into a temporary directory, replacing:

- `__ION_ROOT__` with `/home/sev/ION - Production/ION_CODEX FULL`.
- `__ION_PYTHONPATH__` with `/home/sev/ION - Production/ION_CODEX FULL/ION/04_packages`.
- `__CLOUDFLARED__` with the local cloudflared binary path, usually `/home/sev/.local/bin/cloudflared`.
- `__ION_ACTION_GATEWAY_ENV__` with a private env file path such as `/home/sev/.config/ion/action-gateway.env`.

Create the private Action Gateway env file without printing the token:

```sh
mkdir -p ~/.config/ion
chmod 700 ~/.config/ion
printf 'ION_ACTION_GATEWAY_TOKEN=' > ~/.config/ion/action-gateway.env
cat ~/.cloudflared/ion_action_gateway.token >> ~/.config/ion/action-gateway.env
printf '\n' >> ~/.config/ion/action-gateway.env
chmod 600 ~/.config/ion/action-gateway.env
```

Copy rendered `.service` files into `~/.config/systemd/user/`, then run:

```sh
systemctl --user daemon-reload
systemctl --user enable --now ion-chatops.service
systemctl --user enable --now ion-mcp-preview.service
systemctl --user enable --now ion-mcp-tunnel.service
systemctl --user enable --now ion-action-gateway.service
systemctl --user enable --now ion-action-tunnel.service
systemctl --user enable --now ion-cockpit-app.service
```

## Verification

From the repo root:

```sh
PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_local_service_status --ion-root . --probe-http --json
```

Expected local endpoints:

```text
http://127.0.0.1:8767/health
http://127.0.0.1:8765/health
http://127.0.0.1:8777/health
http://127.0.0.1:8788/health
http://127.0.0.1:8788/
```

Expected public endpoints:

```text
https://ion.helixion.net/mcp
https://ion-actions.helixion.net/health
```

Check journals:

```sh
journalctl --user -u ion-chatops.service -u ion-mcp-preview.service -u ion-mcp-tunnel.service -u ion-action-gateway.service -u ion-action-tunnel.service -u ion-cockpit-app.service -n 100 --no-pager
```
