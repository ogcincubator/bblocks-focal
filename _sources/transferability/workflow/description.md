## FOCAL Transferability Workflow

The workflow-level aggregator: profiles a CWL Workflow
([`ogc.cwl.v1_2_1.CWLWorkflow`](bblocks://ogc.cwl.v1_2_1.CWLWorkflow)) with FOCAL's transferability
model.

| Property | Cardinality | Source block |
|---|---|---|
| `transferability` | required (single object) | [`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement) |
| `computationType` | optional | [`computationType`](bblocks://ogc.focal.transferability.computationType) |
| `maturityStatus` | required | [`maturityStatus`](bblocks://ogc.focal.transferability.maturityStatus) |
| `qualityAnnotation` | optional, repeatable | [`qualityAnnotation`](bblocks://ogc.focal.transferability.qualityAnnotation) |

**Why `transferability` is its own nested object, not flattened here.** `envelope`, `artifacts`
and `rules` — the actual portability boundary — live in
[`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement), a
standalone bundle this block attaches under one `transferability` property, rather than merging
those properties directly onto the CWL Workflow profile. `computationType`, `maturityStatus`, and
`qualityAnnotation` describe the workflow's implementation and result quality generally, not its
portability boundary, so they stay outside that bundle and attach here directly instead.

**Status: draft/WIP**, seven worked examples covering seven of FOCAL's eight pilot workflows
(FP-WF1, FP-WF2, FP-WF3, FP-WF5, UP-WF1, UP-WF2, UP-WF3). Between them they exercise every branch
point in the model: multiple simultaneous envelope roles, OR-set actions, an optional/degrading
rule (`mandatory: false`), the `component-not-executable` terminal outcome with `affects`, one rule
shared across four artifacts, a two-rule cascade over a single constraint, an evidenced temporal
envelope entry, the `grid-structure` dimension, an artifact-level `acceptanceCriteria` contract,
and an entirely empty envelope stated as a claim.

**The eighth, FP-WF4, is deliberately not here.** It is not a CWL Workflow at all but a SensLog
observing system, so it cannot profile `ogc.cwl.v1_2_1.CWLWorkflow` — which is precisely why
`transferabilityStatement` was factored out of this block and carries no CWL assumption. Attaching
it needs a sibling block for observing systems, and an action term for re-deploying physical
infrastructure. See the FOCAL WP10 model-extension note for both.

Not yet circulated to WF owners generally — that circulation will happen through this repo (PR
review on `bblocks-focal`, not a separate document).
