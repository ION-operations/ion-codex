# Runtime Report Bidirectional Temporal Protocol

## Purpose

This protocol defines a bounded, read-only temporal witness over successive generations of one lawful profile↔digest bridge family.

## Scope

The surface composes only existing lawful downstream materials:
- H2 digest-profile definitions
- H1 rendered digests
- I1 forward profile→digest traces
- I2 reverse digest→profile traces
- I3 bidirectional trace packets

## Selection Modes

One and only one selector mode is allowed per temporal request:
- `PROFILE_NAME`
- `PROFILE_PATH`
- `BROWSER_ENTRY`

## Generation Resolution

A bridge family is resolved by profile identity first. Digest generations are discovered from lawful rendered digest JSON packets and are admitted only when reverse tracing resolves them back to the selected profile.

## Temporal Aspects

The temporal packet tracks structural bridge aspects across generations, including:
- forward source kind
- reverse source kind
- reverse profile-resolution mode
- consistency markers
- asymmetries
- shared trigger / artifact / source-family sets
- runtime-ref sets

## Boundary

This packet is read-only downstream witness material.
It does not become:
- kernel truth
- doctrine
- route authority
- runtime authority
- digest authority
- profile authority
- bidirectional-trace authority
- temporal authority
- bridge-history authority
