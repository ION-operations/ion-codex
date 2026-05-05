# Carrier Session Protocol

status: proposed_integration_overlay_v0_1

## Purpose

This protocol defines the live session loop for a Carrier.

## Session loop

1. Start as L0 Manual Carrier.
2. Identify host profile from `carrier_registry.json`.
3. Read authority and Meta Carrier evolution protocol.
4. Produce mount proof.
5. Fill capability survey.
6. Request upgrade only if proven useful and allowed.
7. Await decision artifact.
8. Operate within approved level.
9. Receive all returns as CURRENT_CARRIER unless routed otherwise.
10. Journal or draft journal entries.
11. Produce result packet/report/checkpoint proposal.

## Return rule

All completed work returns to CURRENT_CARRIER unless a scheduler decision explicitly declares another target.

## Failure rule

If any automation, tool, or subagent route fails, the Carrier must:

1. Record the failure.
2. Switch to the manual mirror template.
3. Mark the result as manual fallback.
4. Continue only if the manual route satisfies required fields.
