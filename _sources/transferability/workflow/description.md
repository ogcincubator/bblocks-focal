## FOCAL Transferability Workflow

The workflow-level aggregator: profiles a CWL Workflow
([`ogc.cwl.v1_2_1.CWLWorkflow`](bblocks://ogc.cwl.v1_2_1.CWLWorkflow)) with FOCAL's transferability
model, tying together every other `transferability/*` block onto one workflow instance.

| Property | Cardinality | Source block |
|---|---|---|
| `envelope` | required, repeatable | [`envelopeConstraint`](bblocks://ogc.focal.transferability.envelopeConstraint) |
| `referenceArtifact` | required, repeatable (own wrapper, see below) | wraps [`rule`](bblocks://ogc.focal.transferability.rule) |
| `computationType` | optional | [`computationType`](bblocks://ogc.focal.transferability.computationType) |
| `maturityStatus` | required | [`maturityStatus`](bblocks://ogc.focal.transferability.maturityStatus) |
| `temporalExtent` | optional, repeatable | [`temporalExtent`](bblocks://ogc.focal.transferability.temporalExtent) |
| `qualityAnnotation` | optional, repeatable | [`qualityAnnotation`](bblocks://ogc.focal.transferability.qualityAnnotation) |

**`referenceArtifact` wrapper.** Each entry is `{artifact, rules}`: `artifact` is a free-text label
identifying the reference/calibration artifact (e.g. "Rasdaman climate registry / catalogue"),
`rules` is one or more [`rule`](bblocks://ogc.focal.transferability.rule) statements governing it.
`artifact` is deliberately a free-text label, not a `$ref` to a `steps`/`inputs` entry of the
profiled `CWLWorkflow` — the source questionnaires name artifacts this way, and a real CWL id to
bind against doesn't exist yet for most of these workflows. Revisit once Application Packages exist.

**Decision (2026-09-02, per `20260902-condition-action-expressivity.md`):** kept the simpler flat
`{artifact, rules}` shape rather than a decision-table structure, even though at least one artifact
(UP-WF2's LST/CLMS/Eurostat datasets) has a richer three-way condition than a flat rule list
expresses cleanly. See [`transferability/rule`](bblocks://ogc.focal.transferability.rule)'s own
"known simplification" note — the same simplification applies here, one level up.

**Status: draft/WIP**, four worked examples (FP-WF1, FP-WF2, FP-WF3, UP-WF2) — chosen to cover the
model's main branch points: multiple simultaneous envelope roles, OR-set actions, an
optional/degrading rule (`required: false`), the `component-not-executable` terminal outcome, and
a directly evidenced `temporalExtent`. The remaining 4 pilot workflows (FP-WF4, FP-WF5, UP-WF1,
UP-WF3) aren't yet worked as examples — UP-WF1 in particular can't be, without fabricating values:
its source states no assignable `envelope` or `referenceArtifact` fact at all (see the
mapping-extraction doc's UP-WF1 section), so it fails this schema's `required` properties outright
until its owner is consulted. Not yet circulated to WF owners generally — that circulation will
happen through this repo (PR review on `bblocks-focal`, not a separate document).
