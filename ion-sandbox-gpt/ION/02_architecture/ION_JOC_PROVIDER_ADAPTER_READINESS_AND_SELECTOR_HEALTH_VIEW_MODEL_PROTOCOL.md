# ION/JOC Provider Adapter Readiness and Selector Health View Model Protocol

## Purpose

This protocol defines the V64 view model that sits after V63 dry-run dispatch trace rendering and before any future live provider execution branch.

V64 gives the cockpit a bounded way to answer:

```text
Which provider adapter would be selected?
Is its no-op adapter lane ready?
What access method is being previewed?
Is session/provider health sufficient for a dry-run readiness display?
Which governor and trace evidence supports the selector state?
What capabilities remain explicitly blocked?
```

## Inputs

V64 consumes:

```text
V63 dry-run trace reference
V63 trace verdict
V63 execution mode
selected target/provider
provider adapter id
access method and compute ring
governor snapshot references
provider/session evidence references
no-op adapter reference
blocked capability map
```

## Required boundary

V64 is view-model only. It may not:

```text
call external model providers
mutate browser sessions
read credentials
submit forms
launch paid cloud resources
write canonical graph state
rewrite source summaries
grant production authority
```

## Output

A valid V64 model emits:

```text
provider readiness verdict
adapter health lane
session health lane
selector priority lane
no-op invariant lane
governor evidence lane
blocked capability lane
next required action
```

## Valid ready state

The ready state is:

```text
PROVIDER_ADAPTER_READY_FOR_DRY_RUN_SELECTION
```

This means only that the cockpit can render adapter readiness for a dry-run/no-op route. It does not authorize live dispatch.
