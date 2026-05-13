# ION Extension Evolution Work Packets

These packets decompose the ChatGPT DOM cockpit and automation evolution into bounded implementation slices.

## Packets

1. `ION_EXT_DOM_COCKPIT_SHELL_PACKET.md`
2. `ION_EXT_DOM_ACTION_REGISTRY_PACKET.md`
3. `ION_EXT_CODEX_AGENT_COCKPIT_PACKET.md`
4. `ION_EXT_ARTIFACT_FILE_LANE_PACKET.md`
5. `ION_EXT_GUARDED_MACRO_AUTOMATION_PACKET.md`

## Recommended Order

```text
1. DOM cockpit shell
2. DOM action registry and YAML annotation
3. Codex agent cockpit
4. Artifact/file lane
5. Guarded macro automation MVP
```

## Shared Boundary

No silent send, no silent upload, no silent Codex run, no silent patch apply, no Git mutation, no production authority.
