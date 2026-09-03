
# FOCAL Transferability Workflow (Schema)

`ogc.focal.transferability.workflow` *v0.1*

Profile of a CWL Workflow adding FOCAL's machine-readable transferability facts: validity envelope, reference/calibration-artifact adaptation rules, computation type, maturity status, temporal extent, and quality annotations.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

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

## Examples

### FP-WF1 — Tree species suitability (worked example)
FP-WF1 (Tree species suitability), the richest of the 8 FOCAL pilot workflows for this
model: three simultaneous envelope roles, an OR-set of actions on one artifact, and the
only workflow with an evidenced `qualityAnnotation` so far. Drawn from
`20260817-workflow-transferability-mapping-extraction.md`'s FP-WF1 section.

**`envelope[0].value` (2026-09-03):** now a real GeoJSON `Polygon` — Czechia's country
bounding box (12.09–18.87°E, 48.55–51.06°N, per OpenStreetMap Wiki's published bbox) —
rather than the free-text label this example originally carried, per the
`envelopeConstraint` design resolved 2026-09-03: a `spatial`/`jurisdictional` fact is a real
extent, and text can't support an automated "is my AOI inside this envelope?" check. This is
a **known approximation, not the actual sample-plot network**: the source says "Czech
long-term permanent sample plots," a scattered set of specific monitoring locations, not the
whole country — the real plot coordinates (likely the Czech National Forest Inventory or
ÚHÚL long-term research plot network) are a genuine data gap, not sourced here. The country
bbox is an honest upper bound pending that data, not a fabricated precise answer.

`temporalExtent` is deliberately omitted here: the source states a user-selected "prediction
period" with unspecified bound/granularity — no interval is fabricated for this example.
`steps`/`inputs`/`outputs` (inherited from `CWLWorkflow`) are likewise omitted; no
Application Package exists yet for this workflow to describe them from.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "FP-WF1 — Tree species suitability",
  "envelope": [
    {
      "role": "trained-on",
      "dimension": "spatial",
      "value": {
        "type": "Polygon",
        "coordinates": [
          [
            [12.09, 48.55],
            [18.87, 48.55],
            [18.87, 51.06],
            [12.09, 51.06],
            [12.09, 48.55]
          ]
        ]
      }
    },
    {
      "role": "valid-for",
      "dimension": "ecological",
      "value": "a comparable ecological range"
    },
    {
      "role": "can-run-on",
      "dimension": "climatic",
      "value": "wherever downscaled climate data is available"
    }
  ],
  "referenceArtifact": [
    {
      "artifact": "trained tree growth model (LightGBM, Czech permanent sample plot data)",
      "rules": [
        {
          "triggeredBy": "different-ecological-range",
          "actions": [
            "retrain",
            "replace-with-alternative-published-model"
          ],
          "required": true
        }
      ]
    },
    {
      "artifact": "downscaled FOCAL climate data (current + future)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    }
  ],
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
  "envelope": [
    {
      "role": "trained-on",
      "dimension": "spatial",
      "value": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              12.09,
              48.55
            ],
            [
              18.87,
              48.55
            ],
            [
              18.87,
              51.06
            ],
            [
              12.09,
              51.06
            ],
            [
              12.09,
              48.55
            ]
          ]
        ]
      }
    },
    {
      "role": "valid-for",
      "dimension": "ecological",
      "value": "a comparable ecological range"
    },
    {
      "role": "can-run-on",
      "dimension": "climatic",
      "value": "wherever downscaled climate data is available"
    }
  ],
  "referenceArtifact": [
    {
      "artifact": "trained tree growth model (LightGBM, Czech permanent sample plot data)",
      "rules": [
        {
          "triggeredBy": "different-ecological-range",
          "actions": [
            "retrain",
            "replace-with-alternative-published-model"
          ],
          "required": true
        }
      ]
    },
    {
      "artifact": "downscaled FOCAL climate data (current + future)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    }
  ],
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
@prefix dqv: <http://www.w3.org/ns/dqv#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] rdfs:label "FP-WF1 — Tree species suitability" ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:envelope [ focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
            focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
            focal-transf-prop:value [ geojson:coordinates ( ( ( 1.209e+01 4.855e+01 ) ( 1.887e+01 4.855e+01 ) ( 1.887e+01 5.106e+01 ) ( 1.209e+01 5.106e+01 ) ( 1.209e+01 4.855e+01 ) ) ) ] ],
        [ focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/climatic> ;
            focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
            focal-transf-prop:value "wherever downscaled climate data is available" ],
        [ focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
            focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
            focal-transf-prop:value "a comparable ecological range" ] ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:qualityAnnotation [ dqv:inDimension <https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/decision-support-only> ;
            focal-transf-prop:note "AI model and validation are still being finalised; results are decision-support, not exact forecasts." ] ;
    focal-transf-prop:referenceArtifact [ focal-transf-prop:artifact "trained tree growth model (LightGBM, Czech permanent sample plot data)" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-alternative-published-model>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-ecological-range> ] ],
        [ focal-transf-prop:artifact "downscaled FOCAL climate data (current + future)" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ] .


```


### FP-WF2 — Heat stress (deterministic, jurisdiction-bound reference data)
FP-WF2 (Heat stress), a deterministic/rule-based workflow whose reference data — species
tolerance thresholds, SLT/T5 forest classification, species codes, and the Rasdaman climate
registry — is uniformly Czechia-specific. Drawn from the mapping-extraction doc's FP-WF2
section, all four artifacts share the same `replace-with-local-equivalent` /
`different-geographic-coverage` pair.

The `envelope` entry below (`trained-on`/`jurisdictional`) is an inference from that shared
pattern, not a verbatim source statement the way FP-WF1's envelope entries are — the
questionnaire never states an envelope fact directly for this workflow, only that four
separate artifacts are Czechia-bound. Flag for owner confirmation before treating it as
settled. Its `value` is Czechia's country bounding box (same source and same
bbox-vs-precise-border caveat as FP-WF1's), not the free-text `"Czechia"` this example
originally carried.

`temporalExtent` is omitted for the same reason as FP-WF1: the source states a required
"time period" input with no stated bound or granularity. `steps`/`inputs`/`outputs` are
likewise omitted, pending an Application Package for this workflow.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "FP-WF2 — Heat stress",
  "envelope": [
    {
      "role": "trained-on",
      "dimension": "jurisdictional",
      "value": {
        "type": "Polygon",
        "coordinates": [
          [
            [12.09, 48.55],
            [18.87, 48.55],
            [18.87, 51.06],
            [12.09, 51.06],
            [12.09, 48.55]
          ]
        ]
      }
    }
  ],
  "referenceArtifact": [
    {
      "artifact": "species tolerance thresholds (species_tolerances.json)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true,
          "transferabilityNotes": "Users may also override thresholds directly, even within the source region — a separate user-configurability fact, not modeled here."
        }
      ]
    },
    {
      "artifact": "SLT/T5 forest classification context (Czechia-specific)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    },
    {
      "artifact": "species codes catalogue (species_codes.json)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    },
    {
      "artifact": "Rasdaman climate registry / source catalogue",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    }
  ],
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
  "envelope": [
    {
      "role": "trained-on",
      "dimension": "jurisdictional",
      "value": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              12.09,
              48.55
            ],
            [
              18.87,
              48.55
            ],
            [
              18.87,
              51.06
            ],
            [
              12.09,
              51.06
            ],
            [
              12.09,
              48.55
            ]
          ]
        ]
      }
    }
  ],
  "referenceArtifact": [
    {
      "artifact": "species tolerance thresholds (species_tolerances.json)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true,
          "transferabilityNotes": "Users may also override thresholds directly, even within the source region \u2014 a separate user-configurability fact, not modeled here."
        }
      ]
    },
    {
      "artifact": "SLT/T5 forest classification context (Czechia-specific)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    },
    {
      "artifact": "species codes catalogue (species_codes.json)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    },
    {
      "artifact": "Rasdaman climate registry / source catalogue",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    }
  ],
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational"
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] rdfs:label "FP-WF2 — Heat stress" ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:envelope [ focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/jurisdictional> ;
            focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
            focal-transf-prop:value [ geojson:coordinates ( ( ( 1.209e+01 4.855e+01 ) ( 1.887e+01 4.855e+01 ) ( 1.887e+01 5.106e+01 ) ( 1.209e+01 5.106e+01 ) ( 1.209e+01 4.855e+01 ) ) ) ] ] ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:referenceArtifact [ focal-transf-prop:artifact "Rasdaman climate registry / source catalogue" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ],
        [ focal-transf-prop:artifact "species tolerance thresholds (species_tolerances.json)" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:transferabilityNotes "Users may also override thresholds directly, even within the source region — a separate user-configurability fact, not modeled here." ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ],
        [ focal-transf-prop:artifact "SLT/T5 forest classification context (Czechia-specific)" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ],
        [ focal-transf-prop:artifact "species codes catalogue (species_codes.json)" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ] .


```


