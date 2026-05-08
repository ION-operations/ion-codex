---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-10T03:06:00-04:00
status: ACTIVE
---

# T67 — Allocator and settlement branch-control integration

Allocator must:
- read explicit branch-control posture before selecting child claims
- treat stale claims as decay candidates rather than permanent hidden budget pressure
- refuse recursive re-fan-out once the bounded depth ceiling is reached
- surface budget and drift posture in projection output

Settlement must:
- read explicit branch-control posture before classifying fan-in
- surface stale child returns as review pressure
- remain explicit when stale returns exist outside the active claim set
