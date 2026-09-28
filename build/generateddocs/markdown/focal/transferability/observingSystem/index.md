
# FOCAL Transferability Observing System (Schema)

`ogc.focal.transferability.observingSystem` *v0.1*

Host for a transferability statement on something that is a sensor-data service rather than a CWL Workflow (FP-WF4, a SensLog observation store). Carries the statement and a label; deliberately no computationType, and no maturityStatus until a source states one.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

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

## Examples

### FP-WF4 — Collection of Local Data for Calibration (a SensLog observation store)
The eighth pilot workflow, and the one that is not a CWL Workflow: the owner describes a
SensLog / SensLog-OTS3 service holding local soil-sensor and meteorological-station time
series, used to compare local conditions with downscaled ERA5-Land data. There is no
Application Package to profile, so the statement hangs off an observing system instead.

**Everything here traces to a sentence in the questionnaire, and what is inferred says so.**
Five artifacts are the ones question 9 says must be replaced by local equivalents; the sixth
is the part question 10 calls portable. Question 9's own verb, "replaced by local
equivalents", is `replace-with-local-equivalent`, so no new action term is needed for the
sensor network either.

**The envelope is empty because the source states no extent, not because there is none.** No
region, period or class is named anywhere. `noConstraintsStated` is therefore not set:
that marker says the source named no boundary and no adaptation step, which is not true of
this source (question 9 names what must be replaced), and the rules are not empty anyway.

**Two rules over the same artifacts, not one.** Question 9 opens "another region or dataset",
a disjunction, and the model writes a disjunction as two rules. With no envelope to cite,
each uses the coarse `triggeredBy` form.

**Not recorded, on purpose.** No `computationType` (a store is not an executable package),
no `maturityStatus` (no source states one), no `qualityAnnotation` (question 7's "Data
quality depends on ..." is the same kind of remark FP-WF2 and FP-WF5 make about their
inputs, which the model does not treat as a caveat). Those, the calibration wording that
question 9 and question 10 seem to contradict, and where the comparison is computed, are
raised with the owner.

