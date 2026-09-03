
# FOCAL Transferability Notes (mixin) (Schema)

`ogc.focal.transferability.notes` *v0.3*

Reusable mixin adding a free-text escape hatch for transferability facts the controlled vocabularies cannot capture. Uplifts to rdfs:comment rather than a FOCAL-specific property.

[*Status*](http://www.opengis.net/def/status): Under development

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Notes (mixin)
description: "Reusable mixin adding a free-text escape hatch for transferability facts
  that don't reduce cleanly to the controlled vocabularies \u2014 e.g. UP-WF2's \"the
  classification algorithm is more portable than its current input dataset.\"\n**Uplifts
  to `rdfs:comment`**, not to a FOCAL-specific property: a human-readable note about
  a resource is exactly what `rdfs:comment` is for, every RDF consumer already renders
  it, and minting a FOCAL term for it would have bought nothing. This is the general
  rule across the model \u2014 a FOCAL term only where nothing published says the
  same thing.\nMixed in wherever such a note may apply: on bblocks://ogc.focal.transferability.envelopeConstraint
  (why a value is approximate or inferred) and on bblocks://ogc.focal.transferability.rule
  (what degrades when an optional action is skipped).\n"
type: object
properties:
  transferabilityNotes:
    type: string
    description: 'Free-text elaboration of a transferability fact the controlled vocabularies
      can''t capture. Uplifts to `rdfs:comment` on whatever it is attached to.

      '
    x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#comment
x-jsonld-prefixes:
  rdfs: http://www.w3.org/2000/01/rdf-schema#

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "transferabilityNotes": "rdfs:comment",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
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

