# Dataset Construction — AfriKnow GM-only v3

**Design goal:** a regional comparison in which **every non-region factor that varies is documented** — same benchmark, same language, same answer format, same difficulty band, matched subject and cultural-sensitivity composition.

## Why construction had to be source-controlled

Earlier Africa-versus-Europe evaluations (e.g., comparisons using AfriMMLU for Africa and Global-MMLU or Wikidata for Europe) entangle **region** with **benchmark source**. Any measured difference — accuracy or confidence — is then a mixture of (a) regional differences in model behavior and (b) source-specific differences in difficulty, translation quality, distractor design, and content selection. No statistical adjustment can fully separate those after the fact. The clean fix is at design time: take both regional arms from the *same* benchmark. Global-MMLU is (to our knowledge) the only MMLU-family benchmark that tags items by region on both sides, which makes a GM-only paired design feasible.

## Construction pipeline

### Step 1 — Obtain Global-MMLU (English)
- Source: [CohereLabs/Global-MMLU](https://huggingface.co/datasets/CohereLabs/Global-MMLU), `en` split (Apache-2.0).
- Rationale: English-only removes translation-quality differences between arms; the multilingual limitation is documented (single language).

### Step 2 — GM-only pool filter
- Keep only items with `region ∈ {Africa, Europe}` (Global-MMLU's cultural region tags).
- Keep only standard 4-option MCQ items.
- Effect: both arms now share the identical benchmark, distractor style, and labeling pipeline.

### Step 3 — Medium-difficulty filter
- Keep only `diff == "medium"`.
- Rationale: restricts to the difficulty band where models are neither at ceiling (easy) nor at floor (hard), which maximizes the information in accuracy *and* confidence comparisons.
- Result: all 180 retained items are `medium`.

### Step 4 — Strict regional matching
- Match keys: **(subject category, difficulty, cultural-sensitivity tag)**.
- The Africa-tagged pool surviving Steps 1–3 exhausts at **exactly 90 items** — this is the binding constraint of the whole design (the "180-item hard ceiling").
- The Europe arm is then filled with 90 items matched to that composition.
- Verified: `gm_match_level == "strict"` for 180/180 items; category and CS-tag compositions are identical across arms (see `DATA_QUALITY_REPORT.md`).

### Step 5 — Human content-label check
- Each item's Global-MMLU region tag was checked against its actual content.
- **12 items (6.7%)** flagged as content-label mismatches: US-history questions tagged Africa (6) or Europe (6). All 12 have `cat == high_school_us_history` in the curated file (IDs listed in `DATA_QUALITY_REPORT.md`).
- Decision (recorded in `DECISIONS.md` of the upstream project): keep them in the main analysis, add a leave-them-out robustness check. Excluding them changes no conclusion (manuscript Appendix E).

### Step 6 — Freeze and hash
- Final file: `data/curated/02_gm_only_180_items.json`, seed 42, `gm_only: true`.
- SHA-256 `fc07491b188ca2017b15ef93b6c1a9fd5066007362ea5c4e944f60443a52ef52`.

## Excluded items and why

| Exclusion | Rule | Consequence |
|---|---|---|
| Non-region-tagged Global-MMLU items | `region ∉ {Africa, Europe}` | Excluded by design (source-control requirement) |
| Easy and hard difficulty bands | `diff != "medium"` | Excluded by design (difficulty restriction; documented limitation) |
| Africa pool exhaustion | Pool is empty after 90 items | Sets the hard 180-item ceiling |
| 12 flagged label mismatches | Human content check | **Retained** with leave-out robustness check (not excluded from primary analysis) |

## Reproduction

1. Download Global-MMLU `en` from the official dataset card.
2. Run `python scripts/utilities/generate_gm_only_dataset.py` (documents the selection logic).
3. Validate: `pytest tests/test_dataset.py` checks counts (180), balance (90/90), difficulty (all medium), uniqueness (180 unique IDs, 0 duplicate question texts), and schema.
4. Confirm hashes against `reproducibility/hashes/FINAL_FILE_MANIFEST.sha256`.

## Relationship to the annotation sub-phase

`data/metadata/02_sample_design_manifest.json` records an intermediate 120-item (60/60) sample (2026-07-06) used for the human content-label review. It is provenance for the *annotation* step; the final frozen set is the 180-item file above.