### FP-WF3 — Prediction of threatened stands (prototype maturity, graceful degradation)
FP-WF3 (Prediction of threatened stands), the sharpest evidenced example of a
**non-operational** workflow (`maturityStatus: prototype` — "not yet as operationally mature
as WF2 or WF5," full regression testing and validation still pending), and the only workflow
whose source explicitly describes a rule as optional-but-degrading rather than mandatory:
without local training labels, results are still produced, just "treated as exploratory."
That's `required: false` paired with `transferabilityNotes` describing the consequence, per
`transferability/rule`'s own guidance.

`envelope`'s `spatial` entry is inferred, not stated: the source never names a location for
the historical disturbance/damage labels it trains on. Because FP-WF3 is, like FP-WF1/FP-WF2,
a Forest Pilot workflow, Czechia is the same reasonable proxy used there — carried here as
the same bounding-box `Polygon`, with the same caveat plus this extra one: unlike FP-WF1/
FP-WF2, no sentence in this questionnaire actually names Czechia, so treat this value as
**more speculative than FP-WF1/FP-WF2's**, pending direct owner confirmation. The `ecological`
entry stays a string (`"a comparable phenological regime"`) — a phenological regime isn't
itself a place, per `envelopeConstraint`'s string-fallback rule for genuinely non-spatial
facts.

`temporalExtent` is omitted: source states an EO time-series "time period" with unspecified
bound. `steps`/`inputs`/`outputs` are omitted — this workflow's own questionnaire says its
"final container, API and regression-test packaging are still to be completed," so there is
no Application Package yet to describe them from, more so than for any other example here.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "FP-WF3 — Prediction of threatened stands",
  "envelope": [
    {
      "role": "trained-on",
      "dimension": "spatial",
      "value": {
        "type": "Polygon",
        "coordinates": [
          [
            [12.09, 48.55],
            [18.87, 48.55],
            [18.87, 51.06],
            [12.09, 51.06],
            [12.09, 48.55]
          ]
        ]
      }
    },
    {
      "role": "valid-for",
      "dimension": "ecological",
      "value": "a comparable phenological regime"
    }
  ],
  "referenceArtifact": [
    {
      "artifact": "historical forest disturbance/damage labels (ground truth training data)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "retrain"
          ],
          "required": false,
          "transferabilityNotes": "Without local training labels, results should be treated as exploratory rather than blocked outright — a degraded-mode caveat, not a hard requirement."
        }
      ]
    },
    {
      "artifact": "EO sensor selection, cloud masking, temporal compositing strategy",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    },
    {
      "artifact": "regional phenology normalisation assumptions",
      "rules": [
        {
          "triggeredBy": "different-ecological-range",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    }
  ],
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
  "envelope": [
    {
      "role": "trained-on",
      "dimension": "spatial",
      "value": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              12.09,
              48.55
            ],
            [
              18.87,
              48.55
            ],
            [
              18.87,
              51.06
            ],
            [
              12.09,
              51.06
            ],
            [
              12.09,
              48.55
            ]
          ]
        ]
      }
    },
    {
      "role": "valid-for",
      "dimension": "ecological",
      "value": "a comparable phenological regime"
    }
  ],
  "referenceArtifact": [
    {
      "artifact": "historical forest disturbance/damage labels (ground truth training data)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "retrain"
          ],
          "required": false,
          "transferabilityNotes": "Without local training labels, results should be treated as exploratory rather than blocked outright \u2014 a degraded-mode caveat, not a hard requirement."
        }
      ]
    },
    {
      "artifact": "EO sensor selection, cloud masking, temporal compositing strategy",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    },
    {
      "artifact": "regional phenology normalisation assumptions",
      "rules": [
        {
          "triggeredBy": "different-ecological-range",
          "actions": [
            "replace-with-local-equivalent"
          ],
          "required": true
        }
      ]
    }
  ],
  "computationType": "statistical-ml",
  "maturityStatus": "prototype"
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] rdfs:label "FP-WF3 — Prediction of threatened stands" ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/statistical-ml> ;
    focal-transf-prop:envelope [ focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
            focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
            focal-transf-prop:value "a comparable phenological regime" ],
        [ focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
            focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
            focal-transf-prop:value [ geojson:coordinates ( ( ( 1.209e+01 4.855e+01 ) ( 1.887e+01 4.855e+01 ) ( 1.887e+01 5.106e+01 ) ( 1.209e+01 5.106e+01 ) ( 1.209e+01 4.855e+01 ) ) ) ] ] ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/prototype> ;
    focal-transf-prop:referenceArtifact [ focal-transf-prop:artifact "regional phenology normalisation assumptions" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-ecological-range> ] ],
        [ focal-transf-prop:artifact "EO sensor selection, cloud masking, temporal compositing strategy" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ],
        [ focal-transf-prop:artifact "historical forest disturbance/damage labels (ground truth training data)" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
                    focal-transf-prop:required false ;
                    focal-transf-prop:transferabilityNotes "Without local training labels, results should be treated as exploratory rather than blocked outright — a degraded-mode caveat, not a hard requirement." ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ] .


