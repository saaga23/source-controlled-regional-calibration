# Notebooks

No notebooks are shipped in this release.

The audit's analyses are committed as **scripts** (not notebooks) because the project's verification discipline requires deterministic, hash-logged runs (see `reproducibility/run_logs/05_audit_trail.jsonl`). A Kaggle notebook that reproduces the post-hoc analysis from the released data exists externally:

- Dataset: https://www.kaggle.com/datasets/abrahamsunday123/afriknow-v18-inputs
- Notebook: https://www.kaggle.com/code/abrahamsunday123/afriknow-phase-4b-v18-post-hoc-analysis

If you build a notebook against this repository, keep the frozen-data rule: notebooks must read `data/` and write only to `results/`.
