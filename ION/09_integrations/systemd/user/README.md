# ION Local User Services

These files are repo-owned templates for the operator-local transport stack.
They are not installed automatically and they do not grant production or live
execution authority.

## Services

- `ion-chatops.service`: ChatOps bridge on `127.0.0.1:8767`.
- `ion-mcp-preview.service`: MCP preview on `127.0.0.1:8765`.
- `ion-mcp-tunnel.service`: Cloudflare named tunnel `ion-browser`.
- `ion-action-gateway.service`: Custom GPT Action Gateway on `127.0.0.1:8777`.
- `ion-action-tunnel.service`: Cloudflare named tunnel `ion-actions`.
- `ion-cockpit-app.service`: local-only cockpit UI on `127.0.0.1:8788`.

## Template Variables

Replace these placeholders before copying units to `~/.config/systemd/user`:

- `__ION_ROOT__`: absolute path to this repo, quoted if the path contains spaces.
- `__ION_PYTHONPATH__`: absolute path to `ION/04_packages`, quoted if needed.
- `__CLOUDFLARED__`: absolute path to `cloudflared`.
- `__ION_ACTION_GATEWAY_ENV__`: absolute path to an env file containing `ION_ACTION_GATEWAY_TOKEN=...`.

Do not commit rendered unit files that include local secret paths or token
values. The Action Gateway env file should be mode `0600`.

## Render Example

From the active project root:

```sh
mkdir -p ~/.config/systemd/user
cp ION/09_integrations/systemd/user/*.service.template /tmp/ion-systemd-render/
```

Then replace the placeholders in `/tmp/ion-systemd-render/*.service.template`,
drop the `.template` suffix, and copy the rendered files to
`~/.config/systemd/user/`.

For the current production checkout, the root path is:

```text
/home/sev/ION - Production/ION_CODEX FULL
```

If using an Action Gateway token currently stored as raw text, create a systemd
env file without printing the token:

```sh
mkdir -p ~/.config/ion
chmod 700 ~/.config/ion
printf 'ION_ACTION_GATEWAY_TOKEN=' > ~/.config/ion/action-gateway.env
cat ~/.cloudflared/ion_action_gateway.token >> ~/.config/ion/action-gateway.env
printf '\n' >> ~/.config/ion/action-gateway.env
chmod 600 ~/.config/ion/action-gateway.env
```

## Install Commands

After rendering the unit files:

```sh
systemctl --user daemon-reload
systemctl --user enable --now ion-chatops.service
systemctl --user enable --now ion-mcp-preview.service
systemctl --user enable --now ion-mcp-tunnel.service
systemctl --user enable --now ion-action-gateway.service
systemctl --user enable --now ion-action-tunnel.service
systemctl --user enable --now ion-cockpit-app.service
```

Check local status:

```sh
systemctl --user status ion-chatops.service ion-mcp-preview.service ion-mcp-tunnel.service ion-action-gateway.service ion-action-tunnel.service ion-cockpit-app.service
journalctl --user -u ion-chatops.service -u ion-mcp-preview.service -u ion-mcp-tunnel.service -u ion-action-gateway.service -u ion-action-tunnel.service -u ion-cockpit-app.service -n 100 --no-pager
python3 -S -m kernel.ion_local_service_status --ion-root . --probe-http --json
```

Expected smoke endpoints:

```text
http://127.0.0.1:8767/health
http://127.0.0.1:8765/health
http://127.0.0.1:8777/health
http://127.0.0.1:8788/
http://127.0.0.1:8788/model.json
https://ion.helixion.net/mcp
https://ion-actions.helixion.net/health
```
