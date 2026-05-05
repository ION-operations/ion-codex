# ION CUSTOM GPT BUILD SPEC

## Purpose

This document defines how ION should be built as a custom GPT inside ChatGPT.

The build posture is:

- compact law in Instructions
- stable doctrine in Knowledge
- mutable state in uploaded working continuity bundles
- repeated continuity preservation through exported updated bundles
- encrypted archival outside ChatGPT

## Product posture

The custom GPT should be treated as:

- the **ION operating shell**
- not the whole mutable memory substrate
- not the encrypted vault
- not the complete long-horizon project database

## Recommended components

### Instructions
Use for:
- shell identity
- operating law
- bundle import/export behavior
- anti-drift rules
- continuity preservation rules
- failure handling rules

Do not use for:
- growing project state
- receipts archive
- long mutable history
- bulky protocol docs

### Knowledge
Use for:
- stable ION doctrine
- continuity doctrine
- bundle doctrine
- compact canonical examples
- restart/resume law
- artifact conventions

Do not use for:
- evolving user state
- raw session logs
- rapidly changing project notes

### Code Interpreter / Data Analysis
Enable it.

It is the strongest current ChatGPT-native surface for:
- reading uploaded working bundles
- validating manifests
- generating downloadable updated bundles
- compiling compact continuity artifacts

## Recommended first release posture

**File-only first.**

That means:

- no Actions required at first
- user uploads working continuity bundle
- GPT resumes from bundle + core doctrine
- GPT exports updated continuity bundle at session end
- local helper or manual user flow preserves the archive

This is the smallest serious product loop.

## Why file-only first

Advantages:
- lower complexity
- fewer security surfaces
- easier to validate
- keeps the continuity model legible

Actions should be deferred until a true external continuity service is justified.

## Required operating loop

### Start of session
1. user uploads working continuity bundle
2. GPT validates manifest and continuity generation
3. GPT resumes current state conservatively
4. GPT states resume posture explicitly

### During session
1. GPT works on user goals
2. GPT maintains current-state continuity
3. GPT updates live obligations, decisions, and summaries

### End of session
1. GPT compacts the working state
2. GPT updates manifest + continuity generation
3. GPT emits a downloadable updated continuity bundle
4. local user or helper saves and archives it

## Present conclusion

The right way to build ION as a custom GPT is not to force the GPT to contain everything.

The right way is:

- compact law in Instructions
- stable doctrine in Knowledge
- mutable continuity in uploaded bundles
- encrypted archival outside ChatGPT
