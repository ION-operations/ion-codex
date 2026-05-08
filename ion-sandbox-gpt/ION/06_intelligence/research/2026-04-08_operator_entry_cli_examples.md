---
type: implementation_note
authority: A3_OPERATIONAL
created: 2026-04-08T23:20:00-04:00
status: ACTIVE
purpose: Show discoverable operator-entry examples for the live ION workflow carriers
---

# Operator Entry CLI Examples

All examples assume:
- `PYTHONPATH=ION/04_packages`
- repository root as working directory

## Status

```bash
python -m kernel status --format json
```

## Start supervised runtime

```bash
python -m kernel runtime --format json start --approval
```

## Drain supervised runtime

```bash
python -m kernel runtime --format json drain --reason "Pause bounded runtime"
```

## Hold one scope

```bash
python -m kernel control --format json hold-scope WORK_UNIT wu-123 --reason "Manual review hold"
```

## Dry-run daemon invocation

```bash
python -m kernel daemon --format json run --approval --dry-run --scope-type WORK_UNIT --scope-ref wu-123
```

## Replay latest resumable daemon run

```bash
python -m kernel replay --format json latest --approval
```

## Issue child work from a question/delta pair

```bash
python -m kernel child --format json issue-delta question-1 wu-parent delta-1 \
  --repo-root . \
  --constitution-excerpt "Relevant constitutional excerpt." \
  --template-spec "Bounded CODE/AUDIT template binding." \
  --agent-binding "Nemesis=Nemesis|Audit|T1.Risk.Audit|1|risk|cursor-composer|audit" \
  --approval --dry-run --context-mode COMPILED_RUNTIME
```

## Export one external execution packet

```bash
python -m kernel external --format json export wu-123 --approval
```

## Accept one external execution return

```bash
python -m kernel external --format json accept-return wu-123 submission.json --approval
```

## Render sequential/manual route scaffold

```bash
python -m kernel route implementation "Tighten packet taxonomy for takeover law"
```

## Legacy compatibility route invocation

```bash
python -m kernel implementation "Tighten packet taxonomy for takeover law"
```


## Validate one canonical packet

```bash
python -m kernel packet --format json validate \
  ION/05_context/comms/kernel_router_runs/2026-04-08_k2_packet_handoff_standardization/01_role_session.md
```
