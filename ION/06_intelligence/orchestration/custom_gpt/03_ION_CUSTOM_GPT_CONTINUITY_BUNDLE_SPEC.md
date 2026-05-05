# ION CUSTOM GPT CONTINUITY BUNDLE SPEC

## Purpose

This document defines the continuity-artifact architecture for the custom-GPT version of ION.

The central split is:

- **ION Core Pack** in GPT instructions + knowledge
- **Working Continuity Bundle** uploaded into active sessions
- **Vault Continuity Bundle** stored locally and encrypted

## Product thesis

The product is not “ChatGPT as memory.”

The product is:

**ION Core + User Continuity Bundle + Local Vault + Resume Loop**

## Bundle classes

### 1. Working Continuity Bundle
The GPT-readable, uploadable bundle.

Properties:
- decrypted
- compact
- current
- mutable during the session
- optimized for resume

### 2. Vault Continuity Bundle
The local encrypted archive.

Properties:
- encrypted at rest
- versioned
- immutable once sealed
- suitable for catastrophic chat loss recovery

### 3. Snapshot Bundle
Optional milestone artifact.

Properties:
- less frequent
- more complete than the working bundle
- useful for rollback or archaeology

## Internal bundle layers

A working continuity bundle should carry:

- identity
- current state
- context
- continuity summaries
- active temporal objects
- budget/forecast posture
- recent receipts
- compact history
- handoff/restart notes

## Core design rule

The GPT should normally operate on the **working bundle**.
The **vault bundle** should remain local and encrypted.

That means the trusted loop is:

1. local decrypt before upload
2. GPT reads/writes working bundle
3. GPT exports updated working bundle
4. local helper validates and re-encrypts archive copy

## Present conclusion

The continuity bundle is the real mutable substrate of the custom-GPT product.
The chat is only the live operating surface.
