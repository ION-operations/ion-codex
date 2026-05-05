# Local MCP SDK Wrapper and Hosted HTTP Alpha Boundary Guide

V68 answers a product question: should ION immediately depend on the official MCP SDK, or should it keep its dependency-free local bridge canonical while wrapping the SDK optionally?

The V68 answer is:

```text
Keep the no-dependency bridge canonical for founder/local mode.
Add the official SDK as an optional wrapper seam.
Treat hosted HTTP as an alpha contract preview until auth, tenant isolation, and public hardening exist.
```

## Run the boundary report

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_sdk_wrapper_boundary --ion-root ION --json
```

## Read the SDK decision only

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_sdk_wrapper_boundary --ion-root ION --sdk-decision
```

## Interpretation

A passing V68 report means:

- stdio/local bridge semantics can be projected into a hosted-HTTP-shaped alpha boundary;
- forbidden tools still resolve to `REFUSED`;
- live execution is not authorized;
- official SDK presence or absence does not change ION authority;
- hosted cloud and OAuth remain uncertified.

A passing V68 report does not mean:

- ION has a public MCP endpoint;
- ChatGPT hosted app connection is certified;
- OAuth works;
- tenant isolation exists;
- provider dispatch is authorized;
- daemon loops may run.
