# Decision Rationale

Methodological and engineering decisions with alternatives considered, trade-offs, and verification paths. Chronological where relevant; the same discipline as the upstream project's decision log, extended for this repository.

## D1 — Source-controlled design (both arms from Global-MMLU)
- **Decision:** use Global-MMLU only, for both regional arms.
- **Why:** prior Africa-vs-Europe comparisons used AfriMMLU (Africa) vs Global-MMLU/Wikidata (Europe), entangling region with source-specific difficulty, translation, and distractor design. Design-time control beats post-hoc adjustment.
- **Alternatives:** (a) statistical adjustment for source in mixed-source data — rejected: source and region are collinear by design; (b) matched-pair item translation across regions — infeasible at this scale without a new annotation effort; (c) build a new benchmark — out of scope for an audit.
- **Trade-off:** the Africa-tagged Global-MMLU pool caps the sample at 90 items (180 total) and the content is history-heavy (~71%).
- **Evidence/verification:** dataset construction verified item-by-item (`docs/dataset/`); composition in `DATA_QUALITY_REPORT.md`.

## D2 — VCE as primary confidence signal
- **Why:** black-box accessible, directly interpretable probability scale, lowest ECE among available signals in this run.
- **Alternatives:** MSP (consistency) — reported but not primary (consistency ≠ probability of correctness); logprobs — unavailable through the API routes used; CoCoA composites — present in data but not validated as calibration methods, so not used for headline claims.
- **Trade-off:** verbalized confidence is a stated belief, sensitive to prompt phrasing (single fixed template — documented limitation).

## D3 — QID-level permutation (not row-level)
- **Why:** 7 observations per question are correlated through item difficulty/content; row-level permutation is anti-conservative. Region is a property of the *item*, so the exchangeable unit is the item.
- **Alternatives:** row-level permutation (invalid — computed and reported as a negative control); sign-flipping within item pairs — not applicable (unpaired regions).
- **Trade-off:** cluster-level permutation has fewer exchangeable units (180) — granularity of the permutation distribution is coarser.
- **Verification:** `scripts/robustness/permutation_audit.py`, seed 20260622, 10,000 permutations; the superseded row-level code is archived upstream, not deleted.

## D4 — Two-sided reporting of a one-sided pre-specified hypothesis
- **Why:** the directional H3 was specified before the GM-only run, but data were collected before the analysis plan was final. Reporting two-sided with Holm correction is the conservative choice and is disclosed in the manuscript and protocol.
- **Trade-off:** sacrifices power for the directional claim; protects against directional bias.

## D5 — Keep the 12 flagged content-label mismatches in the primary analysis
- **Why:** the sample is ceiling-limited; removing 6.7% of items reduces power further; the mismatches are split 6/6 so the regional contrast is not asymmetrically biased.
- **Alternatives:** exclude them — reported as a robustness check instead (all conclusions unchanged: pooled accuracy 86.5%→85.8%, p=.277; H3 leave-out p=.331).
- **Trade-off:** primary estimates include known label noise; the leave-out check bounds its influence.

## D6 — No equivalence claim
- **Why:** MDE ≈ d 0.433 at 80% power; the observed CI includes practically large effects; failing to reject ≠ equivalence.
- **Alternatives:** TOST — underpowered at this sample size (achieved power ~49% at d=0.30); reporting "no difference" — rejected as misleading.
- **Verification:** `results/reports/null_equivalence_final.json`, `power_mde_final.json`.

## D7 — Mixed-effects specification: logit-normal LMM + cluster-robust GLM instead of fully crossed GLMM
- **Why:** a fully crossed logistic GLMM (180 item random effects) was unstable in statsmodels (gradient overflow/timeouts). The two-model approach (cluster-robust marginal logistic for accuracy; logit-normal LMM with qid random intercept for confidence) is stable, reproducible, and adequate for the regional question.
- **Alternatives:** Bayesian hierarchical model — out of scope (compute/complexity); bootstrapped GLMM — same instability.
- **Trade-off:** the accuracy model is marginal (not conditionally specified); residuals of the confidence LMM are non-normal (disclosed; logit transform mitigates).
- **Verification:** exact reproduction to 3 decimals in `verify_v18_lmm_ece.py` (log excerpt in `reproducibility/run_logs/`).

## D8 — Report CHR descriptively only
- **Why:** CHR is a tail-conditional ratio with small denominators (per model 79–90 high-confidence predictions; per region 601/609); an inferential test would be noisy and easily misread. The threshold sweep figure shows the full curve.
- **Trade-off:** no p-value for H2 — stated explicitly wherever CHR is discussed.

## D9 — This repository publishes the full 180-item subset
- **Why:** Global-MMLU is Apache-2.0 (verified on the official dataset card, accessed 2026-10-30); redistribution with attribution is permitted. Publishing the subset removes the largest barrier to reproduction.
- **Alternatives:** publish only IDs + reconstruction script — kept as a fallback plan in `docs/dataset/DATA_PROVENANCE.md` in case upstream terms change.
- **Trade-off:** the frozen subset pins the upstream version; re-derivation instructions guard against upstream drift.

## D10 — Refactors applied for this public repository (all minimal, documented)
1. `permutation_audit.py`: hardcoded machine path → `Path(__file__)` root resolution (portability only; logic and seeds unchanged; rerun reproduces the published p-values).
2. `verify_v18_lmm_ece.py`: evidence output directory redirected to `results/reports/` (layout only).
3. Kaggle account-specific upload utilities excluded from the public repo (not needed for reproduction; public Kaggle links documented instead).
- **Verification:** both refactored scripts were re-run in this repository and reproduce the published numbers exactly (see `docs/results/RESULTS.md`).
