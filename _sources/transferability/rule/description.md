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
