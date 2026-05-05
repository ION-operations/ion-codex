# ION Carrier Cycle Plan Protocol

The carrier does not decide which ION role carriers to spawn from chat language.

The carrier asks ION for a carrier-cycle plan. The plan is generated from the existing `SequentialKernelRouter` and materialized as role-session packets plus an active spawn plan.

Canonical command:

```bash
PYTHONPATH=ION/04_packages python3 -m kernel.ion_cycle_runner \
  --ion-root ION \
  --carrier cursor \
  --workstream implementation \
  --objective "<bounded objective>" \
  --spawn-policy required \
  --write-current \
  --json
```

The carrier then executes only role entries with `spawn: true`, in order, using their generated `session_packet_path` as the Task / role-carrier prompt source.

Spawn policies:

- `required`: spawn only kernel-required role passes.
- `objective`: spawn required passes plus optional passes when the objective is risk/governance/release/audit/continuity-sensitive.
- `full`: spawn all roles in the kernel trace.

No human phrase such as “continue” or “do your job” changes the spawn set. Only the generated plan does.

`MINI` and `CAPSULE` may appear as role-private continuity reads in generated sessions. They are not active packet authority. The active authority is the carrier-cycle plan plus the generated role-session packet.

Production authority and live execution authority remain false unless a later certified runtime explicitly changes that under separate law.
