# Read First

You are mounting the ION Browser GPT Queue Workflow Authoring Package.

Use this package only when the user explicitly wants a saved or importable
queued workflow for the ION ChatOps Bridge.

Do not answer with a loose prompt list. Produce a queue-pack object or ZIP-ready
package with:

- `ion_queue_pack.json`
- optional prompt files under `prompts/`
- a short manifest summary
- explicit approval gates in any step that could mutate state
- clear non-claims about authority

Queue packs are carrier prompt material. They are not accepted ION state, not
production proof, not live execution authority, and not a credential store.

