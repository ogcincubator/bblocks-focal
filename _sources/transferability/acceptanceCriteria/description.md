## FOCAL Artifact Acceptance Criteria

What a dataset has to satisfy to serve as a given artifact.

| Property | Combines as | Bound to |
|---|---|---|
| `variables` | **AND** — every entry must be satisfied | see below |
| `variables[].name` / `sameAsCurrent` | one of the two | FOCAL (a local expectation, not a published fact) |
| `variables[].standardName` | one value, or **OR** over a list | CF standard names |
| `variables[].units` | **OR** — any one is acceptable | QUDT unit IRIs |
| `temporal.resolution` | single value | `dcat:temporalResolution` |
| `temporal.calendar` | **OR** — accepted as they are | CF `calendar` values |
| `temporal.minimumPrecedingYears` | single value | FOCAL |
| `temporal.complete` | `true` = no gaps allowed in the required data | FOCAL |
| `temporal.startDate` / `endDate` | span the data must cover; `endDate` optional | `dcat:startDate` / `dcat:endDate` |
| `axes` | **AND** — all must be present | FOCAL axes scheme (open) |
| `gridTypes` | **OR** — any one is acceptable | FOCAL grid-types scheme, cross-walked to CF `grid_mapping_name` where one exists |
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

**Used by** FP-WF1, FP-WF2, FP-WF5, UP-WF2 and UP-WF3. No current record uses `conformsTo`. The
questionnaires never asked the question, so silence elsewhere is not evidence of absence.

**Status: draft/WIP**, but exercised: five workflow examples use it. The examples here
are drawn from the UP-WF3 questionnaire and from a daily climate input.
