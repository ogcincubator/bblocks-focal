
# FOCAL Transferability Workflow (Schema)

`ogc.focal.transferability.workflow` *v0.2*

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

**Status: draft/WIP**, four worked examples (FP-WF1, FP-WF2, FP-WF3, UP-WF2) — chosen to cover the
model's main branch points: multiple simultaneous envelope roles, OR-set actions, an
optional/degrading rule (`mandatory: false`), the `component-not-executable` terminal outcome, one
rule shared across four artifacts, a two-rule cascade over a single constraint, and a directly
evidenced temporal envelope entry. The remaining 4 pilot workflows (FP-WF4, FP-WF5,
UP-WF1, UP-WF3) aren't yet worked as examples — UP-WF1 in particular can't be, without fabricating
values: its source states no assignable `envelope` fact at all (see the
mapping-extraction doc's UP-WF1 section), so it fails this schema's `required` properties outright
until its owner is consulted. Not yet circulated to WF owners generally — that circulation will
happen through this repo (PR review on `bblocks-focal`, not a separate document).

## Examples

### FP-WF1 — Tree species suitability
The richest of the eight FOCAL pilot workflows for this model: three simultaneous envelope
roles, an OR-set of actions on one artifact, and the only workflow with an evidenced quality
caveat so far. Drawn from `20260817-workflow-transferability-mapping-extraction.md`.

**What the rules now say that they could not before.** The trained model must be retrained or
replaced when the target is outside `ecological-range`; the climate data must be swapped when
the target is outside `czech-plots`. Two artifacts, two different boundaries, each rule
naming its own — previously both said only "different geographic coverage" and nothing
recorded which extent that referred to.

**`czech-plots` is an approximation and says so in the data.** The source says "Czech
long-term permanent sample plots", a scattered set of monitoring locations; the value here is
Czechia's country bounding box, an honest upper bound. That caveat is a
`transferabilityNotes` on the constraint (uplifting to `rdfs:comment`), not a remark in this
prose, so a consumer weighing the envelope can see it.

No temporal constraint: the source states a user-selected "prediction period" with no bound
or granularity, and none is invented. `steps` is omitted — no Application Package exists yet.
The `inputs`/`outputs` ids are **placeholders** invented so `artifactRef` has something to
point at; they are not FP-WF1's real interface.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "FP-WF1 — Tree species suitability",
  "inputs": { "climate_data": "File" },
  "outputs": { "trained_growth_model": "File" },
  "transferability": {
    "envelope": [
      {
        "id": "czech-plots",
        "role": "trained-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))" },
        "transferabilityNotes": "Czechia's country bounding box, standing in for the actual Czech long-term permanent sample plot network — a scattered set of monitoring locations, not a rectangle. An honest upper bound pending the real plot coordinates from the workflow owner."
      },
      {
        "id": "ecological-range",
        "role": "valid-for",
        "dimension": "ecological",
        "value": "a comparable ecological range"
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
        "artifactRole": "workflow-output",
        "artifactRef": "/outputs/trained_growth_model"
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
        "mandatory": true
      },
      {
        "appliesTo": ["climate-data"],
        "when": [{ "constraint": "czech-plots", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
      }
    ]
  },
  "computationType": "statistical-ml",
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "AI model and validation are still being finalised; results are decision-support, not exact forecasts."
    }
  ]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "FP-WF1 \u2014 Tree species suitability",
  "inputs": {
    "climate_data": "File"
  },
  "outputs": {
    "trained_growth_model": "File"
  },
  "transferability": {
    "envelope": [
      {
        "id": "czech-plots",
        "role": "trained-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"
        },
        "transferabilityNotes": "Czechia's country bounding box, standing in for the actual Czech long-term permanent sample plot network \u2014 a scattered set of monitoring locations, not a rectangle. An honest upper bound pending the real plot coordinates from the workflow owner."
      },
      {
        "id": "ecological-range",
        "role": "valid-for",
        "dimension": "ecological",
        "value": "a comparable ecological range"
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
        "artifactRole": "workflow-output",
        "artifactRef": "/outputs/trained_growth_model"
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
        "mandatory": true
      },
      {
        "appliesTo": [
          "climate-data"
        ],
        "when": [
          {
            "constraint": "czech-plots",
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
  "maturityStatus": "operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "AI model and validation are still being finalised; results are decision-support, not exact forecasts."
    }
  ]
}
```

#### ttl
```ttl
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<file:///github/workspace/downscaled-climate-available> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value "wherever downscaled climate data is available" .

<file:///github/workspace/climate-data> dcterms:title "downscaled FOCAL climate data (current + future)" ;
    focal-transf-prop:artifactRef "/inputs/climate_data" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<file:///github/workspace/czech-plots> rdfs:comment "Czechia's country bounding box, standing in for the actual Czech long-term permanent sample plot network — a scattered set of monitoring locations, not a rectangle. An honest upper bound pending the real plot coordinates from the workflow owner." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"^^geo:wktLiteral ] .

<file:///github/workspace/ecological-range> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "a comparable ecological range" .

<file:///github/workspace/growth-model> dcterms:title "trained tree growth model (LightGBM, Czech permanent sample plot data)" ;
    focal-transf-prop:artifactRef "/outputs/trained_growth_model" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-output> .

[] rdfs:label "FP-WF1 — Tree species suitability" ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/decision-support-only> ;
            focal-transf-prop:note "AI model and validation are still being finalised; results are decision-support, not exact forecasts." ] ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <file:///github/workspace/climate-data>,
                <file:///github/workspace/growth-model> ;
            focal-transf-prop:envelope <file:///github/workspace/czech-plots>,
                <file:///github/workspace/downscaled-climate-available>,
                <file:///github/workspace/ecological-range> ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-alternative-published-model>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/growth-model> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/ecological-range> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/climate-data> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/czech-plots> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ] .


