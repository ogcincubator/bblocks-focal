
# FOCAL Quality Annotation (Schema)

`ogc.focal.transferability.qualityAnnotation` *v0.1*

A single statement of uncertainty or confidence about a workflow's results, independent of its maturityStatus. Binds to the W3C Data Quality Vocabulary (DQV) directly, since no OGC Block wraps DQV.

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Quality Annotation
description: "A single statement of uncertainty or confidence about a workflow's results
  \u2014 a separate axis from `maturityStatus` (see bblocks://ogc.focal.transferability.maturityStatus):
  FP-WF1 is `operational` *and* carries a caveat that its results are decision-support,
  not exact, and the two facts don't collapse into one. Repeatable at the workflow
  level, same discipline as `temporalExtent`/`envelopeConstraint`.\nCurrently evidenced
  1/8 (FP-WF1 only) \u2014 thinner evidence than any other confirmed transferability
  gap; expect this to grow once other workflow owners are consulted.\n**Binds directly
  to the W3C Data Quality Vocabulary (DQV, `https://www.w3.org/ns/dqv#`)**, checked
  2026-09-02 against the published spec rather than assumed: `dimension` maps to `dqv:inDimension`,
  whose range `dqv:Dimension` is itself a `skos:Concept` \u2014 the open-SKOS-vocabulary
  pattern used everywhere else in this model turns out to already be DQV's own pattern,
  not just an analogy to it. No OGC Block wraps DQV (checked: no register or bblock
  defines it; the only other DQV usage anywhere in the bblocks ecosystem is a Tier-3
  sibling, `ogc.hosted.iliad.api.features.indicator-quality-requirement`, shaped for
  a different domain), so this binds straight to the published namespace rather than
  depending on anything. `note` has no exact DQV equivalent (DQV's annotation body
  normally comes via `oa:hasBody`, heavier machinery than needed here) and stays a
  plain FOCAL property.\n"
type: object
required:
- dimension
properties:
  dimension:
    type: string
    examples:
    - decision-support-only
    - validation-incomplete
    description: 'What kind of uncertainty/confidence statement this is. Open vocabulary
      (SKOS), bound to `dqv:inDimension` -> `dqv:Dimension`.

      '
    x-jsonld-id: http://www.w3.org/ns/dqv#inDimension
    x-jsonld-type: '@id'
    x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/
  note:
    type: string
    description: 'The statement itself, in free text (e.g. FP-WF1''s caveat verbatim:
      "AI model and validation are still being finalised, results are decision-support
      not exact"). No DQV binding.

      '
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/note
  measurement:
    description: "Reserved for a future numeric quality measurement (would map to
      `dqv:QualityMeasurement`). Not yet designed \u2014 no evidenced case needs it.
      Left untyped and unbound deliberately rather than guessing a shape ahead of
      evidence.\n"
x-jsonld-prefixes:
  dqv: http://www.w3.org/ns/dqv#
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/qualityAnnotation/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/qualityAnnotation/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "dimension": {
      "@context": {
        "@base": "https://w3id.org/ogc/hosted/focal/transferability/quality-dimensions/"
      },
      "@id": "dqv:inDimension",
      "@type": "@id"
    },
    "note": "focal-transf-prop:note",
    "dqv": "http://www.w3.org/ns/dqv#",
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/qualityAnnotation/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/qualityAnnotation`

