# Steward current-phase truename and template update note

## Purpose

Record the correction that current-phase orchestration truth should not be flattened into the historical/common `Codex` carrier name.

## Current truth

- `Steward` is the current-phase orchestration truename.
- `Codex` remains the common IDE-native carrier / chassis alias in Cursor.
- Orchestration bindings now exist for Steward directly.
- Template evolution now has an explicit governed path.

## Why this matters

This restores separation between role truth and chassis convenience and prevents orchestration naming drift from silently redefining rank or identity.
