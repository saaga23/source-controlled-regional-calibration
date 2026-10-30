# Dataset Card — AfriKnow GM-only v3

**Version:** v3 (GM-only core) · **Status:** frozen · **Items:** 180 · **License:** Apache-2.0 (derived from Global-MMLU)

## Summary

AfriKnow GM-only v3 is a 180-item, source-controlled multiple-choice benchmark slice derived from [Global-MMLU](https://huggingface.co/datasets/CohereLabs/Global-MMLU) (Singh et al., 2025). It contains exactly **90 items tagged Africa** and **90 items tagged Europe**, all drawn from the *same* benchmark (Global-MMLU English release), all at **medium difficulty**, all with four options, and all in **English**.

The dataset exists to answer one question: **when benchmark source is held constant, does a regional calibration gap persist?** Prior Africa-versus-Europe comparisons used different benchmark sources on each side (e.g., AfriMMLU for Africa, Global-MMLU or Wikidata for Europe), entangling region with source-specific difficulty, translation quality, and distractor design. This slice removes that entanglement by construction.

| Property | Value |
|---|---|
| Source benchmark | Global-MMLU (English), CohereLabs, Apache-2.0 |
| Upstream of source | MMLU (Hendrycks et al., 2021) |
| Items | 180 (unique IDs; no duplicates) |
| Regional composition | 90 Africa-tagged / 90 Europe-tagged |
| Difficulty filter | `medium` only (180/180) |
| Match level | `strict` (category + difficulty + cultural-sensitivity matching) for all 180 |
| Language | English (`en`, 180/180) |
| Cultural-sensitivity tags | 32 CS (culturally sensitive), 14 CA (culturally aware), 134 untagged (`-`) |
| Answer format | 4-option multiple choice (A–D) |
| Known flagged items | 12 content-label mismatches (6 Africa-tagged, 6 Europe-tagged US-history content), retained in main analysis with a leave-them-out robustness check |
| Hard ceiling | 180 items is the maximum feasible GM-only sample: the Africa-tagged Global-MMLU pool exhausts at 90 items after matching |
| Random seed (sampling) | 42 |

## What the data contains

Each item (`data/curated/02_gm_only_180_items.json`) has:

| Field | Meaning |
|---|---|
| `id` | Unique item ID (e.g., `GM-EU-prehistory-test-180`) |
| `source` | Provenance string (`Global-MMLU (ACL 2025)`) |
| `region` | `Africa` or `Europe` (Global-MMLU cultural region tag) |
| `group` | Matching group key (region + CS tag) |
| `cat` | MMLU subject category |
| `diff` | Difficulty band (`medium` — all items) |
| `q` | Question text |
| `ch` | List of four answer options |
| `a` | Index of the correct option (0–3) |
| `cs` | Cultural-sensitivity tag (`CS`, `CA`, or `-`) |
| `lang` | Language code (`en`) |
| `gm_only`, `gm_match_level` | Design flags confirming GM-only core and strict matching |

The evaluation outputs (`data/raw/03_openrouter_outputs_v18_correct.csv`) contain **no question text** — only item references, model metadata, predictions, confidence, tokens, cost, and timestamps — and are published alongside the curated items.

## Intended use

- Source-controlled regional audits of LLM accuracy and calibration (accuracy, Calibration Hit Rate, wrong-answer confidence, ECE, Brier, AUROC).
- Methodological demonstrations of source-confounding in regional evaluation.
- Not intended as a general-purpose capability benchmark: 180 medium-difficulty items cannot rank models on knowledge.

## Out-of-scope / prohibited uses

- Claims about model knowledge in any single African country or language community (the dataset aggregates Africa as one label; Africa contains 54 countries).
- Claims of model ranking or leaderboard use.
- Use of the 12 known content-label-mismatched items as ground truth about regional content without the documented robustness checks.

## Provenance and licensing

- Global-MMLU is released under **Apache-2.0** (confirmed on the [official dataset card](https://huggingface.co/datasets/CohereLabs/Global-MMLU), accessed 2026-10-30). Redistribution of the derived 180-item subset with attribution is permitted under those terms.
- Global-MMLU itself builds on MMLU (Hendrycks et al., 2021), which is MIT-licensed.
- This repository ships the full subset (question text and options) because the upstream license permits it. If you re-derive or extend the subset, keep the upstream attribution.
- The reconstruction path (in case upstream licensing ever changes) is documented in `docs/dataset/DATA_PROVENANCE.md`.

## Maintenance

- The dataset is frozen; no further item edits are planned.
- Corrections should be raised as repository issues; any change would produce a new version tag, never in-place edits.
- Contact and contribution: see the root README.
