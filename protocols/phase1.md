# Phase 1: invoice extraction across an interface change

Written before any participant generations. Motivated, investigator-authored
workload; no public benchmark or imported task labels. This is a feasibility and
choice-headroom experiment, not a claim about autonomous general-purpose agents.

Fixed receiver: existing Docker Qwen3 8B Q4_K_M (reported mixed quantization).
Temperature 0, /no_think, 1000 max tokens, one request at a time. No weight update.
Source: two invoice records expressed in prose, including revisions, unknown
values, currencies with different decimal scales, and cancelled records. Keep
all records, exact identifiers/vendor/memo, correct minor units, final corrections,
null deadlines and order. Closed complete task is constructing the requested API
payload; no actual invoice/payment action occurs.

Actions: D = direct target-schema prompt; C = canonical decimal-string extraction
followed by an authored exact Decimal/date adapter. Both get complete source,
semantics and output contract. Both allow JSON code-fence/think-tag stripping.
Compiler and prompts are shared across all choosers. V1 is a flat row API; V2
is a nested keyed API with explicit order and decomposed date fields. This is an
interface transfer, not a receiver-model transfer. Compiler porting is authored
maintenance, not learned decision experience. Record its source hashes/cost.

Development: seed 110, 2 examples per group, both actions on both interfaces
(24 calls). Diagnose actual failures; maximum one bounded prompt/harness revision
plus 12 diagnostic calls before freezing. Preserve earlier outputs. No positive
transfer hypothesis will be fabricated if one action suffices.

Acquisition: seed 220, 4 examples per group, both actions on V1 (24 calls).
Retained object: a JSON table of mean complete-task success by visible source
category (plain/correction/precision), action and global action; choose highest
success, ties D. Labels are eligible feedback from earlier paid attempts.
These categories are authored inductive bias, not learned representation. The
actual update is filling the table from acquisition scores. No later gold labels
are available to a deployed chooser. Freeze before fresh evaluation.

Fresh confirmation: seed 330, 6 examples per group, both actions on V2 (36 calls).
Fresh = new generated records/values, same authored templates, not an independent
naturalistic workload. Do not change the policy after inspecting these outputs.
Use new seed 440 for a bounded follow-up if interpretation requires it.

Comparisons: fixed D, fixed C; unchanged acquired category policy; old global
best action; current-source diagnosis (C for explicit correction or non-2-digit
currency, otherwise D); schema-aware ordinary reuse (C whenever new target has
nesting, otherwise current-source rule). These ordinary rules are authored
before outcomes, not learned and not knowingly optimized to future outcomes.
Validator fallback D->C uses C only when D is structurally invalid; it cannot see
gold semantic success. All have access to source/contracts/adapter/cache. Paired
counterfactual outcomes are measured by executing both actions; only selected
outcomes and costs count toward each virtual deployment. Oracle max(D,C) is a
retrospective bound. This design evaluates deterministic table policies offline,
not live deliberative agents. A source-retrieval/repair baseline may be added in
follow-up, and any insufficiency of these ordinary controls limits interpretation.

Primary: exact full-payload success (including all still-valid fields). Report
structural validity separately and per-field failures, never as full success.
Measure headroom of oracle over best fixed, policy discordances, actual and
policy-selected requests/tokens, adapter CPU time, acquisition costs, file sizes,
unknown investigator costs. Latencies descriptive, no causal speed claim.
No significance claim from this small balanced constructed sample; report raw
counts and denominators. A useful negative result can close this phase if remedies
function and diagnosis explains why decision experience lacks measured value.

Cap 84 planned participant calls, plus up to 12 diagnosis calls, no automatic
unbounded retry. Timeout/error retained; abort phase on serving failures. No heavy
training. Mutable state here is a policy file, not model weights; serving does not
establish gradient access. Fresh confirmation runs only after implementation,
validators and policy persistence are checked.
