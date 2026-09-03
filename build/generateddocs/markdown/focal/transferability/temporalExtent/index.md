
# FOCAL Temporal Extent (Schema)

`ogc.focal.transferability.temporalExtent` *v0.1*

A single statement of the calendar span (or, for scenario-indexed cases, non-calendar marker) a workflow's results are valid over. Repeatable at the workflow level so more than one window can apply at once.

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Temporal Extent
description: "A single statement of the calendar span a workflow's results are valid
  over. Repeatable at the workflow level: FP-WF3 needs two related windows at once
  (an EO time-series window and the historical-damage window that precedes it). Evidenced
  7/8 across FOCAL's pilot workflows (all but FP-WF4, an ongoing sensor observation
  with no fixed window \u2014 omit the property entirely there, same \"optional, not
  a value\" treatment as computationType).\nTwo shapes, resolved 2026-09-02 after
  re-reading the source questionnaires \u2014 no `kind` discriminator is needed:\n-
  `{start, end}` is the default: a plain calendar interval, covering 6 of the 7 evidenced\n
  \ workflows (FP-WF1, FP-WF2, FP-WF5, UP-WF2, UP-WF3, and FP-WF3 twice).\n- `{scenarioMarker}`
  is the one explicit exception: UP-WF1's \"timeslices are represented as\n  Global
  Warming Levels\" is genuinely not calendar-indexed (a warming level is reached at\n
  \ different years depending on emissions scenario/ensemble member), so no interval
  can be\n  derived from the source without fabricating one. **This value is pending
  direct review with\n  the UP-WF1 workflow owner** \u2014 see the mapping-extraction
  doc's UP-WF1 section \u2014 asking whether\n  a time interval can be declared per
  GWL slice at all.\n\nTwo facts initially proposed for this property were reclassified
  out of it after re-reading the source: UP-WF3's accumulation-window (6h/12h/1d/7d)
  and temporal-aggregation-period (daily/weekly/monthly) values are workflow computation
  *parameters* (rolling-window length, output grouping), naturally expressed as CWL
  `CommandLineTool`/`Workflow` input parameters via `ogc.cwl.*` \u2014 not statements
  about the calendar span the workflow is valid over.\n"
oneOf:
- type: object
  title: Calendar interval
  required:
  - start
  - end
  additionalProperties: false
  properties:
    start:
      type: string
      description: 'Start of the interval. Granularity is workflow-specific (a date,
        a year, a multi-year period) and not constrained here.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/start
    end:
      type: string
      description: End of the interval, same granularity as `start`.
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/end
- type: object
  title: Scenario-indexed marker
  required:
  - scenarioMarker
  additionalProperties: false
  properties:
    scenarioMarker:
      type: string
      examples:
      - GWL+1.5
      - GWL+2.0
      description: 'A non-calendar, scenario-indexed temporal position (e.g. a Global
        Warming Level label) where no calendar interval can be stated. See the description
        above for the pending UP-WF1 owner review before treating any specific value
        here as settled.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/scenarioMarker
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/temporalExtent/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/temporalExtent/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "start": "focal-transf-prop:start",
    "end": "focal-transf-prop:end",
    "scenarioMarker": "focal-transf-prop:scenarioMarker",
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/temporalExtent/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/temporalExtent`

