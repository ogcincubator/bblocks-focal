## FOCAL Transferability Vocabulary

Open SKOS concept schemes backing the FOCAL workflow transferability model (Task 10.3):

- **`transferabilityAction`** — what must be done to a reference/calibration artifact to make it
  valid outside a workflow's original validity envelope (e.g. `retrain`, `replace-with-local-equivalent`).
- **`triggeredBy`** — the condition that triggers a transferability rule (e.g. `different-ecological-range`).
- **dimensions** — the axes a workflow's validity envelope is stated along (spatial, ecological, ...).
  Seeded deliberately small; expected to grow as more workflows are reviewed.
- **roles** — `trained-on` / `valid-for` / `can-run-on`, independent of dimension. A workflow can
  state more than one role for the same dimension at once (see FP-WF1 in the mapping-extraction doc).

All four schemes are **open**, not closed enums — new concepts may be added by extending this
ontology, without a schema change on the blocks that reference it
([`transferability/rule`](bblocks://ogc.focal.transferability.rule),
[`transferability/envelopeConstraint`](bblocks://ogc.focal.transferability.envelopeConstraint)).

**Status: draft/WIP.** This is a first pass seeded from `20260817-workflow-transferability-mapping-extraction.md`
and `20260902-condition-action-expressivity.md` (FOCAL WP10 project directory) — circulated to workflow
owners for review, not locked.
