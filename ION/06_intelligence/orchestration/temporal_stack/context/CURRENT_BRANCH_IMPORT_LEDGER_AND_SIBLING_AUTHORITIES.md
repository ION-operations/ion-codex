# Current Branch Import Ledger and Sibling Authorities

I’ve now reduced it to a real import ledger rather than just a lineage story.

The strongest conclusion is this:

**the current branch is a preserved-and-expanded trunk, not a full reincorporation of every older center.**
It inherited one compact executable line directly, then layered large amounts of recovery law, runtime-law scaffolding, and test proof around it. It did **not** fully absorb the older runtime/session center, the older activation/orchestrator center, or the older Aether meta-template center. Those still survive as sibling authorities.

## What was directly carried forward

The direct trunk is still the old extracted `ION` family, especially `ION (codex branch)`.

In the kernel, the old codex branch had 22 Python modules under `04_packages/kernel`. All 22 survive in the current kernel. They are the true preserved core:

`children`, `commit`, `context_compiler`, `daemon`, `daemon_actions`, `daemon_loop`, `dispatch`, `execution`, `graph`, `index`, `model`, `questions`, `receipts`, `reviews`, `scheduler`, `sequential_kernel`, `signal_followups`, `signals`, `store`, `validation`, plus `__init__` and `__main__`.

That matters because it tells us the original executable heart of the current branch is not speculative. It is a real carry-forward.

The same pattern holds in architecture and tests. The old codex branch had 10 architecture protocols; all 10 survive. It had 20 kernel tests; all 20 survive. So the current branch did not replace its precursor center. It **kept it intact** and built on top of it.

This is the first ledger entry:

**Imported intact:** the compact extracted ION kernel line.

## What the current branch added on top of that trunk

This is where the project became much more explicit and much heavier.

The current kernel has 89 Python modules, which means **67 kernel modules are branch-era additions beyond the preserved codex core**. Those additions cluster very clearly.

One cluster is **bootstrap and operator control**:
`bootstrap_activation`, `bootstrap_bridge`, `bootstrap_init`, `operator_cli`, `operator_control`, `operational_hardening`.

One cluster is **continuation / takeover / replay / equivalence**:
`continuation`, `takeover`, `recovery_replay`, `equivalence`, `packet_validation`.

One cluster is **branch / horizon / schedule governance**:
`branch_controls`, `branch_horizon_sync`, `branch_rescheduling`, `horizon_state`, `schedule_*`, `settlement`.

One cluster is **external-carrier symmetry**:
`external_execution_bridge`, `child_work_service`, `executor_registry`, `allocator`.

And a very large cluster is **runtime reporting and provenance surfaces**:
the many `runtime_report_*` modules and `runtime_reporting`.

So the current branch’s main addition is not “new app features.” It is a huge layer of **lawful execution scaffolding, cross-carrier symmetry, reporting, and recovery instrumentation** wrapped around the preserved trunk.

That gives the second ledger entry:

**Added in current branch:** explicit orchestration law, branch/horizon mechanics, packet/replay/takeover machinery, operator surfaces, and a large runtime-report/provenance layer.

## What was imported only conceptually, not structurally

This is where the earlier confusion came from.

When I compare the current branch to older roots like `ION-BUILD`, `operation-victus`, `Project-Gemini`, `SOS-OPUS`, and `IONv2`, there is **very little direct path-preserved code carryover** into the current filesystem. In other words, those roots were not merged in as intact subtrees.

Instead, the current branch’s own recovery atlas says they were absorbed at the level of **capability claims and authority inheritance**, not filesystem preservation.

That means the import ledger needs two columns:

* what is physically carried into the current branch
* what remains a preserved sibling authority that the current branch still consults

The current branch is already making that distinction itself.

## The real sibling authorities that were not truly imported

The current atlas is explicit here, and the artifact comparison agrees.

### ION-BUILD

This was **not** physically reincorporated as a live subtree. But it remains the first authority for:

* runtime/API/session execution
* queues and session mutation
* API runtime entry
* scheduler tick/session evidence
* Aether constitution/kernel/atlas preservation
* template-development center

So the import ledger says:

**Not imported as structure. Still required as authority.**

The current branch knows it lacks the full runtime/API/session organism and says so.

### operation-victus

This was also **not** structurally imported into the current branch. But it remains the strongest executable center for:

* activation authority
* manager logic
* orchestrator logic
* fleet-state operations
* explicit spawn/suspend/terminate/monitor behavior
* swarm execution harnesses

So again:

**Not imported as structure. Still required as authority.**

The current branch is stronger in packet law and startup law. Victus is still stronger in executable activation center.

### Project-Gemini

This is best read as the rehomed continuation witness of the Victus line. It preserves a great deal of that orchestrator/swarm center in a more compact package.

So:

**Not imported as structure. Preserved as continuation witness of Core C.**

### old Aether / template-development center

This survives materially through `ION-BUILD` and related historical doctrine/template surfaces. The current branch has template-surface repair, but the older center still outranks it in:

* meta-template constitutional strength
* template development as permanent activity
* atlas/kernel compression ideal
* smallest-law precedence

