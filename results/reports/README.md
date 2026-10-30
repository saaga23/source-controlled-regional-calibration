# Evidence Final Directory — Canonical Evidence Files

This directory contains the consolidated, canonical evidence files for the AfriKnow v18 final submission. Each file is derived from validated outputs and is the single authoritative source for its claim.

## Files

### `h1_accuracy_final.json`
- **Source:** Extracted from `evidence/consistency_check.json` (71/71 PASS)
- **Content:** Africa 87.5% vs Europe 85.6%, χ²=0.823, p=0.364, qid permutation p=0.677 (10k perm)
- **Purpose:** Primary evidence for H1 (no accuracy gap)

### `chr_final.json`
- **Source:** Extracted from `evidence/consistency_check.json` (CHR values)
- **Content:** Africa 10.5%, Europe 13.6%, ratio 0.77
- **Purpose:** Evidence for H2 (confident-hit rate, descriptive)

### `h3_wrong_vce_final.json`
- **Source:** Extracted from `evidence/consistency_check.json` (H3 values)
- **Content:** Africa 0.761 vs Europe 0.832, d=-0.317, 95% CI [-0.621, -0.014], MWU p=0.234, qid perm p=0.726
- **Purpose:** Primary evidence for H3 (no Africa-overconfidence)

### `calibration_final.csv`
- **Source:** `evidence/table2_ece_verified.csv`
- **Content:** Per-model ECE, Brier, AUROC values verified against paper claims
- **Purpose:** Pooled calibration metrics

### `mixed_effects_final.json`
- **Source:** `evidence/consistency_check.json` + `evidence/confidence_lmm_verified.csv`
- **Content:** Accuracy GLM (β_Europe=-0.165, p=.646) and Confidence LMM (β_Europe=+0.152, p=.421, qid Var=1.297)
- **Purpose:** Mixed-effects model evidence

### `permutation_qid_final.json`
- **Source:** `archive/final_validation_outputs_intermediate/permutation_test_results.json`
- **Content:** Qid-level permutation test results (10k permutations, seed 20260622)
- **Purpose:** Distribution-free inference for H1 and H3

### `permutation_audit_final.json`
- **Source:** `archive/final_validation_outputs_intermediate/permutation_audit_results.json`
- **Content:** Corrected permutation audit (row-level vs qid-level comparison)
- **Purpose:** Validates permutation test implementation

### `leave_one_model_out_final.csv`
- **Source:** `archive/final_validation_outputs_intermediate/leave_one_model_out_results.csv`
- **Content:** Robustness check removing each of 7 models in turn
- **Purpose:** Model-robustness evidence

### `power_mde_final.json`
- **Source:** `reports/final/POWER_ANALYSIS.md`
- **Content:** MDE=0.433 at 80% power; d=0.30 power=0.492; d=0.50 power=0.899
- **Purpose:** Power analysis evidence

### `model_diagnostics_final.json`
- **Source:** `archive/final_validation_outputs_intermediate/model_diagnostics.json`
- **Content:** LMM diagnostics (ICC=0.41, qid Var=1.297, Levene p=0.54, n=1260)
- **Purpose:** Model assumption checks

### `null_equivalence_final.json`
- **Source:** `archive/final_validation_outputs_intermediate/null_equivalence_interpretation.json`
- **Content:** Null effect interpretation with MDE and power
- **Purpose:** Frames null result as underpowered equivalence test

### `source_control_descriptive_final.json`
- **Source:** `archive/final_validation_outputs_intermediate/source_control_descriptive.json`
- **Content:** Mixed-source vs source-controlled descriptive comparison
- **Purpose:** Supports source-confounding narrative

### `category_sensitivity_final.csv`
- **Source:** `evidence/final/category_sensitivity_final.csv`
- **Content:** Per-category accuracy and H3 sensitivity breakdown
- **Purpose:** Content-label mismatch robustness check

## Provenance

All files in this directory are the **canonical evidence** for the AfriKnow v18 submission. Original validated outputs remain in their original locations:
- `evidence/consistency_check.json` — master 71/71 consistency check
- `evidence/table2_ece_verified.csv` — per-model calibration values
- `evidence/confidence_lmm_verified.csv` — LMM confidence coefficients
- `evidence/summary.json` — summary statistics

Intermediate validation outputs have been archived to `archive/final_validation_outputs_intermediate/` for provenance.
