# Methodology

**Study:** Source-controlled audit of seven LLMs on 180 Global-MMLU items (90 Africa-tagged / 90 Europe-tagged), measuring accuracy and confidence calibration per region.

This document explains the methodology as a connected argument. Metric equations and limitations are in `METRIC_DEFINITIONS.md`; the statistical machinery is detailed in `STATISTICAL_ANALYSIS.md`; the run-level protocol is in `EXPERIMENT_PROTOCOL.md`.

## 1. Why this design

Regional evaluation usually compares model behavior on **different benchmarks per region** (e.g., AfriMMLU for Africa, Global-MMLU or Wikidata for Europe). Any measured gap then mixes together: regional differences in model behavior, source-specific difficulty, translation quality, distractor design, and content selection. Because these co-occur, a post-hoc statistical fix cannot fully unmix them.

The design fix is to **hold the benchmark source constant**: take both regional arms from Global-MMLU, which tags each item with a cultural region. On this slice, the two arms share the identical benchmark, language (English), answer format, and difficulty band; the subject-category and cultural-sensitivity composition are matched by construction. The remaining difference between arms is the region tag (and sampling noise within matched categories).

**The price of this control** is a hard ceiling: the Africa-tagged Global-MMLU pool that survives filtering exhausts at 90 items, so the whole sample is capped at 180. Everything downstream (power, MDE) is shaped by this ceiling.

## 2. Models

Seven models spanning proprietary and open-weight families, released 2024–2026, all evaluated through OpenRouter with their stable English routes at run time:

| Model | Class | Calls | Tokens | Cost (USD) |
|---|---|---|---|---|
| Claude-Sonnet-4.6 | closed | 360 | 681,868 | 0.1700 |
| DeepSeek-V3.2 | — | 360 | 617,656 | 0.1409 |
| Gemini-2.5-Flash-Lite | closed | 360 | 617,680 | 0.0616 |
| Gemma-4-31B | open | 360 | 653,258 | 0.0651 |
| GPT-4o-mini | closed | 360 | 616,902 | 0.0923 |
| GPT-4.1-Nano | closed | 360 | 618,018 | 0.0616 |
| Llama-3.3-70B | open | 360 | 642,634 | 0.0641 |
| **Total** | | **2,520** | **4,448,016** | **0.6556** |

The full panel is reported without selection; the panel is small and English-centric (a limitation, not a representativeness claim). Exact OpenRouter identifiers and the run manifest: `data/metadata/03_openrouter_manifest_v18.json`, `data/manifests/AFRIKNOW_V18_MANIFEST.yaml`.

## 3. Confidence signals

Two black-box signals (no logit access required), both emitted per item:

1. **Verbalized Confidence Estimate (VCE)** — the model states an integer 0–100 for its already-selected answer; ÷100 gives a probability. **Primary signal.** Chosen because it is directly interpretable on the probability scale, works for any API-accessible model, and posted the lowest ECE of the available signals in this run.
2. **Mean Self-Consistency (MSP)** — five samples at temperature 0.8; the share agreeing with the greedy answer. **Supporting analysis only.** Semantic self-consistency, in the sense of Kuhn et al. (2023) and Wang et al. (2023), implemented as greedy-answer agreement.

Fixed composites **CoCoA_α = α·VCE + (1−α)·MSP** (α ∈ {0.25, 0.5, 0.75}) are present in the data as pre-declared composites. They are **not** treated as validated calibration methods here; all reported numbers come from VCE.

## 4. Metrics

| Metric | What it measures | View |
|---|---|---|
| Accuracy | Share of correct greedy answers | Correctness |
| CHR(τ=0.70) | Fraction of wrong answers among predictions with confidence ≥ 0.70 | Operational risk of confident errors |
| Wrong-answer VCE (H3) | Mean confidence on incorrect predictions | Confidence behavior after errors |
| ECE (10 equal-width bins) | Gap between confidence and accuracy, weighted by bin mass | Overall calibration |
| Brier | Mean squared error of confidence vs. correctness | Strictly proper score |
| AUROC | Confidence as a correctness discriminator | Ranking/discrimination |

Every metric is reported per model and region; ECE is additionally checked under 5/10-bin equal-width and 15-bin equal-mass binning (stable: 4.8% → 4.8% → 4.5%). Equations and failure modes: `METRIC_DEFINITIONS.md`.

## 5. Statistical strategy (the connected logic)

**The dependence problem.** Seven models answer the *same* 180 questions. Observations sharing a question are correlated through question difficulty and content — treating all 1,260 rows as independent would produce anti-conservative tests. Every inferential step therefore respects item clustering:

- **H1 (accuracy):** Pearson χ² on the pooled 2×2 table is reported as the conventional test, plus a **qid-level permutation test** (10,000 permutations, seed 20260622) and a **cluster-robust logistic regression** (`correct ~ region + model`, SEs clustered by qid). All three agree (p = .364 / .677 / .646).
- **H3 (wrong-answer confidence):** two-sided Mann–Whitney U with Holm correction across the seven models (conventional), plus the **qid-level permutation test** that keeps each item's seven observations together (p = .726). The per-model tests rest on 7–17 wrong answers per arm — non-significance there reflects sample size, and is labeled as such.
- **H2 (CHR):** reported descriptively with per-model values and a threshold sweep; **no inferential test was performed** and none is claimed.
- **Calibration:** pooled ECE with cluster-bootstrap 95% CI (2,000 resamples for paired comparisons; 100 for individual metrics; NumPy seed 20260622).

**Significance vs. equivalence.** A non-significant result is a failure to detect, not evidence of no effect. The design's minimum detectable effect is **Cohen's d ≈ 0.433 at 80% power** (raw-scale MDE 0.099 on VCE); power is ~49% at d = 0.30 and ~90% at d = 0.50. The paper therefore claims sensitivity to moderate/large effects and explicitly declines an equivalence claim.

## 6. Robustness checks

1. **Leave-one-model-out (LOMO)** — all seven drops leave every conclusion stable (H1 p > 0.28; H3 p > 0.11; CHR ratio 0.733–0.801).
2. **Flagged-item exclusion** — dropping the 12 content-label mismatches moves pooled accuracy 86.5%→85.8% (p=.277); H3 leave-out MWU p = .331; conclusions unchanged.
3. **Binning sensitivity** — ECE stable under equal-width/equal-mass binning.
4. **Signal check** — conclusions reported on VCE; MSP and CoCoA present in data but not the basis of any headline claim.
5. **Model specification search** — LMM specification exploration archived (`scripts/robustness/find_lmm_spec*.py`); the reported LMM uses logit-transformed VCE (clip 0.001), qid random intercept, REML.

## 7. What the design cannot do

- **No causal attribution.** The disappearance of the previously reported Africa-overconfidence effect under source control is *consistent with* source confounding, but item-selection and model-panel differences between studies preclude a definitive causal claim.
- **No equivalence claim.** MDE d≈0.43; smaller regional effects remain possible.
- **No fine-grained regional claims.** "Africa"/"Europe" are Global-MMLU aggregate tags; no country-level analysis is powered.
- **No beyond-medium-difficulty or beyond-English generalization.**
