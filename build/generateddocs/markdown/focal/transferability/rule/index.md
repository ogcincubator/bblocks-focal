
# FOCAL Transferability Rule (Schema)

`ogc.focal.transferability.rule` *v0.1*

A single condition/action rule (triggeredBy + actions + required) describing how a reference or calibration artifact must be adapted outside its workflow's original validity envelope.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## FOCAL Transferability Rule

One condition/action rule attached to a reference or calibration artifact.

- `triggeredBy` — the condition that fires this rule (open vocabulary, see
  [`transferability/vocab`](bblocks://ogc.focal.transferability.vocab)).
- `actions` — an **OR-set**: any one of these actions resolves the rule. FP-WF1's growth model
  needs this — it offers both `retrain` and `replace-with-alternative-published-model` for the
  same artifact and the same trigger.
- `required` — whether applying one of `actions` is mandatory once `triggeredBy` holds. Defaults
  to `true`. `false` means the workflow still runs without it, but result quality/trust degrades —
  describe how in `transferabilityNotes` (mixed in from
  [`transferability/notes`](bblocks://ogc.focal.transferability.notes)). Example: FP-WF3's
  disturbance-detection workflow runs without local training labels, but results should then be
  treated as exploratory rather than authoritative.

**Known simplification (flagged for WF-owner review):** a small number of artifacts (UP-WF2's LST/
CLMS/Eurostat datasets) have a richer three-way condition — reuse inside a coverage boundary,
replace if a substitute exists outside it, hard-fail if none exists — than a flat rule list can
express without an explicit "only if a substitute is obtainable" branch condition. For now these
are represented as two separate flat rules (`reuse-as-is` / `replace-with-local-equivalent`),
dropping that connecting condition. See `20260902-condition-action-expressivity.md` in the FOCAL
WP10 project directory for the full pattern inventory this was decided against.

**Status: draft/WIP**, circulated for review, not locked.

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Rule
description: "A single condition/action rule attached to a reference or calibration
  artifact: the condition that triggers it (`triggeredBy`), the action(s) that resolve
  it (`actions` \u2014 an OR-set, any one action satisfies the rule), and whether
  applying one is mandatory (`required`). `triggeredBy` and `actions` draw from the
  open SKOS vocabulary in bblocks://ogc.focal.transferability.vocab \u2014 the values
  listed in `examples` below are the core, evidenced set from FOCAL's pilot workflows,
  not an exhaustive enum; new terms may be added to the vocabulary without a schema
  change.\n"
allOf:
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/schema.yaml
- type: object
  required:
  - triggeredBy
  - actions
  properties:
    triggeredBy:
      type: string
      examples:
      - different-geographic-coverage
      - different-ecological-range
      - different-climate-regime
      - different-dataset
      description: The condition that triggers this rule.
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/triggeredBy
      x-jsonld-type: '@id'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/triggers/
    actions:
      type: array
      minItems: 1
      items:
        type: string
        examples:
        - reuse-as-is
        - replace-with-local-equivalent
        - retrain
        - replace-with-alternative-published-model
        - component-not-executable
      description: "One or more actions, any of which resolves `triggeredBy` \u2014
        an OR-set, not a required combination (no evidenced case needs more than one
        action applied simultaneously).\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/actions
      x-jsonld-type: '@id'
      x-jsonld-container: '@set'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/actions/
    required:
      type: boolean
      default: true
      description: "Whether applying one of `actions` is mandatory once `triggeredBy`
        holds. Defaults to true. When false, skipping is allowed but degrades result
        quality/trust rather than blocking execution \u2014 describe the consequence
        in `transferabilityNotes`.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/required
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/schema.yaml)


# JSON-LD Context

```jsonld
{
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
    "required": "focal-transf-prop:required",
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/rule`

