
# FOCAL Artifact Acceptance Criteria (Schema)

`ogc.focal.transferability.acceptanceCriteria` *v0.2*

What a dataset must satisfy to serve as a given artifact - variable name, acceptable units (QUDT), required axes, acceptable grids, schemas it must conform to. What makes replace-with-local-equivalent actionable rather than merely stated.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## FOCAL Artifact Acceptance Criteria

What a dataset has to satisfy to serve as a given artifact.

| Property | Combines as | Bound to |
|---|---|---|
| `variable` | single value | FOCAL (a local expectation, not a published fact) |
| `units` | **OR** — any one is acceptable | QUDT unit IRIs |
| `axes` | **AND** — all must be present | FOCAL axes scheme (open) |
| `gridTypes` | **OR** — any one is acceptable | FOCAL grid-types scheme, cross-walked to CF `grid_mapping_name` |
| `conformsTo` | **AND** | `dcterms:conformsTo` |

**Why this block exists.** `replace-with-local-equivalent` is the most common action in the FOCAL
corpus by a wide margin, and by itself it says something must change without saying what would
count as having changed it correctly. A platform asked whether it can run a workflow over a new
area with local data cannot answer from the action. It can answer from these criteria, checked
against a candidate file.

**These are properties of the artifact, not of the transfer.** UP-WF3's precipitation input needs
millimetres or kg m⁻²s⁻¹ and a time axis whether or not anyone is moving the workflow anywhere. The
requirement only becomes visible when a substitution is proposed, which is why it was first noticed
as a transferability fact, but it is a standing property of the interface. So it is stated once on
the artifact declaration in
[`transferabilityStatement`](bblocks://ogc.focal.transferability.transferabilityStatement), and
rules that call for a substitution reach it through the artifact id they already cite.

**`gridTypes` here is not a duplicate of the `grid-structure` envelope dimension.** They do
different jobs. An envelope constraint is a boundary a rule is *conditioned on*: cite it in `when`
and the rule fires when the target falls outside it. These criteria are a specification a candidate
is *checked against*, after a rule has already fired and said to substitute something. Same
vocabulary, two places in the decision.

**Evidenced 2/8**: UP-WF3 (the fullest contract in the corpus) and UP-WF2's planned Eurostat input.
The questionnaires never asked the question, so silence elsewhere is not evidence of absence — this
is the single most useful thing a workflow owner can add in review.

**Status: draft/WIP**, not yet exercised by a worked workflow example: UP-WF3, the workflow that
motivates it, is not modelled yet. The examples here are drawn from its questionnaire directly.

## Examples

### UP-WF3's precipitation source, the fullest contract in the corpus
UP-WF3 states, of any replacement precipitation dataset: the same variable name, the same unit
(mm or kg m⁻²s⁻¹), a time axis, and a grid that is regular lat/lon or rotated pole. Four
requirements, all checkable against a candidate NetCDF, and all of which the model previously
threw away — the workflow got a `replace-with-local-equivalent` action and nothing else, so a
consumer knew a substitution was needed but not what would satisfy it.

Note the three different logics in one object. `units` is an OR-set: millimetres and
kg m⁻²s⁻¹ are the accumulated and flux forms of the same quantity, and either is fine.
`gridTypes` is an OR-set for the same reason. `axes` is an AND: every axis listed must be
present, and there is no useful reading of "either a time axis or something else" for a
rolling accumulation.

The units are QUDT IRIs, whose published symbols are exactly `mm` and `kg/(m²·s)`. That
matters more than it looks: `mm`, `millimetre` and `mm/day` are three incomparable strings and
the last is a different quantity, so a consumer checking a candidate needs the quantity kind,
not the spelling.

#### json
```json
{
  "variable": { "sameAsCurrent": true },
  "units": ["MilliM", "KiloGM-PER-M2-SEC"],
  "axes": ["time"],
  "gridTypes": ["regular-latlon", "rotated-pole"],
  "transferabilityNotes": "From UP-WF3's questionnaire, which specifies its replacement contract more fully than any other in the set. The variable requirement is a relation in the source — 'same precipitation variable name as current dataset' — and is recorded as one. Naming a literal here would assert a name the source never gives, and would be wrong for one of the two paths the workflow reads: the field is `rr` in E-OBS and `pr` in CORDEX-family data."
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/acceptanceCriteria/context.jsonld",
  "variable": {
    "sameAsCurrent": true
  },
  "units": [
    "MilliM",
    "KiloGM-PER-M2-SEC"
  ],
  "axes": [
    "time"
  ],
  "gridTypes": [
    "regular-latlon",
    "rotated-pole"
  ],
  "transferabilityNotes": "From UP-WF3's questionnaire, which specifies its replacement contract more fully than any other in the set. The variable requirement is a relation in the source \u2014 'same precipitation variable name as current dataset' \u2014 and is recorded as one. Naming a literal here would assert a name the source never gives, and would be wrong for one of the two paths the workflow reads: the field is `rr` in E-OBS and `pr` in CORDEX-family data."
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] rdfs:comment "From UP-WF3's questionnaire, which specifies its replacement contract more fully than any other in the set. The variable requirement is a relation in the source — 'same precipitation variable name as current dataset' — and is recorded as one. Naming a literal here would assert a name the source never gives, and would be wrong for one of the two paths the workflow reads: the field is `rr` in E-OBS and `pr` in CORDEX-family data." ;
    focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> ;
    focal-transf-prop:gridType <https://w3id.org/ogc/hosted/focal/transferability/grid-types/regular-latlon>,
        <https://w3id.org/ogc/hosted/focal/transferability/grid-types/rotated-pole> ;
    focal-transf-prop:unit <http://qudt.org/vocab/unit/KiloGM-PER-M2-SEC>,
        <http://qudt.org/vocab/unit/MilliM> ;
    focal-transf-prop:variable [ focal-transf-prop:sameAsCurrent true ] .


```


### A schema requirement, on data that does not exist yet
UP-WF2's planned Heat Risk Indicator needs census or socio-economic data "preferably following
a schema compatible with Eurostat's". `conformsTo` is `dcterms:conformsTo`, which is what
catalogues already use to say a resource follows a specification.

Two honesty notes travel with this one. The source says *preferably*, so stating it as a
criterion is firmer than the questionnaire is, and the note says so rather than smoothing it
over. And the identifier here names Eurostat's census hub rather than a machine-readable
schema document, because no such document was cited; that is a real weakness in the criterion
and is recorded as one.

#### json
```json
{
  "conformsTo": ["https://ec.europa.eu/eurostat/web/population-and-housing-census"],
  "transferabilityNotes": "The source states this as a preference (\"preferably following a schema compatible with Eurostat\"), not a requirement, and cites no schema document, so the identifier names the programme rather than a schema a consumer could validate against. Both need confirmation from the workflow owner before this is treated as a check."
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/acceptanceCriteria/context.jsonld",
  "conformsTo": [
    "https://ec.europa.eu/eurostat/web/population-and-housing-census"
  ],
  "transferabilityNotes": "The source states this as a preference (\"preferably following a schema compatible with Eurostat\"), not a requirement, and cites no schema document, so the identifier names the programme rather than a schema a consumer could validate against. Both need confirmation from the workflow owner before this is treated as a check."
}
```

#### ttl
```ttl
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

[] dcterms:conformsTo <https://ec.europa.eu/eurostat/web/population-and-housing-census> ;
    rdfs:comment "The source states this as a preference (\"preferably following a schema compatible with Eurostat\"), not a requirement, and cites no schema document, so the identifier names the programme rather than a schema a consumer could validate against. Both need confirmation from the workflow owner before this is treated as a check." .


```


### A single criterion is a complete statement
Nothing obliges an artifact to state a full contract. One real criterion beats five invented
ones, and a partial contract still narrows what a consumer has to guess.

What is not allowed is criteria consisting only of a note: `shapes.shacl` rejects that. Free
text saying "must be a compatible climate dataset" reproduces exactly the problem this block
exists to solve, one level further down, while looking like it has been addressed.

#### json
```json
{
  "axes": ["time"]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/acceptanceCriteria/context.jsonld",
  "axes": [
    "time"
  ]
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .

[] focal-transf-prop:axis <https://w3id.org/ogc/hosted/focal/transferability/axes/time> .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Artifact Acceptance Criteria
description: "What a dataset has to satisfy to serve as a given artifact: the variable
  it must carry, the units that variable may be in, the axes it must have, the grids
  it may be on, and any schema it must conform to.\n**This is what makes `replace-with-local-equivalent`
  actionable.** That action is by far the most common in the FOCAL corpus, and on
  its own it says that something must change without saying what would count as having
  changed it correctly. A platform asked \"can I run this workflow over my area of
  interest with my data?\" cannot answer from the action alone. It can answer from
  these criteria, against a candidate file, with no human in the loop.\n**These are
  properties of the artifact, not of the transfer.** UP-WF3's precipitation input
  needs millimetres or kg m\u207B\xB2s\u207B\xB9 and a time axis whether or not anyone
  is moving the workflow anywhere; the requirement simply becomes visible when a substitution
  is proposed. So the criteria attach to the artifact declaration, where they are
  stated once, rather than to the rules that happen to invoke them. A rule saying
  `replace-with-local-equivalent` cites the artifact by id, and the criteria travel
  with it.\nEvery property is optional and at least one is required: a criteria object
  that only carries a note states no criterion. Where a requirement genuinely resists
  structuring, say it in `transferabilityNotes` rather than inventing a property for
  it.\n**Published vocabularies, not FOCAL ones, wherever one exists.** Units are
  QUDT unit IRIs (`MilliM`, `KiloGM-PER-M2-SEC`, whose QUDT symbols are exactly the
  `mm` and `kg/(m\xB2\xB7s)` UP-WF3 states). A schema requirement is `dcterms:conformsTo`.
  Grid types are the same FOCAL scheme bblocks://ogc.focal.transferability.envelopeConstraint
  uses, cross-walked to CF `grid_mapping_name`. Only `variable` and `axes` are FOCAL's
  own, and only because a workflow's internal expectation of what an input is called
  is not a published fact about anything.\n**Evidenced 2/8:** UP-WF3 states the fullest
  contract in the corpus (variable name, either of two units, a time axis, one of
  two grids); UP-WF2's planned Eurostat input states a schema compatibility preference.
  Expect this to grow: the question was never asked in the questionnaires, so absence
  here is not evidence that other workflows have no contract.\n"
allOf:
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/schema.yaml
- type: object
  anyOf:
  - required:
    - variable
  - required:
    - units
  - required:
    - axes
  - required:
    - gridTypes
  - required:
    - conformsTo
  properties:
    variable:
      oneOf:
      - type: string
        examples:
        - pr
        - rr
      - type: object
        title: Same as the current artifact
        required:
        - sameAsCurrent
        additionalProperties: false
        properties:
          sameAsCurrent:
            const: true
            x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/sameAsCurrent
      description: 'The name the workflow expects the variable to be called, either
        as a literal or as a relation to whatever the artifact currently in use carries.

        **The relation form is not a fallback for not knowing.** UP-WF3''s source
        says a replacement must have *"the same precipitation variable name as current
        dataset"*, and that is a complete, precise requirement stated as a relation.
        Recording a literal in its place (`rr`, say, guessed from the fact that one
        of the two current sources is E-OBS) asserts something the source did not,
        and is wrong outright if the workflow reads the CORDEX path where the same
        field is called `pr`. `{"sameAsCurrent": true}` states exactly the requirement,
        and a platform can evaluate it by reading the artifact in use. Use it when
        sameness *is* the claim; where the source names a value, name the value.

        A plain string rather than a term, deliberately. The obvious binding is a
        CF standard name (`precipitation_amount`), and a CF standard name is not what
        a NetCDF variable is called; the two coincide only by convention. Recording
        the actual name keeps the check honest. If a workflow owner supplies a standard
        name as well, that is a second fact and wants its own property, not a reinterpretation
        of this one.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/variable
    units:
      type: array
      minItems: 1
      items:
        type: string
        examples:
        - MilliM
        - KiloGM-PER-M2-SEC
      description: "The units the variable may be in, as QUDT unit IRIs (relative
        names resolve against `http://qudt.org/vocab/unit/`). **An OR-set:** any one
        is acceptable, which is UP-WF3's case exactly \u2014 millimetres or kg m\u207B\xB2s\u207B\xB9,
        the accumulated and the flux form of the same quantity.\nQUDT rather than
        a unit string, because `mm`, `millimetre` and `mm/day` are three incomparable
        strings and one of them is a different quantity. QUDT carries the symbol and
        the quantity kind, so a consumer can tell that a candidate in `kg/(m\xB2\xB7s)`
        satisfies this and one in metres does not.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/unit
      x-jsonld-type: '@id'
      x-jsonld-container: '@set'
      x-jsonld-base: http://qudt.org/vocab/unit/
    axes:
      type: array
      minItems: 1
      items:
        type: string
        examples:
        - time
      description: 'Axes the data must have, as concepts from the FOCAL axes scheme
        (see bblocks://ogc.focal.transferability.vocab). **Conjunctive**, unlike `units`
        and `gridTypes`: every axis listed must be present. UP-WF3 requires a time
        axis, without which its rolling accumulation has nothing to accumulate over.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/axis
      x-jsonld-type: '@id'
      x-jsonld-container: '@set'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/axes/
    gridTypes:
      type: array
      minItems: 1
      items:
        type: string
        examples:
        - regular-latlon
        - rotated-pole
      description: "The grids the data may be on, from the same open scheme an envelope
        constraint's `grid-structure` dimension uses. **An OR-set.**\nNot a duplicate
        of that dimension: the two do different jobs. An envelope constraint is a
        boundary a *rule is conditioned on* \u2014 cite it in `when` and the rule
        fires when the target falls outside it. These criteria are a specification
        a *candidate is checked against* once the rule has already fired and says
        to substitute something. State the constraint at the envelope when it bounds
        the workflow as a whole, and here when it binds this one artifact; UP-WF3
        happens to be a case where both readings are available, because its only gridded
        input is also the whole of its gridded interface.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/gridType
      x-jsonld-type: '@id'
      x-jsonld-container: '@set'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/grid-types/
    conformsTo:
      type: array
      minItems: 1
      items:
        $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/iri-or-curie/schema.yaml
      description: "Schemas or specifications the data must conform to, as identifiers.
        Uplifts to `dcterms:conformsTo`, the term catalogues already use for exactly
        this.\nUP-WF2's planned Heat Risk Indicator is the evidenced case: replacement
        census data \"preferably following a schema compatible with Eurostat's\".
        Note that source says *preferably*, so recording it here states it more firmly
        than the questionnaire does \u2014 which is a thing to check with the owner
        rather than to smooth over. Where the preference is genuinely soft, `transferabilityNotes`
        is the honest home for it.\n"
      x-jsonld-id: http://purl.org/dc/terms/conformsTo
      x-jsonld-type: '@id'
      x-jsonld-container: '@set'
    transferabilityNotes:
      type: string
      description: 'A requirement that does not reduce to the properties above, or
        a qualification on one that does. Uplifts to `rdfs:comment`. Mixed in from
        bblocks://ogc.focal.transferability.notes. Not a criterion on its own: a criteria
        object needs at least one structured property.

        '
      x-jsonld-id: http://www.w3.org/2000/01/rdf-schema#comment
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/
  dcterms: http://purl.org/dc/terms/
  rdfs: http://www.w3.org/2000/01/rdf-schema#

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/acceptanceCriteria/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/acceptanceCriteria/schema.yaml)


# JSON-LD Context

```jsonld
{
  "@context": {
    "transferabilityNotes": "rdfs:comment",
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
    },
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "dcterms": "http://purl.org/dc/terms/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/acceptanceCriteria/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/acceptanceCriteria`

