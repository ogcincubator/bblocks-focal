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

**`value`:** `dimension: spatial` or `jurisdictional` **requires** a GeoJSON Geometry (RFC 7946 —
`Point`/`MultiPoint`/`Polygon`/`MultiPolygon`), enforced by a `oneOf` with two branches keyed on
`dimension` — a string is not a valid alternative there. Every other dimension
(`ecological`/`climatic`, like the two rows above) stays plain `string`, since those facts
genuinely aren't a place. A `spatial`/`jurisdictional` fact with no resolvable source location
should be omitted from `envelope` rather than filled with a placeholder string.

**Status: draft/WIP**, circulated for review, not locked.