```


### FP-WF2 — Heat stress (four artifacts, one shared boundary)
A deterministic/rule-based workflow whose reference data — species tolerance thresholds,
SLT/T5 forest classification, species codes, and the Rasdaman climate registry — is uniformly
Czechia-specific.

**This is the case that motivated declaring artifacts separately from rules.** All four share
one boundary and one action, so this is a single rule naming four artifacts in `appliesTo`,
rather than the same condition repeated four times. Previously each artifact carried its own
copy of an identical rule, and nothing said they were the same fact.

The envelope entry is **inferred, not stated**: the questionnaire never gives an envelope
fact directly, only that four artifacts are Czechia-specific. That inference is recorded on
the constraint itself and needs owner confirmation.

No temporal constraint (the source states a "time period" input with no bound). `steps`
omitted, no Application Package yet. `inputs` ids are placeholders.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "FP-WF2 — Heat stress",
  "inputs": {
    "species_tolerances": "File",
    "forest_classification_context": "File",
    "species_codes": "File",
    "climate_registry_endpoint": "string"
  },
  "transferability": {
    "envelope": [
      {
        "id": "czechia",
        "role": "trained-on",
        "dimension": "jurisdictional",
        "value": { "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))" },
        "transferabilityNotes": "Inferred, not stated: the questionnaire gives no envelope fact directly, only that four separate reference artifacts are Czechia-specific. Value is Czechia's country bounding box. Needs owner confirmation."
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
        "appliesTo": ["tolerances", "slt-t5", "species-codes", "rasdaman"],
        "when": [{ "constraint": "czechia", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Users may also override the tolerance thresholds directly, even within the source region — a separate user-configurability fact, not modelled here."
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
  "cwlVersion": "v1.2",
  "label": "FP-WF2 \u2014 Heat stress",
  "inputs": {
    "species_tolerances": "File",
    "forest_classification_context": "File",
    "species_codes": "File",
    "climate_registry_endpoint": "string"
  },
  "transferability": {
    "envelope": [
      {
        "id": "czechia",
        "role": "trained-on",
        "dimension": "jurisdictional",
        "value": {
          "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"
        },
        "transferabilityNotes": "Inferred, not stated: the questionnaire gives no envelope fact directly, only that four separate reference artifacts are Czechia-specific. Value is Czechia's country bounding box. Needs owner confirmation."
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
          "tolerances",
          "slt-t5",
          "species-codes",
          "rasdaman"
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
        "transferabilityNotes": "Users may also override the tolerance thresholds directly, even within the source region \u2014 a separate user-configurability fact, not modelled here."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational"
}
```

