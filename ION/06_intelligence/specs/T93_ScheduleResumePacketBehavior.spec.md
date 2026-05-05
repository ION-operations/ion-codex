---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T16:33:00-04:00
status: ACTIVE
---

# T93 — Schedule resume packet behavior

When replayed active-cycle state is resumable, M12 must render one minimal canonical `role_session` packet.

The packet must:
- bind the scope explicitly,
- state the active cycle stage,
- name the next action,
- list required reads,
- and remain valid under packet law.