#### json
```json
{
  "id": "",
  "label": "FP-WF4 — Collection of Local Data for Calibration",
  "transferability": {
    "trainingRequired": false,
    "envelope": [],
    "artifacts": [
      {
        "id": "senslog-model-and-api",
        "artifact": "SensLog data model and API-based access",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Question 10: 'Portable parts are the SensLog data model, API-based access, time-series concept and calibration/validation methodology.' No rule applies, so it is reusable unchanged. The role is inferred: a specification a deployment conforms to, not something the workflow ships."
      },
      {
        "id": "sensor-network",
        "artifact": "physical sensor network (local soil sensors and meteorological stations)",
        "artifactRole": "infrastructure",
        "transferabilityNotes": "Question 7: 'the physical sensor network and field procedures are site-specific'. Question 9: 'The sensor network, station metadata, observed properties, calibration rules and target climate datasets would need to be replaced by local equivalents'. Question 8 allows 'sensor units or existing observation data', so installing new sensors is not the only way to satisfy the replacement; the source does not say which is expected."
      },
      {
        "id": "station-metadata",
        "artifact": "station metadata",
        "artifactRole": "workflow-input",
        "transferabilityNotes": "Question 8: 'metadata for stations and observed properties'. Role inferred; there is no executable description to point into."
      },
      {
        "id": "observed-properties",
        "artifact": "observed properties",
        "artifactRole": "workflow-input",
        "transferabilityNotes": "Question 8: 'metadata for stations and observed properties'. Role inferred."
      },
      {
        "id": "calibration-rules",
        "artifact": "calibration rules",
        "artifactRole": "workflow-input",
        "transferabilityNotes": "Question 9 says these must be replaced; question 10 says the 'calibration/validation methodology' is portable. The two may be consistent (the method carries over, the rules are local) but the source does not say so; asked of the owner."
      },
      {
        "id": "target-climate-datasets",
        "artifact": "target climate datasets",
        "artifactRole": "workflow-input",
        "transferabilityNotes": "Question 8: 'matching climate or hydrological datasets for comparison'. Question 10 lists 'selected comparison datasets' as project-specific. Question 1 names downscaled ERA5-Land as the data compared with; the source does not say whether another FOCAL workflow produces it."
      }
    ],
    "rules": [
      {
        "appliesTo": ["sensor-network", "station-metadata", "observed-properties", "calibration-rules", "target-climate-datasets"],
        "triggeredBy": "different-geographic-coverage",
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'What would need to change to apply it to another region or dataset?' answered with 'would need to be replaced by local equivalents'. The region half of that disjunction; no extent is stated, so there is no envelope constraint to cite."
      },
      {
        "appliesTo": ["sensor-network", "station-metadata", "observed-properties", "calibration-rules", "target-climate-datasets"],
        "triggeredBy": "different-dataset",
        "actions": ["replace-with-local-equivalent"],
        "mandatory": true,
        "transferabilityNotes": "The dataset half of question 9's 'another region or dataset'. The source does not separate which artifacts each half applies to, so both rules list all five."
      }
    ],
    "transferabilityNotes": "Every fact here is from the FP-WF4 questionnaire; inferences are marked as such on the entry they affect. The envelope is empty because the source names no region, period or class, which is not a claim that the results are valid everywhere. Question 5 gives 'No ML training is required.', hence trainingRequired false. Question 7: 'The workflow assumes that local sensors are installed, maintained and correctly described by metadata. Data quality depends on sensor calibration, measurement depth, temporal coverage and gap handling.' Recorded here as an assumption and a dependency, not as a quality annotation. Question 9 adds: 'Interpretation of soil moisture differences should be adapted to local soil, rooting depth, stand structure and management context.' Whether that is a validity boundary or only advice is not stated. Question 10 lists as project-specific 'current sensor deployments, credentials, backend routing, FOCAL integration settings and selected comparison datasets'; only the datasets are also in question 9's replacement list, so no rule is recorded for the rest, although question 8 says a new user needs 'access credentials/API endpoints'. Where the comparison with ERA5-Land is computed (inside SensLog, in the Forest backend, or in the web app) is not stated."
  }
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/observingSystem/context.jsonld",
  "id": "",
  "label": "FP-WF4 \u2014 Collection of Local Data for Calibration",
  "transferability": {
    "trainingRequired": false,
    "envelope": [],
    "artifacts": [
      {
        "id": "senslog-model-and-api",
        "artifact": "SensLog data model and API-based access",
        "artifactRole": "external-resource",
        "transferabilityNotes": "Question 10: 'Portable parts are the SensLog data model, API-based access, time-series concept and calibration/validation methodology.' No rule applies, so it is reusable unchanged. The role is inferred: a specification a deployment conforms to, not something the workflow ships."
      },
      {
        "id": "sensor-network",
        "artifact": "physical sensor network (local soil sensors and meteorological stations)",
        "artifactRole": "infrastructure",
        "transferabilityNotes": "Question 7: 'the physical sensor network and field procedures are site-specific'. Question 9: 'The sensor network, station metadata, observed properties, calibration rules and target climate datasets would need to be replaced by local equivalents'. Question 8 allows 'sensor units or existing observation data', so installing new sensors is not the only way to satisfy the replacement; the source does not say which is expected."
      },
      {
        "id": "station-metadata",
        "artifact": "station metadata",
        "artifactRole": "workflow-input",
        "transferabilityNotes": "Question 8: 'metadata for stations and observed properties'. Role inferred; there is no executable description to point into."
      },
      {
        "id": "observed-properties",
        "artifact": "observed properties",
        "artifactRole": "workflow-input",
        "transferabilityNotes": "Question 8: 'metadata for stations and observed properties'. Role inferred."
      },
      {
        "id": "calibration-rules",
        "artifact": "calibration rules",
        "artifactRole": "workflow-input",
        "transferabilityNotes": "Question 9 says these must be replaced; question 10 says the 'calibration/validation methodology' is portable. The two may be consistent (the method carries over, the rules are local) but the source does not say so; asked of the owner."
      },
      {
        "id": "target-climate-datasets",
        "artifact": "target climate datasets",
        "artifactRole": "workflow-input",
        "transferabilityNotes": "Question 8: 'matching climate or hydrological datasets for comparison'. Question 10 lists 'selected comparison datasets' as project-specific. Question 1 names downscaled ERA5-Land as the data compared with; the source does not say whether another FOCAL workflow produces it."
      }
    ],
    "rules": [
      {
        "appliesTo": [
          "sensor-network",
          "station-metadata",
          "observed-properties",
          "calibration-rules",
          "target-climate-datasets"
        ],
        "triggeredBy": "different-geographic-coverage",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "Question 9: 'What would need to change to apply it to another region or dataset?' answered with 'would need to be replaced by local equivalents'. The region half of that disjunction; no extent is stated, so there is no envelope constraint to cite."
      },
      {
        "appliesTo": [
          "sensor-network",
          "station-metadata",
          "observed-properties",
          "calibration-rules",
          "target-climate-datasets"
        ],
        "triggeredBy": "different-dataset",
        "actions": [
          "replace-with-local-equivalent"
        ],
        "mandatory": true,
        "transferabilityNotes": "The dataset half of question 9's 'another region or dataset'. The source does not separate which artifacts each half applies to, so both rules list all five."
      }
    ],
    "transferabilityNotes": "Every fact here is from the FP-WF4 questionnaire; inferences are marked as such on the entry they affect. The envelope is empty because the source names no region, period or class, which is not a claim that the results are valid everywhere. Question 5 gives 'No ML training is required.', hence trainingRequired false. Question 7: 'The workflow assumes that local sensors are installed, maintained and correctly described by metadata. Data quality depends on sensor calibration, measurement depth, temporal coverage and gap handling.' Recorded here as an assumption and a dependency, not as a quality annotation. Question 9 adds: 'Interpretation of soil moisture differences should be adapted to local soil, rooting depth, stand structure and management context.' Whether that is a validity boundary or only advice is not stated. Question 10 lists as project-specific 'current sensor deployments, credentials, backend routing, FOCAL integration settings and selected comparison datasets'; only the datasets are also in question 9's replacement list, so no rule is recorded for the rest, although question 8 says a new user needs 'access credentials/API endpoints'. Where the comparison with ERA5-Land is computed (inside SensLog, in the Forest backend, or in the web app) is not stated."
  }
}
```

