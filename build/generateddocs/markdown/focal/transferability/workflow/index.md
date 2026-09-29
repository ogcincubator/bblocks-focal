
# FOCAL Transferability Workflow (Schema)

`ogc.focal.transferability.workflow` *v0.12*

Profile of a CWL Workflow adding FOCAL's machine-readable transferability facts: a transferability statement (validity envelope, reference/calibration-artifact adaptation rules), computation type, maturity status, and quality annotations.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

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

**Status: draft/WIP**, seven worked examples covering seven of FOCAL's eight pilot workflows (the eighth is in `observingSystem`)
(FP-WF1, FP-WF2, FP-WF3, FP-WF5, UP-WF1, UP-WF2, UP-WF3). Between them they exercise every branch
point in the model: multiple simultaneous envelope roles, OR-set actions, an optional/degrading
rule (`mandatory: false`), the `component-not-executable` terminal outcome with `affects`, one rule
shared across four artifacts, a two-rule cascade over a single constraint, an evidenced temporal
envelope entry, the `grid-structure` dimension, an artifact-level `acceptanceCriteria` contract,
an entirely empty envelope stated as a claim (`noConstraintsStated`), a positive statement that
no training or calibration data is needed (`trainingRequired: false`), and caveats about results
that are neither maturity nor a boundary (`qualityAnnotation`).

