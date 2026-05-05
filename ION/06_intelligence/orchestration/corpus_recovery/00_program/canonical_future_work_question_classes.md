# Canonical future-work question classes

## Purpose

This file defines the smallest stable set of question classes that future work should use when entering the atlas gate.

The goal is to reduce one recurring failure mode:
future work often began from a plausible local framing instead of first deciding what kind of question it actually was.

These classes are not ontology-final.
They are a working control layer for atlas-guided work.

## Canonical classes

### 1. Startup / current-branch truth
Use when the question is about:
- what the current extracted branch currently says
- current startup surfaces
- current routing/default packet law
- current branch-local readiness or state

Default posture:
- consult only

Primary center:
- current extracted ION branch

### 2. Runtime / API / session
Use when the question is about:
- API runtime
- sessions
- queueing
- scheduler tick/runtime server behavior
- execution policies

Default posture:
- consult only

Primary center:
- ION-BUILD

### 3. Activation / manager / swarm
Use when the question is about:
- activation authority
- manager behavior
- orchestrator logic
- swarm or mesh execution
- spawn/suspend/terminate/monitor behavior

Default posture:
- compare centers

Primary center:
- operation-victus

Secondary center:
- Project-Gemini
- current branch activation/startup law if the question also touches current branch routing posture

### 4. Template / meta-template / template evolution
Use when the question is about:
- template law
- template making
- template evolution
- the historical template-development center
- pure-template-state-machine direction

Default posture:
- recover first

Primary center:
- historical ION-BUILD / Aether template-development center

Secondary center:
- current branch bridge-era template-surface-evolution repair

### 5. Values / soul / linkage
Use when the question is about:
- ION/Aether values
- soul/coherence loss
- truename/domain/rank/template/protocol/context linkage
- where the center was weakened or buried

Default posture:
- compare centers

Primary center:
- values and soul recovery surfaces

### 6. Compactness / burden / implementation compression
Use when the question is about:
- compact executable memory
- operator burden
- current-branch explicitness vs older compact lines
- implementation compression

Default posture:
- compare centers

Primary centers:
- production precursor pair
- IONv2
- current branch

### 7. Archaeology / prior atlas / prior consolidation
Use when the question is about:
- what previous audits found
- prior atlas efforts
- previous failed consolidations
- external systems comparative libraries

Default posture:
- consult only

Primary centers:
- 00_CONSOLIDATED_ATLAS
- ProjectOpus
- ATLAS

### 8. Wrapper / provenance / variant interpretation
Use when the question is about:
- wrapper roots
- variant chains
- regenerated audit packages
- archive family interpretation

Default posture:
- consult only

Primary centers:
- archive register + wrapper provenance surfaces

### 9. Recovery gap / unresolved contradiction
Use when the question is about:
- unresolved contradiction
- missing evidence
- preserved tension between centers
- cases where the atlas explicitly says not to flatten yet

Default posture:
- recover first

Primary centers:
- conflict register
- missing evidence register

### 10. Current-branch bridge repair
Use when the question is about:
- a narrow repair inside the current branch
- startup/read-order clarification
- bridge-era repair work already acknowledged by the atlas

Default posture:
- bridge repair

Primary center:
- current branch, but only after atlas gate and conflict check

### 11. New extension candidate
Use only when the atlas has been checked and the work still appears genuinely absent.

Default posture:
- bounded extension

Primary requirement:
- prove non-reinvention first
- prove why no preserved center already covers the work

## Rule

If a question plausibly fits more than one class, the starting posture should usually be:
- compare centers
or
- recover first

not bounded extension.
