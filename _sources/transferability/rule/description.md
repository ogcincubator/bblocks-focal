## FOCAL Transferability Rule

One condition/action rule attached to a reference or calibration artifact.

- `triggeredBy` — the condition that fires this rule (open vocabulary, see
  [`transferability/vocab`](bblocks://ogc.focal.transferability.vocab)).
- `actions` — an **OR-set**: any one of these actions resolves the rule. FP-WF1's growth model
  needs this — it offers both `retrain` and `replace-with-alternative-published-model` for the
  same artifact and the same trigger.
- `required` — whether applying one of `actions` is mandatory once `triggeredBy` holds. Defaults
  to `true`. `false` means the workflow still runs without it, but result quality/trust degrades —
  describe how in `transferabilityNotes` (mixed in from
  [`transferability/notes`](bblocks://ogc.focal.transferability.notes)). Example: FP-WF3's
  disturbance-detection workflow runs without local training labels, but results should then be
  treated as exploratory rather than authoritative.

**Known simplification (flagged for WF-owner review):** a small number of artifacts (UP-WF2's LST/
CLMS/Eurostat datasets) have a richer three-way condition — reuse inside a coverage boundary,
replace if a substitute exists outside it, hard-fail if none exists — than a flat rule list can
express without an explicit "only if a substitute is obtainable" branch condition. For now these
are represented as two separate flat rules (`reuse-as-is` / `replace-with-local-equivalent`),
dropping that connecting condition. See `20260902-condition-action-expressivity.md` in the FOCAL
WP10 project directory for the full pattern inventory this was decided against.

**Status: draft/WIP**, circulated for review, not locked.
