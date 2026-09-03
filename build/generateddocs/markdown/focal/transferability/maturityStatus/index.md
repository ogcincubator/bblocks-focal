
# FOCAL Workflow Maturity Status (mixin) (Schema)

`ogc.focal.transferability.maturityStatus` *v0.2*

Reusable mixin adding maturityStatus, an open-vocabulary classification of a workflow's operational maturity (prototype, pre-operational, operational). Deliberately a separate vocabulary from a bblock's own authoring-lifecycle status field.

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Workflow Maturity Status (mixin)
description: "Reusable mixin adding `maturityStatus`, an open-vocabulary classification
  of a FOCAL pilot workflow's operational maturity \u2014 see bblocks://ogc.focal.transferability.vocab
  for the seeded 3-stage progression (`prototype` -> `pre-operational` -> `operational`).
  Evidenced 8/8 across FOCAL's pilot workflows.\n**Deliberately distinct from a bblock's
  own `bblock.json` `status` field** (`under-development` / `experimental` / `stable`
  / ...), which describes the *block's own authoring lifecycle*, not the operational
  maturity of the FOCAL workflow it describes \u2014 reusing those words here would
  put two unrelated axes on the same object graph under identical strings.\nA caveat
  about result confidence (e.g. FP-WF1's \"AI model and validation are still being
  finalised, results are decision-support not exact\") is a separate fact from maturity
  stage \u2014 see bblocks://ogc.focal.transferability.qualityAnnotation, not a `maturityStatus`
  value or note.\n"
type: object
required:
- maturityStatus
properties:
  maturityStatus:
    type: string
    examples:
    - prototype
    - pre-operational
    - operational
    description: 'The workflow''s operational maturity stage. Open vocabulary (SKOS),
      not a closed enum.

      '
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/maturityStatus
    x-jsonld-type: '@id'
    x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/maturityStatus/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/maturityStatus/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "maturityStatus": {
      "@context": {
        "@base": "https://w3id.org/ogc/hosted/focal/transferability/maturity-statuses/"
      },
      "@id": "focal-transf-prop:maturityStatus",
      "@type": "@id"
    },
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/maturityStatus/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/maturityStatus`