**The eighth, FP-WF4, is not a CWL Workflow at all** but a SensLog observation store, so it cannot
profile `ogc.cwl.v1_2_1.CWLWorkflow`. It is modeled with the sibling block
[`observingSystem`](bblocks://ogc.focal.transferability.observingSystem), which carries the same
`transferabilityStatement` and deliberately no `computationType` and no `maturityStatus`.

Circulated to the pilot workflow owners for review in September 2026; nothing here is locked.

## Examples

### FP-WF1 — Tree species suitability
The richest of the eight FOCAL pilot workflows for this model: three simultaneous envelope
roles, an OR-set of actions on one artifact, and an evidenced quality caveat. Drawn from the owner's questionnaire answers.

**What the rules now say that they could not before.** The trained model must be retrained or
replaced when the target falls outside `ecological-range`; the climate data must be swapped when
the target is outside `downscaled-climate-available`, the coverage of that data. Two artifacts, two different boundaries, each rule
naming its own — previously both said only "different geographic coverage" and nothing
recorded which extent that referred to.

**`ecological-range` is prose, not a classification match.** An earlier version tested it
against the EEA biogeographical regions; the owner's 2026-09-29 review rejected that reading —
the questionnaire's "comparable ecological range" is a general environmental/site-conditions
claim, not a match against any one existing scheme, so it is recorded as a judgement a person
makes, the same shape as `downscaled-climate-available`.

**`czech-plots` is an approximation and says so in the data.** The source says "Czech
long-term permanent sample plots", a scattered set of monitoring locations; the value here is
Czechia's country border (simplified), an honest upper bound. That caveat is a
`transferabilityNotes` on the constraint (uplifting to `rdfs:comment`), not a remark in this
prose, so a consumer weighing the envelope can see it.

      **The climate rule is tested against `downscaled-climate-available`, not against `czech-plots`.**
`czech-plots` is where the growth model was calibrated; where FOCAL's downscaled climate data
extends is a different fact, and the questionnaire does not say. The constraint is a sentence
for now, so a consumer reports the climate rule as unknown until the owner gives the coverage,
instead of answering from the plot extent.

No temporal constraint: the source states a user-selected "prediction period"  with no bound
or granularity, and none is invented. `steps` is omitted — no Application Package exists yet.
The `inputs`/`outputs` ids are **placeholders** invented so `artifactRef` has something to
point at; they are not FP-WF1's real interface.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF1 — Tree species suitability",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        { "package": "python" },
        { "package": "lightgbm" },
        { "package": "flask" },
        { "package": "gunicorn" }
      ]
    }
  },
  "inputs": { "climate_data": { "type": "File" }, "trained_growth_model": { "type": "File" } },
  "outputs": { "growth_projection": { "type": "File" } },
  "transferability": {
    "trainingRequired": true,
    "envelope": [
      {
        "id": "czech-plots",
        "role": "trained-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))" },
        "transferabilityNotes": "Czechia's country border, simplified to a few tens of kilometers, standing in for the actual Czech long-term permanent sample plot network — a scattered set of monitoring locations, not a country. An honest upper bound pending the real plot coordinates from the workflow owner."
      },
      {
        "id": "ecological-range",
        "role": "valid-for",
        "dimension": "ecological",
        "value": "environmental and site conditions comparable to those represented in the Czech training data (`czech-plots`) — an ecological/environmental comparability judgement, not a match against a single named classification scheme",
        "transferabilityNotes": "Question 7: results are 'valid mainly within a comparable ecological range'. Earlier recorded as a same-class-as test against the EEA biogeographical regions; the owner's 2026-09-29 review rejected that reading and asked that it not be defined through a single existing classification scheme. Recorded as prose instead, mirroring `downscaled-climate-available`. The owner notes that in the future the model's applicability could be assessed more explicitly against the environmental range represented in the training data, which would need a purpose-built measure, not an off-the-shelf scheme — still open, no such measure exists yet."
      },
      {
        "id": "downscaled-climate-available",
        "role": "can-run-on",
        "dimension": "climatic",
        "value": "wherever downscaled climate data is available"
      }
    ],
    "artifacts": [
      {
        "id": "growth-model",
        "artifact": "trained tree growth model (LightGBM, Czech permanent sample plot data)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/trained_growth_model"
      },
      {
        "id": "climate-data",
        "artifact": "downscaled FOCAL climate data (current + future)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/climate_data"
      }
    ],
    "rules": [
      {
        "appliesTo": ["growth-model"],
        "when": [{ "constraint": "ecological-range", "test": "outside" }],
        "actions": ["retrain", "replace-with-alternative-published-model"],
        "mandatory": true,
        "transferabilityNotes": "Owner's 2026-09-29 review, item 4: the workflow concept is transferable, while the Czech-trained growth model is a replaceable component outside its applicable environmental range. Two adaptation pathways: retrain/calibrate on suitable target-region data, or replace with another published or locally developed growth model. No rule of thumb for choosing between them is recorded yet (still open, FP-WF1.8)."
      },
      {
        "appliesTo": ["climate-data"],
        "when": [{ "constraint": "downscaled-climate-available", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
      }
    ]
  },
  "computationType": "statistical-ml",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "The AI model and validation are still being finalised, so results should be interpreted as decision-support information rather than exact forecasts."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF1 \u2014 Tree species suitability",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "lightgbm"
        },
        {
          "package": "flask"
        },
        {
          "package": "gunicorn"
        }
      ]
    }
  },
  "inputs": {
    "climate_data": {
      "type": "File"
    },
    "trained_growth_model": {
      "type": "File"
    }
  },
  "outputs": {
    "growth_projection": {
      "type": "File"
    }
  },
  "transferability": {
    "trainingRequired": true,
    "envelope": [
      {
        "id": "czech-plots",
        "role": "trained-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"
        },
        "transferabilityNotes": "Czechia's country border, simplified to a few tens of kilometers, standing in for the actual Czech long-term permanent sample plot network \u2014 a scattered set of monitoring locations, not a country. An honest upper bound pending the real plot coordinates from the workflow owner."
      },
      {
        "id": "ecological-range",
        "role": "valid-for",
        "dimension": "ecological",
        "value": "environmental and site conditions comparable to those represented in the Czech training data (`czech-plots`) \u2014 an ecological/environmental comparability judgement, not a match against a single named classification scheme",
        "transferabilityNotes": "Question 7: results are 'valid mainly within a comparable ecological range'. Earlier recorded as a same-class-as test against the EEA biogeographical regions; the owner's 2026-09-29 review rejected that reading and asked that it not be defined through a single existing classification scheme. Recorded as prose instead, mirroring `downscaled-climate-available`. The owner notes that in the future the model's applicability could be assessed more explicitly against the environmental range represented in the training data, which would need a purpose-built measure, not an off-the-shelf scheme \u2014 still open, no such measure exists yet."
      },
      {
        "id": "downscaled-climate-available",
        "role": "can-run-on",
        "dimension": "climatic",
        "value": "wherever downscaled climate data is available"
      }
    ],
    "artifacts": [
      {
        "id": "growth-model",
        "artifact": "trained tree growth model (LightGBM, Czech permanent sample plot data)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/trained_growth_model"
      },
      {
        "id": "climate-data",
        "artifact": "downscaled FOCAL climate data (current + future)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/climate_data"
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "growth-model"
        ],
        "when": [
          {
            "constraint": "ecological-range",
            "test": "outside"
          }
        ],
        "actions": [
          "retrain",
          "replace-with-alternative-published-model"
        ],
        "mandatory": true,
        "transferabilityNotes": "Owner's 2026-09-29 review, item 4: the workflow concept is transferable, while the Czech-trained growth model is a replaceable component outside its applicable environmental range. Two adaptation pathways: retrain/calibrate on suitable target-region data, or replace with another published or locally developed growth model. No rule of thumb for choosing between them is recorded yet (still open, FP-WF1.8)."
      },
      {
        "appliesTo": [
          "climate-data"
        ],
        "when": [
          {
            "constraint": "downscaled-climate-available",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true
      }
    ]
  },
  "computationType": "statistical-ml",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "The AI model and validation are still being finalised, so results should be interpreted as decision-support information rather than exact forecasts."
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/> a cwl:Workflow ;
    rdfs:label "FP-WF1 — Tree species suitability" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate_data>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/trained_growth_model> ;
    cwl:outputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth_projection> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns1:package "lightgbm" ],
                [ ns1:package "flask" ],
                [ ns1:package "gunicorn" ],
                [ ns1:package "python" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/pre-operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/decision-support-only> ;
            focal-transf-prop:note "The AI model and validation are still being finalised, so results should be interpreted as decision-support information rather than exact forecasts." ] ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate-data>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-plots>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/downscaled-climate-available>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/ecological-range> ;
            focal-transf-prop:rules [ rdfs:comment "Owner's 2026-09-29 review, item 4: the workflow concept is transferable, while the Czech-trained growth model is a replaceable component outside its applicable environmental range. Two adaptation pathways: retrain/calibrate on suitable target-region data, or replace with another published or locally developed growth model. No rule of thumb for choosing between them is recorded yet (still open, FP-WF1.8)." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-alternative-published-model>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/ecological-range> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate-data> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/downscaled-climate-available> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ;
            focal-transf-prop:trainingRequired true ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate_data> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-plots> rdfs:comment "Czechia's country border, simplified to a few tens of kilometers, standing in for the actual Czech long-term permanent sample plot network — a scattered set of monitoring locations, not a country. An honest upper bound pending the real plot coordinates from the workflow owner." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth_projection> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/trained_growth_model> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate-data> dcterms:title "downscaled FOCAL climate data (current + future)" ;
    focal-transf-prop:artifactRef "/inputs/climate_data" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/downscaled-climate-available> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value "wherever downscaled climate data is available" .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/ecological-range> rdfs:comment "Question 7: results are 'valid mainly within a comparable ecological range'. Earlier recorded as a same-class-as test against the EEA biogeographical regions; the owner's 2026-09-29 review rejected that reading and asked that it not be defined through a single existing classification scheme. Recorded as prose instead, mirroring `downscaled-climate-available`. The owner notes that in the future the model's applicability could be assessed more explicitly against the environmental range represented in the training data, which would need a purpose-built measure, not an off-the-shelf scheme — still open, no such measure exists yet." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "environmental and site conditions comparable to those represented in the Czech training data (`czech-plots`) — an ecological/environmental comparability judgement, not a match against a single named classification scheme" .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model> dcterms:title "trained tree growth model (LightGBM, Czech permanent sample plot data)" ;
    focal-transf-prop:artifactRef "/inputs/trained_growth_model" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


```


### FP-WF2 — Heat stress (four artifacts, two boundaries)
A deterministic/rule-based workflow whose reference data — species tolerance thresholds,
SLT/T5 forest classification and species codes — the owner calls Czechia-specific (Questions
5, 7 and 10), and whose Rasdaman climate registry the owner calls project-specific (Question
10) and says must point to the target region's datasets (Question 9).

**This is the case that motivated declaring artifacts separately from rules.** The three
Czechia-specific artifacts shared one boundary in an earlier version. The owner's 2026-09-29
review distinguished them: SLT and species-code resources are spatial/reference inputs that
genuinely need a local or regional equivalent outside their coverage (`mandatory: true`), but
the species-tolerance thresholds are default/reference values a user can already override
directly, regardless of location, so they are split into their own `mandatory: false` rule
over the same `czechia` constraint rather than sharing the SLT/species-codes rule. The
registry has its own rule and its own extent, the coverage of the current collections,
because nothing in the questionnaire says that is Czechia.

Both envelope entries are **inferred, not stated**: the questionnaire never gives an extent
for either. Czechia's country border stands in for both, and each says so on the constraint
itself and needs owner confirmation.

No temporal constraint (the source states a "time period" input with no bound). `steps`
omitted, no Application Package yet. `inputs` ids are placeholders.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF2 — Heat stress",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        { "package": "python" },
        { "package": "flask" },
        { "package": "gunicorn" }
      ]
    },
    "NetworkAccess": { "networkAccess": true }
  },
  "inputs": {
    "species_tolerances": { "type": "File" },
    "forest_classification_context": { "type": "File" },
    "species_codes": { "type": "File" },
    "climate_registry_endpoint": { "type": "string" }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "czechia",
        "role": "derived-from",
        "dimension": "jurisdictional",
        "value": { "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))" },
        "transferabilityNotes": "Inferred, not stated: the questionnaire gives no envelope fact directly, only that three separate reference artifacts are called Czechia-specific. Value is Czechia's country border, simplified, standing in for those artifacts' unstated extent. The owner's 2026-09-29 review confirms this reading: `czechia` names the coverage of the current SLT/species/threshold input resources, not a validity limit of the WF2 methodology itself, which is intended to be transferable wherever the relevant local inputs are available or adapted. Real coverage of these resources still needs owner/technical confirmation."
      },
      {
        "id": "rasdaman-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))" },
        "transferabilityNotes": "Where the current Rasdaman climate collections hold data. The questionnaire calls them project-specific (Question 10) and gives no extent. Czechia's country border, simplified, stands in. Needs owner confirmation."
      }
    ],
    "artifacts": [
      { "id": "tolerances", "artifact": "species tolerance thresholds (species_tolerances.json)", "artifactRole": "workflow-input", "artifactRef": "/inputs/species_tolerances" },
      { "id": "slt-t5", "artifact": "SLT/T5 forest classification context (Czechia-specific)", "artifactRole": "workflow-input", "artifactRef": "/inputs/forest_classification_context" },
      { "id": "species-codes", "artifact": "species codes catalogue (species_codes.json)", "artifactRole": "workflow-input", "artifactRef": "/inputs/species_codes" },
      { "id": "rasdaman", "artifact": "Rasdaman climate registry / source catalogue", "artifactRole": "workflow-input", "artifactRef": "/inputs/climate_registry_endpoint" }
    ],
    "rules": [
      {
        "appliesTo": ["slt-t5", "species-codes"],
        "when": [{ "constraint": "czechia", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Owner's 2026-09-29 review: SLT and species-code resources are Czech-specific spatial/reference inputs and need an appropriate local or regional equivalent outside their coverage. This is a property of these particular resources, not of the WF2 methodology, which the owner considers transferable in general."
      },
      {
        "appliesTo": ["tolerances"],
        "when": [{ "constraint": "czechia", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": false,
        "transferabilityNotes": "Question 4: 'Users can also provide custom thresholds', so the tolerance thresholds can be overridden directly, even within the source region. Question 9 adds that 'Thresholds may need adjustment to local species, forest types and management practice'. The owner's 2026-09-29 review confirms this is not a geographic validity constraint: predefined per-species thresholds are default/reference values, and a user can enter target-appropriate values directly without adding a new species-specific parameter set to the workflow — hence `mandatory: false`, split from the SLT/species-codes rule above rather than sharing its `appliesTo`."
      },
      {
        "appliesTo": ["rasdaman"],
        "when": [{ "constraint": "rasdaman-coverage", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'The climate registry and source catalogue would need to point to the target region's climate datasets.' Question 8 accepts 'Rasdaman or equivalent gridded daily climate data'."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational"
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF2 \u2014 Heat stress",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "flask"
        },
        {
          "package": "gunicorn"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "species_tolerances": {
      "type": "File"
    },
    "forest_classification_context": {
      "type": "File"
    },
    "species_codes": {
      "type": "File"
    },
    "climate_registry_endpoint": {
      "type": "string"
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "czechia",
        "role": "derived-from",
        "dimension": "jurisdictional",
        "value": {
          "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"
        },
        "transferabilityNotes": "Inferred, not stated: the questionnaire gives no envelope fact directly, only that three separate reference artifacts are called Czechia-specific. Value is Czechia's country border, simplified, standing in for those artifacts' unstated extent. The owner's 2026-09-29 review confirms this reading: `czechia` names the coverage of the current SLT/species/threshold input resources, not a validity limit of the WF2 methodology itself, which is intended to be transferable wherever the relevant local inputs are available or adapted. Real coverage of these resources still needs owner/technical confirmation."
      },
      {
        "id": "rasdaman-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"
        },
        "transferabilityNotes": "Where the current Rasdaman climate collections hold data. The questionnaire calls them project-specific (Question 10) and gives no extent. Czechia's country border, simplified, stands in. Needs owner confirmation."
      }
    ],
    "artifacts": [
      {
        "id": "tolerances",
        "artifact": "species tolerance thresholds (species_tolerances.json)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/species_tolerances"
      },
      {
        "id": "slt-t5",
        "artifact": "SLT/T5 forest classification context (Czechia-specific)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/forest_classification_context"
      },
      {
        "id": "species-codes",
        "artifact": "species codes catalogue (species_codes.json)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/species_codes"
      },
      {
        "id": "rasdaman",
        "artifact": "Rasdaman climate registry / source catalogue",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/climate_registry_endpoint"
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "slt-t5",
          "species-codes"
        ],
        "when": [
          {
            "constraint": "czechia",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Owner's 2026-09-29 review: SLT and species-code resources are Czech-specific spatial/reference inputs and need an appropriate local or regional equivalent outside their coverage. This is a property of these particular resources, not of the WF2 methodology, which the owner considers transferable in general."
      },
      {
        "appliesTo": [
          "tolerances"
        ],
        "when": [
          {
            "constraint": "czechia",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Question 4: 'Users can also provide custom thresholds', so the tolerance thresholds can be overridden directly, even within the source region. Question 9 adds that 'Thresholds may need adjustment to local species, forest types and management practice'. The owner's 2026-09-29 review confirms this is not a geographic validity constraint: predefined per-species thresholds are default/reference values, and a user can enter target-appropriate values directly without adding a new species-specific parameter set to the workflow \u2014 hence `mandatory: false`, split from the SLT/species-codes rule above rather than sharing its `appliesTo`."
      },
      {
        "appliesTo": [
          "rasdaman"
        ],
        "when": [
          {
            "constraint": "rasdaman-coverage",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'The climate registry and source catalogue would need to point to the target region's climate datasets.' Question 8 accepts 'Rasdaman or equivalent gridded daily climate data'."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational"
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns3: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/> a cwl:Workflow ;
    rdfs:label "FP-WF2 — Heat stress" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/climate_registry_endpoint>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/forest_classification_context>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_codes>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_tolerances> ;
    cwl:requirements [ a cwl:NetworkAccess ;
            ns3:networkAccess true ],
        [ a cwl:SoftwareRequirement ;
            ns1:packages [ ns2:package "python" ],
                [ ns2:package "flask" ],
                [ ns2:package "gunicorn" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt-t5>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-codes>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/tolerances> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czechia>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman-coverage> ;
            focal-transf-prop:rules [ rdfs:comment "Owner's 2026-09-29 review: SLT and species-code resources are Czech-specific spatial/reference inputs and need an appropriate local or regional equivalent outside their coverage. This is a property of these particular resources, not of the WF2 methodology, which the owner considers transferable in general." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt-t5>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-codes> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czechia> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 9: 'The climate registry and source catalogue would need to point to the target region's climate datasets.' Question 8 accepts 'Rasdaman or equivalent gridded daily climate data'." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman-coverage> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 4: 'Users can also provide custom thresholds', so the tolerance thresholds can be overridden directly, even within the source region. Question 9 adds that 'Thresholds may need adjustment to local species, forest types and management practice'. The owner's 2026-09-29 review confirms this is not a geographic validity constraint: predefined per-species thresholds are default/reference values, and a user can enter target-appropriate values directly without adding a new species-specific parameter set to the workflow — hence `mandatory: false`, split from the SLT/species-codes rule above rather than sharing its `appliesTo`." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/tolerances> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czechia> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/climate_registry_endpoint> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/forest_classification_context> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_codes> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_tolerances> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman> dcterms:title "Rasdaman climate registry / source catalogue" ;
    focal-transf-prop:artifactRef "/inputs/climate_registry_endpoint" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman-coverage> rdfs:comment "Where the current Rasdaman climate collections hold data. The questionnaire calls them project-specific (Question 10) and gives no extent. Czechia's country border, simplified, stands in. Needs owner confirmation." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt-t5> dcterms:title "SLT/T5 forest classification context (Czechia-specific)" ;
    focal-transf-prop:artifactRef "/inputs/forest_classification_context" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-codes> dcterms:title "species codes catalogue (species_codes.json)" ;
    focal-transf-prop:artifactRef "/inputs/species_codes" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/tolerances> dcterms:title "species tolerance thresholds (species_tolerances.json)" ;
    focal-transf-prop:artifactRef "/inputs/species_tolerances" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czechia> rdfs:comment "Inferred, not stated: the questionnaire gives no envelope fact directly, only that three separate reference artifacts are called Czechia-specific. Value is Czechia's country border, simplified, standing in for those artifacts' unstated extent. The owner's 2026-09-29 review confirms this reading: `czechia` names the coverage of the current SLT/species/threshold input resources, not a validity limit of the WF2 methodology itself, which is intended to be transferable wherever the relevant local inputs are available or adapted. Real coverage of these resources still needs owner/technical confirmation." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/jurisdictional> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"^^geo:wktLiteral ] .


```


### FP-WF3 — Prediction of threatened stands (optional rule, degraded mode)
The sharpest evidenced example of a non-operational workflow (`maturityStatus: prototype`),
and the clearest optional-but-degrading rule: without local training labels, results are
still produced, just "treated as exploratory" (Question 7). Question 9 lists the labels
among the things that "would need to be replaced", so the optional flag on the labels combines
the two answers rather than being stated in one sentence. The EO strategy is optional
because Question 9 says it "may also need adjustment", and Question 3 says the Python
requirement is only "expected", so it is provisional. That is
`mandatory: false` with the consequence spelled out — a skippable rule with no stated
consequence tells a consumer nothing they can act on, so `shapes.shacl` rejects that pairing.

The spatial constraint is **more speculative than FP-WF1's or FP-WF2's**: no sentence in this
questionnaire names a location at all. Czechia is a proxy because this is a Forest Pilot
workflow. Recorded as such on the constraint.

Question 9 lists four things to replace for the target region: "Historical disturbance labels,
forest masks, phenological normalisation and model training data". Labels, phenology and the
EO strategy are artifacts here, and forest masks now are too. "Model training data" is read as
the labels themselves (Question 4 describes the labels as the polygons "for training or
validation"), which is recorded on the labels artifact and needs owner confirmation.

Question 5 also says "structured regression testing and full scientific validation are not yet
complete", which is what `validation-incomplete` exists for, so it is carried as a
`qualityAnnotation`, separate from `maturityStatus: prototype`.

No temporal constraint. `steps` omitted — this workflow's own questionnaire says its
container, API and regression-test packaging are still to be completed, so there is less of
an Application Package here than anywhere else. `inputs` ids are placeholders.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF3 — Prediction of threatened stands",
  "requirements": {
    "SoftwareRequirement": { "packages": [{ "package": "python" }] }
  },
  "inputs": {
    "disturbance_labels": { "type": "File" },
    "forest_masks": { "type": "File" },
    "eo_compositing_strategy": { "type": "string" },
    "phenology_normalization_assumptions": { "type": "string" }
  },
  "transferability": {
    "trainingRequired": true,
    "envelope": [
      {
        "id": "label-extent",
        "role": "trained-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))" },
        "transferabilityNotes": "More speculative than FP-WF1's or FP-WF2's: no sentence in this questionnaire names a location for the historical disturbance labels. Czechia is used as a proxy because this is a Forest Pilot workflow, and Czechia's country border (simplified) as the value, standing in for an extent the owner did not state. Needs owner confirmation before being treated as fact."
      },
      {
        "id": "phenological-regime",
        "role": "valid-for",
        "dimension": "ecological",
        "value": "a comparable phenological regime"
      }
    ],
    "artifacts": [
      { "id": "labels", "artifact": "historical forest disturbance/damage labels (ground truth training data)", "artifactRole": "workflow-input", "artifactRef": "/inputs/disturbance_labels",
        "transferabilityNotes": "Question 9 also lists \"model training data\" among the things to replace. Read here as the same thing as these labels, because Question 4 describes the labels as the polygons \"for training or validation\". Needs owner confirmation." },
      { "id": "forest-masks", "artifact": "forest masks or stand boundaries", "artifactRole": "workflow-input", "artifactRef": "/inputs/forest_masks" },
      { "id": "eo-strategy", "artifact": "EO sensor selection, cloud masking, temporal compositing strategy", "artifactRole": "workflow-input", "artifactRef": "/inputs/eo_compositing_strategy" },
      { "id": "phenology", "artifact": "regional phenology normalisation assumptions", "artifactRole": "workflow-input", "artifactRef": "/inputs/phenology_normalization_assumptions" }
    ],
    "rules": [
      {
        "appliesTo": ["labels"],
        "when": [{ "constraint": "label-extent", "test": "outside" }],
        "actions": ["retrain"],
        "mandatory": false,
        "transferabilityNotes": "Without local training labels, results should be treated as exploratory rather than blocked outright — a degraded-mode caveat, not a hard requirement."
      },
      {
        "appliesTo": ["forest-masks"],
        "when": [{ "constraint": "label-extent", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Question 9: forest masks 'would need to be replaced for the target region'. Tested against the label extent like the EO strategy, because the questionnaire names no boundary of its own for them."
      },
      {
        "appliesTo": ["eo-strategy"],
        "when": [{ "constraint": "label-extent", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": false,
        "transferabilityNotes": "Question 9: the strategy 'may also need adjustment to local conditions'. Optional because the owner says 'may'; the source states no consequence for leaving it unadjusted, and the owner is asked what triggers the adjustment."
      },
      {
        "appliesTo": ["phenology"],
        "when": [{ "constraint": "phenological-regime", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
      }
    ]
  },
  "computationType": "statistical-ml",
  "maturityStatus": "prototype",
  "qualityAnnotation": [
    {
      "dimension": "validation-incomplete",
      "note": "Question 5: 'structured regression testing and full scientific validation are not yet complete'. A separate axis from maturityStatus: it says how far the results can be trusted, not how far along the software is."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF3 \u2014 Prediction of threatened stands",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        }
      ]
    }
  },
  "inputs": {
    "disturbance_labels": {
      "type": "File"
    },
    "forest_masks": {
      "type": "File"
    },
    "eo_compositing_strategy": {
      "type": "string"
    },
    "phenology_normalization_assumptions": {
      "type": "string"
    }
  },
  "transferability": {
    "trainingRequired": true,
    "envelope": [
      {
        "id": "label-extent",
        "role": "trained-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"
        },
        "transferabilityNotes": "More speculative than FP-WF1's or FP-WF2's: no sentence in this questionnaire names a location for the historical disturbance labels. Czechia is used as a proxy because this is a Forest Pilot workflow, and Czechia's country border (simplified) as the value, standing in for an extent the owner did not state. Needs owner confirmation before being treated as fact."
      },
      {
        "id": "phenological-regime",
        "role": "valid-for",
        "dimension": "ecological",
        "value": "a comparable phenological regime"
      }
    ],
    "artifacts": [
      {
        "id": "labels",
        "artifact": "historical forest disturbance/damage labels (ground truth training data)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/disturbance_labels",
        "transferabilityNotes": "Question 9 also lists \"model training data\" among the things to replace. Read here as the same thing as these labels, because Question 4 describes the labels as the polygons \"for training or validation\". Needs owner confirmation."
      },
      {
        "id": "forest-masks",
        "artifact": "forest masks or stand boundaries",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/forest_masks"
      },
      {
        "id": "eo-strategy",
        "artifact": "EO sensor selection, cloud masking, temporal compositing strategy",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/eo_compositing_strategy"
      },
      {
        "id": "phenology",
        "artifact": "regional phenology normalisation assumptions",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/phenology_normalization_assumptions"
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "labels"
        ],
        "when": [
          {
            "constraint": "label-extent",
            "test": "outside"
          }
        ],
        "actions": [
          "retrain"
        ],
        "mandatory": false,
        "transferabilityNotes": "Without local training labels, results should be treated as exploratory rather than blocked outright \u2014 a degraded-mode caveat, not a hard requirement."
      },
      {
        "appliesTo": [
          "forest-masks"
        ],
        "when": [
          {
            "constraint": "label-extent",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Question 9: forest masks 'would need to be replaced for the target region'. Tested against the label extent like the EO strategy, because the questionnaire names no boundary of its own for them."
      },
      {
        "appliesTo": [
          "eo-strategy"
        ],
        "when": [
          {
            "constraint": "label-extent",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Question 9: the strategy 'may also need adjustment to local conditions'. Optional because the owner says 'may'; the source states no consequence for leaving it unadjusted, and the owner is asked what triggers the adjustment."
      },
      {
        "appliesTo": [
          "phenology"
        ],
        "when": [
          {
            "constraint": "phenological-regime",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true
      }
    ]
  },
  "computationType": "statistical-ml",
  "maturityStatus": "prototype",
  "qualityAnnotation": [
    {
      "dimension": "validation-incomplete",
      "note": "Question 5: 'structured regression testing and full scientific validation are not yet complete'. A separate axis from maturityStatus: it says how far the results can be trusted, not how far along the software is."
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/> a cwl:Workflow ;
    rdfs:label "FP-WF3 — Prediction of threatened stands" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/disturbance_labels>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo_compositing_strategy>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest_masks>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology_normalization_assumptions> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns1:package "python" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/prototype> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/validation-incomplete> ;
            focal-transf-prop:note "Question 5: 'structured regression testing and full scientific validation are not yet complete'. A separate axis from maturityStatus: it says how far the results can be trusted, not how far along the software is." ] ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo-strategy>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest-masks>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/labels>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenological-regime> ;
            focal-transf-prop:rules [ rdfs:comment "Question 9: forest masks 'would need to be replaced for the target region'. Tested against the label extent like the EO strategy, because the questionnaire names no boundary of its own for them." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest-masks> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 9: the strategy 'may also need adjustment to local conditions'. Optional because the owner says 'may'; the source states no consequence for leaving it unadjusted, and the owner is asked what triggers the adjustment." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo-strategy> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Without local training labels, results should be treated as exploratory rather than blocked outright — a degraded-mode caveat, not a hard requirement." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/labels> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenological-regime> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ;
            focal-transf-prop:trainingRequired true ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/disturbance_labels> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo_compositing_strategy> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest_masks> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology_normalization_assumptions> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo-strategy> dcterms:title "EO sensor selection, cloud masking, temporal compositing strategy" ;
    focal-transf-prop:artifactRef "/inputs/eo_compositing_strategy" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/forest-masks> dcterms:title "forest masks or stand boundaries" ;
    focal-transf-prop:artifactRef "/inputs/forest_masks" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/labels> dcterms:title "historical forest disturbance/damage labels (ground truth training data)" ;
    rdfs:comment "Question 9 also lists \"model training data\" among the things to replace. Read here as the same thing as these labels, because Question 4 describes the labels as the polygons \"for training or validation\". Needs owner confirmation." ;
    focal-transf-prop:artifactRef "/inputs/disturbance_labels" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenological-regime> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "a comparable phenological regime" .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology> dcterms:title "regional phenology normalisation assumptions" ;
    focal-transf-prop:artifactRef "/inputs/phenology_normalization_assumptions" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> rdfs:comment "More speculative than FP-WF1's or FP-WF2's: no sentence in this questionnaire names a location for the historical disturbance labels. Czechia is used as a proxy because this is a Forest Pilot workflow, and Czechia's country border (simplified) as the value, standing in for an extent the owner did not state. Needs owner confirmation before being treated as fact." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"^^geo:wktLiteral ] .


```


### UP-WF2 — Urban hot/cool spot (two footprints, a cascade, a terminal outcome)
The workflow this restructure was designed against, and the one the previous model could not
state correctly.

**Two distinct coverage footprints.** The LST datasets are bounded by the EURO-CORDEX EUR-11
domain; the CLMS layers by that product's own coverage. Previously both were workflow-level
envelope entries told apart only by putting one under `jurisdictional` — a dimension defined
as an administrative or licensing boundary, which a dataset footprint is not. Now both are
`spatial`, each has an `id`, and each rule cites the one that actually governs it.

**CLMS's exclusion of Ukraine is its own constraint, not a hole in a geometry.** The previous
model carried a computed Europe-minus-Ukraine MultiPolygon at full border resolution, with the
exclusion invisible to anyone reading it and quietly lost the moment the geometry was
simplified. Here it is a named constraint cited by a rule with `test: inside`, so falling
within the excluded area is what makes the component unexecutable. It is legible, it is
separately correctable when the authoritative CLMS geometry arrives, and it survives
simplification of the surrounding extent.

Asked "can I run this in Kyiv?", a consumer now gets a per-artifact answer: the LST datasets
are inside EURO-CORDEX and reusable, and the CLMS layers are unavailable, so hot-spot
characterization cannot run.

**`affects` is what makes that last clause a fact rather than a remark.** The rules naming
`component-not-executable` point at the step it costs, so the per-artifact answers roll up
into a per-workflow verdict: Kyiv loses one step, not the run. Without it the model would
say "a component cannot be executed" and leave a consumer no way to find out which, which is
the difference between a partial result and no result.

**Rules are exceptions.** The CLMS layers have no rule for the case where the target is
inside coverage and outside the excluded area, because none is needed: an artifact no rule
fires for is reused unchanged. Only the LST datasets carry an explicit `reuse-as-is`, and
only because pairing it with the `outside` rule is what makes that cascade readable.

**The cascade keeps its connecting condition.** The source describes reuse inside the domain,
substitution if a compatible dataset can be produced outside it, and failure if none can.
That is two rules over the same constraint — `inside` then `outside` — rather than the
previous two flat rules that dropped the "only if a substitute exists" link. The residual
uncertainty stays where the source leaves it: an OR-set of two actions.

The **temporal constraint is directly evidenced**, unlike the omitted periods elsewhere:
discrete epochs, 2022–2025 at time of writing.

Geometries are coarse country-based extents, not cadastral boundaries, and say so on the
constraint. `clms-extent` follows the owner's statement that the CLMS products cover "Europe,
except for Ukraine": a coarse union of European countries clipped to a European window, so
places outside Europe (the Maghreb coast, for one) are outside it. It does not settle whether
CLMS covers Russia, Belarus or Moldova, which the owners were asked. The Ukraine exclusion
stays a separate constraint because it was stated; any others are not known, which is what
question 3 to the workflow owners is for.

`outputs` omitted. `inputs` and `steps` ids are **placeholders** invented so `artifactRef`
and `affects` have something to point at; they are not UP-WF2's real interface, and the step
bodies are stubs. The planned Heat Risk Indicator has one too, so the rule saying it cannot run
without census data names a step that exists: a record that names a component it does not have
would mislead a consumer about which components stop. Its Eurostat dependency stays an
`external-resource` with no `artifactRef`, since the data is not implemented and there is
nothing to point into.

The questionnaire gives the Python requirement as "3.10+"; CWL's version list cannot say "and
later", so only the lower bound is recorded.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF2 — Urban hot/cool spot",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        { "package": "python", "version": ["3.10"] },
        { "package": "rioxarray" },
        { "package": "xarray" },
        { "package": "rasterio" },
        { "package": "geopandas" },
        { "package": "shapely" },
        { "package": "numpy" },
        { "package": "pandas" },
        { "package": "matplotlib" },
        { "package": "joblib" }
      ]
    },
    "NetworkAccess": { "networkAccess": true }
  },
  "inputs": { "lst_datasets": { "type": "File" }, "clms_tcd_imd": { "type": "File" } },
  "steps": {
    "lst_preparation": {
      "run": "#lst_preparation.cwl",
      "in": { "lst": "lst_datasets" },
      "out": ["lst_composite"]
    },
    "hotspot_characterization": {
      "run": "#hotspot_characterization.cwl",
      "in": { "lst": "lst_preparation/lst_composite", "clms": "clms_tcd_imd" },
      "out": ["hotspot_map"]
    },
    "heat_risk_indicator": {
      "run": "#heat_risk_indicator.cwl",
      "in": { "hotspots": "hotspot_characterization/hotspot_map" },
      "out": ["heat_risk_map"]
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "eur11-domain",
        "role": "valid-for",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))" },
        "transferabilityNotes": "The EUR-11 EURO-CORDEX domain's published approximate rectangular extent (about 22W–45E, 27N–72N), not its exact rotated-pole grid footprint, which is not a rectangle in true lat/lon at all. A deliberate simplification."
      },
      {
        "id": "clms-extent",
        "role": "valid-for",
        "dimension": "spatial",
        "value": { "asWKT": "MULTIPOLYGON (((-9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.93 56.44, 9.59 55.49, 9.87 54.47, 14.58 53.64, 13.83 54.13, 18.09 54.84, 19.41 54.39, 21.11 55.62, 20.59 54.98, 21.19 54.94, 21.73 57.57, 24.38 57.25, 24.53 58.35, 23.49 59.2, 30.16 59.9, 28.51 60.68, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.41 62.51, 17.25 60.7, 18.97 59.76, 16.21 58.64, 16.92 58.49, 16.35 56.71, 14.17 55.4, 12.89 55.41, 12.88 56.62, 10.6 59.76, 8.17 58.15, 5.59 58.62, 6.42 59.55, 5.24 59.56, 7 60.51, 5.15 59.64, 5.65 60.69, 5.01 61.04, 7.04 60.95, 7.6 61.21, 5.11 61.19, 4.93 61.88, 6.02 61.79, 6.73 61.87, 5.14 62.16, 8.62 62.85, 8.58 63.6, 10.02 63.39, 11.37 63.8, 9.57 63.71, 12.92 65.34, 12.12 65.36, 14.03 66.3, 13.12 66.23, 13.65 66.91, 15.42 67.2, 14.44 67.27, 15.59 67.35, 15.05 67.96, 16.31 67.88, 19.2 69.75, 23.35 69.98, 24.66 71, 25.77 70.85, 25.04 70.11, 27.6 71.09, 28.39 70.98, 28.19 70.25, 30.07 70.7, 30.94 70.27, 28.8 70.09, 40.97 67.71, 41.19 66.83, 38.65 66.07, 34.48 66.55, 32.93 67.09, 31.9 67.16, 34.69 65.95, 35.04 64.44, 37.44 63.81, 38.06 64.09, 36.88 65.17, 39.76 64.58, 40.44 64.78, 39.82 65.6, 42.21 66.52, 44.1 66.01, 44.2 68.25, 43.33 68.67, 45 68.58, 45 42.71, 39.98 43.42, 36.63 45.15, 39.2 47.27, 35.23 46.44, 35.02 45.7, 36.39 45.07, 33.91 44.39, 32.51 45.4, 33.59 46.1, 31.83 46.28, 32.58 46.62, 31.76 47.21, 31.87 46.65, 28.89 44.92, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.06 37.77, 23.05 37.9, 23.16 36.45, 22.49 36.45, 21.12 37.89, 23.18 38.13, 21.11 38.38, 19.32 40.41, 19.58 41.79, 13.21 45.77, 12.27 45.45, 12.4 44.22, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.94 37.02, -9.18 43.17)), ((-6.32 52.25, -10.38 51.87, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -10.06 54.26, -8.55 54.24, -7.31 55.37, -5.53 54.62, -6.35 53.94, -6.32 52.25)), ((-5.26 51.88, -4.15 52.33, -4.27 53.14, -2.75 53.31, -3.59 54.56, -3.04 54.95, -4.91 54.69, -4.58 55.94, -5.73 55.33, -5.19 56.76, -6.13 56.72, -5.02 58.57, -3.05 58.63, -4.13 57.58, -1.78 57.47, -3.31 56.36, -2.67 56.25, -3.79 56.1, -2.15 55.9, -0.08 54.12, 0.12 53.61, -0.27 53.74, -0.66 53.72, 0.05 52.91, 1.75 52.47, 0.42 51.47, 1.41 51.36, 0.96 50.93, -5.66 50.08, -4.19 51.19, -3.14 51.21, -2.43 51.74, -5.26 51.88)), ((-13.6 65.04, -18.65 63.41, -22.65 63.83, -21.59 64.63, -24.03 64.86, -21.84 65.45, -24.48 65.53, -22.44 65.91, -22.89 66.44, -21.13 65.27, -20.21 66.1, -14.7 66.34, -13.6 65.04)))" },
        "transferabilityNotes": "Question 4: the CLMS products cover 'Europe, except for Ukraine'. The geometry follows that statement: a coarse union of European countries (Natural Earth, public domain, simplified to a few tens of kilometers) clipped to a European window that drops overseas territories and Asian Russia. It does not settle whether CLMS covers Russia, Belarus or Moldova; that is unknown and asked of the owner. The precise boundary is a property of the CLMS product and is better dereferenced from CLMS than restated approximately here. The exclusion of Ukraine is a separate constraint (`clms-excluded-ukraine`) rather than a hole in this one — an exclusion carved into a geometry is invisible to a reader and easy to lose in simplification, whereas a named constraint a rule cites is neither."
      },
      {
        "id": "clms-excluded-ukraine",
        "role": "valid-for",
        "dimension": "spatial",
        "value": { "asWKT": "MULTIPOLYGON (((37.54 47.07, 36.79 46.71, 35.83 46.62, 35.2 46.17, 35.01 46.11, 35.28 46.28, 35.23 46.44, 34.85 46.19, 34.95 45.73, 34.69 45.98, 33.81 46.21, 33.43 46.06, 33.2 46.18, 32.48 46.08, 31.83 46.28, 32.01 46.43, 31.55 46.55, 32.36 46.47, 32.58 46.62, 32.04 46.64, 31.94 46.98, 31.76 47.21, 31.87 46.65, 31.53 46.66, 31.56 46.78, 30.8 46.55, 30.22 45.87, 29.63 45.72, 29.71 45.26, 29.4 45.42, 28.76 45.23, 28.21 45.45, 28.5 45.52, 28.49 45.67, 28.95 46.05, 28.96 46.46, 30.13 46.42, 29.92 46.54, 29.88 46.83, 29.57 46.96, 29.54 47.27, 29.13 47.49, 29.13 47.96, 27.55 48.48, 26.85 48.39, 26.31 48.2, 26.16 47.99, 24.89 47.72, 24.48 47.95, 23.14 48.09, 22.88 47.95, 22.13 48.41, 22.14 48.57, 22.54 49.07, 22.84 49.04, 22.71 49.17, 22.71 49.61, 24.09 50.53, 23.98 50.79, 24.1 50.87, 23.66 51.31, 23.61 51.61, 23.98 51.59, 24.36 51.87, 25.93 51.91, 27.14 51.75, 27.7 51.48, 28.18 51.61, 28.73 51.43, 29.1 51.63, 29.35 51.38, 30.16 51.48, 30.54 51.27, 30.58 51.69, 30.98 52.05, 32.12 52.05, 32.44 52.31, 33.74 52.34, 34.4 51.78, 34.12 51.68, 34.21 51.26, 35.06 51.2, 35.31 51.04, 35.41 50.54, 35.59 50.37, 36.12 50.41, 36.62 50.21, 37.42 50.41, 38.05 49.92, 38.26 50.05, 40.08 49.58, 40.11 49.25, 39.69 49.01, 40 48.82, 39.79 48.81, 39.64 48.59, 39.84 48.54, 39.96 48.27, 39.78 47.89, 38.9 47.86, 38.37 47.61, 38.21 47.09, 37.54 47.07)), ((32.15 46.15, 31.56 46.26, 31.51 46.37, 32.15 46.15)))" },
        "transferabilityNotes": "Ukraine's country border (Natural Earth, public domain, simplified to a few tens of kilometers), the area the owner says the CLMS products exclude (Question 4: 'Europe, except for Ukraine'). Cited by a rule with test `inside`, so falling within it is what makes the component unexecutable. Kept as its own constraint so it can be corrected separately when the authoritative CLMS geometry is available. Near the border a target within a few tens of kilometers of the line may be classified the wrong way."
      },
      {
        "id": "epochs",
        "role": "can-run-on",
        "dimension": "temporal",
        "value": { "startDate": "2022", "endDate": "2025" },
        "transferabilityNotes": "The epochs available now: discrete temporal epochs, explicitly not a time series (one timestep per epoch), 2022–2025 available at time of writing. Question 6 says two to three more periods are planned, and Question 4 that the Landsat source depends on the selected time period, so this is what is available, not a validity limit."
      }
    ],
    "artifacts": [
      { "id": "lst", "artifact": "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)", "artifactRole": "workflow-input", "artifactRef": "/inputs/lst_datasets" },
      { "id": "clms", "artifact": "CLMS Tree Cover Density / Imperviousness Density", "artifactRole": "workflow-input", "artifactRef": "/inputs/clms_tcd_imd" },
      { "id": "eurostat", "artifact": "Eurostat census / socio-economic data (planned Heat Risk Indicator)", "artifactRole": "external-resource", "transferabilityNotes": "Not yet implemented; the envisaged replacement should follow a schema compatible with Eurostat's." }
    ],
    "rules": [
      {
        "appliesTo": ["lst"],
        "when": [{ "constraint": "eur11-domain", "test": "inside" }],
        "actions": ["reuse-as-is"],
        "transferabilityNotes": "Inside the EURO-CORDEX domain the datasets are reused unchanged, by changing the area of interest."
      },
      {
        "appliesTo": ["lst"],
        "when": [{ "constraint": "eur11-domain", "test": "outside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/hotspot_characterization"],
        "mandatory": true,
        "transferabilityNotes": "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target. Which of the two applies depends on whether a substitute is obtainable, which the source does not resolve."
      },
      {
        "appliesTo": ["clms"],
        "when": [{ "constraint": "clms-extent", "test": "outside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/hotspot_characterization"],
        "mandatory": true,
        "transferabilityNotes": "Outside CLMS coverage, Question 9 asks for 'Equivalent environmental datasets (e.g., Tree Cover Density and Imperviousness)' and says that without them some components, particularly hot spot characterization, cannot be executed. Which of the two applies depends on whether an equivalent exists, which the source does not resolve."
      },
      {
        "appliesTo": ["clms"],
        "when": [{ "constraint": "clms-excluded-ukraine", "test": "inside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/hotspot_characterization"],
        "mandatory": true,
        "transferabilityNotes": "Inside the area the product excludes (Question 4): the same cascade as outside CLMS coverage, because Ukraine is one more place the product does not cover. Whether an equivalent exists is not resolved by the source."
      },
      {
        "appliesTo": ["eurostat"],
        "when": [{ "constraint": "eur11-domain", "test": "outside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/heat_risk_indicator"],
        "mandatory": false,
        "transferabilityNotes": "Question 9: outside the EURO-CORDEX domain, 'Availability of comparable census or socio-economic data (preferably following a schema compatible with Eurostat)' is needed, and without the datasets some components cannot be executed. Optional because the Heat Risk Indicator is planned and not yet implemented: today its absence costs a planned step, not the current workflow."
      }
    ],
    "transferabilityNotes": "Question 9 states a portability fact that no shape here holds: the classification step is data-agnostic. 'The LST dataset the hot and cool spot classification is based on is a raster dataset with a single time step and one value per grid cell. It is not a time series. Hence, the classification could also be applied to other raster datasets with a single time step and one value per grid cell.' In other words the algorithm is more portable than the specific input dataset. Recorded as a note because one workflow does not justify a property."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "proxy-variable",
      "note": "Question 7: 'Hot spot detection is based on median summer Land Surface Temperature, which represents surface temperatures rather than near-surface air temperatures.' What the workflow computes is a stand-in for the air temperature a reader might assume, in the source region as much as in any target."
    },
    {
      "dimension": "intended-use-limit",
      "note": "Question 7: 'Results represent long-term thermal patterns for the selected epoch and are not intended for real-time heat monitoring.'"
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF2 \u2014 Urban hot/cool spot",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python",
          "version": [
            "3.10"
          ]
        },
        {
          "package": "rioxarray"
        },
        {
          "package": "xarray"
        },
        {
          "package": "rasterio"
        },
        {
          "package": "geopandas"
        },
        {
          "package": "shapely"
        },
        {
          "package": "numpy"
        },
        {
          "package": "pandas"
        },
        {
          "package": "matplotlib"
        },
        {
          "package": "joblib"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "lst_datasets": {
      "type": "File"
    },
    "clms_tcd_imd": {
      "type": "File"
    }
  },
  "steps": {
    "lst_preparation": {
      "run": "#lst_preparation.cwl",
      "in": {
        "lst": "lst_datasets"
      },
      "out": [
        "lst_composite"
      ]
    },
    "hotspot_characterization": {
      "run": "#hotspot_characterization.cwl",
      "in": {
        "lst": "lst_preparation/lst_composite",
        "clms": "clms_tcd_imd"
      },
      "out": [
        "hotspot_map"
      ]
    },
    "heat_risk_indicator": {
      "run": "#heat_risk_indicator.cwl",
      "in": {
        "hotspots": "hotspot_characterization/hotspot_map"
      },
      "out": [
        "heat_risk_map"
      ]
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "eur11-domain",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))"
        },
        "transferabilityNotes": "The EUR-11 EURO-CORDEX domain's published approximate rectangular extent (about 22W\u201345E, 27N\u201372N), not its exact rotated-pole grid footprint, which is not a rectangle in true lat/lon at all. A deliberate simplification."
      },
      {
        "id": "clms-extent",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "MULTIPOLYGON (((-9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.93 56.44, 9.59 55.49, 9.87 54.47, 14.58 53.64, 13.83 54.13, 18.09 54.84, 19.41 54.39, 21.11 55.62, 20.59 54.98, 21.19 54.94, 21.73 57.57, 24.38 57.25, 24.53 58.35, 23.49 59.2, 30.16 59.9, 28.51 60.68, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.41 62.51, 17.25 60.7, 18.97 59.76, 16.21 58.64, 16.92 58.49, 16.35 56.71, 14.17 55.4, 12.89 55.41, 12.88 56.62, 10.6 59.76, 8.17 58.15, 5.59 58.62, 6.42 59.55, 5.24 59.56, 7 60.51, 5.15 59.64, 5.65 60.69, 5.01 61.04, 7.04 60.95, 7.6 61.21, 5.11 61.19, 4.93 61.88, 6.02 61.79, 6.73 61.87, 5.14 62.16, 8.62 62.85, 8.58 63.6, 10.02 63.39, 11.37 63.8, 9.57 63.71, 12.92 65.34, 12.12 65.36, 14.03 66.3, 13.12 66.23, 13.65 66.91, 15.42 67.2, 14.44 67.27, 15.59 67.35, 15.05 67.96, 16.31 67.88, 19.2 69.75, 23.35 69.98, 24.66 71, 25.77 70.85, 25.04 70.11, 27.6 71.09, 28.39 70.98, 28.19 70.25, 30.07 70.7, 30.94 70.27, 28.8 70.09, 40.97 67.71, 41.19 66.83, 38.65 66.07, 34.48 66.55, 32.93 67.09, 31.9 67.16, 34.69 65.95, 35.04 64.44, 37.44 63.81, 38.06 64.09, 36.88 65.17, 39.76 64.58, 40.44 64.78, 39.82 65.6, 42.21 66.52, 44.1 66.01, 44.2 68.25, 43.33 68.67, 45 68.58, 45 42.71, 39.98 43.42, 36.63 45.15, 39.2 47.27, 35.23 46.44, 35.02 45.7, 36.39 45.07, 33.91 44.39, 32.51 45.4, 33.59 46.1, 31.83 46.28, 32.58 46.62, 31.76 47.21, 31.87 46.65, 28.89 44.92, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.06 37.77, 23.05 37.9, 23.16 36.45, 22.49 36.45, 21.12 37.89, 23.18 38.13, 21.11 38.38, 19.32 40.41, 19.58 41.79, 13.21 45.77, 12.27 45.45, 12.4 44.22, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.94 37.02, -9.18 43.17)), ((-6.32 52.25, -10.38 51.87, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -10.06 54.26, -8.55 54.24, -7.31 55.37, -5.53 54.62, -6.35 53.94, -6.32 52.25)), ((-5.26 51.88, -4.15 52.33, -4.27 53.14, -2.75 53.31, -3.59 54.56, -3.04 54.95, -4.91 54.69, -4.58 55.94, -5.73 55.33, -5.19 56.76, -6.13 56.72, -5.02 58.57, -3.05 58.63, -4.13 57.58, -1.78 57.47, -3.31 56.36, -2.67 56.25, -3.79 56.1, -2.15 55.9, -0.08 54.12, 0.12 53.61, -0.27 53.74, -0.66 53.72, 0.05 52.91, 1.75 52.47, 0.42 51.47, 1.41 51.36, 0.96 50.93, -5.66 50.08, -4.19 51.19, -3.14 51.21, -2.43 51.74, -5.26 51.88)), ((-13.6 65.04, -18.65 63.41, -22.65 63.83, -21.59 64.63, -24.03 64.86, -21.84 65.45, -24.48 65.53, -22.44 65.91, -22.89 66.44, -21.13 65.27, -20.21 66.1, -14.7 66.34, -13.6 65.04)))"
        },
        "transferabilityNotes": "Question 4: the CLMS products cover 'Europe, except for Ukraine'. The geometry follows that statement: a coarse union of European countries (Natural Earth, public domain, simplified to a few tens of kilometers) clipped to a European window that drops overseas territories and Asian Russia. It does not settle whether CLMS covers Russia, Belarus or Moldova; that is unknown and asked of the owner. The precise boundary is a property of the CLMS product and is better dereferenced from CLMS than restated approximately here. The exclusion of Ukraine is a separate constraint (`clms-excluded-ukraine`) rather than a hole in this one \u2014 an exclusion carved into a geometry is invisible to a reader and easy to lose in simplification, whereas a named constraint a rule cites is neither."
      },
      {
        "id": "clms-excluded-ukraine",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "MULTIPOLYGON (((37.54 47.07, 36.79 46.71, 35.83 46.62, 35.2 46.17, 35.01 46.11, 35.28 46.28, 35.23 46.44, 34.85 46.19, 34.95 45.73, 34.69 45.98, 33.81 46.21, 33.43 46.06, 33.2 46.18, 32.48 46.08, 31.83 46.28, 32.01 46.43, 31.55 46.55, 32.36 46.47, 32.58 46.62, 32.04 46.64, 31.94 46.98, 31.76 47.21, 31.87 46.65, 31.53 46.66, 31.56 46.78, 30.8 46.55, 30.22 45.87, 29.63 45.72, 29.71 45.26, 29.4 45.42, 28.76 45.23, 28.21 45.45, 28.5 45.52, 28.49 45.67, 28.95 46.05, 28.96 46.46, 30.13 46.42, 29.92 46.54, 29.88 46.83, 29.57 46.96, 29.54 47.27, 29.13 47.49, 29.13 47.96, 27.55 48.48, 26.85 48.39, 26.31 48.2, 26.16 47.99, 24.89 47.72, 24.48 47.95, 23.14 48.09, 22.88 47.95, 22.13 48.41, 22.14 48.57, 22.54 49.07, 22.84 49.04, 22.71 49.17, 22.71 49.61, 24.09 50.53, 23.98 50.79, 24.1 50.87, 23.66 51.31, 23.61 51.61, 23.98 51.59, 24.36 51.87, 25.93 51.91, 27.14 51.75, 27.7 51.48, 28.18 51.61, 28.73 51.43, 29.1 51.63, 29.35 51.38, 30.16 51.48, 30.54 51.27, 30.58 51.69, 30.98 52.05, 32.12 52.05, 32.44 52.31, 33.74 52.34, 34.4 51.78, 34.12 51.68, 34.21 51.26, 35.06 51.2, 35.31 51.04, 35.41 50.54, 35.59 50.37, 36.12 50.41, 36.62 50.21, 37.42 50.41, 38.05 49.92, 38.26 50.05, 40.08 49.58, 40.11 49.25, 39.69 49.01, 40 48.82, 39.79 48.81, 39.64 48.59, 39.84 48.54, 39.96 48.27, 39.78 47.89, 38.9 47.86, 38.37 47.61, 38.21 47.09, 37.54 47.07)), ((32.15 46.15, 31.56 46.26, 31.51 46.37, 32.15 46.15)))"
        },
        "transferabilityNotes": "Ukraine's country border (Natural Earth, public domain, simplified to a few tens of kilometers), the area the owner says the CLMS products exclude (Question 4: 'Europe, except for Ukraine'). Cited by a rule with test `inside`, so falling within it is what makes the component unexecutable. Kept as its own constraint so it can be corrected separately when the authoritative CLMS geometry is available. Near the border a target within a few tens of kilometers of the line may be classified the wrong way."
      },
      {
        "id": "epochs",
        "role": "can-run-on",
        "dimension": "temporal",
        "value": {
          "startDate": "2022",
          "endDate": "2025"
        },
        "transferabilityNotes": "The epochs available now: discrete temporal epochs, explicitly not a time series (one timestep per epoch), 2022\u20132025 available at time of writing. Question 6 says two to three more periods are planned, and Question 4 that the Landsat source depends on the selected time period, so this is what is available, not a validity limit."
      }
    ],
    "artifacts": [
      {
        "id": "lst",
        "artifact": "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/lst_datasets"
      },
      {
        "id": "clms",
        "artifact": "CLMS Tree Cover Density / Imperviousness Density",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/clms_tcd_imd"
      },
      {
        "id": "eurostat",
        "artifact": "Eurostat census / socio-economic data (planned Heat Risk Indicator)",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Not yet implemented; the envisaged replacement should follow a schema compatible with Eurostat's."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "lst"
        ],
        "when": [
          {
            "constraint": "eur11-domain",
            "test": "inside"
          }
        ],
        "actions": [
          "reuse-as-is"
        ],
        "transferabilityNotes": "Inside the EURO-CORDEX domain the datasets are reused unchanged, by changing the area of interest."
      },
      {
        "appliesTo": [
          "lst"
        ],
        "when": [
          {
            "constraint": "eur11-domain",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "affects": [
          "/steps/hotspot_characterization"
        ],
        "mandatory": true,
        "transferabilityNotes": "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target. Which of the two applies depends on whether a substitute is obtainable, which the source does not resolve."
      },
      {
        "appliesTo": [
          "clms"
        ],
        "when": [
          {
            "constraint": "clms-extent",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "affects": [
          "/steps/hotspot_characterization"
        ],
        "mandatory": true,
        "transferabilityNotes": "Outside CLMS coverage, Question 9 asks for 'Equivalent environmental datasets (e.g., Tree Cover Density and Imperviousness)' and says that without them some components, particularly hot spot characterization, cannot be executed. Which of the two applies depends on whether an equivalent exists, which the source does not resolve."
      },
      {
        "appliesTo": [
          "clms"
        ],
        "when": [
          {
            "constraint": "clms-excluded-ukraine",
            "test": "inside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "affects": [
          "/steps/hotspot_characterization"
        ],
        "mandatory": true,
        "transferabilityNotes": "Inside the area the product excludes (Question 4): the same cascade as outside CLMS coverage, because Ukraine is one more place the product does not cover. Whether an equivalent exists is not resolved by the source."
      },
      {
        "appliesTo": [
          "eurostat"
        ],
        "when": [
          {
            "constraint": "eur11-domain",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "affects": [
          "/steps/heat_risk_indicator"
        ],
        "mandatory": false,
        "transferabilityNotes": "Question 9: outside the EURO-CORDEX domain, 'Availability of comparable census or socio-economic data (preferably following a schema compatible with Eurostat)' is needed, and without the datasets some components cannot be executed. Optional because the Heat Risk Indicator is planned and not yet implemented: today its absence costs a planned step, not the current workflow."
      }
    ],
    "transferabilityNotes": "Question 9 states a portability fact that no shape here holds: the classification step is data-agnostic. 'The LST dataset the hot and cool spot classification is based on is a raster dataset with a single time step and one value per grid cell. It is not a time series. Hence, the classification could also be applied to other raster datasets with a single time step and one value per grid cell.' In other words the algorithm is more portable than the specific input dataset. Recorded as a note because one workflow does not justify a property."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "proxy-variable",
      "note": "Question 7: 'Hot spot detection is based on median summer Land Surface Temperature, which represents surface temperatures rather than near-surface air temperatures.' What the workflow computes is a stand-in for the air temperature a reader might assume, in the source region as much as in any target."
    },
    {
      "dimension": "intended-use-limit",
      "note": "Question 7: 'Results represent long-term thermal patterns for the selected epoch and are not intended for real-time heat monitoring.'"
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns2: <https://w3id.org/cwl/cwl#Workflow/> .
@prefix ns3: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns4: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/> a cwl:Workflow ;
    rdfs:label "UP-WF2 — Urban hot/cool spot" ;
    ns2:steps <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/heat_risk_indicator>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/hotspot_characterization>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst_preparation> ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms_tcd_imd>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst_datasets> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns3:packages [ ns1:package "numpy" ],
                [ ns1:package "shapely" ],
                [ ns1:package "xarray" ],
                [ ns1:package "matplotlib" ],
                [ ns1:package "python" ;
                    ns1:version "3.10" ],
                [ ns1:package "joblib" ],
                [ ns1:package "rioxarray" ],
                [ ns1:package "geopandas" ],
                [ ns1:package "rasterio" ],
                [ ns1:package "pandas" ] ],
        [ a cwl:NetworkAccess ;
            ns4:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/intended-use-limit> ;
            focal-transf-prop:note "Question 7: 'Results represent long-term thermal patterns for the selected epoch and are not intended for real-time heat monitoring.'" ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/proxy-variable> ;
            focal-transf-prop:note "Question 7: 'Hot spot detection is based on median summer Land Surface Temperature, which represents surface temperatures rather than near-surface air temperatures.' What the workflow computes is a stand-in for the air temperature a reader might assume, in the source region as much as in any target." ] ;
    focal-transf-prop:transferability [ rdfs:comment "Question 9 states a portability fact that no shape here holds: the classification step is data-agnostic. 'The LST dataset the hot and cool spot classification is based on is a raster dataset with a single time step and one value per grid cell. It is not a time series. Hence, the classification could also be applied to other raster datasets with a single time step and one value per grid cell.' In other words the algorithm is more portable than the specific input dataset. Recorded as a note because one workflow does not justify a property." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eurostat>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-excluded-ukraine>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-extent>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epochs>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> ;
            focal-transf-prop:rules [ rdfs:comment "Inside the area the product excludes (Question 4): the same cascade as outside CLMS coverage, because Ukraine is one more place the product does not cover. Whether an equivalent exists is not resolved by the source." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/steps/hotspot_characterization" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-excluded-ukraine> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/inside> ] ],
                [ rdfs:comment "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target. Which of the two applies depends on whether a substitute is obtainable, which the source does not resolve." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/steps/hotspot_characterization" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 9: outside the EURO-CORDEX domain, 'Availability of comparable census or socio-economic data (preferably following a schema compatible with Eurostat)' is needed, and without the datasets some components cannot be executed. Optional because the Heat Risk Indicator is planned and not yet implemented: today its absence costs a planned step, not the current workflow." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/steps/heat_risk_indicator" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eurostat> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Outside CLMS coverage, Question 9 asks for 'Equivalent environmental datasets (e.g., Tree Cover Density and Imperviousness)' and says that without them some components, particularly hot spot characterization, cannot be executed. Which of the two applies depends on whether an equivalent exists, which the source does not resolve." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/steps/hotspot_characterization" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Inside the EURO-CORDEX domain the datasets are reused unchanged, by changing the area of interest." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/reuse-as-is> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/inside> ] ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms_tcd_imd> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epochs> rdfs:comment "The epochs available now: discrete temporal epochs, explicitly not a time series (one timestep per epoch), 2022–2025 available at time of writing. Question 6 says two to three more periods are planned, and Question 4 that the Landsat source depends on the selected time period, so this is what is available, not a validity limit." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ dcat:endDate "2025" ;
            dcat:startDate "2022" ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/heat_risk_indicator> cwl:in "hotspot_characterization/hotspot_map" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/heat_risk_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/#heat_risk_indicator.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/hotspot_characterization> cwl:in "clms_tcd_imd",
        "lst_preparation/lst_composite" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/hotspot_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/#hotspot_characterization.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst_datasets> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst_preparation> cwl:in "lst_datasets" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst_composite> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/#lst_preparation.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-excluded-ukraine> rdfs:comment "Ukraine's country border (Natural Earth, public domain, simplified to a few tens of kilometers), the area the owner says the CLMS products exclude (Question 4: 'Europe, except for Ukraine'). Cited by a rule with test `inside`, so falling within it is what makes the component unexecutable. Kept as its own constraint so it can be corrected separately when the authoritative CLMS geometry is available. Near the border a target within a few tens of kilometers of the line may be classified the wrong way." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "MULTIPOLYGON (((37.54 47.07, 36.79 46.71, 35.83 46.62, 35.2 46.17, 35.01 46.11, 35.28 46.28, 35.23 46.44, 34.85 46.19, 34.95 45.73, 34.69 45.98, 33.81 46.21, 33.43 46.06, 33.2 46.18, 32.48 46.08, 31.83 46.28, 32.01 46.43, 31.55 46.55, 32.36 46.47, 32.58 46.62, 32.04 46.64, 31.94 46.98, 31.76 47.21, 31.87 46.65, 31.53 46.66, 31.56 46.78, 30.8 46.55, 30.22 45.87, 29.63 45.72, 29.71 45.26, 29.4 45.42, 28.76 45.23, 28.21 45.45, 28.5 45.52, 28.49 45.67, 28.95 46.05, 28.96 46.46, 30.13 46.42, 29.92 46.54, 29.88 46.83, 29.57 46.96, 29.54 47.27, 29.13 47.49, 29.13 47.96, 27.55 48.48, 26.85 48.39, 26.31 48.2, 26.16 47.99, 24.89 47.72, 24.48 47.95, 23.14 48.09, 22.88 47.95, 22.13 48.41, 22.14 48.57, 22.54 49.07, 22.84 49.04, 22.71 49.17, 22.71 49.61, 24.09 50.53, 23.98 50.79, 24.1 50.87, 23.66 51.31, 23.61 51.61, 23.98 51.59, 24.36 51.87, 25.93 51.91, 27.14 51.75, 27.7 51.48, 28.18 51.61, 28.73 51.43, 29.1 51.63, 29.35 51.38, 30.16 51.48, 30.54 51.27, 30.58 51.69, 30.98 52.05, 32.12 52.05, 32.44 52.31, 33.74 52.34, 34.4 51.78, 34.12 51.68, 34.21 51.26, 35.06 51.2, 35.31 51.04, 35.41 50.54, 35.59 50.37, 36.12 50.41, 36.62 50.21, 37.42 50.41, 38.05 49.92, 38.26 50.05, 40.08 49.58, 40.11 49.25, 39.69 49.01, 40 48.82, 39.79 48.81, 39.64 48.59, 39.84 48.54, 39.96 48.27, 39.78 47.89, 38.9 47.86, 38.37 47.61, 38.21 47.09, 37.54 47.07)), ((32.15 46.15, 31.56 46.26, 31.51 46.37, 32.15 46.15)))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-extent> rdfs:comment "Question 4: the CLMS products cover 'Europe, except for Ukraine'. The geometry follows that statement: a coarse union of European countries (Natural Earth, public domain, simplified to a few tens of kilometers) clipped to a European window that drops overseas territories and Asian Russia. It does not settle whether CLMS covers Russia, Belarus or Moldova; that is unknown and asked of the owner. The precise boundary is a property of the CLMS product and is better dereferenced from CLMS than restated approximately here. The exclusion of Ukraine is a separate constraint (`clms-excluded-ukraine`) rather than a hole in this one — an exclusion carved into a geometry is invisible to a reader and easy to lose in simplification, whereas a named constraint a rule cites is neither." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "MULTIPOLYGON (((-9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.93 56.44, 9.59 55.49, 9.87 54.47, 14.58 53.64, 13.83 54.13, 18.09 54.84, 19.41 54.39, 21.11 55.62, 20.59 54.98, 21.19 54.94, 21.73 57.57, 24.38 57.25, 24.53 58.35, 23.49 59.2, 30.16 59.9, 28.51 60.68, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.41 62.51, 17.25 60.7, 18.97 59.76, 16.21 58.64, 16.92 58.49, 16.35 56.71, 14.17 55.4, 12.89 55.41, 12.88 56.62, 10.6 59.76, 8.17 58.15, 5.59 58.62, 6.42 59.55, 5.24 59.56, 7 60.51, 5.15 59.64, 5.65 60.69, 5.01 61.04, 7.04 60.95, 7.6 61.21, 5.11 61.19, 4.93 61.88, 6.02 61.79, 6.73 61.87, 5.14 62.16, 8.62 62.85, 8.58 63.6, 10.02 63.39, 11.37 63.8, 9.57 63.71, 12.92 65.34, 12.12 65.36, 14.03 66.3, 13.12 66.23, 13.65 66.91, 15.42 67.2, 14.44 67.27, 15.59 67.35, 15.05 67.96, 16.31 67.88, 19.2 69.75, 23.35 69.98, 24.66 71, 25.77 70.85, 25.04 70.11, 27.6 71.09, 28.39 70.98, 28.19 70.25, 30.07 70.7, 30.94 70.27, 28.8 70.09, 40.97 67.71, 41.19 66.83, 38.65 66.07, 34.48 66.55, 32.93 67.09, 31.9 67.16, 34.69 65.95, 35.04 64.44, 37.44 63.81, 38.06 64.09, 36.88 65.17, 39.76 64.58, 40.44 64.78, 39.82 65.6, 42.21 66.52, 44.1 66.01, 44.2 68.25, 43.33 68.67, 45 68.58, 45 42.71, 39.98 43.42, 36.63 45.15, 39.2 47.27, 35.23 46.44, 35.02 45.7, 36.39 45.07, 33.91 44.39, 32.51 45.4, 33.59 46.1, 31.83 46.28, 32.58 46.62, 31.76 47.21, 31.87 46.65, 28.89 44.92, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.06 37.77, 23.05 37.9, 23.16 36.45, 22.49 36.45, 21.12 37.89, 23.18 38.13, 21.11 38.38, 19.32 40.41, 19.58 41.79, 13.21 45.77, 12.27 45.45, 12.4 44.22, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.94 37.02, -9.18 43.17)), ((-6.32 52.25, -10.38 51.87, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -10.06 54.26, -8.55 54.24, -7.31 55.37, -5.53 54.62, -6.35 53.94, -6.32 52.25)), ((-5.26 51.88, -4.15 52.33, -4.27 53.14, -2.75 53.31, -3.59 54.56, -3.04 54.95, -4.91 54.69, -4.58 55.94, -5.73 55.33, -5.19 56.76, -6.13 56.72, -5.02 58.57, -3.05 58.63, -4.13 57.58, -1.78 57.47, -3.31 56.36, -2.67 56.25, -3.79 56.1, -2.15 55.9, -0.08 54.12, 0.12 53.61, -0.27 53.74, -0.66 53.72, 0.05 52.91, 1.75 52.47, 0.42 51.47, 1.41 51.36, 0.96 50.93, -5.66 50.08, -4.19 51.19, -3.14 51.21, -2.43 51.74, -5.26 51.88)), ((-13.6 65.04, -18.65 63.41, -22.65 63.83, -21.59 64.63, -24.03 64.86, -21.84 65.45, -24.48 65.53, -22.44 65.91, -22.89 66.44, -21.13 65.27, -20.21 66.1, -14.7 66.34, -13.6 65.04)))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eurostat> dcterms:title "Eurostat census / socio-economic data (planned Heat Risk Indicator)" ;
    rdfs:comment "Not yet implemented; the envisaged replacement should follow a schema compatible with Eurostat's." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms> dcterms:title "CLMS Tree Cover Density / Imperviousness Density" ;
    focal-transf-prop:artifactRef "/inputs/clms_tcd_imd" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> dcterms:title "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)" ;
    focal-transf-prop:artifactRef "/inputs/lst_datasets" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> rdfs:comment "The EUR-11 EURO-CORDEX domain's published approximate rectangular extent (about 22W–45E, 27N–72N), not its exact rotated-pole grid footprint, which is not a rectangle in true lat/lon at all. A deliberate simplification." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))"^^geo:wktLiteral ] .


```


### UP-WF1 — Regional climate change (an empty envelope, stated deliberately)
The thinnest questionnaire in the corpus, and the reason `envelope` has no minimum. Questions
8, 9 and 10 are answered "Nothing", "Nothing" and "All parts are portable"; this example
records exactly that and nothing more.

**An empty `envelope` and an empty `rules` are the claim here, not a shortfall.** Under the
closed-world default — rules are exceptions, silence means reuse — the two empty arrays say
that the owner named no validity boundary and no adaptation step for the delivery. That
is a strong claim, and the statement's `transferabilityNotes` says plainly that it is the
source's claim rather than a verified one: a nine-member regional climate ensemble almost
certainly does have conditions the questionnaire did not surface. Until the owner confirms,
the honest record is the answer as given, marked as unverified, rather than a boundary
invented to make the entry look substantial.

**`noConstraintsStated: true` says outright that the owner named none.** Two empty arrays cannot
be told from a form nobody filled in, which is exactly how a consumer read them when this
record was first tested. The marker changes that, and a shape rejects it alongside any
envelope entry or rule, so it cannot contradict the lists it summarizes.

**The one artifact carries no rule, and that is the point.** The NUKLEUS ensemble is declared
because the delivery depends on it; no rule fires for it because the source states no
adaptation condition. That combination is precisely what the closed-world default was adopted
to make expressible.

**`computationType: precomputed-delivery` is what this workflow evidences.** "Python but data
is precalculated" — the transferable unit is the delivered indices, not a re-executable
package. It is the only workflow in the set for which that term exists.

**The Global Warming Levels are deliberately not in the envelope.** Question 7 says
"Timeslices are represented as Global Warming Levels", which is a real temporal fact: the
results are scenario-indexed rather than calendar-indexed. But no specific level is named
anywhere in the source, and `scenarioMarker` takes a level, not the statement that levels are
the indexing scheme. Writing `gwl-1.5` here would be inventing a slice. Recorded in
`transferabilityNotes` and raised with the owner instead. `inputs`/`outputs` ids are
placeholders; `steps` is omitted, since there is no Application Package and, on this
workflow's own account (Question 3: "Python but data is precalculated"), no re-executable package was described.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF1 — Regional climate change",
  "requirements": {
    "SoftwareRequirement": { "packages": [{ "package": "python" }] }
  },
  "inputs": { "nukleus_ensemble": { "type": "File" } },
  "outputs": { "climate_indices": { "type": "File" } },
  "transferability": {
    "trainingRequired": false,
    "noConstraintsStated": true,
    "envelope": [],
    "artifacts": [
      {
        "id": "nukleus-ensemble",
        "artifact": "9-member NUKLEUS regional climate ensemble",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/nukleus_ensemble",
        "transferabilityNotes": "Declared because the delivered indices depend on it, and left ungoverned because the source states no condition under which it would have to change. Question 9's answer is 'Nothing'."
      }
    ],
    "rules": [],
    "transferabilityNotes": "Both arrays are empty deliberately, not for want of an entry. The questionnaire answers questions 8, 9 and 10 with 'Nothing', 'Nothing' and 'All parts are portable', so this states no validity boundary and no adaptation step. Two caveats travel with that. First, it is the source's claim and not a verified one: a nine-member regional climate ensemble delivered as precomputed indices very likely does carry conditions this questionnaire did not ask about, and the owner has been asked to confirm or correct the emptiness. Second, question 7 states that timeslices are represented as Global Warming Levels rather than calendar periods, which is a genuine temporal fact but not one this envelope can hold: no specific level is named in the source, and the scenario-marker value takes a level, not the assertion that levels are the indexing scheme. Naming one would be fabricating a slice."
  },
  "computationType": "precomputed-delivery",
  "maturityStatus": "operational"
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF1 \u2014 Regional climate change",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        }
      ]
    }
  },
  "inputs": {
    "nukleus_ensemble": {
      "type": "File"
    }
  },
  "outputs": {
    "climate_indices": {
      "type": "File"
    }
  },
  "transferability": {
    "trainingRequired": false,
    "noConstraintsStated": true,
    "envelope": [],
    "artifacts": [
      {
        "id": "nukleus-ensemble",
        "artifact": "9-member NUKLEUS regional climate ensemble",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/nukleus_ensemble",
        "transferabilityNotes": "Declared because the delivered indices depend on it, and left ungoverned because the source states no condition under which it would have to change. Question 9's answer is 'Nothing'."
      }
    ],
    "rules": [],
    "transferabilityNotes": "Both arrays are empty deliberately, not for want of an entry. The questionnaire answers questions 8, 9 and 10 with 'Nothing', 'Nothing' and 'All parts are portable', so this states no validity boundary and no adaptation step. Two caveats travel with that. First, it is the source's claim and not a verified one: a nine-member regional climate ensemble delivered as precomputed indices very likely does carry conditions this questionnaire did not ask about, and the owner has been asked to confirm or correct the emptiness. Second, question 7 states that timeslices are represented as Global Warming Levels rather than calendar periods, which is a genuine temporal fact but not one this envelope can hold: no specific level is named in the source, and the scenario-marker value takes a level, not the assertion that levels are the indexing scheme. Naming one would be fabricating a slice."
  },
  "computationType": "precomputed-delivery",
  "maturityStatus": "operational"
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/> a cwl:Workflow ;
    rdfs:label "UP-WF1 — Regional climate change" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus_ensemble> ;
    cwl:outputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/climate_indices> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns1:package "python" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/precomputed-delivery> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:transferability [ rdfs:comment "Both arrays are empty deliberately, not for want of an entry. The questionnaire answers questions 8, 9 and 10 with 'Nothing', 'Nothing' and 'All parts are portable', so this states no validity boundary and no adaptation step. Two caveats travel with that. First, it is the source's claim and not a verified one: a nine-member regional climate ensemble delivered as precomputed indices very likely does carry conditions this questionnaire did not ask about, and the owner has been asked to confirm or correct the emptiness. Second, question 7 states that timeslices are represented as Global Warming Levels rather than calendar periods, which is a genuine temporal fact but not one this envelope can hold: no specific level is named in the source, and the scenario-marker value takes a level, not the assertion that levels are the indexing scheme. Naming one would be fabricating a slice." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus-ensemble> ;
            focal-transf-prop:noConstraintsStated true ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/climate_indices> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus-ensemble> dcterms:title "9-member NUKLEUS regional climate ensemble" ;
    rdfs:comment "Declared because the delivered indices depend on it, and left ungoverned because the source states no condition under which it would have to change. Question 9's answer is 'Nothing'." ;
    focal-transf-prop:artifactRef "/inputs/nukleus_ensemble" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus_ensemble> sld:type cwl:File .


```


### FP-WF5 — Map of climatic zones (a national classification scheme, and an optional validation reference)
A deterministic Python/Flask microservice classifying an area into forest-oriented climate
zones from Rasdaman-held annual climate indicators, against Quitt-inspired thresholds.

**Two boundaries that happen to share a geometry but not a role.** The Quitt thresholds are
the Czech national climate-zone scheme; `czech-zone-scheme` names where its current inputs
(the threshold JSON and metadata) come from, role `derived-from`, not a validity boundary of
the scheme itself — the owner's 2026-09-29 review was explicit that the limitation is
climatic, not geographic, and Czechia is at most the extent of particular datasets or mapped
products. The Rasdaman collections are a data footprint, so their boundary is `spatial` and
its role is `can-run-on`: outside it there is simply nothing to read. Both are approximated
by Czechia's simplified country border and both are inferred rather than stated, which is
recorded on each constraint. Collapsing them into one would lose the fact that a target could
satisfy either without satisfying the other — an instance with the Czech scheme's inputs but
no Rasdaman coverage needs a datacube, not a new classification.

**The real validity constraint is prose, and is not Köppen-Geiger.** An earlier version tested
Question 7's assumption that "Quitt-inspired thresholds are meaningful for the target area"
against the same Köppen-Geiger class as the Quitt scheme's coverage. The owner's 2026-09-29
review rejected this: Köppen-Geiger was never intended as the transferability boundary, and
the real question is whether the range of climatic conditions the implemented Quitt classes
can distinguish still meaningfully represents the target area and period — a "classification
range" concept, not a class match. Recorded as prose for that reason. Cited by its own rule,
independent of `czech-zone-scheme`.

**The validation reference is the case that tests `mandatory: false` from the other side.**
FP-WF3's optional rule is a substitution you may skip; this one is a validation you may skip
only "where available", which is question 9's own qualification. Modelling it as an
`external-resource` with a non-mandatory rule states both halves: it is expected outside the
source region, and its absence degrades trust in the adapted zone boundaries rather than
blocking the run. Note the slight stretch, since the current workflow has no validation
artifact to replace — what is really being said is that an adapted classification needs a
local validation reference. The alternative was to declare it with no rule at all, which
states less and reads as an oversight.

No temporal constraint: question 4's "selected year or multi-year period" is a user-supplied
parameter with no stated bound, the same situation as FP-WF1 and FP-WF2. `steps` is omitted;
`inputs` ids are placeholders.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF5 — Map of climatic zones",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [{ "package": "python" }, { "package": "flask" }]
    },
    "NetworkAccess": { "networkAccess": true }
  },
  "inputs": {
    "climate_zone_thresholds": { "type": "File" },
    "climate_metadata": { "type": "File" },
    "climate_source_catalogue": { "type": "string" }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "czech-zone-scheme",
        "role": "derived-from",
        "dimension": "jurisdictional",
        "value": { "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))" },
        "transferabilityNotes": "The Quitt classification is the Czech national forest climate-zone scheme; question 9 says thresholds, labels and metadata 'should be adapted to local or national classification schemes'. Value is Czechia's country border, simplified, standing in for the current inputs' unstated extent. Previously typed `valid-for`; the owner's 2026-09-29 review was explicit this is not a validity boundary of the classification scheme, only (at most) the coverage of particular current datasets or mapped products, so the role is `derived-from`, matching FP-WF2's `czechia`. The real validity condition is `quitt-meaningful`. Extent still inferred and needs owner/technical confirmation."
      },
      {
        "id": "rasdaman-collections",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))" },
        "transferabilityNotes": "Where the current Rasdaman annual-indicator collections hold data. Same stand-in geometry (Czechia's simplified country border, for an extent the owner did not state) as `czech-zone-scheme` and a different fact: this one is about what can be read, that one about what the classification means. Question 9 says the registry and source catalogue 'would need to reference the target region'. Inferred extent; needs owner confirmation."
      },
      {
        "id": "quitt-meaningful",
        "role": "valid-for",
        "dimension": "climatic",
        "value": "the climatic conditions of the target area and period are adequately represented by the range of classes distinguished by the implemented Quitt classification — a classification-range judgement, not a match against Köppen-Geiger or any other external scheme",
        "transferabilityNotes": "Question 7's assumption that Quitt-inspired thresholds are meaningful for the target area. Earlier recorded as a same-class-as test against Köppen-Geiger; the owner's 2026-09-29 review rejected Köppen-Geiger as the transferability boundary outright. The real limitation is the range of climatic conditions the current Quitt classes can distinguish, which is climatic rather than geographic and already bites inside Czechia under warming (large areas collapsing into the warmest class). Recorded as prose, the same shape as FP-WF1's `ecological-range`."
      }
    ],
    "artifacts": [
      {
        "id": "quitt-limits",
        "artifact": "Quitt-limit JSON climate-zone threshold definitions (thresholds, labels, zone descriptions)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/climate_zone_thresholds"
      },
      {
        "id": "climate-metadata",
        "artifact": "climate metadata file (indicator definitions and descriptions)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/climate_metadata"
      },
      {
        "id": "rasdaman-registry",
        "artifact": "Rasdaman collection registry and climate source catalogue",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/climate_source_catalogue"
      },
      {
        "id": "validation-reference",
        "artifact": "local meteorological observations or accepted climate maps, for validating the adapted classification",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Not an input of the current workflow: question 9 recommends it as the way to check an adapted classification, so it enters the model only on transfer. Declared as an external resource with no pointer for that reason."
      }
    ],
    "rules": [
      {
        "appliesTo": ["quitt-limits", "climate-metadata"],
        "when": [{ "constraint": "czech-zone-scheme", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'Climate-zone thresholds, labels and metadata should be adapted to local or national classification schemes.' Thresholds and the metadata that describes them move together — adapting one without the other leaves the zone descriptions naming classes the thresholds no longer produce. Triggered by `czech-zone-scheme` (coverage of these particular inputs, `derived-from`), independent of `quitt-meaningful` (whether the classification range itself still applies) below — either alone can call for replacement."
      },
      {
        "appliesTo": ["quitt-limits"],
        "when": [{ "constraint": "quitt-meaningful", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "The second, independent trigger for the same substitution: question 7 assumes Quitt-inspired thresholds are meaningful for the target area, and a target inside Czechia's borders but outside the range of conditions the current classes distinguish fails that assumption without leaving the jurisdiction — the owner's 2026-09-29 review names this as already happening under warming projections. A separate rule rather than a second condition on the one above, because either alone suffices and `when` is conjunctive."
      },
      {
        "appliesTo": ["rasdaman-registry"],
        "when": [{ "constraint": "rasdaman-collections", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Question 9: the registry and source catalogue 'would need to reference the target region'. Question 8 accepts 'Rasdaman or equivalent annual climate-indicator data', so an equivalent datacube service satisfies this — the substitution is of the collections the catalogue points at, not necessarily of Rasdaman itself."
      },
      {
        "appliesTo": ["validation-reference"],
        "when": [{ "constraint": "czech-zone-scheme", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": false,
        "transferabilityNotes": "Question 9: 'Validation should use local meteorological observations or accepted climate maps where available.' Non-mandatory because the source qualifies it with 'where available'. Skipping it does not stop the workflow: it produces zone maps from thresholds that have been adapted but never checked against anything in the target area, so the classification should be treated as indicative and the fuzzy match scores not compared against those from the Czech setup."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational"
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF5 \u2014 Map of climatic zones",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python"
        },
        {
          "package": "flask"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "climate_zone_thresholds": {
      "type": "File"
    },
    "climate_metadata": {
      "type": "File"
    },
    "climate_source_catalogue": {
      "type": "string"
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "czech-zone-scheme",
        "role": "derived-from",
        "dimension": "jurisdictional",
        "value": {
          "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"
        },
        "transferabilityNotes": "The Quitt classification is the Czech national forest climate-zone scheme; question 9 says thresholds, labels and metadata 'should be adapted to local or national classification schemes'. Value is Czechia's country border, simplified, standing in for the current inputs' unstated extent. Previously typed `valid-for`; the owner's 2026-09-29 review was explicit this is not a validity boundary of the classification scheme, only (at most) the coverage of particular current datasets or mapped products, so the role is `derived-from`, matching FP-WF2's `czechia`. The real validity condition is `quitt-meaningful`. Extent still inferred and needs owner/technical confirmation."
      },
      {
        "id": "rasdaman-collections",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"
        },
        "transferabilityNotes": "Where the current Rasdaman annual-indicator collections hold data. Same stand-in geometry (Czechia's simplified country border, for an extent the owner did not state) as `czech-zone-scheme` and a different fact: this one is about what can be read, that one about what the classification means. Question 9 says the registry and source catalogue 'would need to reference the target region'. Inferred extent; needs owner confirmation."
      },
      {
        "id": "quitt-meaningful",
        "role": "valid-for",
        "dimension": "climatic",
        "value": "the climatic conditions of the target area and period are adequately represented by the range of classes distinguished by the implemented Quitt classification \u2014 a classification-range judgement, not a match against K\u00f6ppen-Geiger or any other external scheme",
        "transferabilityNotes": "Question 7's assumption that Quitt-inspired thresholds are meaningful for the target area. Earlier recorded as a same-class-as test against K\u00f6ppen-Geiger; the owner's 2026-09-29 review rejected K\u00f6ppen-Geiger as the transferability boundary outright. The real limitation is the range of climatic conditions the current Quitt classes can distinguish, which is climatic rather than geographic and already bites inside Czechia under warming (large areas collapsing into the warmest class). Recorded as prose, the same shape as FP-WF1's `ecological-range`."
      }
    ],
    "artifacts": [
      {
        "id": "quitt-limits",
        "artifact": "Quitt-limit JSON climate-zone threshold definitions (thresholds, labels, zone descriptions)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/climate_zone_thresholds"
      },
      {
        "id": "climate-metadata",
        "artifact": "climate metadata file (indicator definitions and descriptions)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/climate_metadata"
      },
      {
        "id": "rasdaman-registry",
        "artifact": "Rasdaman collection registry and climate source catalogue",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/climate_source_catalogue"
      },
      {
        "id": "validation-reference",
        "artifact": "local meteorological observations or accepted climate maps, for validating the adapted classification",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Not an input of the current workflow: question 9 recommends it as the way to check an adapted classification, so it enters the model only on transfer. Declared as an external resource with no pointer for that reason."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "quitt-limits",
          "climate-metadata"
        ],
        "when": [
          {
            "constraint": "czech-zone-scheme",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'Climate-zone thresholds, labels and metadata should be adapted to local or national classification schemes.' Thresholds and the metadata that describes them move together \u2014 adapting one without the other leaves the zone descriptions naming classes the thresholds no longer produce. Triggered by `czech-zone-scheme` (coverage of these particular inputs, `derived-from`), independent of `quitt-meaningful` (whether the classification range itself still applies) below \u2014 either alone can call for replacement."
      },
      {
        "appliesTo": [
          "quitt-limits"
        ],
        "when": [
          {
            "constraint": "quitt-meaningful",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "The second, independent trigger for the same substitution: question 7 assumes Quitt-inspired thresholds are meaningful for the target area, and a target inside Czechia's borders but outside the range of conditions the current classes distinguish fails that assumption without leaving the jurisdiction \u2014 the owner's 2026-09-29 review names this as already happening under warming projections. A separate rule rather than a second condition on the one above, because either alone suffices and `when` is conjunctive."
      },
      {
        "appliesTo": [
          "rasdaman-registry"
        ],
        "when": [
          {
            "constraint": "rasdaman-collections",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Question 9: the registry and source catalogue 'would need to reference the target region'. Question 8 accepts 'Rasdaman or equivalent annual climate-indicator data', so an equivalent datacube service satisfies this \u2014 the substitution is of the collections the catalogue points at, not necessarily of Rasdaman itself."
      },
      {
        "appliesTo": [
          "validation-reference"
        ],
        "when": [
          {
            "constraint": "czech-zone-scheme",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": false,
        "transferabilityNotes": "Question 9: 'Validation should use local meteorological observations or accepted climate maps where available.' Non-mandatory because the source qualifies it with 'where available'. Skipping it does not stop the workflow: it produces zone maps from thresholds that have been adapted but never checked against anything in the target area, so the classification should be treated as indicative and the fuzzy match scores not compared against those from the Czech setup."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational"
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns3: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/> a cwl:Workflow ;
    rdfs:label "FP-WF5 — Map of climatic zones" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_metadata>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_source_catalogue>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_zone_thresholds> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns1:packages [ ns2:package "flask" ],
                [ ns2:package "python" ] ],
        [ a cwl:NetworkAccess ;
            ns3:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate-metadata>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-registry>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/validation-reference> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/czech-zone-scheme>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-meaningful>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-collections> ;
            focal-transf-prop:rules [ rdfs:comment "The second, independent trigger for the same substitution: question 7 assumes Quitt-inspired thresholds are meaningful for the target area, and a target inside Czechia's borders but outside the range of conditions the current classes distinguish fails that assumption without leaving the jurisdiction — the owner's 2026-09-29 review names this as already happening under warming projections. A separate rule rather than a second condition on the one above, because either alone suffices and `when` is conjunctive." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-meaningful> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 9: 'Validation should use local meteorological observations or accepted climate maps where available.' Non-mandatory because the source qualifies it with 'where available'. Skipping it does not stop the workflow: it produces zone maps from thresholds that have been adapted but never checked against anything in the target area, so the classification should be treated as indicative and the fuzzy match scores not compared against those from the Czech setup." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/validation-reference> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/czech-zone-scheme> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 9: the registry and source catalogue 'would need to reference the target region'. Question 8 accepts 'Rasdaman or equivalent annual climate-indicator data', so an equivalent datacube service satisfies this — the substitution is of the collections the catalogue points at, not necessarily of Rasdaman itself." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-registry> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-collections> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 9: 'Climate-zone thresholds, labels and metadata should be adapted to local or national classification schemes.' Thresholds and the metadata that describes them move together — adapting one without the other leaves the zone descriptions naming classes the thresholds no longer produce. Triggered by `czech-zone-scheme` (coverage of these particular inputs, `derived-from`), independent of `quitt-meaningful` (whether the classification range itself still applies) below — either alone can call for replacement." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate-metadata>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/czech-zone-scheme> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_metadata> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_source_catalogue> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_zone_thresholds> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate-metadata> dcterms:title "climate metadata file (indicator definitions and descriptions)" ;
    focal-transf-prop:artifactRef "/inputs/climate_metadata" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-meaningful> rdfs:comment "Question 7's assumption that Quitt-inspired thresholds are meaningful for the target area. Earlier recorded as a same-class-as test against Köppen-Geiger; the owner's 2026-09-29 review rejected Köppen-Geiger as the transferability boundary outright. The real limitation is the range of climatic conditions the current Quitt classes can distinguish, which is climatic rather than geographic and already bites inside Czechia under warming (large areas collapsing into the warmest class). Recorded as prose, the same shape as FP-WF1's `ecological-range`." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "the climatic conditions of the target area and period are adequately represented by the range of classes distinguished by the implemented Quitt classification — a classification-range judgement, not a match against Köppen-Geiger or any other external scheme" .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-collections> rdfs:comment "Where the current Rasdaman annual-indicator collections hold data. Same stand-in geometry (Czechia's simplified country border, for an extent the owner did not state) as `czech-zone-scheme` and a different fact: this one is about what can be read, that one about what the classification means. Question 9 says the registry and source catalogue 'would need to reference the target region'. Inferred extent; needs owner confirmation." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-registry> dcterms:title "Rasdaman collection registry and climate source catalogue" ;
    focal-transf-prop:artifactRef "/inputs/climate_source_catalogue" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/validation-reference> dcterms:title "local meteorological observations or accepted climate maps, for validating the adapted classification" ;
    rdfs:comment "Not an input of the current workflow: question 9 recommends it as the way to check an adapted classification, so it enters the model only on transfer. Declared as an external resource with no pointer for that reason." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/czech-zone-scheme> rdfs:comment "The Quitt classification is the Czech national forest climate-zone scheme; question 9 says thresholds, labels and metadata 'should be adapted to local or national classification schemes'. Value is Czechia's country border, simplified, standing in for the current inputs' unstated extent. Previously typed `valid-for`; the owner's 2026-09-29 review was explicit this is not a validity boundary of the classification scheme, only (at most) the coverage of particular current datasets or mapped products, so the role is `derived-from`, matching FP-WF2's `czechia`. The real validity condition is `quitt-meaningful`. Extent still inferred and needs owner/technical confirmation." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/jurisdictional> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON ((18.16 49.26, 17.76 48.89, 17.14 48.84, 16.95 48.6, 16.54 48.8, 16.06 48.75, 14.99 49, 14.69 48.6, 14.19 48.58, 12.68 49.41, 12.39 49.74, 12.51 49.9, 12.09 50.3, 12.28 50.18, 12.55 50.39, 14.37 50.9, 14.28 51.03, 14.72 50.81, 14.99 51.01, 16.01 50.61, 16.36 50.62, 16.21 50.42, 16.64 50.1, 16.99 50.24, 16.88 50.43, 17.7 50.31, 17.63 50.12, 18.56 49.88, 18.83 49.51, 18.16 49.26))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits> dcterms:title "Quitt-limit JSON climate-zone threshold definitions (thresholds, labels, zone descriptions)" ;
    focal-transf-prop:artifactRef "/inputs/climate_zone_thresholds" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


```


### UP-WF3 — Urban blue-spot flood risk (the fullest contract, and the limits of the model)
The richest questionnaire in the corpus and the one this model was most recently extended
for: `acceptanceCriteria` and the `grid-structure` dimension both exist because of it. This is
their first use in a whole workflow, and it is also where the model's current edges show.

**The precipitation contract is what `replace-with-local-equivalent` was missing.** Question 9
says a replacement must carry the same variable name, be in mm or kg m⁻²s⁻¹, have a time axis,
and be on a regular lat/lon or rotated-pole grid. All four are on the artifact, not the rule,
because they hold whether or not anyone is transferring anything — a platform can check a
candidate file against them without knowing why it was offered.

**An unsupported grid is not a substitution problem.** Question 7 is categorical: "Other
projections are not handled." So the grid constraint is cited by a rule whose action is
`component-not-executable` and whose `affects` names the accumulation and detection steps —
we read "not handled" as: it does not run (for example on a Lambert-conformal grid), which the owner is asked to confirm. That is the
distinction the terminal action exists to draw, and this is a cleaner instance of it than
UP-WF2's, where a substitute might yet be found.

**Two threshold sets, one climatic trigger.** The 6-hour and 12-hour percentile thresholds
come from DWD station data for Germany, the 1-day and 7-day ones from E-OBS for Europe. Both
provenances are recorded as `derived-from` constraints rather than `trained-on`, since the
thresholds were computed, not fitted: this workflow trains nothing. The rule that fires is conditioned
on the climatic constraint, because that is what question 9 actually says: "for a region with
different climate regime, user should use a custom threshold". A target inside Germany with an
unlike climate is as much of a problem as one outside it.

**A support mismatch is a quality fact, not a portability one.** Question 7 states that the
vulnerability index is at NUTS3 level, "coarser than the precipitation grid and does not
align exactly with the AOI boundary". That is a relationship between the supports of two of
the workflow's own artifacts, so no envelope dimension holds it and no rule is conditioned on
it, and it holds in the source deployment as much as in any target. It belongs on the axis
that already exists for "this is `pre-operational` and you should still be careful": it is
carried by a second `qualityAnnotation` on the new `spatial-support-mismatch` dimension.

**What this example still cannot say, and does not pretend to.** Two evidenced facts from
this questionnaire have no home in the model as it stands, and each is recorded in
`transferabilityNotes` on the nearest thing to it rather than forced into a shape that would
misstate it:

1. *Exposure and vulnerability cannot be substituted at all.* Question 9: "If users want to
   use their own exposure or vulnerability data, since current workflow is no option for it."
   That is a standing property of the interface, not an outcome triggered by a target falling
   outside a boundary, and both `when` and `triggeredBy` assume a trigger.
   `component-not-executable` is the closest available term and is wrong: the overlay steps
   run perfectly well, on the built-in layers. So the two artifacts are declared and left
   ungoverned, with the limitation on each.
2. *The available accumulation windows depend on which precipitation source is used.* E-OBS is
   daily, so only 1-day and 7-day windows work with it; 6-hour and 12-hour need hourly NUKLEUS
   data. A co-constraint between two inputs, which is a CWL-level fact this profile does not
   reach into: CWL types an input as a union of record schemas, which is where a choice
   between "E-OBS plus a daily window" and "NUKLEUS plus a sub-daily one" belongs.

Both `qualityAnnotation` entries are directly evidenced, unlike FP-WF1's. Question 1 says in
its own words that these are not hydrological model results and that exposure and
vulnerability are contextual layers never combined into a risk score.

`maturityStatus: pre-operational` is the sharpest use of that middle term in the set — a
Python package on DKRZ's HPC system, "Container: none at this stage", recently shared for
integration testing. `inputs` and `steps` ids are placeholders invented so `artifactRef` and
`affects` resolve; they are not UP-WF3's real interface.

The questionnaire gives the Python requirement as "3.10+"; CWL's version list cannot say "and
later", so only the lower bound is recorded.

#### json
```json
{
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF3 — Urban blue-spot flood risk",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        { "package": "python", "version": ["3.10"] },
        { "package": "xarray" },
        { "package": "numpy" },
        { "package": "pandas" },
        { "package": "rasterio" }
      ]
    },
    "NetworkAccess": { "networkAccess": true }
  },
  "inputs": {
    "precipitation": { "type": "File" },
    "threshold_subdaily": { "type": "File" },
    "threshold_daily": { "type": "File" },
    "exposure_layers": { "type": "File" },
    "vulnerability_index": { "type": "File" }
  },
  "steps": {
    "accumulation": {
      "run": "#accumulation.cwl",
      "in": { "precipitation": "precipitation" },
      "out": ["accumulated_precipitation"]
    },
    "blue_spot_detection": {
      "run": "#blue_spot_detection.cwl",
      "in": { "accumulated": "accumulation/accumulated_precipitation", "threshold": "threshold_daily" },
      "out": ["blue_spot_map"]
    },
    "exposure_overlay": {
      "run": "#exposure_overlay.cwl",
      "in": { "blue_spots": "blue_spot_detection/blue_spot_map", "exposure": "exposure_layers" },
      "out": ["exposure_map"]
    },
    "vulnerability_overlay": {
      "run": "#vulnerability_overlay.cwl",
      "in": { "blue_spots": "blue_spot_detection/blue_spot_map", "vulnerability": "vulnerability_index" },
      "out": ["vulnerability_map"]
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "dwd-stations",
        "role": "derived-from",
        "dimension": "spatial",
        "value": { "asWKT": "MULTIPOLYGON (((8.57 47.78, 8.43 47.59, 7.57 47.61, 7.62 48.16, 8.13 48.97, 6.74 49.16, 6.34 49.45, 6.49 49.8, 6.11 50.09, 6.34 50.45, 5.86 51.03, 6.13 51.15, 6.2 51.45, 5.95 51.8, 6.74 51.91, 6.72 52.08, 7.02 52.27, 7 52.42, 6.69 52.53, 7.01 52.63, 7.18 52.97, 7.2 53.28, 7.05 53.38, 7.21 53.65, 8.01 53.69, 8.11 53.47, 8.33 53.61, 8.5 53.39, 8.62 53.88, 9.21 53.86, 9.59 53.6, 9.78 53.55, 9.31 53.86, 8.98 53.93, 8.91 54.26, 8.64 54.29, 8.96 54.54, 8.67 54.9, 9.62 54.86, 10.02 54.67, 9.87 54.47, 11.01 54.38, 11.01 54.18, 10.81 54.08, 10.92 54, 11.4 53.94, 12.58 54.47, 13.03 54.41, 13.45 54.14, 13.72 54.15, 13.87 53.85, 14.26 53.73, 14.41 53.2, 14.13 52.88, 14.62 52.53, 14.55 52.36, 14.75 52.08, 14.6 51.83, 14.72 51.52, 14.94 51.44, 14.96 51.1, 14.77 50.82, 14.32 51.04, 14.37 50.9, 12.94 50.41, 12.55 50.39, 12.28 50.18, 12.09 50.27, 12.51 49.9, 12.39 49.74, 12.63 49.46, 13.77 48.82, 13.79 48.59, 13.49 48.58, 13.37 48.36, 12.76 48.11, 13.05 47.66, 13.01 47.48, 12.21 47.72, 11.04 47.39, 10.44 47.55, 10.18 47.28, 9.97 47.51, 8.57 47.78)), ((13.36 54.25, 13.16 54.36, 13.18 54.54, 13.42 54.7, 13.71 54.38, 13.36 54.25)), ((13.93 53.88, 13.83 54.13, 14.04 54.03, 14.21 53.95, 13.93 53.88)), ((11.13 54.42, 11.01 54.47, 11.08 54.53, 11.28 54.42, 11.13 54.42)), ((8.41 55.06, 8.38 54.9, 8.63 54.89, 8.31 54.79, 8.41 55.06)), ((8.55 54.69, 8.4 54.71, 8.51 54.76, 8.55 54.69)))" },
        "transferabilityNotes": "Germany's country border, simplified to a few tens of kilometers, standing in for the DWD station network the 6-hour and 12-hour percentile thresholds were pre-computed from. A scattered set of stations, not a country, so this is an upper bound; and station networks are dense in some regions and sparse in others, which a border cannot show at all."
      },
      {
        "id": "eobs-extent",
        "role": "derived-from",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))" },
        "transferabilityNotes": "The E-OBS domain's published approximate extent (about 25W-45E, 25N-71.5N), from which the 1-day and 7-day percentile thresholds were pre-computed. E-OBS is distributed on a regular rectangular latitude/longitude grid, so a rectangle is the right shape for its extent; its actual land coverage is coarser than that and station density is not uniform."
      },
      {
        "id": "threshold-climate-regime",
        "role": "valid-for",
        "dimension": "climatic",
        "value": "the German and European climate regime the pre-computed percentile thresholds were derived from",
        "transferabilityNotes": "Question 9, near-verbatim: 'for a region with different climate regime, user should use a custom threshold'. Prose rather than an extent, because climatic similarity is the judgement being made and no geometry settles it. This is the constraint the threshold rule is conditioned on, rather than the two spatial provenances above: a target inside Germany whose climate is unlike the stations' is as much of a problem as one outside it."
      },
      {
        "id": "eu-input-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": { "asWKT": "MULTIPOLYGON (((-8.79 39.08, -9.48 38.8, -8.66 41.03, -9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.89 56.36, 9.45 55.04, 10.92 54, 12.58 54.47, 13.72 54.15, 13.95 53.8, 14.58 53.64, 13.83 54.13, 18.09 54.84, 22.73 54.35, 22.57 55.06, 21.2 55.34, 21.46 57.32, 24.28 57.17, 24.53 58.35, 23.43 58.92, 24.38 59.47, 28.15 59.37, 27.35 57.53, 28.15 56.14, 26.59 55.67, 25.75 54.16, 23.48 53.94, 23.92 52.77, 23.18 52.29, 24.09 50.53, 22.13 48.41, 24.89 47.72, 26.9 48.21, 28.24 46.64, 28.21 45.45, 29.71 45.26, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.02 38.14, 22.73 37.54, 23.16 36.45, 21.12 37.89, 23.15 38.18, 21.18 38.35, 20 39.71, 20.96 40.85, 22.93 41.36, 22.34 42.31, 22.73 44.57, 19.61 46.17, 18.84 45.84, 19.01 44.87, 15.79 45.18, 17.59 42.94, 15.99 43.52, 14.55 45.3, 13.86 44.84, 13.63 45.77, 12.27 45.45, 12.4 44.22, 14.18 42.51, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.74 37.07, -8.79 39.08)), ((-7.85 54.22, -6.18 54.05, -6.32 52.25, -10.12 51.6, -9.6 51.87, -10.36 52.21, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -9.58 53.81, -10.09 54.22, -6.96 55.24, -7.85 54.22)), ((12.88 61.35, 12.16 61.72, 12.18 63.6, 14.06 64.1, 13.65 64.58, 14.54 66.13, 16.78 67.9, 21.27 69.27, 24.94 68.59, 26.53 69.92, 29.33 69.47, 28.41 68.9, 29.99 67.67, 29.07 66.89, 30.09 65.79, 29.6 64.97, 30.53 64.08, 29.99 63.74, 31.54 62.92, 29.25 61.29, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.38 62.46, 17.25 60.7, 18.99 59.83, 16.21 58.64, 16.92 58.49, 15.92 56.17, 12.89 55.41, 12.88 56.62, 11.25 58.37, 12.88 61.35)))" },
        "transferabilityNotes": "Question 9: 'All input datasets are covering EU.' Approximated by the EU as a coarse union of the 27 member countries (Natural Earth, public domain, simplified) within a European window, so overseas territories are excluded and small islands such as Malta and Cyprus are dropped. Deliberately coarse and known to be too generous: this is really the intersection of E-OBS, the NUKLEUS EUR-11 domain, the Local Climate Zone, imperviousness and population layers, and a NUTS3 vulnerability index that stops at the EU's borders, and the individual footprints were not stated. Needs owner confirmation before it is relied on."
      },
      {
        "id": "supported-grids",
        "role": "can-run-on",
        "dimension": "grid-structure",
        "value": { "gridTypes": ["regular-latlon", "rotated-pole"] },
        "transferabilityNotes": "Question 7: 'Two grid types are supported: regular latitude/longitude and rotated pole. Other projections are not handled.' A hard interface limit over a small enumerable set, and the most mechanically checkable constraint in this envelope: the terms carry the CF-conventions grid_mapping_name as their notation, which gridded datasets declare directly."
      }
    ],
    "artifacts": [
      {
        "id": "precipitation",
        "artifact": "precipitation input dataset (E-OBS or the NUKLEUS regional climate ensemble, read from the FOCAL STAC catalogue)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/precipitation",
        "acceptanceCriteria": {
          "variable": { "sameAsCurrent": true },
          "units": ["MilliM", "KiloGM-PER-M2-SEC"],
          "axes": ["time"],
          "gridTypes": ["regular-latlon", "rotated-pole"],
          "transferabilityNotes": "Question 9 states the fullest replacement contract in the corpus: 'The precipitation dataset must provide same precipitation variable name as current dataset, its unit (mm or flux (kg m-2 s-1)), a time axis, and the grid or projection must be either regular lat/lon or rotated pole.' The variable requirement is recorded as the relation the source states rather than as a literal: it says the replacement must match the current dataset, not what the current dataset is called. An earlier draft guessed `rr`, which is E-OBS's name and wrong for the CORDEX path where the same field is `pr` — the guess was needed only because the schema wanted a literal where the source gave a relation. One further requirement still resists this shape: the source's temporal resolution gates which accumulation windows are available, which is a constraint between two inputs rather than a property of this one."
        }
      },
      {
        "id": "threshold-subdaily",
        "artifact": "pre-computed 95th/99th percentile thresholds for the 6-hour and 12-hour accumulation windows (DWD station data, Germany)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/threshold_subdaily"
      },
      {
        "id": "threshold-daily",
        "artifact": "pre-computed 95th/99th percentile thresholds for the 1-day and 7-day accumulation windows (E-OBS, Europe)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/threshold_daily"
      },
      {
        "id": "focal-stac-loader",
        "artifact": "FOCAL STAC data loader, built into the workflow",
        "artifactRole": "infrastructure",
        "transferabilityNotes": "Question 10 names this as the part that is still specific to the current infrastructure: 'all the required data is from FOCAL collection and data loader are built into the workflow. So, using this workflow outside with different dataset requires replacing that part.' Classified as infrastructure rather than a workflow input because it is a code path, not a dataset, and has nothing in an Application Package to point at."
      },
      {
        "id": "exposure",
        "artifact": "exposure layers (Local Climate Zones, imperviousness, population)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/exposure_layers",
        "transferabilityNotes": "Contextual overlay: Question 4 is explicit that exposure does not enter the calculation, and Question 9 says that if users want their own exposure or vulnerability data, 'current workflow is no option for it'. Not substitutable, then, which this model cannot yet state (see the statement-level note). Question 9 also says 'All input datasets are covering EU', so the overlay cannot be produced outside the EU: recorded as an optional terminal rule on `eu-input-coverage`, our inference from those two answers, to be confirmed with the owner."
      },
      {
        "id": "vulnerability",
        "artifact": "vulnerability index at NUTS3 level (Risk Data Hub)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/vulnerability_index",
        "transferabilityNotes": "Contextual overlay, and not substitutable, for the same reason recorded on `exposure`, with the same optional rule outside the EU. Question 7 also states the index is at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary', which is carried by the `spatial-support-mismatch` qualityAnnotation. Question 8: the index data is 'currently local files, until it is published on the FOCAL STAC'."
      }
    ],
    "rules": [
      {
        "appliesTo": ["threshold-subdaily", "threshold-daily"],
        "when": [{ "constraint": "threshold-climate-regime", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'the percentile thresholds were calculated for Germany(6h,12h)/Europe(1d,7d). So, for a region with different climate regime, user should use a custom threshold.' Question 4 confirms the workflow already accepts one: 'a user-defined threshold can be given', so this substitution needs no code change, only a value the user has to derive from local data."
      },
      {
        "appliesTo": ["precipitation"],
        "when": [{ "constraint": "eu-input-coverage", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Outside the coverage of the bundled sources a local precipitation dataset has to be supplied, and it must satisfy this artifact's acceptance criteria: same variable name, mm or kg m-2 s-1, a time axis, and one of the two supported grids."
      },
      {
        "appliesTo": ["precipitation"],
        "when": [{ "constraint": "supported-grids", "test": "outside" }],
        "actions": ["component-not-executable"],
        "affects": ["/steps/accumulation", "/steps/blue_spot_detection"],
        "mandatory": true,
        "transferabilityNotes": "Question 7: 'Other projections are not handled.' Our reading of 'not handled' (to be confirmed with the owner): terminal rather than a substitution — a dataset on a Lambert-conformal or polar-stereographic grid does not produce worse blue spots, it produces none, because the rolling accumulation has no code path for it. Regridding to a supported grid is a preprocessing step outside this workflow, not an action it offers."
      },
      {
        "appliesTo": ["focal-stac-loader"],
        "triggeredBy": "different-dataset",
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'Since all the data is loaded from FOCAL STAC, user need a new data loader.' Stated with `triggeredBy` rather than a cited constraint because the condition is that the data comes from somewhere other than the FOCAL STAC catalogue, which is a fact about the source rather than about where the target is: a user inside the EU with their own local precipitation archive needs the new loader just as much as one outside it."
      },
      {
        "appliesTo": ["exposure", "vulnerability"],
        "when": [{ "constraint": "eu-input-coverage", "test": "outside" }],
        "actions": ["component-not-executable"],
        "affects": ["/steps/exposure_overlay", "/steps/vulnerability_overlay"],
        "mandatory": false,
        "transferabilityNotes": "Our inference, to be confirmed: Question 9 says 'All input datasets are covering EU' and that users cannot supply their own exposure or vulnerability data, so outside the EU the overlays cannot be produced. Optional because no single sentence of the owner states it: the blue-spot map itself does not depend on the overlays (Question 4), so their absence costs the context layers, not the result."
      }
    ],
    "transferabilityNotes": "Two evidenced facts from this questionnaire are recorded in notes rather than in structure, because no shape in this model holds them without misstating them: that exposure and vulnerability cannot be substituted at all (a standing limitation, not a triggered outcome); and that the choice of precipitation source gates which accumulation windows are available (a co-constraint between two CWL inputs, which CWL's own union-of-record-schemas typing is the right place for). Each is on the artifact it concerns. The NUTS3 support mismatch, previously a third note here, is now carried structurally by a `spatial-support-mismatch` qualityAnnotation."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "Question 1: 'The Blue Spot is an indicator of potentially flood-prone areas'. The workflow does not provide the result of a hydrological or hydraulic model simulation, and exposure and vulnerability, provided as contextual layers, 'are not combined into a single quantitative risk score'. Read together, results support a qualitative judgement about where urban flood risk is likely to be highest (the owner's stated purpose); they are not a risk assessment (our reading of the caveat)."
    },
    {
      "dimension": "spatial-support-mismatch",
      "note": "Question 7: the vulnerability index is provided at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. The overlay can therefore be read no finer than a NUTS3 region, whatever resolution the blue-spot map itself carries, and NUTS3 units straddling the AOI edge are only partly covered. This holds in the source deployment as much as in any target: it bounds how far a result can be read, not whether the workflow moves."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF3 \u2014 Urban blue-spot flood risk",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python",
          "version": [
            "3.10"
          ]
        },
        {
          "package": "xarray"
        },
        {
          "package": "numpy"
        },
        {
          "package": "pandas"
        },
        {
          "package": "rasterio"
        }
      ]
    },
    "NetworkAccess": {
      "networkAccess": true
    }
  },
  "inputs": {
    "precipitation": {
      "type": "File"
    },
    "threshold_subdaily": {
      "type": "File"
    },
    "threshold_daily": {
      "type": "File"
    },
    "exposure_layers": {
      "type": "File"
    },
    "vulnerability_index": {
      "type": "File"
    }
  },
  "steps": {
    "accumulation": {
      "run": "#accumulation.cwl",
      "in": {
        "precipitation": "precipitation"
      },
      "out": [
        "accumulated_precipitation"
      ]
    },
    "blue_spot_detection": {
      "run": "#blue_spot_detection.cwl",
      "in": {
        "accumulated": "accumulation/accumulated_precipitation",
        "threshold": "threshold_daily"
      },
      "out": [
        "blue_spot_map"
      ]
    },
    "exposure_overlay": {
      "run": "#exposure_overlay.cwl",
      "in": {
        "blue_spots": "blue_spot_detection/blue_spot_map",
        "exposure": "exposure_layers"
      },
      "out": [
        "exposure_map"
      ]
    },
    "vulnerability_overlay": {
      "run": "#vulnerability_overlay.cwl",
      "in": {
        "blue_spots": "blue_spot_detection/blue_spot_map",
        "vulnerability": "vulnerability_index"
      },
      "out": [
        "vulnerability_map"
      ]
    }
  },
  "transferability": {
    "trainingRequired": false,
    "envelope": [
      {
        "id": "dwd-stations",
        "role": "derived-from",
        "dimension": "spatial",
        "value": {
          "asWKT": "MULTIPOLYGON (((8.57 47.78, 8.43 47.59, 7.57 47.61, 7.62 48.16, 8.13 48.97, 6.74 49.16, 6.34 49.45, 6.49 49.8, 6.11 50.09, 6.34 50.45, 5.86 51.03, 6.13 51.15, 6.2 51.45, 5.95 51.8, 6.74 51.91, 6.72 52.08, 7.02 52.27, 7 52.42, 6.69 52.53, 7.01 52.63, 7.18 52.97, 7.2 53.28, 7.05 53.38, 7.21 53.65, 8.01 53.69, 8.11 53.47, 8.33 53.61, 8.5 53.39, 8.62 53.88, 9.21 53.86, 9.59 53.6, 9.78 53.55, 9.31 53.86, 8.98 53.93, 8.91 54.26, 8.64 54.29, 8.96 54.54, 8.67 54.9, 9.62 54.86, 10.02 54.67, 9.87 54.47, 11.01 54.38, 11.01 54.18, 10.81 54.08, 10.92 54, 11.4 53.94, 12.58 54.47, 13.03 54.41, 13.45 54.14, 13.72 54.15, 13.87 53.85, 14.26 53.73, 14.41 53.2, 14.13 52.88, 14.62 52.53, 14.55 52.36, 14.75 52.08, 14.6 51.83, 14.72 51.52, 14.94 51.44, 14.96 51.1, 14.77 50.82, 14.32 51.04, 14.37 50.9, 12.94 50.41, 12.55 50.39, 12.28 50.18, 12.09 50.27, 12.51 49.9, 12.39 49.74, 12.63 49.46, 13.77 48.82, 13.79 48.59, 13.49 48.58, 13.37 48.36, 12.76 48.11, 13.05 47.66, 13.01 47.48, 12.21 47.72, 11.04 47.39, 10.44 47.55, 10.18 47.28, 9.97 47.51, 8.57 47.78)), ((13.36 54.25, 13.16 54.36, 13.18 54.54, 13.42 54.7, 13.71 54.38, 13.36 54.25)), ((13.93 53.88, 13.83 54.13, 14.04 54.03, 14.21 53.95, 13.93 53.88)), ((11.13 54.42, 11.01 54.47, 11.08 54.53, 11.28 54.42, 11.13 54.42)), ((8.41 55.06, 8.38 54.9, 8.63 54.89, 8.31 54.79, 8.41 55.06)), ((8.55 54.69, 8.4 54.71, 8.51 54.76, 8.55 54.69)))"
        },
        "transferabilityNotes": "Germany's country border, simplified to a few tens of kilometers, standing in for the DWD station network the 6-hour and 12-hour percentile thresholds were pre-computed from. A scattered set of stations, not a country, so this is an upper bound; and station networks are dense in some regions and sparse in others, which a border cannot show at all."
      },
      {
        "id": "eobs-extent",
        "role": "derived-from",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"
        },
        "transferabilityNotes": "The E-OBS domain's published approximate extent (about 25W-45E, 25N-71.5N), from which the 1-day and 7-day percentile thresholds were pre-computed. E-OBS is distributed on a regular rectangular latitude/longitude grid, so a rectangle is the right shape for its extent; its actual land coverage is coarser than that and station density is not uniform."
      },
      {
        "id": "threshold-climate-regime",
        "role": "valid-for",
        "dimension": "climatic",
        "value": "the German and European climate regime the pre-computed percentile thresholds were derived from",
        "transferabilityNotes": "Question 9, near-verbatim: 'for a region with different climate regime, user should use a custom threshold'. Prose rather than an extent, because climatic similarity is the judgement being made and no geometry settles it. This is the constraint the threshold rule is conditioned on, rather than the two spatial provenances above: a target inside Germany whose climate is unlike the stations' is as much of a problem as one outside it."
      },
      {
        "id": "eu-input-coverage",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "MULTIPOLYGON (((-8.79 39.08, -9.48 38.8, -8.66 41.03, -9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.89 56.36, 9.45 55.04, 10.92 54, 12.58 54.47, 13.72 54.15, 13.95 53.8, 14.58 53.64, 13.83 54.13, 18.09 54.84, 22.73 54.35, 22.57 55.06, 21.2 55.34, 21.46 57.32, 24.28 57.17, 24.53 58.35, 23.43 58.92, 24.38 59.47, 28.15 59.37, 27.35 57.53, 28.15 56.14, 26.59 55.67, 25.75 54.16, 23.48 53.94, 23.92 52.77, 23.18 52.29, 24.09 50.53, 22.13 48.41, 24.89 47.72, 26.9 48.21, 28.24 46.64, 28.21 45.45, 29.71 45.26, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.02 38.14, 22.73 37.54, 23.16 36.45, 21.12 37.89, 23.15 38.18, 21.18 38.35, 20 39.71, 20.96 40.85, 22.93 41.36, 22.34 42.31, 22.73 44.57, 19.61 46.17, 18.84 45.84, 19.01 44.87, 15.79 45.18, 17.59 42.94, 15.99 43.52, 14.55 45.3, 13.86 44.84, 13.63 45.77, 12.27 45.45, 12.4 44.22, 14.18 42.51, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.74 37.07, -8.79 39.08)), ((-7.85 54.22, -6.18 54.05, -6.32 52.25, -10.12 51.6, -9.6 51.87, -10.36 52.21, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -9.58 53.81, -10.09 54.22, -6.96 55.24, -7.85 54.22)), ((12.88 61.35, 12.16 61.72, 12.18 63.6, 14.06 64.1, 13.65 64.58, 14.54 66.13, 16.78 67.9, 21.27 69.27, 24.94 68.59, 26.53 69.92, 29.33 69.47, 28.41 68.9, 29.99 67.67, 29.07 66.89, 30.09 65.79, 29.6 64.97, 30.53 64.08, 29.99 63.74, 31.54 62.92, 29.25 61.29, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.38 62.46, 17.25 60.7, 18.99 59.83, 16.21 58.64, 16.92 58.49, 15.92 56.17, 12.89 55.41, 12.88 56.62, 11.25 58.37, 12.88 61.35)))"
        },
        "transferabilityNotes": "Question 9: 'All input datasets are covering EU.' Approximated by the EU as a coarse union of the 27 member countries (Natural Earth, public domain, simplified) within a European window, so overseas territories are excluded and small islands such as Malta and Cyprus are dropped. Deliberately coarse and known to be too generous: this is really the intersection of E-OBS, the NUKLEUS EUR-11 domain, the Local Climate Zone, imperviousness and population layers, and a NUTS3 vulnerability index that stops at the EU's borders, and the individual footprints were not stated. Needs owner confirmation before it is relied on."
      },
      {
        "id": "supported-grids",
        "role": "can-run-on",
        "dimension": "grid-structure",
        "value": {
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ]
        },
        "transferabilityNotes": "Question 7: 'Two grid types are supported: regular latitude/longitude and rotated pole. Other projections are not handled.' A hard interface limit over a small enumerable set, and the most mechanically checkable constraint in this envelope: the terms carry the CF-conventions grid_mapping_name as their notation, which gridded datasets declare directly."
      }
    ],
    "artifacts": [
      {
        "id": "precipitation",
        "artifact": "precipitation input dataset (E-OBS or the NUKLEUS regional climate ensemble, read from the FOCAL STAC catalogue)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/precipitation",
        "acceptanceCriteria": {
          "variable": {
            "sameAsCurrent": true
          },
          "units": [
            "MilliM",
            "KiloGM-PER-M2-SEC"
          ],
          "axes": [
            "time"
          ],
          "gridTypes": [
            "regular-latlon",
            "rotated-pole"
          ],
          "transferabilityNotes": "Question 9 states the fullest replacement contract in the corpus: 'The precipitation dataset must provide same precipitation variable name as current dataset, its unit (mm or flux (kg m-2 s-1)), a time axis, and the grid or projection must be either regular lat/lon or rotated pole.' The variable requirement is recorded as the relation the source states rather than as a literal: it says the replacement must match the current dataset, not what the current dataset is called. An earlier draft guessed `rr`, which is E-OBS's name and wrong for the CORDEX path where the same field is `pr` \u2014 the guess was needed only because the schema wanted a literal where the source gave a relation. One further requirement still resists this shape: the source's temporal resolution gates which accumulation windows are available, which is a constraint between two inputs rather than a property of this one."
        }
      },
      {
        "id": "threshold-subdaily",
        "artifact": "pre-computed 95th/99th percentile thresholds for the 6-hour and 12-hour accumulation windows (DWD station data, Germany)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/threshold_subdaily"
      },
      {
        "id": "threshold-daily",
        "artifact": "pre-computed 95th/99th percentile thresholds for the 1-day and 7-day accumulation windows (E-OBS, Europe)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/threshold_daily"
      },
      {
        "id": "focal-stac-loader",
        "artifact": "FOCAL STAC data loader, built into the workflow",
        "artifactRole": "infrastructure",
        "transferabilityNotes": "Question 10 names this as the part that is still specific to the current infrastructure: 'all the required data is from FOCAL collection and data loader are built into the workflow. So, using this workflow outside with different dataset requires replacing that part.' Classified as infrastructure rather than a workflow input because it is a code path, not a dataset, and has nothing in an Application Package to point at."
      },
      {
        "id": "exposure",
        "artifact": "exposure layers (Local Climate Zones, imperviousness, population)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/exposure_layers",
        "transferabilityNotes": "Contextual overlay: Question 4 is explicit that exposure does not enter the calculation, and Question 9 says that if users want their own exposure or vulnerability data, 'current workflow is no option for it'. Not substitutable, then, which this model cannot yet state (see the statement-level note). Question 9 also says 'All input datasets are covering EU', so the overlay cannot be produced outside the EU: recorded as an optional terminal rule on `eu-input-coverage`, our inference from those two answers, to be confirmed with the owner."
      },
      {
        "id": "vulnerability",
        "artifact": "vulnerability index at NUTS3 level (Risk Data Hub)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/vulnerability_index",
        "transferabilityNotes": "Contextual overlay, and not substitutable, for the same reason recorded on `exposure`, with the same optional rule outside the EU. Question 7 also states the index is at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary', which is carried by the `spatial-support-mismatch` qualityAnnotation. Question 8: the index data is 'currently local files, until it is published on the FOCAL STAC'."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "threshold-subdaily",
          "threshold-daily"
        ],
        "when": [
          {
            "constraint": "threshold-climate-regime",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'the percentile thresholds were calculated for Germany(6h,12h)/Europe(1d,7d). So, for a region with different climate regime, user should use a custom threshold.' Question 4 confirms the workflow already accepts one: 'a user-defined threshold can be given', so this substitution needs no code change, only a value the user has to derive from local data."
      },
      {
        "appliesTo": [
          "precipitation"
        ],
        "when": [
          {
            "constraint": "eu-input-coverage",
            "test": "outside"
          }
        ],
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Outside the coverage of the bundled sources a local precipitation dataset has to be supplied, and it must satisfy this artifact's acceptance criteria: same variable name, mm or kg m-2 s-1, a time axis, and one of the two supported grids."
      },
      {
        "appliesTo": [
          "precipitation"
        ],
        "when": [
          {
            "constraint": "supported-grids",
            "test": "outside"
          }
        ],
        "actions": [
          "component-not-executable"
        ],
        "affects": [
          "/steps/accumulation",
          "/steps/blue_spot_detection"
        ],
        "mandatory": true,
        "transferabilityNotes": "Question 7: 'Other projections are not handled.' Our reading of 'not handled' (to be confirmed with the owner): terminal rather than a substitution \u2014 a dataset on a Lambert-conformal or polar-stereographic grid does not produce worse blue spots, it produces none, because the rolling accumulation has no code path for it. Regridding to a supported grid is a preprocessing step outside this workflow, not an action it offers."
      },
      {
        "appliesTo": [
          "focal-stac-loader"
        ],
        "triggeredBy": "different-dataset",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'Since all the data is loaded from FOCAL STAC, user need a new data loader.' Stated with `triggeredBy` rather than a cited constraint because the condition is that the data comes from somewhere other than the FOCAL STAC catalogue, which is a fact about the source rather than about where the target is: a user inside the EU with their own local precipitation archive needs the new loader just as much as one outside it."
      },
      {
        "appliesTo": [
          "exposure",
          "vulnerability"
        ],
        "when": [
          {
            "constraint": "eu-input-coverage",
            "test": "outside"
          }
        ],
        "actions": [
          "component-not-executable"
        ],
        "affects": [
          "/steps/exposure_overlay",
          "/steps/vulnerability_overlay"
        ],
        "mandatory": false,
        "transferabilityNotes": "Our inference, to be confirmed: Question 9 says 'All input datasets are covering EU' and that users cannot supply their own exposure or vulnerability data, so outside the EU the overlays cannot be produced. Optional because no single sentence of the owner states it: the blue-spot map itself does not depend on the overlays (Question 4), so their absence costs the context layers, not the result."
      }
    ],
    "transferabilityNotes": "Two evidenced facts from this questionnaire are recorded in notes rather than in structure, because no shape in this model holds them without misstating them: that exposure and vulnerability cannot be substituted at all (a standing limitation, not a triggered outcome); and that the choice of precipitation source gates which accumulation windows are available (a co-constraint between two CWL inputs, which CWL's own union-of-record-schemas typing is the right place for). Each is on the artifact it concerns. The NUTS3 support mismatch, previously a third note here, is now carried structurally by a `spatial-support-mismatch` qualityAnnotation."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "Question 1: 'The Blue Spot is an indicator of potentially flood-prone areas'. The workflow does not provide the result of a hydrological or hydraulic model simulation, and exposure and vulnerability, provided as contextual layers, 'are not combined into a single quantitative risk score'. Read together, results support a qualitative judgement about where urban flood risk is likely to be highest (the owner's stated purpose); they are not a risk assessment (our reading of the caveat)."
    },
    {
      "dimension": "spatial-support-mismatch",
      "note": "Question 7: the vulnerability index is provided at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. The overlay can therefore be read no finer than a NUTS3 region, whatever resolution the blue-spot map itself carries, and NUTS3 units straddling the AOI edge are only partly covered. This holds in the source deployment as much as in any target: it bounds how far a result can be read, not whether the workflow moves."
    }
  ]
}
```

#### ttl
```ttl
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#Workflow/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns3: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns4: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/> a cwl:Workflow ;
    rdfs:label "UP-WF3 — Urban blue-spot flood risk" ;
    ns1:steps <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/accumulation>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/blue_spot_detection>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_overlay>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_overlay> ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_layers>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_daily>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_subdaily>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_index> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns3:packages [ ns2:package "rasterio" ],
                [ ns2:package "pandas" ],
                [ ns2:package "python" ;
                    ns2:version "3.10" ],
                [ ns2:package "xarray" ],
                [ ns2:package "numpy" ] ],
        [ a cwl:NetworkAccess ;
            ns4:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/pre-operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/spatial-support-mismatch> ;
            focal-transf-prop:note "Question 7: the vulnerability index is provided at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. The overlay can therefore be read no finer than a NUTS3 region, whatever resolution the blue-spot map itself carries, and NUTS3 units straddling the AOI edge are only partly covered. This holds in the source deployment as much as in any target: it bounds how far a result can be read, not whether the workflow moves." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/decision-support-only> ;
            focal-transf-prop:note "Question 1: 'The Blue Spot is an indicator of potentially flood-prone areas'. The workflow does not provide the result of a hydrological or hydraulic model simulation, and exposure and vulnerability, provided as contextual layers, 'are not combined into a single quantitative risk score'. Read together, results support a qualitative judgement about where urban flood risk is likely to be highest (the owner's stated purpose); they are not a risk assessment (our reading of the caveat)." ] ;
    focal-transf-prop:transferability [ rdfs:comment "Two evidenced facts from this questionnaire are recorded in notes rather than in structure, because no shape in this model holds them without misstating them: that exposure and vulnerability cannot be substituted at all (a standing limitation, not a triggered outcome); and that the choice of precipitation source gates which accumulation windows are available (a co-constraint between two CWL inputs, which CWL's own union-of-record-schemas typing is the right place for). Each is on the artifact it concerns. The NUTS3 support mismatch, previously a third note here, is now carried structurally by a `spatial-support-mismatch` qualityAnnotation." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/focal-stac-loader>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-daily>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-subdaily>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/dwd-stations>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-extent>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eu-input-coverage>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/supported-grids>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-climate-regime> ;
            focal-transf-prop:rules [ rdfs:comment "Question 9: 'Since all the data is loaded from FOCAL STAC, user need a new data loader.' Stated with `triggeredBy` rather than a cited constraint because the condition is that the data comes from somewhere other than the FOCAL STAC catalogue, which is a fact about the source rather than about where the target is: a user inside the EU with their own local precipitation archive needs the new loader just as much as one outside it." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/focal-stac-loader> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-dataset> ],
                [ rdfs:comment "Outside the coverage of the bundled sources a local precipitation dataset has to be supplied, and it must satisfy this artifact's acceptance criteria: same variable name, mm or kg m-2 s-1, a time axis, and one of the two supported grids." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eu-input-coverage> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 7: 'Other projections are not handled.' Our reading of 'not handled' (to be confirmed with the owner): terminal rather than a substitution — a dataset on a Lambert-conformal or polar-stereographic grid does not produce worse blue spots, it produces none, because the rolling accumulation has no code path for it. Regridding to a supported grid is a preprocessing step outside this workflow, not an action it offers." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable> ;
                    focal-transf-prop:affects "/steps/accumulation",
                        "/steps/blue_spot_detection" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/supported-grids> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 9: 'the percentile thresholds were calculated for Germany(6h,12h)/Europe(1d,7d). So, for a region with different climate regime, user should use a custom threshold.' Question 4 confirms the workflow already accepts one: 'a user-defined threshold can be given', so this substitution needs no code change, only a value the user has to derive from local data." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-daily>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-subdaily> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-climate-regime> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Our inference, to be confirmed: Question 9 says 'All input datasets are covering EU' and that users cannot supply their own exposure or vulnerability data, so outside the EU the overlays cannot be produced. Optional because no single sentence of the owner states it: the blue-spot map itself does not depend on the overlays (Question 4), so their absence costs the context layers, not the result." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable> ;
                    focal-transf-prop:affects "/steps/exposure_overlay",
                        "/steps/vulnerability_overlay" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eu-input-coverage> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/accumulation> cwl:in "precipitation" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/accumulated_precipitation> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#accumulation.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/blue_spot_detection> cwl:in "accumulation/accumulated_precipitation",
        "threshold_daily" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/blue_spot_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#blue_spot_detection.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/dwd-stations> rdfs:comment "Germany's country border, simplified to a few tens of kilometers, standing in for the DWD station network the 6-hour and 12-hour percentile thresholds were pre-computed from. A scattered set of stations, not a country, so this is an upper bound; and station networks are dense in some regions and sparse in others, which a border cannot show at all." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "MULTIPOLYGON (((8.57 47.78, 8.43 47.59, 7.57 47.61, 7.62 48.16, 8.13 48.97, 6.74 49.16, 6.34 49.45, 6.49 49.8, 6.11 50.09, 6.34 50.45, 5.86 51.03, 6.13 51.15, 6.2 51.45, 5.95 51.8, 6.74 51.91, 6.72 52.08, 7.02 52.27, 7 52.42, 6.69 52.53, 7.01 52.63, 7.18 52.97, 7.2 53.28, 7.05 53.38, 7.21 53.65, 8.01 53.69, 8.11 53.47, 8.33 53.61, 8.5 53.39, 8.62 53.88, 9.21 53.86, 9.59 53.6, 9.78 53.55, 9.31 53.86, 8.98 53.93, 8.91 54.26, 8.64 54.29, 8.96 54.54, 8.67 54.9, 9.62 54.86, 10.02 54.67, 9.87 54.47, 11.01 54.38, 11.01 54.18, 10.81 54.08, 10.92 54, 11.4 53.94, 12.58 54.47, 13.03 54.41, 13.45 54.14, 13.72 54.15, 13.87 53.85, 14.26 53.73, 14.41 53.2, 14.13 52.88, 14.62 52.53, 14.55 52.36, 14.75 52.08, 14.6 51.83, 14.72 51.52, 14.94 51.44, 14.96 51.1, 14.77 50.82, 14.32 51.04, 14.37 50.9, 12.94 50.41, 12.55 50.39, 12.28 50.18, 12.09 50.27, 12.51 49.9, 12.39 49.74, 12.63 49.46, 13.77 48.82, 13.79 48.59, 13.49 48.58, 13.37 48.36, 12.76 48.11, 13.05 47.66, 13.01 47.48, 12.21 47.72, 11.04 47.39, 10.44 47.55, 10.18 47.28, 9.97 47.51, 8.57 47.78)), ((13.36 54.25, 13.16 54.36, 13.18 54.54, 13.42 54.7, 13.71 54.38, 13.36 54.25)), ((13.93 53.88, 13.83 54.13, 14.04 54.03, 14.21 53.95, 13.93 53.88)), ((11.13 54.42, 11.01 54.47, 11.08 54.53, 11.28 54.42, 11.13 54.42)), ((8.41 55.06, 8.38 54.9, 8.63 54.89, 8.31 54.79, 8.41 55.06)), ((8.55 54.69, 8.4 54.71, 8.51 54.76, 8.55 54.69)))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-extent> rdfs:comment "The E-OBS domain's published approximate extent (about 25W-45E, 25N-71.5N), from which the 1-day and 7-day percentile thresholds were pre-computed. E-OBS is distributed on a regular rectangular latitude/longitude grid, so a rectangle is the right shape for its extent; its actual land coverage is coarser than that and station density is not uniform." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_layers> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_overlay> cwl:in "blue_spot_detection/blue_spot_map",
        "exposure_layers" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#exposure_overlay.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_daily> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_subdaily> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_index> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_overlay> cwl:in "blue_spot_detection/blue_spot_map",
        "vulnerability_index" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#vulnerability_overlay.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure> dcterms:title "exposure layers (Local Climate Zones, imperviousness, population)" ;
    rdfs:comment "Contextual overlay: Question 4 is explicit that exposure does not enter the calculation, and Question 9 says that if users want their own exposure or vulnerability data, 'current workflow is no option for it'. Not substitutable, then, which this model cannot yet state (see the statement-level note). Question 9 also says 'All input datasets are covering EU', so the overlay cannot be produced outside the EU: recorded as an optional terminal rule on `eu-input-coverage`, our inference from those two answers, to be confirmed with the owner." ;
    focal-transf-prop:artifactRef "/inputs/exposure_layers" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/focal-stac-loader> dcterms:title "FOCAL STAC data loader, built into the workflow" ;
    rdfs:comment "Question 10 names this as the part that is still specific to the current infrastructure: 'all the required data is from FOCAL collection and data loader are built into the workflow. So, using this workflow outside with different dataset requires replacing that part.' Classified as infrastructure rather than a workflow input because it is a code path, not a dataset, and has nothing in an Application Package to point at." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/infrastructure> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/supported-grids> rdfs:comment "Question 7: 'Two grid types are supported: regular latitude/longitude and rotated pole. Other projections are not handled.' A hard interface limit over a small enumerable set, and the most mechanically checkable constraint in this envelope: the terms carry the CF-conventions grid_mapping_name as their notation, which gridded datasets declare directly." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/grid-structure> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-climate-regime> rdfs:comment "Question 9, near-verbatim: 'for a region with different climate regime, user should use a custom threshold'. Prose rather than an extent, because climatic similarity is the judgement being made and no geometry settles it. This is the constraint the threshold rule is conditioned on, rather than the two spatial provenances above: a target inside Germany whose climate is unlike the stations' is as much of a problem as one outside it." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "the German and European climate regime the pre-computed percentile thresholds were derived from" .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-daily> dcterms:title "pre-computed 95th/99th percentile thresholds for the 1-day and 7-day accumulation windows (E-OBS, Europe)" ;
    focal-transf-prop:artifactRef "/inputs/threshold_daily" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold-subdaily> dcterms:title "pre-computed 95th/99th percentile thresholds for the 6-hour and 12-hour accumulation windows (DWD station data, Germany)" ;
    focal-transf-prop:artifactRef "/inputs/threshold_subdaily" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability> dcterms:title "vulnerability index at NUTS3 level (Risk Data Hub)" ;
    rdfs:comment "Contextual overlay, and not substitutable, for the same reason recorded on `exposure`, with the same optional rule outside the EU. Question 7 also states the index is at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary', which is carried by the `spatial-support-mismatch` qualityAnnotation. Question 8: the index data is 'currently local files, until it is published on the FOCAL STAC'." ;
    focal-transf-prop:artifactRef "/inputs/vulnerability_index" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eu-input-coverage> rdfs:comment "Question 9: 'All input datasets are covering EU.' Approximated by the EU as a coarse union of the 27 member countries (Natural Earth, public domain, simplified) within a European window, so overseas territories are excluded and small islands such as Malta and Cyprus are dropped. Deliberately coarse and known to be too generous: this is really the intersection of E-OBS, the NUKLEUS EUR-11 domain, the Local Climate Zone, imperviousness and population layers, and a NUTS3 vulnerability index that stops at the EU's borders, and the individual footprints were not stated. Needs owner confirmation before it is relied on." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "MULTIPOLYGON (((-8.79 39.08, -9.48 38.8, -8.66 41.03, -9.18 43.17, -7.7 43.76, -1.99 43.35, -1.08 45.53, -0.83 45.38, -0.69 45.09, -0.55 45, -1.74 47.22, -4.72 48.54, -1.38 48.65, -1.86 49.68, 0.42 49.45, 1.77 50.94, 4.23 51.39, 3.45 51.54, 4.27 51.47, 5.53 53.27, 9.78 53.55, 8.13 55.6, 8.16 56.61, 9.2 56.7, 8.27 56.75, 8.62 57.11, 10.61 57.74, 10.28 56.62, 10.89 56.36, 9.45 55.04, 10.92 54, 12.58 54.47, 13.72 54.15, 13.95 53.8, 14.58 53.64, 13.83 54.13, 18.09 54.84, 22.73 54.35, 22.57 55.06, 21.2 55.34, 21.46 57.32, 24.28 57.17, 24.53 58.35, 23.43 58.92, 24.38 59.47, 28.15 59.37, 27.35 57.53, 28.15 56.14, 26.59 55.67, 25.75 54.16, 23.48 53.94, 23.92 52.77, 23.18 52.29, 24.09 50.53, 22.13 48.41, 24.89 47.72, 26.9 48.21, 28.24 46.64, 28.21 45.45, 29.71 45.26, 27.48 42.47, 28.01 41.97, 26.58 41.95, 26.04 40.73, 23.76 40.75, 23.95 39.97, 22.63 40.5, 23.33 39.17, 22.57 38.87, 24.02 38.14, 22.73 37.54, 23.16 36.45, 21.12 37.89, 23.15 38.18, 21.18 38.35, 20 39.71, 20.96 40.85, 22.93 41.36, 22.34 42.31, 22.73 44.57, 19.61 46.17, 18.84 45.84, 19.01 44.87, 15.79 45.18, 17.59 42.94, 15.99 43.52, 14.55 45.3, 13.86 44.84, 13.63 45.77, 12.27 45.45, 12.4 44.22, 14.18 42.51, 18.46 40.22, 16.93 40.46, 16.52 39.75, 17.17 39, 16.06 37.94, 15.69 39.99, 8.77 44.42, 6.12 43.07, 3.26 43.19, 3.25 41.94, 0.71 40.82, -0.33 39.52, 0.2 38.76, -2.11 36.78, -5.63 36.03, -6.86 37.28, -8.74 37.07, -8.79 39.08)), ((-7.85 54.22, -6.18 54.05, -6.32 52.25, -10.12 51.6, -9.6 51.87, -10.36 52.21, -8.78 52.68, -9.92 52.57, -8.93 53.21, -10.09 53.41, -9.58 53.81, -10.09 54.22, -6.96 55.24, -7.85 54.22)), ((12.88 61.35, 12.16 61.72, 12.18 63.6, 14.06 64.1, 13.65 64.58, 14.54 66.13, 16.78 67.9, 21.27 69.27, 24.94 68.59, 26.53 69.92, 29.33 69.47, 28.41 68.9, 29.99 67.67, 29.07 66.89, 30.09 65.79, 29.6 64.97, 30.53 64.08, 29.99 63.74, 31.54 62.92, 29.25 61.29, 23.02 59.82, 21.44 60.6, 21.55 63.2, 25.37 65.01, 24.63 65.86, 22.4 65.86, 20.76 63.87, 17.38 62.46, 17.25 60.7, 18.99 59.83, 16.21 58.64, 16.92 58.49, 15.92 56.17, 12.89 55.41, 12.88 56.62, 11.25 58.37, 12.88 61.35)))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation> dcterms:title "precipitation input dataset (E-OBS or the NUKLEUS regional climate ensemble, read from the FOCAL STAC catalogue)" ;
    sld:type cwl:File ;
    focal-transf-prop:acceptanceCriteria [ rdfs:comment "Question 9 states the fullest replacement contract in the corpus: 'The precipitation dataset must provide same precipitation variable name as current dataset, its unit (mm or flux (kg m-2 s-1)), a time axis, and the grid or projection must be either regular lat/lon or rotated pole.' The variable requirement is recorded as the relation the source states rather than as a literal: it says the replacement must match the current dataset, not what the current dataset is called. An earlier draft guessed `rr`, which is E-OBS's name and wrong for the CORDEX path where the same field is `pr` — the guess was needed only because the schema wanted a literal where the source gave a relation. One further requirement still resists this shape: the source's temporal resolution gates which accumulation windows are available, which is a constraint between two inputs rather than a property of this one." ;
            focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> ;
            focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ;
            focal-transf-prop:unit <http://qudt.org/vocab/unit/KiloGM-PER-M2-SEC>,
                <http://qudt.org/vocab/unit/MilliM> ;
            focal-transf-prop:variable [ focal-transf-prop:sameAsCurrent true ] ] ;
    focal-transf-prop:artifactRef "/inputs/precipitation" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Workflow
description: "A profile of a CWL Workflow (`ogc.cwl.v1_2_1.CWLWorkflow`) adding FOCAL's
  machine-readable transferability facts, extracted from FOCAL's 8 pilot-workflow
  questionnaires:\n- `transferability` \u2014 the workflow's portability boundary,
  one\n  [`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement)\n
  \ (its `envelope`, `artifacts` and `rules`). Required: every evidenced workflow
  states one.\n- `computationType`, `maturityStatus` \u2014 the two workflow-level
  classification mixins (see\n  [`computationType`](bblocks://ogc.focal.transferability.computationType)
  and\n  [`maturityStatus`](bblocks://ogc.focal.transferability.maturityStatus) for
  which is optional\n  and which is required).\n- `qualityAnnotation` \u2014 a repeatable,
  optional workflow-level fact (see its own block for\n  evidence density and omission
  rules).\n\n`computationType`/`maturityStatus`/`qualityAnnotation` stay outside `transferability`
  on purpose: they describe the workflow's implementation and result quality generally,
  not its portability boundary \u2014 see `transferabilityStatement` for the same
  distinction from its side.\n"
allOf:
- $ref: https://ogcincubator.github.io/bblocks-cwl/build/annotated/cwl/v1_2_1/CWLWorkflow/schema.yaml
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/computationType/schema.yaml
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/maturityStatus/schema.yaml
- type: object
  required:
  - transferability
  properties:
    id:
      $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/iri-or-curie/schema.yaml
      description: 'Identifier for the workflow, resolved against the document''s
        base URI. Optional, but worth setting: without it the workflow is an anonymous
        node in RDF, and its envelope constraints and artifacts end up as named resources
        hanging off a subject nothing can refer to. An empty string resolves to the
        base URI itself, i.e. "the workflow this document describes".

        '
      x-jsonld-id: '@id'
    transferability:
      $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/transferabilityStatement/schema.yaml
      description: 'The workflow''s portability boundary: where its results are valid
        (`envelope`) and which artifacts it depends on, and what must happen to each
        outside it. See `transferabilityStatement` for the three lists and how they
        reference each other.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/transferability
    qualityAnnotation:
      type: array
      items:
        $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/qualityAnnotation/schema.yaml
      description: 'Uncertainty/confidence statements about the workflow''s results,
        independent of `maturityStatus`. Optional and repeatable.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/qualityAnnotation
      x-jsonld-container: '@set'
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "version": "cwl:SoftwarePackage/version",
    "doc": "rdfs:comment",
    "label": "rdfs:label",
    "Workflow": "cwl:Workflow",
    "class": "@type",
    "hints": {
      "@context": {
        "DockerRequirement": "cwl:DockerRequirement",
        "EnvVarRequirement": "cwl:EnvVarRequirement",
        "InitialWorkDirRequirement": "cwl:InitialWorkDirRequirement",
        "InlineJavascriptRequirement": "cwl:InlineJavascriptRequirement",
        "InplaceUpdateRequirement": "cwl:InplaceUpdateRequirement",
        "LoadListingRequirement": "cwl:LoadListingRequirement",
        "MultipleInputFeatureRequirement": "cwl:MultipleInputFeatureRequirement",
        "NetworkAccess": "cwl:NetworkAccess",
        "ResourceRequirement": "cwl:ResourceRequirement",
        "ScatterFeatureRequirement": "cwl:ScatterFeatureRequirement",
        "SchemaDefRequirement": "cwl:SchemaDefRequirement",
        "ShellCommandRequirement": "cwl:ShellCommandRequirement",
        "SoftwareRequirement": "cwl:SoftwareRequirement",
        "StepInputExpressionRequirement": "cwl:StepInputExpressionRequirement",
        "SubworkflowFeatureRequirement": "cwl:SubworkflowFeatureRequirement",
        "ToolTimeLimit": "cwl:ToolTimeLimit",
        "WorkReuse": "cwl:WorkReuse",
        "dockerFile": "cwl:DockerRequirement/dockerFile",
        "dockerImageId": "cwl:DockerRequirement/dockerImageId",
        "dockerImport": "cwl:DockerRequirement/dockerImport",
        "dockerLoad": "cwl:DockerRequirement/dockerLoad",
        "dockerOutputDirectory": "cwl:DockerRequirement/dockerOutputDirectory",
        "dockerPull": "cwl:DockerRequirement/dockerPull",
        "packages": {
          "@context": {
            "package": "cwl:SoftwarePackage/package",
            "specs": {
              "@id": "cwl:SoftwarePackage/specs",
              "@type": "@id"
            }
          },
          "@id": "cwl:SoftwareRequirement/packages",
          "@container": "@id"
        },
        "envDef": {
          "@context": {
            "envName": "cwl:EnvironmentDef/envName",
            "envValue": "cwl:EnvironmentDef/envValue"
          },
          "@id": "cwl:EnvVarRequirement/envDef",
          "@container": "@id"
        },
        "types": {
          "@context": {
            "type": {
              "@id": "sld:type",
              "@type": "@vocab"
            },
            "fields": {
              "@context": {
                "format": {
                  "@id": "cwl:format",
                  "@type": "@id"
                },
                "loadContents": "cwl:loadContents",
                "secondaryFiles": "cwl:secondaryFiles",
                "streamable": "cwl:FieldBase/streamable"
              },
              "@id": "sld:fields",
              "@container": "@id"
            },
            "name": "@id",
            "items": {
              "@id": "sld:items",
              "@type": "@vocab"
            }
          },
          "@id": "cwl:SchemaDefRequirement/types"
        },
        "listing": "cwl:listing",
        "expressionLib": "cwl:InlineJavascriptRequirement/expressionLib",
        "inplaceUpdate": "cwl:InplaceUpdateRequirement/inplaceUpdate",
        "loadListing": "cwl:loadListing",
        "networkAccess": "cwl:NetworkAccess/networkAccess",
        "coresMin": "cwl:ResourceRequirement/coresMin",
        "coresMax": "cwl:ResourceRequirement/coresMax",
        "ramMin": "cwl:ResourceRequirement/ramMin",
        "ramMax": "cwl:ResourceRequirement/ramMax",
        "outdirMin": "cwl:ResourceRequirement/outdirMin",
        "outdirMax": "cwl:ResourceRequirement/outdirMax",
        "tmpdirMin": "cwl:ResourceRequirement/tmpdirMin",
        "tmpdirMax": "cwl:ResourceRequirement/tmpdirMax",
        "timelimit": "cwl:ToolTimeLimit/timelimit",
        "enableReuse": "cwl:WorkReuse/enableReuse"
      },
      "@id": "cwl:hints",
      "@container": "@type"
    },
    "inputs": {
      "@context": {
        "default": {
          "@context": {
            "basename": "cwl:basename",
            "location": "@id",
            "nameroot": "cwl:File/nameroot",
            "path": {
              "@id": "cwl:path",
              "@type": "@id"
            }
          },
          "@id": "sld:default"
        },
        "type": {
          "@id": "sld:type",
          "@type": "@vocab"
        },
        "inputBinding": {
          "@context": {
            "itemSeparator": "cwl:CommandLineBinding/itemSeparator",
            "position": "cwl:CommandLineBinding/position",
            "prefix": "cwl:CommandLineBinding/prefix",
            "shellQuote": "cwl:CommandLineBinding/shellQuote",
            "valueFrom": "cwl:valueFrom"
          },
          "@id": "cwl:inputBinding"
        }
      },
      "@id": "cwl:inputs",
      "@container": "@id"
    },
    "outputs": {
      "@context": {
        "outputBinding": {
          "@context": {
            "glob": "cwl:CommandOutputBinding/glob"
          },
          "@id": "cwl:outputBinding"
        },
        "type": {
          "@id": "sld:type",
          "@type": "@vocab"
        }
      },
      "@id": "cwl:outputs",
      "@container": "@id"
    },
    "requirements": {
      "@context": {
        "DockerRequirement": "cwl:DockerRequirement",
        "EnvVarRequirement": "cwl:EnvVarRequirement",
        "InitialWorkDirRequirement": "cwl:InitialWorkDirRequirement",
        "InlineJavascriptRequirement": "cwl:InlineJavascriptRequirement",
        "InplaceUpdateRequirement": "cwl:InplaceUpdateRequirement",
        "LoadListingRequirement": "cwl:LoadListingRequirement",
        "MultipleInputFeatureRequirement": "cwl:MultipleInputFeatureRequirement",
        "NetworkAccess": "cwl:NetworkAccess",
        "ResourceRequirement": "cwl:ResourceRequirement",
        "ScatterFeatureRequirement": "cwl:ScatterFeatureRequirement",
        "SchemaDefRequirement": "cwl:SchemaDefRequirement",
        "ShellCommandRequirement": "cwl:ShellCommandRequirement",
        "SoftwareRequirement": "cwl:SoftwareRequirement",
        "StepInputExpressionRequirement": "cwl:StepInputExpressionRequirement",
        "SubworkflowFeatureRequirement": "cwl:SubworkflowFeatureRequirement",
        "ToolTimeLimit": "cwl:ToolTimeLimit",
        "WorkReuse": "cwl:WorkReuse",
        "dockerFile": "cwl:DockerRequirement/dockerFile",
        "dockerImageId": "cwl:DockerRequirement/dockerImageId",
        "dockerImport": "cwl:DockerRequirement/dockerImport",
        "dockerLoad": "cwl:DockerRequirement/dockerLoad",
        "dockerOutputDirectory": "cwl:DockerRequirement/dockerOutputDirectory",
        "dockerPull": "cwl:DockerRequirement/dockerPull",
        "packages": {
          "@context": {
            "package": "cwl:SoftwarePackage/package",
            "specs": {
              "@id": "cwl:SoftwarePackage/specs",
              "@type": "@id"
            }
          },
          "@id": "cwl:SoftwareRequirement/packages",
          "@container": "@id"
        },
        "envDef": {
          "@context": {
            "envName": "cwl:EnvironmentDef/envName",
            "envValue": "cwl:EnvironmentDef/envValue"
          },
          "@id": "cwl:EnvVarRequirement/envDef",
          "@container": "@id"
        },
        "types": {
          "@context": {
            "type": {
              "@id": "sld:type",
              "@type": "@vocab"
            },
            "fields": {
              "@context": {
                "format": {
                  "@id": "cwl:format",
                  "@type": "@id"
                },
                "loadContents": "cwl:loadContents",
                "secondaryFiles": "cwl:secondaryFiles",
                "streamable": "cwl:FieldBase/streamable"
              },
              "@id": "sld:fields",
              "@container": "@id"
            },
            "name": "@id",
            "items": {
              "@id": "sld:items",
              "@type": "@vocab"
            }
          },
          "@id": "cwl:SchemaDefRequirement/types"
        },
        "listing": "cwl:listing",
        "expressionLib": "cwl:InlineJavascriptRequirement/expressionLib",
        "inplaceUpdate": "cwl:InplaceUpdateRequirement/inplaceUpdate",
        "loadListing": "cwl:loadListing",
        "networkAccess": "cwl:NetworkAccess/networkAccess",
        "coresMin": "cwl:ResourceRequirement/coresMin",
        "coresMax": "cwl:ResourceRequirement/coresMax",
        "ramMin": "cwl:ResourceRequirement/ramMin",
        "ramMax": "cwl:ResourceRequirement/ramMax",
        "outdirMin": "cwl:ResourceRequirement/outdirMin",
        "outdirMax": "cwl:ResourceRequirement/outdirMax",
        "tmpdirMin": "cwl:ResourceRequirement/tmpdirMin",
        "tmpdirMax": "cwl:ResourceRequirement/tmpdirMax",
        "timelimit": "cwl:ToolTimeLimit/timelimit",
        "enableReuse": "cwl:WorkReuse/enableReuse"
      },
      "@id": "cwl:requirements",
      "@container": "@type"
    },
    "steps": {
      "@context": {
        "in": {
          "@context": {
            "linkMerge": "cwl:linkMerge",
            "source": {
              "@id": "cwl:source",
              "@type": "@id"
            },
            "valueFrom": "cwl:valueFrom",
            "default": {
              "@context": {
                "basename": "cwl:basename",
                "location": "@id",
                "nameroot": "cwl:File/nameroot",
                "path": {
                  "@id": "cwl:path",
                  "@type": "@id"
                }
              },
              "@id": "sld:default",
              "@container": "@list"
            }
          },
          "@id": "cwl:in",
          "@container": "@id"
        },
        "out": {
          "@id": "cwl:out",
          "@type": "@id"
        },
        "run": {
          "@context": {
            "arguments": {
              "@context": {
                "itemSeparator": "cwl:CommandLineBinding/itemSeparator",
                "position": "cwl:CommandLineBinding/position",
                "prefix": "cwl:CommandLineBinding/prefix",
                "shellQuote": "cwl:CommandLineBinding/shellQuote",
                "valueFrom": "cwl:valueFrom"
              },
              "@id": "cwl:arguments",
              "@container": "@list"
            },
            "baseCommand": {
              "@id": "cwl:baseCommand",
              "@container": "@list"
            },
            "intent": {
              "@id": "cwl:Process/intent",
              "@type": "@id"
            },
            "stderr": "cwl:stderr",
            "stdin": "cwl:stdin",
            "stdout": "cwl:stdout"
          },
          "@id": "cwl:run",
          "@type": "@id"
        },
        "when": "cwl:when",
        "scatter": {
          "@id": "cwl:scatter",
          "@type": "@id",
          "@container": "@list"
        },
        "scatterMethod": {
          "@id": "cwl:scatterMethod",
          "@type": "@vocab"
        }
      },
      "@id": "cwl:Workflow/steps",
      "@container": "@id"
    },
    "computationType": {
      "@context": {
        "@base": "https://w3id.org/ogc/hosted/focal/transferability/computation-types/"
      },
      "@id": "focal-transf-prop:computationType",
      "@type": "@id"
    },
    "maturityStatus": {
      "@context": {
        "@base": "https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/"
      },
      "@id": "focal-transf-prop:maturityStatus",
      "@type": "@id"
    },
    "id": "@id",
    "transferability": {
      "@context": {
        "transferabilityNotes": "rdfs:comment",
        "envelope": {
          "@context": {
            "role": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/roles/"
              },
              "@id": "focal-transf-prop:role",
              "@type": "@id"
            },
            "dimension": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/dimensions/"
              },
              "@id": "focal-transf-prop:dimension",
              "@type": "@id"
            },
            "value": {
              "@context": {
                "asWKT": {
                  "@id": "geo:asWKT",
                  "@type": "geo:wktLiteral"
                },
                "startDate": "dcat:startDate",
                "endDate": "dcat:endDate",
                "scenarioMarker": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/scenario-markers/"
                  },
                  "@id": "focal-transf-prop:scenarioMarker",
                  "@type": "@id"
                },
                "gridTypes": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/grid-types/"
                  },
                  "@id": "focal-transf-prop:gridType",
                  "@type": "@id",
                  "@container": "@set"
                },
                "scheme": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/classification-schemes/"
                  },
                  "@id": "focal-transf-prop:classificationScheme",
                  "@type": "@id"
                },
                "sameClassAs": {
                  "@id": "focal-transf-prop:sameClassAs",
                  "@type": "@id"
                },
                "classes": {
                  "@id": "focal-transf-prop:class",
                  "@container": "@set"
                }
              },
              "@id": "focal-transf-prop:value"
            }
          },
          "@id": "focal-transf-prop:envelope",
          "@container": "@set"
        },
        "noConstraintsStated": "focal-transf-prop:noConstraintsStated",
        "trainingRequired": "focal-transf-prop:trainingRequired",
        "artifacts": {
          "@context": {
            "artifact": "dct:title",
            "artifactRole": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/"
              },
              "@id": "focal-transf-prop:artifactRole",
              "@type": "@id"
            },
            "acceptanceCriteria": {
              "@context": {
                "variable": {
                  "@context": {
                    "sameAsCurrent": "focal-transf-prop:sameAsCurrent"
                  },
                  "@id": "focal-transf-prop:variable"
                },
                "units": {
                  "@context": {
                    "@base": "http://qudt.org/vocab/unit/"
                  },
                  "@id": "focal-transf-prop:unit",
                  "@type": "@id",
                  "@container": "@set"
                },
                "axes": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/axes/"
                  },
                  "@id": "focal-transf-prop:axis",
                  "@type": "@id",
                  "@container": "@set"
                },
                "gridTypes": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/grid-types/"
                  },
                  "@id": "focal-transf-prop:gridType",
                  "@type": "@id",
                  "@container": "@set"
                },
                "conformsTo": {
                  "@id": "dct:conformsTo",
                  "@type": "@id",
                  "@container": "@set"
                }
              },
              "@id": "focal-transf-prop:acceptanceCriteria"
            },
            "artifactRef": "focal-transf-prop:artifactRef"
          },
          "@id": "focal-transf-prop:artifacts",
          "@container": "@set"
        },
        "rules": {
          "@context": {
            "appliesTo": {
              "@id": "focal-transf-prop:appliesTo",
              "@type": "@id",
              "@container": "@set"
            },
            "when": {
              "@context": {
                "constraint": {
                  "@id": "focal-transf-prop:constraint",
                  "@type": "@id"
                },
                "test": {
                  "@context": {
                    "@base": "https://w3id.org/ogc/hosted/focal/transferability/tests/"
                  },
                  "@id": "focal-transf-prop:test",
                  "@type": "@id"
                }
              },
              "@id": "focal-transf-prop:when",
              "@container": "@set"
            },
            "triggeredBy": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/triggers/"
              },
              "@id": "focal-transf-prop:triggeredBy",
              "@type": "@id"
            },
            "affects": {
              "@id": "focal-transf-prop:affects",
              "@container": "@set"
            },
            "actions": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/actions/"
              },
              "@id": "focal-transf-prop:actions",
              "@type": "@id",
              "@container": "@set"
            },
            "mandatory": "focal-transf-prop:mandatory"
          },
          "@id": "focal-transf-prop:rules",
          "@container": "@set"
        }
      },
      "@id": "focal-transf-prop:transferability"
    },
    "qualityAnnotation": {
      "@context": {
        "dimension": {
          "@context": {
            "@base": "https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/"
          },
          "@id": "dqv:inDimension",
          "@type": "@id"
        },
        "note": "focal-transf-prop:note"
      },
      "@id": "focal-transf-prop:qualityAnnotation",
      "@container": "@set"
    },
    "writable": "cwl:Dirent/writable",
    "checksum": "cwl:File/checksum",
    "size": "cwl:File/size",
    "null": "sld:null",
    "boolean": "xsd:boolean",
    "int": "xsd:int",
    "integer": "xsd:int",
    "long": "xsd:long",
    "float": "xsd:float",
    "double": "xsd:double",
    "string": "xsd:string",
    "File": "cwl:File",
    "Directory": "cwl:Directory",
    "BuiltinRequirement": "ogccwl:BuiltinRequirement",
    "OGCAPIRequirement": "ogccwl:OGCAPIRequirement",
    "WPS1Requirement": "ogccwl:WPS1Requirement",
    "CommandLineTool": "cwl:CommandLineTool",
    "ExpressionTool": "cwl:ExpressionTool",
    "s": "https://schema.org/",
    "cwl": "https://w3id.org/cwl/cwl#",
    "cwltool": "http://commonwl.org/cwltool#",
    "sld": "https://w3id.org/cwl/salad#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "ogccwl": "https://w3id.org/ogc/cwl/",
    "dct": "http://purl.org/dc/terms/",
    "focal-transf-prop": "focal-transf:properties/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "dcterms": "http://purl.org/dc/terms/",
    "focal-transf": "https://w3id.org/ogc/hosted/focal/transferability/",
    "prov": "http://www.w3.org/ns/prov#",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dqv": "http://www.w3.org/ns/dqv#",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/workflow`

