# Runtime Boundary Matrix

        This matrix keeps the product package honest about what each runtime
        mode can and cannot do.

        | Runtime mode | Purpose | Allowed | Forbidden |
        | --- | --- | --- | --- |
        | `CUSTOM_GPT_SANDBOX` | Browser-sandbox operation over a mounted product package and continuity data zip. | inspect mounted files, draft state updates, append receipts inside exported data package | claim persistent platform memory as state, mutate live ION repo, execute local daemon actions |
| `LOCAL_DAEMON` | Local bridge for approved package, artifact, queue, and receipt operations. | serve bounded endpoints, write approved inbox/receipt artifacts, expose status | unapproved source patching, secret exposure, silent live execution |
| `BROWSER_EXTENSION` | ChatGPT page perception, approval UI, artifact bridge, and operator cockpit surface. | detect page elements, show status, request approved daemon actions, assist visible workflows | silent send, hidden file upload, unbounded DOM automation, state acceptance |
| `CODEX_CLI_WORKER` | Bounded local filesystem implementation and validation worker. | read/edit scoped files, run tests, return proof-bearing diff | treat raw output as state, push/deploy without authority, widen scope silently |
| `GITHUB_DATA_PLANE` | Durable public collaboration, branch, PR, issue, and review surface. | mirror branch state, carry review history, publish docs/artifacts intentionally | become runtime authority, represent unpushed local truth, expose secrets/runtime credentials |
| `FULL_LOCAL_ION` | The live local repo and runtime organism with kernel, context, daemon, UI, and receipts. | run kernel validations, operate local queues under policy, generate product projections | claim product package is source truth, bypass active gates, erase state without custody |

        ## Product Boundary

        The product package can teach a Custom GPT how to operate portable ION
        continuity data. It is not the full local ION runtime, does not include
        the browser extension implementation, and does not grant Codex, daemon,
        GitHub, local filesystem, or production authority by itself.

        ## User-Facing Compression

        In ordinary use, describe these boundaries as:

        ```text
        I can keep project memory organized here, and I can export a project
        memory pack for continuation. Local execution, browser automation, and
        GitHub actions require their own connected tools and approvals.
        ```
