## FOCAL Transferability Observing System

A host for a [`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement)
when the thing described is a sensor-data service and not a CWL Workflow. It exists because
[`workflow`](bblocks://ogc.focal.transferability.workflow) profiles `CWLWorkflow` and so cannot
describe FP-WF4, a SensLog / SensLog-OTS3 observation store.

| Property | Cardinality | Source block |
|---|---|---|
| `transferability` | required (single object) | [`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement) |
| `id`, `label` | optional | this block (`label` uplifts to `rdfs:label`) |

**What it leaves out, and why.**

- `computationType`: how an executable package computes its results. A service that stores and
  serves observations has none, so the schema rejects the property instead of accepting a
  "not applicable" value.
- `maturityStatus`: no source states one for this subject. Unlike on a workflow, nothing here
  requires it. Add it as an optional property when an owner states a maturity.
- `qualityAnnotation`: no caveat about results beyond "depends on its inputs", which the model does
  not record as a caveat.

**No new vocabulary was needed.** The one thing FP-WF4's owner says must change elsewhere, "the
sensor network, station metadata, observed properties, calibration rules and target climate
datasets", is "replaced by local equivalents": the existing `replace-with-local-equivalent` action.
The sensor network is an `infrastructure` artifact.

**Status: draft/WIP.** One worked example (FP-WF4), built only from the owner's questionnaire. Its
envelope is empty because the source states no extent, which is not a claim that the results hold
everywhere; `noConstraintsStated` is not set. Three negative tests cover the shapes: a
`computationType` on an observing system, an empty label, and `trainingRequired: false` beside a
`trained-on` envelope entry (a check inherited from the statement block, shown to work on this host).
