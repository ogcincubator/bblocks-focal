
# FOCAL Transferability Notes (mixin) (Schema)

`ogc.focal.transferability.notes` *v0.1*

Reusable mixin adding a free-text escape hatch for transferability facts that don't reduce to the controlled transferabilityAction/triggeredBy vocabulary.

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Notes (mixin)
description: "Reusable mixin adding a free-text escape hatch for transferability facts
  that don't reduce cleanly to the controlled `transferabilityAction`/`triggeredBy`
  vocabulary (see bblocks://ogc.focal.transferability.vocab) \u2014 e.g. UP-WF2's
  \"the classification algorithm is more portable than its current input dataset.\"
  Mix in via `allOf` wherever such a note may apply (a rule, an envelope constraint,
  ...); not restricted to one attachment point.\n"
type: object
properties:
  transferabilityNotes:
    type: string
    description: 'Free-text elaboration of a transferability fact the controlled vocabulary
      can''t capture, or of the consequence of an optional action being skipped (see
      transferability/rule''s `required`).

      '
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/transferabilityNotes
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "transferabilityNotes": "focal-transf-prop:transferabilityNotes",
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/notes`

