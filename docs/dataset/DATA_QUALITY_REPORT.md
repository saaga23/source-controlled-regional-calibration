# Data Quality Report — AfriKnow GM-only v3

All figures below were recomputed directly from `data/curated/02_gm_only_180_items.json` on 2026-10-30 (verification code in `tests/test_dataset.py`).

## Structural checks

| Check | Result | Status |
|---|---|---|
| Total items | 180 | PASS (expected 180) |
| Africa-tagged | 90 | PASS |
| Europe-tagged | 90 | PASS |
| Unique item IDs | 180/180 | PASS |
| Duplicate question texts (case/whitespace-normalized) | 0 | PASS |
| Missing values in any field | 0 fields, 0 items | PASS |
| All items 4-option MCQ | 180/180 | PASS |
| Gold answer index in range 0–3 | 180/180 | PASS |
| Difficulty band | `medium` 180/180 | PASS (by construction) |
| Language | `en` 180/180 | PASS |
| `gm_only` flag | true 180/180 | PASS |
| `gm_match_level` | `strict` 180/180 | PASS |

## Answer-index distribution (position-bias sanity check)

| Gold index | Count |
|---|---|
| A (0) | 44 |
| B (1) | 54 |
| C (2) | 45 |
| D (3) | 37 |

No degenerate position concentration (max share 30% on B).

## Category composition

| Category | Items |
|---|---|
| high_school_world_history | 86 |
| prehistory | 30 |
| high_school_us_history | 12 *(all 12 are the flagged content-label mismatches)* |
| global_facts | 12 |
| high_school_biology | 8 |
| high_school_geography | 8 |
| miscellaneous | 6 |
| nutrition | 4 |
| world_religions | 2 |
| virology | 2 |
| professional_law | 2 |
| moral_disputes | 2 |
| formal_logic | 2 |
| moral_scenarios | 2 |
| professional_accounting | 2 |

**Note on composition:** the set is history-heavy (world history + prehistory + US history = 128/180 ≈ 71%). This is a consequence of Global-MMLU's Africa/Europe tag distribution, not a sampling choice; it is a limitation for generalization beyond history-adjacent knowledge (recorded in `docs/results/KNOWN_LIMITATIONS.md`).

## Cultural-sensitivity composition (matched across arms)

| Tag | Africa | Europe |
|---|---|---|
| `CS` (culturally sensitive) | 16 | 16 |
| `CA` (culturally aware) | 7 | 7 |
| `-` (untagged) | 67 | 67 |

Composition is identical across arms by construction (strict matching).

## Flagged content-label mismatches (12 items)

All 12 items with `cat == high_school_us_history` (US-history content tagged Africa or Europe), split 6/6:

- Africa-tagged: `GM-AF-high_school_us_history-test-146`, `-155`, `-54`, `-105`, `-138`, `-117`
- Europe-tagged: `GM-EU-high_school_us_history-test-86`, `-70`, `-185`, `-32`, `-166`, `-186`

Treatment: retained in the primary analysis; leave-them-out robustness check reported in the manuscript (Appendix E) — excluding them moves pooled accuracy 86.5%→85.8% (χ²=1.18, p=.277) and every hypothesis test remains non-significant (H3 leave-out MWU p=.331).

## Raw evaluation-data quality (run quality)

From `data/raw/03_openrouter_outputs_v18_correct.csv` (verified 2026-10-30):

| Check | Result |
|---|---|
| Rows | 2,520 (1,260 items × models × 2 purposes) |
| Missing responses / parse failures | 0 (per run manifest and audit trail) |
| API failures | 0 |
| Regions | 1,260 / 1,260 (Africa / Europe) |
| Purposes | 1,260 greedy / 1,260 vce |
| Total tokens | 4,448,016 (4,435,416 input + 12,600 output) |
| Total cost | $0.6556 |
| Predictions consistent with greedy text | verified by `scripts/verification/verify_consistency.py` (71/71 checks PASS) |

## Residual quality risks (honest disclosure)

1. **Label noise:** 12 known content-label mismatches (handled as above).
2. **Region tags are Global-MMLU's**, produced by its annotation pipeline; this project adds one human content pass but does not re-annotate all 180 items blind.
3. **History-heavy composition** limits topical generalization.
4. **Medium-difficulty-only** band.
