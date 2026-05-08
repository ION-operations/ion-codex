# V67 MCP SDK Adapter and Streamable HTTP Preview Lock

ION branch lock: `V67_OFFICIAL_MCP_SDK_ADAPTER_AND_STREAMABLE_HTTP_PREVIEW`.

This branch authorizes a local transport-preview and SDK-adapter seam only. It does not authorize hosted MCP, OAuth, Kubernetes, cloud multi-tenancy, live execution, provider dispatch, browser mutation, shell execution, credential access, direct governed-write mutation, or daemon-loop activation.

The branch is valid only while all MCP-facing results remain bounded to:

`READ_ONLY`, `DRY_RUN`, `APPROVAL_REQUIRED`, or `REFUSED`.

Any result claiming `LIVE_EXECUTED` invalidates the branch.
