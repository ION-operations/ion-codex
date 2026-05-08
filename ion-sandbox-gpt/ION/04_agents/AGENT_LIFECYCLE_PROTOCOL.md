# ION Agent Lifecycle Protocol

status: proposed_integration_overlay_v0_1

## Agent states

- requested
- approved
- active
- returned
- accepted
- rejected
- archived
- failed

## Required lifecycle fields

Each agent activation or manual phase must record:

- parent carrier
- parent task
- assigned role
- spawn reality
- authority source
- allowed inputs
- forbidden actions
- output packet path
- return target
- journal path or journal draft path
- close condition

## Carrier boundary

The Carrier is the session boundary. It receives returns, verifies required fields, and routes back to Kernel/Scheduler or manual fallback.

## Manual phase lifecycle

Manual phases are allowed in L0/L1 but must be identified as phases, not spawned agents.
