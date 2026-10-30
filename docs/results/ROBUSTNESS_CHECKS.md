# Robustness Checks

All checks were run against the frozen raw CSV (`data/raw/03_openrouter_outputs_v18_correct.csv`). Frozen evidence: `results/reports/`. Reruns on 2026-10-30 reproduce all values.

## 1. Leave-one-model-out (LOMO)

Drop each model in turn; recompute every headline statistic.

| Dropped model | H1 (accuracy) p | H3 (wrong-VCE) p | CHR ratio |
|---|---|---|---|
| (none — full panel) | — (χ² p=.364; perm .677) | .234 (perm .726) | 0.769 |
| each of the 7 drops | all p > 0.28 | all p > 0.11 | 0.733–0.801 |

**Conclusion:** no single model drives the null results; the CHR direction is stable across all drops. Evidence: `results/reports/leave_one_model_out_final.csv`, `LEAVE_ONE_MODEL_OUT_FINAL.md` (upstream report set).

## 2. Flagged-item exclusion (12 content-label mismatches)

Exclude the 12 US-history items tagged Africa (6) / Europe (6):

| Statistic | Full sample | Leave-out | Test |
|---|---|---|---|
| Pooled accuracy | 86.5% | 85.8% | χ² = 1.18, p = .277 |
| H3 (wrong-answer confidence) | MWU p = .234 | MWU p = .331 | two-sided |
| CHR ratio | 0.77 | unchanged in direction | descriptive |

**Conclusion:** the known label noise does not create or mask the regional findings.

## 3. ECE binning sensitivity

| Binning | Pooled ECE |
|---|---|
| 5 equal-width bins | 0.048 |
| 10 equal-width bins (primary) | 0.048 |
| 15 equal-mass bins | 0.045 |

Model ranking stable across binning choices. (Guards against ECE's binning dependence — Guo et al. 2017; Si et al. 2022.)

## 4. Cluster-bootstrap uncertainty

Pooled ECE 95% CI [0.032, 0.083] — 2,000 qid-level bootstrap resamples (100 for individual metrics), NumPy seed 20260622. The CI does not include 0 — pooled miscalibration of ~5% is real, while the *regional* contrasts are null.

## 5. Permutation-test validity (negative control included)

`scripts/robustness/permutation_audit.py` computes both the correct qid-level permutation and the invalid row-level permutation. Row-level tests are anti-conservative (they shred item clusters); the invalid implementation is retained in the output as a documented negative control, and the superseded code is archived (not deleted) in the upstream project. Seed 20260622; 10,000 permutations.

## 6. Mixed-model specification search

Two specification-search scripts (`find_lmm_spec.py`, `find_lmm_spec2.py`) document the exploration from raw confidence to the reported logit-normal LMM. The reported specification reproduces the published coefficients to 3 decimals (`verify_v18_lmm_ece.py`, rerun 2026-10-30). Diagnostics (ICC 0.41, qid variance 1.30, residual non-normality disclosed) are in `results/reports/model_diagnostics_final.json`.

## 7. VCE prompt sensitivity

A dedicated sensitivity report (upstream `VCE_PROMPT_SENSITIVITY_FINAL.md`) examined the stability of VCE under prompt variation during instrument development; the final audit uses a single fixed template (documented limitation rather than uncontrolled variation). Confidence-signal conclusions on VCE hold across the robustness suite.

## 8. Source-control sensitivity (between-design)

The archived mixed-source experiment (180 items, 5 models, $0.072; upstream `archive/experiments/mixed_source_2026-07-18/`) shows the same directional null. Between-study consistency supports (does not prove) the source-confounding interpretation — see `RESULT_INTERPRETATION.md` for why this is not a causal test.

## 9. Category sensitivity

Per-category regional checks are in `results/reports/category_sensitivity_final.csv`; the history-heavy composition means fine-grained category claims are underpowered (see `KNOWN_LIMITATIONS.md`).
