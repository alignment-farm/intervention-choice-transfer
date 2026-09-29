# Invoice-interface transfer: ordinary reuse limits the value of learned choice

29 September 2026. Completed bounded workload phase; broader remit remains open.
Investigator: gpt-6-astra, medium reasoning, OpenAI, Codex CLI 0.158.0. This is an
investigator report with automated consistency checks, not independent review.

## Finding

Earlier outcome feedback produced a functioning persisted category chooser, but
it did not improve complete fresh work beyond ordinary reuse. On 18 fresh tasks
after a flat-to-nested API change, the inherited category chooser solved 16, the
fixed canonical adapter 17, and a prespecified schema-aware ordinary rule 17.
A best-of-two retrospective oracle solved 18; it is not a deployable policy.

A subsequent bounded diagnosis established a stronger limitation. The authored
source grammar is invertible by a short ordinary parser. Frozen before its own
fresh test, this parser solved 36/36 complete tasks (18 new source cases × two
interfaces), without model requests. No marginal chooser value is established on
this workload. This finding concerns the selected grammar, model and interfaces;
it does not reject the wider intervention-choice-transfer hypothesis.

## Experimental objects and boundaries

Receiver: Docker Model Runner's `docker.io/ai/qwen3:8B-Q4_K_M`, reported 8.19B,
GGUF, mixed `IQ2_XXS/Q4_K_M`, manifest digest
`79fa56c07429f64f41950fe2f524937cf3ae9ea9bd3d7ada72170b036ea3cc85`.
The runtime reports llama-server commit 72874f5. Docker Desktop 4.92.0, Engine 29.8.0,
Python 3.14.7, uv 0.12.13. Full inspection output is in `evidence/provenance/`.
No downloaded weights, training, gradient claim or model replacement.

Each task contains two authored prose invoice records. Obligations include exact
ID, supplier and memo; final corrected monetary amount; correct currency scale;
unknown deadlines remaining null; cancellation without dropping the invoice;
and first-mention order. The complete task is producing the API payload; it is
not an actual payment workflow. Tasks use fixed sentence templates with randomized
values, not independently authored natural documents. IDs include cohort seeds.

V1 is a flat row API. V2 changes to an ID-keyed nested object, an explicit order
array, decomposed date fields and a cancellation boolean. Obligations persist.
The model stays fixed, so this is interface transfer only. Both contracts were
authored and available before execution. Their adapters do not simulate the
cost of an unforeseen production migration.

Available remedies were fixed before participant runs:

- **D:** prompt the model for the current target payload directly.
- **C:** prompt for a canonical record with a decimal-string amount, then run an
  exact Decimal/date adapter to the target API.

Both receive the complete source, semantic instructions and a worked schema
example. Shared preprocessing strips code fences/think tags. Temperature 0,
max 1000 completion tokens, `/no_think`; all 84 responses ended with `stop`.
No substantive prompt revision or remedy replacement occurred during phase 1.
The examples, adapter and feature vocabulary are investigator-authored supervision.

The retained learned object is `evidence/policy.json`,723 bytes: empirical success
counts by source category/action, category choices and one global choice. A new
process loaded that file after acquisition. Its SHA-256 was recorded in the
fresh-run manifest and checked unchanged afterward. The actual update was
counting 24 eligible old-interface intervention outcomes. The table has no access
to later labels. Models receive source text only, never ground truth.

The feature categories—plain, explicit correction and JPY/KWD precision—are
handwritten inductive bias. Choice maximizes category success rate; ties choose D.
Acquisition counts were plain D 3/4 versus C 4/4; correction D 3/4 versus C 4/4;
precision D 4/4 versus C 4/4. Thus the inherited mapping is C/C/D, while the old
global winner is C. The preference for D in precision is a tie rule, not learned
evidence that D is superior. No new-interface retraining was performed.

## Sequence, complete outcomes and diagnosis

Protocol/code were committed before generation. Development seed 110 used six
source cases and both remedies on both interfaces (24 calls). D and C each
solved 6/6 on V1. On V2, D solved 3/6 and C 6/6. Every D failure mistyped the second
ID in the redundant order array. This paired development comparison establishes
that the new interface can matter on these cases; it is not a fresh causal
estimate of an average interface effect.

