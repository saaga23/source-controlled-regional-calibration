# Archive Manifest — Superseded Artifacts (2026-07-18)

Purpose: isolate everything NOT tied to the single ground-truth run so no future
analysis can accidentally read a stale/superseded file and reintroduce a
hallucinated number. Nothing here was deleted; every file was **moved**, not removed.

## The ONE ground truth (kept in place, never archived)

- `annotator_pipeline/outputs/03_openrouter_outputs_v18_correct.csv`
  - SHA256: `1915a77c02ff1f08a87f8b2950f2e2c5e3041a353f7e26f456dd700543a6807d`
  - Byte-identical to Kaggle dataset `abrahamsunday123/afriknow-v18-inputs`.
  - 2,520 rows = 7 models x 180 items x 2 purposes (greedy, vce); 90 Africa + 90 Europe.
  - The paper (`paper/main.tex`) is built exclusively from this file.

## Provenance kept in place (defines the 180 items + power)

- `annotator_pipeline/outputs/02_gm_only_180_items.json` — the sampled GM-only items.
- `annotator_pipeline/outputs/01_power_analysis_manifest.json` + `01_power_analysis_report.md`.
- `annotator_pipeline/outputs/02_sample_design_manifest.json` + `02_sample_design_report.md`.
- `annotator_pipeline/outputs/03_openrouter_manifest_v18.json` — the v18 run manifest.
- `annotator_pipeline/outputs/05_audit_trail.jsonl`.

## Cloud reproducibility evidence (kept in place)

- `evidence/kaggle_run/` — Kaggle kernel output proving every paper number reproduces
  on Kaggle servers: log (all `MATCH`), `table2_ece_verified.csv`, `lmm_verified.json`.
- `evidence/table2_ece_verified.csv`, `evidence/confidence_lmm_verified.csv`, `evidence/summary.json` — local run.
- Kaggle kernel: `abrahamsunday123/afriknow-v18-lmm-ece-verification` (COMPLETE, converged).
- Verified scripts kept: `scripts/verify_v18_lmm_ece.py`, `scripts/verify_table4.py`,
  `scripts/build_verify_kernel.py`, `scripts/find_lmm_spec.py`, `scripts/find_lmm_spec2.py`.

## Verified analysis specifications (locked)

- **Table 2 ECE**: 10 equal-width bins on the `vce` column (already in [0,1]),
  per model, per region and pooled. Reproduces every cell.
- **Accuracy LMM**: `correct ~ region + model`, cluster-robust SE by `qid`.
- **Confidence LMM**: `logit(clip(vce, 0.001, 0.999)) ~ region + model + (1|qid)`,
  REML, `cg` optimizer. Reproduces Intercept 2.342, region[Europe] +0.152,
  Gemma +4.049, Llama +2.728, qid Var 1.297. **The clip bound is 0.001, not 0.01.**

## Correction applied this session

- Table 2, DeepSeek ECE(all): paper had `0.033` (a prior wrong "fix").
  Verified value from data = `0.053`. Restored to `0.053`, consistent with the
  discussion prose ("DeepSeek ECE 5.3%"). Confirmed on Kaggle.

## What was archived and why

### `outputs/` (35 files) — superseded run outputs
Mixed-source runs, pilots, resume/full checkpoints, the 8-model Kaggle-roster
outputs (claude-3-haiku / qwen3-235b roster, explicitly NOT the paper roster),
old model/cost histories, smoke logs, annotator interface intermediates.
None feed the paper.

### `scripts/` (28 files) — superseded analysis/runners
Mixed-source and pilot builders/runners, 817-item runners, v16->schema transform,
8-model/modal runners, merge/resume helpers, API smoke tests, and the stale
`annotator_pipeline/verify_paper_numbers.py` (it read `kaggle_8model_outputs.csv`
with wrong paper-claim comments — a hallucination source).

### `docs/` (1 file)
`MIXED_SOURCE_CONTRAST_DESIGN.md` — describes the superseded mixed-source design.

### `dirs/` (30 files across dirs) — temp/scratch directories
`kaggle_dataset_tmp/`, `kaggle_kernel_tmp/`, `kaggle_key_dataset_tmp/`,
`phase2_data/`, `scripts/full_817_outputs/`.

### root-level (5 files)
`kaggle_inference_8models.py`, `kaggle_inference_script.py`,
`kaggle_inference_8models.ipynb`, `kernel_logs.txt`, `afriknow-inference-code.zip`
(all tied to the superseded 8-model roster / old inference).

## Rule going forward

Any recomputation of a paper number must read ONLY
`annotator_pipeline/outputs/03_openrouter_outputs_v18_correct.csv`
(verify SHA256 above first) and use the locked specifications listed here.


---

## Thorough archive pass (2026-07-18, same day)

After the consistency check proved all 71 paper numbers reproduce from the single
ground-truth CSV, a second sweep archived everything NOT in the verification chain.

### Added this pass
- `paper/` leftovers: `main.tex.old`, `references.bib.old`, `references.bbl`,
  `main_ijcai26.pdf`, `ijcai26.sty`, `named.bst`, `acl_style/` (dup), `Dockerfile`,
  `main_sample.txt`, `preview_p01..12.png`, `_unused_figures/` (v17/v18 superseded figs).
- `docs_pre_fix/` — ALL `docs/*.md` pre-fix audit reports (DEEP_AUDIT_FINDINGS, FIXES_APPLIED,
  PAPER_QUALITY_AUDIT, COMPILATION_REPORT, AI_DETECTION_REPORT, MASTER_PRE_SUBMISSION_REVIEW,
  MANUSCRIPT_HANDOFF). These describe pre-fix states; superseded by the verified run.
- Old Kaggle upload tooling: `kaggle_upload/`, `kaggle_upload_notebook/`,
  `kaggle_dataset_metadata.json`, `data/` (the v18 dataset is already uploaded; re-upload
  tooling is not needed for verification).

### What REMAINS LIVE and WHY (verification + current deliverables only)
- Ground truth + provenance: `annotator_pipeline/outputs/03_openrouter_outputs_v18_correct.csv`,
  `02_gm_only_180_items.json`, `01_power_analysis_*`, `02_sample_design_*`, `03_openrouter_manifest_v18.json`, `05_audit_trail.jsonl`.
- Verify scripts: `scripts/consistency_check.py` (single-place 71-check report),
  `scripts/verify_table4.py`, `scripts/verify_v18_lmm_ece.py`, `scripts/find_lmm_spec*.py`,
  `scripts/build_verify_kernel.py`, `scripts/validate_pipeline.py`.
- Kaggle evidence kernel source: `kaggle_kernel_verify/`.
- Evidence: `evidence/consistency_check_report.md`, `evidence/consistency_check.json`, `evidence/kaggle_run/*`.
- Paper build: `paper/main.tex`, `acl.sty`, `acl_natbib.bst`, `references.bib`, `responsible_nlp_checklist.md`, `paper/v18_analysis_figures/`.
- Deliverables: `afriknow_overleaf.zip`, `recommendation_emails.docx`, `rec_letter_targets.md`, `MENTOR_MESSAGE.md`, `memory.md`, `README.md`, `ETHICS.md`, `CITATION.cff`, `REMEDIATION*.md`, `POWER_ANALYSIS.md`, `requirements.txt`.

### Final state
- 153 files archived (0 deleted).
- Local `scripts/consistency_check.py` => 71/71 PASS, SHA256 matches.
- Kaggle kernel `abrahamsunday123/afriknow-v18-lmm-ece-verification` => COMPLETE, all MATCH, same values.
- Single source of truth confirmed; no stale file can be read by verification scripts.
