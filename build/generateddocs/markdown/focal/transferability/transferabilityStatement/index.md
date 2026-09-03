
# FOCAL Transferability Statement (Schema)

`ogc.focal.transferability.transferabilityStatement` *v0.4*

Where something's results are valid (envelope), which reference/calibration artifacts it depends on (artifacts), and what must happen to each under which conditions (rules) - three id-addressable lists joined by reference rather than nesting.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

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

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Statement
description: "Where something's results are valid, which reference or calibration
  artifacts it depends on, and what must happen to each to make the results valid
  elsewhere. Factored out of `ogc.focal.transferability.workflow` so the same bundle
  can attach to something other than a CWL Workflow \u2014 a step, a process, a delivered
  dataset \u2014 and carrying no CWL assumption of its own.\nThree lists, each addressable
  by `id`, joined by reference rather than by nesting:\n- `envelope` \u2014 the validity
  envelope, as\n  [`envelopeConstraint`](bblocks://ogc.focal.transferability.envelopeConstraint)
  statements.\n- `artifacts` \u2014 the reference/calibration artifacts, declared
  once. - `rules` \u2014 what happens to which artifacts under which envelope conditions.\n**Why
  three lists and not nesting.** An earlier draft nested rules inside artifacts and
  kept the envelope entirely separate, so nothing connected a rule to the boundary
  it was evaluated against. UP-WF2 is where that breaks: it has two different coverage
  footprints and three artifacts, every rule saying \"different geographic coverage\",
  and no way to record that the LST datasets are bounded by one and the CLMS layers
  by the other. Asked \"can I run this in Kyiv?\", a consumer could not tell which
  rule fires. Nesting rules under artifacts fixes that one case and fails the next:
  an artifact bounded on two axes at once needs a conjunction, which a tree cannot
  express. Citing ids costs one indirection and expresses both, plus the case that
  motivated neither \u2014 FP-WF2's four artifacts sharing a single boundary, stated
  once rather than four times.\n**Conjunction and disjunction.** A rule's `when` is
  an AND: every condition must hold for the rule to fire. A disjunction is written
  as two rules. That is a deliberate limit rather than a missing feature \u2014 two
  conditions leading to the same action really are two statements, and keeping them
  separate keeps each traceable to the sentence in a questionnaire it came from, which
  a nested boolean expression does not. `actions` remains an OR-set: any one resolves
  the rule.\n"
type: object
required:
- envelope
- artifacts
- rules
properties:
  envelope:
    type: array
    minItems: 1
    items:
      $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/schema.yaml
    description: 'The validity envelope, as one or more role/dimension/value statements.
      Required: something with no stated boundary at all is not yet a portability
      statement, and inventing one to satisfy the schema would be worse than leaving
      the workflow unmodelled.

      '
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/envelope
    x-jsonld-container: '@set'
  artifacts:
    type: array
    items:
      $ref: '#/$defs/artifact'
    description: 'The reference and calibration artifacts this statement''s rules
      govern, each declared once and cited by `rules[].appliesTo`. May be empty when
      every rule is about the workflow as a whole.

      '
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/artifacts
    x-jsonld-container: '@set'
  rules:
    type: array
    items:
      $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/schema.yaml
    description: 'What must happen, to which artifacts, under which conditions. **An
      empty array is a meaningful value**: it says the artifacts were assessed and
      none needs adapting, which is a positive portability fact and quite different
      from the property being absent, which says nobody has looked. Requiring at least
      one entry would force anyone in the first situation to invent a rule.

      '
    x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/rules
    x-jsonld-container: '@set'
$defs:
  artifact:
    title: Artifact dependency
    type: object
    required:
    - id
    - artifact
    - artifactRole
    properties:
      id:
        $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/iri-or-curie/schema.yaml
        description: 'Identifier for this artifact, cited by `rules[].appliesTo`.
          An IRI, a CURIE, or a bare local name resolved against the document base
          (see bblocks://ogc.ogc-utils.iri-or-curie). A shared reference dataset that
          several workflows depend on is worth identifying globally, for the same
          reason a shared envelope constraint is.

          '
        x-jsonld-id: '@id'
      artifact:
        type: string
        description: 'Label identifying the artifact, in the words the source used
          (e.g. "downscaled FOCAL climate data", "Quitt climate-zone thresholds/limits").
          Uplifts to `dcterms:title` on a `prov:Entity`.

          '
        x-jsonld-id: http://purl.org/dc/terms/title
      artifactRole:
        type: string
        examples:
        - workflow-input
        - workflow-output
        - external-resource
        - infrastructure
        description: "What kind of thing this artifact is, independent of whether
          an executable workflow description exists that could give it an identifier
          yet. The eight FOCAL questionnaires' artifacts are not uniformly workflow
          inputs: some are inputs, some are outputs later reused as another run's
          input (a trained model), and some never appear in an executable graph at
          all (physical infrastructure to be re-deployed; an optional validation reference).
          Open vocabulary \u2014 see bblocks://ogc.focal.transferability.vocab.\n"
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/artifactRole
        x-jsonld-type: '@id'
        x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/
      artifactRef:
        type: string
        format: json-pointer
        pattern: ^/
        examples:
        - /inputs/climate_data
        - /outputs/trained_growth_model
        description: 'JSON Pointer (RFC 6901) locating the artifact inside the document
          this statement annotates. For the CWL profile in bblocks://ogc.focal.transferability.workflow
          that means `/inputs/<id>` or `/outputs/<id>`, but the pointer carries no
          CWL assumption. Optional: meaningful only for the `workflow-input` and `workflow-output`
          roles, and only fillable once a real Application Package exists to point
          into. Omit it rather than guess.

          '
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/artifactRef
      transferabilityNotes:
        type: string
        description: Free-text note about the artifact. Uplifts to `rdfs:comment`.
        x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#comment
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/
  dcterms: http://purl.org/dc/terms/
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  focal-transf: https://w3id.org/ogc/hosted/focal/transferability/
  prov: http://www.w3.org/ns/prov#

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/transferabilityStatement/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/transferabilityStatement/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "envelope": {
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
            }
          },
          "@id": "focal-transf-prop:value"
        }
      },
      "@id": "focal-transf-prop:envelope",
      "@container": "@set"
    },
    "artifacts": {
      "@context": {
        "id": "@id",
        "artifact": "dcterms:title",
        "artifactRole": {
          "@context": {
            "@base": "https://w3id.org/ogc/hosted/focal/transferability/artifact-roles/"
          },
          "@id": "focal-transf-prop:artifactRole",
          "@type": "@id"
        },
        "artifactRef": "focal-transf-prop:artifactRef",
        "transferabilityNotes": "rdfs:comment"
      },
      "@id": "focal-transf-prop:artifacts",
      "@container": "@set"
    },
    "rules": {
      "@context": {
        "transferabilityNotes": "rdfs:comment",
        "appliesTo": {
          "@id": "focal-transf-prop:appliesTo",
          "@type": "@id",
          "@container": "@set"
        },
        "when": {
          "@context": {
            "constraint": {
              "@id": "focal-transf-prop:constraint",
              "@type": "@id"
            },
            "test": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/tests/"
              },
              "@id": "focal-transf-prop:test",
              "@type": "@id"
            }
          },
          "@id": "focal-transf-prop:when",
          "@container": "@set"
        },
        "triggeredBy": {
          "@context": {
            "@base": "https://w3id.org/ogc/hosted/focal/transferability/triggers/"
          },
          "@id": "focal-transf-prop:triggeredBy",
          "@type": "@id"
        },
        "actions": {
          "@context": {
            "@base": "https://w3id.org/ogc/hosted/focal/transferability/actions/"
          },
          "@id": "focal-transf-prop:actions",
          "@type": "@id",
          "@container": "@set"
        },
        "mandatory": "focal-transf-prop:mandatory"
      },
      "@id": "focal-transf-prop:rules",
      "@container": "@set"
    },
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "focal-transf-prop": "focal-transf:properties/",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dcterms": "http://purl.org/dc/terms/",
    "focal-transf": "https://w3id.org/ogc/hosted/focal/transferability/",
    "prov": "http://www.w3.org/ns/prov#",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/transferabilityStatement/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/transferabilityStatement`