Acquisition seed 220 used 12 different sources on V1 (24 calls). D solved 10/12 and
C 12/12. Both D failures were structurally valid incorrect monetary values.
Those failures and the earlier failed outputs remain in the evidence.

Before fresh testing, a narrow ordinary source repair was frozen: when emitted
record keys match source IDs exactly, rebuild redundant order from source order.
It changes no semantic fields and is supplied equally to all policies. It was
motivated by development; it is authored remedy improvement, not chooser learning.

Fresh seed 330 used 18 different sources on V2 (36 calls), without policy changes.

| Policy | Exact complete, raw | Exact complete, shared order repair | Raw deployed calls |
|---|---:|---:|---:|
| Fixed direct D |14/18|15/18|18|
| Fixed canonical C |17/18|17/18|18|
| Inherited category C/C/D |16/18|17/18|18|
| Inherited global C |17/18|17/18|18|
| Current-source rule: D plain, C otherwise |16/18|16/18|18|
| Schema-aware ordinary reuse: C on nested API |17/18|17/18|18|
| D, then C if structurally invalid |16/18|16/18|20|
| Retrospective best of D/C |18/18|18/18|not deployable|

These are paired offline replay policies on executed action outcomes, not live
agent deliberations. The raw and repaired versions use the same model outputs;
they are not independent replicates. Repair reduces fallback calls from 20 to 19.
The inherited global chooser and schema-aware rule coincide with fixed C here;
they are comparator identities, not three independent confirmations.

D's four fresh failures were: one tenfold monetary error after a correction;
one bad order ID; one malformed JSON output; and one consistently mistyped ID in
the record key and order. C's single failure extracted 389.177 KWD as the major-unit
string 389177; the correctly functioning adapter then multiplied it by 1000.
This is a receiving-model extraction error, not an arithmetic bug in the adapter.
Structural validation alone cannot detect these valid-looking semantic failures.
Raw validity was D 16/18 and C 18/18; exact success was lower.

Thus the candidate remedies are functioning and complementary on one case, but
that complementarity does not imply useful learned choice. The inherited table
loses two precision cases to D while avoiding C's one precision failure. It trails
ordinary fixed reuse before repair and ties it afterward. There is no measured
benefit that would justify its additional acquisition cost. Sparse counts and a
prespecified tie rule limit any interpretation as robust category acquisition.
No significance or population-level advantage is claimed.

## Follow-up: expose the ordinary source baseline

The seed 330 failures motivated inspecting the full input contract. Both sentence
forms encode all required fields unambiguously, so ordinary parsing is sufficient.
`src/source_parser.py` accepts only that disclosed grammar, applies corrections,
preserves untouched obligations and rejects unsupported text. It has source-only
access and feeds the same adapter. It does not consult case IDs, gold records,
policy labels or historical outcomes at runtime.

It first solved 72/72 development API tasks reconstructed from the 36 earlier
source cases. This is development evidence. The follow-up protocol and parser
were then committed at 9eb5073 before source-only evaluation of seed 440. On 18 fresh sources,
including both interfaces, it solved 36/36 exact payloads with 0 model calls. The
scorer independently reconstructs target fields, avoiding sole reliance on the
adapter used by the treatment. This demonstrates a functioning ordinary remedy
for this grammar. Parser correctness beyond these sentence forms is not claimed;
a real deployment could fall back after rejection, but no outside-grammar
rejection or fallback rate was measured.

The follow-up is a better-remedy result, separate from better intervention
decisions. It removes the reason to spend additional chooser search on this task
family. No claim about parser superiority on natural invoice documents follows.

## Costs and provenance

| Actual phase | Requests | Prompt tokens | Completion tokens | Summed request seconds |
|---|---:|---:|---:|---:|
| Development/trials |24|9,190|3,746|75.53|
| Acquisition |24|8,806|3,062|59.92|
| Fresh action evaluation |36|14,184|6,120|117.85|
| **Total** |**84**|**32,180**|**12,928**|**253.29**|

Ten complete-task failures are included in these costs. There were no generation
transport failures or retries. One SSH resource-discovery attempt failed host-key
verification; local inspection and the HTTP endpoint worked. No sibling files,
services or experiments were changed. Process checks and a local resource-use
note provided passive coordination; exclusive hardware use was not established.
D always preceded C, and server caching was not measured, so the timings are
operational totals, not evidence of a speed advantage.

