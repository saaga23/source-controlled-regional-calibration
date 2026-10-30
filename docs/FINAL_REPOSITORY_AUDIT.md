# Final Repository Audit

**Audit date:** 2026-10-30 · **Auditor:** Kilo (automated + manual checks documented below) · **Auditee:** this repository at release v1.0.0

## 1. Scientific audit

| Check | Result | Evidence |
|---|---|---|
| README accurately represents the manuscript | PASS | All headline numbers cross-checked manuscript↔raw CSV; framing (nulls-not-equivalence; descriptive CHR; H3 chronology) matches manuscript §§Analysis Plan/Limitations |
| Reported results match raw outputs | PASS | `verify_v18_lmm_ece.py` (0 mismatches, Tables 2 & 4 reproduced to 3 decimals); `verify_consistency.py` (0 FAIL); `verify_table4.py` (exact); `permutation_audit.py` rerun (H1 .677, H3 .726 — exact) |
| All citations genuine | PARTIAL | 13/29 entries externally verified at source (2026-10-30); 16 PENDING recorded honestly in `docs/literature/REFERENCE_VERIFICATION.md` (API rate limits); one wrong arXiv ID guess rejected rather than published |
| Methodological explanations correct | PASS | Metric definitions match implementations (26 tests incl. hand-computed ECE/CHR fixtures) |
| Hypotheses & chronology accurate | PASS | One-sided pre-specified H3 reported two-sided — disclosed in manuscript, protocol, and README |
| Null results interpreted appropriately | PASS | MDE (d≈0.43) stated; no equivalence claim anywhere; "no evidence of" phrasing used consistently |
| Limitations acknowledged | PASS | 18 limitations enumerated (`docs/results/KNOWN_LIMITATIONS.md`) |
| Future recommendations supported | PASS | Each direction tied to a gap in `RESEARCH_GAP_ANALYSIS.md` with cost/risk accounting |

## 2. Data audit

| Check | Result | Evidence |
|---|---|---|
| Dataset counts correct | PASS | tests: 180 items, 90/90, 180 unique IDs, 0 duplicate texts, 0 missing values |
| Original source credited | PASS | Dataset card, CITATION.cff, README §19, LICENSE third-party notice |
| Redistribution permitted | PASS | Global-MMLU license = Apache-2.0 (official dataset card, accessed 2026-10-30); attribution provided; reconstruction path documented |
| Selection reproducible | PASS | `generate_gm_only_dataset.py` + construction doc + seeded freeze |
| Provenance clear | PASS | Chain-of-custody diagram in `DATA_PROVENANCE.md`; hashes pinned and test-enforced |
| Sensitive/restricted data excluded | PASS | No personal data; raw CSV contains no question text |

## 3. Engineering audit

| Check | Result | Evidence |
|---|---|---|
| Clean installation succeeds | PASS | `pip install -r requirements.txt` on Python 3.12.4 (Windows); no compiled deps beyond standard wheels |
| Scripts run | PASS | All Class-A scripts executed in this repository on 2026-10-30 (exit 0); logs in `results/reports/` |
| Tests pass | PASS | 26/26 (pytest 3.12.4; note: a broken local pytest plugin requires `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` on this machine — documented in README §14) |
| Paths portable | PASS | Hardcoded machine path removed from `permutation_audit.py` (refactor D10); scripts resolve roots via `__file__` |
| Dependencies documented | PASS | requirements.txt + pyproject.toml |
| Generated outputs traceable | PASS | audit trail (JSONL with hashes); verification logs committed |
| Secrets absent | PASS | test scan (credential-shaped regexes) + manual scan of scripts (only env-var reads); `.env` git-ignored |

## 4. Documentation audit — the "README 12-question test"

A reader using only the README should be able to answer:

| # | Question | Where the README answers it |
|---|---|---|
| 1 | What problem does this research address? | §1, §2 |
| 2 | Why is the problem important? | §2 (consequences + illustrative example, marked as illustration) |
| 3 | What gap does it investigate? | §5 |
| 4 | What dataset was used? | §6 table, §7 |
| 5 | Why constructed this way? | §7 (per-stage rationale; links) |
| 6 | Which models were evaluated? | §6 |
| 7 | What does VCE measure? | §6, §8 (defined at first use) |
| 8 | What analyses were conducted? | §8, §9 |
| 9 | What did the study find? | §10 (verified table) |
| 10 | What are the limitations? | §12 (full list linked) |
| 11 | How to reproduce? | §14, §15 (cost classes separated) |
| 12 | What should future researchers investigate? | §17 (prioritized, costed) |

## 5. Findings summary

- **Blocking issues:** none.
- **Non-blocking gaps (recorded in CHANGELOG/inventory):** 2 missing phase scripts (outputs present); 16 pending reference verifications; Kaggle notebook verification not re-run in this release (external link provided).
- **Audit completeness caveat:** this audit was performed by the same (AI-assisted) process that built the repository. An *independent* human pass over the README-12-question test is recommended before camera-ready.
