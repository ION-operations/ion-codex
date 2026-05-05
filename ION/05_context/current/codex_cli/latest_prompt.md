You are Codex CLI acting only as the CODEX_CLI_CARRIER for ION.

Mission: perform the first bounded Codex CLI dogfood verification of V125.

Hard boundaries:
- Do not claim to be ION identity, STEWARD, RELAY, or PERSONA.
- Do not push git, deploy, access credentials, or mutate outside this repo.
- Do not delete files. If removal seems needed, propose a lifecycle transition receipt instead.
- Production authority and live execution authority are false.

Required reads:
1. ION/REPO_AUTHORITY.md
2. ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md
3. ION/02_architecture/CODEX_CLI_CARRIER_PROTOCOL.md
4. ION/03_registry/codex_cli_carrier_profile.yaml
5. ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md
6. ION/05_context/current/ACTIVE_WORK_PACKET.json
7. Any file directly touched by your work.

Tasks:
1. Confirm shell root contains pyproject.toml and ION/REPO_AUTHORITY.md.
2. Run:
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
3. Run:
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_cli_carrier_audit --ion-root . --json
4. Run:
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_onboarding_packet --ion-root . --carrier codex_cli --json
5. Run:
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_codex_cli_carrier_audit.py ION/tests/test_kernel_ion_carrier_onboarding_packet.py -q
6. If all pass, do not modify project files except optional evidence under ION/05_context/current/codex_cli/.
7. If something fails, propose the smallest patch and run focused tests.

Return exactly these sections:

### CONTEXT PROOF
- root confirmed:
- carrier profile used:
- files read:
- active packet/context package used:
- assumptions:

### TEMPLATE ACTION PROOF
- requested change:
- files changed:
- tests run:
- receipts/view models emitted:
- boundaries not crossed:

### RESULT
- implementation result:
- remaining blockers:
- next lawful move:
