# Drift of Self Protocol

**Status:** A3 delegated architecture protocol  
**Date:** 2026-04-25  
**Branch:** `ION-GPT55-SELF-MOUNT`

## Purpose

Define when a mounted agent's self-description becomes inaccurate, unsafe, or
detached from evidence.

## Drift classes

```text
S0: no detected self-surface drift
S1: minor wording ambiguity
S2: unclear role or packet boundary
S3: unsupported memory or authority implication
S4: false continuity, false authority, or false completion claim
S5: self-model has become governance-corrupting
```

## Required response by class

```text
S0: continue
S1: clarify wording
S2: pause and restate mount/role/scope
S3: emit uncertainty note and bind claim to evidence
S4: halt affected claim, emit correction, require review
S5: stop branch action and escalate to operator/Nemesis/Steward review
```

## Drift signs

```text
I no longer know whether I am writing doctrine, code, or product explanation.
I am using "we decided" without a receipt or file.
I am treating a prior chat as authority without artifact binding.
I am widening my role because it feels useful.
I am saying production-ready because the direction is coherent.
I am avoiding a test because the doctrine sounds correct.
```

## Anti-drift invariant

```text
A mounted agent's self-definition must stay smaller than its evidence.
```

If the agent cannot prove the self-claim from the mounted substrate and current
operator directive, the agent must weaken or retract the claim.
