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

**Why `transferability` is its own nested object, not flattened here.** `envelope` and
`artifactRules` — the actual portability boundary — live in
[`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement), a
standalone bundle this block attaches under one `transferability` property, rather than merging
those properties directly onto the CWL Workflow profile. `computationType`, `maturityStatus`, and
`qualityAnnotation` describe the workflow's implementation and result quality generally, not its
portability boundary, so they stay outside that bundle and attach here directly instead.

**Status: draft/WIP**, four worked examples (FP-WF1, FP-WF2, FP-WF3, UP-WF2) — chosen to cover the
model's main branch points: multiple simultaneous envelope roles, OR-set actions, an
optional/degrading rule (`required: false`), the `component-not-executable` terminal outcome, and
a directly evidenced temporal envelope entry. The remaining 4 pilot workflows (FP-WF4, FP-WF5,
UP-WF1, UP-WF3) aren't yet worked as examples — UP-WF1 in particular can't be, without fabricating
values: its source states no assignable `envelope` or `artifactRules` fact at all (see the
mapping-extraction doc's UP-WF1 section), so it fails this schema's `required` properties outright
until its owner is consulted. Not yet circulated to WF owners generally — that circulation will
happen through this repo (PR review on `bblocks-focal`, not a separate document).
