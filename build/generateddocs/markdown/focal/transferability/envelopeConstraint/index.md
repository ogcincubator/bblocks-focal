
# FOCAL Transferability Envelope Constraint (Schema)

`ogc.focal.transferability.envelopeConstraint` *v0.6*

A single {role, dimension, value} statement bounding where a workflow's results are valid, addressable by id so rules can cite which boundary they are evaluated against. Spatial values are GeoSPARQL geometries and temporal values DCAT periods, so a consumer can evaluate them without knowing FOCAL.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## FOCAL Transferability Envelope Constraint

One `{id, role, dimension, value}` statement bounding where a workflow's results are valid.

`role` and `dimension` are independent axes, both open vocabularies (see
[`transferability/vocab`](bblocks://ogc.focal.transferability.vocab)). A workflow's envelope is an
array of these and more than one applies at once: FP-WF1's growth model needs three.

| role | dimension | value |
|---|---|---|
| `trained-on` | `spatial` | a WKT geometry locating the Czech permanent sample plots |
| `valid-for` | `ecological` | `"a comparable ecological range"` (a string, not a place) |
| `can-run-on` | `climatic` | `"wherever downscaled climate data is available"` |

**`id` is what makes a constraint citable.** A rule's `when` names the constraint it is evaluated
against, so a workflow with two different footprints can say which artifact each one governs.
Without ids the envelope and the rules were two disconnected lists, and a consumer could not tell
which boundary a "different geographic coverage" rule referred to.

**Values reuse published vocabularies wherever one exists**, so a consumer already speaking
GeoSPARQL or DCAT needs to learn nothing about FOCAL to evaluate them:

- `spatial`/`jurisdictional` → `{"asWKT": "POLYGON((...))"}`, uplifting to `geo:asWKT` with
  datatype `geo:wktLiteral`. This is the form GeoSPARQL's topological functions operate on, so
  "is my area of interest inside this?" is `geof:sfWithin` rather than a sentence to read. WKT
  also survives uplift unreshaped and is far more compact than coordinate arrays.
- `temporal` → `{"startDate", "endDate"}`, uplifting to `dcat:startDate`/`dcat:endDate`; or
  `{"scenarioMarker"}` for results that are not calendar-indexed at all, as a concept rather than
  free text. A Global Warming Level is reached in different years under different scenarios, so a
  calendar period would be a fabrication.
- `grid-structure` → `{"gridTypes": [...]}`, a set of accepted grid types drawn from an open
  vocabulary whose terms carry the CF-conventions `grid_mapping_name` as their `skos:notation`.
  `inside` means the candidate dataset's grid is one of them. UP-WF3 states this outright ("other
  projections are not handled"), and it is a hard interface requirement over a small, already
  standardised set, so it is terms rather than prose.
- anything else → a plain string. A phenological regime is not a place and does not become
  machine-checkable by being wrapped in coordinates it does not have. A rule may still cite such a
  constraint; the condition is then a judgement a person makes, recorded in the same structure as
  one a machine can settle.

**What decides whether a dimension gets a structured value shape** is not whether it is
geographic: it is whether the fact is a small enumerable set or a hard interval, rather than a
judgement. Grid structure qualifies and ecological range does not, and a grid type is arguably
more mechanically checkable than any of the approximate bounding boxes in the worked examples.

**Status: draft/WIP**, circulated for review, not locked.

## Examples

### Spatial extent (GeoSPARQL geometry)
A `trained-on`/`spatial` constraint carrying an `id` so rules can cite it.

`value.asWKT` uplifts to `geo:asWKT` with datatype `geo:wktLiteral`, which is the form
GeoSPARQL's topological functions operate on: a consumer answers "is my area of interest
inside this?" with `geof:sfWithin` and no knowledge of FOCAL.

The geometry is Czechia's country bounding box standing in for FP-WF1's actual sample plot
network, which is a scattered set of monitoring locations rather than a rectangle.
`transferabilityNotes` is where that gets said, in the data rather than in prose, so the
approximation travels with the value.

#### json
```json
{
  "id": "czech-plots",
  "role": "trained-on",
  "dimension": "spatial",
  "value": { "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))" },
  "transferabilityNotes": "Country bounding box, standing in for the actual permanent sample plot network; an honest upper bound pending the real plot coordinates."
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/context.jsonld",
  "id": "czech-plots",
  "role": "trained-on",
  "dimension": "spatial",
  "value": {
    "asWKT": "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"
  },
  "transferabilityNotes": "Country bounding box, standing in for the actual permanent sample plot network; an honest upper bound pending the real plot coordinates."
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/envelope-constraint/czech-plots> rdfs:comment "Country bounding box, standing in for the actual permanent sample plot network; an honest upper bound pending the real plot coordinates." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))"^^geo:wktLiteral ] .


```


### Spatial extent with an explicit CRS
GeoSPARQL permits a leading CRS URI on a WKT literal. Without one, CRS84
(longitude/latitude in degrees) is assumed, which is what every other example here relies on.
Stating it explicitly matters for a workflow calibrated in a projected national grid — the
Forest Pilot's S-JTSK (EPSG:5514) is the case to watch.

#### json
```json
{
  "id": "prague-point",
  "role": "trained-on",
  "dimension": "spatial",
  "value": { "asWKT": "<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POINT(14.42 50.09)" }
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/context.jsonld",
  "id": "prague-point",
  "role": "trained-on",
  "dimension": "spatial",
  "value": {
    "asWKT": "<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POINT(14.42 50.09)"
  }
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/envelope-constraint/prague-point> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/trained-on> ;
    focal-transf-prop:value [ geo:asWKT "<http://www.opengis.net/def/crs/OGC/1.3/CRS84> POINT(14.42 50.09)"^^geo:wktLiteral ] .


```


### Temporal extent, calendar period (DCAT)
A `valid-for`/`temporal` constraint using the period branch. `startDate`/`endDate` uplift to
`dcat:startDate`/`dcat:endDate`, the DCAT terms every catalogue already understands for
temporal coverage.

Granularity is workflow-specific and deliberately not fixed — this one is year-level
(UP-WF2's discrete epochs), a date or year-month is equally valid — but the *format* is
fixed to ISO 8601, so two periods stated at the same granularity compare correctly as plain
string ordering. Previously these were unconstrained strings.

#### json
```json
{
  "id": "epochs",
  "role": "valid-for",
  "dimension": "temporal",
  "value": { "startDate": "2022", "endDate": "2025" }
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/context.jsonld",
  "id": "epochs",
  "role": "valid-for",
  "dimension": "temporal",
  "value": {
    "startDate": "2022",
    "endDate": "2025"
  }
}
```

#### ttl
```ttl
@prefix dcat: <http://www.w3.org/ns/dcat#> .
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/envelope-constraint/epochs> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ dcat:endDate "2025" ;
            dcat:startDate "2022" ] .


```


### Temporal extent, scenario marker (non-calendar)
The other temporal branch, for results that are not calendar-indexed at all. UP-WF1's
NUKLEUS output is positioned by Global Warming Level, and a warming level is reached in
different years depending on emissions scenario and ensemble member, so a calendar period
would be a fabrication rather than a simplification.

The marker is a **concept**, not a free string: `GWL+1.5` written two ways by two pilots
would otherwise be two incomparable strings but one thing. This branch had never been
exercised by any example anywhere in the register before, so it had never been validated.

#### json
```json
{
  "id": "gwl-15",
  "role": "valid-for",
  "dimension": "temporal",
  "value": { "scenarioMarker": "gwl-1.5" }
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/context.jsonld",
  "id": "gwl-15",
  "role": "valid-for",
  "dimension": "temporal",
  "value": {
    "scenarioMarker": "gwl-1.5"
  }
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/envelope-constraint/gwl-15> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/temporal> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ focal-transf-prop:scenarioMarker <https://w3id.org/ogc/hosted/focal/transferability/scenario-markers/gwl-1.5> ] .


```


### Non-geometric dimension (string-valued)
A `valid-for`/`ecological` constraint. "A comparable ecological range" is not a place and
does not become machine-checkable by being wrapped in coordinates it does not have, so this
branch keeps `value` a plain string.

A rule may still cite this constraint by `id` and test `outside` against it. The condition
is then a judgement a person makes, recorded in the same structure as one a machine can
settle — which is honest about where automation stops rather than pretending the whole model
is decidable.

This is also the catch-all branch: a dimension term nobody has added a `value` shape for
lands here and validates, so the SKOS scheme can grow without touching the schema. The
schema is only touched when a new dimension turns out to need a shape other than a string,
which is what `grid-structure` did.

#### json
```json
{
  "id": "ecological-range",
  "role": "valid-for",
  "dimension": "ecological",
  "value": "a comparable ecological range"
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/context.jsonld",
  "id": "ecological-range",
  "role": "valid-for",
  "dimension": "ecological",
  "value": "a comparable ecological range"
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/envelope-constraint/ecological-range> focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/ecological> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value "a comparable ecological range" .


```


### Grid structure (a set of accepted grid types)
How a workflow's inputs must be gridded, as opposed to where its results are valid. UP-WF3
states it plainly: the precipitation source must be on a regular lat/lon or a rotated-pole
grid, and "other projections are not handled".

The whole array is the constraint. `inside` means the candidate dataset's grid is one of
these; `outside` that it is not, and a rule citing this constraint fires. Each term carries
the CF-conventions `grid_mapping_name` as its `skos:notation`
(`latitude_longitude`, `rotated_latitude_longitude`), which is what E-OBS, NUKLEUS and
EURO-CORDEX actually declare in their files — so this is a check a consumer runs against a
candidate NetCDF, not one a person reads.

This branch exists because prose was the wrong answer here. Most non-spatial dimensions are
judgements and stay strings; a grid type is a small, closed, already-standardised set, and
it is arguably *more* mechanically checkable than any of the approximate bounding boxes
elsewhere in this model. The test for whether a dimension deserves a structured shape is
that one, not whether it happens to be geographic.

#### json
```json
{
  "id": "eur11-grid",
  "role": "can-run-on",
  "dimension": "grid-structure",
  "value": { "gridTypes": ["regular-latlon", "rotated-pole"] },
  "transferabilityNotes": "UP-WF3's stated input requirement. A dataset on any other projection has to be resampled before the workflow will accept it."
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/context.jsonld",
  "id": "eur11-grid",
  "role": "can-run-on",
  "dimension": "grid-structure",
  "value": {
    "gridTypes": [
      "regular-latlon",
      "rotated-pole"
    ]
  },
  "transferabilityNotes": "UP-WF3's stated input requirement. A dataset on any other projection has to be resampled before the workflow will accept it."
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://w3id.org/ogc/hosted/focal/transferability/examples/envelope-constraint/eur11-grid> rdfs:comment "UP-WF3's stated input requirement. A dataset on any other projection has to be resampled before the workflow will accept it." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/grid-structure> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/can-run-on> ;
    focal-transf-prop:value [ focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
                <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ] .


```


### A shared constraint, identified globally
The EURO-CORDEX EUR-11 domain is the same extent for every workflow driven by that ensemble.
Given a bare local name in each of them, nothing can tell that they are the same boundary —
a consumer holding two workflows sees two unrelated polygons that happen to coincide.

Declaring it under an IRI says they are one boundary. `id` accepts an IRI, a CURIE, or a bare
local name via [`ogc.ogc-utils.iri-or-curie`](bblocks://ogc.ogc-utils.iri-or-curie), so this
is the same field used three ways rather than a separate mechanism.

A global identifier makes the boundary **shareable, not fetchable**: the constraint is still
declared in full in every statement that cites it, so a reader always has the extent in front
of them. What the IRI adds is the ability to ask "which workflows are bounded by this exact
domain?" and get an answer.

#### json
```json
{
  "id": "https://w3id.org/ogc/hosted/focal/transferability/extents/euro-cordex-eur11",
  "role": "valid-for",
  "dimension": "spatial",
  "value": { "asWKT": "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))" },
  "transferabilityNotes": "The EUR-11 domain's published approximate rectangular extent. Shared across every FOCAL workflow driven by the EURO-CORDEX ensemble, which is why it carries a global identifier rather than a name local to one workflow."
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/context.jsonld",
  "id": "https://w3id.org/ogc/hosted/focal/transferability/extents/euro-cordex-eur11",
  "role": "valid-for",
  "dimension": "spatial",
  "value": {
    "asWKT": "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))"
  },
  "transferabilityNotes": "The EUR-11 domain's published approximate rectangular extent. Shared across every FOCAL workflow driven by the EURO-CORDEX ensemble, which is why it carries a global identifier rather than a name local to one workflow."
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://w3id.org/ogc/hosted/focal/transferability/extents/euro-cordex-eur11> rdfs:comment "The EUR-11 domain's published approximate rectangular extent. Shared across every FOCAL workflow driven by the EURO-CORDEX ensemble, which is why it carries a global identifier rather than a name local to one workflow." ;
    focal-transf-prop:dimension <https://w3id.org/ogc/hosted/focal/transferability/dimensions/spatial> ;
    focal-transf-prop:role <https://w3id.org/ogc/hosted/focal/transferability/roles/valid-for> ;
    focal-transf-prop:value [ geo:asWKT "POLYGON((-22 27,45 27,45 72,-22 72,-22 27))"^^geo:wktLiteral ] .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Envelope Constraint
description: "A single statement bounding where a workflow's results are valid: which
  `role` this fact plays (what the workflow was trained on vs. what its results are
  valid for vs. where it can technically run), which `dimension` it concerns (spatial,
  temporal, ecological, climatic, jurisdictional, grid-structure, ... \u2014 an open
  vocabulary), and the `value` itself.\nRepeatable, and `id`-addressable: rules cite
  a constraint by `id` to say which boundary they are evaluated against, so a workflow
  with two different footprints can state which artifact each one governs. FP-WF1
  needs three constraints at once (trained-on/spatial, valid-for/ecological, can-run-on/climatic),
  which is why role and dimension are independent axes rather than a single enum choice.\n**Values
  bind to published vocabularies rather than to FOCAL terms wherever one exists**,
  so a consumer that already understands GeoSPARQL or DCAT can evaluate the constraint
  without knowing anything about FOCAL: a spatial extent is a `geo:Geometry` carrying
  `geo:asWKT`, a calendar span is a `dcterms:PeriodOfTime` carrying `dcat:startDate`/`dcat:endDate`.
  That is what makes \"can I run this workflow over my area of interest?\" a query
  a GeoSPARQL engine can answer with `geof:sfWithin`, rather than a sentence a person
  has to read.\n"
allOf:
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/schema.yaml
- type: object
  required:
  - role
  - dimension
  - value
  properties:
    id:
      $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/iri-or-curie/schema.yaml
      description: 'Identifier for this constraint, so a rule can cite it in `when[].constraint`.
        Optional only for a constraint no rule refers to.

        An **IRI, a CURIE, or a bare local name** (see bblocks://ogc.ogc-utils.iri-or-curie).
        A local name is resolved against the document''s base URI and is right for
        a constraint specific to one workflow. An IRI or CURIE gives the constraint
        a **global identity**, which is what makes a boundary shareable: the EURO-CORDEX
        EUR-11 domain is the same extent for several FOCAL workflows, and each restating
        it as a private local name leaves nothing able to tell that they are the same
        boundary. Declaring it here under its global identifier says so.

        A CURIE expands only if its prefix is declared in the JSON-LD context (via
        `x-jsonld-prefixes` or an imported block); an undeclared prefix is read as
        a URI scheme and `acme:eur11` stays `acme:eur11`, which validates and means
        nothing. Use a full IRI unless the prefix is known to be in scope.

        Giving a constraint a global identifier makes the boundary shareable, not
        fetchable: it is still declared in full in every statement that cites it,
        so a reader always has the extent in front of them. What the identifier buys
        is being able to ask which workflows are bounded by this exact domain.

        '
      x-jsonld-id: '@id'
    role:
      type: string
      examples:
      - trained-on
      - valid-for
      - can-run-on
      description: "Which aspect of the envelope this statement describes. Open vocabulary
        \u2014 see bblocks://ogc.focal.transferability.vocab.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/role
      x-jsonld-type: '@id'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/roles/
    dimension:
      type: string
      examples:
      - spatial
      - temporal
      - ecological
      - climatic
      - jurisdictional
      - grid-structure
      description: 'Which axis of variation this statement constrains, and therefore
        what shape `value` takes. Open vocabulary, seeded from the eight FOCAL pilot
        questionnaires and expected to grow; a new term needs no schema change unless
        it also needs a new `value` shape.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/dimension
      x-jsonld-type: '@id'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/dimensions/
    transferabilityNotes:
      type: string
      description: 'Why this value is what it is, where that is not self-evident:
        an approximated geometry, a fact inferred rather than stated by the source,
        a granularity the source left open. Uplifts to `rdfs:comment`. Mixed in from
        bblocks://ogc.focal.transferability.notes.

        '
      x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#comment
    value:
      description: "The constraint value, shaped by `dimension`:\n- `spatial`/`jurisdictional`
        \u2014 a geometry, as `{\"asWKT\": \"POLYGON((...))\"}`. WKT rather\n  than
        GeoJSON coordinate arrays: it uplifts to a real `geo:wktLiteral`, which is
        the\n  form GeoSPARQL's topological functions actually operate on, it is one
        value rather than\n  a nested array so nothing is lost or reshaped in uplift,
        and it is dramatically more\n  compact (UP-WF2's European coverage MultiPolygon
        costs a few hundred characters\n  instead of 1,283 lines of Turtle). An approximate
        extent is expected and fine \u2014 a\n  published bounding box for a model
        domain, say \u2014 but it must be a real extent, since a\n  free-text place
        name cannot answer the containment question this dimension exists for.\n-
        `temporal` \u2014 either `{\"startDate\", \"endDate\"}` (a calendar span,
        uplifting to\n  `dcat:startDate`/`dcat:endDate` on a `dcterms:PeriodOfTime`)
        or `{\"scenarioMarker\"}`\n  for results that are not calendar-indexed at
        all. A Global Warming Level is the\n  evidenced case: it is reached in different
        years under different emissions scenarios\n  and ensemble members, so a calendar
        interval would be a fabrication rather than a\n  simplification. Markers are
        concepts, not free text, so `GWL+1.5` written two ways by\n  two pilots is
        one thing rather than two.\n- `grid-structure` \u2014 the set of grid types
        the workflow's gridded inputs may be on, as\n  `{\"gridTypes\": [\"regular-latlon\",
        \"rotated-pole\"]}`. A whitelist rather than a\n  description: `inside` means
        the target data's grid is one of these, `outside` that it\n  is not. This
        is a structured branch and not prose because UP-WF3's constraint (\"other\n
        \ projections are not handled\") is a hard interface requirement over a small
        enumerable\n  set \u2014 mechanically checkable, and *more* so than a bounding
        box, since the terms carry\n  the CF-conventions `grid_mapping_name` as their
        `skos:notation` and the datasets in\n  question declare exactly that.\n- **any
        dimension, as an analogy** \u2014 `{\"scheme\": ..., \"sameClassAs\": ...}`,
        saying the\n  target must fall in the same class of a published classification
        as some reference\n  does. This is the shape of every \"comparable to where
        we calibrated\" claim in the\n  corpus, and it is a *relation*, not a value:
        the source says the target must resemble\n  the training area, and says nothing
        about which classes the training area is in.\n  Enumerating those classes
        would state something the source never said and would go\n  stale the moment
        the training geometry is corrected, so the default is to name the\n  reference
        and let a platform derive the rest. Tested with `same-class-as` /\n  `different-class-from`
        rather than `inside`/`outside`.\n- `ecological`/`climatic`/anything else \u2014
        a plain string, where no classification\n  captures the claim. \"A comparable
        ecological range\" does not become machine-checkable\n  by being wrapped in
        coordinates it does not have. A rule may still cite such a\n  constraint;
        the condition is then a judgement a person makes, stated in the same\n  structure,
        which is honest about where automation stops. Prefer the analogy shape above\n
        \ where a scheme does capture it: it says the same thing and a machine can
        settle it.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/value
oneOf:
- title: Spatial or jurisdictional extent (geometry-valued)
  properties:
    dimension:
      enum:
      - spatial
      - jurisdictional
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/dimension
      x-jsonld-type: '@id'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/dimensions/
    value:
      $ref: '#/$defs/geometry'
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/value
  required:
  - dimension
  - value
- title: Temporal extent (period- or marker-valued)
  properties:
    dimension:
      enum:
      - temporal
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/dimension
      x-jsonld-type: '@id'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/dimensions/
    value:
      oneOf:
      - $ref: '#/$defs/period'
      - $ref: '#/$defs/scenarioMarker'
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/value
  required:
  - dimension
  - value
- title: Grid structure (set of accepted grid types)
  properties:
    dimension:
      enum:
      - grid-structure
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/dimension
      x-jsonld-type: '@id'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/dimensions/
    value:
      $ref: '#/$defs/gridStructure'
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/value
  required:
  - dimension
  - value
- title: Classification analogy (any dimension)
  description: 'Available on every dimension, including spatial ones: "the same biogeographical
    region as the training area" is a different claim from "inside the training area''s
    bounding box", and both are legitimate.

    '
  properties:
    value:
      $ref: '#/$defs/analogy'
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/value
  required:
  - value
- title: Any other dimension (string-valued)
  properties:
    dimension:
      not:
        enum:
        - spatial
        - jurisdictional
        - temporal
        - grid-structure
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
  geometry:
    title: Geometry
    type: object
    required:
    - asWKT
    additionalProperties: false
    properties:
      asWKT:
        type: string
        pattern: ^ *(<[^>]*> *)?(POINT|MULTIPOINT|LINESTRING|MULTILINESTRING|POLYGON|MULTIPOLYGON|GEOMETRYCOLLECTION)
          *[ZM]{0,2} *\(
        examples:
        - POLYGON((12.09 48.55,18.87 48.55,18.87 51.06,12.09 51.06,12.09 48.55))
        - <http://www.opengis.net/def/crs/OGC/1.3/CRS84> POINT(14.42 50.09)
        description: 'The extent as a WKT literal, uplifting to `geo:asWKT` with datatype
          `geo:wktLiteral`. An optional leading CRS URI is permitted, per GeoSPARQL;
          without one, CRS84 (longitude/latitude in degrees) is assumed, as GeoSPARQL
          specifies.

          '
        x-jsonld-id: http://www.opengis.net/ont/geosparql#asWKT
        x-jsonld-type: http://www.opengis.net/ont/geosparql#wktLiteral
  period:
    title: Calendar period
    type: object
    required:
    - startDate
    - endDate
    additionalProperties: false
    properties:
      startDate:
        type: string
        pattern: ^\d{4}(-\d{2}(-\d{2})?)?$
        examples:
        - '2022'
        - 2022-06
        - '2022-06-01'
        description: 'Start of the period, as an ISO 8601 year, year-month, or date.
          Granularity is workflow-specific and deliberately not fixed, but the format
          is, so two periods stated at the same granularity compare correctly as plain
          string ordering.

          '
        x-jsonld-id: http://www.w3.org/ns/dcat#startDate
      endDate:
        type: string
        pattern: ^\d{4}(-\d{2}(-\d{2})?)?$
        examples:
        - '2025'
        description: End of the period, in the same form as `startDate`.
        x-jsonld-id: http://www.w3.org/ns/dcat#endDate
  gridStructure:
    title: Accepted grid types
    type: object
    required:
    - gridTypes
    additionalProperties: false
    properties:
      gridTypes:
        type: array
        minItems: 1
        items:
          type: string
          examples:
          - regular-latlon
          - rotated-pole
        description: 'The grid types the workflow accepts, as concepts from the FOCAL
          grid-types scheme (see bblocks://ogc.focal.transferability.vocab). The whole
          array is the constraint: a target is `inside` it if its grid is one of these.
          Open vocabulary, seeded only with the two terms UP-WF3 evidences and cross-walked
          to CF-conventions `grid_mapping_name` values, so adding a projection is
          a lookup in the CF table rather than a judgement.

          '
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/gridType
        x-jsonld-type: '@id'
        x-jsonld-container: '@set'
        x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/grid-types/
  analogy:
    title: Classification analogy
    type: object
    required:
    - scheme
    additionalProperties: false
    anyOf:
    - required:
      - sameClassAs
    - required:
      - classes
    properties:
      scheme:
        type: string
        examples:
        - koppen-geiger
        - eunis-habitats
        - eea-biogeographical-regions
        description: 'The published classification system this constraint is evaluated
          in, as a concept from the FOCAL classification-schemes vocabulary (see bblocks://ogc.focal.transferability.vocab).
          FOCAL names the scheme and records where its terms live; it does not restate
          them, the same discipline applied to QUDT units and CF grid mappings.

          '
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/classificationScheme
        x-jsonld-type: '@id'
        x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/classification-schemes/
      sameClassAs:
        $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/iri-or-curie/schema.yaml
        description: "The reference whose classification the target must share, normally
          the `id` of another constraint in the same envelope \u2014 typically the
          `trained-on` extent. **This is the preferred form**, and the only one usable
          with a scheme that publishes no term identifiers: nothing has to name a
          class, so a platform classifies the reference geometry and the target and
          compares. It also stays correct when the reference geometry is replaced
          by a better one, which an enumerated class list would not.\n"
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/sameClassAs
        x-jsonld-type: '@id'
      classes:
        type: array
        minItems: 1
        items:
          type: string
        examples:
        - - Cfb
          - Dfb
        - - http://eunis.eea.europa.eu/eunishabitats/G1
        description: "Explicitly stated classes, as an alternative to naming a reference.
          Use only where the source actually states them: deriving them from a reference
          and writing them here turns an inference into an assertion. Cite the scheme's
          own identifiers \u2014 EUNIS habitats are published by the EEA, and Koppen-Geiger
          classes are published by FOCAL itself (`.../koppen-geiger/Cfb`) precisely
          because no maintainer publishes them. Each classification-schemes concept
          records where its terms live.\n"
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/class
        x-jsonld-container: '@set'
  scenarioMarker:
    title: Scenario-indexed marker
    type: object
    required:
    - scenarioMarker
    additionalProperties: false
    properties:
      scenarioMarker:
        type: string
        examples:
        - gwl-1.5
        - gwl-2.0
        description: 'A non-calendar, scenario-indexed temporal position, as a concept
          from the FOCAL scenario-markers scheme (see bblocks://ogc.focal.transferability.vocab).
          Open: other scenario indices may follow.

          '
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/scenarioMarker
        x-jsonld-type: '@id'
        x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/scenario-markers/
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/
  geo: http://www.opengis.net/ont/geosparql#
  dcat: http://www.w3.org/ns/dcat#
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  dcterms: http://purl.org/dc/terms/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "transferabilityNotes": "rdfs:comment",
    "id": "@id",
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
    },
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dcterms": "http://purl.org/dc/terms/",
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

