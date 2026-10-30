# Changelog

All notable changes to this repository. The dataset itself is frozen; any change to `data/` would create a new version, never in-place edits.

## [1.0.0] — 2026-10-30

### Added
- Initial public release of the source-controlled regional calibration audit.
- **Data:** AfriKnow GM-only v3 (180 items: 90 Africa-tagged / 90 Europe-tagged, Global-MMLU, Apache-2.0) + frozen raw model outputs (2,520 rows, 7 models, OpenRouter, $0.6556) + run manifests.
- **Code:** primary pipeline (runner, audit trail, orchestrator), verification suite (consistency 71/71, Table 2/4 reproduction), robustness suite (qid-level permutation with negative control, LMM spec search, full validation pass), tested reference implementations (`src/afriknow_calib/`).
- **Tests:** 26 tests covering dataset integrity, metric implementations, published-number reproduction, and secret scanning. All passing.
- **Documentation:** project inventory; literature review + verification matrix (13 externally verified references, 16 pending re-verification recorded honestly); dataset card/provenance/construction/quality/regional composition/dictionary; methodology, protocol, statistics, metric definitions, decision rationale; verified results, interpretation, robustness checks, known limitations; 2027 venue analysis (FAccT and ACL verified from official pages, others TBA) and submission roadmap; future research and roadmap.
- **Provenance:** every headline number re-verified against the raw CSV on 2026-10-30 (see `docs/results/RESULTS.md`); dataset hash matches the upstream canonical hash.
- Refactors (documented in `docs/methodology/DECISION_RATIONALE.md` D10): portable path resolution in `permutation_audit.py`; evidence output redirection in `verify_v18_lmm_ece.py`.

### Excluded (intentionally)
- Kaggle-account-specific upload utilities; internal review-history materials; the separate JUDGe workshop manuscript. Reasons in `docs/PROJECT_INVENTORY.md`.

### Known gaps (recorded, not hidden)
- Two pipeline phase scripts referenced by `run_pipeline.py` (`01_power_analysis.py`, `02_sample_design.py`) are not in this public layout; their *outputs* are (see inventory).
- 16 bibliography entries pending external re-verification (rate-limited at audit time) — `docs/literature/REFERENCE_VERIFICATION.md`.
