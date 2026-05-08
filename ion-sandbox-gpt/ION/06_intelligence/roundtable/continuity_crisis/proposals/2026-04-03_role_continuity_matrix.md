---
type: proposal
authority: A3_OPERATIONAL
template: SYSTEM_EVOLUTION
created: 2026-04-03T13:14:48-04:00
status: PROPOSED
topic: Role continuity matrix
---

# Proposed Role Continuity Matrix

> This matrix exists to make the continuity contract explicit per role.
> It is proposed working law for roundtable review.

| Role | Private MINI | Private CAPSULE | Boot reads private first? | May write root projections? | May emit task files? | Notes |
|------|--------------|-----------------|---------------------------|-----------------------------|----------------------|-------|
| Vizier | **Required** | **Required** | **Yes** | **Yes**, as temporary operator projection curator during recovery | **Yes** | Primary architect and dispatch hub |
| Vice | **Required** | **Required** | **Yes** | No | No | Conjugate Daimon; may emit `DAIMON_*` signals |
| Nemesis | **Required** | **Required** | **Yes** | No | No | External audit; may emit audit/escalation signals |
| Relay | **Required** | Lane-native private relay continuity instead of classic CAPSULE | **Partially** | No | No | User-facing courier; private Eunoia memory in relay lane; boot order still needs final normalization |
| Vestige | **Required** | Lane-native private archaeology continuity instead of classic CAPSULE | **Partially** | No | No | Persistent archaeology daemon; surfaces issues and reports; boot order/continuity language still needs final normalization |
| Atlas | **Required** | **Required** | **Yes** | No | No | Systems ATLAS builder; private source continuity already present and booted correctly |
| Mason | **Required** | **Required** | **Yes** | No | No | Execution-tier builder; updates only own source continuity and assigned outputs |
| Scribe | **Required** | **Required** | **Yes** | No | No | Archivist / utility role; may work on scaffolding, CI, archive, git |
| Thoth | **Required** | **Required** | **Yes** | No | No | Research role; writes only evidence/research plus own continuity |
| Codex | **Required** | **Required** | **Yes** | No | No | Provisional formalization landed; durable role still pending final hierarchy ratification |

## Interpretation notes

1. "May write root projections?" does not mean those projections are source truth.
2. Roles without classic `MINI` / `CAPSULE` names may still need equivalent private continuity objects in their own lane.
3. Task-file emission remains a controlled authority centered on Vizier unless explicitly expanded later.
4. "Partially" on boot order means the role's private continuity exists, but the boot sequence still needs one final alignment pass before being treated as fully clean.
