CODEX SOLO MINI INDEX | 2026-05-09T17:35:55+00:00

ROLE: lookup/receipt index; Capsule is the minimum working context.
ACTIVE_CAPSULE: ION/05_context/current/codex_solo/CAPSULE.md
HOT_CONTEXT: ION/05_context/current/codex_solo/HOT_CONTEXT.md
LONG_HORIZON: ION/05_context/current/codex_solo/LONG_HORIZON.json
PACKAGES: ION/05_context/current/codex_solo/CONTEXT_PACKAGES.json
HISTORY: ION/05_context/current/codex_solo/history

MISSION: Codex Capsule Chat active-root branch continuity and recovery
PHASE: lost_session_recovered_after_push
LAST_RECEIPT: Recovered lost Codex CLI terminal session and verified final pushed branch state
BLOCKER: Project hook only auto-loads when Codex starts under the active ION root; global chats must inspect Codex history/session files and the project capsule explicitly.
NEXT: Use Capsule as minimum context; branch is pushed and synced; next decision is PR/review/merge order for feature/codex-capsule-chat-active-root and release/ion-sandbox-gpt-v1.

ACTIVE_TEMPLATE: codex_solo_lost_session_recovery

CAPSULE_LOOKUP:
- C-050 2026-05-08 PLANNED: Documented GitHub release strategy for ION_sandbox: recommend a dedicated release/ion-sandbox-gpt-v1 branch wi
- C-051 2026-05-08 IMPLEMENTED: Prepared sanitized ion-sandbox-gpt release root from ION_sandbox snapshot: repaired active GPT sandbox packet,
- C-052 2026-05-08 PUBLISHED: Published release/ion-sandbox-gpt-v1 to GitHub with curated ion-sandbox-gpt release root, candidate-domain/sou
- C-053 2026-05-08 PUBLISHED: Published feature/codex-capsule-chat-active-root with active-root Codex Capsule Chat, Mini/Capsule context sys
- C-054 2026-05-09 RECOVERED: Recovered lost Codex CLI terminal session and verified final pushed branch state

ROUTE_INDEX: ION/05_context/current/codex_solo/ROUTE.json validates active refs.
POLICY: Capsule is the minimum working context. Mini is a lookup/receipt index for capsule history. Neither overrides current repo authority, tests, receipts, or explicit operator instructions.
