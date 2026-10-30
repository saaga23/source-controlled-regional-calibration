# Metric Definitions

Every metric used in this repository, with what it measures, how it is computed, how to read it, and how it can mislead. Implementations: `src/afriknow_calib/metrics.py` (tested) and `scripts/verification/verify_v18_lmm_ece.py` (paper reproduction).

---

## 1. Accuracy

**What it measures:** the share of greedy answers that are correct.

**Computation:** `mean(correct)` over rows with `purpose == "greedy"`, where `correct = 1` iff the predicted letter equals the gold letter.

**Reads:** higher is better. Pooled: Africa 87.5% (551/630), Europe 85.6% (539/630).

**Limitations:** accuracy on 180 medium-difficulty items near the ceiling (≈87%) is a coarse instrument; per-model cells rest on 180 observations; it says nothing about confidence.

---

## 2. Verbalized Confidence Estimate (VCE)

**What it measures:** the model's *stated* probability that its already-selected answer is correct.

**Computation:** the model is asked (verbatim prompt in `reproducibility/prompts/prompts.py`) to output an integer 0–100 for its chosen answer; `vce = integer / 100`. Collected in a separate call after the greedy answer, at temperature 0.

**Reads:** 0–1 probability. Used as the primary calibration signal.

**Limitations:** verbalized confidence is known to be overconfident in general (Xiong et al., ICLR 2024); it is a *stated* belief, not a sampling property; prompt phrasing can shift it (single fixed template used here — a documented limitation); it is elicited for an answer the model already committed to, so it measures confidence in that answer only.

---

## 3. Mean Self-Consistency (MSP)

**What it measures:** how strongly sampled behavior agrees with the greedy answer.

**Computation:** five samples at temperature 0.8; `sc_agree` = share of samples whose predicted letter equals the greedy answer. Supporting signal only.

**Reads:** higher = more self-consistent; used as an uncertainty proxy.

**Limitations:** agreement with the greedy answer is a consistency estimate, not a probability of correctness; 5 samples is a small estimate; at temperature 0.8 sampling diversity varies by model.

---

## 4. CoCoA composites (present in data; not primary)

**Definition:** `CoCoA_α = α·VCE + (1−α)·MSP` for α ∈ {0.25, 0.5, 0.75}; the α=0.5 version is `cocoa_fixed` in the raw CSV.

**Status:** fixed linear composites registered at run time. They are **not** validated calibration methods in this project; no headline claim rests on them. They are shipped in the data for completeness and future signal-comparison work.

---

## 5. Calibration Hit Rate — CHR(τ)

**What it measures:** the operational risk of confident errors — among predictions the model is at least τ-confident in, how many are wrong.

**Computation:** over `vce`-purpose rows, `CHR(τ) = P(correct = 0 | vce ≥ τ)`. Primary threshold τ = 0.70. The paper reports the Africa/Europe **ratio**; ratio < 1 means fewer confident errors on Africa.

**Verified values:** pooled CHR 0.105 (Africa, 601 high-conf predictions) vs 0.136 (Europe, 609), ratio 0.769.

**Reads:** a *conditional* error rate — deliberately answers "when this model is confident and deployed, how often is it wrong?"

**Limitations:** threshold-dependent (the threshold sweep `chr_by_tau_v18.png` shows the full curve); tail-sensitive (depends only on the ≥τ subset); reported descriptively — **no inferential test was performed for CHR**, and none should be implied; smaller denominators per model make per-model CHR noisy.

---

## 6. Wrong-answer confidence (H3)

**What it measures:** mean confidence among incorrect predictions — "how confident is the model when it is wrong?"

**Computation:** mean `vce` over `vce`-purpose rows with `correct = 0`. Compared Africa vs. Europe with (a) two-sided Mann–Whitney U (Holm-corrected per model), (b) qid-level permutation test, (c) Cohen's d as a descriptive effect size with a parametric 95% CI.

**Verified values:** Africa 0.761 (n=79 wrong) vs Europe 0.832 (n=91), d = −0.317, MWU p = .234, permutation p = .726.

**Reads:** if Africa > Europe, models are *more* confident when wrong about Africa — the hypothesized (pre-specified, one-sided) Africa-overconfidence signature.

**Limitations:** n = 170 wrong answers total; the parametric CI assumes independent observations (not true under item clustering) and is labeled descriptive; the pre-specified one-sided hypothesis is reported as two-sided because data preceded final analysis-plan freeze (documented in `EXPERIMENT_PROTOCOL.md`).

---

## 7. Expected Calibration Error — ECE

**What it measures:** the average absolute gap between stated confidence and observed accuracy, weighted by bin mass.

**Computation:**

$$\mathrm{ECE} = \sum_{b=1}^{B} \frac{n_b}{N}\,\big|\,\mathrm{acc}(b) - \mathrm{conf}(b)\,\big|$$

with B = 10 equal-width bins over [0,1] (Guo et al., 2017). Per model, per region, and pooled.

**Verified values:** pooled 0.048 (cluster-bootstrap 95% CI [0.032, 0.083], 2,000 resamples); per-model 0.053 (DeepSeek) to 0.136 (Gemma).

**Reads:** lower is better; 0.048 means the average gap between stated and realized accuracy is under 5 points.

**Limitations (all three matter here):**
1. **Binning sensitivity** — checked: 4.8% (5-bin), 4.8% (10-bin), 4.5% (15-bin equal-mass); ranking stable.
2. **Gameability** — flat confidence at the base rate can achieve low ECE without any per-item discrimination (Si et al., 2022). Hence Brier and AUROC are always reported alongside.
3. **Aggregation artifact** — the average of per-model ECEs (0.081) exceeds pooled ECE (0.048) because thin per-model bins inflate bin-level error; this is why pooled and per-model views are both reported.

---

## 8. Brier score

**What it measures:** mean squared error of the confidence as a probability forecast of correctness.

**Computation:** `mean((vce − correct)²)`. Strictly proper — minimized by true probabilities.

**Verified values:** pooled 0.114; per model 0.065 (Claude) to 0.173 (GPT-4.1-Nano).

**Reads:** lower is better; decomposes (for the confidence forecast) into discrimination and calibration components.

**Limitations:** dominated by the accuracy level when accuracy is very high (most terms are (vce−1)² for correct answers); not region-decomposed in the headline table (per-model values are reported).

---

## 9. AUROC

**What it measures:** the probability that a randomly chosen correct answer receives higher confidence than a randomly chosen wrong answer — pure discrimination, ignoring calibration.

**Computation:** ROC AUC of `vce` against `correct` (sklearn `roc_auc_score`).

**Verified values:** pooled 0.679; per model 0.594 (Gemma) to 0.841 (Claude).

**Reads:** 0.5 = no discrimination; 0.679 = moderate separation. Verbalized confidence ranks better than chance but far from cleanly.

**Limitations:** insensitive to calibration (a perfectly discriminating but badly scaled signal still scores 1.0); class imbalance (≈87% correct) makes AUROC optimistic relative to precision-recall (AUPRC was not computed — a documented limitation).

---

## 10. Reliability diagrams

**What they measure:** observed accuracy as a function of stated confidence (deciles), per model; the diagonal is perfect calibration (`reliability_curves_v18.png`).

**Reads:** points below the diagonal = overconfidence.

**Limitations:** bin counts per model are small (180 per model, ~18 per bin); interpret shapes qualitatively, not as precise curves.
