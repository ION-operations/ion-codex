# RUNTIME REPORT DIGEST PROFILE BROWSER PROTOCOL

## Purpose

Define a bounded, read-only browser surface over lawful runtime-report digest-profile
catalog entries and underlying profile definitions. This layer exists for operator
browsing and inspection only.

## Inputs

- Workspace root
- `RuntimeReportDigestProfileCatalogQuery`
- Governed relative output roots

## Outputs

- Browser markdown packets
- Browser HTML packets
- Browser JSON packets
- Optional sidecar catalog packets delegated through H3

## Boundary

- Read-only
- Downstream from H2 digest profiles and H3 catalog packets
- Does not become kernel truth, doctrine, runtime authority, route authority, or browser authority
