# Project Inventory

**Repository:** `source-controlled-regional-calibration`
**Inventory date:** 2026-10-30
**Upstream project:** AfriKnow (internal repository `afriknow-repo`, preserved separately with full Git history)

This inventory maps every important artifact in this repository to its origin, purpose, and verification status. Status classes:

1. **Verified original** — artifact exists in the upstream project, its hash matches the recorded canonical hash, and its content has been checked against the manuscript.
2. **Derived research artifact** — generated from verified originals by scripts in this repository.
3. **Reconstructed artifact** — rebuilt for this repository because the original was in a private/internal location; the derivation is documented.
4. **Missing artifact** — referenced but not available; never silently replaced.
5. **Requires further verification** — present but not yet fully cross-checked.

## Core data

| Artifact | Path | Status | Notes |
|---|---|---|---|
| Raw model outputs | `data/raw/03_openrouter_outputs_v18_correct.csv` | **Verified original** | 2,520 rows (180 items × 7 models × 2 purposes), 23 columns. SHA-256 `1915a77c02ff1f08a87f8b2950f2e2c5e3041a353f7e26f456dd700543a6807d` — matches the canonical hash recorded in the upstream project status file. Headline numbers re-derived independently (accuracy 551/630=87.5% Africa, 539/630=85.6% Europe; χ²=0.823, p=.364; wrong-answer VCE 0.761/0.832; MWU p=.234; CHR₀.₇₀ 0.105/0.136; pooled ECE 0.048; Brier 0.114; AUROC 0.679; cost \$0.6556; 4,448,016 tokens). |
| Curated 180 items | `data/curated/02_gm_only_180_items.json` | **Verified original** | 180 items (90 Africa-tagged, 90 Europe-tagged), 4-option MCQ with question text, choices, gold answer, category, difficulty, cultural-sensitivity tag. SHA-256 `fc07491b188ca2017b15ef93b6c1a9fd5066007362ea5c4e944f60443a52ef52`. Content derived from Global-MMLU (Apache-2.0); redistribution permitted with attribution (see `docs/dataset/DATASET_CARD.md`). |
| Sample design manifest | `data/metadata/02_sample_design_manifest.json` | **Verified original** | Documents matching keys (category+difficulty+cultural sensitivity) used for regional stratification. |
| OpenRouter run manifest | `data/metadata/03_openrouter_manifest_v18.json` | **Verified original** | Model identifiers, routes, pricing, timestamps for the v18 run. |
| Experiment manifest | `data/manifests/AFRIKNOW_V18_MANIFEST.yaml` | **Verified original** | Experiment ID AFRIKNOW_V18; master manifest for the run. |

## Scripts (preserved originals; refactored only where documented)

| Artifact | Path | Status | Notes |
|---|---|---|---|
| OpenRouter runner | `scripts/primary/03_openrouter_runner.py` | **Verified original** | Reads `OPENROUTER_API_KEY` from environment only; no secrets embedded. |
| Audit trail logger | `scripts/primary/05_audit_trail.py` | **Verified original** | Tamper-evident JSONL event log with SHA-256 input/output hashes. |
| Pipeline orchestrator | `scripts/primary/run_pipeline.py` | **Verified original** | References two phase scripts (`01_power_analysis.py`, `02_sample_design.py`) that are **not included** in this public repository (missing artifacts, see below). |
| Consistency verifier | `scripts/verification/verify_consistency.py` | **Verified original** | 71/71 consistency checks against raw CSV. |
| Table 4 verifier | `scripts/verification/verify_table4.py` | **Verified original** | Mixed-effects coefficient verification. |
| LMM/ECE verifier | `scripts/verification/verify_v18_lmm_ece.py` | **Verified original** | Recomputes ECE/Brier/AUROC and LMM results. |
| Stats verifier | `scripts/verification/verify_stats.py` | **Verified original** | |
| Permutation audit | `scripts/robustness/permutation_audit.py` | **Verified original** | QID-level permutation, seed 20260622, 10,000 permutations. |
| Full validation pass | `scripts/robustness/final_validation_pass.py` | **Verified original** | LOMO, permutation, power, diagnostics. |
| LMM spec search | `scripts/robustness/find_lmm_spec.py`, `find_lmm_spec2.py` | **Verified original** | Model-specification exploration; retained for provenance. |
| GM-only dataset generator | `scripts/utilities/generate_gm_only_dataset.py` | **Verified original** | Reproduces the selection from Global-MMLU. |
| Pipeline validator | `scripts/utilities/validate_pipeline.py` | **Verified original** | Secret-scan + schema validation utility. |
| Metrics library | `src/afriknow_calib/metrics.py` | **Reconstructed** | Pure-function re-implementation of VCE parsing, accuracy, CHR, ECE, Brier, AUROC for testing; values cross-checked against `evidence/final/calibration_final.csv` and the raw CSV. |
| Dataset loader | `src/afriknow_calib/dataset.py` | **Reconstructed** | Load + validate the curated JSON (counts, balance, duplicates, schema). |
| Schema module | `src/afriknow_calib/schema.py` | **Verified original** | Copied verbatim from upstream `reproducibility/schema.py`. |

