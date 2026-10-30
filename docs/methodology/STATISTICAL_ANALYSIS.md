# Statistical Analysis — Implementation Detail

**Governing principle:** every inferential procedure respects the clustered structure of the data (7 models × 180 items; observations sharing a question are not independent). All analysis randomness uses NumPy seed **20260622**; the analysis is deterministic given the released raw CSV.

## 1. Data and units

- **Unit of analysis (pair level):** 1,260 model-item pairs (180 items × 7 models), each with a greedy answer and a VCE call → 2,520 rows.
- **Clustering unit:** question ID (`qid`, 180 clusters of 7).
- **Regional contrast:** Africa-tagged (90 items → 630 pairs) vs Europe-tagged (90 items → 630 pairs).
- **H3 subsample:** wrong answers only — 170 (79 Africa + 91 Europe).

## 2. Tests and their roles

### 2.1 Pearson chi-squared (H1, conventional)
- 2×2 table: region × correct, pooled over models.
- **Verified:** χ² = 0.823 (df = 1), p = .364.
- Role: conventional pooled test. Row independence is violated (7 models per item), which is why it is not the primary evidence.

### 2.2 QID-level permutation test (H1 and H3, cluster-aware)
- **Implementation:** `scripts/robustness/permutation_audit.py`.
- Procedure: permute the region labels **at the question level** — the 90 Africa qids and 90 Europe qids are relabeled among themselves, keeping each item's seven model observations together. 10,000 permutations; seed 20260622; p = (#{perm ≥ obs} + 1)/(N + 1).
- Statistics permuted: χ² (accuracy) and Mann–Whitney U (wrong-answer VCE).
- **Verified:** H1 p_perm = .677; H3 p_perm = .726.
- Why not row-level: row-level permutation shreds the item clustering and produces anti-conservative p-values; the script also computes and reports the row-level variant as a documented negative control (archived in the evidence JSON).
- The superseded row-level implementation is archived in the upstream project, not deleted (provenance policy).

### 2.3 Mann–Whitney U + Holm correction (H3, conventional)
- Two-sided MWU on wrong-answer VCE, Africa vs Europe.
- Pooled: p = .234. Per model (n wrong = 7–29 per arm): smallest raw p = .251 (DeepSeek-V3.2); **no per-model p survives Holm correction across the 7 models**.
- Role: conventional rank test; per-model tests are explicitly labeled underpowered (16–29 wrong answers each).

### 2.4 Cohen's d with parametric CI (H3, descriptive)
- d = (mean_Af − mean_Eu)/SD_pooled = **−0.317**; 95% parametric CI [−0.621, −0.014].
- Role: descriptive effect size. The CI assumes independent observations — violated here — so it is **not** treated as formal inferential evidence; the permutation test carries the inferential weight.

### 2.5 Cluster-robust logistic regression (accuracy model)
- `correct ~ region + model`, binomial GLM, **SEs clustered by qid** (statsmodels `cov_type="cluster"`).
- **Verified:** β_Europe = −0.165 (z = −0.46, p = .646). Full coefficient table reproduced exactly (see `results/reports/` evidence CSVs and the verification script output).

### 2.6 Logit-normal linear mixed model (confidence model)
- `logit(C_VCE) ~ region + model + (1 | qid)`, C clipped to [0.001, 0.999], REML, optimizer `cg`, maxiter 5000.
- **Verified:** β_Europe = +0.152 (z = 0.81, p = .421); Gemma +4.049 (p<.001); Llama +2.728 (p<.001) vs Claude baseline; qid variance 1.297 (p<.001).
- Why logit-normal: VCE in (0,1) with clustering; a fully crossed 180-level logistic GLMM was unstable in statsmodels (gradient overflow/timeouts) — documented design trade-off in the manuscript.
- Diagnostics: ICC = 0.41; residuals non-normal (Shapiro–Wilk p<.001) — disclosed; logit transform mitigates.

### 2.7 Cluster bootstrap (calibration uncertainty)
- Pooled ECE 95% CI via **qid-level** cluster bootstrap: 2,000 resamples (paired-comparison CIs); 100 resamples for individual metric CIs.
- **Verified:** pooled ECE 0.048, CI [0.032, 0.083].

## 3. Power and minimum detectable effect

- Framework: two-sample standardized-mean difference on wrong-answer VCE.
- **MDE at 80% power: d ≈ 0.433** (raw-scale MDE 0.099 on the 0–1 VCE scale).
- Achieved power: d=0.30 → 0.492; d=0.50 → 0.899; d=1.00 → 1.000.
- Interpretation discipline: the study is sensitive to moderate and large effects; **smaller regional effects remain possible**; nulls are not equivalence claims (no TOST was run; underpowered for equivalence at d=0.30).

## 4. Sensitivity analyses (all reported, none removed conclusions)

| Check | Result |
|---|---|
| Leave-one-model-out (all 7 drops) | H1 all p>0.28; H3 all p>0.11; CHR ratio 0.733–0.801 — stable |
| Flagged-item exclusion (12 US-history mismatches) | Pooled accuracy 86.5%→85.8% (χ²=1.18, p=.277); H3 leave-out MWU p=.331 — conclusions unchanged |
| ECE binning (5/10 equal-width, 15 equal-mass) | 4.8%/4.8%/4.5%; ranking stable |
| Category sensitivity | `results/reports/category_sensitivity_final.csv` |
| Signal | All headline numbers from VCE; MSP/CoCoA present but not headline |

## 5. Where everything lives

| Artifact | Path |
|---|---|
| Verification script (recomputes Tables 2 & 4) | `scripts/verification/verify_v18_lmm_ece.py` |
| Table-4 verifier | `scripts/verification/verify_table4.py` |
| Consistency suite (71 checks) | `scripts/verification/verify_consistency.py` |
| Permutation audit | `scripts/robustness/permutation_audit.py` |
| Full validation pass (LOMO/power/diagnostics) | `scripts/robustness/final_validation_pass.py` |
| Evidence files (frozen outputs) | `results/reports/` |
| Run log (LMM/ECE verification) | `reproducibility/run_logs/afriknow-v18-lmm-ece-verification.log` |
