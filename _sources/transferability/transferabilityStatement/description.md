## FOCAL Transferability Statement

Where something's results are valid, which artifacts it depends on, and what must happen to each.
Three id-addressable lists joined by reference rather than by nesting:

| Property | Cardinality | Source block |
|---|---|---|
| `envelope` | required, may be empty | [`envelopeConstraint`](bblocks://ogc.focal.transferability.envelopeConstraint) |
| `artifacts` | required, may be empty | own shape, a `prov:Entity` with a `dcterms:title`, optionally carrying [`acceptanceCriteria`](bblocks://ogc.focal.transferability.acceptanceCriteria) |
| `rules` | required, may be empty | [`rule`](bblocks://ogc.focal.transferability.rule) |

**An empty array is a meaningful value, for `rules` and for `envelope` alike**: assessed, nothing
needs adapting; assessed, no validity boundary. Both are positive portability facts, and quite
different from the property being absent, which says nobody has looked. Requiring at least one
entry forces anyone in the first situation to invent one. For `envelope` that minimum also made
"valid everywhere" inexpressible except as a world-sized polygon, and left the one workflow whose
source states no boundary at all (UP-WF1) with no honest representation rather than one saying
exactly that. Say which case it is in `transferabilityNotes`.

**Rules are exceptions; silence means reuse.** An artifact no rule fires for, over a given target,
is reused unchanged. Without that default, a consumer asking "can I run this over my area of
interest?" has to guess what an absent rule means, and the answer a model gives has to be the same
for everyone reading it.

**Why reference rather than nesting.** Nesting rules under artifacts connects each rule to one
artifact but not to the envelope boundary it is evaluated against, and cannot express an artifact
bounded on two axes at once, or four artifacts sharing one boundary. Citing ids costs one
indirection and expresses all three. `shapes.shacl` enforces referential integrity, so a rule
cannot cite a constraint or artifact the statement does not declare.

**Reused vocabularies.** An artifact is a `prov:Entity` labelled with `dcterms:title`; notes,
including the statement's own `transferabilityNotes`, are `rdfs:comment`. FOCAL mints a term only where nothing published says the same thing — see
[`transferability/vocab`](bblocks://ogc.focal.transferability.vocab).

**Status: draft/WIP**, circulated for review, not locked. Carries no CWL assumption:
[`ogc.focal.transferability.workflow`](bblocks://ogc.focal.transferability.workflow) attaches one
statement of this shape to a profiled `CWLWorkflow`, but the same bundle can attach to a step, a
process, or a delivered dataset.