## Evidence and results

| Artifact | Path | Status | Notes |
|---|---|---|---|
| Final evidence set (13 files) | `results/reports/` | **Verified original** | H1/H3/CHR/calibration/LMM/LOMO/permutation/power/null-equivalence/diagnostics/category-sensitivity/source-control JSON+CSV evidence copied from upstream `evidence/final/`. |
| Canonical figures (5) | `results/figures/` | **Verified original** | `accuracy_by_region_v18.png`, `ece_comparison_v18.png`, `reliability_curves_v18.png`, `chr_by_tau_v18.png`, `h3_effect_sizes_v18.png`. |
| File manifest | `reproducibility/hashes/FINAL_FILE_MANIFEST.sha256` | **Verified original** | Upstream canonical hash list. |
| Audit trail | `reproducibility/run_logs/05_audit_trail.jsonl` | **Verified original** | Tamper-evident run log. |
| LMM/ECE verification log | `reproducibility/run_logs/afriknow-v18-lmm-ece-verification.log` | **Verified original** | |
| Prompt definitions | `reproducibility/prompts/prompts.py` | **Verified original** | Verbatim prompt templates (match manuscript Appendix B). |

## Manuscript

| Artifact | Path | Status | Notes |
|---|---|---|---|
| ARR LaTeX source | `paper/manuscript/main.tex` | **Verified original** | 558 lines; all numbers re-verified against raw CSV (see `docs/results/RESULTS.md`). |
| ARR PDF | `paper/manuscript/main_FINAL.pdf` | **Verified original** | Compiled final PDF. |
| Bibliography | `paper/manuscript/references.bib` | **Verified original** | 29 entries; each entry cross-checked in `docs/literature/REFERENCE_VERIFICATION.md`. |

## Missing artifacts (referenced upstream, not included here)

| Artifact | Status | Reason / action |
|---|---|---|
| `scripts/primary/01_power_analysis.py`, `02_sample_design.py` | **Missing** | Referenced by `run_pipeline.py` but not present in the upstream public layout (likely in archive). Power/MDE *outputs* are present (`results/reports/power_mde_final.json`). Do not fabricate; documented here. |
| Kaggle upload/notebook utilities | **Intentionally excluded** | Account-specific tooling (uploads to a personal Kaggle account); not needed for reproduction. Public Kaggle dataset/notebook links are documented in the README. |
| JUDGe workshop manuscript | **Intentionally excluded** | Separate paper/workshop artifact, not part of this repository's scope. |

## Requires further verification

| Artifact | Status | Notes |
|---|---|---|
| Literature entries (29) | **Requires further verification** | Titles/venues verified against manuscript appendix; DOIs and URLs being added in `docs/literature/REFERENCE_VERIFICATION.md` with source links; entries that cannot be verified are flagged there. |
| 2027 venue deadlines | **Requires further verification** | Official CFP pages checked where available; unannounced dates marked TBA in `docs/publication/VENUE_ANALYSIS_2027.md`. |

## Provenance chain

Every number in this repository traces as:

```
manuscript claim → paper/manuscript/main.tex
  → results/reports/*.json|csv (evidence files)
    → scripts/verification/*.py, scripts/robustness/*.py
      → data/raw/03_openrouter_outputs_v18_correct.csv (SHA-256 1915a77c…)
        → data/metadata/03_openrouter_manifest_v18.json + data/manifests/AFRIKNOW_V18_MANIFEST.yaml
```

## Non-goals / hygiene

- The upstream project's archive (superseded mixed-source experiment, quarantined invalid statistics) is **not** reproduced here; it is referenced for provenance only (`docs/results/RESULT_INTERPRETATION.md`). The upstream `afriknow-repo` with full history remains the archive of record.
- No API keys, tokens, or credentials are committed. `.env.example` documents the required variables.
- Internal review-history material is intentionally excluded from this public repository.
