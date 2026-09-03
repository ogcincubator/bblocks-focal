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

**`value`:** four `oneOf` branches keyed on `dimension`, not a single free-form shape:

- `spatial`/`jurisdictional` **requires** a GeoJSON Geometry (RFC 7946 —
  `Point`/`MultiPoint`/`Polygon`/`MultiPolygon`) — a string is not a valid alternative there. A
  fact with no resolvable source location should be omitted from `envelope` rather than filled
  with a placeholder string.
- `temporal` **requires** either `{start, end}` (a calendar interval) or `{scenarioMarker}` (a
  non-calendar, scenario-indexed position, e.g. `GWL+1.5`, for results that aren't
  calendar-indexed at all — a Global Warming Level is reached at different years depending on
  emissions scenario/ensemble member). A fact with no fixed window (e.g. an ongoing sensor
  observation) should likewise be omitted rather than fabricated.
- `ecological`/`climatic` (like the two rows above) get their own branch: still plain `string`,
  since those facts genuinely aren't a place or an interval, but named explicitly rather than
  defined only by "not spatial/temporal."
- Any dimension term not in the three groups above — the vocabulary is open, so a not-yet-seeded
  term is still allowed — falls back to the same plain `string`, as its own branch distinct from
  the named one above, so a currently-known term can later move to a structured shape without
  changing what "not yet classified" means for a genuinely new term.

**Status: draft/WIP**, circulated for review, not locked.
