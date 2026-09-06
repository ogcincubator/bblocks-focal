## FOCAL Transferability Vocabulary and Model Ontology

The RDF behind the FOCAL workflow transferability model (Task 10.3): eleven open SKOS concept
schemes, plus the classes and properties FOCAL mints.

**Concept schemes** — all open, not closed enums. New concepts are added by extending this
ontology, with no schema change on the blocks that reference them.

| Scheme | What it holds |
|---|---|
| actions | what must be done to an artifact to make it valid elsewhere |
| triggers | coarse conditions, for rules that cannot cite a constraint |
| tests | `inside` / `outside`, how a target is compared against a constraint |
| dimensions | the axes an envelope is stated along |
| roles | `trained-on` / `valid-for` / `can-run-on` |
| artifact-roles | what kind of thing an artifact is |
| scenario-markers | non-calendar temporal positions (Global Warming Levels) |
| grid-types | grid structures a workflow's gridded inputs may be on |
| computation-types | how a workflow computes its results |
| maturity-statuses | operational maturity of the workflow itself |
| quality-dimensions | kinds of result-confidence caveat (also `dqv:Dimension`) |

**Reuse before minting.** FOCAL declares a term only where nothing published says the same thing.
What the model uses directly instead:

| Concept | Term used |
|---|---|
| spatial extent | `geo:Geometry` / `geo:asWKT` (GeoSPARQL 1.1) |
| calendar period | `dcterms:PeriodOfTime` / `dcat:startDate` / `dcat:endDate` |
| artifact | `prov:Entity`, labelled with `dcterms:title` |
| free-text note | `rdfs:comment` |
| result-quality caveat | `dqv:QualityAnnotation` / `dqv:inDimension` (W3C DQV) |
| grid structure | CF-conventions `grid_mapping_name`, as each grid type's `skos:notation` |

That choice is what makes the model assessable by software that has never heard of FOCAL: a
GeoSPARQL engine can answer "can this workflow run over my area of interest?" with `geof:sfWithin`
against an envelope constraint's geometry, because the geometry is a real `geo:wktLiteral` and not
a FOCAL-shaped lookalike.

**What FOCAL does mint**, because no published vocabulary covers it: the envelope constraint itself
(`dcterms:spatial` states one coverage, whereas what matters here is the difference between what a
workflow was trained on, what its outputs are valid for, and where it can technically run — three
extents that come apart in practice), the rule and its conditions, and the concept schemes above.

**Where a property's values come from a scheme**, that is stated as an OWL range restriction
(`rdfs:range [ owl:onProperty skos:inScheme ; owl:hasValue <scheme> ]`) rather than by putting
`skos:inScheme` on the property. The second reads as "this property is a concept in that scheme",
which is true of none of them and would have a reasoner concluding that `focal-prop:role` is one
of the roles.

**Status: draft/WIP.** Seeded from `20260817-workflow-transferability-mapping-extraction.md` and
`20260902-condition-action-expressivity.md` (FOCAL WP10 project directory).
