# VAULT_CONTINUITY_BUNDLE_SCHEMA

## Purpose

This document defines the canonical schema for the **vault continuity bundle** used by the ION custom GPT product.

This is the locally archived encrypted bundle that preserves continuity across chat loss, reset, or catastrophic interruption.

## Core principle

The GPT should not operate directly on the vault bundle.

The vault bundle is for:
- archival
- lineage
- recovery
- encrypted persistence

The GPT operates on a decrypted **working** bundle.

## Vault bundle contents

A vault bundle may contain:

- sealed working bundle payload
- immutable manifest
- integrity metadata
- lineage references
- prior bundle reference
- recovery notes

## Canonical top-level layout

```text
ION_VAULT_CONTINUITY_BUNDLE/
  00_manifest/
    vault_manifest.yaml
    integrity_manifest.yaml
    lineage_manifest.yaml

  01_payload/
    working_bundle_payload.enc

  02_keywrap/
    wrapped_content_key.bin
    key_scheme.txt

  03_recovery/
    recovery_notes.md
    source_bundle_ref.yaml
```

## Minimum required fields

### `vault_manifest.yaml`
Must include:
- vault_bundle_id
- vault_schema_version
- archived_from_bundle_id
- archived_from_generation
- archived_at
- encryption_mode
- integrity_mode
- lineage_ref

### `integrity_manifest.yaml`
Must include:
- payload checksum
- wrapped-key checksum
- file list
- archive size
- optional signature reference

### `lineage_manifest.yaml`
Must include:
- prior vault bundle
- originating working bundle lineage
- continuity generation chain

## Encryption model

The design assumption is hybrid envelope encryption:

- payload encrypted symmetrically
- symmetric key wrapped with public-key encryption
- private decryption material stays local

This document does not hard-code one crypto stack; it defines the boundary.

## Recovery rule

A vault bundle is only useful if the local helper can:

1. validate it
2. decrypt it locally
3. reconstruct a working bundle
4. present that working bundle for upload into a fresh chat

## Present conclusion

The vault bundle is the continuity spine.
It is not the active GPT bundle; it is the sovereignty and recovery artifact.