#### ttl
```ttl
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/> rdfs:label "FP-WF4 — Collection of Local Data for Calibration" ;
    focal-transf-prop:transferability [ rdfs:comment "Every fact here is from the FP-WF4 questionnaire; inferences are marked as such on the entry they affect. The envelope is empty because the source names no region, period or class, which is not a claim that the results are valid everywhere. Question 5 gives 'No ML training is required.', hence trainingRequired false. Question 7: 'The workflow assumes that local sensors are installed, maintained and correctly described by metadata. Data quality depends on sensor calibration, measurement depth, temporal coverage and gap handling.' Recorded here as an assumption and a dependency, not as a quality annotation. Question 9 adds: 'Interpretation of soil moisture differences should be adapted to local soil, rooting depth, stand structure and management context.' Whether that is a validity boundary or only advice is not stated. Question 10 lists as project-specific 'current sensor deployments, credentials, backend routing, FOCAL integration settings and selected comparison datasets'; only the datasets are also in question 9's replacement list, so no rule is recorded for the rest, although question 8 says a new user needs 'access credentials/API endpoints'. Where the comparison with ERA5-Land is computed (inside SensLog, in the Forest backend, or in the web app) is not stated." ;
            focal-transf-prop:artifacts <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/calibration-rules>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/observed-properties>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/senslog-model-and-api>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/sensor-network>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/station-metadata>,
                <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/target-climate-datasets> ;
            focal-transf-prop:rules [ rdfs:comment "Question 9: 'What would need to change to apply it to another region or dataset?' answered with 'would need to be replaced by local equivalents'. The region half of that disjunction; no extent is stated, so there is no envelope constraint to cite." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/calibration-rules>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/observed-properties>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/sensor-network>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/station-metadata>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/target-climate-datasets> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ],
                [ rdfs:comment "The dataset half of question 9's 'another region or dataset'. The source does not separate which artifacts each half applies to, so both rules list all five." ;
                    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/calibration-rules>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/observed-properties>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/sensor-network>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/station-metadata>,
                        <https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/target-climate-datasets> ;
                    focal-transf-prop:mandatory true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-dataset> ] ;
            focal-transf-prop:trainingRequired false ] .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/senslog-model-and-api> dcterms:title "SensLog data model and API-based access" ;
    rdfs:comment "Question 10: 'Portable parts are the SensLog data model, API-based access, time-series concept and calibration/validation methodology.' No rule applies, so it is reusable unchanged. The role is inferred: a specification a deployment conforms to, not something the workflow ships." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/external-resource> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/calibration-rules> dcterms:title "calibration rules" ;
    rdfs:comment "Question 9 says these must be replaced; question 10 says the 'calibration/validation methodology' is portable. The two may be consistent (the method carries over, the rules are local) but the source does not say so; asked of the owner." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/observed-properties> dcterms:title "observed properties" ;
    rdfs:comment "Question 8: 'metadata for stations and observed properties'. Role inferred." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/sensor-network> dcterms:title "physical sensor network (local soil sensors and meteorological stations)" ;
    rdfs:comment "Question 7: 'the physical sensor network and field procedures are site-specific'. Question 9: 'The sensor network, station metadata, observed properties, calibration rules and target climate datasets would need to be replaced by local equivalents'. Question 8 allows 'sensor units or existing observation data', so installing new sensors is not the only way to satisfy the replacement; the source does not say which is expected." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/infrastructure> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/station-metadata> dcterms:title "station metadata" ;
    rdfs:comment "Question 8: 'metadata for stations and observed properties'. Role inferred; there is no executable description to point into." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/fp-wf4/target-climate-datasets> dcterms:title "target climate datasets" ;
    rdfs:comment "Question 8: 'matching climate or hydrological datasets for comparison'. Question 10 lists 'selected comparison datasets' as project-specific. Question 1 names downscaled ERA5-Land as the data compared with; the source does not say whether another FOCAL workflow produces it." ;
    focal-transf-prop:artifactRole <https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/workflow-input> .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Observing System
description: "A sibling of `ogc.focal.transferability.workflow` for a pilot component
  that is not a CWL Workflow: a sensor-data service (FP-WF4's SensLog / SensLog-OTS3
  observation store) that cannot profile `CWLWorkflow`. It does one thing, which is
  to give a [`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement)
  a subject to be about.\n- `transferability` \u2014 required, one statement. Nothing
  in the statement assumes CWL. - `id`, `label` \u2014 optional identity, so the statement
  is not an anonymous node.\n**What it deliberately does not carry.** `computationType`
  describes how an executable package computes results; a service that stores and
  serves observations has no such thing, and the property is rejected here rather
  than filled with a \"not applicable\" value. `maturityStatus` is not carried either,
  because no source has stated one for this subject and the vocabulary has no way
  to say \"unknown\": it can be added, as an optional property, the day an owner states
  a maturity. `qualityAnnotation` is likewise absent until there is a caveat about
  results that is more than \"depends on its inputs\".\n"
allOf:
- type: object
  required:
  - transferability
  properties:
    id:
      $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/iri-or-curie/schema.yaml
      description: 'Identifier for the observing system, resolved against the document''s
        base URI. An empty string resolves to the base URI itself, i.e. "the system
        this document describes".

        '
      x-jsonld-id: '@id'
    label:
      type: string
      description: 'A human-readable name, in the words of the source. Uplifts to
        `rdfs:label`.

        '
      x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#label
    transferability:
      $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/transferabilityStatement/schema.yaml
      description: 'The system''s portability boundary: which artifacts it depends
        on and what must happen to each elsewhere, plus a validity envelope where
        a source states one.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/transferability
    computationType:
      not: true
x-jsonld-prefixes:
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/observingSystem/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/observingSystem/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "id": "@id",
    "label": "rdfs:label",
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
            "artifact": "dcterms:title",
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
                  "@id": "dcterms:conformsTo",
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
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "focal-transf-prop": "focal-transf:properties/",
    "dcterms": "http://purl.org/dc/terms/",
    "focal-transf": "https://w3id.org/ogc/hosted/focal/transferability/",
    "prov": "http://www.w3.org/ns/prov#",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/observingSystem/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/observingSystem`

