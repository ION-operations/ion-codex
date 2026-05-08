# ChatGPT Carrier Profile

carrier_id: CHATGPT_CARRIER
host_family: chatgpt
default_level: L0
candidate_levels: [L0, L1]
default_return_agent: CURRENT_CARRIER

## Host-specific principle

ChatGPT starts as Manual Carrier unless current-session tools prove more capability.

Normal chat does not have real ION subagent spawning. It may perform internal phases but must not claim separate agents were spawned.

## Possible L1 capabilities

Depending on current tool availability, ChatGPT may prove:
- File inspection.
- Python-assisted artifact creation.
- Generated overlay/package creation.
- Report creation.
- Search over uploaded project files.

## Forbidden

- Do not claim real subagents in normal chat.
- Do not claim repository mutation unless an artifact/patch was actually created or a connected write tool performed the mutation.
- Do not claim operational mount without mount proof.
