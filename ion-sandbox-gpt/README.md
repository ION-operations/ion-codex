# ION Sandbox GPT

Release candidate: v1.4 public candidate

This package contains the operational ION body needed for a fresh Custom GPT or
browser GPT sandbox to run ION as a single-carrier sequential role-phase system,
plus the Custom GPT adapter and seeded starter data needed for portable product
use.

The 42-tool MCP connector lane remains supported as an optional external-local
ION/Codex communication path, but this package does not require MCP, local
services, Cloudflare tunnels, or Codex CLI to operate.

This is a non-production, non-live release candidate. It does not grant secrets,
deployment, git push, arbitrary shell, live execution, or production authority.

See:

- `START_HERE.md`
- `ION/REPO_AUTHORITY.md`
- `ION/02_architecture/ION_MOUNT_CONTRACT.md`
- `ION/02_architecture/SINGLE_CARRIER_SEQUENTIAL_RUNTIME_PROTOCOL.md`
- `ION/03_registry/gpt_sandbox_carrier_profile.yaml`
- `ION/07_templates/carriers/GPT_SANDBOX_CARRIER_SESSION_PACKET.md`
- `product/custom_gpt_adapter/CUSTOM_GPT_INSTRUCTIONS_8000.md`
- `product/package_guides/ION_FULL_GPT_SANDBOX_AGENT_PACKAGE.md`
- `RELEASE_MANIFEST.json`
- `RELEASE_READINESS.md`
