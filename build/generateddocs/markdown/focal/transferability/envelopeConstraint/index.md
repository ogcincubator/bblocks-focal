
# FOCAL Transferability Envelope Constraint (Schema)

`ogc.focal.transferability.envelopeConstraint` *v0.1*

A single {role, dimension, value} statement describing part of a workflow's validity envelope, repeatable so multiple roles/dimensions can apply to one workflow at once.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## FOCAL Transferability Envelope Constraint

A single `{role, dimension, value}` statement describing part of a workflow's validity envelope.

`role` and `dimension` are independent axes, both open vocabularies (see
[`transferability/vocab`](bblocks://ogc.focal.transferability.vocab)) — not a single enum
choice. A workflow's envelope is an array of these, and more than one can apply at once: FP-WF1's
growth model needs three simultaneously —

| role | dimension | value |
|---|---|---|
| `trained-on` | `spatial` | a GeoJSON `MultiPoint`/`Polygon` locating the Czech permanent sample plots |
| `valid-for` | `ecological` | `"a comparable ecological range"` (string — not a place) |
| `can-run-on` | `climatic` | `"wherever downscaled climate data is available"` (string — not a place) |

**`value` (resolved 2026-09-03, tightened same day):** `dimension: spatial` or `jurisdictional`
**requires** a GeoJSON Geometry (RFC 7946 — `Point`/`MultiPoint`/`Polygon`/`MultiPolygon`),
enforced by a `oneOf` with two branches keyed on `dimension` — not merely permitted alongside string.
Every other dimension (`ecological`/`climatic`, like the two rows above) stays plain `string`,
since those facts genuinely aren't a place. A `spatial`/`jurisdictional` fact with no resolvable
source location should be omitted from `envelope` rather than filled with a placeholder string —
`value` no longer accepts one there at all.

**Status: draft/WIP**, circulated for review, not locked.

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Envelope Constraint
description: "A single statement describing part of a workflow's validity envelope:
  which `role` this fact plays (what the workflow was trained on vs. what it's valid
  for vs. what it can run on), which `dimension` it concerns (spatial, ecological,
  climatic, jurisdictional, ... \u2014 an open vocabulary, seeded small and expected
  to grow), and the `value` itself. Repeatable per workflow: FP-WF1 alone needs three
  of these at once (trained-on/spatial, valid-for/ecological, can-run-on/climatic)
  \u2014 role and dimension are independent axes, not a single enum choice, precisely
  so a new constraint axis can be added later as a new vocabulary term rather than
  a schema change.\n"
type: object
required:
- role
- dimension
- value
properties:
  role:
    type: string
    examples:
    - trained-on
    - valid-for
    - can-run-on
    description: Which aspect of the envelope this statement describes.
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/role
    x-jsonld-type: '@id'
    x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/roles/
  dimension:
    type: string
    examples:
    - spatial
    - ecological
    - climatic
    - jurisdictional
    description: "Which axis of variation this statement constrains. Open vocabulary,
      seeded deliberately small \u2014 expect WF-owner review to surface dimensions
      not yet listed here.\n"
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/dimension
    x-jsonld-type: '@id'
    x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/dimensions/
  value:
    description: "The constraint value itself. **Resolved 2026-09-03, tightened 2026-09-03:**
      a `spatial` or `jurisdictional` fact is a real geographic/administrative extent,
      and text throws away exactly the thing this envelope model exists to support
      \u2014 an automated check like \"does my AOI fall inside this workflow's `valid-for`
      area?\" cannot be answered against a free-text label. So for those two dimensions,
      `value` **must** be a GeoJSON Geometry (RFC 7946 \xA73.1: `Point`, `MultiPoint`,
      `Polygon`, or `MultiPolygon` \u2014 the shapes evidenced so far; `LineString`/`MultiLineString`/`GeometryCollection`
      can be added later if evidence needs them), even an approximate one (e.g. UP-WF2's
      EURO-CORDEX domain, rendered as its published bounding box) \u2014 not just
      permitted, since text is not a fallback for \"haven't looked up the coordinates
      yet.\" A workflow with a genuinely unlocatable `spatial`/`jurisdictional` fact
      (no resolvable source location at all) should omit that envelope entry, or use
      `transferability/notes`' `transferabilityNotes` on a sibling fact to record
      the caveat in prose, rather than smuggling free text into `value`.\nFor every
      other dimension (`ecological`, `climatic`, and any future open-vocabulary term
      not itself a literal extent), `value` stays plain `string` \u2014 \"a comparable
      ecological range\" doesn't become more machine-readable by wrapping it in coordinates
      it doesn't have. This `oneOf` is keyed on today's two known geographic dimension
      terms; a future dimension term that is *also* a literal extent should be added
      to the geometry branch's `enum`, not solved by loosening `value` back to accepting
      a free-text geometry escape hatch.\nNo existing OGC Block carries a bare GeoJSON
      Geometry union standalone (checked 2026-09-03): `ogc.geo.common.data_types.geojson`
      (the main OGC register's stable GeoJSON block) only exposes this shape nested
      inside a full `Feature` wrapper (`type`/`properties`/`geometry`), no `$defs`
      fragment for just the geometry union \u2014 checked its actual schema, not assumed
      \u2014 which is heavier than a constraint value needs and isn't `$ref`-able
      as a bare fragment. This repo's own `forestStandFeature` hits the same wall
      (wraps the full `ogc.geo.features.feature` Feature shape, not a bare geometry),
      and no other register has one either (checked broadly). So, same posture as
      `qualityAnnotation` binding straight to DQV with no wrapping OGC Block to depend
      on, this binds directly to RFC 7946 rather than to a Feature-shaped block.\n"
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/value
    x-jsonld-extra-terms:
      coordinates:
        x-jsonld-container: '@list'
        x-jsonld-id: https://purl.org/geojson/vocab#coordinates
oneOf:
- title: Spatial/jurisdictional extent (geometry-valued)
  properties:
    dimension:
      enum:
      - spatial
      - jurisdictional
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/dimension
      x-jsonld-type: '@id'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/dimensions/
    value:
      $ref: '#/$defs/geoJSONGeometry'
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/value
  required:
  - dimension
  - value
- title: Other envelope dimension (string-valued)
  properties:
    dimension:
      not:
        enum:
        - spatial
        - jurisdictional
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/dimension
      x-jsonld-type: '@id'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/dimensions/
    value:
      type: string
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/value
  required:
  - dimension
  - value
$defs:
  geoJSONGeometry:
    title: GeoJSON Geometry
    type: object
    required:
    - type
    - coordinates
    properties:
      type:
        type: string
        enum:
        - Point
        - MultiPoint
        - Polygon
        - MultiPolygon
        x-jsonld-id: '@type'
      coordinates:
        description: "Position array, nested per `type` as RFC 7946 \xA73.1 defines
          it (e.g. a `Polygon`'s coordinates are an array of linear rings, each an
          array of `[lon, lat]` positions). Left as `array` here rather than spelling
          out all four `type`-specific shapes, since JSON Schema can't easily key
          a nested shape off a sibling `enum` value without substantially more structure
          than a small, evidence-seeded constraint value needs.\n"
        type: array
        x-jsonld-container: '@list'
        x-jsonld-id: https://purl.org/geojson/vocab#coordinates
x-jsonld-extra-terms:
  Point: https://purl.org/geojson/vocab#Point
  MultiPoint: https://purl.org/geojson/vocab#MultiPoint
  Polygon: https://purl.org/geojson/vocab#Polygon
  MultiPolygon: https://purl.org/geojson/vocab#MultiPolygon
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/
  geojson: https://purl.org/geojson/vocab#

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/schema.yaml)


# JSON-LD Context

```jsonld
{
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
    "Point": "geojson:Point",
    "MultiPoint": "geojson:MultiPoint",
    "Polygon": "geojson:Polygon",
    "MultiPolygon": "geojson:MultiPolygon",
    "role": {
      "@context": {
        "@base": "https://w3id.org/ogc/hosted/focal/transferability/roles/"
      },
      "@id": "focal-transf-prop:role",
      "@type": "@id"
    },
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "geojson": "https://purl.org/geojson/vocab#",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/envelopeConstraint`