Raw fixed C deployment on 18 fresh cases charges 6,759 prompt and 2,355 completion
tokens. The inherited category policy charges 6,981 and 2,887, plus acquisition
8,806 and 3,062. The old global policy also pays acquisition even though its use
matches C. The raw validator fallback charges 8,127 and 4,027 across 20 calls.
Actual counterfactual collection executed both remedies; the policy cost tables
charge only actions a deployed policy would request. Oracle token fields are
selected-output bookkeeping and omit unattainable free outcome knowledge.

Fresh source parsing and adaptation took approximately 0.00165 summed seconds
for 36 tasks on this run. Its code development, prior diagnosis, observation and
maintenance are not free. Per-component investigator labor and initial policy
update CPU time were not measured. Local electricity, hardware amortization and
monetary model costs are unknown. Investigator token telemetry is preserved as a
partial session snapshot in `evidence/provenance/investigator-usage.json`; it
includes repeated/cached contexts and is separate from participant costs. Final
session token totals after publication remain unknown. `evidence/costs.json`
keeps native units and limitations explicit.

The current session model/effort/provider were read from local session metadata:
gpt-6-astra, medium, OpenAI; session 01a0ebca-8395-75d0-a7a3-10439f6a4f8a. This is
harness-reported provenance, not an independently verified backend fingerprint.
Git's committer identity is the machine's preconfigured user, not evidence of
human authorship of this report.

## Methods context and limitations

[JSONSchemaBench v1](https://arxiv.org/html/2501.10868v1) separates coverage,
compliance and downstream quality. [LLMStructBench v1](https://arxiv.org/html/2602.14743v1)
uses synthetic structured-extraction scenarios with linguistic variation.
[Self-Refine's authors' description](https://selfrefine.info/) describes iterative
feedback and refinement. These are inspected methodological context, not local
replications. Our fixed fallback is not Self-Refine. See `sources/ledger.md` for
exact inspection scope, cached API metadata, versioned HTML and a noted browser
rate-coordination limitation. Starting RSI leads remain background; no upstream
code, benchmark cases or released labels were imported.

Important limitations: one quantized model; one direction of authored schema
change; only 12 acquisition and 18 fresh source cases; fixed narrow sentence forms;
handwritten features; deterministic tie behavior; correlated paired outcomes;
no stochastic repeats, production API execution, out-of-grammar validation,
receiver-model transfer, long-horizon obligations or unseen schema construction.
The follow-up cases are fresh values from the same grammar, not a new language
distribution. Cohort seeds were instantiated inside earlier structural unit tests;
those tests exposed only pass/fail checks, not source contents or model outcomes.
Freshness means no prior participant evaluation or outcome-guided changes on those
cases; it does not mean the generator had never instantiated their values. Public methods inspected during development cannot serve as untouched
confirmation. The source-only baseline was added after the first fresh results,
so only seed 440 is fresh confirmation of that follow-up claim.

## Reproduction and disposition

Starting repository revision: 3cabc29aa1b784ec8a9129c568224d90badb9cd6.
Protocol/harness freeze: e065235. Ordinary order-repair freeze: 723c13a.
Acquisition-policy freeze and fresh model run: f83506e.
Source-only follow-up freeze: 9eb5073. Full hashes and per-run manifests are saved.
The harness source SHA-256 is unchanged across all participant phases.

Offline verification:

```sh
uv sync --frozen
uv run python -m unittest discover -s tests -v
uv run python src/audit.py
```

To rerun model experiments, use new output directories; the runner refuses to
overwrite existing runs. Preserve the supplied policy when auditing the archived
confirmation. `acquire` writes the policy file, so reproduction of acquisition
should use a separate checkout. Example generation commands and file index are
in README.md. Model determinism across serving versions/hardware is not assumed.

Close this workload phase on explanatory progress: ordinary software fully solves
the supported source grammar, and the measured learned selector does not beat
ordinary reuse. This is a useful limitation, not a positive transfer claim awaiting
acceptance. Root may independently accept, revise or reject its interpretation.
The broader research question remains open. The next useful bounded phase would
first validate independently authored, linguistically varied source/label pairs
and test ordinary parsing, retrieval and repair before allocating intervention
history. A new protocol should require residual action complementarity after those
controls. More chooser training or template samples here would not resolve that
missing ecological variation; no further heavy job is justified on this workload.
