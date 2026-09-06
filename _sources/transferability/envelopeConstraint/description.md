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
