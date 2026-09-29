
# FOCAL Transferability Rule (Schema)

`ogc.focal.transferability.rule` *v0.7*

What must happen, to which artifacts, under which envelope conditions. Conditions cite envelope constraints by id and are conjunctive; actions are an OR-set.

[*Status*](http://www.opengis.net/def/status): Under development

## Description

## FOCAL Transferability Rule

What must happen, to which artifacts, under which envelope conditions.

- `appliesTo` — the artifacts this rule governs, by `id`. FP-WF2's four Czechia-specific reference
  files share one rule rather than carrying four copies of the same condition.
- `when` — the conditions, each citing an envelope constraint by `id` plus how the target is
  tested against it. **Conjunctive: all must hold.**
- `triggeredBy` — a coarse alternative for cases where no constraint can be cited without
  inventing one. At least one of `when` or `triggeredBy` is required; prefer `when`.
- `actions` — an **OR-set**: any one resolves the rule, never a sequence or a combination.
- `affects` — JSON Pointers to what stops working, or works differently, if the terminal branch is
  taken. This is what gives `component-not-executable` an object: without it, "a component cannot
  run" and "the workflow cannot run" are one statement, and per-artifact answers cannot be rolled
  up into the per-workflow verdict a deployment platform has to produce. UP-WF2 loses one step in
  Kyiv, not the run.
- `mandatory` — whether applying one is required once the conditions hold. `false` means the
  workflow still runs with degraded trust, and `transferabilityNotes` must then say what degrades;
  `shapes.shacl` enforces that, because a skippable rule with no stated consequence tells a
  consumer nothing they can act on.

**Rules are exceptions, not a decision table.** A statement lists what has to change; an artifact
no rule fires for is reused unchanged. That default is what stops "no rule fires" from being
ambiguous between *nothing needs doing* and *nobody checked* — the ambiguity is closed structurally
instead, since a statement cannot omit `rules`, so writing none is deliberate. A rule stating
`reuse-as-is` therefore restates the default: worth writing where it makes a cascade legible, and
noise otherwise. It also has no use for `mandatory`, since "you must do nothing" is not an
instruction.

**AND, OR, and why there is no boolean expression language.** `when` is an AND and `actions` is an
OR. A disjunction of *conditions* is written as two rules. That is a deliberate limit: two
conditions leading to the same action really are two statements, and keeping them apart keeps each
traceable to the sentence in a questionnaire it came from, which a nested expression does not.
UP-WF2's three-way logic — reuse inside the domain, substitute or fail outside it — is two rules
over one constraint, `inside` then `outside`, with nothing dropped.

**What this replaced.** Rules used to be nested inside artifacts and carried only a vocabulary term
for their condition, so nothing connected a rule to the boundary it tested. UP-WF2 had two
footprints, three artifacts and three rules all saying "different geographic coverage", and no way
to record which was which.

**Status: draft/WIP**, circulated for review, not locked.

## Examples

### Rule citing an envelope constraint
FP-WF1's trained growth model outside the ecological range it was calibrated for. Two actions
are offered and either resolves the rule: retrain against local data, or substitute a
different already-published model. `actions` is an OR-set, never a sequence.

`when` names the constraint this is evaluated against, by the `id` it carries in the
enclosing statement's `envelope`. That is the difference between a rule a person reads and
one a consumer can act on: it says *which* boundary, and if that boundary is spatial its
value is a GeoSPARQL geometry.

#### json
```json
{
  "appliesTo": ["growth-model"],
  "when": [{ "constraint": "ecological-range", "test": "outside" }],
  "actions": ["retrain", "replace-with-alternative-published-model"],
  "mandatory": true
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/context.jsonld",
  "appliesTo": [
    "growth-model"
  ],
  "when": [
    {
      "constraint": "ecological-range",
      "test": "outside"
    }
  ],
  "actions": [
    "retrain",
    "replace-with-alternative-published-model"
  ],
  "mandatory": true
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-alternative-published-model>,
        <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/growth-model> ;
    focal-transf-prop:mandatory true ;
    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/ecological-range> ;
            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] .


```


### One rule over several artifacts
FP-WF2's four Czechia-specific reference artifacts share one boundary and one action, so
they share one rule. Previously this was the same condition copied four times with nothing
recording that they were the same fact.

#### json
```json
{
  "appliesTo": ["tolerances", "slt-t5", "species-codes", "rasdaman"],
  "when": [{ "constraint": "czechia", "test": "outside" }],
  "actions": ["replace-with-local-equivalent"],
  "mandatory": true
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/context.jsonld",
  "appliesTo": [
    "tolerances",
    "slt-t5",
    "species-codes",
    "rasdaman"
  ],
  "when": [
    {
      "constraint": "czechia",
      "test": "outside"
    }
  ],
  "actions": [
    "replace-with-local-equivalent"
  ],
  "mandatory": true
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/rasdaman>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/slt-t5>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/species-codes>,
        <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/tolerances> ;
    focal-transf-prop:mandatory true ;
    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/czechia> ;
            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] .


```


### Conjunctive conditions (AND)
Two conditions in one `when` mean both must hold. This is the case nesting rules under
artifacts could not express: an artifact bounded on two axes at once, needing adaptation only
when the target falls outside both. The two axes here are genuinely different in kind: a
coverage footprint (spatial, a geometry) and a grid structure (a set of accepted grid types),
and both are machine-evaluable.

A disjunction is written as two rules instead. That is deliberate: two conditions leading to
the same action really are two statements, and keeping them separate keeps each traceable to
the sentence it came from, which a nested boolean expression does not.

#### json
```json
{
  "appliesTo": ["lst"],
  "when": [
    { "constraint": "eur11-domain", "test": "outside" },
    { "constraint": "eur11-grid", "test": "outside" }
  ],
  "actions": ["replace-with-local-equivalent"],
  "mandatory": true
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/context.jsonld",
  "appliesTo": [
    "lst"
  ],
  "when": [
    {
      "constraint": "eur11-domain",
      "test": "outside"
    },
    {
      "constraint": "eur11-grid",
      "test": "outside"
    }
  ],
  "actions": [
    "replace-with-local-equivalent"
  ],
  "mandatory": true
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/lst> ;
    focal-transf-prop:mandatory true ;
    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/eur11-domain> ;
            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ],
        [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/eur11-grid> ;
            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] .


```


### The complementary case (inside), completing a cascade
`inside` is what lets UP-WF2's three-way logic be stated without losing its connecting
condition. Reuse within the domain is this rule; substitute-or-fail outside it is a second
rule over the same constraint. Previously the model had two flat rules and dropped the link
between them.

This rule restates the default (an artifact no rule fires for is reused unchanged), so it
adds no obligation — which is why it carries no `mandatory`: "you must do nothing" is not an
instruction. It earns its place by making the cascade legible, not by changing any answer.

#### json
```json
{
  "appliesTo": ["lst"],
  "when": [{ "constraint": "eur11-domain", "test": "inside" }],
  "actions": ["reuse-as-is"]
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/context.jsonld",
  "appliesTo": [
    "lst"
  ],
  "when": [
    {
      "constraint": "eur11-domain",
      "test": "inside"
    }
  ],
  "actions": [
    "reuse-as-is"
  ]
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .

[] focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/reuse-as-is> ;
    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/lst> ;
    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/eur11-domain> ;
            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/inside> ] .


```


### Non-mandatory rule (runs anyway, with degraded trust)
FP-WF3's disturbance detection without local training labels. The workflow still produces
output, so this is not a hard requirement, but the output means something weaker.

`mandatory: false` obliges `transferabilityNotes` to say what is lost; `shapes.shacl` rejects
the pairing without it, because a skippable rule with no stated consequence tells a consumer
nothing they can act on.

#### json
```json
{
  "appliesTo": ["labels"],
  "when": [{ "constraint": "label-extent", "test": "outside" }],
  "actions": ["retrain"],
  "mandatory": false,
  "transferabilityNotes": "Without local training labels, results should be treated as exploratory rather than blocked outright — a degraded-mode caveat, not a hard requirement."
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/context.jsonld",
  "appliesTo": [
    "labels"
  ],
  "when": [
    {
      "constraint": "label-extent",
      "test": "outside"
    }
  ],
  "actions": [
    "retrain"
  ],
  "mandatory": false,
  "transferabilityNotes": "Without local training labels, results should be treated as exploratory rather than blocked outright \u2014 a degraded-mode caveat, not a hard requirement."
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] rdfs:comment "Without local training labels, results should be treated as exploratory rather than blocked outright — a degraded-mode caveat, not a hard requirement." ;
    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/retrain> ;
    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/labels> ;
    focal-transf-prop:mandatory false ;
    focal-transf-prop:when [ focal-transf-prop:constraint <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/label-extent> ;
            focal-transf-prop:test <https://w3id.org/ogc/hosted/focal/transferability/tests/outside> ] .


```


### Coarse fallback when no constraint can be cited
UP-WF2's planned Eurostat input is not implemented yet, so there is no envelope fact to point
at. `triggeredBy` states the condition coarsely rather than forcing an invented boundary.

At least one of `when` or `triggeredBy` is required, so no rule is left with no stated
condition at all. Prefer `when` wherever a constraint exists to cite.

`affects` names what stops working if the terminal branch of the OR-set is the one taken.
Without it `component-not-executable` has no object, and a consumer cannot tell losing one
step from losing the run.

#### json
```json
{
  "appliesTo": ["eurostat"],
  "triggeredBy": "different-geographic-coverage",
  "actions": ["replace-with-local-equivalent", "component-not-executable"],
  "affects": ["/steps/heat_risk_indicator"],
  "mandatory": true,
  "transferabilityNotes": "Not yet implemented; once built, the planned Heat Risk Indicator would not be executable without it."
}

```

#### jsonld
```jsonld
{
  "@context": "https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/context.jsonld",
  "appliesTo": [
    "eurostat"
  ],
  "triggeredBy": "different-geographic-coverage",
  "actions": [
    "replace-with-local-equivalent",
    "component-not-executable"
  ],
  "affects": [
    "/steps/heat_risk_indicator"
  ],
  "mandatory": true,
  "transferabilityNotes": "Not yet implemented; once built, the planned Heat Risk Indicator would not be executable without it."
}
```

#### ttl
```ttl
@prefix focal-transf-prop: <https://w3id.org/ogc/hosted/focal/transferability/properties/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] rdfs:comment "Not yet implemented; once built, the planned Heat Risk Indicator would not be executable without it." ;
    focal-transf-prop:actions <https://w3id.org/ogc/hosted/focal/transferability/actions/component-not-executable>,
        <https://w3id.org/ogc/hosted/focal/transferability/actions/replace-with-local-equivalent> ;
    focal-transf-prop:affects "/steps/heat_risk_indicator" ;
    focal-transf-prop:appliesTo <https://w3id.org/ogc/hosted/focal/transferability/examples/rule/eurostat> ;
    focal-transf-prop:mandatory true ;
    focal-transf-prop:triggeredBy <https://w3id.org/ogc/hosted/focal/transferability/triggers/different-geographic-coverage> .


```

## Schema

```yaml
$schema: https://json-schema.org/draft/2020-12/schema
title: Transferability Rule
description: "What must happen, to which artifacts, under which envelope conditions.\n-
  `appliesTo` \u2014 the artifacts this rule governs, by `id`. Omit it for a rule
  about the workflow\n  as a whole.\n- `when` \u2014 the conditions, each citing an
  envelope constraint by `id` and how the target is\n  tested against it (`inside`/`outside`).
  **Conjunctive: all of them must hold.** A disjunction\n  is written as two rules.\n-
  `actions` \u2014 an **OR-set**: any one resolves the rule. Never a sequence, never
  a combination to\n  apply together.\n- `affects` \u2014 which parts of the annotated
  document stop working, or work differently, if this\n  rule's outcome is the terminal
  one.\n- `mandatory` \u2014 whether applying one is required once the conditions
  hold.\n**Rules are exceptions, not a complete decision table.** A statement's rules
  say what has to change; anything they do not mention is reusable unchanged. So an
  artifact with no rule firing for a given target is reused as-is, and a rule stating
  `reuse-as-is` explicitly is documenting the default rather than adding to it (worth
  doing where it makes a cascade legible, as UP-WF2's inside/outside pair does, and
  redundant otherwise). See bblocks://ogc.focal.transferability.transferabilityStatement
  for why that default is safe here: a statement cannot omit `rules`, so writing none
  is a deliberate act rather than an oversight.\n**`when` is what makes a rule evaluable
  rather than merely readable.** `triggeredBy: different-geographic-coverage` is a
  string a person reads; `when: [{constraint: clms-coverage, test: outside}]` names
  the boundary, and if that constraint's dimension is spatial its value is a `geo:asWKT`
  geometry, so a GeoSPARQL engine can settle the question with `geof:sfWithin`. Where
  the cited constraint is prose-valued (a comparable ecological range), the same structure
  records a judgement a person still has to make \u2014 which is honest about where
  automation stops rather than pretending the whole model is machine-decidable.\n`triggeredBy`
  is kept, but optional: not every evidenced FOCAL case has a constraint precise enough
  to cite, and forcing one would mean inventing boundaries. At least one of `when`
  or `triggeredBy` is required, so no rule is left with no stated condition at all.
  Prefer `when`.\n"
allOf:
- $ref: https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/notes/schema.yaml
- type: object
  required:
  - actions
  anyOf:
  - required:
    - when
  - required:
    - triggeredBy
  properties:
    appliesTo:
      type: array
      minItems: 1
      items:
        $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/iri-or-curie/schema.yaml
      description: "Identifiers of the artifacts this rule governs, from the enclosing
        statement's `artifacts`. Several artifacts may share one rule \u2014 FP-WF2's
        four Czechia-specific reference files do. Omit for a rule that applies to
        the workflow as a whole.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/appliesTo
      x-jsonld-type: '@id'
      x-jsonld-container: '@set'
    when:
      type: array
      minItems: 1
      items:
        $ref: '#/$defs/condition'
      description: 'The conditions under which this rule fires, ANDed together. Two
        conditions here mean both must hold; two rules mean either suffices.

        '
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/when
      x-jsonld-container: '@set'
    triggeredBy:
      type: string
      examples:
      - different-geographic-coverage
      - different-ecological-range
      - different-climate-regime
      - different-dataset
      description: "A coarse statement of what fires this rule, for cases where no
        envelope constraint can be cited precisely. Open vocabulary \u2014 see bblocks://ogc.focal.transferability.vocab.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/triggeredBy
      x-jsonld-type: '@id'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/triggers/
    affects:
      type: array
      minItems: 1
      items:
        type: string
        format: json-pointer
        pattern: ^/
      description: "JSON Pointers (RFC 6901) to the parts of the annotated document
        this rule's outcome bears on \u2014 for the CWL profile in bblocks://ogc.focal.transferability.workflow,
        typically `/steps/<id>` or `/outputs/<id>`, though the pointer carries no
        CWL assumption.\n**This is what `component-not-executable` needs to be actionable.**
        Without it the action names no component, so \"hot-spot characterization cannot
        run\" and \"the workflow cannot run\" are the same statement, and per-artifact
        answers cannot be assembled into the per-workflow verdict (*runs as is* /
        *runs in part* / *cannot run here*) that a deployment platform actually has
        to produce. UP-WF2 is the evidenced case: losing CLMS costs it one step, not
        the run.\nOptional, and meaningful for any action: a `replace-with-local-equivalent`
        rule may equally name the outputs whose quality changes. Omit it rather than
        guess, the same way `artifactRef` is omitted where no real Application Package
        exists to point into.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/affects
      x-jsonld-container: '@set'
    actions:
      type: array
      minItems: 1
      items:
        type: string
        examples:
        - reuse-as-is
        - replace-with-local-equivalent
        - retrain
        - replace-with-alternative-published-model
        - component-not-executable
      description: "One or more actions, any of which resolves the rule \u2014 an
        OR-set, not a required combination. No evidenced case needs two applied simultaneously.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/actions
      x-jsonld-type: '@id'
      x-jsonld-container: '@set'
      x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/actions/
    mandatory:
      type: boolean
      default: true
      description: "Whether applying one of `actions` is mandatory once the conditions
        hold. Defaults to true. When false, skipping is allowed but degrades result
        quality or trust rather than blocking execution \u2014 say what degrades in
        `transferabilityNotes`.\nSays nothing on a rule whose only action is `reuse-as-is`:
        \"you must do nothing\" and \"you may do nothing\" are the same instruction.
        Omit it there.\nNamed `mandatory` rather than `required`: a data property
        spelled like a JSON Schema keyword reads as the keyword, and this one sits
        beside real `required` lists.\n"
      x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/mandatory
$defs:
  condition:
    title: Envelope condition
    type: object
    required:
    - constraint
    - test
    additionalProperties: false
    properties:
      constraint:
        $ref: https://opengeospatial.github.io/bblocks/annotated-schemas/ogc-utils/iri-or-curie/schema.yaml
        description: "The `id` of an envelope constraint in the enclosing statement's
          `envelope`, written the same way it is declared there \u2014 an IRI, a CURIE,
          or a bare local name. Whichever form is used, the constraint must still
          be declared in the statement, so a reader has the extent in front of them
          rather than a bare identifier: a global identifier makes a boundary shareable,
          it does not make it fetchable.\n"
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/constraint
        x-jsonld-type: '@id'
      test:
        type: string
        examples:
        - outside
        - inside
        description: "How the target is compared against that constraint. `outside`
          is the condition under which almost every evidenced FOCAL rule fires; `inside`
          states the complementary case, which is what lets a cascade be written without
          losing its connecting condition \u2014 UP-WF2's \"reuse within the domain,
          otherwise substitute or fail\" is two rules over the same constraint. Open
          vocabulary \u2014 see bblocks://ogc.focal.transferability.vocab, where each
          term also records how it is evaluated per dimension.\n"
        x-jsonld-id: https://w3id.org/ogc/hosted/focal/transferability/properties/test
        x-jsonld-type: '@id'
        x-jsonld-base: https://w3id.org/ogc/hosted/focal/transferability/tests/
x-jsonld-prefixes:
  focal-transf-prop: https://w3id.org/ogc/hosted/focal/transferability/properties/

```

Links to the schema:

* YAML version: [schema.yaml](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/schema.json)
* JSON version: [schema.json](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/schema.yaml)


# JSON-LD Context

```jsonld
{
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
    "mandatory": "focal-transf-prop:mandatory",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "focal-transf-prop": "https://w3id.org/ogc/hosted/focal/transferability/properties/",
    "@version": 1.1
  }
}
```

You can find the full JSON-LD context here:
[context.jsonld](https://ogcincubator.github.io/bblocks-focal/build/annotated/focal/transferability/rule/context.jsonld)


# For developers

The source code for this Building Block can be found in the following repository:

* URL: [https://github.com/ogcincubator/bblocks-focal](https://github.com/ogcincubator/bblocks-focal)
* Path: `_sources/transferability/rule`