#### ttl
```ttl
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<file:///github/workspace/czechia> rdfs:comment "Inferred, not stated: the questionnaire gives no envelope fact directly, only that four separate reference artifacts are Czechia-specific. Value is Czechia's country bounding box. Needs owner confirmation." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/jurisdictional> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"^^geo:wktLiteral ] .

<file:///github/workspace/rasdaman> dcterms:title "Rasdaman climate registry / source catalogue" ;
    focal-transf-prop:artifactRef "/inputs/climate_registry_endpoint" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<file:///github/workspace/slt-t5> dcterms:title "SLT/T5 forest classification context (Czechia-specific)" ;
    focal-transf-prop:artifactRef "/inputs/forest_classification_context" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<file:///github/workspace/species-codes> dcterms:title "species codes catalogue (species_codes.json)" ;
    focal-transf-prop:artifactRef "/inputs/species_codes" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<file:///github/workspace/tolerances> dcterms:title "species tolerance thresholds (species_tolerances.json)" ;
    focal-transf-prop:artifactRef "/inputs/species_tolerances" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

[] rdfs:label "FP-WF2 — Heat stress" ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <file:///github/workspace/rasdaman>,
                <file:///github/workspace/slt-t5>,
                <file:///github/workspace/species-codes>,
                <file:///github/workspace/tolerances> ;
            focal-transf-prop:envelope <file:///github/workspace/czechia> ;
            focal-transf-prop:rules [ rdfs:comment "Users may also override the tolerance thresholds directly, even within the source region — a separate user-configurability fact, not modelled here." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/rasdaman>,
                        <file:///github/workspace/slt-t5>,
                        <file:///github/workspace/species-codes>,
                        <file:///github/workspace/tolerances> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/czechia> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ] .


```


### FP-WF3 — Prediction of threatened stands (optional rule, degraded mode)
The sharpest evidenced example of a non-operational workflow (`maturityStatus: prototype`),
and the only one whose source explicitly describes a rule as optional-but-degrading: without
local training labels, results are still produced, just "treated as exploratory". That is
`mandatory: false` with the consequence spelled out — a skippable rule with no stated
consequence tells a consumer nothing they can act on, so `shapes.shacl` rejects that pairing.

The spatial constraint is **more speculative than FP-WF1's or FP-WF2's**: no sentence in this
questionnaire names a location at all. Czechia is a proxy because this is a Forest Pilot
workflow. Recorded as such on the constraint.

