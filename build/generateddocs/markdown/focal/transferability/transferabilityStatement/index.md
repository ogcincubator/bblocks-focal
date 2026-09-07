
# FOCAL Transferability Statement (Schema)

`ogc.focal.transferability.transferabilityStatement` *v0.7*

Where something's results are valid (envelope), which reference/calibration artifacts it depends on (artifacts), and what must happen to each under which conditions (rules) - three id-addressable lists joined by reference rather than nesting.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

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
  once rather than four times.\n**Rules are exceptions; silence means reuse.** A statement
  lists what has to change. An artifact no rule fires for, over a given target, is
  reused unchanged. That default is what makes the model answerable rather than merely
  inspectable: without it, \"no rule fires\" is ambiguous between *nothing needs doing*
  and *nobody checked*, and every consumer has to guess. The ambiguity is closed structurally
  rather than by convention: `envelope`, `artifacts` and `rules` are all required,
  so an empty one of any of them is something an author wrote down, not something
  missing. Absent from the document entirely, the statement says nobody has looked;
  an empty array inside it says somebody looked and found nothing.\nTwo consequences
  worth stating plainly. A rule whose only action is `reuse-as-is` restates the default,
  which is worth doing where it makes a cascade legible (UP-WF2 pairs `inside` with
  `outside` over one constraint) and is noise otherwise. And an **empty `envelope`
  is a claim, not a blank**: it says the results carry no validity boundary at all,
  which is what a genuinely universal workflow looks like and what UP-WF1's questionnaire
  literally answers (\"All parts are portable\"). Record why in `transferabilityNotes`
  \u2014 a boundary nobody could find and a boundary that does not exist are the same
  empty array otherwise.\n**Conjunction and disjunction.** A rule's `when` is an AND:
  every condition must hold for the rule to fire. A disjunction is written as two
  rules. That is a deliberate limit rather than a missing feature \u2014 two conditions
  leading to the same action really are two statements, and keeping them separate
  keeps each traceable to the sentence in a questionnaire it came from, which a nested
  boolean expression does not. `actions` remains an OR-set: any one resolves the rule.\n"
allOf:
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/schema.yaml
- type: object
  required:
  - envelope
  - artifacts
  - rules
  properties:
    envelope:
      type: array
      items:
        $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/envelopeConstraint/schema.yaml
      description: 'The validity envelope, as role/dimension/value statements. Required,
        but **an empty array is a meaningful value**, the same way it is for `rules`:
        it says the results were assessed and carry no validity boundary. An earlier
        draft required at least one entry, on the reasoning that inventing a boundary
        to satisfy the schema is worse than leaving a workflow unmodelled. That is
        still true, and the minimum did not achieve it: it made "valid everywhere"
        inexpressible except by drawing a world-sized polygon, and it left the one
        workflow whose source states no boundary (UP-WF1) with no honest representation
        at all rather than one saying exactly that. Say which case it is in `transferabilityNotes`.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/envelope
      x-jsonld-container: '@set'
    transferabilityNotes:
      type: string
      description: "Why this statement is shaped as it is, where that is not self-evident
        \u2014 most usefully on an empty `envelope` or empty `rules`, to distinguish
        a boundary that does not exist from one nobody could establish. Uplifts to
        `rdfs:comment`. Mixed in from bblocks://ogc.focal.transferability.notes.\n"
      x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#comment
    artifacts:
      type: array
      items:
        $ref: '#/$defs/artifact'
      description: 'The reference and calibration artifacts this statement''s rules
        govern, each declared once and cited by `rules[].appliesTo`. May be empty
        when every rule is about the workflow as a whole.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/artifacts
      x-jsonld-container: '@set'
    rules:
      type: array
      items:
        $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/schema.yaml
      description: 'What must happen, to which artifacts, under which conditions.
        **An empty array is a meaningful value**: it says the artifacts were assessed
        and none needs adapting, which is a positive portability fact and quite different
        from the property being absent, which says nobody has looked. Requiring at
        least one entry would force anyone in the first situation to invent a rule.

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
      acceptanceCriteria:
        $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/acceptanceCriteria/schema.yaml
        description: 'What a dataset must satisfy to serve as this artifact: the variable
          it must carry, the units that variable may be in, the axes it must have,
          the grids it may be on, any schema it must conform to. See bblocks://ogc.focal.transferability.acceptanceCriteria.

          **This is what makes a `replace-with-local-equivalent` rule actionable.**
          The action says something must change; these say what would count as having
          changed it correctly, which is what a platform needs in order to accept
          or reject a candidate dataset on the user''s behalf rather than hand the
          question back to a person.

          It lives on the artifact rather than on the rule because it is a standing
          property of the interface, true whether or not anything is being transferred.
          A substitution is merely when it becomes visible. Optional, and thinly evidenced
          (UP-WF3, and loosely UP-WF2''s planned Eurostat input) because the questionnaires
          never asked.

          '
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/acceptanceCriteria
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
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/
  dcterms: http://purl.org/dc/terms/
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
    "transferabilityNotes": "rdfs:comment",
    "envelope": {
      "@context": {
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
        "acceptanceCriteria": {
          "@context": {
            "variable": {
              "@context": {
                "sameAsCurrent": "focal-transf-prop:sameAsCurrent"
              },
              "@id": "focal-transf-prop:variable"
            },
            "units": {
              "@context": {
                "@base": "http://qudt.org/vocab/unit/"
              },
              "@id": "focal-transf-prop:unit",
              "@type": "@id",
              "@container": "@set"
            },
            "axes": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/axes/"
              },
              "@id": "focal-transf-prop:axis",
              "@type": "@id",
              "@container": "@set"
            },
            "gridTypes": {
              "@context": {
                "@base": "https://w3id.org/ogc/hosted/focal/transferability/grid-types/"
              },
              "@id": "focal-transf-prop:gridType",
              "@type": "@id",
              "@container": "@set"
            },
            "conformsTo": {
              "@id": "dcterms:conformsTo",
              "@type": "@id",
              "@container": "@set"
            }
          },
          "@id": "focal-transf-prop:acceptanceCriteria"
        },
        "artifactRef": "focal-transf-prop:artifactRef"
      },
      "@id": "focal-transf-prop:artifacts",
      "@container": "@set"
    },
    "rules": {
      "@context": {
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
        "affects": {
          "@id": "focal-transf-prop:affects",
          "@container": "@set"
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
    "dcterms": "http://purl.org/dc/terms/",
    "focal-transf": "https://w3id.org/ogc/hosted/focal/transferability/",
    "prov": "http://www.w3.org/ns/prov#",
    "geo": "http://www.opengis.net/ont/geosparql#",
    "dcat": "http://www.w3.org/ns/dcat#",
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

