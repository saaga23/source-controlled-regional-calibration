# Repository Release Report

**Release:** v1.0.0 · **Date:** 2026-10-30 · **Repository:** `source-controlled-regional-calibration`

## Status classification of deliverables

| Deliverable | Status |
|---|---|
| Public GitHub repository | **Completed** (URL + verification below) |
| Complete README (22 required sections) | **Completed** — all sections present; README-only comprehension test in `FINAL_REPOSITORY_AUDIT.md` §4 |
| Repository tree | **Completed** (README §13) |
| Literature review + related-work matrix + gap analysis | **Completed** with honesty caveat: 13/29 references externally verified; 16 PENDING recorded (`docs/literature/REFERENCE_VERIFICATION.md`) |
| Dataset card + provenance + construction + quality + composition + dictionary | **Completed and verified** (all counts recomputed from the frozen files; hash-enforced by tests) |
| Methodology documentation (5 docs) | **Completed** (metric fixtures tested; statistics reproduced) |
| Verified results documentation | **Completed** — every headline number recomputed from raw CSV on 2026-10-30, zero mismatches |
| Reproduction guide | **Completed** — Class A (no cost) fully exercised in this release; Class B (fresh inference) documented but **not exercised** (requires spending; not authorized) |
| Future research roadmap | **Completed** (prioritized, costed, authorization-gated) |
| 2027 venue analysis | **Completed** — FAccT 2027 and ACL 2027 verified from official CFP pages; other venues TBA |
| Test report | **Completed** — 26/26 pass (includes published-number reproduction and secret scanning) |
| Security audit | **Completed** — no secrets in tree or history; `.env` ignored; scanner test in suite |
| Licensing audit | **Completed** — MIT (code) + Apache-2.0 provenance chain (dataset) documented with access-dated sources |
| Commit history summary | **Completed** — 8+ logical commits (below) |
| SHA-256 manifest | **Completed** — `MANIFEST_SHA256.txt` (114 files) |
| Final repository audit | **Completed** (`FINAL_REPOSITORY_AUDIT.md`) — one caveat: same-process audit; independent human pass recommended |

## Commit history (logical sequence)

| Commit | Content |
|---|---|
| `cfbf064` | Initial repository and documentation structure |
| `32620ca` | Dataset provenance and construction (frozen data + manifests) |
| `197cb18` | Experimental source code and tested reference implementations |
| `735e436` | Analysis pipeline, verification/robustness scripts, reproducibility artifacts |
| `d49ae35` | Frozen evidence files and canonical figures |
| `18096c1` | Literature investigation and 2027 venue analysis |
| `5764f24` | Full documentation (dataset, methodology, results, audits) |
| (final) | Archived mixed-source contrast data + robustness rerun outputs + manifest + release report |

## Verification performed in this release (all 2026-10-30, this machine)

1. `python -m pytest tests/ -q` → **26 passed** (dataset integrity incl. canonical hashes; metric fixtures; published-number reproduction: accuracy 551/630 & 539/630, wrong-VCE 0.761/0.832, d=−0.317, CHR 0.105/0.136 ratio 0.769, pooled ECE 0.048/Brier 0.114/AUROC 0.679, cost $0.6556, 4,448,016 tokens; secret scan).
2. `python scripts/verification/verify_v18_lmm_ece.py` → exit 0, **0 mismatches** vs published Tables 2 & 4.
3. `python scripts/verification/verify_consistency.py` → exit 0, **0 FAIL** (71 checks).
4. `python scripts/verification/verify_table4.py` → exit 0, exact coefficient match.
5. `python scripts/robustness/permutation_audit.py` → exit 0; qid-level permutation p-values exact (H1 .677, H3 .726); row-level negative control reproduced.
6. `python scripts/robustness/final_validation_pass.py` → exit 0; LOMO, power, diagnostics, category sensitivity; outputs in `results/reports/final_validation_pass/`.

## What was NOT done (honest)

- **No fresh inference** (Class B): requires API spend, not authorized.
- **16 bibliography entries** pending external re-verification (rate-limited APIs); details carried from the manuscript's bib and flagged.
- **No independent human review** of the README-12-question test (this audit is same-process; recommendation recorded).
- **No claim of submission/review status** anywhere in the repository.

## Remaining issues / recommended next actions

1. Re-run reference verification when rate limits allow; move PENDING → VERIFIED or correct the bib.
2. Owner decision: optional prompt-sensitivity run (~cents) before the ARR Jan 4, 2027 deadline (roadmap item 3).
3. Independent human read of README §1–§12 before submission.
4. Verify the Kaggle notebook still runs against the released data (external resource).
5. At camera-ready: finalize author metadata in `CITATION.cff` and BibTeX.
