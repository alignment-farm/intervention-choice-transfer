# Source ledger, 29 September 2026

Background sources in BACKGROUND.md remain root-reported readings, not reproduced
results. No upstream implementation or evaluation cases are used in this workload.
The investigator authored the complete source generator, gold state, interventions,
feature categories and comparator rules. Model pretraining provenance is unknown.

Metadata discovery uses the arXiv API, cached as arxiv-query.xml with response
headers/hash. A single request queried three IDs; no concurrent query-API client
was launched by this study. Exact-version method HTML is cached separately with a
serial three-second spacing script. Initial web-search/HTML inspection also used
the browser service; those service fetches were not coordinated by the local rate
limiter (a procedural limitation). Future arXiv acquisition should use only the
serial scripts.

- [JSONSchemaBench, 2501.10868v1](https://arxiv.org/html/2501.10868v1),
  inspected abstract and §§2–5: separates constraint coverage, compliance and
  downstream quality. Relevant to our distinction between structural validity and
  complete semantic correctness. Its constrained-decoding engines are a distinct
  remedy family we have not reproduced. API metadata reports v3 as latest; our
  method statements concern the explicitly inspected v1, not v3 results.
- [LLMStructBench, 2602.14743v1](https://arxiv.org/html/2602.14743v1),
  inspected §III-A and scenario table: constructs structured ground truth then
  synthetic natural-language inputs, and studies extraction under different
  prompting conditions. Our fixed prose templates provide less linguistic variety.
  No benchmark examples, result labels or source implementation are imported.
- [Self-Refine](https://selfrefine.info/), inspected authors' framework description:
  alternates feedback and refinement and retains earlier outputs in context. Our
  validator-triggered fixed fallback is not a reproduction of learned feedback or
  Self-Refine. API metadata pins the associated paper to 2303.17651v2; that paper's
  full text was not inspected in this phase. Site is unversioned.

No novelty claim or replication claim. These are inspected method descriptions;
author-reported results have not been independently checked. Our inference is
that interface compliance should be separated from source-fidelity obligations,
and ordinary validation/repair is a necessary control here.
