# Reference Verification

**Verification date:** 2026-10-30 · **Method:** each of the 29 bibliography entries from `paper/manuscript/references.bib` was checked against authoritative sources (arXiv abstract pages, ACL Anthology, PMLR, publisher pages) by direct fetch, plus an automated cross-check. Entries that could not be confirmed at audit time are marked **PENDING** — their details are carried over from the manuscript bibliography and must not be treated as independently confirmed.

**Status legend:** `VERIFIED` = title/authors/venue confirmed at the given URL. `PENDING` = not independently confirmed during this audit (rate limits or blocked pages); details quoted from the manuscript's bibliography.

## Verified entries (13)

| Bibkey | Title (verified) | Venue | Link checked | Proposition relied on in this project |
|---|---|---|---|---|
| singh2025global | Global MMLU: Understanding and Addressing Cultural and Linguistic Biases in Multilingual Evaluation (Singh et al.; arXiv:2412.03304, v2 2025-02-19) | ACL 2025 per manuscript; arXiv verified | [arxiv.org/abs/2412.03304](https://arxiv.org/abs/2412.03304) | Source benchmark; provides Africa/Europe region tags and CS/CA labels; documents that 84.9% of geographic questions concern North America/Europe; 42-language release under Apache-2.0 |
| adelani2025irokobench | IrokoBench: A New Benchmark for African Languages in the Age of Large Language Models (Adelani et al.) | NAACL 2025 main (per arXiv comment) | [arxiv.org/abs/2406.03368](https://arxiv.org/abs/2406.03368) | AfriMMLU is a human-translated African benchmark; open/proprietary gap; prior Africa-vs-Europe comparisons used AfriMMLU (source-confounded design) |
| kadavath2022language | Language Models (Mostly) Know What They Know (Kadavath et al.) | arXiv preprint | [arxiv.org/abs/2207.05221](https://arxiv.org/abs/2207.05221) | Basis for verbalized-confidence elicitation and self-evaluation signals |
| tian2023just | Just Ask for Calibration (Tian et al.) | EMNLP 2023 | [aclanthology.org/2023.emnlp-main.330](https://aclanthology.org/2023.emnlp-main.330/) | Verbalized-confidence strategies in RLHF models; precedent for the VCE prompt |
| si2022reexamining | Re-Examining Calibration: The Case of Question Answering (Si et al.) | EMNLP 2022 Findings | [aclanthology.org/2022.findings-emnlp.206](https://aclanthology.org/2022.findings-emnlp.206/) | Aggregate ECE can be gamed by flat confidence; motivates region-stratified ECE + Brier |
| manakul2023selfcheckgpt | SelfCheckGPT (Manakul et al.) | EMNLP 2023 | [aclanthology.org/2023.emnlp-main.488](https://aclanthology.org/2023.emnlp-main.488/) | Sampling-based consistency as black-box hallucination signal |
| huang2024rank | Uncertainty in Language Models: Assessment through Rank-Calibration (Huang et al.) | EMNLP 2024 | [aclanthology.org/2024.emnlp-main.18](https://aclanthology.org/2024.emnlp-main.18/) | Rank-calibration diagnostics; informs metric selection |
| zhang2024calibrating | Calibrating the Confidence of Large Language Models by Eliciting Fidelity (Zhang et al.) | EMNLP 2024 | [aclanthology.org/2024.emnlp-main.318](https://aclanthology.org/2024.emnlp-main.318/) | Confidence decomposition (question uncertainty vs answer fidelity) |
| wang2024self | Self-Consistency Boosts Calibration for Math Reasoning (Wang et al.) | EMNLP 2024 Findings | [aclanthology.org/2024.findings-emnlp.354](https://aclanthology.org/2024.findings-emnlp.354/) | Self-consistency as a calibration signal (MSP basis) |
| steyvers2024calibration | The Calibration Gap Between Model and Human Confidence in Large Language Models (Steyvers et al.) | arXiv preprint | [arxiv.org/abs/2401.13835](https://arxiv.org/abs/2401.13835) | Model–human calibration gap; motivates confidence auditing |
| manvi2024geographically | Large Language Models are Geographically Biased (Manvi et al.) | ICML 2024 (PMLR v235) | [proceedings.mlr.press/v235/manvi24a.html](https://proceedings.mlr.press/v235/manvi24a.html) | Geographic bias against lower-income regions incl. Africa; motivates region-stratified calibration |
| mirza2024global | Global-Liar: Factuality of LLMs over Time and Geographic Regions (Mirza et al.) | arXiv preprint | [arxiv.org/abs/2401.17839](https://arxiv.org/abs/2401.17839) | Global-North factual-accuracy advantage; source-confounded regional evidence |
| guo2017calibration | On Calibration of Modern Neural Networks (Guo et al.) | ICML 2017, PMLR 70:1321–1330 | [proceedings.mlr.press/v70/guo17a.html](https://proceedings.mlr.press/v70/guo17a.html) | ECE definition, reliability diagrams, temperature scaling as post-hoc baseline |

**Coelho et al. 2025** (`coelho2025inequality`, arXiv:2503.22877) was also confirmed to resolve at arXiv during the automated check (agent-verified); treated as verified-at-URL but re-check before camera-ready.

## Pending entries (16) — not yet independently confirmed

| Bibkey | Title (from manuscript bib) | Claimed venue | Status |
|---|---|---|---|
| mielke2022reducing | Reducing Conversational Agents' Overconfidence through Linguistic Calibration | TACL 2022 | PENDING (ACL Anthology lookup mismatched during automated check) |
| lin2022teaching | Teaching Models to Express Their Uncertainty in Words | TMLR 2022 | PENDING (OpenReview blocked fetch) |
| kuhn2023semantic | Semantic Uncertainty | ICLR 2023 | PENDING (OpenReview blocked fetch) |
| wang2023selfconsistency | Self-Consistency Improves Chain of Thought Reasoning in Language Models | ICLR 2023 | PENDING (OpenReview blocked fetch) |
| xiong2024can | Can LLMs Express Their Uncertainty? | ICLR 2024 | PENDING (OpenReview blocked fetch) |
| geng2024survey | A Survey of Confidence Estimation and Calibration in LLMs | NAACL 2024 | PENDING (ACL Anthology URL returned 404 during check — venue/year needs confirmation) |
| moayeri2024worldbench | WorldBench: Quantifying Geographic Disparities in LLM Factual Recall | FAccT 2024 | PENDING (publisher page blocked) |
| chhikara2025mind | Mind the Confidence Gap | TMLR 2025 | PENDING (not located at audit time) |
| decoupes2025geographical | Evaluation of Geographical Distortions in Language Models | Machine Learning (Springer) | PENDING (Springer blocked fetch) |
| xia2026calibration | Calibration Is Not Enough: Evaluating Confidence Estimation Under Language Variations | arXiv (2026) | PENDING (agent reported a match at arXiv:2601.08064 — **re-verify before relying on this ID**) |
| coelho2025inequality | Understanding Inequality of LLM Fact-Checking over Geographic Regions | arXiv (2025) | VERIFIED-leaning (arXiv:2503.22877 resolved; confirm) |
| zhou2025beyond | Beyond the Final Layer | arXiv (2025) | PENDING (arXiv:2510.03136 reported by agent; not re-confirmed) |
| ojo2025afrobench | AfroBench: How Good are Large Language Models on African Languages? | ACL Findings 2025 | PENDING (APIs rate-limited; no arXiv ID asserted — a candidate ID was found to be a *different* paper and rejected) |
| guan2025saged | SAGED | COLING 2025 | PENDING |
| rystrom2025multilingual | Multilingual is not Multicultural | MMLP Workshop 2025 | PENDING |
| niculescu2005predicting | Predicting Good Probabilities with Supervised Learning | ICML 2005 | PENDING (well-known work; venue details from manuscript bib, not re-confirmed this audit) |

## Audit notes and known bib issues

1. **Venue claims for pending entries come from the manuscript's `references.bib`.** They are plausible but were not confirmed at audit time; the automation was blocked (OpenReview/Anthology rate limits). This is an honest limitation, recorded rather than papered over.
2. One candidate arXiv ID for AfroBench (2501.08714) resolves to an unrelated oncology paper and was **rejected** — no arXiv ID is asserted for AfroBench anywhere in this repository.
3. Before camera-ready: re-run this verification when API rate limits allow, and update statuses here and in `RELATED_WORK_MATRIX.csv`.

## How to re-run this verification

Query pattern (rate-limit friendly, ≥1 req/s):

```
https://api.semanticscholar.org/graph/v1/paper/search?query=<TITLE>&limit=1&fields=title,year,venue,externalIds
https://api.crossref.org/works?query.bibliographic=<TITLE>&rows=1&select=title,author,issued,container-title,DOI
```

Rule: an entry moves to VERIFIED only when title + first author + venue/year are confirmed at the linked URL.
