# Intervention-choice transfer

An independent Construct-2 ancillary study, commissioned on 28 September 2026.
The broader question is how agents accumulate useful experience across sessions
and where that experience should live. This study asks:

> Can outcomes from earlier interventions improve adaptation decisions on fresh
> work after the receiving agent or interface changes, beyond competent current
> diagnosis and unchanged reuse of the old decision policy?

**Status, 29 September 2026:** the first bounded experiment and a source-only
follow-up are complete. Across 84 participant model calls, a persisted chooser
learned from earlier intervention outcomes but did not beat ordinary reuse after
an API change. On 18 fresh source cases, direct generation solved 14, the canonical
adapter 17, and the inherited category policy 16. A subsequent ordinary parser
solved 36/36 fresh API tasks (18 new cases × two interfaces) with no model calls.
This exposes a limitation of the authored source grammar, not a general negative
result about learning intervention choices.

Read the [findings and limitations](reports/phase1-findings.md),
[initial protocol](protocols/phase1.md), [follow-up protocol](protocols/followup.md)
and [source ledger](sources/ledger.md). All failed outputs are preserved.
The phase is closed on explanatory progress; the wider question remains open.
No model job is running and no user action is required. Further selector search
on this grammar is unjustified. The next distinct workload should first establish
trustworthy labels and residual remedy complementarity on independently authored
language after ordinary parsing, retrieval and repair.

## Evidence and reproduction

- [Acquired decision table](evidence/policy.json), frozen before fresh evaluation.
- [Development outcomes](evidence/development/summary.json),
  [acquisition](evidence/acquisition/summary.json),
  [fresh policy comparisons](evidence/confirmation/policies.json),
  [comparisons with shared repair](evidence/confirmation/repaired-policies.json).
- [Fresh source-parser results](evidence/parser-confirmation/summary.json),
  [cost ledger](evidence/costs.json), [audit](evidence/audit.json).
- [Provenance](evidence/provenance/investigator.json) and
  [resource record](notes/resource-use.md). Raw prompts, responses, usage and labels
  are colocated in each evidence directory.

Offline checks require no serving resource:

```sh
uv sync --frozen
uv run python -m unittest discover -s tests -v
uv run python src/audit.py
```

For live reproduction in a separate checkout, preserve the archived policy and
use new output paths (the runner rejects overwrites):

```sh
uv run python src/experiment.py run --seed 110 --per-group 2 --interfaces v1 v2 --output evidence/replay-development
uv run python src/experiment.py run --seed 220 --per-group 4 --interfaces v1 --output evidence/replay-acquisition
uv run python src/experiment.py acquire evidence/replay-acquisition/outcomes.jsonl
uv run python src/experiment.py run --seed 330 --per-group 6 --interfaces v2 --output evidence/replay-confirmation
uv run python src/repair_control.py evidence/replay-confirmation/outcomes.jsonl
uv run python src/source_parser.py --fresh --output evidence/replay-parser
```

The model endpoint, model identity, decoding settings and source generator are in
[src/experiment.py](src/experiment.py). Exact recorded revisions are in the report
and manifests. These are offline policy replays on measured alternatives, not
live autonomous chooser-agent runs. Source-parser reproduction is CPU-only.
Read [AGENTS.md](AGENTS.md), [BACKGROUND.md](BACKGROUND.md) and [START.md](START.md)
for the original remit and starting context.

## What is being learned?

Distinguish three objects: a capability that can be changed, records of earlier
interventions and outcomes, and the policy that chooses the next intervention.
Improving candidate remedies can improve task performance without improving the
choice among them. A useful marginal comparison holds the receiving state and
available remedy generators comparable while testing the contribution of decision
experience. Joint development remains allowed when its contribution is identified.

A learned decision policy can live in explicit records, revised instructions,
code or weights. Neural training is optional. Actions may include retaining the
current arrangement, reusing a working remedy, acquiring an observation or applying
a short sequence of changes. Begin with a small credible action set and one
material recipient or interface change; a five-substrate tournament is unnecessary.

This develops the root's existing AD1–AD2 expectations. It does not restart the
completed maintenance-decision study or redirect experience-guided investigation
and EBM exploration. Their publications may inform this study, but their ongoing
work is not a dependency.

## Initial expectation

Develop a bounded comparison in which the consequences of remedies can be checked
through complete later tasks and still-valid obligations. Discover whether prior
outcomes change a useful decision beyond what current observations already reveal.
Different failure labels or different remedy scores alone do not establish that
opportunity. Investigate whether one action dominates, a simple diagnostic rule
already suffices, or inherited decisions continue to work unchanged.

The ordinary alternatives should be competent: a good fixed remedy or sequence,
a developed current-state rule and unchanged reuse of an earlier decision policy,
as relevant to the selected question. Preserve their access to source evidence,
retrieval, caching, existing code and ordinary repair. Do not manufacture a
learning advantage by withholding an effective ordinary capability.

Record what the experimental decision maker actually experienced and what survives
between sessions. Public results, investigator-authored lessons, imported model
knowledge and feedback earned through its own intervention attempts are distinct
sources. The relevant transfer boundary is a new receiving state or history,
not simply new wording or shuffled identifiers. It is legitimate to start with
a narrower within-state acquisition diagnostic before attempting transfer.

Select the smallest contrasts that distinguish your leading explanations. A
complete factorial design is not required. If acquisition fails, pursue bounded
diagnosis or establish a concrete limitation; finite gradients or changed outputs
alone do not establish useful learning. Preserve failed runs. Confirm claims
developed through diagnosis on fresh material, with eligible history separated
from later evaluation outcomes.

Judge complete subsequent work, including obligations that should remain valid.
Record costs for discovery, candidate construction, trial interventions, failed
attempts, observation, acquisition, selection, use and maintenance. Keep native
units separate unless a utility conversion is justified. A retrospective best
choice is a diagnostic bound, not a free deployable policy. An explained absence
of decision value, a stable cheap rule or a demonstrated resource limitation is
a useful result; a learned-policy win is not required.

## Starting assets and autonomy

[BACKGROUND.md](BACKGROUND.md) identifies public methods, a pinned ModularRSI
release and earlier local limits. They are leads, not an adopted workload or
validated treatment. Reuse a platform only when its integration cost serves the
question. Motivated authored tasks are allowed with their construction explicit.
Workload discovery belongs to this study and need not be completed by root first.

Own the methods, protocols, implementation, model choices and bounded next steps.
Do not return routine choices to root. Publication does not automatically close
the wider question; continue useful development within the remit, explaining
any substantial change of question. Close a phase on explanatory progress, a
demonstrated limitation or a concrete resource constraint.

## Resources and publication

Investigators and reviewers use `gpt-6-astra`; record actual reasoning settings
and model provenance. Experimental participant, learner and teacher models remain
scientific choices. [AGENTS.md](AGENTS.md) gives the available serving resources,
dependency conventions and evidence practices.

Publish findings here with exact source/code/model revisions, saved outcomes,
failed attempts, costs, limitations and reproduction instructions. Keep this
README current and distinguish preparation, exploration and confirmation. Root
reviews claims and synthesizes their implications; detailed experimental evidence
and operational ownership remain here.
