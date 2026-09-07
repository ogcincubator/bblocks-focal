
# FOCAL Transferability Workflow (Schema)

`ogc.focal.transferability.workflow` *v0.8*

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

## Examples

### FP-WF1 — Tree species suitability
The richest of the eight FOCAL pilot workflows for this model: three simultaneous envelope
roles, an OR-set of actions on one artifact, and the only workflow with an evidenced quality
caveat so far. Drawn from `20260817-workflow-transferability-mapping-extraction.md`.

**What the rules now say that they could not before.** The trained model must be retrained or
replaced when the target is in a different ecological class from `ecological-range`; the climate data must be swapped when
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
  "inputs": { "climate_data": { "type": "File" } },
  "outputs": { "trained_growth_model": { "type": "File" } },
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
        "value": {
          "scheme": "eea-biogeographical-regions",
          "sameClassAs": "czech-plots"
        },
        "transferabilityNotes": "Question 7: results are 'valid mainly within a comparable ecological range'. That is an analogy to where the model was calibrated, not an extent, so it is stated as one: the target must share the biogeographical region of `czech-plots`. No region is named here on purpose — the source names none, and the set follows from whatever geometry `czech-plots` holds, so correcting that stand-in bounding box to the real plot coordinates sharpens this constraint too. The scheme is the one needing owner confirmation: biogeographical regions, Koppen-Geiger climate zones and EUNIS habitat classes are all plausible readings of 'ecological range' and they do not agree."
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
        "when": [{ "constraint": "ecological-range", "test": "different-class-from" }],
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
    }
  },
  "outputs": {
    "trained_growth_model": {
      "type": "File"
    }
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
        "value": {
          "scheme": "eea-biogeographical-regions",
          "sameClassAs": "czech-plots"
        },
        "transferabilityNotes": "Question 7: results are 'valid mainly within a comparable ecological range'. That is an analogy to where the model was calibrated, not an extent, so it is stated as one: the target must share the biogeographical region of `czech-plots`. No region is named here on purpose \u2014 the source names none, and the set follows from whatever geometry `czech-plots` holds, so correcting that stand-in bounding box to the real plot coordinates sharpens this constraint too. The scheme is the one needing owner confirmation: biogeographical regions, Koppen-Geiger climate zones and EUNIS habitat classes are all plausible readings of 'ecological range' and they do not agree."
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
            "test": "different-class-from"
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
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/> a cwl:Workflow ;
    rdfs:label "FP-WF1 — Tree species suitability" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate_data> ;
    cwl:outputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/trained_growth_model> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns1:packages [ ns2:package "flask" ],
                [ ns2:package "lightgbm" ],
                [ ns2:package "python" ],
                [ ns2:package "gunicorn" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/decision-support-only> ;
            focal-transf-prop:note "AI model and validation are still being finalised; results are decision-support, not exact forecasts." ] ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate-data>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-plots>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/downscaled-climate-available>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/ecological-range> ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate-data> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-plots> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-alternative-published-model>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/ecological-range> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/different-class-from> ] ] ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate_data> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/downscaled-climate-available> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value "wherever downscaled climate data is available" .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/trained_growth_model> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/climate-data> dcterms:title "downscaled FOCAL climate data (current + future)" ;
    focal-transf-prop:artifactRef "/inputs/climate_data" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/ecological-range> rdfs:comment "Question 7: results are 'valid mainly within a comparable ecological range'. That is an analogy to where the model was calibrated, not an extent, so it is stated as one: the target must share the biogeographical region of `czech-plots`. No region is named here on purpose — the source names none, and the set follows from whatever geometry `czech-plots` holds, so correcting that stand-in bounding box to the real plot coordinates sharpens this constraint too. The scheme is the one needing owner confirmation: biogeographical regions, Koppen-Geiger climate zones and EUNIS habitat classes are all plausible readings of 'ecological range' and they do not agree." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:classificationScheme <https://w3id.org/ogc/hosted/focal/transferability/classification-schemes/eea-biogeographical-regions> ;
            focal-transf-prop:sameClassAs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-plots> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/growth-model> dcterms:title "trained tree growth model (LightGBM, Czech permanent sample plot data)" ;
    focal-transf-prop:artifactRef "/outputs/trained_growth_model" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-output> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf1/czech-plots> rdfs:comment "Czechia's country bounding box, standing in for the actual Czech long-term permanent sample plot network — a scattered set of monitoring locations, not a rectangle. An honest upper bound pending the real plot coordinates from the workflow owner." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"^^geo:wktLiteral ] .


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
    "envelope": [
      {
        "id": "czechia",
        "role": "derived-from",
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
    "envelope": [
      {
        "id": "czechia",
        "role": "derived-from",
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
            ns1:packages [ ns2:package "gunicorn" ],
                [ ns2:package "flask" ],
                [ ns2:package "python" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt-t5>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-codes>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/tolerances> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czechia> ;
            focal-transf-prop:rules [ rdfs:comment "Users may also override the tolerance thresholds directly, even within the source region — a separate user-configurability fact, not modelled here." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt-t5>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-codes>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/tolerances> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czechia> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/climate_registry_endpoint> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/forest_classification_context> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_codes> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species_tolerances> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/czechia> rdfs:comment "Inferred, not stated: the questionnaire gives no envelope fact directly, only that four separate reference artifacts are Czechia-specific. Value is Czechia's country bounding box. Needs owner confirmation." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/jurisdictional> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/rasdaman> dcterms:title "Rasdaman climate registry / source catalogue" ;
    focal-transf-prop:artifactRef "/inputs/climate_registry_endpoint" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/slt-t5> dcterms:title "SLT/T5 forest classification context (Czechia-specific)" ;
    focal-transf-prop:artifactRef "/inputs/forest_classification_context" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/species-codes> dcterms:title "species codes catalogue (species_codes.json)" ;
    focal-transf-prop:artifactRef "/inputs/species_codes" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf2/tolerances> dcterms:title "species tolerance thresholds (species_tolerances.json)" ;
    focal-transf-prop:artifactRef "/inputs/species_tolerances" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


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
  "id": "",
  "cwlVersion": "v1.2",
  "label": "FP-WF3 — Prediction of threatened stands",
  "requirements": {
    "SoftwareRequirement": { "packages": [{ "package": "python" }] }
  },
  "inputs": {
    "disturbance_labels": { "type": "File" },
    "eo_compositing_strategy": { "type": "string" },
    "phenology_normalization_assumptions": { "type": "string" }
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
    "eo_compositing_strategy": {
      "type": "string"
    },
    "phenology_normalization_assumptions": {
      "type": "string"
    }
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
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/> a cwl:Workflow ;
    rdfs:label "FP-WF3 — Prediction of threatened stands" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/disturbance_labels>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo_compositing_strategy>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology_normalization_assumptions> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns1:packages [ ns2:package "python" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/prototype> ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo-strategy>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/labels>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenological-regime> ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenological-regime> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Without local training labels, results should be treated as exploratory rather than blocked outright — a degraded-mode caveat, not a hard requirement." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/labels> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo-strategy> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/disturbance_labels> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo_compositing_strategy> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology_normalization_assumptions> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/eo-strategy> dcterms:title "EO sensor selection, cloud masking, temporal compositing strategy" ;
    focal-transf-prop:artifactRef "/inputs/eo_compositing_strategy" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/labels> dcterms:title "historical forest disturbance/damage labels (ground truth training data)" ;
    focal-transf-prop:artifactRef "/inputs/disturbance_labels" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenological-regime> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "a comparable phenological regime" .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/phenology> dcterms:title "regional phenology normalisation assumptions" ;
    focal-transf-prop:artifactRef "/inputs/phenology_normalization_assumptions" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf3/label-extent> rdfs:comment "More speculative than FP-WF1's or FP-WF2's: no sentence in this questionnaire names a location for the historical disturbance labels. Czechia is used as a proxy because this is a Forest Pilot workflow, and its country bounding box as the value. Needs owner confirmation before being treated as fact." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"^^geo:wktLiteral ] .


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

Geometries are coarse extents, not cadastral boundaries, and say so on the constraint. In
particular `clms-extent` is a bounding box over a coverage that is really a list of
countries, so it answers "inside" for places CLMS does not serve at all (the whole Maghreb
coast, for one). The Ukraine exclusion is carved out because it was known; the others are
not, which is what question 3 to the workflow owners is for.

`outputs` omitted. `inputs` and `steps` ids are **placeholders** invented so `artifactRef`
and `affects` have something to point at; they are not UP-WF2's real interface, and the step
bodies are stubs. The planned Heat Risk Indicator has one too, so the rule saying it cannot run
without census data names a step that exists: a record that names a component it does not have
would mislead a consumer about which components stop. Its Eurostat dependency stays an
`external-resource` with no `artifactRef`, since the data is not implemented and there is
nothing to point into.

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
        { "package": "python", "version": ["3.10", "3.11", "3.12", "3.13"] },
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
        "transferabilityNotes": "Inside the EURO-CORDEX domain the datasets are reused unchanged, by changing the area of interest."
      },
      {
        "appliesTo": ["lst"],
        "when": [{ "constraint": "eur11-domain", "test": "outside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/lst_preparation", "/steps/hotspot_characterization"],
        "mandatory": true,
        "transferabilityNotes": "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target. Which of the two applies depends on whether a substitute is obtainable, which the source does not resolve."
      },
      {
        "appliesTo": ["clms"],
        "when": [{ "constraint": "clms-extent", "test": "outside" }],
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/hotspot_characterization"],
        "mandatory": true,
        "transferabilityNotes": "Outside CLMS coverage no substitute is currently defined, and hot-spot characterization, which uses this dataset, cannot be executed."
      },
      {
        "appliesTo": ["clms"],
        "when": [{ "constraint": "clms-excluded-ukraine", "test": "inside" }],
        "actions": ["component-not-executable"],
        "affects": ["/steps/hotspot_characterization"],
        "mandatory": true,
        "transferabilityNotes": "Within the CLMS bounding extent but inside the area the product excludes: no Tree Cover Density or Imperviousness Density data exists, and no substitute is defined, so hot-spot characterization cannot be executed. A terminal outcome with no alternative offered, unlike the coverage rule above."
      },
      {
        "appliesTo": ["eurostat"],
        "triggeredBy": "different-geographic-coverage",
        "actions": ["replace-with-local-equivalent", "component-not-executable"],
        "affects": ["/steps/heat_risk_indicator"],
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
  "id": "",
  "cwlVersion": "v1.2",
  "label": "UP-WF2 \u2014 Urban hot/cool spot",
  "requirements": {
    "SoftwareRequirement": {
      "packages": [
        {
          "package": "python",
          "version": [
            "3.10",
            "3.11",
            "3.12",
            "3.13"
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
          "/steps/lst_preparation",
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
        "affects": [
          "/steps/hotspot_characterization"
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
        "affects": [
          "/steps/heat_risk_indicator"
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
@prefix cwl: <https://w3id.org/cwl/cwl#> .
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns3: <https://w3id.org/cwl/cwl#Workflow/> .
@prefix ns4: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/> a cwl:Workflow ;
    rdfs:label "UP-WF2 — Urban hot/cool spot" ;
    ns3:steps <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/heat_risk_indicator>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/hotspot_characterization>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst_preparation> ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms_tcd_imd>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst_datasets> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns1:package "rioxarray" ],
                [ ns1:package "rasterio" ],
                [ ns1:package "pandas" ],
                [ ns1:package "joblib" ],
                [ ns1:package "geopandas" ],
                [ ns1:package "python" ;
                    ns1:version "3.10",
                        "3.11",
                        "3.12",
                        "3.13" ],
                [ ns1:package "matplotlib" ],
                [ ns1:package "shapely" ],
                [ ns1:package "xarray" ],
                [ ns1:package "numpy" ] ],
        [ a cwl:NetworkAccess ;
            ns4:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eurostat>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-excluded-ukraine>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-extent>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epochs>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> ;
            focal-transf-prop:rules [ rdfs:comment "Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target. Which of the two applies depends on whether a substitute is obtainable, which the source does not resolve." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/steps/hotspot_characterization",
                        "/steps/lst_preparation" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Within the CLMS bounding extent but inside the area the product excludes: no Tree Cover Density or Imperviousness Density data exists, and no substitute is defined, so hot-spot characterization cannot be executed. A terminal outcome with no alternative offered, unlike the coverage rule above." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable> ;
                    focal-transf-prop:affects "/steps/hotspot_characterization" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-excluded-ukraine> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/inside> ] ],
                [ rdfs:comment "Outside CLMS coverage no substitute is currently defined, and hot-spot characterization, which uses this dataset, cannot be executed." ;
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
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/inside> ] ],
                [ rdfs:comment "Stated with triggeredBy rather than a cited constraint: this data is not yet implemented, so there is no envelope fact to point at. Once built, the planned Heat Risk Indicator would not be executable without it." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:affects "/steps/heat_risk_indicator" ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eurostat> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms_tcd_imd> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/epochs> rdfs:comment "Discrete temporal epochs, explicitly not a time series: one timestep per epoch. 2022–2025 available at time of writing." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
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

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-excluded-ukraine> rdfs:comment "Ukraine's approximate bounding extent, which CLMS coverage excludes. Cited by a rule with test `inside`, so falling within it is what makes the component unexecutable. Coarse: a bounding box over Ukraine also covers parts of neighbouring countries, so this errs toward flagging a target that may in fact be covered — the safe direction for a portability check, but it needs the authoritative CLMS geometry before it is relied on." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((22.1 44.4,40.2 44.4,40.2 52.4,22.1 52.4,22.1 44.4))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms-extent> rdfs:comment "CLMS product coverage, as a coarse bounding extent rather than a country-by-country outline: the precise boundary is a property of the CLMS product and is better dereferenced from CLMS than restated approximately here. The product's exclusion of Ukraine is a separate constraint (`clms-excluded-ukraine`) rather than a hole in this one — an exclusion carved into a geometry is invisible to a reader and easy to lose in simplification, whereas a named constraint a rule cites is neither." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-25 34,45 34,45 72,-25 72,-25 34))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eurostat> dcterms:title "Eurostat census / socio-economic data (planned Heat Risk Indicator)" ;
    rdfs:comment "Not yet implemented; the envisaged replacement should follow a schema compatible with Eurostat's." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/clms> dcterms:title "CLMS Tree Cover Density / Imperviousness Density" ;
    focal-transf-prop:artifactRef "/inputs/clms_tcd_imd" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/eur11-domain> rdfs:comment "The EUR-11 EURO-CORDEX domain's published approximate rectangular extent (about 22W–45E, 27N–72N), not its exact rotated-pole grid footprint, which is not a rectangle in true lat/lon at all. A deliberate simplification." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf2/lst> dcterms:title "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)" ;
    focal-transf-prop:artifactRef "/inputs/lst_datasets" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


```


### UP-WF1 — Regional climate change (an empty envelope, stated deliberately)
The thinnest questionnaire in the corpus, and the reason `envelope` has no minimum. Questions
8, 9 and 10 are answered "Nothing", "Nothing" and "All parts are portable"; this example
records exactly that and nothing more.

**An empty `envelope` and an empty `rules` are the claim here, not a shortfall.** Under the
closed-world default — rules are exceptions, silence means reuse — the two empty arrays say
that the delivery was assessed and carries no validity boundary and no adaptation step. That
is a strong claim, and the statement's `transferabilityNotes` says plainly that it is the
source's claim rather than a verified one: a nine-member regional climate ensemble almost
certainly does have conditions the questionnaire did not surface. Until the owner confirms,
the honest record is the answer as given, marked as unverified, rather than a boundary
invented to make the entry look substantial.

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
workflow's own account, no process to package.

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

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/> a cwl:Workflow ;
    rdfs:label "UP-WF1 — Regional climate change" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus_ensemble> ;
    cwl:outputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/climate_indices> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns1:package "python" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/precomputed-delivery> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:transferability [ rdfs:comment "Both arrays are empty deliberately, not for want of an entry. The questionnaire answers questions 8, 9 and 10 with 'Nothing', 'Nothing' and 'All parts are portable', so this states no validity boundary and no adaptation step. Two caveats travel with that. First, it is the source's claim and not a verified one: a nine-member regional climate ensemble delivered as precomputed indices very likely does carry conditions this questionnaire did not ask about, and the owner has been asked to confirm or correct the emptiness. Second, question 7 states that timeslices are represented as Global Warming Levels rather than calendar periods, which is a genuine temporal fact but not one this envelope can hold: no specific level is named in the source, and the scenario-marker value takes a level, not the assertion that levels are the indexing scheme. Naming one would be fabricating a slice." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf1/nukleus-ensemble> ] .

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
the Czech national climate-zone scheme, so their boundary is `jurisdictional` and its role is
`valid-for`: outside it a local or national scheme applies instead. The Rasdaman collections
are a data footprint, so their boundary is `spatial` and its role is `can-run-on`: outside it
there is simply nothing to read. Both are approximated by Czechia's bounding box and both are
inferred rather than stated, which is recorded on each constraint. Collapsing them into one
would lose the fact that a target could satisfy either without satisfying the other — an
instance with the Czech scheme but no Rasdaman coverage needs a datacube, not a new
classification.

**The third constraint is prose on purpose.** Question 7's assumption that "Quitt-inspired
thresholds are meaningful for the target area" is a judgement, not an extent, and wrapping it
in coordinates it does not have would make it look decidable when it is not. Cited by the
same rule as the jurisdictional boundary, so the rule fires on either.

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
    "envelope": [
      {
        "id": "czech-zone-scheme",
        "role": "valid-for",
        "dimension": "jurisdictional",
        "value": { "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))" },
        "transferabilityNotes": "The Quitt classification is the Czech national forest climate-zone scheme, so this is a scheme boundary rather than a data footprint: question 9 says thresholds, labels and metadata 'should be adapted to local or national classification schemes'. Value is Czechia's country bounding box. Inferred — the questionnaire names Quitt and 'Czech climate-zone definitions' but never states an extent — and needs owner confirmation."
      },
      {
        "id": "rasdaman-collections",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))" },
        "transferabilityNotes": "Where the current Rasdaman annual-indicator collections hold data. Same approximated geometry as `czech-zone-scheme` and a different fact: this one is about what can be read, that one about what the classification means. Question 9 says the registry and source catalogue 'would need to reference the target region'. Inferred extent; needs owner confirmation."
      },
      {
        "id": "quitt-meaningful",
        "role": "valid-for",
        "dimension": "climatic",
        "value": {
          "scheme": "koppen-geiger",
          "sameClassAs": "czech-zone-scheme"
        },
        "transferabilityNotes": "Question 7's assumption that Quitt-inspired thresholds are meaningful for the target area. A claim about climatic similarity to where the scheme was built, which no extent settles but a climate classification does: the target must share the Koppen-Geiger class of the area the Quitt scheme covers. Koppen is the apt scheme because Quitt's own zones are a Czech regional climate classification of the same kind. No class is enumerated: Koppen publishes no term identifiers, and the source names no zone."
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
        "transferabilityNotes": "Question 9: 'Climate-zone thresholds, labels and metadata should be adapted to local or national classification schemes.' Thresholds and the metadata that describes them move together — adapting one without the other leaves the zone descriptions naming classes the thresholds no longer produce."
      },
      {
        "appliesTo": ["quitt-limits"],
        "when": [{ "constraint": "quitt-meaningful", "test": "outside" }],
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "The second, independent trigger for the same substitution: question 7 assumes Quitt-inspired thresholds are meaningful for the target area, and a target inside Czechia's borders but climatically unlike the areas the scheme was built around fails that assumption without leaving the jurisdiction. A separate rule rather than a second condition on the one above, because either alone suffices and `when` is conjunctive."
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
    "envelope": [
      {
        "id": "czech-zone-scheme",
        "role": "valid-for",
        "dimension": "jurisdictional",
        "value": {
          "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"
        },
        "transferabilityNotes": "The Quitt classification is the Czech national forest climate-zone scheme, so this is a scheme boundary rather than a data footprint: question 9 says thresholds, labels and metadata 'should be adapted to local or national classification schemes'. Value is Czechia's country bounding box. Inferred \u2014 the questionnaire names Quitt and 'Czech climate-zone definitions' but never states an extent \u2014 and needs owner confirmation."
      },
      {
        "id": "rasdaman-collections",
        "role": "can-run-on",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"
        },
        "transferabilityNotes": "Where the current Rasdaman annual-indicator collections hold data. Same approximated geometry as `czech-zone-scheme` and a different fact: this one is about what can be read, that one about what the classification means. Question 9 says the registry and source catalogue 'would need to reference the target region'. Inferred extent; needs owner confirmation."
      },
      {
        "id": "quitt-meaningful",
        "role": "valid-for",
        "dimension": "climatic",
        "value": {
          "scheme": "koppen-geiger",
          "sameClassAs": "czech-zone-scheme"
        },
        "transferabilityNotes": "Question 7's assumption that Quitt-inspired thresholds are meaningful for the target area. A claim about climatic similarity to where the scheme was built, which no extent settles but a climate classification does: the target must share the Koppen-Geiger class of the area the Quitt scheme covers. Koppen is the apt scheme because Quitt's own zones are a Czech regional climate classification of the same kind. No class is enumerated: Koppen publishes no term identifiers, and the source names no zone."
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
        "transferabilityNotes": "Question 9: 'Climate-zone thresholds, labels and metadata should be adapted to local or national classification schemes.' Thresholds and the metadata that describes them move together \u2014 adapting one without the other leaves the zone descriptions naming classes the thresholds no longer produce."
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
        "transferabilityNotes": "The second, independent trigger for the same substitution: question 7 assumes Quitt-inspired thresholds are meaningful for the target area, and a target inside Czechia's borders but climatically unlike the areas the scheme was built around fails that assumption without leaving the jurisdiction. A separate rule rather than a second condition on the one above, because either alone suffices and `when` is conjunctive."
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
@prefix ns1: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns3: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/> a cwl:Workflow ;
    rdfs:label "FP-WF5 — Map of climatic zones" ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_metadata>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_source_catalogue>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_zone_thresholds> ;
    cwl:requirements [ a cwl:SoftwareRequirement ;
            ns2:packages [ ns3:package "python" ],
                [ ns3:package "flask" ] ],
        [ a cwl:NetworkAccess ;
            ns1:networkAccess true ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:transferability [ focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate-metadata>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-registry>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/validation-reference> ;
            focal-transf-prop:envelope <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/czech-zone-scheme>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-meaningful>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-collections> ;
            focal-transf-prop:rules [ rdfs:comment "Question 9: 'Validation should use local meteorological observations or accepted climate maps where available.' Non-mandatory because the source qualifies it with 'where available'. Skipping it does not stop the workflow: it produces zone maps from thresholds that have been adapted but never checked against anything in the target area, so the classification should be treated as indicative and the fuzzy match scores not compared against those from the Czech setup." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/validation-reference> ;
                    focal-transf-prop:mandatory false ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/czech-zone-scheme> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 9: 'Climate-zone thresholds, labels and metadata should be adapted to local or national classification schemes.' Thresholds and the metadata that describes them move together — adapting one without the other leaves the zone descriptions naming classes the thresholds no longer produce." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate-metadata>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/czech-zone-scheme> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "The second, independent trigger for the same substitution: question 7 assumes Quitt-inspired thresholds are meaningful for the target area, and a target inside Czechia's borders but climatically unlike the areas the scheme was built around fails that assumption without leaving the jurisdiction. A separate rule rather than a second condition on the one above, because either alone suffices and `when` is conjunctive." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-meaningful> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ],
                [ rdfs:comment "Question 9: the registry and source catalogue 'would need to reference the target region'. Question 8 accepts 'Rasdaman or equivalent annual climate-indicator data', so an equivalent datacube service satisfies this — the substitution is of the collections the catalogue points at, not necessarily of Rasdaman itself." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-registry> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-collections> ;
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_metadata> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_source_catalogue> sld:type xsd:string .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate_zone_thresholds> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/climate-metadata> dcterms:title "climate metadata file (indicator definitions and descriptions)" ;
    focal-transf-prop:artifactRef "/inputs/climate_metadata" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-meaningful> rdfs:comment "Question 7's assumption that Quitt-inspired thresholds are meaningful for the target area. A claim about climatic similarity to where the scheme was built, which no extent settles but a climate classification does: the target must share the Koppen-Geiger class of the area the Quitt scheme covers. Koppen is the apt scheme because Quitt's own zones are a Czech regional climate classification of the same kind. No class is enumerated: Koppen publishes no term identifiers, and the source names no zone." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:classificationScheme <https://w3id.org/ogc/hosted/focal/transferability/classification-schemes/koppen-geiger> ;
            focal-transf-prop:sameClassAs <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/czech-zone-scheme> ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-collections> rdfs:comment "Where the current Rasdaman annual-indicator collections hold data. Same approximated geometry as `czech-zone-scheme` and a different fact: this one is about what can be read, that one about what the classification means. Question 9 says the registry and source catalogue 'would need to reference the target region'. Inferred extent; needs owner confirmation." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/rasdaman-registry> dcterms:title "Rasdaman collection registry and climate source catalogue" ;
    focal-transf-prop:artifactRef "/inputs/climate_source_catalogue" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/validation-reference> dcterms:title "local meteorological observations or accepted climate maps, for validating the adapted classification" ;
    rdfs:comment "Not an input of the current workflow: question 9 recommends it as the way to check an adapted classification, so it enters the model only on transfer. Declared as an external resource with no pointer for that reason." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/quitt-limits> dcterms:title "Quitt-limit JSON climate-zone threshold definitions (thresholds, labels, zone descriptions)" ;
    focal-transf-prop:artifactRef "/inputs/climate_zone_thresholds" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf5/czech-zone-scheme> rdfs:comment "The Quitt classification is the Czech national forest climate-zone scheme, so this is a scheme boundary rather than a data footprint: question 9 says thresholds, labels and metadata 'should be adapted to local or national classification schemes'. Value is Czechia's country bounding box. Inferred — the questionnaire names Quitt and 'Czech climate-zone definitions' but never states an extent — and needs owner confirmation." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/jurisdictional> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"^^geo:wktLiteral ] .


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
the computation does not degrade on a Lambert-conformal grid, it does not run. That is the
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
JRC vulnerability index is at NUTS3 level, "coarser than the precipitation grid and does not
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
        { "package": "python", "version": ["3.10", "3.11", "3.12", "3.13"] },
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
    "envelope": [
      {
        "id": "dwd-stations",
        "role": "derived-from",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((5.87 47.27,15.04 47.27,15.04 55.06,5.87 55.06,5.87 47.27))" },
        "transferabilityNotes": "Germany's country bounding box, standing in for the DWD station network the 6-hour and 12-hour percentile thresholds were pre-computed from. A scattered set of stations, not a rectangle, so this is an upper bound; and station networks are dense in some regions and sparse in others, which a bounding box cannot show at all."
      },
      {
        "id": "eobs-extent",
        "role": "derived-from",
        "dimension": "spatial",
        "value": { "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))" },
        "transferabilityNotes": "The E-OBS domain's published approximate extent (about 25W-45E, 25N-71.5N), from which the 1-day and 7-day percentile thresholds were pre-computed. A coarse rectangle: E-OBS's actual land coverage is neither rectangular nor uniform in station density."
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
        "value": { "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))" },
        "transferabilityNotes": "Question 9: 'All input datasets are covering EU.' Approximated by the E-OBS extent, which is the widest of the sources involved. Deliberately coarse and known to be too generous: this is really the intersection of E-OBS, the NUKLEUS EUR-11 domain, the Local Climate Zone, imperviousness and population layers, and a NUTS3 vulnerability index that stops at the EU's borders. The individual footprints were not stated; the union bounding box answers 'inside' for places at least one input does not reach. Needs owner confirmation before it is relied on."
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
        "transferabilityNotes": "Contextual overlay only: question 4 is explicit that exposure does not enter the calculation. Left ungoverned by any rule, which under the closed-world default reads as reusable unchanged, and here that is right for the wrong reason. Question 9 says the workflow offers no way to substitute it: 'If users want to use their own exposure or vulnerability data, since current workflow is no option for it.' That is a standing limitation of the interface, not an outcome triggered by a target falling outside a boundary, and the model has no shape for it — `when` and `triggeredBy` both assume a trigger, and `component-not-executable` would say the overlay step fails, which it does not."
      },
      {
        "id": "vulnerability",
        "artifact": "vulnerability index at NUTS3 level (JRC Risk Data Hub)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/vulnerability_index",
        "transferabilityNotes": "Contextual overlay, and not substitutable, for the same reason recorded on `exposure`. Question 7 also states the index is at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. That is a relationship between the spatial supports of two artifacts, so no envelope dimension describes it and no rule is conditioned on it; it bears on how far the overlay can be read rather than on whether the workflow moves, and it is carried on that axis instead, by the workflow's `spatial-support-mismatch` qualityAnnotation."
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
        "transferabilityNotes": "Question 7: 'Other projections are not handled.' Terminal rather than a substitution, and deliberately so — a dataset on a Lambert-conformal or polar-stereographic grid does not produce worse blue spots, it produces none, because the rolling accumulation has no code path for it. Regridding to a supported grid is a preprocessing step outside this workflow, not an action it offers."
      },
      {
        "appliesTo": ["focal-stac-loader"],
        "triggeredBy": "different-dataset",
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'Since all the data is loaded from FOCAL STAC, user need a new data loader.' Stated with `triggeredBy` rather than a cited constraint because the condition is that the data comes from somewhere other than the FOCAL STAC catalogue, which is a fact about the source rather than about where the target is: a user inside the EU with their own local precipitation archive needs the new loader just as much as one outside it."
      }
    ],
    "transferabilityNotes": "Two evidenced facts from this questionnaire are recorded in notes rather than in structure, because no shape in this model holds them without misstating them: that exposure and vulnerability cannot be substituted at all (a standing limitation, not a triggered outcome); and that the choice of precipitation source gates which accumulation windows are available (a co-constraint between two CWL inputs, which CWL's own union-of-record-schemas typing is the right place for). Each is on the artifact it concerns. The NUTS3 support mismatch, previously a third note here, is now carried structurally by a `spatial-support-mismatch` qualityAnnotation."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "Question 1, in the owner's own words: the workflow does not provide the result of hydrological or hydraulic model simulation, the Blue Spot is an indicator of potentially flood-prone areas, and exposure and vulnerability are contextual layers that are not combined into a single quantitative risk score. Results support a qualitative judgement about where urban flood risk is likely to be highest; they are not a risk assessment."
    },
    {
      "dimension": "spatial-support-mismatch",
      "note": "Question 7: the JRC vulnerability index is provided at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. The overlay can therefore be read no finer than a NUTS3 region, whatever resolution the blue-spot map itself carries, and NUTS3 units straddling the AOI edge are only partly covered. This holds in the source deployment as much as in any target: it bounds how far a result can be read, not whether the workflow moves."
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
            "3.10",
            "3.11",
            "3.12",
            "3.13"
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
    "envelope": [
      {
        "id": "dwd-stations",
        "role": "derived-from",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((5.87 47.27,15.04 47.27,15.04 55.06,5.87 55.06,5.87 47.27))"
        },
        "transferabilityNotes": "Germany's country bounding box, standing in for the DWD station network the 6-hour and 12-hour percentile thresholds were pre-computed from. A scattered set of stations, not a rectangle, so this is an upper bound; and station networks are dense in some regions and sparse in others, which a bounding box cannot show at all."
      },
      {
        "id": "eobs-extent",
        "role": "derived-from",
        "dimension": "spatial",
        "value": {
          "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"
        },
        "transferabilityNotes": "The E-OBS domain's published approximate extent (about 25W-45E, 25N-71.5N), from which the 1-day and 7-day percentile thresholds were pre-computed. A coarse rectangle: E-OBS's actual land coverage is neither rectangular nor uniform in station density."
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
          "asWKT": "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"
        },
        "transferabilityNotes": "Question 9: 'All input datasets are covering EU.' Approximated by the E-OBS extent, which is the widest of the sources involved. Deliberately coarse and known to be too generous: this is really the intersection of E-OBS, the NUKLEUS EUR-11 domain, the Local Climate Zone, imperviousness and population layers, and a NUTS3 vulnerability index that stops at the EU's borders. The individual footprints were not stated; the union bounding box answers 'inside' for places at least one input does not reach. Needs owner confirmation before it is relied on."
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
        "transferabilityNotes": "Contextual overlay only: question 4 is explicit that exposure does not enter the calculation. Left ungoverned by any rule, which under the closed-world default reads as reusable unchanged, and here that is right for the wrong reason. Question 9 says the workflow offers no way to substitute it: 'If users want to use their own exposure or vulnerability data, since current workflow is no option for it.' That is a standing limitation of the interface, not an outcome triggered by a target falling outside a boundary, and the model has no shape for it \u2014 `when` and `triggeredBy` both assume a trigger, and `component-not-executable` would say the overlay step fails, which it does not."
      },
      {
        "id": "vulnerability",
        "artifact": "vulnerability index at NUTS3 level (JRC Risk Data Hub)",
        "artifactRole": "workflow-input",
        "artifactRef": "/inputs/vulnerability_index",
        "transferabilityNotes": "Contextual overlay, and not substitutable, for the same reason recorded on `exposure`. Question 7 also states the index is at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. That is a relationship between the spatial supports of two artifacts, so no envelope dimension describes it and no rule is conditioned on it; it bears on how far the overlay can be read rather than on whether the workflow moves, and it is carried on that axis instead, by the workflow's `spatial-support-mismatch` qualityAnnotation."
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
        "transferabilityNotes": "Question 7: 'Other projections are not handled.' Terminal rather than a substitution, and deliberately so \u2014 a dataset on a Lambert-conformal or polar-stereographic grid does not produce worse blue spots, it produces none, because the rolling accumulation has no code path for it. Regridding to a supported grid is a preprocessing step outside this workflow, not an action it offers."
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
      }
    ],
    "transferabilityNotes": "Two evidenced facts from this questionnaire are recorded in notes rather than in structure, because no shape in this model holds them without misstating them: that exposure and vulnerability cannot be substituted at all (a standing limitation, not a triggered outcome); and that the choice of precipitation source gates which accumulation windows are available (a co-constraint between two CWL inputs, which CWL's own union-of-record-schemas typing is the right place for). Each is on the artifact it concerns. The NUTS3 support mismatch, previously a third note here, is now carried structurally by a `spatial-support-mismatch` qualityAnnotation."
  },
  "computationType": "deterministic-rule-based",
  "maturityStatus": "pre-operational",
  "qualityAnnotation": [
    {
      "dimension": "decision-support-only",
      "note": "Question 1, in the owner's own words: the workflow does not provide the result of hydrological or hydraulic model simulation, the Blue Spot is an indicator of potentially flood-prone areas, and exposure and vulnerability are contextual layers that are not combined into a single quantitative risk score. Results support a qualitative judgement about where urban flood risk is likely to be highest; they are not a risk assessment."
    },
    {
      "dimension": "spatial-support-mismatch",
      "note": "Question 7: the JRC vulnerability index is provided at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. The overlay can therefore be read no finer than a NUTS3 region, whatever resolution the blue-spot map itself carries, and NUTS3 units straddling the AOI edge are only partly covered. This holds in the source deployment as much as in any target: it bounds how far a result can be read, not whether the workflow moves."
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
@prefix ns1: <https://w3id.org/cwl/cwl#SoftwareRequirement/> .
@prefix ns2: <https://w3id.org/cwl/cwl#SoftwarePackage/> .
@prefix ns3: <https://w3id.org/cwl/cwl#Workflow/> .
@prefix ns4: <https://w3id.org/cwl/cwl#NetworkAccess/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sld: <https://w3id.org/cwl/salad#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/> a cwl:Workflow ;
    rdfs:label "UP-WF3 — Urban blue-spot flood risk" ;
    ns3:steps <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/accumulation>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/blue_spot_detection>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_overlay>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_overlay> ;
    cwl:inputs <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_layers>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/precipitation>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_daily>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_subdaily>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_index> ;
    cwl:requirements [ a cwl:NetworkAccess ;
            ns4:networkAccess true ],
        [ a cwl:SoftwareRequirement ;
            ns1:packages [ ns2:package "numpy" ],
                [ ns2:package "rasterio" ],
                [ ns2:package "xarray" ],
                [ ns2:package "pandas" ],
                [ ns2:package "python" ;
                    ns2:version "3.10",
                        "3.11",
                        "3.12",
                        "3.13" ] ] ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/pre-operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/spatial-support-mismatch> ;
            focal-transf-prop:note "Question 7: the JRC vulnerability index is provided at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. The overlay can therefore be read no finer than a NUTS3 region, whatever resolution the blue-spot map itself carries, and NUTS3 units straddling the AOI edge are only partly covered. This holds in the source deployment as much as in any target: it bounds how far a result can be read, not whether the workflow moves." ],
        [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/decision-support-only> ;
            focal-transf-prop:note "Question 1, in the owner's own words: the workflow does not provide the result of hydrological or hydraulic model simulation, the Blue Spot is an indicator of potentially flood-prone areas, and exposure and vulnerability are contextual layers that are not combined into a single quantitative risk score. Results support a qualitative judgement about where urban flood risk is likely to be highest; they are not a risk assessment." ] ;
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
                [ rdfs:comment "Question 7: 'Other projections are not handled.' Terminal rather than a substitution, and deliberately so — a dataset on a Lambert-conformal or polar-stereographic grid does not produce worse blue spots, it produces none, because the rolling accumulation has no code path for it. Regridding to a supported grid is a preprocessing step outside this workflow, not an action it offers." ;
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
                            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] ] ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/accumulation> cwl:in "precipitation" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/accumulated_precipitation> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#accumulation.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/blue_spot_detection> cwl:in "accumulation/accumulated_precipitation",
        "threshold_daily" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/blue_spot_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#blue_spot_detection.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/dwd-stations> rdfs:comment "Germany's country bounding box, standing in for the DWD station network the 6-hour and 12-hour percentile thresholds were pre-computed from. A scattered set of stations, not a rectangle, so this is an upper bound; and station networks are dense in some regions and sparse in others, which a bounding box cannot show at all." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((5.87 47.27,15.04 47.27,15.04 55.06,5.87 55.06,5.87 47.27))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eobs-extent> rdfs:comment "The E-OBS domain's published approximate extent (about 25W-45E, 25N-71.5N), from which the 1-day and 7-day percentile thresholds were pre-computed. A coarse rectangle: E-OBS's actual land coverage is neither rectangular nor uniform in station density." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/derived-from> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"^^geo:wktLiteral ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure> dcterms:title "exposure layers (Local Climate Zones, imperviousness, population)" ;
    rdfs:comment "Contextual overlay only: question 4 is explicit that exposure does not enter the calculation. Left ungoverned by any rule, which under the closed-world default reads as reusable unchanged, and here that is right for the wrong reason. Question 9 says the workflow offers no way to substitute it: 'If users want to use their own exposure or vulnerability data, since current workflow is no option for it.' That is a standing limitation of the interface, not an outcome triggered by a target falling outside a boundary, and the model has no shape for it — `when` and `triggeredBy` both assume a trigger, and `component-not-executable` would say the overlay step fails, which it does not." ;
    focal-transf-prop:artifactRef "/inputs/exposure_layers" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_layers> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_overlay> cwl:in "blue_spot_detection/blue_spot_map",
        "exposure_layers" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/exposure_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#exposure_overlay.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_daily> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/threshold_subdaily> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability> dcterms:title "vulnerability index at NUTS3 level (JRC Risk Data Hub)" ;
    rdfs:comment "Contextual overlay, and not substitutable, for the same reason recorded on `exposure`. Question 7 also states the index is at NUTS3 level, 'coarser than the precipitation grid and does not align exactly with the AOI boundary'. That is a relationship between the spatial supports of two artifacts, so no envelope dimension describes it and no rule is conditioned on it; it bears on how far the overlay can be read rather than on whether the workflow moves, and it is carried on that axis instead, by the workflow's `spatial-support-mismatch` qualityAnnotation." ;
    focal-transf-prop:artifactRef "/inputs/vulnerability_index" ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_index> sld:type cwl:File .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_overlay> cwl:in "blue_spot_detection/blue_spot_map",
        "vulnerability_index" ;
    cwl:out <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/vulnerability_map> ;
    cwl:run <https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/#vulnerability_overlay.cwl> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/up-wf3/eu-input-coverage> rdfs:comment "Question 9: 'All input datasets are covering EU.' Approximated by the E-OBS extent, which is the widest of the sources involved. Deliberately coarse and known to be too generous: this is really the intersection of E-OBS, the NUKLEUS EUR-11 domain, the Local Climate Zone, imperviousness and population layers, and a NUTS3 vulnerability index that stops at the EU's borders. The individual footprints were not stated; the union bounding box answers 'inside' for places at least one input does not reach. Needs owner confirmation before it is relied on." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-25 25,45 25,45 71.5,-25 71.5,-25 25))"^^geo:wktLiteral ] .

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