```


### UP-WF2 — Urban hot/cool spot (coverage boundaries, terminal hard-fail, discrete epochs)
UP-WF2 (Urban hot/cool spot), the workflow whose source most explicitly names a
**hard-fail terminal state**: outside its reference datasets' footprint, "some workflow
components cannot be executed" at all — `component-not-executable`, alongside
`replace-with-local-equivalent`, as an OR-set on the same rule (the actual outcome depends on
whether a substitute is available or not, which this model doesn't resolve any further).

It's also the one example here with a directly evidenced, non-omitted `temporalExtent`: the
workflow operates over discrete "temporal epochs" (2022–2025 available at time of writing),
explicitly "not a time series" — a single timestep per epoch. That single-timestep framing
itself doesn't have a dedicated property yet; captured here only as the interval's practical
meaning, not a modeled fact.

`envelope`'s two entries reflect the two distinct dataset footprints named in the source
(EURO-CORDEX for the LST datasets, Europe-except-Ukraine for CLMS) rather than one shared
boundary — unlike FP-WF2/FP-WF3, these particular coverage facts *are* stated directly in
the source, not inferred, and (2026-09-03) both are now real geometry, not string, per
`envelopeConstraint`'s tightened rule that `spatial`/`jurisdictional` **must** be a GeoJSON
Geometry:

- `valid-for`/`spatial` is the EUR-11 EURO-CORDEX domain's published geographic bounding box,
  approximately 22°W–45°E, 27°N–72°N (per EURO-CORDEX/CLM-Community's own domain description)
  — the domain's stated *approximate* rectangular extent, not its exact rotated-pole grid
  footprint (which isn't a plain rectangle in true lat/lon at all), a deliberate
  simplification, not a hidden loss of precision.
- `valid-for`/`jurisdictional` (Europe, except Ukraine, per the CLMS product coverage note)
  is now a real, computed `MultiPolygon` rather than the placeholder string this example
  carried until 2026-09-03. Computed as: `union(38 of the 39 country polygons in the
  user-supplied Europe FeatureCollection, Russia excluded) − Ukraine (from
  datahub.io/core/geo-countries' `datasets/geo-countries` GitHub source, fetched directly)`,
  using Shapely 2.1 (`unary_union`, `make_valid`, `difference`). **Russia is excluded
  entirely** (2026-09-03, on request) rather than clipped to "European Russia" — that line is
  itself a contested, unsettled one, and CLMS (the dataset this envelope entry actually
  describes) never covered Russia to begin with, so full exclusion is more accurate as well
  as avoiding a needless political judgment call embedded in example data. The same pass also
  drops **French Guiana**, found only once this computation was actually run: the
  user-supplied file's `France` feature is France's full multi-part territory, including its
  South American département, which the original free-text `"Europe, except Ukraine"` string
  silently carried along unnoticed — dropped by excluding any of France's sub-polygons west of
  -20° longitude, well clear of continental France/Corsica. After unioning and differencing,
  52 small (< 0.15 deg², all border-mismatch artifacts between the two independently-sourced
  Ukraine/neighbor boundaries, confirmed by centroid clustering exclusively in the
  28–41°E/44–53°N Ukraine-border band — not real geography) sliver polygons were dropped,
  totaling 0.08% of the raw difference's area, leaving 13 genuine parts: mainland Europe,
  Scandinavia, Great Britain, Ireland, Iceland, Svalbard (3 islands), Sicily, Sardinia,
  Corsica, Zealand, and Crete. Simplified (Douglas-Peucker, tolerance 0.3°,
  topology-preserving) to 283 vertices, coordinates rounded to 3 decimal places (~110 m) to
  match — not survey-accurate, and not intended to be; an illustrative envelope extent, not a
  cadastral boundary.

The full workflow JSON (including the `MultiPolygon`) is kept in `examples/up-wf2.json` and
referenced via `ref` rather than inlined here, unlike the other three examples — a computed
geometry this size isn't practical to keep reviewable inline in this file.

`steps`/`inputs`/`outputs` are omitted, as in every other example here.

#### json
```json
{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "label": "UP-WF2 \u2014 Urban hot/cool spot",
  "envelope": [
    {
      "role": "valid-for",
      "dimension": "spatial",
      "value": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -22,
              27
            ],
            [
              45,
              27
            ],
            [
              45,
              72
            ],
            [
              -22,
              72
            ],
            [
              -22,
              27
            ]
          ]
        ]
      }
    },
    {
      "role": "valid-for",
      "dimension": "jurisdictional",
      "value": {
        "type": "MultiPolygon",
        "coordinates": [
          [
            [
              [
                -9.287,
                38.358
              ],
              [
                -9.447,
                39.392
              ],
              [
                -8.769,
                40.761
              ],
              [
                -9.393,
                43.027
              ],
              [
                -7.978,
                43.748
              ],
              [
                -1.901,
                43.423
              ],
              [
                -1.384,
                44.023
              ],
              [
                -1.194,
                46.015
              ],
              [
                -2.963,
                47.57
              ],
              [
                -4.492,
                47.955
              ],
              [
                -4.592,
                48.684
              ],
              [
                -1.617,
                48.644
              ],
              [
                -1.933,
                49.776
              ],
              [
                -0.989,
                49.347
              ],
              [
                1.339,
                50.127
              ],
              [
                1.639,
                50.947
              ],
              [
                3.83,
                51.621
              ],
              [
                4.706,
                53.092
              ],
              [
                8.122,
                53.528
              ],
              [
                8.801,
                54.021
              ],
              [
                8.12,
                55.518
              ],
              [
                8.543,
                57.11
              ],
              [
                10.58,
                57.73
              ],
              [
                10.25,
                56.89
              ],
              [
                10.912,
                56.459
              ],
              [
                9.65,
                55.47
              ],
              [
                9.94,
                54.597
              ],
              [
                10.95,
                54.364
              ],
              [
                10.939,
                54.009
              ],
              [
                12.518,
                54.47
              ],
              [
                14.12,
                53.757
              ],
              [
                17.623,
                54.852
              ],
              [
                18.696,
                54.439
              ],
              [
                22.731,
                54.328
              ],
              [
                22.758,
                54.857
              ],
              [
                21.268,
                55.19
              ],
              [
                21.09,
                56.784
              ],
              [
                22.524,
                57.753
              ],
              [
                23.318,
                57.006
              ],
              [
                24.121,
                57.026
              ],
              [
                24.429,
                58.383
              ],
              [
                23.427,
                58.613
              ],
              [
                23.34,
                59.187
              ],
              [
                27.981,
                59.475
              ],
              [
                27.42,
                58.725
              ],
              [
                27.717,
                57.792
              ],
              [
                27.288,
                57.475
              ],
              [
                28.177,
                56.169
              ],
              [
                30.874,
                55.551
              ],
              [
                30.758,
                54.812
              ],
              [
                32.694,
                53.351
              ],
              [
                31.305,
                53.074
              ],
              [
                31.786,
                52.102
              ],
              [
                30.919,
                52.059
              ],
              [
                30.551,
                51.237
              ],
              [
                25.768,
                51.929
              ],
              [
                23.594,
                51.605
              ],
              [
                24.108,
                50.541
              ],
              [
                22.666,
                49.567
              ],
              [
                22.867,
                49.01
              ],
              [
                22.133,
                48.405
              ],
              [
                24.897,
                47.71
              ],
              [
                27.752,
                48.452
              ],
              [
                29.136,
                47.968
              ],
              [
                30.132,
                46.423
              ],
              [
                28.946,
                46.455
              ],
              [
                28.202,
                45.469
              ],
              [
                29.653,
                45.341
              ],
              [
                28.838,
                44.914
              ],
              [
                27.674,
                42.578
              ],
              [
                27.997,
                42.007
              ],
              [
                26.117,
                41.827
              ],
              [
                26.604,
                41.562
              ],
              [
                26.057,
                40.824
              ],
              [
                23.715,
                40.687
              ],
              [
                24.408,
                40.125
              ],
              [
                22.626,
                40.257
              ],
              [
                23.35,
                39.19
              ],
              [
                22.973,
                38.971
              ],
              [
                24.025,
                38.22
              ],
              [
                24.04,
                37.655
              ],
              [
                23.115,
                37.92
              ],
              [
                23.41,
                37.41
              ],
              [
                22.775,
                37.305
              ],
              [
                23.154,
                36.423
              ],
              [
                21.67,
                36.845
              ],
              [
                21.12,
                38.31
              ],
              [
                19.406,
                40.251
              ],
              [
                19.372,
                41.878
              ],
              [
                16.015,
                43.507
              ],
              [
                14.902,
                45.076
              ],
              [
                14.259,
                45.234
              ],
              [
                13.952,
                44.802
              ],
              [
                13.938,
                45.591
              ],
              [
                13.142,
                45.737
              ],
              [
                12.329,
                45.382
              ],
              [
                12.589,
                44.091
              ],
              [
                15.143,
                41.955
              ],
              [
                15.926,
                41.961
              ],
              [
                15.889,
                41.541
              ],
              [
                18.48,
                40.169
              ],
              [
                18.293,
                39.811
              ],
              [
                16.87,
                40.442
              ],
              [
                16.449,
                39.795
              ],
              [
                17.171,
                39.425
              ],
              [
                17.053,
                38.903
              ],
              [
                16.101,
                37.986
              ],
              [
                15.684,
                37.909
              ],
              [
                16.109,
                38.965
              ],
              [
                15.414,
                40.048
              ],
              [
                12.107,
                41.705
              ],
              [
                10.512,
                42.931
              ],
              [
                10.2,
                43.92
              ],
              [
                8.889,
                44.366
              ],
              [
                6.529,
                43.129
              ],
              [
                4.557,
                43.4
              ],
              [
                3.1,
                43.075
              ],
              [
                3.039,
                41.892
              ],
              [
                0.811,
                41.015
              ],
              [
                -0.279,
                39.31
              ],
              [
                0.111,
                38.739
              ],
              [
                -2.146,
                36.674
              ],
              [
                -4.369,
                36.678
              ],
              [
                -5.866,
                36.03
              ],
              [
                -6.52,
                36.943
              ],
              [
                -8.899,
                36.869
              ],
              [
                -8.84,
                38.266
              ],
              [
                -9.287,
                38.358
              ]
            ]
          ],
          [
            [
              [
                8.428,
                39.172
              ],
              [
                8.16,
                40.95
              ],
              [
                9.21,
                41.21
              ],
              [
                9.81,
                40.5
              ],
              [
                9.67,
                39.177
              ],
              [
                8.428,
                39.172
              ]
            ]
          ],
          [
            [
              [
                9.39,
                43.01
              ],
              [
                9.56,
                42.152
              ],
              [
                9.23,
                41.38
              ],
              [
                8.544,
                42.257
              ],
              [
                9.39,
                43.01
              ]
            ]
          ],
          [
            [
              [
                -9.689,
                53.881
              ],
              [
                -6.734,
                55.173
              ],
              [
                -5.662,
                54.555
              ],
              [
                -6.198,
                53.868
              ],
              [
                -6.033,
                53.153
              ],
              [
                -6.789,
                52.26
              ],
              [
                -8.562,
                51.669
              ],
              [
                -9.977,
                51.82
              ],
              [
                -9.166,
                52.865
              ],
              [
                -9.689,
                53.881
              ]
            ]
          ],
          [
            [
              [
                -5.083,
                55.062
              ],
              [
                -4.719,
                55.508
              ],
              [
                -5.048,
                55.784
              ],
              [
                -5.586,
                55.311
              ],
              [
                -6.15,
                56.785
              ],
              [
                -5.787,
                57.819
              ],
              [
                -5.01,
                58.63
              ],
              [
                -3.005,
                58.635
              ],
              [
                -4.074,
                57.553
              ],
              [
                -1.959,
                57.685
              ],
              [
                -3.119,
                55.974
              ],
              [
                -2.085,
                55.91
              ],
              [
                -1.115,
                54.625
              ],
              [
                -0.43,
                54.464
              ],
              [
                0.47,
                52.93
              ],
              [
                1.682,
                52.74
              ],
              [
                1.051,
                51.807
              ],
              [
                1.45,
                51.289
              ],
              [
                0.55,
                50.766
              ],
              [
                -5.777,
                50.16
              ],
              [
                -3.415,
                51.426
              ],
              [
                -5.267,
                51.991
              ],
              [
                -4.222,
                52.301
              ],
              [
                -4.77,
                52.84
              ],
              [
                -4.58,
                53.495
              ],
              [
                -3.092,
                53.404
              ],
              [
                -2.945,
                53.985
              ],
              [
                -5.083,
                55.062
              ]
            ]
          ],
          [
            [
              [
                12.09,
                54.8
              ],
              [
                11.044,
                55.365
              ],
              [
                10.904,
                55.78
              ],
              [
                12.371,
                56.111
              ],
              [
                12.69,
                55.61
              ],
              [
                12.09,
                54.8
              ]
            ]
          ],
          [
            [
              [
                -22.763,
                63.96
              ],
              [
                -21.778,
                64.402
              ],
              [
                -23.955,
                64.891
              ],
              [
                -22.184,
                65.085
              ],
              [
                -24.326,
                65.611
              ],
              [
                -23.651,
                66.263
              ],
              [
                -22.135,
                66.41
              ],
              [
                -20.576,
                65.732
              ],
              [
                -19.057,
                66.277
              ],
              [
                -17.799,
                65.994
              ],
              [
                -16.168,
                66.527
              ],
              [
                -14.509,
                66.456
              ],
              [
                -14.74,
                65.809
              ],
              [
                -13.61,
                65.127
              ],
              [
                -14.91,
                64.364
              ],
              [
                -18.656,
                63.496
              ],
              [
                -22.763,
                63.96
              ]
            ]
          ],
          [
            [
              [
                12.431,
                37.613
              ],
              [
                12.571,
                38.126
              ],
              [
                15.52,
                38.231
              ],
              [
                15.1,
                36.62
              ],
              [
                12.431,
                37.613
              ]
            ]
          ],
          [
            [
              [
                21.37,
                64.414
              ],
              [
                17.848,
                62.749
              ],
              [
                17.12,
                61.341
              ],
              [
                18.788,
                60.082
              ],
              [
                17.869,
                58.954
              ],
              [
                16.829,
                58.72
              ],
              [
                15.88,
                56.104
              ],
              [
                14.667,
                56.201
              ],
              [
                14.101,
                55.408
              ],
              [
                12.943,
                55.362
              ],
              [
                10.357,
                59.47
              ],
              [
                8.382,
                58.313
              ],
              [
                7.049,
                58.079
              ],
              [
                5.666,
                58.588
              ],
              [
                4.992,
                61.971
              ],
              [
                10.528,
                64.486
              ],
              [
                14.761,
                67.811
              ],
              [
                19.184,
                69.817
              ],
              [
                23.024,
                70.202
              ],
              [
                24.547,
                71.03
              ],
              [
                28.166,
                71.185
              ],
              [
                31.293,
                70.454
              ],
              [
                30.005,
                70.186
              ],
              [
                31.101,
                69.558
              ],
              [
                28.592,
                69.065
              ],
              [
                28.446,
                68.365
              ],
              [
                29.977,
                67.698
              ],
              [
                29.055,
                66.944
              ],
              [
                30.218,
                65.806
              ],
              [
                29.544,
                64.949
              ],
              [
                30.445,
                64.204
              ],
              [
                30.036,
                63.553
              ],
              [
                31.516,
                62.868
              ],
              [
                30.211,
                61.78
              ],
              [
                28.07,
                60.504
              ],
              [
                22.87,
                59.846
              ],
              [
                21.322,
                60.72
              ],
              [
                21.545,
                61.705
              ],
              [
                21.059,
                62.607
              ],
              [
                22.443,
                63.818
              ],
              [
                25.398,
                65.111
              ],
              [
                25.294,
                65.534
              ],
              [
                23.903,
                66.007
              ],
              [
                22.183,
                65.724
              ],
              [
                21.214,
                65.026
              ],
              [
                21.37,
                64.414
              ]
            ]
          ],
          [
            [
              [
                17.594,
                77.638
              ],
              [
                17.118,
                76.809
              ],
              [
                15.913,
                76.77
              ],
              [
                13.763,
                77.38
              ],
              [
                14.67,
                77.736
              ],
              [
                11.222,
                78.869
              ],
              [
                10.445,
                79.652
              ],
              [
                16.991,
                80.051
              ],
              [
                21.544,
                78.956
              ],
              [
                19.027,
                78.563
              ],
              [
                18.472,
                77.827
              ],
              [
                17.594,
                77.638
              ]
            ]
          ],
          [
            [
              [
                23.7,
                35.705
              ],
              [
                25.745,
                35.18
              ],
              [
                26.29,
                35.3
              ],
              [
                24.725,
                34.92
              ],
              [
                23.515,
                35.28
              ],
              [
                23.7,
                35.705
              ]
            ]
          ],
          [
            [
              [
                24.724,
                77.854
              ],
              [
                22.49,
                77.445
              ],
              [
                20.726,
                77.677
              ],
              [
                21.416,
                77.935
              ],
              [
                20.812,
                78.255
              ],
              [
                22.884,
                78.455
              ],
              [
                24.724,
                77.854
              ]
            ]
          ],
          [
            [
              [
                17.368,
                80.319
              ],
              [
                22.919,
                80.657
              ],
              [
                27.408,
                80.056
              ],
              [
                25.925,
                79.518
              ],
              [
                23.024,
                79.4
              ],
              [
                20.075,
                79.567
              ],
              [
                17.368,
                80.319
              ]
            ]
          ]
        ]
      }
    }
  ],
  "referenceArtifact": [
    {
      "artifact": "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent",
            "component-not-executable"
          ],
          "required": true,
          "transferabilityNotes": "Inside the EURO-CORDEX domain, reuse as-is by changing the AOI. Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target."
        }
      ]
    },
    {
      "artifact": "CLMS Tree Cover Density / Imperviousness Density",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent",
            "component-not-executable"
          ],
          "required": true,
          "transferabilityNotes": "CLMS product coverage is generally limited to Europe, except Ukraine (see this workflow's `envelope`); outside it, no substitute is currently defined, and hot-spot characterization (which uses this dataset) cannot be executed."
        }
      ]
    },
    {
      "artifact": "Eurostat census / socio-economic data (planned Heat Risk Indicator)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent",
            "component-not-executable"
          ],
          "required": true,
          "transferabilityNotes": "Not yet implemented; the envisaged replacement should follow a schema compatible with Eurostat's. Once built, the source's stated consequence for unavailable data applies here too: the planned Heat Risk Indicator (risk assessment) component would not be executable without it."
        }
      ]
    }
  ],
  "temporalExtent": [
    {
      "start": "2022",
      "end": "2025"
    }
  ],
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
  "envelope": [
    {
      "role": "valid-for",
      "dimension": "spatial",
      "value": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -22,
              27
            ],
            [
              45,
              27
            ],
            [
              45,
              72
            ],
            [
              -22,
              72
            ],
            [
              -22,
              27
            ]
          ]
        ]
      }
    },
    {
      "role": "valid-for",
      "dimension": "jurisdictional",
      "value": {
        "type": "MultiPolygon",
        "coordinates": [
          [
            [
              [
                -9.287,
                38.358
              ],
              [
                -9.447,
                39.392
              ],
              [
                -8.769,
                40.761
              ],
              [
                -9.393,
                43.027
              ],
              [
                -7.978,
                43.748
              ],
              [
                -1.901,
                43.423
              ],
              [
                -1.384,
                44.023
              ],
              [
                -1.194,
                46.015
              ],
              [
                -2.963,
                47.57
              ],
              [
                -4.492,
                47.955
              ],
              [
                -4.592,
                48.684
              ],
              [
                -1.617,
                48.644
              ],
              [
                -1.933,
                49.776
              ],
              [
                -0.989,
                49.347
              ],
              [
                1.339,
                50.127
              ],
              [
                1.639,
                50.947
              ],
              [
                3.83,
                51.621
              ],
              [
                4.706,
                53.092
              ],
              [
                8.122,
                53.528
              ],
              [
                8.801,
                54.021
              ],
              [
                8.12,
                55.518
              ],
              [
                8.543,
                57.11
              ],
              [
                10.58,
                57.73
              ],
              [
                10.25,
                56.89
              ],
              [
                10.912,
                56.459
              ],
              [
                9.65,
                55.47
              ],
              [
                9.94,
                54.597
              ],
              [
                10.95,
                54.364
              ],
              [
                10.939,
                54.009
              ],
              [
                12.518,
                54.47
              ],
              [
                14.12,
                53.757
              ],
              [
                17.623,
                54.852
              ],
              [
                18.696,
                54.439
              ],
              [
                22.731,
                54.328
              ],
              [
                22.758,
                54.857
              ],
              [
                21.268,
                55.19
              ],
              [
                21.09,
                56.784
              ],
              [
                22.524,
                57.753
              ],
              [
                23.318,
                57.006
              ],
              [
                24.121,
                57.026
              ],
              [
                24.429,
                58.383
              ],
              [
                23.427,
                58.613
              ],
              [
                23.34,
                59.187
              ],
              [
                27.981,
                59.475
              ],
              [
                27.42,
                58.725
              ],
              [
                27.717,
                57.792
              ],
              [
                27.288,
                57.475
              ],
              [
                28.177,
                56.169
              ],
              [
                30.874,
                55.551
              ],
              [
                30.758,
                54.812
              ],
              [
                32.694,
                53.351
              ],
              [
                31.305,
                53.074
              ],
              [
                31.786,
                52.102
              ],
              [
                30.919,
                52.059
              ],
              [
                30.551,
                51.237
              ],
              [
                25.768,
                51.929
              ],
              [
                23.594,
                51.605
              ],
              [
                24.108,
                50.541
              ],
              [
                22.666,
                49.567
              ],
              [
                22.867,
                49.01
              ],
              [
                22.133,
                48.405
              ],
              [
                24.897,
                47.71
              ],
              [
                27.752,
                48.452
              ],
              [
                29.136,
                47.968
              ],
              [
                30.132,
                46.423
              ],
              [
                28.946,
                46.455
              ],
              [
                28.202,
                45.469
              ],
              [
                29.653,
                45.341
              ],
              [
                28.838,
                44.914
              ],
              [
                27.674,
                42.578
              ],
              [
                27.997,
                42.007
              ],
              [
                26.117,
                41.827
              ],
              [
                26.604,
                41.562
              ],
              [
                26.057,
                40.824
              ],
              [
                23.715,
                40.687
              ],
              [
                24.408,
                40.125
              ],
              [
                22.626,
                40.257
              ],
              [
                23.35,
                39.19
              ],
              [
                22.973,
                38.971
              ],
              [
                24.025,
                38.22
              ],
              [
                24.04,
                37.655
              ],
              [
                23.115,
                37.92
              ],
              [
                23.41,
                37.41
              ],
              [
                22.775,
                37.305
              ],
              [
                23.154,
                36.423
              ],
              [
                21.67,
                36.845
              ],
              [
                21.12,
                38.31
              ],
              [
                19.406,
                40.251
              ],
              [
                19.372,
                41.878
              ],
              [
                16.015,
                43.507
              ],
              [
                14.902,
                45.076
              ],
              [
                14.259,
                45.234
              ],
              [
                13.952,
                44.802
              ],
              [
                13.938,
                45.591
              ],
              [
                13.142,
                45.737
              ],
              [
                12.329,
                45.382
              ],
              [
                12.589,
                44.091
              ],
              [
                15.143,
                41.955
              ],
              [
                15.926,
                41.961
              ],
              [
                15.889,
                41.541
              ],
              [
                18.48,
                40.169
              ],
              [
                18.293,
                39.811
              ],
              [
                16.87,
                40.442
              ],
              [
                16.449,
                39.795
              ],
              [
                17.171,
                39.425
              ],
              [
                17.053,
                38.903
              ],
              [
                16.101,
                37.986
              ],
              [
                15.684,
                37.909
              ],
              [
                16.109,
                38.965
              ],
              [
                15.414,
                40.048
              ],
              [
                12.107,
                41.705
              ],
              [
                10.512,
                42.931
              ],
              [
                10.2,
                43.92
              ],
              [
                8.889,
                44.366
              ],
              [
                6.529,
                43.129
              ],
              [
                4.557,
                43.4
              ],
              [
                3.1,
                43.075
              ],
              [
                3.039,
                41.892
              ],
              [
                0.811,
                41.015
              ],
              [
                -0.279,
                39.31
              ],
              [
                0.111,
                38.739
              ],
              [
                -2.146,
                36.674
              ],
              [
                -4.369,
                36.678
              ],
              [
                -5.866,
                36.03
              ],
              [
                -6.52,
                36.943
              ],
              [
                -8.899,
                36.869
              ],
              [
                -8.84,
                38.266
              ],
              [
                -9.287,
                38.358
              ]
            ]
          ],
          [
            [
              [
                8.428,
                39.172
              ],
              [
                8.16,
                40.95
              ],
              [
                9.21,
                41.21
              ],
              [
                9.81,
                40.5
              ],
              [
                9.67,
                39.177
              ],
              [
                8.428,
                39.172
              ]
            ]
          ],
          [
            [
              [
                9.39,
                43.01
              ],
              [
                9.56,
                42.152
              ],
              [
                9.23,
                41.38
              ],
              [
                8.544,
                42.257
              ],
              [
                9.39,
                43.01
              ]
            ]
          ],
          [
            [
              [
                -9.689,
                53.881
              ],
              [
                -6.734,
                55.173
              ],
              [
                -5.662,
                54.555
              ],
              [
                -6.198,
                53.868
              ],
              [
                -6.033,
                53.153
              ],
              [
                -6.789,
                52.26
              ],
              [
                -8.562,
                51.669
              ],
              [
                -9.977,
                51.82
              ],
              [
                -9.166,
                52.865
              ],
              [
                -9.689,
                53.881
              ]
            ]
          ],
          [
            [
              [
                -5.083,
                55.062
              ],
              [
                -4.719,
                55.508
              ],
              [
                -5.048,
                55.784
              ],
              [
                -5.586,
                55.311
              ],
              [
                -6.15,
                56.785
              ],
              [
                -5.787,
                57.819
              ],
              [
                -5.01,
                58.63
              ],
              [
                -3.005,
                58.635
              ],
              [
                -4.074,
                57.553
              ],
              [
                -1.959,
                57.685
              ],
              [
                -3.119,
                55.974
              ],
              [
                -2.085,
                55.91
              ],
              [
                -1.115,
                54.625
              ],
              [
                -0.43,
                54.464
              ],
              [
                0.47,
                52.93
              ],
              [
                1.682,
                52.74
              ],
              [
                1.051,
                51.807
              ],
              [
                1.45,
                51.289
              ],
              [
                0.55,
                50.766
              ],
              [
                -5.777,
                50.16
              ],
              [
                -3.415,
                51.426
              ],
              [
                -5.267,
                51.991
              ],
              [
                -4.222,
                52.301
              ],
              [
                -4.77,
                52.84
              ],
              [
                -4.58,
                53.495
              ],
              [
                -3.092,
                53.404
              ],
              [
                -2.945,
                53.985
              ],
              [
                -5.083,
                55.062
              ]
            ]
          ],
          [
            [
              [
                12.09,
                54.8
              ],
              [
                11.044,
                55.365
              ],
              [
                10.904,
                55.78
              ],
              [
                12.371,
                56.111
              ],
              [
                12.69,
                55.61
              ],
              [
                12.09,
                54.8
              ]
            ]
          ],
          [
            [
              [
                -22.763,
                63.96
              ],
              [
                -21.778,
                64.402
              ],
              [
                -23.955,
                64.891
              ],
              [
                -22.184,
                65.085
              ],
              [
                -24.326,
                65.611
              ],
              [
                -23.651,
                66.263
              ],
              [
                -22.135,
                66.41
              ],
              [
                -20.576,
                65.732
              ],
              [
                -19.057,
                66.277
              ],
              [
                -17.799,
                65.994
              ],
              [
                -16.168,
                66.527
              ],
              [
                -14.509,
                66.456
              ],
              [
                -14.74,
                65.809
              ],
              [
                -13.61,
                65.127
              ],
              [
                -14.91,
                64.364
              ],
              [
                -18.656,
                63.496
              ],
              [
                -22.763,
                63.96
              ]
            ]
          ],
          [
            [
              [
                12.431,
                37.613
              ],
              [
                12.571,
                38.126
              ],
              [
                15.52,
                38.231
              ],
              [
                15.1,
                36.62
              ],
              [
                12.431,
                37.613
              ]
            ]
          ],
          [
            [
              [
                21.37,
                64.414
              ],
              [
                17.848,
                62.749
              ],
              [
                17.12,
                61.341
              ],
              [
                18.788,
                60.082
              ],
              [
                17.869,
                58.954
              ],
              [
                16.829,
                58.72
              ],
              [
                15.88,
                56.104
              ],
              [
                14.667,
                56.201
              ],
              [
                14.101,
                55.408
              ],
              [
                12.943,
                55.362
              ],
              [
                10.357,
                59.47
              ],
              [
                8.382,
                58.313
              ],
              [
                7.049,
                58.079
              ],
              [
                5.666,
                58.588
              ],
              [
                4.992,
                61.971
              ],
              [
                10.528,
                64.486
              ],
              [
                14.761,
                67.811
              ],
              [
                19.184,
                69.817
              ],
              [
                23.024,
                70.202
              ],
              [
                24.547,
                71.03
              ],
              [
                28.166,
                71.185
              ],
              [
                31.293,
                70.454
              ],
              [
                30.005,
                70.186
              ],
              [
                31.101,
                69.558
              ],
              [
                28.592,
                69.065
              ],
              [
                28.446,
                68.365
              ],
              [
                29.977,
                67.698
              ],
              [
                29.055,
                66.944
              ],
              [
                30.218,
                65.806
              ],
              [
                29.544,
                64.949
              ],
              [
                30.445,
                64.204
              ],
              [
                30.036,
                63.553
              ],
              [
                31.516,
                62.868
              ],
              [
                30.211,
                61.78
              ],
              [
                28.07,
                60.504
              ],
              [
                22.87,
                59.846
              ],
              [
                21.322,
                60.72
              ],
              [
                21.545,
                61.705
              ],
              [
                21.059,
                62.607
              ],
              [
                22.443,
                63.818
              ],
              [
                25.398,
                65.111
              ],
              [
                25.294,
                65.534
              ],
              [
                23.903,
                66.007
              ],
              [
                22.183,
                65.724
              ],
              [
                21.214,
                65.026
              ],
              [
                21.37,
                64.414
              ]
            ]
          ],
          [
            [
              [
                17.594,
                77.638
              ],
              [
                17.118,
                76.809
              ],
              [
                15.913,
                76.77
              ],
              [
                13.763,
                77.38
              ],
              [
                14.67,
                77.736
              ],
              [
                11.222,
                78.869
              ],
              [
                10.445,
                79.652
              ],
              [
                16.991,
                80.051
              ],
              [
                21.544,
                78.956
              ],
              [
                19.027,
                78.563
              ],
              [
                18.472,
                77.827
              ],
              [
                17.594,
                77.638
              ]
            ]
          ],
          [
            [
              [
                23.7,
                35.705
              ],
              [
                25.745,
                35.18
              ],
              [
                26.29,
                35.3
              ],
              [
                24.725,
                34.92
              ],
              [
                23.515,
                35.28
              ],
              [
                23.7,
                35.705
              ]
            ]
          ],
          [
            [
              [
                24.724,
                77.854
              ],
              [
                22.49,
                77.445
              ],
              [
                20.726,
                77.677
              ],
              [
                21.416,
                77.935
              ],
              [
                20.812,
                78.255
              ],
              [
                22.884,
                78.455
              ],
              [
                24.724,
                77.854
              ]
            ]
          ],
          [
            [
              [
                17.368,
                80.319
              ],
              [
                22.919,
                80.657
              ],
              [
                27.408,
                80.056
              ],
              [
                25.925,
                79.518
              ],
              [
                23.024,
                79.4
              ],
              [
                20.075,
                79.567
              ],
              [
                17.368,
                80.319
              ]
            ]
          ]
        ]
      }
    }
  ],
  "referenceArtifact": [
    {
      "artifact": "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent",
            "component-not-executable"
          ],
          "required": true,
          "transferabilityNotes": "Inside the EURO-CORDEX domain, reuse as-is by changing the AOI. Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target."
        }
      ]
    },
    {
      "artifact": "CLMS Tree Cover Density / Imperviousness Density",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent",
            "component-not-executable"
          ],
          "required": true,
          "transferabilityNotes": "CLMS product coverage is generally limited to Europe, except Ukraine (see this workflow's `envelope`); outside it, no substitute is currently defined, and hot-spot characterization (which uses this dataset) cannot be executed."
        }
      ]
    },
    {
      "artifact": "Eurostat census / socio-economic data (planned Heat Risk Indicator)",
      "rules": [
        {
          "triggeredBy": "different-geographic-coverage",
          "actions": [
            "replace-with-local-equivalent",
            "component-not-executable"
          ],
          "required": true,
          "transferabilityNotes": "Not yet implemented; the envisaged replacement should follow a schema compatible with Eurostat's. Once built, the source's stated consequence for unavailable data applies here too: the planned Heat Risk Indicator (risk assessment) component would not be executable without it."
        }
      ]
    }
  ],
  "temporalExtent": [
    {
      "start": "2022",
      "end": "2025"
    }
  ],
  "computationType": "deterministic-rule-based",
  "maturityStatus": "operational"
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geojson: <https://purl.org/geojson/vocab#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] rdfs:label "UP-WF2 — Urban hot/cool spot" ;
    focal-transf-prop:computationType <https://w3id.org/ogc/hosted/focal/transferability/computation-types/deterministic-rule-based> ;
    focal-transf-prop:envelope [ focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/jurisdictional> ;
            focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
            focal-transf-prop:value [ geojson:coordinates ( ( ( ( -9.287e+00 3.8358e+01 ) ( -9.447e+00 3.9392e+01 ) ( -8.769e+00 4.0761e+01 ) ( -9.393e+00 4.3027e+01 ) ( -7.978e+00 4.3748e+01 ) ( -1.901e+00 4.3423e+01 ) ( -1.384e+00 4.4023e+01 ) ( -1.194e+00 4.6015e+01 ) ( -2.963e+00 4.757e+01 ) ( -4.492e+00 4.7955e+01 ) ( -4.592e+00 4.8684e+01 ) ( -1.617e+00 4.8644e+01 ) ( -1.933e+00 4.9776e+01 ) ( -9.89e-01 4.9347e+01 ) ( 1.339e+00 5.0127e+01 ) ( 1.639e+00 5.0947e+01 ) ( 3.83e+00 5.1621e+01 ) ( 4.706e+00 5.3092e+01 ) ( 8.122e+00 5.3528e+01 ) ( 8.801e+00 5.4021e+01 ) ( 8.12e+00 5.5518e+01 ) ( 8.543e+00 5.711e+01 ) ( 1.058e+01 5.773e+01 ) ( 1.025e+01 5.689e+01 ) ( 1.0912e+01 5.6459e+01 ) ( 9.65e+00 5.547e+01 ) ( 9.94e+00 5.4597e+01 ) ( 1.095e+01 5.4364e+01 ) ( 1.0939e+01 5.4009e+01 ) ( 1.2518e+01 5.447e+01 ) ( 1.412e+01 5.3757e+01 ) ( 1.7623e+01 5.4852e+01 ) ( 1.8696e+01 5.4439e+01 ) ( 2.2731e+01 5.4328e+01 ) ( 2.2758e+01 5.4857e+01 ) ( 2.1268e+01 5.519e+01 ) ( 2.109e+01 5.6784e+01 ) ( 2.2524e+01 5.7753e+01 ) ( 2.3318e+01 5.7006e+01 ) ( 2.4121e+01 5.7026e+01 ) ( 2.4429e+01 5.8383e+01 ) ( 2.3427e+01 5.8613e+01 ) ( 2.334e+01 5.9187e+01 ) ( 2.7981e+01 5.9475e+01 ) ( 2.742e+01 5.8725e+01 ) ( 2.7717e+01 5.7792e+01 ) ( 2.7288e+01 5.7475e+01 ) ( 2.8177e+01 5.6169e+01 ) ( 3.0874e+01 5.5551e+01 ) ( 3.0758e+01 5.4812e+01 ) ( 3.2694e+01 5.3351e+01 ) ( 3.1305e+01 5.3074e+01 ) ( 3.1786e+01 5.2102e+01 ) ( 3.0919e+01 5.2059e+01 ) ( 3.0551e+01 5.1237e+01 ) ( 2.5768e+01 5.1929e+01 ) ( 2.3594e+01 5.1605e+01 ) ( 2.4108e+01 5.0541e+01 ) ( 2.2666e+01 4.9567e+01 ) ( 2.2867e+01 4.901e+01 ) ( 2.2133e+01 4.8405e+01 ) ( 2.4897e+01 4.771e+01 ) ( 2.7752e+01 4.8452e+01 ) ( 2.9136e+01 4.7968e+01 ) ( 3.0132e+01 4.6423e+01 ) ( 2.8946e+01 4.6455e+01 ) ( 2.8202e+01 4.5469e+01 ) ( 2.9653e+01 4.5341e+01 ) ( 2.8838e+01 4.4914e+01 ) ( 2.7674e+01 4.2578e+01 ) ( 2.7997e+01 4.2007e+01 ) ( 2.6117e+01 4.1827e+01 ) ( 2.6604e+01 4.1562e+01 ) ( 2.6057e+01 4.0824e+01 ) ( 2.3715e+01 4.0687e+01 ) ( 2.4408e+01 4.0125e+01 ) ( 2.2626e+01 4.0257e+01 ) ( 2.335e+01 3.919e+01 ) ( 2.2973e+01 3.8971e+01 ) ( 2.4025e+01 3.822e+01 ) ( 2.404e+01 3.7655e+01 ) ( 2.3115e+01 3.792e+01 ) ( 2.341e+01 3.741e+01 ) ( 2.2775e+01 3.7305e+01 ) ( 2.3154e+01 3.6423e+01 ) ( 2.167e+01 3.6845e+01 ) ( 2.112e+01 3.831e+01 ) ( 1.9406e+01 4.0251e+01 ) ( 1.9372e+01 4.1878e+01 ) ( 1.6015e+01 4.3507e+01 ) ( 1.4902e+01 4.5076e+01 ) ( 1.4259e+01 4.5234e+01 ) ( 1.3952e+01 4.4802e+01 ) ( 1.3938e+01 4.5591e+01 ) ( 1.3142e+01 4.5737e+01 ) ( 1.2329e+01 4.5382e+01 ) ( 1.2589e+01 4.4091e+01 ) ( 1.5143e+01 4.1955e+01 ) ( 1.5926e+01 4.1961e+01 ) ( 1.5889e+01 4.1541e+01 ) ( 1.848e+01 4.0169e+01 ) ( 1.8293e+01 3.9811e+01 ) ( 1.687e+01 4.0442e+01 ) ( 1.6449e+01 3.9795e+01 ) ( 1.7171e+01 3.9425e+01 ) ( 1.7053e+01 3.8903e+01 ) ( 1.6101e+01 3.7986e+01 ) ( 1.5684e+01 3.7909e+01 ) ( 1.6109e+01 3.8965e+01 ) ( 1.5414e+01 4.0048e+01 ) ( 1.2107e+01 4.1705e+01 ) ( 1.0512e+01 4.2931e+01 ) ( 1.02e+01 4.392e+01 ) ( 8.889e+00 4.4366e+01 ) ( 6.529e+00 4.3129e+01 ) ( 4.557e+00 4.34e+01 ) ( 3.1e+00 4.3075e+01 ) ( 3.039e+00 4.1892e+01 ) ( 8.11e-01 4.1015e+01 ) ( -2.79e-01 3.931e+01 ) ( 1.11e-01 3.8739e+01 ) ( -2.146e+00 3.6674e+01 ) ( -4.369e+00 3.6678e+01 ) ( -5.866e+00 3.603e+01 ) ( -6.52e+00 3.6943e+01 ) ( -8.899e+00 3.6869e+01 ) ( -8.84e+00 3.8266e+01 ) ( -9.287e+00 3.8358e+01 ) ) ) ( ( ( 8.428e+00 3.9172e+01 ) ( 8.16e+00 4.095e+01 ) ( 9.21e+00 4.121e+01 ) ( 9.81e+00 4.05e+01 ) ( 9.67e+00 3.9177e+01 ) ( 8.428e+00 3.9172e+01 ) ) ) ( ( ( 9.39e+00 4.301e+01 ) ( 9.56e+00 4.2152e+01 ) ( 9.23e+00 4.138e+01 ) ( 8.544e+00 4.2257e+01 ) ( 9.39e+00 4.301e+01 ) ) ) ( ( ( -9.689e+00 5.3881e+01 ) ( -6.734e+00 5.5173e+01 ) ( -5.662e+00 5.4555e+01 ) ( -6.198e+00 5.3868e+01 ) ( -6.033e+00 5.3153e+01 ) ( -6.789e+00 5.226e+01 ) ( -8.562e+00 5.1669e+01 ) ( -9.977e+00 5.182e+01 ) ( -9.166e+00 5.2865e+01 ) ( -9.689e+00 5.3881e+01 ) ) ) ( ( ( -5.083e+00 5.5062e+01 ) ( -4.719e+00 5.5508e+01 ) ( -5.048e+00 5.5784e+01 ) ( -5.586e+00 5.5311e+01 ) ( -6.15e+00 5.6785e+01 ) ( -5.787e+00 5.7819e+01 ) ( -5.01e+00 5.863e+01 ) ( -3.005e+00 5.8635e+01 ) ( -4.074e+00 5.7553e+01 ) ( -1.959e+00 5.7685e+01 ) ( -3.119e+00 5.5974e+01 ) ( -2.085e+00 5.591e+01 ) ( -1.115e+00 5.4625e+01 ) ( -4.3e-01 5.4464e+01 ) ( 4.7e-01 5.293e+01 ) ( 1.682e+00 5.274e+01 ) ( 1.051e+00 5.1807e+01 ) ( 1.45e+00 5.1289e+01 ) ( 5.5e-01 5.0766e+01 ) ( -5.777e+00 5.016e+01 ) ( -3.415e+00 5.1426e+01 ) ( -5.267e+00 5.1991e+01 ) ( -4.222e+00 5.2301e+01 ) ( -4.77e+00 5.284e+01 ) ( -4.58e+00 5.3495e+01 ) ( -3.092e+00 5.3404e+01 ) ( -2.945e+00 5.3985e+01 ) ( -5.083e+00 5.5062e+01 ) ) ) ( ( ( 1.209e+01 5.48e+01 ) ( 1.1044e+01 5.5365e+01 ) ( 1.0904e+01 5.578e+01 ) ( 1.2371e+01 5.6111e+01 ) ( 1.269e+01 5.561e+01 ) ( 1.209e+01 5.48e+01 ) ) ) ( ( ( -2.2763e+01 6.396e+01 ) ( -2.1778e+01 6.4402e+01 ) ( -2.3955e+01 6.4891e+01 ) ( -2.2184e+01 6.5085e+01 ) ( -2.4326e+01 6.5611e+01 ) ( -2.3651e+01 6.6263e+01 ) ( -2.2135e+01 6.641e+01 ) ( -2.0576e+01 6.5732e+01 ) ( -1.9057e+01 6.6277e+01 ) ( -1.7799e+01 6.5994e+01 ) ( -1.6168e+01 6.6527e+01 ) ( -1.4509e+01 6.6456e+01 ) ( -1.474e+01 6.5809e+01 ) ( -1.361e+01 6.5127e+01 ) ( -1.491e+01 6.4364e+01 ) ( -1.8656e+01 6.3496e+01 ) ( -2.2763e+01 6.396e+01 ) ) ) ( ( ( 1.2431e+01 3.7613e+01 ) ( 1.2571e+01 3.8126e+01 ) ( 1.552e+01 3.8231e+01 ) ( 1.51e+01 3.662e+01 ) ( 1.2431e+01 3.7613e+01 ) ) ) ( ( ( 2.137e+01 6.4414e+01 ) ( 1.7848e+01 6.2749e+01 ) ( 1.712e+01 6.1341e+01 ) ( 1.8788e+01 6.0082e+01 ) ( 1.7869e+01 5.8954e+01 ) ( 1.6829e+01 5.872e+01 ) ( 1.588e+01 5.6104e+01 ) ( 1.4667e+01 5.6201e+01 ) ( 1.4101e+01 5.5408e+01 ) ( 1.2943e+01 5.5362e+01 ) ( 1.0357e+01 5.947e+01 ) ( 8.382e+00 5.8313e+01 ) ( 7.049e+00 5.8079e+01 ) ( 5.666e+00 5.8588e+01 ) ( 4.992e+00 6.1971e+01 ) ( 1.0528e+01 6.4486e+01 ) ( 1.4761e+01 6.7811e+01 ) ( 1.9184e+01 6.9817e+01 ) ( 2.3024e+01 7.0202e+01 ) ( 2.4547e+01 7.103e+01 ) ( 2.8166e+01 7.1185e+01 ) ( 3.1293e+01 7.0454e+01 ) ( 3.0005e+01 7.0186e+01 ) ( 3.1101e+01 6.9558e+01 ) ( 2.8592e+01 6.9065e+01 ) ( 2.8446e+01 6.8365e+01 ) ( 2.9977e+01 6.7698e+01 ) ( 2.9055e+01 6.6944e+01 ) ( 3.0218e+01 6.5806e+01 ) ( 2.9544e+01 6.4949e+01 ) ( 3.0445e+01 6.4204e+01 ) ( 3.0036e+01 6.3553e+01 ) ( 3.1516e+01 6.2868e+01 ) ( 3.0211e+01 6.178e+01 ) ( 2.807e+01 6.0504e+01 ) ( 2.287e+01 5.9846e+01 ) ( 2.1322e+01 6.072e+01 ) ( 2.1545e+01 6.1705e+01 ) ( 2.1059e+01 6.2607e+01 ) ( 2.2443e+01 6.3818e+01 ) ( 2.5398e+01 6.5111e+01 ) ( 2.5294e+01 6.5534e+01 ) ( 2.3903e+01 6.6007e+01 ) ( 2.2183e+01 6.5724e+01 ) ( 2.1214e+01 6.5026e+01 ) ( 2.137e+01 6.4414e+01 ) ) ) ( ( ( 1.7594e+01 7.7638e+01 ) ( 1.7118e+01 7.6809e+01 ) ( 1.5913e+01 7.677e+01 ) ( 1.3763e+01 7.738e+01 ) ( 1.467e+01 7.7736e+01 ) ( 1.1222e+01 7.8869e+01 ) ( 1.0445e+01 7.9652e+01 ) ( 1.6991e+01 8.0051e+01 ) ( 2.1544e+01 7.8956e+01 ) ( 1.9027e+01 7.8563e+01 ) ( 1.8472e+01 7.7827e+01 ) ( 1.7594e+01 7.7638e+01 ) ) ) ( ( ( 2.37e+01 3.5705e+01 ) ( 2.5745e+01 3.518e+01 ) ( 2.629e+01 3.53e+01 ) ( 2.4725e+01 3.492e+01 ) ( 2.3515e+01 3.528e+01 ) ( 2.37e+01 3.5705e+01 ) ) ) ( ( ( 2.4724e+01 7.7854e+01 ) ( 2.249e+01 7.7445e+01 ) ( 2.0726e+01 7.7677e+01 ) ( 2.1416e+01 7.7935e+01 ) ( 2.0812e+01 7.8255e+01 ) ( 2.2884e+01 7.8455e+01 ) ( 2.4724e+01 7.7854e+01 ) ) ) ( ( ( 1.7368e+01 8.0319e+01 ) ( 2.2919e+01 8.0657e+01 ) ( 2.7408e+01 8.0056e+01 ) ( 2.5925e+01 7.9518e+01 ) ( 2.3024e+01 7.94e+01 ) ( 2.0075e+01 7.9567e+01 ) ( 1.7368e+01 8.0319e+01 ) ) ) ) ] ],
        [ focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
            focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
            focal-transf-prop:value [ geojson:coordinates ( ( ( -22 27 ) ( 45 27 ) ( 45 72 ) ( -22 72 ) ( -22 27 ) ) ) ] ] ;
    focal-transf-prop:maturityStatus <https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/operational> ;
    focal-transf-prop:referenceArtifact [ focal-transf-prop:artifact "median summer LST datasets (FOCAL STAC, Landsat 5/7/8/9-derived)" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:transferabilityNotes "Inside the EURO-CORDEX domain, reuse as-is by changing the AOI. Outside it, compatible LST datasets must be generated or preprocessed if possible; if none can be produced, this component cannot be executed for the target." ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ],
        [ focal-transf-prop:artifact "CLMS Tree Cover Density / Imperviousness Density" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:transferabilityNotes "CLMS product coverage is generally limited to Europe, except Ukraine (see this workflow's `envelope`); outside it, no substitute is currently defined, and hot-spot characterization (which uses this dataset) cannot be executed." ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ],
        [ focal-transf-prop:artifact "Eurostat census / socio-economic data (planned Heat Risk Indicator)" ;
            focal-transf-prop:rules [ focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
                        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
                    focal-transf-prop:required true ;
                    focal-transf-prop:transferabilityNotes "Not yet implemented; the envisaged replacement should follow a schema compatible with Eurostat's. Once built, the source's stated consequence for unavailable data applies here too: the planned Heat Risk Indicator (risk assessment) component would not be executable without it." ;
                    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> ] ] ;
    focal-transf-prop:temporalExtent [ focal-transf-prop:end "2025" ;
            focal-transf-prop:start "2022" ] .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Workflow
description: "A profile of a CWL Workflow (`ogc.cwl.v1_2_1.CWLWorkflow`) adding the
  machine-readable transferability facts extracted from FOCAL's 8 pilot-workflow questionnaires.
  Ties together the other `transferability/*` blocks onto one workflow instance:\n-
  `envelope` \u2014 the workflow's validity envelope, one or more\n  [`envelopeConstraint`](bblocks://ogc.focal.transferability.envelopeConstraint)
  statements\n  (`{role, dimension, value}`). Required: every evidenced workflow states
  at least one.\n- `referenceArtifact` \u2014 the workflow's reference/calibration
  artifacts, each wrapping one or more\n  [`rule`](bblocks://ogc.focal.transferability.rule)
  statements. Required for the same reason.\n- `computationType`, `maturityStatus`
  \u2014 the two workflow-level classification mixins (see\n  [`computationType`](bblocks://ogc.focal.transferability.computationType)
  and\n  [`maturityStatus`](bblocks://ogc.focal.transferability.maturityStatus) for
  which is optional\n  and which is required).\n- `temporalExtent`, `qualityAnnotation`
  \u2014 repeatable workflow-level facts, both optional (see\n  their own blocks for
  evidence density and omission rules).\n\n**`referenceArtifact`'s wrapper shape**
  identifies the artifact by a free-text `artifact` label (e.g. \"trained tree growth
  model (LightGBM, Czech PSP data)\") rather than a CWL input/step identifier \u2014
  the 8 questionnaires describe artifacts this way, not by CWL id, and binding `artifact`
  to a concrete `steps`/`inputs` entry of the profiled `CWLWorkflow` is deliberately
  left for later, once real CWL Application Packages for these workflows exist to
  bind against, rather than guessed now.\n"
allOf:
- $ref: https://ogcincubator.github.io/bblocks-cwl/build/annotated/cwl/v1_2_1/CWLWorkflow/schema.yaml
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/computationType/schema.yaml
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/maturityStatus/schema.yaml
- type: object
  required:
  - envelope
  - referenceArtifact
  properties:
    envelope:
      type: array
      minItems: 1
      items:
        $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/schema.yaml
      description: "The workflow's validity envelope, as one or more role/dimension/value
        statements. FP-WF1 alone needs three at once (trained-on/spatial, valid-for/ecological,
        can-run-on/climatic) \u2014 see `envelopeConstraint` for why role and dimension
        are independent axes.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/envelope
      x-jsonld-container: '@set'
    referenceArtifact:
      type: array
      minItems: 1
      items:
        type: object
        required:
        - artifact
        - rules
        properties:
          artifact:
            type: string
            description: 'Free-text label identifying the reference or calibration
              artifact these rules apply to (e.g. "downscaled FOCAL climate data",
              "Quitt climate-zone thresholds/limits").

              '
            x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/artifact
          rules:
            type: array
            minItems: 1
            items:
              $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/schema.yaml
            description: One or more condition/action rules governing this artifact.
            x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/rules
            x-jsonld-container: '@set'
      description: "The workflow's reference/calibration artifacts and the rules governing
        how each must be adapted outside the workflow's validity envelope. Not every
        artifact a workflow depends on needs an entry here \u2014 only those with
        an evidenced transferability fact.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/referenceArtifact
      x-jsonld-container: '@set'
    temporalExtent:
      type: array
      items:
        $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/temporalExtent/schema.yaml
      description: "The calendar span(s), or scenario-indexed marker, the workflow's
        results are valid over. Optional and repeatable \u2014 see `temporalExtent`
        for the omission rule (no fixed window, e.g. an ongoing sensor observation)
        and the two supported shapes.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/temporalExtent
      x-jsonld-container: '@set'
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
    "label": "http://www.w3.org/2000/01/rdf-schema#label",
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
    "envelope": {
      "@context": {
        "dimension": {
          "@context": {
            "@base": "https://w3id.org/ogc/hosted/focal/transferability/dimensions/"
          },
          "@id": "focal-transf-prop:dimension",
          "@type": "@id"
        },
        "value": {
          "@context": {
            "coordinates": {
              "@container": "@list",
              "@id": "geojson:coordinates"
            }
          },
          "@id": "focal-transf-prop:value"
        },
        "role": {
          "@context": {
            "@base": "https://w3id.org/ogc/hosted/focal/transferability/roles/"
          },
          "@id": "focal-transf-prop:role",
          "@type": "@id"
        }
      },
      "@id": "focal-transf-prop:envelope",
      "@container": "@set"
    },
    "referenceArtifact": {
      "@context": {
        "artifact": "focal-transf-prop:artifact",
        "rules": {
          "@context": {
            "transferabilityNotes": "focal-transf-prop:transferabilityNotes",
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
            "required": "focal-transf-prop:required"
          },
          "@id": "focal-transf-prop:rules",
          "@container": "@set"
        }
      },
      "@id": "focal-transf-prop:referenceArtifact",
      "@container": "@set"
    },
    "temporalExtent": {
      "@context": {
        "start": "focal-transf-prop:start",
        "end": "focal-transf-prop:end",
        "scenarioMarker": "focal-transf-prop:scenarioMarker"
      },
      "@id": "focal-transf-prop:temporalExtent",
      "@container": "@set"
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
    "Point": "geojson:Point",
    "MultiPoint": "geojson:MultiPoint",
    "Polygon": "geojson:Polygon",
    "MultiPolygon": "geojson:MultiPolygon",
    "cwl": "https://w3id.org/cwl/cwl#",
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "geojson": "https://purl.org/geojson/vocab#",
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