No temporal constraint. `steps` omitted — this workflow's own questionnaire says its
container, API and regression-test packaging are still to be completed, so there is less of
an Application Package here than anywhere else. `inputs` ids are placeholders.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "FP-WF3 — Prediction of threatened stands",
  "inputs": {
    "disturbance_labels": "File",
    "eo_compositing_strategy": "string",
    "phenology_normalization_assumptions": "string"
  },
  "transferability": {
    "envelope": [
      {
        "id": "label-extent",
        "role": "trained-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))" },
        "transferabilityNotes": "More speculative than FP-WF1's or FP-WF2's: no sentence in this questionnaire names a location for the historical disturbance labels. Czechia is used as a proxy because this is a Forest Pilot workflow, and its country bounding box as the value. Needs owner confirmation before being treated as fact."
      },
      {
        "id": "phenological-regime",
        "role": "valid-for",
        "dimension": "ecological",
        "value": "a comparable phenological regime"
      }
    ],
    "artifacts": [
      { "id": "labels", "artifact": "historical forest disturbance/damage labels (ground truth training data)", "artifactRole": "workflow-input", "artifactRef": "/inputs/disturbance_labels" },
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
        "appliesTo": ["eo-strategy"],
        "when": [{ "constraint": "label-extent", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true
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
  "maturityStatus": "prototype"
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/workflow/context.jsonld",
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "FP-WF3 \u2014 Prediction of threatened stands",
  "inputs": {
    "disturbance_labels": "File",
    "eo_compositing_strategy": "string",
    "phenology_normalization_assumptions": "string"
  },
  "transferability": {
    "envelope": [
      {
        "id": "label-extent",
        "role": "trained-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"
        },
        "transferabilityNotes": "More speculative than FP-WF1's or FP-WF2's: no sentence in this questionnaire names a location for the historical disturbance labels. Czechia is used as a proxy because this is a Forest Pilot workflow, and its country bounding box as the value. Needs owner confirmation before being treated as fact."
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
        "artifactRef": "/inputs/disturbance_labels"
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
        "mandatory": true
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
  "maturityStatus": "prototype"
}
```

#### ttl
```ttl
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<file:///github/workspace/eo-strategy> dcterms:title "EO sensor selection, cloud masking, temporal compositing strategy" ;
    focal-transf-prop:artifactRef "/inputs/eo_compositing_strategy" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<file:///github/workspace/labels> dcterms:title "historical forest disturbance/damage labels (ground truth training data)" ;
    focal-transf-prop:artifactRef "/inputs/disturbance_labels" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<file:///github/workspace/phenological-regime> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "a comparable phenological regime" .

<file:///github/workspace/phenology> dcterms:title "regional phenology normalisation assumptions" ;
    focal-transf-prop:artifactRef "/inputs/phenology_normalization_assumptions" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<file:///github/workspace/label-extent> rdfs:comment "More speculative than FP-WF1's or FP-WF2's: no sentence in this questionnaire names a location for the historical disturbance labels. Czechia is used as a proxy because this is a Forest Pilot workflow, and its country bounding box as the value. Needs owner confirmation before being treated as fact." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"^^geo:wktLiteral ] .

[] rdfs:label "FP-WF3 — Prediction of threatened stands" ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/prototype> ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <file:///github/workspace/eo-strategy>,
                <file:///github/workspace/labels>,
                <file:///github/workspace/phenology> ;
            focal-transf-prop:envelope <file:///github/workspace/label-extent>,
                <file:///github/workspace/phenological-regime> ;
            focal-transf-prop:rules [ rdfs:comment "Without local training labels, results should be treated as exploratory rather than blocked outright — a degraded-mode caveat, not a hard requirement." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/labels> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/eo-strategy> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/phenology> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/phenological-regime> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ] .


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
model carried a computed Europe-minus-Ukraine MultiPolygon — 1,283 lines of Turtle, with the
exclusion invisible to anyone reading it and quietly lost the moment the geometry was
simplified. Here it is a named constraint cited by a rule with `test: inside`, so falling
within the excluded area is what makes the component unexecutable. It is legible, it is
separately correctable when the authoritative CLMS geometry arrives, and it survives
simplification of the surrounding extent.

Asked "can I run this in Kyiv?", a consumer now gets a per-artifact answer: the LST datasets
are inside EURO-CORDEX and reusable, and the CLMS layers are unavailable, so hot-spot
characterization cannot run.

**The cascade keeps its connecting condition.** The source describes reuse inside the domain,
substitution if a compatible dataset can be produced outside it, and failure if none can.
That is two rules over the same constraint — `inside` then `outside` — rather than the
previous two flat rules that dropped the "only if a substitute exists" link. The residual
uncertainty stays where the source leaves it: an OR-set of two actions.

The **temporal constraint is directly evidenced**, unlike the omitted periods elsewhere:
discrete epochs, 2022–2025 at time of writing.

Geometries are coarse extents, not cadastral boundaries, and say so on the constraint.
`outputs`/`steps` omitted; `inputs` ids are placeholders.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "UP-WF2 — Urban hot/cool spot",
  "inputs": { "lst_datasets": "File", "clms_tcd_imd": "File" },
  "transferability": {
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
        "value": { "asWKT": "POLYGON((-25 34,45 34,45 72,-25 72,-25 34))" },
        "transferabilityNotes": "CLMS product coverage, as a coarse bounding extent rather than a country-by-country outline: the precise boundary is a property of the CLMS product and is better dereferenced from CLMS than restated approximately here. The product's exclusion of Ukraine is a separate constraint (`clms-excluded-ukraine`) rather than a hole in this one — an exclusion carved into a geometry is invisible to a reader and easy to lose in simplification, whereas a named constraint a rule cites is neither."
      },
      {
        "id": "clms-excluded-ukraine",
        "role": "valid-for",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((22.1 44.4,40.2 44.4,40.2 52.4,22.1 52.4,22.1 44.4))" },
        "transferabilityNotes": "Ukraine's approximate bounding extent, which CLMS coverage excludes. Cited by a rule with test `inside`, so falling within it is what makes the component unexecutable. Coarse: a bounding box over Ukraine also covers parts of neighbouring countries, so this errs toward flagging a target that may in fact be covered — the safe direction for a portability check, but it needs the authoritative CLMS geometry before it is relied on."
      },
      {
        "id": "epochs",
        "role": "valid-for",
        "dimension": "temporal",
        "value": { "startDate": "2022", "endDate": "2025" },
        "transferabilityNotes": "Discrete temporal epochs, explicitly not a time series: one timestep per epoch. 2022–2025 available at time of writing."
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
        "mandatory": true,
        "transferabilityNotes": "Inside the EURO-CORDEX domain the datasets are reused unchanged, by changing the area of interest."
      },
      {
        "appliesTo": ["lst"],
        "when": [{ "constraint": "eur11-domain", "test": "outside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "mandatory": true,
        "transferabilityNotes": "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target. Which of the two applies depends on whether a substitute is obtainable, which the source does not resolve."
      },
      {
        "appliesTo": ["clms"],
        "when": [{ "constraint": "clms-extent", "test": "outside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "mandatory": true,
        "transferabilityNotes": "Outside CLMS coverage no substitute is currently defined, and hot-spot characterization, which uses this dataset, cannot be executed."
      },
      {
        "appliesTo": ["clms"],
        "when": [{ "constraint": "clms-excluded-ukraine", "test": "inside" }],
        "actions": ["component-not-executable"],
        "mandatory": true,
        "transferabilityNotes": "Within the CLMS bounding extent but inside the area the product excludes: no Tree Cover Density or Imperviousness Density data exists, and no substitute is defined, so hot-spot characterization cannot be executed. A terminal outcome with no alternative offered, unlike the coverage rule above."
      },
      {
        "appliesTo": ["eurostat"],
        "triggeredBy": "different-geographic-coverage",
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "mandatory": true,
        "transferabilityNotes": "Stated with triggeredBy rather than a cited constraint: this data is not yet implemented, so there is no envelope fact to point at. Once built, the planned Heat Risk Indicator would not be executable without it."
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
  "cwlVersion": "v1.2",
  "label": "UP-WF2 \u2014 Urban hot/cool spot",
  "inputs": {
    "lst_datasets": "File",
    "clms_tcd_imd": "File"
  },
  "transferability": {
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
          "asWKT": "POLYGON((-25 34,45 34,45 72,-25 72,-25 34))"
        },
        "transferabilityNotes": "CLMS product coverage, as a coarse bounding extent rather than a country-by-country outline: the precise boundary is a property of the CLMS product and is better dereferenced from CLMS than restated approximately here. The product's exclusion of Ukraine is a separate constraint (`clms-excluded-ukraine`) rather than a hole in this one \u2014 an exclusion carved into a geometry is invisible to a reader and easy to lose in simplification, whereas a named constraint a rule cites is neither."
      },
      {
        "id": "clms-excluded-ukraine",
        "role": "valid-for",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((22.1 44.4,40.2 44.4,40.2 52.4,22.1 52.4,22.1 44.4))"
        },
        "transferabilityNotes": "Ukraine's approximate bounding extent, which CLMS coverage excludes. Cited by a rule with test `inside`, so falling within it is what makes the component unexecutable. Coarse: a bounding box over Ukraine also covers parts of neighbouring countries, so this errs toward flagging a target that may in fact be covered \u2014 the safe direction for a portability check, but it needs the authoritative CLMS geometry before it is relied on."
      },
      {
        "id": "epochs",
        "role": "valid-for",
        "dimension": "temporal",
        "value": {
          "startDate": "2022",
          "endDate": "2025"
        },
        "transferabilityNotes": "Discrete temporal epochs, explicitly not a time series: one timestep per epoch. 2022\u20132025 available at time of writing."
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
        "mandatory": true,
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
        "mandatory": true,
        "transferabilityNotes": "Outside CLMS coverage no substitute is currently defined, and hot-spot characterization, which uses this dataset, cannot be executed."
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
          "component-not-executable"
        ],
        "mandatory": true,
        "transferabilityNotes": "Within the CLMS bounding extent but inside the area the product excludes: no Tree Cover Density or Imperviousness Density data exists, and no substitute is defined, so hot-spot characterization cannot be executed. A terminal outcome with no alternative offered, unlike the coverage rule above."
      },
      {
        "appliesTo": [
          "eurostat"
        ],
        "triggeredBy": "different-geographic-coverage",
        "actions": [
          "replace-with-local-equivalent",
          "component-not-executable"
        ],
        "mandatory": true,
        "transferabilityNotes": "Stated with triggeredBy rather than a cited constraint: this data is not yet implemented, so there is no envelope fact to point at. Once built, the planned Heat Risk Indicator would not be executable without it."
      }
    ]
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational"
}
```

#### ttl
```ttl
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<file:///github/workspace/epochs> rdfs:comment "Discrete temporal epochs, explicitly not a time series: one timestep per epoch. 2022–2025 available at time of writing." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ dcat:endDate "2025" ;
            dcat:startDate "2022" ] .

<file:///github/workspace/clms-excluded-ukraine> rdfs:comment "Ukraine's approximate bounding extent, which CLMS coverage excludes. Cited by a rule with test `inside`, so falling within it is what makes the component unexecutable. Coarse: a bounding box over Ukraine also covers parts of neighbouring countries, so this errs toward flagging a target that may in fact be covered — the safe direction for a portability check, but it needs the authoritative CLMS geometry before it is relied on." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((22.1 44.4,40.2 44.4,40.2 52.4,22.1 52.4,22.1 44.4))"^^geo:wktLiteral ] .

<file:///github/workspace/clms-extent> rdfs:comment "CLMS product coverage, as a coarse bounding extent rather than a country-by-country outline: the precise boundary is a property of the CLMS product and is better dereferenced from CLMS than restated approximately here. The product's exclusion of Ukraine is a separate constraint (`clms-excluded-ukraine`) rather than a hole in this one — an exclusion carved into a geometry is invisible to a reader and easy to lose in simplification, whereas a named constraint a rule cites is neither." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-25 34,45 34,45 72,-25 72,-25 34))"^^geo:wktLiteral ] .

<file:///github/workspace/eurostat> dcterms:title "Eurostat census / socio-economic data (planned Heat Risk Indicator)" ;
    rdfs:comment "Not yet implemented; the envisaged replacement should follow a schema compatible with Eurostat's." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<file:///github/workspace/clms> dcterms:title "CLMS Tree Cover Density / Imperviousness Density" ;
    focal-transf-prop:artifactRef "/inputs/clms_tcd_imd" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<file:///github/workspace/eur11-domain> rdfs:comment "The EUR-11 EURO-CORDEX domain's published approximate rectangular extent (about 22W–45E, 27N–72N), not its exact rotated-pole grid footprint, which is not a rectangle in true lat/lon at all. A deliberate simplification." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))"^^geo:wktLiteral ] .

<file:///github/workspace/lst> dcterms:title "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)" ;
    focal-transf-prop:artifactRef "/inputs/lst_datasets" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

[] rdfs:label "UP-WF2 — Urban hot/cool spot" ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <file:///github/workspace/clms>,
                <file:///github/workspace/eurostat>,
                <file:///github/workspace/lst> ;
            focal-transf-prop:envelope <file:///github/workspace/clms-excluded-ukraine>,
                <file:///github/workspace/clms-extent>,
                <file:///github/workspace/epochs>,
                <file:///github/workspace/eur11-domain> ;
            focal-transf-prop:rules [ rdfs:comment "Inside the EURO-CORDEX domain the datasets are reused unchanged, by changing the area of interest." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/reuse-as-is> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/lst> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/eur11-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/inside> ] ],
                [ rdfs:comment "Stated with triggeredBy rather than a cited constraint: this data is not yet implemented, so there is no envelope fact to point at. Once built, the planned Heat Risk Indicator would not be executable without it." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/eurostat> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ],
                [ rdfs:comment "Within the CLMS bounding extent but inside the area the product excludes: no Tree Cover Density or Imperviousness Density data exists, and no substitute is defined, so hot-spot characterization cannot be executed. A terminal outcome with no alternative offered, unlike the coverage rule above." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/clms> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/clms-excluded-ukraine> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/inside> ] ],
                [ rdfs:comment "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target. Which of the two applies depends on whether a substitute is obtainable, which the source does not resolve." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/lst> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/eur11-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Outside CLMS coverage no substitute is currently defined, and hot-spot characterization, which uses this dataset, cannot be executed." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <file:///github/workspace/clms> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <file:///github/workspace/clms-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ] .


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
    "label": "rdfs:label",
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
    "transferability": {
      "@context": {
        "envelope": {
          "@context": {
            "transferabilityNotes": "rdfs:comment",
            "id": "@id",
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
                }
              },
              "@id": "focal-transf-prop:value"
            }
          },
          "@id": "focal-transf-prop:envelope",
          "@container": "@set"
        },
        "artifacts": {
          "@context": {
            "id": "@id",
            "artifact": "dcterms:title",
            "artifactRole": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/"
              },
              "@id": "focal-transf-prop:artifactRole",
              "@type": "@id"
            },
            "artifactRef": "focal-transf-prop:artifactRef",
            "transferabilityNotes": "rdfs:comment"
          },
          "@id": "focal-transf-prop:artifacts",
          "@container": "@set"
        },
        "rules": {
          "@context": {
            "transferabilityNotes": "rdfs:comment",
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
    "loadContents": "cwl:loadContents",
    "streamable": "cwl:FieldBase/streamable",
    "loadListing": "cwl:loadListing",
    "cwl": "https://w3id.org/cwl/cwl#",
    "focal-transf-prop": "focal-transf:properties/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dcterms": "http://purl.org/dc/terms/",
    "focal-transf": "https://w3id.org/ogc/hosted/focal/transferability/",
    "prov": "http://www.w3.org/ns/prov#",
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

