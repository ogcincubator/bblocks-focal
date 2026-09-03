## FOCAL Transferability Statement

Where something's results are valid, which artifacts it depends on, and what must happen to each.
Three id-addressable lists joined by reference rather than by nesting:

| Property | Cardinality | Source block |
|---|---|---|
| `envelope` | required, repeatable | [`envelopeConstraint`](bblocks://ogc.focal.transferability.envelopeConstraint) |
| `artifacts` | required, may be empty | own shape, a `prov:Entity` with a `dcterms:title` |
| `rules` | required, may be empty | [`rule`](bblocks://ogc.focal.transferability.rule) |

**An empty `rules` array is a meaningful value**: assessed, nothing needs adapting. That is a
positive portability fact, and quite different from the property being absent, which says nobody
has looked. Requiring at least one entry forced anyone in the first situation to invent a rule.

**Why reference rather than nesting.** Nesting rules under artifacts connects each rule to one
artifact but not to the envelope boundary it is evaluated against, and cannot express an artifact
bounded on two axes at once, or four artifacts sharing one boundary. Citing ids costs one
indirection and expresses all three. `shapes.shacl` enforces referential integrity, so a rule
cannot cite a constraint or artifact the statement does not declare.

**Reused vocabularies.** An artifact is a `prov:Entity` labelled with `dcterms:title`; notes are
`rdfs:comment`. FOCAL mints a term only where nothing published says the same thing — see
[`transferability/vocab`](bblocks://ogc.focal.transferability.vocab).

**Status: draft/WIP**, circulated for review, not locked. Carries no CWL assumption:
[`ogc.focal.transferability.workflow`](bblocks://ogc.focal.transferability.workflow) attaches one
statement of this shape to a profiled `CWLWorkflow`, but the same bundle can attach to a step, a
process, or a delivered dataset.
