# Codex Carrier Limits Context Protocol

```yaml
schema_id: ion.codex_carrier_limits_context_protocol.v1
created_at: 2026-05-10T16:05:00+00:00
status: ACTIVE
authority_rank: CONTEXT_DOMAIN_PROTOCOL
production_authority: false
live_execution_authority: false
secrets_authority: false
```

## Purpose

Codex carrier limits are a first-class ION context domain. The domain exists so
ION does not assume that a model's advertised context window, a CLI setting, a
hook payload, a tool output, or a plan-level usage allowance are the same thing.

## Core rule

Do not plan continuity, packaging, or carrier handoff from a single generic
"context window" number.

Every Codex-facing context plan must distinguish:

1. Model-level limits published by OpenAI.
2. Codex product or plan limits published by OpenAI.
3. Local Codex CLI configuration and version.
4. ION-enforced context packaging limits.
5. Tool transcript, command-output, hook, UI, and bridge limits.
6. Unknown or dynamic limits that require runtime verification.

## Local hard limits currently enforced by ION

These are repository-enforced limits and may be treated as current local truth
until the registry changes:

| Surface | Current limit | Source |
|---|---:|---|
| Codex Solo boot context default payload | 24000 bytes | `kernel.ion_codex_solo_context.DEFAULT_BOOT_CONTEXT_MAX_BYTES` |
| Mini index | 30 lines | `kernel.ion_codex_solo_context.MAX_MINI_LINES` |
| Capsule active context tail | 80 lines | `kernel.ion_codex_solo_context.MAX_CAPSULE_CONTEXT_LINES` |
| Long-horizon epoch size | 10 capsule rows | `kernel.ion_codex_solo_context.MAX_CAPSULE_ROWS_PER_EPOCH` |
| Hot context recent long-horizon epochs | 6 epochs | `kernel.ion_codex_solo_context.MAX_LONG_HORIZON_EPOCHS_IN_HOT_CONTEXT` |
| Route excerpt per file | 1600 characters | `kernel.ion_codex_solo_context.MAX_ROUTE_EXCERPT_CHARS` |
| Active-root SessionStart hook timeout | 10 seconds | `.codex/config.toml` |
| Parent SessionStart bridge hook timeout | 10 seconds | `/home/sev/ION - Production/.codex/config.toml` |
| Local ION MCP startup timeout | 10 seconds | `.codex/config.toml` |
| Local ION MCP tool timeout | 60 seconds | `.codex/config.toml` |

## Current external reference points

These values are not ION law. They are external reference points that must be
rechecked when model, plan, account, or Codex version changes.

| Surface | Current observation | Source |
|---|---|---|
| OpenAI model comparison for GPT-5.5 | 1,050,000 context window; 128,000 max output tokens | `https://developers.openai.com/api/docs/models/compare` |
| OpenAI Codex usage allowance | Depends on plan, task size, complexity, execution surface, and context held | `https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan/` |
| Codex CLI local capability | CLI can inspect the repo, edit files, and run commands in the selected directory | `https://developers.openai.com/codex/cli` |
| Local installed Codex CLI | `codex-cli 0.130.0` | `codex --version` |

## Planning consequences

- ION boot context must preserve recency before broad history.
- Long context capacity does not remove the need for Capsule, Mini, route, and
  receipt surfaces.
- If the boot context is capped, include a startup recency snapshot before any
  large historical block.
- If a response depends on a plan, rate, model, or product limit, verify the
  current official/runtime value before making a claim.
- If a bridge or UI may truncate output, write durable artifacts first and use
  chat text only as a summary.
- If a task requires large context, split it into named packages with evidence
  refs rather than relying on raw transcript continuity.

## Required audit posture

For every Codex carrier continuity change, verify at least:

1. Active-root startup can load `ION_CODEX_SOLO_CONTEXT_READY`.
2. Parent-root startup can load the active-root capsule bridge when applicable.
3. The latest capsule row survives default boot-context truncation.
4. New or changed limits are captured in
   `ION/05_context/current/codex_solo/CODEX_CARRIER_LIMITS_CONTEXT.json`.
5. The Codex Solo capsule receives a receipt for material context-domain changes.

## Non-claims

- This protocol does not grant production authority.
- This protocol does not grant live execution authority.
- This protocol does not grant secrets authority.
- This protocol does not claim that the full model context window is available
  to every Codex CLI, ChatGPT, hook, MCP, or tool-output surface.
- This protocol does not replace official OpenAI documentation for dynamic
  product, model, pricing, or plan limits.
