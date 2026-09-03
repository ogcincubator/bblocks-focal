## FOCAL Transferability Statement

Groups the two facts that actually describe a portability boundary — everything else FOCAL's
model tracks about a workflow (`computationType`, `maturityStatus`, `qualityAnnotation`) describes
its implementation or result quality generally, not where it can go.

| Property | Cardinality | Source block |
|---|---|---|
| `envelope` | required, repeatable | [`envelopeConstraint`](bblocks://ogc.focal.transferability.envelopeConstraint) |
| `artifactRules` | required, repeatable (own wrapper, see below) | wraps [`rule`](bblocks://ogc.focal.transferability.rule) |

**`envelope`** covers the calendar/scenario dimension too: a `dimension: temporal` entry, `value`
shaped `{start, end}` or `{scenarioMarker}` — see `envelopeConstraint` for the full four-branch
`value` shape. There's no separate temporal-extent property here; it's one more envelope entry,
same as `spatial`/`ecological`/`climatic`/`jurisdictional`.

**`artifactRules` wrapper.** Each entry is `{artifact, artifactRole, artifactRef?, rules}`:
`artifact` is a free-text label identifying the reference/calibration artifact (e.g. "Rasdaman
climate registry / catalogue"), `artifactRole` classifies what kind of thing it is
(`workflow-input`, `workflow-output`, `external-resource`, or `infrastructure` — see
`schema.yaml` for the full distinction), `artifactRef` optionally gives its actual
`inputs.<id>`/`outputs.<id>` in whatever `CWLWorkflow` this statement is attached to once a real
CWL id exists to bind against, and `rules` is one or more
[`rule`](bblocks://ogc.focal.transferability.rule) statements governing it. Not every artifact a
workflow depends on needs an entry — only those with an evidenced transferability fact.

**Status: draft/WIP**, circulated for review, not locked. Factored out of
[`ogc.focal.transferability.workflow`](bblocks://ogc.focal.transferability.workflow), which
attaches one `transferability` property of this shape to a profiled `CWLWorkflow`, alongside its
own `computationType`/`maturityStatus`/`qualityAnnotation` properties.