So:

**Not imported whole. Still the senior source for meta-template and values-compression questions.**

### SOS-OPUS and broader SOS family

These are not direct structural ancestors of the current kernel trunk. But they remain important doctrine/context/template sibling lines. The current recovery program treats them as major supporting evidence, especially for sovereign doctrine, context protocol, template-development recurrence, and earlier recovery memory.

So:

**Contributed doctrine pressure and witness surfaces, not live trunk structure.**

### IONv2

This one is subtle. It also was not imported as a preserved subtree, but it remains a serious compact executable witness for:

* capsule manager patterns
* store/context/compiler discipline
* compact governance implementation memory
* compression that the current branch may have lost

So:

**Not structurally imported. Still a living comparison partner for compactness and implementation burden.**

## The current branch’s own gating logic confirms this reading

One reason I’m confident here is that the current repo already encodes which center should answer which kind of question.

Its own question-class defaults say, in effect:

* startup/current-branch truth → current extracted ION branch
* runtime/API/session → ION-BUILD
* activation/manager/swarm → operation-victus, with Project-Gemini as continuation witness
* template/meta-template evolution → historical ION-BUILD/Aether template center
* compactness/compression questions → production precursor pair plus IONv2
* archaeology/prior atlas → 00_CONSOLIDATED_ATLAS and supporting archaeology centers
* genuinely new extension → only after proving non-reinvention

That means the current branch has already stopped pretending it is the sole center of the whole organism.

That is a major milestone in the consolidation.

## What the pass52–pass55 snapshots reveal

The neighboring pass snapshots sharpen the picture further.

All four snapshots are packaged as **ION-only exports**. None of them include root-level `pyproject.toml`, `ATLAS`, or `00_CONSOLIDATED_ATLAS`. The standalone `pyproject.toml` you uploaded is exactly the missing packaging file the branch expected, and it restores the packaging posture the tests were asserting. It defines `ion-kernel`, points package discovery at `ION/04_packages`, and sets pytest to use `ION/tests` and `ION/04_packages`.

The pass chain itself is also revealing.

`pass53` is not simply “pass52 plus more.” It is a narrower runtime-review entry pack that drops a large number of earlier pass52 recovery artifacts and adds a focused quarantined runtime review set.

Then `pass54` adds a runtime seam-pressure layer.

Then `pass55` adds worked examples on top of that.

So the pass family is best read as:

* `pass52`: broader branch-charter / recovery packing state
* `pass53`: narrowed runtime review entry
* `pass54`: seam-pressure refinement
* `pass55`: worked-example refinement

That means the current pass chain was converging on **lane C runtime/session clarification**, not broadly restating the whole organism each pass.

## The clean import ledger

Here is the usable ledger in plain terms.

**Imported intact into current branch**

* extracted ION / codex-branch compact kernel trunk
* its precursor architecture floor
* its precursor kernel tests

**Expanded heavily inside current branch**

* packet/handoff standardization
* replay/takeover/continuation law
* branch/horizon/schedule law
* operator and daemon control surfaces
* external execution bridge
* runtime reporting/provenance/navigation surfaces
* corpus-recovery atlas and question-class gating

**Absorbed conceptually but not structurally**

* SOS-OPUS doctrine/context/consolidation witness
* IONv2 compact implementation memory
* ION-BUILD runtime/API/session and Aether constitutional pressure
* Victus/Gemini activation/orchestrator/swarm pressure
* ProjectOpus archaeology/anti-contagion method

**Still preserved outside the current branch because not actually imported**

* full runtime/API/session organism → ION-BUILD
* executable activation authority center → operation-victus
* rehomed swarm/orchestrator continuation → Project-Gemini
* strongest meta-template constitutional center → old Aether / ION-BUILD line
* strongest archaeology/prior-atlas center → 00_CONSOLIDATED_ATLAS / ProjectOpus / ATLAS
* strongest compact implementation comparison partner → IONv2 and production precursor pair

## The deepest unresolved truth

So the consolidation is more precise than “many repos became one repo.”

What actually happened is:

**one compact executable ION trunk became the active branch, and the branch then built a recovery atlas sophisticated enough to admit that several older sibling centers still outrank it in their own domain.**

That is the true shape.

The unfinished work is no longer repo-merging. It is **truthful reintegration without flattening distributed authority**.

## My present judgment of the organism

The current branch is the lawful operational center.

But it is still only **Core A plus recovery intelligence about B, C, and D**.

It is not yet the total recovered organism.

That is why the most important remaining work is not “build more stuff” in the abstract. It is:

* recover the runtime/session center from ION-BUILD without losing current startup law
* recover activation authority from Victus/Gemini without regressing into older drift
* reconcile current template-bridge law with the older Aether template-development center
* preserve compactness lessons from precursor ION and IONv2 while keeping current explicit governance gains

That is the real reintegration frontier.

The next move I’d take is a **target-by-target reincorporation ledger**: for each missing center, name the exact current files that already gesture toward it, the exact historical files that still outrank them, and the smallest lawful merge target rather than a vague “bring it back.”
